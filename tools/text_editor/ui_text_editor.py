"""
TEXT EDITOR
UI Display Component
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.tree import Tree
from rich.columns import Columns
from typing import Dict, Any
from pathlib import Path

console = Console()

def display_error(error_message: str):
    """Display standardized error message with Panel formatting"""
    console.print(Panel(
        f"[red]❌ {error_message}[ / red]",
        title="[bold red]Error[ / bold red]",
        border_style="red"
    ))

def display_text_editor_result(result: Dict[str, Any], verbose: bool = False):
    """
    Display text editor operation results with beautiful formatting
    
    Args:
        result: Result dictionary from text editor operations
        verbose: Whether to show detailed information
    """
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    operation = result.get("operation", "unknown")
    
    if operation == "create_document":
        _display_document_creation(result, verbose)
    elif operation == "edit_content":
        _display_content_edit(result, verbose)
    elif operation == "append_content":
        _display_content_append(result, verbose)
    elif operation == "format_document":
        _display_document_format(result, verbose)
    elif operation == "document_info":
        _display_document_info(result, verbose)
    elif operation == "path_validation":
        _display_path_validation(result, verbose)
    elif operation == "template_creation":
        _display_template_creation(result, verbose)
    else:
        _display_generic_result(result, verbose)

def _display_document_creation(result: Dict[str, Any], verbose: bool):
    """Display document creation results"""
    file_name = result.get("file_name", "Unknown")
    content_length = result.get("content_length", 0)
    document_type = result.get("document_type", "general")
    
    # Main success message
    console.print(f"[green]✅ Document created: {file_name}[ / green]")
    
    if verbose:
        # Detailed information panel
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("📝 Document Type", document_type.title())
        info_table.add_row("📊 Content Length", f"{content_length:,} characters")
        info_table.add_row("⏰ Created", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Document Details[ / bold]", border_style="green"))
    else:
        console.print(f"[dim]📝 {document_type.title()} • {content_length:,} characters[ / dim]")

def _display_content_edit(result: Dict[str, Any], verbose: bool):
    """Display content editing results"""
    file_name = result.get("file_name", "Unknown")
    change_delta = result.get("change_delta", 0)
    backup_path = result.get("backup_path")
    
    # Main success message with change indicator
    if change_delta > 0:
        change_text = f"[green]+{change_delta}[ / green]"
    elif change_delta < 0:
        change_text = f"[red]{change_delta}[ / red]"
    else:
        change_text = "[yellow]±0[ / yellow]"
    
    console.print(f"[green]✅ Content updated: {file_name}[ / green] {change_text}")
    
    if verbose:
        # Detailed edit information
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("📊 Original Length", f"{result.get('original_length', 0):,} characters")
        info_table.add_row("📊 Updated Length", f"{result.get('updated_length', 0):,} characters")
        info_table.add_row("📈 Change Delta", f"{change_delta:+,} characters")
        
        if backup_path:
            info_table.add_row("💾 Backup Created", backup_path.split(' / ')[-1])
        
        info_table.add_row("⏰ Modified", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Edit Details[ / bold]", border_style="green"))
    else:
        if backup_path:
            console.print(f"[dim]💾 Backup created • {result.get('updated_length', 0):,} characters total[ / dim]")

def _display_content_append(result: Dict[str, Any], verbose: bool):
    """Display content append results"""
    file_name = result.get("file_name", "Unknown")
    appended_length = result.get("appended_length", 0)
    total_length = result.get("total_length", 0)
    
    console.print(f"[green]✅ Content appended: {file_name}[/green] [green]+{appended_length}[ / green]")
    
    if verbose:
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("📊 Original Length", f"{result.get('original_length', 0):,} characters")
        info_table.add_row("📝 Appended Length", f"{appended_length:,} characters")
        info_table.add_row("📊 Total Length", f"{total_length:,} characters")
        info_table.add_row("⏰ Modified", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Append Details[ / bold]", border_style="green"))
    else:
        console.print(f"[dim]📊 Total: {total_length:,} characters[ / dim]")

def _display_document_format(result: Dict[str, Any], verbose: bool):
    """Display document formatting preparation results"""
    file_name = result.get("file_name", "Unknown")
    format_type = result.get("format_type", "unknown")
    content_length = result.get("content_length", 0)
    
    console.print(f"[green]✅ Document ready for AI formatting: {file_name}[ / green]")
    
    if verbose:
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("🎨 Format Type", format_type.title())
        info_table.add_row("📊 Content Length", f"{content_length:,} characters")
        
        backup_path = result.get("backup_path")
        if backup_path:
            info_table.add_row("💾 Backup Created", backup_path.split(' / ')[-1])
        
        info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Format Preparation[ / bold]", border_style="blue"))
    else:
        console.print(f"[dim]🎨 {format_type.title()} formatting • {content_length:,} characters[ / dim]")

def _display_document_info(result: Dict[str, Any], verbose: bool):
    """Display comprehensive document information"""
    file_name = result.get("file_name", "Unknown")
    content_stats = result.get("content_stats", {})
    
    console.print(f"[blue]📊 Document Analysis: {file_name}[ / blue]")
    
    if verbose:
        # File information
        file_table = Table(show_header=False, box=None, padding=(0, 1))
        file_table.add_column("Property", style="cyan")
        file_table.add_column("Value", style="white")
        
        file_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        file_table.add_row("📁 File Size", f"{result.get('file_size_kb', 0)} KB")
        file_table.add_row("📝 Document Type", result.get("document_type", "unknown").title())
        file_table.add_row("📅 Created", result.get("created", "Unknown"))
        file_table.add_row("📅 Modified", result.get("modified", "Unknown"))
        
        # Content statistics
        stats_table = Table(show_header=False, box=None, padding=(0, 1))
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Count", style="white")
        
        stats_table.add_row("Characters", f"{content_stats.get('characters', 0):,}")
        stats_table.add_row("Characters (no spaces)", f"{content_stats.get('characters_no_spaces', 0):,}")
        stats_table.add_row("Words", f"{content_stats.get('words', 0):,}")
        stats_table.add_row("Lines", f"{content_stats.get('lines', 0):,}")
        stats_table.add_row("Paragraphs", f"{content_stats.get('paragraphs', 0):,}")
        stats_table.add_row("Empty Lines", f"{content_stats.get('empty_lines', 0):,}")
        
        # Display in columns
        console.print(Columns([
            Panel(file_table, title="[bold]File Information[ / bold]", border_style="blue"),
            Panel(stats_table, title="[bold]Content Statistics[ / bold]", border_style="green")
        ]))
    else:
        # Compact display
        words = content_stats.get('words', 0)
        lines = content_stats.get('lines', 0)
        console.print(f"[dim]📊 {words:,} words • {lines:,} lines • {result.get('file_size_kb', 0)} KB[ / dim]")

def _display_path_validation(result: Dict[str, Any], verbose: bool):
    """Display path validation results"""
    file_name = result.get("file_name", "Unknown")
    exists = result.get("exists", False)
    is_writable = result.get("is_writable", False)
    
    if exists:
        status_icon = "[green]✅[ / green]"
        status_text = "exists"
    else:
        status_icon = "[yellow]📝[ / yellow]"
        status_text = "will be created"
    
    console.print(f"{status_icon} Path validation: {file_name} {status_text}")
    
    if verbose:
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("📁 Directory", result.get("directory", "Unknown"))
        info_table.add_row("📋 Extension", result.get("extension", "None"))
        info_table.add_row("✅ Exists", "Yes" if exists else "No")
        info_table.add_row("✏️ Writable", "Yes" if is_writable else "No")
        
        console.print(Panel(info_table, title="[bold]Path Details[ / bold]", border_style="blue"))

def _display_template_creation(result: Dict[str, Any], verbose: bool):
    """Display template-based document creation results"""
    file_name = result.get("file_name", "Unknown")
    document_type = result.get("document_type", "general")
    content_length = result.get("content_length", 0)
    
    console.print(f"[green]✅ Document created from template: {file_name}[ / green]")
    
    if verbose:
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("📄 File Path", result.get("file_path", "Unknown"))
        info_table.add_row("📋 Template Type", document_type.title())
        info_table.add_row("📊 Content Length", f"{content_length:,} characters")
        info_table.add_row("⏰ Created", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Template Document[ / bold]", border_style="green"))
    else:
        console.print(f"[dim]📋 {document_type.title()} template • {content_length:,} characters[ / dim]")

def _display_generic_result(result: Dict[str, Any], verbose: bool):
    """Display generic operation results"""
    status = result.get("status", "unknown")
    operation = result.get("operation", "operation")
    
    if status == "success":
        console.print(f"[green]✅ {operation.replace('_', ' ').title()} completed successfully[ / green]")
    else:
        console.print(f"[yellow]⚠️ {operation.replace('_', ' ').title()}: {status}[ / yellow]")
    
    if verbose:
        # Display all available information
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        for key, value in result.items():
            if key not in ["status", "operation"]:
                display_key = key.replace('_', ' ').title()
                display_value = str(value)
                if len(display_value) > 50:
                    display_value = display_value[:47] + "..."
                info_table.add_row(display_key, display_value)
        
        console.print(Panel(info_table, title="[bold]Operation Details[ / bold]", border_style="blue"))

def display_autosave_status(file_path: str, operation: str = "saved"):
    """
    Display seamless autosave status (minimal, non-intrusive)
    
    Args:
        file_path: Path of the file being autosaved
        operation: Type of autosave operation
    """
    file_name = file_path.split(' / ')[-1] if ' / ' in file_path else file_path
    
    # Very subtle autosave indicator
    console.print(f"[dim green]💾 {file_name}[ / dim green]", end="")

def display_editing_session_start(file_path: str, document_type: str = "document"):
    """
    Display the start of an editing session
    
    Args:
        file_path: Path of the document being edited
        document_type: Type of document
    """
    file_name = file_path.split(' / ')[-1] if ' / ' in file_path else file_path
    
    console.print(f"[blue]📝 Editing: {file_name}[ / blue]")
    console.print(f"[dim]Document type: {document_type.title()}[ / dim]")

def display_editing_session_summary(results: list, total_time: float = None):
    """
    Display summary of an editing session
    
    Args:
        results: List of operation results from the session
        total_time: Total editing time in seconds
    """
    if not results:
        return
    
    total_operations = len(results)
    successful_operations = len([r for r in results if r.get("status") == "success"])
    
    console.print(f"\n[blue]📊 Editing Session Complete[" / "blue]")
    console.print(f"[dim]Operations: {successful_operations}/{total_operations} successful[ / dim]")
    
    if total_time:
        console.print(f"[dim]Duration: {total_time:.1f} seconds[ / dim]")

def display_agent_handoff_format(result: Dict[str, Any]):
    """
    Format result for agent-to-agent handoff
    
    Args:
        result: Result dictionary to format for handoff
    """
    if "error" in result:
        return f"❌ Text Editor Error: {result['error']}"
    
    operation = result.get("operation", "unknown")
    file_name = result.get("file_name", "Unknown")
    
    if operation == "create_document":
        content_length = result.get("content_length", 0)
        return f"✅ Created: {file_name} ({content_length:,} chars)"
    elif operation == "edit_content":
        change_delta = result.get("change_delta", 0)
        return f"✅ Edited: {file_name} ({change_delta:+,} chars)"
    elif operation == "append_content":
        appended_length = result.get("appended_length", 0)
        return f"✅ Appended: {file_name} (+{appended_length:,} chars)"
    else:
        return f"✅ {operation.replace('_', ' ').title()}: {file_name}" 