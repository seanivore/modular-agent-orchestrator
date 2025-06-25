#!/usr/bin/env python3
"""
MCP Connector UI Components
Rich console display for MCP server integration
"""

from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def display_server_status(servers: Dict[str, Dict[str, Any]], verbose: bool = False) -> None:
    """Display MCP server status in formatted table"""
    
    table = Table(
        title="🔌 MCP Server Status",
        box=box.ROUNDED,
        header_style="bold cyan"
    )
    
    table.add_column("Server", style="white", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Tools", justify="right", style="cyan")
    table.add_column("Last Check", style="dim")
    
    if verbose:
        table.add_column("Details", style="yellow")
    
    for server_name, status in servers.items():
        # Status icon and color
        if status["status"] == "online":
            status_text = Text("🟢 Online", style="green")
        elif status["status"] == "offline":
            status_text = Text("🔴 Offline", style="red")
        else:
            status_text = Text("⚠️ Error", style="yellow")
        
        # Tools count
        tools_count = str(status.get("tools_count", 0))
        
        # Format timestamp
        last_check = status["last_check"].split("T")[1][:8] if "T" in status["last_check"] else status["last_check"]
        
        row = [server_name, status_text, tools_count, last_check]
        
        if verbose and "error" in status:
            row.append(status["error"][:50] + "..." if len(status["error"]) > 50 else status["error"])
        elif verbose:
            row.append("Running normally")
        
        table.add_row(*row)
    
    console.print(table)
    console.print()


def display_available_tools(tools: Dict[str, Dict[str, Any]], verbose: bool = False) -> None:
    """Display available MCP tools in formatted table"""
    
    table = Table(
        title="🛠️ Available MCP Tools",
        box=box.ROUNDED,
        header_style="bold green"
    )
    
    table.add_column("Tool", style="white", no_wrap=True)
    table.add_column("Server", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Description", style="dim")
    
    if verbose:
        table.add_column("Parameters", style="yellow")
    
    for tool_name, tool_info in tools.items():
        # Status icon
        status_icon = "✅" if tool_info["available"] else "❌"
        status_text = Text(f"{status_icon} {'Ready' if tool_info['available'] else 'Unavailable'}")
        
        # Description truncation
        description = tool_info["description"]
        if len(description) > 50 and not verbose:
            description = description[:47] + "..."
        
        row = [tool_name, tool_info["server"], status_text, description]
        
        if verbose:
            params = tool_info.get("parameters", {})
            param_text = ", ".join(params.keys()) if params else "None"
            row.append(param_text)
        
        table.add_row(*row)
    
    console.print(table)
    console.print()


def display_execution_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """Display MCP tool execution result"""
    
    if result["success"]:
        panel_style = "green"
        title = "✅ MCP Tool Execution Successful"
    else:
        panel_style = "red"
        title = "❌ MCP Tool Execution Failed"
    
    content = []
    content.append(f"🖥️ Server: {result['server']}")
    content.append(f"🛠️ Tool: {result['tool']}")
    content.append(f"⏰ Time: {result['timestamp'].split('T')[1][:8] if 'T' in result['timestamp'] else result['timestamp']}")
    
    if result["success"]:
        if verbose and "result" in result:
            content.append("📊 Result:")
            if isinstance(result["result"], dict):
                for key, value in result["result"].items():
                    content.append(f"  • {key}: {value}")
            else:
                content.append(f"  {result['result']}")
        else:
            content.append("📊 Execution completed successfully")
    else:
        content.append(f"⚠️ Error: {result.get('error', 'Unknown error')}")
    
    panel = Panel(
        "\n".join(content),
        title=title,
        border_style=panel_style,
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_registration_result(result: Dict[str, Any]) -> None:
    """Display MCP server registration result"""
    
    if result["status"] == "registered":
        panel_style = "green"
        title = "✅ MCP Server Registration Successful"
        content = [
            f"🖥️ Server: {result['server_name']}",
            f"🛠️ Tools Available: {result['tools_count']}",
            f"📋 Tools: {', '.join(result.get('tools', []))}"
        ]
    else:
        panel_style = "red"
        title = "❌ MCP Server Registration Failed"
        content = [
            f"🖥️ Server: {result['server_name']}",
            f"⚠️ Error: {result.get('error', 'Unknown error')}"
        ]
    
    panel = Panel(
        "\n".join(content),
        title=title,
        border_style=panel_style,
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_error(operation: str, error: str) -> None:
    """Display error message with consistent formatting"""
    
    panel = Panel(
        f"⚠️ Operation: {operation}\n🚨 Error: {error}",
        title="❌ MCP Connector Error",
        border_style="red",
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_mcp_summary(servers: Dict[str, Any], tools: Dict[str, Any]) -> None:
    """Display comprehensive MCP integration summary"""
    
    # Count stats
    total_servers = len(servers)
    online_servers = sum(1 for s in servers.values() if s.get("status") == "online")
    total_tools = len(tools)
    available_tools = sum(1 for t in tools.values() if t.get("available", False))
    
    # Create summary text
    summary_text = [
        f"🔌 Servers: {online_servers}/{total_servers} online",
        f"🛠️ Tools: {available_tools}/{total_tools} available",
        f"📊 Integration: {'✅ Ready' if online_servers > 0 else '❌ No servers online'}"
    ]
    
    panel = Panel(
        "\n".join(summary_text),
        title="🚀 MCP Integration Summary",
        border_style="cyan",
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def display_help() -> None:
    """Display MCP Connector help information"""
    
    help_content = [
        "🔌 MCP Connector Operations:",
        "",
        "📋 list_servers - Show all registered MCP servers and their tools",
        "🛠️ execute_tool - Run a specific tool on an MCP server", 
        "📡 register_server - Add a new MCP server to the system",
        "🔍 get_server_status - Check health and status of all servers",
        "",
        "💡 MCP (Model Context Protocol) allows integration with external",
        "   tools and services through standardized server connections.",
        "",
        "🔧 Common MCP servers: aider, filesystem, git, database, etc."
    ]
    
    panel = Panel(
        "\n".join(help_content),
        title="🔌 MCP Connector Help",
        border_style="blue",
        box=box.ROUNDED
    )
    
    console.print(panel)
    console.print()


def format_operation_params(operation: str, params: Dict[str, Any]) -> str:
    """Format operation parameters for display"""
    
    if operation == "execute_tool":
        return f"Server: {params.get('server_name', 'N/A')}, Tool: {params.get('tool_name', 'N/A')}"
    elif operation == "register_server":
        config = params.get('server_config', {})
        return f"Server: {config.get('name', 'N/A')}, Command: {' '.join(config.get('command', []))}"
    elif operation == "list_servers":
        return "Listing all registered servers and tools"
    elif operation == "get_server_status":
        return "Checking health of all registered servers"
    else:
        return f"Operation: {operation}"
