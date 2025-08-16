"""Tests for py_psscriptanalyzer.powershell module."""

import subprocess
from unittest.mock import MagicMock, Mock, call, patch

from py_psscriptanalyzer.constants import (
    INSTALL_TIMEOUT,
    MODULE_CHECK_TIMEOUT,
    POWERSHELL_CHECK_TIMEOUT,
    POWERSHELL_EXECUTABLES,
)
from py_psscriptanalyzer.powershell import check_psscriptanalyzer_installed, find_powershell, install_psscriptanalyzer


class TestFindPowershell:
    """Tests for find_powershell function."""

    @patch("subprocess.run")
    def test_find_powershell_success_first_executable(self, mock_run: MagicMock) -> None:
        """Test finding PowerShell when first executable is available."""
        # Mock subprocess.run to return success for the first executable
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = "PSVersion 7.3.0"
        mock_run.return_value = mock_process

        # Call the function
        result = find_powershell()

        # Verify it called subprocess with the first executable in the list
        first_executable = POWERSHELL_EXECUTABLES[0]
        mock_run.assert_called_once_with(
            [first_executable, "-Command", "$PSVersionTable.PSVersion"],
            capture_output=True,
            text=True,
            timeout=POWERSHELL_CHECK_TIMEOUT,
            check=False,
        )
        assert result == first_executable

    @patch("subprocess.run")
    def test_find_powershell_try_multiple_executables(self, mock_run: MagicMock) -> None:
        """Test finding PowerShell when first executable fails but second succeeds."""

        # Mock subprocess.run to fail for first executable but succeed for second
        def side_effect(cmd, *_args, **_kwargs):
            if cmd[0] == POWERSHELL_EXECUTABLES[0]:
                raise FileNotFoundError("No such file")

            if cmd[0] == POWERSHELL_EXECUTABLES[1]:
                mock_success = Mock()
                mock_success.returncode = 0
                mock_success.stdout = "PSVersion 5.1"
                return mock_success
            return Mock(returncode=1)

        mock_run.side_effect = side_effect

        # Call the function
        result = find_powershell()

        # Verify it returned the second executable
        assert result == POWERSHELL_EXECUTABLES[1]

    @patch("subprocess.run")
    def test_find_powershell_timeout(self, mock_run: MagicMock) -> None:
        """Test finding PowerShell when subprocess times out."""
        # Mock subprocess.run to time out
        mock_run.side_effect = subprocess.TimeoutExpired("powershell", POWERSHELL_CHECK_TIMEOUT)

        # Call the function
        result = find_powershell()

        # Verify it tried all executables but returned None
        assert mock_run.call_count == len(POWERSHELL_EXECUTABLES)
        assert result is None

    @patch("subprocess.run")
    def test_find_powershell_not_found(self, mock_run: MagicMock) -> None:
        """Test finding PowerShell when no executables are available."""

        # Mock subprocess.run to fail for all executables
        def side_effect(cmd, *_args, **_kwargs):
            if cmd[0] in POWERSHELL_EXECUTABLES:
                return Mock(returncode=1)
            return Mock(returncode=0)

        mock_run.side_effect = side_effect

        # Call the function
        result = find_powershell()

        # Verify it tried all executables but returned None
        assert mock_run.call_count == len(POWERSHELL_EXECUTABLES)
        assert result is None


