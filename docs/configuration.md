# Configuration

## Pre-commit Hook Configuration

### Basic Configuration

Add py-psscriptanalyzer to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0  # Use the latest version
    hooks:
      - id: py-psscriptanalyzer
      - id: py-psscriptanalyzer-format
```

### Severity Levels

Control which issues are reported by setting the severity level:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      - id: py-psscriptanalyzer
        args: ["--severity", "Error"]  # Only show errors
```

Available severity levels:

- **`Error`**: Only critical issues that prevent code execution
- **`Warning`**: Style issues and potential problems (default for most rules)
- **`Information`**: Minor style suggestions
- **`All`**: All issues (default)

### File Patterns

By default, the hooks run on all PowerShell files. You can customize this:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      - id: py-psscriptanalyzer
        files: \\.ps1$  # Only .ps1 files
      
      - id: py-psscriptanalyzer-format
        files: ^src/.*\\.(ps1|psm1)$  # Only files in src/ directory
```

### Excluding Files

Exclude specific files or directories:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      - id: py-psscriptanalyzer
        exclude: ^(tests/|examples/).*\\.ps1$  # Skip test and example files
```

### Advanced Configuration Examples

#### Separate Analysis and Formatting

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      # Strict analysis for main code
      - id: py-psscriptanalyzer
        name: PowerShell Analysis (Strict)
        files: ^src/.*\\.ps1$
        args: ["--severity", "Warning"]
      
      # Lenient analysis for tests
      - id: py-psscriptanalyzer
        name: PowerShell Analysis (Tests)
        files: ^tests/.*\\.ps1$
        args: ["--severity", "Error"]
      
      # Format all PowerShell files
      - id: py-psscriptanalyzer-format
        name: PowerShell Formatting
```

#### Integration with Other Hooks

```yaml
repos:
  # Other language hooks
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff

  # PowerShell hooks
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0
    hooks:
      - id: py-psscriptanalyzer
      - id: py-psscriptanalyzer-format
```

## PSScriptAnalyzer Configuration

### PowerShell Profile Configuration

You can configure PSScriptAnalyzer behavior in your PowerShell profile or via `.psscriptanalyzer-settings.psd1` files.

#### Example Settings File

Create a `.psscriptanalyzer-settings.psd1` file in your project root:

```powershell
@{
    # Severity levels to include
    Severity = @('Error', 'Warning')
    
    # Rules to exclude
    ExcludeRules = @(
        'PSAvoidUsingWriteHost',  # Allow Write-Host for scripts
        'PSUseShouldProcessForStateChangingFunctions'  # Not applicable for simple scripts
    )
    
    # Rules to include (if you want to be explicit)
    IncludeRules = @(
        'PSAvoidUsingCmdletAliases',
        'PSAvoidUsingPlainTextForPassword',
        'PSUseDeclaredVarsMoreThanAssignments'
    )
    
    # Custom rule settings
    Rules = @{
        PSAvoidUsingCmdletAliases = @{
            'allowlist' = @('cd', 'dir', 'type')  # Allow these specific aliases
        }
        
        PSPlaceOpenBrace = @{
            Enable = $true
            OnSameLine = $true
            NewLineAfter = $true
            IgnoreOneLineBlock = $true
        }
        
        PSUseConsistentIndentation = @{
            Enable = $true
            IndentationSize = 4
            PipelineIndentation = 'IncreaseIndentationForFirstPipeline'
            Kind = 'space'
        }
    }
}
```

### Environment Variables

Control PSScriptAnalyzer behavior with environment variables:

```bash
# Set custom settings file location
export PSSCRIPTANALYZER_SETTINGS="/path/to/custom-settings.psd1"

# Disable automatic PSScriptAnalyzer module installation
export PY_PSSCRIPTANALYZER_NO_INSTALL="1"

# Set custom PowerShell executable
export PY_PSSCRIPTANALYZER_POWERSHELL="/usr/local/bin/pwsh"
```

## CI/CD Configuration

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
        run: sudo snap install powershell --classic
        
      - name: Install py-psscriptanalyzer
        run: pip install py-psscriptanalyzer
        
      - name: Analyze PowerShell files
        run: py-psscriptanalyzer --severity Warning **/*.ps1
        
      - name: Check formatting
        run: py-psscriptanalyzer --format --dry-run **/*.ps1
```

### Azure DevOps

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
    
- script: sudo snap install powershell --classic
  displayName: 'Install PowerShell'
  
- script: pip install py-psscriptanalyzer
  displayName: 'Install py-psscriptanalyzer'
  
- script: py-psscriptanalyzer --severity Warning **/*.ps1
  displayName: 'Analyze PowerShell files'
```

## Best Practices

### Repository Setup

1. **Create settings file**: Add `.psscriptanalyzer-settings.psd1` to your repository
2. **Configure pre-commit**: Use appropriate severity levels for your project
3. **Document exceptions**: Comment why specific rules are disabled
4. **Regular updates**: Keep py-psscriptanalyzer version up to date

### Team Workflow

1. **Standardize settings**: Use the same PSScriptAnalyzer configuration across the team
2. **Gradual adoption**: Start with errors only, then add warnings
3. **Training**: Educate team on PowerShell best practices
4. **Review regularly**: Update rules and settings based on team feedback

### Performance Optimization

1. **File patterns**: Use specific file patterns to avoid analyzing unnecessary files
2. **Exclude patterns**: Exclude generated code, vendor code, and test fixtures
3. **Severity levels**: Use appropriate severity levels to balance quality and speed
4. **Parallel execution**: Pre-commit runs hooks in parallel automatically
