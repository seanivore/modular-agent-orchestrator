"""
Review CLI Command - Core Logic
Workflow state management to review and search workflows
"""

import json
import hashlib
# import os  # Removed - was only used for sys.path.append
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.workflow_manager import WorkflowManager
from orchestrator.workflow_state import WorkflowStateManager
from orchestrator.memory_mcp import MemoryMCPManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="review", return_dict=True)
def execute_review(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main review command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI / app input
        - workflow_id: Optional workflow ID to review
        - command: Optional custom command to search for
        - user_id: Optional user ID filter
        - search: Optional search term
        - detailed: Optional flag for detailed review
        - include_context: Optional flag to include workflow context
        
    Returns:
        Standardized result dictionary with workflow review information
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "review")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute review logic
    result = _execute_review_logic(params)
    
    # Cache result with 10-minute duration
    cache.cache_content_analysis(cache_key, json.dumps(result), "review")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Moderate cost for workflow search, state retrieval, and context analysis
    base_cost = 0.003
    
    # Add cost for detailed review operations
    if params and params.get("detailed", False):
        base_cost += 0.002
    
    # Add cost for context retrieval
    if params and params.get("include_context", False):
        base_cost += 0.002
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including workflow state"""
    base_key = f"review|{str(params) if params else 'none'}"
    
    # Add workflow directory fingerprint
    workflows_dir = Path(__file__).parent.parent.parent  /  "workflows"
    
    # Include directory modification time and workflow state
    directory_state = ""
    if workflows_dir.exists():
        # Get all workflow directories
        workflow_dirs = [d for d in workflows_dir.iterdir() 
                        if d.is_dir() and not d.name.startswith('.') 
                        and d.name != 'json_object_templates']
        
        if workflow_dirs:
            file_count = len(workflow_dirs)
            # Get most recent modification from all workflow directories
            last_modified = max([d.stat().st_mtime for d in workflow_dirs] + [0])
            directory_state = f"dirs:{file_count}|modified:{last_modified}"
        else:
            directory_state = "dirs:0|modified:0"
    
    # Add current timestamp component for moderate freshness
    time_component = datetime.now().strftime("%Y%m%d%H%M")[:12]  # 10-minute granularity
    
    fingerprint = f"{base_key}|{directory_state}|{time_component}"
    return hashlib.md5(fingerprint.encode()).hexdigest()[:16]

def _execute_review_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core review logic implementation"""
    try:
        # Initialize managers
        workflow_manager = WorkflowManager()
        state_manager = WorkflowStateManager()
        memory_manager = MemoryMCPManager()
        
        # Extract search parameters
        workflow_id = params.get("workflow_id", "") if params else ""
        custom_command = params.get("command", "") if params else ""
        user_id = params.get("user_id", "") if params else ""
        search_term = params.get("search", "") if params else ""
        detailed = params.get("detailed", False) if params else False
        include_context = params.get("include_context", False) if params else False
        
        # Determine search strategy
        if workflow_id:
            # Direct workflow ID lookup
            workflow = workflow_manager.get_workflow_by_id(workflow_id)
            workflows = [workflow] if workflow else []
        elif custom_command:
            # Search by custom command using general search
            workflows = workflow_manager.find_workflows(custom_command)
        elif search_term:
            # General search
            workflows = workflow_manager.find_workflows(search_term)
        else:
            # List recent workflows for review
            workflows = workflow_manager.list_workflows()
            # Limit to most recent 20 for review interface
            workflows = workflows[:20] if workflows else []
        
        # Apply user filter if specified
        if user_id:
            workflows = [w for w in workflows if w.get("user_id", "").lower() == user_id.lower()]
        
        # Enhance workflows with detailed information
        enhanced_workflows = []
        for workflow in workflows:
            enhanced_workflow = _enhance_workflow_for_review(
                workflow, state_manager, memory_manager, detailed, include_context
            )
            enhanced_workflows.append(enhanced_workflow)
        
        # Sort by last modified or created date
        enhanced_workflows.sort(
            key=lambda w: w.get("last_modified", w.get("created_at", "")), 
            reverse=True
        )
        
        # Generate review summary
        review_summary = _generate_review_summary(enhanced_workflows, params)
        
        return {
            "success": True,
            "workflows": enhanced_workflows,
            "total_count": len(enhanced_workflows),
            "review_summary": review_summary,
            "search_parameters": {
                "workflow_id": workflow_id,
                "command": custom_command,
                "user_id": user_id,
                "search": search_term,
                "detailed": detailed,
                "include_context": include_context
            },
            "review_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Workflow review failed: {str(e)}",
            "workflows": [],
            "total_count": 0,
            "review_summary": {},
            "search_parameters": params if params else {}
        }

