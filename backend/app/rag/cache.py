"""
💾 In-memory LRU response cache for RAG pipeline results.
"""

import time
import json
import hashlib
from collections import OrderedDict
from typing import Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config


class ResponseCache:
    """LRU cache for RAG pipeline responses with TTL expiration."""

    def __init__(
        self,
        enabled: Optional[bool] = None,
        max_entries: Optional[int] = None,
        ttl_seconds: Optional[int] = None
    ):
        """
        Initialize the response cache.

        Args:
            enabled: Whether caching is enabled (defaults to config)
            max_entries: Maximum cache entries before LRU eviction (defaults to config)
            ttl_seconds: Time-to-live for each entry in seconds (defaults to config)
        """
        self.enabled = enabled if enabled is not None else config.rag_cache_enabled
        self.max_entries = max_entries or config.rag_cache_max_entries
        self.ttl_seconds = ttl_seconds or config.rag_cache_ttl_seconds

        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._hits = 0
        self._misses = 0

        logger.info(
            f"[RAG] ResponseCache initialized "
            f"(enabled={self.enabled}, max_entries={self.max_entries}, ttl={self.ttl_seconds}s)"
        )

    def _make_key(self, query: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a deterministic cache key from query and filters.

        Args:
            query: Search query string
            filters: Optional metadata filters dict

        Returns:
            SHA-256 hex digest string
        """
        key_data = {
            "query": query.strip().lower(),
            "filters": filters or {},
            "embedding_profile": config.embedding_profile_fingerprint,
            "chat_profile": config.active_ai_profile,
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

    def get(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if available and not expired.

        Args:
            query: Search query string
            filters: Optional metadata filters dict

        Returns:
            Cached response dict or None on cache miss/expiry
        """
        if not self.enabled:
            return None

        key = self._make_key(query, filters)
        entry = self._cache.get(key)

        if entry is None:
            self._misses += 1
            return None

        # Check TTL expiry
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            # Expired entry — remove it
            del self._cache[key]
            self._misses += 1
            logger.debug(f"[RAG] Cache entry expired for query: '{query[:50]}...'")
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        self._hits += 1
        logger.info(f"[RAG] Cache HIT for query: '{query[:50]}...'")
        return entry["response"]

    def set(self, query: str, response: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> None:
        """
        Store a response in the cache.

        Args:
            query: Search query string
            response: RAG pipeline response dict
            filters: Optional metadata filters dict
        """
        if not self.enabled:
            return

        key = self._make_key(query, filters)

        # Evict oldest if at capacity
        while len(self._cache) >= self.max_entries:
            evicted_key, _ = self._cache.popitem(last=False)
            logger.debug(f"[RAG] Cache evicted oldest entry (key={evicted_key[:16]}...)")

        self._cache[key] = {
            "response": response,
            "timestamp": time.time()
        }
        logger.debug(f"[RAG] Cached response for query: '{query[:50]}...'")

    def invalidate(self, query: str, filters: Optional[Dict[str, Any]] = None) -> None:
        """Remove a specific entry from cache."""
        key = self._make_key(query, filters)
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        logger.info("[RAG] Response cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0.0
        return {
            "entries": len(self._cache),
            "max_entries": self.max_entries,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate_percent": round(hit_rate, 1),
            "ttl_seconds": self.ttl_seconds,
            "enabled": self.enabled
        }


# Global response cache
response_cache = ResponseCache()
