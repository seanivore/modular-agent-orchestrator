"""
Update CLI Command - UI Display Patterns
Data structure definitions for workflow update display
"""

from typing import Dict, Any, List

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

def display_update_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize update command results for UI display.
    
    Returns structured data for update status display.
    Focus: Essential data structure, not detailed formatting.
    
    Args:
        result: Update execution result dictionary
        
    Returns:
        Structured display data dictionary
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "show_retry_options": True,
            "suggested_actions": [
                "Check file path and permissions", 
                "Verify JSON format",
                "Review secondary flag syntax"
            ]
        }
    
    # Structure success data for display
    display_data = {
        "display_type": "update_success",
        "header": {
            "title": "Workflow Update Complete",
            "message": result.get("message", "Update completed successfully"),
            "timestamp": result.get("timestamp"),
            "workflow_id": result.get("workflow_id")
        },
        "file_operations": {
            "output_file": result.get("output_file"),
            "target_directory": result.get("target_directory"),
            "original_preserved": True
        },
        "modifications": _structure_modifications(result.get("modifications_applied", {})),
        "next_steps": _structure_next_steps(result),
        "show_success_indicator": True
    }
    
    return display_data

def _structure_modifications(modifications: Dict[str, Any]) -> Dict[str, Any]:
    """Structure modifications data for display"""
    if not modifications:
        return {"has_modifications": False}
    
    structured_mods = {
        "has_modifications": True,
        "update_method": modifications.get("update_method", "cli_update_command"),
        "timestamp": modifications.get("updated_at"),
        "modifications_list": []
    }
    
    # Process modification entries
    for key, value in modifications.items():
        if key in ["updated_at", "update_method", "original_file_preserved"]:
            continue
            
        mod_entry = {
            "type": key.replace("_", " ").title(),
            "description": str(value) if value else "",
            "applied": True
        }
        structured_mods["modifications_list"].append(mod_entry)
    
    return structured_mods

def _structure_next_steps(result: Dict[str, Any]) -> Dict[str, Any]:
    """Structure next steps data for display"""
    workflow_id = result.get("workflow_id")
    output_file = result.get("output_file")
    
    next_steps = {
        "has_workflow_actions": bool(workflow_id),
        "has_file_actions": bool(output_file),
        "workflow_actions": [],
        "file_actions": [],
        "general_actions": []
    }
    
    # Workflow-specific actions
    if workflow_id:
        next_steps["workflow_actions"] = [
            {"action": "review", "command": f"mao review {workflow_id}", "description": "Review updated workflow"},
            {"action": "continue", "command": f"mao continue {workflow_id}", "description": "Continue workflow execution"}
        ]
    
    # File-specific actions
    if output_file:
        next_steps["file_actions"] = [
            {"action": "view", "path": output_file, "description": "Review output file contents"}
        ]
    
    # General actions
    next_steps["general_actions"] = [
        {"action": "list", "command": "mao workflows", "description": "List all workflows"},
        {"action": "stats", "command": "mao stats", "description": "Check system status"}
    ]
    
    return next_steps

def display_secondary_flags_help() -> Dict[str, Any]:
    """Structure secondary flags help data for display"""
    return {
        "display_type": "help_secondary_flags",
        "title": "Update Command Secondary Flags",
        "flags": [
            {
                "flag": "-add",
                "format": "type:name",
                "description": "Add new phase or agent to workflow",
                "examples": ["phase:testing", "agent:validator"]
            },
            {
                "flag": "-remove", 
                "format": "type:name",
                "description": "Remove existing phase or agent",
                "examples": ["phase:outdated", "agent:deprecated"]
            },
            {
                "flag": "-replace",
                "format": "type:old:new",
                "description": "Replace existing workflow elements",
                "examples": ["phase:dev:development", "agent:old:new"]
            },
            {
                "flag": "-rename",
                "format": "old:new",
                "description": "Rename workflow elements",
                "examples": ["old_name:new_name", "test:testing"]
            },
            {
                "flag": "-chat",
                "format": "message",
                "description": "Natural language workflow updates",
                "examples": ["add phase called validation", "update goal to include testing"]
            }
        ],
        "usage_examples": [
            {
                "title": "Basic update",
                "command": "mao update ." / "workflow.json"
            },
            {
                "title": "Multi-path update",
                "command": "mao update ./update.json --target /path/to" / "workflow"
            },
            {
                "title": "With secondary flags",
                "commands": [
                    "mao update ." / "workflow.json -add phase:validation",
                    "mao update ." / "workflow.json -remove agent:outdated_agent",
                    "mao update ." / Path(r"workflow.json -chat \")add testing phase\""
                ]
            },
            {
                "title": "Combined operations",
                "command": "mao update ." / "workflow.json -add phase:qa -remove phase:temp"
            }
        ]
    }

def display_multi_path_info(path_info: Dict[str, Any]) -> Dict[str, Any]:
    """Structure multi-path resolution data for display"""
    if not path_info:
        return {"display_type": "no_path_info"}
    
    return {
        "display_type": "path_resolution",
        "paths": {
            "json_file": path_info.get("json_path", "Unknown"),
            "target_directory": path_info.get("target_path", "Unknown")
        },
        "detection_results": {
            "is_workflow_directory": path_info.get("is_workflow_directory", False),
            "requires_json_copy": path_info.get("requires_json_copy", False)
        },
        "status_indicators": {
            "workflow_dir_detected": path_info.get("is_workflow_directory", False),
            "json_copy_needed": path_info.get("requires_json_copy", False)
        }
    }

def display_validation_errors(errors: List[str]) -> Dict[str, Any]:
    """Structure validation errors data for display"""
    if not errors:
        return {"display_type": "no_errors"}
    
    return {
        "display_type": "validation_errors",
        "error_count": len(errors),
        "errors": [{"message": error, "severity": "error"} for error in errors],
        "show_fix_suggestions": True
    }

def display_processing_status(status: str, details: str = "") -> Dict[str, Any]:
    """Structure processing status data for display"""
    return {
        "display_type": "processing_status",
        "status": status,
        "details": details,
        "show_progress": True,
        "timestamp": None  # Would be set by caller
    }

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate update UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free