"""
🧪 Unit tests for ResultRanker ranking strategies.
"""

import unittest
from app.rag.ranker import ResultRanker


class TestScoreBasedRanking(unittest.TestCase):
    """Test the default score-based ranking strategy."""

    def test_sorts_by_score_descending(self):
        ranker = ResultRanker(strategy="score_based")
        results = [
            {"chunk_id": "c1", "text": "low", "score": 0.5, "metadata": {}},
            {"chunk_id": "c2", "text": "high", "score": 0.95, "metadata": {}},
            {"chunk_id": "c3", "text": "mid", "score": 0.75, "metadata": {}},
        ]
        ranked = ranker.rank(results)
        self.assertEqual(ranked[0]["chunk_id"], "c2")
        self.assertEqual(ranked[1]["chunk_id"], "c3")
        self.assertEqual(ranked[2]["chunk_id"], "c1")

    def test_empty_input(self):
        ranker = ResultRanker(strategy="score_based")
        self.assertEqual(ranker.rank([]), [])

    def test_single_result(self):
        ranker = ResultRanker(strategy="score_based")
        results = [{"chunk_id": "c1", "text": "only", "score": 0.8, "metadata": {}}]
        ranked = ranker.rank(results)
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["score"], 0.8)


class TestRecencyBiasRanking(unittest.TestCase):
    """Test the recency bias ranking strategy."""

    def test_boosts_recent_documents(self):
        ranker = ResultRanker(strategy="recency_bias")
        import datetime
        current_year = datetime.datetime.now().year

        results = [
            {"chunk_id": "old", "text": "old doc", "score": 0.80,
             "metadata": {"year": current_year - 5}},
            {"chunk_id": "new", "text": "new doc", "score": 0.80,
             "metadata": {"year": current_year}},
        ]
        ranked = ranker.rank(results)

        # New document should rank higher due to recency boost
        self.assertEqual(ranked[0]["chunk_id"], "new")
        self.assertGreater(ranked[0]["score"], ranked[1]["score"])

    def test_missing_year_no_crash(self):
        ranker = ResultRanker(strategy="recency_bias")
        results = [
            {"chunk_id": "c1", "text": "no year", "score": 0.7, "metadata": {}},
        ]
        ranked = ranker.rank(results)
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["score"], 0.7)  # No boost applied

    def test_score_capped_at_one(self):
        ranker = ResultRanker(strategy="recency_bias")
        import datetime
        current_year = datetime.datetime.now().year

        results = [
            {"chunk_id": "c1", "text": "high", "score": 0.99,
             "metadata": {"year": current_year}},
        ]
        ranked = ranker.rank(results)
        self.assertLessEqual(ranked[0]["score"], 1.0)


class TestDiversityAwareRanking(unittest.TestCase):
    """Test the diversity-aware ranking strategy."""

    def test_penalizes_same_page_chunks(self):
        ranker = ResultRanker(strategy="diversity_aware")
        results = [
            {"chunk_id": "c1", "text": "first", "score": 0.90,
             "metadata": {"document_id": "doc1", "page_number": 1}},
            {"chunk_id": "c2", "text": "second", "score": 0.89,
             "metadata": {"document_id": "doc1", "page_number": 1}},
            {"chunk_id": "c3", "text": "other page", "score": 0.88,
             "metadata": {"document_id": "doc1", "page_number": 2}},
        ]
        ranked = ranker.rank(results)

        # c1 should still be first (highest score, first from page 1)
        self.assertEqual(ranked[0]["chunk_id"], "c1")
        # c3 (different page, no penalty) should rank above c2 (same page, penalized)
        self.assertEqual(ranked[1]["chunk_id"], "c3")
        self.assertEqual(ranked[2]["chunk_id"], "c2")

    def test_different_documents_no_penalty(self):
        ranker = ResultRanker(strategy="diversity_aware")
        results = [
            {"chunk_id": "c1", "text": "doc1", "score": 0.85,
             "metadata": {"document_id": "doc1", "page_number": 1}},
            {"chunk_id": "c2", "text": "doc2", "score": 0.84,
             "metadata": {"document_id": "doc2", "page_number": 1}},
        ]
        ranked = ranker.rank(results)

        # No penalty since they're from different documents
        self.assertEqual(ranked[0]["chunk_id"], "c1")
        self.assertEqual(ranked[1]["chunk_id"], "c2")
        self.assertEqual(ranked[0]["score"], 0.85)
        self.assertEqual(ranked[1]["score"], 0.84)

    def test_empty_results(self):
        ranker = ResultRanker(strategy="diversity_aware")
        self.assertEqual(ranker.rank([]), [])
