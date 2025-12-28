"""Command-line interface for the detective agent."""

import asyncio
import logging
from pathlib import Path

from pydantic import ValidationError

from detective_agent.agent import DetectiveAgent
from detective_agent.config import AgentConfig
from detective_agent.providers.openrouter import OpenRouterProvider
from detective_agent.tools import register_release_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """CLI for interacting with the agent."""
    # Load configuration from environment
    try:
        config = AgentConfig()
    except ValidationError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Make sure OPENROUTER_API_KEY is set in .env file")
        return

    logger.info("Detective Agent CLI started")
    logger.info(f"Using model: {config.provider.model}")

    print("Detective Agent CLI")
    print("Type 'exit' to quit, 'new' for new conversation, 'history' to see messages, 'tools' to list available tools")
    print("Example: 'Assess the risk of deploying v2.1.0'")
    print("-" * 60)

    # Use async context manager for automatic cleanup
    async with OpenRouterProvider(config.provider) as provider:
        agent = DetectiveAgent(provider, config)

        # Register release assessment tools
        # releases.json is in the project root
        releases_path = Path("releases.json")
        reports_dir = Path("data/reports")
        register_release_tools(
            agent.tool_registry,
            releases_path=releases_path,
            reports_dir=reports_dir,
        )
        logger.info(f"Registered tools: {agent.tool_registry.list_names()}")

        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                logger.info("Received interrupt signal")
                break

            # Use pattern matching for command handling
            match user_input.lower():
                case "exit" | "quit":
                    logger.info("User requested exit")
                    break
                case "new":
                    agent.new_conversation()
                    logger.info("Started new conversation")
                    print("Started new conversation")
                case "history":
                    for msg in agent.get_history():
                        print(f"{msg.role}: {msg.content[:100]}...")
                case "tools":
                    print("Available tools:")
                    for tool in agent.tool_registry.get_tools():
                        print(f"  - {tool.name}: {tool.description}")
                case "" | None:
                    continue
                case _:
                    try:
                        response = await agent.send_message(user_input)
                        print(f"\nAssistant: {response}")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}", exc_info=True)
                        print(f"Error: {e}")

    logger.info("Detective Agent CLI stopped")


def main_sync():
    """Synchronous wrapper for console script entry point.

    This enables the 'detective-agent' command via pyproject.toml scripts.
    """
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()

