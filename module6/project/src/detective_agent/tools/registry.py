"""Tool registry for managing and executing tools."""

from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    """Definition of a callable tool."""

    name: str
    description: str
    parameters: dict[str, Any]  # JSON schema
    handler: Callable[[dict[str, Any]], Awaitable[Any]] = Field(exclude=True)

    class Config:
        arbitrary_types_allowed = True


class ToolNotFoundError(Exception):
    """Tool not found in registry."""

    pass


class ToolExecutionError(Exception):
    """Tool handler raised an exception."""

    pass


class ToolRegistry:
    """Registry for managing and executing tools."""

    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool.

        Args:
            tool: The tool definition to register.
        """
        self.tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        """Get a tool by name.

        Args:
            name: The name of the tool.

        Returns:
            The tool definition.

        Raises:
            ToolNotFoundError: If tool is not registered.
        """
        if name not in self.tools:
            raise ToolNotFoundError(f"Tool not found: {name}")
        return self.tools[name]

    def get_tools(self) -> list[ToolDefinition]:
        """Get all registered tools.

        Returns:
            List of all registered tool definitions.
        """
        return list(self.tools.values())

    def list_names(self) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names.
        """
        return list(self.tools.keys())

    async def execute(self, name: str, args: dict[str, Any]) -> Any:
        """Execute a tool by name.

        Args:
            name: The name of the tool to execute.
            args: Arguments to pass to the tool handler.

        Returns:
            The result from the tool handler.

        Raises:
            ToolNotFoundError: If tool is not registered.
            ToolExecutionError: If tool handler raises an exception.
        """
        tool = self.get(name)

        try:
            result = await tool.handler(args)
            return result
        except Exception as e:
            raise ToolExecutionError(f"Tool '{name}' execution failed: {e}") from e

    def format_for_openai(self) -> list[dict[str, Any]]:
        """Format tools for OpenAI-compatible API (used by OpenRouter).

        Returns:
            List of tool definitions in OpenAI format.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools.values()
        ]

