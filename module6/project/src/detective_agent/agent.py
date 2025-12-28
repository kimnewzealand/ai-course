"""Core agent orchestration."""

from detective_agent.config import AgentConfig
from detective_agent.models import Conversation, Message
from detective_agent.persistence import ConversationStore
from detective_agent.providers.base import Provider
from detective_agent.tools.registry import ToolDefinition, ToolRegistry


class DetectiveAgent:
    """Core agent orchestration."""

    def __init__(
        self,
        provider: Provider,
        config: AgentConfig,
        conversation: Conversation | None = None,
    ):
        self.provider = provider
        self.config = config
        self.conversation = conversation or Conversation(
            system_prompt=config.system_prompt
        )
        self.store = ConversationStore(config.conversation_dir)
        self.tool_registry = ToolRegistry()

    def register_tool(self, tool: ToolDefinition) -> None:
        """Register a tool with the agent.

        Args:
            tool: The tool definition to register.
        """
        self.tool_registry.register(tool)

    async def send_message(self, content: str) -> str:
        """Send user message and get assistant response.

        Implements a tool calling loop: if the LLM requests tool calls,
        execute them and continue until a final text response is received.

        Args:
            content: The user's message content.

        Returns:
            The assistant's response content.
        """
        import json

        # Add user message
        self.conversation.add_message("user", content)

        # Get tools in OpenAI format if any are registered
        tools = None
        if self.tool_registry.get_tools():
            tools = self.tool_registry.format_for_openai()

        # Tool calling loop
        max_iterations = 10  # Prevent infinite loops
        for _ in range(max_iterations):
            # Prepare messages for provider (system + history)
            messages = [
                Message(role="system", content=self.conversation.system_prompt)
            ] + self.conversation.messages

            # Call provider with tools
            response = await self.provider.complete(
                messages=messages,
                temperature=self.config.provider.temperature,
                max_tokens=self.config.provider.max_tokens,
                tools=tools,
            )

            # Check if response contains tool calls
            tool_calls = response.metadata.get("tool_calls")
            if not tool_calls:
                # No tool calls - this is the final response
                self.conversation.messages.append(response)
                self.store.save(self.conversation)
                return response.content

            # Add assistant message with tool calls to conversation
            self.conversation.messages.append(response)

            # Execute each tool call and add results
            for tool_call in tool_calls:
                tool_name = tool_call.get("function", {}).get("name", "")
                tool_args_str = tool_call.get("function", {}).get("arguments", "{}")
                tool_call_id = tool_call.get("id", "")

                try:
                    tool_args = json.loads(tool_args_str)
                    result = await self.tool_registry.execute(tool_name, tool_args)
                    result_str = json.dumps(result) if isinstance(result, dict) else str(result)
                except Exception as e:
                    result_str = json.dumps({"error": str(e)})

                # Add tool result message
                tool_msg = Message(
                    role="tool",
                    content=result_str,
                    metadata={"tool_call_id": tool_call_id, "name": tool_name},
                )
                self.conversation.messages.append(tool_msg)

        # If we reach here, we hit max iterations
        self.store.save(self.conversation)
        return "Error: Maximum tool calling iterations reached."

    def get_history(self, limit: int | None = None) -> list[Message]:
        """Get conversation history.

        Args:
            limit: Optional limit on number of messages to return.

        Returns:
            List of messages in the conversation.
        """
        if limit:
            return self.conversation.messages[-limit:]
        return self.conversation.messages

    def new_conversation(self) -> None:
        """Start a new conversation."""
        self.conversation = Conversation(system_prompt=self.config.system_prompt)

