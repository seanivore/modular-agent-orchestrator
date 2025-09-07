# orchestrator/agent_orchestrator.py
"""
Agent Orchestration 
Coordinates agent handoffs with context packages via Files API
"""

import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import MCP components built in previous phases
from .memory_mcp import MemoryMCPManager
from tools.files_api.files_api import FilesAPIManager
from .manager_tools import ToolManager
from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError
from pathlib import Path


@dataclass
class PhaseResult:
    """Results from completed workflow phase"""
    phase_name: str
    deliverables: List[str]
    success: bool
    agent_feedback: str
    execution_time: float
    cost: float


class AgentOrchestrator:
    """
    Coordinates agent handoffs with parallel execution support
    Simple, focused orchestration trusting AI intelligence completely
    Supports simultaneous agents with phase patterns like 01a, 01b, 01c
    """
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        self.tool_manager = ToolManager()
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Agent orchestration involves phase coordination and file operations
        base_cost = 0.0
        
        # Add cost for workflow phases
        num_phases = params.get("num_phases", 1)
        base_cost += num_phases * 0.005  # $0.005 per phase coordination
        
        # Add cost for parallel agent execution
        parallel_agents = params.get("parallel_agents", 1)
        base_cost += parallel_agents * 0.003  # $0.003 per parallel agent
        
        # Add cost for file operations
        file_operations = params.get("file_operations", 2)
        base_cost += file_operations * 0.002  # $0.002 per file operation
        
        return base_cost
    
    @handle_errors(operation_name="execute_workflow_phase", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, ConnectionError))
    def execute_workflow_phase(self, workflow_id: str, phase: dict) -> Dict[str, Any]:
        """Execute a workflow phase with agent coordination"""
        
        # Check cache for similar phase executions
        cache_key = f"{workflow_id}|{phase.get('name', 'unknown')}|phase_execution"
        cached_result = self.cache.get_cached_analysis(cache_key, "workflow_phase")
        if cached_result:
            return json.loads(cached_result)
        
        # Get workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        if not workflow_context:
            return {
                "success": False,
                "error": f"No workflow context found for {workflow_id}"
            }
        
        # Prepare agent handoff package
        handoff_package = self._create_agent_package(
            workflow_id, 
            phase, 
            workflow_context
        )
        
        # Store package via Files API
        package_id = self.files_api.save_agent_package(workflow_id, handoff_package)
        
        # Track phase start in Memory MCP
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Phase started: {phase['name']} (Package: {package_id})"
        )
        
        result = {
            "success": True,
            "package_id": package_id,
            "agent_instructions": handoff_package["instructions"],
            "tool_buttons": handoff_package["tool_buttons"],
            "callback_info": handoff_package["callback"],
            "phase_context": handoff_package["phase_info"]
        }
        
        # Cache the result for future use
        self.cache.cache_content_analysis(cache_key, json.dumps(result), "workflow_phase")
        
        return result
    
    @handle_errors(operation_name="execute_parallel_phases", return_dict=True)
    async def execute_parallel_phases(self, workflow_id: str, phase_group: List[dict]) -> Dict[str, Any]:
        """Execute multiple agents in parallel for simultaneous workflow phases"""
        
        if not phase_group:
            return {"success": False, "error": "No phases provided for parallel execution"}
        
        # Check cache for similar parallel executions
        phase_names = "|".join([phase.get('name', 'unknown') for phase in phase_group])
        cache_key = f"{workflow_id}|parallel|{phase_names}"
        cached_result = self.cache.get_cached_analysis(cache_key, "parallel_phases")
        if cached_result:
            return json.loads(cached_result)
        
        # Get workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        if not workflow_context:
            return {
                "success": False,
                "error": f"No workflow context found for {workflow_id}"
            }
        
        # Create agent packages for all parallel phases
        parallel_packages = []
        for phase in phase_group:
            package = self._create_agent_package(workflow_id, phase, workflow_context)
            parallel_packages.append(package)
        
        # Store all packages simultaneously via Files API
        package_storage_tasks = []
        for package in parallel_packages:
            task = asyncio.create_task(
                self._store_agent_package_async(workflow_id, package)
            )
            package_storage_tasks.append(task)
        
        try:
            package_ids = await asyncio.gather(*package_storage_tasks)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to store parallel packages: {str(e)}"
            }
        
        # Track parallel group start in Memory MCP
        phase_list = ", ".join([phase['name'] for phase in phase_group])
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Parallel group started: {phase_list} (Packages: {', '.join(package_ids)})"
        )
        
        result = {
            "success": True,
            "parallel_execution": True,
            "phase_count": len(phase_group),
            "package_ids": package_ids,
            "agent_packages": parallel_packages,
            "group_id": f"group_{uuid.uuid4().hex[:8]}",
            "simultaneous_agents": len(phase_group)
        }
        
        # Cache the parallel execution result
        self.cache.cache_content_analysis(cache_key, json.dumps(result), "parallel_phases")
        
        return result
    
    async def _store_agent_package_async(self, workflow_id: str, package: dict) -> str:
        """Asynchronously store agent package via Files API"""
        # Wrapper for async package storage
        return self.files_api.save_agent_package(workflow_id, package)
    
    @handle_errors(operation_name="handle_parallel_callbacks", return_dict=True)
    def handle_parallel_callbacks(self, workflow_id: str, parallel_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process multiple simultaneous agent completion callbacks"""
        
        if not parallel_results:
            return {"success": False, "error": "No parallel results provided"}
        
        individual_results = []
        all_deliverables = []
        successful_phases = 0
        total_cost = 0.0
        
        # Process each parallel result
        for result in parallel_results:
            try:
                phase_name = result.get('phase_name', 'unknown')
                
                # Process individual callback (reuse existing logic)
                processed = self.handle_agent_callback(
                    workflow_id, 
                    phase_name, 
                    result
                )
                
                individual_results.append(processed)
                
                # Aggregate deliverables and metrics
                if processed.get('success', False):
                    successful_phases += 1
                    deliverables = processed.get('deliverables', {}).get('processed_files', [])
                    all_deliverables.extend(deliverables)
                    total_cost += result.get('cost', 0.0)
                    
            except Exception as e:
                individual_results.append({
                    "success": False,
                    "error": str(e),
                    "phase_name": result.get('phase_name', 'unknown')
                })
        
        # Aggregate parallel group results
        group_completion = {
            "all_successful": successful_phases == len(parallel_results),
            "success_rate": successful_phases / len(parallel_results) if parallel_results else 0,
            "successful_count": successful_phases,
            "total_phases": len(parallel_results),
            "combined_deliverables": len(all_deliverables),
            "total_cost": total_cost
        }
        
        # Update workflow state with parallel completion
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Parallel group completed: {successful_phases}/{len(parallel_results)} phases successful | "
            f"Deliverables: {len(all_deliverables)} | Cost: ${total_cost:.4f}"
        )
        
        # Determine next phase based on group completion
        next_phase_info = self._determine_next_phase_from_parallel(
            workflow_id, individual_results, group_completion
        )
        
        return {
            "success": True,
            "parallel_execution": True,
            "individual_results": individual_results,
            "group_completion": group_completion,
            "aggregated_deliverables": all_deliverables,
            "next_phase": next_phase_info,
            "workflow_status": self._get_workflow_status(workflow_id)
        }
    
    def _determine_next_phase_from_parallel(self, workflow_id: str, individual_results: List[Dict], group_completion: Dict) -> Dict[str, Any]:
        """Determine next workflow phase after parallel group completion"""
        
        # Get workflow context for intelligent phase progression
        context = self.memory_mcp.get_workflow_context(workflow_id)
        if not context:
            return {"available": False, "reason": "No workflow context"}
        
        # AI-driven phase determination based on parallel group results
        # MAO_FLOW.md: Let AI analyze deliverables and determine optimal next steps
        analysis_context = {
            "parallel_completion": group_completion,
            "workflow_goal": context.get('goal', ''),
            "total_deliverables": group_completion.get('combined_deliverables', 0),
            "success_rate": group_completion.get('success_rate', 0),
            "workflow_progress": len(context.get('observations', [])),
            "deliverable_quality": "high" if group_completion.get('all_successful', False) else "mixed"
        }
        
        # Trust AI intelligence to determine appropriate next phase
        # Provide rich context for intelligent workflow progression
        if group_completion.get('all_successful', False):
            return {
                "available": True,
                "progression_type": "continue_workflow",
                "analysis_context": analysis_context,
                "ai_recommendation": "Analyze parallel deliverables to determine optimal next workflow phase",
                "ready_for_progression": True
            }
        else:
            return {
                "available": True,
                "progression_type": "handle_partial_completion",
                "analysis_context": analysis_context,
                "ai_recommendation": "Review partial results and determine recovery or continuation strategy",
                "ready_for_progression": False
            }
    
    def _create_agent_package(self, workflow_id: str, phase: dict, context: dict) -> dict:
        """Create complete agent handoff package"""
        
        # Generate executable tool buttons for this phase
        tool_buttons = {}
        for tool_name in phase.get("tools", []):
            try:
                tool_buttons[tool_name] = self.tool_manager.create_button_snippet(
                    tool_name,
                    {
                        "workflow_id": workflow_id, 
                        "phase": phase["name"],
                        "context": "workflow_execution"
                    },
                    phase.get("model", "claude-sonnet-4")
                )
            except Exception as e:
                # Graceful degradation - include error info but continue
                tool_buttons[tool_name] = {
                    "error": f"Tool {tool_name} unavailable: {str(e)}",
                    "fallback_instructions": f"Please use {tool_name} manually if needed"
                }
        
        # Generate comprehensive agent instructions
        instructions = self._generate_agent_instructions(phase, context)
        
        # Create callback configuration
        callback_config = {
            "workflow_id": workflow_id,
            "phase_name": phase["name"],
            "callback_method": "handle_agent_callback",
            "required_deliverables": phase.get("expected_outputs", []),
            "success_criteria": phase.get("success_criteria", "Phase completed successfully")
        }
        
        return {
            "workflow_id": workflow_id,
            "package_id": f"pkg_{uuid.uuid4().hex[:8]}",
            "created_at": datetime.now().isoformat(),
            "phase_info": phase,
            "previous_deliverables": context.get("deliverables", []),
            "workflow_goal": context.get("goal", "No goal specified"),
            "tool_buttons": tool_buttons,
            "instructions": instructions,
            "callback": callback_config,
            "context_summary": self._create_context_summary(context)
        }
    
    def _generate_agent_instructions(self, phase: dict, context: dict) -> str:
        """Generate context-rich instructions trusting AI communication intelligence"""
        
        # Provide rich context and let AI determine optimal communication approach
        # MAO_FLOW.md: Trust AI completely - no rigid templates or constraints
        core_context = {
            "phase_name": phase.get('name', 'Workflow Phase'),
            "objective": phase.get('task_instructions', 'Complete the assigned workflow phase'),
            "workflow_goal": context.get('goal', 'Not specified'),
            "available_tools": phase.get('tools', []),
            "expected_outputs": phase.get('expected_outputs', []),
            "previous_deliverables_count": len(context.get('deliverables', [])),
            "success_criteria": phase.get('success_criteria', 'Phase completed successfully'),
            "agent_role": phase.get('agent_role', 'Workflow execution agent')
        }
        
        # Simple, flexible instruction format that trusts AI intelligence
        instructions = f"""Workflow Phase: {core_context['phase_name']}
        
Objective: {core_context['objective']}
Workflow Goal: {core_context['workflow_goal']}
Available Tools: {', '.join(core_context['available_tools']) if core_context['available_tools'] else 'None specified'}
Expected Outputs: {', '.join(core_context['expected_outputs']) if core_context['expected_outputs'] else 'To be determined'}
Previous Deliverables: {core_context['previous_deliverables_count']} files available

Role: {core_context['agent_role']}
Success Criteria: {core_context['success_criteria']}

Use provided tool buttons for interactions. This phase is part of a larger workflow - maintain consistency and quality."""
        
        return instructions.strip()
    
    def _format_tool_list(self, tools: List[str]) -> str:
        """Format tool list for agent instructions"""
        if not tools:
            return "- No specific tools assigned for this phase"
        
        formatted = []
        for tool in tools:
            formatted.append(f"- {tool}")
        return "\n".join(formatted)
    
    def _format_deliverables_list(self, deliverables: List[str]) -> str:
        """Format deliverables list for agent instructions"""
        if not deliverables:
            return "- Complete phase objectives (specific deliverables TBD)"
        
        formatted = []
        for deliverable in deliverables:
            formatted.append(f"- {deliverable}")
        return "\n".join(formatted)
    
    def _create_context_summary(self, context: dict) -> str:
        """Create concise context summary for agent"""
        
        summary_parts = []
        
        if context.get("goal"):
            summary_parts.append(f"Goal: {context['goal']}")
        
        deliverables = context.get("deliverables", [])
        if deliverables:
            summary_parts.append(f"Previous deliverables: {len(deliverables)} files")
        
        if context.get("progress"):
            summary_parts.append(f"Progress: {context['progress']}")
        
        return " | ".join(summary_parts) if summary_parts else "No context summary available"
    
    @handle_errors(operation_name="handle_agent_callback", return_dict=True)
    def handle_agent_callback(self, workflow_id: str, phase_name: str, results: dict) -> dict:
        """Process agent completion callback"""
        
        try:
            # Validate callback results
            validation = self._validate_callback_results(results)
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": f"Invalid callback results: {validation['errors']}",
                    "retry_instructions": validation["retry_instructions"]
                }
            
            # Process deliverables via Files API
            deliverable_results = self._process_deliverables(
                workflow_id, 
                phase_name, 
                results.get("deliverables", [])
            )
            
            # Update workflow state in Memory MCP
            phase_result = PhaseResult(
                phase_name=phase_name,
                deliverables=deliverable_results["processed_files"],
                success=results.get("success", False),
                agent_feedback=results.get("feedback", "No feedback provided"),
                execution_time=results.get("execution_time", 0.0),
                cost=results.get("cost", 0.0)
            )
            
            # Store results in Memory MCP
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Phase completed: {phase_name} | "
                f"Deliverables: {len(deliverable_results['processed_files'])} | "
                f"Success: {phase_result.success}"
            )
            
            # Determine next phase or completion
            next_phase_info = self._determine_next_phase(workflow_id, phase_result)
            
            return {
                "success": True,
                "phase_result": phase_result.__dict__,
                "deliverables": deliverable_results,
                "next_phase": next_phase_info,
                "workflow_status": self._get_workflow_status(workflow_id)
            }
            
        except Exception as e:
            # Log error and return graceful failure
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Phase callback error: {phase_name} | Error: {str(e)}"
            )
            
            return {
                "success": False,
                "error": str(e),
                "phase_name": phase_name,
                "recovery_suggestions": [
                    "Check agent callback format",
                    "Verify deliverables are accessible",
                    "Review phase requirements"
                ]
            }
    
    def _validate_callback_results(self, results: dict) -> dict:
        """Lightweight validation trusting agent intelligence"""
        
        # MAO_FLOW.md: Trust AI completely - minimal validation
        # Agent intelligence is sufficient for most validation concerns
        errors = []
        
        # Only validate essential structure exists
        if not isinstance(results, dict):
            errors.append("Results must be a dictionary")
        
        # Trust agent intelligence for field presence and format
        # Agents are perfectly capable of providing appropriate results
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "retry_instructions": "Provide results as dictionary structure"
        }
    
    def _process_deliverables(self, workflow_id: str, phase_name: str, deliverables: List[str]) -> dict:
        """Process and store phase deliverables"""
        
        processed_files = []
        processing_errors = []
        
        for deliverable in deliverables:
            try:
                # Store deliverable via Files API
                file_result = self.files_api.store_workflow_deliverable(
                    workflow_id,
                    phase_name,
                    deliverable
                )
                processed_files.append(file_result)
                
            except Exception as e:
                processing_errors.append({
                    "deliverable": deliverable,
                    "error": str(e)
                })
        
        return {
            "processed_files": processed_files,
            "processing_errors": processing_errors,
            "total_deliverables": len(deliverables),
            "successful_processing": len(processed_files)
        }
    
    def _determine_next_phase(self, workflow_id: str, completed_phase: PhaseResult) -> dict:
        """Determine next workflow phase or completion"""
        
        # Get current workflow context
        context = self.memory_mcp.get_workflow_context(workflow_id)
        if not context:
            return {"available": False, "reason": "No workflow context"}
        
        # Simple next phase logic (can be enhanced)
        workflow_config = context.get("workflow_config", {})
        all_phases = workflow_config.get("phases", [])
        
        # Find current phase index
        current_index = -1
        for i, phase in enumerate(all_phases):
            if phase.get("name") == completed_phase.phase_name:
                current_index = i
                break
        
        # Check if there's a next phase
        if current_index >= 0 and current_index + 1 < len(all_phases):
            next_phase = all_phases[current_index + 1]
            return {
                "available": True,
                "phase": next_phase,
                "phase_number": current_index + 2,
                "total_phases": len(all_phases)
            }
        else:
            return {
                "available": False,
                "reason": "Workflow complete",
                "completion_status": "All phases executed"
            }
    
    def _get_workflow_status(self, workflow_id: str) -> dict:
        """Get current workflow status summary"""
        
        context = self.memory_mcp.get_workflow_context(workflow_id)
        if not context:
            return {"status": "unknown", "error": "No workflow context"}
        
        observations = context.get("observations", [])
        
        # Count phases
        completed_phases = len([obs for obs in observations if "Phase completed:" in obs])
        started_phases = len([obs for obs in observations if "Phase started:" in obs])
        
        return {
            "status": "active" if started_phases > completed_phases else "ready",
            "phases_completed": completed_phases,
            "phases_started": started_phases,
            "last_activity": observations[-1] if observations else "No activity",
            "workflow_health": "healthy"
        }
    
    @handle_errors(operation_name="recover_interrupted_workflow", return_dict=True)
    def recover_interrupted_workflow(self, workflow_id: str) -> dict:
        """Recover workflow from interruption using Memory MCP"""
        
        try:
            # Get complete workflow context
            context = self.memory_mcp.get_workflow_context(workflow_id)
            if not context:
                return {
                    "success": False,
                    "error": f"No context found for workflow {workflow_id}"
                }
            
            # Analyze workflow state
            status = self._get_workflow_status(workflow_id)
            
            # Determine recovery point
            if status["phases_started"] > status["phases_completed"]:
                # There's an interrupted phase
                return {
                    "success": True,
                    "recovery_type": "resume_interrupted_phase",
                    "message": "Found interrupted phase, ready to resume",
                    "context": context,
                    "status": status
                }
            elif status["phases_completed"] > 0:
                # Previous phases completed, ready for next
                next_phase = self._determine_next_phase(workflow_id, 
                    PhaseResult("", [], True, "", 0, 0))  # Dummy for logic
                
                return {
                    "success": True,
                    "recovery_type": "continue_next_phase",
                    "message": f"Ready to continue with next phase",
                    "next_phase": next_phase,
                    "context": context
                }
            else:
                # Workflow was created but never started
                return {
                    "success": True,
                    "recovery_type": "restart_workflow",
                    "message": "Workflow ready to start from beginning",
                    "context": context
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Recovery failed: {str(e)}",
                "recovery_suggestions": [
                    "Check Memory MCP connectivity",
                    "Verify workflow ID is correct",
                    "Review workflow configuration"
                ]
            }
    
    def group_phases_for_parallel_execution(self, phases: List[dict]) -> List[List[dict]]:
        """Group phases by base number for parallel execution (01a, 01b → group 01)"""
        
        if not phases:
            return []
        
        phase_groups = {}
        
        for phase in phases:
            # Extract base phase number from phase numbering like "01a", "01b", "02", etc.
            phase_number = phase.get('phase_number', phase.get('number', '1'))
            
            # Extract base number (01a → 01, 02b → 02, 03 → 03)
            base_number = ''.join(filter(str.isdigit, str(phase_number)))
            if not base_number:
                base_number = "1"  # Default fallback
            
            # Group phases by base number
            if base_number not in phase_groups:
                phase_groups[base_number] = []
            phase_groups[base_number].append(phase)
        
        # Return groups in sorted order
        return [phase_groups[key] for key in sorted(phase_groups.keys())]
    
    async def execute_workflow_with_parallel_support(self, workflow_id: str, phases: List[dict]) -> Dict[str, Any]:
        """Execute workflow with automatic parallel phase detection and execution"""
        
        # Group phases for parallel execution
        phase_groups = self.group_phases_for_parallel_execution(phases)
        
        all_results = []
        workflow_successful = True
        
        # Execute each group (sequential groups, parallel within groups)
        for group in phase_groups:
            if len(group) == 1:
                # Single phase execution
                result = self.execute_workflow_phase(workflow_id, group[0])
                all_results.append(result)
                
                if not result.get('success', False):
                    workflow_successful = False
                    break
            else:
                # Parallel phase group execution
                try:
                    result = await self.execute_parallel_phases(workflow_id, group)
                    all_results.append(result)
                    
                    if not result.get('success', False):
                        workflow_successful = False
                        break
                except Exception as e:
                    workflow_successful = False
                    all_results.append({
                        "success": False,
                        "error": f"Parallel execution failed: {str(e)}",
                        "group_size": len(group)
                    })
                    break
        
        return {
            "workflow_success": workflow_successful,
            "total_groups": len(phase_groups),
            "parallel_groups": len([g for g in phase_groups if len(g) > 1]),
            "sequential_groups": len([g for g in phase_groups if len(g) == 1]),
            "all_results": all_results,
            "execution_pattern": "mixed_parallel_sequential"
        }