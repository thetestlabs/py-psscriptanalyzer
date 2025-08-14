# py-psscriptanalyzer

A Python wrapper for PSScriptAnalyzer that provides PowerShell static analysis and formatting capabilities.

```{toctree}
:maxdepth: 2
:caption: Contents

installation
usage
configuration
development
api
changelog
```

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
   ```

3. **Or use directly from command line:**

   ```bash
   py-psscriptanalyzer script.ps1
   py-psscriptanalyzer --format script.ps1
   ```

## Features

- **Static Analysis**: Comprehensive PowerShell code analysis using PSScriptAnalyzer
- **Code Formatting**: Automatic PowerShell code formatting with Invoke-Formatter
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Configurable**: Customizable severity levels and rule selection
- **Fast**: Efficient processing with proper error handling
- **Modern Python**: Built with modern Python packaging standards
- **CLI Tool**: Standalone command-line interface
- **Pre-commit Integration**: Ready-to-use pre-commit hooks
