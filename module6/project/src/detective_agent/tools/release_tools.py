"""Release assessment tools for the detective agent.

These tools read release data from releases.json and provide risk assessment capabilities.
"""

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, TypeAlias

# Type aliases
ReleaseData: TypeAlias = dict[str, Any]

# Default path to releases.json (relative to project root)
DEFAULT_RELEASES_PATH = Path("releases.json")


class RiskSeverity(str, Enum):
    """Risk severity levels for release assessments."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReleaseDataError(Exception):
    """Error loading or parsing release data."""

    pass


def load_releases(releases_path: Path | None = None) -> dict[str, ReleaseData]:
    """Load release data from JSON file.

    Args:
        releases_path: Path to the releases.json file. Defaults to project root.

    Returns:
        Dictionary mapping release IDs to release data.

    Raises:
        ReleaseDataError: If file not found or JSON parsing fails.
    """
    path = releases_path or DEFAULT_RELEASES_PATH

    if not path.exists():
        raise ReleaseDataError(f"Releases file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ReleaseDataError(f"Invalid JSON in releases file: {e}") from e
    except OSError as e:
        raise ReleaseDataError(f"Error reading releases file: {e}") from e


def list_releases(releases_path: Path | None = None) -> list[str]:
    """List all available release IDs.

    Args:
        releases_path: Path to the releases.json file.

    Returns:
        List of release version IDs.
    """
    try:
        releases = load_releases(releases_path)
        return list(releases.keys())
    except ReleaseDataError:
        return []


async def get_release_summary(
    args: dict[str, Any], releases_path: Path | None = None
) -> ReleaseData:
    """Get release summary tool handler.

    Args:
        args: Dictionary containing release_id.
        releases_path: Optional path to releases.json for testing.

    Returns:
        Release data dictionary or error dictionary.
    """
    release_id = args.get("release_id", "")

    if not release_id:
        return {"error": "release_id is required"}

    try:
        releases = load_releases(releases_path)
    except ReleaseDataError as e:
        return {"error": str(e)}

    if release_id in releases:
        return releases[release_id]
    else:
        available = list(releases.keys())
        return {
            "error": f"Release {release_id} not found",
            "available_releases": available,
        }


async def list_all_releases(
    args: dict[str, Any], releases_path: Path | None = None
) -> dict[str, Any]:
    """List all available releases tool handler.

    Args:
        args: Dictionary (unused, but required for tool interface).
        releases_path: Optional path to releases.json for testing.

    Returns:
        Dictionary with list of release IDs or error.
    """
    try:
        releases = load_releases(releases_path)
        return {
            "releases": list(releases.keys()),
            "count": len(releases),
        }
    except ReleaseDataError as e:
        return {"error": str(e)}


async def file_risk_report(
    args: dict[str, Any], reports_dir: Path | None = None
) -> dict[str, str]:
    """File risk report tool handler.

    Args:
        args: Dictionary containing release_id, severity, and findings.
        reports_dir: Optional directory to save reports.

    Returns:
        Status dictionary with report information.

    Raises:
        ValueError: If severity is invalid.
    """
    release_id = args.get("release_id")
    severity_str = args.get("severity")
    findings = args.get("findings", [])

    if not release_id:
        return {"error": "release_id is required"}
    if not severity_str:
        return {"error": "severity is required"}

    # Validate severity using Enum
    try:
        severity = RiskSeverity(severity_str)
    except ValueError:
        valid_severities = ", ".join(s.value for s in RiskSeverity)
        return {"error": f"Invalid severity: {severity_str}. Must be one of: {valid_severities}"}

    # Create report
    timestamp = datetime.now(timezone.utc).isoformat()
    report = {
        "release_id": release_id,
        "severity": severity.value,
        "findings": findings,
        "filed_at": timestamp,
    }

    # Save report if directory provided
    if reports_dir:
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"risk_report_{release_id}_{timestamp[:10]}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return {
            "status": "filed",
            "report_id": str(report_file),
            "severity": severity.value,
            "message": f"Risk report filed. Please review the report at: {report_file.resolve()}",
        }

    return {
        "status": "filed",
        "report_id": f"report_{release_id}_{timestamp}",
        "severity": severity.value,
        "message": f"Risk report filed for {release_id} with severity: {severity.value}",
    }

