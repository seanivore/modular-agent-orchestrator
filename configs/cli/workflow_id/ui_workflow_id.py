"""
Workflow ID UI Display Patterns
Provides consistent display formatting for workflow ID generation results
"""

import json
from typing import Dict, Any, List
from datetime import datetime

def format_workflow_id_result(result: Dict[str, Any]) -> str:
    """
    Format workflow ID generation result for display
    
    Args:
        result: Result dictionary from workflow_id command
        
    Returns:
        Formatted string for terminal/UI display
    """
    if not result.get("success"):
        return _format_error_result(result)
    
    # Main workflow ID display
    output_lines = []
    
    # Header
    output_lines.append("🆔 WORKFLOW ID GENERATED")
    output_lines.append("=" * 50)
    
    # Primary workflow ID
    workflow_id = result.get("workflow_id", "N/A")
    output_lines.append(f"Workflow ID: {workflow_id}")
    output_lines.append("")
    
    # Mathematical explanation if provided
    if result.get("mathematical_details") and "explanation" in result:
        output_lines.append("📊 MATHEMATICAL EXPLANATION")
        output_lines.append("-" * 30)
        explanation = result.get("explanation", "")
        if isinstance(explanation, str):
            output_lines.append(explanation)
        else:
            output_lines.append(json.dumps(explanation, indent=2))
        output_lines.append("")
    
    # Workflow setup status
    output_lines.append("⚙️ WORKFLOW SETUP STATUS")
    output_lines.append("-" * 25)
    output_lines.append(f"Ready for Setup: {'✅ Yes' if result.get('ready_for_workflow_setup') else '❌ No'}")
    output_lines.append(f"Generation Method: {result.get('generation_method', 'unknown')}")
    
    # Memory context status
    if "memory_context_created" in result:
        memory_status = "✅ Created" if result.get("memory_context_created") else "❌ Failed"
        output_lines.append(f"Memory Context: {memory_status}")
        
        if result.get("memory_warning"):
            output_lines.append(f"  Warning: {result.get('memory_warning')}")
    
    output_lines.append("")
    
    # Next steps guidance
    if "next_steps" in result:
        output_lines.append("📋 NEXT STEPS")
        output_lines.append("-" * 15)
        for i, step in enumerate(result.get("next_steps", []), 1):
            output_lines.append(f"{i}. {step}")
        output_lines.append("")
    
    # Usage examples
    output_lines.append("💡 USAGE EXAMPLES")
    output_lines.append("-" * 20)
    output_lines.append(f"In workflow JSON: \"workflow_id\": \"{workflow_id}\"")
    output_lines.append(f"Template replacement: uid-REPLACE_WITH_GENERATED_ID → {workflow_id}")
    output_lines.append("")
    
    # Metadata
    output_lines.append("ℹ️ METADATA")
    output_lines.append("-" * 12)
    output_lines.append(f"Generated: {result.get('timestamp', 'unknown')}")
    if result.get("context_id"):
        output_lines.append(f"Context ID: {result.get('context_id')}")
    
    return "\n".join(output_lines)

def format_workflow_id_compact(result: Dict[str, Any]) -> str:
    """
    Format workflow ID result in compact form for logs/automation
    
    Args:
        result: Result dictionary from workflow_id command
        
    Returns:
        Compact formatted string
    """
    if not result.get("success"):
        return f"ERROR: {result.get('error', 'Workflow ID generation failed')}"
    
    workflow_id = result.get("workflow_id", "N/A")
    timestamp = result.get("timestamp", "unknown")
    
    compact_info = [
        f"ID: {workflow_id}",
        f"Time: {timestamp}",
        f"Setup: {'Ready' if result.get('ready_for_workflow_setup') else 'Not Ready'}"
    ]
    
    return " | ".join(compact_info)

def format_workflow_id_json(result: Dict[str, Any]) -> str:
    """
    Format workflow ID result as JSON for API/integration use
    
    Args:
        result: Result dictionary from workflow_id command
        
    Returns:
        JSON formatted string
    """
    # Create clean JSON output
    json_output = {
        "success": result.get("success", False),
        "workflow_id": result.get("workflow_id"),
        "timestamp": result.get("timestamp"),
        "ready_for_setup": result.get("ready_for_workflow_setup", False)
    }
    
    # Add optional fields if present
    if result.get("explanation"):
        json_output["explanation"] = result.get("explanation")
    
    if result.get("context_id"):
        json_output["context_id"] = result.get("context_id")
    
    if result.get("error"):
        json_output["error"] = result.get("error")
    
    return json.dumps(json_output, indent=2)

def _format_error_result(result: Dict[str, Any]) -> str:
    """Format error result for workflow ID generation"""
    output_lines = []
    
    output_lines.append("❌ WORKFLOW ID GENERATION FAILED")
    output_lines.append("=" * 40)
    
    error_msg = result.get("error", "Unknown error occurred")
    output_lines.append(f"Error: {error_msg}")
    output_lines.append("")
    
    # Troubleshooting guidance
    output_lines.append("🔧 TROUBLESHOOTING")
    output_lines.append("-" * 20)
    output_lines.append("1. Verify workflow manager is properly configured")
    output_lines.append("2. Check that unique ID generator scripts are accessible")
    output_lines.append("3. Ensure proper permissions for workflow directory")
    output_lines.append("4. Try running the command again")
    
    if result.get("fallback_available"):
        output_lines.append("")
        output_lines.append(f"💡 Fallback: {result.get('fallback_available')}")
    
    return "\n".join(output_lines)

def format_workflow_id_table(results: List[Dict[str, Any]]) -> str:
    """
    Format multiple workflow ID results in table format
    
    Args:
        results: List of workflow ID result dictionaries
        
    Returns:
        Table formatted string
    """
    if not results:
        return "No workflow IDs to display"
    
    # Table headers
    headers = ["Workflow ID", "Status", "Generated", "Setup Ready"]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    
    # Process results and calculate widths
    table_rows = []
    for result in results:
        if result.get("success"):
            row = [
                result.get("workflow_id", "N/A"),
                "✅ Success",
                result.get("timestamp", "unknown")[:16],  # Truncate timestamp
                "✅" if result.get("ready_for_workflow_setup") else "❌"
            ]
        else:
            row = [
                "N/A",
                "❌ Failed",
                result.get("timestamp", "unknown")[:16],
                "❌"
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
    
    return "\n".join(output_lines)

# Helper functions for UI integration
def get_workflow_id_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """Get summary data for UI widgets/components"""
    return {
        "workflow_id": result.get("workflow_id"),
        "success": result.get("success", False),
        "ready": result.get("ready_for_workflow_setup", False),
        "has_explanation": bool(result.get("explanation")),
        "memory_context": result.get("memory_context_created", False),
        "timestamp": result.get("timestamp")
    }

def get_workflow_id_display_title(result: Dict[str, Any]) -> str:
    """Get display title for workflow ID result"""
    if result.get("success"):
        return f"Workflow ID: {result.get('workflow_id', 'N/A')}"
    else:
        return "Workflow ID Generation Failed"