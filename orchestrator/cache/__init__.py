"""
Mao Cache Tools
Universal caching infrastructure for modular tools
"""

from .cache_system import (
    CacheManager,
    CacheEntry
)

__all__ = [
    'CacheManager',
    'CacheEntry'
]

# Version info
__version__ = "4.0.0"
__description__ = "Universal caching system for modular orchestration tools" 