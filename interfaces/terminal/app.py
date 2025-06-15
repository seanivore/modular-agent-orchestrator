# interfaces/terminal/app.py - Main Terminal Application

import asyncio
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header
from textual.binding import Binding

from .styles import MAO_THEME, MAO_COLORS
from .components.main_menu import MainMenu
from .navigation import NavigationManager


class MaoTerminalApp(App):
    """
    Beautiful Terminal UI for MAO - AI Workflow Orchestration
    Professional interface for creating, managing, and executing AI workflows
    """
    
    CSS_PATH = "styles.css"
    TITLE = "Mao - AI Workflow Orchestrator"
    SUB_TITLE = "Professional terminal interface for AI collaboration"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("ctrl+c", "quit", "Quit", priority=True),
        Binding("escape", "back", "Back"),
        Binding("h,f1", "help", "Help"),
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
        """Initialize the application."""
        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE
        self.current_screen = "main-menu"
        self.navigation.push("main-menu")
        
    async def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
        
    async def action_back(self) -> None:
        """Navigate back."""
        if self.navigation.can_go_back():
            previous_screen = self.navigation.pop()
            await self.switch_to_screen(previous_screen)
            
    async def action_help(self) -> None:
        """Show help."""
        self.notify("Help: q=quit, esc=back, tab=navigate, enter=select")
        
    async def switch_to_screen(self, screen_name: str) -> None:
        """Switch to different screen."""
        # Implementation will be completed by multistage integration
        self.notify(f"Switching to: {screen_name}")


def main():
    """Launch the beautiful terminal UI."""
    app = MaoTerminalApp()
    app.run()


if __name__ == "__main__":
    main()