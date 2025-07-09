"""
Workflows CLI Command - UI Display Patterns
Essential data structure for workflow listing display
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

# Standard cache instance
cache = CacheManager()

# Module-level console for consistency
console = Console()

def display_workflows_result(result: Dict[str, Any]) -> None:
    """
    Display workflows command results with consistent CLI UI patterns.
    
    Args:
        result: Workflow discovery result from workflows.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    workflows = result.get("workflows", [])
    active_workflows = result.get("active_workflows", [])
    temp_workflows = result.get("temp_workflows", [])
    stats = result.get("stats", {})
    filters = result.get("filters_applied", {})
    
    # Display summary information
    _display_workflow_summary(result, filters)
    
    # Display active workflows first if any
    if active_workflows:
        _display_active_workflows(active_workflows)
    
    # Display temporary workflows if any
    if temp_workflows:
        _display_temp_workflows(temp_workflows)
    
    # Display main workflow listings
    if workflows:
        _display_workflow_listings(workflows)
    else:
        _display_no_workflows_message(filters)
    
    # Display statistics if available
    if stats and workflows:
        _display_workflow_statistics(stats)

def _display_workflow_summary(result: Dict[str, Any], filters: Dict[str, Any]) -> None:
    """Display high-level workflow statistics and filter information"""
    total_count = result.get("total_count", 0)
    filtered_count = result.get("filtered_count", 0)
    active_count = result.get("active_count", 0)
    temp_count = result.get("temp_count", 0)
    
    # Build summary text
    summary_parts = [f"Found {total_count} total workflows"]
    
    if filtered_count != total_count:
        summary_parts.append(f"{filtered_count} matching filters")
    
    if active_count > 0:
        summary_parts.append(f"{active_count} active")
    
    if temp_count > 0:
        summary_parts.append(f"{temp_count} temporary")
    
    summary_text = " | ".join(summary_parts)
    console.print(f"\n[bold]{summary_text}[/bold]")
    
    # Display active filters
    active_filters = []
    for filter_name, filter_value in filters.items():
        if filter_value:
            active_filters.append(f"{filter_name}: {filter_value}")
    
    if active_filters:
        console.print(f"[dim]Filters: {', '.join(active_filters)}[/dim]")
    
    console.print()

def _display_active_workflows(active_workflows: List[Dict[str, Any]]) -> None:
    """Display currently active workflows"""
    console.print("[bold green]Active Workflows[/bold green]")
    
    for workflow in active_workflows:
        _display_single_workflow(workflow, highlight_active=True)
    
    console.print()

def _display_temp_workflows(temp_workflows: List[Dict[str, Any]]) -> None:
    """Display temporary workflows in creation"""
    console.print("[bold yellow]Temporary Workflows (In Creation)[/bold yellow]")
    
    for workflow in temp_workflows:
        _display_single_workflow(workflow, highlight_temp=True)
    
    console.print()

def _display_workflow_listings(workflows: List[Dict[str, Any]]) -> None:
    """
    Display workflow listings with essential metadata.
    
    Data Structure Priority:
    - Workflow identification (workflow_id, custom_command)
    - Status and progress information
    - Goal and description
    - User and timestamp information
    - Directory and deliverable status
    
    UI Design Philosophy:
    - Essential data only, no excessive formatting
    - Structured for easy UI translation
    - Preserve creative freedom for actual interface design
    """
    
    # Group workflows by status for natural organization
    workflows_by_status = {}
    for workflow in workflows:
        status = workflow.get("status", "unknown")
        if status not in workflows_by_status:
            workflows_by_status[status] = []
        workflows_by_status[status].append(workflow)
    
    # Display each status group
    status_order = ["completed", "active", "created", "unknown"]
    
    for status in status_order:
        if status in workflows_by_status:
            status_workflows = workflows_by_status[status]
            console.print(f"\n[bold cyan]{status.upper()} Workflows ({len(status_workflows)})[/bold cyan]")
            
            for workflow in status_workflows:
                _display_single_workflow(workflow)

