"""Core PSScriptAnalyzer functionality."""

import argparse
import subprocess
import sys
from collections.abc import Sequence
from typing import Optional

from .constants import ANALYSIS_TIMEOUT, POWERSHELL_FILE_EXTENSIONS, SEVERITY_LEVELS
from .powershell import check_psscriptanalyzer_installed, find_powershell, install_psscriptanalyzer
from .scripts import build_powershell_file_array, generate_analysis_script, generate_format_script


def run_script_analyzer(
    powershell_cmd: str,
    files: list[str],
    format_files: bool = False,
    severity: str = "Warning",
) -> int:
    """Run PSScriptAnalyzer on the given files."""
    if not files:
        return 0

    files_param = build_powershell_file_array(files)

    if format_files:
        ps_command = generate_format_script(files_param)
    else:
        ps_command = generate_analysis_script(files_param, severity)

    try:
        result = subprocess.run(
            [powershell_cmd, "-Command", ps_command],
            text=True,
            timeout=ANALYSIS_TIMEOUT,
            check=False,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        print("Timeout while running PSScriptAnalyzer")
        return 1


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
