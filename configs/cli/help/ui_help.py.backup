"""
Help CLI Command - UI Display Patterns
Provides essential data structure for git-style help display
"""

from typing import Dict, Any

def display_help_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize help command results for UI display.
    
    Returns structured data for git-style command grouping.
    Focus: Essential data structure, not detailed formatting.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "show_suggestions": True
        }
    
    categorized_commands = result.get("categorized_commands", {})
    
    # Structure data for git-style grouping display
    display_data = {
        "display_type": "help_categories",
        "header": {
            "title": "Mao - Modular Agent Orchestrator",
            "subtitle": "These are common Mao commands used in various situations:"
        },
        "categories": [],
        "footer": {
            "total_commands": result.get("total_commands", 0),
            "show_tutorial_hint": True
        }
    }
    
    # Define category display order and descriptions
    category_info = {
        "BASICS": {
            "title": "getting started",
            "description": "(see also: mao help tutorial)"
        },
        "CREATION": {
            "title": "workflow creation", 
            "description": "(see also: mao help workflows)"
        },
        "CONFIGURATION": {
            "title": "user and session management",
            "description": "(see also: mao help config)"
        },
        "INFORMATION": {
            "title": "system information",
            "description": "(see also: mao help stats)"
        },
        "OPERATIONS": {
            "title": "workflow operations",
            "description": "(see also: mao help advanced)"
        }
    }
    
    # Build category display data
    for category_name in ["BASICS", "CREATION", "CONFIGURATION", "INFORMATION", "OPERATIONS"]:
        if category_name in categorized_commands:
            commands = categorized_commands[category_name]
            if commands:  # Only include categories with commands
                
                category_display = {
                    "category_name": category_name,
                    "title": category_info[category_name]["title"],
                    "description": category_info[category_name]["description"],
                    "commands": []
                }
                
                # Add command data for display
                for cmd in commands:
                    category_display["commands"].append({
                        "name": cmd["command"],
                        "terminal_usage": cmd["terminal_flag"],
                        "app_usage": cmd["app_command"], 
                        "description": cmd["help"],
                        "type": cmd["type"]
                    })
                
                display_data["categories"].append(category_display)
    
    # Add OTHER category if it exists
    if "OTHER" in categorized_commands and categorized_commands["OTHER"]:
        other_category = {
            "category_name": "OTHER",
            "title": "additional commands",
            "description": "",
            "commands": []
        }
        
        for cmd in categorized_commands["OTHER"]:
            other_category["commands"].append({
                "name": cmd["command"],
                "terminal_usage": cmd["terminal_flag"],
                "app_usage": cmd["app_command"],
                "description": cmd["help"],
                "type": cmd["type"]
            })
        
        display_data["categories"].append(other_category)
    
    return display_data

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know.
    """
    return {
        "layout_pattern": "git_style_grouping",
        "essential_elements": [
            "header_with_title",
            "category_sections_with_headers", 
            "command_list_with_alignment",
            "description_text_for_each_command",
            "footer_with_command_count"
        ],
        "grouping_requirements": {
            "category_headers": "lowercase with optional description",
            "command_alignment": "consistent spacing for readability",
            "description_alignment": "right-aligned or tabbed",
            "visual_hierarchy": "clear separation between categories"
        },
        "content_priorities": [
            "command_name_visibility",
            "description_clarity", 
            "category_organization",
            "usage_format_consistency"
        ],
        "interaction_needs": [
            "scannable_layout",
            "quick_command_lookup",
            "category_browsing"
        ]
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check that CLI directory is accessible",
            "Verify command JSON files are valid", 
            "Try running the command again"
        ],
        "show_help_hint": True
    }