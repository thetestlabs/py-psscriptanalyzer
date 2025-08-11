# Usage

## Command Line Usage

py-psscriptanalyzer can be used both as a standalone command-line tool and as a pre-commit hook.

### Basic Command Line

Analyze PowerShell files directly:

```bash
# Analyze a single file
py-psscriptanalyzer script.ps1

# Analyze multiple files
py-psscriptanalyzer script1.ps1 module.psm1 manifest.psd1

# Analyze all PowerShell files in current directory
py-psscriptanalyzer *.ps1

# Format a file
py-psscriptanalyzer --format script.ps1
```

### Command Line Options

```bash
py-psscriptanalyzer --help
```

Available options:

- `--format, -f`: Format PowerShell files instead of analyzing
- `--severity, -s {Information,Warning,Error,All}`: Set minimum severity level (hierarchical)
- `--recursive, -r`: Search for PowerShell files recursively from current directory
- `--version, -v`: Show version information
- `--help, -h`: Show help message

### Severity Levels

py-psscriptanalyzer uses a **hierarchical severity system**:

- **`Information`**: Shows all issues (Information, Warning, Error) - most comprehensive
- **`Warning`**: Shows Warning and Error issues (default) - recommended for most use cases
- **`Error`**: Shows only Error issues - most strict, only critical problems

The default severity level is **Warning**, but you can customize this using:

1. **Command line argument**: `--severity Error`
2. **Environment variable**: `export SEVERITY_LEVEL=Error`

Command line arguments always override environment variable settings.

### Environment Variables

Set the `SEVERITY_LEVEL` environment variable to change the default severity:

```bash
# Set default to Error level
export SEVERITY_LEVEL=Error
py-psscriptanalyzer script.ps1

# Override environment variable with command line
export SEVERITY_LEVEL=Error
py-psscriptanalyzer --severity Warning script.ps1  # Uses Warning, not Error
```

Valid values: `Information`, `Warning`, `Error`, `All`

### Examples

#### Basic Analysis

```bash
# Analyze with default settings (Warning and Error issues)
py-psscriptanalyzer MyScript.ps1

# Show all issues including informational
py-psscriptanalyzer --severity Information MyScript.ps1

# Show only critical errors
py-psscriptanalyzer --severity Error MyScript.ps1

# Search recursively for PowerShell files
py-psscriptanalyzer --recursive

# Use environment variable for default severity
export SEVERITY_LEVEL=Error
py-psscriptanalyzer MyScript.ps1  # Uses Error level

# Override environment variable
export SEVERITY_LEVEL=Error
py-psscriptanalyzer --severity Information MyScript.ps1  # Uses Information level
```

#### Recursive File Search

```bash
# Analyze all PowerShell files in current directory and subdirectories
py-psscriptanalyzer --recursive

# Combine with severity filtering
py-psscriptanalyzer --recursive --severity Error

# Combine with formatting (format all found files)
py-psscriptanalyzer --recursive --format
```

The recursive search will find all files with extensions: `.ps1`, `.psm1`, `.psd1`

#### Code Formatting

```bash
# Format a single file
py-psscriptanalyzer --format MyScript.ps1

# Format multiple files
py-psscriptanalyzer --format *.ps1
```

## Pre-commit Hook Usage

### Available Hooks

The package provides two main hooks:

1. **`py-psscriptanalyzer`** - Static analysis and linting
2. **`py-psscriptanalyzer-format`** - Code formatting

### Automatic Execution

When you commit PowerShell files (`.ps1`, `.psm1`, `.psd1`), the hooks will automatically:

1. **Analysis Hook**: Check for code quality issues, style violations, and potential bugs
2. **Format Hook**: Apply consistent formatting to your PowerShell code

```bash
git add MyScript.ps1
git commit -m "Add new PowerShell script"
# Hooks run automatically
```

### Manual Execution

You can also run the hooks manually:

#### Run All Hooks

```bash
# Run on all PowerShell files
pre-commit run --all-files

# Run on specific files
pre-commit run --files MyScript.ps1 MyModule.psm1
```

#### Run Specific Hooks

```bash
# Run only the analyzer
pre-commit run py-psscriptanalyzer --all-files

# Run only the formatter
pre-commit run py-psscriptanalyzer-format --all-files
```

