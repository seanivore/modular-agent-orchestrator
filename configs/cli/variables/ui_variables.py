"""
Variables UI Display Patterns
Provides consistent display formatting for workflow variables discovery results
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

def format_variables_result(result: Dict[str, Any]) -> str:
    """
    Format variables discovery result for display
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        Formatted string for terminal" / "UI display
    """
    if not result.get("success"):
        return _format_error_result(result)
    
    output_format = result.get("output_format", "table")
    
    if output_format == "json":
        return format_variables_json(result)
    elif output_format == "compact":
        return format_variables_compact(result)
    else:
        return format_variables_table(result)

def format_variables_table(result: Dict[str, Any]) -> str:
    """
    Format variables result in detailed table format
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        Table formatted string
    """
    output_lines = []
    
    # Header
    analysis_scope = result.get("analysis_scope", "all_templates")
    scope_display = f"Template: {analysis_scope}" if analysis_scope != "all_templates" else "All Templates"
    
    output_lines.append("WORKFLOW VARIABLES DISCOVERY")
    output_lines.append("=" * 50)
    output_lines.append(f"Analysis Scope: {scope_display}")
    output_lines.append(f"Total Variables: {result.get('total_variables', 0)}")
    
    with_explanations = result.get("with_explanations", False)
    if with_explanations:
        output_lines.append("Detailed explanations included")
    
    output_lines.append("")
    
    # Variables table
    variables = result.get("variables", {}).get("common_variables", {})
    
    if not variables:
        output_lines.append("ERROR: No variables found")
        return Path(r"\n").join(output_lines)
    
    # Required vs Optional sections
    setup_guidance = result.get("setup_guidance", {})
    categorized = setup_guidance.get("required_vs_optional", {})
    
    # Required Variables Section
    required_vars = categorized.get("required", [])
    if required_vars:
        output_lines.append("REQUIRED VARIABLES")
        output_lines.append("-" * 25)
        
        for var_name in required_vars:
            var_info = variables.get(var_name, {})
            output_lines.append(f"• {var_name}")
            output_lines.append(f"  Type: {var_info.get('type', 'unknown')}")
            output_lines.append(f"  Description: {var_info.get('description', 'No description')}")
            
            # Add generation command if available
            if var_info.get("generation_command"):
                output_lines.append(f"  Generate with: {var_info.get('generation_command')}")
            
            # Add example if available
            examples = var_info.get("examples", [])
            if examples:
                output_lines.append(f"  Example: {examples[0]}")
            
            # Add explanation for --explain flag
            if with_explanations and var_info.get("explanation"):
                output_lines.append(f"  Note: {var_info.get('explanation')}")
                
                if var_info.get("usage_pattern"):
                    output_lines.append(f"  Pattern: {var_info.get('usage_pattern')}")
                
                if var_info.get("placeholder_pattern"):
                    output_lines.append(f"  Placeholder: {var_info.get('placeholder_pattern')}")
            
            output_lines.append("")
    
    # Optional Variables Section
    optional_vars = categorized.get("optional", [])
    if optional_vars:
        output_lines.append("OPTIONAL VARIABLES")
        output_lines.append("-" * 25)
        
        for var_name in optional_vars:
            var_info = variables.get(var_name, {})
            output_lines.append(f"• {var_name}")
            output_lines.append(f"  Type: {var_info.get('type', 'unknown')}")
            output_lines.append(f"  Description: {var_info.get('description', 'No description')}")
            
            # Add example if available
            examples = var_info.get("examples", [])
            if examples:
                output_lines.append(f"  Example: {examples[0]}")
            
            # Add explanation for --explain flag
            if with_explanations and var_info.get("explanation"):
                output_lines.append(f"  Note: {var_info.get('explanation')}")
                
                if var_info.get("usage_pattern"):
                    output_lines.append(f"  Pattern: {var_info.get('usage_pattern')}")
            
            output_lines.append("")
    
    # Workflow JSON Structure
    if setup_guidance.get("workflow_json_structure"):
        output_lines.append("WORKFLOW JSON STRUCTURE")
        output_lines.append("-" * 30)
        
        structure = setup_guidance["workflow_json_structure"]["structure"]
        output_lines.append(json.dumps(structure, indent=2))
        output_lines.append("")
        
        # Add structure notes
        notes = setup_guidance["workflow_json_structure"].get("notes", [])
        if notes:
            output_lines.append("STRUCTURE NOTES:")
            for note in notes:
                output_lines.append(f"• {note}")
            output_lines.append("")
    
    # Placeholder Patterns
    placeholder_patterns = setup_guidance.get("placeholder_patterns", {})
    if placeholder_patterns:
        output_lines.append("PLACEHOLDER PATTERNS")
        output_lines.append("-" * 25)
        for var_name, pattern in placeholder_patterns.items():
            output_lines.append(f"• {var_name}: {pattern}")
        output_lines.append("")
    
    # Template Analysis Summary
    template_analysis = result.get("template_analysis")
    if template_analysis:
        output_lines.append("TEMPLATE ANALYSIS")
        output_lines.append("-" * 20)
        
        for template_name, analysis in template_analysis.items():
            if "error" in analysis:
                output_lines.append(f"ERROR {template_name}: {analysis['error']}")
            else:
                vars_found = analysis.get("variables_found", 0)
                output_lines.append(f"SUCCESS {template_name}: {vars_found} variables found")
        
        output_lines.append("")
    
    # Usage Examples
    output_lines.append("USAGE EXAMPLES")
    output_lines.append("-" * 20)
    output_lines.append("1. Generate required IDs:")
    output_lines.append("   mao user_id")
    output_lines.append("   mao workflow_id")
    output_lines.append("")
    output_lines.append("2. Create workflow JSON with variables:")
    output_lines.append("   Replace placeholders with generated values")
    output_lines.append("")
    output_lines.append("3. Get detailed variable explanations:")
    output_lines.append("   mao variables --explain")
    
    return Path(r"\n").join(output_lines)

def format_variables_compact(result: Dict[str, Any]) -> str:
    """
    Format variables result in compact form for logs" / "automation
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        Compact formatted string
    """
    if not result.get("success"):
        return f"ERROR: {result.get('error', 'Variables discovery failed')}"
    
    total_vars = result.get("total_variables", 0)
    analysis_scope = result.get("analysis_scope", "all")
    timestamp = result.get("timestamp", "unknown")
    
    # Get required vs optional counts
    setup_guidance = result.get("setup_guidance", {})
    categorized = setup_guidance.get("required_vs_optional", {})
    required_count = len(categorized.get("required", []))
    optional_count = len(categorized.get("optional", []))
    
    compact_info = [
        f"Total: {total_vars}",
        f"Required: {required_count}",
        f"Optional: {optional_count}",
        f"Scope: {analysis_scope}",
        f"Time: {timestamp[:16]}"
    ]
    
    return " | ".join(compact_info)

def format_variables_json(result: Dict[str, Any]) -> str:
    """
    Format variables result as JSON for API" / "integration use
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        JSON formatted string
    """
    # Create clean JSON output
    json_output = {
        "success": result.get("success", False),
        "total_variables": result.get("total_variables", 0),
        "analysis_scope": result.get("analysis_scope"),
        "timestamp": result.get("timestamp")
    }
    
    # Add variables data
    if result.get("variables"):
        json_output["variables"] = result.get("variables")
    
    # Add setup guidance
    if result.get("setup_guidance"):
        json_output["setup_guidance"] = result.get("setup_guidance")
    
    # Add template analysis
    if result.get("template_analysis"):
        json_output["template_analysis"] = result.get("template_analysis")
    
    # Add error if present
    if result.get("error"):
        json_output["error"] = result.get("error")
    
    return json.dumps(json_output, indent=2)

def format_variables_list(result: Dict[str, Any]) -> List[str]:
    """
    Format variables as a simple list for UI components
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        List of variable names
    """
    variables = result.get("variables", {}).get("common_variables", {})
    return list(variables.keys())

def format_variables_summary_table(result: Dict[str, Any]) -> str:
    """
    Format variables in a compact summary table
    
    Args:
        result: Result dictionary from variables command
        
    Returns:
        Summary table formatted string
    """
    variables = result.get("variables", {}).get("common_variables", {})
    
    if not variables:
        return "No variables found"
    
    # Table headers
    headers = ["Variable", "Type", "Required", "Description"]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    
    # Process variables and calculate widths
    table_rows = []
    for var_name, var_info in variables.items():
        row = [
            var_name,
            var_info.get("type", "unknown"),
            "YES" if var_info.get("required", False) else "NO",
            var_info.get("description", "No description")[:50] + ("..." if len(var_info.get("description", "")) > 50 else "")
        ]
        
        table_rows.append(row)
        
        # Update column widths
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Format table
    output_lines = []
    
    # Header row
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    output_lines.append(header_row)
    output_lines.append("-" * len(header_row))
    
    # Data rows
    for row in table_rows:
        data_row = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        output_lines.append(data_row)
    
    return Path(r"\n").join(output_lines)

def _format_error_result(result: Dict[str, Any]) -> str:
    """Format error result for variables discovery"""
    output_lines = []
    
    output_lines.append("WORKFLOW VARIABLES DISCOVERY FAILED")
    output_lines.append("=" * 45)
    
    error_msg = result.get("error", "Unknown error occurred")
    output_lines.append(f"Error: {error_msg}")
    output_lines.append("")
    
    # Troubleshooting guidance
    troubleshooting = result.get("troubleshooting", [])
    if troubleshooting:
        output_lines.append("TROUBLESHOOTING")
        output_lines.append("-" * 20)
        for i, step in enumerate(troubleshooting, 1):
            output_lines.append(f"{i}. {step}")
        output_lines.append("")
    
    # Default troubleshooting if none provided
    if not troubleshooting:
        output_lines.append("TROUBLESHOOTING")
        output_lines.append("-" * 20)
        output_lines.append("1. Verify workflow templates directory exists")
        output_lines.append("2. Check that template JSON files are valid")
        output_lines.append("3. Ensure proper permissions for template files")
        output_lines.append("4. Try running with a specific template: --template example-workflow")
    
    return Path(r"\n").join(output_lines)

# Helper functions for UI integration
def get_variables_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """Get summary data for UI widgets" / "components"""
    variables = result.get("variables", {}).get("common_variables", {})
    setup_guidance = result.get("setup_guidance", {})
    categorized = setup_guidance.get("required_vs_optional", {})
    
    return {
        "total_variables": result.get("total_variables", 0),
        "required_count": len(categorized.get("required", [])),
        "optional_count": len(categorized.get("optional", [])),
        "success": result.get("success", False),
        "analysis_scope": result.get("analysis_scope"),
        "variable_names": list(variables.keys()),
        "has_explanations": result.get("with_explanations", False),
        "timestamp": result.get("timestamp")
    }

def get_required_variables(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get list of required variables with details"""
    variables = result.get("variables", {}).get("common_variables", {})
    setup_guidance = result.get("setup_guidance", {})
    categorized = setup_guidance.get("required_vs_optional", {})
    required_names = categorized.get("required", [])
    
    required_vars = []
    for var_name in required_names:
        if var_name in variables:
            var_info = variables[var_name].copy()
            var_info["name"] = var_name
            required_vars.append(var_info)
    
    return required_vars

def get_variables_display_title(result: Dict[str, Any]) -> str:
    """Get display title for variables result"""
    if result.get("success"):
        total = result.get("total_variables", 0)
        scope = result.get("analysis_scope", "all")
        return f"Workflow Variables ({total} found, scope: {scope})"
    else:
        return "Workflow Variables Discovery Failed"