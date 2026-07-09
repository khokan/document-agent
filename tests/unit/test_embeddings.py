"""
🧪 Unit tests for OllamaEmbeddingService.
"""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from app.embeddings.ollama_service import OllamaEmbeddingService


class TestOllamaEmbeddingService(unittest.IsolatedAsyncioTestCase):
    """Test generating embeddings with mocked HTTP client."""

    @patch("app.embeddings.client.OllamaClient")
    async def test_get_embedding(self, mock_client_class):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
        
        mock_client = mock_client_class.return_value
        mock_client.post = AsyncMock(return_value=mock_response)

        service = OllamaEmbeddingService(client=mock_client)
        vector = await service.get_embedding("hello world")

        self.assertEqual(vector, [0.1, 0.2, 0.3])
        mock_client.post.assert_called_once_with(
            "/api/embeddings",
            {"model": service.model, "prompt": "hello world"}
        )

    @patch("app.embeddings.client.OllamaClient")
    async def test_get_embeddings_batch(self, mock_client_class):
        # Setup mock response for /api/embed batch endpoint
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "embeddings": [
                [0.1, 0.2],
                [0.3, 0.4]
            ]
        }
        
        mock_client = mock_client_class.return_value
        mock_client.post = AsyncMock(return_value=mock_response)

        service = OllamaEmbeddingService(client=mock_client)
        vectors = await service.get_embeddings(["hello", "world"])

        self.assertEqual(len(vectors), 2)
        self.assertEqual(vectors[0], [0.1, 0.2])
        self.assertEqual(vectors[1], [0.3, 0.4])
        mock_client.post.assert_called_once_with(
            "/api/embed",
            {"model": service.model, "input": ["hello", "world"]}
        )
