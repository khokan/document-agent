"""
🧪 Unit tests for the RAGPipeline orchestrator.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from app.rag.pipeline import RAGPipeline


class TestRAGPipeline(unittest.IsolatedAsyncioTestCase):
    """Test coordinating retriever and generator and output schema formatting."""

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

        # 2. Instantiate pipeline
        pipeline = RAGPipeline(retriever=mock_retriever, generator=mock_generator)

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

        # Verify calls
        mock_retriever.retrieve.assert_called_once_with(
            query="What was Acme's revenue?",
            top_k=None,
            filters=None,
            score_threshold=None
        )
        mock_generator.generate_response.assert_called_once()
