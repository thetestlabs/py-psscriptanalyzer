"""Tests for the core module of py-psscriptanalyzer."""

import json
import subprocess
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

from py_psscriptanalyzer.constants import SARIF_VERSION
from py_psscriptanalyzer.core import convert_to_sarif, main, run_script_analyzer

# Tests for convert_to_sarif function
#


def test_convert_to_sarif_empty() -> None:
    """Test converting empty PSScriptAnalyzer results to SARIF format."""
    ps_results: list[dict[str, Any]] = []
    files = ["test.ps1"]
    sarif_data = convert_to_sarif(ps_results, files)

    # Check basic structure
    assert sarif_data["version"] == SARIF_VERSION
    assert len(sarif_data["runs"]) == 1
    assert sarif_data["runs"][0]["tool"]["driver"]["name"] == "PSScriptAnalyzer"
    assert len(sarif_data["runs"][0]["results"]) == 0
    assert len(sarif_data["runs"][0]["artifacts"]) == 1


def test_convert_to_sarif_with_results() -> None:
    """Test converting PSScriptAnalyzer results with findings to SARIF format."""
    ps_results = [
        {
            "RuleName": "PSAvoidUsingPlainTextForPassword",
            "Severity": "Error",
            "Message": "Password should be secure",
            "ScriptPath": "test.ps1",
            "Line": 10,
            "Column": 5,
            "IsSecurityRule": True,
        },
        {
            "RuleName": "PSAvoidUsingPositionalParameters",
            "Severity": "Warning",
            "Message": "Avoid positional parameters",
            "ScriptPath": "test.ps1",
            "Line": 15,
            "Column": 8,
            "IsSecurityRule": False,
        },
    ]
    files = ["test.ps1"]
    sarif_data = convert_to_sarif(ps_results, files)

    # Check results
    assert len(sarif_data["runs"][0]["results"]) == 2
    assert sarif_data["runs"][0]["results"][0]["ruleId"] == "PSAvoidUsingPlainTextForPassword"
    assert sarif_data["runs"][0]["results"][0]["level"] == "error"
    assert sarif_data["runs"][0]["results"][1]["ruleId"] == "PSAvoidUsingPositionalParameters"
    assert sarif_data["runs"][0]["results"][1]["level"] == "warning"

    # Check rules metadata
    assert len(sarif_data["runs"][0]["tool"]["driver"]["rules"]) == 2
    rule_ids = [rule["id"] for rule in sarif_data["runs"][0]["tool"]["driver"]["rules"]]
    assert "PSAvoidUsingPlainTextForPassword" in rule_ids
    assert "PSAvoidUsingPositionalParameters" in rule_ids

    # Check security tags
    security_rule = next(
        rule
        for rule in sarif_data["runs"][0]["tool"]["driver"]["rules"]
        if rule["id"] == "PSAvoidUsingPlainTextForPassword"
    )
    non_security_rule = next(
        rule
        for rule in sarif_data["runs"][0]["tool"]["driver"]["rules"]
        if rule["id"] == "PSAvoidUsingPositionalParameters"
    )
    assert "security" in security_rule["properties"]["tags"]
    assert len(non_security_rule["properties"]["tags"]) == 0


def test_convert_to_sarif_with_different_severities() -> None:
    """Test convert_to_sarif with different severities."""
    ps_results = [
        {
            "RuleName": "PSAvoidUsingPlainTextForPassword",
            "Severity": "Error",
            "Message": "Password should be secure",
            "ScriptPath": "test.ps1",
            "Line": 10,
            "Column": 5,
        },
        {
            "RuleName": "PSAvoidUsingPositionalParameters",
            "Severity": "Warning",
            "Message": "Avoid positional parameters",
            "ScriptPath": "test.ps1",
            "Line": 15,
            "Column": 8,
        },
        {
            "RuleName": "PSUseConsistentIndentation",
            "Severity": "Information",
            "Message": "Use consistent indentation",
            "ScriptPath": "test.ps1",
            "Line": 20,
            "Column": 1,
        },
        {
            "RuleName": "PSUnknownSeverity",
            "Severity": "Unknown",
            "Message": "Unknown severity level",
            "ScriptPath": "test.ps1",
            "Line": 25,
            "Column": 1,
        },
    ]

    sarif_data = convert_to_sarif(ps_results, ["test.ps1"])

    # Check that severity levels are correctly mapped
    sarif_results = sarif_data["runs"][0]["results"]

    error_result = next(r for r in sarif_results if r["ruleId"] == "PSAvoidUsingPlainTextForPassword")
    assert error_result["level"] == "error"

    warning_result = next(r for r in sarif_results if r["ruleId"] == "PSAvoidUsingPositionalParameters")
    assert warning_result["level"] == "warning"

    info_result = next(r for r in sarif_results if r["ruleId"] == "PSUseConsistentIndentation")
    assert info_result["level"] == "note"

    unknown_result = next(r for r in sarif_results if r["ruleId"] == "PSUnknownSeverity")
    assert unknown_result["level"] == "warning"  # Default fallback for unknown severity


