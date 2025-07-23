"""
FILES API TOOL
UI Display Components  
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import Dict, Any

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

console = Console()
cache = CacheManager()


@handle_errors(operation_name="display_files_api_result", return_dict=False)
def display_files_api_result(result: Dict[str, Any], interface: str = "terminal") -> None:
    """
    Display Files API results with beautiful formatting
    
    Args:
        result: Files API execution result
        interface: "terminal" or "web"
    """
    
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    if interface == "terminal":
        display_terminal_results(result)
    elif interface == "web":
        display_web_results(result)


@handle_errors(operation_name="display_terminal_results", return_dict=False)
def display_terminal_results(result: Dict[str, Any]) -> None:
    """Display Files API results in beautiful terminal format"""
    
    operation = result.get("operation", "files_api_operation")
    
    # Create header panel
    title = "📁 Files API Results"
    console.print(Panel(title, style="bold blue"))
    
    # Display based on operation type
    if "workspace_structure" in result:
        display_workspace_creation(result)
    elif "draft_info" in result:
        display_draft_save(result)
    elif "handoff_id" in result:
        display_handoff_preparation(result)
    elif "saved_files" in result:
        display_deliverables_save(result)
    elif "workflow_files" in result:
        display_workflow_files(result)
    else:
        display_generic_result(result)
    
    # Display cost information
    cost = result.get("cost", 0.0)
    cost_text = Text(f"💰 Cost: ${cost:.4f}", style="green")
    console.print(cost_text)


def display_workspace_creation(result: Dict[str, Any]) -> None:
    """Display workspace creation results"""
    workspace = result.get("workspace_structure", {})
    
    console.print("✅ Workspace Created Successfully", style="bold green")
    
    # Create workspace structure table
    table = Table(title="Workspace Structure", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", min_width=15)
    table.add_column("Path", style="white")
    
    for component, path in workspace.items():
        table.add_row(component.replace("_", " ").title(), path)
    
    console.print(table)
    
    metadata_file = result.get("metadata_file")
    if metadata_file:
        console.print(f"📄 Metadata: {metadata_file}", style="dim")


def display_draft_save(result: Dict[str, Any]) -> None:
    """Display draft save results"""
    draft_info = result.get("draft_info", {})
    
    console.print("💾 Draft Saved Successfully", style="bold green")
    
    # Draft details
    filename = draft_info.get("filename", "unknown")
    draft_type = draft_info.get("draft_type", "general")
    content_length = draft_info.get("content_length", 0)
    saved_time = draft_info.get("saved", "unknown")
    
    details_table = Table(show_header=False)
    details_table.add_column("Label", style="cyan", min_width=12)
    details_table.add_column("Value", style="white")
    
    details_table.add_row("📄 Filename:", filename)
    details_table.add_row("📋 Type:", draft_type)
    details_table.add_row("📏 Size:", f"{content_length:,} characters")
    details_table.add_row("⏰ Saved:", saved_time)
    
    console.print(details_table)


def display_handoff_preparation(result: Dict[str, Any]) -> None:
    """Display handoff preparation results"""
    handoff_id = result.get("handoff_id", "unknown")
    materials_count = result.get("materials_count", 0)
    package_file = result.get("package_file", "unknown")
    
    console.print("🤝 Handoff Package Prepared", style="bold green")
    
    # Handoff details
    details_table = Table(show_header=False)
    details_table.add_column("Label", style="cyan", min_width=12)
    details_table.add_column("Value", style="white")
    
    details_table.add_row("🆔 Handoff ID:", handoff_id)
    details_table.add_row("📦 Materials:", f"{materials_count} items")
    details_table.add_row("📄 Package:", package_file)
    
    console.print(details_table)


def display_deliverables_save(result: Dict[str, Any]) -> None:
    """Display deliverables save results"""
    saved_files = result.get("saved_files", {})
    deliverables_count = result.get("deliverables_count", 0)
    phase = result.get("phase", "unknown")
    
    console.print("📋 Deliverables Saved Successfully", style="bold green")
    
    # Summary info
    summary_table = Table(show_header=False)
    summary_table.add_column("Label", style="cyan", min_width=12)
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("🎯 Phase:", phase)
    summary_table.add_row("📄 Files:", f"{deliverables_count} deliverables")
    
    console.print(summary_table)
    
    # Individual files
    if saved_files:
        console.print(Path(r"\n📁 Saved Files:"), style="bold")
        files_table = Table(show_header=True, header_style="bold magenta")
        files_table.add_column("Deliverable", style="cyan")
        files_table.add_column("Filename", style="white")
        files_table.add_column("Size", style="yellow", justify="right")
        
        for name, info in saved_files.items():
            filename = info.get("filename", "unknown")
            size = info.get("size", 0)
            files_table.add_row(name, filename, f"{size:,} chars")
        
        console.print(files_table)


def display_workflow_files(result: Dict[str, Any]) -> None:
    """Display workflow files listing"""
    workflow_files = result.get("workflow_files", {})
    total_files = result.get("total_files", 0)
    workspace_path = result.get("workspace_path", "unknown")
    
    console.print("📂 Workflow Files Retrieved", style="bold green")
    
    # Summary
    summary_table = Table(show_header=False)
    summary_table.add_column("Label", style="cyan", min_width=12)
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("📊 Total Files:", f"{total_files}")
    summary_table.add_row("📁 Workspace:", workspace_path)
    
    console.print(summary_table)
    
    # Files by category
    if workflow_files:
        console.print(Path(r"\n📋 Files by Category:"), style="bold")
        category_table = Table(show_header=True, header_style="bold magenta")
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Count", style="yellow", justify="right")
        category_table.add_column("Latest File", style="white")
        
        for category, file_list in workflow_files.items():
            count = len(file_list)
            if count > 0:
                # Get most recent file
                latest_file = max(file_list, key=lambda f: f.get("modified", 0))
                latest_name = latest_file.get("filename", "unknown")
                category_table.add_row(category.title(), str(count), latest_name)
            else:
                category_table.add_row(category.title(), "0", "—")
        
        console.print(category_table)


def display_generic_result(result: Dict[str, Any]) -> None:
    """Display generic Files API result"""
    console.print("📁 Files API Operation Completed", style="bold green")
    
    # Display all result keys
    if result:
        details_table = Table(show_header=False)
        details_table.add_column("Key", style="cyan")
        details_table.add_column("Value", style="white")
        
        for key, value in result.items():
            if key != "cost":  # Cost displayed separately
                str_value = str(value)
                if len(str_value) > 50:
                    str_value = str_value[:47] + "..."
                details_table.add_row(key.replace("_", " ").title(), str_value)
        
        console.print(details_table)


@handle_errors(operation_name="display_error", return_dict=False)
def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="Files API Error",
        border_style="red"
    )
    console.print(panel)


def display_web_results(result: Dict[str, Any]) -> None:
    """Display Files API results for web interface"""
    # Simple text output for web interface
    operation = result.get("operation", "files_api")
    
    if result.get("error"):
        console.print(f"❌ Files API Error: {result.get('error', 'Unknown error')}")
        return
    
    console.print(f"✅ Files API {operation} completed successfully")
    
    # Display key result information
    for key, value in result.items():
        if key not in ["status", "cost"]:
            console.print(f"  {key}: {value}")
    
    cost = result.get("cost", 0.0)
    console.print(f"💰 Cost: ${cost:.4f}")


def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for Files API operations"""
    if cost == 0:
        console.print("💰 Cost: FREE", style="green bold")
    else:
        console.print(f"💰 Estimated cost: ${cost:.4f}", style="yellow")
    
    if verbose:
        console.print("   Files API operations are typically low cost", style="dim")


def display_operation_summary(results: Dict[str, Any], verbose: bool = False) -> None:
    """Display a summary of Files API operations"""
    if results.get("error"):
        display_error(results.get("error", "Unknown error"))
        return
    
    operation = results.get("operation", "Unknown")
    console.print(f"✅ {operation} completed successfully", style="green bold")
    
    if verbose and results:
        console.print(Path(r"\n📋 Operation Details:"), style="bold")
        for key, value in results.items():
            if key not in ["status", "error", "cost"]:
                console.print(f"   {key}: {value}", style="dim")


@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Estimate cost for UI operations (typically free)
    
    Args:
        params: Operation parameters
        
    Returns:
        Cost estimate (0.0 for UI operations)
    """
    return 0.0  # UI operations are free
