"""Constants used throughout py-psscriptanalyzer."""

from typing import Final

# PowerShell executable names in order of preference
POWERSHELL_EXECUTABLES: Final[list[str]] = ["pwsh", "pwsh-lts", "powershell"]

# Supported PowerShell file extensions
POWERSHELL_FILE_EXTENSIONS: Final[tuple[str, ...]] = (".ps1", ".psm1", ".psd1")

# Severity levels for PSScriptAnalyzer
SEVERITY_LEVELS: Final[list[str]] = ["All", "Information", "Warning", "Error"]

# Timeouts (in seconds)
POWERSHELL_CHECK_TIMEOUT: Final[int] = 10
MODULE_CHECK_TIMEOUT: Final[int] = 30
INSTALL_TIMEOUT: Final[int] = 120
ANALYSIS_TIMEOUT: Final[int] = 300
