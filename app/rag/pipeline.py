"""
🚀 RAG pipeline orchestrator linking query retrieval and text response generation.
"""

import time
from typing import Dict, Any, List, Optional
from app.utils.logger import logger
from app.rag.retriever import Retriever
from app.rag.generator import Generator


class RAGPipeline:
    """Orchestrates query semantic search retrieval and context-aware response generation."""

    def __init__(self, retriever: Retriever, generator: Generator):
        self.retriever = retriever
        self.generator = generator
        logger.info("[RAG] RAGPipeline initialized successfully")

    async def query(
        self, 
        question: str, 
        filters: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Execute full RAG pipeline: retrieve relevant context then generate answer.

        Args:
            question: Question/search query
            filters: Key-value metadata filtering dictionary
            top_k: Maximum chunks to retrieve
            score_threshold: Minimum similarity threshold

        Returns:
            Dict containing answer, source references, query, and response_time_ms
        """
        start_time = time.perf_counter()

        # 1. Retrieve relevant chunks
        context_chunks = await self.retriever.retrieve(
            query=question,
            top_k=top_k,
            filters=filters,
            score_threshold=score_threshold
        )

        # 2. Generate response using LLM
        answer = await self.generator.generate_response(question, context_chunks)

        # 3. Format sources using metadata from chunks
        sources = []
        for chunk in context_chunks:
            metadata = chunk["metadata"]
            sources.append({
                "document_id": metadata.get("document_id", "unknown"),
                "filename": metadata.get("original_filename", metadata.get("filename", "unknown")),
                "page": metadata.get("page_number", 1),
                "score": chunk["score"],
                "text": chunk["text"]
            })

        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000.0

        logger.info(f"[OK] RAG pipeline query completed in {response_time_ms:.1f}ms")

        return {
            "answer": answer,
            "sources": sources,
            "query": question,
            "response_time_ms": round(response_time_ms, 2)
        }