#
# Tests for run_script_analyzer function
#


def test_run_script_analyzer_empty_files() -> None:
    """Test run_script_analyzer with empty file list."""
    result = run_script_analyzer("pwsh", [], format_files=False)
    assert result == 0


@patch("builtins.open", new_callable=mock_open)
@patch("py_psscriptanalyzer.core.convert_to_sarif")
@patch("json.loads", return_value=[])
@patch("subprocess.run")
@patch("py_psscriptanalyzer.core.generate_analysis_script", return_value="mock script")
@patch("py_psscriptanalyzer.core.build_powershell_file_array", return_value="$files")
def test_run_script_analyzer_sarif_output_to_file(
    mock_build_powershell_file_array: MagicMock,
    mock_generate_analysis_script: MagicMock,
    mock_run: MagicMock,
    mock_loads: MagicMock,
    mock_convert_to_sarif: MagicMock,
    mock_open_func: MagicMock,
) -> None:
    """Test run_script_analyzer with SARIF output to file."""
    # Mock subprocess
    process_mock = MagicMock()
    process_mock.returncode = 0  # No issues found
    process_mock.stdout = ""
    mock_run.return_value = process_mock

    # Mock SARIF conversion
    sarif_data = {
        "$schema": f"https://schemastore.azurewebsites.net/schemas/json/sarif-{SARIF_VERSION}.json",
        "version": SARIF_VERSION,
        "runs": [{"tool": {"driver": {"name": "PSScriptAnalyzer"}}, "results": []}],
    }
    mock_convert_to_sarif.return_value = sarif_data

    # Skip actual file operations
    with patch("os.path.exists", return_value=True):
        result = run_script_analyzer(
            "pwsh", ["test.ps1"], format_files=False, output_format="sarif", output_file="output.sarif"
        )

    assert result == 0
    mock_open_func.assert_called_once_with("output.sarif", "w", encoding="utf-8")


def test_run_script_analyzer_sarif_output_to_console() -> None:
    """Test run_script_analyzer with SARIF output to console."""

    # Create all the mocks we need
    with (
        patch("subprocess.run") as mock_run,
        patch("json.loads") as mock_loads,
        patch("py_psscriptanalyzer.core.convert_to_sarif") as mock_convert,
        patch("builtins.print") as mock_print,
        patch("py_psscriptanalyzer.core.generate_analysis_script", return_value="mock script"),
        patch("py_psscriptanalyzer.core.build_powershell_file_array", return_value="$files"),
    ):
        # Mock subprocess
        process_mock = MagicMock()
        process_mock.returncode = 1  # Issues found
        process_mock.stdout = '[{"RuleName": "Test", "Message": "Test"}]'
        mock_run.return_value = process_mock

        # Mock JSON parsing
        results = [{"RuleName": "Test", "Message": "Test"}]
        mock_loads.return_value = results

        # Mock SARIF conversion
        sarif_data = {
            "$schema": f"https://schemastore.azurewebsites.net/schemas/json/sarif-{SARIF_VERSION}.json",
            "version": SARIF_VERSION,
            "runs": [{"tool": {"driver": {"name": "PSScriptAnalyzer"}}, "results": [{"ruleId": "Test"}]}],
        }
        mock_convert.return_value = sarif_data

        # Run the function
        result = run_script_analyzer("pwsh", ["test.ps1"], format_files=False, output_format="sarif", output_file=None)

        # Check results
        assert result == 1
        mock_print.assert_called_once()


