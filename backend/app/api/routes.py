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

router = APIRouter(prefix="/documents", tags=["Documents"])

# In-memory document store (replace with database in production)
DOCUMENTS_STORE = {}


async def _process_and_store_document(document_id: str, filename: str, page_texts: dict) -> int:
    """Helper to chunk, embed, and store document in vector database."""
    # 1. Chunk document
    splitter = ChunkSplitter()
    doc_metadata = {"filename": filename}
    chunks = splitter.split_document(document_id, page_texts, doc_metadata)
    
    if chunks:
        # 2. Generate embeddings
        texts = [c["text"] for c in chunks]
        embeddings = await embedding_service.get_embeddings(texts)
        
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

        # Generate document ID
        document_id = f"{Path(file.filename).stem}_{uuid.uuid4().hex[:8]}"

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

        # Store document metadata
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
        }

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

        logger.info(f"[INFO] Listed {len(documents)} documents")

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
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
async def delete_document(document_id: str):
    """
    Delete a document and all its chunks from the system.

    Args:
        document_id: ID of document to delete

    Raises:
        HTTPException: If document not found
    """
    try:
        if document_id not in DOCUMENTS_STORE:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")

        doc_info = DOCUMENTS_STORE[document_id]

        # Delete file from disk
        file_path = Path(doc_info.get("file_path", ""))
        if file_path.exists():
            os.remove(file_path)
            logger.info(f"[INFO] Deleted file: {file_path}")

        # Delete chunks from ChromaDB
        await vector_service.delete_document_chunks(document_id)

        # Remove from store
        del DOCUMENTS_STORE[document_id]

        logger.info(f"[OK] Document deleted: {document_id}")

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
        if document_id not in DOCUMENTS_STORE:
            raise HTTPException(status_code=404, detail=f"Document not found: {document_id}")

        doc_info = DOCUMENTS_STORE[document_id]
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
        total_docs = len(DOCUMENTS_STORE)
        total_chunks = sum(doc.get("chunk_count", 0) for doc in DOCUMENTS_STORE.values())

        # Calculate total size
        total_size_mb = 0.0
        for doc_info in DOCUMENTS_STORE.values():
            file_path = Path(doc_info.get("file_path", ""))
            if file_path.exists():
                total_size_mb += file_path.stat().st_size / (1024 * 1024)

        logger.info(f"[INFO] System stats: {total_docs} docs, {total_chunks} chunks")

        return SystemStats(
            total_documents=total_docs,
            total_chunks=total_chunks,
            total_size_mb=round(total_size_mb, 2),
            embedding_dimension=config.embedding_dimension,
            collection_name=config.chroma_collection_name,
        )

    except Exception as e:
        logger.error(f"[ERR] Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
