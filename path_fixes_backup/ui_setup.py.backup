"""
Setup CLI Command - UI Display Patterns
Professional display of workflow setup results and progress feedback
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

def display_setup_result(result: Dict[str, Any]) -> None:
    """
    Display setup command results with consistent CLI UI patterns.
    
    Args:
        result: Setup execution result from setup.py
    """
    if not result.get("success", True):
        display_setup_error(result)
        return
    
    # Successful setup display
    setup_type = result.get("setup_type", "unknown")
    
    if setup_type == "single_file":
        _display_file_setup_success(result)
    elif setup_type == "directory":
        _display_directory_setup_success(result)
    else:
        _display_generic_setup_success(result)

def _display_file_setup_success(result: Dict[str, Any]) -> None:
    """Display successful single file setup"""
    
    # Main success panel
    success_content = Text()
    success_content.append("Workflow Setup Complete\n", style="bold green")
    success_content.append(f"Source: {result.get('source_file', 'Unknown')}", style="dim")
    
    console.print(Panel(
        success_content,
        title="Setup Successful",
        style="green",
        border_style="green"
    ))
    
    # Workflow details table
    details_table = Table(title="Workflow Details")
    details_table.add_column("Property", style="cyan")
    details_table.add_column("Value", style="white")
    
    details_table.add_row("Workflow ID", result.get("workflow_id", "N/A"))
    details_table.add_row("Custom Command", result.get("custom_command", "N/A"))
    details_table.add_row("Directory", result.get("workflow_directory", "N/A"))
    details_table.add_row("Setup Type", "Single Configuration File")
    
    console.print(details_table)
    
    # Created structure display
    created_files = result.get("created_structure", [])
    if created_files:
        console.print("\n[bold]Created Directory Structure:[/bold]")
        for file_path in created_files:
            console.print(f"  • {file_path}", style="green")
    
    # Next steps guidance
    console.print(Panel(
        f"Your workflow is ready! Use command: [bold cyan]{result.get('custom_command', 'workflow')}[/bold cyan]",
        title="Next Steps",
        style="blue"
    ))

def _display_directory_setup_success(result: Dict[str, Any]) -> None:
    """Display successful directory setup"""
    
    # Main success panel
    success_content = Text()
    success_content.append("Workflow Directory Setup Complete\n", style="bold green")
    success_content.append(f"Source: {result.get('source_directory', 'Unknown')}", style="dim")
    
    console.print(Panel(
        success_content,
        title="Directory Setup Successful",
        style="green",
        border_style="green"
    ))
    
    # Workflow details table
    details_table = Table(title="Workflow Details")
    details_table.add_column("Property", style="cyan")
    details_table.add_column("Value", style="white")
    
    details_table.add_row("Workflow ID", result.get("workflow_id", "N/A"))
    details_table.add_row("Custom Command", result.get("custom_command", "N/A"))
    details_table.add_row("Final Directory", result.get("workflow_directory", "N/A"))
    details_table.add_row("Main Config", result.get("main_config_file", "N/A"))
    details_table.add_row("Setup Type", "Directory Import")
    
    console.print(details_table)
    
    # Configuration files found
    config_files = result.get("config_files_found", [])
    if config_files:
        console.print("\n[bold]Configuration Files Found:[/bold]")
        for config_file in config_files:
            console.print(f"  • {config_file}", style="green")
    
    # Validation warnings if any
    validation_errors = result.get("validation_errors")
    if validation_errors:
        console.print("\n[bold yellow]Validation Warnings:[/bold yellow]")
        for error in validation_errors:
            console.print(f"  ! {error}", style="yellow")
    
    # Next steps guidance
    console.print(Panel(
        f"Directory imported successfully! Use command: [bold cyan]{result.get('custom_command', 'workflow')}[/bold cyan]",
        title="Next Steps",
        style="blue"
    ))

def _display_generic_setup_success(result: Dict[str, Any]) -> None:
    """Display generic successful setup"""
    
    console.print(Panel(
        "Workflow setup completed successfully",
        title="Setup Complete",
        style="green"
    ))
    
    # Basic workflow information
    if result.get("workflow_id"):
        console.print(f"Workflow ID: [cyan]{result['workflow_id']}[/cyan]")
    
    if result.get("custom_command"):
        console.print(f"Custom Command: [cyan]{result['custom_command']}[/cyan]")
    
    if result.get("workflow_directory"):
        console.print(f"Directory: [dim]{result['workflow_directory']}[/dim]")

def display_setup_error(result: Dict[str, Any]) -> None:
    """Display setup errors with helpful guidance"""
    
    error_message = result.get("error", "Unknown setup error occurred")
    error_type = result.get("error_type", "unknown_error")
    
    # Main error panel
    console.print(Panel(
        f"[red]Setup Failed:[/red] {error_message}",
        title="Setup Error",
        style="red",
        border_style="red"
    ))
    
    # Error-specific guidance
    guidance = _get_error_guidance(error_type, result)
    if guidance:
        console.print(Panel(
            guidance,
            title="Troubleshooting",
            style="yellow"
        ))
    
    # Additional error details if available
    if result.get("path"):
        console.print(f"\nPath: [dim]{result['path']}[/dim]")
    
    if result.get("file"):
        console.print(f"File: [dim]{result['file']}[/dim]")
    
    if result.get("directory"):
        console.print(f"Directory: [dim]{result['directory']}[/dim]")
    
    # Validation errors
    validation_errors = result.get("validation_errors")
    if validation_errors:
        console.print("\n[bold red]Validation Errors:[/bold red]")
        for error in validation_errors:
            console.print(f"  × {error}", style="red")

def _get_error_guidance(error_type: str, result: Dict[str, Any]) -> str:
    """Get contextual error guidance based on error type"""
    
    guidance_map = {
        "path_not_found": "Verify the file or directory path exists and is accessible. Use absolute paths for reliability.",
        
        "invalid_path_type": "Ensure the path points to either a JSON configuration file or a directory containing workflow configs.",
        
        "config_validation_error": "Check that your JSON configuration file is valid and contains required workflow fields: workflow_id, custom_command.",
        
        "missing_required_fields": "Workflow configuration must include 'workflow_id' and 'custom_command' fields. Refer to workflow templates for proper structure.",
        
        "no_config_files": "Directory must contain at least one workflow configuration file. Look for files ending in '_workflow_config.json' or containing 'workflow' in the name.",
        
        "no_valid_config": "None of the found configuration files are valid. Check JSON syntax and required fields in each file.",
        
        "directory_creation_error": "Unable to create workflow directory structure. Check permissions and available disk space.",
        
        "directory_copy_error": "Failed to copy workflow directory. Ensure source directory is accessible and target location has sufficient space.",
        
        "target_exists": "A workflow with this name already exists. Use a different custom_command or remove the existing workflow first.",
        
        "tracking_initialization_error": "Workflow setup completed but state tracking failed. The workflow is usable but may not be properly tracked.",
        
        "setup_execution_error": "An unexpected error occurred during setup. Check file permissions and system resources."
    }
    
    return guidance_map.get(error_type, "Check the error message above and verify your configuration files and system permissions.")

def display_setup_progress(message: str) -> None:
    """Display setup progress message"""
    console.print(f"[dim]Setup: {message}[/dim]")

def display_validation_progress(files: List[str]) -> None:
    """Display validation progress for multiple files"""
    console.print(f"[dim]Validating {len(files)} configuration files...[/dim]")
    
    for file_name in files:
        console.print(f"  • Checking {file_name}", style="dim")

def display_setup_summary(workflow_count: int = 1) -> None:
    """Display setup operation summary"""
    
    if workflow_count == 1:
        console.print("\n[green]✓[/green] 1 workflow setup completed")
    else:
        console.print(f"\n[green]✓[/green] {workflow_count} workflows setup completed")

def display_multi_setup_results(results: List[Dict[str, Any]]) -> None:
    """Display results for multiple workflow setups"""
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    # Summary table
    summary_table = Table(title="Setup Results Summary")
    summary_table.add_column("Status", style="cyan")
    summary_table.add_column("Count", justify="right")
    summary_table.add_column("Details", style="dim")
    
    summary_table.add_row("Successful", str(len(successful)), f"{len(successful)} workflows ready")
    summary_table.add_row("Failed", str(len(failed)), f"{len(failed)} setups failed")
    
    console.print(summary_table)
    
    # Display individual results
    if successful:
        console.print("\n[bold green]Successful Setups:[/bold green]")
        for result in successful:
            console.print(f"  ✓ {result.get('custom_command', 'Unknown')} - {result.get('workflow_id', 'N/A')}")
    
    if failed:
        console.print("\n[bold red]Failed Setups:[/bold red]")
        for result in failed:
            console.print(f"  × {result.get('error', 'Unknown error')}")

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate setup UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free