"""
Set Model CLI Command - Core Logic
Set user's favorite model preference via settings_manager.py
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="set_model", return_dict=True)
def execute_set_model(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main set-model command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI" / "app input
        Expected params:
        - model_name: Target model name to set as favorite
        - username: User's username (for settings update)
        
    Returns:
        Standardized result dictionary
    """
    # Validate required parameters
    if not params:
        return {
            "success": False,
            "error": "Missing parameters. Usage: mao set-model model-name",
            "timestamp": datetime.now().isoformat()
        }
    
    model_name = params.get("model_name")
    username = params.get("username")
    
    if not model_name:
        return {
            "success": False,
            "error": "Model name required. Usage: mao set-model model-name",
            "timestamp": datetime.now().isoformat()
        }
    
    if not username:
        return {
            "success": False,
            "error": "Username required for settings update",
            "timestamp": datetime.now().isoformat()
        }
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "set_model")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Only cache successful results for a short duration (1 minute)
    if result.get("success"):
        cache.cache_content_analysis(cache_key, json.dumps(result), "set_model")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Local file operations with model validation
    return 0.001

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including system state"""
    base_key = f"set_model|{str(params) if params else 'none'}"
    
    # Add models directory state fingerprint for validation accuracy
    models_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "models"
    if models_dir.exists():
        dir_stat = models_dir.stat()
        model_count = len([f for f in models_dir.iterdir() if f.is_file() and f.suffix == '.json'])
        dir_fingerprint = f"{dir_stat.st_mtime}|{model_count}"
        base_key += f"|models:{hashlib.md5(dir_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core set-model command logic implementation"""
    try:
        model_name = params.get("model_name")
        username = params.get("username")
        
        # Get current user settings to show before" / "after
        current_settings = _get_current_user_settings(username)
        current_model = current_settings.get("favorite_model", "Not set")
        
        # Validate that the model exists
        if not _validate_model_exists(model_name):
            available_models = _get_available_models()
            return {
                "success": False,
                "error": f"Model '{model_name}' not found",
                "available_models": list(available_models.keys()),
                "current_model": current_model,
                "timestamp": datetime.now().isoformat()
            }
        
        # Update user setting via settings_manager
        success = _update_user_model_setting(username, model_name)
        
        if success:
            return {
                "success": True,
                "message": f"Successfully set favorite model to '{model_name}'",
                "previous_model": current_model,
                "new_model": model_name,
                "username": username,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Failed to update user settings",
                "current_model": current_model,
                "attempted_model": model_name,
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to set model preference: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _get_current_user_settings(username: str) -> Dict[str, Any]:
    """Get current user settings via settings_manager"""
    try:
        from orchestrator.settings_manager import ApplicationSettingsManager
        settings_manager = ApplicationSettingsManager()
        return settings_manager.get_user_settings(username)
    except Exception:
        return {}

def _validate_model_exists(model_name: str) -> bool:
    """Validate that the specified model exists"""
    try:
        # Primary: Use ModelManager for proper validation
        from orchestrator.manager_models import ModelManager
        model_manager = ModelManager()
        available_models = model_manager.get_available_models()
        
        # Check if model exists in available models
        return model_name in available_models
        
    except Exception:
        # Fallback: Direct directory check
        models_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "models"
        for model_file in models_dir.iterdir():
            if model_file.is_file() and model_file.suffix == '.json':
                try:
                    with open(model_file, 'r') as f:
                        model_config = json.load(f)
                        if model_config.get("name") == model_name or model_file.stem == model_name:
                            return True
                except:
                    continue
        return False

def _get_available_models() -> Dict[str, Dict[str, Any]]:
    """Get list of available models for error display"""
    try:
        from orchestrator.manager_models import ModelManager
        model_manager = ModelManager()
        return model_manager.get_available_models()
    except Exception:
        # Fallback: Direct directory scanning
        models = {}
        models_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "models"
        for model_file in models_dir.iterdir():
            if model_file.is_file() and model_file.suffix == '.json':
                try:
                    with open(model_file, 'r') as f:
                        model_config = json.load(f)
                        model_name = model_config.get("name", model_file.stem)
                        models[model_name] = model_config
                except:
                    continue
        return models

def _update_user_model_setting(username: str, model_name: str) -> bool:
    """Update user's favorite model setting via settings_manager"""
    try:
        from orchestrator.settings_manager import ApplicationSettingsManager
        settings_manager = ApplicationSettingsManager()
        
        # Update the favorite_model setting
        return settings_manager.update_user_setting(username, "favorite_model", model_name)
        
    except Exception:
        return False

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_set_model(params)