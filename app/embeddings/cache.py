"""
💾 Persistent caching for generated dense vector embeddings.
"""

import os
import json
import hashlib
from typing import Dict, List, Optional
from app.utils.logger import logger
from app.utils.config import config


class EmbeddingCache:
    """JSON-backed persistent cache for text embeddings."""

    def __init__(self, cache_file: str = ".embedding_cache.json"):
        self.cache_enabled = config.cache_embeddings
        # Place cache file inside persist directory or root
        persist_dir = config.chroma_persist_directory
        self.cache_path = os.path.join(persist_dir, cache_file)
        self._cache: Dict[str, List[float]] = {}
        self._dirty = False

        if self.cache_enabled:
            self._load_cache()

    def _get_hash(self, text: str) -> str:
        """Generate SHA-256 hash for text chunk."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _load_cache(self) -> None:
        """Load cache from disk."""
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
                logger.info(f"[EMBEDDINGS] Loaded {len(self._cache)} cached embeddings from {self.cache_path}")
        except Exception as e:
            logger.warning(f"[WARN] Failed to load embedding cache: {str(e)}")
            self._cache = {}

    def save(self) -> None:
        """Persist cache to disk if modified."""
        if not self.cache_enabled or not self._dirty:
            return

        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self._cache, f)
            self._dirty = False
            logger.info(f"[EMBEDDINGS] Saved embedding cache to {self.cache_path}")
        except Exception as e:
            logger.error(f"[ERR] Failed to save embedding cache: {str(e)}")

    def get(self, text: str) -> Optional[List[float]]:
        """Retrieve embedding from cache if exists."""
        if not self.cache_enabled:
            return None

        h = self._get_hash(text)
        return self._cache.get(h)

    def set(self, text: str, embedding: List[float]) -> None:
        """Store embedding in cache."""
        if not self.cache_enabled:
            return

        h = self._get_hash(text)
        self._cache[h] = embedding
        self._dirty = True


# Global embedding cache
embedding_cache = EmbeddingCache()
