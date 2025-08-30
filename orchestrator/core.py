#!/usr/bin/env python3
"""
Orchestrator Core
The main brain that turns natural language into intelligent workflows
"""

import asyncio
import json
import uuid
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# MAO error handling
from .error_handling import handle_errors

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
from .cache.cache_system import CacheManager
from .mcp_hub import MCPIntegrationHub
from .agent_callback import AgentCallbackHandler

# Conditional import for code execution tool
try:
    from tools.code_execution.code_execution import CodeExecutionTool
    CODE_EXECUTION_AVAILABLE = True
except ImportError:
    CODE_EXECUTION_AVAILABLE = False
    CodeExecutionTool = None

@dataclass
class WorkflowPhase:
    """Individual phase in a workflow"""
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
    """Complete workflow plan"""
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
    🎭 THE MAESTRO!
    Conducts the symphony of AI models to accomplish any goal
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.model_manager = ModelManager(config_dir)
        self.buttons = ButtonManager(self.model_manager)
        self.tool_discovery = ToolManager(config_dir)
        self.cache_manager = CacheManager()
        self.protocol = self._load_protocol()
        
        # Initialize MCP Integration Hub
        self.mcp_hub = MCPIntegrationHub()
        
        # Initialize Tool Integration Framework
        self.agent_callback = AgentCallbackHandler()
        self.code_execution = CodeExecutionTool() if CODE_EXECUTION_AVAILABLE else None
        
        # Workflow state
        self.active_workflows: Dict[str, WorkflowPlan] = {}
        self.execution_history: Dict[str, List[ExecutionResult]] = {}
        
        # Store initialization info for UI layer to display
        stats = self.model_manager.get_stats()
        self.initialization_info = {
            "status": "initialized",
            "stats": stats,
            "message": f"Orchestrator ready with {stats['total_models']} models across {stats['total_providers']} providers"
        }
    
    def _load_protocol(self) -> Dict[str, Any]:
        """Load orchestration protocol from JSON config with fallback defaults"""
        protocol_path = self.config_dir / "orchestrator_protocol.json"
        
        # Try to load from JSON config first
        if protocol_path.exists():
            try:
                with open(protocol_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                # Fall back to defaults if JSON is invalid
                pass
        
        # Default protocol - no hardcoded workflow patterns, trust AI intelligence
        return {
            "cost_optimization": {
                "always_try_free_first": True,
                "max_cost_per_workflow": 1.00,
                "warn_at_cost": 0.50
            }
            # Removed hardcoded workflow_patterns - let AI design optimal workflows
        }
    
    async def create_workflow_from_goal(
        self, 
        user_goal: str, 
        preferences: Optional[Dict] = None
    ) -> WorkflowPlan:
        """
        THE MAGIC METHOD!
        Transform natural language goal into intelligent workflow
        """
        preferences = preferences or {}
        
        # 1. Check if we've seen this goal before (caching!)
        cached_analysis = self.cache_manager.get_cached_analysis(user_goal, "goal_analysis")
        if cached_analysis:
            analysis = json.loads(cached_analysis)
            analysis["_cache_hit"] = True
        else:
            # First time seeing this goal - analyze it
            analysis = self._analyze_goal(user_goal)
            # Cache the analysis for future use
            self.cache_manager.cache_content_analysis(
                user_goal, 
                json.dumps(analysis), 
                "goal_analysis"
            )
        
        # 2. Get suggested tools for this goal and model preferences
        budget_pref = preferences.get("budget", "balanced")
        tool_suggestions = self.tool_discovery.interactive_tool_selection(
            user_goal, 
            "claude-sonnet-4",  # We'll update this with actual model selection
            budget_pref
        )
        
        # Store tool suggestions for workflow plan
        tool_suggestions["_explanation_shown"] = True
        
        # 3. Design optimal workflow structure with tools
        phases = await self._design_workflow_phases(analysis, preferences, tool_suggestions)
        
        # 3. Select optimal models for each phase
        for phase in phases:
            phase.model = self._select_optimal_model(phase, preferences)
            phase.estimated_tokens, phase.estimated_cost = self._estimate_phase_cost(phase)
        
        # 4. Create workflow plan with tool costs
        total_phase_cost = sum(p.estimated_cost for p in phases)
        total_tool_cost = tool_suggestions.get("estimated_tool_cost", 0.0)
        
        workflow_plan = WorkflowPlan(
            id=str(uuid.uuid4()),
            name=self._generate_workflow_name(user_goal),
            description=user_goal,
            phases=phases,
            total_estimated_cost=total_phase_cost + total_tool_cost,
            estimated_duration_minutes=len(phases) * 3,  # Rough estimate
            workspace_dir=f"projects/{self._sanitize_name(user_goal)}"
        )
        
        # 5. Store for execution
        self.active_workflows[workflow_plan.id] = workflow_plan
        
        # 6. Initialize MCP workflow context
        self.mcp_hub.create_workflow(workflow_plan.id, user_goal)
        
        # Add creation metadata for UI layer
        workflow_plan.creation_info = {
            "phases_count": len(phases),
            "estimated_cost": workflow_plan.total_estimated_cost,
            "estimated_duration": workflow_plan.estimated_duration_minutes,
            "tool_suggestions": tool_suggestions,
            "analysis": analysis
        }
        
        return workflow_plan
    
    def _analyze_goal(self, goal: str) -> Dict[str, Any]:
        """
        Analyze user goal dynamically without hardcoded English assumptions
        Let AI understand the goal in user's language and cultural context
        """
        # Provide minimal structure - let AI fill in requirements dynamically
        analysis = {
            "user_goal": goal,
            "goal_length": len(goal),
            "word_count": len(goal.split()),
            "has_multiple_sentences": len([s for s in goal.split('.') if s.strip()]) > 1,
            "estimated_complexity": "medium",  # Default only
            "requires_tools": True,  # Assume tools needed - let tool manager decide which
            "output_format": "markdown"
        }
        
        # Simple complexity estimation based on goal structure, not content
        words = goal.split()
        if len(words) < 10:
            analysis["estimated_complexity"] = "low"
        elif len(words) > 30:
            analysis["estimated_complexity"] = "high"
        
        # Let AI determine everything else dynamically based on actual goal content
        # No English keyword detection - trust AI to understand goal in any language
        
        return analysis
    
    async def _design_workflow_phases(
        self, 
        analysis: Dict[str, Any], 
        preferences: Dict[str, Any],
        tool_suggestions: Dict[str, Any]
    ) -> List[WorkflowPhase]:
        """
        Let AI design optimal workflow phases dynamically based on actual user goal
        No predetermined patterns - trust AI intelligence to create appropriate workflow structure
        """
        phases = []
        selected_tools = tool_suggestions.get("core_tools", [])
        
        # Add tool-specific phases based on selected tools (if tools define phase structure)
        tool_phases = self._create_tool_phases(selected_tools, analysis)
        phases.extend(tool_phases)
        
        # For goals without tool-defined phases, create a single intelligent phase
        # Let AI determine the optimal approach without predetermined workflow patterns
        if not phases:
            phases.append(WorkflowPhase(
                name="intelligent_execution",
                model="",  # Will be selected by model manager
                agent_role="Expert agent capable of understanding and executing user goals dynamically",
                task_instructions=f"Analyze and execute the following goal using appropriate methods and tools: {analysis.get('user_goal', '')}",
                input_sources=[],
                output_files=["goal_execution_results.md"]
            ))
        
        # Let AI add additional phases if needed based on goal complexity
        # This allows for emergent workflow patterns that don't fit predetermined categories
        complexity = analysis.get("estimated_complexity", "medium")
        if complexity == "high" and len(phases) == 1:
            # For complex goals, suggest AI might want to break into planning + execution phases
            phases.insert(0, WorkflowPhase(
                name="planning_analysis",
                model="",
                agent_role="Strategic planning agent for complex goal analysis",
                task_instructions=f"Analyze and plan the optimal approach for: {analysis.get('user_goal', '')}",
                input_sources=[],
                output_files=["execution_plan.md"]
            ))
            # Update main phase to use planning input
            phases[1].input_sources = ["execution_plan.md"]
        
        return phases
    
    def _create_tool_phases(self, selected_tools: List[str], analysis: Dict[str, Any]) -> List[WorkflowPhase]:
        """Create workflow phases dynamically from tool registry configurations"""
        tool_phases = []
        
        for tool_id in selected_tools:
            # Get tool configuration from registry
            tool_config = self.tool_discovery.get_tool_details(tool_id)
            if not tool_config:
                continue
                
            # Get workflow phase configuration from tool registry
            phase_config = tool_config.get("workflow_phase", {})
            if not phase_config:
                # Skip tools that don't define workflow phases
                continue
            
            # Create dynamic workflow phase from JSON configuration
            # Tools define their own optimal integration patterns
            tool_phases.append(WorkflowPhase(
                name=phase_config.get("phase_name", f"{tool_id}_execution"),
                model=phase_config.get("preferred_model", ""),  # Will be selected later if empty
                agent_role=phase_config.get("agent_role", f"Agent specialized in using {tool_id} effectively"),
                task_instructions=phase_config.get("task_instructions", f"Apply {tool_id} capabilities to help achieve: {analysis.get('user_goal', 'the user goal')}"),
                input_sources=phase_config.get("input_sources", []),
                output_files=phase_config.get("output_files", [f"{tool_id}_results.md"])
            ))
            
        return tool_phases
    
    def _get_agent_role(self, task_type: str, domain: str) -> str:
        """Generate agent role description dynamically without hardcoded assumptions"""
        # Instead of hardcoded roles, provide behavioral guidance for AI to generate appropriate role
        # AI should create role description based on actual user goal and context
        return f"Expert agent capable of {task_type} tasks with deep understanding of user requirements"
    
    def _get_task_instructions(self, task_type: str, analysis: Dict[str, Any]) -> str:
        """Generate task instructions dynamically based on actual user goal"""
        # Instead of hardcoded instructions, provide guidance for AI to understand what to do
        # Let AI generate appropriate instructions based on user's actual goal and context
        
        user_goal = analysis.get('user_goal', '')
        complexity = analysis.get('estimated_complexity', 'medium')
        
        # Generate context-aware instructions without predetermined examples
        instruction = f"Execute the following user goal effectively: {user_goal}"
        
        # Add complexity guidance without hardcoded assumptions
        if complexity == "high":
            instruction += " Take time to thoroughly understand requirements and provide comprehensive results."
        elif complexity == "low":
            instruction += " Focus on clear, direct execution that addresses the core need."
        else:
            instruction += " Use professional judgment to determine the appropriate level of detail and approach."
        
        return instruction
    
    def _select_optimal_model(self, phase: WorkflowPhase, preferences: Dict[str, Any]) -> str:
        """🎯 Select the best model for a specific phase using dynamic analysis"""
        
        # Use phase task instructions as task description for dynamic model selection
        task_description = f"{phase.name}: {phase.task_instructions}"
        
        # Apply preferences
        model_preferences = {}
        if preferences.get("free_only", False):
            model_preferences["free_only"] = True
        if preferences.get("privacy_focused", False):
            model_preferences["privacy_focused"] = True
        
        # Use dynamic model selection based on task description
        selected_model = self.model_manager.get_best_model_for_task(task_description, model_preferences)
        
        if not selected_model:
            # Fallback to any available model
            models = list(self.model_manager.models.keys())
            selected_model = models[0] if models else "claude-sonnet-4"
        
        return selected_model
    
    def _estimate_phase_cost(self, phase: WorkflowPhase) -> Tuple[int, float]:
        """💰 Estimate tokens and cost for a phase"""
        
        # Rough estimation based on phase complexity
        base_tokens = 2000  # Base prompt and response
        
        # Add tokens for input sources
        input_tokens = len(phase.input_sources) * 1000  # Assume 1K tokens per input
        
        # Add tokens based on task complexity
        task_multiplier = {
            "research": 3.0,  # Lots of web search results
            "reasoning": 2.0,  # Detailed analysis
            "creative": 2.5,  # Rich content creation
            "coding": 3.0,    # Code + documentation
            "vision": 1.5     # Image analysis
        }
        
        task_type = "research"
        for task in task_multiplier.keys():
            if task in phase.name:
                task_type = task
                break
        
        estimated_tokens = int(base_tokens * task_multiplier.get(task_type, 2.0) + input_tokens)
        
        # Estimate cost (rough 70% input, 30% output split)
        input_tokens_est = int(estimated_tokens * 0.7)
        output_tokens_est = int(estimated_tokens * 0.3)
        
        estimated_cost = self.model_manager.estimate_cost(
            phase.model if phase.model else "claude-sonnet-4",
            input_tokens_est,
            output_tokens_est
        )
        
        return estimated_tokens, estimated_cost
    
    def _generate_workflow_name(self, goal: str) -> str:
        """Generate a clean workflow name"""
        # Extract key words and create a name
        words = re.findall(r'\b\w+\b', goal.lower())
        key_words = [w for w in words if len(w) > 3 and w not in ["and", "the", "for", "with", "that", "this"]]
        return "-".join(key_words[:4])  # Max 4 words
    
    def _sanitize_name(self, name: str) -> str:
        """🧹 Create filesystem-safe name"""
        # Remove special characters and spaces
        clean = re.sub(r'[^\w\s-]', '', name)
        clean = re.sub(r'[-\s]+', '-', clean)
        return clean.lower().strip('-')
    
    def _generate_phase_hash(self, phase: WorkflowPhase, goal: str) -> str:
        """🔐 Generate unique hash for phase configuration"""
        # Create unique identifier for this phase configuration
        phase_config = {
            "name": phase.name,
            "model": phase.model,
            "agent_role": phase.agent_role,
            "task_instructions": phase.task_instructions,
            "goal": goal
        }
        
        config_str = json.dumps(phase_config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:12]
    
    async def _execute_phase_with_caching(self, phase: WorkflowPhase, workflow: WorkflowPlan, 
                                         workflow_memory: Dict, anthropic_client) -> ExecutionResult:
        """Execute a single phase with context from Files API"""
        
        # Build context from previous phases using Files API
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
        
        # Generate execution snippet with context
        full_instructions = phase.task_instructions
        if context_content:
            full_instructions += f"\n\nContext from previous phases:{context_content}"
        
        snippet = self.buttons.create_api_call_snippet(
            phase.model,
            full_instructions,
            system_message=phase.agent_role
        )
        
        # For now, simulate execution (in real version, Claude 4 would execute it)
        content = f"[Phase {phase.name} executed with context from {len(phase.input_sources)} sources]"
        if context_content:
            content += f"\n\nGenerated response based on: {', '.join(phase.input_sources)}"
        
        return ExecutionResult(
            phase_name=phase.name,
            model_used=phase.model,
            content=content,
            tool_calls=[],
            tokens_used=phase.estimated_tokens,
            cost=phase.estimated_cost,
            duration_seconds=2.0,
            success=True
        )
    
    async def execute_workflow(self, workflow_id: str, anthropic_client=None) -> Dict[str, Any]:
        """
        Execute a complete workflow with hybrid caching
        """
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        results = []
        total_cost = 0.0
        
        # Store execution info for UI layer
        execution_info = {
            "workflow_name": workflow.name,
            "total_phases": len(workflow.phases),
            "status": "executing"
        }
        
        # Execute each phase with caching
        workflow_memory = {}
        
        for i, phase in enumerate(workflow.phases):
            # Store phase info for UI layer
            phase_info = {
                "phase_number": i+1,
                "total_phases": len(workflow.phases),
                "phase_name": phase.name,
                "model": phase.model,
                "estimated_cost": phase.estimated_cost
            }
            
            try:
                # Check if we have cached results for this exact phase configuration
                phase_config_hash = self._generate_phase_hash(phase, workflow.description)
                cached_result = self.cache_manager.get_cached_analysis(phase_config_hash, "phase_execution")
                
                if cached_result:
                    # Cache hit - add to phase info
                    phase_info["cache_hit"] = True
                    cached_data = json.loads(cached_result)
                    
                    result = ExecutionResult(
                        phase_name=phase.name,
                        model_used=phase.model,
                        content=cached_data["content"],
                        tool_calls=cached_data.get("tool_calls", []),
                        tokens_used=0,  # Cached = 0 tokens!
                        cost=0.0,  # Cached = $0!
                        duration_seconds=0.1,  # Near-instant
                        success=True
                    )
                else:
                    # Execute phase with fresh model call
                    result = await self._execute_phase_with_caching(
                        phase, workflow, workflow_memory, anthropic_client
                    )
                    
                    # Cache successful results for future use
                    if result.success:
                        cache_data = {
                            "content": result.content,
                            "tool_calls": result.tool_calls,
                            "model": result.model_used
                        }
                        self.cache_manager.cache_content_analysis(
                            phase_config_hash,
                            json.dumps(cache_data),
                            "phase_execution"
                        )
                
                # Store result in workflow memory for next phases
                if anthropic_client and result.success and ANTHROPIC_AVAILABLE:
                    workflow_id = f"{workflow.id}_{phase.name}"
                    file_id = await self.cache_manager.store_workflow_file(
                        result.content,
                        f"{phase.name}_result.md",
                        anthropic_client
                    )
                    if file_id:
                        workflow_memory[phase.name] = file_id
                
                results.append(result)
                total_cost += result.cost
                
                # Add completion info to phase data
                phase_info.update({
                    "completed": True,
                    "tokens_used": result.tokens_used,
                    "actual_cost": result.cost,
                    "success": result.success
                })
                
            except Exception as e:
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
                # Add failure info to phase data
                phase_info.update({
                    "completed": True,
                    "success": False,
                    "error": str(e)
                })
        
        # Store execution history
        self.execution_history[workflow_id] = results
        
        # Update execution info with completion data
        execution_info.update({
            "status": "completed",
            "total_cost": total_cost,
            "successful_phases": sum(1 for r in results if r.success),
            "total_phases": len(results)
        })
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "total_cost": total_cost,
            "results": [asdict(r) for r in results],
            "success": all(r.success for r in results)
        }
    
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
            
            cache_operations = params.get("cache_operations", 5)
            base_cost += cache_operations * 0.0001
        
        return base_cost


