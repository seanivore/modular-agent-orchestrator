"""
FILE OPERATIONS
UI Display Component
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.tree import Tree
from typing import Dict, Any, List
from datetime import datetime

console = Console()

def display_file_operations_header(operation: str, file_path: str = "", verbose: bool = False):
    """Display file operations execution header"""
    print(f"📄 File Operation: {operation.replace('_', ' ').title()}")
    if file_path:
        print(f"📁 Target: {Path(file_path).name}")
    print("="*60)
    
    if verbose:
        print(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
        if file_path:
            print(f"🔗 Full Path: {file_path}")

def display_file_read_result(result: Dict[str, Any], verbose: bool = False):
    """Display file reading results with beautiful formatting"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    if result.get("status") == "success":
        metadata = result.get("metadata", {})
        content = result.get("content", "")
        
        # Create info panel
        info_text = f"""📁 [bold blue]{metadata.get('file_name', 'Unknown')}[/bold blue]
📊 Size: {metadata.get('file_size_kb', 0)} KB ({metadata.get('character_count', 0):,} chars)
🔤 Encoding: {metadata.get('encoding_used', 'unknown')}
📍 Path: {metadata.get('file_path', 'unknown')}"""
        
        if verbose:
            info_text += f"\n⏰ Read at: {metadata.get('timestamp', 'unknown')}"
        
        console.print(Panel(info_text, title="📄 File Information", border_style="blue"))
        
        if verbose:
            # Show content with syntax highlighting if possible
            console.print("\n📝 [bold]File Content:[/bold]")
            console.print("─" * 50)
            console.print(content)
        else:
            # Show truncated content
            preview = content[:200] + "..." if len(content) > 200 else content
            console.print(f"\n📝 [bold]Content Preview:[/bold]\n{preview}")

def display_directory_listing(result: Dict[str, Any], verbose: bool = False):
    """Display directory listing with tree structure"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    directory = result.get("directory", "unknown")
    pattern = result.get("pattern", "*")
    items = result.get("items", [])
    summary = result.get("summary", {})
    
    # Header panel
    header_text = f"""📂 Directory: [bold blue]{directory}[/bold blue]
