"""
Goal CLI Command - Core Logic
Create workflow from single natural language message
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError
from orchestrator.conversation_bridge import ConversationToWorkflowBridge
from orchestrator.workflow_manager import WorkflowManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="goal", return_dict=True)
def execute_goal(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main goal command execution with caching and error handling.
    
    Args:
        params: Command parameters containing user goal text
        
    Returns:
        Standardized result dictionary with workflow creation results
    """
    if not params or not params.get("goal"):
        return {
            "success": False,
            "error": "Goal text is required. Usage: mao --goal 'your project goal'"
        }
    
    user_goal = params["goal"]
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get(cache_key)
    if cached_result:
        cached_data = json.loads(cached_result)
        cached_data["from_cache"] = True
        return cached_data
    
    # Execute goal workflow creation
    result = _execute_goal_logic(user_goal, params)
    
    # Cache successful results with appropriate duration
    if result.get("success"):
        cache.set(cache_key, json.dumps(result), duration=300)  # 5 minutes
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure for goal analysis and workflow creation.
    """
    if not params:
        return 0.005  # Default medium complexity
    
    # Estimate complexity based on goal length and content
    goal_text = params.get("goal", "")
    goal_length = len(goal_text)
    
    # Base cost for goal analysis
    if goal_length < 50:
        base_cost = 0.001  # Simple goal
    elif goal_length < 200:
        base_cost = 0.003  # Medium complexity
    else:
        base_cost = 0.005  # Complex goal
    
    # Add cost for workflow setup
    base_cost += 0.002
    
    # Add cost for custom command creation
    base_cost += 0.001
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including goal content"""
    goal_text = params.get("goal", "") if params else ""
    user_context = params.get("user_id", "anonymous") if params else "anonymous"
    
    # Create base key with goal content and user context
    base_key = f"goal|{goal_text}|{user_context}"
    
    # Add system state fingerprint
    current_time_rounded = int(datetime.now().timestamp() / /  300) * 300  # 5-minute blocks
    
    cache_input = f"{base_key}|{current_time_rounded}"
    return hashlib.md5(cache_input.encode()).hexdigest()[:16]

def _execute_goal_logic(user_goal: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core goal command logic implementation"""
    try:
        # Initialize conversation bridge for workflow creation
        bridge = ConversationToWorkflowBridge()
        workflow_manager = WorkflowManager()
        
        # Create workflow from conversation using existing bridge
        creation_result = bridge.create_workflow_from_conversation(user_goal)
        
        if creation_result.get("success"):
            # Get workflow details for response
            workflow_id = creation_result.get("workflow_id")
            custom_command = creation_result.get("custom_command")
            use_case_directory = creation_result.get("use_case_directory")
            
            return {
                "success": True,
                "message": f"Workflow created successfully: '{custom_command}'",
                "workflow_id": workflow_id,
                "custom_command": custom_command,
                "use_case_directory": use_case_directory,
                "next_steps": f"Run '{custom_command}' to execute your workflow",
                "setup_output": creation_result.get("setup_output", ""),
                "ready_to_execute": True
            }
        else:
            # Return the error from the bridge
            return {
                "success": False,
                "error": creation_result.get("error", "Unknown workflow creation error"),
                "workflow_id": creation_result.get("workflow_id"),
                "details": creation_result.get("setup_stderr", "")
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Goal command execution failed: {str(e)}",
            "troubleshooting": "Check that workflow setup scripts are available and accessible"
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_goal(params)