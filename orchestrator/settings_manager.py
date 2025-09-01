"""
Application Settings Manager
Manages user application settings with UserID-based storage and delta-only persistence.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError

# Standard cache instance
cache = CacheManager()

# Core application settings as defined in MAO_FLOW.md
CORE_SETTINGS = {
    "default_agent": "claude-sonnet-4",
    "default_provider": "anthropic_direct",
    "app_theme": "dark_mode",
    "notifications": "once_no_push",
    "cat_vibes": "i_love_it",
    "double_texting": "always",
    "remember_credentials": False,
    "productive_startup": False,
    "public_profile": True,
    "public_contact": True,
    "offer_my_services": False,
    "user_analytics": True,
    "latest_models": True,
    "mao_model": "sonnet-latest",
    "claude_code_model": "opus-latest",
    "code_nudges": True,
    "currency": "USD",
    "payment_frequency": "yearly",
    "language": "english",
    "local_data_backup": "setup"
}

# Setting validation rules
SETTING_OPTIONS = {
    "app_theme": ["dark_mode", "light_mode"],
    "notifications": ["once_no_push", "silent_with_push", "silent_no_push", "notifications_on"],
    "cat_vibes": ["i_love_it", "be_serious_please"],
    "double_texting": ["always", "user_only", "mao_only", "never", "queue"],
    "mao_model": ["sonnet-latest", "opus-latest", "claude_code_as_mao"],
    "claude_code_model": ["sonnet-latest", "opus-latest", "secondary_sonnet", "secondary_opus"],
    "currency": ["USD", "EUR", "GBP", "CAD", "AUD", "BRL", "MXN", "CNY", "JPY", "KRW", "INR"],
    "payment_frequency": ["monthly", "quarterly", "six_months", "yearly"],
    "language": ["english", "spanish", "portuguese", "french", "german", "chinese", "japanese", "arabic"]
}

class ApplicationSettingsManager:
    """
    Manages application settings with UserID-based storage and delta-only persistence.
    
    Core Principles:
    1. UserID-based directory structure (not username)
    2. Delta-only storage - only store changes from defaults
    3. Predefined settings structure from MAO_FLOW.md
    4. Simple validation against known setting options
    """
    
    def __init__(self):
        self.user_base_dir = Path("./configs/user")
        
        # Ensure base user directory exists
        self.user_base_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_settings(self) -> Dict[str, Any]:
        """
        Get available settings with their default values.
        Returns the core settings structure defined in MAO_FLOW.md.
        
        Returns:
            Dict mapping setting names to default values
        """
        return CORE_SETTINGS.copy()
    
    def estimate_cost(self, params: Dict[str, Any] = None) -> float:
        """
        Estimate operation cost for budget planning.
        
        Args:
            params: Operation parameters (optional)
            
        Returns:
            Estimated cost in USD
        """
        # Settings operations are local file operations with minimal cost
        return 0.0001
    
    @handle_errors(operation_name="get_default_settings", return_dict=True)
    def get_default_settings(self) -> Dict[str, Any]:
        """
        Get all default settings values.
        
        Returns:
            Dict mapping setting names to default values
        """
        return CORE_SETTINGS.copy()
    
    @handle_errors(operation_name="get_user_settings", return_dict=True)
    def get_user_settings(self, user_id: str) -> Dict[str, Any]:
        """
        Get user settings with delta-only storage using UserID-based structure.
        Merges user changes with application defaults.
        
        Args:
            user_id: User's ID (format: user-1234)
            
        Returns:
            Complete settings dict (defaults + user changes)
        """
        cache_key = f"user_settings|{user_id}"
        
        # Check cache first
        cached_result = cache.get_cached_analysis(cache_key, "user_settings")
        if cached_result:
            return json.loads(cached_result)
        
        # Get current defaults
        defaults = self.get_default_settings()
        
        # Load user deltas from UserID directory
        user_file = self._get_user_file_path(user_id)
        user_deltas = {}
        
        if user_file and user_file.exists():
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    # Extract only setting changes (exclude metadata)
                    user_deltas = {k: v for k, v in user_data.items() 
                                 if k in CORE_SETTINGS}
            except Exception:
                user_deltas = {}  # Use empty deltas on error
        
        # Merge defaults with user changes
        merged_settings = defaults.copy()
        merged_settings.update(user_deltas)
        
        # Cache the merged results
        cache.cache_content_analysis(cache_key, json.dumps(merged_settings), "user_settings")
        
        return merged_settings
    
    @handle_errors(operation_name="update_user_setting", return_dict=True)
    def update_user_setting(self, user_id: str, setting_name: str, value: Any) -> bool:
        """
        Update a single user setting using UserID-based delta-only storage.
        
        Args:
            user_id: User's ID (format: user-1234)
            setting_name: Name of setting to update
            value: New value for setting
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate setting exists and value is valid
            if setting_name not in CORE_SETTINGS:
                return False
                
            if not self._validate_setting_value(setting_name, value):
                return False
            
            # Get user directory and file path
            user_dir = self.user_base_dir / user_id
            username = self._extract_username_from_file(user_dir)
            
            if not username:
                return False
                
            user_file = user_dir / f"user_{username}.json"
            user_data = {}
            
            # Load existing user data
            if user_file.exists():
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
            
            # Update setting (delta-only - only store if different from default)
            default_value = CORE_SETTINGS[setting_name]
            if value != default_value:
                user_data[setting_name] = value
            elif setting_name in user_data:
                # Remove setting if it matches default (clean delta storage)
                del user_data[setting_name]
            
            # Ensure user directory structure exists
            if not user_dir.exists():
                user_dir.mkdir(parents=True, exist_ok=True)
                (user_dir / "memories").mkdir(exist_ok=True)
                (user_dir / "analytics").mkdir(exist_ok=True)
            
            # Save updated user file
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            
            # Clear user settings cache
            cache.clear_cache(f"user_settings|{user_id}")
            
            return True
            
        except Exception:
            return False
    
    def _validate_setting_value(self, setting_name: str, value: Any) -> bool:
        """
        Validate a setting value against defined options.
        
        Args:
            setting_name: Name of setting
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        if setting_name not in CORE_SETTINGS:
            return False
            
        # Check against predefined options if they exist
        if setting_name in SETTING_OPTIONS:
            return value in SETTING_OPTIONS[setting_name]
            
        # For boolean settings
        if isinstance(CORE_SETTINGS[setting_name], bool):
            return isinstance(value, bool)
            
        # For string settings without specific options
        if isinstance(CORE_SETTINGS[setting_name], str):
            return isinstance(value, str)
            
        return True
    
    def _get_user_file_path(self, user_id: str) -> Optional[Path]:
        """
        Get user file path based on UserID directory structure.
        
        Args:
            user_id: User's ID (format: user-1234)
            
        Returns:
            Path to user file or None if not found
        """
        user_dir = self.user_base_dir / user_id
        if not user_dir.exists():
            return None
            
        # Find the user file in the UserID directory
        for file_path in user_dir.glob("user_*.json"):
            return file_path
            
        return None
        
    def _extract_username_from_file(self, user_dir: Path) -> Optional[str]:
        """
        Extract username from existing user file in UserID directory.
        
        Args:
            user_dir: Path to user's directory
            
        Returns:
            Username if found, None otherwise
        """
        if not user_dir.exists():
            return None
            
        for file_path in user_dir.glob("user_*.json"):
            try:
                with open(file_path, 'r') as f:
                    user_data = json.load(f)
                    return user_data.get('username')
            except Exception:
                continue
                
        return None

# Standalone functions for button file imports
def get_default_settings() -> Dict[str, Any]:
    """Standalone function for getting default settings"""
    manager = ApplicationSettingsManager()
    return manager.get_default_settings()

def get_user_settings(user_id: str) -> Dict[str, Any]:
    """Standalone function for getting user settings"""
    manager = ApplicationSettingsManager()
    return manager.get_user_settings(user_id)

def update_user_setting(user_id: str, setting_name: str, value: Any) -> bool:
    """Standalone function for updating user setting"""
    manager = ApplicationSettingsManager()
    return manager.update_user_setting(user_id, setting_name, value)

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate operation cost for budget planning"""
    return 0.0001