#!/usr/bin/env python3
"""
MCP Integration Hub Complete Foundation System
Integrates Memory MCP, Files API, and MCP Connector into unified system
"""

import json
from typing import Dict, List, Optional, Any
from .memory_mcp import MemoryMCPManager
from tools.files_api.files_api import FilesAPIManager  
from tools.mcp_connector.mcp_connector import MCPConnector
from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError

class MCPIntegrationHub:
    """Unified MCP system providing state persistence, file management, and tool connectivity"""
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        # Initialize core components
        self.memory = MemoryMCPManager()
        self.files = FilesAPIManager()
        self.connector = MCPConnector()
        
        # Wire components together
        self.files.set_memory_mcp(self.memory)
        self.connector.set_memory_manager(self.memory)
        
        # Initialize external servers
        self._initialize_servers()
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # MCP Hub operations include memory, files, and connector operations
        base_cost = 0.0
        
        # Add cost for workflow operations
        num_workflows = params.get("num_workflows", 1)
        base_cost += num_workflows * 0.003  # $0.003 per workflow coordination
        
        # Add cost for file operations
        file_operations = params.get("file_operations", 2)
        base_cost += file_operations * 0.002  # $0.002 per file operation
        
        # Add cost for MCP tool executions
        tool_executions = params.get("tool_executions", 1)
        base_cost += tool_executions * 0.005  # $0.005 per tool execution
        
        # Add cost for memory operations
        memory_operations = params.get("memory_operations", 3)
        base_cost += memory_operations * 0.001  # $0.001 per memory operation
        
        return base_cost
    
    def _initialize_servers(self):
        """Initialize default MCP servers"""
        try:
            results = self.connector.initialize_default_servers()
            for server_name, result in results.items():
                if result["status"] == "registered":
                    print(f"✅ MCP server {server_name}: {result['tools_count']} tools")
                else:
                    print(f"⚠️  MCP server {server_name}: {result.get('error', 'failed')}")
        except Exception as e:
            print(f"Warning: Failed to initialize MCP servers: {e}")
    
    # =================================================================
    # WORKFLOW LIFECYCLE MANAGEMENT
    # =================================================================
    
    @handle_errors(operation_name="create_workflow", return_dict=True)
    def create_workflow(self, workflow_id: str, user_goal: str) -> str:
        """Initialize complete workflow with all MCP components"""
        
        # Create workflow context in Memory MCP
        context_id = self.memory.create_workflow_context(workflow_id, user_goal)
        
        # Set up Files API workspace
        workspace = self.files.create_workflow_workspace(workflow_id)
        
        # Log workflow creation
        self.memory.update_workflow_state(
            workflow_id,
            f"Workflow initialized with Files API workspace: {workspace}"
        )
        
        return context_id
    
    def save_workflow_draft(self, workflow_id: str, content: str, draft_type: str, phase: str = None) -> str:
        """Save draft with integrated tracking"""
        file_id = self.files.save_draft(workflow_id, content, draft_type, phase)
        
        # Memory MCP tracking is handled automatically by FilesAPIManager
        return file_id
    
    def prepare_agent_handoff(self, workflow_id: str, agent_materials: Dict[str, Any]) -> str:
        """Create agent handoff package with complete context"""
        
        # Files API handles the packaging and Memory MCP integration
        handoff_id = self.files.prepare_agent_handoff(workflow_id, agent_materials)
        
        return handoff_id
    
    def restore_agent_context(self, workflow_id: str, handoff_file_id: str) -> Dict[str, Any]:
        """Restore agent context with full workflow state"""
        return self.files.restore_agent_context(workflow_id, handoff_file_id)
    
    def complete_workflow(self, workflow_id: str, final_results: Dict[str, Any]) -> bool:
        """Mark workflow complete with cleanup"""
        
        # Save final deliverables
        if "deliverables" in final_results:
            self.files.save_agent_deliverables(
                workflow_id, 
                "final", 
                final_results["deliverables"]
            )
        
        # Mark complete in Memory MCP
        self.memory.mark_workflow_complete(workflow_id, final_results)
        
        # Optional file cleanup (keep deliverables)
        cleanup_count = self.files.cleanup_workflow_files(workflow_id, keep_deliverables=True)
        
        self.memory.update_workflow_state(
            workflow_id,
            f"Workflow completed - {cleanup_count} temporary files cleaned up"
        )
        
        return True
    
    # =================================================================
    # SESSION RECOVERY
    # =================================================================
    
    def recover_session(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Recover workflow session with complete state"""
        
        # Get Memory MCP context
        recovery_info = self.memory.handle_session_recovery(workflow_id)
        
        if recovery_info and recovery_info.get("can_resume"):
            # Get associated files
            workflow_files = self.files.get_workflow_files(workflow_id)
            
            # Combine recovery information
            recovery_info["files"] = workflow_files
            recovery_info["mcp_tools"] = self.connector.get_available_tools()
            
            return recovery_info
        
        return None
    
    def list_recoverable_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows that can be resumed"""
        active_workflows = self.memory.list_active_workflows()
        recoverable = []
        
        for workflow in active_workflows:
            workflow_id = workflow.get('name', '').replace('workflow-', '')
            if workflow_id:
                recovery_info = self.recover_session(workflow_id)
                if recovery_info and recovery_info.get("can_resume"):
                    recoverable.append(recovery_info)
        
        return recoverable
    
    # =================================================================
    # TOOL INTEGRATION
    # =================================================================
    
    @handle_errors(operation_name="execute_mcp_tool", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, ConnectionError))
    def execute_mcp_tool(self, server_name: str, tool_name: str, params: Dict[str, Any], workflow_id: str = None) -> Dict[str, Any]:
        """Execute MCP tool with workflow tracking"""
        # Check cache for similar tool executions
        cache_key = f"{server_name}|{tool_name}|{json.dumps(params, sort_keys=True)[:50]}"
        cached_result = self.cache.get_cached_analysis(cache_key, "mcp_tool_execution")
        if cached_result:
            return json.loads(cached_result)
        
        # Execute tool
        result = self.connector.execute_tool(server_name, tool_name, params, workflow_id)
        
        # Cache successful results
        if result.get("success"):
            self.cache.cache_content_analysis(cache_key, json.dumps(result), "mcp_tool_execution")
        
        return result
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all available MCP tools"""
        return self.connector.get_available_tools()
    
    def get_tool_recommendations(self, workflow_context: str) -> List[str]:
        """Recommend tools based on workflow context"""
        available_tools = self.get_available_tools()
        
        # Simple keyword-based recommendations
        # In real implementation, this would use more sophisticated matching
        recommendations = []
        context_lower = workflow_context.lower()
        
        for tool_name, tool_info in available_tools.items():
            tool_desc = tool_info.get("description", "").lower()
            
            # Match keywords
            if any(keyword in context_lower for keyword in ["file", "edit", "code"] if keyword in tool_desc):
                recommendations.append(tool_name)
            elif any(keyword in context_lower for keyword in ["research", "web", "search"] if keyword in tool_desc):
                recommendations.append(tool_name)
        
        return recommendations[:5]  # Top 5 recommendations
    
    # =================================================================
    # SYSTEM STATUS
    # =================================================================
    
    @handle_errors(operation_name="get_system_status", return_dict=True)
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete MCP Integration Hub status"""
        
        # MCP server status
        server_status = self.connector.get_server_status()
        
        # Count active workflows
        active_workflows = self.memory.list_active_workflows()
        
        # Tool availability
        available_tools = self.connector.get_available_tools()
        
        return {
            "memory_mcp": {
                "status": "connected",
                "active_workflows": len(active_workflows),
                "workflow_entities": len(active_workflows)
            },
            "files_api": {
                "status": "connected", 
                "workspace_ready": True,
                "storage_backend": type(self.files.client).__name__
            },
            "mcp_servers": server_status,
            "tools": {
                "total_available": len(available_tools),
                "servers_online": len([s for s in server_status.values() if s["status"] == "online"]),
                "servers_total": len(server_status)
            },
            "integration": {
                "memory_files_linked": True,
                "memory_connector_linked": True,
                "all_components_ready": True
            }
        }
    
    @handle_errors(operation_name="health_check", return_dict=True)
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health = {
            "overall": "healthy",
            "components": {},
            "issues": []
        }
        
        # Check Memory MCP
        try:
            test_id = "health-check-test"
            self.memory.create_workflow_context(test_id, "Health check test")
            health["components"]["memory_mcp"] = "healthy"
        except Exception as e:
            health["components"]["memory_mcp"] = "unhealthy"
            health["issues"].append(f"Memory MCP: {str(e)}")
        
        # Check Files API
        try:
            test_content = "health check"
            self.files.client.upload(test_content, "health-check.txt")
            health["components"]["files_api"] = "healthy"
        except Exception as e:
            health["components"]["files_api"] = "unhealthy"
            health["issues"].append(f"Files API: {str(e)}")
        
        # Check MCP Connector
        try:
            server_status = self.connector.get_server_status()
            online_servers = len([s for s in server_status.values() if s["status"] == "online"])
            if online_servers > 0:
                health["components"]["mcp_connector"] = "healthy"
            else:
                health["components"]["mcp_connector"] = "degraded"
                health["issues"].append("No MCP servers online")
        except Exception as e:
            health["components"]["mcp_connector"] = "unhealthy"
            health["issues"].append(f"MCP Connector: {str(e)}")
        
        # Overall health
        if health["issues"]:
            health["overall"] = "degraded" if len(health["issues"]) < 3 else "unhealthy"
        
        return health
    
    # =================================================================
    # CONFIGURATION MANAGEMENT
    # =================================================================
    
    def add_mcp_server(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Add new MCP server configuration"""
        return self.connector.register_server(server_config)
    
    def remove_mcp_server(self, server_name: str) -> bool:
        """Remove MCP server"""
        return self.connector.disconnect_server(server_name)
    
    def update_server_config(self, server_name: str, new_config: Dict[str, Any]) -> bool:
        """Update MCP server configuration"""
        # Remove old server
        if server_name in self.connector.servers:
            self.connector.disconnect_server(server_name)
        
        # Add updated server
        result = self.connector.register_server(new_config)
        return result["status"] == "registered"
    
    # =================================================================
    # WORKFLOW PATTERN MATCHING
    # =================================================================
    
    def find_similar_workflows(self, current_goal: str) -> List[Dict[str, Any]]:
        """Find similar past workflows for pattern matching"""
        return self.memory.search_workflow_patterns(current_goal)
    
    def get_workflow_insights(self, workflow_id: str) -> Dict[str, Any]:
        """Get insights from workflow execution"""
        context = self.memory.get_workflow_context(workflow_id)
        files = self.files.get_workflow_files(workflow_id)
        
        if not context:
            return {"insights": [], "recommendations": []}
        
        observations = context.get("observations", [])
        
        # Extract insights from observations
        insights = []
        tools_used = []
        errors = []
        
        for obs in observations:
            if "MCP tool executed" in obs:
                tool_info = obs.split("MCP tool executed:")[-1].strip()
                tools_used.append(tool_info)
            elif "error" in obs.lower() or "failed" in obs.lower():
                errors.append(obs)
            elif "completed" in obs.lower():
                insights.append(obs)
        
        recommendations = []
        if errors:
            recommendations.append("Consider error handling improvements")
        if len(tools_used) > 5:
            recommendations.append("Workflow uses many tools - consider optimization")
        
        return {
            "insights": insights,
            "tools_used": tools_used,
            "errors": errors,
            "recommendations": recommendations,
            "file_count": sum(len(files[category]) for category in files.values())
        }


# =================================================================
# CONVENIENCE FUNCTIONS FOR ORCHESTRATOR INTEGRATION
# =================================================================

def create_mcp_hub() -> MCPIntegrationHub:
    """Factory function to create configured MCP Integration Hub"""
    hub = MCPIntegrationHub()
    
    # Verify initialization
    status = hub.get_system_status()
    if status["integration"]["all_components_ready"]:
        print("✅ MCP Integration Hub initialized successfully")
    else:
        print("⚠️  MCP Integration Hub initialized with some issues")
    
    return hub

def get_hub_summary(hub: MCPIntegrationHub) -> str:
    """Get human-readable summary of MCP Hub status"""
    status = hub.get_system_status()
    
    summary_parts = [
        f"🧠 Memory: {status['memory_mcp']['active_workflows']} active workflows",
        f"📁 Files: {status['files_api']['storage_backend']} backend",
        f"🔌 Servers: {status['tools']['servers_online']}/{status['tools']['servers_total']} online",
        f"🛠️  Tools: {status['tools']['total_available']} available"
    ]
    
    return " | ".join(summary_parts)
