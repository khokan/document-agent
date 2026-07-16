"""
🤖 Response generation logic using local Ollama model (e.g. Mistral).
"""

import asyncio
import httpx
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.utils.logger import logger
from app.utils.config import config
from app.embeddings.client import OllamaClient
from app.rag.prompt_templates import PromptTemplate


class Generator:
    """Generates context-aware answers using a local Ollama Large Language Model."""

    def __init__(self, client: Optional[OllamaClient] = None):
        self.client = client or OllamaClient()
        self.model = config.rag_generator_model
        self.temperature = config.rag_generator_temperature
        self.max_tokens = config.rag_generator_max_tokens
        self.timeout_seconds = config.rag_generator_timeout_seconds

        logger.info(
            f"[RAG] Generator initialized (model={self.model}, "
            f"temperature={self.temperature}, max_tokens={self.max_tokens}, "
            f"timeout={self.timeout_seconds}s)"
        )

    def _build_prompt(self, query: str, context_chunks: List[str]) -> str:
        """Construct prompt with context instructions using template system."""
        return PromptTemplate.build_qa_prompt(query, context_chunks)

    def _build_chat_prompt(
        self,
        query: str,
        context_chunks: List[str],
        history: List[Dict[str, str]] = None
    ) -> str:
        """Construct multi-turn chat prompt with conversation history."""
        return PromptTemplate.build_chat_prompt(query, context_chunks, history)

    def _build_summary_prompt(self, context_chunks: List[str]) -> str:
        """Construct summarization prompt."""
        return PromptTemplate.build_summary_prompt(context_chunks)

    async def _post_to_llm(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post to Ollama with the generator's timeout, bypassing OllamaClient."""
        url = f"{self.client.base_url.rstrip('/')}/api/generate"
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(float(self.timeout_seconds))
        ) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    async def generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]],
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate answer from local LLM using the provided query and retrieved context chunks.

        Args:
            query: Question/search query
            context: List of matched chunk dicts containing 'text'
            history: Optional conversation history for multi-turn chat

        Returns:
            String representing the LLM's generated response
        """
        if not context:
            return "I was unable to find any relevant document context to answer your question."

        context_texts = [c["text"] for c in context]

        # Choose prompt based on whether we have conversation history
        if history:
            prompt = self._build_chat_prompt(query, context_texts, history)
        else:
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
            data = await asyncio.wait_for(
                self._post_to_llm(payload),
                timeout=self.timeout_seconds
            )
            if "response" in data:
                return data["response"].strip()
            else:
                raise ValueError(f"Ollama generation response missing 'response' field: {data}")
        except (asyncio.TimeoutError, httpx.TimeoutError):
            logger.error(f"[ERR] LLM generation timed out after {self.timeout_seconds}s")
            return (
                f"The request timed out after {self.timeout_seconds} seconds. "
                "Please try a simpler question or try again later."
            )
        except Exception as e:
            logger.error(f"[ERR] Failed during LLM response generation: {str(e)}")
            return f"An error occurred while generating the response: {str(e)}"

    async def generate_summary(self, context: List[Dict[str, Any]]) -> str:
        """
        Generate a summary from document context chunks.

        Args:
            context: List of chunk dicts containing 'text'

        Returns:
            Summary string
        """
        if not context:
            return "No document content available to summarize."

        context_texts = [c["text"] for c in context]
        prompt = self._build_summary_prompt(context_texts)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for factual summaries
                "num_predict": self.max_tokens,
            }
        }

        logger.info(f"[RAG] Generating summary using model: '{self.model}'")

        try:
            data = await asyncio.wait_for(
                self._post_to_llm(payload),
                timeout=self.timeout_seconds
            )
            if "response" in data:
                return data["response"].strip()
            else:
                raise ValueError(f"Ollama response missing 'response' field: {data}")
        except (asyncio.TimeoutError, httpx.TimeoutError):
            logger.error(f"[ERR] Summary generation timed out after {self.timeout_seconds}s")
            return f"Summary generation timed out after {self.timeout_seconds} seconds."
        except Exception as e:
            logger.error(f"[ERR] Failed during summary generation: {str(e)}")
            return f"An error occurred while generating the summary: {str(e)}"

    async def generate_streaming_response(
        self,
        query: str,
        context: List[Dict[str, Any]]
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM for Server-Sent Events (SSE).

        Args:
            query: Question/search query
            context: List of matched chunk dicts containing 'text'

        Yields:
            String tokens as they are generated
        """
        if not context:
            yield "I was unable to find any relevant document context to answer your question."
            return

        context_texts = [c["text"] for c in context]
        prompt = self._build_prompt(query, context_texts)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            }
        }

        logger.info(f"[RAG] Streaming response using model: '{self.model}'")

        url = f"{self.client.base_url.rstrip('/')}/api/generate"

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(float(self.timeout_seconds))) as client:
                async with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                            if data.get("done", False):
                                break
        except (asyncio.TimeoutError, httpx.TimeoutError):
            logger.error(f"[ERR] Streaming timed out after {self.timeout_seconds}s")
            yield f"\n[Timeout after {self.timeout_seconds}s]"
        except Exception as e:
            logger.error(f"[ERR] Streaming error: {str(e)}")
            yield f"\n[Error: {str(e)}]"
