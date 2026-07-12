"""
🧪 Unit tests for ResponseCache LRU cache with TTL.
"""

import time
import unittest
from app.rag.cache import ResponseCache


class TestResponseCacheBasics(unittest.TestCase):
    """Test basic cache set/get operations."""

    def setUp(self):
        self.cache = ResponseCache(enabled=True, max_entries=5, ttl_seconds=60)

    def test_set_and_get(self):
        response = {"answer": "42", "sources": []}
        self.cache.set("meaning of life", response)

        result = self.cache.get("meaning of life")
        self.assertIsNotNone(result)
        self.assertEqual(result["answer"], "42")

    def test_cache_miss(self):
        result = self.cache.get("nonexistent query")
        self.assertIsNone(result)

    def test_case_insensitive_keys(self):
        response = {"answer": "test"}
        self.cache.set("Hello World", response)

        # Same query with different case should hit cache
        result = self.cache.get("hello world")
        self.assertIsNotNone(result)
        self.assertEqual(result["answer"], "test")

    def test_filters_affect_key(self):
        response_a = {"answer": "A"}
        response_b = {"answer": "B"}

        self.cache.set("revenue", response_a, filters={"company": "Acme"})
        self.cache.set("revenue", response_b, filters={"company": "Beta"})

        result_a = self.cache.get("revenue", filters={"company": "Acme"})
        result_b = self.cache.get("revenue", filters={"company": "Beta"})

        self.assertEqual(result_a["answer"], "A")
        self.assertEqual(result_b["answer"], "B")


class TestResponseCacheTTL(unittest.TestCase):
    """Test TTL expiry behavior."""

    def test_expired_entry_returns_none(self):
        cache = ResponseCache(enabled=True, max_entries=5, ttl_seconds=1)
        cache.set("test", {"answer": "stale"})

        # Wait for TTL to expire
        time.sleep(1.1)

        result = cache.get("test")
        self.assertIsNone(result)

    def test_non_expired_entry_returns_value(self):
        cache = ResponseCache(enabled=True, max_entries=5, ttl_seconds=60)
        cache.set("test", {"answer": "fresh"})

        result = cache.get("test")
        self.assertIsNotNone(result)
        self.assertEqual(result["answer"], "fresh")


class TestResponseCacheEviction(unittest.TestCase):
    """Test LRU eviction when max_entries is reached."""

    def test_evicts_oldest_entry(self):
        cache = ResponseCache(enabled=True, max_entries=3, ttl_seconds=60)

        cache.set("query1", {"answer": "1"})
        cache.set("query2", {"answer": "2"})
        cache.set("query3", {"answer": "3"})

        # This should evict query1 (oldest)
        cache.set("query4", {"answer": "4"})

        self.assertIsNone(cache.get("query1"))
        self.assertIsNotNone(cache.get("query2"))
        self.assertIsNotNone(cache.get("query3"))
        self.assertIsNotNone(cache.get("query4"))

    def test_access_refreshes_position(self):
        cache = ResponseCache(enabled=True, max_entries=3, ttl_seconds=60)

        cache.set("query1", {"answer": "1"})
        cache.set("query2", {"answer": "2"})
        cache.set("query3", {"answer": "3"})

        # Access query1 to make it most recently used
        cache.get("query1")

        # Now add query4 — should evict query2 (oldest unreferenced)
        cache.set("query4", {"answer": "4"})

        self.assertIsNotNone(cache.get("query1"))  # Still alive (was accessed)
        self.assertIsNone(cache.get("query2"))      # Evicted
        self.assertIsNotNone(cache.get("query3"))
        self.assertIsNotNone(cache.get("query4"))


class TestResponseCacheDisabled(unittest.TestCase):
    """Test behavior when cache is disabled."""

    def test_disabled_cache_always_misses(self):
        cache = ResponseCache(enabled=False)
        cache.set("test", {"answer": "ignored"})
        result = cache.get("test")
        self.assertIsNone(result)


class TestResponseCacheStats(unittest.TestCase):
    """Test cache statistics tracking."""

    def test_stats_tracking(self):
        cache = ResponseCache(enabled=True, max_entries=10, ttl_seconds=60)

        cache.set("q1", {"answer": "1"})
        cache.get("q1")  # Hit
        cache.get("q2")  # Miss

        stats = cache.get_stats()
        self.assertEqual(stats["entries"], 1)
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate_percent"], 50.0)

    def test_clear_cache(self):
        cache = ResponseCache(enabled=True, max_entries=10, ttl_seconds=60)
        cache.set("q1", {"answer": "1"})
        cache.set("q2", {"answer": "2"})
        cache.clear()

        stats = cache.get_stats()
        self.assertEqual(stats["entries"], 0)

    def test_invalidate_specific_entry(self):
        cache = ResponseCache(enabled=True, max_entries=10, ttl_seconds=60)
        cache.set("q1", {"answer": "1"})
        cache.set("q2", {"answer": "2"})

        cache.invalidate("q1")
        self.assertIsNone(cache.get("q1"))
        self.assertIsNotNone(cache.get("q2"))
