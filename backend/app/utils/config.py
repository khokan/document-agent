"""
Configuration loader for the PDF Knowledge Assistant.

Loads configuration from config.yaml and environment variables.
Environment variables take precedence over config.yaml.
"""

import os
import hashlib
import json
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


class Config:
    """Configuration management for the PDF Knowledge Assistant."""

    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize configuration loader.

        Args:
            config_file: Path to the configuration YAML file.
        """
        # Load environment variables from .env
        load_dotenv()

        # Load config from YAML
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, "r") as f:
                self._config: Dict[str, Any] = yaml.safe_load(f) or {}
        else:
            self._config = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with dot notation support.

        Args:
            key: Configuration key (supports nested access with dots, e.g., "app.name")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_from_env(self, env_key: str, default: Any = None) -> Any:
        """
        Get value from environment variable.

        Args:
            env_key: Environment variable name
            default: Default value if not found

        Returns:
            Environment variable value
        """
        return os.getenv(env_key, default)

    @property
    def app_name(self) -> str:
        """Get application name."""
        return self.get("app.name", "PDF Knowledge Assistant")

    @property
    def app_version(self) -> str:
        """Get application version."""
        return self.get("app.version", "1.0.0")

    @property
    def app_debug(self) -> bool:
        """Get debug mode flag."""
        return self.get("app.debug", False)

    @property
    def pdf_max_size_mb(self) -> int:
        """Get max PDF upload size in MB."""
        return self.get("pdf.max_size_mb", 100)

    @property
    def pdf_allowed_extensions(self) -> list:
        """Get allowed PDF extensions."""
        return self.get("pdf.allowed_extensions", [".pdf"])

    @property
    def chunk_size(self) -> int:
        """Get chunk size in words."""
        return self.get("chunking.chunk_size", 500)

    @property
    def chunk_overlap(self) -> int:
        """Get chunk overlap in words."""
        return self.get("chunking.chunk_overlap", 100)

    @property
    def min_chunk_size(self) -> int:
        """Get minimum chunk size in words."""
        return self.get("chunking.min_chunk_size", 50)

    @property
    def active_ai_profile(self) -> str:
        return self.get_from_env("AI_ACTIVE_PROFILE") or self.get("ai.active_profile", "local")

    @property
    def ai_profile(self) -> Dict[str, Any]:
        profile = self.get(f"ai.profiles.{self.active_ai_profile}")
        if not isinstance(profile, dict):
            raise ValueError(f"AI profile '{self.active_ai_profile}' is not configured")
        return profile

    @property
    def chat_settings(self) -> Dict[str, Any]:
        settings = self.ai_profile.get("chat")
        if not isinstance(settings, dict):
            raise ValueError(f"AI profile '{self.active_ai_profile}' has no chat settings")
        return settings

    @property
    def embedding_settings(self) -> Dict[str, Any]:
        settings = self.ai_profile.get("embeddings")
        if not isinstance(settings, dict):
            raise ValueError(f"AI profile '{self.active_ai_profile}' has no embedding settings")
        return settings

    @property
    def embedding_profile_fingerprint(self) -> str:
        settings = self.embedding_settings
        safe_settings = {key: settings.get(key) for key in ("provider", "model", "base_url", "dimension")}
        encoded = json.dumps(safe_settings, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()[:16]

    @property
    def embedding_model(self) -> str:
        """Get embedding model name."""
        return self.embedding_settings["model"]

    @property
    def embedding_dimension(self) -> int:
        """Get embedding dimension."""
        return int(self.embedding_settings["dimension"])

    @property
    def chroma_collection_name(self) -> str:
        """Get ChromaDB collection name."""
        return self.get("chromadb.collection_name", "company_documents")

    @property
    def chroma_persist_directory(self) -> str:
        """Get ChromaDB persist directory."""
        return self.get("chromadb.persist_directory", "./chroma_db")

    @property
    def chroma_distance_metric(self) -> str:
        """Get ChromaDB distance metric."""
        return self.get("chromadb.distance_metric", "cosine")

    @property
    def llm_model(self) -> str:
        """Get LLM model name."""
        return self.get("llm.model", "mistral")

    @property
    def llm_temperature(self) -> float:
        """Get LLM temperature."""
        return self.get("llm.temperature", 0.1)

    @property
    def llm_max_tokens(self) -> int:
        """Get LLM max tokens."""
        return self.get("llm.max_tokens", 500)

    @property
    def llm_timeout_seconds(self) -> int:
        """Get LLM timeout in seconds."""
        return self.get("llm.timeout_seconds", 30)

    @property
    def search_top_k(self) -> int:
        """Get search top K results."""
        return self.get("search.top_k", 5)

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get_from_env("LOG_LEVEL") or self.get("logging.level", "INFO")

    @property
    def log_file(self) -> str:
        """Get log file path."""
        return self.get_from_env("LOG_FILE") or self.get("logging.file", "./logs/app.log")

    @property
    def upload_dir(self) -> str:
        """Get upload directory path."""
        return self.get_from_env("UPLOAD_DIR") or "./uploads/pdfs"

    @property
    def temp_dir(self) -> str:
        """Get temp directory path."""
        return self.get_from_env("TEMP_DIR") or "./uploads/temp"

    @property
    def chunking_strategy(self) -> str:
        """Get chunking strategy."""
        return self.get("chunking.strategy", "recursive")

    @property
    def cache_embeddings(self) -> bool:
        """Get cache embeddings flag."""
        return self.get("embeddings.cache_embeddings", True)

    @property
    def rag_retriever_k(self) -> int:
        """Get retriever K value."""
        return self.get("rag.retriever.k", 5)

    @property
    def rag_retriever_score_threshold(self) -> float:
        """Get retriever score threshold."""
        return self.get("rag.retriever.score_threshold", 0.3)

    @property
    def rag_generator_model(self) -> str:
        """Get generator LLM model."""
        return self.chat_settings["model"]

    @property
    def rag_generator_temperature(self) -> float:
        """Get generator LLM temperature."""
        return float(self.chat_settings.get("temperature", self.get("rag.generator.temperature", 0.7)))

    @property
    def rag_generator_max_tokens(self) -> int:
        """Get generator LLM max tokens."""
        return int(self.chat_settings.get("max_tokens", self.get("rag.generator.max_tokens", 500)))

    @property
    def rag_generator_timeout_seconds(self) -> int:
        """Get generator LLM timeout in seconds."""
        return int(self.chat_settings.get("timeout_seconds", self.get("rag.generator.timeout_seconds", 120)))

    @property
    def rag_generator_system_prompt(self) -> str:
        """Get generator system prompt template."""
        return self.get(
            "rag.generator.system_prompt",
            "You are a professional PDF Knowledge Assistant. Answer the user's question "
            "using ONLY the provided document context sections below. If the context does "
            "not contain the answer, politely state that you do not have sufficient information to answer."
        )

    @property
    def rag_ranker_strategy(self) -> str:
        """Get retrieval result ranking strategy."""
        return self.get("rag.ranker.strategy", "score_based")

    @property
    def rag_cache_enabled(self) -> bool:
        """Get RAG response cache enabled flag."""
        return self.get("rag.cache.enabled", True)

    @property
    def rag_cache_max_entries(self) -> int:
        """Get RAG response cache max entries."""
        return self.get("rag.cache.max_entries", 100)

    @property
    def rag_cache_ttl_seconds(self) -> int:
        """Get RAG response cache TTL in seconds."""
        return self.get("rag.cache.ttl_seconds", 3600)

    @property
    def database_url(self) -> str:
        """Get database URL for chat persistence."""
        return self.get_from_env("DATABASE_URL") or self.get(
            "database.url", "sqlite:///./data/chat.db"
        )


# Global config instance
config = Config()
