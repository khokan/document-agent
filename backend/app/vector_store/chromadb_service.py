"""
🗄️ ChromaDB service wrapper for vector database operations.
"""

import asyncio
import chromadb
from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config


class IndexCompatibilityError(RuntimeError):
    """Raised when vectors belong to a different embedding profile."""


class ChromaDBService:
    """Service to manage ChromaDB collection operations, document storage, and queries."""

    def __init__(self):
        self.persist_dir = config.chroma_persist_directory
        self.collection_name = config.chroma_collection_name
        self.distance_metric = config.chroma_distance_metric
        self.embedding_fingerprint = config.embedding_profile_fingerprint
        self.embedding_dimension = config.embedding_dimension

        # Create persistent client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Load/create collection with selected distance metric
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata=self._expected_metadata("ready")
        )
        self._initialize_empty_collection()
        logger.info(
            f"[VECTOR STORE] Connected to ChromaDB at '{self.persist_dir}' "
            f"(collection='{self.collection_name}', metric='{self.distance_metric}')"
        )

    def _expected_metadata(self, status: str) -> Dict[str, Any]:
        return {
            "hnsw:space": self.distance_metric,
            "embedding_fingerprint": self.embedding_fingerprint,
            "embedding_dimension": self.embedding_dimension,
            "index_status": status,
        }

    def _initialize_empty_collection(self) -> None:
        """Adopt only genuinely empty legacy collections; never overwrite indexed metadata."""
        metadata = self.collection.metadata or {}
        if self.collection.count() == 0 and metadata.get("embedding_fingerprint") != self.embedding_fingerprint:
            # Exclude hnsw:space — ChromaDB forbids changing it after creation.
            update = {k: v for k, v in self._expected_metadata("ready").items() if k != "hnsw:space"}
            self.collection.modify(metadata=update)

    def index_status(self) -> Dict[str, Any]:
        metadata = self.collection.metadata or {}
        compatible = (
            metadata.get("index_status") == "ready"
            and metadata.get("embedding_fingerprint") == self.embedding_fingerprint
            and metadata.get("embedding_dimension") == self.embedding_dimension
        )
        return {
            "compatible": compatible,
            "reindex_required": not compatible,
            "active_embedding_profile": self.embedding_fingerprint,
            "stored_embedding_profile": metadata.get("embedding_fingerprint"),
            "embedding_dimension": self.embedding_dimension,
            "stored_embedding_dimension": metadata.get("embedding_dimension"),
        }

    def require_ready(self) -> None:
        if not self.index_status()["compatible"]:
            raise IndexCompatibilityError("The active embedding profile differs from the index; run confirmed reindexing first.")

    async def reset_for_reindex(self) -> None:
        """Destructively reset only this configured collection for the maintenance command."""
        await asyncio.to_thread(self.client.delete_collection, self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name, metadata=self._expected_metadata("reindexing")
        )

    async def mark_reindex_complete(self) -> None:
        # Exclude hnsw:space — ChromaDB forbids changing it after creation.
        update = {k: v for k, v in self._expected_metadata("ready").items() if k != "hnsw:space"}
        await asyncio.to_thread(self.collection.modify, metadata=update)

    def _normalize_score(self, distance: float) -> float:
        """
        Normalize distance metric to a similarity score between 0.0 and 1.0.

        - Cosine: distance = 1 - similarity => similarity = 1 - distance
        - L2: distance = sum((a-b)^2) => similarity = 1 / (1 + distance)
        - IP (Inner Product): distance = 1 - similarity => similarity = 1 - distance
        """
        if self.distance_metric in ("cosine", "ip"):
            similarity = 1.0 - distance
        elif self.distance_metric == "l2":
            similarity = 1.0 / (1.0 + distance)
        else:
            similarity = 1.0 - distance  # Default fallback

        # Ensure range [0.0, 1.0]
        return max(0.0, min(1.0, similarity))

    async def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]], allow_reindex: bool = False) -> None:
        """
        Add text chunks with their dense embeddings and metadata to ChromaDB.

        Args:
            chunks: List of chunk dicts containing 'chunk_id', 'text', 'metadata'
            embeddings: List of embedding vectors corresponding to chunks
        """
        if not chunks or not embeddings:
            return
        if not allow_reindex:
            self.require_ready()
        if len(embeddings) != len(chunks) or any(len(vector) != self.embedding_dimension for vector in embeddings):
            raise ValueError("Embedding provider returned vectors incompatible with the configured dimension")

        ids = [c["chunk_id"] for c in chunks]
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        # Chroma DB adds synchronously; run in thread pool to prevent event loop blocking
        await asyncio.to_thread(
            self.collection.add,
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )
        logger.info(f"[OK] Added {len(chunks)} chunks to vector store collection '{self.collection_name}'")

    async def query_similarity(
        self, 
        query_embedding: List[float], 
        top_k: int = 5, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in vector store.

        Args:
            query_embedding: Target vector to search against
            top_k: Number of nearest matches to return
            filters: Key-value metadata filtering parameters

        Returns:
            List of matching records with similarity scores
        """
        self.require_ready()
        # Convert Pydantic/None filters to ChromaDB format
        where_clause = {}
        if filters:
            for k, v in filters.items():
                if v is not None:
                    where_clause[k] = v

        # Run query in thread pool to avoid blocking
        results = await asyncio.to_thread(
            self.collection.query,
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause if where_clause else None
        )

        formatted_results = []
        if not results or not results["ids"] or not results["ids"][0]:
            return formatted_results

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):
            score = self._normalize_score(distances[i])
            formatted_results.append({
                "chunk_id": ids[i],
                "text": documents[i],
                "metadata": metadatas[i],
                "score": score
            })

        # Sort by similarity score descending
        formatted_results.sort(key=lambda x: x["score"], reverse=True)
        return formatted_results

    async def delete_document_chunks(self, document_id: str) -> None:
        """Delete all chunks belonging to a document ID."""
        await asyncio.to_thread(
            self.collection.delete,
            where={"document_id": document_id}
        )
        logger.info(f"[OK] Deleted all chunks for document '{document_id}' from vector store")

    async def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        count = await asyncio.to_thread(self.collection.count)
        return {
            "count": count,
            "collection_name": self.collection_name,
        }

    async def get_all_document_ids(self) -> List[str]:
        """Get all unique document IDs currently stored in the vector database."""
        try:
            # Get all items with limit to avoid memory issues
            all_results = await asyncio.to_thread(
                self.collection.get,
                limit=100000  # Adjust based on your needs
            )
            
            if not all_results or not all_results.get("metadatas"):
                return []
            
            # Extract unique document_ids from metadata
            document_ids = set()
            for metadata in all_results["metadatas"]:
                if metadata and "document_id" in metadata:
                    document_ids.add(metadata["document_id"])
            
            return list(document_ids)
        except Exception as e:
            logger.error(f"[ERR] Failed to get document IDs from vector store: {str(e)}")
            return []

    async def get_document_metadata(self, document_id: str) -> Dict[str, Any]:
        """
        Get aggregated metadata for a specific document.
        
        Returns document info including filename, chunk count, page info, etc.
        """
        try:
            # Get all chunks for this document
            all_results = await asyncio.to_thread(
                self.collection.get,
                where={"document_id": document_id},
                limit=100000
            )
            
            if not all_results or not all_results.get("metadatas") or not all_results["metadatas"]:
                return {}
            
            metadatas = all_results["metadatas"]
            chunk_count = len(all_results["ids"])
            
            # Aggregate metadata from chunks
            first_metadata = metadatas[0]
            unique_pages = set()
            
            for metadata in metadatas:
                if metadata and "page_number" in metadata:
                    unique_pages.add(metadata["page_number"])
            
            return {
                "document_id": document_id,
                "filename": first_metadata.get("filename", "unknown"),
                "original_filename": first_metadata.get("original_filename", first_metadata.get("filename", "unknown")),
                "chunk_count": chunk_count,
                "page_count": len(unique_pages) if unique_pages else 1,
                "status": "indexed",
            }
        except Exception as e:
            logger.error(f"[ERR] Failed to get document metadata: {str(e)}")
            return {}
