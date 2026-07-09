"""
🎯 Chunking strategies for splitting document text.
"""

from abc import ABC, abstractmethod
from typing import List
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChunkingStrategy(ABC):
    """Abstract base class for all chunking strategies."""

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """
        Split a string of text into smaller chunks.

        Args:
            text: Raw string to split

        Returns:
            List of chunk strings
        """
        pass


class RecursiveChunkingStrategy(ChunkingStrategy):
    """Recursively splits text using separators (e.g. paragraphs, sentences, words)."""

    def __init__(self, chunk_size: int, chunk_overlap: int):
        """
        Initialize the recursive chunking strategy.

        Args:
            chunk_size: Maximum size of a chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

    def split_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)


class FixedSizeChunkingStrategy(ChunkingStrategy):
    """Splits text into fixed size character chunks with overlap."""

    def __init__(self, chunk_size: int, chunk_overlap: int):
        """
        Initialize the fixed-size chunking strategy.

        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
            
            # Avoid infinite loop if overlap >= size
            if self.chunk_size <= self.chunk_overlap:
                break

        return chunks