class TestCheckPSScriptAnalyzerInstalled:
    """Tests for check_psscriptanalyzer_installed function."""

    @patch("subprocess.run")
    def test_check_psscriptanalyzer_installed_success(self, mock_run: MagicMock) -> None:
        """Test checking PSScriptAnalyzer when it is installed."""
        # Mock subprocess.run to return success
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = (
            "ModuleType Version    Name\n---------- -------    ----\nScript     1.21.0     PSScriptAnalyzer"
        )
        mock_run.return_value = mock_process

        # Call the function
        result = check_psscriptanalyzer_installed("pwsh")

        # Verify it called subprocess with the correct command
        mock_run.assert_called_once_with(
            [
                "pwsh",
                "-Command",
                "Get-Module -ListAvailable -Name PSScriptAnalyzer",
            ],
            capture_output=True,
            text=True,
            timeout=MODULE_CHECK_TIMEOUT,
            check=False,
        )
        assert result is True

    @patch("subprocess.run")
    def test_check_psscriptanalyzer_installed_not_found(self, mock_run: MagicMock) -> None:
        """Test checking PSScriptAnalyzer when it is not installed."""
        # Mock subprocess.run to return success but without the module name
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = "No modules found"
        mock_run.return_value = mock_process

        # Call the function
        result = check_psscriptanalyzer_installed("pwsh")

        assert result is False

    @patch("subprocess.run")
    def test_check_psscriptanalyzer_installed_command_error(self, mock_run: MagicMock) -> None:
        """Test checking PSScriptAnalyzer when the command fails."""
        # Mock subprocess.run to return error
        mock_process = Mock()
        mock_process.returncode = 1
        mock_process.stdout = ""
        mock_run.return_value = mock_process

        # Call the function
        result = check_psscriptanalyzer_installed("pwsh")

        assert result is False

    @patch("subprocess.run")
    def test_check_psscriptanalyzer_installed_timeout(self, mock_run: MagicMock) -> None:
        """Test checking PSScriptAnalyzer when the command times out."""
        # Mock subprocess.run to time out
        mock_run.side_effect = subprocess.TimeoutExpired("pwsh", MODULE_CHECK_TIMEOUT)

        # Call the function
        result = check_psscriptanalyzer_installed("pwsh")

        assert result is False


class TestInstallPSScriptAnalyzer:
    """Tests for install_psscriptanalyzer function."""

    @patch("builtins.print")
    @patch("subprocess.run")
    def test_install_psscriptanalyzer_success(self, mock_run: MagicMock, mock_print: MagicMock) -> None:
        """Test installing PSScriptAnalyzer successfully."""
        # Mock subprocess.run to return success
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stdout = "PSScriptAnalyzer installed successfully"
        mock_run.return_value = mock_process

        # Call the function
        result = install_psscriptanalyzer("pwsh")

        # Verify it called subprocess with the correct command
        mock_run.assert_called_once_with(
            [
                "pwsh",
                "-Command",
                "Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser",
            ],
            capture_output=True,
            text=True,
            timeout=INSTALL_TIMEOUT,
            check=False,
        )
        assert result is True
        mock_print.assert_called_once_with("PSScriptAnalyzer not found. Installing...")

    @patch("builtins.print")
    @patch("subprocess.run")
    def test_install_psscriptanalyzer_failure(self, mock_run: MagicMock, mock_print: MagicMock) -> None:
        """Test installing PSScriptAnalyzer with failure."""
        # Mock subprocess.run to return error
        mock_process = Mock()
        mock_process.returncode = 1
        mock_process.stdout = "Installation failed"
        mock_run.return_value = mock_process

        # Call the function
        result = install_psscriptanalyzer("pwsh")

        assert result is False
        mock_print.assert_called_once_with("PSScriptAnalyzer not found. Installing...")

    @patch("builtins.print")
    @patch("subprocess.run")
    def test_install_psscriptanalyzer_timeout(self, mock_run: MagicMock, mock_print: MagicMock) -> None:
        """Test installing PSScriptAnalyzer when the command times out."""
        # Mock subprocess.run to time out
        mock_run.side_effect = subprocess.TimeoutExpired("pwsh", INSTALL_TIMEOUT)

        # Call the function
        result = install_psscriptanalyzer("pwsh")

        assert result is False
        assert mock_print.call_count == 2
        mock_print.assert_has_calls(
            [call("PSScriptAnalyzer not found. Installing..."), call("Timeout while installing PSScriptAnalyzer")]
        )
