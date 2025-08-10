# Examples

## Test Files Overview

The `examples/` directory contains PowerShell files with intentional errors that demonstrate various PSScriptAnalyzer rules and violations. These examples serve multiple purposes:

- **Learning Tool**: Understand what PSScriptAnalyzer detects
- **Testing**: Verify the pre-commit hooks work correctly
- **Reference**: See examples of common PowerShell issues

## File Structure

```text
examples/
├── README.md                     # This file
├── scripts/                      # Script examples with various issues
│   ├── BadScript.ps1             # Basic scripting mistakes
│   ├── MixedSeverity.ps1         # All severity levels demonstrated
│   ├── AdvancedIssues.ps1        # Complex rule violations
│   ├── ConfigurationIssues.ps1   # Configuration-related problems
│   ├── InformationIssues.ps1     # Information-level violations
│   ├── EdgeCases.ps1             # Edge case scenarios
│   └── test.ps1                  # Simple test script
├── modules/                      # Module examples
│   ├── BadModule.psm1            # Module with security/performance issues
│   └── BadModule.psd1            # Module manifest with errors
├── functions/                    # Function examples
│   └── BadFunctions.psm1         # Function-specific violations
└── classes/                      # Class examples
    └── BadClasses.ps1            # PowerShell class issues
```

## Error Categories by Severity

### Error Level Issues (Red) 🔴

Critical problems that should always be fixed:

- **PSAvoidUsingPlainTextForPassword**: Plain text passwords in code
- **PSAvoidUsingInvokeExpression**: Dangerous `Invoke-Expression` usage
- **PSAvoidUsingConvertToSecureStringWithPlainText**: Insecure string conversion

### Warning Level Issues (Orange) 🟡

Important issues that affect code quality and should be addressed::

- **PSUseApprovedVerbs**: Non-approved verbs in function names
- **PSUseSingularNouns**: Plural nouns in function names
- **PSAvoidUsingWriteHost**: Using `Write-Host` inappropriately
- **PSUseDeclaredVarsMoreThanAssignments**: Variables assigned but never used
- **PSUseShouldProcessForStateChangingFunctions**: Missing ShouldProcess support

### Information Level Issues (Cyan) 🔵

Style and best practice suggestions:

- **PSAvoidUsingDoubleQuotesForConstantString**: Unnecessary double quotes
- **PSUseCorrectCasing**: Incorrect cmdlet casing
- **PSProvideCommentHelp**: Missing comment-based help

## Example Files Breakdown

### Scripts Directory

**`BadScript.ps1`** - Demonstrates basic scripting issues:
- Variable naming problems
- Unused parameters and variables  
- Plain text password handling
- Missing ShouldProcess support

**`MixedSeverity.ps1`** - Shows all three severity levels:
- Error: Security vulnerabilities
- Warning: Code quality issues
- Information: Style suggestions

**`AdvancedIssues.ps1`** - Complex rule violations:
- Advanced security concerns
- Performance anti-patterns
- Module design issues

### Modules Directory

**`BadModule.psm1`** - Module-specific problems:
- Security vulnerabilities in authentication
- Performance issues
- Module design violations

**`BadModule.psd1`** - Manifest validation errors:
- Missing required fields
- Invalid field values
- Encoding issues

### Functions Directory

**`BadFunctions.psm1`** - Function design issues:
- Parameter validation problems
- Function naming violations
- Help documentation issues

### Classes Directory

**`BadClasses.ps1`** - PowerShell class problems:
- Class design violations
- Property and method issues
- Inheritance problems

## Running Examples

### Test All Examples

Run PSScriptAnalyzer on all example files:

```bash
# Using pre-commit (will fail as expected)
pre-commit run psscriptanalyzer --files examples/**/*.ps*

# Direct PowerShell analysis
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/ -Recurse"
```

### Test Specific Categories

Run analysis on specific file types:

```bash
# Test all scripts
pre-commit run psscriptanalyzer --files examples/scripts/*.ps1

# Test module issues
pre-commit run psscriptanalyzer --files examples/modules/BadModule.psm1

# Test manifest problems
pre-commit run psscriptanalyzer --files examples/modules/BadModule.psd1

# Test function issues
pre-commit run psscriptanalyzer --files examples/functions/BadFunctions.psm1

# Test class issues
pre-commit run psscriptanalyzer --files examples/classes/BadClasses.ps1
```

