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

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

console = Console()
cache = CacheManager()


@handle_errors(operation_name="display_mcp_connector_result", return_dict=False)
def display_mcp_connector_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display MCP Connector operation results with beautiful formatting
    
    Args:
        result: Result from MCP operations
        verbose: Whether to show detailed information
    """
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    operation = result.get("operation", "unknown")
    
    if operation == "list_servers":
        servers = result.get("servers", {})
        tools = result.get("tools", {})
        display_server_status(servers, verbose)
        if tools:
            display_available_tools(tools, verbose)
    elif operation == "execute_tool":
        display_execution_result(result, verbose)
    elif operation == "register_server":
        display_registration_result(result)
    elif operation == "get_server_status":
        servers = result.get("servers", {})
        tools = result.get("tools", {})
        display_mcp_summary(servers, tools)
    else:
        # Generic display for other operations
        console.print("🔌 MCP Connector Operation Completed", style="bold green")
        if verbose:
            for key, value in result.items():
                if key not in ["error", "operation"]:
                    console.print(f"  {key}: {value}")


@handle_errors(operation_name="display_error", return_dict=False)
def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="MCP Connector Error",
        border_style="red"
    )
    console.print(panel)

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
    
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
        
    if result.get("success", False):
        panel_style = "green"
        title = "✅ MCP Tool Execution Successful"
    else:
        panel_style = "red"
        title = "❌ MCP Tool Execution Failed"
    
    content = []
    content.append(f"🖥️ Server: {result.get('server', 'Unknown')}")
    content.append(f"🛠️ Tool: {result.get('tool', 'Unknown')}")
    content.append(f"⏰ Time: {result.get('timestamp', 'Unknown').split('T')[1][:8] if 'T' in result.get('timestamp', '') else result.get('timestamp', 'Unknown')}")
    
    if result.get("success", False):
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
    
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
        
    if result.get("status") == "registered":
        panel_style = "green"
        title = "✅ MCP Server Registration Successful"
        content = [
            f"🖥️ Server: {result.get('server_name', 'Unknown')}",
            f"🛠️ Tools Available: {result.get('tools_count', 0)}",
            f"📋 Tools: {', '.join(result.get('tools', []))}"
        ]
    else:
        panel_style = "red"
        title = "❌ MCP Server Registration Failed"
        content = [
            f"🖥️ Server: {result.get('server_name', 'Unknown')}",
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
