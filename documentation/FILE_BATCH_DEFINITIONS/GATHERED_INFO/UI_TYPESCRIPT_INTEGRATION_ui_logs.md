# UI TypeScript Integration - ui_logs.py

## Overview
Logs CLI command UI component that provides professional workflow log viewing with filtering and search capabilities. Uses Rich library for advanced terminal displays while supporting comprehensive log analysis for the LOCAL application architecture.

## Code & Explanation

### Architecture Overview
**Professional Log Management**: Advanced log viewing system with Rich terminal integration and filtering capabilities.

- **Rich Terminal Display**: Professional log tables, panels, and tree structures
- **Advanced Filtering**: Support for workflow ID, search terms, status, and date range filters
- **Multiple View Modes**: Single log details, table view, and empty state handling
- **Statistics Integration**: Log count summaries and status breakdowns

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
def display_logs_result(result: Dict[str, Any]) -> None:
    """
    Rich terminal display for logs command results.
    Node.js could capture formatted output or implement equivalent display.
    """
    logs = result.get("logs", [])
    statistics = result.get("statistics", {})
    filters_applied = result.get("filters_applied", {})
    
    # Display components based on log content
    _display_logs_header(total_logs, statistics, filters_applied)
    
    if not logs:
        _display_empty_logs()
    elif len(logs) == 1:
        _display_single_log_details(logs[0])
    else:
        _display_logs_table(logs)
```

#### Data Exchange Formats
- **Input**: Log search results with filtering metadata
- **Output**: Rich terminal formatted log displays
- **Filter Support**: workflow_id, search terms, status, date_range
- **Statistics**: Log count breakdowns by status and timeframe

#### Terminal UI Rendering
```python
# Professional log table with Rich formatting
table = Table(show_header=True, header_style="bold blue")
table.add_column("Workflow ID", style="cyan", width=12)
table.add_column("Status", style="green", width=10)
table.add_column("Type", style="yellow", width=12)
table.add_column("Message", style="white", width=40)
table.add_column("Timestamp", style="dim", width=20)

# Status-based styling
if status == "error":
    status_style = "[red]" + status + "[/red]"
elif status == "completed":
    status_style = "[green]" + status + "[/green]"
elif status == "active":
    status_style = "[yellow]" + status + "[/yellow]"
```

#### Configuration & State Sharing
- **Filter State**: Preserves and displays active filter settings
- **Search Capabilities**: Text search across log content
- **Date Range Filtering**: Flexible time-based log filtering

## Written & Illustrated Data Info

### Data In-Flow
- **Log Query Results**: Filtered log entries from workflow managers
- **Filter Parameters**: Search terms, workflow IDs, status filters, date ranges
- **Statistics Data**: Log count summaries and status breakdowns
- **System Context**: Available workflows and system status

### Data Out-Flow
- **Rich Log Tables**: Professional formatted log displays
- **Filter Status**: Current filter settings and applied criteria
- **Navigation Guidance**: Usage hints and related commands
- **Detailed Log Views**: Single log entry details with tree structures

### Integration Touchpoints
- **Workflow Manager Integration**: Receives log data from workflow systems
- **Search System**: Advanced text search across log content
- **Filter Management**: Preserves and displays active filters
- **Related Commands**: Integration with workflows, stats, and review commands

## Log Display Features

### Header with Filter Information
```python
def _display_logs_header(total_logs: int, statistics: Dict[str, Any], filters_applied: Dict[str, Any]) -> None:
    """Display comprehensive log summary with active filters"""
    summary_text = f"Found {total_logs} log entries"
    
    if filters_applied:
        filter_parts = []
        if filters_applied.get("workflow_id"):
            filter_parts.append(f"Workflow: {filters_applied['workflow_id']}")
        if filters_applied.get("search"):
            filter_parts.append(f"Search: '{filters_applied['search']}'")
        # ... additional filter display
        
        summary_text += f" | Filters: {', '.join(filter_parts)}"
```

### Single Log Detail View
```python
def _display_single_log_details(log: Dict[str, Any]) -> None:
    """Detailed view with Rich panels and tree structures"""
    # Main info panel
    log_info = [
        f"Workflow ID: {log.get('workflow_id', 'Unknown')}",
        f"Status: {log.get('status', 'Unknown')}",
        f"Type: {log.get('type', 'Unknown')}",
        f"Timestamp: {log.get('timestamp', 'Unknown')}"
    ]
    
    console.print(Panel("\n".join(log_info), title="Log Entry Details"))
    
    # Details tree for hierarchical data
    if log.get("details", {}):
        _display_log_details_tree(details)
```

### Advanced Filtering System
```python
def _display_logs_footer(filters_applied: Dict[str, Any]) -> None:
    """Display filter usage and related commands"""
    footer_lines = []
    
    if not filters_applied:
        footer_lines.extend([
            "Filter options:",
            "  /logs --workflow-id <id>     Show logs for specific workflow",
            "  /logs --search <term>        Search log content",
            "  /logs --status <status>      Filter by status (active, completed, error)",
            "  /logs --date-range <range>   Filter by time (1d, 7d, 30d, 1h, 24h)"
        ])
```

### Search Help System
```python
def display_logs_search_help() -> None:
    """Comprehensive search guidance"""
    console.print(Panel(
        "Log Search Guide:\n\n"
        "Search Examples:\n"
        "  /logs --search 'error'           Find logs containing 'error'\n"
        "  /logs --search 'workflow_123'    Find logs for specific workflow\n"
        "  /logs --search 'completed'       Find completion logs\n\n"
        "Filter Combinations:\n"
        "  /logs --search 'error' --date-range 1d\n"
        "  /logs --status active --limit 10\n"
        "  /logs --workflow-id abc123 --search 'phase'",
        title="Search Help"
    ))
```

## Error Handling and Empty States

### Empty Log Display
```python
def _display_empty_logs() -> None:
    """User-friendly empty state with guidance"""
    console.print(Panel(
        "No workflow logs found matching the specified criteria.\n\n"
        "Tips:\n"
        "- Remove filters to see all logs: /logs\n"
        "- Check for active workflows: /workflows\n"
        "- View system stats: /stats",
        title="No Logs Found",
        style="yellow"
    ))
```

### Error Display
```python
def display_error(error_message: str) -> None:
    """Comprehensive error display with troubleshooting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}\n\n"
        "Troubleshooting:\n"
        "- Check if workflow managers are available\n"
        "- Verify workflow directory permissions\n"
        "- Try /doctor for system diagnostics",
        title="Logs Command Error"
    ))
```

## Dependencies
- **rich library**: Console, Table, Panel, Tree for advanced terminal display
- **datetime**: Timestamp formatting and parsing
- **typing**: Type hints for structured interfaces

## Professional Software Architecture Notes
This component represents professional log management system design:
- **Advanced Filtering**: Comprehensive search and filter capabilities
- **Rich Display**: Professional terminal formatting with colors and structures
- **User Experience**: Clear navigation, helpful empty states, and usage guidance
- **Error Recovery**: Comprehensive error handling with specific troubleshooting steps
- **Performance**: Efficient display for both single logs and large log sets

This is exactly how professional development tools handle log viewing - advanced filtering, rich terminal displays, and comprehensive user guidance for complex log analysis.