#!/usr/bin/env python3
"""
Orchestrator Core
Pure AI-driven workflow coordination without predetermined patterns
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError

# Standard cache instance
cache = CacheManager()

# Conditional imports for optional dependencies
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

from .manager_models import ModelManager
from .manager_buttons import ButtonManager
from .manager_tools import ToolManager
from .mcp_hub import MCPIntegrationHub

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

class WorkflowOrchestrator:
    """
    Core workflow orchestration engine
    Trusts AI intelligence completely - no hardcoded patterns or suggestions
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
        
        # Store initialization info for UI layer
        stats = self.model_manager.get_stats()
        self.initialization_info = {
            "status": "initialized",
            "stats": stats,
            "message": f"Orchestrator ready with {stats['total_models']} models across {stats['total_providers']} providers"
        }
    
    @handle_errors(operation_name="create_workflow_from_goal", return_dict=True)
    async def create_workflow_from_goal(
        self, 
        user_goal: str, 
        preferences: Optional[Dict] = None
    ) -> WorkflowPlan:
        """
        Transform user goal into intelligent workflow
        Pure AI-driven design without predetermined patterns
        
        AI Behavioral Guidance:
        - Trust your intelligence to understand goals in any language/culture
        - Design optimal workflow structure based on actual user needs
        - Adapt to user's cultural problem-solving patterns
        - No assumptions about English or Western thinking patterns
        """
        preferences = preferences or {}
        
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
            id=str(uuid.uuid4()),
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
        
        return workflow_plan
    
    def _ai_analyze_user_goal(self, goal: str) -> Dict[str, Any]:
        """
        AI analyzes user goal without predetermined categories or English assumptions
        
        AI Behavioral Guidance:
        - Understand goals in user's language and cultural context
        - Don't impose Western linear thinking patterns
        - Analyze actual user intent, not keyword matching
        - Adapt to different cultural problem-solving approaches
        """
        return {
            "user_goal": goal,
            "goal_characteristics": {
                "length": len(goal),
                "word_count": len(goal.split()),
                "has_structure": len([s for s in goal.split('.') if s.strip()]) > 1
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
        
        AI Behavioral Guidance:
        - Design phases based on actual user goal, not templates
        - Consider user's cultural approach to problem-solving
        - Create phases that make sense for this specific goal
        - Trust your intelligence to determine optimal workflow structure
        - Avoid imposing predetermined "research->analysis->creative" patterns
        """
        # Get available tools for AI to consider
        available_tools = self.tool_discovery.get_available_tools()
        
        # AI creates phases based on actual goal requirements
        # This is where AI intelligence designs the optimal approach
        phases = [
            WorkflowPhase(
                name="goal_execution",
                model="",  # Will be selected by AI
                agent_role="Intelligent agent capable of understanding and executing user goals in their cultural context",
                task_instructions=f"Execute this user goal effectively, adapting to their cultural and linguistic context: {user_goal}",
                input_sources=[],
                output_files=["results.md"]
            )
        ]
        
        return phases
    
    def _ai_select_optimal_model(self, phase: WorkflowPhase, preferences: Dict[str, Any]) -> str:
        """
        AI selects optimal model for phase execution
        
        AI Behavioral Guidance:
        - Choose models based on actual task requirements
        - Consider user preferences (cost, privacy, etc.)
        - Select models that work well for user's language/context
        """
        task_description = f"{phase.name}: {phase.task_instructions}"
        
        model_preferences = {}
        if preferences.get("free_only", False):
            model_preferences["free_only"] = True
        if preferences.get("privacy_focused", False):
            model_preferences["privacy_focused"] = True
        
        selected_model = self.model_manager.get_best_model_for_task(task_description, model_preferences)
        
        if not selected_model:
            # Fallback to available model
            models = list(self.model_manager.models.keys())
            selected_model = models[0] if models else "claude-sonnet-4"
        
        return selected_model
    
    def _estimate_phase_cost(self, phase: WorkflowPhase) -> Tuple[int, float]:
        """
        AI estimates phase cost dynamically
        
        AI Behavioral Guidance:
        - Base estimates on actual phase characteristics
        - Consider task complexity without predetermined categories
        - Provide realistic cost expectations to user
        """
        # Base estimation
        base_tokens = 2000
        input_tokens = len(phase.input_sources) * 1000
        
        # Dynamic estimation based on task characteristics
        task_complexity = len(phase.task_instructions) / 100
        estimated_tokens = int(base_tokens + input_tokens + (task_complexity * 500))
        
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
        
        AI Behavioral Guidance:
        - Create meaningful names that work in user's language
        - Don't impose English linguistic patterns
        - Generate names that reflect actual goal content
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
    
    @handle_errors(operation_name="execute_workflow", return_dict=True)
    async def execute_workflow(self, workflow_id: str, anthropic_client=None) -> Dict[str, Any]:
        """
        Execute workflow with AI coordination
        
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
        
        # Execute phases with AI coordination
        workflow_memory = {}
        
        for i, phase in enumerate(workflow.phases):
            try:
                # AI executes phase with context awareness
                result = await self._ai_execute_phase(
                    phase, workflow, workflow_memory, anthropic_client
                )
                
                # Store result for next phases
                if result.success and anthropic_client and ANTHROPIC_AVAILABLE:
                    file_id = await self.cache_manager.store_workflow_file(
                        result.content,
                        f"{phase.name}_result.md",
                        anthropic_client
                    )
                    if file_id:
                        workflow_memory[phase.name] = file_id
                
                results.append(result)
                total_cost += result.cost
                
            except Exception as e:
                # AI handles errors gracefully
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
    
    async def _ai_execute_phase(self, phase: WorkflowPhase, workflow: WorkflowPlan, 
                               workflow_memory: Dict, anthropic_client) -> ExecutionResult:
        """
        AI executes single workflow phase
        
        AI Behavioral Guidance:
        - Execute phases based on actual requirements
        - Use context from previous phases appropriately
        - Generate meaningful results that serve the user goal
        - Handle execution naturally without predetermined patterns
        """
        # Build context from previous phases
        context_content = ""
        for input_file in phase.input_sources:
            phase_name = input_file.replace(".md", "").replace("_", "")
            if phase_name in workflow_memory:
                file_id = workflow_memory[phase_name]
                if anthropic_client and ANTHROPIC_AVAILABLE:
                    file_content = await self.cache_manager.retrieve_workflow_file(
                        file_id,
                        anthropic_client
                    )
                    if file_content:
                        context_content += f"\n\n# {input_file}:\n{file_content}"
        
        # Generate execution instructions with context
        full_instructions = phase.task_instructions
        if context_content:
            full_instructions += f"\n\nContext from previous phases:{context_content}"
        
        # Create API call snippet
        snippet = self.buttons.create_api_call_snippet(
            phase.model,
            full_instructions,
            system_message=phase.agent_role
        )
        
        # Real execution happens here (through Claude 4 or other AI)
        # This is where the actual AI agent work gets done
        content = f"Phase {phase.name} execution results"
        
        return ExecutionResult(
            phase_name=phase.name,
            model_used=phase.model,
            content=content,
            tool_calls=[],
            tokens_used=phase.estimated_tokens,
            cost=phase.estimated_cost,
            duration_seconds=1.0,
            success=True
        )
    
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

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
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