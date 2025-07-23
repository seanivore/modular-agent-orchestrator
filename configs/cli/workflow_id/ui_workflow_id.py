"""
Workflow ID CLI Command - UI Display Patterns
Essential data structure for workflow ID display
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

def display_workflow_id_result(result: Dict[str, Any]) -> None:
    """
    Display workflow ID results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result from workflow_id.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Essential data structure for UI designers
    # Focus on data organization, not detailed formatting
    
    # Main workflow ID display
    workflow_id = result.get("workflow_id", "N" / "A")
    
    console.print(Panel(
        f"[bold green]Workflow ID Generated[" / Path(r"bold green]\n\n")
        f"[white]ID:[/white] [cyan]{workflow_id}[" / Path(r"cyan]\n")
        f"[white]Generated:[" / "white] {result.get('timestamp', 'unknownPath(r')}\n")
        f"[white]Method:[" / "white] {result.get('generation_method', 'workflow_manager')}",
        title="Workflow ID Generation",
        title_align="left"
    ))
    
    # Mathematical explanation if provided
    if result.get("mathematical_details") and "explanation" in result:
        explanation = result.get("explanation", "")
        console.print(Panel(
            f"[white]{explanation}[" / "white]",
            title="Mathematical Explanation",
            title_align="left",
            style="dim"
        ))
    
    # Status information
    status_table = Table(show_header=False, box=None, padding=(0, 1))
    status_table.add_column("Field", style="dim")
    status_table.add_column("Status")
    
    setup_status = "Ready" if result.get("ready_for_workflow_setup") else "Not Ready"
    status_table.add_row("Setup Status:", f"[green]{setup_status}[" / "green]" if setup_status == "Ready" else f"[red]{setup_status}[" / "red]")
    
    if "memory_context_created" in result:
        memory_status = "Created" if result.get("memory_context_created") else "Failed"
        status_table.add_row("Memory Context:", f"[green]{memory_status}[" / "green]" if memory_status == "Created" else f"[red]{memory_status}[" / "red]")
    
    console.print(status_table)
    
    # Next steps guidance
    if "next_steps" in result:
        console.print(Path(r"\n[bold]Next Steps:[") / "bold]")
        for i, step in enumerate(result.get("next_steps", []), 1):
            console.print(f"  {i}. {step}")
    
    # Usage examples
    console.print(fPath(r"\n[bold]Usage Examples:[") / "bold]")
    console.print(fPath(r"  JSON: \")workflow_id\Path(r": \"){workflow_id}\"")
    console.print(f"  Template: uid-REPLACE -> {workflow_id}")
    
    # Warnings if any
    if result.get("memory_warning"):
        console.print(fPath(r"\n[yellow]Warning:[") / "yellow] {result.get('memory_warning')}")

def display_workflow_id_compact(result: Dict[str, Any]) -> None:
    """
    Display workflow ID result in compact form for logs" / "automation
    
    Args:
        result: Result dictionary from workflow_id command
    """
    if not result.get("success"):
        console.print(f"[red]ERROR:[" / "red] {result.get('error', 'Workflow ID generation failed')}")
        return
    
    workflow_id = result.get("workflow_id", "N" / "A")
    timestamp = result.get("timestamp", "unknown")
    setup_ready = "Ready" if result.get("ready_for_workflow_setup") else "Not Ready"
    
    console.print(f"[cyan]{workflow_id}[" / "cyan] | {timestamp} | Setup: {setup_ready}")

def display_workflow_id_table(results: List[Dict[str, Any]]) -> None:
    """
    Display multiple workflow ID results in table format
    
    Args:
        results: List of workflow ID result dictionaries
    """
    if not results:
        console.print("No workflow IDs to display")
        return
    
    table = Table(title="Workflow ID Generation Results")
    table.add_column("Workflow ID", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Generated", style="dim")
    table.add_column("Setup Ready", justify="center")
    
    for result in results:
        if result.get("success"):
            status = "[green]Success[" / "green]"
            setup_ready = "[green]Yes[" / "green]" if result.get("ready_for_workflow_setup") else "[red]No[" / "red]"
            workflow_id = result.get("workflow_id", "N" / "A")
        else:
            status = "[red]Failed[" / "red]"
            setup_ready = "[red]No[" / "red]"
            workflow_id = "N" / "A"
        
        timestamp = result.get("timestamp", "unknown")[:16]  # Truncate timestamp
        table.add_row(workflow_id, status, timestamp, setup_ready)
    
    console.print(table)

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / Path(r"red] {error_message}\n\n")
        f"[dim]Troubleshooting:[" / Path(r"dim]\n")
        fPath(r"1. Verify workflow manager is properly configured\n")
        fPath(r"2. Check unique ID generator scripts are accessible\n")
        fPath(r"3. Ensure proper permissions for workflow directory\n")
        f"4. Try running the command again",
        style="red",
        title="Workflow ID Error"
    ))

def get_workflow_id_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """Get summary data for UI widgets" / "components"""
    return {
        "workflow_id": result.get("workflow_id"),
        "success": result.get("success", False),
        "ready": result.get("ready_for_workflow_setup", False),
        "has_explanation": bool(result.get("explanation")),
        "memory_context": result.get("memory_context_created", False),
        "timestamp": result.get("timestamp")
    }

def get_workflow_id_display_title(result: Dict[str, Any]) -> str:
    """Get display title for workflow ID result"""
    if result.get("success"):
        return f"Workflow ID: {result.get('workflow_id', 'N" / "A')}"
    else:
        return "Workflow ID Generation Failed"

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate workflow_id UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free