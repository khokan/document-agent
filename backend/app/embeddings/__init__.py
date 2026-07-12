"""
🚀 Embeddings module exposing the client, service, and cache.
"""

from app.embeddings.client import OllamaClient
from app.embeddings.ollama_service import OllamaEmbeddingService
from app.embeddings.cache import embedding_cache

__all__ = [
    "OllamaClient",
    "OllamaEmbeddingService",
    "embedding_cache",
]
