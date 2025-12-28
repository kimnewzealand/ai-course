"""Detective Agent - AI agent for release risk assessment."""

from detective_agent.agent import DetectiveAgent
from detective_agent.config import AgentConfig, ProviderConfig
from detective_agent.models import Conversation, Message

__version__ = "0.1.0"

__all__ = [
    "DetectiveAgent",
    "AgentConfig",
    "ProviderConfig",
    "Conversation",
    "Message",
]
