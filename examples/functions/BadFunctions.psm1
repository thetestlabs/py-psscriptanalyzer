# Functions with parameter and pipeline issues

# PSReviewUnusedParameter - unused parameters
function Test-UnusedParams {
    param(
        [string]$UsedParam,
        [string]$UnusedParam,  # This parameter is never used
        [int]$AnotherUnusedParam
    )
    
    Write-Output "Only using: $UsedParam"
}

# PSUseConsistentIndentation - inconsistent indentation
function Test-BadIndentation {
param(
[string]$Name
)

  if ($Name) {
        Write-Output $Name
      }
    else {
  Write-Output "No name"
    }
}

# PSUseConsistentWhitespace - inconsistent whitespace
function Test-BadWhitespace{
    param(
        [string]$Value
    )
    
    $result=$Value+  "suffix"   # Bad spacing around operators
    if($result -eq""){  # Missing spaces
        return$null
    }
    
    return $result
}

# PSUseShouldProcessForStateChangingFunctions - missing ShouldProcess
function Remove-UserData {
    param(
        [string]$UserName
    )
    
    # This function changes state but doesn't use ShouldProcess
    Remove-Item "C:\Users\$UserName\*" -Recurse -Force
    Remove-ADUser $UserName
}

# PSMisleadingBacktick - misleading use of backticks
function Get-ProcessInfo {
    param(
        [string]$ProcessName
    )
    
    # PSMisleadingBacktick - backtick at end of line that's not needed
    Get-Process -Name $ProcessName `
    | Select-Object Name, CPU
    
    # Should be:
    # Get-Process -Name $ProcessName |
    #     Select-Object Name, CPU
}

# PSAvoidUsingDoubleQuotesForConstantString - unnecessary double quotes
function Test-Quotes {
    $constant = "Hello"  # Should use single quotes for constants
    $variable = "Hello $env:USERNAME"  # Double quotes needed here
    
    Write-Output $constant
    Write-Output $variable
}

# PSUseCompatibleCmdlets - using cmdlets not available in all versions
function Test-Compatibility {
    # Get-Clipboard is not available in PowerShell Core on Linux/macOS
    $clipboardContent = Get-Clipboard
    
    # Using Windows-specific cmdlets
    Get-EventLog -LogName Application -Newest 10
    
    return $clipboardContent
}

# PSAvoidAssignmentToAutomaticVariable - assigning to automatic variables
function Test-AutomaticVars {
    $Error = "Custom error"  # $Error is an automatic variable
    $Host = "Custom host"    # $Host is an automatic variable
    
    Write-Output $Error
    Write-Output $Host
}

# PSUseLiteralInitializerForHashtable - using New-Object for hashtables
function Test-HashtableCreation {
    # Inefficient way to create hashtable
    $hash1 = New-Object hashtable
    $hash1.Add("key", "value")
    
    # Should use literal syntax:
    $hash2 = @{
        key = "value"
    }
    
    return $hash1, $hash2
}

# PSAvoidUsingBrokenHashAlgorithms - using deprecated hash algorithms
function Get-FileHash-Broken {
    param([string]$FilePath)
    
    # MD5 and SHA1 are considered broken
    $md5Hash = Get-FileHash -Path $FilePath -Algorithm MD5
    $sha1Hash = Get-FileHash -Path $FilePath -Algorithm SHA1
    
    return $md5Hash, $sha1Hash
}

# Export all functions (this would normally be in a module manifest)
Export-ModuleMember -Function *
