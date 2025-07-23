"""
Continue CLI Command - UI Display Patterns
Provides essential data structure for workflow continuation display
"""

from typing import Dict, Any

def display_continue_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize continue command results for UI display.
    
    Returns structured data for workflow continuation interface.
    Focus: Essential data structure and display priorities.
    """
    if not result.get("success", True):
        return _format_error_display(result)
    
    continuation_type = result.get("continuation_type", "unknown")
    
    if continuation_type == "recent_interrupted":
        return _format_recent_interrupted_display(result)
    elif continuation_type == "specific_workflow":
        return _format_specific_workflow_display(result)
    elif continuation_type == "workflow_selection":
        return _format_workflow_selection_display(result)
    elif continuation_type == "no_interrupted_workflows":
        return _format_no_workflows_display(result)
    else:
        return _format_unknown_display(result)

def _format_error_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format error display structure"""
    error_type = result.get("error_type", "unknown_error")
    
    display_data = {
        "display_type": "error",
        "error_message": result.get("error", "Unknown error occurred"),
        "error_type": error_type
    }
    
    # Add specific error handling based on type
    if error_type == "authentication_required":
        display_data.update({
            "show_login_suggestion": True,
            "suggested_actions": [
                "Run 'mao --login' to authenticate",
                "Check user session status"
            ]
        })
    elif error_type == "workflow_not_found":
        display_data.update({
            "show_workflow_suggestions": True,
            "suggested_actions": result.get("suggestions", [])
        })
    
    return display_data

def _format_recent_interrupted_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for most recent interrupted workflow"""
    workflow = result.get("workflow", {})
    recovery_plan = result.get("recovery_plan", {})
    
    return {
        "display_type": "recent_interrupted",
        "workflow_info": {
            "workflow_id": workflow.get("workflow_id", "Unknown"),
            "custom_command": workflow.get("custom_command", ""),
            "workflow_goal": workflow.get("workflow_goal", ""),
            "last_activity": workflow.get("last_modified", ""),
            "phases_completed": workflow.get("workflow_status", {}).phases_completed,
            "phases_total": workflow.get("workflow_status", {}).phases_total
        },
        "recovery_info": {
            "ready_to_continue": recovery_plan.get("ready_to_continue", False),
            "recovery_type": recovery_plan.get("recovery_type", "unknown"),
            "current_phase": recovery_plan.get("current_phase", "Unknown"),
            "estimated_time": recovery_plan.get("estimated_recovery_time", "Unknown"),
            "recovery_actions": recovery_plan.get("recovery_actions", [])
        },
        "other_interrupted_count": result.get("other_interrupted", 0),
        "action_buttons": {
            "primary": "Continue This Workflow",
            "secondary": "View All Interrupted Workflows" if result.get("other_interrupted", 0) > 0 else None
        }
    }

def _format_specific_workflow_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for specific workflow continuation"""
    workflow = result.get("workflow", {})
    workflow_status = result.get("workflow_status", {})
    recovery_plan = result.get("recovery_plan", {})
    
    return {
        "display_type": "specific_workflow",
        "workflow_info": {
            "workflow_id": workflow.get("workflow_id", "Unknown"),
            "custom_command": workflow.get("custom_command", ""),
            "workflow_goal": workflow.get("workflow_goal", ""),
            "workflow_description": workflow.get("workflow_description", ""),
            "created_at": workflow.get("created_at", ""),
            "last_modified": workflow.get("last_modified", "")
        },
        "status_info": {
            "current_status": workflow_status.status if workflow_status else "Unknown",
            "health": workflow_status.health if workflow_status else "Unknown",
            "phases_completed": workflow_status.phases_completed if workflow_status else 0,
            "phases_total": workflow_status.phases_total if workflow_status else 0,
            "last_activity": workflow_status.last_activity if workflow_status else "Unknown"
        },
        "recovery_info": {
            "ready_to_continue": recovery_plan.get("ready_to_continue", False),
            "recovery_type": recovery_plan.get("recovery_type", "unknown"),
            "message": recovery_plan.get("message", ""),
            "suggestion": recovery_plan.get("suggestion", ""),
            "recovery_actions": recovery_plan.get("recovery_actions", [])
        },
        "context_preview": {
            "show_context": bool(result.get("workflow_context")),
            "context_available": bool(result.get("workflow_context"))
        },
        "action_buttons": {
            "primary": "Continue Workflow" if recovery_plan.get("ready_to_continue") else "Cannot Continue",
            "secondary": "View Workflow Details"
        }
    }

def _format_workflow_selection_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for workflow selection interface"""
    return {
        "display_type": "workflow_selection",
        "header_info": {
            "total_workflows": result.get("total_workflows", 0),
            "total_continuable": result.get("total_continuable", 0)
        },
        "workflow_categories": {
            "interrupted": {
                "title": "Interrupted Workflows",
                "description": "Workflows that were paused or interrupted",
                "workflows": _format_workflow_list(result.get("interrupted_workflows", [])),
                "priority": "high"
            },
            "active": {
                "title": "Active Workflows", 
                "description": "Currently running workflows",
                "workflows": _format_workflow_list(result.get("active_workflows", [])),
                "priority": "medium"
            },
            "completed": {
                "title": "Completed Workflows",
                "description": "Finished workflows (for reference)",
                "workflows": _format_workflow_list(result.get("completed_workflows", [])),
                "priority": "low"
            }
        },
        "display_options": {
            "show_interrupted_prominently": True,
            "group_by_recency": True,
            "enable_search": True
        },
        "action_buttons": {
            "primary": "Select Workflow to Continue",
            "secondary": "Start New Workflow"
        }
    }

def _format_no_workflows_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display when no interrupted workflows found"""
    return {
        "display_type": "no_workflows",
        "message": result.get("message", "No interrupted workflows found"),
        "suggested_actions": result.get("suggested_actions", []),
        "helpful_commands": {
            "start_workflow": "mao --goal <description>",
            "list_all_workflows": "mao --workflows", 
            "review_workflows": "mao --review"
        },
        "action_buttons": {
            "primary": "Start New Workflow",
            "secondary": "View All Workflows"
        }
    }

def _format_unknown_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format display for unknown continuation types"""
    return {
        "display_type": "unknown",
        "message": "Unknown continuation result",
        "raw_data": result,
        "action_buttons": {
            "primary": "Try Again",
            "secondary": "Get Help"
        }
    }

def _format_workflow_list(workflows: list) -> list:
    """Format workflow list for consistent display"""
    formatted_workflows = []
    
    for workflow in workflows:
        workflow_status = workflow.get("workflow_status", {})
        
        formatted_workflow = {
            "workflow_id": workflow.get("workflow_id", "Unknown"),
            "display_name": workflow.get("custom_command") or workflow.get("workflow_goal", "Unnamed Workflow"),
            "status": workflow_status.status if workflow_status else "Unknown",
            "progress": {
                "completed": workflow_status.phases_completed if workflow_status else 0,
                "total": workflow_status.phases_total if workflow_status else 0,
                "percentage": _calculate_progress_percentage(workflow_status) if workflow_status else 0
            },
            "last_activity": workflow.get("last_modified", "Unknown"),
            "continuable": workflow.get("continuable", False)
        }
        
        formatted_workflows.append(formatted_workflow)
    
    return formatted_workflows

def _calculate_progress_percentage(workflow_status) -> int:
    """Calculate workflow progress percentage"""
    if not workflow_status or not workflow_status.phases_total:
        return 0
    
    return int((workflow_status.phases_completed / workflow_status.phases_total) * 100)