#!/usr/bin/env python3
"""
Agent Callback Handler of the Workflow Progression System
Handles agent returns, execution results, and workflow progression
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError

# Set up logger
logger = logging.getLogger(__name__)

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
        # Agent callback operations are typically free (memory / file operations)
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
                    # Process real execution files via Files API or Code Execution
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
            # Read actual file content from Files API or Code Execution
            file_content = ""
            file_size = 0
            
            # Try to read from Files API first
            try:
                file_content = self.files_api.client.download(file_ref)
                file_size = len(file_content)
            except Exception:
                # Try to read from Code Execution tool
                try:
                    file_content = self.code_execution.read_file(file_ref)
                    file_size = len(file_content)
                except Exception:
                    # If both fail, log error and continue with empty content
                    logger.warning(f"Unable to read file content for {file_ref}")
                    file_content = ""
                    file_size = 0
            
            # Extract file metadata
            file_info = {
                "file_ref": file_ref,
                "filename": Path(file_ref).name,
                "size": file_size,
                "content_preview": file_content[:100] + "..." if len(file_content) > 100 else file_content,
                "accessible": file_size > 0,
                "file_type": Path(file_ref).suffix,
                "processing_timestamp": datetime.now().isoformat()
            }
            
            # Save to Files API for later access if we got content
            if file_content:
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
        """Determine next workflow phase based on actual results and context"""
        
        if not workflow_context:
            return {
                "phase_available": False,
                "reason": "No workflow context available"
            }
        
        # Extract workflow observations
        observations = workflow_context.get('observations', [])
        
        # Count completed phases
        completed_phases = len([obs for obs in observations if "execution completed" in obs])
        
        # AI-driven phase progression based on comprehensive analysis
        if execution_results.get('success'):
            return {
                "phase_available": True,
                "next_phase_number": completed_phases + 1,
                "phase_type": "continuation",
                "recommendations": self._generate_contextual_recommendations(workflow_context, execution_results),
                "ready_to_proceed": True,
                "analysis_context": self._create_phase_analysis_context(workflow_context, execution_results)
            }
        else:
            return {
                "phase_available": True,
                "next_phase_number": completed_phases,
                "phase_type": "retry",
                "recommendations": self._generate_failure_recovery_guidance(workflow_context, execution_results),
                "ready_to_proceed": False,
                "analysis_context": self._create_failure_analysis_context(workflow_context, execution_results)
            }
    
    def _generate_contextual_recommendations(self, workflow_context: Dict, execution_results: Dict) -> List[str]:
        """Generate AI-driven contextual recommendations based on comprehensive analysis"""
        
        # Provide rich context for AI to generate intelligent recommendations
        analysis_data = {
            "workflow_goal": workflow_context.get('goal', ''),
            "execution_success": execution_results.get('success', False),
            "files_created": len(execution_results.get('files', [])),
            "tool_used": execution_results.get('tool_name', ''),
            "execution_summary": execution_results.get('summary', ''),
            "workflow_progress": len(workflow_context.get('observations', [])),
            "deliverables_quality": self._assess_deliverable_quality(execution_results),
            "context_continuity": self._assess_context_continuity(workflow_context, execution_results)
        }
        
        # Let AI analyze the situation and provide contextual guidance
        # This allows for culturally neutral, goal-specific recommendations
        return self._ai_analyze_next_steps(analysis_data)
    
    def _generate_failure_recovery_guidance(self, workflow_context: Dict, execution_results: Dict) -> List[str]:
        """Generate AI-driven failure recovery guidance based on actual error context"""
        
        failure_context = {
            "error_details": execution_results.get('error', ''),
            "tool_used": execution_results.get('tool_name', ''),
            "execution_attempt": execution_results.get('execution_id', ''),
            "workflow_goal": workflow_context.get('goal', ''),
            "previous_successes": [obs for obs in workflow_context.get('observations', []) if "completed" in obs],
            "failure_patterns": self._identify_failure_patterns(workflow_context),
            "resource_availability": self._check_resource_status(execution_results)
        }
        
        # Generate intelligent recovery strategies based on actual failure context
        return self._ai_analyze_failure_recovery(failure_context)
    
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
    
    @handle_errors(operation_name="handle_parallel_agent_returns", return_dict=True)
    def handle_parallel_agent_returns(self, workflow_id: str, parallel_execution_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle multiple simultaneous agent returns for parallel execution"""
        
        if not parallel_execution_data:
            return {"success": False, "error": "No execution data provided"}
        
        # Process each agent return individually
        individual_results = []
        for execution_data in parallel_execution_data:
            try:
                result = self.handle_agent_return(workflow_id, execution_data)
                individual_results.append(result)
            except Exception as e:
                individual_results.append({
                    "success": False,
                    "error": str(e),
                    "execution_id": execution_data.get("execution_id", "unknown")
                })
        
        # Aggregate parallel results
        aggregated_results = self._aggregate_parallel_results(individual_results)
        
        # Determine group completion status
        group_completion = self._assess_parallel_group_completion(individual_results)
        
        # Update workflow state with parallel completion
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Parallel group completed: {len(individual_results)} agents returned - {group_completion['summary']}"
        )
        
        return {
            "parallel_execution": True,
            "individual_results": individual_results,
            "aggregated_deliverables": aggregated_results,
            "group_completion": group_completion,
            "ready_for_next_phase": group_completion["all_successful"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _aggregate_parallel_results(self, individual_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from parallel agent executions"""
        
        all_files = []
        total_cost = 0.0
        all_tools_used = set()
        success_count = 0
        
        for result in individual_results:
            execution_results = result.get("execution_results", {})
            
            # Aggregate files
            files = execution_results.get("files", [])
            all_files.extend(files)
            
            # Aggregate metrics
            metrics = execution_results.get("metrics", {})
            if isinstance(metrics, dict):
                total_cost += metrics.get("cost", 0.0)
                all_tools_used.add(metrics.get("tool_used", "unknown"))
            
            # Count successes
            if execution_results.get("success", False):
                success_count += 1
        
        return {
            "combined_files": all_files,
            "total_parallel_cost": total_cost,
            "tools_utilized": list(all_tools_used),
            "success_rate": success_count / len(individual_results) if individual_results else 0,
            "total_deliverables": len(all_files)
        }
    
    def _assess_parallel_group_completion(self, individual_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the completion status of a parallel agent group"""
        
        successful_agents = [r for r in individual_results if r.get("execution_results", {}).get("success", False)]
        failed_agents = [r for r in individual_results if not r.get("execution_results", {}).get("success", False)]
        
        all_successful = len(failed_agents) == 0
        partial_success = len(successful_agents) > 0
        
        return {
            "all_successful": all_successful,
            "partial_success": partial_success,
            "successful_count": len(successful_agents),
            "failed_count": len(failed_agents),
            "total_agents": len(individual_results),
            "summary": f"{len(successful_agents)}/{len(individual_results)} agents completed successfully",
            "completion_quality": "complete" if all_successful else ("partial" if partial_success else "failed")
        }
    
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
    
    def _assess_deliverable_quality(self, execution_results: Dict) -> str:
        """Assess the quality of deliverables based on execution results"""
        
        files = execution_results.get('files', [])
        success = execution_results.get('success', False)
        
        if not success:
            return "execution_failed"
        
        if not files:
            return "no_deliverables"
        
        # Analyze file accessibility and content
        accessible_files = [f for f in files if f.get('accessible', False)]
        if len(accessible_files) == 0:
            return "deliverables_inaccessible"
        elif len(accessible_files) < len(files):
            return "partial_deliverables"
        else:
            return "deliverables_complete"
    
    def _assess_context_continuity(self, workflow_context: Dict, execution_results: Dict) -> str:
        """Assess how well execution results align with workflow context"""
        
        workflow_goal = workflow_context.get('goal', '')
        execution_summary = execution_results.get('summary', '')
        
        if not workflow_goal or not execution_summary:
            return "insufficient_context"
        
        # This provides context for AI to make intelligent assessments
        # rather than using hardcoded pattern matching
        return "context_available_for_analysis"
    
    def _identify_failure_patterns(self, workflow_context: Dict) -> List[str]:
        """Identify patterns in workflow failures for intelligent recovery"""
        
        observations = workflow_context.get('observations', [])
        failure_observations = [obs for obs in observations if "failed" in obs.lower()]
        
        # Return actual failure context for AI analysis rather than predetermined patterns
        return failure_observations
    
    def _check_resource_status(self, execution_results: Dict) -> Dict[str, Any]:
        """Check the status of resources used in execution for recovery planning"""
        
        return {
            "tool_available": execution_results.get('tool_name') is not None,
            "files_accessible": len([f for f in execution_results.get('files', []) if f.get('accessible', False)]),
            "execution_environment": "available" if execution_results.get('execution_id') else "unknown"
        }
    
    def _create_phase_analysis_context(self, workflow_context: Dict, execution_results: Dict) -> Dict[str, Any]:
        """Create rich context for AI phase analysis"""
        
        return {
            "workflow_progression": len(workflow_context.get('observations', [])),
            "execution_quality": self._assess_deliverable_quality(execution_results),
            "context_alignment": self._assess_context_continuity(workflow_context, execution_results),
            "resource_status": self._check_resource_status(execution_results),
            "goal_context": workflow_context.get('goal', ''),
            "execution_context": execution_results.get('summary', '')
        }
    
    def _create_failure_analysis_context(self, workflow_context: Dict, execution_results: Dict) -> Dict[str, Any]:
        """Create comprehensive failure analysis context"""
        
        return {
            "failure_details": execution_results.get('error', ''),
            "execution_history": workflow_context.get('observations', []),
            "failure_patterns": self._identify_failure_patterns(workflow_context),
            "resource_status": self._check_resource_status(execution_results),
            "recovery_options": self._assess_recovery_options(workflow_context, execution_results)
        }
    
    def _assess_recovery_options(self, workflow_context: Dict, execution_results: Dict) -> List[str]:
        """Assess available recovery options based on actual context"""
        
        options = []
        
        # Tool-based recovery options
        if execution_results.get('tool_name'):
            options.append("tool_retry_available")
        
        # Context-based recovery options  
        if workflow_context.get('observations'):
            options.append("context_rollback_possible")
        
        # Resource-based recovery options
        if execution_results.get('files'):
            options.append("partial_results_salvageable")
        
        return options
    
    def _ai_analyze_next_steps(self, analysis_data: Dict) -> List[str]:
        """Placeholder for AI-driven next step analysis"""
        # In a production system, this would integrate with the AI model
        # to generate contextual recommendations based on the analysis_data
        # For now, return context-aware generic guidance that avoids hardcoding
        
        recommendations = []
        
        if analysis_data.get("deliverables_quality") == "deliverables_complete":
            recommendations.append("Proceed with workflow based on successful deliverables")
        
        if analysis_data.get("files_created", 0) > 0:
            recommendations.append("Review generated outputs for next phase planning")
        
        if analysis_data.get("workflow_goal"):
            recommendations.append("Align next steps with stated workflow objectives")
        
        return recommendations[:3]
    
    def _ai_analyze_failure_recovery(self, failure_context: Dict) -> List[str]:
        """Placeholder for AI-driven failure recovery analysis"""
        # In a production system, this would use AI to analyze the actual failure
        # and generate recovery strategies based on the specific error context
        
        recovery_strategies = []
        
        if failure_context.get("resource_availability", {}).get("tool_available"):
            recovery_strategies.append("Retry execution with current tool configuration")
        
        if failure_context.get("previous_successes"):
            recovery_strategies.append("Apply successful patterns from previous phases")
        
        if failure_context.get("error_details"):
            recovery_strategies.append("Address specific error conditions identified")
        
        return recovery_strategies[:3]


# === CONVENIENCE FUNCTIONS ===

def create_agent_callback_handler() -> AgentCallbackHandler:
    """Factory function for Agent Callback Handler"""
    return AgentCallbackHandler()

def handle_agent_return(workflow_id: str, execution_data: Dict) -> Dict[str, Any]:
    """Quick function to handle agent return"""
    handler = create_agent_callback_handler()
    return handler.handle_agent_return(workflow_id, execution_data)

def handle_parallel_agent_returns(workflow_id: str, parallel_execution_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Quick function to handle parallel agent returns"""
    handler = create_agent_callback_handler()
    return handler.handle_parallel_agent_returns(workflow_id, parallel_execution_data)