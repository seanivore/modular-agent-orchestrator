# mao_terminal_app.py - Main Terminal Application Entry Point

import asyncio
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header
from textual.binding import Binding

from ui.styles import MAO_THEME
from ui.main_menu import MainMenu
from ui.workflow_wizard import WorkflowWizard
from ui.workflow_manager import WorkflowManager
from ui.command_runner import CommandRunner
from ui.settings_screen import SettingsScreen
from ui.navigation import NavigationManager


class MaoTerminalApp(App):
    """
    Mao Terminal Application - Beautiful AI Workflow Orchestration
    
    A premium terminal interface for creating, managing, and executing
    AI agent workflows with elegant UX and powerful functionality.
    """
    
    CSS_PATH = "ui/styles.css"
    TITLE = "Mao - AI Workflow Orchestrator"
    SUB_TITLE = "Beautiful terminal interface for AI collaboration"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("h", "help", "Help"),
        Binding("ctrl+c", "quit", "Quit", priority=True),
        Binding("escape", "back", "Back"),
        Binding("f1", "help", "Help"),
    ]
    
    def __init__(self):
        super().__init__()
        self.console = Console(theme=MAO_THEME)
        self.navigation = NavigationManager()
        self.current_screen = None
        
    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        yield Header(show_clock=True)
        yield Container(
            MainMenu(id="main-menu"),
            id="main-container"
        )
        yield Footer()
        
    def on_mount(self) -> None:
        """Initialize the application on startup."""
        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE
        
        # Set initial screen
        self.current_screen = "main-menu"
        self.navigation.push("main-menu")
        
        # Welcome message
        self.notify("Welcome to Mao! 🚀", title="AI Workflow Orchestrator", timeout=3)
        
    async def action_quit(self) -> None:
        """Graceful application shutdown."""
        self.notify("Shutting down Mao...", title="Goodbye! 👋")
        await asyncio.sleep(0.5)  # Brief pause for user feedback
        self.exit()
        
    async def action_back(self) -> None:
        """Navigate back to previous screen."""
        if self.navigation.can_go_back():
            previous_screen = self.navigation.pop()
            await self.switch_to_screen(previous_screen)
        else:
            self.notify("Already at main menu", severity="information")
            
    async def action_help(self) -> None:
        """Show contextual help."""
        help_text = Text.assemble(
            ("Mao Keyboard Shortcuts\n\n", "bold blue"),
            ("q, Ctrl+C", "bold"), (" - Quit application\n"),
            ("h, F1", "bold"), (" - Show this help\n"),
            ("Escape", "bold"), (" - Go back\n"),
            ("Tab", "bold"), (" - Navigate between options\n"),
            ("Enter", "bold"), (" - Select option\n"),
        )
        
        self.push_screen(
            Panel(
                help_text,
                title="Help",
                border_style="blue",
                padding=(1, 2)
            )
        )
        
    async def switch_to_screen(self, screen_name: str) -> None:
        """Switch to a different screen with smooth transition."""
        container = self.query_one("#main-container")
        
        # Remove current screen
        if self.current_screen:
            current_widget = container.query_one(f"#{self.current_screen}")
            current_widget.remove()
            
        # Add new screen
        if screen_name == "main-menu":
            container.mount(MainMenu(id="main-menu"))
        elif screen_name == "workflow-wizard":
            container.mount(WorkflowWizard(id="workflow-wizard"))
        elif screen_name == "workflow-manager":
            container.mount(WorkflowManager(id="workflow-manager"))
        elif screen_name == "command-runner":
            container.mount(CommandRunner(id="command-runner"))
        elif screen_name == "settings":
            container.mount(SettingsScreen(id="settings"))
            
        self.current_screen = screen_name
        self.navigation.push(screen_name)
        
    def on_main_menu_option_selected(self, message) -> None:
        """Handle main menu selection."""
        option = message.option
        
        if option == "new_workflow":
            asyncio.create_task(self.switch_to_screen("workflow-wizard"))
        elif option == "manage_workflows":
            asyncio.create_task(self.switch_to_screen("workflow-manager"))
        elif option == "run_workflow":
            asyncio.create_task(self.switch_to_screen("command-runner"))
        elif option == "settings":
            asyncio.create_task(self.switch_to_screen("settings"))
        elif option == "quit":
            asyncio.create_task(self.action_quit())


