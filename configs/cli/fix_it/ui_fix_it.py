"""
Fix_it CLI Command - UI Display Patterns
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, Any, List

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

# Module-level console for consistency
console = Console()

def display_fix_it_result(result: Dict[str, Any]) -> None:
    """
    Display fix_it command results with consistent CLI UI patterns.
    
    Args:
        result: Fix_it command execution result
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Display fix operation summary
    _display_fix_summary(result)
    
    # Display JSON copying details if applicable
    if result.get("json_copied"):
        _display_json_copying_details(result)
    
    # Display workflow correction details
    if result.get("phases_corrected"):
        _display_correction_details(result)
    
    # Display workflow state update
    if result.get("workflow_state"):
        _display_state_update(result.get("workflow_state"))

def _display_fix_summary(result: Dict[str, Any]) -> None:
    """Display overall fix operation summary"""
    summary_text = Text()
    summary_text.append("Fix Operation Completed Successfully", style="bold green")
    
    # Add key metrics
    phases_count = len(result.get("phases_corrected", []))
    if phases_count > 0:
        summary_text.append(f"\n• {phases_count} phase(s) corrected", style="green")
    
    if result.get("json_copied"):
        summary_text.append(Path(r"\n• JSON configuration copied to workflow directory"), style="blue")
    
    timestamp = result.get("timestamp", "")
    if timestamp:
        summary_text.append(f"\n• Completed at: {timestamp}", style="dim")
    
    console.print(Panel(
        summary_text,
        title="Fix_it Results",
        border_style="green"
    ))

def _display_json_copying_details(result: Dict[str, Any]) -> None:
    """Display JSON copying operation details"""
    copying_table = Table(title="JSON File Operations", show_header=True)
    copying_table.add_column("Operation", style="cyan")
    copying_table.add_column("Details", style="white")
    
    copying_table.add_row("Source Path", result.get("source_path", "N / A"))
    copying_table.add_row("Target Path", result.get("target_path", "N / A"))
    copying_table.add_row("Target Directory", result.get("target_directory", "N / A"))
    copying_table.add_row("Copy Status", "Completed" if result.get("json_copied") else "Not Required")
    
    console.print(copying_table)

def _display_correction_details(result: Dict[str, Any]) -> None:
    """Display workflow correction details"""
    phases_corrected = result.get("phases_corrected", [])
    if not phases_corrected:
        return
    
    correction_table = Table(title="Workflow Corrections Applied", show_header=True)
    correction_table.add_column("Phase", style="cyan")
    correction_table.add_column("Correction Type", style="yellow")
    correction_table.add_column("Status", style="green")
    
    # Display corrected phases
    for i, phase in enumerate(phases_corrected):
        phase_name = phase if isinstance(phase, str) else f"Phase {i+1}"
        correction_table.add_row(
            phase_name,
            "Applied",
            "Completed"
        )
    
    console.print(correction_table)

def _display_state_update(state_update: Dict[str, Any]) -> None:
    """Display workflow state update information"""
    if not state_update:
        return
    
    state_text = Text()
    state_text.append("Workflow State Updated", style="bold blue")
    
    # Add state update details
    if state_update.get("success"):
        state_text.append(Path(r"\n• State synchronization: Successful"), style="green")
    else:
        state_text.append(Path(r"\n• State synchronization: Failed"), style="red")
        if state_update.get("error"):
            state_text.append(fPath(r"\n• Error: {state_update[')error']}", style="red")
    
    console.print(Panel(
        state_text,
        title="State Management",
        border_style="blue"
    ))

def display_fix_progress(operation: str, workflow_id: str) -> Progress:
    """
    Display progress for long-running fix operations
    
    Args:
        operation: Name of the operation being performed
        workflow_id: ID of the workflow being fixed
        
    Returns:
        Progress object for task tracking
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    )
    
    progress.add_task(
        description=f"Fixing workflow {workflow_id[:8]}... ({operation})",
        total=None
    )
    
    return progress

def display_validation_results(validation_results: List[Dict[str, Any]]) -> None:
    """Display JSON validation results for debugging"""
    if not validation_results:
        return
    
    validation_table = Table(title="JSON Validation Results", show_header=True)
    validation_table.add_column("Field", style="cyan")
    validation_table.add_column("Status", style="white")
    validation_table.add_column("Details", style="dim")
    
    for result in validation_results:
        status_style = "green" if result.get("valid") else "red"
        status_text = "Valid" if result.get("valid") else "Invalid"
        
        validation_table.add_row(
            result.get("field", "Unknown"),
            Text(status_text, style=status_style),
            result.get("details", "")
        )
    
    console.print(validation_table)

def display_workflow_context(workflow_context: Dict[str, Any]) -> None:
    """Display current workflow context for debugging"""
    if not workflow_context:
        console.print(Panel(
            "No workflow context available",
            title="Workflow Context",
            style="yellow"
        ))
        return
    
    context_table = Table(title="Current Workflow Context", show_header=True)
    context_table.add_column("Property", style="cyan")
    context_table.add_column("Value", style="white")
    
    # Display key workflow properties
    key_properties = [
        "workflow_id", "current_phase", "status", 
        "phases_total", "phases_completed", "last_activity"
    ]
    
    for prop in key_properties:
        value = workflow_context.get(prop, "Not available")
        context_table.add_row(prop.replace("_", " ").title(), str(value))
    
    console.print(context_table)

def display_available_fix_types() -> None:
    """Display available fix types for user reference"""
    fix_types_table = Table(title="Available Fix Types", show_header=True)
    fix_types_table.add_column("Fix Type", style="cyan")
    fix_types_table.add_column("Description", style="white")
    fix_types_table.add_column("Use Case", style="dim")
    
    fix_types = [
        ("re_run_phase", "Re-execute a specific workflow phase", "Phase execution failed"),
        ("correct_deliverable", "Fix specific deliverable issues", "Output quality problems"),
        ("update_parameters", "Update phase parameters and re-run", "Configuration changes needed"),
        ("resume_workflow", "Resume workflow from specified phase", "Workflow was interrupted")
    ]
    
    for fix_type, description, use_case in fix_types:
        fix_types_table.add_row(fix_type, description, use_case)
    
    console.print(fix_types_table)

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[ / red] {error_message}",
        style="red",
        title="Fix_it Command Error"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate fix_it UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free