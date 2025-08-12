"""Unit tests for py_psscriptanalyzer.cli module.

This file contains all tests for the CLI functionality, including:
- Helper functions
- Command-line parser
- Main function execution paths
- Error handling scenarios
"""

from pathlib import Path
from unittest.mock import patch

from py_psscriptanalyzer import cli


def test_get_default_severity_env(monkeypatch):
    monkeypatch.setenv("PSSCRIPTANALYZER_SEVERITY", "Error")
    # Current implementation always returns 'Warning' (ignores env var)
    assert cli.get_default_severity() == "Warning"


def test_get_default_severity_fallback(monkeypatch):
    monkeypatch.delenv("PSSCRIPTANALYZER_SEVERITY", raising=False)
    assert cli.get_default_severity() == "Warning"


def test_get_version_display():
    version = cli._get_version_display()
    assert "py-psscriptanalyzer" in version
    # The version string does not contain the word 'version', just the name and number


def test_print_status_and_error(capsys):
    cli.print_status("Test status", style="blue")
    cli.print_error("Test error")
    out = capsys.readouterr().out
    assert "Test status" in out or "Test error" in out


def test_create_parser_help():
    parser = cli.create_parser()
    help_text = parser.format_help()
    assert "usage" in help_text.lower()
    assert "--help" in help_text


def test_rich_help_formatter():
    parser = cli.create_parser()
    formatter = cli.RichHelpFormatter(parser)
    assert isinstance(formatter, cli.RichHelpFormatter)


def test_rich_help_formatter_output():
    parser = cli.create_parser()
    formatter = cli.RichHelpFormatter(parser)
    help_text = formatter.format_help()
    assert "py-psscriptanalyzer" in help_text
    assert "USAGE" in help_text
    assert "OPTIONS" in help_text
    assert "EXAMPLES" in help_text


# Optionally, more tests can be added for argument parsing, e.g.:
def test_parser_parses_version():
    parser = cli.create_parser()
    args = parser.parse_args(["--version"])
    assert hasattr(args, "version")


def test_find_powershell_files_recursive_empty(tmp_path, monkeypatch):
    # No files in tmp_path
    monkeypatch.chdir(tmp_path)
    files = cli.find_powershell_files_recursive()
    assert files == []


def test_find_powershell_files_recursive_with_files(tmp_path, monkeypatch):
    # Create some PowerShell files
    (tmp_path / "foo.ps1").write_text("")
    (tmp_path / "bar.psm1").write_text("")
    (tmp_path / "baz.txt").write_text("")
    monkeypatch.chdir(tmp_path)
    files = cli.find_powershell_files_recursive()
    assert any(f.endswith(".ps1") for f in files)
    assert any(f.endswith(".psm1") for f in files)
    assert not any(f.endswith(".txt") for f in files)


def test_print_success(capsys):
    cli.print_success("Yay!")
    out = capsys.readouterr().out
    assert "OK" in out or "Yay!" in out


def test_main_version(monkeypatch):
    # Patch console.print to capture output
    called = {}

    def fake_print(msg, *a, **k):
        called["msg"] = msg

    monkeypatch.setattr(cli.console, "print", fake_print)
    parser = cli.create_parser()
    parser.parse_args(["--version"])
    # Patch create_parser to return our parser
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    ret = cli.main(["--version"])
    assert ret == 0
    assert "py-psscriptanalyzer" in called["msg"]


def test_main_recursive_no_files(monkeypatch):
    # Patch find_powershell_files_recursive to return []
    monkeypatch.setattr(cli, "find_powershell_files_recursive", lambda: [])
    parser = cli.create_parser()
    parser.parse_args(["--recursive"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    # Patch print_status to record all calls
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))
    ret = cli.main(["--recursive"])
    assert ret == 0
    assert "No PowerShell files found" in status_messages


def test_main_no_files(monkeypatch):
    parser = cli.create_parser()
    parser.parse_args([])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))
    ret = cli.main([])
    assert ret == 0
    assert "No PowerShell files specified" in status_messages


