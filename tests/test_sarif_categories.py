"""Tests for SARIF output with rule categories."""

import json
from unittest.mock import patch, MagicMock

from py_psscriptanalyzer.core import convert_to_sarif


def test_convert_to_sarif_with_rule_categories():
    """Test convert_to_sarif handles rule categories correctly."""
    # Create sample results with different rule categories
    ps_results = [
        {
            "RuleName": "AvoidUsingPlainTextForPassword",
            "Severity": "Error",
            "Message": "Password should be secure",
            "ScriptPath": "test.ps1",
            "Line": 10,
            "Column": 5,
            "IsSecurityRule": True,
            "RuleCategory": "Security"
        },
        {
            "RuleName": "PSAlignAssignmentStatement",
            "Severity": "Warning",
            "Message": "Align assignment statements",
            "ScriptPath": "test.ps1",
            "Line": 15,
            "Column": 8,
            "RuleCategory": "Style"
        },
        {
            "RuleName": "PSAvoidUsingInvokeExpression",
            "Severity": "Warning",
            "Message": "Avoid using Invoke-Expression",
            "ScriptPath": "test.ps1",
            "Line": 20,
            "Column": 3,
            "RuleCategory": "Performance"
        },
        {
            "RuleName": "PSUseApprovedVerbs",
            "Severity": "Warning",
            "Message": "Use approved verbs",
            "ScriptPath": "test.ps1",
            "Line": 25,
            "Column": 1,
            "RuleCategory": "BestPractices"
        }
    ]
    
    files = ["test.ps1"]
    sarif_data = convert_to_sarif(ps_results, files)
    
    # Check that rules have correct tags in SARIF output
    rules = sarif_data["runs"][0]["tool"]["driver"]["rules"]
    
    # Find rules by ID
    security_rule = next(rule for rule in rules if rule["id"] == "AvoidUsingPlainTextForPassword")
    style_rule = next(rule for rule in rules if rule["id"] == "PSAlignAssignmentStatement")
    performance_rule = next(rule for rule in rules if rule["id"] == "PSAvoidUsingInvokeExpression")
    best_practices_rule = next(rule for rule in rules if rule["id"] == "PSUseApprovedVerbs")
    
    # Verify tags
    assert "security" in security_rule["properties"]["tags"]
    assert "style" in style_rule["properties"]["tags"]
    assert "performance" in performance_rule["properties"]["tags"]
    assert "bestpractices" in best_practices_rule["properties"]["tags"]
    
    # Verify categories
    assert security_rule["properties"]["category"] == "Security"
    assert style_rule["properties"]["category"] == "Style"
    assert performance_rule["properties"]["category"] == "Performance"
    assert best_practices_rule["properties"]["category"] == "BestPractices"
