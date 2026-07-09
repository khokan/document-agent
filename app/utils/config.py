"""
🔧 Configuration loader for the PDF Knowledge Assistant.

Loads configuration from config.yaml and environment variables.
Environment variables take precedence over config.yaml.
"""

import os
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
    def embedding_model(self) -> str:
        """Get embedding model name."""
        return self.get("embeddings.model", "nomic-embed-text")

    @property
    def embedding_dimension(self) -> int:
        """Get embedding dimension."""
        return self.get("embeddings.dimension", 768)

    @property
    def ollama_endpoint(self) -> str:
        """Get Ollama API endpoint."""
        return self.get_from_env("OLLAMA_BASE_URL") or self.get(
            "embeddings.ollama_endpoint", "http://localhost:11434"
        )

    @property
    def chroma_collection_name(self) -> str:
        """Get ChromaDB collection name."""
        return self.get("chromadb.collection_name", "company_documents")

    @property
    def chroma_persist_directory(self) -> str:
        """Get ChromaDB persist directory."""
        return self.get("chromadb.persist_directory", "./chroma_db")

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


# Global config instance
config = Config()
