# API Reference

## py-psscriptanalyzer Module

The `py_psscriptanalyzer` package provides the core functionality for PowerShell static analysis and formatting.

### Main Module Functions

#### `main(argv=None)`

Main entry point for the py-psscriptanalyzer CLI tool.

**Parameters:**

- `argv` (list, optional): Command line arguments. If None, uses `sys.argv[1:]`

**Returns:**

- `int`: Exit code (0 for success, non-zero for failure)

**Example:**

```python
from py_psscriptanalyzer import main

# Analyze a file programmatically
result = main(['script.ps1'])
```

#### `run_script_analyzer(files, format_mode=False, severity='All')`

Run PSScriptAnalyzer on the specified PowerShell files.

**Parameters:**

- `files` (list[str]): List of PowerShell file paths to analyze
- `format_mode` (bool, optional): If True, format files instead of analyzing. Defaults to False
- `severity` (str, optional): Severity level to filter results. Options: 'Error', 'Warning', 'Information', 'All'. Defaults to 'All'

**Returns:**

- `int`: Exit code (0 for success, non-zero for issues found or errors)

**Example:**

```python
from py_psscriptanalyzer import run_script_analyzer

# Analyze files
result = run_script_analyzer(['script1.ps1', 'script2.ps1'], severity='Warning')

# Format files
result = run_script_analyzer(['script.ps1'], format_mode=True)
```

## Core Module (`py_psscriptanalyzer.core`)

### Functions

#### `parse_arguments(args)`

Parse command line arguments for the CLI tool.

**Parameters:**

- `args` (list[str]): Command line arguments

**Returns:**

- `argparse.Namespace`: Parsed arguments

#### `filter_powershell_files(files)`

Filter input files to only include PowerShell files.

**Parameters:**

- `files` (list[str]): List of file paths

**Returns:**

- `list[str]`: List of PowerShell file paths only

## PowerShell Module (`py_psscriptanalyzer.powershell`)

### Functions

#### `find_powershell()`

Find an available PowerShell executable on the system.

**Returns:**

- `str | None`: Path to PowerShell executable, or None if not found

**Example:**

```python
from py_psscriptanalyzer.powershell import find_powershell

pwsh_path = find_powershell()
if pwsh_path:
    print(f"Found PowerShell at: {pwsh_path}")
else:
    print("PowerShell not found")
```

#### `check_psscriptanalyzer_installed(powershell_exe)`

Check if the PSScriptAnalyzer module is installed.

**Parameters:**

- `powershell_exe` (str): Path to PowerShell executable

**Returns:**

- `bool`: True if PSScriptAnalyzer is installed, False otherwise

#### `install_psscriptanalyzer(powershell_exe)`

Install the PSScriptAnalyzer PowerShell module.

**Parameters:**

- `powershell_exe` (str): Path to PowerShell executable

**Returns:**

- `bool`: True if installation succeeded, False otherwise

## Scripts Module (`py_psscriptanalyzer.scripts`)

### Functions

#### `build_powershell_file_array(files)`

Build a PowerShell array string for the given files.

**Parameters:**

- `files` (list[str]): List of file paths

**Returns:**

- `str`: PowerShell array string

#### `escape_powershell_path(path)`

Escape a file path for use in PowerShell commands.

**Parameters:**

- `path` (str): File path to escape

**Returns:**

- `str`: Escaped file path

#### `generate_analysis_script(files, severity)`

Generate a PowerShell script for analyzing files.

**Parameters:**

- `files` (list[str]): List of PowerShell file paths
- `severity` (str): Severity level to filter results

**Returns:**

- `str`: PowerShell script content

#### `generate_format_script(files)`

Generate a PowerShell script for formatting files.

**Parameters:**

- `files` (list[str]): List of PowerShell file paths

**Returns:**

- `str`: PowerShell script content

## Constants Module (`py_psscriptanalyzer.constants`)

### Constants

#### `POWERSHELL_EXECUTABLES`

List of PowerShell executable names to search for:

```python
POWERSHELL_EXECUTABLES = ["pwsh", "powershell"]
```

#### `POWERSHELL_FILE_EXTENSIONS`

Set of PowerShell file extensions:

```python
POWERSHELL_FILE_EXTENSIONS = {".ps1", ".psm1", ".psd1"}
```

#### `SEVERITY_LEVELS`

Valid PSScriptAnalyzer severity levels:

```python
SEVERITY_LEVELS = ["Error", "Warning", "Information", "All"]
```

#### `ANALYSIS_TIMEOUT`

Timeout for PowerShell analysis operations (in seconds):

```python
ANALYSIS_TIMEOUT = 300  # 5 minutes
```

## Error Handling

The package provides comprehensive error handling for common scenarios:

### PowerShell Not Found

```python
from py_psscriptanalyzer.powershell import find_powershell

if not find_powershell():
    print("❌ PowerShell not found. Please install PowerShell Core.")
```

### PSScriptAnalyzer Module Missing

```python
from py_psscriptanalyzer.powershell import check_psscriptanalyzer_installed, install_psscriptanalyzer

pwsh = find_powershell()
if not check_psscriptanalyzer_installed(pwsh):
    if install_psscriptanalyzer(pwsh):
        print("✅ PSScriptAnalyzer installed successfully")
    else:
        print("❌ Failed to install PSScriptAnalyzer")
```

## Type Hints

The package is fully type-annotated for better IDE support and development experience. All public functions include proper type hints for parameters and return values.

## Compatibility

- **Python:** 3.9+
- **PowerShell:** Core 7.0+ or Windows PowerShell 5.1+
- **Operating Systems:** Windows, macOS, Linux
