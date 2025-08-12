"""Tests for the new CLI rule category filters."""

from unittest.mock import patch
import pytest

from py_psscriptanalyzer import cli


def test_parser_with_rule_category_filters():
    """Test the command-line parser with the new rule category filter arguments."""
    parser = cli.create_parser()
    
    # Test with all rule category filters
    args = parser.parse_args([
        "--security-only",
        "--style-only",
        "--performance-only",
        "--best-practices-only",
        "--dsc-only",
        "--compatibility-only",
        "script.ps1"
    ])
    
    # Verify all arguments are parsed correctly
    assert args.security_only is True
    assert args.style_only is True
    assert args.performance_only is True
    assert args.best_practices_only is True
    assert args.dsc_only is True
    assert args.compatibility_only is True
    assert args.files == ["script.ps1"]


def test_parser_with_include_exclude_rules():
    """Test the command-line parser with include and exclude rules arguments."""
    parser = cli.create_parser()
    
    # Test with include rules
    args = parser.parse_args([
        "--include-rules", "Rule1,Rule2,Rule3",
        "script.ps1"
    ])
    
    # Verify include rules are parsed correctly
    assert args.include_rules == "Rule1,Rule2,Rule3"
    
    # Test with exclude rules
    args = parser.parse_args([
        "--exclude-rules", "Rule4,Rule5",
        "script.ps1"
    ])
    
    # Verify exclude rules are parsed correctly
    assert args.exclude_rules == "Rule4,Rule5"


def test_main_with_style_filter(monkeypatch):
    """Test main function with style filter."""
    parser = cli.create_parser()
    args = parser.parse_args(["--style-only", "script.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    
    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    
    # Mock run_script_analyzer to verify arguments
    called = {}
    def mock_run_script_analyzer(cmd, files, **kwargs):
        called['style_only'] = kwargs.get('style_only', False)
        return 0
    
    monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
    
    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))
    
    cli.main(["--style-only", "script.ps1"])
    
    # Verify style_only parameter was set to True
    assert called['style_only'] is True
    
    # Verify the correct status message was shown
    assert any("(style rules only)" in msg for msg in status_messages)


def test_main_with_include_rules(monkeypatch):
    """Test main function with include rules."""
    parser = cli.create_parser()
    args = parser.parse_args(["--include-rules", "Rule1,Rule2", "script.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    
    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    
    # Mock run_script_analyzer to verify arguments
    called = {}
    def mock_run_script_analyzer(cmd, files, **kwargs):
        called['include_rules'] = kwargs.get('include_rules', None)
        return 0
    
    monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
    
    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))
    
    cli.main(["--include-rules", "Rule1,Rule2", "script.ps1"])
    
    # Verify include_rules parameter contains the correct rules
    assert called['include_rules'] == ['Rule1', 'Rule2']
    
    # Verify the correct status message was shown
    assert any("(specific included rules)" in msg for msg in status_messages)


def test_main_with_multiple_category_filters(monkeypatch):
    """Test main function with multiple category filters (only first should be used)."""
    parser = cli.create_parser()
    args = parser.parse_args([
        "--security-only", 
        "--style-only", 
        "--performance-only", 
        "script.ps1"
    ])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    
    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    
    # Mock run_script_analyzer to verify arguments
    called = {}
    def mock_run_script_analyzer(cmd, files, **kwargs):
        called['security_only'] = kwargs.get('security_only', False)
        called['style_only'] = kwargs.get('style_only', False)
        called['performance_only'] = kwargs.get('performance_only', False)
        return 0
    
    monkeypatch.setattr(cli, "run_script_analyzer", mock_run_script_analyzer)
    
    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))
    
    cli.main(["--security-only", "--style-only", "--performance-only", "script.ps1"])
    
    # Verify all filter parameters were passed correctly
    assert called['security_only'] is True
    assert called['style_only'] is True
    assert called['performance_only'] is True
    
    # Verify the status message mentions only security rules
    # (since it's checked first in the if-else chain)
    assert any("(security rules only)" in msg for msg in status_messages)
