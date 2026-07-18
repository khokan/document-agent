"""Provider factory validation without contacting model services."""

import os
import unittest
from unittest.mock import patch, MagicMock

from app.ai.factory import (
    ProviderConfigurationError,
    _api_key,
    _common,
    create_chat_model,
    create_embeddings,
    validate_active_profile,
)


class TestProviderFactoryValidation(unittest.TestCase):
    def test_missing_model_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"timeout_seconds": 60}, "chat")

    def test_missing_remote_key_is_rejected_without_value_leakage(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ProviderConfigurationError, "REMOTE_API_KEY"):
                _api_key({"api_key_env": "REMOTE_API_KEY"}, "chat")

    def test_negative_timeout_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": -1}, "chat")

    def test_zero_timeout_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": 0}, "chat")

    def test_temperature_out_of_range_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": 10, "temperature": 3.0}, "chat")

    def test_negative_temperature_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": 10, "temperature": -0.5}, "chat")

    def test_zero_max_tokens_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": 10, "max_tokens": 0}, "chat")

    def test_negative_max_tokens_is_rejected(self):
        with self.assertRaises(ProviderConfigurationError):
            _common({"model": "m", "timeout_seconds": 10, "max_tokens": -100}, "chat")

    def test_valid_settings_pass(self):
        result = _common({"model": "test", "timeout_seconds": 30, "temperature": 0.5, "max_tokens": 256}, "chat")
        self.assertEqual(result["model"], "test")
        self.assertEqual(result["timeout"], 30)


class TestCreateChatModel(unittest.TestCase):
    @patch("app.ai.factory.config")
    def test_ollama_provider(self, mock_config):
        mock_config.chat_settings = {
            "provider": "ollama",
            "model": "mistral",
            "base_url": "http://localhost:11434",
            "timeout_seconds": 60,
            "temperature": 0.7,
            "max_tokens": 500,
        }
        with patch("langchain_ollama.ChatOllama") as MockOllama:
            MockOllama.return_value = MagicMock()
            result = create_chat_model()
            MockOllama.assert_called_once()
            self.assertEqual(result, MockOllama.return_value)

    @patch("app.ai.factory.config")
    def test_openai_compatible_provider(self, mock_config):
        mock_config.chat_settings = {
            "provider": "openai_compatible",
            "model": "llama-3.1-8b-instant",
            "base_url": "https://api.example.com/v1",
            "api_key_env": "TEST_API_KEY",
            "timeout_seconds": 60,
            "temperature": 0.7,
            "max_tokens": 500,
        }
        with patch.dict(os.environ, {"TEST_API_KEY": "test-key-123"}):
            with patch("langchain_openai.ChatOpenAI") as MockOpenAI:
                MockOpenAI.return_value = MagicMock()
                result = create_chat_model()
                MockOpenAI.assert_called_once()
                self.assertEqual(result, MockOpenAI.return_value)

    @patch("app.ai.factory.config")
    def test_unsupported_provider_is_rejected(self, mock_config):
        mock_config.chat_settings = {
            "provider": "unsupported_provider",
            "model": "test",
            "timeout_seconds": 60,
        }
        with self.assertRaisesRegex(ProviderConfigurationError, "Unsupported chat provider"):
            create_chat_model()


class TestCreateEmbeddings(unittest.TestCase):
    @patch("app.ai.factory.config")
    def test_ollama_provider(self, mock_config):
        mock_config.embedding_settings = {
            "provider": "ollama",
            "model": "nomic-embed-text",
            "base_url": "http://localhost:11434",
            "timeout_seconds": 60,
            "dimension": 768,
        }
        with patch("langchain_ollama.OllamaEmbeddings") as MockOllama:
            MockOllama.return_value = MagicMock()
            result = create_embeddings()
            MockOllama.assert_called_once()
            self.assertEqual(result, MockOllama.return_value)

    @patch("app.ai.factory.config")
    def test_openai_compatible_provider(self, mock_config):
        mock_config.embedding_settings = {
            "provider": "openai_compatible",
            "model": "text-embedding-3-small",
            "base_url": "https://api.example.com/v1",
            "api_key_env": "TEST_API_KEY",
            "timeout_seconds": 60,
            "dimension": 1536,
        }
        with patch.dict(os.environ, {"TEST_API_KEY": "test-key-123"}):
            with patch("langchain_openai.OpenAIEmbeddings") as MockOpenAI:
                MockOpenAI.return_value = MagicMock()
                result = create_embeddings()
                MockOpenAI.assert_called_once()
                self.assertEqual(result, MockOpenAI.return_value)

    @patch("app.ai.factory.config")
    def test_unsupported_provider_is_rejected(self, mock_config):
        mock_config.embedding_settings = {
            "provider": "unsupported_provider",
            "model": "test",
            "timeout_seconds": 60,
            "dimension": 768,
        }
        with self.assertRaisesRegex(ProviderConfigurationError, "Unsupported embedding provider"):
            create_embeddings()

    @patch("app.ai.factory.config")
    def test_missing_dimension_is_rejected(self, mock_config):
        mock_config.embedding_settings = {
            "provider": "ollama",
            "model": "test",
            "base_url": "http://localhost:11434",
            "timeout_seconds": 60,
        }
        with self.assertRaisesRegex(ProviderConfigurationError, "dimension"):
            create_embeddings()

    @patch("app.ai.factory.config")
    def test_zero_dimension_is_rejected(self, mock_config):
        mock_config.embedding_settings = {
            "provider": "ollama",
            "model": "test",
            "base_url": "http://localhost:11434",
            "timeout_seconds": 60,
            "dimension": 0,
        }
        with self.assertRaises(ProviderConfigurationError):
            create_embeddings()


class TestValidateActiveProfile(unittest.TestCase):
    @patch("app.ai.factory.create_chat_model")
    @patch("app.ai.factory.create_embeddings")
    def test_validate_calls_both_factories(self, mock_embeddings, mock_chat):
        validate_active_profile()
        mock_chat.assert_called_once()
        mock_embeddings.assert_called_once()