### Test with Different Severity Levels

```bash
# Only show errors (critical issues)
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/ -Recurse -Severity Error"

# Show warnings and errors (recommended)
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/ -Recurse -Severity Warning"

# Show all issues including information
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/ -Recurse -Severity Information"
```

### Running Without Pre-commit

You can also install the package from PyPI and run it directly without pre-commit:

```bash
# Install from PyPI
pip install psscriptanalyzer-pre-commit

# Run directly on files (linting)
psscriptanalyzer-hook examples/scripts/BadScript.ps1
psscriptanalyzer-hook examples/**/*.ps1

# Run with specific severity
psscriptanalyzer-hook --severity Error examples/scripts/BadScript.ps1
psscriptanalyzer-hook --severity Warning examples/modules/BadModule.psm1
psscriptanalyzer-hook --severity Information examples/**/*.ps1

# Format files directly
psscriptanalyzer-hook --format examples/scripts/BadScript.ps1
psscriptanalyzer-hook --format examples/**/*.ps1

#### Direct Usage Examples

```bash
# Analyze a single file
psscriptanalyzer-hook examples/scripts/MixedSeverity.ps1

# Analyze multiple files
psscriptanalyzer-hook examples/scripts/*.ps1 examples/modules/*.psm1

# Format and analyze with all severity levels
psscriptanalyzer-hook --format --severity All examples/scripts/BadScript.ps1

# Only check for errors (strictest)
psscriptanalyzer-hook --severity Error examples/scripts/AdvancedIssues.ps1

# Check everything including style suggestions
psscriptanalyzer-hook --severity Information examples/**/*.ps*
```

#### Integration in Build Scripts

You can integrate this into your build scripts or CI/CD without pre-commit:

```bash
# In a shell script
#!/bin/bash
echo "Checking PowerShell code quality..."

# Install if not already installed
pip install psscriptanalyzer-pre-commit

# Run analysis
if psscriptanalyzer-hook --severity Warning src/**/*.ps1; then
    echo "✅ PowerShell code quality check passed"
else
    echo "❌ PowerShell code quality issues found"
    exit 1
fi

# Format code
echo "Formatting PowerShell files..."
psscriptanalyzer-hook --format src/**/*.ps1
```

#### Python Script Integration

```python
# In a Python script
import subprocess
import sys

def check_powershell_quality(files, severity="Warning"):
    """Check PowerShell files using psscriptanalyzer-hook."""
    cmd = ["psscriptanalyzer-hook", "--severity", severity] + files
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ PowerShell quality check passed")
        return True
    else:
        print("❌ PowerShell quality issues:")
        print(result.stdout)
        return False

# Usage
files = ["examples/scripts/BadScript.ps1", "examples/modules/BadModule.psm1"]
if not check_powershell_quality(files, "Error"):
    sys.exit(1)
```

## Expected Output

When running PSScriptAnalyzer on these examples, you should see output similar to:

```text
Warning: BadScript.ps1: Line 6:1: PSUseApprovedVerbs
  The cmdlet 'Download-File' uses an unapproved verb.
Warning: BadScript.ps1: Line 35:1: PSAvoidUsingWriteHost
  File 'BadScript.ps1' uses Write-Host. Avoid using Write-Host because it might 
  not work in all hosts, does not work when there is no host, and (prior to PS 5.0) 
  cannot be suppressed, captured, or redirected. Instead, use Write-Output, Write-Verbose, 
  or Write-Information.
Error: BadModule.psm1: Line 8:1: PSAvoidUsingUserNameAndPasswordParams
  Function 'Connect-ToService' has both Username and Password parameters.
```

## Using Examples for Development

### Pre-commit Hook Testing

These examples are perfect for testing pre-commit hook functionality:

```bash
# Install hooks
pre-commit install

# Test on examples (should fail)
git add examples/
git commit -m "Test commit"  # Will be blocked by hooks

