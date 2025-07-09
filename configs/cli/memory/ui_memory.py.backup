"""
Memory CLI Command - UI Display Patterns
Provides essential data structure for memory command results with rich formatting
"""

from typing import Dict, Any, List

def display_memory_result(result: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """
    Organize memory command results for UI display with rich formatting.
    
    Args:
        result: Command execution result
        verbose: Whether to show detailed information
        
    Returns:
        Structured data for memory operation display with Panel formatting
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "usage_hint": result.get("usage", ""),
            "show_help": True,
            "error_details": {
                "operation": result.get("operation", "unknown"),
                "timestamp": result.get("timestamp")
            }
        }
    
    operation = result.get("operation", "unknown")
    
    # Handle different operation types
    if operation == "store":
        return _display_store_result(result, verbose)
    elif operation == "retrieve":
        return _display_retrieve_result(result, verbose)
    elif operation == "list":
        return _display_list_result(result, verbose)
    elif operation == "delete":
        return _display_delete_result(result, verbose)
    elif operation == "suggest":
        return _display_suggest_result(result, verbose)
    else:
        return _display_generic_result(result, verbose)

def _display_store_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for memory store operations"""
    return {
        "display_type": "success",
        "header": {
            "title": "Memory Stored",
            "subtitle": "Successfully saved to your personal memory"
        },
        "memory_info": {
            "memory_id": result.get("memory_id"),
            "category": result.get("category", "general"),
            "content_preview": result.get("content", "")[:100] + "..." if len(result.get("content", "")) > 100 else result.get("content", ""),
            "full_content": result.get("content", "") if verbose else None
        },
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_retrieve_suggestion": True,
            "show_list_suggestion": True
        }
    }

def _display_retrieve_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for memory retrieve operations"""
    memories = result.get("memories", [])
    
    return {
        "display_type": "search_results",
        "header": {
            "title": f"Memory Search Results",
            "subtitle": f"Found {result.get('total_found', 0)} memories for query: '{result.get('query', '')}'"
        },
        "search_info": {
            "query": result.get("query", ""),
            "total_found": result.get("total_found", 0),
            "showing_count": len(memories)
        },
        "memories": [_format_memory_for_display(memory, verbose) for memory in memories],
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_related_suggestions": True,
            "show_store_suggestion": True
        }
    }

def _display_list_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for memory list operations"""
    memories = result.get("memories", [])
    
    return {
        "display_type": "memory_list",
        "header": {
            "title": "Your Memories",
            "subtitle": f"Showing {len(memories)} memories" + (f" in category '{result.get('category', '')}'" if result.get('category') != 'all' else "")
        },
        "list_info": {
            "total_memories": result.get("total_memories", 0),
            "category": result.get("category", "all"),
            "showing_count": len(memories)
        },
        "memories": [_format_memory_for_display(memory, verbose) for memory in memories],
        "categories": _extract_categories(memories),
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_category_filter": True,
            "show_search_suggestion": True,
            "show_store_suggestion": True
        }
    }

def _display_delete_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for memory delete operations"""
    return {
        "display_type": "success",
        "header": {
            "title": "Memory Deleted",
            "subtitle": "Successfully removed from your personal memory"
        },
        "delete_info": {
            "memory_id": result.get("memory_id"),
            "message": result.get("message", "")
        },
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_list_suggestion": True,
            "show_undo_warning": True
        }
    }

def _display_suggest_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for memory suggest operations"""
    suggestions = result.get("suggestions", [])
    
    return {
        "display_type": "suggestions",
        "header": {
            "title": "Memory Suggestions",
            "subtitle": f"Found {result.get('total_suggestions', 0)} relevant memories for your context"
        },
        "context_info": {
            "context": result.get("context", ""),
            "total_suggestions": result.get("total_suggestions", 0),
            "showing_count": len(suggestions)
        },
        "suggestions": [_format_suggestion_for_display(suggestion, verbose) for suggestion in suggestions],
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_store_suggestion": True,
            "show_search_suggestion": True
        }
    }

