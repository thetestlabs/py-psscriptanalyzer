# Bad example with multiple issues
function Get-Users {
    param(
        [string]$Password
    )
    
    # Using alias instead of full cmdlet
    ls C:\Users | where Name -like "*test*"
    
    # Hardcoded credential (security issue)
    $cred = New-Object PSCredential("admin", (ConvertTo-SecureString "password123" -AsPlainText -Force))
    
    # Missing help documentation
    Write-Host "Getting users..."
}

# Information-level issues examples
function Test-InformationIssues {
    param([string]$Name, [int]$Count)
    
    # PSAvoidUsingPositionalParameters - using positional instead of named parameters
    Write-Output "Processing" "data"    
    
    # PSAvoidUsingDoubleQuotesForConstantString - using double quotes unnecessarily
    $simpleString = "Hello"
    $anotherString = "World"
    
    # PSUseCorrectCasing - incorrect cmdlet casing
    write-host "This has wrong casing"
    get-process "notepad"
    
    # PSPossibleIncorrectUsageOfAssignmentOperator - potential assignment vs comparison issue
    if ($Name = "test") {
        Write-Output "Found test"
    }
    
    # PSAvoidTrailingWhitespace - lines with trailing spaces (added manually)
    $variable = "value"    
    $another = "data"   
}

# Function without comment-based help (PSProvideCommentHelp)
function Get-DataWithoutHelp {
    param([string]$Path)
    Get-Content $Path
}