#!/usr/bin/env python3
"""
MCP Connector Button Snippet Generator
Creates executable button snippets for MCP server integration
"""

from typing import Dict, Any

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Single entry point for MCP Connector button snippet generation
    Universal model compatibility via code generation
    """
    operation = params.get("operation", "list_servers")
    
    if operation == "list_servers":
        return _create_list_servers_snippet(params, model)
    elif operation == "execute_tool":
        return _create_execute_tool_snippet(params, model)
    elif operation == "register_server":
        return _create_register_server_snippet(params, model)
    elif operation == "get_server_status":
        return _create_server_status_snippet(params, model)
    else:
        return _create_default_snippet(params, model)


def _create_list_servers_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for listing available MCP servers"""
    workflow_id = params.get("workflow_id", "mcp-exploration")
    
    return f'''
# MCP Connector - List Available Servers
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_connector.mcp_connector import MCPConnector
from orchestrator.memory_mcp import MemoryMCPManager
import json

def main():
    # Initialize MCP Connector
    connector = MCPConnector()
    memory_mcp = MemoryMCPManager()
    connector.set_memory_manager(memory_mcp)
    
    # Initialize default servers
    print("🔌 Initializing MCP servers...")
    results = connector.initialize_default_servers()
    
    # Get available tools across all servers
    available_tools = connector.get_available_tools()
    
    # Get server status
    server_status = connector.get_server_status()
    
    print("\\n📊 MCP Server Status:")
    for server_name, status in server_status.items():
        status_icon = "🟢" if status["status"] == "online" else "🔴"
        print(f"  {status_icon} {{server_name}}: {{status['status']}} ({{status['tools_count']}} tools)")
    
    print("\\n🛠️ Available Tools:")
    for tool_name, tool_info in available_tools.items():
        available_icon = "✅" if tool_info["available"] else "❌"
        print(f"  {available_icon} {{tool_name}}: {{tool_info['description']}}")
    
    # Log to Memory MCP for workflow tracking
    memory_mcp.update_workflow_state(
        "{workflow_id}",
        f"MCP servers initialized: {{len(server_status)}} servers, {{len(available_tools)}} tools"
    )
    
    return {{
        "servers": server_status,
        "tools": available_tools,
        "initialization_results": results
    }}

if __name__ == "__main__":
    result = main()
    print(f"\\n✅ MCP Connector ready with {{len(result['servers'])}} servers")
'''


def _create_execute_tool_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for executing MCP tool"""
    server_name = params.get("server_name", "filesystem")
    tool_name = params.get("tool_name", "read_file")
    tool_params = params.get("tool_params", {})
    workflow_id = params.get("workflow_id", "mcp-execution")
    
    params_json = json.dumps(tool_params, indent=2) if tool_params else "{}"
    
    return f'''
# MCP Connector - Execute Tool
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_connector.mcp_connector import MCPConnector
from orchestrator.memory_mcp import MemoryMCPManager
import json

def main():
    # Initialize MCP Connector
    connector = MCPConnector()
    memory_mcp = MemoryMCPManager()
    connector.set_memory_manager(memory_mcp)
    
    # Initialize servers first
    connector.initialize_default_servers()
    
    # Execute the specified tool
    tool_params = {params_json}
    
    print(f"🛠️ Executing {{'{tool_name}'}} on {{'{server_name}'}} server...")
    
    result = connector.execute_tool(
        server_name="{server_name}",
        tool_name="{tool_name}",
        params=tool_params,
        workflow_id="{workflow_id}"
    )
    
    if result["success"]:
        print(f"✅ Tool execution successful!")
        print(f"📊 Result: {{json.dumps(result['result'], indent=2)}}")
    else:
        print(f"❌ Tool execution failed: {{result['error']}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🔄 Tool execution {{\"completed\" if result[\"success\"] else \"failed\"}}")
'''


def _create_register_server_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for registering new MCP server"""
    server_config = params.get("server_config", {
        "name": "new_server",
        "command": ["python", "-m", "server"],
        "description": "New MCP server"
    })
    workflow_id = params.get("workflow_id", "mcp-registration")
    
    config_json = json.dumps(server_config, indent=2)
    
    return f'''
# MCP Connector - Register New Server
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_connector.mcp_connector import MCPConnector
from orchestrator.memory_mcp import MemoryMCPManager
import json

def main():
    # Initialize MCP Connector
    connector = MCPConnector()
    memory_mcp = MemoryMCPManager()
    connector.set_memory_manager(memory_mcp)
    
    # Server configuration
    server_config = {config_json}
    
    print(f"📡 Registering MCP server: {{server_config['name']}}...")
    
    result = connector.register_server(server_config)
    
    if result["status"] == "registered":
        print(f"✅ Server registered successfully!")
        print(f"🛠️ Available tools: {{result['tools']}}")
    else:
        print(f"❌ Server registration failed: {{result.get('error', 'Unknown error')}}")
    
    # Log to Memory MCP
    memory_mcp.update_workflow_state(
        "{workflow_id}",
        f"MCP server registration: {{server_config['name']}} -> {{result['status']}}"
    )
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🔌 Server registration {{result['status']}}")
'''


