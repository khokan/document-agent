"""
🧠 Embedding generator service using local Ollama nomic-embed-text model.
"""

import asyncio
from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config
from app.embeddings.client import OllamaClient


class OllamaEmbeddingService:
    """Service to handle embedding generation using local Ollama models."""

    def __init__(self, client: Optional[OllamaClient] = None):
        self.client = client or OllamaClient()
        self.model = config.embedding_model
        logger.info(f"[EMBEDDINGS] OllamaEmbeddingService initialized (model={self.model})")

    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate dense vector embedding for a single text chunk.

        Args:
            text: Input text chunk

        Returns:
            List of floats representing the embedding vector
        """
        try:
            payload = {
                "model": self.model,
                "prompt": text
            }
            res = await self.client.post("/api/embeddings", payload)
            data = res.json()
            if "embedding" in data:
                return data["embedding"]
            else:
                raise ValueError(f"Ollama response missing 'embedding' field: {data}")
        except Exception as e:
            logger.error(f"[ERR] Failed to generate embedding for text: {str(e)}")
            raise

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks (batch).

        Tries the newer batch endpoint `/api/embed` first, then falls back to `/api/embeddings`.

        Args:
            texts: List of input text chunks

        Returns:
            List of embedding vectors (list of list of floats)
        """
        if not texts:
            return []

        # Try Ollama's newer batch API first (/api/embed)
        try:
            payload = {
                "model": self.model,
                "input": texts
            }
            res = await self.client.post("/api/embed", payload)
            data = res.json()
            if "embeddings" in data:
                return data["embeddings"]
        except Exception as e:
            # Fall back to sequential/concurrent requests to /api/embeddings
            logger.debug(f"[EMBEDDINGS] Batch /api/embed failed ({str(e)}), falling back to /api/embeddings")

        # Concurrently request embeddings for each text
        tasks = [self.get_embedding(text) for text in texts]
        return await asyncio.gather(*tasks)
