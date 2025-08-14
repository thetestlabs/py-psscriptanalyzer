"""Tests for GitHub Actions integration functionality."""

import os
from unittest.mock import MagicMock, patch

from py_psscriptanalyzer.scripts import _generate_github_actions_output, generate_analysis_script


def test_github_actions_output_function():
    """Test the GitHub Actions output generation function."""
    # This tests the function directly
    output = _generate_github_actions_output()

    # Check that it contains key parts of GitHub Actions annotation format
    assert "::" in output
    assert "file=" in output
    assert "line=" in output
    assert "title=" in output

    # Check that it doesn't contain duplicate message output
    assert output.count("Write-Host $annotation") == 1
    assert "Write-Host $issue.Message" not in output


def test_github_actions_script_generation():
    """Test that the script for GitHub Actions is generated correctly."""
    script = generate_analysis_script("'test.ps1'")

    # Check that script detects GitHub Actions environment
    assert '$isGitHubActions = $env:GITHUB_ACTIONS -eq "true"' in script

    # Check for GitHub Actions annotation format
    assert "::" in script
    assert "file=" in script
    assert "line=" in script
    assert "title=" in script


@patch("subprocess.run")
def test_github_actions_environment_detection(mock_run):
    """Test that GitHub Actions environment is properly detected."""
    # Mock successful command execution
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = (
        "::warning file=test.ps1,line=10,title=PSAvoidUsingPlainTextForPassword::Password should be secure"
    )
    mock_run.return_value = mock_process

    # Set GitHub Actions environment variable
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
        from py_psscriptanalyzer.core import run_script_analyzer

        # Run the analyzer
        run_script_analyzer("pwsh", ["test.ps1"])

        # Check that the script was generated with GitHub Actions detection
        script_call = mock_run.call_args[0][0]
        assert any(
            '$isGitHubActions = $env:GITHUB_ACTIONS -eq "true"' in arg for arg in script_call if isinstance(arg, str)
        )
