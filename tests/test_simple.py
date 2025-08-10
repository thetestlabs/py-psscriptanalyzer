"""Tests for py-psscriptanalyzer module."""

import subprocess
from unittest.mock import Mock, patch

import pytest

from py_psscriptanalyzer import (
    check_psscriptanalyzer_installed,
    find_powershell,
    install_psscriptanalyzer,
    main,
    run_script_analyzer,
)
from py_psscriptanalyzer.constants import POWERSHELL_EXECUTABLES, SEVERITY_LEVELS
from py_psscriptanalyzer.scripts import (
    build_powershell_file_array,
    escape_powershell_path,
    generate_analysis_script,
    generate_format_script,
)


class TestFindPowershell:
    """Test find_powershell function."""

    def test_find_powershell_success_first_executable(self) -> None:
        """Test finding PowerShell when first executable is available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = find_powershell()
            assert result == POWERSHELL_EXECUTABLES[0]

    def test_find_powershell_success_second_executable(self) -> None:
        """Test finding PowerShell when second executable is available."""
        with patch("subprocess.run") as mock_run:
            # First call fails, second succeeds
            mock_run.side_effect = [
                Mock(returncode=1),  # First executable fails
                Mock(returncode=0),  # Second succeeds
            ]
            result = find_powershell()
            assert result == POWERSHELL_EXECUTABLES[1]

    def test_find_powershell_not_found(self) -> None:
        """Test when PowerShell is not found."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = find_powershell()
            assert result is None

    def test_find_powershell_timeout(self) -> None:
        """Test when PowerShell check times out."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 10)):
            result = find_powershell()
            assert result is None

    def test_find_powershell_all_fail(self) -> None:
        """Test when all PowerShell executables fail."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            result = find_powershell()
            assert result is None


class TestCheckPSScriptAnalyzer:
    """Test check_psscriptanalyzer_installed function."""

    def test_check_installed_success(self) -> None:
        """Test when PSScriptAnalyzer is installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "PSScriptAnalyzer module found"
            result = check_psscriptanalyzer_installed("pwsh")
            assert result is True

    def test_check_installed_not_found(self) -> None:
        """Test when PSScriptAnalyzer is not installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = ""
            result = check_psscriptanalyzer_installed("pwsh")
            assert result is False

    def test_check_installed_timeout(self) -> None:
        """Test when module check times out."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
            result = check_psscriptanalyzer_installed("pwsh")
            assert result is False

    def test_check_installed_no_module_name_in_output(self) -> None:
        """Test when command succeeds but module name not in output."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Some other output"
            result = check_psscriptanalyzer_installed("pwsh")
            assert result is False


