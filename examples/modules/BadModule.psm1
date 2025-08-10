# Module with security and performance issues
# This module intentionally violates security and performance rules

# PSAvoidUsingUserNameAndPasswordParams - username/password parameters
function Connect-ToService {
    [CmdletBinding()]
    param(
        [string]$UserName,
        [string]$Password,  # Should use SecureString
        [string]$Server
    )
    
    # PSAvoidUsingPlainTextForPassword
    $cred = New-Object System.Management.Automation.PSCredential($UserName, $Password)
    
    # PSUsePSCredentialType - should use PSCredential type
    return $cred
}

# PSAvoidUsingComputerNameHardcoded - hardcoded computer names
function Get-RemoteData {
    # PSAvoidUsingInvokeExpression with user input
    $computerName = "SERVER01"  # Hardcoded
    $script = "Get-Process -ComputerName $computerName"
    Invoke-Expression $script
    
    # PSUseBOMForUnicodeEncodedFile - file encoding issues would be detected
    $data = Get-Content "C:\temp\file.txt" -Encoding UTF8
    
    # PSAvoidLongLines - this line is intentionally very long to trigger the rule about line length being too excessive for readability
    $reallyLongVariableName = "This is a really long string that goes on and on and on and makes the line extremely long which violates PSScriptAnalyzer rules"
    
    return $data
}

# PSUseOutputTypeCorrectly - incorrect output type
function Get-Numbers {
    [OutputType([string])]  # Claims to return string but returns int
    param()
    
    return 42
}

# PSUseSupportsShouldProcess but no ShouldProcess implementation
function Remove-Something {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [string]$Path
    )
    
    # Missing if ($PSCmdlet.ShouldProcess(...))
    Remove-Item $Path -Force
}

# PSAvoidGlobalVars and PSAvoidUsingWriteHost
$global:ModuleGlobalVar = "Bad practice"

function Write-BadOutput {
    # PSAvoidUsingWriteHost
    Write-Host "This should use Write-Output or Write-Verbose" -ForegroundColor Red
    
    # PSAvoidUsingClearHost
    Clear-Host
    
    # PSMissingModuleManifestField - this would be caught if manifest exists
    Write-Output "Module loaded"
}

# PSReservedCmdletChar - using reserved characters
function Test-$pecialFunction {
    param()
    Write-Output "Special function with bad name"
}

# PSAvoidUsingDeprecatedManifestFields - would be in .psd1 file
# PSDSCReturnCorrectTypesForDSCFunctions - DSC specific issues

# PSAvoidTrailingWhitespace - this line has trailing spaces    
$trailingSpaces = "value"   

# PSAlignAssignmentStatement - misaligned assignments
$short = "value"
$muchLongerVariableName    = "value"
$x= "value"

# PSUseCorrectCasing - incorrect casing
$mylowercasevariable = "should be PascalCase"
$MYUPPERCASEVARIABLE = "should be PascalCase"

Export-ModuleMember -Function Connect-ToService, Get-RemoteData, Get-Numbers, Remove-Something, Write-BadOutput
