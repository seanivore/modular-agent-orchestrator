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
        Get all default settings values with caching.
        
        Returns:
            Dict mapping setting names to default values
        """
        cache_key = "default_settings"
        
        # Check cache first
        cached_result = cache.get_cached_analysis(cache_key, "default_settings")
        if cached_result:
            return json.loads(cached_result)
        
        # Get settings and extract defaults
        settings = self.discover_settings()
        defaults = {name: setting.default for name, setting in settings.items()}
        
        # Cache the results
        cache.cache_content_analysis(cache_key, json.dumps(defaults), "default_settings")
        
        return defaults
    
    @handle_errors(operation_name="get_user_settings", return_dict=True)
    def get_user_settings(self, username: str) -> Dict[str, Any]:
        """
        Get user settings with delta-only storage.
        Merges user changes with current application defaults.
        Supports both legacy (flat) and new (nested) directory structures.
        
        Args:
            username: User's username
            
        Returns:
            Complete settings dict (defaults + user changes)
        """
        cache_key = f"user_settings|{username}"
        
        # Check cache first
        cached_result = cache.get_cached_analysis(cache_key, "user_settings")
        if cached_result:
            return json.loads(cached_result)
        
        # Get current defaults
        defaults = self.get_default_settings()
        
        # Load user deltas - check both new and legacy paths
        user_file = self._get_user_file_path(username)
        user_deltas = {}
        
        if user_file and user_file.exists():
            try:
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    # Extract only setting changes (exclude username, user_id, created_at, last_login, etc.)
                    user_deltas = {k: v for k, v in user_data.items() 
                                 if k not in ['username', 'user_id', 'first_name', 'last_name', 'email', 'dob', 'created_at', 'last_login', 'last_updated']}
            except Exception:
                user_deltas = {}  # Use empty deltas on error
        
        # Merge defaults with user changes
        merged_settings = defaults.copy()
        merged_settings.update(user_deltas)
        
        # Cache the merged results
        cache.cache_content_analysis(cache_key, json.dumps(merged_settings), "user_settings")
        
        return merged_settings
    
    @handle_errors(operation_name="update_user_setting", return_dict=True)
    def update_user_setting(self, username: str, setting_name: str, value: Any) -> bool:
        """
        Update a single user setting (delta-only storage).
        Supports both legacy (flat) and new (nested) directory structures.
        
        Args:
            username: User's username
            setting_name: Name of setting to update
            value: New value for setting
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate setting exists
            settings = self.discover_settings()
            if setting_name not in settings:
                return False
            
            # Load existing user file or create new
            user_file = self._get_user_file_path(username)
            user_data = {}
            
            if user_file and user_file.exists():
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
            else:
                # Initialize with username and user_id if new file
                from scripts.user_id_generator.user_id_generator import UserIDGenerator
                generator = UserIDGenerator()
                user_id, _ = generator.generate_user_id(username)
                user_data = {
                    "username": username,
                    "user_id": user_id
                }
                
                # Ensure nested directory exists if using new structure
                nested_dir = self.user_dir / username
                if not nested_dir.exists():
                    nested_dir.mkdir(parents=True, exist_ok=True)
                    # Create memories and analytics subdirectories
                    (nested_dir / "memories").mkdir(exist_ok=True)
                    (nested_dir / "analytics").mkdir(exist_ok=True)
            
            # Update setting (delta-only - only store if different from default)
            default_value = settings[setting_name].default
            if value != default_value:
                user_data[setting_name] = value
            elif setting_name in user_data:
                # Remove setting if it matches default (clean delta storage)
                del user_data[setting_name]
            
            # Save updated user file
            if not user_file:
                # Default to new nested structure if no existing file
                user_file = self.user_dir / username / f"user_{username}.json"
                user_file.parent.mkdir(parents=True, exist_ok=True)
                (user_file.parent / "memories").mkdir(exist_ok=True)
                (user_file.parent / "analytics").mkdir(exist_ok=True)
            
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            
            # Clear relevant caches
            cache_keys = [
                f"user_settings|{username}",
                "default_settings"
            ]
            for key in cache_keys:
                cache.clear_cache(key)
            
            return True
            
        except Exception:
            return False
    
    @handle_errors(operation_name="get_settings_by_section", return_dict=True)
    def get_settings_by_section(self) -> Dict[str, List[str]]:
        """
        Group settings by UI section for organized display.
        
        Returns:
            Dict mapping section names to lists of setting names
        """
        cache_key = "settings_by_section"
        
        # Check cache first
        cached_result = cache.get_cached_analysis(cache_key, "settings_sections")
        if cached_result:
            return json.loads(cached_result)
        
        settings = self.discover_settings()
        sections = {}
        
        for name, setting in settings.items():
            section = setting.ui_metadata.get('section', 'Other')
            if section not in sections:
                sections[section] = []
            sections[section].append(name)
        
        # Cache the results
        cache.cache_content_analysis(cache_key, json.dumps(sections), "settings_sections")
        
        return sections
    
    @handle_errors(operation_name="validate_setting_value", return_dict=True)
    def validate_setting_value(self, setting_name: str, value: Any) -> bool:
        """
        Validate a setting value against its definition.
        
        Args:
            setting_name: Name of setting
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        settings = self.discover_settings()
        if setting_name not in settings:
            return False
        
        setting = settings[setting_name]
        
        # For select types, validate against options
        if setting.type == 'select' and setting.options:
            valid_values = [opt['value'] for opt in setting.options]
            return value in valid_values
        
        # For dynamic source types, validate against fallback options
        if setting.source and setting.fallback_options:
            return value in setting.fallback_options
        
        # Basic type validation
        if setting.type in ['model_select', 'provider_select']:
            return isinstance(value, str)
        
        return True
    
    @handle_errors(operation_name="create_setting_template", return_dict=True)
    def create_setting_template(self, setting_name: str) -> Optional[str]:
        """
        Create a new setting file from template.
        
        Args:
            setting_name: Name for new setting
            
        Returns:
            Path to created file or None if failed
        """
        template_file = self.examples_dir / "setting_name_app_settings.json"
        new_file = self.settings_dir / f"{setting_name}_app_settings.json"
        
        if template_file.exists():
            try:
                # Copy template and update setting name
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                
                # Update template with actual setting name
                updated_data = {setting_name: template_data['setting_name']}
                
                with open(new_file, 'w') as f:
                    json.dump(updated_data, f, indent=2)
                
                # Clear discovery cache
                cache.clear_cache("settings_discovery")
                
                return str(new_file)
            except Exception:
                return None
        
        return None
    
    def _get_user_file_path(self, username: str) -> Optional[Path]:
        """
        Get user file path, checking both new nested structure and legacy flat structure.
        Prioritizes nested structure for forward compatibility.
        
        Args:
            username: User's username
            
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

# Standalone functions for button file imports (Mao standardization pattern)
def get_default_settings() -> Dict[str, Any]:
    """Standalone function for getting default settings"""
    manager = ApplicationSettingsManager()
    return manager.get_default_settings()

def get_user_settings(username: str) -> Dict[str, Any]:
    """Standalone function for getting user settings"""
    manager = ApplicationSettingsManager()
    return manager.get_user_settings(username)

def update_user_setting(username: str, setting_name: str, value: Any) -> bool:
    """Standalone function for updating user setting"""
    manager = ApplicationSettingsManager()
    return manager.update_user_setting(username, setting_name, value)

def discover_settings() -> Dict[str, SettingDefinition]:
    """Standalone function for discovering settings"""
    manager = ApplicationSettingsManager()
    return manager.discover_settings()