def main():
    """Main entry point for Mao terminal application."""
    try:
        # Ensure required directories exist
        Path("workflows").mkdir(exist_ok=True)
        Path("ui/components").mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
        # Launch the application
        app = MaoTerminalApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error starting Mao:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# ui/__init__.py - UI Package Initialization

"""
Mao Terminal UI Package

Beautiful, modern terminal interface components for AI workflow orchestration.
Inspired by the best terminal UX practices with a focus on elegance and usability.
"""

from .styles import MAO_THEME, MAO_COLORS
from .main_menu import MainMenu
from .navigation import NavigationManager

__version__ = "0.1.0"
__all__ = [
    "MAO_THEME",
    "MAO_COLORS", 
    "MainMenu",
    "NavigationManager"
]


# ui/styles.py - Centralized Color Schemes, Typography, Layout Constants

from rich.theme import Theme
from rich.style import Style
from typing import Dict, Any

# Color Palette - Inspired by modern terminal themes with Mao personality
MAO_COLORS = {
    # Primary brand colors
    "primary": "#00D4FF",        # Bright cyan - main accent
    "primary_dark": "#0088CC",   # Darker cyan for contrast
    "secondary": "#FF6B9D",      # Soft pink - secondary accent
    "accent": "#FFD93D",         # Warm yellow - highlights
    
    # Semantic colors
    "success": "#00FF88",        # Bright green
    "warning": "#FFB347",        # Orange
    "error": "#FF4757",          # Red
    "info": "#74B9FF",           # Light blue
    
    # Interface colors
    "background": "#0D1117",     # Deep dark blue
    "surface": "#161B22",        # Slightly lighter dark
    "surface_hover": "#21262D",  # Hover state
    "border": "#30363D",         # Subtle borders
    "text_primary": "#F0F6FC",   # High contrast white
    "text_secondary": "#8B949E", # Muted text
    "text_dim": "#6E7681",       # Very subtle text
    
    # Workflow status colors  
    "active": "#00FF88",         # Currently running
    "pending": "#FFD93D",        # Waiting to run
    "completed": "#00D4FF",      # Successfully finished
    "failed": "#FF4757",         # Error state
    "draft": "#8B949E",          # Not yet configured
}

# Rich theme configuration
MAO_THEME = Theme({
    # Base styles
    "primary": MAO_COLORS["primary"],
    "secondary": MAO_COLORS["secondary"], 
    "accent": MAO_COLORS["accent"],
    "success": MAO_COLORS["success"],
    "warning": MAO_COLORS["warning"],
    "error": MAO_COLORS["error"],
    "info": MAO_COLORS["info"],
    
    # Text styles
    "text.primary": MAO_COLORS["text_primary"],
    "text.secondary": MAO_COLORS["text_secondary"],
    "text.dim": MAO_COLORS["text_dim"],
    
    # Component styles
    "panel.border": MAO_COLORS["border"],
    "panel.title": f"bold {MAO_COLORS['primary']}",
    "button.focus": f"bold {MAO_COLORS['primary']} on {MAO_COLORS['surface_hover']}",
    "menu.selected": f"bold {MAO_COLORS['text_primary']} on {MAO_COLORS['primary']}",
    "progress.bar": MAO_COLORS["primary"],
    "progress.percentage": MAO_COLORS["accent"],
    
    # Workflow status styles
    "status.active": MAO_COLORS["active"],
    "status.pending": MAO_COLORS["pending"], 
    "status.completed": MAO_COLORS["completed"],
    "status.failed": MAO_COLORS["failed"],
    "status.draft": MAO_COLORS["draft"],
})

