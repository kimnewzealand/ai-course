"""Interactive CLI for Investigator Agent.

Provides a simple REPL for talking to :class:`InvestigatorAgent`.
"""

import asyncio
import sys

from investigator_agent.agent import InvestigatorAgent
from investigator_agent.config import load_config


async def main() -> None:
    """Run interactive CLI."""

    print("=" * 60)
    print("Investigator Agent - Feature Readiness Assessment")
    print("=" * 60)
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("=" * 60)
    print()

    try:
        config = load_config()
        agent = InvestigatorAgent(config)
        print(f"✓ Agent initialized with Groq ({config.model_name})")
        print()
    except Exception as exc:  # pragma: no cover - early-exit path
        print(f"✗ Failed to initialize agent: {exc}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            if user_input.lower() == "reset":
                agent.reset_conversation()
                print("\n✓ Conversation reset\n")
                continue

            # Get response
            response = await agent.send_message(user_input)
            print(f"\nAgent: {response}\n")

        except (KeyboardInterrupt, EOFError):  # pragma: no cover - interactive only
            print("\n\nGoodbye!")
            break
        except Exception as exc:  # pragma: no cover - defensive guardrail
            print(f"\n✗ Error: {exc}\n")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    asyncio.run(main())