🔍 Pattern: {pattern}
📊 Total Items: {summary.get('total_items', 0)} ({summary.get('directories', 0)} dirs, {summary.get('files', 0)} files)"""
    
    console.print(Panel(header_text, title="📁 Directory Listing", border_style="blue"))
    
    if not items:
        console.print("📭 [yellow]No items found matching pattern[/yellow]")
        return
    
    if verbose:
        # Detailed table view
        table = Table(title="📋 Detailed View")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Size", style="yellow")
        table.add_column("Modified", style="magenta")
        table.add_column("Permissions", style="red")
        
        for item in items:
            name = item.get("name", "unknown")
            if "item_count" in item:  # Directory
                item_type = "📁 Directory"
                size = f"{item.get('item_count', 0)} items"
            else:  # File
                item_type = "📄 File"
                size_kb = item.get("size_kb", 0)
                size_mb = item.get("size_mb")
                if size_mb:
                    size = f"{size_mb} MB"
                else:
                    size = f"{size_kb} KB"
            
            modified = item.get("modified", "unknown")[:19] if item.get("modified") else "unknown"
            permissions = item.get("permissions", "unknown")
            
            table.add_row(name, item_type, size, modified, permissions)
        
        console.print(table)
    else:
        # Simple tree view
        tree = Tree(f"📂 {directory}")
        
        # Separate directories and files
        directories = [item for item in items if "item_count" in item]
        files = [item for item in items if "item_count" not in item]
        
        # Add directories first
        for directory_item in directories:
            name = directory_item.get("name", "unknown")
            count = directory_item.get("item_count", 0)
            tree.add(f"📁 {name}/ ({count} items)")
        
        # Add files
        for file_item in files:
            name = file_item.get("name", "unknown")
            size_kb = file_item.get("size_kb", 0)
            tree.add(f"📄 {name} ({size_kb} KB)")
        
        console.print(tree)

def display_file_info(result: Dict[str, Any], verbose: bool = False):
    """Display comprehensive file information"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    # Basic info panel
    name = result.get("name", "unknown")
    path = result.get("path", "unknown")
    file_type = "📁 Directory" if result.get("is_directory") else f"📄 {result.get('file_type', 'File').title()}"
    
    basic_info = f"""📛 Name: [bold blue]{name}[/bold blue]
🏷️ Type: {file_type}
📍 Path: {path}"""
    
    if result.get("is_file"):
        size_kb = result.get("size_kb", 0)
        size_mb = result.get("size_mb")
        if size_mb:
            basic_info += f"\n📊 Size: {size_mb} MB ({size_kb} KB)"
        else:
            basic_info += f"\n📊 Size: {size_kb} KB"
    
    console.print(Panel(basic_info, title="📋 File Information", border_style="blue"))
    
    if verbose:
        # Detailed metadata table
        table = Table(title="🔍 Detailed Metadata")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        metadata_items = [
            ("Parent Directory", result.get("parent", "unknown")),
            ("Created", result.get("created", "unknown")[:19] if result.get("created") else "unknown"),
            ("Modified", result.get("modified", "unknown")[:19] if result.get("modified") else "unknown"),
            ("Accessed", result.get("accessed", "unknown")[:19] if result.get("accessed") else "unknown"),
            ("Permissions", result.get("permissions", "unknown")),
            ("Is Symlink", "Yes" if result.get("is_symlink") else "No"),
        ]
        
        if result.get("is_file"):
            metadata_items.extend([
                ("File Extension", result.get("suffix", "none")),
                ("File Stem", result.get("stem", "unknown")),
                ("Size (bytes)", f"{result.get('size_bytes', 0):,}"),
            ])
        
        for prop, value in metadata_items:
            table.add_row(prop, str(value))
        
        console.print(table)

def display_search_results(result: Dict[str, Any], verbose: bool = False):
    """Display file search results"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    search_dir = result.get("search_directory", "unknown")
    pattern = result.get("pattern", "unknown")
    summary = result.get("summary", {})
    results_data = result.get("results", {})
    
    # Search summary
    summary_text = f"""🔍 Search Directory: [bold blue]{search_dir}[/bold blue]
