"""
Memory CLI Command - Core Logic
Store, retrieve, and manage user memories and contextual information
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="memory", return_dict=True)
@retry_with_backoff(max_retries=2, base_delay=1.0)
def execute_memory(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main memory command execution with caching and error handling.
    
    Args:
        params: Command parameters including operation type and data
        
    Returns:
        Standardized result dictionary with memory operation results
    """
    # Validate parameters
    if not params:
        return {
            "success": False,
            "error": "Memory command requires parameters",
            "usage": "Use: " / "memory 'text' to store, /memory --list to view, " / "memory --delete [ID] to remove",
            "timestamp": datetime.now().isoformat()
        }
    
    # Determine operation type
    operation_type = _determine_operation_type(params)
    
    # Check cache first for read operations
    if operation_type in ["retrieve", "list", "suggest"]:
        cache_key = _generate_cache_key(params, operation_type)
        cached_result = cache.get_cached_analysis(cache_key, "memory")
        if cached_result:
            cached_data = json.loads(cached_result)
            cached_data["timestamp"] = datetime.now().isoformat()
            cached_data["from_cache"] = True
            return cached_data
    
    # Execute command logic
    result = _execute_command_logic(params, operation_type)
    
    # Cache result for read operations (5 minutes)
    if result.get("success") and operation_type in ["retrieve", "list", "suggest"]:
        cache_key = _generate_cache_key(params, operation_type)
        cache.cache_content_analysis(cache_key, json.dumps(result), "memory")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Memory operations are generally low-cost with MCP integration.
    """
    if not params:
        return 0.001  # Base cost for simple operations
    
    # Get current user for cost estimation
    try:
        from orchestrator.user_memory_manager import UserMemoryManager
        memory_manager = UserMemoryManager()
        
        operation_type = _determine_operation_type(params)
        
        # Use memory manager cost estimation
        cost_params = {
            "operation": operation_type,
            "memory_count": params.get("limit", 10),
            "query_complexity": len(params.get("query", params.get("content", "")).split()),
            "mcp_operations": 1
        }
        
        return memory_manager.estimate_cost(cost_params)
        
    except Exception:
        # Fallback cost estimation
        operation_type = _determine_operation_type(params)
        
        cost_map = {
            "store": 0.002,     # Higher cost for storage operations
            "retrieve": 0.001,  # Lower cost for retrieval
            "list": 0.001,      # Low cost for listing
            "delete": 0.001,    # Low cost for deletion
            "suggest": 0.003    # Higher cost for AI suggestions
        }
        
        return cost_map.get(operation_type, 0.001)

def _determine_operation_type(params: Dict[str, Any]) -> str:
    """Determine the memory operation type from parameters"""
    # Check for explicit flags
    if params.get("list") or params.get("--list"):
        return "list"
    elif params.get("delete") or params.get("--delete"):
        return "delete"
    elif params.get("suggest") or params.get("--suggest"):
        return "suggest"
    elif params.get("query") or params.get("--query"):
        return "retrieve"
    elif params.get("content") or params.get("message"):
        return "store"
    else:
        # Default to store for simple text input
        return "store"

def _generate_cache_key(params: Dict[str, Any], operation_type: str) -> str:
    """Generate fingerprinted cache key for memory operations"""
    # Get current user for user-specific caching
    try:
        from orchestrator.username_manager import get_session_user
        user = get_session_user()
        user_id = user.get("user_id", "anonymous") if user else "anonymous"
    except Exception:
        user_id = "anonymous"
    
    # Create operation-specific cache key
    key_parts = [f"memory_{operation_type}", f"user_{user_id}"]
    
    if operation_type == "retrieve":
        query = params.get("query", "")
        key_parts.append(f"query_{hashlib.md5(query.encode()).hexdigest()[:8]}")
    elif operation_type == "list":
        category = params.get("category", "all")
        limit = params.get("limit", 10)
        key_parts.append(f"category_{category}_limit_{limit}")
    elif operation_type == "suggest":
        context = params.get("context", "")
        key_parts.append(f"context_{hashlib.md5(context.encode()).hexdigest()[:8]}")
    
    cache_key = "|".join(key_parts)
    return hashlib.md5(cache_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any], operation_type: str) -> Dict[str, Any]:
    """Core memory command logic implementation"""
    try:
        # Initialize user memory manager
        from orchestrator.user_memory_manager import UserMemoryManager
        memory_manager = UserMemoryManager()
        
        # Get current user
        from orchestrator.username_manager import get_session_user
        user = get_session_user()
        
        if not user:
            return {
                "success": False,
                "error": "No user logged in. Please login first to use memory commands.",
                "timestamp": datetime.now().isoformat()
            }
        
        user_id = user.get("user_id")
        
        # Execute operation based on type
        if operation_type == "store":
            content = params.get("content") or params.get("message", "")
            if not content:
                return {
                    "success": False,
                    "error": "Memory store requires content to save",
                    "timestamp": datetime.now().isoformat()
                }
            
            result = memory_manager.store_memory(
                user_id=user_id,
                content=content,
                category=params.get("category"),
                tags=params.get("tags"),
                priority=params.get("priority", "medium")
            )
            
            return {
                "success": True,
                "operation": "store",
                "memory_id": result.get("memory_id"),
                "content": content,
                "category": result.get("category"),
                "message": "Memory stored successfully",
                "timestamp": datetime.now().isoformat()
            }
        
        elif operation_type == "retrieve":
            query = params.get("query", "")
            if not query:
                return {
                    "success": False,
                    "error": "Memory retrieve requires a search query",
                    "timestamp": datetime.now().isoformat()
                }
            
            memories = memory_manager.retrieve_memories(
                user_id=user_id,
                query=query,
                category=params.get("category"),
                limit=params.get("limit", 10)
            )
            
            return {
                "success": True,
                "operation": "retrieve",
                "query": query,
                "memories": memories,
                "total_found": len(memories),
                "timestamp": datetime.now().isoformat()
            }
        
        elif operation_type == "list":
            memories = memory_manager.list_memories(
                user_id=user_id,
                category=params.get("category"),
                limit=params.get("limit", 20),
                sort_by=params.get("sort_by", "created_at")
            )
            
            return {
                "success": True,
                "operation": "list",
                "memories": memories,
                "total_memories": len(memories),
                "category": params.get("category", "all"),
                "timestamp": datetime.now().isoformat()
            }
        
        elif operation_type == "delete":
            memory_id = params.get("memory_id") or params.get("--delete")
            if not memory_id:
                return {
                    "success": False,
                    "error": "Memory delete requires a memory ID",
                    "usage": "Use: " / "memory --delete [memory_id]",
                    "timestamp": datetime.now().isoformat()
                }
            
            result = memory_manager.delete_memory(user_id=user_id, memory_id=memory_id)
            
            return {
                "success": True,
                "operation": "delete",
                "memory_id": memory_id,
                "message": "Memory deleted successfully",
                "timestamp": datetime.now().isoformat()
            }
        
        elif operation_type == "suggest":
            context = params.get("context", "")
            if not context:
                return {
                    "success": False,
                    "error": "Memory suggest requires context for suggestions",
                    "timestamp": datetime.now().isoformat()
                }
            
            suggestions = memory_manager.suggest_contextual(
                user_id=user_id,
                context=context,
                limit=params.get("limit", 5),
                relevance_threshold=params.get("relevance_threshold", 0.7)
            )
            
            return {
                "success": True,
                "operation": "suggest",
                "context": context,
                "suggestions": suggestions,
                "total_suggestions": len(suggestions),
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown memory operation: {operation_type}",
                "available_operations": ["store", "retrieve", "list", "delete", "suggest"],
                "timestamp": datetime.now().isoformat()
            }
            
    except ImportError as e:
        return {
            "success": False,
            "error": f"Memory system not available: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Memory command execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_memory(params)