def _display_single_workflow(workflow: Dict[str, Any], highlight_active: bool = False, highlight_temp: bool = False) -> None:
    """Display individual workflow with key metadata"""
    
    # Core identification
    workflow_id = workflow.get("workflow_id", "unknown")
    custom_command = workflow.get("custom_command", "unknown")
    status = workflow.get("status", "unknown")
    
    # Status styling
    status_color = "green" if highlight_active else ("yellow" if highlight_temp else "blue")
    status_text = f"[{status_color}]{status}[/{status_color}]"
    
    console.print(f"  [bold]{custom_command}[/bold] ({workflow_id}) - {status_text}")
    
    # Goal and description
    goal = workflow.get("workflow_goal", "")
    description = workflow.get("workflow_description", "")
    
    if goal:
        console.print(f"    Goal: {goal}")
    elif description:
        console.print(f"    Description: {description}")
    else:
        console.print(f"    [dim]No description available[/dim]")
    
    # User and timestamp information
    user_id = workflow.get("user_id", "unknown")
    created_at = workflow.get("created_at", "")
    last_modified = workflow.get("last_modified", "")
    
    info_parts = [f"User: {user_id}"]
    
    if created_at:
        try:
            # Format timestamp for display
            from datetime import datetime
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            info_parts.append(f"Created: {created_dt.strftime('%Y-%m-%d %H:%M')}")
        except:
            info_parts.append(f"Created: {created_at}")
    
    console.print(f"    [dim]{' | '.join(info_parts)}[/dim]")
    
    # Directory and deliverable status
    directory_name = workflow.get("directory_name", "")
    has_deliverables = workflow.get("has_deliverables", False)
    has_metadata = workflow.get("has_metadata", False)
    
    status_indicators = []
    if directory_name:
        status_indicators.append(f"Directory: {directory_name}")
    if has_deliverables:
        status_indicators.append("[green]Has deliverables[/green]")
    if has_metadata:
        status_indicators.append("[blue]Has metadata[/blue]")
    
    if status_indicators:
        console.print(f"    {' | '.join(status_indicators)}")
    
    console.print()  # Add spacing between workflows

def _display_no_workflows_message(filters: Dict[str, Any]) -> None:
    """Display appropriate message when no workflows are found"""
    has_filters = any(filters.values())
    
    if has_filters:
        message = "[yellow]No workflows match the specified filters[/yellow]\nTry adjusting your search criteria or removing filters"
    else:
        message = "[yellow]No workflows found[/yellow]\nCreate your first workflow to get started"
    
    console.print(Panel(message, title="Workflows Status"))

def _display_workflow_statistics(stats: Dict[str, Any]) -> None:
    """Display workflow statistics and insights"""
    console.print("\n[bold]Workflow Statistics[/bold]")
    
    # Status distribution
    status_dist = stats.get("status_distribution", {})
    if status_dist:
        console.print("\n[bold cyan]Status Distribution:[/bold cyan]")
        for status, count in sorted(status_dist.items()):
            console.print(f"  {status}: {count}")
    
    # User distribution (top 5)
    user_dist = stats.get("user_distribution", {})
    if user_dist and len(user_dist) > 1:
        console.print("\n[bold cyan]Top Users:[/bold cyan]")
        sorted_users = sorted(user_dist.items(), key=lambda x: x[1], reverse=True)[:5]
        for user, count in sorted_users:
            console.print(f"  {user}: {count} workflows")
    
    # Recent activity
    recent_count = stats.get("recent_activity_count", 0)
    if recent_count > 0:
        console.print(f"\n[bold cyan]Recent Activity:[/bold cyan] {recent_count} workflows modified in last 7 days")
    
    # Deliverables and metadata
    deliverables_count = stats.get("has_deliverables_count", 0)
    metadata_count = stats.get("has_metadata_count", 0)
    
    if deliverables_count > 0 or metadata_count > 0:
        console.print(f"\n[bold cyan]Completion Status:[/bold cyan]")
        if deliverables_count > 0:
            console.print(f"  {deliverables_count} workflows with deliverables")
        if metadata_count > 0:
            console.print(f"  {metadata_count} workflows with metadata")

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="Workflows Command Error"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate workflows UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free