"""
🚀 RAG pipeline orchestrator linking query retrieval, ranking, and text response generation.
"""

import time
from typing import Dict, Any, List, Optional
from app.utils.logger import logger
from app.rag.retriever import Retriever
from app.rag.ranker import ResultRanker
from app.rag.generator import Generator
from app.rag.cache import ResponseCache


class RAGPipeline:
    """Orchestrates query semantic search retrieval, ranking, caching, and context-aware response generation."""

    def __init__(
        self,
        retriever: Retriever,
        generator: Generator,
        ranker: Optional[ResultRanker] = None,
        cache: Optional[ResponseCache] = None
    ):
        self.retriever = retriever
        self.generator = generator
        self.ranker = ranker or ResultRanker()
        self.cache = cache
        logger.info("[RAG] RAGPipeline initialized successfully")

    async def query(
        self, 
        question: str, 
        filters: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Execute full RAG pipeline: retrieve → rank → generate answer.

        Args:
            question: Question/search query
            filters: Key-value metadata filtering dictionary
            top_k: Maximum chunks to retrieve
            score_threshold: Minimum similarity threshold

        Returns:
            Dict containing answer, source references, query, timing breakdown
        """
        total_start = time.perf_counter()

        # 0. Check cache first
        if self.cache:
            cached = self.cache.get(question, filters)
            if cached is not None:
                cached["cached"] = True
                return cached

        # 1. Retrieve relevant chunks
        retrieval_start = time.perf_counter()
        context_chunks = await self.retriever.retrieve(
            query=question,
            top_k=top_k,
            filters=filters,
            score_threshold=score_threshold
        )
        retrieval_ms = (time.perf_counter() - retrieval_start) * 1000.0

        # 2. Rank retrieved results
        ranked_chunks = self.ranker.rank(context_chunks)

        # 3. Generate response using LLM
        generation_start = time.perf_counter()
        answer = await self.generator.generate_response(question, ranked_chunks)
        generation_ms = (time.perf_counter() - generation_start) * 1000.0

        # 4. Format sources using metadata from chunks
        sources = self._format_sources(ranked_chunks)

        total_ms = (time.perf_counter() - total_start) * 1000.0

        logger.info(
            f"[OK] RAG pipeline completed in {total_ms:.1f}ms "
            f"(retrieval={retrieval_ms:.1f}ms, generation={generation_ms:.1f}ms)"
        )

        result = {
            "answer": answer,
            "sources": sources,
            "query": question,
            "response_time_ms": round(total_ms, 2),
            "retrieval_time_ms": round(retrieval_ms, 2),
            "generation_time_ms": round(generation_ms, 2),
            "cached": False,
        }

        # 5. Store in cache
        if self.cache:
            self.cache.set(question, result, filters)

        return result

    async def chat(
        self,
        question: str,
        history: List[Dict[str, str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Execute multi-turn chat with conversation history.

        Args:
            question: Current user message
            history: List of previous messages [{"role": "user"/"assistant", "content": "..."}]
            filters: Key-value metadata filtering dictionary
            top_k: Maximum chunks to retrieve
            score_threshold: Minimum similarity threshold

        Returns:
            Dict containing answer, sources, query, and timing
        """
        total_start = time.perf_counter()

        # 1. Retrieve relevant chunks
        retrieval_start = time.perf_counter()
        context_chunks = await self.retriever.retrieve(
            query=question,
            top_k=top_k,
            filters=filters,
            score_threshold=score_threshold
        )
        retrieval_ms = (time.perf_counter() - retrieval_start) * 1000.0

        # 2. Rank retrieved results
        ranked_chunks = self.ranker.rank(context_chunks)

        # 3. Generate response with history
        generation_start = time.perf_counter()
        answer = await self.generator.generate_response(
            question,
            ranked_chunks,
            history=history
        )
        generation_ms = (time.perf_counter() - generation_start) * 1000.0

        # 4. Format sources
        sources = self._format_sources(ranked_chunks)

        total_ms = (time.perf_counter() - total_start) * 1000.0

        logger.info(
            f"[OK] RAG chat completed in {total_ms:.1f}ms "
            f"(retrieval={retrieval_ms:.1f}ms, generation={generation_ms:.1f}ms)"
        )

        return {
            "answer": answer,
            "sources": sources,
            "query": question,
            "response_time_ms": round(total_ms, 2),
            "retrieval_time_ms": round(retrieval_ms, 2),
            "generation_time_ms": round(generation_ms, 2),
        }

    async def summarize(
        self,
        document_id: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 20
    ) -> Dict[str, Any]:
        """
        Summarize a document using its indexed chunks.

        Args:
            document_id: Document to summarize
            filters: Additional metadata filters
            top_k: Number of chunks to include in summary context

        Returns:
            Dict containing summary, sources, and timing
        """
        total_start = time.perf_counter()

        # Build filters to target specific document
        doc_filters = {"document_id": document_id}
        if filters:
            doc_filters.update(filters)

        # Retrieve document chunks (use a dummy query to get all chunks from that doc)
        retrieval_start = time.perf_counter()
        context_chunks = await self.retriever.retrieve(
            query="summarize the document",
            top_k=top_k,
            filters=doc_filters,
            score_threshold=0.0  # Get all chunks for the document
        )
        retrieval_ms = (time.perf_counter() - retrieval_start) * 1000.0

        # Sort by page number for coherent summary
        context_chunks.sort(
            key=lambda x: (
                x.get("metadata", {}).get("page_number", 0),
                x.get("metadata", {}).get("chunk_number", 0)
            )
        )

        # Generate summary
        generation_start = time.perf_counter()
        summary = await self.generator.generate_summary(context_chunks)
        generation_ms = (time.perf_counter() - generation_start) * 1000.0

        total_ms = (time.perf_counter() - total_start) * 1000.0

        logger.info(
            f"[OK] Document summary completed for '{document_id}' in {total_ms:.1f}ms"
        )

        return {
            "summary": summary,
            "document_id": document_id,
            "chunks_used": len(context_chunks),
            "response_time_ms": round(total_ms, 2),
            "retrieval_time_ms": round(retrieval_ms, 2),
            "generation_time_ms": round(generation_ms, 2),
        }

    def _format_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format chunk metadata into source citation format."""
        sources = []
        for chunk in chunks:
            metadata = chunk.get("metadata", {})
            sources.append({
                "document_id": metadata.get("document_id", "unknown"),
                "filename": metadata.get("original_filename", metadata.get("filename", "unknown")),
                "page": metadata.get("page_number", 1),
                "score": chunk.get("score", 0.0),
                "text": chunk.get("text", "")
            })
        return sources
