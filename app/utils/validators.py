"""
✅ Input validators for the PDF Knowledge Assistant.

Validates file types, sizes, and other inputs.
"""

import os
from pathlib import Path
from typing import Tuple

from app.utils.config import config
from app.utils.logger import logger


class FileValidator:
    """Validates uploaded files."""

    @staticmethod
    def validate_pdf_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate if a file is a valid PDF.

        Args:
            file_path: Path to the file to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)

        # Check file exists
        if not path.exists():
            error = f"File does not exist: {file_path}"
            logger.error(error)
            return False, error

        # Check file extension
        if path.suffix.lower() not in config.pdf_allowed_extensions:
            error = f"Invalid file extension. Allowed: {config.pdf_allowed_extensions}"
            logger.error(error)
            return False, error

        # Check file size
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > config.pdf_max_size_mb:
            error = f"File size {file_size_mb:.2f}MB exceeds max allowed {config.pdf_max_size_mb}MB"
            logger.error(error)
            return False, error

        # Check if file is not empty
        if path.stat().st_size == 0:
            error = "File is empty"
            logger.error(error)
            return False, error

        # Check PDF magic bytes
        try:
            with open(file_path, "rb") as f:
                magic_bytes = f.read(4)
                if magic_bytes != b"%PDF":
                    error = "File is not a valid PDF (invalid magic bytes)"
                    logger.error(error)
                    return False, error
        except Exception as e:
            error = f"Error validating PDF magic bytes: {str(e)}"
            logger.error(error)
            return False, error

        logger.info(f"✅ File validation passed: {file_path}")
        return True, ""

    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, str]:
        """
        Validate filename for security.

        Args:
            filename: Filename to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            error = "Invalid filename: path traversal detected"
            logger.error(error)
            return False, error

        # Check length
        if len(filename) > 255:
            error = "Filename is too long (max 255 characters)"
            logger.error(error)
            return False, error

        if len(filename) == 0:
            error = "Filename cannot be empty"
            logger.error(error)
            return False, error

        logger.info(f"✅ Filename validation passed: {filename}")
        return True, ""


class SearchValidator:
    """Validates search queries."""

    @staticmethod
    def validate_query(query: str, max_length: int = 1000) -> Tuple[bool, str]:
        """
        Validate search query.

        Args:
            query: Search query string
            max_length: Maximum query length

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or len(query.strip()) == 0:
            error = "Query cannot be empty"
            logger.warning(error)
            return False, error

        if len(query) > max_length:
            error = f"Query exceeds max length of {max_length} characters"
            logger.warning(error)
            return False, error

        logger.info(f"✅ Query validation passed: {query[:50]}...")
        return True, ""
