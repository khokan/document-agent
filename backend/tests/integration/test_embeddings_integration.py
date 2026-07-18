"""Optional integration coverage for the active LangChain embedding provider."""

import unittest

from app.ai.factory import create_embeddings
from app.utils.config import config


class TestEmbeddingsIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = create_embeddings()

    async def test_real_embedding_generation(self):
        embedding = await self.service.aembed_query("Integration testing embeddings")
        self.assertEqual(len(embedding), config.embedding_dimension)
        self.assertTrue(all(isinstance(value, float) for value in embedding))

    async def test_real_embeddings_batch(self):
        embeddings = await self.service.aembed_documents(["First test text", "Second test text"])
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), config.embedding_dimension)