🎯 Pattern: "{pattern}"
📊 Total Found: {summary.get('total_found', 0)} ({summary.get('files_found', 0)} files, {summary.get('directories_found', 0)} dirs)
🔄 Recursive: {"Yes" if result.get('recursive') else "No"}
🔤 Case Sensitive: {"Yes" if result.get('case_sensitive') else "No"}"""
    
    console.print(Panel(summary_text, title="🔍 Search Results", border_style="green"))
    
    files = results_data.get("files", [])
    directories = results_data.get("directories", [])
    
    if not files and not directories:
        console.print("📭 [yellow]No matches found[/yellow]")
        return
    
    if verbose:
        # Detailed results with full paths
        if directories:
            console.print("\n📁 [bold]Directories Found:[/bold]")
            dir_table = Table()
            dir_table.add_column("Name", style="cyan")
            dir_table.add_column("Path", style="blue")
            dir_table.add_column("Depth", style="yellow")
            
            for directory in directories:
                dir_table.add_row(
                    directory.get("name", "unknown"),
                    directory.get("relative_path", "unknown"),
                    str(directory.get("depth", 0))
                )
            console.print(dir_table)
        
        if files:
            console.print("\n📄 [bold]Files Found:[/bold]")
            file_table = Table()
            file_table.add_column("Name", style="cyan")
            file_table.add_column("Path", style="blue")
            file_table.add_column("Size", style="yellow")
            file_table.add_column("Modified", style="magenta")
            file_table.add_column("Depth", style="red")
            
            for file_item in files:
                size = f"{file_item.get('size_kb', 0)} KB"
                modified = file_item.get("modified", "unknown")[:19] if file_item.get("modified") else "unknown"
                file_table.add_row(
                    file_item.get("name", "unknown"),
                    file_item.get("relative_path", "unknown"),
                    size,
                    modified,
                    str(file_item.get("depth", 0))
                )
            console.print(file_table)
    else:
        # Simple list view
        if directories:
            console.print("\n📁 [bold]Directories:[/bold]")
            for directory in directories:
                console.print(f"  📁 {directory.get('relative_path', 'unknown')}")
        
        if files:
            console.print("\n📄 [bold]Files:[/bold]")
            for file_item in files:
                size = f"{file_item.get('size_kb', 0)} KB"
                console.print(f"  📄 {file_item.get('relative_path', 'unknown')} ({size})")

def display_multiple_files_result(result: Dict[str, Any], verbose: bool = False):
    """Display multiple file reading results with progress summary"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    summary = result.get("summary", {})
    results = result.get("results", [])
    
    # Summary panel
    summary_text = f"""📚 Total Files: {summary.get('total_files', 0)}
✅ Successful: {summary.get('successful_reads', 0)}
❌ Failed: {summary.get('failed_reads', 0)}
📊 Total Size: {summary.get('total_size_kb', 0)} KB"""
    
    console.print(Panel(summary_text, title="📋 Batch Read Summary", border_style="green"))
    
    if verbose:
        # Show detailed results for each file
        for file_result in results:
            file_path = file_result.get("file_path", "unknown")
            file_data = file_result.get("result", {})
            
            console.print(f"\n📄 [bold]{file_path}[/bold]")
            console.print("─" * 40)
            
            if file_data.get("error"):
                console.print(f"❌ [red]{file_data['error']}[/red]")
            else:
                metadata = file_data.get("metadata", {})
                console.print(f"✅ {metadata.get('file_size_kb', 0)} KB, {metadata.get('character_count', 0):,} chars")
    else:
        # Show just the file list with status
        table = Table(title="📁 File Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Size", style="yellow")
        
        for file_result in results:
            file_path = file_result.get("file_path", "unknown")
            file_data = file_result.get("result", {})
            
            if file_data.get("error"):
                table.add_row(file_path, "❌ Error", "N/A")
            else:
                metadata = file_data.get("metadata", {})
                size = f"{metadata.get('file_size_kb', 0)} KB"
                table.add_row(file_path, "✅ Success", size)
        
        console.print(table)

def display_file_operations_progress(message: str, step: int = None, total: int = None):
    """Display file operations progress"""
    if step and total:
        progress = f"[{step}/{total}] "
    else:
        progress = ""
    
    print(f"⏳ {progress}{message}")

def display_file_tool_info(verbose: bool = False):
    """Display file operations tool information"""
    print("🔧 Enhanced File Operations")
    print("📝 Safe, efficient file and directory operations with comprehensive error handling")
    print("💰 Cost: Free")
    
    print("\n🎯 Capabilities:")
    print("   • File Management")
    print("   • Data Access")
    print("   • Directory Navigation")
    print("   • File Safety")
    
    print("\n📋 Use Cases:")
    print("   • Reading Resources")
    print("   • Organizing Work")
    print("   • File Discovery")
    print("   • Safe File Operations")
    
    if verbose:
        print("\n🏷️ Tags: core, files, essential, enhanced")
        print("🤖 Model compatibility: all")
        print("🔧 Functions: read_file, read_multiple_files, list_directory, get_file_info, move_file, search_files")

