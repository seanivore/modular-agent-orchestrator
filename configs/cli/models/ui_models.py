"""
Models CLI Command - UI Display Patterns
Provides essential data structure for model listing without hardcoded grouping
"""

from typing import Dict, Any

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

def display_models_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize models command results for UI display.
    
    Returns raw model data for Claude to organize naturally.
    Focus: Essential data structure, no predefined categorization.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "show_suggestions": True
        }
    
    models = result.get("models", {})
    
    # Structure data for flexible model display
    display_data = {
        "display_type": "model_list",
        "header": {
            "title": "Available Models",
            "subtitle": f"Found {result.get('total_models', 0)} models"
        },
        "models": [],
        "footer": {
            "total_models": result.get("total_models", 0),
            "show_usage_hint": True
        }
    }
    
    # Convert models to display format (no hardcoded grouping)
    for model_name, model_config in models.items():
        model_display = {
            "name": model_name,
            "display_name": model_config.get("display_name", model_name),
            "description": model_config.get("description", "No description available"),
            "provider": model_config.get("provider", "Unknown"),
            "capabilities": model_config.get("capabilities", []),
            "cost_info": model_config.get("cost_estimate", "Unknown"),
            "context_window": model_config.get("context_window", "Unknown"),
            "max_tokens": model_config.get("max_tokens", "Unknown")
        }
        
        display_data["models"].append(model_display)
    
    return display_data

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know.
    """
    return {
        "layout_pattern": "flexible_model_list",
        "essential_elements": [
            "header_with_model_count",
            "model_cards_with_info",
            "display_name_prominence", 
            "provider_indication",
            "capability_display",
            "footer_with_usage_hints"
        ],
        "data_requirements": {
            "model_name": "technical identifier for commands",
            "display_name": "user-friendly name for display",
            "provider": "model provider information",
            "capabilities": "array of model capabilities",
            "cost_info": "pricing information for planning"
        },
        "content_priorities": [
            "display_name_visibility",
            "provider_clarity", 
            "capability_communication",
            "cost_transparency"
        ],
        "interaction_needs": [
            "scannable_model_list",
            "quick_model_identification",
            "provider_filtering_potential",
            "capability_comparison"
        ],
        "data_structure_notes": [
            "raw_model_data_for_flexible_organization",
            "no_hardcoded_grouping_constraints",
            "claude_can_organize_contextually",
            "future_proof_against_new_model_types"
        ]
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check that models directory is accessible",
            "Verify model JSON files are valid",
            "Try running the command again"
        ],
        "show_help_hint": True
    }

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate models UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free
