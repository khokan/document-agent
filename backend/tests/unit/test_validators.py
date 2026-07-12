"""
🧪 Unit tests for input validators.
"""

import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from app.utils.validators import FileValidator, SearchValidator


class TestFileValidator(unittest.TestCase):
    """Test file validation functions."""

    def test_validate_filename_valid(self):
        """Test validation of valid filename."""
        is_valid, error = FileValidator.validate_filename("document.pdf")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_filename_path_traversal(self):
        """Test rejection of path traversal."""
        is_valid, error = FileValidator.validate_filename("../../../etc/passwd")
        self.assertFalse(is_valid)
        self.assertIn("traversal", error.lower())

    def test_validate_filename_empty(self):
        """Test rejection of empty filename."""
        is_valid, error = FileValidator.validate_filename("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_validate_filename_too_long(self):
        """Test rejection of overly long filename."""
        long_name = "a" * 300 + ".pdf"
        is_valid, error = FileValidator.validate_filename(long_name)
        self.assertFalse(is_valid)
        self.assertIn("long", error.lower())

    def test_validate_pdf_file_not_exists(self):
        """Test validation with non-existent file."""
        is_valid, error = FileValidator.validate_pdf_file("nonexistent.pdf")
        self.assertFalse(is_valid)
        self.assertIn("not exist", error.lower())

    def test_validate_pdf_file_empty(self):
        """Test validation with empty file."""
        with NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            is_valid, error = FileValidator.validate_pdf_file(tmp_path)
            self.assertFalse(is_valid)
            self.assertIn("empty", error.lower())
        finally:
            Path(tmp_path).unlink()

    def test_validate_pdf_file_invalid_extension(self):
        """Test validation with invalid extension."""
        with NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"%PDF-1.4")  # PDF magic bytes but .txt extension
            tmp_path = tmp.name

        try:
            is_valid, error = FileValidator.validate_pdf_file(tmp_path)
            self.assertFalse(is_valid)
            self.assertIn("extension", error.lower())
        finally:
            Path(tmp_path).unlink()


class TestSearchValidator(unittest.TestCase):
    """Test search query validation."""

    def test_validate_query_valid(self):
        """Test validation of valid query."""
        is_valid, error = SearchValidator.validate_query("What is the company revenue?")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_query_empty(self):
        """Test rejection of empty query."""
        is_valid, error = SearchValidator.validate_query("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_validate_query_whitespace_only(self):
        """Test rejection of whitespace-only query."""
        is_valid, error = SearchValidator.validate_query("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_validate_query_too_long(self):
        """Test rejection of overly long query."""
        long_query = "a" * 1500
        is_valid, error = SearchValidator.validate_query(long_query)
        self.assertFalse(is_valid)
        self.assertIn("exceed", error.lower())


if __name__ == "__main__":
    unittest.main()
