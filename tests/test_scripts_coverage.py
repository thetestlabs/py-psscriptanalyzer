"""Tests for scripts.py module focused on improving coverage."""

from py_psscriptanalyzer.scripts import generate_analysis_script, generate_format_script


def test_generate_analysis_script_with_security_filter():
    """Test generating analysis script with security filter."""
    script = generate_analysis_script("$files", security_only=True)

    # Check security filter is included
    assert "# Filter to include only security-related rules" in script
    assert "$categoryRules = @(" in script
    assert "IsSecurityRule" in script  # Check if the IsSecurityRule property is added


def test_generate_format_script():
    """Test generating formatting script."""
    script = generate_format_script("$files")

    # Check formatting commands are included
    assert "Invoke-Formatter" in script
    assert "foreach ($file in $files)" in script


def test_generate_analysis_script_with_style_filter():
    """Test generating analysis script with style filter."""
    script = generate_analysis_script("$files", style_only=True)

    # Check style filter is included
    assert "# Filter to include only style-related rules" in script
    assert "$categoryRules = @(" in script
    assert "RuleCategory" in script
    assert "Style" in script


def test_generate_analysis_script_with_performance_filter():
    """Test generating analysis script with performance filter."""
    script = generate_analysis_script("$files", performance_only=True)

    # Check performance filter is included
    assert "# Filter to include only performance-related rules" in script
    assert "$categoryRules = @(" in script
    assert "RuleCategory" in script
    assert "Performance" in script


def test_generate_analysis_script_with_best_practices_filter():
    """Test generating analysis script with best practices filter."""
    script = generate_analysis_script("$files", best_practices_only=True)

    # Check best practices filter is included
    assert "# Filter to include only best practices rules" in script
    assert "$categoryRules = @(" in script
    assert "RuleCategory" in script
    assert "BestPractices" in script


def test_generate_analysis_script_with_dsc_filter():
    """Test generating analysis script with DSC filter."""
    script = generate_analysis_script("$files", dsc_only=True)

    # Check DSC filter is included
    assert "# Filter to include only DSC-related rules" in script
    assert "$categoryRules = @(" in script
    assert "RuleCategory" in script
    assert "DSC" in script


def test_generate_analysis_script_with_compatibility_filter():
    """Test generating analysis script with compatibility filter."""
    script = generate_analysis_script("$files", compatibility_only=True)

    # Check compatibility filter is included
    assert "# Filter to include only compatibility-related rules" in script
    assert "$categoryRules = @(" in script
    assert "RuleCategory" in script
    assert "Compatibility" in script


def test_generate_analysis_script_with_include_rules():
    """Test generating analysis script with include rules."""
    script = generate_analysis_script("$files", include_rules=["Rule1", "Rule2"])

    # Check include rules filter is included
    assert "# Filter to include only specific rules" in script
    assert "$includeRules = @(" in script
    assert "'Rule1'" in script
    assert "'Rule2'" in script


def test_generate_analysis_script_with_exclude_rules():
    """Test generating analysis script with exclude rules."""
    script = generate_analysis_script("$files", exclude_rules=["Rule1", "Rule2"])

    # Check exclude rules filter is included
    assert "# Filter to exclude specific rules" in script
    assert "$excludeRules = @(" in script
    assert "'Rule1'" in script
    assert "'Rule2'" in script
