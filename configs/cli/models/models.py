"""
Models CLI Command - Core Logic
Discovers and lists all available models with display names and metadata
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

@handle_errors(operation_name="models", return_dict=True)
def execute_models(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main models command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI" / "app input
        
    Returns:
        Standardized result dictionary with model data
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "models")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 10 minutes (models change less frequently than commands)
    cache.cache_content_analysis(cache_key, json.dumps(result), "models")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # API message exchange with potentially large model list response
    return 0.002

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including models directory state"""
    base_key = f"models|{str(params) if params else 'none'}"
    
    # Add models directory state fingerprint for cache invalidation
    models_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "models"
    if models_dir.exists():
        # Include directory modification time and model count
        dir_stat = models_dir.stat()
        model_files = [f for f in models_dir.iterdir() if f.is_file() and f.suffix == '.json']
        model_count = len(model_files)
        
        # Include modification times of model JSON files for granular invalidation
        json_mod_times = []
        for model_file in model_files:
            if model_file.exists():
                json_mod_times.append(model_file.stat().st_mtime)
        
        # Create fingerprint from directory and file state
        dir_fingerprint = f"{dir_stat.st_mtime}|{model_count}|{sorted(json_mod_times)}"
        base_key += f"|dir:{hashlib.md5(dir_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core models command logic implementation"""
    try:
        # Discover all models using manager integration
        models = _discover_models()
        
        # Return raw model data for Claude to organize naturally
        return {
            "success": True,
            "models": models,
            "total_models": len(models),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to discover models: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _discover_models() -> Dict[str, Dict[str, Any]]:
    """Discover all models using ModelManager integration"""
    try:
        # Primary: Use ModelManager for proper model discovery
        from orchestrator.manager_models import ModelManager
        model_manager = ModelManager()
        
        # Get all available models using existing discovery
        models_data = model_manager.get_available_models()
        
        return models_data
        
    except Exception as e:
        # Fallback: Direct directory scanning if ModelManager fails
        models = {}
        models_dir = Path(__file__).parent.parent.parent " / " "configs" " / " "models"
        
        for model_file in models_dir.iterdir():
            if not model_file.is_file() or model_file.suffix != '.json':
                continue
                
            try:
                with open(model_file, 'r') as f:
                    model_config = json.load(f)
                    
                    model_name = model_config.get("name", model_file.stem)
                    models[model_name] = model_config
                    
            except (json.JSONDecodeError, KeyError) as e:
                # Skip malformed files but don't break entire models listing
                continue
        
        return models

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_models(params)
