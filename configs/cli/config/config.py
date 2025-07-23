"""
Config CLI Command - Core Logic
Application settings management with settings_manager integration and user configuration persistence
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError
from orchestrator.settings_manager import ApplicationSettingsManager, get_user_settings, update_user_setting
from orchestrator.username_manager import get_session_user

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="config", return_dict=True)
def execute_config(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main config command execution with settings management and user persistence.
    
    Integrates with settings_manager.py for dynamic settings discovery and
    automatic user config JSON file updates via User ID/Username.
    
    Args:
        params: Command parameters from CLI" / "app input
        
    Returns:
        Standardized result dictionary with settings data and user configuration
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "config")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 12 minutes (settings change moderately frequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "config")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Medium complexity due to settings operations and user file management.
    """
    operation = params.get('operation', 'view_settings') if params else 'view_settings'
    
    # Cost varies by operation complexity
    cost_map = {
        'view_settings': 0.002,
        'discover_settings': 0.003,
        'update_setting': 0.004,
        'bulk_update': 0.005,
        'export_config': 0.003,
        'import_config': 0.004
    }
    
    return cost_map.get(operation, 0.003)

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including settings state and user context"""
    base_key = f"config|{str(params) if params else 'none'}"
    
    # Add current user context
    session_user = get_session_user()
    if session_user:
        username = session_user.get('username', 'anonymous')
        user_id = session_user.get('user_id', 'unknown')
        base_key += f"|user:{username}|id:{user_id}"
    
    # Add settings directory state fingerprint for cache invalidation
    settings_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "settings"
    if settings_dir.exists():
        # Include directory modification time and settings count
        dir_stat = settings_dir.stat()
        settings_files = [f for f in settings_dir.iterdir() if f.is_file() and f.name.endswith('_app_settings.json')]
        settings_count = len(settings_files)
        
        # Include modification times of settings JSON files for granular invalidation
        json_mod_times = []
        for settings_file in settings_files:
            if settings_file.exists():
                json_mod_times.append(settings_file.stat().st_mtime)
        
        # Create fingerprint from directory and file state
        dir_fingerprint = f"{dir_stat.st_mtime}|{settings_count}|{sorted(json_mod_times)}"
        base_key += f"|dir:{hashlib.md5(dir_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core config command logic implementation with settings_manager integration"""
    try:
        operation = params.get('operation', 'view_settings') if params else 'view_settings'
        
        # Get current session user for user-specific settings
        session_user = get_session_user()
        username = session_user.get('username') if session_user else None
        
        if operation == 'view_settings':
            return _handle_view_settings(username, params)
        elif operation == 'update_setting':
            return _handle_update_setting(username, params)
        elif operation == 'discover_settings':
            return _handle_discover_settings(params)
        elif operation == 'reset_setting':
            return _handle_reset_setting(username, params)
        elif operation == 'export_config':
            return _handle_export_config(username, params)
        elif operation == 'import_config':
            return _handle_import_config(username, params)
        else:
            # Default to view_settings for unknown operations
            return _handle_view_settings(username, params)
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Config operation failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_view_settings(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle viewing current settings with user overrides"""
    try:
        # Discover all available settings using manager directly
        manager = ApplicationSettingsManager()
        settings_definitions = manager.discover_settings()
        
        # Get user-specific settings (merged with defaults)
        if username:
            user_settings = get_user_settings(username)
        else:
            # Use settings manager to get defaults
            manager = ApplicationSettingsManager()
            user_settings = manager.get_default_settings()
        
        # Organize settings by section for display
        settings_by_section = manager.get_settings_by_section()
        
        return {
            "success": True,
            "operation": "view_settings",
            "user": {
                "username": username,
                "has_overrides": bool(username)
            },
            "settings": user_settings,
            "settings_definitions": {name: {
                "name": setting.name,
                "description": setting.description,
                "type": setting.type,
                "default": setting.default,
                "options": setting.options,
                "ui_metadata": setting.ui_metadata
            } for name, setting in settings_definitions.items()},
            "sections": settings_by_section,
            "total_settings": len(settings_definitions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve settings: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_update_setting(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle updating a user setting with automatic JSON file management"""
    if not username:
        return {
            "success": False,
            "error": "User must be logged in to update settings",
            "timestamp": datetime.now().isoformat()
        }
    
    if not params or 'setting_name' not in params or 'value' not in params:
        return {
            "success": False,
            "error": "Missing required parameters: setting_name and value",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        setting_name = params['setting_name']
        value = params['value']
        
        # Validate setting exists and value is valid
        manager = ApplicationSettingsManager()
        if not manager.validate_setting_value(setting_name, value):
            return {
                "success": False,
                "error": f"Invalid value '{value}' for setting '{setting_name}'",
                "timestamp": datetime.now().isoformat()
            }
        
        # Update user setting (automatic JSON file management via User ID" / "Username)
        success = update_user_setting(username, setting_name, value)
        
        if success:
            # Clear relevant caches
            _clear_config_caches(username)
            
            return {
                "success": True,
                "operation": "update_setting",
                "setting_name": setting_name,
                "new_value": value,
                "user": username,
                "message": f"Setting '{setting_name}' updated successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"Failed to update setting '{setting_name}'",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Update setting failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_discover_settings(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle discovering all available settings"""
    try:
        # Force refresh if requested
        force_refresh = params.get('force_refresh', False) if params else False
        
        # Discover settings using settings_manager
        manager = ApplicationSettingsManager()
        settings_definitions = manager.discover_settings(force_refresh=force_refresh)
        
        # Get settings organized by section
        settings_by_section = manager.get_settings_by_section()
        
        return {
            "success": True,
            "operation": "discover_settings",
            "settings_definitions": {name: {
                "name": setting.name,
                "description": setting.description,
                "type": setting.type,
                "default": setting.default,
                "options": setting.options,
                "source": setting.source,
                "fallback_options": setting.fallback_options,
                "ui_metadata": setting.ui_metadata
            } for name, setting in settings_definitions.items()},
            "sections": settings_by_section,
            "total_settings": len(settings_definitions),
            "force_refresh": force_refresh,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Settings discovery failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_reset_setting(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle resetting a setting to its default value"""
    if not username:
        return {
            "success": False,
            "error": "User must be logged in to reset settings",
            "timestamp": datetime.now().isoformat()
        }
    
    if not params or 'setting_name' not in params:
        return {
            "success": False,
            "error": "Missing required parameter: setting_name",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        setting_name = params['setting_name']
        
        # Get default value
        manager = ApplicationSettingsManager()
        settings_definitions = manager.discover_settings()
        if setting_name not in settings_definitions:
            return {
                "success": False,
                "error": f"Setting '{setting_name}' not found",
                "timestamp": datetime.now().isoformat()
            }
        
        default_value = settings_definitions[setting_name].default
        
        # Update to default value (this will remove the setting from user file if it matches default)
        success = update_user_setting(username, setting_name, default_value)
        
        if success:
            # Clear relevant caches
            _clear_config_caches(username)
            
            return {
                "success": True,
                "operation": "reset_setting",
                "setting_name": setting_name,
                "default_value": default_value,
                "user": username,
                "message": f"Setting '{setting_name}' reset to default value",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"Failed to reset setting '{setting_name}'",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Reset setting failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_export_config(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle exporting user configuration"""
    if not username:
        return {
            "success": False,
            "error": "User must be logged in to export configuration",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # Get user settings
        user_settings = get_user_settings(username)
        
        # Get settings definitions for context
        manager = ApplicationSettingsManager()
        settings_definitions = manager.discover_settings()
        
        # Create export data
        export_data = {
            "export_info": {
                "username": username,
                "export_date": datetime.now().isoformat(),
                "settings_count": len(user_settings)
            },
            "user_settings": user_settings,
            "settings_metadata": {name: {
                "description": setting.description,
                "type": setting.type,
                "default": setting.default
            } for name, setting in settings_definitions.items() if name in user_settings}
        }
        
        return {
            "success": True,
            "operation": "export_config",
            "user": username,
            "export_data": export_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Export configuration failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_import_config(username: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle importing user configuration"""
    if not username:
        return {
            "success": False,
            "error": "User must be logged in to import configuration",
            "timestamp": datetime.now().isoformat()
        }
    
    if not params or 'config_data' not in params:
        return {
            "success": False,
            "error": "Missing required parameter: config_data",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        config_data = params['config_data']
        user_settings = config_data.get('user_settings', {})
        
        if not user_settings:
            return {
                "success": False,
                "error": "No user settings found in configuration data",
                "timestamp": datetime.now().isoformat()
            }
        
        # Validate and import settings
        manager = ApplicationSettingsManager()
        imported_count = 0
        failed_settings = []
        
        for setting_name, value in user_settings.items():
            if manager.validate_setting_value(setting_name, value):
                success = update_user_setting(username, setting_name, value)
                if success:
                    imported_count += 1
                else:
                    failed_settings.append(setting_name)
            else:
                failed_settings.append(setting_name)
        
        # Clear relevant caches
        _clear_config_caches(username)
        
        return {
            "success": True,
            "operation": "import_config",
            "user": username,
            "imported_count": imported_count,
            "failed_settings": failed_settings,
            "message": f"Successfully imported {imported_count} settings",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Import configuration failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _clear_config_caches(username: str = None):
    """Clear relevant caches after settings updates"""
    cache_keys = [
        "settings_discovery",
        "default_settings",
        "settings_by_section"
    ]
    
    if username:
        cache_keys.append(f"user_settings|{username}")
    
    for key in cache_keys:
        cache.clear_cache(key)

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_config(params)