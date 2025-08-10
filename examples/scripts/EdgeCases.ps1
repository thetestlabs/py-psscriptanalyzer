# Additional edge cases and less common PSScriptAnalyzer rules

# PSAvoidNullOrEmptyHelpMessageAttribute - empty help messages
function Test-EmptyHelp {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, HelpMessage = "")]  # Empty help message
        [string]$InputValue,
        
        [Parameter(HelpMessage = $null)]  # Null help message
        [string]$OptionalValue
    )
    
    Write-Output $InputValue
}

# PSAvoidUsingFilePath parameter name violations
function Test-FilePathIssues {
    param(
        [string]$file,      # Should be FilePath or Path
        [string]$filepath   # Inconsistent casing
    )
    
    # PSAvoidUsingReservedCharNames
    $char = "test"  # 'char' is a reserved type name
    $string = "value"  # 'string' is a reserved type name
    
    Test-Path $file
    Get-Content $filepath
}

# PSAvoidSemicolonsAsLineTerminators - using semicolons
function Test-Semicolons {
    $var1 = "value1"; $var2 = "value2";  # Avoid semicolons as line terminators
    Write-Output $var1; Write-Output $var2;
}

# PSAvoidUsingAlias for Export-ModuleMember
New-Alias -Name "BadAlias" -Value "Get-Process"  # Creating aliases

# PSPlaceOpenBrace - brace placement issues
function Test-BracePlacement
{  # Opening brace should be on same line
    param($Parameter)
    
    if ($Parameter)
    {  # Inconsistent brace placement
        Write-Output "Value: $Parameter"
    }
    else {
        Write-Output "No value"
    }
}

# PSPlaceCloseBrace - closing brace issues
function Test-ClosingBraces {
    if ($true) {
        Write-Output "True"
        }  # Poor indentation of closing brace
}

# PSUseCompatibleSyntax - using syntax not compatible with older versions
class ModernClass {
    [string] $Property = "default"  # Property initialization (PS 5.0+)
    
    static [string] $StaticProperty = "static"  # Static properties (PS 5.0+)
    
    [void] Method() {
        # Using null-conditional operator (PS 6.0+)
        $result = $this.Property?.Length
        Write-Output $result
    }
}

# PSAvoidUsingWMICmdlets - comprehensive WMI usage
function Get-SystemInfo-Bad {
    # All these WMI cmdlets are deprecated
    $os = Get-WmiObject -Class Win32_OperatingSystem
    $computer = Get-WmiObject -Class Win32_ComputerSystem
    $bios = Get-WmiObject -Class Win32_BIOS
    
    # Should use Get-CimInstance instead
    return $os, $computer, $bios
}

# PSAvoidUsingWildcardForPath - using wildcards in paths unsafely
function Test-WildcardPaths {
    param([string]$BasePath)
    
    # Unsafe wildcard usage
    Remove-Item "$BasePath\*" -Force -Recurse  # Could be dangerous
    Copy-Item "C:\Source\*" "C:\Destination\"  # Wildcard in paths
}

# PSUseProcessBlockForPipelineCommand - missing process block
function Test-PipelineWithoutProcess {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = $true)]
        [string[]]$InputObject
    )
    
    # Missing process block for pipeline input
    begin {
        Write-Verbose "Starting"
    }
    
    end {
        Write-Verbose "Ending"
        # Process block missing - pipeline input won't work correctly
    }
}

# PSReturnCorrectTypesForDSCFunctions - DSC function return types
function Get-TargetResource {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )
    
    # Should return hashtable but returns string
    return "Not a hashtable"
}

function Test-TargetResource {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )
    
    # Should return boolean but returns string
    return "true"
}

# PSUseCmdletCorrectly - incorrect cmdlet usage
function Test-CmdletMisuse {
    # Get-Process with invalid parameter combination
    Get-Process -Name "notepad" -Id 1234  # Can't use both Name and Id
    
    # Set-Location with non-existent parameter
    Set-Location -InvalidParameter "C:\"
    
    # Using positional parameters incorrectly
    Get-ChildItem C:\ -Include *.txt -Exclude *.log  # Include requires -Recurse or -Path with wildcards
}

# PSAvoidDefaultValueForMandatoryParameter - mandatory param with default
function Test-MandatoryDefault {
    param(
        [Parameter(Mandatory = $true)]
        [string]$MandatoryParam = "default"  # Mandatory parameters shouldn't have defaults
    )
    
    Write-Output $MandatoryParam
}

# PSAvoidOverwritingBuiltInCmdlets - overwriting built-in commands
function Get-Process {  # Overwriting built-in cmdlet
    param([string]$Name)
    
    Write-Output "Custom Get-Process: $Name"
}

function Where-Object {  # Overwriting built-in cmdlet
    param($FilterScript)
    
    Write-Output "Custom Where-Object"
}

# PSProvideDefaultParameterValue - missing default values where appropriate
function Test-MissingDefaults {
    param(
        [ValidateSet("Option1", "Option2", "Option3")]
        [string]$Choice,  # Should have a default value from the ValidateSet
        
        [int]$Count,  # Numeric parameters often benefit from defaults
        
        [switch]$Force
    )
    
    Write-Output "Choice: $Choice, Count: $Count, Force: $Force"
}

# PSUseUnifiedDiffFormat - when writing diff-like output
function Show-Comparison {
    $before = "Original text"
    $after = "Modified text"
    
    # Poor diff representation
    Write-Host "Before: $before" -ForegroundColor Red
    Write-Host "After: $after" -ForegroundColor Green
    
    # Should use unified diff format or proper comparison cmdlets
}

# Additional variable and scoping issues
$script:ScriptVar = "This is a script variable"  # PSAvoidGlobalVars equivalent

function Test-VariableScoping {
    # PSUseDeclaredVarsMoreThanAssignments - multiple scenarios
    $local:LocalVar = "Local variable never used"
    $private:PrivateVar = "Private variable never used"
    
    # PSAvoidAssignmentToAutomaticVariable - more automatic variables
    $LASTEXITCODE = 0  # Automatic variable
    $ErrorActionPreference = "Stop"  # This one is actually OK to set
    $DebugPreference = "Continue"  # But these assignments are questionable in functions
    
    Write-Output "Function completed"
}

# PSMissingModuleManifestField would be detected in module manifest files
# PSUseToExportFieldsInManifest would be detected in module manifest files

# Execute some of the problematic functions
Test-EmptyHelp -InputValue "test"
Test-FilePathIssues -file "test.txt" -filepath "another.txt"
Test-Semicolons
Test-BracePlacement "parameter"
