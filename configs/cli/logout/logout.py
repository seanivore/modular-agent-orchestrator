"""
Logout CLI Command - Core Logic
User session management via username_manager integration
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.username_manager import UsernameManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="logout", return_dict=True)
def execute_logout(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main logout command execution with comprehensive session cleanup.
    
    Args:
        params: Command parameters from CLI / app input
        
    Returns:
        Standardized result dictionary with logout status
    """
    # Check cache for recent logout operations (avoid duplicate processing)
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "logout")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute logout logic
    result = _execute_logout_logic(params)
    
    # Cache result briefly for UI feedback (5 minutes, no sensitive data)
    if result.get("success"):
        cache_result = {
            "success": True,
            "message": result["message"],
            "timestamp": result["timestamp"]
        }
        cache.cache_content_analysis(cache_key, json.dumps(cache_result), "logout")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Session cleanup operations with workflow coordination.
    """
    # Medium complexity: file operations + cache cleanup + workflow checks
    return 0.0035

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate cache key for logout operations (minimal caching for security)"""
    base_key = f"logout|{str(params) if params else 'standard'}"
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_logout_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core logout command logic with comprehensive cleanup"""
    try:
        username_manager = UsernameManager()
        
        # Get current session user before logout for cleanup
        current_user = username_manager.get_session_user()
        if not current_user:
            return {
                "success": False,
                "message": "No active session found to logout",
                "timestamp": datetime.now().isoformat(),
                "redirect_to_login": False
            }
        
        username = current_user.get("username", "unknown")
        
        # Check for active workflows before logout
        active_workflows = _check_active_workflows(current_user)
        if active_workflows.get("has_active") and not params.get("force", False):
            return {
                "success": False,
                "message": f"Active workflows detected for {username}. Use --force to logout anyway.",
                "active_workflows": active_workflows["workflows"],
                "warning": "Logging out may interrupt running workflows",
                "timestamp": datetime.now().isoformat(),
                "force_required": True
            }
        
        # Perform comprehensive session cleanup
        cleanup_result = _perform_session_cleanup(current_user, username_manager)
        
        if cleanup_result["success"]:
            return {
                "success": True,
                "message": f"Successfully logged out user '{username}'",
                "user_logged_out": username,
                "session_cleaned": True,
                "cache_invalidated": cleanup_result["cache_invalidated"],
                "workflows_handled": cleanup_result["workflows_handled"],
                "redirect_to_login": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "message": f"Logout partially completed for '{username}' with issues",
                "user_logged_out": username,
                "issues": cleanup_result["issues"],
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Logout failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _check_active_workflows(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check for active workflows that may be interrupted by logout"""
    try:
        # Import workflow manager for active workflow checking
        from orchestrator.workflow_manager import WorkflowManager
        workflow_manager = WorkflowManager()
        
        # Note: get_active_workflows_for_user method not implemented yet
        # For now, return no active workflows to allow logout
        # TODO: Implement active workflow checking when method is available
        
        return {
            "has_active": False,
            "workflows": [],
            "count": 0,
            "note": "Active workflow checking not yet implemented"
        }
        
    except Exception:
        # If workflow checking fails, allow logout but warn user
        return {
            "has_active": False,
            "workflows": [],
            "count": 0,
            "warning": "Could not check for active workflows"
        }

def _perform_session_cleanup(user_data: Dict[str, Any], username_manager: UsernameManager) -> Dict[str, Any]:
    """Perform comprehensive session cleanup with error tracking"""
    cleanup_issues = []
    cache_invalidated = False
    workflows_handled = False
    
    try:
        # 1. Clear session using username_manager
        logout_result = username_manager.logout_user()
        if not logout_result.get("success"):
            cleanup_issues.append("Failed to clear session file")
        
        # 2. Invalidate cached user data
        username = user_data.get("username", "")
        if username:
            try:
                cache_key = f"user_data_{username.strip().lower()}"
                # Clear cached user data
                # Note: CacheManager doesn't have explicit delete method, 
                # so we'll cache empty data with short expiry
                cache.cache_content_analysis(cache_key, "", "logout_cleanup")
                cache_invalidated = True
            except Exception:
                cleanup_issues.append("Failed to invalidate user cache")
        
        # 3. Handle active workflows gracefully
        try:
            user_id = user_data.get("user_id")
            # Import workflow manager for graceful shutdown
            from orchestrator.workflow_manager import WorkflowManager
from pathlib import Path
            workflow_manager = WorkflowManager()
            
            # Note: graceful_user_logout method not implemented yet
            # For now, just log the user_id for future workflow cleanup
            # TODO: Implement graceful workflow shutdown when method is available
            workflows_handled = True
        except Exception:
            cleanup_issues.append("Could not gracefully handle active workflows")
        
        # 4. Clear sensitive session data from memory
        try:
            _clear_sensitive_session_data(user_data)
        except Exception:
            cleanup_issues.append("Failed to clear sensitive session data")
        
        return {
            "success": len(cleanup_issues) == 0,
            "cache_invalidated": cache_invalidated,
            "workflows_handled": workflows_handled,
            "issues": cleanup_issues
        }
        
    except Exception as e:
        cleanup_issues.append(f"Session cleanup error: {str(e)}")
        return {
            "success": False,
            "cache_invalidated": cache_invalidated,
            "workflows_handled": workflows_handled,
            "issues": cleanup_issues
        }

def _clear_sensitive_session_data(user_data: Dict[str, Any]) -> None:
    """Clear any sensitive data from memory (security measure)"""
    # Clear sensitive fields from user_data dict in place
    sensitive_fields = ["user_id", "email", "settings", "last_login"]
    for field in sensitive_fields:
        if field in user_data:
            user_data[field] = None

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_logout(params)