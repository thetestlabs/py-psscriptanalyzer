"""PowerShell Script Analyzer pre-commit hook.

This module provides a Python wrapper around PowerShell's PSScriptAnalyzer
for use as a pre-commit hook to analyze PowerShell scripts for potential
issues, style violations, and best practice violations.

Key Features:
    - PowerShell script static analysis
    - Integration with pre-commit hooks
    - Configurable analysis rules
"""

__version__ = "0.3.1"

from .core import main, run_script_analyzer
from .powershell import check_psscriptanalyzer_installed, find_powershell, install_psscriptanalyzer

__all__ = [
    "main",
    "run_script_analyzer",
    "find_powershell",
    "check_psscriptanalyzer_installed",
    "install_psscriptanalyzer",
]