# Example usage and testing
async def main():
    """🎭 Demo the orchestrator in action!"""
    
    orchestrator = WorkflowOrchestrator()
    
    # Demo examples (UI layer handles display in production)
    
    # Example 1: Simple research task
    workflow1 = await orchestrator.create_workflow_from_goal(
        "Research the latest trends in renewable energy"
    )
    
    # Example 2: Complex multi-phase workflow
    workflow2 = await orchestrator.create_workflow_from_goal(
        "Research AI market trends, analyze the data, and create a comprehensive marketing strategy with visual content"
    )
    
    # Example 3: Cost-optimized workflow
    workflow3 = await orchestrator.create_workflow_from_goal(
        "Create a business plan for a new startup",
        preferences={"free_only": True}
    )
    
    # Return demo results for UI layer to display
    return {
        "demo_workflows": [
            {
                "name": workflow1.name,
                "phases": len(workflow1.phases),
                "estimated_cost": workflow1.total_estimated_cost,
                "phase_details": [{"name": p.name, "model": p.model} for p in workflow1.phases]
            },
            {
                "name": workflow2.name,
                "phases": len(workflow2.phases),
                "estimated_cost": workflow2.total_estimated_cost,
                "phase_details": [{"name": p.name, "model": p.model} for p in workflow2.phases]
            },
            {
                "name": workflow3.name,
                "phases": len(workflow3.phases),
                "estimated_cost": workflow3.total_estimated_cost,
                "phase_details": [{"name": p.name, "model": p.model} for p in workflow3.phases]
            }
        ]
    }


if __name__ == "__main__":
    asyncio.run(main())