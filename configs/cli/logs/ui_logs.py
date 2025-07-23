"""
Logs CLI Command - UI Display Patterns
Professional workflow log viewing with filtering and search capabilities
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.tree import Tree
from typing import Dict, Any, List

# Module-level console for consistency
console = Console()

def display_logs_result(result: Dict[str, Any]) -> None:
    """
    Display logs command results with consistent CLI UI patterns.
    
    Args:
        result: Logs execution result with log entries and metadata
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    logs = result.get("logs", [])
    statistics = result.get("statistics", {})
    filters_applied = result.get("filters_applied", {})
    total_logs = result.get("total_logs", 0)
    
    # Display header with summary
    _display_logs_header(total_logs, statistics, filters_applied)
    
    # Display logs based on content
    if not logs:
        _display_empty_logs()
    elif len(logs) == 1:
        _display_single_log_details(logs[0])
    else:
        _display_logs_table(logs)
    
    # Display footer with navigation hints
    _display_logs_footer(filters_applied)

def _display_logs_header(total_logs: int, statistics: Dict[str, Any], filters_applied: Dict[str, Any]) -> None:
    """Display header with log summary and filter information"""
    
    # Create summary text
    summary_text = f"Found {total_logs} log entries"
    
    if filters_applied:
        filter_parts = []
        if filters_applied.get("workflow_id"):
            filter_parts.append(f"Workflow: {filters_applied['workflow_id']}")
        if filters_applied.get("search"):
            filter_parts.append(f"Search: '{filters_applied['search']}'")
        if filters_applied.get("status"):
            filter_parts.append(f"Status: {filters_applied['status']}")
        if filters_applied.get("date_range"):
            filter_parts.append(f"Range: {filters_applied['date_range']}")
        
        if filter_parts:
            summary_text += f" | Filters: {', '.join(filter_parts)}"
    
    # Display statistics if available
    stats_text = ""
    if statistics.get("by_status"):
        status_counts = []
        for status, count in statistics["by_status"].items():
            status_counts.append(f"{status}: {count}")
        stats_text = f"Status breakdown: {', '.join(status_counts)}"
    
    # Create header panel
    header_content = summary_text
    if stats_text:
        header_content += f"\n{stats_text}"
    
    console.print(Panel(
        header_content,
        title="Workflow Logs",
        style="blue"
    ))

def _display_empty_logs() -> None:
    """Display message when no logs are found"""
    console.print(Panel(
        Path(r"No workflow logs found matching the specified criteria.\n\n")
        Path(r"Tips:\n")
        "- Remove filters to see all logs: " / Path(r"logs\n")
        "- Check for active workflows: " / Path(r"workflows\n")
        "- View system stats:  / stats",
        title="No Logs Found",
        style="yellow"
    ))

def _display_single_log_details(log: Dict[str, Any]) -> None:
    """Display detailed view of a single log entry"""
    
    # Create main info panel
    log_info = [
        f"Workflow ID: {log.get('workflow_id', 'Unknown')}",
        f"Status: {log.get('status', 'Unknown')}",
        f"Type: {log.get('type', 'Unknown')}",
        f"Timestamp: {log.get('timestamp', 'Unknown')}"
    ]
    
    console.print(Panel(
        Path(r"\n").join(log_info),
        title=f"Log Entry Details",
        style="green"
    ))
    
    # Display message
    if log.get("message"):
        console.print(Panel(
            log["message"],
            title="Message",
            style="white"
        ))
    
    # Display details if available
    details = log.get("details", {})
    if details:
        _display_log_details_tree(details)

def _display_log_details_tree(details: Dict[str, Any]) -> None:
    """Display log details in a tree structure"""
    
    tree = Tree("Details")
    
    for key, value in details.items():
        if isinstance(value, dict):
            branch = tree.add(f"{key}:")
            for sub_key, sub_value in value.items():
                branch.add(f"{sub_key}: {sub_value}")
        elif isinstance(value, list):
            branch = tree.add(f"{key}:")
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    item_branch = branch.add(f"[{i}]")
                    for sub_key, sub_value in item.items():
                        item_branch.add(f"{sub_key}: {sub_value}")
                else:
                    branch.add(f"[{i}]: {item}")
        else:
            tree.add(f"{key}: {value}")
    
    console.print(tree)

