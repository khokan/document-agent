"""
💾 Cache manager for chunked document pages.
"""

from typing import Dict, List, Any


class ChunkCache:
    """Simple in-memory cache to manage document chunks."""

    def __init__(self):
        self._cache: Dict[str, List[Dict[str, Any]]] = {}

    def get(self, document_id: str) -> List[Dict[str, Any]]:
        """Get cached chunks for a document ID."""
        return self._cache.get(document_id, [])

    def set(self, document_id: str, chunks: List[Dict[str, Any]]) -> None:
        """Store chunks in cache for a document ID."""
        self._cache[document_id] = chunks

    def remove(self, document_id: str) -> None:
        """Remove document ID chunks from cache."""
        if document_id in self._cache:
            del self._cache[document_id]

    def clear(self) -> None:
        """Clear all cached chunks."""
        self._cache.clear()


# Global chunk cache
chunk_cache = ChunkCache()
