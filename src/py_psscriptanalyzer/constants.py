"""Constants used throughout py-psscriptanalyzer."""

from typing import Final

# PowerShell executable names in order of preference
POWERSHELL_EXECUTABLES: Final[list[str]] = ["pwsh", "pwsh-lts", "powershell"]

# Supported PowerShell file extensions
POWERSHELL_FILE_EXTENSIONS: Final[tuple[str, ...]] = (".ps1", ".psm1", ".psd1")

# Severity levels for PSScriptAnalyzer
SEVERITY_LEVELS: Final[list[str]] = ["All", "Information", "Warning", "Error"]

# Timeouts (in seconds)
POWERSHELL_CHECK_TIMEOUT: Final[int] = 10
MODULE_CHECK_TIMEOUT: Final[int] = 30
INSTALL_TIMEOUT: Final[int] = 120
ANALYSIS_TIMEOUT: Final[int] = 300

# Output formats
OUTPUT_FORMATS: Final[list[str]] = ["text", "json", "sarif"]

# SARIF version for output
SARIF_VERSION: Final[str] = "2.1.0"

# Security-related PSScriptAnalyzer rules
SECURITY_RULES: Final[list[str]] = [
    "AvoidUsingPlainTextForPassword",
    "AvoidUsingComputerNameHardcoded",
    "AvoidUsingConvertToSecureStringWithPlainText",
    "AvoidUsingInvokeExpression",
    "UseProcessBlockForPipelineCommand",
    "PSAvoidUsingUserNameAndPasswordParams",
    "PSUsePSCredentialType",
    "PSAvoidUsingUnencryptedNetworkResources",
    "PSAvoidGlobalAliases",
    "PSAvoidGlobalFunctions",
    "PSAvoidUsingBrokenHashAlgorithms",
]

# Style and formatting related PSScriptAnalyzer rules
STYLE_RULES: Final[list[str]] = [
    "PSAlignAssignmentStatement",
    "PSPlaceCloseBrace",
    "PSPlaceOpenBrace",
    "PSUseConsistentIndentation",
    "PSUseConsistentWhitespace",
    "PSUseCorrectCasing",
    "PSAvoidTrailingWhitespace",
    "PSAvoidSemicolonsAsLineTerminators",
    "PSAvoidLongLines",
]

# Performance-related PSScriptAnalyzer rules
PERFORMANCE_RULES: Final[list[str]] = [
    "PSAvoidUsingCmdletAliases",
    "PSAvoidUsingInvokeExpression",
    "PSAvoidUsingPositionalParameters",
    "PSUseLiteralInitializerForHashtable",
    "PSUseProcessBlockForPipelineCommand",
]

# Best practices related PSScriptAnalyzer rules
BEST_PRACTICES_RULES: Final[list[str]] = [
    "PSUseApprovedVerbs",
    "PSAvoidDefaultValueForMandatoryParameter",
    "PSAvoidDefaultValueSwitchParameter",
    "PSAvoidGlobalVars",
    "PSAvoidUsingWriteHost",
    "PSProvideCommentHelp",
    "PSUseSingularNouns",
    "PSUseShouldProcessForStateChangingFunctions",
    "PSUseSupportsShouldProcess",
    "PSShouldProcess",
]

# DSC (Desired State Configuration) related rules
DSC_RULES: Final[list[str]] = [
    "PSDSCDscExamplesPresent",
    "PSDSCDscTestsPresent",
    "PSDSCReturnCorrectTypesForDSCFunctions",
    "PSDSCUseIdenticalMandatoryParametersForDSC",
    "PSDSCUseIdenticalParametersForDSC",
    "PSDSCStandardDSCFunctionsInResource",
    "PSDSCUseVerboseMessageInDSCResource",
]

# Compatibility-related rules
COMPATIBILITY_RULES: Final[list[str]] = [
    "PSUseCompatibleCommands",
    "PSUseCompatibleSyntax",
    "PSUseCompatibleTypes",
    "PSUseCompatibleCmdlets",
]
