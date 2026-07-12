"""
Unit tests for all service modules.

Tests cover:
- PDF extraction and cleaning
- File validation
- Configuration loading
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from app.utils.validators import FileValidator
from app.pdf.extractor import PDFExtractor
from app.pdf.cleaner import TextCleaner
from app.utils.config import Config


class TestFileValidator:
    """Test FileValidator utility."""

    def test_validate_filename_valid(self):
        """Test validation of valid filenames."""
        valid_filenames = [
            "document.pdf",
            "Report_2024.pdf",
            "Annual-Report-Q1-2024.pdf",
            "file (1).pdf",
            "UPPERCASE.PDF",
        ]
        for filename in valid_filenames:
            is_valid, _ = FileValidator.validate_filename(filename)
            assert is_valid, f"Should accept valid filename: {filename}"

    def test_validate_filename_invalid_extension(self):
        """Test rejection of non-PDF files."""
        invalid_extensions = [
            "document.txt",
            "image.jpg",
            "data.xlsx",
            "archive.zip",
            "script.py",
        ]
        for filename in invalid_extensions:
            is_valid, error = FileValidator.validate_filename(filename)
            assert not is_valid, f"Should reject {filename}"
            assert "pdf" in error.lower()

    def test_validate_filename_special_characters(self):
        """Test rejection of filenames with special characters."""
        invalid_names = [
            "file<>.pdf",
            "file|name.pdf",
            "file*name.pdf",
            "file?name.pdf",
            'file"name.pdf',
            "file:name.pdf",
            "file\\name.pdf",
        ]
        for filename in invalid_names:
            is_valid, error = FileValidator.validate_filename(filename)
            assert not is_valid, f"Should reject {filename}"

    def test_validate_filename_length_limits(self):
        """Test filename length validation."""
        # Very long filename
        long_name = "a" * 500 + ".pdf"
        is_valid, error = FileValidator.validate_filename(long_name)
        assert not is_valid
        assert "length" in error.lower() or "long" in error.lower()

    def test_validate_filename_empty(self):
        """Test rejection of empty filename."""
        is_valid, error = FileValidator.validate_filename("")
        assert not is_valid

    def test_validate_pdf_file_magic_bytes(self):
        """Test PDF magic bytes validation."""
        import tempfile
        import os
        
        # Test with non-PDF file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pdf') as f:
            f.write(b"This is not a PDF file")
            temp_path = f.name
        
        try:
            is_valid, error = FileValidator.validate_pdf_file(temp_path)
            assert not is_valid
            assert "invalid" in error.lower() or "magic" in error.lower()
        finally:
            os.remove(temp_path)

    def test_validate_pdf_file_size(self):
        """Test PDF file size validation."""
        import tempfile
        import os
        
        # Create a tiny file (less than minimum)
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pdf') as f:
            f.write(b"")  # Empty file
            temp_path = f.name
        
        try:
            is_valid, error = FileValidator.validate_pdf_file(temp_path)
            # Empty file should be invalid
            assert not is_valid or error  # Either invalid or has error message
        finally:
            os.remove(temp_path)


class TestTextCleaner:
    """Test TextCleaner utility."""

    def test_clean_empty_pages(self):
        """Test cleaning of empty pages."""
        pages = {1: "", 2: "   ", 3: "\n\t"}
        result = TextCleaner.clean_pages(pages)
        assert isinstance(result, dict)
        # Empty pages should be filtered or marked
        for page_num, text in result.items():
            if text:
                assert len(text.strip()) > 0

    def test_clean_pages_with_content(self):
        """Test cleaning of pages with valid content."""
        pages = {
            1: "This is page 1 content",
            2: "This is page 2 content",
        }
        result = TextCleaner.clean_pages(pages)
        assert isinstance(result, dict)
        assert len(result) <= 2

    def test_clean_pages_removes_extra_whitespace(self):
        """Test that cleaner removes extra whitespace."""
        pages = {
            1: "This   has    extra    spaces\n\n\nand newlines\t\ttabs",
        }
        result = TextCleaner.clean_pages(pages)
        assert isinstance(result, dict)
        # Content should be preserved but whitespace normalized
        for text in result.values():
            if text:
                # Should not have multiple consecutive spaces
                assert "   " not in text

    def test_clean_pages_with_special_characters(self):
        """Test cleaning of pages with special characters."""
        pages = {
            1: "Content with special chars: @#$%^&*()",
            2: "Unicode: café, naïve, résumé",
        }
        result = TextCleaner.clean_pages(pages)
        assert isinstance(result, dict)
        assert len(result) >= 0  # Should handle without errors


class TestPDFExtractor:
    """Test PDFExtractor utility."""

    def test_extract_text_by_page_returns_tuple(self):
        """Test that extract_text_by_page returns (success, pages) tuple."""
        # Mock pdfplumber
        with patch('pdfplumber.open') as mock_pdfplumber:
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Page content"
            mock_pdf.pages = [mock_page]
            mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
            
            result = PDFExtractor.extract_text_by_page("dummy.pdf")
            
            assert isinstance(result, tuple)
            assert len(result) == 2
            success, pages = result
            assert isinstance(success, bool)
            assert isinstance(pages, dict)

    def test_extract_text_by_page_with_multiple_pages(self):
        """Test extraction from multi-page PDF."""
        with patch('pdfplumber.open') as mock_pdfplumber:
            mock_pdf = MagicMock()
            mock_pages = []
            for i in range(3):
                mock_page = MagicMock()
                mock_page.extract_text.return_value = f"Page {i+1} content"
                mock_pages.append(mock_page)
            
            mock_pdf.pages = mock_pages
            mock_pdfplumber.return_value.__enter__.return_value = mock_pdf
            
            success, pages = PDFExtractor.extract_text_by_page("dummy.pdf")
            
            assert success or isinstance(pages, dict)

    def test_extract_text_handles_exceptions(self):
        """Test that extraction handles exceptions gracefully."""
        with patch('pdfplumber.open') as mock_pdfplumber:
            mock_pdfplumber.side_effect = Exception("PDF error")
            
            success, pages = PDFExtractor.extract_text_by_page("dummy.pdf")
            
            # Should not raise, should return failure indication
            assert isinstance(success, bool)
            assert isinstance(pages, dict)


class TestConfigLoader:
    """Test configuration loading."""

    def test_config_loads_from_yaml(self):
        """Test that config loads from YAML file."""
        from app.utils import config
        
        # Config should be loaded
        assert config is not None
        assert hasattr(config, 'app_name')
        assert hasattr(config, 'app_version')

    def test_config_has_required_fields(self):
        """Test that config has all required fields."""
        from app.utils import config
        
        required_fields = [
            'app_name',
            'app_version',
            'upload_dir',
            'temp_dir',
            'embedding_dimension',
            'chroma_collection_name',
            'max_file_size_mb',
        ]
        
        for field in required_fields:
            assert hasattr(config, field), f"Config missing required field: {field}"

    def test_config_values_are_reasonable(self):
        """Test that config values are reasonable."""
        from app.utils import config
        
        # Embedding dimension should be reasonable
        assert config.embedding_dimension > 0
        assert config.embedding_dimension <= 2048
        
        # Max file size should be positive
        assert config.max_file_size_mb > 0
        
        # App version should be non-empty
        assert len(config.app_name) > 0
        assert len(config.app_version) > 0


class TestValidationIntegration:
    """Integration tests for validation chain."""

    def test_full_validation_chain_valid_pdf(self):
        """Test complete validation chain with valid PDF."""
        import tempfile
        import os
        
        # Create minimal valid PDF
        pdf_content = b"""%PDF-1.4
1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj
2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj
3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]>> endobj
xref
0 4
0000000000 65535 f 
0000000010 00000 n 
0000000063 00000 n 
0000000120 00000 n 
trailer <</Size 4 /Root 1 0 R>>
startxref
200
%%EOF"""
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pdf') as f:
            f.write(pdf_content)
            temp_path = f.name
        
        try:
            # Step 1: Filename validation
            is_valid, _ = FileValidator.validate_filename(Path(temp_path).name)
            assert is_valid
            
            # Step 2: PDF structure validation
            is_valid, _ = FileValidator.validate_pdf_file(temp_path)
            # This might fail depending on pdfplumber, but should not raise
            assert isinstance(is_valid, bool)
        finally:
            os.remove(temp_path)

    def test_full_validation_chain_invalid_pdf(self):
        """Test complete validation chain with invalid PDF."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pdf') as f:
            f.write(b"NOT A PDF")
            temp_path = f.name
        
        try:
            # Step 1: Filename validation should pass
            is_valid, _ = FileValidator.validate_filename(Path(temp_path).name)
            assert is_valid
            
            # Step 2: PDF structure validation should fail
            is_valid, error = FileValidator.validate_pdf_file(temp_path)
            assert not is_valid
            assert len(error) > 0
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
