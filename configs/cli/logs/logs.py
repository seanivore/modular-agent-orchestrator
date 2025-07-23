"""
Logs CLI Command - Core Logic
Workflow log viewing with comprehensive filtering and search capabilities
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="logs", return_dict=True)
def execute_logs(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main logs command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI" / "app input
            - workflow_id (optional): Filter logs for specific workflow
            - search_query (optional): Search term for log content
            - limit (optional): Number of log entries to return (default: 50)
            - status_filter (optional): Filter by workflow status
            - date_range (optional): Filter by date range
        
    Returns:
        Standardized result dictionary with workflow logs
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "logs")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 2 minutes (logs may update frequently)
    cache.cache_content_analysis(cache_key, json.dumps(result), "logs")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if not params:
        params = {}
    
    base_cost = 0.001  # Base cost for log viewing
    
    # Add cost for search operations
    if params.get("search_query"):
        base_cost += 0.0005
    
    # Add cost for multiple workflow context fetches
    limit = params.get("limit", 50)
    if limit > 50:
        base_cost += (limit - 50) * 0.0001
    
    # Add cost for date range filtering (more processing)
    if params.get("date_range"):
        base_cost += 0.0003
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including workflow state"""
    base_key = f"logs|{str(params) if params else 'none'}"
    
    # Add system state fingerprints for log dependencies
    try:
        # Include workflow directory state for cache invalidation
        from orchestrator.workflow_manager import WorkflowManager
        workflow_manager = WorkflowManager()
        
        # Get basic workflow state fingerprint
        workflow_fingerprint = f"workflows:{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
        base_key += f"|{workflow_fingerprint}"
        
    except Exception:
        # Fallback to basic timestamp if managers unavailable
        base_key += f"|fallback:{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core logs command logic implementation"""
    try:
        if not params:
            params = {}
        
        # Initialize managers for log retrieval
        workflow_logs = _get_workflow_logs(params)
        
        # Apply filters if specified
        filtered_logs = _apply_filters(workflow_logs, params)
        
        # Get summary statistics
        stats = _get_log_statistics(filtered_logs)
        
        return {
            "success": True,
            "logs": filtered_logs,
            "total_logs": len(filtered_logs),
            "statistics": stats,
            "filters_applied": _get_applied_filters(params),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve logs: {str(e)}",
            "logs": [],
            "total_logs": 0,
            "timestamp": datetime.now().isoformat()
        }

