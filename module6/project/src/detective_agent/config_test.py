"""Tests for configuration system."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from detective_agent.config import AgentConfig, ProviderConfig


class TestProviderConfig:
    """Tests for ProviderConfig."""

    def test_provider_config_with_api_key(self):
        """Test creating config with API key."""
        config = ProviderConfig(api_key="test-key-123")

        assert config.api_key == "test-key-123"
        assert config.model == "meta-llama/llama-3.3-70b-instruct:free"
        assert config.base_url == "https://openrouter.ai/api/v1"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096
        assert config.timeout == 30.0

    def test_provider_config_custom_values(self):
        """Test creating config with custom values."""
        config = ProviderConfig(
            api_key="key",
            model="gpt-4",
            temperature=0.5,
            max_tokens=2048,
            timeout=60.0,
        )

        assert config.model == "gpt-4"
        assert config.temperature == 0.5
        assert config.max_tokens == 2048
        assert config.timeout == 60.0

    def test_provider_config_missing_api_key(self):
        """Test that missing API key raises ValidationError."""
        # Clear any env vars that might provide the key
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                ProviderConfig(_env_file=None)

            assert "api_key" in str(exc_info.value)

    def test_provider_config_temperature_validation(self):
        """Test temperature range validation."""
        # Valid temperatures
        ProviderConfig(api_key="key", temperature=0.0)
        ProviderConfig(api_key="key", temperature=2.0)

        # Invalid temperatures
        with pytest.raises(ValidationError):
            ProviderConfig(api_key="key", temperature=-0.1)

        with pytest.raises(ValidationError):
            ProviderConfig(api_key="key", temperature=2.1)

    def test_provider_config_max_tokens_validation(self):
        """Test max_tokens must be positive."""
        with pytest.raises(ValidationError):
            ProviderConfig(api_key="key", max_tokens=0)

        with pytest.raises(ValidationError):
            ProviderConfig(api_key="key", max_tokens=-100)

    def test_provider_config_from_env_vars(self):
        """Test loading config from environment variables."""
        env_vars = {
            "OPENROUTER_API_KEY": "env-api-key",
            "OPENROUTER_MODEL": "env-model",
            "OPENROUTER_TEMPERATURE": "0.3",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = ProviderConfig(_env_file=None)

            assert config.api_key == "env-api-key"
            assert config.model == "env-model"
            assert config.temperature == 0.3


class TestAgentConfig:
    """Tests for AgentConfig."""

    def test_agent_config_with_provider(self):
        """Test creating agent config with provider."""
        provider = ProviderConfig(api_key="test-key")
        config = AgentConfig(provider=provider)

        assert config.provider.api_key == "test-key"
        assert config.system_prompt == "You are a helpful AI assistant."

    def test_agent_config_custom_system_prompt(self):
        """Test custom system prompt."""
        provider = ProviderConfig(api_key="test-key")
        config = AgentConfig(
            provider=provider,
            system_prompt="You are a code reviewer.",
        )

        assert config.system_prompt == "You are a code reviewer."

    def test_agent_config_paths(self):
        """Test path configuration."""
        provider = ProviderConfig(api_key="test-key")
        config = AgentConfig(
            provider=provider,
            conversation_dir=Path("custom/convos"),
            trace_dir=Path("custom/traces"),
        )

        assert config.conversation_dir == Path("custom/convos")
        assert config.trace_dir == Path("custom/traces")

    def test_agent_config_loads_provider_from_env(self):
        """Test that AgentConfig loads nested ProviderConfig from env."""
        env_vars = {
            "OPENROUTER_API_KEY": "nested-env-key",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = AgentConfig(_env_file=None)

            assert config.provider is not None
            assert config.provider.api_key == "nested-env-key"