def _display_generic_result(result: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Display structure for generic memory operations"""
    return {
        "display_type": "generic",
        "header": {
            "title": "Memory Operation",
            "subtitle": f"Operation: {result.get('operation', 'unknown')}"
        },
        "result_data": result,
        "metadata": {
            "timestamp": result.get("timestamp"),
            "from_cache": result.get("from_cache", False)
        },
        "actions": {
            "show_help_suggestion": True
        }
    }

def _format_memory_for_display(memory: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Format individual memory for display"""
    return {
        "memory_id": memory.get("memory_id"),
        "content": memory.get("content", ""),
        "content_preview": memory.get("content", "")[:80] + "..." if len(memory.get("content", "")) > 80 else memory.get("content", ""),
        "category": memory.get("category", "general"),
        "tags": memory.get("tags", []),
        "priority": memory.get("priority", "medium"),
        "created_at": memory.get("created_at"),
        "last_accessed": memory.get("last_accessed"),
        "access_count": memory.get("access_count", 0),
        "relevance_score": memory.get("relevance_score"),
        "show_full_content": verbose
    }

def _format_suggestion_for_display(suggestion: Dict[str, Any], verbose: bool) -> Dict[str, Any]:
    """Format individual suggestion for display"""
    return {
        "memory_id": suggestion.get("memory_id"),
        "content": suggestion.get("content", ""),
        "content_preview": suggestion.get("content", "")[:80] + "..." if len(suggestion.get("content", "")) > 80 else suggestion.get("content", ""),
        "category": suggestion.get("category", "general"),
        "relevance_score": suggestion.get("relevance_score", 0.0),
        "relevance_reason": suggestion.get("relevance_reason", ""),
        "tags": suggestion.get("tags", []),
        "created_at": suggestion.get("created_at"),
        "show_full_content": verbose
    }

def _extract_categories(memories: List[Dict[str, Any]]) -> List[str]:
    """Extract unique categories from memories list"""
    categories = set()
    for memory in memories:
        category = memory.get("category", "general")
        if category:
            categories.add(category)
    return sorted(list(categories))

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know for memory command display.
    """
    return {
        "layout_patterns": {
            "store": "success_confirmation",
            "retrieve": "search_results_list",
            "list": "memory_grid_or_list",
            "delete": "deletion_confirmation",
            "suggest": "suggestions_with_relevance"
        },
        "essential_elements": [
            "operation_header_with_icon",
            "memory_content_display",
            "metadata_information",
            "action_buttons_section",
            "search_and_filter_controls"
        ],
        "interaction_requirements": {
            "memory_cards": "clickable memory items with preview/expand",
            "search_interface": "query input with real-time suggestions",
            "category_filtering": "dropdown or tag-based filtering",
            "action_buttons": "store, search, delete, suggest operations",
            "pagination": "for large memory lists"
        },
        "content_priorities": [
            "memory_content_visibility",
            "category_and_tag_organization",
            "relevance_scoring_display",
            "timestamp_and_access_info"
        ],
        "rich_formatting": {
            "panels": "use rich Panel for sectioned display",
            "colors": "category-based color coding",
            "icons": "operation-specific icons",
            "progress": "relevance bars for suggestions"
        },
        "data_structure_notes": [
            "memory_id_for_actions",
            "content_preview_vs_full",
            "category_hierarchy_support",
            "relevance_scoring_integration",
            "cache_indicator_transparency"
        ]
    }

def display_error(error_message: str, operation: str = "unknown") -> Dict[str, Any]:
    """Provide error display structure for memory command failures"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "operation": operation,
        "suggestions": [
            "Ensure you are logged in to use memory commands",
            "Check that the memory system is properly configured",
            "Verify your input parameters are correct",
            "Try with simpler queries or content"
        ],
        "show_help_hint": True,
        "error_category": "memory_operation",
        "available_operations": ["store", "retrieve", "list", "delete", "suggest"]
    }

def display_usage_help() -> Dict[str, Any]:
    """Provide usage help structure for memory commands"""
    return {
        "display_type": "help",
        "title": "Memory Command Usage",
        "operations": [
            {
                "operation": "store",
                "usage": "/memory 'your content here'",
                "description": "Store new memory with automatic categorization"
            },
            {
                "operation": "retrieve",
                "usage": "/memory --query 'search terms'",
                "description": "Search through your memories"
            },
            {
                "operation": "list",
                "usage": "/memory --list",
                "description": "List all your memories"
            },
            {
                "operation": "delete",
                "usage": "/memory --delete [memory_id]",
                "description": "Delete specific memory"
            },
            {
                "operation": "suggest",
                "usage": "/memory --suggest 'context'",
                "description": "Get contextual memory suggestions"
            }
        ],
        "examples": [
            "/memory 'I prefer working in the morning'",
            "/memory --query 'preferences'",
            "/memory --list",
            "/memory --delete mem_123",
            "/memory --suggest 'starting new project'"
        ]
    }