"""Tests for tool registry."""

from typing import Any

import pytest

from detective_agent.tools.registry import (
    ToolDefinition,
    ToolExecutionError,
    ToolNotFoundError,
    ToolRegistry,
)


async def mock_handler(args: dict[str, Any]) -> dict[str, Any]:
    """Simple mock handler for testing."""
    return {"result": "success", "args": args}


async def failing_handler(args: dict[str, Any]) -> dict[str, Any]:
    """Handler that raises an exception."""
    raise ValueError("Test error")


@pytest.fixture
def sample_tool() -> ToolDefinition:
    """Create a sample tool for testing."""
    return ToolDefinition(
        name="test_tool",
        description="A test tool",
        parameters={
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "Test input"}
            },
            "required": ["input"],
        },
        handler=mock_handler,
    )


@pytest.fixture
def failing_tool() -> ToolDefinition:
    """Create a tool that fails when executed."""
    return ToolDefinition(
        name="failing_tool",
        description="A tool that fails",
        parameters={"type": "object", "properties": {}},
        handler=failing_handler,
    )


class TestToolRegistry:
    """Tests for ToolRegistry class."""

    def test_register_tool(self, sample_tool: ToolDefinition):
        """Test registering a tool."""
        registry = ToolRegistry()
        registry.register(sample_tool)
        assert "test_tool" in registry.list_names()

    def test_get_tool(self, sample_tool: ToolDefinition):
        """Test getting a registered tool."""
        registry = ToolRegistry()
        registry.register(sample_tool)
        retrieved = registry.get("test_tool")
        assert retrieved.name == "test_tool"
        assert retrieved.description == "A test tool"

    def test_get_tool_not_found(self):
        """Test error when tool not found."""
        registry = ToolRegistry()
        with pytest.raises(ToolNotFoundError, match="not found"):
            registry.get("nonexistent")

    def test_get_tools(self, sample_tool: ToolDefinition, failing_tool: ToolDefinition):
        """Test getting all registered tools."""
        registry = ToolRegistry()
        registry.register(sample_tool)
        registry.register(failing_tool)
        tools = registry.get_tools()
        assert len(tools) == 2
        names = [t.name for t in tools]
        assert "test_tool" in names
        assert "failing_tool" in names

    def test_list_names(self, sample_tool: ToolDefinition):
        """Test listing tool names."""
        registry = ToolRegistry()
        assert registry.list_names() == []
        registry.register(sample_tool)
        assert "test_tool" in registry.list_names()

    @pytest.mark.asyncio
    async def test_execute_success(self, sample_tool: ToolDefinition):
        """Test successful tool execution."""
        registry = ToolRegistry()
        registry.register(sample_tool)
        result = await registry.execute("test_tool", {"input": "test"})
        assert result["result"] == "success"
        assert result["args"]["input"] == "test"

    @pytest.mark.asyncio
    async def test_execute_not_found(self):
        """Test execution error when tool not found."""
        registry = ToolRegistry()
        with pytest.raises(ToolNotFoundError):
            await registry.execute("nonexistent", {})

    @pytest.mark.asyncio
    async def test_execute_failure(self, failing_tool: ToolDefinition):
        """Test execution error when handler raises."""
        registry = ToolRegistry()
        registry.register(failing_tool)
        with pytest.raises(ToolExecutionError, match="execution failed"):
            await registry.execute("failing_tool", {})

    def test_format_for_openai(self, sample_tool: ToolDefinition):
        """Test formatting tools for OpenAI API."""
        registry = ToolRegistry()
        registry.register(sample_tool)
        formatted = registry.format_for_openai()
        assert len(formatted) == 1
        assert formatted[0]["type"] == "function"
        assert formatted[0]["function"]["name"] == "test_tool"
        assert formatted[0]["function"]["description"] == "A test tool"
        assert "parameters" in formatted[0]["function"]

    def test_register_overwrites(self, sample_tool: ToolDefinition):
        """Test that registering same name overwrites."""
        registry = ToolRegistry()
        registry.register(sample_tool)

        new_tool = ToolDefinition(
            name="test_tool",
            description="Updated description",
            parameters={"type": "object"},
            handler=mock_handler,
        )
        registry.register(new_tool)

        retrieved = registry.get("test_tool")
        assert retrieved.description == "Updated description"

