"""
FastAPI routes for PDF document management and search.

Implements endpoints for:
- PDF upload
- Document listing
- Document deletion
- Document reindexing
- System statistics
"""

import os
import uuid
import hashlib
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models import (
    DocumentInfo,
    DocumentListResponse,
    DocumentUploadResponse,
    ErrorResponse,
    SystemStats,
)
from app.pdf import PDFExtractor, TextCleaner
from app.utils import FileValidator, config, logger

from app.api.deps import vector_service, embedding_service
from app.chunking.splitter import ChunkSplitter
from app.services.document_catalog import document_catalog

router = APIRouter(prefix="/documents", tags=["Documents"])

# In-memory document store (replace with database in production)
DOCUMENTS_STORE = {}

# Track file hashes to detect duplicate uploads
FILE_HASH_MAP = {}  # Maps file_hash -> document_id


def _calculate_file_hash(file_bytes: bytes) -> str:
    """Calculate SHA256 hash of file contents."""
    return hashlib.sha256(file_bytes).hexdigest()


def _check_duplicate_upload(file_hash: str) -> str | None:
    """Check if file has already been uploaded. Returns existing document_id if found."""
    return FILE_HASH_MAP.get(file_hash)


async def _process_and_store_document(document_id: str, filename: str, page_texts: dict) -> int:
    """Helper to chunk, embed, and store document in vector database."""
    # 1. Chunk document
    splitter = ChunkSplitter()
    doc_metadata = {"filename": filename}
    chunks = splitter.split_document(document_id, page_texts, doc_metadata)
    
    if chunks:
        # 2. Generate embeddings
        texts = [c["text"] for c in chunks]
        vector_service.require_ready()
        embeddings = await embedding_service.aembed_documents(texts)
        
        # 3. Add to vector store
        await vector_service.add_chunks(chunks, embeddings)
        
        # 4. Save embedding cache if dirty
        from app.embeddings.cache import embedding_cache
        embedding_cache.save()
        
        return len(chunks)
    return 0



