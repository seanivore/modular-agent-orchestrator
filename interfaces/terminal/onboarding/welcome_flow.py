#!/usr/bin/env python3
"""
MAO Welcome Flow and User Onboarding
Implements new user setup with theme selection and user identification
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from textual.widget import Widget
from textual.widgets import Static, Input, RadioSet, RadioButton
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.reactive import reactive

from ..visual_language import MAO_COLORS, MAOVisualProtocol


class UserManager:
    """Manages user identification and settings persistence"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.user_dir = self.config_dir / "user"
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_user_id(self, username: str) -> str:
        """Generate user ID from username using MAO's mathematical approach"""
        
        # Character count operations
        char_count = len(username)
        doubled_count = char_count * 2
        
        # ASCII values sum
        ascii_sum = sum(ord(char) for char in username.lower())
        
        # Apply mathematical operations similar to MAO's uid system
        operations = [
            ascii_sum + char_count,           # add
            ascii_sum * doubled_count % 1000, # multiply with modulo
            abs(ascii_sum - doubled_count),   # subtract
        ]
        
        # Create user ID
        final_value = sum(operations) % 10000
        user_id = f"user-{final_value:04d}"
        
        return user_id
        
    def user_exists(self, username: str) -> bool:
        """Check if user already exists"""
        user_file = self.user_dir / f"user_{username}.json"
        return user_file.exists()
        
    def load_user_settings(self, username: str) -> Optional[Dict[str, Any]]:
        """Load user settings from JSON file"""
        user_file = self.user_dir / f"user_{username}.json"
        
        if not user_file.exists():
            return None
            
        try:
            with open(user_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
            
    def save_user_settings(self, username: str, settings: Dict[str, Any]) -> bool:
        """Save user settings to JSON file"""
        user_file = self.user_dir / f"user_{username}.json"
        
        # Generate user ID if not present
        if 'user_id' not in settings:
            settings['user_id'] = self.generate_user_id(username)
            
        # Add metadata
        settings.update({
            'username': username,
            'created_at': settings.get('created_at', datetime.now().isoformat()),
            'last_login': datetime.now().isoformat()
        })
        
        try:
            with open(user_file, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except IOError:
            return False
            
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default user settings"""
        return {
            'quick_launch': 'always',
            'favorite_model': 'claude-sonnet-4',
            'default_provider': 'anthropic direct',
            'theme': 'dark mode CVD',
            'tone_notification': 'one time, no push',
            'cat_vibes': 'I love it',
            'double_texting': 'always'
        }


class ThemePreview(Widget):
    """Theme preview widget showing visual examples"""
    
    def __init__(self, theme_name: str):
        super().__init__()
        self.theme_name = theme_name
        self.visual_protocol = MAOVisualProtocol()
        
    def compose(self):
        """Compose theme preview"""
        preview_text = self.get_preview_text()
        
        yield Container(
            Static("Preview", classes="preview-title"),
            Static(preview_text, markup=True, classes="preview-content"),
            classes="theme-preview"
        )
        
    def get_preview_text(self) -> str:
        """Get preview text for theme"""
        
        # Theme-specific color mappings from NEW_USER_FLOW.md
        if "dark mode" in self.theme_name.lower():
            if "cvd" in self.theme_name.lower():
                # Dark Mode Colorblind-Friendly
                colors = {
                    'text': '#ffffff',
                    'removal': '#6d1813', 
                    'addition': '#18516d'
                }
            else:
                # Regular Dark Mode
                colors = {
                    'text': '#ffffff',
                    'removal': '#6b5251',
                    'addition': '#506d51'
                }
        else:
            if "cvd" in self.theme_name.lower():
                # Light Mode Colorblind-Friendly  
                colors = {
                    'text': '#11100f',
                    'removal': '#bea4a3',
                    'addition': '#87a4c0'
                }
            else:
                # Regular Light Mode
                colors = {
                    'text': '#131313', 
                    'removal': '#bf88a4',
                    'addition': '#6ca36c'
                }
                
        preview_lines = [
            f"[{colors['text']}]1   standard ~(=^‥^) {{[/]",
            f"[{colors['removal']}]2 -    removed (\"Bye, mao.\");[/]",
            f"[{colors['addition']}]2 +    addition (\"Mao!\");[/]",
            f"[{colors['text']}]3   }}[/]"
        ]
        
        return '\n'.join(preview_lines)


class ThemeSelector(Widget):
    """Theme selection widget with previews"""
    
    selected_theme = reactive("dark mode CVD")
    
    def __init__(self):
        super().__init__()
        self.themes = [
            "dark mode",
            "light mode", 
            "dark mode CVD",
            "light mode CVD",
            "dark mode ANSI colors only",
            "light mode ANSI colors only"
        ]
        
    def compose(self):
        """Compose theme selector"""
        
        radio_buttons = []
        for i, theme in enumerate(self.themes):
            is_default = theme == "dark mode CVD"
            radio_buttons.append(
                RadioButton(f"{i+1}. {theme}", value=is_default, id=f"theme-{i}")
            )
            
        yield Vertical(
            Static("Which text style looks best on your screen?", classes="theme-question"),
            RadioSet(*radio_buttons, id="theme-radio-set"),
            ThemePreview(self.selected_theme),
            id="theme-selector"
        )
        
    async def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle theme selection change"""
        if event.pressed:
            # Extract theme index from button ID
            button_id = event.pressed.id
            if button_id and button_id.startswith("theme-"):
                try:
                    theme_index = int(button_id.split("-")[1])
                    self.selected_theme = self.themes[theme_index]
                    
                    # Update preview
                    preview = self.query_one(ThemePreview)
                    await preview.remove()
                    new_preview = ThemePreview(self.selected_theme)
                    await self.mount(new_preview)
                except (ValueError, IndexError):
                    pass


class UserLoginScreen(ModalScreen):
    """User login/identification screen"""
    
    def __init__(self, user_manager: UserManager):
        super().__init__()
        self.user_manager = user_manager
        self.visual_protocol = MAOVisualProtocol()
        
    def compose(self):
        """Compose login screen"""
        
        yield Container(
            # MAO welcome header
            Static(
                f"[{MAO_COLORS['pink']}]~(=^‥^)  Mao welcomes you![/]",
                classes="welcome-header"
            ),
            
            # Login prompt
            Vertical(
                Static(
                    f"[{MAO_COLORS['yellow']}]●[/]   What is your name?",
                    classes="login-prompt"
                ),
                Static(
                    f"[{MAO_COLORS['light_brown']}]    └ Please enter User ID to continue[/]",
                    classes="login-subtext"
                ),
                
                # Input field
                Input(
                    placeholder="Username (6-20 alpha-numeric characters)",
                    id="username-input"
                ),
                
                # Help text
                Static(
                    f"[{MAO_COLORS['gray']}]? 6-20 alpha-numeric characters[/]",
                    classes="help-text"
                ),
                
                id="login-form"
            ),
            
            id="login-container"
        )
        
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle username submission"""
        username = event.value.strip()
        
        if not self.validate_username(username):
            # Show error message
            error_msg = Static(
                f"[{MAO_COLORS['error']}]Invalid username. Use 6-20 alpha-numeric characters.[/]",
                classes="error-message"
            )
            await self.mount(error_msg)
            return
            
        # Check if user exists
        if self.user_manager.user_exists(username):
            # Load existing user
            settings = self.user_manager.load_user_settings(username)
            self.dismiss({"username": username, "settings": settings, "new_user": False})
        else:
            # New user - proceed to theme selection
            self.dismiss({"username": username, "settings": None, "new_user": True})
            
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not 6 <= len(username) <= 20:
            return False
        return username.isalnum()


class ThemeSelectionScreen(ModalScreen):
    """Theme selection screen for new users"""
    
    def __init__(self, username: str, user_manager: UserManager):
        super().__init__()
        self.username = username
        self.user_manager = user_manager
        self.visual_protocol = MAOVisualProtocol()
        
    def compose(self):
        """Compose theme selection screen"""
        
        # Show conversation-style progression
        conversation = [
            f"[{MAO_COLORS['gray']}]>   {self.username}[/]",
            "",
            f"[{MAO_COLORS['yellow']}]●[/]   Mao, {self.username}!",
            f"[{MAO_COLORS['light_brown']}]    └ This is your first time here[/]",
            "",
            f"[{MAO_COLORS['yellow']}]●[/]   We won't ask you again, mao.",
            f"[{MAO_COLORS['light_brown']}]    └ We'll save your settings to your User ID[/]",
            f"[{MAO_COLORS['gray']}]      Change this and other settings with /config[/]",
            ""
        ]
        
        yield Container(
            # MAO welcome header
            Static(
                f"[{MAO_COLORS['pink']}]~(=^‥^)  Mao welcomes you![/]",
                classes="welcome-header"
            ),
            
            # Conversation history
            Static('\n'.join(conversation), markup=True, classes="conversation"),
            
            # Theme selector
            ThemeSelector(),
            
            # Continue button
            Static(
                f"[{MAO_COLORS['gray']}]Press Enter to continue[/]",
                classes="continue-hint"
            ),
            
            id="theme-selection-container"
        )
        
    async def on_key(self, event) -> None:
        """Handle key press"""
        if event.key == "enter":
            # Get selected theme
            theme_selector = self.query_one(ThemeSelector)
            selected_theme = theme_selector.selected_theme
            
            # Create user settings
            settings = self.user_manager.get_default_settings()
            settings['theme'] = selected_theme
            
            # Save user
            if self.user_manager.save_user_settings(self.username, settings):
                self.dismiss({
                    "username": self.username,
                    "settings": settings,
                    "new_user": True,
                    "success": True
                })
            else:
                # Show error
                error_msg = Static(
                    f"[{MAO_COLORS['error']}]Failed to save user settings.[/]",
                    classes="error-message"
                )
                await self.mount(error_msg)


class WelcomeFlow:
    """
    Main welcome flow coordinator
    Handles the complete user onboarding process
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.user_manager = UserManager(config_dir)
        self.visual_protocol = MAOVisualProtocol()
        
    async def start_login_flow(self, app) -> Dict[str, Any]:
        """Start the complete login flow"""
        
        # Show login screen
        login_screen = UserLoginScreen(self.user_manager)
        login_result = await app.push_screen_wait(login_screen)
        
        if login_result["new_user"]:
            # Show theme selection for new users
            theme_screen = ThemeSelectionScreen(login_result["username"], self.user_manager)
            theme_result = await app.push_screen_wait(theme_screen)
            return theme_result
        else:
            # Existing user
            return login_result
            
    def get_last_user(self) -> Optional[Dict[str, Any]]:
        """Get the last logged in user for quick launch"""
        
        # Look for most recently modified user file
        user_files = list(self.user_manager.user_dir.glob("user_*.json"))
        
        if not user_files:
            return None
            
        # Sort by modification time
        latest_file = max(user_files, key=lambda f: f.stat().st_mtime)
        
        try:
            with open(latest_file) as f:
                settings = json.load(f)
                return {
                    "username": settings.get("username"),
                    "settings": settings,
                    "new_user": False
                }
        except (json.JSONDecodeError, IOError):
            return None
            
    def should_auto_login(self, settings: Dict[str, Any]) -> bool:
        """Check if should auto-login based on quick_launch setting"""
        
        quick_launch = settings.get('quick_launch', 'always')
        return quick_launch in ['always', 'continue only']


# Export key components
__all__ = [
    'WelcomeFlow',
    'UserManager', 
    'UserLoginScreen',
    'ThemeSelectionScreen'
]