# Run formatting (may fix some issues)
pre-commit run psscriptanalyzer-format --files examples/**/*.ps1
```

### Formatting PowerShell Files

The pre-commit hook can automatically format PowerShell code using PSScriptAnalyzer's `Invoke-Formatter`:

```bash
# Format all PowerShell files in examples
pre-commit run psscriptanalyzer-format --all-files

# Format specific files
pre-commit run psscriptanalyzer-format --files examples/scripts/BadScript.ps1

# Format files with issues (like inconsistent indentation)
pre-commit run psscriptanalyzer-format --files examples/scripts/ConfigurationIssues.ps1

# See what would be formatted (dry run)
git add examples/scripts/BadScript.ps1
git commit -m "Test formatting" --dry-run
```

#### Before and After Formatting Example

**Before formatting** (inconsistent style):
```powershell
function Get-UserData{
    param($UserName,$Domain)
    
  if($UserName){
      write-host "Processing: $UserName"
        $result=Get-ADUser -Identity $UserName
    return $result}
}
```

**After formatting** (consistent style):
```powershell
function Get-UserData {
    param(
        $UserName,
        $Domain
    )
    
    if ($UserName) {
        Write-Host "Processing: $UserName"
        $result = Get-ADUser -Identity $UserName
        return $result
    }
}
```

### GitHub Actions Integration

Here's how to use these examples with GitHub Actions for both linting and formatting:

#### Complete GitHub Actions Workflow

```yaml
name: PowerShell Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  powershell-quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
    
    - name: Install PowerShell
      run: |
        # Install PowerShell on Linux
        wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
        sudo dpkg -i packages-microsoft-prod.deb
        sudo apt-get update
        sudo apt-get install -y powershell
    
    - name: Install pre-commit
      run: |
        pip install pre-commit
        pip install psscriptanalyzer-pre-commit
    
    - name: Run PSScriptAnalyzer Linting
      run: |
        # This will show errors with GitHub Actions annotations
        pre-commit run psscriptanalyzer --all-files
      continue-on-error: true  # Don't fail the build, just report
    
    - name: Run PowerShell Formatting Check
      run: |
        # Check if files need formatting
        pre-commit run psscriptanalyzer-format --all-files
        
        # Check for any changes after formatting
        if [[ -n $(git status --porcelain) ]]; then
          echo "❌ Files need formatting. Run 'pre-commit run psscriptanalyzer-format --all-files' locally."
          git diff
          exit 1
        else
          echo "✅ All PowerShell files are properly formatted."
        fi
    
    # Optional: Auto-format and commit back (for specific workflows)
    - name: Auto-format PowerShell Files
      if: github.event_name == 'pull_request'
      run: |
        pre-commit run psscriptanalyzer-format --all-files
        
        # Commit changes if any
        if [[ -n $(git status --porcelain) ]]; then
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "Auto-format PowerShell files [skip ci]"
          git push
        fi
```

#### Simplified Linting-Only Workflow

```yaml
name: PowerShell Linting

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python and PowerShell
      run: |
        pip install pre-commit psscriptanalyzer-pre-commit
        sudo apt-get update && sudo apt-get install -y powershell
    
    - name: Run PSScriptAnalyzer
      run: |
        # Test examples (should find issues)
        echo "Testing examples directory..."
        pre-commit run psscriptanalyzer --files examples/**/*.ps* || true
        
        # Test actual PowerShell files (should pass)
        echo "Testing project PowerShell files..."
        find . -name "*.ps1" -o -name "*.psm1" -o -name "*.psd1" | grep -v examples/ | xargs pre-commit run psscriptanalyzer --files
```

#### Direct Package Usage in CI

You can also use the package directly without pre-commit:

```yaml
name: PowerShell Quality (Direct)

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python and PowerShell
      run: |
        pip install psscriptanalyzer-pre-commit
        sudo apt-get update && sudo apt-get install -y powershell
    
    - name: Check PowerShell Code Quality
      run: |
        # Run directly on files
        psscriptanalyzer-hook --severity Warning src/**/*.ps1 src/**/*.psm1 || true
        
        # Format files and check for changes
        psscriptanalyzer-hook --format src/**/*.ps1
        
        # Verify no formatting changes needed
        if [[ -n $(git status --porcelain) ]]; then
          echo "Files were formatted. Please run 'psscriptanalyzer-hook --format' locally."
          git diff
          exit 1
        fi
