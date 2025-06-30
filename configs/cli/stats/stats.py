"""
Stats CLI Command - Core Logic
Real-time system performance metrics via SystemMetricsProvider, WorkflowMonitor, CostTracker
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError
from orchestrator.real_time_metrics import SystemMetricsProvider, WorkflowMonitor, CostTracker

# Standard cache instance with shorter duration for real-time data
cache = CacheManager()

@handle_errors(operation_name="stats", return_dict=True)
def execute_stats(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main stats command execution with real-time metrics integration.
    
    Args:
        params: Command parameters including search filters
        
    Returns:
        Standardized result dictionary with system metrics data
    """
    # Check cache first - shorter duration for real-time data
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "stats")
    if cached_result:
        cached_data = json.loads(cached_result)
        # Check if cached data is still fresh (1 minute for real-time)
        if _is_cache_fresh(cached_data, minutes=1):
            return cached_data
    
    # Execute command logic with real-time data
    result = _execute_command_logic(params)
    
    # Cache result for 1 minute (real-time data needs frequent updates)
    cache.cache_content_analysis(cache_key, json.dumps(result), "stats")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for complex metrics processing.
    Uses Claude Sonnet 4 cost structure with higher estimate for metrics aggregation.
    """
    # Complex metrics processing with multiple data sources
    # Higher cost due to real-time data aggregation and analysis
    return 0.007

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate cache key with search parameters and timestamp granularity"""
    base_key = f"stats|{str(params) if params else 'none'}"
    
    # Add minute-level timestamp for real-time cache invalidation
    timestamp_minute = datetime.now().strftime("%Y%m%d%H%M")
    base_key += f"|time:{timestamp_minute}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _is_cache_fresh(cached_data: Dict[str, Any], minutes: int = 1) -> bool:
    """Check if cached data is still fresh for real-time requirements"""
    try:
        cached_time = datetime.fromisoformat(cached_data.get("timestamp", ""))
        age_limit = datetime.now() - timedelta(minutes=minutes)
        return cached_time > age_limit
    except (ValueError, TypeError):
        return False

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core stats command logic with real-time metrics integration"""
    try:
        # Initialize metrics providers
        orchestrator = _get_orchestrator_instance()
        if not orchestrator:
            return _create_error_result("Unable to access orchestrator instance")
        
        metrics_provider = SystemMetricsProvider(orchestrator)
        workflow_monitor = WorkflowMonitor()
        cost_tracker = CostTracker()
        
        # Collect real-time metrics
        dashboard_metrics = metrics_provider.get_dashboard_metrics()
        live_stats = metrics_provider.get_live_stats()
        budget_status = cost_tracker.get_budget_status()
        active_workflows = workflow_monitor.get_active_workflows()
        
        # Apply search filters if provided
        filtered_data = _apply_search_filters(
            dashboard_metrics, 
            active_workflows, 
            params or {}
        )
        
        # Compile comprehensive stats result
        result = {
            "success": True,
            "dashboard_metrics": dashboard_metrics,
            "live_stats": live_stats,
            "budget_status": budget_status,
            "active_workflows": active_workflows,
            "filtered_data": filtered_data,
            "search_params": params or {},
            "timestamp": datetime.now().isoformat(),
            "data_freshness": "real_time"
        }
        
        return result
        
    except Exception as e:
        return _create_error_result(f"Failed to collect system metrics: {str(e)}")

def _get_orchestrator_instance():
    """Get orchestrator instance for metrics collection"""
    try:
        # Try to import and get orchestrator instance
        from orchestrator.core import get_orchestrator_instance
        return get_orchestrator_instance()
    except ImportError:
        try:
            # Fallback approach
            from orchestrator.agent_orchestrator import AgentOrchestrator
            return AgentOrchestrator()
        except ImportError:
            return None

def _apply_search_filters(dashboard_metrics: Dict, active_workflows: Dict, params: Dict) -> Dict[str, Any]:
    """Apply search filters by User ID, Workflow ID, Model ID, Provider ID"""
    filtered_result = {
        "workflows": [],
        "models": [],
        "providers": [],
        "users": [],
        "applied_filters": {}
    }
    
    # Extract filter parameters
    user_id_filter = params.get("user_id")
    workflow_id_filter = params.get("workflow_id")
    model_id_filter = params.get("model_id")
    provider_id_filter = params.get("provider_id")
    
    # Filter active workflows
    for workflow_id, workflow_data in active_workflows.items():
        workflow_info = workflow_data.get("info", {})
        
        # Apply filters
        if user_id_filter and workflow_info.get("user_id") != user_id_filter:
            continue
        if workflow_id_filter and workflow_id != workflow_id_filter:
            continue
        if model_id_filter and workflow_info.get("model_id") != model_id_filter:
            continue
        if provider_id_filter and workflow_info.get("provider_id") != provider_id_filter:
            continue
        
        filtered_result["workflows"].append({
            "workflow_id": workflow_id,
            "workflow_data": workflow_data,
            "user_id": workflow_info.get("user_id"),
            "model_id": workflow_info.get("model_id"),
            "provider_id": workflow_info.get("provider_id")
        })
    
    # Filter model statistics
    if dashboard_metrics.get("models"):
        for model_name, model_data in dashboard_metrics["models"].items():
            if model_id_filter and model_name != model_id_filter:
                continue
            
            filtered_result["models"].append({
                "model_id": model_name,
                "model_data": model_data
            })
    
    # Record applied filters
    filtered_result["applied_filters"] = {
        "user_id": user_id_filter,
        "workflow_id": workflow_id_filter,
        "model_id": model_id_filter,
        "provider_id": provider_id_filter,
        "filter_count": sum(1 for f in [user_id_filter, workflow_id_filter, model_id_filter, provider_id_filter] if f)
    }
    
    return filtered_result

def _create_error_result(error_message: str) -> Dict[str, Any]:
    """Create standardized error result"""
    return {
        "success": False,
        "error": error_message,
        "timestamp": datetime.now().isoformat(),
        "data_freshness": "error"
    }

def get_workflow_progress(workflow_id: str) -> Dict[str, Any]:
    """Get detailed progress for a specific workflow"""
    try:
        orchestrator = _get_orchestrator_instance()
        if not orchestrator:
            return _create_error_result("Unable to access orchestrator instance")
        
        metrics_provider = SystemMetricsProvider(orchestrator)
        return metrics_provider.get_workflow_progress(workflow_id)
    except Exception as e:
        return _create_error_result(f"Failed to get workflow progress: {str(e)}")

def get_live_metrics_snapshot() -> Dict[str, Any]:
    """Get simplified live metrics for frequent polling"""
    try:
        orchestrator = _get_orchestrator_instance()
        if not orchestrator:
            return _create_error_result("Unable to access orchestrator instance")
        
        metrics_provider = SystemMetricsProvider(orchestrator)
        return metrics_provider.get_live_stats()
    except Exception as e:
        return _create_error_result(f"Failed to get live metrics: {str(e)}")

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_stats(params)