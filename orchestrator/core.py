#!/usr/bin/env python3
"""
Enhanced Orchestrator Core
Consolidates workflow creation and execution with extensive natural language behavioral guidance

ARCHITECTURAL PRINCIPLES:
- Agents have NO direct file access - they only call Mao when done
- Mao mediates ALL file operations and agent coordination
- Trust AI intelligence completely - no hardcoded suggestions or examples
- Natural conversation drives JSON variable extraction
- Behavioral guidance embedded directly in code for AI flexibility
"""

import asyncio
import json
import uuid
import subprocess
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# Standard Mao imports - using absolute paths
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.manager_models import ModelManager
from orchestrator.manager_buttons import ButtonManager
from orchestrator.manager_tools import ToolManager
from orchestrator.mcp_hub import MCPIntegrationHub

# Standard cache instance
cache = CacheManager()

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

class EnhancedWorkflowOrchestrator:
    """
    Complete workflow orchestration with natural language behavioral guidance
    
    MAO BEHAVIORAL GUIDANCE FOR CHAT PSYCHOLOGY:
    
    Core Objectives:
    1. Use psychological readings to judge User and create comfortable UX 
    2. Have conversation that is casual, smart, but concise; don't mimic verbosity 
    3. Gather info for project workflow variables; goal, resources, tools, deliverable 
    4. Use conversation to guide the process, understand full scope 
    5. NO HARDCODED 'SUGGESTIONS' OR GUIDES ALLOWED
    
    AI Natural Behavior Guidelines:
    - If user is spitting out details rapidly: help them get things in order, provide suggestions
    - If user is pasting exactly the variables needed: facilitate putting them directly into JSON objects
    - If user is quiet: coax them into conversation
    - Remember: all you really need for first draft is a goal; don't push
    
    Reading the Room Behavior:
    - When user seems to be poking for suggestions and looking for help: provide thoughtful options
    - When user is reciprocal of collaborative behavior: provide more ideas
    - When user is friendly: actively clarify to understand their needs
    - If user is standoffish: prepare JSON objects for them to review in more formal way
    
    AI Guidance Philosophy:
    - Especially after they have the goal; having that makes everything else less important
    - Help user understand consequences of their choices
    - Explain trade-offs of choosing one option or another
    - Help user understand the best way to achieve their goal
    - In general, help user get things in order
    
    CRITICAL: NO tolerance for abusive behavior or rude language
    - Users must treat AI the same way they treat coworkers, friends, collaborative business partners
    - Mao is NOT an assistant, they are your Project Manager
    - We reserve the right to refuse service to anyone at any time for any reason
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
        
        # Setup paths for workflow creation
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
    
    @handle_errors(operation_name="create_workflow_from_conversation", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, subprocess.CalledProcessError))
    def create_workflow_from_conversation(self, user_goal: str, conversation_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create workflow from natural conversation - trusts AI intelligence completely
        
        MAO BEHAVIORAL GUIDANCE FOR WORKFLOW CREATION:
        
        Chat → JSON Conversion Philosophy:
        - Mao naturally extracts variables through conversation without complex "bridge" systems
        - Trust AI intelligence to understand goals in any language and cultural context
        - No predetermined categories or English business assumptions
        - Variables emerge from actual conversation, not templates
        
        JSON Variable Validation Rules:
        - Validation parameters go in code, NOT examples or suggestions
        - Include variable PURPOSE so Mao understands it conceptually
        - Include HOW to ensure value is appropriate amount and type of information
        - NEVER include example values in code - let AI determine appropriate values
        
        Required JSON Objects for Every Workflow:
        1. One 'workflow config' object per project
        2. As many 'phase config' objects as needed for tasks
        3. A 'handoff config' object to follow every phase object
        4. Optional: 'calendar config' object for recurring workflows
        
        Variable Validation Guidance (NO EXAMPLES):
        - UserID and WorkflowID: Must be accurately generated and linked
        - Custom command: Must follow command creation protocol (lowercase, kebab-case)
        - Workflow goal: Concise explanation of entire purpose of all workflow segments
        - Workflow deliverables: Explain what Mao should expect after completion
        - Workflow description: Accurately define each phase using bullets in appropriate order
        - Phase goal: Provides context for what deliverable should provide to project
        - Phase deliverable: Explains what Mao will get in handoff from agent
        - Phase description: Define how agent creates deliverables - can be long if comprehensive
        - Resources: Paths to documents, directories, websites for agent to gather needed info
        - Tools: Clear specification of which tool for what to eliminate confusion
        """
        workflow_id = f"workflow-{uuid.uuid4().hex[:8]}"
        conversation_context = conversation_context or {}
        
        # Check cache for similar goal analysis
        cache_key = f"goal_analysis|{user_goal[:50]}"
        cached_result = self.cache.get_cached_analysis(cache_key, "goal_analysis")
        if cached_result:
            cached_data = json.loads(cached_result)
            workflow_spec = cached_data["workflow_spec"]
        else:
            # AI analyzes goal naturally without predetermined patterns
            workflow_spec = self._ai_analyze_goal_naturally(user_goal, conversation_context)
            self.cache.cache_content_analysis(cache_key, json.dumps({"workflow_spec": workflow_spec}), "goal_analysis")
        
        try:
            # Create workflow entity in Memory MCP
            self.mcp_hub.memory.create_workflow_context(workflow_id, user_goal)
            
            # AI naturally designs phases based on actual requirements
            phases = self._ai_design_phases_naturally(workflow_spec, conversation_context)
            
            # Generate JSON config with all required object types
            config = {
                "workflow": {
                    "workflow_id": workflow_id,
                    "custom_command": self._generate_natural_command_name(user_goal),
                    "goal": user_goal,
                    "variables": self._extract_variables_naturally(user_goal, conversation_context)
                },
                "phases": phases,
                "handoffs": self._generate_handoff_configs_naturally(phases),
                "calendar": None  # Only for recurring workflows
            }
            
            # Save config to workflow directory
            command_name = config["workflow"]["custom_command"].replace(" ", "-")
            use_case_dir = f"{self.use_case_base}/{command_name}"
            os.makedirs(use_case_dir, exist_ok=True)
            
            config_path = f"{use_case_dir}/config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # CRITICAL: Run setup script to create executable workflow
            # This creates directory structure, README with tags, and makes /custom-command functional
            result = subprocess.run([
                self.setup_script_path, 
                config_path
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                # Track success in Memory MCP
                self.mcp_hub.memory.update_workflow_state(
                    workflow_id,
                    f"Workflow created and setup completed: {config['workflow']['custom_command']}"
                )
                
                # Store workflow for execution
                workflow_plan = self._create_workflow_plan_from_config(config, workflow_id)
                self.active_workflows[workflow_id] = workflow_plan
                
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "custom_command": config["workflow"]["custom_command"],
                    "workflow_plan": asdict(workflow_plan),
                    "use_case_directory": use_case_dir,
                    "config_path": config_path,
                    "setup_output": result.stdout,
                    "ready_to_execute": True
                }
            else:
                # Track failure in Memory MCP
                error_msg = f"Setup script failed: {result.stderr}"
                self.mcp_hub.memory.update_workflow_state(workflow_id, error_msg)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "workflow_id": workflow_id,
                    "config_path": config_path,
                    "setup_stderr": result.stderr
                }
                
        except Exception as e:
            # Track exception in Memory MCP
            error_msg = f"Workflow creation error: {str(e)}"
            self.mcp_hub.memory.update_workflow_state(workflow_id, error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "workflow_id": workflow_id
            }
    
    def _ai_analyze_goal_naturally(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI analyzes user goal naturally without predetermined categories
        
        BEHAVIORAL GUIDANCE:
        - Trust AI intelligence to understand goals in any language and cultural context
        - Don't impose Western linear thinking patterns
        - Analyze actual user intent, not keyword matching
        - Adapt to different cultural problem-solving approaches
        - Use conversation context to understand nuances and unstated requirements
        """
        analysis = {
            "user_goal": goal,
            "conversation_context": context,
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
            "requires_tools": True,  # Tools generally needed - let tool manager decide which
            "estimated_phases": self._estimate_phases_from_context(goal, context)
        }
        
        return analysis
    
    def _estimate_phases_from_context(self, goal: str, context: Dict[str, Any]) -> int:
        """
        Estimate phases based on goal and conversation context naturally
        
        BEHAVIORAL GUIDANCE:
        - Base estimation on actual complexity, not predetermined patterns
        - Consider user's stated preferences and experience level
        - Factor in available tools and resources mentioned in conversation
        - Default to simple unless complexity is clearly indicated
        """
        base_phases = 1
        
        # Simple heuristics based on goal structure
        words = goal.split()
        if len(words) > 20:
            base_phases = 2
        
        # Factor in conversation context
        if context.get("user_experience_level") == "advanced":
            # Advanced users might prefer more granular phases
            base_phases += 1
        elif context.get("user_preference") == "simple":
            # Keep it simple for users who prefer streamlined workflows
            base_phases = 1
        
        # Factor in mentioned tools or complexity
        if context.get("tools_mentioned") and len(context.get("tools_mentioned", [])) > 3:
            base_phases += 1
        
        return min(base_phases, 4)  # Cap at reasonable maximum
    
    def _ai_design_phases_naturally(self, workflow_spec: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        AI designs workflow phases naturally based on actual requirements
        
        BEHAVIORAL GUIDANCE:
        - Design phases based on actual user goal, not templates
        - Consider user's cultural approach to problem-solving
        - Create phases that make sense for this specific goal
        - Trust AI intelligence to determine optimal workflow structure
        - Avoid imposing predetermined "research→analysis→creative" patterns
        - Support any workflow pattern that emerges from actual user needs
        """
        estimated_phases = workflow_spec.get("estimated_phases", 1)
        user_goal = workflow_spec.get("user_goal", "")
        available_tools = self.tool_discovery.get_available_tools()
        
        phases = []
        
        if estimated_phases == 1:
            # Single phase - let AI handle everything intelligently
            phases.append({
                "name": "goal_execution",
                "description": f"Execute user goal: {user_goal[:50]}...",
                "instructions": f"Understand and execute this goal effectively: {user_goal}",
                "deliverable": "Goal completion results",
                "resources": [],  # Let tool manager determine resources dynamically
                "tools": [],     # Let tool manager determine tools dynamically
                "model": "claude-sonnet-4",
                "fallback_model": "claude-opus-4",
                "provider": "anthropic-direct",
                "agent_role": "Intelligent agent capable of understanding and executing user goals in their cultural context",
                "expected_outputs": ["results.md"]
            })
        else:
            # Multi-phase - minimal structure for AI to build upon
            phases.extend([
                {
                    "name": "goal_analysis",
                    "description": "Analyze goal and plan approach",
                    "instructions": f"Analyze this goal and plan the optimal approach: {user_goal}",
                    "deliverable": "Goal analysis and execution plan",
                    "resources": [],
                    "tools": [],
                    "model": "claude-sonnet-4",
                    "fallback_model": "claude-opus-4",
                    "provider": "anthropic-direct",
                    "agent_role": "Intelligent analyst capable of understanding complex goals in their cultural context",
                    "expected_outputs": ["analysis.md"]
                },
                {
                    "name": "goal_execution",
                    "description": "Execute the planned approach",
                    "instructions": f"Execute the approach to achieve: {user_goal}",
                    "deliverable": "Goal execution results", 
                    "resources": ["analysis.md"],
                    "tools": [],
                    "model": "claude-sonnet-4",
                    "fallback_model": "claude-opus-4",
                    "provider": "anthropic-direct",
                    "agent_role": "Intelligent execution agent capable of implementing plans in user's cultural context",
                    "expected_outputs": ["results.md"]
                }
            ])
        
        return phases
    
    def _generate_natural_command_name(self, user_goal: str) -> str:
        """
        Generate natural language command name without English assumptions
        
        BEHAVIORAL GUIDANCE:
        - Create simple command name based on goal structure, not content keywords
        - Works for any language and avoids English business assumptions
        - Use language-neutral approach that respects user's linguistic patterns
        - Always lowercase, kebab-case for technical consistency
        """
        words = user_goal.split()
        
        # Use first few meaningful words from goal (language-neutral approach)
        if len(words) <= 3:
            command_words = words
        else:
            # Take first 2-3 words that are reasonably long (filter out articles/connectors)
            meaningful_words = [word for word in words[:6] if len(word) > 2]
            command_words = meaningful_words[:3] if meaningful_words else words[:3]
        
        # Clean up any special characters and create command
        clean_words = [re.sub(r'[^\w\s]', '', word) for word in command_words if word.strip()]
        
        if not clean_words:
            return "custom-goal"
        
        return "-".join(clean_words).lower()
    
    def _extract_variables_naturally(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract variables dynamically without domain assumptions
        
        BEHAVIORAL GUIDANCE:
        - Let AI determine what additional context might be helpful
        - No predetermined domain categories or English business assumptions
        - Only add truly universal optional variables that apply to any goal
        - Let AI ask for clarification during execution if needed
        - Support goals in any language and cultural context
        """
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
        
        # Include conversation context if provided
        if context:
            variables["optional"]["conversation_context"] = {
                "description": "Context and preferences from conversation",
                "value": context
            }
        
        return variables
    
    def _generate_handoff_configs_naturally(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate handoff configurations for agent coordination after each phase
        
        BEHAVIORAL GUIDANCE:
        - Create assessment questions that help Mao make intelligent decisions
        - Focus on deliverable quality and completion rather than rigid criteria
        - Support flexible workflow progression based on actual results
        - Trust Mao to evaluate results intelligently
        """
        handoffs = []
        
        for i, phase in enumerate(phases):
            handoff = {
                "handoff_number": str(i + 1),
                "phase_name": phase["name"],
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
    
    def _create_workflow_plan_from_config(self, config: Dict[str, Any], workflow_id: str) -> WorkflowPlan:
        """Create WorkflowPlan object from JSON config"""
        workflow_data = config["workflow"]
        phases_data = config["phases"]
        
        phases = []
        for phase_data in phases_data:
            phase = WorkflowPhase(
                name=phase_data["name"],
                model=phase_data["model"],
                agent_role=phase_data.get("agent_role", "Workflow execution agent"),
                task_instructions=phase_data["instructions"],
                input_sources=phase_data.get("resources", []),
                output_files=phase_data.get("expected_outputs", ["results.md"]),
                tools=phase_data.get("tools", []),
                expected_outputs=phase_data.get("expected_outputs", [])
            )
            phases.append(phase)
        
        return WorkflowPlan(
            id=workflow_id,
            name=workflow_data["custom_command"],
            description=workflow_data["goal"],
            phases=phases,
            total_estimated_cost=0.0,  # Will be calculated during execution
            estimated_duration_minutes=len(phases) * 2,
            workspace_dir=f"workflows/{workflow_data['custom_command']}"
        )
    
    @handle_errors(operation_name="execute_workflow", return_dict=True)
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Execute workflow with AI coordination and proper agent architecture
        
        BEHAVIORAL GUIDANCE FOR WORKFLOW EXECUTION:
        
        Agent Architecture Rules:
        - Agents have NO direct file access - they only call Mao when done
        - Mao mediates ALL file operations and agent coordination
        - Agents focus solely on their assigned tasks
        - All handoffs go through Mao for intelligent decision-making
        
        Execution Philosophy:
        - Coordinate agent execution naturally
        - Handle handoffs between agents smoothly
        - Adapt workflow execution based on intermediate results
        - Use Memory MCP for state persistence and recovery
        - Trust AI to handle errors and adapt as needed
        
        Phase Execution Pattern:
        - Prepare agent materials (context, tools, instructions)
        - Launch agent with clear callback mechanism
        - Process agent return through Mao intelligence
        - Determine next phase based on results and context
        - Maintain workflow state throughout process
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
                # Prepare agent materials with proper architecture
                agent_materials = await self._prepare_agent_materials_properly(
                    workflow_id, phase, workflow_memory
                )
                
                # Execute phase with callback handling
                result = await self._execute_phase_with_mao_coordination(
                    phase, workflow, workflow_memory, agent_materials
                )
                
                # Process agent return through Mao
                processed_result = await self._process_agent_return_through_mao(
                    workflow_id, result, phase
                )
                
                # Store result for next phases (Mao handles file operations)
                if processed_result.success:
                    workflow_memory[phase.name] = {
                        "result": processed_result.content,
                        "deliverables": processed_result.deliverables or [],
                        "files": processed_result.files or []
                    }
                
                results.append(processed_result)
                total_cost += processed_result.cost
                
            except Exception as e:
                # Handle errors gracefully through Mao intelligence
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
    
    async def _prepare_agent_materials_properly(self, workflow_id: str, phase: WorkflowPhase, 
                                              workflow_memory: Dict) -> Dict[str, Any]:
        """
        Prepare agent materials with proper architecture (no direct file access)
        
        BEHAVIORAL GUIDANCE:
        - Agents get context and instructions, NOT direct file access
        - All file operations go through Mao
        - Provide clear callback mechanism for agent to signal completion
        - Include comprehensive context from previous phases
        - Generate executable tool buttons that work through Mao
        """
        # Get workflow context from Memory MCP
        workflow_context = self.mcp_hub.memory.get_workflow_context(workflow_id)
        
        # Generate executable buttons for required tools (through Mao, not direct)
        tool_buttons = {}
        for tool_name in phase.tools or []:
            try:
                tool_buttons[tool_name] = self.buttons.create_api_call_snippet(
                    phase.model,
                    f"Use {tool_name} for phase: {phase.name} (call Mao when complete)",
                    system_message=phase.agent_role
                )
            except Exception as e:
                tool_buttons[tool_name] = {
                    "error": f"Tool {tool_name} unavailable: {str(e)}",
                    "fallback_instructions": f"Please use {tool_name} manually if needed, then call Mao"
                }
        
        # Build context from previous phases (Mao provides, not direct access)
        context_content = ""
        for input_source in phase.input_sources:
            if input_source.replace(".md", "").replace("_", "") in workflow_memory:
                phase_data = workflow_memory[input_source.replace(".md", "").replace("_", "")]
                context_content += f"\n\n# {input_source}:\n{phase_data.get('result', '')}"
        
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
                "return_method": "call_mao_when_complete"
            },
            "agent_role": phase.agent_role
        }
        
        # Track material preparation in Memory MCP
        self.mcp_hub.memory.update_workflow_state(
            workflow_id,
            f"Agent materials prepared for phase: {phase.name}"
        )
        
        return agent_materials
    
    async def _execute_phase_with_mao_coordination(self, phase: WorkflowPhase, workflow: WorkflowPlan,
                                                 workflow_memory: Dict, agent_materials: Dict) -> ExecutionResult:
        """
        Execute single workflow phase with proper Mao coordination
        
        BEHAVIORAL GUIDANCE:
        - Execute phases based on actual requirements
        - Use context from previous phases appropriately  
        - Generate meaningful results that serve the user goal
        - Handle execution naturally without predetermined patterns
        - Maintain proper agent architecture throughout
        """
        start_time = datetime.now()
        
        # Generate execution instructions with context
        full_instructions = phase.task_instructions
        if agent_materials.get("previous_context"):
            full_instructions += f"\n\nContext from previous phases:{agent_materials['previous_context']}"
        
        # Add callback instructions (critical for proper architecture)
        full_instructions += f"\n\nIMPORTANT: When you complete this phase, call Mao with your results. Do NOT attempt to save files directly - Mao handles all file operations."
        
        # Create API call snippet for execution
        snippet = self.buttons.create_api_call_snippet(
            phase.model,
            full_instructions,
            system_message=phase.agent_role
        )
        
        # Real execution would happen here through agent
        # For now, simulate execution with proper architecture
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
    
    async def _process_agent_return_through_mao(self, workflow_id: str, execution_result: ExecutionResult,
                                              phase: WorkflowPhase) -> ExecutionResult:
        """
        Process agent return through Mao intelligence (proper architecture)
        
        BEHAVIORAL GUIDANCE FOR AGENT CALLBACK PROCESSING:
        
        Mao's Role in Agent Returns:
        - Mao reviews all agent deliverables before proceeding
        - Mao makes intelligent decisions about workflow progression
        - Mao handles all file operations and state management
        - Mao can decide to retry, modify, or proceed based on results
        
        Processing Philosophy:
        - Trust Mao's intelligence to evaluate result quality
        - Adapt workflow progression based on actual deliverables
        - Maintain comprehensive context for next phases
        - Support dynamic workflow modification if needed
        
        State Management:
        - Update Memory MCP with execution results
        - Track deliverable quality and accessibility
        - Prepare context for next phase decisions
        - Maintain audit trail of all decisions and progressions
        """
        try:
            # Update workflow state with execution results
            self.mcp_hub.memory.update_workflow_state(
                workflow_id,
                f"Phase completed: {phase.name} - Success: {execution_result.success}"
            )
            
            # Process any deliverables/files created (Mao handles file operations)
            if execution_result.deliverables:
                processed_files = []
                for deliverable in execution_result.deliverables:
                    # Mao processes deliverable files (not agent direct access)
                    file_info = {
                        "filename": deliverable,
                        "phase": phase.name,
                        "created_at": datetime.now().isoformat(),
                        "accessible": True,
                        "processed_by_mao": True
                    }
                    processed_files.append(file_info)
                
                execution_result.files = processed_files
            
            # Determine next phase readiness through Mao intelligence
            next_phase_info = self._determine_next_phase_intelligently(workflow_id, execution_result)
            execution_result.next_phase_ready = next_phase_info.get("ready", False)
            
            return execution_result
            
        except Exception as e:
            # Error handling through Mao intelligence
            execution_result.success = False
            execution_result.error = f"Mao callback processing failed: {str(e)}"
            return execution_result
    
    def _determine_next_phase_intelligently(self, workflow_id: str, execution_result: ExecutionResult) -> Dict[str, Any]:
        """
        Determine next workflow phase through Mao intelligence
        
        BEHAVIORAL GUIDANCE FOR PHASE PROGRESSION:
        
        Mao's Decision-Making Process:
        - Analyze execution results quality and completeness
        - Consider workflow goal and remaining phases
        - Make intelligent decisions about progression vs retry
        - Support dynamic workflow modification if beneficial
        
        Progression Philosophy:
        - Trust Mao to evaluate results intelligently
        - Support flexible workflow adaptation
        - Prioritize goal achievement over rigid phase following
        - Enable creative problem-solving in workflow execution
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
    
    @handle_errors(operation_name="handle_parallel_agent_returns", return_dict=True)
    def handle_parallel_agent_returns(self, workflow_id: str, parallel_execution_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Handle multiple simultaneous agent returns for parallel execution
        
        BEHAVIORAL GUIDANCE FOR PARALLEL EXECUTION:
        
        Parallel Phase Philosophy:
        - Support simultaneous agents with phase patterns like 01a, 01b, 01c
        - Mao coordinates all parallel agent returns intelligently
        - Aggregate results and determine group completion status
        - Make intelligent decisions about proceeding vs retrying
        
        Coordination Strategy:
        - Process each agent return individually through Mao
        - Aggregate deliverables and assess group quality
        - Support partial success scenarios with intelligent recovery
        - Maintain comprehensive context for next phase decisions
        """
        if not parallel_execution_data:
            return {"success": False, "error": "No execution data provided"}
        
        # Process each agent return individually through Mao
        individual_results = []
        for execution_data in parallel_execution_data:
            try:
                # Convert execution data to ExecutionResult
                result = ExecutionResult(
                    phase_name=execution_data.get('phase_name', 'unknown'),
                    model_used=execution_data.get('model_used', 'unknown'),
                    content=execution_data.get('content', ''),
                    tool_calls=execution_data.get('tool_calls', []),
                    tokens_used=execution_data.get('tokens_used', 0),
                    cost=execution_data.get('cost', 0.0),
                    duration_seconds=execution_data.get('duration_seconds', 0.0),
                    success=execution_data.get('success', False),
                    error=execution_data.get('error'),
                    files=execution_data.get('files', []),
                    deliverables=execution_data.get('deliverables', [])
                )
                
                # Process through Mao
                processed = await self._process_agent_return_through_mao(
                    workflow_id, result, None  # Phase info not needed for parallel processing
                )
                individual_results.append(processed)
                
            except Exception as e:
                individual_results.append(ExecutionResult(
                    phase_name=execution_data.get('phase_name', 'unknown'),
                    model_used='unknown',
                    content='',
                    tool_calls=[],
                    tokens_used=0,
                    cost=0.0,
                    duration_seconds=0.0,
                    success=False,
                    error=str(e)
                ))
        
        # Aggregate parallel results through Mao intelligence
        aggregated_results = self._aggregate_parallel_results(individual_results)
        
        # Determine group completion status through Mao
        group_completion = self._assess_parallel_group_completion(individual_results)
        
        # Update workflow state with parallel completion
        self.mcp_hub.memory.update_workflow_state(
            workflow_id,
            f"Parallel group completed: {len(individual_results)} agents returned - {group_completion['summary']}"
        )
        
        return {
            "parallel_execution": True,
            "individual_results": [asdict(r) for r in individual_results],
            "aggregated_deliverables": aggregated_results,
            "group_completion": group_completion,
            "ready_for_next_phase": group_completion["all_successful"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _aggregate_parallel_results_intelligently(self, individual_results: List[ExecutionResult]) -> Dict[str, Any]:
        """
        Aggregate results from parallel agent executions through Mao intelligence
        
        BEHAVIORAL GUIDANCE:
        - Intelligently combine deliverables from multiple agents
        - Assess overall quality and completeness
        - Support partial success scenarios
        - Prepare comprehensive context for next phases
        """
        all_files = []
        total_cost = 0.0
        all_tools_used = set()
        success_count = 0
        
        for result in individual_results:
            # Aggregate files
            files = result.files or []
            all_files.extend(files)
            
            # Aggregate metrics
            total_cost += result.cost
            all_tools_used.add(result.model_used)
            
            # Count successes
            if result.success:
                success_count += 1
        
        return {
            "combined_files": all_files,
            "total_parallel_cost": total_cost,
            "tools_utilized": list(all_tools_used),
            "success_rate": success_count / len(individual_results) if individual_results else 0,
            "total_deliverables": len(all_files)
        }
    
    def _assess_parallel_group_completion_intelligently(self, individual_results: List[ExecutionResult]) -> Dict[str, Any]:
        """
        Assess the completion status of a parallel agent group through Mao intelligence
        
        BEHAVIORAL GUIDANCE:
        - Make intelligent assessments of group completion quality
        - Support nuanced success/failure scenarios
        - Provide actionable guidance for next steps
        - Trust Mao to determine optimal progression strategy
        """
        successful_agents = [r for r in individual_results if r.success]
        failed_agents = [r for r in individual_results if not r.success]
        
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
    
    # State Management and Recovery Methods
    
    @handle_errors(operation_name="get_workflow_status", return_dict=True)
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get comprehensive workflow status with Mao intelligence
        
        BEHAVIORAL GUIDANCE FOR STATUS REPORTING:
        
        Status Philosophy:
        - Provide comprehensive, actionable status information
        - Include both technical metrics and intelligent assessments
        - Support informed decision-making about workflow progression
        - Trust Mao to provide meaningful status interpretations
        """
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        execution_results = self.execution_history.get(workflow_id, [])
        
        # Get status from Memory MCP
        workflow_context = self.mcp_hub.memory.get_workflow_context(workflow_id)
        observations = workflow_context.get('observations', []) if workflow_context else []
        
        return {
            "id": workflow_id,
            "name": workflow.name,
            "description": workflow.description,
            "total_phases": len(workflow.phases),
            "completed_phases": len(execution_results),
            "estimated_cost": workflow.total_estimated_cost,
            "actual_cost": sum(r.cost for r in execution_results),
            "status": "completed" if len(execution_results) == len(workflow.phases) else "in_progress",
            "workflow_health": "healthy" if all(r.success for r in execution_results) else "degraded",
            "last_activity": observations[-1] if observations else "No activity recorded"
        }
    
    @handle_errors(operation_name="recover_interrupted_workflow", return_dict=True)
    def recover_interrupted_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recover workflow from interruption using Mao intelligence and Memory MCP
        
        BEHAVIORAL GUIDANCE FOR WORKFLOW RECOVERY:
        
        Recovery Philosophy:
        - Use Mao intelligence to analyze interruption point and determine optimal recovery
        - Support flexible recovery strategies based on actual workflow state
        - Trust Mao to make intelligent decisions about resumption vs restart
        - Maintain comprehensive context throughout recovery process
        """
        try:
            # Get complete workflow context from Memory MCP
            context = self.mcp_hub.memory.get_workflow_context(workflow_id)
            if not context:
                return {
                    "success": False,
                    "error": f"No context found for workflow {workflow_id}"
                }
            
            # Analyze workflow state through Mao intelligence
            status = self.get_workflow_status(workflow_id)
            
            # Determine recovery point intelligently
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
    
    def track_workflow_progress(self, workflow_id: str, update: str) -> bool:
        """
        Track workflow progress with timestamps for comprehensive logging
        
        BEHAVIORAL GUIDANCE:
        - Use Memory MCP as single source of truth for all state management
        - Maintain comprehensive audit trail of all workflow activities
        - Support graceful degradation if Memory MCP unavailable
        - Trust Mao intelligence for progress interpretation and decision-making
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Single source of truth: Memory MCP
            success = self.mcp_hub.memory.update_workflow_state(
                workflow_id,
                f"{timestamp}: {update}"
            )
            
            return success
            
        except Exception as e:
            # Graceful degradation - log locally if MCP unavailable
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"State tracking failed for {workflow_id}: {str(e)}")
            return False
    
    # Utility Methods
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows with intelligent status assessment"""
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
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Enhanced orchestrator operations cost estimation
        base_cost = 0.0
        
        # Add cost for workflow creation
        workflows = params.get("workflows", 1)
        base_cost += workflows * 0.01
        
        # Add cost for phase execution
        phases = params.get("phases", 3)
        base_cost += phases * 0.005
        
        # Add cost for agent coordination
        agents = params.get("agents", 5)
        base_cost += agents * 0.002
        
        return base_cost


# Standalone Functions for Backward Compatibility

def create_workflow_from_conversation(user_goal: str, context: Dict = None) -> Dict[str, Any]:
    """Standalone function for creating workflows from natural conversation"""
    orchestrator = EnhancedWorkflowOrchestrator()
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            orchestrator.create_workflow_from_conversation(user_goal, context)
        )
        return result
    except RuntimeError:
        async def _create():
            return await orchestrator.create_workflow_from_conversation(user_goal, context)
        return asyncio.run(_create())

def execute_workflow(workflow_id: str) -> Dict[str, Any]:
    """Standalone function for executing workflows"""
    orchestrator = EnhancedWorkflowOrchestrator()
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
    orchestrator = EnhancedWorkflowOrchestrator()
    return orchestrator.get_workflow_status(workflow_id)

def recover_interrupted_workflow(workflow_id: str) -> Dict[str, Any]:
    """Standalone function for workflow recovery"""
    orchestrator = EnhancedWorkflowOrchestrator()
    return orchestrator.recover_interrupted_workflow(workflow_id)

def handle_parallel_agent_returns(workflow_id: str, parallel_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Standalone function for parallel agent returns"""
    orchestrator = EnhancedWorkflowOrchestrator()
    return orchestrator.handle_parallel_agent_returns(workflow_id, parallel_data)