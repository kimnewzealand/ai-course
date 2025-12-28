"""Tool definitions for release assessment.

This module provides pre-configured ToolDefinition instances that can be
registered with the agent's tool registry.
"""

from pathlib import Path
from typing import Any

from detective_agent.tools.registry import ToolDefinition, ToolRegistry
from detective_agent.tools.release_tools import (
    file_risk_report,
    get_release_summary,
    list_all_releases,
)


def create_get_release_summary_tool(releases_path: Path | None = None) -> ToolDefinition:
    """Create the get_release_summary tool definition.

    Args:
        releases_path: Optional path to releases.json file.

    Returns:
        ToolDefinition for get_release_summary.
    """

    async def handler(args: dict[str, Any]) -> dict[str, Any]:
        return await get_release_summary(args, releases_path)

    return ToolDefinition(
        name="get_release_summary",
        description=(
            "Retrieve high-level release information including version, changes, "
            "test results, and deployment metrics for a specific release."
        ),
        parameters={
            "type": "object",
            "properties": {
                "release_id": {
                    "type": "string",
                    "description": "The release version identifier (e.g., 'v2.1.0')",
                }
            },
            "required": ["release_id"],
        },
        handler=handler,
    )


def create_list_releases_tool(releases_path: Path | None = None) -> ToolDefinition:
    """Create the list_releases tool definition.

    Args:
        releases_path: Optional path to releases.json file.

    Returns:
        ToolDefinition for list_releases.
    """

    async def handler(args: dict[str, Any]) -> dict[str, Any]:
        return await list_all_releases(args, releases_path)

    return ToolDefinition(
        name="list_releases",
        description="List all available releases with their version identifiers.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        handler=handler,
    )


def create_file_risk_report_tool(reports_dir: Path | None = None) -> ToolDefinition:
    """Create the file_risk_report tool definition.

    Args:
        reports_dir: Optional directory to save risk reports.

    Returns:
        ToolDefinition for file_risk_report.
    """

    async def handler(args: dict[str, Any]) -> dict[str, Any]:
        return await file_risk_report(args, reports_dir)

    return ToolDefinition(
        name="file_risk_report",
        description=(
            "File a risk assessment report for a release with severity level "
            "and key findings. Use after analyzing release data."
        ),
        parameters={
            "type": "object",
            "properties": {
                "release_id": {
                    "type": "string",
                    "description": "The release version identifier",
                },
                "severity": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Risk severity level",
                },
                "findings": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of key findings and concerns",
                },
            },
            "required": ["release_id", "severity", "findings"],
        },
        handler=handler,
    )


def register_release_tools(
    registry: ToolRegistry,
    releases_path: Path | None = None,
    reports_dir: Path | None = None,
) -> None:
    """Register all release assessment tools with a registry.

    Args:
        registry: The tool registry to register tools with.
        releases_path: Optional path to releases.json file.
        reports_dir: Optional directory to save risk reports.
    """
    registry.register(create_get_release_summary_tool(releases_path))
    registry.register(create_list_releases_tool(releases_path))
    registry.register(create_file_risk_report_tool(reports_dir))

