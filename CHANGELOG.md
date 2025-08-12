# Change Log

## [0.3.0] - 2025-08-12

### Added

- **Rule Category Filtering**: Added specialized filtering options by rule category
  - `--style-only`: Filter for style/formatting rules
  - `--performance-only`: Filter for performance rules
  - `--security-only`: Filter for security rules
  - `--best-practices-only`: Filter for best practice rules
  - `--dsc-only`: Filter for DSC rules
  - `--compatibility-only`: Filter for compatibility rules
- **Rule Include/Exclude Options**: Added options to include or exclude specific rules
  - `--include-rules`: Specify rules to include
  - `--exclude-rules`: Specify rules to exclude
- **Multiple Output Formats**: Added support for different output formats
  - `--output-format`: Specify output format (text, json, sarif)
  - `--output-file`: Write output to a file instead of console
- **SARIF Output Support**: Added SARIF output format for integration with GitHub Code Scanning
  - Enhanced SARIF output with rule category tagging
- **Rule Categorization**: Added rule category property to results for better organization

## [0.2.0] - 2025-08-11

### Added

- **Hierarchical Severity System**: Implemented hierarchical severity filtering where each level includes more severe issues
  - `Information`: Shows all issues (Information + Warning + Error)
  - `Warning`: Shows Warning and Error issues (default)
  - `Error`: Shows only Error issues
- **Environment Variable Support**: Added `SEVERITY_LEVEL` environment variable to set default severity level
- **Recursive File Search**: Added `--recursive/-r` flag to search for PowerShell files recursively from current directory
- **Modern CLI with Rich Formatting**: Enhanced CLI interface with Rich library for beautiful terminal output
- **Improved Help System**: Professional help output with styled sections, tables, and examples

### Changed

- **Default Severity Behavior**: Changed default from showing all issues to showing Warning and Error issues only
- **CLI Architecture**: Modernized CLI architecture with Rich-based formatting and better error handling
- **Command Line Arguments**: Added short flag support (`-s`, `-r`, `-f`, `-v`, `-h`)

### Fixed

- **PowerShell Script Generation**: Improved PowerShell script generation for better filtering logic
- **Code Quality**: Refactored large functions to improve maintainability and readability

## [0.1.0] - 2025-08-11

### Added

- **PSScriptAnalyzer Integration**: Seamless integration with Microsoft's PSScriptAnalyzer for PowerShell static analysis
- **Pre-commit Hook Support**: Full compatibility with the pre-commit framework for automated code quality checks
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux with automatic PowerShell detection
- **Multiple PowerShell File Support**: Supports `.ps1`, `.psm1`, and `.psd1` file extensions
- **Configurable Severity Levels**: Filter analysis results by Error, Warning, Information, or All severity levels
- **Color-coded Terminal Output**: Enhanced readability with severity-based color coding in terminal output
- **GitHub Actions Integration**: Native support for GitHub Actions with proper error annotations (`::error`, `::warning`, `::notice`)
- **Automatic PowerShell Installation Detection**: Intelligent detection of PowerShell Core, Windows PowerShell, and pwsh installations
- **Comprehensive Documentation**: Complete documentation with installation guides, usage examples, and API reference
- **Professional Package Distribution**: Published to PyPI with proper metadata and dependency management

### Technical Features

- **Modern Python Packaging**: Built with `pyproject.toml` using modern Python packaging standards with src/ layout
- **Type Hints**: Full type annotation support for better IDE integration and maintainability
- **Robust Error Handling**: Comprehensive error handling with informative error messages
- **Environment-aware Output**: Different output formats for local development vs CI/CD environments
- **Zero Dependencies**: No external Python dependencies required for core functionality
- **Python 3.9+ Support**: Compatible with Python 3.9 through 3.13
- **Clean Code Architecture**: Modular codebase with proper separation of concerns and maintainable functions

### Documentation

- **ReadTheDocs Integration**: Professional documentation hosted at https://py-psscriptanalyzer.thetestlabs.io/
- **Comprehensive Guides**: Installation, usage, and configuration documentation
- **API Reference**: Complete function documentation with examples
- **CI/CD Examples**: Ready-to-use examples for GitHub Actions and other CI platforms
- **Troubleshooting Guide**: Common issues and solutions
- **Markdown-first Documentation**: Clean documentation structure using MyST Markdown parser

### Package Management

- **PyPI Distribution**: Available via `pip install py-psscriptanalyzer`
- **MIT License**: Open source with permissive MIT license
- **Professional Metadata**: Complete package metadata with proper classifiers and keywords
- **Automated Release Pipeline**: Full CI/CD pipeline with automated testing, building, and publishing

### Command Line Interface

- **Standalone CLI**: Available as `py-psscriptanalyzer` command after installation
- **Format Mode**: Support for `--format` flag to format PowerShell files
- **Severity Filtering**: Command-line options to filter by severity levels
- **File Pattern Matching**: Automatic detection and processing of PowerShell files

### Quality Assurance

- **Comprehensive Test Suite**: Full test coverage with unit tests and integration tests
- **Multi-platform Testing**: Automated testing on Windows, macOS, and Linux
- **Code Quality Tools**: Integrated with Ruff, MyPy, and pre-commit hooks
- **Security Best Practices**: Secure subprocess handling with proper input sanitization
- **Expected Failure Handling**: Robust test infrastructure that correctly handles expected analysis failures
