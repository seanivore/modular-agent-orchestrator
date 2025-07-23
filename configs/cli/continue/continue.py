"""
Continue CLI Command - Core Logic
Workflow state management to jump back into interrupted workflows
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Integration imports
from orchestrator.workflow_manager import WorkflowManager
from orchestrator.workflow_state import WorkflowStateManager
from orchestrator.memory_mcp import MemoryMCPManager
from orchestrator.username_manager import UsernameManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="continue", return_dict=True)
def execute_continue(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main continue command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI / app input
        
    Returns:
        Standardized result dictionary with workflow continuation data
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "continue")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result with short duration (workflow states change frequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "continue")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if not params:
        params = {}
    
    base_cost = 0.0
    
    # Base workflow discovery cost
    base_cost += 0.002  # Workflow scanning and state analysis
    
    # Memory MCP operations
    mcp_operations = params.get("mcp_operations", 3)
    base_cost += mcp_operations * 0.001  # Memory retrieval operations
    
    # State restoration complexity
    state_operations = params.get("state_operations", 2)
    base_cost += state_operations * 0.002  # State analysis and recovery planning
    
    # Recovery plan generation
    if params.get("generate_recovery_plan", True):
        base_cost += 0.003  # Recovery plan analysis
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including user and workflow state"""
    base_key = f"continue|{str(params) if params else 'none'}"
    
    # Add user context fingerprint
    try:
        username_manager = UsernameManager()
        current_user = username_manager.get_current_user()
        if current_user:
            base_key += f"|user:{current_user.get('user_id', 'unknown')}"
    except Exception:
        pass  # Graceful degradation if user context unavailable
    
    # Add workflow directory state fingerprint
    workflows_dir = Path(__file__).parent.parent.parent  /  "workflows"
    if workflows_dir.exists():
        # Include directory modification time for cache invalidation
        dir_stat = workflows_dir.stat()
        base_key += f"|workflows:{dir_stat.st_mtime}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core continue command logic implementation"""
    try:
        # Initialize managers
        workflow_manager = WorkflowManager()
        state_manager = WorkflowStateManager()
        memory_mcp = MemoryMCPManager()
        username_manager = UsernameManager()
        
        # Get current user context
        current_user = username_manager.get_current_user()
        if not current_user:
            return {
                "success": False,
                "error": "No user session found. Please login first with 'mao --login'",
                "error_type": "authentication_required"
            }
        
        user_id = current_user.get("user_id")
        
        # Determine continuation strategy
        continue_strategy = params.get("strategy", "auto") if params else "auto"
        workflow_identifier = params.get("workflow_id") if params else None
        
        if continue_strategy == "auto" and not workflow_identifier:
            # Simple UX: Find most recent interrupted workflow
            result = _find_recent_interrupted_workflow(user_id, workflow_manager, state_manager)
        elif workflow_identifier:
            # Specific workflow continuation
            result = _continue_specific_workflow(workflow_identifier, workflow_manager, state_manager, memory_mcp)
        else:
            # List available workflows for user selection
            result = _list_continuable_workflows(user_id, workflow_manager, state_manager)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to process continue command: {str(e)}",
            "error_type": "execution_error"
        }

def _find_recent_interrupted_workflow(user_id: str, workflow_manager: WorkflowManager, state_manager: WorkflowStateManager) -> Dict[str, Any]:
    """Find and prepare continuation for most recent interrupted workflow"""
    try:
        # Get all workflows for user
        workflows = workflow_manager.list_workflows()
        
        # Filter for user's interrupted workflows
        interrupted_workflows = []
        for workflow in workflows:
            if workflow.get("user_id") == user_id:
                # Check workflow state
                workflow_id = workflow.get("workflow_id")
                if workflow_id:
                    status = state_manager.get_workflow_status(workflow_id)
                    if status and status.status in ["paused", "interrupted", "active"]:
                        workflow["workflow_status"] = status
                        interrupted_workflows.append(workflow)
        
        if not interrupted_workflows:
            return {
                "success": True,
                "continuation_type": "no_interrupted_workflows",
                "message": "No interrupted workflows found for current user",
                "suggested_actions": [
                    "Start a new workflow with 'mao --goal <description>'",
                    "List all workflows with 'mao --workflows'",
                    "Review existing workflows with 'mao --review'"
                ]
            }
        
        # Sort by last activity (most recent first)
        interrupted_workflows.sort(
            key=lambda w: w.get("workflow_status", {}).last_activity or "", 
            reverse=True
        )
        
        # Get most recent interrupted workflow
        most_recent = interrupted_workflows[0]
        
        # Generate recovery plan
        recovery_plan = _generate_recovery_plan(most_recent, state_manager)
        
        return {
            "success": True,
            "continuation_type": "recent_interrupted",
            "workflow": most_recent,
            "recovery_plan": recovery_plan,
            "other_interrupted": len(interrupted_workflows) - 1,
            "ready_to_continue": recovery_plan.get("ready_to_continue", False)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to find recent interrupted workflow: {str(e)}",
            "error_type": "workflow_discovery_error"
        }

