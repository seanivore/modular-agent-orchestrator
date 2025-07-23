"""
Login CLI Command - Core Logic
User authentication via username_manager.py integration with session management
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
from orchestrator.username_manager import UsernameManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="login", return_dict=True)
def execute_login(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main login command execution with username_manager integration.
    
    Args:
        params: Command parameters from CLI/app input
        - username: Username for authentication
        - create_new: Boolean flag to create new user if not found
        - search_mode: Boolean flag to enable username search / recovery
        - search_term: Search term for username recovery
        
    Returns:
        Standardized result dictionary with authentication status
    """
    if params is None:
        params = {}
    
    username = params.get("username", "").strip()
    create_new = params.get("create_new", False)
    search_mode = params.get("search_mode", False)
    search_term = params.get("search_term", "").strip()
    
    # Check cache for recent authentication attempts (security consideration)
    cache_key = _generate_cache_key(params)
    
    # Search mode for username recovery
    if search_mode:
        return _handle_username_search(search_term)
    
    # Interactive mode - no username provided
    if not username:
        return _handle_interactive_login()
    
    # Direct authentication with provided username
    return _handle_direct_authentication(username, create_new)

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if params is None:
        params = {}
    
    # Medium complexity authentication operations
    operation_type = params.get("operation_type", "standard")
    
    cost_map = {
        "standard": 0.003,
        "search": 0.004,
        "create_new": 0.005,
        "interactive": 0.002
    }
    
    return cost_map.get(operation_type, 0.003)

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate cache key for session-based caching with security considerations"""
    if params is None:
        params = {}
    
    # Include timestamp for session-based invalidation (security)
    current_hour = datetime.now().strftime("%Y%m%d%H")
    base_key = f"login|{str(params)}|{current_hour}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _handle_interactive_login() -> Dict[str, Any]:
    """Handle interactive login flow when no username provided"""
    try:
        manager = UsernameManager()
        
        # Check if there's already a session user
        current_user = manager.get_session_user()
        
        if current_user:
            return {
                "success": True,
                "login_type": "existing_session",
                "user_data": current_user,
                "message": f"Already logged in as {current_user.get('username')}",
                "prompt_required": False,
                "timestamp": datetime.now().isoformat()
            }
        
        # No current session - require username input
        return {
            "success": True,
            "login_type": "username_required",
            "message": "Please enter your username to continue",
            "prompt_required": True,
            "show_help": True,
            "help_message": "Enter your username (6-20 alphanumeric characters)",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to check session: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_direct_authentication(username: str, create_new: bool = False) -> Dict[str, Any]:
    """Handle direct authentication with provided username"""
    try:
        manager = UsernameManager()
        
        # Validate username format
        if not _validate_username_format(username):
            return {
                "success": False,
                "error": "Invalid username format. Use 6-20 alphanumeric characters.",
                "show_help": True,
                "timestamp": datetime.now().isoformat()
            }
        
        # Try to load existing user
        user_data = manager.load_user(username)
        
        if user_data:
            # User exists - set session
            session_result = manager.set_session_user(username)
            
            if session_result.get("success"):
                return {
                    "success": True,
                    "login_type": "existing_user",
                    "user_data": user_data,
                    "message": f"Welcome back, {username}!",
                    "session_set": True,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to set session: {session_result.get('message', 'Unknown error')}",
                    "timestamp": datetime.now().isoformat()
                }
        
        # User doesn't exist
        if create_new:
            # Create new user
            create_result = manager.create_user(username)
            
            if create_result.get("success"):
                return {
                    "success": True,
                    "login_type": "new_user_created",
                    "user_data": create_result.get("user_data"),
                    "message": f"New user '{username}' created successfully",
                    "session_set": True,
                    "first_time": True,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to create user: {create_result.get('message', 'Unknown error')}",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # User not found and not creating new
            return {
                "success": False,
                "login_type": "user_not_found",
                "error": f"User '{username}' not found",
                "suggestions": [
                    "Check your username spelling",
                    "Use search mode to find your username",
                    "Create a new account if you're a first-time user"
                ],
                "show_search_option": True,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Authentication failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _handle_username_search(search_term: str) -> Dict[str, Any]:
    """Handle username search / recovery functionality"""
    try:
        if not search_term:
            return {
                "success": False,
                "error": "Search term required for username recovery",
                "help_message": "Enter part of your name, email, or user ID to search",
                "timestamp": datetime.now().isoformat()
            }
        
        manager = UsernameManager()
        matches = manager.find_user(search_term)
        
        if matches:
            return {
                "success": True,
                "search_type": "username_recovery",
                "matches": matches,
                "total_matches": len(matches),
                "message": f"Found {len(matches)} matching user(s)",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "search_type": "no_matches",
                "error": f"No users found matching '{search_term}'",
                "suggestions": [
                    "Try a different search term",
                    "Check spelling of names or email",
                    "Contact administrator if you need help"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Search failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _validate_username_format(username: str) -> bool:
    """Validate username format per NEW_USER_FLOW.md requirements"""
    if not username:
        return False
        
    # 6-20 alphanumeric characters
    if len(username) < 6 or len(username) > 20:
        return False
        
    # Only alphanumeric characters allowed
    if not username.isalnum():
        return False
        
    return True

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_login(params)

# Additional utility functions for authentication workflow
def check_session_status() -> Dict[str, Any]:
    """Check current session status without login attempt"""
    try:
        manager = UsernameManager()
        current_user = manager.get_session_user()
        
        if current_user:
            return {
                "success": True,
                "session_active": True,
                "user_data": current_user,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": True,
                "session_active": False,
                "message": "No active session",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to check session: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def get_user_list() -> Dict[str, Any]:
    """Get list of all users for selection (admin / debugging purposes)"""
    try:
        manager = UsernameManager()
        users = manager.list_users()
        
        return {
            "success": True,
            "users": users,
            "total_users": len(users),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list users: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }