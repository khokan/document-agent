"""
🗄️ ChromaDB service wrapper for vector database operations.
"""

import asyncio
import chromadb
from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config


class ChromaDBService:
    """Service to manage ChromaDB collection operations, document storage, and queries."""

    def __init__(self):
        self.persist_dir = config.chroma_persist_directory
        self.collection_name = config.chroma_collection_name
        self.distance_metric = config.chroma_distance_metric

        # Create persistent client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Load/create collection with selected distance metric
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": self.distance_metric}
        )
        logger.info(
            f"[VECTOR STORE] Connected to ChromaDB at '{self.persist_dir}' "
            f"(collection='{self.collection_name}', metric='{self.distance_metric}')"
        )

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

    async def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """
        Add text chunks with their dense embeddings and metadata to ChromaDB.

        Args:
            chunks: List of chunk dicts containing 'chunk_id', 'text', 'metadata'
            embeddings: List of embedding vectors corresponding to chunks
        """
        if not chunks or not embeddings:
            return

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
