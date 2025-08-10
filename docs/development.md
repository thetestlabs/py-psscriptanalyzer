# Development

## Setting Up Development Environment

### Prerequisites

- Python 3.9+
- PowerShell Core 7.0+
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/thetestlabs/py-psscriptanalyzer.git
cd py-psscriptanalyzer

# Install uv if not already installed
pip install uv

# Install dependencies
uv sync --group dev --group docs

# Install the package in editable mode
uv pip install -e .

# Install pre-commit hooks
uv run pre-commit install
```

### Verify Installation

```bash
# Test the CLI
py-psscriptanalyzer --help

# Run tests
uv run pytest

# Check code quality
uv run ruff check .
uv run mypy src/py_psscriptanalyzer/
```

## Project Structure

```
py-psscriptanalyzer/
├── src/
│   └── py_psscriptanalyzer/
│       ├── __init__.py          # Main exports
│       ├── __main__.py          # CLI entry point
│       ├── constants.py         # Configuration constants
│       ├── core.py              # Core functionality
│       ├── powershell.py        # PowerShell integration
│       └── scripts.py           # PowerShell script generation
├── tests/
│   ├── __init__.py
│   └── test_simple.py           # Test suite
├── docs/                        # Documentation
├── examples/                    # Example PowerShell files
├── .github/workflows/           # CI/CD pipelines
├── pyproject.toml              # Package configuration
└── README.md
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow these guidelines:

- **Code Style**: Use Ruff for formatting and linting
- **Type Hints**: Add type hints to all functions
- **Documentation**: Update docstrings and docs
- **Tests**: Add tests for new functionality

### 3. Test Your Changes

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/py_psscriptanalyzer --cov-report=html

# Test specific functionality
uv run pytest tests/test_simple.py::TestFindPowershell

# Run linting
uv run ruff check .
uv run ruff format .
uv run mypy src/py_psscriptanalyzer/

# Test pre-commit hooks
uv run pre-commit run --all-files
```

### 4. Test CLI Integration

```bash
# Test CLI directly
py-psscriptanalyzer test-good.ps1
py-psscriptanalyzer --format test-good.ps1

# Test pre-commit integration
echo "Write-Host 'test'" > test.ps1
git add test.ps1
git commit -m "Test commit"  # Should trigger hooks
```

### 5. Update Documentation

If you've added new features or changed behavior:

```bash
# Build documentation locally
cd docs
uv run sphinx-build -b html . _build/html

# Or use make
make html

# View documentation
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
```

### 6. Submit Pull Request

```bash
git push origin feature/your-feature-name
# Then create PR on GitHub
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_simple.py

# Run specific test method
uv run pytest tests/test_simple.py::TestFindPowershell::test_find_powershell_success_first_executable

# Run with coverage
uv run pytest --cov=src/py_psscriptanalyzer --cov-report=html
```

### Writing Tests

Tests are located in the `tests/` directory. Follow these patterns:

#### Unit Test Example

```python
"""Test for new functionality."""

import pytest
from unittest.mock import Mock, patch

from py_psscriptanalyzer.core import your_new_function


class TestYourNewFunction:
    """Test your_new_function."""

    def test_success_case(self) -> None:
        """Test successful execution."""
        result = your_new_function("input")
        assert result == "expected_output"

    def test_error_case(self) -> None:
        """Test error handling."""
        with pytest.raises(ValueError):
            your_new_function("invalid_input")

    @patch("py_psscriptanalyzer.powershell.subprocess.run")
    def test_with_mock(self, mock_run: Mock) -> None:
        """Test with mocked subprocess."""
        mock_run.return_value.returncode = 0
        result = your_new_function("input")
        assert result is not None
```

### Integration Tests

Integration tests should test the full workflow:

```python
def test_full_analysis_workflow(tmp_path):
    """Test complete analysis workflow."""
    # Create test PowerShell file
    ps_file = tmp_path / "test.ps1"
    ps_file.write_text("Write-Host 'Hello World'")
    
    # Run analysis
    result = run_script_analyzer([str(ps_file)])
    
    # Verify results
    assert result != 0  # Should find Write-Host issue
```

## Code Style and Quality

### Code Formatting

We use Ruff for code formatting and linting:

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check . --fix
```

### Type Checking

We use MyPy for static type checking:

```bash
# Run type checking
uv run mypy src/py_psscriptanalyzer/

# Check specific file
uv run mypy src/py_psscriptanalyzer/core.py
```

### Pre-commit Hooks

Pre-commit hooks run automatically on commit:

```bash
# Install hooks (one-time setup)
uv run pre-commit install

# Run manually on all files
uv run pre-commit run --all-files

# Skip hooks for a commit (discouraged)
git commit --no-verify -m "Emergency fix"
```

## Documentation

### Building Documentation

```bash
cd docs

# Install docs dependencies
uv sync --group docs

# Build HTML documentation
uv run sphinx-build -b html . _build/html

# Or use make
make html

# Build and watch for changes (if available)
make livehtml
```

### Writing Documentation

- Use **Markdown** for most documentation (processed by MyST)
- Use **reStructuredText** only when advanced Sphinx features are needed
- Include **code examples** for all features
- Add **docstrings** to all public functions

#### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Short description of the function.

    Longer description with more details about what the function does,
    how it works, and any important notes.

    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter. Defaults to 0.

    Returns:
        Description of what the function returns.

    Raises:
        ValueError: Description of when this exception is raised.
        
    Example:
        Basic usage example:
        
        >>> result = example_function("hello", 42)
        >>> print(result)
        True
    """
    return True
```

## Release Process

### Version Management

Versions are managed in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

### Creating a Release

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with new features and fixes
3. **Update documentation** if needed
4. **Create and push tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
5. **GitHub Actions** will automatically build and publish to PyPI

### Publishing to PyPI

Publishing is automated via GitHub Actions when a version tag is pushed. Manual publishing:

```bash
# Build package
uv build

# Check package
uv run twine check dist/*

# Upload to test PyPI (optional)
uv run twine upload --repository testpypi dist/*

# Upload to PyPI
uv run twine upload dist/*
```

## Contributing Guidelines

### Pull Request Process

1. **Fork** the repository
2. **Create feature branch** from main
3. **Make changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Ensure all checks pass** (tests, linting, type checking)
7. **Submit pull request** with clear description

### Commit Messages

Use conventional commit format:

```
feat: add new feature
fix: resolve bug in parser
docs: update installation guide
test: add integration tests
refactor: improve error handling
chore: update dependencies
```

### Code Review

All changes require code review:

- **Functionality**: Does it work as expected?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it well documented?
- **Style**: Does it follow our coding standards?
- **Performance**: Any performance implications?

## Debugging

### Common Development Issues

#### PowerShell Not Found

```bash
# Check PowerShell installation
which pwsh
pwsh --version

# Set custom PowerShell path
export PY_PSSCRIPTANALYZER_POWERSHELL="/usr/local/bin/pwsh"
```

#### PSScriptAnalyzer Module Issues

```bash
# Check module availability
pwsh -Command "Get-Module -ListAvailable PSScriptAnalyzer"

# Install manually
pwsh -Command "Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser"
```

#### Test Failures

```bash
# Run tests with more verbose output
uv run pytest -v -s

# Run specific failing test
uv run pytest tests/test_simple.py::TestFindPowershell::test_find_powershell_not_found -v

# Run with debugger
uv run pytest --pdb tests/test_simple.py
```

### Logging and Debugging

Enable debug logging in your code:

```python
import logging

# Set up debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def your_function():
    logger.debug("Starting function execution")
    # Your code here
    logger.debug("Function completed successfully")
```
