"""
Config CLI Command - UI Display Patterns
Essential data structure for config display
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager(), List

# Module-level console for consistency
console = Console()

def display_config_result(result: Dict[str, Any]) -> None:
    """
    Display config results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result from config.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Configuration operation failed"))
        return
    
    # Essential data structure for UI designers
    # Focus on data organization, not detailed formatting
    # Preserve creative freedom for actual interface design
    
    operation = result.get("operation", "view_settings")
    
    if operation == "view_settings":
        _display_settings_overview(result)
    elif operation == "discover_settings":
        _display_settings_discovery(result)
    elif operation in ["update_setting", "reset_setting"]:
        _display_setting_action(result)
    elif operation in ["export_config", "import_config"]:
        _display_config_transfer(result)
    else:
        _display_generic_result(result)

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / "red] {error_message}",
        style="red",
        title="Config Error"
    ))
    
    # Show helpful suggestions
    console.print(Path(r"\n[yellow]Suggestions:[") / "yellow]")
    suggestions = [
        "Ensure user is logged in for setting updates",
        "Check that setting names are valid", 
        "Verify setting values match expected types",
        "Try discovering settings to refresh available options"
    ]
    for suggestion in suggestions:
        console.print(f"  • {suggestion}")

def _display_settings_overview(result: Dict[str, Any]) -> None:
    """Display settings overview with sections"""
    user_info = result.get("user", {})
    settings = result.get("settings", {})
    sections = result.get("sections", {})
    
    # Header with user context
    title = f"Configuration Settings - {user_info.get('username', 'Default User')}"
    console.print(Panel(title, style="blue"))
    
    # Settings by section
    for section_name, setting_names in sections.items():
        console.print(fPath(r"\n[bold]{section_name}[") / "bold]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Current Value", style="green")
        table.add_column("Default", style="dim")
        table.add_column("Modified", justify="center")
        
        for setting_name in setting_names:
            if setting_name in settings:
                current_value = str(settings[setting_name])
                # This would need settings definitions for defaults
                table.add_row(setting_name, current_value, "-", "")
        
        console.print(table)
    
    console.print(fPath(r"\n[dim]Total settings: {result.get(')total_settings', 0)}[" / "dim]")

def _display_settings_discovery(result: Dict[str, Any]) -> None:
    """Display settings discovery results"""
    console.print(Panel("Settings Discovery Results", style="green"))
    
    total_settings = result.get("total_settings", 0)
    sections = result.get("sections", {})
    
    console.print(f"Found [bold]{total_settings}[" / "bold] configurable settings")
    console.print(f"Organized into [bold]{len(sections)}[" / Path(r"bold] sections:\n"))
    
    for section_name, setting_names in sections.items():
        console.print(f"  [cyan]{section_name}[" / "cyan]: {len(setting_names)} settings")

def _display_setting_action(result: Dict[str, Any]) -> None:
    """Display setting update" / "reset confirmation"""
    operation = result.get("operation")
    setting_name = result.get("setting_name")
    
    if operation == "update_setting":
        new_value = result.get("new_value")
        console.print(Panel(
            f"Setting '[cyan]{setting_name}[" / "cyan]' updated to '[green]{new_value}[" / "green]'",
            title="Setting Updated",
            style="green"
        ))
    elif operation == "reset_setting":
        default_value = result.get("default_value")
        console.print(Panel(
            f"Setting '[cyan]{setting_name}[" / "cyan]' reset to default '[yellow]{default_value}[" / "yellow]'",
            title="Setting Reset",
            style="yellow"
        ))

def _display_config_transfer(result: Dict[str, Any]) -> None:
    """Display config import" / "export results"""
    operation = result.get("operation")
    
    if operation == "export_config":
        export_data = result.get("export_data", {})
        export_info = export_data.get("export_info", {})
        console.print(Panel(
            f"Configuration exported for {export_info.get('username', 'UnknownPath(r')}\n") +
            f"Settings count: {export_info.get('settings_count', 0)}",
            title="Config Export Complete",
            style="blue"
        ))
    elif operation == "import_config":
        imported_count = result.get("imported_count", 0)
        failed_count = len(result.get("failed_settings", []))
        console.print(Panel(
            f"Imported: [green]{imported_count}[" / Path(r"green] settings\n") +
            f"Failed: [red]{failed_count}[" / "red] settings",
            title="Config Import Complete",
            style="green" if failed_count == 0 else "yellow"
        ))

def _display_generic_result(result: Dict[str, Any]) -> None:
    """Display generic operation result"""
    operation = result.get("operation", "Unknown")
    message = result.get("message", "Operation completed")
    
    console.print(Panel(
        fPath(r"Operation: {operation}\n{message}"),
        title="Config Operation",
        style="blue"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate config UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free