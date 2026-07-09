"""
🧪 Integration tests for the semantic search API.
"""

import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app


class TestSearchAPI(unittest.TestCase):
    """Verify that POST /search returns formatted search results."""

    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.search.Retriever.retrieve", new_callable=AsyncMock)
    def test_search_endpoint_success(self, mock_retrieve):
        # Mock retrieval results
        mock_retrieve.return_value = [
            {
                "chunk_id": "doc1_p1_c0",
                "text": "Acme reported $10M revenue.",
                "score": 0.95,
                "metadata": {
                    "document_id": "doc1",
                    "original_filename": "acme.pdf",
                    "page_number": 1
                }
            }
        ]

        payload = {
            "question": "What is Acme's revenue?",
            "top_k": 3
        }

        response = self.client.post("/search", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["document_id"], "doc1")
        self.assertEqual(data[0]["filename"], "acme.pdf")
        self.assertEqual(data[0]["page"], 1)
        self.assertEqual(data[0]["score"], 0.95)
        self.assertEqual(data[0]["text"], "Acme reported $10M revenue.")

    def test_search_endpoint_invalid_payload(self):
        # Send empty question which should fail Pydantic validation (min_length=1)
        payload = {
            "question": "",
            "top_k": 3
        }
        response = self.client.post("/search", json=payload)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity
