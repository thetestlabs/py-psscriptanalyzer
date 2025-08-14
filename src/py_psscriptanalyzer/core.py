"""Core PSScriptAnalyzer functionality."""

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from typing import Any, Optional

from .constants import ANALYSIS_TIMEOUT, POWERSHELL_FILE_EXTENSIONS, SARIF_VERSION, SEVERITY_LEVELS
from .powershell import check_psscriptanalyzer_installed, find_powershell, install_psscriptanalyzer
from .scripts import build_powershell_file_array, generate_analysis_script, generate_format_script


def run_script_analyzer(
    powershell_cmd: str,
    files: list[str],
    format_files: bool = False,
    severity: str = "Warning",
    security_only: bool = False,
    style_only: bool = False,
    performance_only: bool = False,
    best_practices_only: bool = False,
    dsc_only: bool = False,
    compatibility_only: bool = False,
    include_rules: Optional[list[str]] = None,
    exclude_rules: Optional[list[str]] = None,
    output_format: str = "text",
    output_file: Optional[str] = None,
) -> int:
    """Run PSScriptAnalyzer on the given files."""
    if not files:
        return 0

    files_param = build_powershell_file_array(files)

    if format_files:
        ps_command = generate_format_script(files_param)
    else:
        ps_command = generate_analysis_script(
            files_param,
            severity=severity,
            security_only=security_only,
            style_only=style_only,
            performance_only=performance_only,
            best_practices_only=best_practices_only,
            dsc_only=dsc_only,
            compatibility_only=compatibility_only,
            include_rules=include_rules,
            exclude_rules=exclude_rules,
            json_output=(output_format in ["json", "sarif"]),
        )

    try:
        if format_files:
            # For formatting, just run the command normally
            result = subprocess.run(
                [powershell_cmd, "-Command", ps_command],
                text=True,
                timeout=ANALYSIS_TIMEOUT,
                check=False,
                capture_output=False,
            )
            return result.returncode

        if output_format == "text":
            # Standard console output mode
            result = subprocess.run(
                [powershell_cmd, "-Command", ps_command],
                text=True,
                timeout=ANALYSIS_TIMEOUT,
                check=False,
                capture_output=False,
            )
            return result.returncode

        # Handle JSON and SARIF output formats
        result = subprocess.run(
            [powershell_cmd, "-Command", ps_command],
            text=True,
            timeout=ANALYSIS_TIMEOUT,
            check=False,
            capture_output=True,
        )

        # Parse PowerShell JSON output or empty list if no results
        json_data = [] if result.returncode == 0 and not result.stdout.strip() else json.loads(result.stdout)

        # If SARIF format is requested, convert JSON to SARIF
        output_data = convert_to_sarif(json_data, files) if output_format == "sarif" else json_data

        output_json = json.dumps(output_data, indent=2)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_json)
        else:
            print(output_json)

        return result.returncode

    except subprocess.TimeoutExpired:
        print("Timeout while running PSScriptAnalyzer")
        return 1
    except json.JSONDecodeError:
        print("Error parsing JSON output from PSScriptAnalyzer")
        return 1
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error processing results: {e}")
        return 1


def convert_to_sarif(ps_results: list[dict[str, Any]], files: list[str]) -> dict[str, Any]:
    """Convert PSScriptAnalyzer results to SARIF format."""
    # Map severity levels to SARIF levels
    severity_map = {
        "Error": "error",
        "Warning": "warning",
        "Information": "note",
        # PowerShell may return numeric severity values
        0: "note",  # Information
        1: "warning",  # Warning
        2: "error",  # Error
    }

    # Create base SARIF structure
    sarif = {
        "$schema": f"https://schemastore.azurewebsites.net/schemas/json/sarif-{SARIF_VERSION}.json",
        "version": SARIF_VERSION,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "PSScriptAnalyzer",
                        "semanticVersion": "1.x",
                        "informationUri": "https://github.com/PowerShell/PSScriptAnalyzer",
                        "rules": [],
                    }
                },
                "results": [],
                "artifacts": [{"location": {"uri": f"file://{os.path.abspath(f)}"}} for f in files],
            }
        ],
    }

    # Track rules we've already added
    rules_added = set()

    # Ensure ps_results is a list
    ps_results = [ps_results] if ps_results and not isinstance(ps_results, list) else ps_results

    # Process results
    for result in ps_results:
        rule_id = result.get("RuleName", "")
        severity = result.get("Severity", "Warning")
        message = result.get("Message", "")
        file_path = result.get("ScriptPath", "")
        line = result.get("Line", 1)
        column = result.get("Column", 1)

        # Add rule metadata if not already added
        if rule_id and rule_id not in rules_added:
            # Determine tags based on rule category
            tags = []
            if result.get("IsSecurityRule", False):
                tags.append("security")

            # Add other category tags
            rule_category = result.get("RuleCategory", "")
            if rule_category and rule_category.lower() not in [t.lower() for t in tags]:
                tags.append(rule_category.lower())

            # Type annotation for mypy
            sarif_runs = sarif["runs"]
            if isinstance(sarif_runs, list) and len(sarif_runs) > 0:
                driver = sarif_runs[0]["tool"]["driver"]
                if isinstance(driver, dict) and "rules" in driver:
                    driver["rules"].append(
                        {
                            "id": rule_id,
                            "shortDescription": {"text": rule_id},
                            "properties": {"tags": tags, "category": result.get("RuleCategory", "")},
                        }
                    )
            rules_added.add(rule_id)

        # Add result
        sarif_result = {
            "ruleId": rule_id,
            "level": severity_map.get(severity, "warning"),
            "message": {"text": message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": f"file://{os.path.abspath(file_path)}"},
                        "region": {"startLine": line, "startColumn": column},
                    }
                }
            ],
        }

        # Type annotation for mypy
        sarif_runs = sarif["runs"]
        if isinstance(sarif_runs, list) and len(sarif_runs) > 0 and "results" in sarif_runs[0]:
            sarif_runs[0]["results"].append(sarif_result)

    return sarif


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="py-psscriptanalyzer - PowerShell static analysis and formatting")
    parser.add_argument(
        "--format",
        action="store_true",
        help="Format files instead of just analyzing them",
    )
    parser.add_argument(
        "--severity",
        choices=SEVERITY_LEVELS,
        default="Warning",
        help="Severity level to report: All (shows all levels), Information, Warning, Error (default: Warning)",
    )
    parser.add_argument("files", nargs="*", help="Files to check")

    args = parser.parse_args(argv)

    # Filter for PowerShell files
    ps_files = [f for f in args.files if f.endswith(POWERSHELL_FILE_EXTENSIONS)]

    if not ps_files:
        return 0

    # Find PowerShell
    powershell_cmd = find_powershell()
    if not powershell_cmd:
        print(
            "Error: PowerShell not found. Please install PowerShell Core (pwsh) or Windows PowerShell.",
            file=sys.stderr,
        )
        print(
            "Visit: https://github.com/PowerShell/PowerShell#get-powershell",
            file=sys.stderr,
        )
        return 1

    print(f"Using PowerShell: {powershell_cmd}")

    # Check if PSScriptAnalyzer is installed
    if not check_psscriptanalyzer_installed(powershell_cmd):
        if not install_psscriptanalyzer(powershell_cmd):
            print("Error: Failed to install PSScriptAnalyzer", file=sys.stderr)
            return 1
        print("PSScriptAnalyzer installed successfully")

    # Run the analysis or formatting
    action = "Formatting" if args.format else "Analyzing"
    print(f"{action} {len(ps_files)} PowerShell file(s)...")

    return run_script_analyzer(powershell_cmd, ps_files, format_files=args.format, severity=args.severity)
