# Change Log

## [1.0.0] - 2025-08-10

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

### Documentation

- **ReadTheDocs Integration**: Professional documentation hosted at https://py-psscriptanalyzer.thetestlabs.io/
- **Comprehensive Guides**: Installation, usage, and configuration documentation
- **API Reference**: Complete function documentation with examples
- **CI/CD Examples**: Ready-to-use examples for GitHub Actions and other CI platforms
- **Troubleshooting Guide**: Common issues and solutions

### Package Management

- **PyPI Distribution**: Available via `pip install py-psscriptanalyzer`
- **MIT License**: Open source with permissive MIT license
- **Professional Metadata**: Complete package metadata with proper classifiers and keywords

### Command Line Interface

- **Standalone CLI**: Available as `py-psscriptanalyzer` command after installation
- **Format Mode**: Support for `--format` flag to format PowerShell files
- **Severity Filtering**: Command-line options to filter by severity levels
- **File Pattern Matching**: Automatic detection and processing of PowerShell files
