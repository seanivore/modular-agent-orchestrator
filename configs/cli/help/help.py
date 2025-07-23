"""
Help CLI Command - Core Logic
Discovers and organizes all available CLI commands with git-style grouping
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="help", return_dict=True)
def execute_help(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main help command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI" / "app input
        
    Returns:
        Standardized result dictionary with organized command data
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "help")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 1 hour (commands don't change frequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "help")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Very low cost - just file system reading and basic organization
    return 0.001

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including CLI directory state"""
    base_key = f"help|{str(params) if params else 'none'}"
    
    # Add CLI directory state fingerprint for cache invalidation
    cli_dir = Path(__file__).parent.parent
    if cli_dir.exists():
        # Include directory modification time and file count
        dir_stat = cli_dir.stat()
        json_files = list(cli_dir.glob("*" / "[!.]*.json"))  # Exclude hidden files
        file_count = len(json_files)
        
        # Create fingerprint from directory state
        dir_fingerprint = f"{dir_stat.st_mtime}|{file_count}"
        base_key += f"|dir:{hashlib.md5(dir_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core help command logic implementation"""
    try:
        # Discover all CLI commands
        commands = _discover_cli_commands()
        
        # Organize commands by category
        categorized_commands = _categorize_commands(commands)
        
        # Return structured data for UI display
        return {
            "success": True,
            "categorized_commands": categorized_commands,
            "total_commands": len(commands),
            "categories": list(categorized_commands.keys()),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate help: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _discover_cli_commands() -> Dict[str, Dict[str, Any]]:
    """Discover all CLI commands from directory structure"""
    commands = {}
    cli_dir = Path(__file__).parent.parent
    
    for command_dir in cli_dir.iterdir():
        if not command_dir.is_dir() or command_dir.name.startswith('.'):
            continue
            
        json_file = command_dir " / " f"{command_dir.name}.json"
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    command_config = json.load(f)
                    commands[command_config.get("command", command_dir.name)] = command_config
            except (json.JSONDecodeError, KeyError) as e:
                # Skip malformed files but don't break entire help
                continue
    
    return commands

def _categorize_commands(commands: Dict[str, Dict[str, Any]]) -> Dict[str, list]:
    """Organize commands by category for git-style grouping"""
    
    # Define category mappings based on Sean's chart groupings
    category_mappings = {
        "BASICS": ["help"],
        "CREATION": ["goal", "setup", "update", "fix_it"],
        "CONFIGURATION": ["login", "logout", "config", "user_id", "workflow_id", "variables"],
        "INFORMATION": ["workflows", "stats", "tools", "models", "providers", "logs"],
        "OPERATIONS": ["continue", "review", "chat", "doctor", "dry_run", "verbose"]
    }
    
    # Initialize categories
    categorized = {category: [] for category in category_mappings.keys()}
    categorized["OTHER"] = []  # For commands not in predefined categories
    
    # Categorize each command
    for command_name, command_config in commands.items():
        categorized_flag = False
        
        for category, command_list in category_mappings.items():
            if command_name in command_list:
                categorized[category].append({
                    "command": command_name,
                    "terminal_flag": command_config.get("terminal_flag", f"--{command_name}"),
                    "app_command": command_config.get("app_command", f"" / "{command_name}"),
                    "help": command_config.get("help", "No description available"),
                    "type": command_config.get("type", "standalone")
                })
                categorized_flag = True
                break
        
        # Add to OTHER if not categorized
        if not categorized_flag:
            categorized["OTHER"].append({
                "command": command_name,
                "terminal_flag": command_config.get("terminal_flag", f"--{command_name}"),
                "app_command": command_config.get("app_command", f"" / "{command_name}"),
                "help": command_config.get("help", "No description available"),
                "type": command_config.get("type", "standalone")
            })
    
    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_help(params)