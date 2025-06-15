# interfaces/terminal/components/main_menu.py - Main Navigation Menu

from textual.widgets import Static
from textual.containers import Vertical
from textual.message import Message
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table

from ..styles import MAO_COLORS, get_panel_style


class MainMenu(Static):
    """
    Beautiful main menu interface - professional navigation hub
    """
    
    class OptionSelected(Message):
        """Message sent when menu option is selected."""
        def __init__(self, option: str) -> None:
            self.option = option
            super().__init__()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_index = 0
        self.options = [
            ("new_workflow", "Create New Workflow", "Set up a new AI workflow"),
            ("manage_workflows", "Manage Workflows", "View and edit existing workflows"),
            ("run_workflow", "Run Workflow", "Execute a workflow"),
            ("settings", "Settings", "Configure Mao preferences"),
            ("help", "Help", "Documentation and support"),
            ("quit", "Quit", "Exit Mao")
        ]
    
    def compose(self):
        """Compose the main menu layout."""
        # Welcome header
        welcome_text = Text.assemble(
            ("Welcome to ", "white"),
            ("Mao", f"bold {MAO_COLORS['primary']}"),
            ("\n", "white"),
            ("AI Workflow Orchestrator", f"{MAO_COLORS['text_secondary']} italic"),
        )
        
        welcome_panel = Panel(
            Align.center(welcome_text),
            title="AI-Powered Development",
            **get_panel_style("primary")
        )
        
        # Menu options
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style=f"bold {MAO_COLORS['text_primary']}")
        menu_table.add_column("Description", style=MAO_COLORS['text_secondary'])
        
        for i, (key, label, description) in enumerate(self.options):
            if i == self.selected_index:
                menu_table.add_row(
                    f"▶ {label}",
                    description,
                    style=f"bold {MAO_COLORS['primary']}"
                )
            else:
                menu_table.add_row(f"  {label}", description)
        
        menu_panel = Panel(
            menu_table,
            title="Main Menu",
            **get_panel_style("default")
        )
        
        # Status footer
        status_text = Text.assemble(
            ("Status: ", "bold"),
            ("Ready", f"bold {MAO_COLORS['success']}"),
            (" | Version: ", ""),
            ("0.1.0", f"{MAO_COLORS['text_dim']}")
        )
        
        status_panel = Panel(
            Align.center(status_text),
            **get_panel_style("default")
        )
        
        with Vertical():
            yield Static(welcome_panel)
            yield Static(menu_panel) 
            yield Static(status_panel)
    
    def on_key(self, event) -> None:
        """Handle keyboard navigation."""
        if event.key == "down" or event.key == "j":
            self.selected_index = min(self.selected_index + 1, len(self.options) - 1)
            self.refresh()
        elif event.key == "up" or event.key == "k":
            self.selected_index = max(self.selected_index - 1, 0)
            self.refresh()
        elif event.key == "enter":
            option_key = self.options[self.selected_index][0]
            self.post_message(self.OptionSelected(option_key))