def _continue_specific_workflow(workflow_identifier: str, workflow_manager: WorkflowManager, state_manager: WorkflowStateManager, memory_mcp: MemoryMCPManager) -> Dict[str, Any]:
    """Continue a specific workflow by ID or custom command"""
    try:
        # Try to find workflow by ID first
        workflows = workflow_manager.list_workflows()
        target_workflow = None
        
        for workflow in workflows:
            if (workflow.get("workflow_id") == workflow_identifier or 
                workflow.get("custom_command") == workflow_identifier):
                target_workflow = workflow
                break
        
        if not target_workflow:
            # Try searching by partial match
            matches = workflow_manager.find_workflows(workflow_identifier)
            if matches:
                target_workflow = matches[0]  # Use first match
            else:
                return {
                    "success": False,
                    "error": f"Workflow '{workflow_identifier}' not found",
                    "error_type": "workflow_not_found",
                    "suggestions": [
                        "Check workflow ID spelling",
                        "List available workflows with 'mao --workflows'",
                        "Use 'mao --review' to browse workflows"
                    ]
                }
        
        # Get workflow state and context
        workflow_id = target_workflow.get("workflow_id")
        workflow_status = state_manager.get_workflow_status(workflow_id)
        workflow_context = memory_mcp.get_workflow_context(workflow_id)
        
        # Generate recovery plan
        recovery_plan = _generate_recovery_plan(target_workflow, state_manager)
        
        return {
            "success": True,
            "continuation_type": "specific_workflow",
            "workflow": target_workflow,
            "workflow_status": workflow_status,
            "workflow_context": workflow_context,
            "recovery_plan": recovery_plan,
            "ready_to_continue": recovery_plan.get("ready_to_continue", False)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to continue specific workflow: {str(e)}",
            "error_type": "workflow_continuation_error"
        }

def _list_continuable_workflows(user_id: str, workflow_manager: WorkflowManager, state_manager: WorkflowStateManager) -> Dict[str, Any]:
    """List all workflows that can be continued for user selection"""
    try:
        # Get all workflows for user
        workflows = workflow_manager.list_workflows()
        
        # Filter and categorize workflows
        user_workflows = []
        for workflow in workflows:
            if workflow.get("user_id") == user_id:
                workflow_id = workflow.get("workflow_id")
                if workflow_id:
                    status = state_manager.get_workflow_status(workflow_id)
                    workflow["workflow_status"] = status
                    workflow["continuable"] = status and status.status != "completed"
                    user_workflows.append(workflow)
        
        # Sort by last activity
        user_workflows.sort(key=lambda w: w.get("last_modified", ""), reverse=True)
        
        # Separate by status
        interrupted_workflows = [w for w in user_workflows if w.get("continuable") and w.get("workflow_status", {}).status in ["paused", "interrupted"]]
        active_workflows = [w for w in user_workflows if w.get("continuable") and w.get("workflow_status", {}).status == "active"]
        completed_workflows = [w for w in user_workflows if not w.get("continuable")]
        
        return {
            "success": True,
            "continuation_type": "workflow_selection",
            "interrupted_workflows": interrupted_workflows,
            "active_workflows": active_workflows,
            "completed_workflows": completed_workflows,
            "total_workflows": len(user_workflows),
            "total_continuable": len(interrupted_workflows) + len(active_workflows)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list continuable workflows: {str(e)}",
            "error_type": "workflow_listing_error"
        }

def _generate_recovery_plan(workflow: Dict[str, Any], state_manager: WorkflowStateManager) -> Dict[str, Any]:
    """Generate recovery plan for workflow continuation"""
    try:
        workflow_id = workflow.get("workflow_id")
        workflow_status = workflow.get("workflow_status")
        
        if not workflow_status:
            return {
                "ready_to_continue": False,
                "recovery_type": "status_unknown",
                "message": "Cannot determine workflow status for recovery planning"
            }
        
        # Determine recovery strategy based on status
        if workflow_status.status == "completed":
            return {
                "ready_to_continue": False,
                "recovery_type": "already_completed",
                "message": "Workflow is already completed",
                "suggestion": "Use 'mao --review' to examine completed workflow"
            }
        
        elif workflow_status.status in ["paused", "interrupted"]:
            return {
                "ready_to_continue": True,
                "recovery_type": "resume_from_pause",
                "current_phase": f"Phase {workflow_status.phases_completed + 1}",
                "phases_remaining": workflow_status.phases_total - workflow_status.phases_completed,
                "estimated_recovery_time": "1-2 minutes",
                "recovery_actions": [
                    "Restore workflow context from Memory MCP",
                    "Verify file accessibility",
                    "Resume from last completed phase",
                    "Continue workflow execution"
                ]
            }
        
        elif workflow_status.status == "active":
            return {
                "ready_to_continue": True,
                "recovery_type": "rejoin_active",
                "current_phase": f"Phase {workflow_status.phases_active}",
                "phases_remaining": workflow_status.phases_total - workflow_status.phases_completed,
                "estimated_recovery_time": "< 1 minute",
                "recovery_actions": [
                    "Rejoin active workflow session",
                    "Sync with current execution state",
                    "Continue monitoring progress"
                ]
            }
        
        else:
            return {
                "ready_to_continue": False,
                "recovery_type": "unknown_status",
                "message": f"Unknown workflow status: {workflow_status.status}",
                "suggestion": "Contact support or restart workflow"
            }
            
    except Exception as e:
        return {
            "ready_to_continue": False,
            "recovery_type": "recovery_plan_error",
            "message": f"Failed to generate recovery plan: {str(e)}"
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_continue(params)