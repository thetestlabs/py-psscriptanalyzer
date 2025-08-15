[![codecov](https://codecov.io/github/thetestlabs/py-psscriptanalyzer/graph/badge.svg?token=B6K3MDQ2HF)](https://codecov.io/github/thetestlabs/py-psscriptanalyzer) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc86fb73526e4d649739e34158c2cb05)](https://app.codacy.com/gh/thetestlabs/py-psscriptanalyzer/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) [![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[![Python Compatibility](https://img.shields.io/pypi/pyversions/py-psscriptanalyzer)](https://pypi.org/project/py-psscriptanalyzer/)

[![docs](https://app.readthedocs.org/projects/py-psscriptanalyzer/badge/?version=latest)](https://readthedocs.org/projects/py-psscriptanalyzer/) [![Release](https://github.com/thetestlabs/py-psscriptanalyzer/actions/workflows/release.yaml/badge.svg)](https://github.com/thetestlabs/py-psscriptanalyzer/actions/workflows/release.yaml)

[![PyPI version](https://badge.fury.io/py/py-psscriptanalyzer.svg)](https://badge.fury.io/py/py-psscriptanalyzer) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# py-psscriptanalyzer

---

<div align="center">
  <strong><a href="https://py-psscriptanalyzer.thetestlabs.io">Read the full documentation on ReadTheDocs!</a></strong>
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

## Quick Start

1. **Install the package:**

   ```bash
   pip install py-psscriptanalyzer
   ```

2. **Use as a pre-commit hook:**

   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: https://github.com/thetestlabs/py-psscriptanalyzer
       rev: v0.3.1
       hooks:
         - id: py-psscriptanalyzer
         - id: py-psscriptanalyzer-format

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

- **Windows**: Get [PowerShell Core](https://github.com/PowerShell/PowerShell/releases)
- **macOS**: `brew install powershell`
- **Linux**: [Installation guide](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux)

## Documentation

Full documentation available at **[py-psscriptanalyzer.thetestlabs.io](https://py-psscriptanalyzer.thetestlabs.io/)**

## Contributing

Contributions welcome! See our [development guide](https://py-psscriptanalyzer.thetestlabs.io/en/latest/development.html) in the documentation.

## License

MIT - see [LICENSE](LICENSE) file.

A tool for linting and formatting PowerShell code using PSScriptAnalyzer.