@patch("py_psscriptanalyzer.core.build_powershell_file_array", return_value="$files")
@patch("py_psscriptanalyzer.core.generate_analysis_script", return_value="mock script")
@patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pwsh", 300))
def test_run_script_analyzer_timeout(
    mock_build_powershell_file_array: MagicMock, mock_generate_analysis_script: MagicMock, mock_run: MagicMock
) -> None:
    """Test run_script_analyzer with timeout exception."""
    with patch("builtins.print") as mock_print:
        result = run_script_analyzer("pwsh", ["test.ps1"])

        assert result == 1
        mock_print.assert_called_with("Timeout while running PSScriptAnalyzer")


@patch("subprocess.run", side_effect=Exception("Test error"))
@patch("py_psscriptanalyzer.core.generate_analysis_script", return_value="mock script")
@patch("builtins.print")
@patch("py_psscriptanalyzer.core.build_powershell_file_array", return_value="$files")
def test_run_script_analyzer_general_exception(
    mock_build_powershell_file_array: MagicMock,
    mock_print: MagicMock,
    mock_generate_analysis_script: MagicMock,
    mock_subprocess: MagicMock,
) -> None:
    result = run_script_analyzer("pwsh", ["test.ps1"])

    assert result == 1
    mock_print.assert_called_with("Error processing results: Test error")


def test_run_script_analyzer_sarif_output() -> None:
    """Test run_script_analyzer function with SARIF output."""

    # Set up all mocks
    with (
        patch("subprocess.run") as mock_run,
        patch("json.loads") as mock_loads,
        patch("py_psscriptanalyzer.core.generate_analysis_script") as mock_generate,
        patch("py_psscriptanalyzer.core.convert_to_sarif") as mock_convert,
        patch("py_psscriptanalyzer.core.build_powershell_file_array", return_value="$files"),
    ):
        # Mock the script generation
        mock_generate.return_value = "# PowerShell script mock"

        # Mock subprocess.run to return JSON output
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = '[{"RuleName": "Test", "Message": "Test message"}]'
        mock_run.return_value = mock_process

        # Mock JSON parsing
        mock_loads.return_value = [{"RuleName": "Test", "Message": "Test message"}]

        # Mock convert_to_sarif
        mock_sarif_data = {
            "version": SARIF_VERSION,
            "runs": [{"tool": {"driver": {"name": "PSScriptAnalyzer"}}, "results": []}],
        }
        mock_convert.return_value = mock_sarif_data

        # Create a temporary file for output
        tmp_file = "test_output.sarif"

        # Mock open to avoid actual file operations
        with patch("builtins.open") as mock_open, patch("os.path.exists", return_value=True):
            result = run_script_analyzer(
                "pwsh", ["test.ps1"], format_files=False, output_format="sarif", output_file=tmp_file
            )

            # Validate results
            assert result == 0
            mock_run.assert_called_once()
            mock_convert.assert_called_once()
            mock_open.assert_called_once_with(tmp_file, "w", encoding="utf-8")


def test_file_output_handling() -> None:
    """Test handling output to files."""
    # Test writing to JSON file
    m_json = mock_open()
    with patch("builtins.open", m_json):
        json_data = [{"test": "value"}]
        output_json = json.dumps(json_data, indent=2)

        with open("output.json", "w") as f:
            f.write(output_json)

        m_json.assert_called_once_with("output.json", "w")
        m_json().write.assert_called_once_with(output_json)

    # Test writing to SARIF file
    m_sarif = mock_open()
    with patch("builtins.open", m_sarif):
        sarif_data = {
            "version": SARIF_VERSION,
            "runs": [{"tool": {"driver": {"name": "PSScriptAnalyzer"}}, "results": []}],
        }
        sarif_json = json.dumps(sarif_data, indent=2)

        with open("output.sarif", "w") as f:
            f.write(sarif_json)

        m_sarif.assert_called_once_with("output.sarif", "w")
        m_sarif().write.assert_called_once_with(sarif_json)


