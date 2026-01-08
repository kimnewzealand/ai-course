"""Tests for configuration system."""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from investigator_agent.config import AgentConfig, load_config


class TestAgentConfig:
    """Tests for AgentConfig."""

    def test_config_with_required_fields(self, tmp_path):
        """Test creating config with required API key."""
        config = AgentConfig(
            groq_api_key="test-key-123",
            data_dir=tmp_path / "data",
            conversations_dir=tmp_path / "conversations",
            traces_dir=tmp_path / "traces",
            evaluations_dir=tmp_path / "evaluations",
        )

        assert config.groq_api_key == "test-key-123"
        assert config.model_name == "llama-3.1-8b-instant"
        assert config.temperature == 0.0
        assert config.max_tokens == 4096
        assert config.enable_tracing is True
        assert config.trace_export_format == "json"

    def test_config_missing_api_key(self):
        """Test that missing API key raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(_env_file=None)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("groq_api_key",)
        assert errors[0]["type"] == "missing"

    def test_config_custom_values(self, tmp_path):
        """Test config with custom values."""
        config = AgentConfig(
            groq_api_key="custom-key",
            model_name="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=2048,
            enable_tracing=False,
            trace_export_format="otlp",
            data_dir=tmp_path / "custom_data",
            conversations_dir=tmp_path / "custom_conversations",
            traces_dir=tmp_path / "custom_traces",
            evaluations_dir=tmp_path / "custom_evaluations",
        )

        assert config.groq_api_key == "custom-key"
        assert config.model_name == "llama-3.3-70b-versatile"
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
        assert config.enable_tracing is False
        assert config.trace_export_format == "otlp"

    def test_temperature_validation(self, tmp_path):
        """Test temperature validation (must be between 0.0 and 2.0)."""
        # Valid temperatures
        config = AgentConfig(
            groq_api_key="test-key",
            temperature=0.0,
            data_dir=tmp_path / "data",
            conversations_dir=tmp_path / "conversations",
            traces_dir=tmp_path / "traces",
            evaluations_dir=tmp_path / "evaluations",
        )
        assert config.temperature == 0.0

        config = AgentConfig(
            groq_api_key="test-key",
            temperature=2.0,
            data_dir=tmp_path / "data",
            conversations_dir=tmp_path / "conversations",
            traces_dir=tmp_path / "traces",
            evaluations_dir=tmp_path / "evaluations",
        )
        assert config.temperature == 2.0

        # Invalid temperature (too high)
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                groq_api_key="test-key",
                temperature=2.5,
                data_dir=tmp_path / "data",
                conversations_dir=tmp_path / "conversations",
                traces_dir=tmp_path / "traces",
                evaluations_dir=tmp_path / "evaluations",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("temperature",) for e in errors)

        # Invalid temperature (negative)
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                groq_api_key="test-key",
                temperature=-0.1,
                data_dir=tmp_path / "data",
                conversations_dir=tmp_path / "conversations",
                traces_dir=tmp_path / "traces",
                evaluations_dir=tmp_path / "evaluations",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("temperature",) for e in errors)

    def test_max_tokens_validation(self, tmp_path):
        """Test max_tokens validation (must be > 0)."""
        # Valid max_tokens
        config = AgentConfig(
            groq_api_key="test-key",
            max_tokens=1,
            data_dir=tmp_path / "data",
            conversations_dir=tmp_path / "conversations",
            traces_dir=tmp_path / "traces",
            evaluations_dir=tmp_path / "evaluations",
        )
        assert config.max_tokens == 1

        # Invalid max_tokens (zero)
        with pytest.raises(ValidationError) as exc_info:
            AgentConfig(
                groq_api_key="test-key",
                max_tokens=0,
                data_dir=tmp_path / "data",
                conversations_dir=tmp_path / "conversations",
                traces_dir=tmp_path / "traces",
                evaluations_dir=tmp_path / "evaluations",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("max_tokens",) for e in errors)

    def test_directory_creation(self, tmp_path):
        """Test that directories are automatically created."""
        data_dir = tmp_path / "new_data"
        conversations_dir = tmp_path / "new_conversations"
        traces_dir = tmp_path / "new_traces"
        evaluations_dir = tmp_path / "new_evaluations"

        # Directories should not exist yet
        assert not data_dir.exists()
        assert not conversations_dir.exists()
        assert not traces_dir.exists()
        assert not evaluations_dir.exists()

        config = AgentConfig(
            groq_api_key="test-key",
            data_dir=data_dir,
            conversations_dir=conversations_dir,
            traces_dir=traces_dir,
            evaluations_dir=evaluations_dir,
        )

        # Directories should now exist
        assert config.data_dir.exists()
        assert config.conversations_dir.exists()
        assert config.traces_dir.exists()
        assert config.evaluations_dir.exists()

    def test_get_base_url(self, tmp_path):
        """Test get_base_url method."""
        config = AgentConfig(
            groq_api_key="test-key",
            data_dir=tmp_path / "data",
            conversations_dir=tmp_path / "conversations",
            traces_dir=tmp_path / "traces",
            evaluations_dir=tmp_path / "evaluations",
        )

        assert config.get_base_url() == "https://api.groq.com/openai/v1"

    def test_config_from_env_vars(self, tmp_path):
        """Test loading config from environment variables."""
        env_vars = {
            "GROQ_API_KEY": "env-api-key",
            "MODEL_NAME": "qwen3-32b",
            "TEMPERATURE": "0.5",
            "MAX_TOKENS": "2048",
            "ENABLE_TRACING": "false",
            "TRACE_EXPORT_FORMAT": "otlp",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = AgentConfig(
                _env_file=None,
                data_dir=tmp_path / "data",
                conversations_dir=tmp_path / "conversations",
                traces_dir=tmp_path / "traces",
                evaluations_dir=tmp_path / "evaluations",
            )

            assert config.groq_api_key == "env-api-key"
            assert config.model_name == "qwen3-32b"
            assert config.temperature == 0.5
            assert config.max_tokens == 2048
            assert config.enable_tracing is False
            assert config.trace_export_format == "otlp"

    def test_config_case_insensitive(self, tmp_path):
        """Test that environment variables are case-insensitive."""
        env_vars = {
            "groq_api_key": "lowercase-key",
            "model_name": "llama-3.3-70b-versatile",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = AgentConfig(
                _env_file=None,
                data_dir=tmp_path / "data",
                conversations_dir=tmp_path / "conversations",
                traces_dir=tmp_path / "traces",
                evaluations_dir=tmp_path / "evaluations",
            )

            assert config.groq_api_key == "lowercase-key"
            assert config.model_name == "llama-3.3-70b-versatile"


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_success(self, tmp_path):
        """Test successful config loading."""
        env_vars = {
            "GROQ_API_KEY": "test-key-from-env",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            with patch("investigator_agent.config.AgentConfig") as mock_config:
                mock_instance = mock_config.return_value
                result = load_config()

                assert result == mock_instance
                mock_config.assert_called_once()

    def test_load_config_error(self, tmp_path, monkeypatch):
        """Test that load_config raises ValueError on configuration error."""
        # Change to a directory without .env file
        monkeypatch.chdir(tmp_path)

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                load_config()

            assert "Configuration error:" in str(exc_info.value)
