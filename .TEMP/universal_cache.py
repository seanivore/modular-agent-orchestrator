"""
SFA v4.0.0 Universal Cache Fingerprinting System
Shared caching infrastructure for all modular tools
"""

import hashlib
import json
import os
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import pickle

class CacheFingerprint:
    """Generate unique fingerprints for caching operations"""
    
    @staticmethod
    def generate_fingerprint(operation: str, params: Dict[str, Any], 
                           model: str = None, context: str = None) -> str:
        """
        Generate unique fingerprint for cache key
        
        Args:
            operation: Tool operation name
            params: Operation parameters
            model: Model being used (optional)
            context: Additional context (optional)
            
        Returns:
            Unique fingerprint string
        """
        # Create deterministic hash input
        hash_input = {
            "operation": operation,
            "params": params,
            "model": model,
            "context": context
        }
        
        # Convert to JSON string with sorted keys for consistency
        json_string = json.dumps(hash_input, sort_keys=True, default=str)
        
        # Generate SHA-256 hash
        fingerprint = hashlib.sha256(json_string.encode()).hexdigest()
        
        return f"sfa_v4_{operation}_{fingerprint[:16]}"
    
    @staticmethod
    def generate_model_tool_key(tool_name: str, model: str, operation: str = None) -> str:
        """
        Generate key for model-tool mapping cache
        
        Args:
            tool_name: Name of the tool
            model: Model identifier
            operation: Specific operation (optional)
            
        Returns:
            Model-tool mapping key
        """
        key_parts = [tool_name, model]
        if operation:
            key_parts.append(operation)
        
        return "_".join(key_parts).lower()