class TestInstallPSScriptAnalyzer:
    """Test install_psscriptanalyzer function."""

    def test_install_success(self) -> None:
        """Test successful installation of PSScriptAnalyzer."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = install_psscriptanalyzer("pwsh")
            assert result is True

    def test_install_failure(self) -> None:
        """Test failed installation of PSScriptAnalyzer."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            result = install_psscriptanalyzer("pwsh")
            assert result is False

    def test_install_timeout(self) -> None:
        """Test when installation times out."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 120)):
            result = install_psscriptanalyzer("pwsh")
            assert result is False


class TestPowershellHelpers:
    """Test PowerShell helper functions."""

    def test_escape_powershell_path_no_quotes(self) -> None:
        """Test escaping path with no quotes."""
        result = escape_powershell_path("/path/to/file.ps1")
        assert result == "/path/to/file.ps1"

    def test_escape_powershell_path_with_single_quotes(self) -> None:
        """Test escaping path with single quotes."""
        result = escape_powershell_path("/path/to/file's script.ps1")
        assert result == "/path/to/file''s script.ps1"

    def test_escape_powershell_path_with_multiple_quotes(self) -> None:
        """Test escaping path with multiple single quotes."""
        result = escape_powershell_path("path'with'many'quotes.ps1")
        assert result == "path''with''many''quotes.ps1"

    def test_build_powershell_file_array_single_file(self) -> None:
        """Test building PowerShell array with single file."""
        result = build_powershell_file_array(["test.ps1"])
        assert result == "'test.ps1'"

    def test_build_powershell_file_array_multiple_files(self) -> None:
        """Test building PowerShell array with multiple files."""
        result = build_powershell_file_array(["test1.ps1", "test2.ps1"])
        assert result == "'test1.ps1','test2.ps1'"

    def test_build_powershell_file_array_with_quotes(self) -> None:
        """Test building PowerShell array with files containing quotes."""
        result = build_powershell_file_array(["test's file.ps1"])
        assert result == "'test''s file.ps1'"

    def test_build_powershell_file_array_empty(self) -> None:
        """Test building PowerShell array with no files."""
        result = build_powershell_file_array([])
        assert result == ""


class TestScriptGeneration:
    """Test PowerShell script generation functions."""

    def test_generate_format_script(self) -> None:
        """Test format script generation."""
        script = generate_format_script("'test.ps1'")
        assert "$files = @('test.ps1')" in script
        assert "Invoke-Formatter" in script
        assert "Set-Content" in script

    def test_generate_analysis_script_with_severity(self) -> None:
        """Test analysis script generation with severity."""
        script = generate_analysis_script("'test.ps1'", "Error")
        assert "$files = @('test.ps1')" in script
        assert "Invoke-ScriptAnalyzer" in script
        assert "-Severity Error" in script

    def test_generate_analysis_script_all_severity(self) -> None:
        """Test analysis script generation with 'All' severity."""
        script = generate_analysis_script("'test.ps1'", "All")
        assert "$files = @('test.ps1')" in script
        assert "Invoke-ScriptAnalyzer" in script
        assert "-Severity" not in script

    def test_generate_analysis_script_contains_github_actions_logic(self) -> None:
        """Test that analysis script contains GitHub Actions detection logic."""
        script = generate_analysis_script("'test.ps1'", "Warning")
        assert "$isGitHubActions = $env:GITHUB_ACTIONS" in script
        assert "error" in script  # Check for annotation type, not full format
        assert "warning" in script
        assert "notice" in script


class TestRunScriptAnalyzer:
    """Test run_script_analyzer function."""

    def test_run_script_analyzer_no_files(self) -> None:
        """Test running analyzer with no files."""
        result = run_script_analyzer("pwsh", [])
        assert result == 0

    def test_run_script_analyzer_success(self) -> None:
        """Test successful script analysis."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = run_script_analyzer("pwsh", ["test.ps1"])
            assert result == 0

    def test_run_script_analyzer_with_issues(self) -> None:
        """Test script analysis with issues found."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            result = run_script_analyzer("pwsh", ["test.ps1"])
            assert result == 1

    def test_run_script_analyzer_format_mode(self) -> None:
        """Test script analyzer in format mode."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = run_script_analyzer("pwsh", ["test.ps1"], format_files=True)
            assert result == 0

    def test_run_script_analyzer_timeout(self) -> None:
        """Test when script analysis times out."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 300)):
            result = run_script_analyzer("pwsh", ["test.ps1"])
            assert result == 1

    @pytest.mark.parametrize("severity", SEVERITY_LEVELS)
    def test_run_script_analyzer_all_severities(self, severity: str) -> None:
        """Test script analyzer with all severity levels."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = run_script_analyzer("pwsh", ["test.ps1"], severity=severity)
            assert result == 0

    def test_run_script_analyzer_multiple_files(self) -> None:
        """Test script analyzer with multiple files."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = run_script_analyzer("pwsh", ["test1.ps1", "test2.ps1", "test3.psm1"])
            assert result == 0


class TestMain:
    """Test main function."""

    def test_main_no_files(self) -> None:
        """Test main function with no files."""
        result = main([])
        assert result == 0

    def test_main_no_ps_files(self) -> None:
        """Test main function with no PowerShell files."""
        result = main(["test.txt", "test.py", "README.md"])
        assert result == 0

    def test_main_no_powershell(self) -> None:
        """Test main function when PowerShell is not found."""
        with patch("py_psscriptanalyzer.powershell.find_powershell", return_value=None):
            result = main(["test.ps1"])
            assert result == 1

    def test_main_psscriptanalyzer_not_installed_install_fails(self) -> None:
        """Test main when PSScriptAnalyzer not installed and installation fails."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=False),
            patch("py_psscriptanalyzer.powershell.install_psscriptanalyzer", return_value=False),
        ):
            result = main(["test.ps1"])
            assert result == 1

    def test_main_success_with_installation(self) -> None:
        """Test successful execution with PSScriptAnalyzer installation."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=False),
            patch("py_psscriptanalyzer.powershell.install_psscriptanalyzer", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["test.ps1"])
            assert result == 0

    def test_main_success_already_installed(self) -> None:
        """Test successful execution when PSScriptAnalyzer already installed."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["test.ps1"])
            assert result == 0

    def test_main_analysis_finds_issues(self) -> None:
        """Test main function when analysis finds issues."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=1),
        ):
            result = main(["test.ps1"])
            assert result == 1

    def test_main_format_mode(self) -> None:
        """Test main function in format mode."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["--format", "test.ps1"])
            assert result == 0

    @pytest.mark.parametrize("severity", SEVERITY_LEVELS)
    def test_main_all_severity_levels(self, severity: str) -> None:
        """Test main function with all severity levels."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["--severity", severity, "test.ps1"])
            assert result == 0

    def test_main_mixed_file_types(self) -> None:
        """Test main function with mixed file types."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["test.ps1", "test.txt", "module.psm1", "data.psd1", "script.py"])
            assert result == 0

    def test_main_format_and_severity(self) -> None:
        """Test main function with both format and severity options."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["--format", "--severity", "Error", "test.ps1"])
            assert result == 0

    def test_main_with_powershell_lts(self) -> None:
        """Test main function when using PowerShell LTS."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="pwsh-lts"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["test.ps1"])
            assert result == 0

    def test_main_with_windows_powershell(self) -> None:
        """Test main function when using Windows PowerShell."""
        with (
            patch("py_psscriptanalyzer.powershell.find_powershell", return_value="powershell"),
            patch("py_psscriptanalyzer.powershell.check_psscriptanalyzer_installed", return_value=True),
            patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0),
        ):
            result = main(["test.ps1"])
            assert result == 0


class TestConstants:
    """Test that constants are properly defined."""

    def test_powershell_executables_defined(self) -> None:
        """Test that PowerShell executables list is defined."""
        assert len(POWERSHELL_EXECUTABLES) > 0
        assert "pwsh" in POWERSHELL_EXECUTABLES

    def test_severity_levels_defined(self) -> None:
        """Test that severity levels are defined."""
        assert len(SEVERITY_LEVELS) == 4
        assert "All" in SEVERITY_LEVELS
        assert "Error" in SEVERITY_LEVELS
        assert "Warning" in SEVERITY_LEVELS
        assert "Information" in SEVERITY_LEVELS
