"""
🧹 Text cleaning and normalization for extracted PDF content.

Removes headers, footers, extra whitespace, and normalizes text.
"""

import re
from typing import Dict

from app.utils.logger import logger


class TextCleaner:
    """Clean and normalize extracted text."""

    # Common header/footer patterns
    HEADER_PATTERNS = [
        r"^.*\d{1,2}.*$",  # Lines with mostly numbers (page numbers, etc)
        r"^[A-Za-z\s]{1,5}$",  # Very short lines (likely headers)
    ]

    FOOTER_PATTERNS = [
        r"^Page \d+",
        r"^-{3,}",
        r"^_{3,}",
        r"Copyright|©",
    ]

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters but keep basic punctuation
        text = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)

        # Remove URLs
        text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", text)

        # Remove email addresses
        text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "", text)

        # Trim whitespace
        text = text.strip()

        return text

    @staticmethod
    def remove_headers_and_footers(text: str) -> str:
        """
        Remove header and footer lines from text.

        Args:
            text: Text containing headers/footers

        Returns:
            Text with headers/footers removed
        """
        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            line_stripped = line.strip()

            # Skip empty lines
            if not line_stripped:
                continue

            # Check if line matches header patterns
            is_header = any(re.match(pattern, line_stripped) for pattern in TextCleaner.HEADER_PATTERNS)

            # Check if line matches footer patterns
            is_footer = any(re.search(pattern, line_stripped, re.IGNORECASE) for pattern in TextCleaner.FOOTER_PATTERNS)

            if not is_header and not is_footer:
                cleaned_lines.append(line_stripped)

        return "\n".join(cleaned_lines)

    @staticmethod
    def clean_page_text(text: str) -> str:
        """
        Apply all cleaning operations to page text.

        Args:
            text: Raw page text

        Returns:
            Cleaned page text
        """
        # Remove headers and footers first
        text = TextCleaner.remove_headers_and_footers(text)

        # Then clean the text
        text = TextCleaner.clean_text(text)

        return text

    @staticmethod
    def clean_pages(page_texts: Dict[int, str]) -> Dict[int, str]:
        """
        Clean all pages.

        Args:
            page_texts: Dictionary mapping page numbers to text

        Returns:
            Dictionary with cleaned text
        """
        cleaned_pages = {}

        for page_num, text in page_texts.items():
            try:
                cleaned_text = TextCleaner.clean_page_text(text)
                if cleaned_text:  # Only keep non-empty pages
                    cleaned_pages[page_num] = cleaned_text
                else:
                    logger.warning(f"⚠️ Page {page_num} resulted in empty text after cleaning")
            except Exception as e:
                logger.error(f"Error cleaning page {page_num}: {str(e)}")

        logger.info(f"✅ Cleaned {len(cleaned_pages)} pages successfully")
        return cleaned_pages

    @staticmethod
    def get_text_statistics(text: str) -> Dict:
        """
        Get text statistics.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with statistics
        """
        words = text.split()
        sentences = re.split(r"[.!?]+", text)

        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        }
