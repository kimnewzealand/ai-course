"""Tests for :mod:`investigator_agent.agent`."""

from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import AIMessage

from investigator_agent.agent import InvestigatorAgent
from investigator_agent.config import AgentConfig


@patch("investigator_agent.agent.ChatOpenAI")
def test_agent_initializes_with_config_values(mock_chat_openai, tmp_path):
    """Agent should pass core config values into ChatOpenAI."""

    mock_instance = mock_chat_openai.return_value
    mock_instance.ainvoke = AsyncMock(return_value=AIMessage(content="ok"))

    config = AgentConfig(
        groq_api_key="test-key-123",
        data_dir=tmp_path / "data",
        conversations_dir=tmp_path / "conversations",
        traces_dir=tmp_path / "traces",
        evaluations_dir=tmp_path / "evaluations",
    )

    agent = InvestigatorAgent(config)

    assert agent.config is config
    mock_chat_openai.assert_called_once()
    kwargs = mock_chat_openai.call_args.kwargs
    assert kwargs["model"] == config.model_name
    assert kwargs["temperature"] == config.temperature
    assert kwargs["max_tokens"] == config.max_tokens
    assert kwargs["api_key"] == config.groq_api_key
    assert kwargs["base_url"] == config.get_base_url()


@pytest.mark.asyncio
@patch("investigator_agent.agent.ChatOpenAI")
async def test_send_message_calls_llm_and_updates_memory(mock_chat_openai, tmp_path):
    """send_message should call LLM and store messages in memory."""

    mock_instance = mock_chat_openai.return_value
    mock_instance.ainvoke = AsyncMock(return_value=AIMessage(content="Mock response"))

    config = AgentConfig(
        groq_api_key="test-key",
        data_dir=tmp_path / "data",
        conversations_dir=tmp_path / "conversations",
        traces_dir=tmp_path / "traces",
        evaluations_dir=tmp_path / "evaluations",
    )

    agent = InvestigatorAgent(config)

    assert agent.memory.chat_memory.messages == []

    reply = await agent.send_message("Hello")

    assert reply == "Mock response"

    history = agent.memory.chat_memory.messages
    assert len(history) == 2
    assert history[0].type == "human"
    assert history[0].content == "Hello"
    assert history[1].type == "ai"
    assert history[1].content == "Mock response"


@patch("investigator_agent.agent.ChatOpenAI")
def test_reset_conversation_clears_memory(mock_chat_openai, tmp_path):
    """reset_conversation should clear existing chat history."""

    mock_instance = mock_chat_openai.return_value
    mock_instance.ainvoke = AsyncMock(return_value=AIMessage(content="response"))

    config = AgentConfig(
        groq_api_key="test-key",
        data_dir=tmp_path / "data",
        conversations_dir=tmp_path / "conversations",
        traces_dir=tmp_path / "traces",
        evaluations_dir=tmp_path / "evaluations",
    )

    agent = InvestigatorAgent(config)

    # Seed some existing history
    agent.memory.chat_memory.add_user_message("hello")
    agent.memory.chat_memory.add_ai_message("hi there")
    assert agent.memory.chat_memory.messages  # ensure not empty

    # When
    agent.reset_conversation()

    # Then
    assert agent.memory.chat_memory.messages == []
