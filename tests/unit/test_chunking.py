"""
🧪 Unit tests for text chunking strategies and ChunkSplitter.
"""

import unittest
from app.chunking.strategies import FixedSizeChunkingStrategy, RecursiveChunkingStrategy
from app.chunking.splitter import ChunkSplitter


class TestChunkingStrategies(unittest.TestCase):
    """Test the behavior of splitting strategies."""

    def test_fixed_size_chunking(self):
        strategy = FixedSizeChunkingStrategy(chunk_size=10, chunk_overlap=2)
        text = "abcdefghijklmnop"
        chunks = strategy.split_text(text)
        # Expected chunks:
        # "abcdefghij" (0-10)
        # "ijlkmnop" (overlap start is 8: 'ij' is 8-10. Wait, 10-2 = 8, so start at 8)
        # Let's verify size and overlap
        self.assertTrue(len(chunks) >= 2)
        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1], "ijklmnop")

    def test_recursive_chunking(self):
        strategy = RecursiveChunkingStrategy(chunk_size=20, chunk_overlap=5)
        text = "This is a sentence.\n\nThis is another sentence."
        chunks = strategy.split_text(text)
        self.assertTrue(len(chunks) >= 1)
        self.assertIn("This is a sentence.", chunks[0])


class TestChunkSplitter(unittest.TestCase):
    """Test the main ChunkSplitter service."""

    def test_split_document(self):
        splitter = ChunkSplitter()
        page_texts = {
            1: "This is page one text.",
            2: "Here is page two content."
        }
        
        chunks = splitter.split_document(
            document_id="test_doc",
            page_texts=page_texts,
            doc_metadata={"company": "Acme Inc", "year": 2026}
        )
        
        self.assertTrue(len(chunks) >= 2)
        self.assertEqual(chunks[0]["metadata"]["document_id"], "test_doc")
        self.assertEqual(chunks[0]["metadata"]["page_number"], 1)
        self.assertEqual(chunks[0]["metadata"]["company"], "Acme Inc")
        self.assertEqual(chunks[0]["metadata"]["year"], 2026)
        
        # Verify page 2 chunk has correct page number
        page2_chunks = [c for c in chunks if c["metadata"]["page_number"] == 2]
        self.assertTrue(len(page2_chunks) > 0)
        self.assertEqual(page2_chunks[0]["metadata"]["page_number"], 2)
