#!/usr/bin/env python3
"""
Agent Callback Handler of the Workflow Progression System
Handles agent returns, execution results, and workflow progression
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError

class AgentCallbackHandler:
    """Manages agent returns and workflow progression"""
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        # Lazy load to avoid circular imports
        self._memory_mcp = None
        self._files_api = None
        self._code_execution = None
    
    @property
    def memory_mcp(self):
        """Lazy load Memory MCP manager"""
        if self._memory_mcp is None:
            from orchestrator.memory_mcp import MemoryMCPManager
            self._memory_mcp = MemoryMCPManager()
        return self._memory_mcp
    
    @property
    def files_api(self):
        """Lazy load Files API manager"""
        if self._files_api is None:
            from tools.files_api.files_api import FilesAPIManager
            self._files_api = FilesAPIManager()
        return self._files_api
    
    @property
    def code_execution(self):
        """Lazy load Code Execution tool"""
        if self._code_execution is None:
            from tools.code_execution.code_execution import CodeExecutionTool
            self._code_execution = CodeExecutionTool()
        return self._code_execution
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Agent callback operations are typically free (memory/file operations)
        # Cost comes from tool executions which are estimated separately
        base_cost = 0.0
        
        # Add small cost for memory operations
        memory_operations = params.get("memory_operations", 1)
        base_cost += memory_operations * 0.001  # $0.001 per memory operation
        
        # Add cost for file operations  
        file_operations = params.get("file_operations", 0)
        base_cost += file_operations * 0.002  # $0.002 per file operation
        
        return base_cost
    
    @handle_errors(operation_name="agent_callback", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, ConnectionError))
    def handle_agent_return(self, workflow_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent return with execution results"""
        
        execution_id = execution_data.get('execution_id', 'unknown')
        tool_name = execution_data.get('tool_name', 'unknown')
        
        # Check cache for similar workflow executions
        cache_key = f"{workflow_id}|{tool_name}|{execution_id}"
        cached_result = self.cache.get_cached_analysis(cache_key, "agent_callback")
        if cached_result:
            return json.loads(cached_result)
        
        # Retrieve workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Process execution results
        processed_results = self._process_execution_results(workflow_id, execution_data)
        
        # Determine next workflow phase
        next_phase_info = self._determine_next_phase(workflow_context, processed_results)
        
        # Update workflow state with agent return
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent returned: {tool_name} execution {execution_id} - {processed_results['summary']}"
        )
        
        result = {
            "workflow_context": workflow_context,
            "execution_results": processed_results,
            "next_phase": next_phase_info,
            "workflow_status": self._get_workflow_status(workflow_context, processed_results),
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result for future use
        self.cache.cache_content_analysis(cache_key, json.dumps(result), "agent_callback")
        
        return result
    
    @handle_errors(operation_name="process_execution_results", return_dict=True)
    def _process_execution_results(self, workflow_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate execution results"""
        
        processed_files = []
        file_count = 0
        
        # Process files created during execution
        if execution_data.get('files'):
            for file_ref in execution_data['files']:
                try:
                    # Files are accessible because uploaded via Code Execution
                    file_info = self._process_execution_file(workflow_id, file_ref)
                    processed_files.append(file_info)
                    file_count += 1
                except Exception as e:
                    processed_files.append({
                        "file_ref": file_ref,
                        "error": str(e),
                        "accessible": False
                    })
        
        # Extract execution metrics
        metrics = {
            "execution_time": execution_data.get('execution_time', 0),
            "files_created": file_count,
            "success": execution_data.get('success', False),
            "tool_used": execution_data.get('tool_name', 'unknown')
        }
        
        # Generate summary
        summary = self._generate_execution_summary(execution_data, metrics)
        
        return {
            "execution_id": execution_data.get('execution_id'),
            "tool_name": execution_data.get('tool_name'),
            "success": execution_data.get('success', False),
            "files": processed_files,
            "metrics": metrics,
            "summary": summary,
            "raw_results": execution_data.get('result', {}),
            "error": execution_data.get('error')
        }
    
    def _process_execution_file(self, workflow_id: str, file_ref: str) -> Dict[str, Any]:
        """Process individual execution file"""
        
        try:
            # In real implementation, would read from Files API or Code Execution
            # For now, simulate file processing
            file_content = f"Mock content for {file_ref}"
            file_size = len(file_content)
            
            # Extract file metadata
            file_info = {
                "file_ref": file_ref,
                "filename": Path(file_ref).name,
                "size": file_size,
                "content_preview": file_content[:100] + "..." if len(file_content) > 100 else file_content,
                "accessible": True,
                "file_type": Path(file_ref).suffix,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            # Save to Files API for later access
            draft_id = self.files_api.save_draft(
                workflow_id,
                file_content,
                "agent-execution",
                Path(file_ref).name
            )
            
            file_info["draft_id"] = draft_id
            
            return file_info
            
        except Exception as e:
            return {
                "file_ref": file_ref,
                "error": str(e),
                "accessible": False,
                "processing_timestamp": datetime.now().isoformat()
            }
    
    def _generate_execution_summary(self, execution_data: Dict, metrics: Dict) -> str:
        """Generate human-readable execution summary"""
        
        tool_name = execution_data.get('tool_name', 'Unknown tool')
        success = execution_data.get('success', False)
        file_count = metrics.get('files_created', 0)
        
        if success:
            summary = f"{tool_name} executed successfully"
            if file_count > 0:
                summary += f" and created {file_count} file{'s' if file_count != 1 else ''}"
        else:
            error = execution_data.get('error', 'Unknown error')
            summary = f"{tool_name} execution failed: {error}"
        
        return summary
    
    def _determine_next_phase(self, workflow_context: Dict, execution_results: Dict) -> Dict[str, Any]:
        """Determine next workflow phase based on results"""
        
        if not workflow_context:
            return {
                "phase_available": False,
                "reason": "No workflow context available"
            }
        
        # Extract workflow observations
        observations = workflow_context.get('observations', [])
        
        # Count completed phases
        completed_phases = len([obs for obs in observations if "execution completed" in obs])
        
        # Simple phase progression logic
        # In real implementation, this would be more sophisticated
        if execution_results.get('success'):
            return {
                "phase_available": True,
                "next_phase_number": completed_phases + 1,
                "phase_type": "continuation",
                "recommendations": self._generate_phase_recommendations(execution_results),
                "ready_to_proceed": True
            }
        else:
            return {
                "phase_available": True,
                "next_phase_number": completed_phases,
                "phase_type": "retry",
                "recommendations": ["Fix execution errors", "Review tool configuration"],
                "ready_to_proceed": False
            }
    
    def _generate_phase_recommendations(self, execution_results: Dict) -> List[str]:
        """Generate recommendations for next phase"""
        
        recommendations = []
        
        # File-based recommendations
        file_count = len(execution_results.get('files', []))
        if file_count > 0:
            recommendations.append(f"Review {file_count} generated files")
            recommendations.append("Consider next workflow phase based on outputs")
        
        # Tool-specific recommendations
        tool_name = execution_results.get('tool_name', '')
        if 'research' in tool_name.lower():
            recommendations.append("Proceed to analysis phase")
        elif 'analysis' in tool_name.lower():
            recommendations.append("Proceed to creative/implementation phase")
        elif 'creative' in tool_name.lower():
            recommendations.append("Review and finalize deliverables")
        
        return recommendations[:3]  # Top 3 recommendations
    
    def _get_workflow_status(self, workflow_context: Dict, execution_results: Dict) -> Dict[str, Any]:
        """Get current workflow status"""
        
        if not workflow_context:
            return {
                "status": "unknown",
                "progress": 0,
                "phase": "unknown"
            }
        
        observations = workflow_context.get('observations', [])
        
        # Count different types of observations
        executions = len([obs for obs in observations if "execution completed" in obs])
        errors = len([obs for obs in observations if "failed" in obs])
        
        # Determine status
        if execution_results.get('success'):
            status = "progressing"
        elif errors > 0:
            status = "error"
        else:
            status = "in_progress"
        
        return {
            "status": status,
            "executions_completed": executions,
            "errors_encountered": errors,
            "last_activity": observations[-1] if observations else "No activity",
            "workflow_health": "healthy" if errors == 0 else "degraded"
        }
    
    @handle_errors(operation_name="prepare_agent_materials", return_dict=True)
    def prepare_agent_materials(self, workflow_id: str, phase_config: Dict[str, Any], 
                              available_tools: List[str]) -> Dict[str, Any]:
        """Prepare materials for agent with executable tools"""
        
        # Get workflow context
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Generate executable buttons for required tools
        tool_buttons = {}
        for tool_name in available_tools:
            button_code = self.code_execution.create_executable_button_snippet(
                tool_name=tool_name,
                workflow_id=workflow_id,
                agent_context=phase_config,
                tool_config={}
            )
            tool_buttons[tool_name] = button_code
        
        agent_materials = {
            "workflow_id": workflow_id,
            "phase": phase_config.get('name', 'unknown'),
            "context": workflow_context,
            "tools": tool_buttons,
            "instructions": phase_config.get('instructions', ''),
            "expected_outputs": phase_config.get('expected_outputs', []),
            "callback_info": {
                "workflow_id": workflow_id,
                "phase_name": phase_config.get('name'),
                "return_method": "agent_callback_handler"
            }
        }
        
        # Track material preparation
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent materials prepared for phase: {phase_config.get('name', 'unknown')}"
        )
        
        return agent_materials
    
    def get_workflow_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get complete workflow execution history"""
        
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        if not workflow_context:
            return []
        
        observations = workflow_context.get('observations', [])
        
        # Parse observations into structured history
        history = []
        for obs in observations:
            if "execution completed" in obs:
                # Parse execution completion
                parts = obs.split(" - ")
                if len(parts) >= 2:
                    history.append({
                        "type": "execution_completed",
                        "timestamp": parts[0] if ":" in parts[0] else datetime.now().strftime('%H:%M:%S'),
                        "details": parts[1] if len(parts) > 1 else obs,
                        "raw_observation": obs
                    })
            elif "failed" in obs:
                # Parse failures
                history.append({
                    "type": "execution_failed",
                    "timestamp": datetime.now().strftime('%H:%M:%S'),
                    "details": obs,
                    "raw_observation": obs
                })
            else:
                # General workflow events
                history.append({
                    "type": "workflow_event",
                    "timestamp": datetime.now().strftime('%H:%M:%S'),
                    "details": obs,
                    "raw_observation": obs
                })
        
        return history


# === CONVENIENCE FUNCTIONS ===

def create_agent_callback_handler() -> AgentCallbackHandler:
    """Factory function for Agent Callback Handler"""
    return AgentCallbackHandler()

def handle_agent_return(workflow_id: str, execution_data: Dict) -> Dict[str, Any]:
    """Quick function to handle agent return"""
    handler = create_agent_callback_handler()
    return handler.handle_agent_return(workflow_id, execution_data)