# Typography hierarchy
TYPOGRAPHY = {
    "title": Style(color=MAO_COLORS["primary"], bold=True),
    "subtitle": Style(color=MAO_COLORS["text_secondary"], italic=True),
    "heading": Style(color=MAO_COLORS["text_primary"], bold=True),
    "body": Style(color=MAO_COLORS["text_primary"]),
    "caption": Style(color=MAO_COLORS["text_dim"]),
    "code": Style(color=MAO_COLORS["accent"], bold=True),
    "link": Style(color=MAO_COLORS["info"], underline=True),
}

# Layout constants
LAYOUT = {
    "padding": 2,
    "margin": 1,
    "border_radius": 1,
    "min_width": 80,
    "max_width": 120,
    "content_width": 100,
}

# Animation settings
ANIMATIONS = {
    "transition_duration": 0.3,
    "fade_duration": 0.2,
    "bounce_duration": 0.4,
    "easing": "ease_out",
}

# Component styling helpers
def get_panel_style(variant: str = "default") -> Dict[str, Any]:
    """Get consistent panel styling."""
    base_style = {
        "border_style": "rounded",
        "padding": (1, 2),
        "highlight": True,
    }
    
    variants = {
        "default": {"title_style": "primary", "border_style": MAO_COLORS["border"]},
        "success": {"title_style": "success", "border_style": MAO_COLORS["success"]},
        "warning": {"title_style": "warning", "border_style": MAO_COLORS["warning"]},
        "error": {"title_style": "error", "border_style": MAO_COLORS["error"]},
        "info": {"title_style": "info", "border_style": MAO_COLORS["info"]},
    }
    
    return {**base_style, **variants.get(variant, variants["default"])}

def get_button_style(state: str = "normal") -> Style:
    """Get consistent button styling."""
    states = {
        "normal": Style(color=MAO_COLORS["text_primary"]),
        "hover": Style(color=MAO_COLORS["primary"], bold=True),
        "active": Style(color=MAO_COLORS["text_primary"], bold=True, bgcolor=MAO_COLORS["primary"]),
        "disabled": Style(color=MAO_COLORS["text_dim"]),
    }
    return states.get(state, states["normal"])


# config.py - Application Configuration and Settings

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LLMConfig:
    """LLM configuration settings."""
    default_model: str = "claude-sonnet-4"
    api_key_path: str = "~/.anthropic/api_key"
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 30


@dataclass
class UIConfig:
    """UI configuration settings."""
    theme: str = "default"
    animations: bool = True
    notifications: bool = True
    auto_save: bool = True
    refresh_rate: int = 60


@dataclass
class WorkflowConfig:
    """Workflow configuration settings."""
    default_directory: str = "./workflows"
    backup_directory: str = "./workflows/backups"
    auto_backup: bool = True
    max_parallel_agents: int = 5
    default_timeout: int = 300


@dataclass
class MaoConfig:
    """Main Mao application configuration."""
    llm: LLMConfig
    ui: UIConfig
    workflow: WorkflowConfig
    version: str = "0.1.0"
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'MaoConfig':
        """Load configuration from file."""
        if config_path is None:
            config_path = Path.home() / ".mao" / "config.json"
            
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    
                return cls(
                    llm=LLMConfig(**data.get('llm', {})),
                    ui=UIConfig(**data.get('ui', {})),
                    workflow=WorkflowConfig(**data.get('workflow', {})),
                    version=data.get('version', '0.1.0')
                )
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                
        # Return default configuration
        return cls(
            llm=LLMConfig(),
            ui=UIConfig(), 
            workflow=WorkflowConfig()
        )
        
    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = Path.home() / ".mao" / "config.json"
            
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(asdict(self), f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
            
    def get_workflow_directory(self) -> Path:
        """Get the workflow directory as a Path object."""
        return Path(self.workflow.default_directory).expanduser().resolve()
        
    def get_backup_directory(self) -> Path:
        """Get the backup directory as a Path object.""" 
        return Path(self.workflow.backup_directory).expanduser().resolve()


# Global configuration instance
_config = None

def get_config() -> MaoConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = MaoConfig.load()
    return _config

def reload_config() -> MaoConfig:
    """Reload configuration from file."""
    global _config
    _config = MaoConfig.load()
    return _config