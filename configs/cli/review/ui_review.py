"""
Review CLI Command - UI Display Patterns
Essential data structure for workflow review display
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Dict, Any, List

# Module-level console for consistency
console = Console()

def display_review_result(result: Dict[str, Any]) -> None:
    """
    Display review command results with consistent CLI UI patterns.
    
    Args:
        result: Review execution result from review.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    workflows = result.get("workflows", [])
    review_summary = result.get("review_summary", {})
    search_params = result.get("search_parameters", {})
    
    # Display review session header
    _display_review_header(result, search_params)
    
    # Display review summary
    if review_summary:
        _display_review_summary(review_summary)
    
    # Display workflows for review
    if workflows:
        _display_workflows_for_review(workflows)
    else:
        _display_no_workflows_message(search_params)

def _display_review_header(result: Dict[str, Any], search_params: Dict[str, Any]) -> None:
    """Display review session header with search context"""
    total_count = result.get("total_count", 0)
    review_time = result.get("review_time", "")
    
    # Build header text
    header_text = f"Workflow Review Session - {total_count} workflows found"
    
    # Add search context
    search_context = []
    for param, value in search_params.items():
        if value and param != "detailed" and param != "include_context":
            search_context.append(f"{param}: {value}")
    
    if search_context:
        header_text += f"\nSearch: {', '.join(search_context)}"
    
    if review_time:
        try:
            from datetime import datetime
            review_dt = datetime.fromisoformat(review_time.replace('Z', '+00:00'))
            header_text += f"\nReviewed: {review_dt.strftime('%Y-%m-%d %H:%M')}"
        except:
            pass
    
    console.print(Panel(header_text, title="Review Session", style="blue"))
    console.print()

def _display_review_summary(summary: Dict[str, Any]) -> None:
    """Display review summary with actionable insights"""
    console.print("[bold]Review Summary[/bold]")
    
    # Quick stats
    total_reviewed = summary.get("total_reviewed", 0)
    status_dist = summary.get("status_distribution", {})
    categories = summary.get("review_categories", {})
    
    console.print(f"  Total workflows reviewed: {total_reviewed}")
    
    # Status distribution
    if status_dist:
        status_text = []
        for status, count in sorted(status_dist.items()):
            status_text.append(f"{status}: {count}")
        console.print(f"  Status breakdown: {', '.join(status_text)}")
    
    # Categories that need attention
    needs_attention = categories.get("needs_attention", 0)
    recently_active = categories.get("recently_active", 0)
    
    if needs_attention > 0:
        console.print(f"  [yellow]Workflows needing attention: {needs_attention}[/yellow]")
    
    if recently_active > 0:
        console.print(f"  [green]Recently active workflows: {recently_active}[/green]")
    
    # Recommendations
    recommendations = summary.get("recommendations", [])
    if recommendations:
        console.print("\n[bold cyan]Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  - {rec}")
    
    console.print()

def _display_workflows_for_review(workflows: List[Dict[str, Any]]) -> None:
    """
    Display workflows organized for review purposes.
    
    Data Structure Priority:
    - Workflow identification and status
    - Progress and completion information
    - Action items and recovery options
    - Context and timeline information
    
    UI Design Philosophy:
    - Essential review data only
    - Structured for UI development translation
    - Preserve creative freedom for interface design
    """
    
    # Group workflows by review priority
    prioritized_workflows = _prioritize_workflows_for_review(workflows)
    
    # Display high priority workflows first
    if prioritized_workflows.get("high_priority"):
        console.print("[bold red]High Priority - Needs Immediate Attention[/bold red]")
        for workflow in prioritized_workflows["high_priority"]:
            _display_workflow_review_item(workflow, priority="high")
        console.print()
    
    # Display medium priority workflows
    if prioritized_workflows.get("medium_priority"):
        console.print("[bold yellow]Medium Priority - Recent Activity[/bold yellow]")
        for workflow in prioritized_workflows["medium_priority"]:
            _display_workflow_review_item(workflow, priority="medium")
        console.print()
    
    # Display normal workflows
    if prioritized_workflows.get("normal"):
        console.print("[bold]Standard Workflows[/bold]")
        for workflow in prioritized_workflows["normal"]:
            _display_workflow_review_item(workflow, priority="normal")

