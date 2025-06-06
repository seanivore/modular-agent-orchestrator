"""
SFA v4.0.0 Cache Tools
Universal caching infrastructure for modular tools
"""

from .universal_cache import (
    UniversalCache,
    CacheFingerprint, 
    ModelToolMapper,
    get_global_cache,
    cache_operation
)

__all__ = [
    'UniversalCache',
    'CacheFingerprint',
    'ModelToolMapper', 
    'get_global_cache',
    'cache_operation'
]

# Version info
__version__ = "4.0.0"
__description__ = "Universal caching system for SFA v4 modular tools" 