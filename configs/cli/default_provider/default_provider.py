"""
Default Provider CLI Command - Core Logic
Set default provider via settings_manager.py integration with user config JSON updates
"""

import json
import hashlib
# import os  # Removed - was only used for sys.path.append
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError
from orchestrator.settings_manager import ApplicationSettingsManager, get_user_settings, update_user_setting, discover_settings
from orchestrator.username_manager import get_session_user

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="default_provider", return_dict=True)
def execute_default_provider(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main default-provider command execution with settings management and provider validation.
    
    Integrates with settings_manager.py for user config updates and validates
    provider availability before setting as default.
    
    Args:
        params: Command parameters including 'provider_name' for the desired default provider
        
    Returns:
        Standardized result dictionary with success status and provider information
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "default_provider")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 5 minutes (settings change moderately frequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "default_provider")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure - essentially free for local file operations.
    """
    # Settings operations are local file operations with minimal processing
    return 0.0001

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including user context and provider state"""
    base_key = f"default_provider|{str(params) if params else 'none'}"
    
    # Add user context for cache differentiation
    try:
        current_user = get_session_user()
        if current_user:
            base_key += f"|{current_user.get('username', 'anonymous')}"
    except:
        base_key += "|anonymous"
    
    # Add system state fingerprint for provider availability
    providers_dir = Path("./configs/providers / ")
    if providers_dir.exists():
        provider_files = list(providers_dir.glob("*.json"))
        provider_count = len(provider_files)
        base_key += f"|providers_count:{provider_count}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core command logic for setting default provider"""
    
    # Validate input parameters
    if not params or not params.get('provider_name'):
        return {
            "success": False,
            "error": "Provider name is required. Usage: mao default-provider <provider-name>",
            "current_provider": _get_current_default_provider()
        }
    
    provider_name = params['provider_name'].strip()
    
    # Get current user context
    try:
        current_user = get_session_user()
        if not current_user or not current_user.get('username'):
            return {
                "success": False,
                "error": "User session required. Please login first with 'mao login'",
                "provider_name": provider_name
            }
        
        username = current_user['username']
    except Exception as e:
        return {
            "success": False,
            "error": "Could not get user session. Please login first with 'mao login'",
            "provider_name": provider_name
        }
    
    # Validate provider exists and is available
    validation_result = _validate_provider(provider_name)
    if not validation_result['valid']:
        return {
            "success": False,
            "error": validation_result['error'],
            "provider_name": provider_name,
            "available_providers": validation_result.get('available_providers', [])
        }
    
    # Get current default provider for comparison
    current_provider = _get_current_user_provider(username)
    
    # Update user setting via settings_manager
    try:
        settings_manager = ApplicationSettingsManager()
        success = settings_manager.update_user_setting(username, 'default_provider', provider_name)
        
        if success:
            return {
                "success": True,
                "message": f"Default provider updated successfully",
                "previous_provider": current_provider,
                "new_provider": provider_name,
                "username": username,
                "provider_details": validation_result.get('provider_details', {})
            }
        else:
            return {
                "success": False,
                "error": "Failed to update user settings. Please try again.",
                "provider_name": provider_name,
                "current_provider": current_provider
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Settings update failed: {str(e)}",
            "provider_name": provider_name,
            "current_provider": current_provider
        }

def _validate_provider(provider_name: str) -> Dict[str, Any]:
    """Validate that the provider exists and is available"""
    
    # Get settings definition for provider validation
    try:
        settings_manager = ApplicationSettingsManager()
        settings = settings_manager.discover_settings()
        
        if 'default_provider' in settings:
            setting_def = settings['default_provider']
            
            # Check against fallback options first
            if setting_def.fallback_options and provider_name in setting_def.fallback_options:
                return {
                    "valid": True,
                    "provider_details": {"name": provider_name, "source": "fallback_options"}
                }
            
            # For dynamic provider sources, check actual provider files
            if setting_def.source == "dynamic_provider_list":
                available_providers = _get_available_providers()
                
                if provider_name in available_providers:
                    return {
                        "valid": True,
                        "provider_details": available_providers[provider_name]
                    }
                else:
                    return {
                        "valid": False,
                        "error": f"Provider '{provider_name}' not found. Available providers: {', '.join(available_providers.keys())}",
                        "available_providers": list(available_providers.keys())
                    }
        
        return {
            "valid": False,
            "error": "Default provider setting not found in system configuration",
            "available_providers": []
        }
        
    except Exception as e:
        return {
            "valid": False,
            "error": f"Provider validation failed: {str(e)}",
            "available_providers": []
        }

def _get_available_providers() -> Dict[str, Dict[str, Any]]:
    """Get list of available providers from provider JSON files"""
    providers = {}
    providers_dir = Path("./configs/providers / ")
    
    if not providers_dir.exists():
        return providers
    
    for provider_file in providers_dir.glob("provider_*.json"):
        try:
            with open(provider_file, 'r') as f:
                provider_data = json.load(f)
                
            # Extract provider name and metadata
            provider_name = provider_data.get('name', provider_file.stem.replace('provider_', ''))
            display_name = provider_data.get('display_name', provider_name)
            
            providers[provider_name] = {
                "name": provider_name,
                "display_name": display_name,
                "description": provider_data.get('description', ''),
                "file_path": str(provider_file)
            }
            
        except Exception:
            continue  # Skip malformed files
    
    return providers

def _get_current_default_provider() -> str:
    """Get the system default provider from settings"""
    try:
        settings_manager = ApplicationSettingsManager()
        defaults = settings_manager.get_default_settings()
        return defaults.get('default_provider', 'anthropic direct')
    except:
        return 'anthropic direct'

def _get_current_user_provider(username: str) -> str:
    """Get the current user's default provider setting"""
    try:
        settings_manager = ApplicationSettingsManager()
        user_settings = settings_manager.get_user_settings(username)
        return user_settings.get('default_provider', _get_current_default_provider())
    except:
        return _get_current_default_provider()

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_default_provider(params)