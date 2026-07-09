"""
📑 PDF text extraction using PdfPlumber.

Extracts text from PDF files while maintaining page structure.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

import pdfplumber
from pypdf import PdfReader

from app.utils.logger import logger


class PDFExtractor:
    """Extract text from PDF files."""

    @staticmethod
    def extract_text_by_page(pdf_path: str) -> Tuple[bool, Dict[int, str]]:
        """
        Extract text from PDF organized by page.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Tuple of (success, page_text_dict)
            page_text_dict: {page_number: text}
        """
        try:
            if not Path(pdf_path).exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return False, {}

            page_texts = {}

            # Try pdfplumber first (more reliable)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    logger.info(f"📑 Extracting text from {len(pdf.pages)} pages...")

                    for page_num, page in enumerate(pdf.pages, start=1):
                        text = page.extract_text()
                        if text:
                            page_texts[page_num] = text
                        else:
                            page_texts[page_num] = ""
                            logger.warning(f"⚠️ No text extracted from page {page_num}")

                logger.info(f"✅ Successfully extracted text from {len(page_texts)} pages")
                return True, page_texts

            except Exception as e:
                logger.warning(f"PdfPlumber failed: {str(e)}. Attempting fallback with PyPDF...")

                # Fallback to PyPDF
                reader = PdfReader(pdf_path)
                logger.info(f"📑 Extracting text from {len(reader.pages)} pages (PyPDF)...")

                for page_num, page in enumerate(reader.pages, start=1):
                    text = page.extract_text()
                    page_texts[page_num] = text if text else ""

                logger.info(f"✅ Successfully extracted text from {len(page_texts)} pages (PyPDF)")
                return True, page_texts

        except Exception as e:
            error_msg = f"❌ Error extracting PDF: {str(e)}"
            logger.error(error_msg)
            return False, {}

    @staticmethod
    def get_page_count(pdf_path: str) -> Tuple[bool, int]:
        """
        Get total page count from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Tuple of (success, page_count)
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                count = len(pdf.pages)
                logger.info(f"📄 PDF has {count} pages")
                return True, count
        except Exception as e:
            logger.error(f"Error getting page count: {str(e)}")
            return False, 0

    @staticmethod
    def get_pdf_metadata(pdf_path: str) -> Dict:
        """
        Extract PDF metadata.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary containing metadata
        """
        try:
            reader = PdfReader(pdf_path)
            metadata = reader.metadata

            return {
                "title": metadata.title if metadata else None,
                "author": metadata.author if metadata else None,
                "subject": metadata.subject if metadata else None,
                "creator": metadata.creator if metadata else None,
                "producer": metadata.producer if metadata else None,
                "page_count": len(reader.pages),
            }
        except Exception as e:
            logger.warning(f"Could not extract PDF metadata: {str(e)}")
            return {}
