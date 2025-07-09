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
        
        # Default protocol if file doesn't exist or is invalid
        return {
            "cost_optimization": {
                "always_try_free_first": True,
                "max_cost_per_workflow": 1.00,
                "warn_at_cost": 0.50
            },
            "workflow_patterns": {
                "research_then_create": ["research", "reasoning", "creative"],
                "analyze_and_recommend": ["research", "reasoning"],
                "multimedia_project": ["research", "creative", "vision"]
            }
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
        Analyze user goal to understand requirements
        """
        goal_lower = goal.lower()
        
        analysis = {
            "task_types": [],
            "complexity": "medium",
            "requires_tools": False,
            "requires_vision": False,
            "requires_web_access": False,
            "output_format": "markdown",
            "domain": "general"
        }
        
        # Detect task types
        if any(word in goal_lower for word in ["research", "analyze", "study", "investigate", "find", "look up"]):
            analysis["task_types"].append("research")
            analysis["requires_web_access"] = True
        
        if any(word in goal_lower for word in ["create", "write", "design", "draft", "compose", "generate"]):
            analysis["task_types"].append("creative")
        
        if any(word in goal_lower for word in ["strategy", "plan", "recommend", "decide", "evaluate", "assess"]):
            analysis["task_types"].append("reasoning")
        
        if any(word in goal_lower for word in ["code", "program", "develop", "build", "implement"]):
            analysis["task_types"].append("coding")
        
        if any(word in goal_lower for word in ["image", "photo", "visual", "picture", "graphic", "generate", "create", "paint", "draw", "art", "logo", "design"]):
            analysis["task_types"].append("vision")
            analysis["requires_vision"] = True
            
            # Special detection for image GENERATION (not just analysis)
            if any(word in goal_lower for word in ["generate", "create", "paint", "draw", "design", "make"]):
                analysis["task_types"].append("image_generation")
                analysis["requires_image_generation"] = True
        
        # Detect complexity
        if len(analysis["task_types"]) > 2 or any(word in goal_lower for word in ["comprehensive", "detailed", "thorough", "complete"]):
            analysis["complexity"] = "high"
        elif len(analysis["task_types"]) == 1 and any(word in goal_lower for word in ["simple", "quick", "brief"]):
            analysis["complexity"] = "low"
        
        # Detect domain
        domains = {
            "business": ["marketing", "strategy", "sales", "business", "company", "revenue"],
            "technology": ["ai", "software", "tech", "programming", "data", "algorithm"],
            "creative": ["design", "art", "creative", "brand", "content", "copy"],
            "research": ["study", "analysis", "research", "investigation", "report"]
        }
        
        for domain, keywords in domains.items():
            if any(keyword in goal_lower for keyword in keywords):
                analysis["domain"] = domain
                break
        
        return analysis
    
    async def _design_workflow_phases(
        self, 
        analysis: Dict[str, Any], 
        preferences: Dict[str, Any],
        tool_suggestions: Dict[str, Any]
    ) -> List[WorkflowPhase]:
        """
        Design optimal workflow structure with tools
        """
        phases = []
        task_types = analysis["task_types"]
        selected_tools = tool_suggestions.get("core_tools", [])
        
        # Add tool-specific phases based on selected tools
        tool_phases = self._create_tool_phases(selected_tools, analysis)
        phases.extend(tool_phases)
        
        # Single task type workflows
        if len(task_types) == 1:
            task_type = task_types[0]
            phases.append(WorkflowPhase(
                name=f"{task_type}_phase",
                model="",  # Will be selected later
                agent_role=self._get_agent_role(task_type, analysis["domain"]),
                task_instructions=self._get_task_instructions(task_type, analysis),
                input_sources=[],
                output_files=[f"{task_type}_result.md"]
            ))
        
        # Multi-task workflows
        else:
            # Research-driven workflows
            if "research" in task_types:
                phases.append(WorkflowPhase(
                    name="research_phase",
                    model="",
                    agent_role=self._get_agent_role("research", analysis["domain"]),
                    task_instructions=self._get_task_instructions("research", analysis),
                    input_sources=[],
                    output_files=["research_findings.md", "key_data.json"]
                ))
            
            # Analysis/reasoning phase
            if "reasoning" in task_types:
                input_sources = ["research_findings.md"] if "research" in task_types else []
                phases.append(WorkflowPhase(
                    name="analysis_phase",
                    model="",
                    agent_role=self._get_agent_role("reasoning", analysis["domain"]),
                    task_instructions=self._get_task_instructions("reasoning", analysis),
                    input_sources=input_sources,
                    output_files=["analysis_report.md", "recommendations.md"]
                ))
            
            # Creative/implementation phase
            if "creative" in task_types:
                input_sources = []
                if "research" in task_types:
                    input_sources.append("research_findings.md")
                if "reasoning" in task_types:
                    input_sources.append("analysis_report.md")
                
                phases.append(WorkflowPhase(
                    name="creative_phase",
                    model="",
                    agent_role=self._get_agent_role("creative", analysis["domain"]),
                    task_instructions=self._get_task_instructions("creative", analysis),
                    input_sources=input_sources,
                    output_files=["creative_output.md", "final_deliverable.md"]
                ))
            
            # Vision phase (if needed)
            if "vision" in task_types:
                phases.append(WorkflowPhase(
                    name="vision_phase",
                    model="",
                    agent_role="Visual content specialist with expertise in image analysis and generation",
                    task_instructions=self._get_task_instructions("vision", analysis),
                    input_sources=["creative_output.md"] if "creative" in task_types else [],
                    output_files=["visual_content.md", "image_specifications.json"]
                ))
            
            # Image Generation phase (if needed) 
            if "image_generation" in task_types:
                input_sources = []
                if "research" in task_types:
                    input_sources.append("research_findings.md")
                if "creative" in task_types:
                    input_sources.append("creative_output.md")
                if "vision" in task_types:
                    input_sources.append("visual_content.md")
                    
                phases.append(WorkflowPhase(
                    name="image_generation_phase",
                    model="",
                    agent_role="AI artist specialist with expertise in visual creation and DALL-E prompting",
                    task_instructions=self._get_task_instructions("image_generation", analysis),
                    input_sources=input_sources,
                    output_files=["generated_images.md", "image_prompts.json"]
                ))
            
            # Coding phase (if needed)
            if "coding" in task_types:
                input_sources = []
                if "reasoning" in task_types:
                    input_sources.append("analysis_report.md")
                
                phases.append(WorkflowPhase(
                    name="coding_phase",
                    model="",
                    agent_role=self._get_agent_role("coding", analysis["domain"]),
                    task_instructions=self._get_task_instructions("coding", analysis),
                    input_sources=input_sources,
                    output_files=["implementation.py", "technical_docs.md"]
                ))
        
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
            tool_phases.append(WorkflowPhase(
                name=phase_config.get("phase_name", f"{tool_id}_phase"),
                model=phase_config.get("preferred_model", ""),  # Will be selected later if empty
                agent_role=phase_config.get("agent_role", f"Specialist with {tool_id} capabilities"),
                task_instructions=phase_config.get("task_instructions", f"Use {tool_id} to complete the assigned task."),
                input_sources=phase_config.get("input_sources", []),
                output_files=phase_config.get("output_files", [f"{tool_id}_results.md"])
            ))
            
        return tool_phases
    
    def _get_agent_role(self, task_type: str, domain: str) -> str:
        """🎭 Generate appropriate agent role description"""
        
        roles = {
            "research": {
                "business": "Business intelligence analyst with expertise in market research and competitive analysis",
                "technology": "Technology research specialist with deep knowledge of AI and software trends",
                "creative": "Creative industry research expert with understanding of design and brand trends",
                "general": "Professional research analyst with broad domain expertise"
            },
            "reasoning": {
                "business": "Strategic business consultant with expertise in data-driven decision making",
                "technology": "Technical architect with strong analytical and problem-solving skills",
                "creative": "Creative strategist with analytical thinking and brand expertise",
                "general": "Strategic analyst with critical thinking and synthesis capabilities"
            },
            "creative": {
                "business": "Marketing strategist and content creator with business acumen",
                "technology": "Technical writer and content strategist with tech industry knowledge",
                "creative": "Creative director with expertise in content creation and brand development",
                "general": "Creative professional with strong writing and content development skills"
            },
            "coding": {
                "business": "Business application developer with understanding of commercial requirements",
                "technology": "Senior software engineer with expertise in modern development practices",
                "creative": "Creative technologist with skills in interactive and visual programming",
                "general": "Full-stack developer with broad technical expertise"
            }
        }
        
        return roles.get(task_type, {}).get(domain, f"Expert {task_type} specialist")
    
    def _get_task_instructions(self, task_type: str, analysis: Dict[str, Any]) -> str:
        """📋 Generate specific task instructions"""
        
        base_instructions = {
            "research": "Conduct comprehensive research using web search and analysis tools. Gather current, relevant information and organize findings clearly.",
            "reasoning": "Analyze the provided information critically. Identify patterns, draw insights, and develop strategic recommendations based on evidence.",
            "creative": "Create compelling, high-quality content that meets the specified requirements. Focus on clarity, engagement, and achieving the stated goals.",
            "coding": "Develop clean, efficient, and well-documented code that solves the specified problem. Follow best practices and include appropriate error handling.",
            "vision": "Analyze visual content and create detailed specifications for image generation or editing. Focus on composition, style, and technical requirements.",
            "image_generation": "Create detailed, artistic prompts for DALL-E 3 image generation. Focus on style, composition, lighting, and artistic techniques. Generate multiple creative variations."
        }
        
        instruction = base_instructions.get(task_type, "Complete the assigned task professionally and thoroughly.")
        
        # Add dynamic complexity modifiers based on analysis
        complexity = analysis.get("complexity", "medium")
        if complexity == "high":
            instruction += " This is a complex task requiring thorough analysis and detailed output."
        elif complexity == "low":
            instruction += " Focus on providing a clear, concise response that addresses the core requirements."
        
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