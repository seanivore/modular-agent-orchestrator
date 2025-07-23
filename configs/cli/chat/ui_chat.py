"""
Chat CLI Command - UI Display Patterns
Provides essential data structure for chat command results and workflow transition
"""

from typing import Dict, Any
from pathlib import Path

def display_chat_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize chat command results for UI display.
    
    Returns structured data for conversation bridge transition display.
    Focus: Essential data structure for workflow creation feedback.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "original_message": result.get("original_message", ""),
            "show_suggestions": True,
            "error_details": {
                "workflow_id": result.get("workflow_id"),
                "bridge_stderr": result.get("bridge_stderr", "")
            }
        }
    
    # Structure data for successful workflow creation display
    display_data = {
        "display_type": "workflow_created",
        "header": {
            "title": "Workflow Created Successfully",
            "subtitle": "Your message has been converted into an executable workflow"
        },
        "workflow_info": {
            "workflow_id": result.get("workflow_id"),
            "custom_command": result.get("custom_command"),
            "ready_to_execute": result.get("ready_to_execute", False),
            "from_cache": result.get("from_cache", False)
        },
        "message_info": {
            "original_message": result.get("original_message", ""),
            "message_processed": True
        },
        "file_locations": {
            "use_case_directory": result.get("use_case_directory"),
            "config_path": result.get("config_path")
        },
        "next_steps": {
            "show_execution_options": True,
            "show_review_option": True,
            "show_modify_option": True
        },
        "system_output": {
            "bridge_output": result.get("bridge_output", ""),
            "timestamp": result.get("timestamp")
        }
    }
    
    return display_data

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know for chat command display.
    """
    return {
        "layout_pattern": "workflow_creation_feedback",
        "essential_elements": [
            "success_confirmation_header",
            "workflow_information_section",
            "original_message_display",
            "file_location_information",
            "next_steps_action_area",
            "system_output_details"
        ],
        "interaction_requirements": {
            "success_state": "clear confirmation of workflow creation",
            "workflow_display": "show workflow ID and custom command prominently",
            "message_confirmation": "display original message for verification",
            "action_buttons": "provide clear next step options",
            "file_access": "show where files were created for transparency"
        },
        "content_priorities": [
            "workflow_creation_success",
            "custom_command_visibility",
            "execution_readiness_status",
            "next_action_clarity"
        ],
        "error_handling": {
            "error_message_prominence": "clear error communication",
            "original_message_preservation": "show what was attempted",
            "suggestion_display": "helpful next steps for errors",
            "technical_details": "collapsible system error details"
        },
        "data_structure_notes": [
            "workflow_id_for_tracking",
            "custom_command_for_execution",
            "file_paths_for_user_access",
            "bridge_output_for_debugging",
            "cache_indicator_for_transparency"
        ]
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure for chat command failures"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check that your message is clear and specific",
            "Verify conversation bridge is properly configured",
            "Try with a simpler, more direct message",
            "Check system logs for detailed error information"
        ],
        "show_help_hint": True,
        "error_category": "conversation_bridge"
    }

def display_transition_feedback() -> Dict[str, Any]:
    """Provide feedback structure for CLI to app transition"""
    return {
        "display_type": "transition",
        "message": "Processing your message and creating workflow...",
        "show_progress": True,
        "steps": [
            "Analyzing your message",
            "Creating workflow configuration", 
            "Generating custom command",
            "Setting up execution environment"
        ]
    }