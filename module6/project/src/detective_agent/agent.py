"""Core agent orchestration."""

from pathlib import Path

from detective_agent.config import AgentConfig
from detective_agent.models import Conversation, Message
from detective_agent.observability import FileTraceExporter, SpanKind, get_tracer
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
        trace_dir: Path | str = "data/traces",
    ):
        self.provider = provider
        self.config = config
        self.conversation = conversation or Conversation(
            system_prompt=config.system_prompt
        )
        self.store = ConversationStore(config.conversation_dir)
        self.tool_registry = ToolRegistry()
        self._tracer = get_tracer()
        self._exporter = FileTraceExporter(trace_dir)

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

        # Start a new trace for this message
        trace = self._tracer.start_trace({"user_message": content[:100]})
        self.conversation.trace_id = trace.trace_id

        try:
            with self._tracer.span("send_message", attributes={"message_length": len(content)}) as root_span:
                # Add user message
                self.conversation.add_message("user", content)

                # Get tools in OpenAI format if any are registered
                tools = None
                if self.tool_registry.get_tools():
                    tools = self.tool_registry.format_for_openai()
                    root_span.set_attribute("tools_count", len(tools))

                # Tool calling loop
                max_iterations = 10
                iteration = 0
                for iteration in range(max_iterations):
                    # Prepare messages for provider (system + history)
                    messages = [
                        Message(role="system", content=self.conversation.system_prompt)
                    ] + self.conversation.messages

                    # Call provider with tracing
                    with self._tracer.span(
                        "llm_call",
                        kind=SpanKind.CLIENT,
                        attributes={
                            "model": self.config.provider.model,
                            "message_count": len(messages),
                            "iteration": iteration,
                        },
                    ) as llm_span:
                        response = await self.provider.complete(
                            messages=messages,
                            temperature=self.config.provider.temperature,
                            max_tokens=self.config.provider.max_tokens,
                            tools=tools,
                        )

                        # Record token usage
                        usage = response.metadata.get("usage", {})
                        llm_span.set_attribute("tokens.prompt", usage.get("prompt_tokens", 0))
                        llm_span.set_attribute("tokens.completion", usage.get("completion_tokens", 0))
                        llm_span.set_attribute("tokens.total", usage.get("total_tokens", 0))

                    # Check if response contains tool calls
                    tool_calls = response.metadata.get("tool_calls")
                    if not tool_calls:
                        # No tool calls - final response
                        self.conversation.messages.append(response)
                        root_span.set_attribute("total_messages", len(self.conversation.messages))
                        root_span.set_attribute("iterations", iteration + 1)
                        self.store.save(self.conversation)
                        return response.content

                    # Add assistant message with tool calls
                    self.conversation.messages.append(response)

                    # Execute each tool call with tracing
                    for tool_call in tool_calls:
                        tool_name = tool_call.get("function", {}).get("name", "")
                        tool_args_str = tool_call.get("function", {}).get("arguments", "{}")
                        tool_call_id = tool_call.get("id", "")

                        with self._tracer.span(
                            f"tool:{tool_name}",
                            attributes={"tool_name": tool_name, "tool_call_id": tool_call_id},
                        ) as tool_span:
                            try:
                                tool_args = json.loads(tool_args_str)
                                tool_span.set_attribute("arguments", tool_args)
                                result = await self.tool_registry.execute(tool_name, tool_args)
                                result_str = json.dumps(result) if isinstance(result, dict) else str(result)
                                tool_span.set_attribute("success", True)
                            except Exception as e:
                                result_str = json.dumps({"error": str(e)})
                                tool_span.set_attribute("success", False)
                                tool_span.set_attribute("error", str(e))

                        # Add tool result message
                        tool_msg = Message(
                            role="tool",
                            content=result_str,
                            metadata={"tool_call_id": tool_call_id, "name": tool_name},
                        )
                        self.conversation.messages.append(tool_msg)

                # Max iterations reached
                root_span.set_attribute("max_iterations_reached", True)
                self.store.save(self.conversation)
                return "Error: Maximum tool calling iterations reached."
        finally:
            # End and export the trace
            completed_trace = self._tracer.end_trace()
            if completed_trace:
                self._exporter.export(completed_trace)

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

