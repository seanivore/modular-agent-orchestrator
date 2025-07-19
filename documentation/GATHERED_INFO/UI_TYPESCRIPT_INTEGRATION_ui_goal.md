# UI TypeScript Integration - ui_goal.py

## Overview
Goal CLI command UI component that provides rich terminal display for workflow creation with progress tracking. Uses Rich library for enhanced terminal interfaces while maintaining structured data patterns for subprocess communication.

## Code & Explanation

### Architecture Overview
**Rich Terminal Integration**: Advanced terminal UI component with professional display capabilities.

- **Rich Library Usage**: Professional terminal formatting with panels, tables, and trees
- **Workflow Creation Focus**: Specialized display for goal-to-workflow conversion results
- **Progress Tracking**: Real-time feedback during workflow creation process
- **Error Recovery**: Comprehensive error display with troubleshooting guidance

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
# Direct terminal display when run as Python subprocess
def display_goal_result(result: Dict[str, Any]) -> None:
    """
    Rich terminal display for goal command results.
    Node.js could capture this output or call structured data functions.
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    display_success_result(result)  # Rich formatting

# For structured data exchange with Node.js:
def get_goal_display_data(result: Dict[str, Any]) -> Dict[str, Any]:
    """Returns JSON-serializable data for Node.js terminal rendering"""
    return {
        "display_type": "workflow_creation_success",
        "workflow_data": {...},
        "rich_formatting_hints": {...}
    }
```

#### Data Exchange Formats
- **Rich Display**: Uses Rich library for immediate terminal output
- **Structured Data**: Can provide JSON-serializable data for Node.js consumption
- **Progress Indicators**: Stage-based progress feedback during creation
- **Help Integration**: Built-in help and usage guidance

#### Terminal UI Rendering
```python
# Rich terminal components for professional display:
console = Console()

# Success panels with green styling
console.print(Panel(
    f"[green]Workflow Created Successfully[/green]\n"
    f"[bold]{result.get('message', 'Workflow ready for execution')}[/bold]",
    title="Goal → Workflow",
    style="green"
))

# Structured details table
details_table = Table(show_header=False, box=None, padding=(0, 2))
details_table.add_column("Label", style="dim", width=20)
details_table.add_column("Value", style="bold")

# Error panels with troubleshooting
console.print(Panel(
    f"[red]Error:[/red] {error_message}",
    style="red",
    title="Goal Command Error"
))
```

#### Configuration & State Sharing
- **Rich Console**: Module-level console for consistent formatting
- **Cache Integration**: CacheManager for performance optimization
- **Error Handling**: Standard MAO error handling decorators

## Written & Illustrated Data Info

### Data In-Flow
- **Natural Language Goals**: User goal descriptions for workflow creation
- **Command Results**: Workflow creation results from goal processing
- **Progress Updates**: Stage-by-stage progress during workflow generation
- **Error Context**: Detailed error information for troubleshooting

### Data Out-Flow
- **Rich Terminal Display**: Professional formatted output with colors and panels
- **Workflow Details**: Comprehensive workflow information display
- **Progress Feedback**: Real-time status updates during creation
- **Troubleshooting Guidance**: Error-specific help and suggestions

### Integration Touchpoints
- **Goal Processing System**: Receives workflow creation results
- **Rich Terminal Framework**: Advanced terminal display capabilities
- **Help System Integration**: Built-in usage guidance and examples
- **Error Recovery Pipeline**: Comprehensive error handling and suggestions

## Rich Terminal Display Features

### Success Display Components
```python
def display_success_result(result: Dict[str, Any]) -> None:
    """Professional success display with Rich components"""
    
    # Header panel with success confirmation
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
```

### Progress Tracking
```python
def display_goal_progress(stage: str) -> None:
    """Real-time progress indicators"""
    progress_messages = {
        "analyzing": "Analyzing your goal...",
        "creating": "Creating workflow configuration...",
        "setting_up": "Setting up custom command...",
        "finalizing": "Finalizing workflow..."
    }
    
    message = progress_messages.get(stage, f"Processing {stage}...")
    console.print(f"[dim]• {message}[/dim]")
```

### Error Display System
```python
def display_error(error_message: str) -> None:
    """Comprehensive error display with troubleshooting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="Goal Command Error"
    ))
    
    # Troubleshooting tips
    console.print(f"\n[dim]Common solutions:[/dim]")
    console.print(f"[dim]• Ensure your goal is clear and specific[/dim]")
    console.print(f"[dim]• Check that setup scripts are available[/dim]")
    console.print(f"[dim]• Try with mao --verbose for more details[/dim]")
```

## Dependencies
- **rich library**: Console, Table, Panel, Text for advanced terminal display
- **orchestrator.cache.cache_system**: CacheManager for performance
- **orchestrator.error_handling**: handle_errors decorator
- **typing**: Type hints for structured interfaces

## Professional Software Architecture Notes
This component represents professional terminal UI design patterns:
- **Rich Terminal Integration**: Advanced formatting with colors, panels, and tables
- **Progress Feedback**: Real-time user feedback during long operations
- **Error Recovery**: Comprehensive error display with specific troubleshooting steps
- **Consistent Styling**: Professional color schemes and layout patterns
- **Dual Interface**: Can provide both Rich display and structured data

This is exactly how professional terminal applications provide rich user experiences - advanced formatting libraries combined with structured data patterns for flexible integration.