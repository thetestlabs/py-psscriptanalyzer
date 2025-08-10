# py-psscriptanalyzer

[![PyPI version](https://badge.fury.io/py/py-psscriptanalyzer.svg)](https://badge.fury.io/py/py-psscriptanalyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python Compatibility](https://img.shields.io/pypi/pyversions/py-psscriptanalyzer)](https://pypi.org/project/py-psscriptanalyzer/)

---

**[Read the documentation on ReadTheDocs!](https://py-psscriptanalyzer.thetestlabs.io)**

---

A Python wrapper for [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer) - bringing PowerShell static analysis and formatting to your Python workflows!

## What it does

✅ **Lints PowerShell files** (`.ps1`, `.psm1`, `.psd1`) for code quality issues  
✅ **Formats PowerShell code** automatically  
✅ **Works everywhere** - Windows, macOS, Linux  
✅ **Zero config** - installs PSScriptAnalyzer automatically  
✅ **GitHub Actions ready** - with standard error annotations  
✅ **CI/CD friendly** - perfect for automation pipelines  
✅ **Pre-commit hooks** - catch issues before they hit your repo  

## Installation

```bash
pip install py-psscriptanalyzer
```

## Usage

### Command Line

```bash
# Analyze PowerShell files
py-psscriptanalyzer script.ps1 module.psm1

# Format PowerShell files
py-psscriptanalyzer --format script.ps1

# Set severity level
py-psscriptanalyzer --severity Error script.ps1

# Show all issues
py-psscriptanalyzer --severity All script.ps1
```

### Python API

```python
from py_psscriptanalyzer import run_script_analyzer, find_powershell

# Find PowerShell installation
powershell_cmd = find_powershell()

# Analyze files
exit_code = run_script_analyzer(
    powershell_cmd, 
    ["script.ps1"], 
    severity="Warning"
)

# Format files
exit_code = run_script_analyzer(
    powershell_cmd, 
    ["script.ps1"], 
    format_files=True
)
```

### Pre-commit Hooks

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      - id: py-psscriptanalyzer        # Lint your PowerShell
      - id: py-psscriptanalyzer-format  # Format your PowerShell
```

### GitHub Actions

```yaml
- name: Analyze PowerShell
  run: |
    pip install py-psscriptanalyzer
    py-psscriptanalyzer --severity Error **/*.ps1
```

## Prerequisites

- Python 3.9+
- PowerShell (any version - we'll find it!)

Need PowerShell? Get it here:

- **Windows**: Already installed, or get [PowerShell Core](https://github.com/PowerShell/PowerShell/releases)
- **macOS**: `brew install powershell`
- **Linux**: [Installation guide](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux)

## Documentation

Full documentation available at **[py-psscriptanalyzer.thetestlabs.io](https://py-psscriptanalyzer.thetestlabs.io/)**

## Contributing

Contributions welcome! See our development guide in the documentation.

## License

MIT - see [LICENSE](LICENSE) file.

A tool for linting and formatting PowerShell code using PSScriptAnalyzer.
