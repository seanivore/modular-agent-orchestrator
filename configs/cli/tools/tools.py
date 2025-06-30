"""
Tools CLI Command - Core Logic
Discovers and organizes all available tools with display names and smart categorization
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="tools", return_dict=True)
def execute_tools(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main tools command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary with organized tool data
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "tools")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 10 minutes (tools change less frequently than commands)
    cache.cache_content_analysis(cache_key, json.dumps(result), "tools")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Very low cost - just file system reading and basic JSON parsing
    return 0.001

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including tools directory state"""
    base_key = f"tools|{str(params) if params else 'none'}"
    
    # Add tools directory state fingerprint for cache invalidation
    tools_dir = Path(__file__).parent.parent.parent / "tools"
    if tools_dir.exists():
        # Include directory modification time and tool count
        dir_stat = tools_dir.stat()
        tool_dirs = [d for d in tools_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        tool_count = len(tool_dirs)
        
        # Include modification times of tool JSON files for granular invalidation
        json_mod_times = []
        for tool_dir in tool_dirs:
            json_file = tool_dir / f"tool_{tool_dir.name}.json"
            if json_file.exists():
                json_mod_times.append(json_file.stat().st_mtime)
        
        # Create fingerprint from directory and file state
        dir_fingerprint = f"{dir_stat.st_mtime}|{tool_count}|{sorted(json_mod_times)}"
        base_key += f"|dir:{hashlib.md5(dir_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core tools command logic implementation"""
    try:
        # Discover all tools
        tools = _discover_tools()
        
        # Organize tools by category
        categorized_tools = _categorize_tools(tools)
        
        # Return structured data for UI display
        return {
            "success": True,
            "categorized_tools": categorized_tools,
            "total_tools": len(tools),
            "categories": list(categorized_tools.keys()),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to discover tools: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _discover_tools() -> Dict[str, Dict[str, Any]]:
    """Discover all tools from directory structure"""
    tools = {}
    tools_dir = Path(__file__).parent.parent.parent / "tools"
    
    for tool_dir in tools_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith('.'):
            continue
            
        json_file = tool_dir / f"tool_{tool_dir.name}.json"
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    tool_config = json.load(f)
                    
                    # Ensure display_name exists, create from name if missing
                    if "display_name" not in tool_config:
                        tool_config["display_name"] = _create_display_name(tool_config.get("name", tool_dir.name))
                    
                    tools[tool_config.get("name", tool_dir.name)] = tool_config
                    
            except (json.JSONDecodeError, KeyError) as e:
                # Skip malformed files but don't break entire tools listing
                continue
    
    return tools

def _create_display_name(name: str) -> str:
    """Create display-friendly name from tool name"""
    # Convert snake_case to Title Case
    return name.replace("_", " ").title()

def _categorize_tools(tools: Dict[str, Dict[str, Any]]) -> Dict[str, list]:
    """Organize tools by category for optimal UX"""
    
    # Define category mappings based on tool functionality
    category_mappings = {
        "SEARCH": ["brave_search", "web_search", "perplexity_search"],
        "CONTENT": ["text_editor", "dalle_generate", "graphic_design"],
        "DEVELOPMENT": ["code_execution", "file_operations", "mcp_connector"],
        "SYSTEM": ["files_api", "think"]
    }
    
    # Initialize categories
    categorized = {category: [] for category in category_mappings.keys()}
    categorized["OTHER"] = []  # For tools not in predefined categories
    
    # Categorize each tool
    for tool_name, tool_config in tools.items():
        categorized_flag = False
        
        for category, tool_list in category_mappings.items():
            if tool_name in tool_list:
                categorized[category].append({
                    "name": tool_name,
                    "display_name": tool_config.get("display_name", _create_display_name(tool_name)),
                    "description": tool_config.get("description", "No description available"),
                    "capabilities": tool_config.get("capabilities", []),
                    "cost_info": tool_config.get("cost_estimate", "Unknown")
                })
                categorized_flag = True
                break
        
        # Add to OTHER if not categorized
        if not categorized_flag:
            categorized["OTHER"].append({
                "name": tool_name,
                "display_name": tool_config.get("display_name", _create_display_name(tool_name)),
                "description": tool_config.get("description", "No description available"),
                "capabilities": tool_config.get("capabilities", []),
                "cost_info": tool_config.get("cost_estimate", "Unknown")
            })
    
    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_tools(params)