def _get_workflow_logs(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Retrieve workflow logs from available sources"""
    logs = []
    
    try:
        # Try to import and use workflow managers
        from orchestrator.memory_mcp import MemoryMCPManager
        from orchestrator.workflow_state import WorkflowStateManager
        
        memory_mcp = MemoryMCPManager()
        workflow_state = WorkflowStateManager()
        
        # Get specific workflow logs if workflow_id provided
        if params.get("workflow_id"):
            workflow_id = params["workflow_id"]
            workflow_log = _get_single_workflow_log(workflow_id, memory_mcp, workflow_state)
            if workflow_log:
                logs.append(workflow_log)
        else:
            # Get all workflow summaries for log overview
            summaries = workflow_state.get_all_workflow_summaries()
            for summary in summaries:
                workflow_log = _format_workflow_summary_as_log(summary, memory_mcp)
                if workflow_log:
                    logs.append(workflow_log)
        
    except ImportError as e:
        # Fallback to basic log structure if managers unavailable
        logs.append({
            "workflow_id": "system",
            "status": "info",
            "message": f"Log system initializing - managers not available: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "type": "system_log",
            "details": {
                "note": "Full log functionality requires workflow managers",
                "available": "basic log viewing only"
            }
        })
    
    return logs

def _get_single_workflow_log(workflow_id: str, memory_mcp, workflow_state) -> Optional[Dict[str, Any]]:
    """Get detailed log for a specific workflow"""
    try:
        # Get workflow status and context
        status = workflow_state.get_workflow_status(workflow_id)
        context = memory_mcp.get_workflow_context(workflow_id)
        
        if not status and not context:
            return None
        
        # Format as log entry
        log_entry = {
            "workflow_id": workflow_id,
            "status": status.status if status else "unknown",
            "message": f"Workflow {workflow_id} log entry",
            "timestamp": status.updated_at if status else datetime.now().isoformat(),
            "type": "workflow_log",
            "details": {
                "phases_total": status.phases_total if status else 0,
                "phases_completed": status.phases_completed if status else 0,
                "health": status.health if status else "unknown",
                "last_activity": status.last_activity if status else "unknown",
                "context_available": context is not None
            }
        }
        
        # Add context observations if available
        if context and context.get("observations"):
            log_entry["details"]["recent_observations"] = context["observations"][-5:]  # Last 5
        
        return log_entry
        
    except Exception as e:
        return {
            "workflow_id": workflow_id,
            "status": "error",
            "message": f"Failed to retrieve workflow log: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "type": "error_log",
            "details": {"error": str(e)}
        }

def _format_workflow_summary_as_log(summary: Dict[str, Any], memory_mcp) -> Optional[Dict[str, Any]]:
    """Format workflow summary as log entry"""
    try:
        workflow_id = summary.get("workflow_id", "unknown")
        
        return {
            "workflow_id": workflow_id,
            "status": summary.get("status", "unknown"),
            "message": f"Workflow summary: {summary.get('name', workflow_id)}",
            "timestamp": summary.get("updated_at", datetime.now().isoformat()),
            "type": "workflow_summary",
            "details": {
                "phases_total": summary.get("phases_total", 0),
                "phases_completed": summary.get("phases_completed", 0),
                "success_rate": summary.get("success_rate", 0),
                "health": summary.get("health", "unknown")
            }
        }
        
    except Exception:
        return None

def _apply_filters(logs: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply filtering based on parameters"""
    filtered_logs = logs
    
    # Filter by status
    if params.get("status_filter"):
        status_filter = params["status_filter"]
        filtered_logs = [log for log in filtered_logs if log.get("status") == status_filter]
    
    # Filter by search query
    if params.get("search_query"):
        search_query = params["search_query"].lower()
        filtered_logs = [
            log for log in filtered_logs 
            if search_query in log.get("message", "").lower() 
            or search_query in str(log.get("details", {})).lower()
            or search_query in log.get("workflow_id", "").lower()
        ]
    
    # Filter by date range
    if params.get("date_range"):
        filtered_logs = _filter_by_date_range(filtered_logs, params["date_range"])
    
    # Apply limit
    limit = params.get("limit", 50)
    if limit and len(filtered_logs) > limit:
        # Sort by timestamp (most recent first) before limiting
        filtered_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        filtered_logs = filtered_logs[:limit]
    
    return filtered_logs

def _filter_by_date_range(logs: List[Dict[str, Any]], date_range: str) -> List[Dict[str, Any]]:
    """Filter logs by date range (e.g., '1d', '7d', '30d')"""
    try:
        # Parse date range
        if date_range.endswith('d'):
            days = int(date_range[:-1])
            cutoff_date = datetime.now() - timedelta(days=days)
        elif date_range.endswith('h'):
            hours = int(date_range[:-1])
            cutoff_date = datetime.now() - timedelta(hours=hours)
        else:
            # Default to 1 day if format not recognized
            cutoff_date = datetime.now() - timedelta(days=1)
        
        # Filter logs
        filtered = []
        for log in logs:
            try:
                log_time = datetime.fromisoformat(log.get("timestamp", ""))
                if log_time >= cutoff_date:
                    filtered.append(log)
            except ValueError:
                # Include logs with invalid timestamps
                filtered.append(log)
        
        return filtered
        
    except (ValueError, AttributeError):
        # Return original logs if date parsing fails
        return logs

def _get_log_statistics(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate statistics for log summary"""
    if not logs:
        return {"total": 0}
    
    stats = {
        "total": len(logs),
        "by_status": {},
        "by_type": {},
        "date_range": {
            "oldest": None,
            "newest": None
        }
    }
    
    timestamps = []
    
    for log in logs:
        # Count by status
        status = log.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by type
        log_type = log.get("type", "unknown")
        stats["by_type"][log_type] = stats["by_type"].get(log_type, 0) + 1
        
        # Collect timestamps
        if log.get("timestamp"):
            timestamps.append(log["timestamp"])
    
    # Calculate date range
    if timestamps:
        timestamps.sort()
        stats["date_range"]["oldest"] = timestamps[0]
        stats["date_range"]["newest"] = timestamps[-1]
    
    return stats

def _get_applied_filters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get summary of applied filters"""
    filters = {}
    
    if params.get("workflow_id"):
        filters["workflow_id"] = params["workflow_id"]
    if params.get("search_query"):
        filters["search"] = params["search_query"]
    if params.get("status_filter"):
        filters["status"] = params["status_filter"]
    if params.get("date_range"):
        filters["date_range"] = params["date_range"]
    if params.get("limit"):
        filters["limit"] = params["limit"]
    
    return filters

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_logs(params)