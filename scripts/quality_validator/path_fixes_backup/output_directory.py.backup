"""
Output CLI Command - Core Logic
Set output directory via settings_manager.py with path validation and user configuration persistence
"""

import json
import hashlib
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError
from orchestrator.settings_manager import ApplicationSettingsManager, get_user_settings, update_user_setting
from orchestrator.username_manager import get_session_user

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="output", return_dict=True)
def execute_output(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main output command execution with path validation and settings integration.
    
    Sets user output directory via settings_manager.py with automatic
    user config JSON file updates via User ID/Username.
    
    Args:
        params: Command parameters including 'path' for output directory
        
    Returns:
        Standardized result dictionary with output directory information
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "output")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 5 minutes (output directory changes infrequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "output")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Low cost as primarily file system operations with minimal processing.
    """
    operation = params.get('operation', 'set_output') if params else 'set_output'
    
    # Cost varies by operation complexity
    cost_map = {
        'set_output': 0.002,          # Path validation + settings update
        'get_current_output': 0.001,   # Settings retrieval only
        'validate_path': 0.001,        # Path validation only
        'create_directory': 0.002      # Directory creation + validation
    }
    
    return cost_map.get(operation, 0.002)

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including user context and path state"""
    base_key = f"output|{str(params) if params else 'none'}"
    
    # Add current user context
    session_user = get_session_user()
    if session_user:
        username = session_user.get('username', 'anonymous')
        user_id = session_user.get('user_id', 'unknown')
        base_key += f"|user:{username}|id:{user_id}"
    
    # Add current output directory setting state
    try:
        if session_user and session_user.get('username'):
            user_settings = get_user_settings(session_user['username'])
            current_output = user_settings.get('output_directory', 'default')
            base_key += f"|current:{current_output}"
    except Exception:
        base_key += "|current:unknown"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core output command logic implementation with settings_manager integration"""
    try:
        operation = params.get('operation', 'set_output') if params else 'set_output'
        
        # Get current session user
        session_user = get_session_user()
        username = session_user.get('username') if session_user else None
        
        if not username:
            return {
                "success": False,
                "error": "User must be logged in to set output directory",
                "timestamp": datetime.now().isoformat()
            }
        
        if operation == 'set_output':
            return _handle_set_output(username, params)
        elif operation == 'get_current_output':
            return _handle_get_current_output(username, params)
        else:
            # Default to set_output for unknown operations
            return _handle_set_output(username, params)
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Output command failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_set_output(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle setting output directory with path validation"""
    try:
        # Get target path from params
        if not params or 'path' not in params:
            return {
                "success": False,
                "error": "Missing required parameter: path",
                "help": "Usage: mao --output /path/to/directory or /output /path/to/directory",
                "timestamp": datetime.now().isoformat()
            }
        
        target_path = params['path']
        
        # Get current output directory setting
        user_settings = get_user_settings(username)
        current_output = user_settings.get('output_directory', None)
        
        # Validate and normalize path
        validation_result = _validate_output_path(target_path)
        if not validation_result['valid']:
            return {
                "success": False,
                "error": validation_result['error'],
                "current_output": current_output,
                "timestamp": datetime.now().isoformat()
            }
        
        normalized_path = validation_result['normalized_path']
        
        # Check if directory needs creation
        path_obj = Path(normalized_path)
        directory_existed = path_obj.exists()
        
        # Create directory if it doesn't exist
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create directory: {str(e)}",
                "path": normalized_path,
                "current_output": current_output,
                "timestamp": datetime.now().isoformat()
            }
        
        # Update user setting via settings_manager
        success = update_user_setting(username, 'output_directory', normalized_path)
        
        if success:
            # Clear relevant caches
            _clear_output_caches(username)
            
            return {
                "success": True,
                "operation": "set_output",
                "previous_output": current_output,
                "new_output": normalized_path,
                "user": username,
                "message": f"Output directory updated to: {normalized_path}",
                "directory_created": not directory_existed,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Failed to update output directory setting",
                "path": normalized_path,
                "current_output": current_output,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Set output directory failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_get_current_output(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle getting current output directory setting"""
    try:
        # Get user settings
        user_settings = get_user_settings(username)
        current_output = user_settings.get('output_directory', None)
        
        # Get default output directory from settings definition
        manager = ApplicationSettingsManager()
        settings_definitions = manager.discover_settings()
        default_output = None
        
        if 'output_directory' in settings_definitions:
            default_output = settings_definitions['output_directory'].default
        
        return {
            "success": True,
            "operation": "get_current_output",
            "current_output": current_output,
            "default_output": default_output,
            "using_default": current_output == default_output,
            "user": username,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Get current output directory failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _validate_output_path(path: str) -> Dict[str, Any]:
    """Validate and normalize output directory path"""
    try:
        # Handle tilde expansion
        expanded_path = os.path.expanduser(path)
        
        # Convert to absolute path
        absolute_path = os.path.abspath(expanded_path)
        
        # Validate path format (basic checks)
        if not absolute_path:
            return {
                "valid": False,
                "error": "Invalid path format"
            }
        
        # Check if parent directory exists (for creation feasibility)
        parent_dir = Path(absolute_path).parent
        if not parent_dir.exists():
            return {
                "valid": False,
                "error": f"Parent directory does not exist: {parent_dir}"
            }
        
        # Check write permissions on parent directory
        if not os.access(parent_dir, os.W_OK):
            return {
                "valid": False,
                "error": f"No write permission for parent directory: {parent_dir}"
            }
        
        return {
            "valid": True,
            "normalized_path": absolute_path,
            "original_path": path
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Path validation failed: {str(e)}"
        }

def _clear_output_caches(username: str = None):
    """Clear relevant caches after output directory updates"""
    cache_keys = [
        "settings_discovery",
        "default_settings",
        "settings_by_section"
    ]
    
    if username:
        cache_keys.extend([
            f"user_settings|{username}",
            f"output|user:{username}"
        ])
    
    for key in cache_keys:
        cache.clear_cache(key)

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_output(params)