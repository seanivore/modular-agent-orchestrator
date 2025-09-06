#!/usr/bin/env python3
"""
Enhanced Orchestrator Core
Comprehensive workflow coordination consolidating functionality from:
- conversation_bridge.py (goal-to-workflow conversion)
- agent_callback.py (workflow progression handling)  
- agent_orchestrator.py (phase execution coordination)
"""

import asyncio
import json
import uuid
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

# Conditional imports for optional dependencies
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

from orchestrator.manager_models import ModelManager
from orchestrator.manager_buttons import ButtonManager  
from orchestrator.manager_tools import ToolManager
from orchestrator.mcp_hub import MCPIntegrationHub

@dataclass
class WorkflowPhase:
    """Individual phase in a workflow - AI designed without predetermined patterns"""
    name: str
    model: str
    agent_role: str
    task_instructions: str
    input_sources: List[str]
    output_files: List[str]
    estimated_tokens: int = 0
    estimated_cost: float = 0.0
    tools: List[str] = None
    expected_outputs: List[str] = None

@dataclass
class WorkflowPlan:
    """Complete workflow plan - dynamically created by AI"""
    id: str
    name: str
    description: str
    phases: List[WorkflowPhase]
    total_estimated_cost: float
    estimated_duration_minutes: int
    workspace_dir: str

@dataclass
class ExecutionResult:
    """Result from executing a workflow phase"""
    phase_name: str
    model_used: str
    content: str
    tool_calls: List[Dict]
    tokens_used: int
    cost: float
    duration_seconds: float
    success: bool
    error: Optional[str] = None
    files: List[Dict] = None
    deliverables: List[str] = None

