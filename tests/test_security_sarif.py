"""Tests for security filtering and SARIF output functionality."""

import os
from pathlib import Path

import pytest

from py_psscriptanalyzer import cli
from py_psscriptanalyzer.constants import SARIF_VERSION, SECURITY_RULES
from py_psscriptanalyzer.core import convert_to_sarif
from py_psscriptanalyzer.scripts import generate_analysis_script


class TestSecurityFilter:
    """Test security filtering functionality."""

    def test_generate_script_with_security_filter(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test that the generated script includes security filter when requested."""
        script = generate_analysis_script("'test.ps1'", security_only=True)
        # Verify security filter is included
        assert "Filter to include only security-related rules" in script
        # Verify each security rule is included
        for rule in SECURITY_RULES:
            assert f"'{rule}'" in script

    def test_generate_script_without_security_filter(self) -> None:
        """Test that the generated script doesn't include security filter by default."""
        script = generate_analysis_script("'test.ps1'")
        assert "Filter to include only security-related rules" not in script

    def test_main_with_security_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with security_only flag."""
        parser = cli.create_parser()
        parser.parse_args(["--security-only", "script.ps1"])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)

        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)

        # Mock run_script_analyzer to verify arguments
        called = {}

        def mock_run_script_analyzer(cmd, files, **kwargs):
            called["security_only"] = kwargs.get("security_only", False)
            return 0

        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)

        cli.main(["--security-only", "script.ps1"])
        assert called["security_only"] is True


class TestSarifOutput:
    """Test SARIF output functionality."""

    def test_convert_to_sarif_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test conversion of empty results to SARIF."""
        sarif_data = convert_to_sarif([], ["test.ps1"])
        assert "$schema" in sarif_data
        assert sarif_data["version"] == SARIF_VERSION
        assert len(sarif_data["runs"]) == 1
        assert len(sarif_data["runs"][0]["results"]) == 0
        assert len(sarif_data["runs"][0]["artifacts"]) == 1

    def test_convert_to_sarif_with_results(self) -> None:
        """Test conversion of PSScriptAnalyzer results to SARIF."""
        ps_results = [
            {
                "RuleName": "AvoidUsingPlainTextForPassword",
                "Severity": "Error",
                "Message": "Password is in plain text",
                "ScriptPath": "/path/to/test.ps1",
                "Line": 10,
                "Column": 1,
                "IsSecurityRule": True,
            }
        ]

        sarif_data = convert_to_sarif(ps_results, ["/path/to/test.ps1"])

        # Verify SARIF structure
        assert sarif_data["version"] == SARIF_VERSION
        assert len(sarif_data["runs"]) == 1
        assert len(sarif_data["runs"][0]["results"]) == 1
        assert len(sarif_data["runs"][0]["tool"]["driver"]["rules"]) == 1

        # Verify result content
        result = sarif_data["runs"][0]["results"][0]
        assert result["ruleId"] == "AvoidUsingPlainTextForPassword"
        assert result["level"] == "error"
        assert "Password is in plain text" in result["message"]["text"]

        # Verify rule metadata
        rule = sarif_data["runs"][0]["tool"]["driver"]["rules"][0]
        assert rule["id"] == "AvoidUsingPlainTextForPassword"
        assert "security" in rule["properties"]["tags"]

    def test_main_with_sarif_output(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with sarif output format."""
        parser = cli.create_parser()
        parser.parse_args(["--output-format", "sarif", "script.ps1"])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)

        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)

        # Mock run_script_analyzer to verify arguments
        called = {}

        def mock_run_script_analyzer(cmd, files, **kwargs):
            called["output_format"] = kwargs.get("output_format", "text")
            return 0

        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)

        cli.main(["--output-format", "sarif", "script.ps1"])
        assert called["output_format"] == "sarif"

    def test_output_to_file(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test writing output to a file."""
        output_file = tmp_path / "results.sarif"

        parser = cli.create_parser()
        parser.parse_args(["--output-format", "sarif", "--output-file", str(output_file), "script.ps1"])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)

        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)

        # Mock run_script_analyzer to verify arguments
        called = {}

        def mock_run_script_analyzer(cmd, files, **kwargs):
            called["output_file"] = kwargs.get("output_file")
            # Create a minimal file to verify it was written
            if called["output_file"]:
                with open(called["output_file"], "w") as f:
                    f.write("{}")
            return 0

        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)

        cli.main(["--output-format", "sarif", "--output-file", str(output_file), "script.ps1"])

        assert called["output_file"] == str(output_file)
        assert os.path.exists(output_file)


def test_convert_to_sarif_with_rule_categories() -> None:
    """Test convert_to_sarif handles rule categories correctly."""
    # Create sample results with different rule categories
    ps_results = [
        {
            "RuleName": "AvoidUsingPlainTextForPassword",
            "Severity": "Error",
            "Message": "Password should be secure",
            "ScriptPath": "test.ps1",
            "Line": 10,
            "Column": 5,
            "IsSecurityRule": True,
            "RuleCategory": "Security",
        },
        {
            "RuleName": "PSAlignAssignmentStatement",
            "Severity": "Warning",
            "Message": "Align assignment statements",
            "ScriptPath": "test.ps1",
            "Line": 15,
            "Column": 8,
            "RuleCategory": "Style",
        },
        {
            "RuleName": "PSAvoidUsingInvokeExpression",
            "Severity": "Warning",
            "Message": "Avoid using Invoke-Expression",
            "ScriptPath": "test.ps1",
            "Line": 20,
            "Column": 3,
            "RuleCategory": "Performance",
        },
        {
            "RuleName": "PSUseApprovedVerbs",
            "Severity": "Warning",
            "Message": "Use approved verbs",
            "ScriptPath": "test.ps1",
            "Line": 25,
            "Column": 1,
            "RuleCategory": "BestPractices",
        },
    ]

    files = ["test.ps1"]
    sarif_data = convert_to_sarif(ps_results, files)

    # Check that rules have correct tags in SARIF output
    rules = sarif_data["runs"][0]["tool"]["driver"]["rules"]

    # Find rules by ID
    security_rule = next(rule for rule in rules if rule["id"] == "AvoidUsingPlainTextForPassword")
    style_rule = next(rule for rule in rules if rule["id"] == "PSAlignAssignmentStatement")
    performance_rule = next(rule for rule in rules if rule["id"] == "PSAvoidUsingInvokeExpression")
    best_practices_rule = next(rule for rule in rules if rule["id"] == "PSUseApprovedVerbs")

    # Verify tags
    assert "security" in security_rule["properties"]["tags"]
    assert "style" in style_rule["properties"]["tags"]
    assert "performance" in performance_rule["properties"]["tags"]
    assert "bestpractices" in best_practices_rule["properties"]["tags"]

    # Verify categories
    assert security_rule["properties"]["category"] == "Security"
    assert style_rule["properties"]["category"] == "Style"
    assert performance_rule["properties"]["category"] == "Performance"
    assert best_practices_rule["properties"]["category"] == "BestPractices"
