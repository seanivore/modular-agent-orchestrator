#!/usr/bin/env python3
"""
MCP API Connector - External MCP Server Integration
Provides connectivity to external MCP servers and tool discovery
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

class MCPConnector:
    """Anthropic MCP API Connector for external tool integration"""
    
    def __init__(self):
        self.servers = {}
        self.memory_manager = None
        self.registered_tools = {}
        self.config_dir = Path.cwd() / "configs" / "connections"
        
    def set_memory_manager(self, memory_manager):
        """Set Memory MCP manager for integration"""
        self.memory_manager = memory_manager
    
    @handle_errors(operation_name="mcp_connector_load_configs", return_dict=True)
    def load_server_configs(self) -> Dict[str, Dict]:
        """Load MCP server configurations from configs/connections/"""
        config_file = self.config_dir / "mcp_servers.json"
        
        # Check cache first
        cache_key = f"mcp_server_configs|{config_file.stat().st_mtime if config_file.exists() else 'new'}"
        cached_result = cache.get_cached_analysis(cache_key, "mcp_connector")
        if cached_result:
            return json.loads(cached_result)
        
        try:
            with open(config_file) as f:
                config_data = json.load(f)
        except FileNotFoundError:
            # Create default config if not exists
            config_data = {
                "servers": {
                    "aider": {
                        "name": "aider",
                        "command": ["python", "-m", "aider.mcp"],
                        "description": "Aider code editing MCP server",
                        "tools": ["edit_file", "create_file", "read_file"]
                    },
                    "filesystem": {
                        "name": "filesystem", 
                        "command": ["npx", "@modelcontextprotocol/server-filesystem"],
                        "description": "File system operations MCP server",
                        "tools": ["read_file", "write_file", "list_directory"]
                    }
                }
            }
            
            # Create config directory and file
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        
        # Cache the result
        cache.cache_content_analysis(cache_key, json.dumps(config_data), "mcp_connector")
        return config_data
    
    @handle_errors(operation_name="mcp_connector_register", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(ConnectionError, APIError))
    def register_server(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Register external MCP server"""
        server_name = server_config["name"]
        
        try:
            # Create server connection
            connection = MCPServerConnection(server_config)
            self.servers[server_name] = connection
            
            # Discover available tools
            tools = connection.list_tools()
            self.registered_tools[server_name] = tools
            
            # Log server registration in Memory MCP
            if self.memory_manager:
                self.memory_manager.create_entities([{
                    "name": f"mcp-server-{server_name}",
                    "entityType": "mcp-server",
                    "observations": [
                        f"Registered: {server_config['description']}",
                        f"Command: {' '.join(server_config['command'])}",
                        f"Available tools: {list(tools.keys())}",
                        f"Registration time: {datetime.now().isoformat()}"
                    ]
                }])
            
            return {
                "server_name": server_name,
                "status": "registered",
                "tools_count": len(tools),
                "tools": list(tools.keys())
            }
            
        except Exception as e:
            error_msg = f"Failed to register server {server_name}: {str(e)}"
            print(f"Warning: {error_msg}")
            
            if self.memory_manager:
                self.memory_manager.create_entities([{
                    "name": f"mcp-server-{server_name}-error",
                    "entityType": "mcp-error",
                    "observations": [error_msg]
                }])
            
            return {
                "server_name": server_name,
                "status": "failed",
                "error": str(e)
            }
    
    @handle_errors(operation_name="mcp_connector_execute", return_dict=True)
    def execute_tool(self, server_name: str, tool_name: str, params: Dict[str, Any], workflow_id: str = None) -> Dict[str, Any]:
        """Execute tool on external MCP server"""
        
        # Validate server and tool
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not registered")
            
        if tool_name not in self.registered_tools.get(server_name, {}):
            raise ValueError(f"Tool {tool_name} not available on {server_name}")
        
        try:
            # Execute tool
            result = self.servers[server_name].execute_tool(tool_name, params)
            
            # Log tool execution if part of workflow
            if workflow_id and self.memory_manager:
                self.memory_manager.update_workflow_state(
                    workflow_id,
                    f"MCP tool executed: {server_name}.{tool_name} -> Success"
                )
            
            return {
                "success": True,
                "server": server_name,
                "tool": tool_name,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_result = {
                "success": False,
                "server": server_name,
                "tool": tool_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            # Log error if part of workflow
            if workflow_id and self.memory_manager:
                self.memory_manager.update_workflow_state(
                    workflow_id,
                    f"MCP tool error: {server_name}.{tool_name} -> {str(e)}"
                )
            
            return error_result
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all available tools across all servers"""
        all_tools = {}
        
        for server_name, tools in self.registered_tools.items():
            for tool_name, tool_info in tools.items():
                qualified_name = f"{server_name}.{tool_name}"
                all_tools[qualified_name] = {
                    "server": server_name,
                    "tool": tool_name,
                    "description": tool_info.get("description", ""),
                    "parameters": tool_info.get("parameters", {}),
                    "available": server_name in self.servers
                }
        
        return all_tools
    
    def get_server_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered servers"""
        status = {}
        
        for server_name, connection in self.servers.items():
            try:
                # Test server connection
                is_alive = connection.ping()
                tools_count = len(self.registered_tools.get(server_name, {}))
                
                status[server_name] = {
                    "name": server_name,
                    "status": "online" if is_alive else "offline",
                    "tools_count": tools_count,
                    "last_check": datetime.now().isoformat()
                }
                
            except Exception as e:
                status[server_name] = {
                    "name": server_name,
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return status
    
    @handle_errors(operation_name="mcp_connector_initialize", return_dict=True)
    def initialize_default_servers(self) -> Dict[str, Any]:
        """Initialize servers from configuration"""
        server_configs = self.load_server_configs()
        results = {}
        
        for server_id, config in server_configs.get("servers", {}).items():
            result = self.register_server(config)
            results[server_id] = result
        
        return results
    
    def disconnect_server(self, server_name: str) -> bool:
        """Disconnect from MCP server"""
        if server_name in self.servers:
            try:
                self.servers[server_name].disconnect()
                del self.servers[server_name]
                
                # Remove tools
                if server_name in self.registered_tools:
                    del self.registered_tools[server_name]
                
                # Log disconnection
                if self.memory_manager:
                    self.memory_manager.update_workflow_state(
                        "system",
                        f"MCP server disconnected: {server_name}"
                    )
                
                return True
            except Exception as e:
                print(f"Warning: Error disconnecting from {server_name}: {e}")
                return False
        
        return False


# REQUIRED: Standard cost estimation function
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    # MCP operations are typically free but may have setup overhead
    server_count = len(params.get("servers", []))
    tool_executions = params.get("tool_executions", 1)
    
    # Small cost for server setup and tool execution overhead
    setup_cost = server_count * 0.001  # $0.001 per server
    execution_cost = tool_executions * 0.0005  # $0.0005 per tool execution
    
    return setup_cost + execution_cost

# REQUIRED: Standalone function wrappers for button file imports
@handle_errors(operation_name="list_mcp_servers", return_dict=True)
def list_mcp_servers(workflow_id: str = None) -> Dict[str, Any]:
    """List all registered MCP servers and available tools"""
    connector = MCPConnector()
    
    # Initialize default servers
    init_results = connector.initialize_default_servers()
    
    # Get server status and available tools
    server_status = connector.get_server_status()
    available_tools = connector.get_available_tools()
    
    result = {
        "status": "success",
        "operation": "list_servers",
        "servers": server_status,
        "tools": available_tools,
        "initialization_results": init_results,
        "timestamp": datetime.now().isoformat()
    }
    
    return result

@handle_errors(operation_name="execute_mcp_tool", return_dict=True)
def execute_mcp_tool(server_name: str, tool_name: str, tool_params: Dict[str, Any] = None, workflow_id: str = None) -> Dict[str, Any]:
    """Execute tool on external MCP server"""
    connector = MCPConnector()
    
    # Initialize servers
    connector.initialize_default_servers()
    
    # Execute the tool
    result = connector.execute_tool(
        server_name=server_name,
        tool_name=tool_name,
        params=tool_params or {},
        workflow_id=workflow_id
    )
    
    result["operation"] = "execute_tool"
    return result

@handle_errors(operation_name="register_mcp_server", return_dict=True)
def register_mcp_server(server_config: Dict[str, Any], workflow_id: str = None) -> Dict[str, Any]:
    """Register a new MCP server"""
    connector = MCPConnector()
    
    result = connector.register_server(server_config)
    result["operation"] = "register_server"
    result["timestamp"] = datetime.now().isoformat()
    
    return result

@handle_errors(operation_name="get_mcp_server_status", return_dict=True)
def get_mcp_server_status(workflow_id: str = None) -> Dict[str, Any]:
    """Check health and status of all MCP servers"""
    connector = MCPConnector()
    
    # Initialize servers
    connector.initialize_default_servers()
    
    # Get status
    status = connector.get_server_status()
    
    result = {
        "status": "success",
        "operation": "get_server_status", 
        "servers": status,
        "timestamp": datetime.now().isoformat()
    }
    
    return result


class MCPServerConnection:
    """Manages connection to individual MCP server"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config["name"]
        self.command = config["command"]
        self.description = config.get("description", "")
        self.process = None
        self._connected = False
        
        # For now, mock the connection
        # In real implementation, this would start the MCP server process
        self._mock_tools = self._create_mock_tools()
    
    def _create_mock_tools(self) -> Dict[str, Dict[str, Any]]:
        """Create mock tools based on server type"""
        if "aider" in self.name.lower():
            return {
                "edit_file": {
                    "description": "Edit a file using Aider",
                    "parameters": {
                        "file_path": {"type": "string", "required": True},
                        "instructions": {"type": "string", "required": True}
                    }
                },
                "create_file": {
                    "description": "Create a new file",
                    "parameters": {
                        "file_path": {"type": "string", "required": True},
                        "content": {"type": "string", "required": True}
                    }
                }
            }
        elif "filesystem" in self.name.lower():
            return {
                "read_file": {
                    "description": "Read file contents",
                    "parameters": {
                        "path": {"type": "string", "required": True}
                    }
                },
                "write_file": {
                    "description": "Write file contents",
                    "parameters": {
                        "path": {"type": "string", "required": True},
                        "content": {"type": "string", "required": True}
                    }
                },
                "list_directory": {
                    "description": "List directory contents",
                    "parameters": {
                        "path": {"type": "string", "required": True}
                    }
                }
            }
        else:
            return {
                "generic_tool": {
                    "description": f"Generic tool for {self.name}",
                    "parameters": {
                        "input": {"type": "string", "required": True}
                    }
                }
            }
    
    def connect(self) -> bool:
        """Connect to MCP server"""
        try:
            # In real implementation, this would start the server process
            # and establish MCP protocol connection
            print(f"Mock connecting to {self.name} server...")
            self._connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to {self.name}: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from MCP server"""
        try:
            if self.process:
                self.process.terminate()
            self._connected = False
            return True
        except Exception:
            return False
    
    def ping(self) -> bool:
        """Check if server is responsive"""
        return self._connected
    
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get available tools from server"""
        if not self._connected:
            self.connect()
        return self._mock_tools
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool on server"""
        if not self._connected:
            raise ConnectionError(f"Not connected to {self.name} server")
        
        if tool_name not in self._mock_tools:
            raise ValueError(f"Tool {tool_name} not available on {self.name}")
        
        # Mock tool execution
        if tool_name == "read_file":
            return {
                "content": f"Mock file content from {params.get('path', 'unknown')}",
                "size": 1024
            }
        elif tool_name == "write_file":
            return {
                "success": True,
                "bytes_written": len(params.get('content', ''))
            }
        elif tool_name == "list_directory":
            return {
                "files": ["file1.txt", "file2.py", "subdirectory/"],
                "count": 3
            }
        elif tool_name == "edit_file":
            return {
                "success": True,
                "changes_made": ["Added function", "Fixed imports"],
                "lines_modified": 5
            }
        else:
            return {
                "result": f"Mock result from {tool_name} on {self.name}",
                "success": True
            }
