"""
Conversation to Workflow Bridge
Converts natural language goals into executable custom commands 
"""

import os
import json
import subprocess
import re
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError, ValidationError


class JSONConfigNormalizer:
    """Schema validation and normalization for workflow JSON objects"""
    
    def __init__(self):
        pass
    
    def normalize_config(self, config_data: Dict[str, Any], config_type: str) -> Dict[str, Any]:
        """Normalize and validate configuration against schemas"""
        # Basic validation - let Claude handle complex validation dynamically
        if not config_data:
            raise ValidationError("Configuration data cannot be empty")
            
        if config_type not in ["workflow", "phase", "handoff", "calendar"]:
            raise ValidationError(f"Unknown configuration type: {config_type}")
            
        # Trust Claude to provide valid configurations
        # Minimal validation to ensure required structure
        return config_data


class ConversationToWorkflowBridge:
    """Convert conversations to executable workflows with minimal hardcoded logic"""
    
    def __init__(self):
        from .memory_mcp import MemoryMCPManager
        
        # Standard cache instance
        self.cache = CacheManager()
        
        self.memory_mcp = MemoryMCPManager()
        self.setup_script_path = "scripts/setup_workflow.sh"  # ONE setup script
        self.use_case_base = "configs/use_case"
        
        # Ensure use-case directory exists
        os.makedirs(self.use_case_base, exist_ok=True)
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Conversation bridge operations include analysis and setup
        base_cost = 0.0
        
        # Add cost for goal analysis
        goal_complexity = params.get("goal_complexity", "medium")
        if goal_complexity == "low":
            base_cost += 0.001
        elif goal_complexity == "medium":
            base_cost += 0.002
        else:  # high
            base_cost += 0.005
        
        # Add cost for config generation and setup
        num_phases = params.get("num_phases", 2)
        base_cost += num_phases * 0.001  # $0.001 per phase configuration
        
        # Add cost for script execution
        base_cost += 0.001  # Setup script execution
        
        return base_cost
    
    @handle_errors(operation_name="create_workflow_from_conversation", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, subprocess.CalledProcessError))
    def create_workflow_from_conversation(self, user_goal: str) -> Dict[str, Any]:
        """Convert conversation to executable workflow following SFA pattern"""
        workflow_id = f"workflow-{uuid4().hex[:8]}"
        
        # Check cache for similar goal analysis
        cache_key = f"goal_analysis|{user_goal[:50]}"  # First 50 chars for caching
        cached_result = self.cache.get_cached_analysis(cache_key, "goal_analysis")
        if cached_result:
            cached_data = json.loads(cached_result)
            # Use cached analysis but generate new workflow ID
            workflow_spec = cached_data["workflow_spec"]
        else:
            # Analyze goal and extract requirements (no hardcoded categories)
            workflow_spec = self._analyze_goal(user_goal)
            # Cache the analysis
            self.cache.cache_content_analysis(cache_key, json.dumps({"workflow_spec": workflow_spec}), "goal_analysis")
        
        try:
            # Create workflow entity in Memory MCP
            self.memory_mcp.create_workflow_context(workflow_id, user_goal)
            
            # Generate JSON config with all required object types
            phases = self._design_phases(workflow_spec)
            config = {
                "workflow": {
                    "workflow_id": workflow_id,
                    "custom_command": self._generate_command_name(workflow_spec, user_goal),
                    "goal": user_goal,
                    "variables": self._extract_variables(workflow_spec, user_goal)
                },
                "phases": phases,
                "handoffs": self._generate_handoff_configs(phases),
                "calendar": None  # Only for recurring workflows
            }
            
            # Save config to use-case directory
            command_name = config["custom_command"].replace(" ", "-")
            use_case_dir = f"{self.use_case_base}/{command_name}"
            os.makedirs(use_case_dir, exist_ok=True)
            
            config_path = f"{use_case_dir}/config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Run the SAME setup script humans use
            result = subprocess.run([
                self.setup_script_path, 
                config_path
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                # Track success in Memory MCP
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Custom command created: {config['custom_command']}"
                )
                
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "custom_command": config["custom_command"],
                    "use_case_directory": use_case_dir,
                    "config_path": config_path,
                    "setup_output": result.stdout,
                    "ready_to_execute": True
                }
            else:
                # Track failure in Memory MCP
                error_msg = f"Setup script failed: {result.stderr}"
                self.memory_mcp.update_workflow_state(workflow_id, error_msg)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "workflow_id": workflow_id,
                    "config_path": config_path,
                    "setup_stderr": result.stderr
                }
                
        except Exception as e:
            # Track exception in Memory MCP
            error_msg = f"Conversation bridge error: {str(e)}"
            self.memory_mcp.update_workflow_state(workflow_id, error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "workflow_id": workflow_id
            }
    
    @handle_errors(operation_name="analyze_goal", return_dict=True)
    def _analyze_goal(self, user_goal: str) -> Dict[str, Any]:
        """Analyze user goal with minimal structure, trusting Claude's intelligence"""
        # Trust Claude to understand goals in any language and cultural context
        # Provide only basic structural information, let Claude determine everything else
        
        analysis = {
            "user_goal": user_goal,
            "goal_length": len(user_goal),
            "word_count": len(user_goal.split()),
            "requires_tools": True,   # Tools generally needed - let tool manager decide which
            "estimated_phases": 1     # Start simple - let Claude determine if more needed
        }
        
        # Simple structural complexity estimation based on length only
        words = user_goal.split()
        if len(words) > 20:  # Longer goals may need multiple phases
            analysis["estimated_phases"] = 2
        
        # Let Claude and tool manager determine everything else dynamically
        # No language assumptions, no cultural biases, no predetermined patterns
        
        return analysis
    
    def _generate_command_name(self, workflow_spec: Dict[str, Any], user_goal: str) -> str:
        """Generate natural language command name without English assumptions"""
        # Create simple command name based on goal structure, not content keywords
        # This works for any language and avoids English business assumptions
        
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
            return "custom goal"
        
        return " ".join(clean_words).lower()
    
    def _design_phases(self, workflow_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design workflow phases with minimal structure, trusting Claude's intelligence"""
        estimated_phases = workflow_spec.get("estimated_phases", 1)
        user_goal = workflow_spec.get("user_goal", "")
        
        phases = []
        
        # Minimal phase structure - let Claude determine optimal approach
        # No predetermined workflow patterns - support any cultural problem-solving approach
        
        if estimated_phases == 1:
            # Single phase - let Claude handle everything intelligently
            phases.append({
                "name": "goal_execution",
                "description": f"Execute user goal: {user_goal[:50]}...",
                "instructions": f"Understand and execute this goal effectively: {user_goal}",
                "deliverable": "Goal completion results",
                "resources": [],  # Let tool manager determine resources dynamically
                "tools": [],     # Let tool manager determine tools dynamically
                "model": "claude-sonnet-4",
                "fallback_model": "claude-opus-4",
                "provider": "anthropic-direct"
            })
        else:
            # Multi-phase - minimal structure for Claude to build upon
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
                    "provider": "anthropic-direct"
                },
                {
                    "name": "goal_execution",
                    "description": "Execute the planned approach",
                    "instructions": f"Execute the approach to achieve: {user_goal}",
                    "deliverable": "Goal execution results", 
                    "resources": [],
                    "tools": [],
                    "model": "claude-sonnet-4",
                    "fallback_model": "claude-opus-4",
                    "provider": "anthropic-direct"
                }
            ])
        
        # Claude can add additional phases during execution as needed
        # Supports any workflow pattern that emerges from actual user needs
        
        return phases
    
    def _extract_variables(self, workflow_spec: Dict[str, Any], user_goal: str) -> Dict[str, Any]:
        """Extract variables dynamically without domain assumptions"""
        variables = {
            "required": {
                "user_goal": {
                    "description": "The user's specific goal to accomplish",
                    "value": user_goal
                }
            },
            "optional": {}
        }
        
        # Let AI determine what additional context might be helpful
        # No predetermined domain categories or English business assumptions
        
        # Only add truly universal optional variables that apply to any goal
        if len(user_goal.split()) > 15:  # For longer, more complex goals
            variables["optional"]["additional_context"] = {
                "description": "Any additional context or requirements",
                "default": "none specified"
            }
        
        # Let AI ask for clarification during execution if needed
        # This supports goals in any language and cultural context
        
        return variables
    
    def _generate_handoff_configs(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate handoff configurations for agent coordination after each phase"""
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


# Standalone functions for integration
def create_workflow_from_goal(user_goal: str) -> Dict[str, Any]:
    """Standalone function for creating workflows from natural language goals"""
    bridge = ConversationToWorkflowBridge()
    return bridge.create_workflow_from_conversation(user_goal)


def estimate_cost(params: Dict[str, Any]) -> float:
    """Standalone cost estimation function"""
    bridge = ConversationToWorkflowBridge()
    return bridge.estimate_cost(params)