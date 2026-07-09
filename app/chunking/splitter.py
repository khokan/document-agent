"""
📄 Main splitter service for processing document text into chunks.
"""

from typing import Dict, List, Any
from app.utils.logger import logger
from app.utils.config import config
from app.chunking.strategies import RecursiveChunkingStrategy, FixedSizeChunkingStrategy


class ChunkSplitter:
    """Service to handle document chunking using configured strategies."""

    def __init__(self):
        """Initialize the chunk splitter with configured parameters."""
        self.strategy_name = config.chunking_strategy
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap

        # Choose strategy
        if self.strategy_name == "fixed":
            self.strategy = FixedSizeChunkingStrategy(self.chunk_size, self.chunk_overlap)
        else:
            # Default to recursive
            self.strategy = RecursiveChunkingStrategy(self.chunk_size, self.chunk_overlap)
            
        logger.info(
            f"[CHUNKING] Initialized with strategy '{self.strategy_name}' "
            f"(size={self.chunk_size}, overlap={self.chunk_overlap})"
        )

    def split_document(self, document_id: str, page_texts: Dict[int, str], doc_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split a document (represented as page number to text mapping) into chunks.

        Args:
            document_id: Unique identifier for the document
            page_texts: Dict mapping page number (int) to page text (str)
            doc_metadata: Optional dict of document-level metadata (company, year, etc.)

        Returns:
            List of dictionaries, each representing a chunk with text and metadata.
        """
        chunks = []
        overall_chunk_index = 0
        metadata = doc_metadata or {}

        for page_num, text in page_texts.items():
            if not text or not text.strip():
                continue

            page_chunks = self.strategy.split_text(text)
            logger.debug(f"[CHUNKING] Split page {page_num} of {document_id} into {len(page_chunks)} chunks")

            for page_chunk_index, chunk_text in enumerate(page_chunks):
                chunk_id = f"{document_id}_p{page_num}_c{overall_chunk_index}"
                
                # Build chunk metadata
                chunk_metadata = {
                    "document_id": document_id,
                    "page_number": int(page_num),
                    "chunk_number": overall_chunk_index,
                    "page_chunk_index": page_chunk_index,
                    **metadata
                }

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })
                
                overall_chunk_index += 1

        logger.info(f"[OK] Split document {document_id} into {len(chunks)} total chunks")
        return chunks
