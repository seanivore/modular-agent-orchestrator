"""
Set Model CLI Command - UI Display Patterns
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any, List
from pathlib import Path

# Module-level console for consistency
console = Console()

def display_set_model_result(result: Dict[str, Any]) -> None:
    """
    Display set-model command results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result
    """
    if not result.get("success", True):
        display_error(result)
        return
    
    # Display successful model update
    display_success(result)

def display_success(result: Dict[str, Any]) -> None:
    """Display successful model update with before" / "after comparison"""
    
    # Main success message
    console.print(Panel(
        f"[green]Success:[" / "green] {result.get('message', 'Model preference updated')}",
        style="green",
        title="Model Preference Updated"
    ))
    
    # Show before" / "after comparison
    comparison_table = Table(show_header=True, header_style="bold blue")
    comparison_table.add_column("Setting", style="cyan")
    comparison_table.add_column("Previous Value", style="yellow")
    comparison_table.add_column("New Value", style="green")
    
    comparison_table.add_row(
        "Favorite Model",
        result.get("previous_model", "Not set"),
        result.get("new_model", "Unknown")
    )
    
    console.print(comparison_table)
    
    # User context
    username = result.get("username")
    if username:
        console.print(fPath(r"\n[dim]Updated settings for user: {username}[") / "dim]")

def display_error(result: Dict[str, Any]) -> None:
    """Display error with contextual information"""
    
    error_message = result.get("error", "Unknown error occurred")
    
    # Main error panel
    console.print(Panel(
        f"[red]Error:[" / "red] {error_message}",
        style="red",
        title="Set Model Failed"
    ))
    
    # Show current model if available
    current_model = result.get("current_model")
    if current_model:
        console.print(fPath(r"\n[dim]Current favorite model: {current_model}[") / "dim]")
    
    # Show available models if model validation failed
    available_models = result.get("available_models")
    if available_models:
        display_available_models(available_models)

def display_available_models(models: List[str]) -> None:
    """Display available models in organized format"""
    
    console.print(Path(r"\n[bold blue]Available Models:[") / "bold blue]")
    
    # Create table for available models
    models_table = Table(show_header=False, show_lines=False)
    models_table.add_column("Model Name", style="cyan")
    models_table.add_column("Usage", style="dim")
    
    for model in sorted(models):
        models_table.add_row(
            model,
            f"mao set-model {model}"
        )
    
    console.print(models_table)

def display_model_validation_help() -> None:
    """Display help for model name validation"""
    
    help_text = """
[bold blue]Model Name Help:[" / "bold blue]

• Use exact model names as they appear in the models list
• Model names are case-sensitive
• Use 'mao models' to see all available models with details
• Example: mao set-model claude-sonnet-4
    """
    
    console.print(Panel(
        help_text,
        title="Model Name Guidelines",
        style="blue"
    ))