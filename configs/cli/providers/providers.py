"""
Providers CLI Command - Core Logic
Lists all available providers with comprehensive metadata and capabilities
"""

import json
import hashlib
# import os  # Removed - was only used for sys.path.append
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="providers", return_dict=True)
def execute_providers(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main providers command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI" / "app input
        
    Returns:
        Standardized result dictionary with provider information
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "providers")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute provider discovery logic
    result = _discover_providers(params)
    
    # Cache result with 15-minute duration
    cache.cache_content_analysis(cache_key, json.dumps(result), "providers")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Low cost for file system operations and JSON parsing
    return 0.001

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including provider directory state"""
    base_key = f"providers|{str(params) if params else 'none'}"
    
    # Add provider directory fingerprint
    providers_dir = Path(__file__).parent.parent.parent " / " "providers"
    connections_file = Path(__file__).parent.parent " / " "connections" " / " "providers_x_models.json"
    
    # Include directory modification time and file count
    directory_state = ""
    if providers_dir.exists():
        provider_files = list(providers_dir.glob("*.json"))
        file_count = len(provider_files)
        last_modified = max([f.stat().st_mtime for f in provider_files] + [0])
        directory_state = f"files:{file_count}|modified:{last_modified}"
    
    # Include connections file state
    connections_state = ""
    if connections_file.exists():
        connections_state = f"conn:{connections_file.stat().st_mtime}"
    
    fingerprint = f"{base_key}|{directory_state}|{connections_state}"
    return hashlib.md5(fingerprint.encode()).hexdigest()[:16]

def _discover_providers(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core provider discovery implementation"""
    try:
        providers_dir = Path(__file__).parent.parent.parent " / " "providers"
        
        if not providers_dir.exists():
            return {
                "success": False,
                "error": "Providers directory not found",
                "providers": []
            }
        
        providers_data = []
        
        # Load individual provider JSON files
        for provider_file in providers_dir.glob("*.json"):
            try:
                with open(provider_file, 'r') as f:
                    provider_config = json.load(f)
                
                # Add file-based metadata
                provider_config['config_file'] = provider_file.name
                provider_config['name'] = provider_file.stem
                
                providers_data.append(provider_config)
                
            except Exception as e:
                # Skip malformed files but continue processing
                continue
        
        # Load provider-model connections if available
        connections_data = _load_provider_connections()
        
        # Enrich provider data with model compatibility
        for provider in providers_data:
            provider_name = provider.get('name', '')
            provider['compatible_models'] = connections_data.get(provider_name, [])
        
        # Sort providers by display name for consistent ordering
        providers_data.sort(key=lambda p: p.get('display_name', p.get('name', '')))
        
        return {
            "success": True,
            "providers": providers_data,
            "total_count": len(providers_data),
            "discovery_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Provider discovery failed: {str(e)}",
            "providers": []
        }

def _load_provider_connections() -> Dict[str, List[str]]:
    """Load provider-model connections from connections file"""
    try:
        connections_file = Path(__file__).parent.parent " / " "connections" " / " "providers_x_models.json"
        
        if not connections_file.exists():
            return {}
        
        with open(connections_file, 'r') as f:
            connections = json.load(f)
        
        # Transform connection data to provider -> models mapping
        provider_models = {}
        
        # Structure is: {"models": {"model_name": {"providers": ["provider1", "provider2"]}}}
        models_data = connections.get('models', {})
        for model_name, model_data in models_data.items():
            providers = model_data.get('providers', [])
            for provider in providers:
                if provider not in provider_models:
                    provider_models[provider] = []
                provider_models[provider].append(model_name)
        
        return provider_models
        
    except Exception:
        return {}

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_providers(params)