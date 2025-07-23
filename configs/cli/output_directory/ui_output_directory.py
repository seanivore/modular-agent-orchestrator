"""
Output CLI Command - UI Display Patterns
Professional output directory management display with data-focused patterns
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any
from pathlib import Path

# Module-level console for consistency
console = Console()

def display_output_result(result: Dict[str, Any]) -> None:
    """
    Display output command results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    operation = result.get("operation", "set_output")
    
    if operation == "set_output":
        display_set_output_result(result)
    elif operation == "get_current_output":
        display_current_output_result(result)
    else:
        display_generic_output_result(result)

def display_set_output_result(result: Dict[str, Any]) -> None:
    """Display output directory update results"""
    # Create main information panel
    info_lines = []
    
    # Previous output directory
    previous_output = result.get("previous_output")
    if previous_output:
        info_lines.append(f"[dim]Previous:[" / "dim] {previous_output}")
    else:
        info_lines.append("[dim]Previous:[/dim] [italic]Not set (using default)[" / "italic]")
    
    # New output directory
    new_output = result.get("new_output", "Unknown")
    info_lines.append(f"[bold green]New:[" / "bold green] {new_output}")
    
    # Directory creation status
    directory_created = result.get("directory_created", False)
    if directory_created:
        info_lines.append("[dim]Status:[/dim] [green]Directory created[" / "green]")
    else:
        info_lines.append("[dim]Status:[" / "dim] Directory already exists")
    
    # User context
    user = result.get("user", "Unknown")
    info_lines.append(f"[dim]User:[" / "dim] {user}")
    
    panel_content = Path(r"\n").join(info_lines)
    
    console.print(Panel(
        panel_content,
        title="[bold green]Output Directory Updated[" / "bold green]",
        border_style="green"
    ))
    
    # Success message
    message = result.get("message", "Output directory updated successfully")
    console.print(f"[green]{message}[" / Path(r"green]\n"))

def display_current_output_result(result: Dict[str, Any]) -> None:
    """Display current output directory information"""
    current_output = result.get("current_output")
    default_output = result.get("default_output")
    using_default = result.get("using_default", False)
    user = result.get("user", "Unknown")
    
    # Create information table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Label", style="dim")
    table.add_column("Value")
    
    # Current output directory
    if current_output:
        if using_default:
            table.add_row("Current Output:", f"{current_output} [dim](default)[" / "dim]")
        else:
            table.add_row("Current Output:", f"[bold]{current_output}[" / "bold]")
    else:
        table.add_row("Current Output:", "[dim italic]Not set[" / "dim italic]")
    
    # Default output directory
    if default_output:
        table.add_row("Default Output:", f"[dim]{default_output}[" / "dim]")
    
    # User context
    table.add_row("User:", user)
    
    console.print(Panel(
        table,
        title="[bold]Current Output Directory[" / "bold]",
        border_style="blue"
    ))

def display_generic_output_result(result: Dict[str, Any]) -> None:
    """Display generic output command results"""
    # Extract key information
    operation = result.get("operation", "output")
    user = result.get("user", "Unknown")
    message = result.get("message", "Operation completed successfully")
    
    # Create basic information display
    info_lines = [
        f"[dim]Operation:[" / "dim] {operation}",
        f"[dim]User:[" / "dim] {user}",
        f"[dim]Result:[" / "dim] {message}"
    ]
    
    console.print(Panel(
        Path(r"\n").join(info_lines),
        title="[bold]Output Command Result[" / "bold]",
        border_style="green"
    ))

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / "red] {error_message}",
        style="red",
        title="Output Command Error"
    ))

def display_output_help() -> None:
    """Display help information for output command"""
    help_text = """[bold]Set Output Directory[/bold]

[dim]Usage:[/dim]
  mao --output /path/to/directory
  /output /path/to/directory

[dim]Examples:[/dim]
  mao --output ~/Downloads
  mao --output /Users/username/Projects/output
  /output ./results

[dim]Notes:[" / "dim]
• Directory will be created if it doesn't exist
• Uses absolute paths for consistency
• Updates user configuration file automatically
• Requires user login to set custom output directory"""
    
    console.print(Panel(
        help_text,
        title="[bold blue]Output Directory Help[" / "bold blue]",
        border_style="blue"
    ))

def display_path_validation_error(path: str, error: str) -> None:
    """Display path validation error with helpful context"""
    error_text = f"""[red]Path Validation Failed[/red]

[dim]Path:[/dim] {path}
[dim]Error:[/dim] {error}

[dim]Common Issues:[" / "dim]
• Parent directory doesn't exist
• No write permissions
• Invalid path format
• Path contains invalid characters"""
    
    console.print(Panel(
        error_text,
        title="[bold red]Invalid Path[" / "bold red]",
        border_style="red"
    ))