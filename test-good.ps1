#!/usr/bin/env pwsh

<#
.SYNOPSIS
    This is a clean PowerShell script for testing PSScriptAnalyzer.

.DESCRIPTION
    A well-formatted PowerShell script that follows best practices and should
    not trigger any PSScriptAnalyzer warnings or errors.

.EXAMPLE
    PS> Get-SystemInformation -ComputerName "localhost"
    Returns system information for the specified computer.
#>

function Get-SystemInformation {
    <#
    .SYNOPSIS
        Gets basic system information for a computer.

    .DESCRIPTION
        Retrieves and returns system information for the specified computer name.
        This function demonstrates proper PowerShell coding practices.

    .PARAMETER ComputerName
        The name of the computer to get information for.

    .EXAMPLE
        PS> Get-SystemInformation -ComputerName "localhost"
        Returns: "System info for localhost"

    .OUTPUTS
        System.String
    #>
    [CmdletBinding()]
    [OutputType([System.String])]
    param(
        [Parameter(Mandatory = $true, HelpMessage = "Enter the computer name")]
        [ValidateNotNullOrEmpty()]
        [System.String]$ComputerName
    )

    begin {
        Write-Verbose "Starting system information retrieval for $ComputerName"
    }

    process {
        try {
            # Use Write-Verbose instead of Write-Output for logging
            Write-Verbose "Processing system information request for $ComputerName"

            # Return the result properly
            $result = "System info for $ComputerName"
            return $result
        }
        catch {
            Write-Error "Failed to get system information for $ComputerName`: $($_.Exception.Message)"
            throw
        }
    }

    end {
        Write-Verbose "Completed system information retrieval"
    }
}

# Example usage (commented out to avoid execution during analysis)
# $systemInfo = Get-SystemInformation -ComputerName "localhost" -Verbose
# Write-Information "Retrieved: $systemInfo" -InformationAction Continue
