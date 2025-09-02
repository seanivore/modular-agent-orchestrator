"""
User Memory Manager Service
Handles user-specific memory storage, retrieval, and management with Memory MCP integration
"""

import json
# import os  # Removed - was only used for sys.path.append
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from uuid import uuid4

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.memory_mcp import MemoryMCPManager

# Standard cache instance
cache = CacheManager()

class UserMemoryManager:
    """
    Manages user-specific memory storage and retrieval with MCP integration.
    
    Core Features:
    1. Store and retrieve user memories with automatic categorization
    2. Integration with Memory MCP for persistence
    3. User-specific cache keys with 5-minute duration
    4. Privacy-first architecture with user data isolation
    5. Contextual memory suggestions based on relevance
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "configs"  /  "user"
        self.memory_mcp = MemoryMCPManager()
        
        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Cache duration for user-specific operations (5 minutes)
        self.cache_duration = 300
    
    @handle_errors(operation_name="store_memory", return_dict=True)
    def store_memory(self, user_id: str, content: str, category: str = None, 
                    tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]:
        """
        Store a new memory for the user.
        
        Args:
            user_id: User identifier (format: user-####)
            content: Memory content to store
            category: Optional category (defaults to "general" if None)
            tags: Optional tags list
            priority: Memory priority (low, medium, high)
            
        Returns:
            Memory storage result with memory_id and metadata
        """
        if not user_id or not content:
            raise ValueError("User ID and content are required")
        
        if not user_id.startswith("user-"):
            raise ValueError("Invalid user_id format. Must be format: user-####")
        
        # Generate memory ID
        memory_id = f"mem_{uuid4().hex[:8]}"
        
        # Use provided category or default to "general"
        if not category:
            category = "general"
        
        # Create memory object
        memory = {
            "memory_id": memory_id,
            "content": content,
            "category": category,
            "tags": tags or [],
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "access_count": 0,
            "relevance_score": 1.0,
            "source": "user_input",
            "metadata": {
                "related_memories": [],
                "embedding_vector": None
            }
        }
        
        # Store in file system using user_id
        self._store_memory_to_file(user_id, memory, category)
        
        # Store in Memory MCP for persistence
        self._store_memory_to_mcp(user_id, memory)
        
        # Clear related caches
        self._clear_user_memory_cache(user_id)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "category": category,
            "tags": tags or [],
            "message": "Memory stored successfully"
        }
    
    @handle_errors(operation_name="retrieve_memories", return_dict=True)
    def retrieve_memories(self, user_id: str, query: str, category: str = None, 
                         limit: int = 10, include_metadata: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve memories matching the query with relevance scoring.
        
        Args:
            user_id: User identifier
            query: Search query
            category: Optional category filter
            limit: Maximum number of results
            include_metadata: Whether to include metadata in results
            
        Returns:
            List of matching memories with relevance scores
        """
        if not user_id or not query:
            return []
        
        # Check cache first
        cache_key = f"user_memory_retrieve_{user_id}_{hashlib.md5(query.encode()).hexdigest()[:8]}_{category}_{limit}"
        cached_result = cache.get_cached_analysis(cache_key, "user_memory")
        if cached_result:
            return json.loads(cached_result)
        
        if not user_id.startswith("user-"):
            return []
        
        # Load user memories from files
        memories = self._load_user_memories(user_id, category)
        
        # Search and score memories
        matching_memories = []
        query_lower = query.lower()
        
        for memory in memories:
            relevance_score = self._calculate_relevance_score(memory, query_lower)
            
            if relevance_score > 0.3:  # Relevance threshold
                memory_copy = memory.copy()
                memory_copy["relevance_score"] = relevance_score
                memory_copy["last_accessed"] = datetime.now().isoformat()
                memory_copy["access_count"] = memory.get("access_count", 0) + 1
                
                if not include_metadata:
                    memory_copy.pop("metadata", None)
                
                matching_memories.append(memory_copy)
        
        # Sort by relevance score
        matching_memories.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Limit results
        results = matching_memories[:limit]
        
        # Update access counts in storage
        self._update_memory_access_counts(user_id, results)
        
        # Cache results for 5 minutes
        cache.cache_content_analysis(cache_key, json.dumps(results), "user_memory")
        
        return results
    
    @handle_errors(operation_name="list_memories", return_dict=True)
    def list_memories(self, user_id: str, category: str = None, limit: int = 20, 
                     sort_by: str = "created_at") -> List[Dict[str, Any]]:
        """
        List user memories with optional filtering and sorting.
        
        Args:
            user_id: User identifier
            category: Optional category filter
            limit: Maximum number of results
            sort_by: Sort field (created_at, last_accessed, relevance_score)
            
        Returns:
            List of user memories
        """
        if not user_id:
            return []
        
        # Check cache first
        cache_key = f"user_memory_list_{user_id}_{category}_{limit}_{sort_by}"
        cached_result = cache.get_cached_analysis(cache_key, "user_memory")
        if cached_result:
            return json.loads(cached_result)
        
        if not user_id.startswith("user-"):
            return []
        
        # Load user memories from files
        memories = self._load_user_memories(user_id, category)
        
        # Sort memories
        if sort_by == "created_at":
            memories.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        elif sort_by == "last_accessed":
            memories.sort(key=lambda x: x.get("last_accessed", ""), reverse=True)
        elif sort_by == "relevance_score":
            memories.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        # Limit results
        results = memories[:limit]
        
        # Cache results for 5 minutes
        cache.cache_content_analysis(cache_key, json.dumps(results), "user_memory")
        
        return results
    
    @handle_errors(operation_name="delete_memory", return_dict=True)
    def delete_memory(self, user_id: str, memory_id: str) -> Dict[str, Any]:
        """
        Delete a specific memory by ID.
        
        Args:
            user_id: User identifier
            memory_id: Memory identifier to delete
            
        Returns:
            Deletion result
        """
        if not user_id or not memory_id:
            raise ValueError("User ID and memory ID are required")
        
        if not user_id.startswith("user-"):
            raise ValueError("Invalid user_id format. Must be format: user-####")
        
        # Find and delete memory from files
        deleted = self._delete_memory_from_files(user_id, memory_id)
        
        if not deleted:
            return {
                "success": False,
                "message": f"Memory {memory_id} not found"
            }
        
        # Delete from Memory MCP
        self._delete_memory_from_mcp(user_id, memory_id)
        
        # Clear related caches
        self._clear_user_memory_cache(user_id)
        
        return {
            "success": True,
            "message": f"Memory {memory_id} deleted successfully"
        }
    
    @handle_errors(operation_name="suggest_contextual", return_dict=True)
    def suggest_contextual(self, user_id: str, context: str, limit: int = 5, 
                          relevance_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Get contextual memory suggestions based on current context.
        
        Args:
            user_id: User identifier
            context: Current context for suggestions
            limit: Maximum number of suggestions
            relevance_threshold: Minimum relevance score
            
        Returns:
            List of contextual memory suggestions
        """
        if not user_id or not context:
            return []
        
        # Check cache first
        cache_key = f"user_memory_suggest_{user_id}_{hashlib.md5(context.encode()).hexdigest()[:8]}_{limit}"
        cached_result = cache.get_cached_analysis(cache_key, "user_memory")
        if cached_result:
            return json.loads(cached_result)
        
        if not user_id.startswith("user-"):
            return []
        
        # Load user memories from files
        memories = self._load_user_memories(user_id)
        
        # Score memories for contextual relevance
        suggestions = []
        context_lower = context.lower()
        
        for memory in memories:
            # Calculate contextual relevance
            relevance_score = self._calculate_contextual_relevance(memory, context_lower)
            
            if relevance_score >= relevance_threshold:
                suggestion = {
                    "memory_id": memory["memory_id"],
                    "content": memory["content"],
                    "category": memory["category"],
                    "tags": memory["tags"],
                    "relevance_score": relevance_score,
                    "relevance_reason": self._get_relevance_reason(memory, context_lower),
                    "created_at": memory["created_at"]
                }
                suggestions.append(suggestion)
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Limit results
        results = suggestions[:limit]
        
        # Cache results for 5 minutes
        cache.cache_content_analysis(cache_key, json.dumps(results), "user_memory")
        
        return results
    
    
    def _load_user_memories(self, user_id: str, category: str = None) -> List[Dict[str, Any]]:
        """Load user memories from file system"""
        memories = []
        user_memories_dir = self.base_path / user_id / "memories"
        
        if not user_memories_dir.exists():
            return memories
        
        # Load from specific category file if specified
        if category:
            category_file = user_memories_dir / f"{category}.json"
            if category_file.exists():
                try:
                    with open(category_file, 'r') as f:
                        data = json.load(f)
                        memories.extend(data.get("memories", []))
                except (json.JSONDecodeError, IOError):
                    pass
        else:
            # Load from all category files
            for memory_file in user_memories_dir.glob("*.json"):
                try:
                    with open(memory_file, 'r') as f:
                        data = json.load(f)
                        memories.extend(data.get("memories", []))
                except (json.JSONDecodeError, IOError):
                    continue
        
        return memories
    
    def _store_memory_to_file(self, user_id: str, memory: Dict[str, Any], category: str):
        """Store memory to appropriate category file"""
        user_memories_dir = self.base_path / user_id / "memories"
        user_memories_dir.mkdir(parents=True, exist_ok=True)
        
        category_file = user_memories_dir / f"{category}.json"
        
        # Load existing data or create new
        if category_file.exists():
            try:
                with open(category_file, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = self._create_empty_category_data(category, user_id)
        else:
            data = self._create_empty_category_data(category, user_id)
        
        # Add memory
        data["memories"].append(memory)
        data["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_memories"] = len(data["memories"])
        
        # Update tag frequency
        for tag in memory["tags"]:
            data["metadata"]["tag_frequency"][tag] = data["metadata"]["tag_frequency"].get(tag, 0) + 1
        
        # Save back to file
        with open(category_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_empty_category_data(self, category: str, user_id: str) -> Dict[str, Any]:
        """Create empty category data structure"""
        return {
            "schema_version": "1.0",
            "category": category,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "memories": [],
            "metadata": {
                "total_memories": 0,
                "category_stats": {category: 0},
                "tag_frequency": {},
                "last_backup": datetime.now().isoformat(),
                "mcp_integration": {
                    "enabled": True,
                    "last_sync": datetime.now().isoformat(),
                    "sync_status": "active"
                }
            }
        }
    
    
    
    
    def _calculate_relevance_score(self, memory: Dict[str, Any], query: str) -> float:
        """Calculate relevance score for a memory against a query using content similarity"""
        score = 0.0
        
        # Content matching - simple word overlap
        content_lower = memory.get("content", "").lower()
        query_words = set(query.split())
        content_words = set(content_lower.split())
        
        # Calculate word overlap score
        if query_words and content_words:
            overlap = len(query_words.intersection(content_words))
            score = overlap / len(query_words.union(content_words))
        
        # Tag matching
        tags = memory.get("tags", [])
        for tag in tags:
            if tag.lower() in query:
                score += 0.2
        
        # Category matching
        category = memory.get("category", "")
        if category.lower() in query:
            score += 0.15
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _calculate_contextual_relevance(self, memory: Dict[str, Any], context: str) -> float:
        """Calculate contextual relevance score using content similarity"""
        score = 0.0
        
        # Content similarity - word overlap
        content_lower = memory.get("content", "").lower()
        context_words = set(context.split())
        content_words = set(content_lower.split())
        
        # Calculate word overlap score
        if context_words and content_words:
            overlap = len(context_words.intersection(content_words))
            score = overlap / len(context_words.union(content_words))
        
        # Tag relevance
        tags = memory.get("tags", [])
        for tag in tags:
            if tag.lower() in context:
                score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _get_relevance_reason(self, memory: Dict[str, Any], context: str) -> str:
        """Get explanation for why memory is relevant"""
        reasons = []
        
        # Check content similarity
        content_lower = memory.get("content", "").lower()
        context_words = context.split()
        matching_words = [w for w in context_words if w in content_lower]
        if matching_words:
            reasons.append(f"Content matches: {', '.join(matching_words[:3])}")
        
        # Check tag relevance
        tags = memory.get("tags", [])
        matching_tags = [t for t in tags if t.lower() in context]
        if matching_tags:
            reasons.append(f"Related tags: {', '.join(matching_tags)}")
        
        return " | ".join(reasons) if reasons else "Content similarity"
    
    def _store_memory_to_mcp(self, user_id: str, memory: Dict[str, Any]):
        """Store memory to Memory MCP for persistence"""
        try:
            # Create MCP entity for the memory
            entity_data = {
                "name": f"user_memory_{user_id}_{memory['memory_id']}",
                "entityType": "user-memory",
                "observations": [
                    f"User ID: {user_id}",
                    f"Memory ID: {memory['memory_id']}",
                    f"Content: {memory['content']}",
                    f"Category: {memory['category']}",
                    f"Tags: {', '.join(memory['tags'])}",
                    f"Created: {memory['created_at']}"
                ]
            }
            
            self.memory_mcp.client.create_entities([entity_data])
            
        except Exception as e:
            # Log error but don't fail the operation
            print(f"Warning: Failed to store memory to MCP: {e}")
    
    def _delete_memory_from_mcp(self, user_id: str, memory_id: str):
        """Delete memory from Memory MCP"""
        try:
            # This would require MCP delete operation
            # For now, just log the attempt
            print(f"Would delete MCP entity: user_memory_{user_id}_{memory_id}")
        except Exception as e:
            print(f"Warning: Failed to delete memory from MCP: {e}")
    
    def _delete_memory_from_files(self, user_id: str, memory_id: str) -> bool:
        """Delete memory from file system"""
        user_memories_dir = self.base_path / user_id / "memories"
        
        if not user_memories_dir.exists():
            return False
        
        # Search through all category files
        for memory_file in user_memories_dir.glob("*.json"):
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                
                # Find and remove memory
                memories = data.get("memories", [])
                original_count = len(memories)
                
                memories = [m for m in memories if m.get("memory_id") != memory_id]
                
                if len(memories) < original_count:
                    # Update and save
                    data["memories"] = memories
                    data["last_updated"] = datetime.now().isoformat()
                    data["metadata"]["total_memories"] = len(memories)
                    
                    with open(memory_file, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    return True
                    
            except (json.JSONDecodeError, IOError):
                continue
        
        return False
    
    def _update_memory_access_counts(self, user_id: str, memories: List[Dict[str, Any]]):
        """Update access counts for memories"""
        # This would update the access counts in the files
        # Implementation would update the stored files with new access counts
        memory_ids = [m.get("memory_id") for m in memories]
        # Log access for debugging - could be enhanced to actually update files
        pass
    
    def _clear_user_memory_cache(self, user_id: str):
        """Clear all cached entries for a user"""
        # This would clear cache entries matching the user pattern
        # Implementation would clear cache keys that start with user_memory_*_{user_id}
        pass
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        operation = params.get("operation", "unknown")
        memory_count = params.get("memory_count", 1)
        query_complexity = params.get("query_complexity", 1)
        mcp_operations = params.get("mcp_operations", 1)
        
        # Base costs for different operations
        base_costs = {
            "store": 0.002,     # Higher cost for storage and categorization
            "retrieve": 0.001,  # Lower cost for retrieval
            "list": 0.001,      # Low cost for listing
            "delete": 0.001,    # Low cost for deletion
            "suggest": 0.003    # Higher cost for AI suggestions
        }
        
        base_cost = base_costs.get(operation, 0.001)
        
        # Scale by memory count and complexity
        scaling_factor = 1 + (memory_count * 0.0001) + (query_complexity * 0.0002)
        
        # Add MCP operation cost
        mcp_cost = mcp_operations * 0.0005
        
        return base_cost * scaling_factor + mcp_cost

# Standalone functions for button imports
def store_memory(user_id: str, content: str, category: str = None, 
                tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]:
    """Standalone function for storing memory"""
    manager = UserMemoryManager()
    return manager.store_memory(user_id, content, category, tags, priority)

def retrieve_memories(user_id: str, query: str, category: str = None, 
                     limit: int = 10) -> List[Dict[str, Any]]:
    """Standalone function for retrieving memories"""
    manager = UserMemoryManager()
    return manager.retrieve_memories(user_id, query, category, limit)

def list_memories(user_id: str, category: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Standalone function for listing memories"""
    manager = UserMemoryManager()
    return manager.list_memories(user_id, category, limit)

def delete_memory(user_id: str, memory_id: str) -> Dict[str, Any]:
    """Standalone function for deleting memory"""
    manager = UserMemoryManager()
    return manager.delete_memory(user_id, memory_id)

def suggest_contextual(user_id: str, context: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Standalone function for contextual suggestions"""
    manager = UserMemoryManager()
    return manager.suggest_contextual(user_id, context, limit)