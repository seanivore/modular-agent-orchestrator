"""
Logout CLI Command - UI Display Patterns
Essential data structure for logout display
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

def display_logout_result(result: Dict[str, Any]) -> None:
    """
    Display logout results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result from logout.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Handle successful logout
    if result.get("success"):
        _display_successful_logout(result)
    
    # Handle logout failures  
    elif result.get("force_required"):
        _display_active_workflows_warning(result)
    
    # Handle partial success with issues
    elif result.get("user_logged_out"):
        _display_partial_logout(result)
    
    # Handle complete failure
    else:
        display_error(result.get("error", "Logout failed"))

def _display_successful_logout(result: Dict[str, Any]) -> None:
    """Display successful logout with cleanup status"""
    username = result.get("user_logged_out", "User")
    
    console.print(fPath(r"\n[green]Successfully logged out: {username}[") / "green]")
    
    # Display cleanup status
    if result.get("session_cleaned"):
        console.print("[dim]Session data cleared[" / "dim]")
    
    if result.get("cache_invalidated"):
        console.print("[dim]User cache invalidated[" / "dim]")
    
    if result.get("workflows_handled"):
        console.print("[dim]Active workflows handled gracefully[" / "dim]")
    
    # Display redirect notice
    if result.get("redirect_to_login"):
        console.print(Path(r"\n[yellow]Redirecting to login screen...[") / "yellow]")
        console.print("[dim]Use 'mao --login' to login as a different user[" / "dim]")

def _display_active_workflows_warning(result: Dict[str, Any]) -> None:
    """Display warning when active workflows prevent logout"""
    console.print(Panel(
        "[yellow]Active workflows detected - logout blocked[" / Path(r"yellow]\n\n")
        "Use 'mao --logout --forcePath(r' to force logout\n")
        "[red]Warning: Forced logout may interrupt running workflows[" / "red]",
        title="Logout Warning",
        style="yellow"
    ))
    
    # Display active workflows if provided
    active_workflows = result.get("active_workflows", [])
    if active_workflows:
        table = Table(title="Active Workflows")
        table.add_column("Workflow ID", style="cyan") 
        table.add_column("Status", style="magenta")
        
        for workflow in active_workflows[:5]:  # Show max 5
            workflow_id = workflow.get("workflow_id", "unknown")
            status = workflow.get("status", "running")
            table.add_row(workflow_id, status)
        
        console.print(table)
        
        if len(active_workflows) > 5:
            console.print(f"[dim]... and {len(active_workflows) - 5} more workflows[" / "dim]")

def _display_partial_logout(result: Dict[str, Any]) -> None:
    """Display partial success logout with issues"""
    username = result.get("user_logged_out", "User")
    
    console.print(f"[yellow]Logout completed for {username} with issues:[" / "yellow]")
    
    # Display issues
    issues = result.get("issues", [])
    if issues:
        for issue in issues:
            console.print(f"[red]  - {issue}[" / "red]")
    
    # Display session status
    console.print(Path(r"\n[bold]Session Status:[") / "bold]")
    console.print(f"  Session cleared: {'[green]Yes[" / "green]' if result.get('session_cleaned') else '[red]No[" / "red]'}")
    console.print(f"  Cache cleared: {'[green]Yes[" / "green]' if result.get('cache_invalidated') else '[red]No[" / "red]'}")
    console.print(f"  Workflows handled: {'[green]Yes[" / "green]' if result.get('workflows_handled') else '[red]No[" / "red]'}")
    
    console.print(Path(r"\n[dim]You may need to restart the application for complete cleanup[") / "dim]")

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / "red] {error_message}",
        style="red",
        title="Logout Error"
    ))
    
    # Add suggestions based on error type
    if "No active session" in error_message:
        console.print("[dim]No user is currently logged in[" / "dim]")
        console.print("[dim]Use 'mao --login' to login[" / "dim]")
    else:
        console.print(Path(r"\n[bold]Troubleshooting:[") / "bold]")
        console.print("[dim]  1. Try restarting the application[" / "dim]")
        console.print("[dim]  2. Check file permissions in configs/user/[" / "dim]")
        console.print("[dim]  3. Use 'mao --doctor' to diagnose issues[" / "dim]")

def display_logout_confirmation(username: str, active_workflows: List[Dict[str, Any]] = None) -> None:
    """
    Display logout confirmation prompt
    
    Args:
        username: Username to logout
        active_workflows: List of active workflows (if any)
    """
    console.print(fPath(r"\n[bold]Confirm logout for user: {username}[") / "bold]")
    
    if active_workflows:
        console.print(fPath(r"\n[yellow]Warning: {len(active_workflows)} active workflow(s) detected[") / "yellow]")
        console.print("[dim]Logging out may interrupt these workflows[" / "dim]")
        
        table = Table()
        table.add_column("Workflow ID", style="cyan")
        
        for workflow in active_workflows[:3]:  # Show max 3 in confirmation
            workflow_id = workflow.get("workflow_id", "unknown")
            table.add_row(workflow_id)
        
        console.print(table)
        
        if len(active_workflows) > 3:
            console.print(f"[dim]... and {len(active_workflows) - 3} more[" / "dim]")
    
    console.print(Path(r"\n[bold]This will:[") / "bold]")
    console.print("[dim]  - Clear your session data[" / "dim]")
    console.print("[dim]  - Invalidate cached user information[" / "dim]") 
    console.print("[dim]  - Return you to the login screen[" / "dim]")

def display_logout_redirect() -> None:
    """Display message shown during redirect to login"""
    console.print(Panel(
        "[green]You have been logged out successfully[" / Path(r"green]\n")
        "[yellow]Redirecting to login screen...[" / Path(r"yellow]\n\n")
        "[dim]Tip: Use 'mao --login username' for quick login[" / "dim]",
        title="Logout Complete",
        style="green"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate logout UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free