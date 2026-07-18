"""Create LangChain models from the active server-side AI profile."""

import os
from typing import Any, Dict

from app.utils.config import config


class ProviderConfigurationError(RuntimeError):
    """Safe-to-return configuration error; it never contains credential values."""


def _required(settings: Dict[str, Any], field: str, kind: str) -> Any:
    value = settings.get(field)
    if value in (None, ""):
        raise ProviderConfigurationError(f"Active {kind} provider is missing '{field}'")
    return value


def _api_key(settings: Dict[str, Any], kind: str) -> str:
    env_name = _required(settings, "api_key_env", kind)
    value = os.getenv(env_name)
    if not value:
        raise ProviderConfigurationError(f"Active {kind} provider requires environment variable '{env_name}'")
    return value


def _common(settings: Dict[str, Any], kind: str) -> Dict[str, Any]:
    timeout = int(settings.get("timeout_seconds", 60))
    if timeout <= 0:
        raise ProviderConfigurationError(f"Active {kind} provider timeout_seconds must be positive")
    temperature = float(settings.get("temperature", 0.7))
    if not (0.0 <= temperature <= 2.0):
        raise ProviderConfigurationError(f"Active {kind} provider temperature must be between 0.0 and 2.0")
    max_tokens = int(settings.get("max_tokens", 500))
    if max_tokens <= 0:
        raise ProviderConfigurationError(f"Active {kind} provider max_tokens must be positive")
    return {"model": _required(settings, "model", kind), "timeout": timeout}


def create_chat_model():
    settings = config.chat_settings
    provider = _required(settings, "provider", "chat")
    common = _common(settings, "chat")
    timeout = common.pop("timeout")
    temperature = float(settings.get("temperature", 0.7))
    max_tokens = int(settings.get("max_tokens", 500))
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(base_url=_required(settings, "base_url", "chat"), temperature=temperature,
                          num_predict=max_tokens, client_kwargs={"timeout": timeout}, **common)
    if provider == "openai_compatible":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(base_url=_required(settings, "base_url", "chat"), api_key=_api_key(settings, "chat"),
                          temperature=temperature, max_tokens=max_tokens, timeout=timeout, **common)
    raise ProviderConfigurationError(f"Unsupported chat provider '{provider}'")


def create_embeddings():
    settings = config.embedding_settings
    provider = _required(settings, "provider", "embedding")
    common = _common(settings, "embedding")
    timeout = common.pop("timeout")
    dimension = settings.get("dimension")
    if not isinstance(dimension, int) or dimension <= 0:
        raise ProviderConfigurationError("Active embedding provider requires a positive integer 'dimension'")
    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(base_url=_required(settings, "base_url", "embedding"), client_kwargs={"timeout": timeout}, **common)
    if provider == "openai_compatible":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(base_url=_required(settings, "base_url", "embedding"), api_key=_api_key(settings, "embedding"), timeout=timeout, **common)
    raise ProviderConfigurationError(f"Unsupported embedding provider '{provider}'")


def validate_active_profile() -> None:
    """Validate config and construct models without logging secrets."""
    create_chat_model()
    create_embeddings()
