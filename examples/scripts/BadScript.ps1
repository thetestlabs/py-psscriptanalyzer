# Script with variable and naming issues
# This script intentionally violates various PSScriptAnalyzer rules

# PSUseApprovedVerbs - using non-approved verb
# PSProvideCommentHelp - missing comment-based help (Information)
function Download-File {
    param(
        $url,    # PSReviewUnusedParameter - parameter defined but not used
        $path
    )
    
    # PSUseDeclaredVarsMoreThanAssignments - variable assigned but never used
    $unusedVariable = "This variable is never used"
    
    # PSAvoidUsingPlainTextForPassword - plain text password
    $password = "MyPlainTextPassword"
    
    # PSAvoidUsingConvertToSecureStringWithPlainText - insecure conversion
    $securePassword = ConvertTo-SecureString $password -AsPlainText -Force
    
    # PSAvoidUsingDoubleQuotesForConstantString - Information level
    $simpleString = "Hello"
    $greeting = "Welcome"
    
    # PSUseCorrectCasing - Information level (incorrect cmdlet casing)
    get-process | where-object Name -eq "notepad"
    
    # PSUseShouldProcessForStateChangingFunctions - missing ShouldProcess
    Remove-Item $path -Force
    
    # PSAvoidUsingInvokeExpression - avoid Invoke-Expression
    $command = "Get-Process"
    Invoke-Expression $command
    
    Write-Host "File downloaded" # PSAvoidUsingWriteHost - avoid Write-Host
}

# PSUseSingularNouns - plural noun in function name
function Get-Files {
    # PSAvoidUsingPositionalParameters - using positional parameters
    Get-ChildItem C:\Windows *.txt
    
    # PSAvoidUsingCmdletAliases - using alias instead of full cmdlet name
    ls | where {$_.Name -like "*.log"} | foreach {Write-Output $_.FullName}
}

# PSUseVerboseNameForParameter - single character parameter
function Test-Function($f) {
    # PSAvoidGlobalVars - using global variable
    $global:MyGlobalVar = $f
    
    # PSUseCmdletCorrectly - incorrect parameter usage
    Get-Process -Name
}

# PSProvideCommentHelp - missing comment-based help
function Invoke-SomethingBad {
    param(
        [string]$ComputerName = "localhost"
    )
    
    # PSAvoidUsingWMICmdlets - using deprecated WMI cmdlets
    Get-WmiObject -Class Win32_Process -ComputerName $ComputerName
    
    # PSAvoidUsingEmptyCatchBlock - empty catch block
    try {
        Get-Process -Name "nonexistent"
    }
    catch {
        # Empty catch block - should handle the error
    }
}

# PSAvoidDefaultValueSwitchParameter - switch with default value
function Test-Switch {
    param(
        [switch]$TestSwitch = $true
    )
    
    if ($TestSwitch) {
        Write-Output "Switch is on"
    }
}

# Main script execution with issues
$VerbosePreference = "Continue"  # PSUseDeclaredVarsMoreThanAssignments

# PSAvoidUsingClearHost - avoid Clear-Host
Clear-Host

# PSReservedParams - using reserved parameter name
function Test-Reserved {
    param($Verbose)
    Write-Output $Verbose
}

Download-File
