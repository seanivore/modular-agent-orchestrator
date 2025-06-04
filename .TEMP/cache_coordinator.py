"""
Cache Coordinator
Routes cache operations to appropriate cache system based on use case
"""

import os
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add paths for cache systems
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'orchestrator'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'cache_tools'))

from hybrid_cache import HybridCacheManager
from universal_cache import UniversalCache, CacheFingerprint


class CacheCoordinator:
    """
    Traffic director for SFA v4 cache systems
    Routes workflow operations to hybrid cache, tool operations to universal cache
    """
    
    def __init__(self):
        """Initialize both cache systems"""
        self.hybrid_cache = HybridCacheManager()
        self.universal_cache = UniversalCache()
        
    # ==========================================
    # TOOL RESULT CACHING (Universal Cache)
    # ==========================================
    
    def cache_tool_result(self, tool_name: str, params: Dict, result: Dict, 
                         model: str, estimated_cost: float = 0.0, 
                         ttl_hours: int = 24) -> bool:
        """
        Cache tool execution result
        Routes to Universal Cache for tool-specific optimization
        
        Args:
            tool_name: Name of the tool (brave_search, text_editor, etc.)
            params: Tool parameters used
            result: Tool execution result
            model: Model used for execution
            estimated_cost: Cost of the operation
            ttl_hours: Time to live in hours
            
        Returns:
            bool: Success status
        """
        try:
            # Generate fingerprint for tool operation
            fingerprint = CacheFingerprint.generate_fingerprint(
                operation=f"tool_{tool_name}",
                params=params,
                model=model,
                context={}
            )
            
            # Cache in universal cache
            return self.universal_cache.set(
                fingerprint=fingerprint,
                data=result,
                ttl_hours=ttl_hours,
                estimated_cost=estimated_cost
            )
            
        except Exception as e:
            print(f"Error caching tool result: {e}")
            return False
    
    def get_cached_tool_result(self, tool_name: str, params: Dict, 
                              model: str) -> Optional[Dict]:
        """
        Retrieve cached tool result
        
        Args:
            tool_name: Name of the tool
            params: Tool parameters
            model: Model identifier
            
        Returns:
            Cached result or None if not found
        """
        try:
            # Generate same fingerprint
            fingerprint = CacheFingerprint.generate_fingerprint(
                operation=f"tool_{tool_name}",
                params=params,
                model=model,
                context={}
            )
            
            return self.universal_cache.get(fingerprint)
            
        except Exception as e:
            print(f"Error retrieving cached tool result: {e}")
            return None
    
    # ==========================================
    # WORKFLOW STATE CACHING (Hybrid Cache)
    # ==========================================
    
    def cache_workflow_state(self, workflow_id: str, state_data: Dict, 
                           anthropic_client=None) -> bool:
        """
        Cache workflow state for handoffs between agents
        Routes to Hybrid Cache for orchestrator workflow management
        
        Args:
            workflow_id: Unique workflow identifier
            state_data: Workflow state to cache
            anthropic_client: Anthropic client for Files API
            
        Returns:
            bool: Success status
        """
        try:
            filename = f"workflow_{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            return self.hybrid_cache.smart_cache_decision(
                content=state_data,
                content_type="workflow_state",
                filename=filename,
                client=anthropic_client
            )
            
        except Exception as e:
            print(f"Error caching workflow state: {e}")
            return False
    
    def get_cached_workflow_state(self, workflow_id: str) -> Optional[Dict]:
        """
        Retrieve cached workflow state
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Cached workflow state or None if not found
        """
        try:
            # Try to get from hybrid cache
            # Note: This would need the specific file_id from Files API
            # For now, return None - this needs integration with workflow tracking
            return None
            
        except Exception as e:
            print(f"Error retrieving workflow state: {e}")
            return None
    
    def cache_agent_handoff(self, from_agent: str, to_agent: str, 
                           handoff_data: Dict, anthropic_client=None) -> bool:
        """
        Cache agent handoff data
        Routes to Hybrid Cache for inter-agent communication
        
        Args:
            from_agent: Source agent identifier
            to_agent: Target agent identifier  
            handoff_data: Data being handed off
            anthropic_client: Anthropic client for Files API
            
        Returns:
            bool: Success status
        """
        try:
            filename = f"handoff_{from_agent}_to_{to_agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            return self.hybrid_cache.smart_cache_decision(
                content=handoff_data,
                content_type="agent_handoff",
                filename=filename,
                client=anthropic_client
            )
            
        except Exception as e:
            print(f"Error caching agent handoff: {e}")
            return False
    
    # ==========================================
    # GOAL ANALYSIS CACHING (Hybrid Cache)
    # ==========================================
    
    def cache_goal_analysis(self, goal: str, analysis: Dict, 
                           cache_type: str = "goal_analysis") -> bool:
        """
        Cache goal analysis results
        Routes to Hybrid Cache for orchestrator analysis
        
        Args:
            goal: User goal/prompt
            analysis: Analysis result
            cache_type: Type of analysis
            
        Returns:
            bool: Success status
        """
        try:
            return self.hybrid_cache.cache_content_analysis(
                content=goal,
                analysis=analysis,
                cache_type=cache_type
            )
            
        except Exception as e:
            print(f"Error caching goal analysis: {e}")
            return False
    
    def get_cached_goal_analysis(self, goal: str, 
                                cache_type: str = "goal_analysis") -> Optional[Dict]:
        """
        Retrieve cached goal analysis
        
        Args:
            goal: User goal/prompt
            cache_type: Type of analysis
            
        Returns:
            Cached analysis or None if not found
        """
        try:
            return self.hybrid_cache.get_cached_analysis(
                content=goal,
                cache_type=cache_type
            )
            
        except Exception as e:
            print(f"Error retrieving goal analysis: {e}")
            return None
    
    # ==========================================
    # CACHE MANAGEMENT & STATISTICS
    # ==========================================
    
    def get_cache_stats(self) -> Dict:
        """
        Get statistics from both cache systems
        
        Returns:
            Combined cache statistics
        """
        try:
            universal_stats = self.universal_cache.get_cache_stats()
            
            # Hybrid cache doesn't have built-in stats, so we'll create basic ones
            hybrid_stats = {
                "type": "hybrid_cache",
                "status": "active"
            }
            
            return {
                "universal_cache": universal_stats,
                "hybrid_cache": hybrid_stats,
                "coordinator_status": "active",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "coordinator_status": "error",
                "last_updated": datetime.now().isoformat()
            }
    
    def cleanup_expired_cache(self) -> Dict:
        """
        Clean up expired cache entries in both systems
        
        Returns:
            Cleanup results
        """
        try:
            # Universal cache has built-in cleanup
            universal_cleanup = self.universal_cache.cleanup_expired()
            
            # Hybrid cache cleanup would need to be implemented
            hybrid_cleanup = {"status": "no_cleanup_implemented"}
            
            return {
                "universal_cache_cleanup": universal_cleanup,
                "hybrid_cache_cleanup": hybrid_cleanup,
                "cleanup_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "cleanup_timestamp": datetime.now().isoformat()
            }


