"""
Doctor CLI Command - UI Display Patterns
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn
from typing import Dict, Any, List

# Module-level console for consistency
console = Console()

def display_doctor_result(result: Dict[str, Any]) -> None:
    """
    Display doctor command results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result with system health diagnostics
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Display overall system status
    _display_overall_status(result.get("overall_status", {}))
    
    # Display detailed health checks
    _display_health_checks(result.get("health_checks", {}))
    
    # Display actionable insights
    _display_insights(result.get("insights", []))
    
    # Display summary
    _display_summary(result.get("summary", ""))

def _display_overall_status(overall_status: Dict[str, Any]) -> None:
    """Display overall system health status"""
    status = overall_status.get("overall_status", "unknown")
    health_score = overall_status.get("health_score", 0)
    
    # Status color mapping
    status_colors = {
        "healthy": "green",
        "warning": "yellow", 
        "degraded": "orange",
        "critical": "red",
        "unknown": "white"
    }
    
    status_color = status_colors.get(status, "white")
    
    # Create status panel
    status_text = f"[{status_color}]{status.upper()}[/{status_color}] - Health Score: {health_score:.1f}%"
    
    console.print(Panel(
        status_text,
        title="System Health Status",
        style=status_color,
        width=60
    ))
    
    # Display check summary
    checks_passed = overall_status.get("checks_passed", 0)
    checks_warning = overall_status.get("checks_warning", 0)
    checks_failed = overall_status.get("checks_failed", 0)
    total_checks = overall_status.get("total_checks", 0)
    
    summary_table = Table(show_header=False, box=None, padding=(0, 1))
    summary_table.add_column("Status", style="bold")
    summary_table.add_column("Count", justify="right")
    
    summary_table.add_row("[green]Passed[/green]", str(checks_passed))
    if checks_warning > 0:
        summary_table.add_row("[yellow]Warnings[/yellow]", str(checks_warning))
    if checks_failed > 0:
        summary_table.add_row("[red]Failed[/red]", str(checks_failed))
    summary_table.add_row("[white]Total[/white]", str(total_checks))
    
    console.print(summary_table)
    console.print()

def _display_health_checks(health_checks: Dict[str, Dict[str, Any]]) -> None:
    """Display detailed health check results"""
    console.print("[bold]Detailed Health Checks:[/bold]")
    
    # Create tree structure for health checks
    tree = Tree("System Components")
    
    for check_name, check_result in health_checks.items():
        status = check_result.get("status", "unknown")
        
        # Status icons and colors
        status_display = {
            "healthy": "[green]✓[/green]",
            "warning": "[yellow]⚠[/yellow]", 
            "error": "[red]✗[/red]",
            "unknown": "[white]?[/white]"
        }
        
        icon = status_display.get(status, "[white]?[/white]")
        component_name = check_name.replace("_", " ").title()
        
        # Add main component node
        component_node = tree.add(f"{icon} {component_name}")
        
        # Add relevant detail information
        _add_check_details(component_node, check_result)
    
    console.print(tree)
    console.print()

def _add_check_details(node, check_result: Dict[str, Any]) -> None:
    """Add relevant details to health check tree nodes"""
    status = check_result.get("status", "unknown")
    
    # Add error details if present
    if "error" in check_result:
        node.add(f"[red]Error: {check_result['error']}[/red]")
    
    # Add specific details based on check type
    if "python_version" in check_result:
        node.add(f"Python Version: {check_result['python_version']}")
    
    if "present_directories" in check_result:
        present_count = len(check_result["present_directories"])
        total_count = check_result.get("total_required", present_count)
        node.add(f"Directories: {present_count}/{total_count} present")
    
    if "import_successful" in check_result:
        import_status = "✓" if check_result["import_successful"] else "✗"
        node.add(f"Import: {import_status}")
    
    if "present_files" in check_result:
        present_count = len(check_result["present_files"])
        total_count = check_result.get("total_critical", present_count)
        node.add(f"Files: {present_count}/{total_count} present")
    
    if "health_score" in check_result:
        node.add(f"Score: {check_result['health_score']:.1f}%")

def _display_insights(insights: List[Dict[str, Any]]) -> None:
    """Display actionable insights and recommendations"""
    if not insights:
        return
    
    console.print("[bold]Insights and Recommendations:[/bold]")
    
    # Group insights by type
    error_insights = [i for i in insights if i.get("type") == "error"]
    warning_insights = [i for i in insights if i.get("type") == "warning"]
    success_insights = [i for i in insights if i.get("type") == "success"]
    
    # Display errors first (highest priority)
    if error_insights:
        console.print("[red]Critical Issues:[/red]")
        for insight in error_insights:
            _display_insight_item(insight, "red")
        console.print()
    
    # Display warnings
    if warning_insights:
        console.print("[yellow]Warnings:[/yellow]")
        for insight in warning_insights:
            _display_insight_item(insight, "yellow")
        console.print()
    
    # Display success messages
    if success_insights:
        for insight in success_insights:
            _display_insight_item(insight, "green")

def _display_insight_item(insight: Dict[str, Any], color: str) -> None:
    """Display individual insight item"""
    component = insight.get("component", "system")
    message = insight.get("message", "No message")
    action = insight.get("action", "No action specified")
    
    console.print(f"[{color}]• {message}[/{color}]")
    console.print(f"  Action: {action}")
    if "details" in insight:
        console.print(f"  Details: {insight['details']}")
    console.print()

def _display_summary(summary: str) -> None:
    """Display system health summary"""
    if summary:
        console.print(Panel(
            summary,
            title="Summary",
            style="blue",
            width=80
        ))

def display_system_metrics(metrics: Dict[str, Any]) -> None:
    """
    Display system performance metrics in tabular format.
    Data-focused display for system monitoring integration.
    """
    if not metrics:
        console.print("[yellow]No system metrics available[/yellow]")
        return
    
    # Create metrics table
    table = Table(title="System Metrics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", width=20)
    table.add_column("Value", style="white", width=15)
    table.add_column("Status", style="green", width=10)
    
    for metric_name, metric_data in metrics.items():
        if isinstance(metric_data, dict):
            value = metric_data.get("value", "N/A")
            status = metric_data.get("status", "unknown")
        else:
            value = str(metric_data)
            status = "active"
        
        table.add_row(metric_name.replace("_", " ").title(), str(value), status)
    
    console.print(table)

def display_diagnostic_progress(total_checks: int, completed_checks: int, current_check: str) -> None:
    """
    Display diagnostic progress for real-time feedback.
    Essential for long-running diagnostic operations.
    """
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        
        task = progress.add_task("Running diagnostics...", total=total_checks)
        progress.update(task, completed=completed_checks, description=f"Checking {current_check}")

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="System Diagnostic Error"
    ))