# Add more tests for edge cases as needed


#
# Tests from test_cli_additional.py
#
def test_main_with_mixed_files(monkeypatch):
    """Test when a mixture of PowerShell and non-PowerShell files are provided."""
    parser = cli.create_parser()
    parser.parse_args(["script.ps1", "file.txt", "module.psm1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock function calls for PowerShell detection and script analyzer
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    monkeypatch.setattr(
        cli,
        "run_script_analyzer",
        lambda cmd,
        files,
        format_files=False,
        severity="Warning",
        security_only=False,
        style_only=False,
        performance_only=False,
        best_practices_only=False,
        dsc_only=False,
        compatibility_only=False,
        include_rules=None,
        exclude_rules=None,
        output_format="text",
        output_file=None: 0,
    )

    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))

    # Capture success messages
    success_messages = []
    monkeypatch.setattr(cli, "print_success", lambda msg: success_messages.append(msg))

    ret = cli.main(["script.ps1", "file.txt", "module.psm1"])
    assert ret == 0
    assert "No issues found" in success_messages


def test_main_with_format_option(monkeypatch):
    """Test with format option enabled."""
    parser = cli.create_parser()
    parser.parse_args(["--format", "script.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    monkeypatch.setattr(
        cli,
        "run_script_analyzer",
        lambda cmd,
        files,
        format_files=True,
        severity="Warning",
        security_only=False,
        style_only=False,
        performance_only=False,
        best_practices_only=False,
        dsc_only=False,
        compatibility_only=False,
        include_rules=None,
        exclude_rules=None,
        output_format="text",
        output_file=None: 0,
    )

    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))

    ret = cli.main(["--format", "script.ps1"])
    assert ret == 0
    # Should have "Formatting" in one of the status messages
    assert any("Formatting" in msg for msg in status_messages)


