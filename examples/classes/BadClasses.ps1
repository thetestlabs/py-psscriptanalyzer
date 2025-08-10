# PowerShell classes with intentional design issues

# PSUseVerboseNameForParameter - single letter parameters in methods
class badclass {  # PSUseCorrectCasing - should be PascalCase
    
    # PSAvoidGlobalVars - using global variables in class
    static $GlobalClassVar = "Bad practice"
    
    # Properties without proper access modifiers
    $publicProperty = "default"
    hidden $hiddenProperty
    
    # Constructor with issues
    badclass($p) {  # PSUseVerboseNameForParameter - single char param
        $this.publicProperty = $p
        
        # PSAvoidUsingWriteHost in class methods
        Write-Host "Object created" -ForegroundColor Green
    }
    
    # Method with multiple issues
    [void]doSomething($x, $y) {  # Poor naming and single char params
        
        # PSAvoidUsingInvokeExpression in class
        $command = "Get-Date"
        $result = Invoke-Expression $command
        
        # PSUseShouldProcessForStateChangingFunctions
        Remove-Item "C:\temp\somefile.txt" -Force
        
        # PSAvoidUsingClearHost
        Clear-Host
        
        # PSAvoidUsingWriteHost
        Write-Host "Method executed: $result"
    }
    
    # Method missing proper error handling
    [string]GetData($path) {
        # PSAvoidUsingEmptyCatchBlock
        try {
            $content = Get-Content $path -ErrorAction Stop
            return $content
        }
        catch {
            # Empty catch block
        }
        return ""
    }
    
    # Method with hardcoded paths
    [void]ProcessFiles() {
        # PSAvoidUsingComputerNameHardcoded equivalent for paths
        $hardcodedPath = "C:\Windows\System32"  # Hardcoded path
        Get-ChildItem $hardcodedPath
        
        # PSAvoidUsingPositionalParameters
        Copy-Item "source.txt" "destination.txt"  # Should use -Path and -Destination
    }
    
    # Static method with issues
    static [string]StaticMethod() {
        # PSUseDeclaredVarsMoreThanAssignments
        $unusedVar = "This is never used"
        
        # PSAvoidUsingCmdletAliases
        $processes = ps | where {$_.ProcessName -like "note*"}
        
        return "Static method result"
    }
}

# Class with inheritance issues
class DerivedBadClass : badclass {
    
    # Constructor that doesn't call base constructor properly
    DerivedBadClass() {
        # Missing proper base constructor call
        $this.publicProperty = "derived"
    }
    
    # Override method with poor implementation
    [void]doSomething($x, $y) {
        # PSReviewUnusedParameter - y is not used
        Write-Output "Derived implementation: $x"
        
        # PSAvoidUsingCmdletAliases
        ls | foreach {
            # PSAvoidUsingWriteHost
            Write-Host $_.Name
        }
    }
}

# Class with validation issues
class ValidationIssues {
    [ValidateSet("Valid1", "Valid2")]
    [string]$ValidatedProperty
    
    # Constructor with no validation
    ValidationIssues($prop) {
        # Direct assignment without validation
        $this.ValidatedProperty = $prop  # Could fail if $prop is invalid
    }
    
    # Method that doesn't respect validation
    [void]SetProperty($value) {
        # PSUseShouldProcessForStateChangingFunctions
        $this.ValidatedProperty = $value  # No validation check
    }
}

# Enum with issues
enum BadEnum {
    value1 = 1  # PSUseCorrectCasing - should be PascalCase
    value2 = 2
    VALUE3 = 3  # Inconsistent casing
}

# Using the problematic classes
$instance = [badclass]::new("test")
$instance.doSomething("a", "b")

$derived = [DerivedBadClass]::new()
$derived.doSomething("x", "y")

$validation = [ValidationIssues]::new("InvalidValue")  # This would fail at runtime
