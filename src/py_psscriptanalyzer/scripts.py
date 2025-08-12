"""PowerShell script generation utilities."""

from typing import Optional


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


def generate_analysis_script(
    files_param: str,
    severity: str = "Warning",
    security_only: bool = False,
    style_only: bool = False,
    performance_only: bool = False,
    best_practices_only: bool = False,
    dsc_only: bool = False,
    compatibility_only: bool = False,
    include_rules: Optional[list[str]] = None,
    exclude_rules: Optional[list[str]] = None,
    json_output: bool = False,
) -> str:
    """Generate PowerShell script to analyze PowerShell files."""
    from .constants import (
        BEST_PRACTICES_RULES,
        COMPATIBILITY_RULES,
        DSC_RULES,
        PERFORMANCE_RULES,
        SECURITY_RULES,
        STYLE_RULES,
    )

    # Handle different severity levels
    if severity == "All" or severity == "Information":
        # Show all issues including Information severity
        severity_param = ""
        filter_logic = ""
    elif severity == "Warning":
        # Show only Warning and Error severity issues (default)
        severity_param = ""
        filter_logic = """
                # Filter to show only Warning and Error severity issues
                $result = $result | Where-Object { $_.Severity -eq "Warning" -or $_.Severity -eq "Error" }"""
    elif severity == "Error":
        # Show only Error issues
        severity_param = "-Severity Error"
        filter_logic = ""
    else:
        # Fallback to Warning behavior
        severity_param = ""
        filter_logic = """
                # Filter to show only Warning and Error severity issues
                $result = $result | Where-Object { $_.Severity -eq "Warning" -or $_.Severity -eq "Error" }"""

    # Add rule category filtering if requested
    rule_category_filter = ""

    # Security rules filter
    if security_only:
        security_rules_list = ", ".join(f"'{rule}'" for rule in SECURITY_RULES)
        rule_category_filter = f"""
                # Filter to include only security-related rules
                $categoryRules = @({security_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "IsSecurityRule" -Value $true -Force
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "Security" -Force
                }}
        """

    # Style rules filter
    elif style_only:
        style_rules_list = ", ".join(f"'{rule}'" for rule in STYLE_RULES)
        rule_category_filter = f"""
                # Filter to include only style-related rules
                $categoryRules = @({style_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "Style" -Force
                }}
        """

    # Performance rules filter
    elif performance_only:
        performance_rules_list = ", ".join(f"'{rule}'" for rule in PERFORMANCE_RULES)
        rule_category_filter = f"""
                # Filter to include only performance-related rules
                $categoryRules = @({performance_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "Performance" -Force
                }}
        """

    # Best practices rules filter
    elif best_practices_only:
        best_practices_rules_list = ", ".join(f"'{rule}'" for rule in BEST_PRACTICES_RULES)
        rule_category_filter = f"""
                # Filter to include only best practices rules
                $categoryRules = @({best_practices_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "BestPractices" -Force
                }}
        """

    # DSC rules filter
    elif dsc_only:
        dsc_rules_list = ", ".join(f"'{rule}'" for rule in DSC_RULES)
        rule_category_filter = f"""
                # Filter to include only DSC-related rules
                $categoryRules = @({dsc_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "DSC" -Force
                }}
        """

    # Compatibility rules filter
    elif compatibility_only:
        compatibility_rules_list = ", ".join(f"'{rule}'" for rule in COMPATIBILITY_RULES)
        rule_category_filter = f"""
                # Filter to include only compatibility-related rules
                $categoryRules = @({compatibility_rules_list})
                $result = $result | Where-Object {{ $categoryRules -contains $_.RuleName }}
                # Add category property to results for SARIF conversion
                $result | ForEach-Object {{
                    $_ | Add-Member -MemberType NoteProperty -Name "RuleCategory" -Value "Compatibility" -Force
                }}
        """

    # Include/exclude specific rules if specified
    include_exclude_filter = ""
    if include_rules:
        include_rules_list = ", ".join(f"'{rule}'" for rule in include_rules)
        include_exclude_filter = f"""
                # Filter to include only specific rules
                $includeRules = @({include_rules_list})
                $result = $result | Where-Object {{ $includeRules -contains $_.RuleName }}
        """

    if exclude_rules:
        exclude_rules_list = ", ".join(f"'{rule}'" for rule in exclude_rules)
        include_exclude_filter = f"""
                # Filter to exclude specific rules
                $excludeRules = @({exclude_rules_list})
                $result = $result | Where-Object {{ $excludeRules -notcontains $_.RuleName }}
        """

    # Combine all filters
    if rule_category_filter:
        filter_logic += rule_category_filter

    if include_exclude_filter:
        filter_logic += include_exclude_filter

    # Choose output format
    if json_output:
        output_code = """
            # Convert to JSON format
            if ($issues.Count -gt 0) {
                $issues | ConvertTo-Json -Depth 4
                exit 1
            } else {
                Write-Host ""
                exit 0
            }"""
    else:
        issue_reporting = _generate_issue_reporting_logic()
        output_code = f"""
            if ($issues.Count -gt 0) {{
                Write-Host ""

                # Check if running in GitHub Actions
                $isGitHubActions = $env:GITHUB_ACTIONS -eq "true"
{issue_reporting}
                exit 1
            }} else {{
                Write-Host "No issues found" -ForegroundColor Green
                exit 0
            }}"""

    error_handling = _generate_error_handling()

    return f"""
        try {{
            $files = @({files_param})
            $issues = @()
            foreach ($file in $files) {{
                $result = Invoke-ScriptAnalyzer -Path $file {severity_param}{filter_logic}
                if ($result) {{
                    $issues += $result
                }}
            }}
{output_code}
        }} {error_handling}
        """
