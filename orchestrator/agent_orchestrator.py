# orchestrator/agent_orchestrator.py
"""
Agent Orchestration - Component B
Coordinates agent handoffs with context packages via Files API
Follows clean, focused patterns - no unnecessary complexity
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import MCP components built in previous phases
from orchestrator.memory_mcp import MemoryMCPManager
from orchestrator.files_api import FilesAPIManager
from orchestrator.manager_tools import ToolManager


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
    Coordinates agent handoffs with context packages
    Simple, focused orchestration following proven SFA patterns
    """
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        self.tool_manager = ToolManager()
    
    def execute_workflow_phase(self, workflow_id: str, phase: dict) -> Dict[str, Any]:
        """Execute a workflow phase with agent coordination"""
        
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
        
        return {
            "success": True,
            "package_id": package_id,
            "agent_instructions": handoff_package["instructions"],
            "tool_buttons": handoff_package["tool_buttons"],
            "callback_info": handoff_package["callback"],
            "phase_context": handoff_package["phase_info"]
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
        """Generate comprehensive instructions for the agent"""
        
        instructions = f"""
# Workflow Phase: {phase['name']}

## Your Role
{phase.get('agent_role', 'Workflow execution agent')}

## Phase Objective
{phase.get('task_instructions', 'Complete the assigned workflow phase')}

## Workflow Context
**Goal**: {context.get('goal', 'Not specified')}
**Previous Results**: {len(context.get('deliverables', []))} deliverables available

## Available Tools
{self._format_tool_list(phase.get('tools', []))}

## Expected Deliverables
{self._format_deliverables_list(phase.get('expected_outputs', []))}

## Execution Guidelines
1. Use the provided tool buttons for all tool interactions
2. Follow the phase objective closely
3. Build on previous deliverables when relevant
4. Document your process and decisions
5. Call back when phase is complete with all deliverables

## Success Criteria
{phase.get('success_criteria', 'Phase completed with all expected deliverables')}

## Important Notes
- This is part of a larger workflow; maintain consistency with previous phases
- Use Memory MCP integration for state tracking if available
- Quality over speed; thorough execution expected
"""
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
        """Validate agent callback results format"""
        
        errors = []
        
        # Check required fields
        required_fields = ["success", "deliverables"]
        for field in required_fields:
            if field not in results:
                errors.append(f"Missing required field: {field}")
        
        # Validate deliverables format
        deliverables = results.get("deliverables", [])
        if not isinstance(deliverables, list):
            errors.append("Deliverables must be a list")
        
        # Check success field type
        success = results.get("success")
        if success is not None and not isinstance(success, bool):
            errors.append("Success field must be boolean")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "retry_instructions": "Ensure callback includes: success (bool), deliverables (list)"
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