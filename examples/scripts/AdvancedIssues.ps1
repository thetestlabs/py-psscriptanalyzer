# Advanced script with DSC and advanced function issues

# PSUseIdenticalMandatoryParametersForDSC - DSC resource issues
[DscResource()]
class BadDscResource {
    [DscProperty(Key)]
    [string]$Name
    
    [DscProperty(Mandatory)]
    [string]$Value
    
    # PSReturnCorrectTypesForDSCFunctions - wrong return types for DSC methods
    [BadDscResource] Get() {
        # Should return the current state
        return $null  # Wrong return type
    }
    
    [bool] Test() {
        # Should return boolean indicating if in desired state
        return "true"  # Wrong return type - string instead of bool
    }
    
    [void] Set() {
        # PSUseShouldProcessForStateChangingFunctions in DSC
        # DSC Set() should change state to match desired configuration
        Write-Host "Setting resource state"  # PSAvoidUsingWriteHost
    }
}

# Advanced function with parameter issues
function Test-AdvancedFunction {
    [CmdletBinding(
        SupportsShouldProcess = $true,
        ConfirmImpact = 'High'
    )]
    param(
        [Parameter(
            Mandatory = $true,
            ValueFromPipeline = $true,
            ValueFromPipelineByPropertyName = $true,
            Position = 0
        )]
        [ValidateNotNullOrEmpty()]
        [string[]]$InputObject,
        
        [Parameter(Mandatory = $false)]
        [ValidateSet('Option1', 'Option2', 'Option3')]
        [string]$Option = 'Option1',
        
        # PSReservedParams - using reserved parameter name differently
        [switch]$Debug  # This conflicts with common parameter
    )
    
    begin {
        # PSUseDeclaredVarsMoreThanAssignments
        $beginVar = "This variable is assigned but never used"
        
        Write-Verbose "Starting advanced function"
    }
    
    process {
        foreach ($item in $InputObject) {
            # PSUseShouldProcessForStateChangingFunctions
            if ($PSCmdlet.ShouldProcess($item, "Process item")) {
                # PSAvoidUsingInvokeExpression
                $scriptBlock = "Write-Output 'Processing: $item'"
                Invoke-Expression $scriptBlock
                
                # PSAvoidUsingPositionalParameters
                Start-Process notepad $item  # Should use -FilePath parameter
            }
        }
        
        # PSReviewUnusedParameter - $Option is defined but never used in this block
        Write-Output "Processing complete"
    }
    
    end {
        # PSAvoidUsingWriteHost
        Write-Host "Advanced function completed" -ForegroundColor Cyan
        
        # PSAvoidUsingClearHost
        if ($Debug) {
            Clear-Host
        }
    }
}

# Function with pipeline issues
function Get-BadPipelineData {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline)]
        [string[]]$ComputerName
    )
    
    # PSUsePipelineForOutput - not using pipeline correctly
    begin {
        $results = @()  # Collecting results in array instead of streaming
    }
    
    process {
        foreach ($computer in $ComputerName) {
            try {
                # PSAvoidUsingWMICmdlets
                $data = Get-WmiObject -Class Win32_OperatingSystem -ComputerName $computer
                $results += $data  # Building array instead of outputting
            }
            catch {
                # PSAvoidUsingEmptyCatchBlock
            }
        }
    }
    
    end {
        return $results  # Should use Write-Output or just output objects
    }
}

# Function with scope issues
function Test-ScopeIssues {
    param([string]$Value)
    
    # PSAvoidGlobalVars
    $global:FunctionResult = $Value
    
    # PSUseDeclaredVarsMoreThanAssignments
    $script:ModuleVariable = "Set but never read"
    
    # PSAvoidAssignmentToAutomaticVariable
    $PWD = "Custom working directory"  # $PWD is automatic
    
    Write-Output $global:FunctionResult
}

# Function with encoding and formatting issues
function Get-FileContent-BadEncoding {
    param([string]$FilePath)
    
    # PSUseBOMForUnicodeEncodedFile - encoding issues
    $content = Get-Content $FilePath -Encoding Unicode
    
    # PSAvoidLongLines - this is an intentionally very long line that exceeds recommended line length limits and makes code harder to read and maintain, especially when working in teams with different screen sizes and editor configurations, and it also makes code reviews more difficult
    
    # PSUseConsistentIndentation - mixed indentation
    if ($content) {
      Write-Output "File has content"
        if ($content.Length -gt 100) {
            Write-Output "Large file"
      }
    }
    
    # PSAvoidTrailingWhitespace - line with trailing spaces below
    $result = $content    
    
    return $result
}

# Main execution with issues
try {
    # PSAvoidUsingCmdletAliases
    $files = dir C:\temp | where {$_.Extension -eq '.txt'}
    
    # Pipeline misuse
    $files | Test-AdvancedFunction -Option 'Option2' -Debug
}
catch {
    # PSAvoidUsingEmptyCatchBlock - but this one has minimal content
    Write-Error "Something went wrong"
}

# PSMissingModuleManifestField - if this were a module
# PSAvoidUsingDeprecatedManifestFields would be checked in .psd1 files
