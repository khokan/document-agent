"""
📂 Collection management utilities for ChromaDB.
"""

from typing import List
from app.utils.logger import logger
from app.vector_store.chromadb_service import ChromaDBService


class CollectionManager:
    """Manages collection lifecycle in ChromaDB."""

    def __init__(self, service: ChromaDBService):
        self.service = service

    def list_collections(self) -> List[str]:
        """List all collection names."""
        collections = self.service.client.list_collections()
        return [c.name for c in collections]

    def delete_collection(self, name: str) -> None:
        """Delete a collection by name."""
        try:
            self.service.client.delete_collection(name)
            logger.info(f"[OK] Collection '{name}' deleted successfully.")
        except Exception as e:
            logger.error(f"[ERR] Failed to delete collection '{name}': {str(e)}")

    def reset_database(self) -> None:
        """Reset database client state (dangerous - clears all collections)."""
        try:
            self.service.client.reset()
            logger.info("[OK] ChromaDB client state reset.")
        except Exception as e:
            logger.error(f"[ERR] Failed to reset ChromaDB client: {str(e)}")
            # Falls back to deleting the current collection
            self.delete_collection(self.service.collection_name)
            self.service.collection = self.service.client.get_or_create_collection(
                name=self.service.collection_name,
                metadata={"hnsw:space": self.service.distance_metric}
            )