def _prioritize_workflows_for_review(workflows: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Prioritize workflows for review display"""
    prioritized = {
        "high_priority": [],
        "medium_priority": [],
        "normal": []
    }
    
    for workflow in workflows:
        status = workflow.get("status", "").lower()
        has_recovery = "recovery_options" in workflow
        workflow_status = workflow.get("workflow_status", {})
        health = workflow_status.get("health", "")
        
        # High priority: Failed, interrupted, or unhealthy workflows
        if status in ["failed", "interrupted", "paused"] or health == "error" or has_recovery:
            prioritized["high_priority"].append(workflow)
        # Medium priority: Active or recently modified workflows
        elif status == "active" or _is_recently_active(workflow):
            prioritized["medium_priority"].append(workflow)
        # Normal priority: Completed or standard workflows
        else:
            prioritized["normal"].append(workflow)
    
    return prioritized

def _is_recently_active(workflow: Dict[str, Any]) -> bool:
    """Check if workflow has been recently active"""
    detailed_analysis = workflow.get("detailed_analysis", {})
    timeline = detailed_analysis.get("timeline_analysis", {})
    return timeline.get("is_recent", False) or timeline.get("is_active", False)

def _display_workflow_review_item(workflow: Dict[str, Any], priority: str = "normal") -> None:
    """Display individual workflow review item with key information"""
    
    # Core identification
    workflow_id = workflow.get("workflow_id", "unknown")
    custom_command = workflow.get("custom_command", "unknown")
    status = workflow.get("status", "unknown")
    
    # Priority styling
    priority_colors = {
        "high": "red",
        "medium": "yellow", 
        "normal": "blue"
    }
    color = priority_colors.get(priority, "blue")
    
    # Main workflow line
    console.print(f"  [{color}]{custom_command}[/{color}] ({workflow_id}) - Status: {status}")
    
    # Goal or description
    goal = workflow.get("workflow_goal", "")
    description = workflow.get("workflow_description", "")
    
    if goal:
        console.print(f"    Goal: {goal}")
    elif description:
        console.print(f"    Description: {description}")
    
    # Workflow status details
    workflow_status = workflow.get("workflow_status", {})
    if workflow_status and not workflow_status.get("error"):
        phases_total = workflow_status.get("phases_total", 0)
        phases_completed = workflow_status.get("phases_completed", 0)
        health = workflow_status.get("health", "unknown")
        
        if phases_total > 0:
            completion_rate = (phases_completed / phases_total) * 100
            console.print(f"    Progress: {phases_completed}/{phases_total} phases ({completion_rate:.1f}%) - Health: {health}")
    
    # Recovery options for interrupted workflows
    recovery_options = workflow.get("recovery_options", {})
    if recovery_options and not recovery_options.get("error"):
        recovery_type = recovery_options.get("recovery_type", "unknown")
        current_phase = recovery_options.get("current_phase", "")
        estimated_time = recovery_options.get("estimated_recovery_time", "")
        
        console.print(f"    [yellow]Recovery Available:[/yellow] {recovery_type}")
        if current_phase:
            console.print(f"    Current phase: {current_phase}")
        if estimated_time:
            console.print(f"    Estimated recovery time: {estimated_time}")
    
    # Detailed analysis if available
    detailed_analysis = workflow.get("detailed_analysis", {})
    if detailed_analysis:
        complexity_score = detailed_analysis.get("complexity_score", 0)
        completion_rate = detailed_analysis.get("completion_rate", 0.0)
        timeline = detailed_analysis.get("timeline_analysis", {})
        
        analysis_parts = []
        if complexity_score > 0:
            analysis_parts.append(f"Complexity: {complexity_score}")
        if completion_rate > 0:
            analysis_parts.append(f"Completion: {completion_rate:.1%}")
        if timeline.get("duration_hours"):
            duration = timeline["duration_hours"]
            if duration < 1:
                analysis_parts.append(f"Duration: {duration * 60:.0f}m")
            else:
                analysis_parts.append(f"Duration: {duration:.1f}h")
        
        if analysis_parts:
            console.print(f"    [dim]Analysis: {' | '.join(analysis_parts)}[/dim]")
    
    # User and timestamp information
    user_id = workflow.get("user_id", "unknown")
    created_at = workflow.get("created_at", "")
    last_modified = workflow.get("last_modified", "")
    
    info_parts = [f"User: {user_id}"]
    
    if last_modified:
        try:
            from datetime import datetime
            modified_dt = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
            info_parts.append(f"Modified: {modified_dt.strftime('%Y-%m-%d %H:%M')}")
        except:
            info_parts.append(f"Modified: {last_modified}")
    elif created_at:
        try:
            from datetime import datetime
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            info_parts.append(f"Created: {created_dt.strftime('%Y-%m-%d %H:%M')}")
        except:
            info_parts.append(f"Created: {created_at}")
    
    console.print(f"    [dim]{' | '.join(info_parts)}[/dim]")
    console.print()  # Add spacing between workflows

def _display_no_workflows_message(search_params: Dict[str, Any]) -> None:
    """Display appropriate message when no workflows are found for review"""
    has_search_params = any(v for v in search_params.values() if v)
    
    if has_search_params:
        message = "[yellow]No workflows found matching your search criteria[/yellow]\n"
        message += "Try adjusting your search parameters or broadening your criteria"
    else:
        message = "[yellow]No workflows available for review[/yellow]\n"
        message += "Create workflows to begin using the review functionality"
    
    console.print(Panel(message, title="Review Status"))

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="Review Command Error"
    ))