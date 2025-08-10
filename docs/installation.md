# Installation

## Prerequisites

Before installing py-psscriptanalyzer, ensure you have the following prerequisites:

### Python

py-psscriptanalyzer requires Python 3.9 or later.

```bash
python --version  # Should be 3.9 or higher
```

### PowerShell

The package requires PowerShell Core (pwsh) to be installed and available in your system PATH.

#### Windows

##### Option 1: Microsoft Store (Recommended)

```bash
# Install from Microsoft Store using winget
winget install --id Microsoft.PowerShell --source winget
```

##### Option 2: Direct Download (Windows)

Download from the [PowerShell GitHub releases page](https://github.com/PowerShell/PowerShell/releases).

#### macOS

##### Option 1: Homebrew (Recommended)

```bash
brew install --cask powershell
```

##### Option 2: Direct Download (macOS)

Download from the [PowerShell GitHub releases page](https://github.com/PowerShell/PowerShell/releases).

#### Linux

##### Ubuntu/Debian

```bash
# Update package index
sudo apt update

# Install dependencies
sudo apt install -y wget apt-transport-https software-properties-common

# Download Microsoft signing key and repository
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
sudo dpkg -i packages-microsoft-prod.deb

# Update package index after adding Microsoft repository
sudo apt update

# Install PowerShell
sudo apt install -y powershell
```

##### CentOS/RHEL/Fedora

```bash
# Register Microsoft signature key
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

# Register Microsoft repository
curl https://packages.microsoft.com/config/rhel/8/prod.repo | sudo tee /etc/yum.repos.d/microsoft.repo

# Install PowerShell
sudo dnf install -y powershell
```

### Verify PowerShell Installation

After installation, verify PowerShell is working:

```bash
pwsh --version
```

You should see output similar to:

```text
PowerShell 7.5.2
```

## Installing py-psscriptanalyzer

### Method 1: PyPI (Recommended)

Install directly from PyPI using pip:

```bash
pip install py-psscriptanalyzer
```

### Method 2: From Source

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/thetestlabs/py-psscriptanalyzer.git
```

### Verify Installation

After installation, verify the CLI is working:

```bash
py-psscriptanalyzer --help
```

## Using as Pre-commit Hook

### Method 1: Add to Existing .pre-commit-config.yaml

If you already have a `.pre-commit-config.yaml` file in your repository, add the py-psscriptanalyzer hooks:

```yaml
repos:
  # ... your existing hooks ...

  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0  # Use the latest version
    hooks:
      # Lint PowerShell files
      - id: py-psscriptanalyzer
        args: ["--severity", "Warning"]

      # Format PowerShell files
      - id: py-psscriptanalyzer-format
```

### Method 2: Create New .pre-commit-config.yaml

Create a new `.pre-commit-config.yaml` file in your repository root:

```yaml
repos:
  - repo: https://github.com/thetestlabs/py-psscriptanalyzer
    rev: v1.0.0  # Use the latest version
    hooks:
      - id: py-psscriptanalyzer
      - id: py-psscriptanalyzer-format
```

### Install and Run Pre-commit

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Run against all files (optional)
pre-commit run --all-files
```

## Development Installation

For development or contributing to py-psscriptanalyzer:

```bash
# Clone the repository
git clone https://github.com/thetestlabs/py-psscriptanalyzer.git
cd py-psscriptanalyzer

# Install uv (if not already installed)
pip install uv

# Install dependencies
uv sync --group dev

# Install in editable mode
uv pip install -e .
```

## Troubleshooting

### PowerShell Not Found

If you get an error that PowerShell is not found:

1. Ensure PowerShell is installed (see prerequisites above)
2. Verify PowerShell is in your PATH:
   ```bash
   which pwsh  # On Unix-like systems
   where pwsh  # On Windows
   ```
3. Try running PowerShell directly:
   ```bash
   pwsh -Command "Write-Output 'Hello World'"
   ```

### PSScriptAnalyzer Module Missing

The first time you run py-psscriptanalyzer, it will automatically attempt to install the PSScriptAnalyzer PowerShell module. If this fails:

1. Install manually:
   ```bash
   pwsh -Command "Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser"
   ```

2. Verify installation:
   ```bash
   pwsh -Command "Get-Module -ListAvailable PSScriptAnalyzer"
   ```

### Permission Issues

On Unix-like systems, you might need to update the PowerShell execution policy:

```bash
pwsh -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
```
