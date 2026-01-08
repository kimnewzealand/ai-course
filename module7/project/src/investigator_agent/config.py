"""Configuration management for Investigator Agent."""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Main configuration for the Investigator Agent."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Groq LLM Settings (Free Tier - Open Source Models)
    groq_api_key: str = Field(..., description="Groq API key from console.groq.com")
    model_name: str = Field(
        default="llama-3.1-8b-instant",
        description="Groq model (llama-3.1-8b-instant, llama-3.3-70b-versatile, qwen3-32b)",
    )

    # Agent Settings
    temperature: float = Field(
        default=0.0, ge=0.0, le=2.0, description="Temperature for LLM (0.0 for deterministic)"
    )
    max_tokens: int = Field(default=4096, gt=0, description="Maximum tokens for LLM response")

    # Data Paths
    data_dir: Path = Field(
        default=Path("incoming_data"), description="Directory containing feature data"
    )
    conversations_dir: Path = Field(
        default=Path("data/conversations"), description="Directory for saved conversations"
    )
    traces_dir: Path = Field(
        default=Path("data/traces"), description="Directory for OpenTelemetry traces"
    )
    evaluations_dir: Path = Field(
        default=Path("data/evaluations"), description="Directory for evaluation results"
    )

    # Observability
    enable_tracing: bool = Field(default=True, description="Enable OpenTelemetry tracing")
    trace_export_format: Literal["json", "otlp"] = Field(
        default="json", description="Trace export format"
    )

    @field_validator("data_dir", "conversations_dir", "traces_dir", "evaluations_dir")
    @classmethod
    def ensure_path_exists(cls, v: Path) -> Path:
        """Ensure directory exists, create if needed."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    def get_base_url(self) -> str:
        """Get Groq API base URL (OpenAI-compatible)."""
        return "https://api.groq.com/openai/v1"


def load_config() -> AgentConfig:
    """Load and validate configuration from environment."""
    try:
        config = AgentConfig()  # type: ignore[call-arg]
        return config
    except Exception as e:
        raise ValueError(f"Configuration error: {e}") from e
