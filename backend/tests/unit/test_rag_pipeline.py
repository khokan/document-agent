"""
🧪 Unit tests for the RAGPipeline orchestrator.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from app.rag.pipeline import RAGPipeline
from app.rag.ranker import ResultRanker


class TestRAGPipeline(unittest.IsolatedAsyncioTestCase):
    """Test coordinating retriever, ranker, generator and output schema formatting."""

    async def test_pipeline_query(self):
        # 1. Setup mocks
        mock_retriever = MagicMock()
        mock_retriever.retrieve = AsyncMock(return_value=[
            {
                "chunk_id": "doc1_p1_c0",
                "text": "Acme Inc reported $10M revenue.",
                "score": 0.92,
                "metadata": {
                    "document_id": "doc1",
                    "filename": "acme_report.pdf",
                    "page_number": 1
                }
            }
        ])

        mock_generator = MagicMock()
        mock_generator.generate_response = AsyncMock(return_value="Acme Inc made 10 million dollars in revenue.")

        ranker = ResultRanker(strategy="score_based")

        # 2. Instantiate pipeline (no cache for testing)
        pipeline = RAGPipeline(
            retriever=mock_retriever,
            generator=mock_generator,
            ranker=ranker,
            cache=None
        )

        # 3. Execute
        result = await pipeline.query(question="What was Acme's revenue?")

        # 4. Assertions
        self.assertEqual(result["answer"], "Acme Inc made 10 million dollars in revenue.")
        self.assertEqual(result["query"], "What was Acme's revenue?")
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(result["sources"][0]["document_id"], "doc1")
        self.assertEqual(result["sources"][0]["filename"], "acme_report.pdf")
        self.assertEqual(result["sources"][0]["page"], 1)
        self.assertEqual(result["sources"][0]["score"], 0.92)
        self.assertEqual(result["sources"][0]["text"], "Acme Inc reported $10M revenue.")
        self.assertTrue(result["response_time_ms"] > 0)
        self.assertIn("retrieval_time_ms", result)
        self.assertIn("generation_time_ms", result)
        self.assertEqual(result["cached"], False)

        # Verify calls
        mock_retriever.retrieve.assert_called_once_with(
            query="What was Acme's revenue?",
            top_k=None,
            filters=None,
            score_threshold=None
        )
        mock_generator.generate_response.assert_called_once()

    async def test_pipeline_chat(self):
        mock_retriever = MagicMock()
        mock_retriever.retrieve = AsyncMock(return_value=[
            {
                "chunk_id": "doc1_p2_c0",
                "text": "Revenue grew 15% YoY.",
                "score": 0.88,
                "metadata": {
                    "document_id": "doc1",
                    "filename": "report.pdf",
                    "page_number": 2
                }
            }
        ])

        mock_generator = MagicMock()
        mock_generator.generate_response = AsyncMock(return_value="Revenue grew by 15%.")

        pipeline = RAGPipeline(
            retriever=mock_retriever,
            generator=mock_generator,
            ranker=ResultRanker(),
            cache=None
        )

        history = [
            {"role": "user", "content": "What was the revenue?"},
            {"role": "assistant", "content": "Revenue was $10M."},
        ]

        result = await pipeline.chat(
            question="How did it compare?",
            history=history
        )

        self.assertEqual(result["answer"], "Revenue grew by 15%.")
        self.assertEqual(result["query"], "How did it compare?")
        self.assertTrue(result["response_time_ms"] > 0)
        mock_generator.generate_response.assert_called_once()

    async def test_pipeline_summarize(self):
        mock_retriever = MagicMock()
        mock_retriever.retrieve = AsyncMock(return_value=[
            {
                "chunk_id": "doc1_p1_c0",
                "text": "Introduction to the report.",
                "score": 0.5,
                "metadata": {"document_id": "doc1", "page_number": 1, "chunk_number": 0}
            },
            {
                "chunk_id": "doc1_p2_c1",
                "text": "Key findings section.",
                "score": 0.5,
                "metadata": {"document_id": "doc1", "page_number": 2, "chunk_number": 1}
            }
        ])

        mock_generator = MagicMock()
        mock_generator.generate_summary = AsyncMock(return_value="This report covers introduction and findings.")

        pipeline = RAGPipeline(
            retriever=mock_retriever,
            generator=mock_generator,
            ranker=ResultRanker(),
            cache=None
        )

        result = await pipeline.summarize(document_id="doc1")

        self.assertIn("introduction and findings", result["summary"])
        self.assertEqual(result["document_id"], "doc1")
        self.assertEqual(result["chunks_used"], 2)
        self.assertTrue(result["response_time_ms"] > 0)
