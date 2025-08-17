# Installation

## Prerequisites

Before installing py-psscriptanalyzer, ensure you have the following:

### Python

py-psscriptanalyzer requires Python 3.9 or later:

```bash
python --version  # Should be 3.9 or higher
```

### PowerShell

PowerShell Core (pwsh) must be installed and available in your system PATH.

#### Windows

##### Option 1: Microsoft Store (Recommended)

```bash
# Install from Microsoft Store using winget
winget install --id Microsoft.PowerShell --source winget
```

##### Option 2: Direct Download

Download from the [PowerShell GitHub releases page](https://github.com/PowerShell/PowerShell/releases).

#### macOS

```bash
# Using Homebrew (recommended)
brew install powershell

# Or using MacPorts
sudo port install powershell
```

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

```bash
pwsh --version
```

## Install py-psscriptanalyzer

### From PyPI (Recommended)

```bash
pip install py-psscriptanalyzer
```

### From Source

```bash
# Clone the repository
git clone https://github.com/thetestlabs/py-psscriptanalyzer.git
cd py-psscriptanalyzer

# Install using pip
pip install .
```

### Verify Installation

```bash
py-psscriptanalyzer --version
py-psscriptanalyzer --help
```

## Development Installation

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/thetestlabs/py-psscriptanalyzer.git
cd py-psscriptanalyzer

# Install uv (modern Python package manager)
pip install uv

# Install dependencies and development tools
uv sync --group dev --group docs

# Install in editable mode
uv pip install -e .

# Install pre-commit hooks
uv run pre-commit install
```

## Troubleshooting

### PowerShell Not Found

If you encounter "PowerShell not found" errors:

1. **Verify PowerShell is installed:**
   ```bash
   which pwsh  # On Unix-like systems
   where pwsh  # On Windows
   ```

2. **Test PowerShell directly:**
   ```bash
   pwsh -Command "Write-Output 'Hello World'"
   ```

3. **Check your PATH:** Ensure the PowerShell installation directory is in your system PATH.

### PSScriptAnalyzer Module Missing

py-psscriptanalyzer automatically installs the PSScriptAnalyzer PowerShell module on first use. If installation fails:

1. **Install manually:**
   ```bash
   pwsh -Command "Install-Module -Name PSScriptAnalyzer -Force -Scope CurrentUser"
   ```

2. **Verify installation:**
   ```bash
   pwsh -Command "Get-Module -ListAvailable PSScriptAnalyzer"
   ```

### Permission Issues

On Unix-like systems, you may need to adjust the PowerShell execution policy:

```bash
pwsh -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
```

### Python Version Issues

Ensure you're using Python 3.9 or later:

```bash
python --version
pip --version
```

If you have multiple Python versions, you may need to use `python3` and `pip3` instead.

## Next Steps

After installation:

- See [Usage](usage.md) for command-line usage examples
- See [Configuration](configuration.md) for pre-commit hook setup and advanced configuration
- See [Development](development.md) for contributing guidelines