```

#### Using with Matrix Strategy

```yaml
name: Cross-Platform PowerShell Testing

on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        severity: [Error, Warning, Information]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.13'
    
    - name: Install PowerShell (Linux)
      if: runner.os == 'Linux'
      run: |
        sudo apt-get update
        sudo apt-get install -y powershell
    
    - name: Install PowerShell (macOS)
      if: runner.os == 'macOS'
      run: brew install powershell
    
    - name: Install pre-commit tools
      run: |
        pip install pre-commit psscriptanalyzer-pre-commit
    
    - name: Test Examples with Severity ${{ matrix.severity }}
      run: |
        # Run with specific severity level
        pre-commit run psscriptanalyzer --files examples/**/*.ps* -- --severity ${{ matrix.severity }}
      continue-on-error: true
```

### Expected GitHub Actions Output

When running in GitHub Actions, you'll see annotations like:

**Error Annotations (Red):**
```text
::error file=examples/scripts/BadScript.ps1,line=15,title=PSAvoidUsingPlainTextForPassword::Parameter 'password' should use SecureString
```

**Warning Annotations (Orange):**
```text
::warning file=examples/scripts/BadScript.ps1,line=6,title=PSUseApprovedVerbs::The cmdlet 'Download-File' uses the verb 'Download' which is not approved
```

**Information Annotations (Blue):**
```text
::notice file=examples/scripts/BadScript.ps1,line=23,title=PSProvideCommentHelp::The function 'Download-File' does not have a help comment
```

### GitHub Actions Integration

The examples work great with GitHub Actions annotations. When run in CI/CD, you'll see:

- **Error annotations** appear as red error markers
- **Warning annotations** appear as orange warning markers  
- **Information annotations** appear as blue notice markers

See the detailed GitHub Actions examples above for complete workflow configurations.

### Learning PowerShell Best Practices

Each file demonstrates what NOT to do:

1. **Read the comments**: Each violation is documented in the code
2. **Run analysis**: See what PSScriptAnalyzer reports
3. **Fix the issues**: Practice correcting common problems
4. **Compare results**: See how the analysis output changes

## Severity Level Testing

Use the `MixedSeverity.ps1` file to test different severity configurations:

```bash
# Test Error only (should show 2-3 issues)
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/scripts/MixedSeverity.ps1 -Severity Error"

# Test Warning and above (should show 5-7 issues)
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/scripts/MixedSeverity.ps1 -Severity Warning"

# Test All levels (should show 10+ issues)
pwsh -Command "Invoke-ScriptAnalyzer -Path ./examples/scripts/MixedSeverity.ps1 -Severity Information"
```

## Contributing New Examples

To add new example violations:

1. **Identify the rule**: Find a PSScriptAnalyzer rule not covered
2. **Choose the right directory**: Scripts, modules, functions, or classes
3. **Create minimal reproduction**: Write the smallest code that triggers the rule
4. **Add comments**: Explain what the violation demonstrates
5. **Test thoroughly**: Ensure PSScriptAnalyzer detects the issue
6. **Update this README**: Document the new example

### Example Template

```powershell
# Example: Rule Name (PSRuleName)
# This demonstrates [what the violation is]
# PSScriptAnalyzer should report: [expected message]

# Violating code here
function Bad-Example {
    # This violates PSRuleName because...
    Write-Host "This is problematic"
}

# Correct version (commented)
# function Good-Example {
#     Write-Output "This is better"
# }
```

## Integration with Documentation

These examples are referenced throughout the project documentation:

- **Installation Guide**: Used to verify hook installation works
- **Usage Examples**: Demonstrate different hook behaviors
- **Configuration Guide**: Show how settings affect output
- **Troubleshooting**: Help diagnose hook issues

## Summary

The examples directory provides a comprehensive test suite organized by PowerShell construct type (scripts, modules, functions, classes). Each file contains intentionally flawed code that demonstrates specific PSScriptAnalyzer rules across all severity levels. They serve as both a learning resource for PowerShell best practices and a validation tool for the pre-commit hook implementation.
