# PowerShell script with Information-level PSScriptAnalyzer issues
# This file is designed to trigger Information-level warnings

# PSProvideCommentHelp - Function without comment-based help
function Get-ServerInfo {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ComputerName,
        [string]$LogPath = "C:\Logs"
    )
    
    # PSUseCorrectCasing - Incorrect cmdlet casing
    get-computerinfo -ComputerName $ComputerName
    write-output "Server information retrieved"
    set-location $LogPath
}

# PSAvoidUsingDoubleQuotesForConstantString - Unnecessary double quotes
function Test-StringQuotes {
    $greeting = "Hello"
    $name = "World"
    $message = "Welcome"
    $status = "Active"
    
    # PSAvoidUsingPositionalParameters - Using positional parameters
    Write-Output $greeting $name
    Join-Path "C:\Temp" "file.txt"
    
    return $message
}

# PSPossibleIncorrectUsageOfAssignmentOperator - Assignment instead of comparison
function Test-AssignmentOperator {
    param([string]$UserName)
    
    # This should be -eq for comparison, not =
    if ($UserName = "admin") {
        Write-Output "Admin user detected"
    }
    
    # Another example
    if ($Status = "Running") {
        Write-Output "Service is running"
    }
}

# PSAvoidTrailingWhitespace - Lines with trailing spaces (added intentionally)
function Test-TrailingSpaces {
    $data = "sample"    
    $info = "information"   
    $result = "output"     
    
    # PSUseCorrectCasing - Mixed case issues
    foreach ($item in get-childitem) {
        write-verbose $item.Name
        start-process $item.FullName
    }
}

# Function with multiple Information issues
function Process-Data {
    # PSAvoidUsingDoubleQuotesForConstantString
    $folder = "Documents"
    $extension = "txt"
    
    # PSAvoidUsingPositionalParameters and PSUseCorrectCasing
    get-childitem "C:\Users" "*.log"
    copy-item "source.txt" "destination.txt"
    
    # PSPossibleIncorrectUsageOfAssignmentOperator
    $files = get-childitem
    foreach ($file in $files) {
        if ($file.Extension = ".txt") {
            write-host "Found text file"
        }
    }
}

# PSProvideCommentHelp - Another function without help
function Start-BackgroundTask {
    param([scriptblock]$ScriptBlock)
    Start-Job -ScriptBlock $ScriptBlock
}

# Lines with trailing whitespace (Information-level issue)
$global:config = @{
    Server = "localhost"    
    Database = "TestDB"   
    Timeout = 30     
}
