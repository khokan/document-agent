"""Singleton services built from the active LangChain provider profile."""

from app.ai.factory import create_chat_model, create_embeddings
from app.rag.cache import response_cache
from app.rag.generator import Generator
from app.rag.pipeline import RAGPipeline
from app.rag.ranker import ResultRanker
from app.rag.retriever import Retriever
from app.vector_store.chromadb_service import ChromaDBService

vector_service = ChromaDBService()
embedding_service = create_embeddings()
retriever_service = Retriever(embedding_service, vector_service)
generator_service = Generator(chat_model=create_chat_model())
ranker_service = ResultRanker()
rag_pipeline = RAGPipeline(retriever_service, generator_service, ranker_service, response_cache)


def get_vector_service(): return vector_service
def get_embedding_service(): return embedding_service
def get_retriever_service(): return retriever_service
def get_generator_service(): return generator_service
def get_ranker_service(): return ranker_service
def get_rag_pipeline(): return rag_pipeline
