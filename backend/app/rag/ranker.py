"""
📊 Result ranking strategies to re-order retrieved chunks before context injection.
"""

from typing import List, Dict, Any
from app.utils.logger import logger
from app.utils.config import config


class ResultRanker:
    """Re-ranks retrieved chunks using configurable ranking strategies."""

    def __init__(self, strategy: str = None):
        """
        Initialize the result ranker.

        Args:
            strategy: Ranking strategy name. Options:
                - "score_based" (default): Sort by raw cosine similarity
                - "recency_bias": Boost recent documents by metadata year
                - "diversity_aware": Penalize chunks from the same page to diversify context
        """
        self.strategy = strategy or config.rag_ranker_strategy
        logger.info(f"[RAG] ResultRanker initialized (strategy='{self.strategy}')")

    def rank(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Re-rank retrieved results using the configured strategy.

        Args:
            results: List of chunk dicts with 'score', 'text', 'metadata', 'chunk_id'

        Returns:
            Re-ordered list of chunk dicts
        """
        if not results:
            return []

        if self.strategy == "recency_bias":
            return self._rank_recency_bias(results)
        elif self.strategy == "diversity_aware":
            return self._rank_diversity_aware(results)
        else:
            return self._rank_score_based(results)

    def _rank_score_based(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort by raw similarity score descending."""
        ranked = sorted(results, key=lambda x: x.get("score", 0.0), reverse=True)
        logger.debug(f"[RAG] Score-based ranking applied to {len(ranked)} results")
        return ranked

    def _rank_recency_bias(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Boost results from more recent documents.

        Applies a bonus multiplier based on the 'year' metadata field.
        More recent years receive a higher boost (up to 10% bonus).
        """
        import datetime
        current_year = datetime.datetime.now().year

        scored = []
        for r in results:
            base_score = r.get("score", 0.0)
            year = r.get("metadata", {}).get("year")

            if year and isinstance(year, (int, float)):
                # Years closer to current get a bigger boost (max +10%)
                years_ago = max(0, current_year - int(year))
                recency_boost = max(0.0, 0.10 - (years_ago * 0.02))
            else:
                recency_boost = 0.0

            adjusted_score = min(1.0, base_score + recency_boost)
            entry = dict(r)
            entry["score"] = adjusted_score
            scored.append(entry)

        ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
        logger.debug(f"[RAG] Recency-bias ranking applied to {len(ranked)} results")
        return ranked

    def _rank_diversity_aware(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Penalize chunks from the same page/document to diversify context.

        Applies a small score penalty for each previously selected chunk from the
        same document+page combination to encourage diversity.
        """
        if not results:
            return []

        # Sort by base score first
        sorted_results = sorted(results, key=lambda x: x.get("score", 0.0), reverse=True)

        selected = []
        seen_pages: Dict[str, int] = {}  # "doc_id:page" -> count

        for r in sorted_results:
            metadata = r.get("metadata", {})
            doc_id = metadata.get("document_id", "unknown")
            page = metadata.get("page_number", 0)
            page_key = f"{doc_id}:{page}"

            # Apply penalty for repeated page
            repetitions = seen_pages.get(page_key, 0)
            penalty = repetitions * 0.05  # 5% penalty per repeat

            entry = dict(r)
            entry["score"] = max(0.0, r.get("score", 0.0) - penalty)
            selected.append(entry)

            seen_pages[page_key] = repetitions + 1

        # Re-sort after penalties
        ranked = sorted(selected, key=lambda x: x["score"], reverse=True)
        logger.debug(f"[RAG] Diversity-aware ranking applied to {len(ranked)} results")
        return ranked
