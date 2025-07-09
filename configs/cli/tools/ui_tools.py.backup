"""
Tools CLI Command - UI Display Patterns
Provides essential data structure for categorized tool listing
"""

from typing import Dict, Any

def display_tools_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize tools command results for UI display.
    
    Returns structured data for categorized tool listing.
    Focus: Essential data structure, not detailed formatting.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "show_suggestions": True
        }
    
    categorized_tools = result.get("categorized_tools", {})
    
    # Structure data for categorized tool display
    display_data = {
        "display_type": "tool_categories",
        "header": {
            "title": "Available Tools",
            "subtitle": f"Found {result.get('total_tools', 0)} tools across {len(categorized_tools)} categories"
        },
        "categories": [],
        "footer": {
            "total_tools": result.get("total_tools", 0),
            "show_usage_hint": True
        }
    }
    
    # Define category display order and descriptions
    category_info = {
        "SEARCH": {
            "title": "search and research",
            "description": "Find information and conduct research"
        },
        "CONTENT": {
            "title": "content creation",
            "description": "Create and edit text, images, and graphics"
        },
        "DEVELOPMENT": {
            "title": "development and coding",
            "description": "Execute code and manage files"
        },
        "SYSTEM": {
            "title": "system and workflow",
            "description": "Workflow management and system operations"
        }
    }
    
    # Build category display data
    for category_name in ["SEARCH", "CONTENT", "DEVELOPMENT", "SYSTEM"]:
        if category_name in categorized_tools:
            tools = categorized_tools[category_name]
            if tools:  # Only include categories with tools
                
                category_display = {
                    "category_name": category_name,
                    "title": category_info[category_name]["title"],
                    "description": category_info[category_name]["description"],
                    "tools": []
                }
                
                # Add tool data for display
                for tool in tools:
                    category_display["tools"].append({
                        "name": tool["name"],
                        "display_name": tool["display_name"],
                        "description": tool["description"],
                        "capabilities": tool.get("capabilities", []),
                        "cost_info": tool.get("cost_info", "Unknown")
                    })
                
                display_data["categories"].append(category_display)
    
    # Add OTHER category if it exists
    if "OTHER" in categorized_tools and categorized_tools["OTHER"]:
        other_category = {
            "category_name": "OTHER",
            "title": "additional tools",
            "description": "Other available tools",
            "tools": []
        }
        
        for tool in categorized_tools["OTHER"]:
            other_category["tools"].append({
                "name": tool["name"],
                "display_name": tool["display_name"],
                "description": tool["description"],
                "capabilities": tool.get("capabilities", []),
                "cost_info": tool.get("cost_info", "Unknown")
            })
        
        display_data["categories"].append(other_category)
    
    return display_data

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know.
    """
    return {
        "layout_pattern": "categorized_tool_grid",
        "essential_elements": [
            "header_with_tool_count",
            "category_sections_with_headers",
            "tool_cards_with_info",
            "description_and_capabilities",
            "footer_with_usage_hints"
        ],
        "grouping_requirements": {
            "category_headers": "lowercase with description",
            "tool_alignment": "grid or card layout for scanability",
            "description_prominence": "tool description should be prominent",
            "capability_display": "list or badge format for capabilities"
        },
        "content_priorities": [
            "tool_display_name_visibility",
            "description_clarity",
            "category_organization",
            "capability_communication"
        ],
        "interaction_needs": [
            "scannable_tool_grid",
            "quick_tool_identification",
            "category_browsing",
            "tool_capability_review"
        ],
        "data_structure_notes": [
            "display_name_field_for_ui_flexibility",
            "capabilities_array_for_feature_listing",
            "cost_info_for_user_planning",
            "category_grouping_for_navigation"
        ]
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check that tools directory is accessible",
            "Verify tool JSON files are valid",
            "Try running the command again"
        ],
        "show_help_hint": True
    }