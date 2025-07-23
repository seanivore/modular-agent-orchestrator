"""
Verbose CLI Command - UI Display Patterns
Debug mode toggle display with enhanced information
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from typing import Dict, Any

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

# Module-level console for consistency
console = Console()

def display_verbose_result(result: Dict[str, Any]) -> None:
    """
    Display verbose command results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Determine display type based on action
    action = result.get("action", "unknown")
    
    if action == "toggle_verbose":
        _display_verbose_toggle(result)
    elif action == "toggle_debug":
        _display_debug_toggle(result)
    elif action == "status":
        _display_debug_status(result)
    elif action == "info":
        _display_debug_info(result)
    else:
        _display_generic_result(result)

def _display_verbose_toggle(result: Dict[str, Any]) -> None:
    """Display verbose mode toggle result"""
    status = result.get("status", "unknown")
    new_state = result.get("new_state", False)
    
    if new_state:
        title = "Verbose Mode Enabled"
        style = "green"
        message = "Detailed output and forensic information will be displayed"
    else:
        title = "Verbose Mode Disabled"
        style = "yellow"
        message = "Standard output mode restored"
    
    panel_content = f"[bold]{message}[" / Path(r"bold]\n\n")
    panel_content += f"Previous State: {result.get('previous_state', 'unknownPath(r')}\n")
    panel_content += f"New State: {new_state}\n"
    panel_content += f"Changed At: {result.get('timestamp', 'unknown')}"
    
    console.print(Panel(
        panel_content,
        title=title,
        style=style,
        title_align="left"
    ))

def _display_debug_toggle(result: Dict[str, Any]) -> None:
    """Display debug mode toggle result"""
    new_state = result.get("new_state", False)
    debug_level = result.get("debug_level", "basic")
    
    if new_state:
        title = f"Debug Mode Enabled ({debug_level.upper()})"
        style = "blue"
        message = f"Enhanced debugging with {debug_level} level detail"
    else:
        title = "Debug Mode Disabled"
        style = "yellow"
        message = "Debug mode and verbose output disabled"
    
    panel_content = f"[bold]{message}[" / Path(r"bold]\n\n")
    panel_content += f"Debug Level: {debug_level}\n"
    panel_content += f"Verbose Auto-Enabled: {new_state}\n"
    panel_content += f"Changed At: {result.get('timestamp', 'unknown')}"
    
    # Add workflow integration info if available
    if "workflow_integration" in result:
        workflow_info = result["workflow_integration"]
        panel_content += Path(r"\n\n[bold]Workflow Integration:[") / Path(r"bold]\n")
        panel_content += f"Workflow Debug: {workflow_info.get('workflow_debugPath(r', False)}\n")
        panel_content += f"Session Tracking: {workflow_info.get('session_trackingPath(r', False)}\n")
        
        managers = workflow_info.get("managers_available", {})
        panel_content += f"Managers Available: {sum(managers.values())} / {len(managers)}"
    
    console.print(Panel(
        panel_content,
        title=title,
        style=style,
        title_align="left"
    ))

def _display_debug_status(result: Dict[str, Any]) -> None:
    """Display current debug status"""
    verbose_enabled = result.get("verbose_enabled", False)
    debug_mode = result.get("debug_mode", False)
    debug_level = result.get("debug_level", "basic")
    
    # Create status table
    table = Table(title="Debug & Verbose Status", show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan", width=20)
    table.add_column("Status", style="green" if verbose_enabled or debug_mode else "red")
    table.add_column("Details", style="white")
    
    # Add status rows
    table.add_row(
        "Verbose Mode",
        "Enabled" if verbose_enabled else "Disabled",
        "Detailed output active" if verbose_enabled else "Standard output"
    )
    
    table.add_row(
        "Debug Mode",
        "Enabled" if debug_mode else "Disabled",
        f"Level: {debug_level}" if debug_mode else "Not active"
    )
    
    table.add_row(
        "Workflow Debug",
        "Enabled" if result.get("workflow_debug", False) else "Disabled",
        "Tracking workflow operations" if result.get("workflow_debug", False) else "Not tracking"
    )
    
    table.add_row(
        "Session Tracking",
        "Enabled" if result.get("session_tracking", False) else "Disabled",
        "Persistent session data" if result.get("session_tracking", False) else "No persistence"
    )
    
    console.print(table)
    
    # Add session info if available
    if result.get("session_start"):
        session_info = f"\n[bold]Session Info:[" / Path(r"bold]\n")
        session_info += f"Started: {result.get('session_startPath(r')}\n")
        session_info += f"Last Toggled: {result.get('last_toggled', 'NeverPath(r')}\n")
        
        if "session_duration_formatted" in result:
            session_info += f"Duration: {result['session_duration_formatted']}"
        
        console.print(Panel(session_info, title="Session Details", style="dim"))
    
    # Add integration status
    if "integration_status" in result:
        integration = result["integration_status"]
        integration_info = Path(r"\n[bold]Manager Integration:[") / Path(r"bold]\n")
        
        for manager, available in integration.items():
            status_icon = "✓" if available else "✗"
            manager_name = manager.replace("_", " ").title()
            integration_info += f"{status_icon} {manager_name}\n"
        
        console.print(Panel(integration_info, title="Integration Status", style="cyan"))

