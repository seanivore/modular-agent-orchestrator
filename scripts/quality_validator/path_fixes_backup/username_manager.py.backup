"""
Username Manager 
Handles user creation, session persistence, and settings integration
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Import user ID generator
from scripts.user_id_generator.user_id_generator import generate_user_id

# Standard cache instance
cache = CacheManager()

class UsernameManager:
    """
    Manages user accounts, session persistence, and settings integration
    Implements delta-only storage for user settings
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "configs"
        self.user_dir = self.base_path / "user"
        self.examples_dir = self.base_path / "examples"
        self.session_file = self.user_dir / ".last_session"
        
        # Ensure directories exist
        self.user_dir.mkdir(exist_ok=True)
        
        # Load settings manager for default values
        self.settings_manager = None
        self._load_settings_manager()
    
    def _load_settings_manager(self):
        """Load settings manager for default value access"""
        try:
            from orchestrator.settings_manager import get_default_settings
            self.get_defaults = get_default_settings
        except ImportError:
            self.get_defaults = lambda: {}
    
    @handle_errors(operation_name="create_user", return_dict=True)
    def create_user(self, username: str, first_name: str = "", last_name: str = "", 
                   email: str = "", dob: str = "") -> Dict[str, Any]:
        """
        Create a new user with generated user_id
        Creates nested directory structure with memories and analytics subdirectories
        Returns user data and creation status
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        clean_username = username.strip().lower()
        
        # Check if user already exists (check both new and legacy paths)
        existing_user = self.load_user(username)
        if existing_user:
            return {
                "success": False,
                "message": f"User '{username}' already exists",
                "user_data": existing_user
            }
        
        # Generate user_id using meid script
        try:
            user_id = generate_user_id(username)
        except Exception as e:
            raise APIError(f"Failed to generate user ID: {str(e)}")
        
        # Create user data
        user_data = {
            "username": username,
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "dob": dob,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        # Create nested directory structure
        user_dir = self.user_dir / clean_username
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Create memories and analytics subdirectories
        (user_dir / "memories").mkdir(exist_ok=True)
        (user_dir / "analytics").mkdir(exist_ok=True)
        
        # Save user file in nested structure
        user_file = user_dir / f"user_{clean_username}.json"
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        # Set as current session user
        self.set_session_user(username)
        
        # Cache user data
        cache_key = f"user_data_{clean_username}"
        cache.cache_content_analysis(cache_key, json.dumps(user_data), "username_manager")
        
        return {
            "success": True,
            "message": f"User '{username}' created successfully",
            "user_data": user_data
        }
    
    @handle_errors(operation_name="load_user", return_dict=True)
    def load_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Load user data by username, checking both new nested and legacy flat structures"""
        if not username:
            return None
        
        clean_username = username.strip().lower()
        
        # Check cache first
        cache_key = f"user_data_{clean_username}"
        cached_result = cache.get_cached_analysis(cache_key, "username_manager")
        if cached_result:
            return json.loads(cached_result)
        
        # Check both new nested structure and legacy flat structure
        user_file = self._get_user_file_path(clean_username)
        
        if not user_file or not user_file.exists():
            return None
        
        try:
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            
            # Cache user data
            cache.cache_content_analysis(cache_key, json.dumps(user_data), "username_manager")
            
            return user_data
            
        except (json.JSONDecodeError, IOError) as e:
            raise APIError(f"Failed to load user data: {str(e)}")
    
    @handle_errors(operation_name="update_user_settings", return_dict=True)
    def update_user_settings(self, username: str, settings_changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user settings with delta-only storage
        Only saves settings that differ from defaults
        Supports both legacy and new nested directory structures
        """
        user_data = self.load_user(username)
        if not user_data:
            return {"success": False, "message": f"User '{username}' not found"}
        
        # Get default settings
        default_settings = self.get_defaults() if self.get_defaults else {}
        
        # Calculate delta changes (only non-default values)
        delta_settings = {}
        for key, value in settings_changes.items():
            default_value = default_settings.get(key)
            if value != default_value:
                delta_settings[key] = value
        
        # Update user data with delta settings
        if "settings" not in user_data:
            user_data["settings"] = {}
        
        user_data["settings"].update(delta_settings)
        user_data["last_updated"] = datetime.now().isoformat()
        
        # Save updated user file using appropriate path
        clean_username = username.strip().lower()
        user_file = self._get_user_file_path(clean_username)
        
        if not user_file:
            # Create new file in nested structure
            user_dir = self.user_dir / clean_username
            user_dir.mkdir(parents=True, exist_ok=True)
            (user_dir / "memories").mkdir(exist_ok=True)
            (user_dir / "analytics").mkdir(exist_ok=True)
            user_file = user_dir / f"user_{clean_username}.json"
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        # Update cache
        cache_key = f"user_data_{clean_username}"
        cache.cache_content_analysis(cache_key, json.dumps(user_data), "username_manager")
        
        return {
            "success": True,
            "message": f"Settings updated for user '{username}'",
            "delta_changes": delta_settings,
            "user_data": user_data
        }
    
    @handle_errors(operation_name="set_session_user", return_dict=True)
    def set_session_user(self, username: str) -> Dict[str, Any]:
        """Set the current session user with nested directory support"""
        user_data = self.load_user(username)
        if not user_data:
            return {"success": False, "message": f"User '{username}' not found"}
        
        # Update last login
        user_data["last_login"] = datetime.now().isoformat()
        clean_username = username.strip().lower()
        user_file = self._get_user_file_path(clean_username)
        
        if not user_file:
            # Create new file in nested structure
            user_dir = self.user_dir / clean_username
            user_dir.mkdir(parents=True, exist_ok=True)
            (user_dir / "memories").mkdir(exist_ok=True)
            (user_dir / "analytics").mkdir(exist_ok=True)
            user_file = user_dir / f"user_{clean_username}.json"
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        # Save session state
        session_data = {
            "username": username,
            "user_id": user_data["user_id"],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return {"success": True, "message": f"Session set for user '{username}'"}
    
    @handle_errors(operation_name="get_session_user", return_dict=True)
    def get_session_user(self) -> Optional[Dict[str, Any]]:
        """Get the current session user"""
        if not self.session_file.exists():
            return None
        
        try:
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verify user still exists
            username = session_data.get("username")
            if username:
                user_data = self.load_user(username)
                if user_data:
                    return user_data
            
            # Clean up invalid session
            self.session_file.unlink(missing_ok=True)
            return None
            
        except (json.JSONDecodeError, IOError):
            # Clean up corrupted session
            self.session_file.unlink(missing_ok=True)
            return None
    
    @handle_errors(operation_name="list_users", return_dict=True)
    def list_users(self) -> List[Dict[str, Any]]:
        """Get fresh list of all users from directory, checking both nested and legacy structures"""
        users = []
        
        # Check legacy flat structure
        for user_file in self.user_dir.glob("user_*.json"):
            if user_file.name.startswith('.'):
                continue
                
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                users.append(user_data)
            except (json.JSONDecodeError, IOError):
                continue
        
        # Check new nested structure
        for user_dir in self.user_dir.iterdir():
            if user_dir.is_dir() and not user_dir.name.startswith('.'):
                user_file = user_dir / f"user_{user_dir.name}.json"
                if user_file.exists():
                    try:
                        with open(user_file, 'r') as f:
                            user_data = json.load(f)
                        # Check if we already have this user (avoid duplicates)
                        if not any(u.get('username') == user_data.get('username') for u in users):
                            users.append(user_data)
                    except (json.JSONDecodeError, IOError):
                        continue
        
        # Sort by last_login (most recent first)
        users.sort(key=lambda x: x.get("last_login", ""), reverse=True)
        
        return users
    
    @handle_errors(operation_name="find_user", return_dict=True)
    def find_user(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Find users by username, user_id, name, or email
        Useful for username recovery
        """
        if not search_term:
            return []
        
        search_lower = search_term.lower().strip()
        matches = []
        
        for user_data in self.list_users():
            # Search in various fields
            searchable_fields = [
                user_data.get("username", "").lower(),
                user_data.get("user_id", "").lower(),
                user_data.get("first_name", "").lower(),
                user_data.get("last_name", "").lower(),
                user_data.get("email", "").lower(),
                f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".lower().strip()
            ]
            
            if any(search_lower in field for field in searchable_fields if field):
                matches.append(user_data)
        
        return matches
    
    @handle_errors(operation_name="logout_user", return_dict=True)
    def logout_user(self) -> Dict[str, Any]:
        """Clear session user"""
        if self.session_file.exists():
            self.session_file.unlink()
        
        return {"success": True, "message": "User logged out successfully"}
    
    def _get_user_file_path(self, username: str) -> Optional[Path]:
        """
        Get user file path, checking both new nested structure and legacy flat structure.
        Prioritizes nested structure for forward compatibility.
        
        Args:
            username: Clean username (already processed)
            
        Returns:
            Path to user file or None if not found
        """
        # First check new nested structure: ./configs/user/[username]/user_[username].json
        nested_path = self.user_dir / username / f"user_{username}.json"
        if nested_path.exists():
            return nested_path
        
        # Fallback to legacy flat structure: ./configs/user/user_[username].json
        legacy_path = self.user_dir / f"user_{username}.json"
        if legacy_path.exists():
            return legacy_path
        
        # Return None if neither exists
        return None
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        operation = params.get("operation", "unknown")
        
        cost_map = {
            "create_user": 0.001,
            "load_user": 0.0005,
            "update_settings": 0.002,
            "list_users": 0.001,
            "find_user": 0.002,
            "session_management": 0.0005
        }
        
        return cost_map.get(operation, 0.001)

# Standalone functions for button imports
def create_user(username: str, first_name: str = "", last_name: str = "", 
                email: str = "", dob: str = "") -> Dict[str, Any]:
    """Standalone function for creating a new user"""
    manager = UsernameManager()
    return manager.create_user(username, first_name, last_name, email, dob)

def load_user(username: str) -> Optional[Dict[str, Any]]:
    """Standalone function for loading user data"""
    manager = UsernameManager()
    return manager.load_user(username)

def get_session_user() -> Optional[Dict[str, Any]]:
    """Standalone function for getting current session user"""
    manager = UsernameManager()
    return manager.get_session_user()

def set_session_user(username: str) -> Dict[str, Any]:
    """Standalone function for setting session user"""
    manager = UsernameManager()
    return manager.set_session_user(username)

def update_user_settings(username: str, settings_changes: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for updating user settings"""
    manager = UsernameManager()
    return manager.update_user_settings(username, settings_changes)

def list_users() -> List[Dict[str, Any]]:
    """Standalone function for listing all users"""
    manager = UsernameManager()
    return manager.list_users()

def find_user(search_term: str) -> List[Dict[str, Any]]:
    """Standalone function for finding users"""
    manager = UsernameManager()
    return manager.find_user(search_term)

def logout_user() -> Dict[str, Any]:
    """Standalone function for logging out current user"""
    manager = UsernameManager()
    return manager.logout_user()
