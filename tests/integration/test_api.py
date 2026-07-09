"""
🧪 Integration tests for the PDF upload pipeline.
"""

import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestUploadPipeline(unittest.TestCase):
    """Test the full upload pipeline."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertIn("version", data)

    def test_health_check_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")

    def test_list_documents_empty(self):
        """Test listing documents when empty."""
        response = client.get("/documents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_count"], 0)
        self.assertEqual(len(data["documents"]), 0)

    def test_delete_nonexistent_document(self):
        """Test deleting non-existent document."""
        response = client.delete("/documents/nonexistent_id")
        self.assertEqual(response.status_code, 404)

    def test_reindex_nonexistent_document(self):
        """Test reindexing non-existent document."""
        response = client.post("/documents/reindex/nonexistent_id")
        self.assertEqual(response.status_code, 404)

    def test_system_stats_empty(self):
        """Test system stats when empty."""
        response = client.get("/documents/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_documents"], 0)
        self.assertEqual(data["total_chunks"], 0)


if __name__ == "__main__":
    unittest.main()
