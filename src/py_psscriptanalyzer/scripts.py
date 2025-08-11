"""PowerShell script generation utilities."""


def escape_powershell_path(path: str) -> str:
    """Escape a file path for use in PowerShell."""
    return path.replace("'", "''")


def build_powershell_file_array(files: list[str]) -> str:
    """Build a PowerShell array string from a list of files."""
    escaped_files = [f"'{escape_powershell_path(f)}'" for f in files]
    return ",".join(escaped_files)


def generate_format_script(files_param: str) -> str:
    """Generate PowerShell script for formatting files."""
    return f"""
        $files = @({files_param})
        $exitCode = 0
        foreach ($file in $files) {{
            try {{
                $originalContent = Get-Content -Path $file -Raw
                $formatted = Invoke-Formatter -ScriptDefinition $originalContent
                if ($formatted -ne $originalContent) {{
                    Set-Content -Path $file -Value $formatted -NoNewline
                    Write-Host "Formatted: $file"
                }}
            }} catch {{
                Write-Error "Failed to format $file`: $($_.Exception.Message)"
                $exitCode = 1
            }}
        }}
        exit $exitCode
        """


def _generate_github_actions_output() -> str:
    """Generate PowerShell code for GitHub Actions issue reporting."""
    return """
                        # Use GitHub Actions annotations
                        $annotationType = switch ($issue.Severity) {
                            "Error" { "error" }
                            "Warning" { "warning" }
                            "Information" { "notice" }
                            default { "error" }
                        }

                        # Map severity for GitHub Actions display
                        $displaySeverity = switch ($issue.Severity) {
                            "Error" { "Error" }
                            "Warning" { "Warning" }
                            "Information" { "Notice" }
                            default { "Error" }
                        }

                        # GitHub Actions annotation format
                        $annotation = "::" + $annotationType + " file=" + $issue.ScriptName + `
                            ",line=" + $issue.Line + ",title=" + $issue.RuleName + "::" + $issue.Message
                        Write-Host $annotation

                        # Also show regular output for readability with GitHub Actions terminology
                        $header = "$($displaySeverity): $($location): $($issue.RuleName)"
                        Write-Host $header
                        Write-Host "  $($issue.Message)"
                        Write-Host ""
    """


def _generate_terminal_output() -> str:
    """Generate PowerShell code for terminal issue reporting."""
    return """
                        # Set color based on severity for local terminal
                        $severityColor = switch ($issue.Severity) {
                            "Error" { "Red" }
                            "Warning" { "DarkYellow" }
                            "Information" { "Cyan" }
                            default { "Red" }
                        }

                        $header = "$($issue.Severity): $($location): $($issue.RuleName)"
                        Write-Host $header -ForegroundColor $severityColor
                        Write-Host "  $($issue.Message)" -ForegroundColor Gray
                        Write-Host ""
    """


def _generate_issue_reporting_logic() -> str:
    """Generate PowerShell code for issue reporting logic."""
    github_output = _generate_github_actions_output()
    terminal_output = _generate_terminal_output()

    return f"""
                foreach ($issue in $issues) {{
                    $fileName = Split-Path -Leaf $issue.ScriptName
                    $location = "$($fileName): Line $($issue.Line):1"

                    if ($isGitHubActions) {{{github_output}
                    }} else {{{terminal_output}
                    }}
                }}
                Write-Host "Found $($issues.Count) issue(s)" -ForegroundColor Yellow
    """


def _generate_error_handling() -> str:
    """Generate PowerShell code for error handling."""
    return """
        catch [System.IO.FileLoadException] {
            Write-Error "Assembly loading error: $($_.Exception.Message)"
            Write-Error "This may be due to .NET runtime compatibility issues."
            Write-Error "Try updating PowerShell or reinstalling PSScriptAnalyzer."
            exit 250
        } catch {
            Write-Error "Unexpected error: $($_.Exception.Message)"
            exit 250
        }
    """


def generate_analysis_script(files_param: str, severity: str) -> str:
    """
    Generate PowerShell script for analyzing files.

    Conditionally adds the Severity parameter: if "All" is selected, the parameter is omitted to get all severities.
    """
    severity_param = f"-Severity {severity}" if severity != "All" else ""
    issue_reporting = _generate_issue_reporting_logic()
    error_handling = _generate_error_handling()

    return f"""
        try {{
            $files = @({files_param})
            $issues = @()
            foreach ($file in $files) {{
                $result = Invoke-ScriptAnalyzer -Path $file {severity_param}
                if ($result) {{
                    $issues += $result
                }}
            }}
            if ($issues.Count -gt 0) {{
                Write-Host ""

                # Check if running in GitHub Actions
                $isGitHubActions = $env:GITHUB_ACTIONS -eq "true"
{issue_reporting}
                exit 1
            }} else {{
                Write-Host "No issues found" -ForegroundColor Green
                exit 0
            }}
        }} {error_handling}
        """
