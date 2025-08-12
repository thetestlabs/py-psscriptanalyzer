"""Tests for security filtering and SARIF output functionality."""

import json
import os
import tempfile
from unittest.mock import patch, Mock
import pytest

from py_psscriptanalyzer import cli
from py_psscriptanalyzer.core import convert_to_sarif, run_script_analyzer
from py_psscriptanalyzer.scripts import generate_analysis_script
from py_psscriptanalyzer.constants import SECURITY_RULES, SARIF_VERSION


class TestSecurityFilter:
    """Test security filtering functionality."""

    def test_generate_script_with_security_filter(self) -> None:
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

    def test_main_with_security_only(self, monkeypatch) -> None:
        """Test main function with security_only flag."""
        parser = cli.create_parser()
        args = parser.parse_args(["--security-only", "script.ps1"])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)
        
        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
        
        # Mock run_script_analyzer to verify arguments
        called = {}
        def mock_run_script_analyzer(cmd, files, **kwargs):
            called['security_only'] = kwargs.get('security_only', False)
            return 0
        
        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
        
        cli.main(["--security-only", "script.ps1"])
        assert called['security_only'] is True


class TestSarifOutput:
    """Test SARIF output functionality."""

    def test_convert_to_sarif_empty(self) -> None:
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
                "IsSecurityRule": True
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

    def test_main_with_sarif_output(self, monkeypatch) -> None:
        """Test main function with sarif output format."""
        parser = cli.create_parser()
        args = parser.parse_args(["--output-format", "sarif", "script.ps1"])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)
        
        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
        
        # Mock run_script_analyzer to verify arguments
        called = {}
        def mock_run_script_analyzer(cmd, files, **kwargs):
            called['output_format'] = kwargs.get('output_format', "text")
            return 0
        
        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
        
        cli.main(["--output-format", "sarif", "script.ps1"])
        assert called['output_format'] == "sarif"

    def test_output_to_file(self, monkeypatch, tmp_path) -> None:
        """Test writing output to a file."""
        output_file = tmp_path / "results.sarif"
        
        parser = cli.create_parser()
        args = parser.parse_args([
            "--output-format", "sarif", 
            "--output-file", str(output_file),
            "script.ps1"
        ])
        monkeypatch.setattr(cli, "create_parser", lambda: parser)
        
        # Mock function calls
        monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
        monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
        
        # Mock run_script_analyzer to verify arguments
        called = {}
        def mock_run_script_analyzer(cmd, files, **kwargs):
            called['output_file'] = kwargs.get('output_file')
            # Create a minimal file to verify it was written
            if called['output_file']:
                with open(called['output_file'], 'w') as f:
                    f.write("{}")
            return 0
        
        monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
        
        cli.main([
            "--output-format", "sarif", 
            "--output-file", str(output_file),
            "script.ps1"
        ])
        
        assert called['output_file'] == str(output_file)
        assert os.path.exists(output_file)
