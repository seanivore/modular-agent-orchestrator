"""
Goal CLI Command - UI Display Patterns
Professional terminal display for workflow creation results
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

# Standard cache instance
cache = CacheManager()

# Module-level console for consistency
console = Console()

def display_goal_result(result: Dict[str, Any]) -> None:
    """
    Display goal command results with consistent CLI UI patterns.
    
    Args:
        result: Goal command execution result
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        if result.get("details"):
            console.print(f"\n[dim]Details: {result['details']}[/dim]")
        return
    
    # Display successful workflow creation
    display_success_result(result)

def display_success_result(result: Dict[str, Any]) -> None:
    """Display successful workflow creation with structured information"""
    
    # Header panel with success message
    console.print(Panel(
        f"[green]Workflow Created Successfully[/green]\n"
        f"[bold]{result.get('message', 'Workflow ready for execution')}[/bold]",
        title="Goal → Workflow",
        style="green"
    ))
    
    # Workflow details table
    details_table = Table(show_header=False, box=None, padding=(0, 2))
    details_table.add_column("Label", style="dim", width=20)
    details_table.add_column("Value", style="bold")
    
    if result.get("workflow_id"):
        details_table.add_row("Workflow ID:", result["workflow_id"])
    
    if result.get("custom_command"):
        details_table.add_row("Command:", f"[cyan]{result['custom_command']}[/cyan]")
    
    if result.get("use_case_directory"):
        details_table.add_row("Directory:", result["use_case_directory"])
    
    console.print(details_table)
    
    # Next steps section
    if result.get("next_steps"):
        console.print(f"\n[bold]Next Steps:[/bold]")
        console.print(f"• {result['next_steps']}")
    
    # Show workflow ready status
    if result.get("ready_to_execute"):
        console.print(f"\n[green]• Workflow is ready to execute[/green]")
    
    # Show cache status if applicable
    if result.get("from_cache"):
        console.print(f"\n[dim]• Result retrieved from cache[/dim]")

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="Goal Command Error"
    ))
    
    # Show common troubleshooting tips
    console.print(f"\n[dim]Common solutions:[/dim]")
    console.print(f"[dim]• Ensure your goal is clear and specific[/dim]")
    console.print(f"[dim]• Check that setup scripts are available[/dim]")
    console.print(f"[dim]• Try with mao --verbose for more details[/dim]")

def display_goal_progress(stage: str) -> None:
    """Display progress indicator during workflow creation"""
    progress_messages = {
        "analyzing": "Analyzing your goal...",
        "creating": "Creating workflow configuration...",
        "setting_up": "Setting up custom command...",
        "finalizing": "Finalizing workflow..."
    }
    
    message = progress_messages.get(stage, f"Processing {stage}...")
    console.print(f"[dim]• {message}[/dim]")

def display_goal_help() -> None:
    """Display help information for goal command usage"""
    help_panel = Panel(
        "[bold]Goal Command Usage[/bold]\n\n"
        "[cyan]Terminal:[/cyan] mao --goal 'create a marketing strategy for my startup'\n"
        "[cyan]In-App:[/cyan] /goal create a marketing strategy for my startup\n\n"
        "[dim]The goal command instantly creates a complete workflow from your description.\n"
        "Be specific about what you want to accomplish for best results.[/dim]",
        title="mao --goal",
        style="blue"
    )
    console.print(help_panel)

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate goal UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free