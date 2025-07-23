"""
User ID CLI Command - Core Logic
Displays current user ID or generates user ID from username with workflow state integration
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.username_manager import UsernameManager
from orchestrator.workflow_state import WorkflowStateManager
from orchestrator.memory_mcp import MemoryMCPManager

# Import user ID generator
from scripts.user_id_generator.user_id_generator import generate_user_id, generate_user_id_with_explanation

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="user_id", return_dict=True)
def execute_user_id(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main user_id command execution with caching and workflow state integration.
    
    Args:
        params: Command parameters from CLI / app input
        
    Returns:
        Standardized result dictionary with user ID data and workflow context
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "user_id")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 5 minutes (user context changes moderately)
    cache.cache_content_analysis(cache_key, json.dumps(result), "user_id")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Medium complexity due to multi-manager operations.
    Uses Claude Sonnet 4 cost structure.
    """
    # Base cost for user ID operations (aligns with JSON config)
    base_cost = 0.003
    
    # Add cost for username manager operations
    username_operations = params.get("username_operations", 1) if params else 1
    if username_operations > 1:
        base_cost += (username_operations - 1) * 0.001
    
    # Add cost for workflow state management (heavy operations)
    workflow_state_ops = params.get("workflow_state_operations", 1) if params else 1
    if workflow_state_ops > 1:
        base_cost += (workflow_state_ops - 1) * 0.0005
    
    # Add cost for memory MCP integration (heavy operations)
    memory_mcp_ops = params.get("memory_mcp_operations", 1) if params else 1
    if memory_mcp_ops > 1:
        base_cost += (memory_mcp_ops - 1) * 0.0005
    
    # Add cost for user ID generation (if needed)
    if params and params.get("generate_new_id", False):
        base_cost += 0.001
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including user context and workflow state"""
    base_key = f"user_id|{str(params) if params else 'none'}"
    
    # Add session user fingerprint for cache invalidation
    try:
        username_manager = UsernameManager()
        session_user = username_manager.get_session_user()
        if session_user:
            user_fingerprint = f"{session_user.get('username', '')}|{session_user.get('user_id', '')}|{session_user.get('last_login', '')}"
            base_key += f"|session:{hashlib.md5(user_fingerprint.encode()).hexdigest()[:8]}"
    except Exception:
        pass
    
    # Add workflow state fingerprint
    try:
        workflow_state_manager = WorkflowStateManager()
        # Include any active workflow context in fingerprint
        base_key += f"|workflow_state:{datetime.now().strftime('%Y%m%d%H')}"  # Hourly refresh
    except Exception:
        pass
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core user_id command logic implementation with multi-manager integration"""
    try:
        # Initialize managers
        username_manager = UsernameManager()
        workflow_state_manager = WorkflowStateManager()
        memory_mcp_manager = MemoryMCPManager()
        
        # Check if username provided for generation
        input_username = params.get("username") if params else None
        
        if input_username:
            # Generate user ID from provided username
            return _generate_user_id_from_username(input_username, username_manager, workflow_state_manager, memory_mcp_manager)
        else:
            # Display current session user ID
            return _display_current_user_id(username_manager, workflow_state_manager, memory_mcp_manager)
        
    except Exception as e:
        return {
            "success": False,
            "error": f"User ID operation failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _display_current_user_id(username_manager: UsernameManager, 
                           workflow_state_manager: WorkflowStateManager,
                           memory_mcp_manager: MemoryMCPManager) -> Dict[str, Any]:
    """Display current session user ID with workflow context"""
    try:
        # Get current session user
        session_user = username_manager.get_session_user()
        
        if not session_user:
            return {
                "success": False,
                "error": "No user currently logged in",
                "suggestion": "Use 'mao --login' or ' / login' to log in",
                "timestamp": datetime.now().isoformat()
            }
        
        # Get workflow context for user
        workflow_context = _get_user_workflow_context(session_user, workflow_state_manager, memory_mcp_manager)
        
        return {
            "success": True,
            "user_id": session_user.get("user_id"),
            "username": session_user.get("username"),
            "user_info": {
                "created_at": session_user.get("created_at"),
                "last_login": session_user.get("last_login"),
                "first_name": session_user.get("first_name", ""),
                "last_name": session_user.get("last_name", "")
            },
            "workflow_context": workflow_context,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get current user ID: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _generate_user_id_from_username(username: str, 
                                  username_manager: UsernameManager,
                                  workflow_state_manager: WorkflowStateManager,
                                  memory_mcp_manager: MemoryMCPManager) -> Dict[str, Any]:
    """Generate user ID from username with workflow integration"""
    try:
        # Generate user ID using the dedicated generator
        user_id, explanation = generate_user_id_with_explanation(username)
        
        # Check if this user already exists
        existing_user = username_manager.load_user(username)
        
        if existing_user:
            # User exists, return existing info with workflow context
            workflow_context = _get_user_workflow_context(existing_user, workflow_state_manager, memory_mcp_manager)
            
            return {
                "success": True,
                "user_id": existing_user.get("user_id"),
                "username": username,
                "status": "existing_user",
                "user_info": {
                    "created_at": existing_user.get("created_at"),
                    "last_login": existing_user.get("last_login"),
                    "first_name": existing_user.get("first_name", ""),
                    "last_name": existing_user.get("last_name", "")
                },
                "workflow_context": workflow_context,
                "generation_explanation": explanation,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # New user, return generated ID with option to create
            return {
                "success": True,
                "user_id": user_id,
                "username": username,
                "status": "new_user_id_generated",
                "generation_explanation": explanation,
                "next_steps": [
                    "This user ID will be assigned if you create this user",
                    "Use 'mao --login' to create and login as this user",
                    "Or use ' / login' in the app to create and login"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate user ID: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _get_user_workflow_context(user_data: Dict[str, Any], 
                             workflow_state_manager: WorkflowStateManager,
                             memory_mcp_manager: MemoryMCPManager) -> Dict[str, Any]:
    """Get workflow context for user with workflow state integration"""
    try:
        user_id = user_data.get("user_id")
        if not user_id:
            return {"active_workflows": 0, "context_available": False}
        
        # Get active workflows for user (simplified - in real implementation would search by user_id)
        active_workflows = memory_mcp_manager.list_active_workflows()
        
        # Filter workflows for this user (simplified check)
        user_workflows = []
        for workflow in active_workflows:
            workflow_observations = workflow.get("observations", [])
            if any(user_id in obs for obs in workflow_observations):
                user_workflows.append(workflow)
        
        return {
            "active_workflows": len(user_workflows),
            "context_available": len(user_workflows) > 0,
            "recent_workflows": [w.get("name", "").replace("workflow-", "") for w in user_workflows[:3]],
            "workflow_state_integration": True
        }
        
    except Exception as e:
        return {
            "active_workflows": 0,
            "context_available": False,
            "error": f"Failed to get workflow context: {str(e)}"
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_user_id(params)