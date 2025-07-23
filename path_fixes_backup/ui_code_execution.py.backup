#!/usr/bin/env python3
"""
Code Execution UI Components
Rich console display for Python code execution results
"""

from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich import box

console = Console()

def display_code_execution_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """Display code execution operation results with beautiful formatting"""
    
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    if result.get("success", False):
        panel_style = "green"
        title = "✅ Code Execution Successful"
    else:
        panel_style = "red"
        title = "❌ Code Execution Failed"
    
    content = []
    content.append(f"🆔 Execution ID: {result.get('execution_id', 'N/A')}")
    content.append(f"⏰ Time: {result['timestamp'].split('T')[1][:8] if 'T' in result['timestamp'] else result['timestamp']}")
    
    if result.get("container_id"):
        content.append(f"🔗 Container: {result['container_id']}")
    
    if result["success"]:
        content.append(f"✅ Return Code: {result.get('return_code', 0)}")
        
        if result.get("stdout"):
            content.append("📊 Output:")
            # Truncate long output unless verbose
            output = result["stdout"]
            if len(output) > 500 and not verbose:
                output = output[:497] + "..."
            content.append(output)
        
        if result.get("files"):
            content.append(f"📁 Files Generated: {len(result['files'])}")
            for file_info in result["files"]:
                content.append(f"  • {file_info.get('filename', 'unknown')} (ID: {file_info.get('file_id', 'N/A')})")
    else:
        if result.get("stderr"):
            content.append(f"⚠️ Error Output: {result['stderr']}")
        if result.get("error"):
            content.append(f"🚨 Exception: {result['error']}")
        if result.get("return_code") is not None:
            content.append(f"❌ Return Code: {result['return_code']}")
    
    panel = Panel(
        "\n".join(content),
        title=title,
        border_style=panel_style,
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_code_with_syntax(code: str, language: str = "python") -> None:
    """Display code with syntax highlighting"""
    
    syntax = Syntax(
        code,
        language,
        theme="monokai",
        line_numbers=True,
        background_color="default"
    )
    
    panel = Panel(
        syntax,
        title="🐍 Python Code",
        border_style="blue",
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_execution_files(files: List[Dict[str, Any]], verbose: bool = False) -> None:
    """Display execution files in formatted table"""
    
    if not files:
        console.print("📁 No files generated during execution")
        console.print()
        return
    
    table = Table(
        title="📁 Generated Files",
        box=box.ROUNDED,
        header_style="bold cyan"
    )
    
    table.add_column("Filename", style="white", no_wrap=True)
    table.add_column("File ID", style="dim")
    table.add_column("Type", style="cyan")
    table.add_column("Size", justify="right", style="green")
    
    if verbose:
        table.add_column("Status", justify="center")
    
    for file_info in files:
        filename = file_info.get("filename", "unknown")
        file_id = file_info.get("file_id", "N/A")
        file_type = file_info.get("type", "unknown")
        size = str(file_info.get("size", "N/A"))
        
        if size != "N/A":
            # Format file size
            size_bytes = int(size) if size.isdigit() else 0
            if size_bytes > 1024 * 1024:
                size = f"{size_bytes / (1024 * 1024):.1f} MB"
            elif size_bytes > 1024:
                size = f"{size_bytes / 1024:.1f} KB"
            else:
                size = f"{size_bytes} B"
        
        row = [filename, file_id[:20] + "..." if len(file_id) > 20 else file_id, file_type, size]
        
        if verbose:
            status = "✅ Ready" if file_info.get("success", True) else "❌ Error"
            row.append(status)
        
        table.add_row(*row)
    
    console.print(table)
    console.print()


def display_container_info(container_info: Dict[str, Any]) -> None:
    """Display container information"""
    
    if container_info.get("error"):
        display_error(container_info.get("error", "Unknown error"))
        return
        
    if container_info.get("success", False):
        panel_style = "green"
        title = "🔗 Container Created Successfully"
        content = [
            f"🆔 Container ID: {container_info.get('container_id', 'N/A')}",
            f"⏰ Expires At: {container_info.get('expires_at', 'N/A')}",
            f"📅 Created: {container_info['timestamp'].split('T')[1][:8] if 'T' in container_info['timestamp'] else container_info['timestamp']}",
            "",
            "💡 This container will persist for 1 hour and can be reused",
            "   for multiple executions to maintain state and files."
        ]
    else:
        panel_style = "red"
        title = "❌ Container Creation Failed"
        content = [
            f"🚨 Error: {container_info.get('error', 'Unknown error')}",
            f"📅 Attempted: {container_info['timestamp'].split('T')[1][:8] if 'T' in container_info['timestamp'] else container_info['timestamp']}"
        ]
    
    panel = Panel(
        "\n".join(content),
        title=title,
        border_style=panel_style,
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_download_results(results: List[Dict[str, Any]], verbose: bool = False) -> None:
    """Display file download results"""
    
    success_count = sum(1 for r in results if r.get("success", False))
    
    table = Table(
        title=f"📥 File Downloads ({success_count}/{len(results)} successful)",
        box=box.ROUNDED,
        header_style="bold cyan"
    )
    
    table.add_column("Filename", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Size", justify="right", style="green")
    
    if verbose:
        table.add_column("File ID", style="dim")
        table.add_column("Error", style="red")
    
    for result in results:
        filename = result.get("filename", "unknown")
        success = result.get("success", False)
        
        if success:
            status = Text("✅ Success", style="green")
            size = result.get("size", 0)
            if size > 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
        else:
            status = Text("❌ Failed", style="red")
            size_str = "N/A"
        
        row = [filename, status, size_str]
        
        if verbose:
            file_id = result.get("file_id", "N/A")
            error = result.get("error", "") if not success else ""
            row.extend([file_id[:20] + "..." if len(file_id) > 20 else file_id, error[:30] + "..." if len(error) > 30 else error])
        
        table.add_row(*row)
    
    console.print(table)
    console.print()


def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="Code Execution Error",
        border_style="red"
    )
    console.print(panel)


def display_execution_summary(executions: List[Dict[str, Any]]) -> None:
    """Display summary of multiple executions"""
    
    if not executions:
        console.print("📊 No code executions found")
        console.print()
        return
    
    table = Table(
        title="📊 Code Execution Summary",
        box=box.ROUNDED,
        header_style="bold cyan"
    )
    
    table.add_column("Execution ID", style="white", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Files", justify="right", style="cyan")
    table.add_column("Time", style="dim")
    
    for execution in executions:
        exec_id = execution.get("execution_id", "unknown")[:12]
        success = execution.get("success", False)
        
        if success:
            status = Text("✅ Success", style="green")
        else:
            status = Text("❌ Failed", style="red")
        
        files_count = str(len(execution.get("files", [])))
        timestamp = execution.get("timestamp", "")
        time_str = timestamp.split("T")[1][:8] if "T" in timestamp else timestamp
        
        table.add_row(exec_id, status, files_count, time_str)
    
    console.print(table)
    console.print()


def display_help() -> None:
    """Display Code Execution Tool help information"""
    
    help_content = [
        "🐍 Code Execution Tool Operations:",
        "",
        "📝 execute_code - Run Python code in Claude's secure sandbox",
        "📁 execute_with_files - Run code with uploaded file inputs",
        "🔗 create_container - Create persistent execution environment",
        "📥 download_files - Download files generated during execution",
        "",
        "💡 Features:",
        "  • Secure Python 3.11 sandbox environment",
        "  • Pre-installed data science libraries (pandas, numpy, matplotlib)",
        "  • File upload/download integration",
        "  • Persistent containers for multi-step workflows",
        "  • 1GB RAM, 5GB storage per container",
        "",
        "⚠️ Limitations:",
        "  • No internet access (security isolation)",
        "  • 1 hour container expiration",
        "  • Minimum 5-minute billing per session"
    ]
    
    panel = Panel(
        "\n".join(help_content),
        title="🐍 Code Execution Help",
        border_style="blue",
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()
