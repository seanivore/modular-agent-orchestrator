#!/usr/bin/env python3
"""
MCP Connector Button Snippet Generator - Fixed Version
Creates executable button snippets for MCP server integration
"""

from typing import Dict, Any
import json
from tools.mcp_connector.mcp_connector import (
    list_mcp_servers,
    execute_mcp_tool,
    register_mcp_server,
    get_mcp_server_status,
    estimate_cost
)

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
    """Generate snippet for listing available MCP servers using MAO logic"""
    workflow_id = params.get("workflow_id", "mcp-exploration")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"servers": ["aider", "filesystem"], "tool_executions": 1})
    
    snippet = f'''
# MCP Connector - List Available Servers
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.mcp_connector.mcp_connector import list_mcp_servers
from tools.mcp_connector.ui_mcp_connector import display_server_status, display_available_tools, display_mcp_summary

# Execute server listing using MAO logic
result = list_mcp_servers(workflow_id="{workflow_id}")

if result.get("status") == "success":
    print("🔌 MCP Server Discovery Complete")
    
    servers = result.get("servers", {{}})
    tools = result.get("tools", {{}})
    
    # Display results using MAO UI components
    display_server_status(servers, verbose=True)
    display_available_tools(tools, verbose=True)
    display_mcp_summary(servers, tools)
    
    print(f"📊 Summary: {{len(servers)}} servers, {{len(tools)}} tools")
else:
    print(f"❌ Error: {{result.get('error', 'Unknown error')}}")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_execute_tool_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for executing MCP tool using MAO logic"""
    server_name = params.get("server_name", "filesystem")
    tool_name = params.get("tool_name", "read_file")
    tool_params = params.get("tool_params", {})
    workflow_id = params.get("workflow_id", "mcp-execution")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"tool_executions": 1})
    
    # Escape tool_params for safe inclusion in code
    params_json = json.dumps(tool_params) if tool_params else "{}"
    
    snippet = f'''
# MCP Connector - Execute Tool
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.mcp_connector.mcp_connector import execute_mcp_tool
from tools.mcp_connector.ui_mcp_connector import display_execution_result

# Tool parameters
tool_params = {params_json}

print(f"🛠️ Executing '{tool_name}' on '{server_name}' server...")

# Execute tool using MAO logic
result = execute_mcp_tool(
    server_name="{server_name}",
    tool_name="{tool_name}",
    tool_params=tool_params,
    workflow_id="{workflow_id}"
)

# Display results using MAO UI
display_execution_result(result, verbose=True)

if result.get("success"):
    print("✅ Tool execution completed successfully")
else:
    print(f"❌ Tool execution failed: {{result.get('error', 'Unknown error')}}")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_register_server_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for registering new MCP server using MAO logic"""
    server_config = params.get("server_config", {
        "name": "new_server",
        "command": ["python", "-m", "server"],
        "description": "New MCP server"
    })
    workflow_id = params.get("workflow_id", "mcp-registration")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"servers": [server_config.get("name", "new_server")]})
    
    snippet = f'''
# MCP Connector - Register New Server
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.mcp_connector.mcp_connector import register_mcp_server
from tools.mcp_connector.ui_mcp_connector import display_registration_result

# Server configuration
server_config = {json.dumps(server_config, indent=2)}

print(f"📡 Registering MCP server: {{server_config['name']}}...")

# Register server using MAO logic
result = register_mcp_server(
    server_config=server_config,
    workflow_id="{workflow_id}"
)

# Display results using MAO UI
display_registration_result(result)

if result.get("status") == "registered":
    print(f"✅ Server '{{server_config['name']}}' registered successfully")
    print(f"🛠️ Available tools: {{result.get('tools_count', 0)}}")
else:
    print(f"❌ Registration failed: {{result.get('error', 'Unknown error')}}")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_server_status_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for checking server status using MAO logic"""
    workflow_id = params.get("workflow_id", "mcp-status")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"servers": ["aider", "filesystem"]})
    
    snippet = f'''
# MCP Connector - Server Status Check
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.mcp_connector.mcp_connector import get_mcp_server_status
from tools.mcp_connector.ui_mcp_connector import display_server_status

print("🔍 Checking MCP server status...")

# Get server status using MAO logic
result = get_mcp_server_status(workflow_id="{workflow_id}")

if result.get("status") == "success":
    servers = result.get("servers", {{}})
    
    # Display results using MAO UI
    display_server_status(servers, verbose=True)
    
    online_count = sum(1 for s in servers.values() if s.get("status") == "online")
    total_count = len(servers)
    
    print(f"📊 Status Summary: {{online_count}}/{{total_count}} servers online")
else:
    print(f"❌ Error: {{result.get('error', 'Unknown error')}}")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate default MCP Connector snippet"""
    operation = params.get("operation", "unknown")
    workflow_id = params.get("workflow_id", "mcp-default")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"servers": []})
    
    snippet = f'''
# MCP Connector - General Integration
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.mcp_connector.mcp_connector import estimate_cost
from tools.mcp_connector.ui_mcp_connector import display_help

print("🔌 MCP Connector - Unknown Operation: {operation}")

# Display help information
display_help()

# Show available operations
available_operations = [
    "list_servers",
    "execute_tool", 
    "register_server",
    "get_server_status"
]

print("\\n📋 Available Operations:")
for op in available_operations:
    print(f"  • {{op}}")

print(f"\\n💰 Estimated cost: ${cost_estimate:.4f}")

result = {{
    "error": f"Unknown operation: {operation}",
    "available_operations": available_operations,
    "cost": cost_estimate
}}

# Return result
result
'''
    
    return snippet.strip()
