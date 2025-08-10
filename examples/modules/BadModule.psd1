# Module manifest with intentional issues
@{
    # PSMissingModuleManifestField - missing required fields
    ModuleVersion = '1.0.0'
    # Missing GUID
    # Missing Author
    # Missing Description
    
    RootModule = 'BadModule.psm1'
    
    # PSAvoidUsingDeprecatedManifestFields - using deprecated fields
    ModuleList = @('BadModule')  # Deprecated field
    
    # PSUseToExportFieldsInManifest - should specify what to export
    # Missing FunctionsToExport, CmdletsToExport, etc.
    
    # Incomplete manifest - many required fields missing
    PowerShellVersion = '5.1'
}
