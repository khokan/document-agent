"""
🤖 Response generation logic using local Ollama model (e.g. Mistral).
"""

from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config
from app.embeddings.client import OllamaClient


class Generator:
    """Generates context-aware answers using a local Ollama Large Language Model."""

    def __init__(self, client: Optional[OllamaClient] = None):
        self.client = client or OllamaClient()
        self.model = config.rag_generator_model
        self.temperature = config.rag_generator_temperature
        self.max_tokens = config.rag_generator_max_tokens

        logger.info(
            f"[RAG] Generator initialized (model={self.model}, "
            f"temperature={self.temperature}, max_tokens={self.max_tokens})"
        )

    def _build_prompt(self, query: str, context_chunks: List[str]) -> str:
        """Construct prompt with context instructions."""
        joined_context = "\n\n---\n\n".join(context_chunks)
        
        prompt = (
            "You are a professional PDF Knowledge Assistant. Answer the user's question using ONLY the provided document context sections below. "
            "If the context does not contain the answer, politely state that you do not have sufficient information to answer.\n\n"
            "Context Sections:\n"
            f"{joined_context}\n\n"
            "User Question:\n"
            f"{query}\n\n"
            "Response (Be concise, accurate, and cite information when appropriate):"
        )
        return prompt

    async def generate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Generate answer from local LLM using the provided query and retrieved context chunks.

        Args:
            query: Question/search query
            context: List of matched chunk dicts containing 'text'

        Returns:
            String representing the LLM's generated response
        """
        if not context:
            return "I was unable to find any relevant document context to answer your question."

        context_texts = [c["text"] for c in context]
        prompt = self._build_prompt(query, context_texts)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            }
        }

        logger.info(f"[RAG] Generating response using model: '{self.model}'")
        
        try:
            res = await self.client.post("/api/generate", payload)
            data = res.json()
            if "response" in data:
                return data["response"].strip()
            else:
                raise ValueError(f"Ollama generation response missing 'response' field: {data}")
        except Exception as e:
            logger.error(f"[ERR] Failed during LLM response generation: {str(e)}")
            return f"An error occurred while generating the response: {str(e)}"
