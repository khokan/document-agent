"""
🧪 Unit tests for PDF extraction functionality.
"""

import unittest
from pathlib import Path
from unittest.mock import patch

from app.pdf.cleaner import TextCleaner
from app.pdf.extractor import PDFExtractor


class TestPDFExtractor(unittest.TestCase):
    """Test PDF extraction functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_pdf_path = "test_sample.pdf"

    def test_extract_text_by_page_file_not_found(self):
        """Test extraction with non-existent file."""
        success, pages = PDFExtractor.extract_text_by_page("nonexistent.pdf")
        self.assertFalse(success)
        self.assertEqual(pages, {})

    def test_get_text_statistics(self):
        """Test text statistics calculation."""
        text = "This is a sample text. It has multiple sentences!"
        stats = TextCleaner.get_text_statistics(text)

        self.assertIn("character_count", stats)
        self.assertIn("word_count", stats)
        self.assertIn("sentence_count", stats)
        self.assertGreater(stats["word_count"], 0)


class TestTextCleaner(unittest.TestCase):
    """Test text cleaning functionality."""

    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        dirty_text = "This   has   extra    spaces"
        clean = TextCleaner.clean_text(dirty_text)
        self.assertEqual(clean, "This has extra spaces")

    def test_clean_text_remove_urls(self):
        """Test URL removal."""
        text_with_url = "Visit https://example.com for more info"
        clean = TextCleaner.clean_text(text_with_url)
        self.assertNotIn("https", clean)

    def test_clean_text_remove_emails(self):
        """Test email removal."""
        text_with_email = "Contact us at test@example.com today"
        clean = TextCleaner.clean_text(text_with_email)
        self.assertNotIn("test@example.com", clean)

    def test_clean_text_empty_string(self):
        """Test cleaning empty string."""
        clean = TextCleaner.clean_text("")
        self.assertEqual(clean, "")

    def test_remove_headers_and_footers(self):
        """Test header/footer removal."""
        text = """Page 1
        
        This is the main content
        
        Page 2"""
        clean = TextCleaner.remove_headers_and_footers(text)
        self.assertIn("main content", clean)

    def test_clean_pages_with_dict(self):
        """Test cleaning multiple pages."""
        pages = {1: "Page 1   text", 2: "Page 2   text"}
        cleaned = TextCleaner.clean_pages(pages)
        self.assertEqual(len(cleaned), 2)


if __name__ == "__main__":
    unittest.main()
