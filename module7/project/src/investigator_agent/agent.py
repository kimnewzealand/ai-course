"""Core Investigator Agent using LangChain.

This module defines the :class:`InvestigatorAgent`, which provides a
minimal conversational interface for Phase 1 (no tools yet).
"""

from typing import Any

from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from investigator_agent.config import AgentConfig
from investigator_agent.observability.callbacks import TracingCallbackHandler
from investigator_agent.observability.tracer import setup_tracing


class InvestigatorAgent:
    """Feature readiness assessment agent using LangChain."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent with configuration.

        For Phase 1 we wire a basic LLM client and conversation memory. Tools
        and a full agent executor will be added in later phases.
        """

        self.config = config

        # Initialize Groq LLM (OpenAI-compatible)
        # Note: ``langchain_openai.ChatOpenAI`` expects ``api_key`` and
        # ``base_url`` keyword arguments for non-OpenAI providers.
        self.llm = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=config.groq_api_key,
            base_url=config.get_base_url(),
        )

        # Set up conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        # Tools will be added in Phase 2–3
        self.tools: list[Any] = []

        # Create prompt template
        self.prompt = self._create_prompt()

        # Agent executor (will be initialized when tools are added)
        self.agent_executor: AgentExecutor | None = None

        # Tracing callbacks (Step 1.4)
        if config.enable_tracing:
            self.tracer = setup_tracing(config.traces_dir)
            self.callbacks = [TracingCallbackHandler(self.tracer)]
        else:
            self.tracer = None
            self.callbacks: list[Any] = []

    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the agent prompt template."""

        system_message = """You are the Investigator Agent, an automated feature readiness assessor.

Your role is to help determine if software features are ready to progress to the next development phase.

When asked about a feature, you should:
1. Understand what the user is asking
2. Provide helpful information about feature assessment

For now, you can have general conversations about feature readiness assessment.
In later phases, you will have tools to retrieve actual feature data."""

        return ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    async def send_message(self, user_message: str) -> str:
        """Send a message and get a response from the LLM.

        For Phase 1 we call the underlying chat model directly (no tools or
        agent executor yet) but we still maintain conversation history.
        """

        try:
            # Import here to avoid circular imports at module import time.
            from langchain_core.messages import HumanMessage

            # Existing chat history
            history = self.memory.chat_memory.messages

            # Compose messages for the model call
            messages = [
                SystemMessage(content=self.prompt.messages[0].content),
                *history,
                HumanMessage(content=user_message),
            ]

            # Invoke model asynchronously (with tracing callbacks when enabled)
            config = {"callbacks": self.callbacks} if self.callbacks else None
            response = await self.llm.ainvoke(messages, config=config)

            # Persist to memory
            self.memory.chat_memory.add_user_message(user_message)
            self.memory.chat_memory.add_ai_message(response.content)

            return response.content

        except Exception as exc:  # pragma: no cover - defensive guardrail
            # Basic error handling for early phases; later phases may
            # integrate richer observability and user-facing error messages.
            return f"Error: {exc}"  # type: ignore[return-value]

    def reset_conversation(self) -> None:
        """Clear conversation history for a fresh start."""

        self.memory.clear()
