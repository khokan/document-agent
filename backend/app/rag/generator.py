"""Provider-neutral response generation using LangChain chat models."""

from typing import Any, AsyncGenerator, Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from app.ai.factory import create_chat_model
from app.rag.prompt_templates import PromptTemplate
from app.utils.config import config
from app.utils.logger import logger


def _content(value: Any) -> str:
    """Normalize LangChain string/list content into API-safe text."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in value)
    return str(value or "")


class Generator:
    """Generates RAG answers through a configured LangChain BaseChatModel."""

    def __init__(self, chat_model=None):
        self.chat_model = chat_model or create_chat_model()
        self.model = config.rag_generator_model
        self.timeout_seconds = config.rag_generator_timeout_seconds
        logger.info("[RAG] Generator initialized (profile=%s, model=%s)", config.active_ai_profile, self.model)

    def _messages(self, prompt: str) -> List[BaseMessage]:
        return [SystemMessage(content=config.rag_generator_system_prompt), HumanMessage(content=prompt)]

    async def generate_response(self, query: str, context: List[Dict[str, Any]], history: Optional[List[Dict[str, str]]] = None) -> str:
        if not context:
            return "I was unable to find any relevant document context to answer your question."
        texts = [chunk["text"] for chunk in context]
        prompt = (PromptTemplate.build_chat_prompt(query, texts, history) if history
                  else PromptTemplate.build_qa_prompt(query, texts))
        try:
            response: AIMessage = await self.chat_model.ainvoke(self._messages(prompt))
            return _content(response.content).strip()
        except Exception as exc:
            logger.exception("[RAG] Provider failed during response generation")
            raise RuntimeError("The configured chat provider could not generate a response.") from exc

    async def generate_summary(self, context: List[Dict[str, Any]]) -> str:
        if not context:
            return "No document content available to summarize."
        prompt = PromptTemplate.build_summary_prompt([chunk["text"] for chunk in context])
        try:
            response: AIMessage = await self.chat_model.ainvoke(self._messages(prompt))
            return _content(response.content).strip()
        except Exception as exc:
            logger.exception("[RAG] Provider failed during summarization")
            raise RuntimeError("The configured chat provider could not generate a summary.") from exc

    async def generate_streaming_response(self, query: str, context: List[Dict[str, Any]]) -> AsyncGenerator[str, None]:
        if not context:
            yield "I was unable to find any relevant document context to answer your question."
            return
        prompt = PromptTemplate.build_qa_prompt(query, [chunk["text"] for chunk in context])
        try:
            async for chunk in self.chat_model.astream(self._messages(prompt)):
                text = _content(chunk.content)
                if text:
                    yield text
        except Exception as exc:
            logger.exception("[RAG] Provider failed during streaming")
            raise RuntimeError("The configured chat provider could not stream a response.") from exc