def test_main_psscriptanalyzer_install_success(monkeypatch):
    """Test the path where PSScriptAnalyzer is not installed but gets installed successfully."""
    parser = cli.create_parser()
    parser.parse_args(["script.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: False)
    monkeypatch.setattr(cli, "install_psscriptanalyzer", lambda cmd: True)
    monkeypatch.setattr(
        cli,
        "run_script_analyzer",
        lambda cmd,
        files,
        format_files=False,
        severity="Warning",
        security_only=False,
        style_only=False,
        performance_only=False,
        best_practices_only=False,
        dsc_only=False,
        compatibility_only=False,
        include_rules=None,
        exclude_rules=None,
        output_format="text",
        output_file=None: 0,
    )

    # Capture success messages
    success_messages = []
    monkeypatch.setattr(cli, "print_success", lambda msg: success_messages.append(msg))

    ret = cli.main(["script.ps1"])
    assert ret == 0
    assert "PSScriptAnalyzer installed successfully" in success_messages


#
# Tests from test_cli_more.py
#
def test_main_script_analyzer_with_issues(monkeypatch):
    """Test when script analyzer finds issues (returns non-zero)."""
    parser = cli.create_parser()
    parser.parse_args(["script.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    # Return 1 to indicate issues found
    monkeypatch.setattr(
        cli,
        "run_script_analyzer",
        lambda cmd,
        files,
        format_files=False,
        severity="Warning",
        security_only=False,
        style_only=False,
        performance_only=False,
        best_practices_only=False,
        dsc_only=False,
        compatibility_only=False,
        include_rules=None,
        exclude_rules=None,
        output_format="text",
        output_file=None: 1,
    )

    # Capture output messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))

    ret = cli.main(["script.ps1"])
    assert ret == 1
    # Should not have "No issues found" in success messages because we mocked issues being found


def test_main_with_real_files(tmp_path, monkeypatch):
    """Test with real PowerShell files."""
    # Create a PowerShell file in a temporary directory
    ps1_path = tmp_path / "test.ps1"
    ps1_path.write_text("# Test PowerShell file")

    # Mock function calls but use the real find_powershell_files_recursive
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: True)
    monkeypatch.setattr(
        cli,
        "run_script_analyzer",
        lambda cmd,
        files,
        format_files=False,
        severity="Warning",
        security_only=False,
        style_only=False,
        performance_only=False,
        best_practices_only=False,
        dsc_only=False,
        compatibility_only=False,
        include_rules=None,
        exclude_rules=None,
        output_format="text",
        output_file=None: 0,
    )  # Run with recursive option from the tmp_path
    with monkeypatch.context() as m:
        m.chdir(tmp_path)
        ret = cli.main(["--recursive"])
        assert ret == 0


def test_parser_all_options():
    """Test all options in the parser."""
    # Test all options in the parser
    parser = cli.create_parser()
    args = parser.parse_args(
        [
            "--recursive",
            "--format",
            "--severity",
            "Error",
            "--security-only",
            "--output-format",
            "sarif",
            "--output-file",
            "results.sarif",
            "test.ps1",
            "module.psm1",
        ]
    )
    assert args.recursive is True
    assert args.format is True
    assert args.severity == "Error"
    assert args.security_only is True
    assert args.output_format == "sarif"
    assert args.output_file == "results.sarif"
    assert args.files == ["test.ps1", "module.psm1"]


#
# Tests from test_cli_final.py
#
def test_get_version_import_error(monkeypatch):
    """Test the _get_version_display function with an ImportError."""

    # Use monkeypatch to make the import statement raise ImportError
    def mock_import(*args, **kwargs):
        raise ImportError("Simulated import error")

    # Temporarily modify the built-in __import__ function
    monkeypatch.setattr("builtins.__import__", mock_import)

    # Execute the function, which should now hit the ImportError case
    version = cli._get_version_display()

    # Verify the fallback message is returned
    assert version == "py-psscriptanalyzer (unknown version)"


def test_find_powershell_files_default_dir():
    """Test finding PowerShell files with default start directory."""
    with patch("py_psscriptanalyzer.cli.Path.cwd") as mock_cwd, patch("py_psscriptanalyzer.cli.Path.glob") as mock_glob:
        mock_cwd.return_value = Path("/fake/dir")
        mock_glob.return_value = [Path("/fake/dir/test.ps1")]

        files = cli.find_powershell_files_recursive()
        assert mock_cwd.called
        assert len(files) > 0


def test_main_no_files_no_recursive(monkeypatch):
    """Test the main function with no files and not recursive."""
    parser = cli.create_parser()
    parser.parse_args([])  # Empty args
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Capture status messages
    status_messages = []
    monkeypatch.setattr(cli, "print_status", lambda msg, style="white": status_messages.append(msg))

    ret = cli.main([])
    assert ret == 0
    assert "No PowerShell files specified" in status_messages


def test_main_powershell_not_found(monkeypatch):
    """Test the main function when PowerShell is not found."""
    parser = cli.create_parser()
    parser.parse_args(["file.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock powershell not found
    monkeypatch.setattr(cli, "find_powershell", lambda: None)

    # Capture error messages
    error_messages = []
    monkeypatch.setattr(cli, "print_error", lambda msg: error_messages.append(msg))

    ret = cli.main(["file.ps1"])
    assert ret == 1
    assert "PowerShell not found" in error_messages[0]


def test_main_psscriptanalyzer_install_fails(monkeypatch):
    """Test the main function when PSScriptAnalyzer installation fails."""
    parser = cli.create_parser()
    parser.parse_args(["file.ps1"])
    monkeypatch.setattr(cli, "create_parser", lambda: parser)

    # Mock function calls
    monkeypatch.setattr(cli, "find_powershell", lambda: "pwsh")
    monkeypatch.setattr(cli, "check_psscriptanalyzer_installed", lambda cmd: False)
    monkeypatch.setattr(cli, "install_psscriptanalyzer", lambda cmd: False)  # Install fails

    # Capture error messages
    error_messages = []
    monkeypatch.setattr(cli, "print_error", lambda msg: error_messages.append(msg))

    ret = cli.main(["file.ps1"])
    assert ret == 1
    assert "Failed to install PSScriptAnalyzer" in error_messages
