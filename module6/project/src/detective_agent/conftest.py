"""Shared test fixtures for the detective agent package."""

import pytest

from detective_agent.config import AgentConfig, ProviderConfig


@pytest.fixture
def mock_provider_config():
    """Provide a test configuration without real API key."""
    return ProviderConfig(api_key="test-key-not-real")


@pytest.fixture
def mock_agent_config(mock_provider_config):
    """Provide a test agent configuration."""
    return AgentConfig(provider=mock_provider_config)

