"""Configuration management for the detective agent package."""

from pathlib import Path
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderConfig(BaseSettings):
    """Configuration for LLM provider with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="OPENROUTER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str  # Reads from OPENROUTER_API_KEY
    model: str = "meta-llama/llama-3.3-70b-instruct:free"  # OPENROUTER_MODEL
    base_url: str = "https://openrouter.ai/api/v1"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)
    timeout: float = 30.0


class AgentConfig(BaseSettings):
    """Main agent configuration with environment variable support."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    provider: ProviderConfig | None = None
    system_prompt: str = "You are a helpful AI assistant."
    conversation_dir: Path = Path("data/conversations")
    trace_dir: Path = Path("data/traces")

    @model_validator(mode="before")
    @classmethod
    def load_provider_from_env(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Ensure nested ProviderConfig is properly loaded from environment."""
        if "provider" not in data or data["provider"] is None:
            data["provider"] = ProviderConfig()
        return data

    @field_validator("conversation_dir", "trace_dir", mode="after")
    @classmethod
    def ensure_directory_exists(cls, v: Path) -> Path:
        """Create directory if it doesn't exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v