### Hook Configuration

You can customize the hooks in your `.pre-commit-config.yaml`:

```yaml
  repos:
    - repo: https://github.com/thetestlabs/py-psscriptanalyzer
      rev: v0.2.0
      hooks:
      # Analyzer with custom severity
      - id: py-psscriptanalyzer
        args: ["--severity", "Warning"]

      # Formatter (no additional args needed)
      - id: py-psscriptanalyzer-format
```

## File Types

py-psscriptanalyzer automatically processes the following PowerShell file types:

- **`.ps1`** - PowerShell scripts
- **`.psm1`** - PowerShell modules  
- **`.psd1`** - PowerShell data/manifest files

## Output Examples

### Analysis Output

```bash
$ py-psscriptanalyzer bad-script.ps1

PSScriptAnalyzer found 2 issue(s):

ERROR: [PSAvoidUsingCmdletAliases] Line 5: 'ls' is an alias of 'Get-ChildItem'. Alias can introduce possible problems and make scripts hard to maintain. Please consider changing alias to its full content.

WARNING: [PSAvoidUsingWriteHost] Line 8: Avoid using Write-Host because it might not work in all hosts, does not work when there is no host, and (prior to PS 5.0) cannot be suppressed, captured, or redirected. Instead, use Write-Output, Write-Verbose, or Write-Information.
```

### Format Output

```bash
$ py-psscriptanalyzer --format script.ps1

Formatted 1 file(s):
  ✓ script.ps1
```

### Success Output

```bash
$ py-psscriptanalyzer good-script.ps1

✓ No issues found in PowerShell files.
```

## Integration Examples

### GitHub Actions

```yaml
name: PowerShell Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install PowerShell
        run: |
          sudo snap install powershell --classic

      - name: Install py-psscriptanalyzer
        run: pip install py-psscriptanalyzer

      - name: Analyze PowerShell files
        run: py-psscriptanalyzer **/*.ps1
```

### Azure Pipelines

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    sudo snap install powershell --classic
  displayName: 'Install PowerShell'

- script: |
    pip install py-psscriptanalyzer
  displayName: 'Install py-psscriptanalyzer'

- script: |
    py-psscriptanalyzer **/*.ps1
  displayName: 'Analyze PowerShell files'
```

## Best Practices

### Development Workflow

1. **Install pre-commit hooks** in your development repository
2. **Run formatting first** to fix style issues automatically
3. **Address analysis issues** to improve code quality
4. **Commit clean code** that passes all checks

### Continuous Integration

1. **Install PowerShell** in your CI environment
2. **Run analysis** as part of your build process
3. **Fail builds** on serious issues (errors/warnings)
4. **Generate reports** for code quality tracking

### Team Usage

1. **Standardize configuration** across team repositories
2. **Document custom rules** and severity levels
3. **Train team members** on PowerShell best practices
4. **Review analysis results** during code reviews

## Quick Reference

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--format` | `-f` | Format files instead of analyzing |
| `--severity` | `-s` | Set severity level (Information/Warning/Error) |
| `--recursive` | `-r` | Search files recursively |
| `--version` | `-v` | Show version information |
| `--help` | `-h` | Show help message |

### Severity Levels

| Level | Shows | Use Case |
|-------|-------|----------|
| `Information` | All issues | Development, comprehensive analysis |
| `Warning` | Warning + Error | Default, recommended for most projects |
| `Error` | Error only | CI/CD, strict quality gates |

### Environment Variables

| Variable | Values | Default |
|----------|--------|---------|
| `SEVERITY_LEVEL` | Information, Warning, Error, All | Warning |

### Common Commands

```bash
# Basic analysis
py-psscriptanalyzer script.ps1

# Recursive analysis with Error level
py-psscriptanalyzer --recursive --severity Error

# Format all files in project
py-psscriptanalyzer --recursive --format

# Use environment variable
export SEVERITY_LEVEL=Information && py-psscriptanalyzer --recursive
```

### Team Best Practices

1. **Standardize configuration** across team repositories
2. **Document custom rules** and severity levels
3. **Train team members** on PowerShell best practices
4. **Review analysis results** during code reviews
