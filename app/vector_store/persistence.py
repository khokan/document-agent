"""
💾 Persistence management for ChromaDB vector store.
"""

import os
from app.utils.logger import logger
from app.utils.config import config
from app.vector_store.chromadb_service import ChromaDBService


class PersistenceManager:
    """Manages database directories and validation checks for ChromaDB."""

    def __init__(self, service: ChromaDBService):
        self.service = service
        self.db_path = config.chroma_persist_directory

    def verify_persistence(self) -> bool:
        """
        Verify that ChromaDB data is persisted on disk and the folder exists.
        """
        exists = os.path.exists(self.db_path)
        if not exists:
            logger.warning(f"[WARN] ChromaDB directory '{self.db_path}' does not exist yet.")
            return False

        files = os.listdir(self.db_path)
        logger.info(f"[PERSISTENCE] ChromaDB directory contains {len(files)} files/folders.")
        return len(files) > 0
