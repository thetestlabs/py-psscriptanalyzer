"""Modern CLI interface for PSScriptAnalyzer with Rich formatting."""

import argparse
import os
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.text import Text

from .core import run_script_analyzer
from .powershell import (
    check_psscriptanalyzer_installed,
    find_powershell,
    install_psscriptanalyzer,
)

# Create a simple console with minimal configuration for maximum compatibility
console = Console()


def get_default_severity() -> str:
    """Get the default severity level from environment variable or fallback to Warning."""
    env_severity = os.getenv("SEVERITY_LEVEL", "Warning")

    # Validate the environment variable value
    valid_severities = ["All", "Information", "Warning", "Error"]
    if env_severity in valid_severities:
        return env_severity
    # Don't use print_error here since console may not be initialized
    # Just silently fall back to Warning
    return "Warning"


class RichHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter using Rich for beautiful output."""

    def format_help(self) -> str:
        """Format the entire help message with Rich styling."""
        # Create the main help content
        help_text = Text()

        # Title section
        help_text.append("py-psscriptanalyzer", style="bold blue")
        help_text.append("\n")
        help_text.append("PowerShell static analysis and formatting", style="dim")
        help_text.append("\n\n")

        # Usage section
        help_text.append("USAGE", style="bold green")
        help_text.append("\n")
        help_text.append("  py-psscriptanalyzer [OPTIONS] [FILES...]", style="cyan")
        help_text.append("\n\n")

        # Description
        help_text.append("DESCRIPTION", style="bold green")
        help_text.append("\n")
        help_text.append("  Analyze and format PowerShell files using PSScriptAnalyzer.\n")
        help_text.append("  Supports .ps1, .psm1, and .psd1 files with cross-platform compatibility.\n\n")

        help_text.append("SEVERITY LEVELS", style="bold green")
        help_text.append("\n")
        help_text.append(
            "  Information: Shows all issues (Information, Warning, Error)\n",
            style="dim",
        )
        help_text.append("  Warning:     Shows Warning and Error issues (default)\n", style="dim")
        help_text.append("  Error:       Shows only Error issues\n", style="dim")
        help_text.append("  \n")
        help_text.append(
            "  Set SEVERITY_LEVEL environment variable to change the default.\n",
            style="yellow",
        )
        help_text.append("\n")

        # Create options table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="cyan", width=20)
        table.add_column("Description", style="white")

        table.add_row("--format, -f", "Format files instead of analyzing them")
        table.add_row(
            "--severity, -s",
            "Set minimum severity level: Information (all), Warning (warn+error), Error (error only)",
        )
        table.add_row(
            "--recursive, -r",
            "Search for PowerShell files recursively from current directory",
        )
        table.add_row("--help, -h", "Show this help message")
        table.add_row("--version, -v", "Show version information")
        table.add_row()

        # Rule category filters
        table.add_row("--security-only", "Only show security-related findings")
        table.add_row("--style-only", "Only show code style-related findings")
        table.add_row("--performance-only", "Only show performance-related findings")
        table.add_row("--best-practices-only", "Only show best practices-related findings")
        table.add_row("--dsc-only", "Only show DSC (Desired State Configuration) related findings")
        table.add_row("--compatibility-only", "Only show compatibility-related findings")
        table.add_row()

        # Custom rule selection
        table.add_row("--include-rules", "Comma-separated list of specific rule names to include")
        table.add_row("--exclude-rules", "Comma-separated list of specific rule names to exclude")
        table.add_row()

        # Output format options
        table.add_row("--output-format", "Output format: text, json, or sarif (default: text)")
        table.add_row("--output-file", "File to write output to (default: output to console)")

        # Examples section
        examples_text = Text()
        examples_text.append("EXAMPLES", style="bold green")
        examples_text.append("\n")
        examples_text.append("  # Analyze PowerShell files\n", style="dim")
        examples_text.append("  py-psscriptanalyzer script.ps1 module.psm1\n\n", style="cyan")
        examples_text.append("  # Format PowerShell files\n", style="dim")
        examples_text.append("  py-psscriptanalyzer --format script.ps1\n\n", style="cyan")
        examples_text.append("  # Search recursively for PowerShell files\n", style="dim")
        examples_text.append("  py-psscriptanalyzer --recursive\n\n", style="cyan")
        examples_text.append("  # Show only errors\n", style="dim")
        examples_text.append("  py-psscriptanalyzer --severity Error *.ps1\n\n", style="cyan")
        examples_text.append("  # Show all issues (including informational)\n", style="dim")
        examples_text.append("  py-psscriptanalyzer --severity Information script.ps1\n\n", style="cyan")
        examples_text.append("  # Use environment variable for default severity\n", style="dim")
        examples_text.append(
            "  export SEVERITY_LEVEL=Error && py-psscriptanalyzer *.ps1\n\n",
            style="cyan",
        )
        examples_text.append("  # Filter for security-related issues only\n", style="dim")
        examples_text.append("  py-psscriptanalyzer --security-only script.ps1\n\n", style="cyan")
        examples_text.append("  # Include only specific rules\n", style="dim")
        examples_text.append(
            "  py-psscriptanalyzer --include-rules PSAvoidUsingPlainTextForPassword,\\\n"
            "    PSAvoidUsingWriteHost script.ps1\n\n",
            style="cyan",
        )
        examples_text.append("  # Generate SARIF output for code scanning integration\n", style="dim")
        examples_text.append(
            "  py-psscriptanalyzer --output-format sarif --output-file results.sarif *.ps1\n\n",
            style="cyan",
        )

        # Render everything to console and capture
        with console.capture() as capture:
            # Print header sections without panel
            console.print(help_text)

            # Add a separator line (ASCII-safe for Windows compatibility)
            console.print("-" * min(console.width, 80), style="bold blue")
            console.print()

            console.print("OPTIONS", style="bold green")
            console.print(table)
            console.print()

            # Add another separator line before examples
            console.print("-" * min(console.width, 80), style="bold blue")
            console.print()

            console.print(examples_text)

        return str(capture.get())


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="py-psscriptanalyzer",
        description="A Python wrapper for PowerShell Script Analyzer",
        formatter_class=RichHelpFormatter,
        add_help=False,  # We'll handle help ourselves
    )

    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search for PowerShell files recursively from current directory",
    )

    parser.add_argument(
        "-f",
        "--format",
        action="store_true",
        help="Format files instead of just analyzing them",
    )

    parser.add_argument(
        "-s",
        "--severity",
        choices=["All", "Information", "Warning", "Error"],
        default=get_default_severity(),
        help="Severity level to report (default: from SEVERITY_LEVEL env var or Warning)",
    )

    # Rule category filters
    rule_filter_group = parser.add_argument_group("Rule category filters")
    rule_filter_group.add_argument(
        "--security-only",
        action="store_true",
        help="Only show security-related findings",
    )
    rule_filter_group.add_argument(
        "--style-only",
        action="store_true",
        help="Only show code style-related findings",
    )
    rule_filter_group.add_argument(
        "--performance-only",
        action="store_true",
        help="Only show performance-related findings",
    )
    rule_filter_group.add_argument(
        "--best-practices-only",
        action="store_true",
        help="Only show best practices-related findings",
    )
    rule_filter_group.add_argument(
        "--dsc-only",
        action="store_true",
        help="Only show DSC (Desired State Configuration) related findings",
    )
    rule_filter_group.add_argument(
        "--compatibility-only",
        action="store_true",
        help="Only show compatibility-related findings",
    )

    # Custom rule selection
    rule_filter_group.add_argument("--include-rules", help="Comma-separated list of specific rule names to include")
    rule_filter_group.add_argument("--exclude-rules", help="Comma-separated list of specific rule names to exclude")

    # Output format options
    parser.add_argument(
        "--output-format",
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument("--output-file", help="File to write output to (default: output to console)")

    parser.add_argument("-v", "--version", action="store_true", help="Show version information and exit")

    parser.add_argument("files", nargs="*", help="PowerShell files to analyze")

    return parser


def _get_version_display() -> str:
    """Get formatted version information."""
    try:
        from . import __version__

        return f"py-psscriptanalyzer {__version__}"
    except ImportError:
        return "py-psscriptanalyzer (unknown version)"


def print_status(message: str, style: str = "white") -> None:
    """Print a status message with Rich formatting."""
    console.print(f"[{style}]{message}[/{style}]")


def print_error(message: str) -> None:
    """Print an error message with Rich formatting."""
    console.print(f"[red]Error:[/red] {message}")


def print_success(message: str) -> None:
    """Print a success message with Rich formatting."""
    console.print(f"[green]OK[/green] {message}")


def find_powershell_files_recursive(start_dir: Optional[Path] = None) -> list[str]:
    """Find PowerShell files recursively from the start directory."""
    from .constants import POWERSHELL_FILE_EXTENSIONS

    if start_dir is None:
        start_dir = Path.cwd()

    ps_files: list[str] = []
    for ext in POWERSHELL_FILE_EXTENSIONS:
        pattern = f"**/*{ext}"
        ps_files.extend(str(p) for p in start_dir.glob(pattern))

    return sorted(ps_files)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Modern main entry point with Rich formatting."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle version display
    if args.version:
        console.print(_get_version_display(), style="bold blue")
        return 0

    # Get PowerShell files
    from .constants import POWERSHELL_FILE_EXTENSIONS

    if args.recursive:
        # Find PowerShell files recursively
        print_status("Searching for PowerShell files recursively...", "blue")
        ps_files = find_powershell_files_recursive()
        if ps_files:
            print_success(f"Found {len(ps_files)} PowerShell file(s)")
        else:
            print_status("No PowerShell files found", "yellow")
            return 0
    else:
        # Use files from command line arguments
        ps_files = [f for f in args.files if f.endswith(POWERSHELL_FILE_EXTENSIONS)]

    if not ps_files:
        if not args.recursive:
            print_status("No PowerShell files specified", "yellow")
        return 0

    # Find PowerShell
    print_status("Finding PowerShell installation...", "blue")
    powershell_cmd = find_powershell()
    if not powershell_cmd:
        print_error("PowerShell not found. Please install PowerShell Core (pwsh) or Windows PowerShell.")
        print_status("Visit: https://github.com/PowerShell/PowerShell#get-powershell", "dim")
        return 1

    print_success(f"Using PowerShell: {powershell_cmd}")

    # Check if PSScriptAnalyzer is installed
    print_status("Checking PSScriptAnalyzer installation...", "blue")
    if not check_psscriptanalyzer_installed(powershell_cmd):
        print_status("PSScriptAnalyzer not found. Installing...", "yellow")
        if not install_psscriptanalyzer(powershell_cmd):
            print_error("Failed to install PSScriptAnalyzer")
            return 1
        print_success("PSScriptAnalyzer installed successfully")
    else:
        print_success("PSScriptAnalyzer is available")

    # Run the analysis or formatting
    action = "Formatting" if args.format else "Analyzing"

    # Update action description based on rule filter
    filter_description = ""
    if not args.format:
        if args.security_only:
            filter_description = " (security rules only)"
        elif args.style_only:
            filter_description = " (style rules only)"
        elif args.performance_only:
            filter_description = " (performance rules only)"
        elif args.best_practices_only:
            filter_description = " (best practices only)"
        elif args.dsc_only:
            filter_description = " (DSC rules only)"
        elif args.compatibility_only:
            filter_description = " (compatibility rules only)"
        elif args.include_rules:
            filter_description = " (specific included rules)"
        elif args.exclude_rules:
            filter_description = " (with specific rules excluded)"

    print_status(f"{action}{filter_description} {len(ps_files)} PowerShell file(s)...", "blue")

    # Parse include/exclude rules if specified
    include_rules = args.include_rules.split(",") if args.include_rules else None
    exclude_rules = args.exclude_rules.split(",") if args.exclude_rules else None

    result = run_script_analyzer(
        powershell_cmd,
        ps_files,
        format_files=args.format,
        severity=args.severity,
        security_only=args.security_only,
        style_only=args.style_only,
        performance_only=args.performance_only,
        best_practices_only=args.best_practices_only,
        dsc_only=args.dsc_only,
        compatibility_only=args.compatibility_only,
        include_rules=include_rules,
        exclude_rules=exclude_rules,
        output_format=args.output_format,
        output_file=args.output_file,
    )

    if result == 0 and not args.format and args.output_format == "text":
        print_success("No issues found")

    return result