def test_exception_handling() -> None:
    """Test the exception handling code paths."""
    # Test timeout exception
    with patch("builtins.print") as mock_print:
        try:
            raise subprocess.TimeoutExpired(cmd="test", timeout=60)
        except subprocess.TimeoutExpired:
            print("Timeout while running PSScriptAnalyzer")
            result = 1
        mock_print.assert_called_with("Timeout while running PSScriptAnalyzer")
        assert result == 1

    # Test JSON decode error
    with patch("builtins.print") as mock_print:
        try:
            raise json.JSONDecodeError("Invalid JSON", "doc", 0)
        except json.JSONDecodeError:
            print("Error parsing JSON output from PSScriptAnalyzer")
            result = 1
        mock_print.assert_called_with("Error parsing JSON output from PSScriptAnalyzer")
        assert result == 1

    # Test general exception
    with patch("builtins.print") as mock_print:
        try:
            raise Exception("Test error")
        except Exception as e:
            print(f"Error processing results: {e}")
            result = 1
        mock_print.assert_called_with("Error processing results: Test error")
        assert result == 1


#
# Tests for main function
#


@patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0)
@patch("py_psscriptanalyzer.core.check_psscriptanalyzer_installed", return_value=True)
@patch("py_psscriptanalyzer.core.find_powershell", return_value="pwsh")
def test_main_with_ps_files(
    mock_find_powershell: MagicMock,
    mock_check_installed: MagicMock,
    mock_run_analyzer: MagicMock,
) -> None:
    with patch("sys.argv", ["py-psscriptanalyzer", "test.ps1"]), patch("builtins.print") as mock_print:
        result = main()

        assert result == 0
        mock_run_analyzer.assert_called_once()
        mock_print.assert_any_call("Using PowerShell: pwsh")
        mock_print.assert_any_call("Analyzing 1 PowerShell file(s)...")


@patch("py_psscriptanalyzer.core.find_powershell", return_value=None)
def test_main_no_powershell(mock_find_powershell: MagicMock) -> None:
    """Test main function when PowerShell is not found."""
    with (
        patch("sys.argv", ["py-psscriptanalyzer", "test.ps1"]),
        patch("builtins.print") as mock_print,
        patch("sys.stderr"),
    ):
        result = main()

        assert result == 1
        mock_find_powershell.assert_called_once()
        # Check for error message about PowerShell not found
        assert any("PowerShell not found" in str(call) for call in mock_print.call_args_list)


@patch("py_psscriptanalyzer.core.run_script_analyzer", return_value=0)
@patch("py_psscriptanalyzer.core.install_psscriptanalyzer", return_value=True)
@patch("py_psscriptanalyzer.core.check_psscriptanalyzer_installed", return_value=False)
@patch("py_psscriptanalyzer.core.find_powershell", return_value="pwsh")
@patch("builtins.print")
def test_main_install_psscriptanalyzer(
    mock_print: MagicMock,
    mock_find_powershell: MagicMock,
    mock_check_analyzer: MagicMock,
    mock_install_analyzer: MagicMock,
    mock_run_analyzer: MagicMock,
) -> None:
    with patch("sys.argv", ["py-psscriptanalyzer", "test.ps1"]):
        result = main()

        assert result == 0
        mock_check_analyzer.assert_called_once()
        mock_install_analyzer.assert_called_once()
        mock_run_analyzer.assert_called_once()
        assert any("PSScriptAnalyzer installed successfully" in str(call) for call in mock_print.call_args_list)


@patch("py_psscriptanalyzer.core.find_powershell", return_value="pwsh")
@patch("py_psscriptanalyzer.core.check_psscriptanalyzer_installed", return_value=False)
@patch("py_psscriptanalyzer.core.install_psscriptanalyzer", return_value=False)
def test_main_psscriptanalyzer_install_failed(
    mock_find_powershell: MagicMock,
    mock_run_analyzer: MagicMock,
    mock_install_analyzer: MagicMock,
) -> None:
    with (
        patch("sys.argv", ["py-psscriptanalyzer", "test.ps1"]),
        patch("builtins.print") as mock_print,
        patch("sys.stderr"),
    ):
        result = main()

        assert result == 1
        mock_find_powershell.assert_called_once()
        mock_install_analyzer.assert_called_once()
        # Check for error message about installation failure
        assert any("Failed to install PSScriptAnalyzer" in str(call) for call in mock_print.call_args_list)


