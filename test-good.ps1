#!/usr/bin/env pwsh
# This is a clean PowerShell script for testing
# It should not trigger any PSScriptAnalyzer warnings

function Get-SystemInformation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ComputerName
    )

    Write-Output "Getting system information for $ComputerName"
    # Simple function that doesn't use problematic cmdlets
    return "System info for $ComputerName"
}

# Example usage - but don't actually call it to avoid issues
# Get-SystemInformation -ComputerName "localhost"