def _display_logs_table(logs: List[Dict[str, Any]]) -> None:
    """Display logs in a table format"""
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Workflow ID", style="cyan", width=12)
    table.add_column("Status", style="green", width=10)
    table.add_column("Type", style="yellow", width=12)
    table.add_column("Message", style="white", width=40)
    table.add_column("Timestamp", style="dim", width=20)
    
    for log in logs:
        # Format timestamp for display
        timestamp = log.get("timestamp", "")
        if timestamp:
            try:
                from datetime import datetime
from pathlib import Path
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                display_time = dt.strftime("%Y-%m-%d %H:%M")
            except:
                display_time = timestamp[:16]
        else:
            display_time = "Unknown"
        
        # Truncate message if too long
        message = log.get("message", "")
        if len(message) > 37:
            message = message[:34] + "..."
        
        # Style status based on content
        status = log.get("status", "unknown")
        if status == "error":
            status_style = "[red]" + status + "[ / red]"
        elif status == "completed":
            status_style = "[green]" + status + "[ / green]"
        elif status == "active":
            status_style = "[yellow]" + status + "[ / yellow]"
        else:
            status_style = status
        
        table.add_row(
            log.get("workflow_id", "unknown")[:11],
            status_style,
            log.get("type", "unknown"),
            message,
            display_time
        )
    
    console.print(table)

def _display_logs_footer(filters_applied: Dict[str, Any]) -> None:
    """Display footer with usage hints"""
    
    footer_lines = []
    
    # Add filter usage hints
    if not filters_applied:
        footer_lines.extend([
            "Filter options:",
            "   / logs --workflow-id <id>     Show logs for specific workflow",
            "   / logs --search <term>        Search log content",
            "   / logs --status <status>      Filter by status (active, completed, error)",
            "   / logs --date-range <range>   Filter by time (1d, 7d, 30d, 1h, 24h)"
        ])
    else:
        footer_lines.extend([
            "Clear filters:  / logs",
            "Combine filters:  / logs --search error --date-range 1d"
        ])
    
    # Add related commands
    footer_lines.extend([
        "",
        "Related commands:",
        "   / workflows    List all workflows",
        "   / stats        System performance metrics", 
        "   / review       Review workflow details"
    ])
    
    console.print(Panel(
        Path(r"\n").join(footer_lines),
        title="Usage",
        style="dim"
    ))

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / Path(r"red] {error_message}\n\n")
        Path(r"Troubleshooting:\n")
        Path(r"- Check if workflow managers are available\n")
        Path(r"- Verify workflow directory permissions\n")
        "- Try  / doctor for system diagnostics",
        style="red",
        title="Logs Command Error"
    ))

def display_logs_search_help() -> None:
    """Display help for log search functionality"""
    console.print(Panel(
        Path(r"Log Search Guide:\n\n")
        Path(r"Search Examples:\n")
        "   / logs --search 'error'           Find logs containing 'errorPath(r'\n")
        "   / logs --search 'workflow_123Path(r'    Find logs for specific workflow\n")
        "   / logs --search 'completedPath(r'       Find completion logs\n\n")
        Path(r"Filter Combinations:\n")
        "   / logs --search 'errorPath(r' --date-range 1d\n")
        "  " / Path(r"logs --status active --limit 10\n")
        "   / logs --workflow-id abc123 --search 'phasePath(r'\n\n")
        Path(r"Date Range Formats:\n")
        Path(r"  1d, 7d, 30d    (days)\n")
        "  1h, 12h, 24h   (hours)",
        title="Search Help",
        style="blue"
    ))