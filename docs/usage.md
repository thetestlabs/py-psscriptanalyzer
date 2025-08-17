# Usage

## Command Line Usage

py-psscriptanalyzer provides PowerShell static analysis and formatting from the command line.

### Basic Commands

```bash
# Analyze a single file
py-psscriptanalyzer script.ps1

# Analyze multiple files
py-psscriptanalyzer script1.ps1 module.psm1 manifest.psd1

# Analyze all PowerShell files recursively
py-psscriptanalyzer --recursive

# Format a PowerShell file
py-psscriptanalyzer --format script.ps1
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--severity` | Set severity level (Error, Warning, Information) | `--severity Error` |
| `--recursive` | Find PowerShell files recursively | `--recursive` |
| `--format` | Format files instead of analyzing | `--format` |
| `--output-format` | Output format (text, json, sarif) | `--output-format json` |
| `--output-file` | Write output to file | `--output-file results.json` |
| `--security-only` | Show only security issues | `--security-only` |
| `--style-only` | Show only style issues | `--style-only` |
| `--performance-only` | Show only performance issues | `--performance-only` |
| `--best-practices-only` | Show only best practice issues | `--best-practices-only` |
| `--dsc-only` | Show only DSC issues | `--dsc-only` |
| `--compatibility-only` | Show only compatibility issues | `--compatibility-only` |
| `--include-rules` | Include only specific rules | `--include-rules Rule1,Rule2` |
| `--exclude-rules` | Exclude specific rules | `--exclude-rules Rule1,Rule2` |

### Severity Levels

py-psscriptanalyzer uses hierarchical severity filtering:

- **`Error`**: Only critical errors that must be fixed
- **`Warning`**: Warnings and errors (default)
- **`Information`**: All issues including informational messages

```bash
# Show only critical errors
py-psscriptanalyzer --severity Error script.ps1

# Show warnings and errors (default)
py-psscriptanalyzer --severity Warning script.ps1

# Show all issues
py-psscriptanalyzer --severity Information script.ps1
```

### Environment Variables

Set the `SEVERITY_LEVEL` environment variable to change the default:

```bash
# Set default severity
export SEVERITY_LEVEL=Error
py-psscriptanalyzer script.ps1  # Uses Error level

# Command line always overrides environment variables
export SEVERITY_LEVEL=Error
py-psscriptanalyzer --severity Warning script.ps1  # Uses Warning level
```

### Rule Filtering

#### By Category

Filter by PSScriptAnalyzer rule categories:

```bash
# Security-focused analysis
py-psscriptanalyzer --security-only script.ps1

# Style and formatting issues
py-psscriptanalyzer --style-only script.ps1

# Performance-related issues
py-psscriptanalyzer --performance-only script.ps1

# Best practice violations
py-psscriptanalyzer --best-practices-only script.ps1

# DSC-specific issues
py-psscriptanalyzer --dsc-only script.ps1

# Compatibility issues
py-psscriptanalyzer --compatibility-only script.ps1
```

#### By Specific Rules

Include or exclude specific PSScriptAnalyzer rules:

```bash
# Include only specific rules
py-psscriptanalyzer --include-rules PSAvoidUsingPlainTextForPassword,PSAvoidUsingConvertToSecureStringWithPlainText script.ps1

# Exclude specific rules
py-psscriptanalyzer --exclude-rules PSAvoidUsingWriteHost,PSAvoidUsingPositionalParameters script.ps1

# Combine with other filters
py-psscriptanalyzer --severity Error --security-only --exclude-rules PSAvoidDefaultValueSwitchParameter script.ps1
```

### Output Formats

#### Text Output (Default)

Standard console output with color coding:

```bash
py-psscriptanalyzer script.ps1
```

#### JSON Output

Machine-readable JSON format:

```bash
# Output to console
py-psscriptanalyzer --output-format json script.ps1

# Save to file
py-psscriptanalyzer --output-format json --output-file results.json script.ps1
```

#### SARIF Output

Static Analysis Results Interchange Format for GitHub Code Scanning:

```bash
# Generate SARIF file for GitHub integration
py-psscriptanalyzer --output-format sarif --output-file powershell-analysis.sarif --recursive
```

### Formatting

Format PowerShell files using Invoke-Formatter:

```bash
# Format a single file
py-psscriptanalyzer --format script.ps1

# Format multiple files
py-psscriptanalyzer --format script1.ps1 script2.ps1

# Format all PowerShell files recursively
py-psscriptanalyzer --format --recursive
```

### Recursive Processing

Process all PowerShell files in the current directory and subdirectories:

```bash
# Analyze all PowerShell files
py-psscriptanalyzer --recursive

# Format all PowerShell files
py-psscriptanalyzer --format --recursive

# Combine with other options
py-psscriptanalyzer --recursive --severity Error --security-only
```

### Exit Codes

py-psscriptanalyzer returns standard exit codes:

- `0`: Success (no issues found or formatting completed)
- `1`: Issues found or errors occurred
- `2`: Invalid arguments or configuration

### Examples

#### Basic Analysis

```bash
# Quick check with default settings
py-psscriptanalyzer MyScript.ps1

# Comprehensive analysis
py-psscriptanalyzer --recursive --severity Information

# Security audit
py-psscriptanalyzer --recursive --security-only --severity Error
```

#### Output to Files

```bash
# JSON report for CI/CD
py-psscriptanalyzer --recursive --output-format json --output-file analysis.json

# SARIF for GitHub Code Scanning
py-psscriptanalyzer --security-only --recursive --output-format sarif --output-file security.sarif
```

#### Custom Rule Sets

```bash
# Focus on critical security rules only
py-psscriptanalyzer --include-rules PSAvoidUsingPlainTextForPassword,PSAvoidUsingConvertToSecureStringWithPlainText --severity Error script.ps1

# Exclude noisy style rules
py-psscriptanalyzer --exclude-rules PSAvoidUsingWriteHost,PSAvoidSemicolonsAsLineTerminators script.ps1
```

## Pre-commit Hook Usage

For pre-commit hook configuration, see the [Configuration](configuration.md) documentation.

## Integration with IDEs

### VS Code

py-psscriptanalyzer can be integrated with VS Code through tasks or extensions that support external linters.

### Other Editors

Any editor that supports external command execution can integrate py-psscriptanalyzer for PowerShell analysis.
