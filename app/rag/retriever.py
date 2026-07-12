"""
🔍 Retrieval logic to query similarity matches from the vector database.
"""

from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config
from app.embeddings.ollama_service import OllamaEmbeddingService
from app.vector_store.chromadb_service import ChromaDBService


class Retriever:
    """Retrieves relevant text chunks from the vector database based on semantic query matching."""

    def __init__(self, embedding_service: OllamaEmbeddingService, vector_service: ChromaDBService):
        self.embeddings = embedding_service
        self.vector_store = vector_service
        self.default_k = config.rag_retriever_k
        self.default_threshold = config.rag_retriever_score_threshold

        logger.info(f"[RAG] Retriever initialized (default_k={self.default_k}, threshold={self.default_threshold})")

    async def retrieve(
        self, 
        query: str, 
        top_k: Optional[int] = None, 
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Embed the query and retrieve relevant document chunks from ChromaDB.

        Args:
            query: Question/search query
            top_k: Maximum chunks to retrieve (falls back to config.yaml value)
            filters: Key-value metadata filtering dictionary
            score_threshold: Minimum similarity threshold (0.0 to 1.0)

        Returns:
            List of matching records filtered by threshold
        """
        k = top_k or self.default_k
        threshold = score_threshold if score_threshold is not None else self.default_threshold

        # 1. Embed query
        logger.info(f"[RAG] Retrieving context for query: '{query}'")
        query_vector = await self.embeddings.get_embedding(query)

        # 2. Query similarity from vector store
        raw_matches = await self.vector_store.query_similarity(
            query_embedding=query_vector,
            top_k=k,
            filters=filters
        )

        # 3. Filter by similarity threshold
        filtered_matches = []
        for match in raw_matches:
            if match["score"] >= threshold:
                # Enrich metadata with original_filename if missing
                metadata = match.get("metadata", {})
                if "original_filename" not in metadata and "filename" in metadata:
                    metadata["original_filename"] = metadata["filename"]
                filtered_matches.append(match)
            else:
                logger.debug(
                    f"[RAG] Skip chunk '{match['chunk_id']}' with score {match['score']:.3f} "
                    f"(threshold={threshold:.3f})"
                )

        logger.info(f"[OK] Retrieved {len(filtered_matches)} chunks above threshold {threshold:.2f}")
        return filtered_matches
