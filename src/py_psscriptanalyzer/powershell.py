"""PowerShell detection and module management utilities."""

import subprocess
from typing import Optional

from .constants import (
    INSTALL_TIMEOUT,
    MODULE_CHECK_TIMEOUT,
    POWERSHELL_CHECK_TIMEOUT,
    POWERSHELL_EXECUTABLES,
)


def find_powershell() -> Optional[str]:
    """Find PowerShell executable on the system."""
    for name in POWERSHELL_EXECUTABLES:
        try:
            result = subprocess.run(
                [name, "-Command", "$PSVersionTable.PSVersion"],
                capture_output=True,
                text=True,
                timeout=POWERSHELL_CHECK_TIMEOUT,
                check=False,
            )
            if result.returncode == 0:
                return name
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    return None


def check_psscriptanalyzer_installed(powershell_cmd: str) -> bool:
    """Check if PSScriptAnalyzer module is available."""
    try:
        result = subprocess.run(
            [
                powershell_cmd,
                "-Command",
                "Get-Module -ListAvailable -Name PSScriptAnalyzer",
            ],
            capture_output=True,
            text=True,
            timeout=MODULE_CHECK_TIMEOUT,
            check=False,
        )
        return result.returncode == 0 and "PSScriptAnalyzer" in result.stdout
    except subprocess.TimeoutExpired:
        return False


def install_psscriptanalyzer(powershell_cmd: str) -> bool:
    """Install PSScriptAnalyzer module."""
    print("PSScriptAnalyzer not found. Installing...")
    try:
        result = subprocess.run(
            [
                powershell_cmd,
                "-Command",
                "Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser",
            ],
            capture_output=True,
            text=True,
            timeout=INSTALL_TIMEOUT,
            check=False,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Timeout while installing PSScriptAnalyzer")
        return False
