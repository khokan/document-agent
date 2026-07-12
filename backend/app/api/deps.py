"""
🔗 API dependency provider, initializing services as singletons.
"""

from app.vector_store.chromadb_service import ChromaDBService
from app.embeddings.ollama_service import OllamaEmbeddingService
from app.rag.retriever import Retriever
from app.rag.generator import Generator
from app.rag.ranker import ResultRanker
from app.rag.cache import response_cache
from app.rag.pipeline import RAGPipeline

# Initialize singletons
vector_service = ChromaDBService()
embedding_service = OllamaEmbeddingService()
retriever_service = Retriever(embedding_service, vector_service)
generator_service = Generator()
ranker_service = ResultRanker()
rag_pipeline = RAGPipeline(
    retriever=retriever_service,
    generator=generator_service,
    ranker=ranker_service,
    cache=response_cache
)


def get_vector_service() -> ChromaDBService:
    return vector_service


def get_embedding_service() -> OllamaEmbeddingService:
    return embedding_service


def get_retriever_service() -> Retriever:
    return retriever_service


def get_generator_service() -> Generator:
    return generator_service


def get_ranker_service() -> ResultRanker:
    return ranker_service


def get_rag_pipeline() -> RAGPipeline:
    return rag_pipeline