class UniversalCache:
    """Universal caching system for SFA v4 modular tools"""
    
    def __init__(self, cache_dir: str = None, max_size_mb: int = 100, 
                 default_ttl_hours: int = 24):
        """
        Initialize universal cache
        
        Args:
            cache_dir: Directory for cache files
            max_size_mb: Maximum cache size in MB
            default_ttl_hours: Default time-to-live in hours
        """
        self.cache_dir = Path(cache_dir or os.path.expanduser("~/.sfa_v4_cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = timedelta(hours=default_ttl_hours)
        
        # Cache metadata
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self.metadata = self._load_metadata()
        
        # Performance tracking
        self.stats = {
            "hits": 0,
            "misses": 0,
            "saves": 0,
            "evictions": 0,
            "cost_savings": 0.0
        }
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "entries": {},
            "created": datetime.now().isoformat(),
            "last_cleanup": datetime.now().isoformat()
        }
    
    def _save_metadata(self):
        """Save cache metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache metadata: {e}")
    
    def _get_cache_file_path(self, fingerprint: str) -> Path:
        """Get file path for cache entry"""
        return self.cache_dir / f"{fingerprint}.cache"
    
    def _is_expired(self, entry_metadata: Dict[str, Any]) -> bool:
        """Check if cache entry is expired"""
        created_time = datetime.fromisoformat(entry_metadata["created"])
        ttl = timedelta(seconds=entry_metadata.get("ttl_seconds", self.default_ttl.total_seconds()))
        
        return datetime.now() > created_time + ttl
    
    def get(self, fingerprint: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached result
        
        Args:
            fingerprint: Cache fingerprint
            
        Returns:
            Cached result or None if not found/expired
        """
        # Check metadata
        if fingerprint not in self.metadata["entries"]:
            self.stats["misses"] += 1
            return None
        
        entry_metadata = self.metadata["entries"][fingerprint]
        
        # Check expiration
        if self._is_expired(entry_metadata):
            self.invalidate(fingerprint)
            self.stats["misses"] += 1
            return None
        
        # Load cached data
        cache_file = self._get_cache_file_path(fingerprint)
        if not cache_file.exists():
            # Metadata exists but file doesn't - clean up
            del self.metadata["entries"][fingerprint]
            self._save_metadata()
            self.stats["misses"] += 1
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
            
            # Update access time
            entry_metadata["last_accessed"] = datetime.now().isoformat()
            entry_metadata["access_count"] = entry_metadata.get("access_count", 0) + 1
            self._save_metadata()
            
            # Track cost savings
            estimated_cost = entry_metadata.get("estimated_cost", 0.0)
            self.stats["cost_savings"] += estimated_cost
            self.stats["hits"] += 1
            
            return cached_data
            
        except Exception as e:
            print(f"Warning: Could not load cache entry {fingerprint}: {e}")
            self.invalidate(fingerprint)
            self.stats["misses"] += 1
            return None
    
    def set(self, fingerprint: str, data: Dict[str, Any], 
            ttl_hours: int = None, estimated_cost: float = 0.0,
            operation_metadata: Dict[str, Any] = None):
        """
        Store result in cache
        
        Args:
            fingerprint: Cache fingerprint
            data: Data to cache
            ttl_hours: Time-to-live in hours
            estimated_cost: Estimated cost of operation
            operation_metadata: Additional metadata about the operation
        """
        try:
            # Ensure cache directory exists
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Save data to file
            cache_file = self._get_cache_file_path(fingerprint)
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
            
            # Update metadata
            ttl_seconds = (ttl_hours or (self.default_ttl.total_seconds() / 3600)) * 3600
            
            entry_metadata = {
                "created": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
                "ttl_seconds": ttl_seconds,
                "estimated_cost": estimated_cost,
                "access_count": 0,
                "file_size": cache_file.stat().st_size,
                "operation_metadata": operation_metadata or {}
            }
            
            self.metadata["entries"][fingerprint] = entry_metadata
            self._save_metadata()
            
            self.stats["saves"] += 1
            
            # Check if cleanup is needed
            self._cleanup_if_needed()
            
        except Exception as e:
            print(f"Warning: Could not cache result {fingerprint}: {e}")
    
    def invalidate(self, fingerprint: str):
        """Remove specific cache entry"""
        # Remove file
        cache_file = self._get_cache_file_path(fingerprint)
        if cache_file.exists():
            try:
                cache_file.unlink()
            except:
                pass
        
        # Remove metadata
        if fingerprint in self.metadata["entries"]:
            del self.metadata["entries"][fingerprint]
            self._save_metadata()
    
    def _cleanup_if_needed(self):
        """Clean up cache if size limit exceeded"""
        total_size = sum(
            entry.get("file_size", 0) 
            for entry in self.metadata["entries"].values()
        )
        
        if total_size > self.max_size_bytes:
            self._cleanup_cache()
    
    def _cleanup_cache(self):
        """Clean up expired and least-used cache entries"""
        current_time = datetime.now()
        entries_to_remove = []
        
        # First pass: remove expired entries
        for fingerprint, entry in self.metadata["entries"].items():
            if self._is_expired(entry):
                entries_to_remove.append(fingerprint)
        
        # Remove expired entries
        for fingerprint in entries_to_remove:
            self.invalidate(fingerprint)
            self.stats["evictions"] += 1
        
        # Second pass: if still over limit, remove least-used entries
        total_size = sum(
            entry.get("file_size", 0) 
            for entry in self.metadata["entries"].values()
        )
        
        if total_size > self.max_size_bytes:
            # Sort by access count and last accessed time
            entries_by_usage = sorted(
                self.metadata["entries"].items(),
                key=lambda x: (x[1].get("access_count", 0), x[1].get("last_accessed", ""))
            )
            
            # Remove least-used entries until under limit
            for fingerprint, entry in entries_by_usage:
                if total_size <= self.max_size_bytes:
                    break
                
                file_size = entry.get("file_size", 0)
                self.invalidate(fingerprint)
                total_size -= file_size
                self.stats["evictions"] += 1
        
        # Update cleanup time
        self.metadata["last_cleanup"] = current_time.isoformat()
        self._save_metadata()
    
    def clear_all(self):
        """Clear entire cache"""
        # Remove all cache files
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
            except:
                pass
        
        # Reset metadata
        self.metadata = {
            "entries": {},
            "created": datetime.now().isoformat(),
            "last_cleanup": datetime.now().isoformat()
        }
        self._save_metadata()
        
        # Reset stats
        self.stats = {
            "hits": 0,
            "misses": 0,
            "saves": 0,
            "evictions": 0,
            "cost_savings": 0.0
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        cache_size = sum(
            entry.get("file_size", 0) 
            for entry in self.metadata["entries"].values()
        )
        
        return {
            "hit_rate_percent": round(hit_rate, 2),
            "total_hits": self.stats["hits"],
            "total_misses": self.stats["misses"],
            "total_saves": self.stats["saves"],
            "total_evictions": self.stats["evictions"],
            "estimated_cost_savings": round(self.stats["cost_savings"], 4),
            "cache_entries": len(self.metadata["entries"]),
            "cache_size_mb": round(cache_size / (1024 * 1024), 2),
            "max_size_mb": round(self.max_size_bytes / (1024 * 1024), 2)
        }

class ModelToolMapper:
    """Manages model-tool compatibility and optimization mappings"""
    
    def __init__(self, cache: UniversalCache):
        self.cache = cache
        self.mappings = self._load_default_mappings()
    
    def _load_default_mappings(self) -> Dict[str, Any]:
        """Load default model-tool compatibility mappings"""
        return {
            "tool_compatibility": {
                "web_search": {
                    "optimal_models": ["claude-3-5-sonnet", "gpt-4"],
                    "cost_efficient": ["claude-3-haiku", "gpt-3.5-turbo"],
                    "features_required": ["web_access"]
                },
                "perplexity_search": {
                    "optimal_models": ["claude-3-5-sonnet", "gpt-4"],
                    "cost_efficient": ["claude-3-haiku"],
                    "features_required": ["reasoning", "analysis"]
                },
                "dalle_generate": {
                    "optimal_models": ["dall-e-3", "dall-e-2"],
                    "cost_efficient": ["dall-e-2"],
                    "features_required": ["image_generation"]
                },
                "think": {
                    "optimal_models": ["claude-sonnet-4", "claude-3-5-sonnet", "gpt-4"],
                    "cost_efficient": ["claude-3-haiku", "gpt-3.5-turbo"],
                    "features_required": ["reasoning"]
                },
                "text_editor": {
                    "optimal_models": ["claude-3-5-sonnet", "gpt-4"],
                    "cost_efficient": ["claude-3-haiku", "gpt-3.5-turbo"],
                    "features_required": ["text_processing"]
                },
                "file_operations": {
                    "optimal_models": ["claude-3-5-sonnet", "gpt-4"],
                    "cost_efficient": ["claude-3-haiku", "gpt-3.5-turbo"],
                    "features_required": ["file_processing"]
                },
                "graphic_design": {
                    "optimal_models": ["claude-3-5-sonnet", "gpt-4", "dall-e-3"],
                    "cost_efficient": ["claude-3-haiku", "dall-e-2"],
                    "features_required": ["creative_reasoning", "image_generation"]
                }
            },
            "cost_optimization": {
                "low_complexity": {
                    "recommended_models": ["claude-3-haiku", "gpt-3.5-turbo"],
                    "cost_threshold": 0.01
                },
                "medium_complexity": {
                    "recommended_models": ["claude-3-5-sonnet", "gpt-4"],
                    "cost_threshold": 0.05
                },
                "high_complexity": {
                    "recommended_models": ["claude-sonnet-4", "gpt-4-turbo"],
                    "cost_threshold": 0.10
                }
            }
        }
    
    def get_optimal_model(self, tool_name: str, operation: str = None, 
                         budget_limit: float = None) -> str:
        """
        Get optimal model for tool operation
        
        Args:
            tool_name: Name of the tool
            operation: Specific operation (optional)
            budget_limit: Budget constraint (optional)
            
        Returns:
            Recommended model name
        """
        tool_config = self.mappings["tool_compatibility"].get(tool_name, {})
        
        if budget_limit and budget_limit < 0.02:
            # Low budget - use cost efficient models
            cost_efficient = tool_config.get("cost_efficient", ["claude-3-haiku"])
            return cost_efficient[0]
        else:
            # Normal budget - use optimal models
            optimal = tool_config.get("optimal_models", ["claude-3-5-sonnet"])
            return optimal[0]
    
    def get_cost_estimate(self, tool_name: str, model: str, 
                         complexity: str = "medium") -> float:
        """
        Estimate cost for tool operation with specific model
        
        Args:
            tool_name: Name of the tool
            model: Model to use
            complexity: Operation complexity (low/medium/high)
            
        Returns:
            Estimated cost
        """
        base_costs = {
            "claude-sonnet-4": 0.015,
            "claude-3-5-sonnet": 0.003,
            "claude-3-haiku": 0.00025,
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002,
            "dall-e-3": 0.04,
            "dall-e-2": 0.02
        }
        
        complexity_multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 2.0
        }
        
        base_cost = base_costs.get(model, 0.005)
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        return base_cost * multiplier

# Global cache instance
_global_cache = None

def get_global_cache() -> UniversalCache:
    """Get or create global cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = UniversalCache()
    return _global_cache

def cache_operation(operation: str, ttl_hours: int = 24, 
                   estimated_cost: float = 0.0):
    """
    Decorator for caching tool operations
    
    Args:
        operation: Operation name
        ttl_hours: Time-to-live in hours
        estimated_cost: Estimated cost of operation
        
    Returns:
        Decorated function with caching
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_global_cache()
            
            # Generate fingerprint
            fingerprint = CacheFingerprint.generate_fingerprint(
                operation=operation,
                params=kwargs,
                model=kwargs.get("model"),
                context=kwargs.get("context")
            )
            
            # Try to get from cache
            cached_result = cache.get(fingerprint)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(
                fingerprint=fingerprint,
                data=result,
                ttl_hours=ttl_hours,
                estimated_cost=estimated_cost,
                operation_metadata={
                    "operation": operation,
                    "function": func.__name__
                }
            )
            
            return result
        
        return wrapper
    return decorator 