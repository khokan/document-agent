"""
🧪 Integration tests for Ollama embedding service.
"""

import unittest
import httpx
from app.embeddings.client import OllamaClient
from app.embeddings.ollama_service import OllamaEmbeddingService


class TestEmbeddingsIntegration(unittest.IsolatedAsyncioTestCase):
    """Test generating real embeddings from a local Ollama server if available."""

    async def asyncSetUp(self):
        self.client = OllamaClient()
        self.service = OllamaEmbeddingService(client=self.client)
        self.ollama_online = await self.client.check_health()
        
        self.model_available = False
        if self.ollama_online:
            try:
                async with httpx.AsyncClient(timeout=3.0) as http_client:
                    res = await http_client.get(f"{self.client.base_url.rstrip('/')}/api/tags")
                    if res.status_code == 200:
                        models = res.json().get("models", [])
                        model_names = [m["name"].split(":")[0] for m in models]
                        self.model_available = self.service.model.split(":")[0] in model_names
            except Exception:
                pass

    async def test_real_embedding_generation(self):
        if not self.ollama_online:
            self.skipTest("Ollama server is offline. Skipping integration test.")
        if not self.model_available:
            self.skipTest(f"Ollama model '{self.service.model}' not available. Skipping integration test.")

        embedding = await self.service.get_embedding("Integration testing embeddings")
        self.assertEqual(len(embedding), 768)  # nomic-embed-text size
        self.assertTrue(all(isinstance(x, float) for x in embedding))

    async def test_real_embeddings_batch(self):
        if not self.ollama_online:
            self.skipTest("Ollama server is offline. Skipping integration test.")
        if not self.model_available:
            self.skipTest(f"Ollama model '{self.service.model}' not available. Skipping integration test.")

        texts = ["First test text", "Second test text"]
        embeddings = await self.service.get_embeddings(texts)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), 768)
        self.assertEqual(len(embeddings[1]), 768)