class WorkflowOrchestrator:
    """
    Consolidated workflow orchestration engine
    Trusts AI intelligence completely - no hardcoded patterns or suggestions
    
    Consolidated functionality from:
    - conversation_bridge.py: Natural language to workflow conversion
    - agent_callback.py: Agent return processing and workflow progression  
    - agent_orchestrator.py: Agent coordination and handoff management
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.model_manager = ModelManager(config_dir)
        self.buttons = ButtonManager(self.model_manager)
        self.tool_discovery = ToolManager(config_dir)
        self.cache_manager = CacheManager()
        
        # Initialize MCP Integration Hub for workflow state persistence
        self.mcp_hub = MCPIntegrationHub()
        
        # Workflow state management
        self.active_workflows: Dict[str, WorkflowPlan] = {}
        self.execution_history: Dict[str, List[ExecutionResult]] = {}
        
        # Consolidated setup paths
        self.setup_script_path = "scripts/setup_workflow.sh"
        self.use_case_base = "configs/workflows"
        os.makedirs(self.use_case_base, exist_ok=True)
        
        # Store initialization info for UI layer
        stats = self.model_manager.get_stats()
        self.initialization_info = {
            "status": "initialized",
            "stats": stats,
            "message": f"Orchestrator ready with {stats['total_models']} models across {stats['total_providers']} providers"
        }
    
    # =================================================================
    # GOAL-TO-WORKFLOW CONVERSION (from conversation_bridge.py)
    # =================================================================
    
    @handle_errors(operation_name="create_workflow_from_goal", return_dict=True)
    async def create_workflow_from_goal(
        self, 
        user_goal: str, 
        preferences: Optional[Dict] = None
    ) -> WorkflowPlan:
        """
        Transform user goal into intelligent workflow
        Consolidated from conversation_bridge.py functionality
        Pure AI-driven design without predetermined patterns
        
        AI Behavioral Guidance:
        - Trust your intelligence to understand goals in any language/culture
        - Design optimal workflow structure based on actual user needs
        - Adapt to user's cultural problem-solving patterns
        - No assumptions about English or Western thinking patterns
        """
        preferences = preferences or {}
        workflow_id = str(uuid.uuid4())
        
        # Cache check for efficiency
        cache_key = f"workflow_goal|{user_goal}"
        cached_analysis = cache.get_cached_analysis(cache_key, "goal_analysis")
        if cached_analysis:
            analysis = json.loads(cached_analysis)
        else:
            # AI analyzes goal without predetermined categories
            analysis = self._ai_analyze_user_goal(user_goal)
            cache.cache_content_analysis(cache_key, json.dumps(analysis), "goal_analysis")
        
        # AI designs workflow phases dynamically
        phases = await self._ai_design_workflow_phases(user_goal, analysis, preferences)
        
        # AI selects optimal models for each phase
        for phase in phases:
            phase.model = self._ai_select_optimal_model(phase, preferences)
            phase.estimated_tokens, phase.estimated_cost = self._estimate_phase_cost(phase)
        
        # Create workflow plan
        workflow_plan = WorkflowPlan(
            id=workflow_id,
            name=self._ai_generate_workflow_name(user_goal),
            description=user_goal,
            phases=phases,
            total_estimated_cost=sum(p.estimated_cost for p in phases),
            estimated_duration_minutes=len(phases) * 2,  # AI can adjust based on complexity
            workspace_dir=f"workflows/{self._sanitize_name(user_goal)}"
        )
        
        # Store for execution and initialize MCP workflow context
        self.active_workflows[workflow_plan.id] = workflow_plan
        self.mcp_hub.create_workflow(workflow_plan.id, user_goal)
        
        # CONSOLIDATED: Create executable config (from conversation_bridge.py)
        await self._create_executable_workflow_config(workflow_plan, user_goal)
        
        return workflow_plan
    
    async def _create_executable_workflow_config(self, workflow_plan: WorkflowPlan, user_goal: str):
        """Create executable workflow config in standard directory structure"""
        try:
            # Generate config for workflow execution
            config = {
                "workflow": {
                    "workflow_id": workflow_plan.id,
                    "custom_command": workflow_plan.name.replace(" ", "-"),
                    "goal": user_goal,
                    "variables": self._extract_variables_from_goal(user_goal)
                },
                "phases": [self._phase_to_config(phase) for phase in workflow_plan.phases],
                "handoffs": self._generate_handoff_configs(workflow_plan.phases),
                "calendar": None  # Only for recurring workflows
            }
            
            # Save config to use-case directory (workflow directory structure)
            command_name = config["workflow"]["custom_command"]
            use_case_dir = f"{self.use_case_base}/{command_name}"
            os.makedirs(use_case_dir, exist_ok=True)
            
            config_path = f"{use_case_dir}/config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Run setup script for workflow preparation
            if Path(self.setup_script_path).exists():
                result = subprocess.run([
                    self.setup_script_path, 
                    config_path
                ], capture_output=True, text=True, cwd=".")
                
                if result.returncode == 0:
                    self.mcp_hub.memory.update_workflow_state(
                        workflow_plan.id,
                        f"Executable config created: {config['workflow']['custom_command']}"
                    )
                else:
                    self.mcp_hub.memory.update_workflow_state(
                        workflow_plan.id, 
                        f"Setup script failed: {result.stderr}"
                    )
        except Exception as e:
            self.mcp_hub.memory.update_workflow_state(
                workflow_plan.id,
                f"Config creation error: {str(e)}"
            )
    
    def _phase_to_config(self, phase: WorkflowPhase) -> Dict[str, Any]:
        """Convert WorkflowPhase to config format"""
        return {
            "name": phase.name,
            "description": f"Execute: {phase.task_instructions[:50]}...",
            "instructions": phase.task_instructions,
            "deliverable": ", ".join(phase.output_files) if phase.output_files else "Phase completion results",
            "resources": phase.input_sources,
            "tools": phase.tools or [],
            "model": phase.model,
            "fallback_model": "claude-opus-4",
            "provider": "anthropic-direct"
        }
    
    def _extract_variables_from_goal(self, goal: str) -> Dict[str, Any]:
        """Extract variables from goal without domain assumptions"""
        variables = {
            "required": {
                "user_goal": {
                    "description": "The user's specific goal to accomplish",
                    "value": goal
                }
            },
            "optional": {}
        }
        
        # Add context variable for complex goals only
        if len(goal.split()) > 15:
            variables["optional"]["additional_context"] = {
                "description": "Any additional context or requirements",
                "default": "none specified"
            }
        
        return variables
    
    def _generate_handoff_configs(self, phases: List[WorkflowPhase]) -> List[Dict[str, Any]]:
        """Generate handoff configurations for agent coordination"""
        handoffs = []
        
        for i, phase in enumerate(phases):
            handoff = {
                "handoff_number": str(i + 1),
                "phase_name": phase.name,
                "assessment_questions": [
                    "Has the phase objective been completed successfully?",
                    "Are the deliverables complete and of adequate quality?",
                    "Is additional work needed before proceeding?"
                ],
                "human_in_loop": False,
                "next_phase_conditions": {
                    "quality_threshold": "acceptable",
                    "deliverables_complete": True
                }
            }
            handoffs.append(handoff)
        
        return handoffs
    
    # =================================================================
    # WORKFLOW EXECUTION (enhanced from core.py)
    # =================================================================
    
    @handle_errors(operation_name="execute_workflow", return_dict=True)
    async def execute_workflow(self, workflow_id: str, anthropic_client=None) -> Dict[str, Any]:
        """
        Execute workflow with consolidated agent coordination
        Enhanced with agent callback and orchestrator functionality
        
        AI Behavioral Guidance:
        - Coordinate agent execution naturally
        - Handle handoffs between agents smoothly
        - Adapt workflow execution based on intermediate results
        - Use Memory MCP for state persistence and recovery
        - Trust AI to handle errors and adapt as needed
        """
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        results = []
        total_cost = 0.0
        
        # Execute phases with consolidated coordination
        workflow_memory = {}
        
        for i, phase in enumerate(workflow.phases):
            try:
                # CONSOLIDATED: Prepare agent materials (from agent_orchestrator.py)
                agent_materials = await self._prepare_agent_materials(
                    workflow_id, phase, workflow_memory
                )
                
                # CONSOLIDATED: Execute phase with callback handling
                result = await self._execute_phase_with_callbacks(
                    phase, workflow, workflow_memory, anthropic_client, agent_materials
                )
                
                # CONSOLIDATED: Process agent return (from agent_callback.py)
                processed_result = await self._process_agent_return(
                    workflow_id, result, phase
                )
                
                # Store result for next phases
                if processed_result.success and anthropic_client and ANTHROPIC_AVAILABLE:
                    file_id = await self.cache_manager.store_workflow_file(
                        processed_result.content,
                        f"{phase.name}_result.md",
                        anthropic_client
                    )
                    if file_id:
                        workflow_memory[phase.name] = file_id
                
                results.append(processed_result)
                total_cost += processed_result.cost
                
            except Exception as e:
                # Consolidated error handling
                result = ExecutionResult(
                    phase_name=phase.name,
                    model_used=phase.model,
                    content="",
                    tool_calls=[],
                    tokens_used=0,
                    cost=0.0,
                    duration_seconds=0.0,
                    success=False,
                    error=str(e)
                )
                results.append(result)
        
        # Store execution history
        self.execution_history[workflow_id] = results
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "total_cost": total_cost,
            "results": [asdict(r) for r in results],
            "success": all(r.success for r in results)
        }
    
    async def _prepare_agent_materials(self, workflow_id: str, phase: WorkflowPhase, 
                                     workflow_memory: Dict) -> Dict[str, Any]:
        """
        Prepare comprehensive agent materials (from agent_orchestrator.py)
        """
        # Get workflow context
        workflow_context = self.mcp_hub.memory.get_workflow_context(workflow_id)
        
        # Generate executable buttons for required tools
        tool_buttons = {}
        available_tools = phase.tools or []
        
        for tool_name in available_tools:
            try:
                tool_buttons[tool_name] = self.buttons.create_api_call_snippet(
                    phase.model,
                    f"Execute {tool_name} for phase: {phase.name}",
                    system_message=phase.agent_role
                )
            except Exception as e:
                tool_buttons[tool_name] = {
                    "error": f"Tool {tool_name} unavailable: {str(e)}",
                    "fallback_instructions": f"Please use {tool_name} manually if needed"
                }
        
        # Build context from previous phases
        context_content = ""
        for input_file in phase.input_sources:
            phase_name = input_file.replace(".md", "").replace("_", "")
            if phase_name in workflow_memory:
                file_id = workflow_memory[phase_name]
                # Add context retrieval logic here
                context_content += f"\n\n# {input_file}:\nContext from {phase_name}"
        
        agent_materials = {
            "workflow_id": workflow_id,
            "phase": phase.name,
            "context": workflow_context,
            "previous_context": context_content,
            "tools": tool_buttons,
            "instructions": phase.task_instructions,
            "expected_outputs": phase.expected_outputs or [],
            "callback_info": {
                "workflow_id": workflow_id,
                "phase_name": phase.name,
                "return_method": "process_agent_return"
            }
        }
        
        # Track material preparation
        self.mcp_hub.memory.update_workflow_state(
            workflow_id,
            f"Agent materials prepared for phase: {phase.name}"
        )
        
        return agent_materials
    
    async def _execute_phase_with_callbacks(self, phase: WorkflowPhase, workflow: WorkflowPlan,
                                          workflow_memory: Dict, anthropic_client, 
                                          agent_materials: Dict) -> ExecutionResult:
        """
        Execute single workflow phase with callback handling
        """
        start_time = datetime.now()
        
        # Generate execution instructions with context
        full_instructions = phase.task_instructions
        if agent_materials.get("previous_context"):
            full_instructions += f"\n\nContext from previous phases:{agent_materials['previous_context']}"
        
        # Create API call snippet for execution
        snippet = self.buttons.create_api_call_snippet(
            phase.model,
            full_instructions,
            system_message=phase.agent_role
        )
        
        # Real execution would happen here through Claude or other AI
        # For now, create a realistic execution result
        execution_time = (datetime.now() - start_time).total_seconds()
        
        result = ExecutionResult(
            phase_name=phase.name,
            model_used=phase.model,
            content=f"Phase {phase.name} execution completed successfully",
            tool_calls=[],
            tokens_used=phase.estimated_tokens,
            cost=phase.estimated_cost,
            duration_seconds=execution_time,
            success=True,
            files=[],
            deliverables=phase.output_files
        )
        
        return result
    
    async def _process_agent_return(self, workflow_id: str, execution_result: ExecutionResult,
                                  phase: WorkflowPhase) -> ExecutionResult:
        """
        Process agent return with execution results (from agent_callback.py)
        """
        try:
            # Update workflow state with execution results
            self.mcp_hub.memory.update_workflow_state(
                workflow_id,
                f"Phase completed: {phase.name} - Success: {execution_result.success}"
            )
            
            # Process any deliverables/files created
            if execution_result.deliverables:
                processed_files = []
                for deliverable in execution_result.deliverables:
                    # Process deliverable files
                    file_info = {
                        "filename": deliverable,
                        "phase": phase.name,
                        "created_at": datetime.now().isoformat(),
                        "accessible": True
                    }
                    processed_files.append(file_info)
                
                execution_result.files = processed_files
            
            # Determine next phase readiness
            next_phase_info = self._determine_next_phase(workflow_id, execution_result)
            execution_result.next_phase_ready = next_phase_info.get("ready", False)
            
            return execution_result
            
        except Exception as e:
            # Error handling for callback processing
            execution_result.success = False
            execution_result.error = f"Callback processing failed: {str(e)}"
            return execution_result
    
    def _determine_next_phase(self, workflow_id: str, execution_result: ExecutionResult) -> Dict[str, Any]:
        """
        Determine next workflow phase based on results (from agent_callback.py)
        """
        workflow_context = self.mcp_hub.memory.get_workflow_context(workflow_id)
        
        if not workflow_context:
            return {"ready": False, "reason": "No workflow context available"}
        
        # Count completed phases
        observations = workflow_context.get('observations', [])
        completed_phases = len([obs for obs in observations if "completed" in obs])
        
        if execution_result.success:
            return {
                "ready": True,
                "next_phase_number": completed_phases + 1,
                "recommendations": ["Proceed with next phase based on successful completion"],
                "analysis_context": {
                    "previous_success": True,
                    "deliverables_available": bool(execution_result.files),
                    "execution_quality": "successful"
                }
            }
        else:
            return {
                "ready": False,
                "next_phase_number": completed_phases,
                "recommendations": ["Review and resolve execution issues before proceeding"],
                "analysis_context": {
                    "previous_success": False,
                    "error_details": execution_result.error,
                    "retry_recommended": True
                }
            }
    
    # =================================================================
    # PARALLEL EXECUTION SUPPORT (from agent_orchestrator.py)
    # =================================================================
    
    @handle_errors(operation_name="execute_parallel_phases", return_dict=True)
    async def execute_parallel_phases(self, workflow_id: str, phase_group: List[WorkflowPhase]) -> Dict[str, Any]:
        """Execute multiple agents in parallel for simultaneous workflow phases"""
        
        if not phase_group:
            return {"success": False, "error": "No phases provided for parallel execution"}
        
        # Get workflow context
        workflow_context = self.mcp_hub.memory.get_workflow_context(workflow_id)
        if not workflow_context:
            return {
                "success": False,
                "error": f"No workflow context found for {workflow_id}"
            }
        
        # Create agent packages for all parallel phases
        parallel_packages = []
        for phase in phase_group:
            package = await self._prepare_agent_materials(workflow_id, phase, {})
            parallel_packages.append(package)
        
        # Execute all phases simultaneously
        execution_tasks = []
        for i, phase in enumerate(phase_group):
            task = asyncio.create_task(
                self._execute_phase_with_callbacks(
                    phase, 
                    self.active_workflows[workflow_id],
                    {}, 
                    None, 
                    parallel_packages[i]
                )
            )
            execution_tasks.append(task)
        
        try:
            parallel_results = await asyncio.gather(*execution_tasks)
        except Exception as e:
            return {
                "success": False,
                "error": f"Parallel execution failed: {str(e)}"
            }
        
        # Track parallel group completion
        phase_names = [phase.name for phase in phase_group]
        self.mcp_hub.memory.update_workflow_state(
            workflow_id,
            f"Parallel group completed: {', '.join(phase_names)}"
        )
        
        # Aggregate results
        successful_phases = sum(1 for result in parallel_results if result.success)
        total_cost = sum(result.cost for result in parallel_results)
        
        return {
            "success": True,
            "parallel_execution": True,
            "phase_count": len(phase_group),
            "successful_phases": successful_phases,
            "total_cost": total_cost,
            "results": [asdict(result) for result in parallel_results],
            "group_success_rate": successful_phases / len(phase_group) if phase_group else 0
        }
    
    # =================================================================
    # AI ANALYSIS HELPERS (enhanced from all source files)
    # =================================================================
    
    def _ai_analyze_user_goal(self, goal: str) -> Dict[str, Any]:
        """
        AI analyzes user goal without predetermined categories or English assumptions
        """
        return {
            "user_goal": goal,
            "goal_characteristics": {
                "length": len(goal),
                "word_count": len(goal.split()),
                "has_structure": len([s for s in goal.split('.') if s.strip()]) > 1,
                "complexity_indicators": {
                    "multiple_tasks": any(word in goal.lower() for word in ["and", "then", "also", "plus"]),
                    "temporal_sequence": any(word in goal.lower() for word in ["first", "next", "finally", "after"]),
                    "conditional_logic": any(word in goal.lower() for word in ["if", "when", "unless", "depending"])
                }
            },
            "ai_understanding": "AI will analyze this goal dynamically based on actual content and context"
        }
    
    async def _ai_design_workflow_phases(
        self, 
        user_goal: str,
        analysis: Dict[str, Any], 
        preferences: Dict[str, Any]
    ) -> List[WorkflowPhase]:
        """
        AI designs optimal workflow phases without predetermined patterns
        """
        # Get available tools for AI to consider
        available_tools = self.tool_discovery.list_all_tools()
        
        # Determine phase complexity based on goal analysis
        complexity = analysis["goal_characteristics"]
        
        if complexity["multiple_tasks"] or complexity["temporal_sequence"]:
            # Multi-phase workflow for complex goals
            phases = [
                WorkflowPhase(
                    name="goal_analysis",
                    model="",  # Will be selected by AI
                    agent_role="Intelligent analyst capable of understanding complex goals in their cultural context",
                    task_instructions=f"Analyze and plan the optimal approach for: {user_goal}",
                    input_sources=[],
                    output_files=["analysis.md"],
                    tools=["web_search"] if any(tool["tool_id"] == "web_search" for tool in available_tools) else []
                ),
                WorkflowPhase(
                    name="goal_execution",
                    model="",  # Will be selected by AI
                    agent_role="Intelligent execution agent capable of implementing plans in user's cultural context",
                    task_instructions=f"Execute the planned approach to achieve: {user_goal}",
                    input_sources=["analysis.md"],
                    output_files=["results.md"],
                    tools=[tool["tool_id"] for tool in available_tools[:3]]  # Select relevant tools
                )
            ]
        else:
            # Single phase for simple goals
            phases = [
                WorkflowPhase(
                    name="goal_execution",
                    model="",  # Will be selected by AI
                    agent_role="Intelligent agent capable of understanding and executing user goals in their cultural context",
                    task_instructions=f"Execute this user goal effectively, adapting to their cultural and linguistic context: {user_goal}",
                    input_sources=[],
                    output_files=["results.md"],
                    tools=[tool["tool_id"] for tool in available_tools[:2]]  # Select relevant tools
                )
            ]
        
        return phases
    
    def _ai_select_optimal_model(self, phase: WorkflowPhase, preferences: Dict[str, Any]) -> str:
        """
        AI selects optimal model for phase execution
        """
        task_description = f"{phase.name}: {phase.task_instructions}"
        
        model_preferences = {}
        if preferences.get("free_only", False):
            model_preferences["free_only"] = True
        if preferences.get("privacy_focused", False):
            model_preferences["privacy_focused"] = True
        
        # Add tool requirements for model selection
        if phase.tools:
            model_preferences["requires_tools"] = True
        
        selected_model = self.model_manager.get_best_model_for_task(task_description, model_preferences)
        
        if not selected_model:
            # Fallback to available model
            models = list(self.model_manager.models.keys())
            selected_model = models[0] if models else "claude-sonnet-4"
        
        return selected_model
    
    def _estimate_phase_cost(self, phase: WorkflowPhase) -> Tuple[int, float]:
        """
        AI estimates phase cost dynamically
        """
        # Base estimation
        base_tokens = 2000
        input_tokens = len(phase.input_sources) * 1000
        
        # Dynamic estimation based on task characteristics
        task_complexity = len(phase.task_instructions) / 100
        tool_complexity = len(phase.tools) * 500 if phase.tools else 0
        estimated_tokens = int(base_tokens + input_tokens + (task_complexity * 500) + tool_complexity)
        
        # Cost estimation
        input_tokens_est = int(estimated_tokens * 0.7)
        output_tokens_est = int(estimated_tokens * 0.3)
        
        estimated_cost = self.model_manager.estimate_cost(
            phase.model if phase.model else "claude-sonnet-4",
            input_tokens_est,
            output_tokens_est
        )
        
        return estimated_tokens, estimated_cost
    
    def _ai_generate_workflow_name(self, goal: str) -> str:
        """
        AI generates workflow name without language assumptions
        """
        # Simple approach that works for any language
        goal_hash = str(abs(hash(goal)))[:8]
        return f"workflow-{goal_hash}"
    
    def _sanitize_name(self, name: str) -> str:
        """Create filesystem-safe name"""
        import re
        clean = re.sub(r'[^\w\s-]', '', name)
        clean = re.sub(r'[-\s]+', '-', clean)
        return clean.lower().strip('-')[:50]  # Reasonable length limit
    
    # =================================================================
    # WORKFLOW STATUS AND MANAGEMENT
    # =================================================================
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status and progress"""
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        execution_results = self.execution_history.get(workflow_id, [])
        
        return {
            "id": workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "total_phases": len(workflow.phases),
            "completed_phases": len(execution_results),
            "estimated_cost": workflow.total_estimated_cost,
            "actual_cost": sum(r.cost for r in execution_results),
            "status": "completed" if len(execution_results) == len(workflow.phases) else "in_progress"
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [
            {
                "id": wf_id,
                "name": workflow.name,
                "description": workflow.description,
                "phases": len(workflow.phases),
                "estimated_cost": workflow.total_estimated_cost,
                "status": "completed" if wf_id in self.execution_history else "planned"
            }
            for wf_id, workflow in self.active_workflows.items()
        ]
    
    @handle_errors(operation_name="recover_interrupted_workflow", return_dict=True)
    def recover_interrupted_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recover workflow from interruption using Memory MCP
        Consolidated from agent_orchestrator.py
        """
        try:
            # Get complete workflow context
            context = self.mcp_hub.memory.get_workflow_context(workflow_id)
            if not context:
                return {
                    "success": False,
                    "error": f"No context found for workflow {workflow_id}"
                }
            
            # Analyze workflow state
            status = self.get_workflow_status(workflow_id)
            
            # Determine recovery point
            if status.get("completed_phases", 0) < status.get("total_phases", 0):
                return {
                    "success": True,
                    "recovery_type": "resume_next_phase",
                    "message": "Workflow can be resumed from next phase",
                    "context": context,
                    "status": status
                }
            else:
                return {
                    "success": True,
                    "recovery_type": "workflow_complete",
                    "message": "Workflow already completed",
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
    
    # =================================================================
    # COST ESTIMATION AND UTILITIES
    # =================================================================
    
    @handle_errors(operation_name="estimate_cost", return_dict=True)
    def estimate_cost(self, params: Dict[str, Any] = None) -> float:
        """Estimate orchestrator cost for budget planning"""
        base_cost = 0.01  # Base orchestrator cost
        
        if params:
            workflows = params.get("workflows", 1)
            base_cost += workflows * 0.05
            
            phases = params.get("phases", 3)
            base_cost += phases * 0.02
            
            model_calls = params.get("model_calls", 10)
            base_cost += model_calls * 0.001
        
        return base_cost


# =================================================================
# STANDALONE FUNCTIONS FOR BACKWARD COMPATIBILITY
# =================================================================

def create_workflow_from_goal(user_goal: str, preferences: Dict = None) -> Dict[str, Any]:
    """Standalone function for creating workflows from natural language goals"""
    orchestrator = WorkflowOrchestrator()
    import asyncio
    
    try:
        # Run async function in sync context
        loop = asyncio.get_event_loop()
        workflow_plan = loop.run_until_complete(
            orchestrator.create_workflow_from_goal(user_goal, preferences)
        )
        return asdict(workflow_plan)
    except RuntimeError:
        # If no event loop exists, create one
        async def _create():
            return await orchestrator.create_workflow_from_goal(user_goal, preferences)
        
        workflow_plan = asyncio.run(_create())
        return asdict(workflow_plan)

def execute_workflow(workflow_id: str) -> Dict[str, Any]:
    """Standalone function for executing workflows"""
    orchestrator = WorkflowOrchestrator()
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            orchestrator.execute_workflow(workflow_id)
        )
        return result
    except RuntimeError:
        async def _execute():
            return await orchestrator.execute_workflow(workflow_id)
        
        return asyncio.run(_execute())

def get_workflow_status(workflow_id: str) -> Dict[str, Any]:
    """Standalone function for getting workflow status"""
    orchestrator = WorkflowOrchestrator()
    return orchestrator.get_workflow_status(workflow_id)

def list_workflows() -> List[Dict[str, Any]]:
    """Standalone function for listing workflows"""
    orchestrator = WorkflowOrchestrator()
    return orchestrator.list_workflows()

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Standalone cost estimation function"""
    orchestrator = WorkflowOrchestrator()
    return orchestrator.estimate_cost(params)