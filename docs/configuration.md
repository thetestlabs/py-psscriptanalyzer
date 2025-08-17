# Configuration

## Pre-commit Hook Configuration

### Basic Setup

Add py-psscriptanalyzer to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1  # Use the latest version
    hooks:
      - id: py-psscriptanalyzer        # Analyze PowerShell files
      - id: py-psscriptanalyzer-format # Format PowerShell files
```

### Severity Configuration

Configure which issues are reported based on severity:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      - id: py-psscriptanalyzer
        args: ["--severity", "Error"]  # Only show critical errors
```

**Available severity levels:**
- `Error`: Only critical errors
- `Warning`: Warnings and errors (default)
- `Information`: All issues including informational messages

### Environment Variables

Set default severity using the `SEVERITY_LEVEL` environment variable:

```bash
export SEVERITY_LEVEL=Error
```

Command line arguments always override environment variable settings.

### Rule Category Filtering

Filter analysis by rule category:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      - id: py-psscriptanalyzer
        args: ["--security-only"]  # Only security-related issues

      # Other available category filters:
      # args: ["--style-only"]
      # args: ["--performance-only"]
      # args: ["--best-practices-only"]
      # args: ["--dsc-only"]
      # args: ["--compatibility-only"]
```

### Include/Exclude Rules

Specify which rules to include or exclude:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      # Include only specific rules
      - id: py-psscriptanalyzer
        name: Security Rules Check
        args: ["--include-rules", "PSAvoidUsingPlainTextForPassword,PSAvoidUsingConvertToSecureStringWithPlainText"]

      # Exclude specific rules
      - id: py-psscriptanalyzer
        name: General Analysis (No Style)
        args: ["--exclude-rules", "PSAvoidSemicolonsAsLineTerminators,PSUseShouldProcessForStateChangingFunctions"]
```

### Output Formats

Generate different output formats:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      # SARIF output for GitHub Code Scanning
      - id: py-psscriptanalyzer
        name: PowerShell Security Scan
        args: ["--security-only", "--output-format", "sarif", "--output-file", "powershell-security.sarif"]

      # JSON output for further processing
      - id: py-psscriptanalyzer
        name: PowerShell Analysis (JSON)
        args: ["--output-format", "json", "--output-file", "analysis-results.json"]
```

### File Patterns and Exclusions

Customize which files are processed:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      - id: py-psscriptanalyzer
        files: ^src/.*\\.ps1$  # Only .ps1 files in src/ directory
        exclude: ^(tests/|examples/).*\\.ps1$  # Skip test and example files

      - id: py-psscriptanalyzer-format
        files: \\.(ps1|psm1)$  # Format .ps1 and .psm1 files
```

### Advanced Examples

#### Environment-Specific Configuration

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      # Strict analysis for production code
      - id: py-psscriptanalyzer
        name: Production Code Analysis
        files: ^src/.*\\.ps1$
        args: ["--severity", "Warning", "--security-only"]

      # Lenient analysis for test code
      - id: py-psscriptanalyzer
        name: Test Code Analysis
        files: ^tests/.*\\.ps1$
        args: ["--severity", "Error"]
```

#### Multiple Output Formats

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v0.3.1
    hooks:
      # Regular console output for developers
      - id: py-psscriptanalyzer
        name: PowerShell Analysis (Console)
        args: ["--recursive", "--severity", "Warning"]

      # SARIF output for CI/CD integration
      - id: py-psscriptanalyzer
        name: PowerShell Analysis (SARIF)
        args: ["--recursive", "--security-only", "--output-format", "sarif", "--output-file", "security-scan.sarif"]
```

## CI/CD Integration

### GitHub Actions

```yaml
name: PowerShell Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install py-psscriptanalyzer
        run: pip install py-psscriptanalyzer
      - name: Analyze PowerShell files
        run: py-psscriptanalyzer --recursive --severity Warning
```

### Azure DevOps

```yaml
steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.13'
- script: |
    pip install py-psscriptanalyzer
    py-psscriptanalyzer --recursive --severity Warning
  displayName: 'Analyze PowerShell Files'
```

### GitLab CI

```yaml
powershell_analysis:
  image: python:3.13
  before_script:
    - pip install py-psscriptanalyzer
  script:
    - py-psscriptanalyzer --recursive --severity Warning
  only:
    - merge_requests
    - main
```
