"""Tests for release assessment tools."""

import json
from pathlib import Path

import pytest

from detective_agent.tools.release_tools import (
    ReleaseDataError,
    RiskSeverity,
    file_risk_report,
    get_release_summary,
    list_all_releases,
    list_releases,
    load_releases,
)

# Test fixture for mock release data
MOCK_RELEASES = {
    "v2.1.0": {
        "version": "v2.1.0",
        "changes": ["Added payment processing", "Fixed authentication bug"],
        "tests": {"passed": 142, "failed": 2, "skipped": 5},
        "deployment_metrics": {"error_rate": 0.02, "response_time_p95": 450},
    },
    "v2.0.0": {
        "version": "v2.0.0",
        "changes": ["Minor UI updates"],
        "tests": {"passed": 149, "failed": 0, "skipped": 0},
        "deployment_metrics": {"error_rate": 0.001, "response_time_p95": 320},
    },
}


@pytest.fixture
def mock_releases_file(tmp_path: Path) -> Path:
    """Create a temporary releases.json file for testing."""
    releases_file = tmp_path / "releases.json"
    releases_file.write_text(json.dumps(MOCK_RELEASES))
    return releases_file


@pytest.fixture
def invalid_json_file(tmp_path: Path) -> Path:
    """Create a file with invalid JSON."""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{ invalid json }")
    return invalid_file


class TestLoadReleases:
    """Tests for load_releases function."""

    def test_load_releases_success(self, mock_releases_file: Path):
        """Test loading valid releases file."""
        releases = load_releases(mock_releases_file)
        assert "v2.1.0" in releases
        assert "v2.0.0" in releases
        assert releases["v2.1.0"]["version"] == "v2.1.0"

    def test_load_releases_file_not_found(self, tmp_path: Path):
        """Test error when file doesn't exist."""
        with pytest.raises(ReleaseDataError, match="not found"):
            load_releases(tmp_path / "nonexistent.json")

    def test_load_releases_invalid_json(self, invalid_json_file: Path):
        """Test error when JSON is invalid."""
        with pytest.raises(ReleaseDataError, match="Invalid JSON"):
            load_releases(invalid_json_file)


class TestListReleases:
    """Tests for list_releases function."""

    def test_list_releases_success(self, mock_releases_file: Path):
        """Test listing release IDs."""
        releases = list_releases(mock_releases_file)
        assert set(releases) == {"v2.1.0", "v2.0.0"}

    def test_list_releases_empty_on_error(self, tmp_path: Path):
        """Test returns empty list when file doesn't exist."""
        releases = list_releases(tmp_path / "nonexistent.json")
        assert releases == []


class TestGetReleaseSummary:
    """Tests for get_release_summary tool handler."""

    @pytest.mark.asyncio
    async def test_get_release_summary_valid(self, mock_releases_file: Path):
        """Test getting summary for valid release."""
        result = await get_release_summary({"release_id": "v2.1.0"}, mock_releases_file)
        assert result["version"] == "v2.1.0"
        assert "changes" in result
        assert "tests" in result

    @pytest.mark.asyncio
    async def test_get_release_summary_not_found(self, mock_releases_file: Path):
        """Test error for non-existent release."""
        result = await get_release_summary({"release_id": "v9.9.9"}, mock_releases_file)
        assert "error" in result
        assert "not found" in result["error"]
        assert "available_releases" in result

    @pytest.mark.asyncio
    async def test_get_release_summary_missing_id(self, mock_releases_file: Path):
        """Test error when release_id is missing."""
        result = await get_release_summary({}, mock_releases_file)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_release_summary_file_error(self, tmp_path: Path):
        """Test error when releases file doesn't exist."""
        result = await get_release_summary(
            {"release_id": "v2.1.0"}, tmp_path / "nonexistent.json"
        )
        assert "error" in result


class TestListAllReleases:
    """Tests for list_all_releases tool handler."""

    @pytest.mark.asyncio
    async def test_list_all_releases(self, mock_releases_file: Path):
        """Test listing all releases."""
        result = await list_all_releases({}, mock_releases_file)
        assert "releases" in result
        assert "count" in result
        assert result["count"] == 2
        assert set(result["releases"]) == {"v2.1.0", "v2.0.0"}

    @pytest.mark.asyncio
    async def test_list_all_releases_file_error(self, tmp_path: Path):
        """Test error when file doesn't exist."""
        result = await list_all_releases({}, tmp_path / "nonexistent.json")
        assert "error" in result


class TestFileRiskReport:
    """Tests for file_risk_report tool handler."""

    @pytest.mark.asyncio
    async def test_file_risk_report_success(self):
        """Test filing a risk report."""
        result = await file_risk_report({
            "release_id": "v2.1.0",
            "severity": "high",
            "findings": ["Failed tests detected", "High error rate"],
        })
        assert result["status"] == "filed"
        assert result["severity"] == "high"
        assert "report_id" in result
        assert "message" in result
        assert "v2.1.0" in result["message"]

    @pytest.mark.asyncio
    async def test_file_risk_report_with_directory(self, tmp_path: Path):
        """Test filing a risk report to a directory includes file path."""
        result = await file_risk_report(
            {
                "release_id": "v2.1.0",
                "severity": "medium",
                "findings": ["Minor issues found"],
            },
            reports_dir=tmp_path,
        )
        assert result["status"] == "filed"
        assert "message" in result
        # Message should include the file path
        assert str(tmp_path) in result["message"] or "risk_report" in result["message"]
        # Check a file was created
        report_files = list(tmp_path.glob("*.json"))
        assert len(report_files) == 1

    @pytest.mark.asyncio
    async def test_file_risk_report_invalid_severity(self):
        """Test error for invalid severity."""
        result = await file_risk_report({
            "release_id": "v2.1.0",
            "severity": "critical",  # Invalid
            "findings": ["Test"],
        })
        assert "error" in result
        assert "Invalid severity" in result["error"]

    @pytest.mark.asyncio
    async def test_file_risk_report_missing_release_id(self):
        """Test error when release_id is missing."""
        result = await file_risk_report({
            "severity": "high",
            "findings": ["Test"],
        })
        assert "error" in result
        assert "release_id" in result["error"]

    @pytest.mark.asyncio
    async def test_file_risk_report_missing_severity(self):
        """Test error when severity is missing."""
        result = await file_risk_report({
            "release_id": "v2.1.0",
            "findings": ["Test"],
        })
        assert "error" in result
        assert "severity" in result["error"]


class TestRiskSeverity:
    """Tests for RiskSeverity enum."""

    def test_valid_severities(self):
        """Test all valid severity values."""
        assert RiskSeverity("high") == RiskSeverity.HIGH
        assert RiskSeverity("medium") == RiskSeverity.MEDIUM
        assert RiskSeverity("low") == RiskSeverity.LOW

    def test_invalid_severity(self):
        """Test invalid severity raises ValueError."""
        with pytest.raises(ValueError):
            RiskSeverity("critical")