def _enhance_workflow_for_review(
    workflow: Dict[str, Any], 
    state_manager: WorkflowStateManager, 
    memory_manager: MemoryMCPManager,
    detailed: bool = False,
    include_context: bool = False
) -> Dict[str, Any]:
    """Enhance workflow with additional review information"""
    
    enhanced = workflow.copy()
    workflow_id = workflow.get("workflow_id", "")
    
    # Add workflow state information
    try:
        workflow_status = state_manager.get_workflow_status(workflow_id)
        if workflow_status:
            enhanced["workflow_status"] = {
                "status": workflow_status.status,
                "phases_total": workflow_status.phases_total,
                "phases_completed": workflow_status.phases_completed,
                "phases_active": workflow_status.phases_active,
                "last_activity": workflow_status.last_activity,
                "health": workflow_status.health
            }
    except Exception as e:
        enhanced["workflow_status"] = {"error": f"Status unavailable: {str(e)}"}
    
    # Add recovery information if workflow is interrupted
    if enhanced.get("status", "").lower() in ["interrupted", "paused", "failed"]:
        try:
            recovery_plan = state_manager.recover_interrupted_workflow(workflow_id)
            if recovery_plan:
                enhanced["recovery_options"] = {
                    "recovery_type": recovery_plan.recovery_type,
                    "current_phase": recovery_plan.current_phase,
                    "next_phase": recovery_plan.next_phase,
                    "context_available": recovery_plan.context_available,
                    "files_accessible": recovery_plan.files_accessible,
                    "recovery_actions": recovery_plan.recovery_actions,
                    "estimated_recovery_time": recovery_plan.estimated_recovery_time
                }
        except Exception as e:
            enhanced["recovery_options"] = {"error": f"Recovery analysis failed: {str(e)}"}
    
    # Add detailed workflow analysis if requested
    if detailed:
        enhanced["detailed_analysis"] = _analyze_workflow_details(workflow)
    
    # Add workflow context if requested
    if include_context:
        try:
            context = memory_manager.get_workflow_context(workflow_id)
            enhanced["workflow_context"] = context
        except Exception as e:
            enhanced["workflow_context"] = {"error": f"Context unavailable: {str(e)}"}
    
    return enhanced

def _analyze_workflow_details(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze workflow for detailed review information"""
    
    analysis = {
        "complexity_score": 0,
        "completion_rate": 0.0,
        "file_count": 0,
        "deliverable_count": 0,
        "phase_breakdown": {},
        "timeline_analysis": {}
    }
    
    # Analyze workflow complexity
    phases = workflow.get("phases", [])
    if phases:
        analysis["complexity_score"] = len(phases)
        
        # Calculate completion rate
        completed_phases = len([p for p in phases if p.get("status") == "completed"])
        analysis["completion_rate"] = completed_phases  /  len(phases) if phases else 0.0
        
        # Phase breakdown
        phase_statuses = {}
        for phase in phases:
            status = phase.get("status", "unknown")
            phase_statuses[status] = phase_statuses.get(status, 0) + 1
        analysis["phase_breakdown"] = phase_statuses
    
    # Analyze files and deliverables
    if workflow.get("has_deliverables", False):
        # This would typically scan the workflow directory
        analysis["deliverable_count"] = 1  # Placeholder
    
    # Timeline analysis
    created_at = workflow.get("created_at", "")
    last_modified = workflow.get("last_modified", "")
    
    if created_at and last_modified:
        try:
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            modified_dt = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
            duration = (modified_dt - created_dt).total_seconds()
            
            analysis["timeline_analysis"] = {
                "duration_seconds": duration,
                "duration_hours": duration  /  3600,
                "is_recent": duration < 86400,  # Less than 24 hours
                "is_active": (datetime.now() - modified_dt).total_seconds() < 3600  # Modified within 1 hour
            }
        except:
            analysis["timeline_analysis"] = {"error": "Could not parse timestamps"}
    
    return analysis

def _generate_review_summary(workflows: List[Dict[str, Any]], params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate summary information for the review session"""
    
    if not workflows:
        return {
            "message": "No workflows found for review",
            "recommendations": ["Try adjusting search criteria", "Check if workflows exist in the system"]
        }
    
    # Status distribution
    status_counts = {}
    for workflow in workflows:
        status = workflow.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Identify workflows needing attention
    interrupted_workflows = [w for w in workflows if w.get("status", "").lower() in ["interrupted", "paused", "failed"]]
    recent_workflows = []
    
    for workflow in workflows:
        last_modified = workflow.get("last_modified", "")
        if last_modified:
            try:
                modified_dt = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                if (datetime.now() - modified_dt).total_seconds() < 86400:  # 24 hours
                    recent_workflows.append(workflow)
            except:
                pass
    
    # Generate actionable recommendations
    recommendations = []
    if interrupted_workflows:
        recommendations.append(f"Consider continuing {len(interrupted_workflows)} interrupted workflows")
    if recent_workflows:
        recommendations.append(f"Review progress on {len(recent_workflows)} recently active workflows")
    if len(workflows) > 10:
        recommendations.append("Use filters to narrow down workflow selection")
    
    return {
        "total_reviewed": len(workflows),
        "status_distribution": status_counts,
        "interrupted_count": len(interrupted_workflows),
        "recent_activity_count": len(recent_workflows),
        "recommendations": recommendations,
        "review_categories": {
            "needs_attention": len(interrupted_workflows),
            "recently_active": len(recent_workflows),
            "completed": status_counts.get("completed", 0),
            "in_progress": status_counts.get("active", 0)
        }
    }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_review(params)