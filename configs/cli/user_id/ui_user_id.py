"""
User ID CLI Command - UI Display Patterns
Provides structured display for user ID operations with workflow state context
"""

from typing import Dict, Any

def display_user_id_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize user_id command results for UI display.
    
    Returns structured data for user ID display with workflow context.
    Focus: Clear user ID presentation with workflow integration indicators.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "suggestion": result.get("suggestion", ""),
            "show_help_hint": True
        }
    
    user_id = result.get("user_id")
    username = result.get("username", "")
    status = result.get("status", "current_user")
    
    # Structure data for user ID display
    display_data = {
        "display_type": "user_id_info",
        "header": {
            "title": "User ID Information",
            "user_id": user_id,
            "username": username
        },
        "main_content": {},
        "workflow_context": result.get("workflow_context", {}),
        "footer": {
            "show_usage_hints": True,
            "integration_status": "workflow_state_enabled"
        }
    }
    
    # Configure display based on status
    if status == "existing_user":
        display_data["main_content"] = {
            "user_status": "Existing User",
            "user_info": result.get("user_info", {}),
            "workflow_context": result.get("workflow_context", {}),
            "generation_details": {
                "explanation": result.get("generation_explanation", ""),
                "show_mathematical_steps": True
            }
        }
        display_data["footer"]["actions"] = [
            "User ID belongs to existing user",
            "Workflow context available" if result.get("workflow_context", {}).get("context_available") else "No active workflows"
        ]
        
    elif status == "new_user_id_generated":
        display_data["main_content"] = {
            "user_status": "New User ID Generated",
            "generation_details": {
                "explanation": result.get("generation_explanation", ""),
                "show_mathematical_steps": True
            },
            "next_steps": result.get("next_steps", [])
        }
        display_data["footer"]["actions"] = [
            "User ID generated but user not created yet",
            "Use login to create this user account"
        ]
        
    else:  # current_user
        display_data["main_content"] = {
            "user_status": "Current Session User",
            "user_info": result.get("user_info", {}),
            "workflow_context": result.get("workflow_context", {})
        }
        
        # Add workflow context indicators
        workflow_ctx = result.get("workflow_context", {})
        active_count = workflow_ctx.get("active_workflows", 0)
        
        if active_count > 0:
            display_data["footer"]["actions"] = [
                f"Active workflows: {active_count}",
                "Workflow state management integrated"
            ]
        else:
            display_data["footer"]["actions"] = [
                "No active workflows",
                "Ready for new workflow creation"
            ]
    
    return display_data

def display_workflow_context(workflow_context: Dict[str, Any]) -> Dict[str, Any]:
    """Display workflow context information"""
    if not workflow_context.get("context_available", False):
        return {
            "context_status": "no_workflows",
            "message": "No active workflows for this user"
        }
    
    return {
        "context_status": "workflows_active",
        "active_count": workflow_context.get("active_workflows", 0),
        "recent_workflows": workflow_context.get("recent_workflows", []),
        "integration_active": workflow_context.get("workflow_state_integration", False)
    }

def display_generation_explanation(explanation: str) -> Dict[str, Any]:
    """Structure mathematical explanation for user ID generation"""
    if not explanation:
        return {"show_explanation": False}
    
    # Parse explanation for structured display
    lines = explanation.split('\n')
    main_line = lines[0] if lines else explanation
    
    # Extract components
    if '->' in main_line:
        parts = main_line.split('->')
        username_part = parts[0].strip() if len(parts) > 0 else ""
        user_id_part = parts[1].strip() if len(parts) > 1 else ""
    else:
        username_part = explanation
        user_id_part = ""
    
    return {
        "show_explanation": True,
        "username_input": username_part,
        "user_id_output": user_id_part,
        "mathematical_steps": explanation,
        "explanation_type": "deterministic_generation"
    }

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know for user ID display.
    """
    return {
        "layout_pattern": "user_id_focused_display",
        "essential_elements": [
            "prominent_user_id_display",
            "username_context", 
            "workflow_context_indicators",
            "generation_explanation_section",
            "status_specific_actions",
            "integration_status_indicators"
        ],
        "data_requirements": {
            "user_id": "primary identifier in format user-####",
            "username": "human-readable username for context",
            "user_status": "existing_user, new_user_id_generated, or current_user",
            "workflow_context": "active workflow count and integration status",
            "generation_explanation": "mathematical steps for transparency"
        },
        "status_specific_displays": {
            "existing_user": [
                "show_user_info_summary",
                "display_workflow_context",
                "include_generation_explanation"
            ],
            "new_user_id_generated": [
                "prominent_new_id_display",
                "show_next_steps_clearly",
                "include_generation_explanation"
            ],
            "current_user": [
                "session_context_emphasis",
                "workflow_activity_summary",
                "management_options"
            ]
        },
        "workflow_integration_indicators": [
            "active_workflow_count",
            "workflow_state_management_status",
            "recent_workflow_references"
        ],
        "interaction_needs": [
            "clear_user_id_visibility",
            "quick_context_understanding",
            "workflow_relationship_clarity",
            "mathematical_transparency"
        ],
        "new_user_flow_compliance": [
            "supports_user_creation_flow",
            "integrates_with_login_process",
            "provides_clear_next_steps",
            "maintains_workflow_state_context"
        ]
    }

def display_error(error_message: str, suggestion: str = "") -> Dict[str, Any]:
    """Provide error display structure for user ID operations"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestion": suggestion,
        "help_actions": [
            "Check if you are logged in with '/login'",
            "Verify username format (6-20 alphanumeric characters)",
            "Try running the command again"
        ],
        "integration_notes": [
            "User ID operations require username manager integration",
            "Workflow state integration may be temporarily unavailable"
        ],
        "show_help_hint": True
    }