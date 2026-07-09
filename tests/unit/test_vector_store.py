"""
🧪 Unit tests for ChromaDBService vector database integration.
"""

import unittest
from unittest.mock import patch
import chromadb
from app.vector_store.chromadb_service import ChromaDBService


class TestChromaDBService(unittest.IsolatedAsyncioTestCase):
    """Test vector storage CRUD and querying using EphemeralClient."""

    def setUp(self):
        # Patch PersistentClient to use EphemeralClient (in-memory)
        self.client_patcher = patch("chromadb.PersistentClient")
        self.mock_persistent = self.client_patcher.start()
        
        # Ephemeral client for real in-memory ChromaDB operations
        self.ephemeral_client = chromadb.EphemeralClient()
        self.mock_persistent.return_value = self.ephemeral_client

        # Instantiate service
        self.service = ChromaDBService()

    def tearDown(self):
        self.client_patcher.stop()

    async def test_add_and_query_chunks(self):
        chunks = [
            {
                "chunk_id": "doc1_p1_c0",
                "text": "The quick brown fox jumps over the lazy dog.",
                "metadata": {"document_id": "doc1", "page_number": 1}
            },
            {
                "chunk_id": "doc1_p1_c1",
                "text": "Artificial Intelligence is shaping the future.",
                "metadata": {"document_id": "doc1", "page_number": 1}
            }
        ]
        embeddings = [
            [0.1 if idx % 2 == 0 else -0.1 for idx in range(768)],
            [-0.1 if idx % 2 == 0 else 0.1 for idx in range(768)]
        ]

        # 1. Add chunks
        await self.service.add_chunks(chunks, embeddings)

        # 2. Get stats
        stats = await self.service.get_stats()
        self.assertEqual(stats["count"], 2)

        # 3. Query similarity
        query_embedding = [0.12 if idx % 2 == 0 else -0.12 for idx in range(768)]
        results = await self.service.query_similarity(query_embedding, top_k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["chunk_id"], "doc1_p1_c0")
        self.assertTrue(results[0]["score"] > 0.9)  # High similarity score

    async def test_delete_document_chunks(self):
        chunks = [
            {
                "chunk_id": "doc1_p1_c0",
                "text": "Hello world",
                "metadata": {"document_id": "doc1"}
            },
            {
                "chunk_id": "doc2_p1_c0",
                "text": "Goodbye world",
                "metadata": {"document_id": "doc2"}
            }
        ]
        embeddings = [
            [0.1 if idx % 2 == 0 else -0.1 for idx in range(768)],
            [-0.1 if idx % 2 == 0 else 0.1 for idx in range(768)]
        ]

        await self.service.add_chunks(chunks, embeddings)
        await self.service.delete_document_chunks("doc1")

        stats = await self.service.get_stats()
        self.assertEqual(stats["count"], 1)

        # Make sure only doc2 is left
        query_embedding = [-0.1 if idx % 2 == 0 else 0.1 for idx in range(768)]
        results = await self.service.query_similarity(query_embedding, top_k=1)
        self.assertEqual(results[0]["chunk_id"], "doc2_p1_c0")
