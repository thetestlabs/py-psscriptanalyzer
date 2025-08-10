# Mixed severity example - shows Error (red), Warning (orange), Information (cyan)
# This script demonstrates all three severity levels with color coding

# Error level issues
function Test-ErrorIssues {
    # PSAvoidUsingPlainTextForPassword (Error)
    $password = "plaintext123"
    $securePass = ConvertTo-SecureString $password -AsPlainText -Force
    
    # PSAvoidUsingInvokeExpression (Error)  
    $dangerousCommand = "Remove-Item C:\*"
    # Invoke-Expression $dangerousCommand  # Commented to prevent actual execution
}

# Warning level issues  
function Test-WarningIssues {
    # PSUseApprovedVerbs (Warning)
    # PSUseSingularNouns (Warning)
    param([string]$FilePath)
    
    # PSAvoidUsingWriteHost (Warning)
    Write-Host "Processing files..."
    
    # PSUseDeclaredVarsMoreThanAssignments (Warning)
    $unusedVariable = "Never used"
}

# Information level issues
function Test-InformationIssues {
    # PSAvoidUsingDoubleQuotesForConstantString (Information)
    $name = "TestUser"
    $status = "Active"    
    
    # PSUseCorrectCasing (Information)
    get-process | where-object Name -like "*test*"
    
    # PSPossibleIncorrectUsageOfAssignmentOperator (Information)
    if ($status = "Active") {
        write-host "User is active"
    }
}

# Function without help documentation (Information)
function Get-SystemData {
    Get-ComputerInfo
}
