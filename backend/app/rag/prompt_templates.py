"""
📝 Prompt templates for RAG pipeline response generation.
"""

from typing import List, Dict, Any, Optional
from app.utils.logger import logger
from app.utils.config import config


class PromptTemplate:
    """Manages prompt template rendering with variable injection."""

    # -- Predefined Templates --

    QA_TEMPLATE = (
        "Context Sections:\n"
        "{context}\n\n"
        "User Question:\n"
        "{question}\n\n"
        "Response (Be concise, accurate, and cite information when appropriate):"
    )

    SUMMARY_TEMPLATE = (
        "You are a professional document summarizer. Provide a clear and comprehensive "
        "summary of the following document sections. Focus on key points, findings, and "
        "conclusions. Use bullet points where appropriate.\n\n"
        "Document Sections:\n"
        "{context}\n\n"
        "Summary:"
    )

    CHAT_TEMPLATE = (
        "Conversation History:\n"
        "{history}\n\n"
        "Context Sections:\n"
        "{context}\n\n"
        "User Message:\n"
        "{question}\n\n"
        "Assistant Response:"
    )

    def __init__(self, template: Optional[str] = None):
        """
        Initialize with a custom template or use the QA template by default.

        Args:
            template: Custom template string with {placeholders}
        """
        self.template = template or self.QA_TEMPLATE
        self.system_prompt = config.rag_generator_system_prompt

    def render(self, **kwargs) -> str:
        """
        Render the template by injecting variables.

        Args:
            **kwargs: Variables to inject (e.g., context, question, history)

        Returns:
            Rendered prompt string
        """
        # Inject system prompt if not provided
        if "system_prompt" not in kwargs:
            kwargs["system_prompt"] = self.system_prompt

        try:
            rendered = self.template.format(**kwargs)
            logger.debug(f"[RAG] Prompt rendered ({len(rendered)} chars)")
            return rendered
        except KeyError as e:
            logger.error(f"[ERR] Missing template variable: {e}")
            raise ValueError(f"Missing required template variable: {e}")

    @classmethod
    def build_qa_prompt(cls, question: str, context_chunks: List[str]) -> str:
        """
        Build a question-answering prompt from question and context chunks.

        Args:
            question: User's question
            context_chunks: List of context text strings

        Returns:
            Rendered QA prompt string
        """
        joined_context = "\n\n---\n\n".join(context_chunks)
        template = cls(cls.QA_TEMPLATE)
        return template.render(context=joined_context, question=question)

    @classmethod
    def build_summary_prompt(cls, context_chunks: List[str]) -> str:
        """
        Build a document summarization prompt from context chunks.

        Args:
            context_chunks: List of document text strings

        Returns:
            Rendered summary prompt string
        """
        joined_context = "\n\n---\n\n".join(context_chunks)
        template = cls(cls.SUMMARY_TEMPLATE)
        return template.render(context=joined_context)

    @classmethod
    def build_chat_prompt(
        cls,
        question: str,
        context_chunks: List[str],
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Build a multi-turn conversation prompt with history and context.

        Args:
            question: User's current message
            context_chunks: List of context text strings
            history: List of previous messages [{"role": "user"/"assistant", "content": "..."}]

        Returns:
            Rendered chat prompt string
        """
        joined_context = "\n\n---\n\n".join(context_chunks)

        # Format conversation history
        if history:
            formatted_history = "\n".join(
                f"{msg.get('role', 'user').capitalize()}: {msg.get('content', '')}"
                for msg in history
            )
        else:
            formatted_history = "(No previous conversation)"

        template = cls(cls.CHAT_TEMPLATE)
        return template.render(
            context=joined_context,
            question=question,
            history=formatted_history
        )