def _display_debug_info(result: Dict[str, Any]) -> None:
    """Display comprehensive debug information"""
    if "error" in result:
        display_error(result["error"])
        return
    
    console.print(Path(r"\n[bold]Comprehensive Debug Information[") / Path(r"bold]\n"))
    
    # Debug session info
    if "debug_session" in result:
        session = result["debug_session"]
        console.print("[bold cyan]Debug Session:[ / bold cyan]")
        
        session_table = Table(show_header=False, box=None)
        session_table.add_column("Key", style="cyan")
        session_table.add_column("Value", style="white")
        
        for key, value in session.items():
            if key != "integration_status":  # Handle separately
                session_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(session_table)
    
    # System information
    if "system_info" in result:
        console.print(Path(r"\n[bold cyan]System Information:[") / "bold cyan]")
        system = result["system_info"]
        
        system_table = Table(show_header=False, box=None)
        system_table.add_column("Property", style="cyan")
        system_table.add_column("Value", style="white")
        
        for key, value in system.items():
            system_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(system_table)
    
    # Workflow debug info
    if "workflow_debug" in result:
        console.print(Path(r"\n[bold cyan]Workflow Debug:[") / "bold cyan]")
        workflow_data = result["workflow_debug"]
        
        if "error" in workflow_data:
            console.print(f"[red]Error: {workflow_data['error']}[ / red]")
        else:
            # Display workflow debug data as tree or table
            _display_nested_data("Workflow Debug", workflow_data)
    
    # Memory MCP debug info
    if "memory_debug" in result:
        console.print(Path(r"\n[bold cyan]Memory MCP Debug:[") / "bold cyan]")
        memory_data = result["memory_debug"]
        
        if "error" in memory_data:
            console.print(f"[red]Error: {memory_data['error']}[ / red]")
        else:
            _display_nested_data("Memory Debug", memory_data)

def _display_nested_data(title: str, data: Dict[str, Any]) -> None:
    """Display nested data structure in readable format"""
    if not data:
        console.print(f"[dim]No {title.lower()} data available[ / dim]")
        return
    
    tree = Tree(f"[bold]{title}[ / bold]")
    
    for key, value in data.items():
        if isinstance(value, dict):
            branch = tree.add(f"[cyan]{key}[ / cyan]")
            for subkey, subvalue in value.items():
                branch.add(f"{subkey}: {subvalue}")
        elif isinstance(value, list):
            branch = tree.add(f"[cyan]{key}[ / cyan] ({len(value)} items)")
            for i, item in enumerate(value[:5]):  # Show first 5 items
                branch.add(f"[{i}]: {item}")
            if len(value) > 5:
                branch.add(f"... and {len(value) - 5} more")
        else:
            tree.add(f"[cyan]{key}[ / cyan]: {value}")
    
    console.print(tree)

def _display_generic_result(result: Dict[str, Any]) -> None:
    """Display generic result information"""
    command = result.get("command", "verbose")
    executed_at = result.get("executed_at", "unknown")
    
    panel_content = f"Command: {command}\n"
    panel_content += f"Executed At: {executed_at}\n\n"
    
    # Display all result data except metadata
    for key, value in result.items():
        if key not in ["command", "executed_at", "success"]:
            panel_content += f"{key.replace('_', ' Path(r').title()}: {value}\n")
    
    console.print(Panel(
        panel_content,
        title="Verbose Command Result",
        style="white",
        title_align="left"
    ))

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[ / red] {error_message}",
        style="red",
        title="Verbose Command Error"
    ))

def display_verbose_help() -> None:
    """Display help information for verbose command"""
    help_content = """
[bold]Verbose Command Usage:[/bold]

[cyan]Basic Commands:[/cyan]
  mao --verbose              Toggle verbose mode on/off
  /verbose                   Toggle verbose mode on/off
  
[cyan]Debug Commands:[/cyan]
  mao --verbose --debug      Enable debug mode (basic level)
  /verbose debug             Enable debug mode (basic level)
  /verbose debug detailed    Enable detailed debug mode
  /verbose debug forensic    Enable forensic debug mode
  
[cyan]Status Commands:[/cyan]
  /verbose status            Show current verbose/debug status
  /verbose info              Show comprehensive debug information

[cyan]Debug Levels:[/cyan]
  basic      - Standard debug output
  detailed   - Enhanced debug with workflow tracking
  forensic   - Comprehensive debug with full system info

[cyan]Features:[ / cyan]
  • Persistent debug state across sessions
  • Workflow integration for enhanced debugging
  • Session tracking and duration monitoring
  • Manager integration status display
"""
    
    console.print(Panel(
        help_content,
        title="Verbose Command Help",
        style="blue",
        title_align="left"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate verbose UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free