# ==========================================
# CONVENIENCE FUNCTIONS
# ==========================================

# Global coordinator instance
_coordinator = None

def get_cache_coordinator() -> CacheCoordinator:
    """Get global cache coordinator instance"""
    global _coordinator
    if _coordinator is None:
        _coordinator = CacheCoordinator()
    return _coordinator

def cache_tool_result(tool_name: str, params: Dict, result: Dict, 
                     model: str, **kwargs) -> bool:
    """Convenience function for caching tool results"""
    return get_cache_coordinator().cache_tool_result(tool_name, params, result, model, **kwargs)

def get_cached_tool_result(tool_name: str, params: Dict, model: str) -> Optional[Dict]:
    """Convenience function for retrieving cached tool results"""
    return get_cache_coordinator().get_cached_tool_result(tool_name, params, model)

def cache_workflow_state(workflow_id: str, state_data: Dict, **kwargs) -> bool:
    """Convenience function for caching workflow state"""
    return get_cache_coordinator().cache_workflow_state(workflow_id, state_data, **kwargs)

def cache_goal_analysis(goal: str, analysis: Dict, **kwargs) -> bool:
    """Convenience function for caching goal analysis"""
    return get_cache_coordinator().cache_goal_analysis(goal, analysis, **kwargs)

def get_cached_goal_analysis(goal: str, **kwargs) -> Optional[Dict]:
    """Convenience function for retrieving cached goal analysis"""
    return get_cache_coordinator().get_cached_goal_analysis(goal, **kwargs) 