def display_operation_result(result: Dict[str, Any], operation_name: str, verbose: bool = False):
    """Display file operation results (move, delete, etc.)"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    if result.get("status") == "success":
        operation = result.get("operation", operation_name)
        
        if operation == "move":
            source = result.get("source", "unknown")
            destination = result.get("destination", "unknown")
            console.print(f"✅ [green]Successfully moved:[/green]")
            console.print(f"   📤 From: {source}")
            console.print(f"   📥 To: {destination}")
        
        elif operation in ["delete_file", "delete_directory", "delete_empty_directory"]:
            path = result.get("path", "unknown")
            console.print(f"✅ [green]Successfully deleted:[/green] {path}")
        
        else:
            console.print(f"✅ [green]Operation '{operation}' completed successfully[/green]")
        
        if verbose:
            timestamp = result.get("timestamp", "unknown")
            console.print(f"⏰ Completed at: {timestamp}")

def display_validation_results(result: Dict[str, Any], verbose: bool = False):
    """Display path validation results"""
    
    if result.get("error"):
        console.print(f"❌ [red]Error:[/red] {result['error']}")
        return
    
    summary = result.get("summary", {})
    validation_results = result.get("validation_results", [])
    
    # Summary panel
    summary_text = f"""📊 Total Paths: {summary.get('total_paths', 0)}
✅ Existing: {summary.get('existing_paths', 0)}
❌ Missing: {summary.get('missing_paths', 0)}"""
    
    console.print(Panel(summary_text, title="🔍 Path Validation Summary", border_style="blue"))
    
    if verbose:
        # Detailed validation table
        table = Table(title="📋 Validation Details")
        table.add_column("Path", style="cyan")
        table.add_column("Exists", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Absolute Path", style="blue")
        
        for validation in validation_results:
            path = validation.get("path", "unknown")
            exists = "✅ Yes" if validation.get("exists") else "❌ No"
            
            if validation.get("exists"):
                if validation.get("is_file"):
                    file_type = "📄 File"
                elif validation.get("is_directory"):
                    file_type = "📁 Directory"
                else:
                    file_type = "❓ Unknown"
            else:
                file_type = "N/A"
            
            abs_path = validation.get("absolute_path", "unknown")
            table.add_row(path, exists, file_type, abs_path)
        
        console.print(table)
    else:
        # Simple status list
        for validation in validation_results:
            path = validation.get("path", "unknown")
            if validation.get("exists"):
                console.print(f"✅ {path}")
            else:
                console.print(f"❌ {path}")

def display_agent_handoff_format(result: Dict[str, Any], operation: str):
    """Format results for agent-to-agent handoff"""
    
    if result.get("error"):
        return f"❌ File operation failed: {result['error']}"
    
    if operation == "read_file" and result.get("status") == "success":
        metadata = result.get("metadata", {})
        content = result.get("content", "")
        return f"✅ Read {metadata.get('file_name', 'file')} ({metadata.get('file_size_kb', 0)} KB)\n\n{content}"
    
    elif operation == "list_directory" and result.get("status") == "success":
        summary = result.get("summary", {})
        items = result.get("items", [])
        
        output = f"✅ Listed {summary.get('total_items', 0)} items in {result.get('directory', 'directory')}\n\n"
        
        for item in items:
            if "item_count" in item:  # Directory
                output += f"📁 {item.get('name', 'unknown')}/ ({item.get('item_count', 0)} items)\n"
            else:  # File
                output += f"📄 {item.get('name', 'unknown')} ({item.get('size_kb', 0)} KB)\n"
        
        return output
    
    elif operation == "search_files" and result.get("status") == "success":
        summary = result.get("summary", {})
        results_data = result.get("results", {})
        
        output = f"✅ Found {summary.get('total_found', 0)} matches for '{result.get('pattern', 'pattern')}'\n\n"
        
        for file_item in results_data.get("files", []):
            output += f"📄 {file_item.get('relative_path', 'unknown')} ({file_item.get('size_kb', 0)} KB)\n"
        
        for directory in results_data.get("directories", []):
            output += f"📁 {directory.get('relative_path', 'unknown')}/\n"
        
        return output
    
    else:
        return f"✅ File operation '{operation}' completed successfully"