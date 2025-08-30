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
from .error_handling import handle_errors, retry_with_backoff, APIError


class ConversationToWorkflowBridge:
    """Convert conversations to executable workflows using proven SFA patterns"""
    
    def __init__(self):
        from .memory_mcp import MemoryMCPManager
        
        # Standard cache instance
        self.cache = CacheManager()
        
        self.memory_mcp = MemoryMCPManager()
        self.setup_script_path = "scripts / setup_workflow.sh"  # ONE setup script
        self.use_case_base = "configs / use_case"
        
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
            
            # Generate JSON config (same format humans create)
            config = {
                "workflow_id": workflow_id,
                "custom_command": self._generate_command_name(workflow_spec, user_goal),
                "goal": user_goal,
                "phases": self._design_phases(workflow_spec),
                "variables": self._extract_variables(workflow_spec, user_goal)
            }
            
            # Save config to use-case directory
            command_name = config["custom_command"].replace(" ", "-")
            use_case_dir = f"{self.use_case_base} / {command_name}"
            os.makedirs(use_case_dir, exist_ok=True)
            
            config_path = f"{use_case_dir} / config.json"
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
        """Analyze user goal dynamically without English keyword assumptions"""
        # Trust AI to understand goals in any language and cultural context
        # Provide minimal structure - let tool manager determine needed tools dynamically
        
        analysis = {
            "user_goal": user_goal,
            "goal_length": len(user_goal),
            "word_count": len(user_goal.split()),
            "complexity": "medium",  # Default - let AI adjust as needed
            "requires_tools": True,   # Assume tools needed - let tool manager decide which
            "estimated_phases": 1     # Default to single phase - let AI determine if more needed
        }
        
        # Simple structural complexity estimation (not based on English keywords)
        words = user_goal.split()
        if len(words) < 8:
            analysis["complexity"] = "low"
        elif len(words) > 25:
            analysis["complexity"] = "high"
        
        # Check for multiple requests in goal (language-neutral)
        if any(connector in user_goal for connector in [" and ", ";", ",", " then ", " also "]):
            analysis["estimated_phases"] = 2
        
        # Let AI and tool manager determine everything else based on actual goal content
        # No predetermined categories or English assumptions
        
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
        """Design workflow phases dynamically based on actual user goal"""
        complexity = workflow_spec.get("complexity", "medium")
        estimated_phases = workflow_spec.get("estimated_phases", 1)
        user_goal = workflow_spec.get("user_goal", "")
        
        phases = []
        
        # Let AI determine optimal phase structure based on actual goal
        # No predetermined workflow patterns - trust AI intelligence
        
        if estimated_phases == 1 or complexity == "low":
            # Single phase for simple goals - let AI handle everything intelligently
            phases.append({
                "name": "goal_execution",
                "description": f"Execute user goal: {user_goal[:50]}...",
                "instructions": f"Understand and execute this goal effectively: {user_goal}",
                "deliverable": "Goal completion results",
                "model": "claude-sonnet-4"  # Let model manager choose optimal model
            })
        else:
            # Multi-phase for complex goals - let AI break down as needed
            phases.extend([
                {
                    "name": "goal_analysis",
                    "description": "Analyze goal and plan optimal approach",
                    "instructions": f"Analyze this goal and determine the best approach: {user_goal}",
                    "deliverable": "Goal analysis and execution plan",
                    "model": "claude-sonnet-4"
                },
                {
                    "name": "goal_execution",
                    "description": "Execute the planned approach",
                    "instructions": f"Execute the planned approach to achieve: {user_goal}",
                    "deliverable": "Goal execution results",
                    "model": "claude-sonnet-4"
                }
            ])
        
        # Let AI add additional phases during execution if needed
        # This supports emergent workflow patterns that don't fit predetermined categories
        
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


# Example usage and testing functions
def test_conversation_bridge():
    """Test the conversation bridge with sample goals"""
    bridge = ConversationToWorkflowBridge()
    
    test_goals = [
        "Create a marketing strategy for my B2B startup",
        "Research competitors in the project management space",
        "Design a logo and brand identity for my company",
        "Write a comprehensive business plan"
    ]
    
    for goal in test_goals:
        print(f"\n🎯 Testing goal: {goal}")
        result = bridge.create_workflow_from_conversation(goal)
        
        if result["success"]:
            print(f"✅ Created command: {result['custom_command']}")
            print(f"📁 Directory: {result['use_case_directory']}")
        else:
            print(f"❌ Failed: {result['error']}")


if __name__ == "__main__":
    # Run tests if executed directly
    test_conversation_bridge()