def _create_server_status_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for checking server status"""
    workflow_id = params.get("workflow_id", "mcp-status")
    
    return f'''
# MCP Connector - Server Status Check
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_connector.mcp_connector import MCPConnector
from orchestrator.memory_mcp import MemoryMCPManager

def main():
    # Initialize MCP Connector
    connector = MCPConnector()
    memory_mcp = MemoryMCPManager()
    connector.set_memory_manager(memory_mcp)
    
    # Initialize servers
    connector.initialize_default_servers()
    
    # Get server status
    print("🔍 Checking MCP server status...")
    status = connector.get_server_status()
    
    print("\\n📊 Server Status Report:")
    for server_name, server_status in status.items():
        status_icon = "🟢" if server_status["status"] == "online" else "🔴"
        print(f"  {status_icon} {{server_name}}:")
        print(f"    Status: {{server_status['status']}}")
        print(f"    Tools: {{server_status.get('tools_count', 0)}}")
        print(f"    Last Check: {{server_status['last_check']}}")
        if "error" in server_status:
            print(f"    Error: {{server_status['error']}}")
    
    # Log to Memory MCP
    online_count = sum(1 for s in status.values() if s["status"] == "online")
    memory_mcp.update_workflow_state(
        "{workflow_id}",
        f"MCP status check: {{online_count}}/{{len(status)}} servers online"
    )
    
    return status

if __name__ == "__main__":
    result = main()
    online_servers = [name for name, info in result.items() if info["status"] == "online"]
    print(f"\\n✅ {{len(online_servers)}} servers online: {{', '.join(online_servers)}}")
'''


def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate default MCP Connector snippet"""
    workflow_id = params.get("workflow_id", "mcp-default")
    
    return f'''
# MCP Connector - General Integration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_connector.mcp_connector import MCPConnector
from orchestrator.memory_mcp import MemoryMCPManager

def main():
    # Initialize MCP Connector
    connector = MCPConnector()
    memory_mcp = MemoryMCPManager()
    connector.set_memory_manager(memory_mcp)
    
    print("🔌 MCP Connector initialized")
    print("📋 Available operations:")
    print("  - list_servers: Show all MCP servers and tools")
    print("  - execute_tool: Run specific MCP tool")
    print("  - register_server: Add new MCP server")
    print("  - get_server_status: Check server health")
    
    # Basic initialization
    results = connector.initialize_default_servers()
    
    # Log initialization
    memory_mcp.update_workflow_state(
        "{workflow_id}",
        "MCP Connector initialized with default servers"
    )
    
    return {{
        "connector": "ready",
        "initialization": results
    }}

if __name__ == "__main__":
    result = main()
    print(f"\\n🚀 MCP Connector ready for integration")
'''