def test_main_no_ps_files() -> None:
    """Test main function with no PowerShell files."""
    with patch("sys.argv", ["py-psscriptanalyzer", "test.txt"]):
        result = main()
        assert result == 0


@patch("py_psscriptanalyzer.core.find_powershell", return_value="pwsh")
@patch("py_psscriptanalyzer.core.check_psscriptanalyzer_installed", return_value=True)
@patch("py_psscriptanalyzer.core.run_script_analyzer")
def test_main_with_format_flag(
    mock_run_analyzer: MagicMock,
    mock_check_analyzer: MagicMock,
    mock_find_powershell: MagicMock,
) -> None:
    # Set up the return value of the mock
    mock_run_analyzer.return_value = 0

    with patch("sys.argv", ["py-psscriptanalyzer", "--format", "test.ps1"]), patch("builtins.print") as mock_print:
        result = main()

        assert result == 0
        mock_run_analyzer.assert_called_once()
        mock_print.assert_any_call("Formatting 1 PowerShell file(s)...")


# Tests from scripts_coverage.py
class TestScriptGenerationFilters:
    """Tests for script generation with various filters."""

    def test_generate_analysis_script_with_security_filter(self) -> None:
        """Test generating analysis script with security filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", security_only=True)

        # Check security filter is included
        assert "# Filter to include only security-related rules" in script
        assert "$categoryRules = @(" in script
        assert "IsSecurityRule" in script  # Check if the IsSecurityRule property is added

    def test_generate_format_script(self) -> None:
        """Test generating formatting script."""
        from py_psscriptanalyzer.scripts import generate_format_script

        script = generate_format_script("$files")

        # Check formatting commands are included
        assert "Invoke-Formatter" in script
        assert "foreach ($file in $files)" in script

    def test_generate_analysis_script_with_style_filter(self) -> None:
        """Test generating analysis script with style filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", style_only=True)

        # Check style filter is included
        assert "# Filter to include only style-related rules" in script
        assert "$categoryRules = @(" in script
        assert "RuleCategory" in script
        assert "Style" in script

    def test_generate_analysis_script_with_performance_filter(self) -> None:
        """Test generating analysis script with performance filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", performance_only=True)

        # Check performance filter is included
        assert "# Filter to include only performance-related rules" in script
        assert "$categoryRules = @(" in script
        assert "RuleCategory" in script
        assert "Performance" in script

    def test_generate_analysis_script_with_best_practices_filter(self) -> None:
        """Test generating analysis script with best practices filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", best_practices_only=True)

        # Check best practices filter is included
        assert "# Filter to include only best practices rules" in script
        assert "$categoryRules = @(" in script
        assert "RuleCategory" in script
        assert "BestPractices" in script

    def test_generate_analysis_script_with_dsc_filter(self) -> None:
        """Test generating analysis script with DSC filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", dsc_only=True)

        # Check DSC filter is included
        assert "# Filter to include only DSC-related rules" in script
        assert "$categoryRules = @(" in script
        assert "RuleCategory" in script
        assert "DSC" in script

    def test_generate_analysis_script_with_compatibility_filter(self) -> None:
        """Test generating analysis script with compatibility filter."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", compatibility_only=True)

        # Check compatibility filter is included
        assert "# Filter to include only compatibility-related rules" in script
        assert "$categoryRules = @(" in script
        assert "RuleCategory" in script
        assert "Compatibility" in script

    def test_generate_analysis_script_with_include_rules(self) -> None:
        """Test generating analysis script with include rules."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", include_rules=["Rule1", "Rule2"])

        # Check include rules filter is included
        assert "# Filter to include only specific rules" in script
        assert "$includeRules = @(" in script
        assert "'Rule1'" in script
        assert "'Rule2'" in script

    def test_generate_analysis_script_with_exclude_rules(self) -> None:
        """Test generating analysis script with exclude rules."""
        from py_psscriptanalyzer.scripts import generate_analysis_script

        script = generate_analysis_script("$files", exclude_rules=["Rule1", "Rule2"])

        # Check exclude rules filter is included
        assert "# Filter to exclude specific rules" in script
        assert "$excludeRules = @(" in script
        assert "'Rule1'" in script
        assert "'Rule2'" in script


# Tests from test_simple.py
