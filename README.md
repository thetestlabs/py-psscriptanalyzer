[![PyPI version](https://badge.fury.io/py/py-psscriptanalyzer.svg)](https://badge.fury.io/py/py-psscriptanalyzer)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python Compatibility](https://img.shields.io/pypi/pyversions/py-psscriptanalyzer)](https://pypi.org/project/py-psscriptanalyzer/)
[![codecov](https://codecov.io/github/thetestlabs/py-psscriptanalyzer/graph/badge.svg?token=B6K3MDQ2HF)](https://codecov.io/github/thetestlabs/py-psscriptanalyzer)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc86fb73526e4d649739e34158c2cb05)](https://app.codacy.com/gh/thetestlabs/py-psscriptanalyzer/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![docs](https://app.readthedocs.org/projects/py-psscriptanalyzer/badge/?version=latest)](https://readthedocs.org/projects/py-psscriptanalyzer/)
[![Release](https://github.com/thetestlabs/py-psscriptanalyzer/actions/workflows/release.yaml/badge.svg)](https://github.com/thetestlabs/py-psscriptanalyzer/actions/workflows/release.yaml)

# py-psscriptanalyzer

---

<div align="center">
  <strong><a href="https://py-psscriptanalyzer.thetestlabs.io">Read the documentation on ReadTheDocs!</a></strong>
</div>

---

A Python wrapper for [PSScriptAnalyzer](https://github.com/PowerShell/PSScriptAnalyzer) - bringing cross-platform PowerShell static analysis and formatting to your projects, including a `pre-commit` hook and integration with CI/CD tools

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

### Troubleshooting Installation

#### macOS/Linux: "externally-managed-environment" Error

If you encounter an "externally-managed-environment" error, you have several options:

1. **Use a virtual environment** (recommended):

   ```bash
   python3 -m venv py-psscriptanalyzer-env
   source py-psscriptanalyzer-env/bin/activate  # On Windows: py-psscriptanalyzer-env\Scripts\activate
   pip install py-psscriptanalyzer
   ```

2. **Use pipx** (for command-line use):

   ```bash
   # Install pipx if not already installed
   brew install pipx  # macOS
   # sudo apt install pipx  # Ubuntu/Debian

   # Install py-psscriptanalyzer with pipx
   pipx install py-psscriptanalyzer
   ```

3. **Install to user directory**:
   ```bash
   pip install --user py-psscriptanalyzer
   ```

**Note**: If you're using the package in a CI/CD environment, virtual environments or containers are typically the best approach.

## Usage

### Command Line

```bash
# Analyze PowerShell files
py-psscriptanalyzer script.ps1 module.psm1

# Format PowerShell files
py-psscriptanalyzer --format script.ps1

# Set severity level (hierarchical: Information > Warning > Error)
py-psscriptanalyzer --severity Error script.ps1        # Only errors
py-psscriptanalyzer --severity Warning script.ps1      # Warnings + errors (default)
py-psscriptanalyzer --severity Information script.ps1  # All issues

# Search recursively for PowerShell files
py-psscriptanalyzer --recursive

# Use environment variable for default severity
export SEVERITY_LEVEL=Error
py-psscriptanalyzer script.ps1  # Uses Error level
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
    rev: v0.3.1 # Use the latest version
    hooks:
      - id: py-psscriptanalyzer # Lint your PowerShell
      - id: py-psscriptanalyzer-format # Format your PowerShell
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
