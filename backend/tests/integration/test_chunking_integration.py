"""
🧪 Integration tests for chunking.
"""

import unittest
from app.pdf.extractor import PDFExtractor
from app.pdf.cleaner import TextCleaner
from app.chunking.splitter import ChunkSplitter


class TestChunkingIntegration(unittest.TestCase):
    """Verify document extraction-to-chunking integration."""

    def test_extraction_to_chunking_flow(self):
        # We simulate extractor and cleaner outputs
        page_texts = {
            1: "Header Section\nThis is a sample document containing financial statements of Acme Corp for 2026.\nFooter - Page 1",
            2: "This is page 2 content.\nWe recorded total profit of $5 million.\nFooter - Page 2"
        }
        
        # Clean the text
        cleaned_pages = TextCleaner.clean_pages(page_texts)
        self.assertTrue(len(cleaned_pages) >= 1)

        # Chunk the text
        splitter = ChunkSplitter()
        chunks = splitter.split_document(
            document_id="acme_2026",
            page_texts=cleaned_pages,
            doc_metadata={"company": "Acme Corp", "year": 2026}
        )

        self.assertTrue(len(chunks) >= 1)
        # Verify metadata is correct
        for chunk in chunks:
            self.assertEqual(chunk["metadata"]["document_id"], "acme_2026")
            self.assertEqual(chunk["metadata"]["company"], "Acme Corp")
            self.assertEqual(chunk["metadata"]["year"], 2026)
            self.assertIn("page_number", chunk["metadata"])
