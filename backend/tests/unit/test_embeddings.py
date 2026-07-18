"""Unit tests for the provider-neutral LangChain embedding contract."""

import unittest
from unittest.mock import AsyncMock, patch

from app.rag.retriever import Retriever
from app.embeddings.cache import EmbeddingCache


class TestEmbeddingProviderInterface(unittest.IsolatedAsyncioTestCase):
    async def test_retriever_uses_aembed_query(self):
        embeddings = AsyncMock()
        embeddings.aembed_query.return_value = [0.1, 0.2, 0.3]
        vector_store = AsyncMock()
        vector_store.query_similarity.return_value = []
        vector_store.require_ready = lambda: None
        retriever = Retriever(embeddings, vector_store)

        self.assertEqual(await retriever.retrieve("hello"), [])
        embeddings.aembed_query.assert_awaited_once_with("hello")

    async def test_retriever_passes_filters_to_vector_store(self):
        embeddings = AsyncMock()
        embeddings.aembed_query.return_value = [0.1, 0.2]
        vector_store = AsyncMock()
        vector_store.query_similarity.return_value = []
        vector_store.require_ready = lambda: None
        retriever = Retriever(embeddings, vector_store)

        await retriever.retrieve("test query", top_k=10, filters={"company": "Acme"})
        vector_store.query_similarity.assert_awaited_once_with(
            query_embedding=[0.1, 0.2],
            top_k=10,
            filters={"company": "Acme"},
        )

    async def test_batch_embedding_via_aembed_documents(self):
        embeddings = AsyncMock()
        embeddings.aembed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]
        texts = ["chunk one", "chunk two"]
        result = await embeddings.aembed_documents(texts)
        embeddings.aembed_documents.assert_awaited_once_with(texts)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [0.1, 0.2])
        self.assertEqual(result[1], [0.3, 0.4])


class TestEmbeddingCache(unittest.TestCase):
    def test_cache_key_includes_profile_fingerprint(self):
        with patch("app.embeddings.cache.config") as mock_config:
            mock_config.cache_embeddings = True
            mock_config.chroma_persist_directory = "/tmp"
            mock_config.embedding_profile_fingerprint = "abc123"

            cache = EmbeddingCache()
            key1 = cache._get_hash("test text")

        with patch("app.embeddings.cache.config") as mock_config:
            mock_config.cache_embeddings = True
            mock_config.chroma_persist_directory = "/tmp"
            mock_config.embedding_profile_fingerprint = "def456"

            cache2 = EmbeddingCache()
            key2 = cache2._get_hash("test text")

        self.assertNotEqual(key1, key2, "Cache keys must differ when embedding profiles differ")

    def test_cache_hit_after_set(self):
        with patch("app.embeddings.cache.config") as mock_config:
            mock_config.cache_embeddings = True
            mock_config.chroma_persist_directory = "/tmp"
            mock_config.embedding_profile_fingerprint = "test"

            cache = EmbeddingCache()
            cache.set("hello", [0.1, 0.2])
            result = cache.get("hello")

        self.assertEqual(result, [0.1, 0.2])

    def test_cache_miss(self):
        with patch("app.embeddings.cache.config") as mock_config:
            mock_config.cache_embeddings = True
            mock_config.chroma_persist_directory = "/tmp"
            mock_config.embedding_profile_fingerprint = "test"

            cache = EmbeddingCache()
            result = cache.get("nonexistent")

        self.assertIsNone(result)
