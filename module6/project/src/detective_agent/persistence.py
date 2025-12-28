"""Filesystem-based conversation persistence."""

import json
from pathlib import Path

from detective_agent.models import Conversation


class ConversationStore:
    """Filesystem-based conversation persistence."""

    def __init__(self, base_dir: str | Path = "data/conversations"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, conversation: Conversation) -> None:
        """Save conversation to filesystem.

        Args:
            conversation: The conversation to save.
        """
        file_path = self.base_dir / f"{conversation.id}.json"
        with open(file_path, "w") as f:
            json.dump(conversation.model_dump(), f, indent=2, default=str)

    def load(self, conversation_id: str) -> Conversation:
        """Load conversation from filesystem.

        Args:
            conversation_id: The ID of the conversation to load.

        Returns:
            The loaded Conversation object.

        Raises:
            FileNotFoundError: If the conversation file doesn't exist.
        """
        file_path = self.base_dir / f"{conversation_id}.json"
        with open(file_path, "r") as f:
            data = json.load(f)
        return Conversation.model_validate(data)

    def list_conversations(self) -> list[str]:
        """List all conversation IDs.

        Returns:
            List of conversation IDs.
        """
        return [f.stem for f in self.base_dir.glob("*.json")]

