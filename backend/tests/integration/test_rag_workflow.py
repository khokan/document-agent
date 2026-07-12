"""
🧪 Integration tests for RAG workflow API.
"""

import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app


class TestRAGWorkflowAPI(unittest.TestCase):
    """Verify that POST /rag/query runs the pipeline and returns a SearchResponse."""

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.rag.RAGPipeline.query", new_callable=AsyncMock)
    def test_rag_query_endpoint_success(self, mock_query):
        # Mock RAG query output matching SearchResponse schema
        mock_query.return_value = {
            "answer": "Acme Corp earned $10 million in revenue in 2026.",
            "sources": [
                {
                    "document_id": "acme_2026",
                    "filename": "acme_report.pdf",
                    "page": 2,
                    "score": 0.88,
                    "text": "Acme Corp earned $10 million in revenue."
                }
            ],
            "query": "How much did Acme earn in 2026?",
            "response_time_ms": 150.5
        }

        payload = {
            "question": "How much did Acme earn in 2026?",
            "top_k": 3
        }

        response = self.client.post("/rag/query", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["answer"], "Acme Corp earned $10 million in revenue in 2026.")
        self.assertEqual(data["query"], "How much did Acme earn in 2026?")
        self.assertEqual(len(data["sources"]), 1)
        self.assertEqual(data["sources"][0]["document_id"], "acme_2026")
        self.assertEqual(data["sources"][0]["filename"], "acme_report.pdf")
        self.assertEqual(data["sources"][0]["page"], 2)
        self.assertEqual(data["sources"][0]["score"], 0.88)
        self.assertEqual(data["sources"][0]["text"], "Acme Corp earned $10 million in revenue.")
        self.assertEqual(data["response_time_ms"], 150.5)

    def test_rag_query_endpoint_invalid_payload(self):
        payload = {
            "question": "a" * 1001,  # Exceeds max length limit (1000)
            "top_k": 3
        }
        response = self.client.post("/rag/query", json=payload)
        self.assertEqual(response.status_code, 422)
