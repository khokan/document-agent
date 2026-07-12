"""
🧪 Integration tests for RAG chat and summarize API endpoints.
"""

import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app


class TestRAGChatAPI(unittest.TestCase):
    """Verify that POST /rag/chat runs multi-turn conversation pipeline."""

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.rag.RAGPipeline.chat", new_callable=AsyncMock)
    def test_chat_endpoint_success(self, mock_chat):
        mock_chat.return_value = {
            "answer": "Revenue grew by 15% year-over-year.",
            "sources": [
                {
                    "document_id": "acme_2026",
                    "filename": "acme_report.pdf",
                    "page": 5,
                    "score": 0.91,
                    "text": "Year-over-year revenue growth was 15%."
                }
            ],
            "query": "How does that compare to last year?",
            "response_time_ms": 1200.0,
            "retrieval_time_ms": 200.0,
            "generation_time_ms": 1000.0,
        }

        payload = {
            "message": "How does that compare to last year?",
            "history": [
                {"role": "user", "content": "What was Acme's revenue?"},
                {"role": "assistant", "content": "Acme's revenue was $10M."},
            ],
            "top_k": 5
        }

        response = self.client.post("/rag/chat", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["answer"], "Revenue grew by 15% year-over-year.")
        self.assertEqual(data["query"], "How does that compare to last year?")
        self.assertEqual(len(data["sources"]), 1)
        self.assertEqual(data["sources"][0]["document_id"], "acme_2026")
        self.assertEqual(data["sources"][0]["page"], 5)
        self.assertGreater(data["response_time_ms"], 0)

    def test_chat_endpoint_empty_message_rejected(self):
        payload = {
            "message": "",
            "history": [],
            "top_k": 5
        }
        response = self.client.post("/rag/chat", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_chat_endpoint_message_too_long(self):
        payload = {
            "message": "x" * 2001,
            "history": [],
            "top_k": 5
        }
        response = self.client.post("/rag/chat", json=payload)
        self.assertEqual(response.status_code, 422)


class TestRAGSummarizeAPI(unittest.TestCase):
    """Verify that POST /rag/summarize generates document summary."""

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.rag.RAGPipeline.summarize", new_callable=AsyncMock)
    def test_summarize_endpoint_success(self, mock_summarize):
        mock_summarize.return_value = {
            "summary": "The annual report highlights 15% revenue growth driven by market expansion.",
            "document_id": "acme_2026_abc123",
            "chunks_used": 12,
            "response_time_ms": 3200.0,
            "retrieval_time_ms": 150.0,
            "generation_time_ms": 3050.0,
        }

        payload = {
            "document_id": "acme_2026_abc123",
            "max_chunks": 20
        }

        response = self.client.post("/rag/summarize", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("revenue growth", data["summary"])
        self.assertEqual(data["document_id"], "acme_2026_abc123")
        self.assertEqual(data["chunks_used"], 12)
        self.assertGreater(data["response_time_ms"], 0)

    def test_summarize_endpoint_missing_document_id(self):
        payload = {"max_chunks": 20}
        response = self.client.post("/rag/summarize", json=payload)
        self.assertEqual(response.status_code, 422)


class TestRAGQueryEnhancements(unittest.TestCase):
    """Verify Sprint 3 enhancements to POST /rag/query."""

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.rag.RAGPipeline.query", new_callable=AsyncMock)
    def test_query_with_score_threshold(self, mock_query):
        mock_query.return_value = {
            "answer": "Revenue was $10M.",
            "sources": [],
            "query": "revenue?",
            "response_time_ms": 100.0,
            "retrieval_time_ms": 50.0,
            "generation_time_ms": 50.0,
            "cached": False,
        }

        payload = {
            "question": "What was the revenue?",
            "top_k": 3,
            "score_threshold": 0.5
        }

        response = self.client.post("/rag/query", json=payload)

        self.assertEqual(response.status_code, 200)
        mock_query.assert_called_once()
        call_kwargs = mock_query.call_args
        self.assertEqual(call_kwargs.kwargs.get("score_threshold") or call_kwargs[1].get("score_threshold"), 0.5)

    @patch("app.api.rag.RAGPipeline.query", new_callable=AsyncMock)
    def test_query_response_includes_timing(self, mock_query):
        mock_query.return_value = {
            "answer": "Test answer.",
            "sources": [],
            "query": "test?",
            "response_time_ms": 500.0,
            "retrieval_time_ms": 200.0,
            "generation_time_ms": 300.0,
            "cached": False,
        }

        payload = {"question": "test?", "top_k": 3}
        response = self.client.post("/rag/query", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("retrieval_time_ms", data)
        self.assertIn("generation_time_ms", data)
        self.assertIn("cached", data)
        self.assertEqual(data["cached"], False)

    @patch("app.api.rag.RAGPipeline.query", new_callable=AsyncMock)
    def test_query_cached_response(self, mock_query):
        mock_query.return_value = {
            "answer": "Cached answer.",
            "sources": [],
            "query": "cached?",
            "response_time_ms": 1.0,
            "retrieval_time_ms": 0.0,
            "generation_time_ms": 0.0,
            "cached": True,
        }

        payload = {"question": "cached query?", "top_k": 3}
        response = self.client.post("/rag/query", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["cached"], True)