@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def upload_pdf(file: UploadFile = File(..., description="PDF file to upload")):
    """
    Upload a PDF document for processing.

    The endpoint:
    1. Validates the uploaded file
    2. Saves the file to storage
    3. Extracts and cleans text
    4. Prepares for chunking and embedding

    Args:
        file: PDF file from form data

    Returns:
        DocumentUploadResponse with document ID and status

    Raises:
        HTTPException: If validation fails
    """
    temp_file_path = None

    try:
        # Validate filename
        is_valid, error_msg = FileValidator.validate_filename(file.filename)
        if not is_valid:
            logger.error(f"[ERR] Upload rejected: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Create temporary file path
        temp_dir = Path(config.temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_file_path = temp_dir / f"temp_{uuid.uuid4()}.pdf"

        # Save uploaded file temporarily
        logger.info(f"[INFO] Saving uploaded file: {file.filename}")
        contents = await file.read()

        with open(temp_file_path, "wb") as f:
            f.write(contents)

        # Calculate file hash for deduplication
        file_hash = _calculate_file_hash(contents)
        
        # Check if this file has already been uploaded
        existing_record = document_catalog.get_by_hash(file_hash)
        existing_doc_id = existing_record.document_id if existing_record else _check_duplicate_upload(file_hash)
        if existing_doc_id:
            logger.warning(f"[WARN] Duplicate file detected. Already indexed as: {existing_doc_id}")
            existing_doc = DOCUMENTS_STORE.get(existing_doc_id)
            if not existing_doc and existing_record:
                existing_doc = {
                    "filename": existing_record.filename, "upload_date": existing_record.upload_date,
                    "chunk_count": existing_record.chunk_count,
                }
            if existing_doc:
                logger.info(f"[OK] Returning existing document: {existing_doc_id}")
                return DocumentUploadResponse(
                    document_id=existing_doc_id,
                    filename=existing_doc["filename"],
                    upload_date=existing_doc["upload_date"],
                    status="indexed",
                    chunk_count=existing_doc["chunk_count"],
                )

        # Validate PDF
        is_valid, error_msg = FileValidator.validate_pdf_file(str(temp_file_path))
        if not is_valid:
            raise HTTPException(status_code=422, detail=error_msg)

        # Extract text from PDF
        logger.info(f"[INFO] Extracting text from {file.filename}")
        success, page_texts = PDFExtractor.extract_text_by_page(str(temp_file_path))
        if not success or not page_texts:
            raise HTTPException(status_code=422, detail="Failed to extract text from PDF")

        # Clean extracted text
        logger.info("[INFO] Cleaning extracted text")
        cleaned_pages = TextCleaner.clean_pages(page_texts)
        if not cleaned_pages:
            raise HTTPException(status_code=422, detail="No text content found in PDF")

        # Generate document ID using filename only (no UUID) to support re-uploads
        document_id = Path(file.filename).stem

        # If document already exists, delete old chunks first
        if document_id in DOCUMENTS_STORE or document_catalog.get(document_id):
            logger.info(f"[INFO] Document '{document_id}' already exists. Removing old chunks...")
            try:
                await vector_service.delete_document_chunks(document_id)
                logger.info(f"[OK] Deleted old chunks for document: {document_id}")
            except Exception as e:
                logger.error(f"[ERR] Failed to delete old chunks: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to re-index document: {str(e)}")

        # Save to permanent storage
        pdf_dir = Path(config.upload_dir)
        pdf_dir.mkdir(parents=True, exist_ok=True)
        final_path = pdf_dir / f"{document_id}.pdf"

        with open(temp_file_path, "rb") as src:
            with open(final_path, "wb") as dst:
                dst.write(src.read())

        # Process chunking, embedding, and storage
        logger.info(f"[INFO] Processing and storing document: {document_id}")
        chunk_count = await _process_and_store_document(document_id, file.filename, cleaned_pages)

        # Store document metadata and file hash
        DOCUMENTS_STORE[document_id] = {
            "document_id": document_id,
            "filename": file.filename,
            "original_filename": file.filename,
            "upload_date": datetime.utcnow(),
            "status": "indexed",
            "page_count": len(cleaned_pages),
            "chunk_count": chunk_count,
            "file_path": str(final_path),
            "page_texts": cleaned_pages,
            "file_hash": file_hash,
        }
        
        # Store file hash mapping for future duplicate detection
        FILE_HASH_MAP[file_hash] = document_id
        document_catalog.upsert(
            document_id=document_id, filename=file.filename, file_path=str(final_path), file_hash=file_hash,
            page_count=len(cleaned_pages), chunk_count=chunk_count,
        )

        logger.info(f"[OK] Document uploaded and indexed successfully: {document_id} ({chunk_count} chunks)")

        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            upload_date=datetime.utcnow(),
            status="indexed",
            chunk_count=chunk_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERR] Unexpected error during upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    finally:
        # Clean up temporary file
        if temp_file_path and Path(temp_file_path).exists():
            try:
                os.remove(temp_file_path)
                logger.debug(f"[INFO] Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"[WARN] Could not clean up temp file: {str(e)}")


@router.get(
    "",
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_documents():
    """
    List all uploaded and indexed documents.

    Returns:
        DocumentListResponse with list of documents and statistics
    """
    try:
        documents = []
        total_chunks = 0

        catalogued = document_catalog.list()
        if catalogued:
            DOCUMENTS_STORE.update({
                record.document_id: {
                    "document_id": record.document_id, "filename": record.filename,
                    "upload_date": record.upload_date, "status": record.status,
                    "chunk_count": record.chunk_count, "page_count": record.page_count,
                    "file_path": record.file_path, "file_hash": record.file_hash,
                    "embedding_fingerprint": record.embedding_fingerprint,
                } for record in catalogued
            })
        for doc_id, doc_info in DOCUMENTS_STORE.items():
            documents.append(
                DocumentInfo(
                    document_id=doc_id,
                    filename=doc_info["filename"],
                    upload_date=doc_info["upload_date"],
                    status=doc_info["status"],
                    chunk_count=doc_info.get("chunk_count", 0),
                    page_count=doc_info.get("page_count", 0),
                )
            )
            total_chunks += doc_info.get("chunk_count", 0)

        doc_ids = list(DOCUMENTS_STORE.keys())
        logger.info(f"[INFO] Listed {len(documents)} documents: {doc_ids}")

        return DocumentListResponse(
            documents=documents,
            total_count=len(documents),
            total_chunks=total_chunks,
        )

    except Exception as e:
        logger.error(f"[ERR] Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
async def delete_document(document_id: str):
    """
    Delete a document and all its chunks from the system.

    Args:
        document_id: ID of document to delete

    Returns:
        Status message confirming deletion

    Raises:
        HTTPException: If document not found or ID is invalid
    """
    try:
        # Validate document_id
        if not document_id or document_id == "undefined" or document_id.strip() == "":
            logger.warning(f"[WARN] Invalid document_id provided: '{document_id}'")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid document ID: '{document_id}'. Document ID cannot be empty or undefined."
            )
        
        catalog_record = document_catalog.get(document_id)
        if document_id not in DOCUMENTS_STORE and not catalog_record:
            logger.warning(f"[WARN] Attempt to delete non-existent document: {document_id}")
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")

        doc_info = DOCUMENTS_STORE.get(document_id) or {
            "file_path": catalog_record.file_path, "file_hash": catalog_record.file_hash,
        }

        # Delete file from disk
        file_path = Path(doc_info.get("file_path", ""))
        if file_path.exists():
            os.remove(file_path)
            logger.info(f"[INFO] Deleted file: {file_path}")

        # Delete chunks from ChromaDB
        await vector_service.delete_document_chunks(document_id)
        
        # Remove file hash mapping
        file_hash = doc_info.get("file_hash")
        if file_hash and file_hash in FILE_HASH_MAP:
            del FILE_HASH_MAP[file_hash]
            logger.debug(f"[INFO] Removed file hash mapping: {file_hash}")

        # Remove from store
        DOCUMENTS_STORE.pop(document_id, None)
        document_catalog.delete(document_id)

        logger.info(f"[OK] Document deleted: {document_id}")
        
        return {
            "status": "success",
            "message": f"Document '{document_id}' has been successfully deleted",
            "document_id": document_id,
            "deleted_at": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERR] Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")


@router.post(
    "/reindex/{document_id}",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
)
async def reindex_document(document_id: str):
    """
    Reindex a document by re-processing and re-embedding it.

    Args:
        document_id: ID of document to reindex

    Raises:
        HTTPException: If document not found
    """
    try:
        record = document_catalog.get(document_id)
        if document_id not in DOCUMENTS_STORE and not record:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")

        if record and record.embedding_fingerprint != config.embedding_profile_fingerprint:
            raise HTTPException(status_code=409, detail="Document uses a different embedding profile; run confirmed full reindexing.")
        doc_info = DOCUMENTS_STORE.get(document_id) or {
            "filename": record.filename, "file_path": record.file_path,
            "upload_date": record.upload_date, "file_hash": record.file_hash,
        }
        file_path = doc_info.get("file_path", "")

        if not Path(file_path).exists():
            raise HTTPException(status_code=404, detail="Document file not found on disk")

        # Re-extract text
        logger.info(f"[INFO] Reindexing document: {document_id}")
        success, page_texts = PDFExtractor.extract_text_by_page(file_path)
        if not success:
            raise HTTPException(status_code=422, detail="Failed to extract text during reindex")

        # Re-clean text
        cleaned_pages = TextCleaner.clean_pages(page_texts)

        # Update vector store
        await vector_service.delete_document_chunks(document_id)
        chunk_count = await _process_and_store_document(document_id, doc_info["filename"], cleaned_pages)

        # Update document
        doc_info["page_texts"] = cleaned_pages
        doc_info["page_count"] = len(cleaned_pages)
        doc_info["chunk_count"] = chunk_count
        doc_info["status"] = "reindexed"
        document_catalog.upsert(
            document_id=document_id, filename=doc_info["filename"], file_path=file_path,
            file_hash=doc_info.get("file_hash", ""), page_count=len(cleaned_pages),
            chunk_count=chunk_count, status="reindexed",
        )

        logger.info(f"[OK] Document reindexed: {document_id} ({chunk_count} chunks)")

        return DocumentUploadResponse(
            document_id=document_id,
            filename=doc_info["filename"],
            upload_date=doc_info["upload_date"],
            status="reindexed",
            chunk_count=chunk_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERR] Error reindexing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reindex failed: {str(e)}")


@router.get(
    "/stats",
    response_model=SystemStats,
    status_code=status.HTTP_200_OK,
)
async def get_system_stats():
    """
    Get system-wide statistics.

    Returns:
        SystemStats with document counts and storage information
    """
    try:
        # Count from both in-memory store and vector store
        catalogued = document_catalog.list()
        total_docs = len(catalogued) if catalogued else len(DOCUMENTS_STORE)
        total_chunks = sum(record.chunk_count for record in catalogued) if catalogued else sum(doc.get("chunk_count", 0) for doc in DOCUMENTS_STORE.values())

        # Get actual counts from vector store for comparison
        vector_store_stats = await vector_service.get_stats()
        vector_doc_ids = await vector_service.get_all_document_ids()
        
        actual_chunks_in_db = vector_store_stats.get("count", 0)
        actual_docs_in_db = len(vector_doc_ids)

        # Calculate total size from disk
        total_size_mb = 0.0
        size_records = catalogued or []
        for doc_info in (size_records or DOCUMENTS_STORE.values()):
            file_path = Path(doc_info.file_path if size_records else doc_info.get("file_path", ""))
            if file_path.exists():
                total_size_mb += file_path.stat().st_size / (1024 * 1024)

        # Log if there's a mismatch
        if total_docs != actual_docs_in_db or total_chunks != actual_chunks_in_db:
            logger.warning(
                f"[WARN] Document store mismatch detected:\n"
                f"  Tracked: {total_docs} docs, {total_chunks} chunks\n"
                f"  Vector DB: {actual_docs_in_db} docs, {actual_chunks_in_db} chunks"
            )
        else:
            logger.info(f"[INFO] System stats: {total_docs} docs, {total_chunks} chunks (synced)")

        index_state = vector_service.index_status()
        return SystemStats(
            total_documents=total_docs,
            total_chunks=total_chunks,
            total_size_mb=round(total_size_mb, 2),
            embedding_dimension=config.embedding_dimension,
            collection_name=config.chroma_collection_name,
            active_ai_profile=config.active_ai_profile,
            chat_provider=config.chat_settings.get("provider"),
            chat_model=config.chat_settings.get("model"),
            embedding_provider=config.embedding_settings.get("provider"),
            index_compatible=index_state["compatible"],
            reindex_required=index_state["reindex_required"],
        )

    except Exception as e:
        logger.error(f"[ERR] Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


async def _cleanup_orphaned_chunks():
    """
    Cleanup orphaned chunks in vector store that don't belong to any document in DOCUMENTS_STORE.
    This handles cases where documents were deleted but chunks remain in the database.
    """
    try:
        vector_doc_ids = await vector_service.get_all_document_ids()
        tracked_doc_ids = set(DOCUMENTS_STORE.keys())
        orphaned_doc_ids = set(vector_doc_ids) - tracked_doc_ids
        
        if orphaned_doc_ids:
            logger.warning(f"[WARN] Found {len(orphaned_doc_ids)} orphaned document(s) in vector store: {orphaned_doc_ids}")
            for orphaned_id in orphaned_doc_ids:
                logger.info(f"[INFO] Deleting orphaned chunks for document: {orphaned_id}")
                await vector_service.delete_document_chunks(orphaned_id)
            logger.info(f"[OK] Cleaned up {len(orphaned_doc_ids)} orphaned document(s)")
        else:
            logger.debug("[OK] No orphaned documents found in vector store")
    except Exception as e:
        logger.error(f"[ERR] Failed to cleanup orphaned chunks: {str(e)}")


async def _sync_documents_from_vector_store():
    """
    Sync DOCUMENTS_STORE with actual vector store data on startup.
    This ensures consistency after app restarts or crashes.
    
    - Loads all documents from vector store into memory
    - Cleans up orphaned chunks
    - Restores document metadata
    """
    try:
        logger.info("[INFO] Starting document store sync from vector store...")
        
        # Get all document IDs from vector store
        vector_doc_ids = await vector_service.get_all_document_ids()
        
        if not vector_doc_ids:
            logger.info("[OK] No documents found in vector store")
            return
        
        logger.info(f"[INFO] Found {len(vector_doc_ids)} document(s) in vector store")
        
        # Load metadata for each document into DOCUMENTS_STORE
        loaded_count = 0
        for doc_id in vector_doc_ids:
            try:
                metadata = await vector_service.get_document_metadata(doc_id)
                if metadata:
                    # Store in memory for fast access
                    DOCUMENTS_STORE[doc_id] = {
                        "document_id": doc_id,
                        "filename": metadata.get("filename", "unknown"),
                        "original_filename": metadata.get("original_filename", metadata.get("filename", "unknown")),
                        "upload_date": datetime.utcnow(),  # Use current time (actual date is not stored in chunks)
                        "status": metadata.get("status", "indexed"),
                        "chunk_count": metadata.get("chunk_count", 0),
                        "page_count": metadata.get("page_count", 0),
                        "file_path": str(Path(config.upload_dir) / f"{doc_id}.pdf"),
                    }
                    loaded_count += 1
                    logger.debug(f"[DEBUG] Loaded document: {doc_id} ({metadata.get('chunk_count', 0)} chunks)")
            except Exception as e:
                logger.error(f"[ERR] Failed to load document {doc_id}: {str(e)}")
        
        logger.info(f"[OK] Loaded {loaded_count} document(s) into memory")
        
        # Cleanup orphaned chunks
        await _cleanup_orphaned_chunks()
        logger.info("[OK] Document store synchronized with vector store")
        
    except Exception as e:
        logger.error(f"[ERR] Failed to sync document store: {str(e)}")


@router.post(
    "/cleanup",
    status_code=status.HTTP_200_OK,
    responses={500: {"model": ErrorResponse}},
)
async def cleanup_orphaned_documents():
    """
    Cleanup orphaned chunks in vector store.
    
    This endpoint removes any chunks that don't belong to documents in the tracked list.
    Useful for syncing the system after crashes or manual deletions.
    
    Returns:
        Status message with number of cleaned up documents
    """
    try:
        vector_doc_ids = await vector_service.get_all_document_ids()
        tracked_doc_ids = set(DOCUMENTS_STORE.keys())
        orphaned_doc_ids = set(vector_doc_ids) - tracked_doc_ids
        
        if orphaned_doc_ids:
            logger.warning(f"[WARN] Cleaning up {len(orphaned_doc_ids)} orphaned document(s): {orphaned_doc_ids}")
            for orphaned_id in orphaned_doc_ids:
                await vector_service.delete_document_chunks(orphaned_id)
            logger.info(f"[OK] Cleaned up {len(orphaned_doc_ids)} orphaned document(s)")
            
            return {
                "status": "success",
                "message": f"Cleaned up {len(orphaned_doc_ids)} orphaned document(s)",
                "orphaned_documents": list(orphaned_doc_ids),
            }
        else:
            return {
                "status": "success",
                "message": "No orphaned documents found",
                "orphaned_documents": [],
            }
    
    except Exception as e:
        logger.error(f"[ERR] Cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def document_store_health():
    """
    Check the health and consistency of the document store.
    
    Returns:
        Detailed health status including any mismatches between tracked and actual documents
    """
    try:
        tracked_doc_ids = set(DOCUMENTS_STORE.keys())
        vector_doc_ids = set(await vector_service.get_all_document_ids())
        
        tracked_chunks = sum(doc.get("chunk_count", 0) for doc in DOCUMENTS_STORE.values())
        vector_stats = await vector_service.get_stats()
        vector_chunks = vector_stats.get("count", 0)
        
        orphaned_docs = vector_doc_ids - tracked_doc_ids
        missing_docs = tracked_doc_ids - vector_doc_ids
        
        is_healthy = (tracked_doc_ids == vector_doc_ids) and (tracked_chunks == vector_chunks)
        
        status_msg = "healthy" if is_healthy else "inconsistent"
        
        logger.info(
            f"[{status_msg.upper()}] Document store health:\n"
            f"  Tracked: {len(tracked_doc_ids)} docs, {tracked_chunks} chunks\n"
            f"  Vector DB: {len(vector_doc_ids)} docs, {vector_chunks} chunks"
        )
        
        return {
            "status": status_msg,
            "tracked_documents": len(tracked_doc_ids),
            "tracked_chunks": tracked_chunks,
            "vector_db_documents": len(vector_doc_ids),
            "vector_db_chunks": vector_chunks,
            "orphaned_documents": list(orphaned_docs),
            "missing_documents": list(missing_docs),
            "is_consistent": is_healthy,
            "needs_cleanup": len(orphaned_docs) > 0,
            "tracked_doc_ids": list(tracked_doc_ids),
            "vector_doc_ids": list(vector_doc_ids),
        }
    
    except Exception as e:
        logger.error(f"[ERR] Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
