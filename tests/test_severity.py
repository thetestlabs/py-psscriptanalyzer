"""Tests for severity level handling and environment variable support."""

import os
from unittest.mock import patch

from py_psscriptanalyzer.cli import get_default_severity
from py_psscriptanalyzer.scripts import generate_analysis_script


class TestSeverityDefaults:
    """Test default severity level handling."""

    def test_get_default_severity_no_env_var(self) -> None:
        """Test default severity when no environment variable is set."""
        with patch.dict(os.environ, {}, clear=False):
            # Remove SEVERITY_LEVEL if it exists
            if "SEVERITY_LEVEL" in os.environ:
                del os.environ["SEVERITY_LEVEL"]
            assert get_default_severity() == "Warning"

    def test_get_default_severity_from_env_var_error(self) -> None:
        """Test default severity from environment variable - Error."""
        with patch.dict(os.environ, {"SEVERITY_LEVEL": "Error"}):
            assert get_default_severity() == "Error"

    def test_get_default_severity_from_env_var_information(self) -> None:
        """Test default severity from environment variable - Information."""
        with patch.dict(os.environ, {"SEVERITY_LEVEL": "Information"}):
            assert get_default_severity() == "Information"

    def test_get_default_severity_from_env_var_warning(self) -> None:
        """Test default severity from environment variable - Warning."""
        with patch.dict(os.environ, {"SEVERITY_LEVEL": "Warning"}):
            assert get_default_severity() == "Warning"

    def test_get_default_severity_from_env_var_all(self) -> None:
        """Test default severity from environment variable - All."""
        with patch.dict(os.environ, {"SEVERITY_LEVEL": "All"}):
            assert get_default_severity() == "All"

    def test_get_default_severity_invalid_env_var(self) -> None:
        """Test default severity with invalid environment variable value."""
        with patch.dict(os.environ, {"SEVERITY_LEVEL": "InvalidLevel"}):
            assert get_default_severity() == "Warning"


class TestSeverityFiltering:
    """Test severity filtering logic in PowerShell script generation."""

    def test_generate_analysis_script_information_level(self) -> None:
        """Test that Information level includes all issues."""
        script = generate_analysis_script("'test.ps1'", "Information")

        # Should not use -Severity parameter (gets all issues)
        assert "-Severity" not in script
        # Should not have filtering logic
        assert "Where-Object" not in script

    def test_generate_analysis_script_warning_level(self) -> None:
        """Test that Warning level includes Warning and Error issues."""
        script = generate_analysis_script("'test.ps1'", "Warning")

        # Should not use -Severity parameter but should filter
        assert "-Severity" not in script or "-Severity Error" not in script
        # Should have filtering logic for Warning and Error
        assert "Warning" in script and "Error" in script
        assert "Where-Object" in script

    def test_generate_analysis_script_error_level(self) -> None:
        """Test that Error level includes only Error issues."""
        script = generate_analysis_script("'test.ps1'", "Error")

        # Should use -Severity Error parameter
        assert "-Severity Error" in script
        # Should not have additional filtering logic
        filtering_lines = [line for line in script.split("\n") if "Where-Object" in line]
        assert len(filtering_lines) == 0

    def test_generate_analysis_script_all_level(self) -> None:
        """Test that All level includes all issues (same as Information)."""
        script = generate_analysis_script("'test.ps1'", "All")

        # Should not use -Severity parameter (gets all issues)
        assert "-Severity" not in script
        # Should not have filtering logic
        assert "Where-Object" not in script

    def test_generate_analysis_script_consistency(self) -> None:
        """Test that All and Information generate similar scripts."""
        script_all = generate_analysis_script("'test.ps1'", "All")
        script_info = generate_analysis_script("'test.ps1'", "Information")

        # Both should not use -Severity parameter
        assert "-Severity" not in script_all
        assert "-Severity" not in script_info

        # Both should have similar structure (no filtering)
        assert "Where-Object" not in script_all
        assert "Where-Object" not in script_info
