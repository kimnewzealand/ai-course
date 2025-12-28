"""Tool framework and implementations."""

from detective_agent.tools.definitions import (
    create_file_risk_report_tool,
    create_get_release_summary_tool,
    create_list_releases_tool,
    register_release_tools,
)
from detective_agent.tools.registry import (
    ToolDefinition,
    ToolExecutionError,
    ToolNotFoundError,
    ToolRegistry,
)
from detective_agent.tools.release_tools import (
    ReleaseDataError,
    RiskSeverity,
    file_risk_report,
    get_release_summary,
    list_all_releases,
    list_releases,
    load_releases,
)

__all__ = [
    # Registry
    "ToolRegistry",
    "ToolDefinition",
    "ToolNotFoundError",
    "ToolExecutionError",
    # Definitions
    "create_get_release_summary_tool",
    "create_list_releases_tool",
    "create_file_risk_report_tool",
    "register_release_tools",
    # Release tools
    "load_releases",
    "list_releases",
    "get_release_summary",
    "list_all_releases",
    "file_risk_report",
    "ReleaseDataError",
    "RiskSeverity",
]
