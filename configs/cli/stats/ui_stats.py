"""
Stats CLI Command - UI Display Patterns
Performance-focused UI patterns for real-time metrics display
"""

from typing import Dict, Any, List

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

# Standard cache instance
cache = CacheManager()
from datetime import datetime
from pathlib import Path

def display_stats_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize stats command results for UI display with real-time focus.
    
    Returns structured data for performance metrics visualization.
    Focus: Real-time data presentation with search and filtering capabilities.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Unknown error occurred"),
            "show_suggestions": True,
            "error_type": "metrics_error"
        }
    
    dashboard_metrics = result.get("dashboard_metrics", {})
    live_stats = result.get("live_stats", {})
    budget_status = result.get("budget_status", {})
    active_workflows = result.get("active_workflows", {})
    filtered_data = result.get("filtered_data", {})
    search_params = result.get("search_params", {})
    
    # Structure comprehensive stats display
    display_data = {
        "display_type": "real_time_stats",
        "header": {
            "title": "System Performance Statistics",
            "subtitle": f"Real-time metrics as of {_format_timestamp(result.get('timestamp'))}",
            "data_freshness": result.get("data_freshness", "unknown"),
            "refresh_indicator": True
        },
        "metrics_sections": [
            _build_system_overview(dashboard_metrics, live_stats),
            _build_workflow_metrics(dashboard_metrics, active_workflows),
            _build_cost_analysis(dashboard_metrics, budget_status),
            _build_performance_metrics(dashboard_metrics),
            _build_cache_metrics(dashboard_metrics)
        ],
        "search_results": _build_search_results(filtered_data, search_params),
        "active_monitoring": {
            "active_workflows_count": len(active_workflows),
            "system_status": live_stats.get("system_status", "unknown"),
            "last_update": live_stats.get("last_update"),
            "auto_refresh_recommended": True
        },
        "footer": {
            "total_workflows": dashboard_metrics.get("workflows", {}).get("total", 0),
            "system_uptime": dashboard_metrics.get("uptime", {}).get("formatted", "Unknown"),
            "show_detailed_view_hint": True
        }
    }
    
    return display_data

def _build_system_overview(dashboard_metrics: Dict, live_stats: Dict) -> Dict[str, Any]:
    """Build system overview metrics section"""
    models_data = dashboard_metrics.get("models", {})
    tools_data = dashboard_metrics.get("tools", {})
    
    return {
        "section_type": "system_overview",
        "title": "System Overview",
        "metrics": [
            {
                "name": "Models Available",
                "value": models_data.get("total", 0),
                "detail": f"{models_data.get('providers', 0)} providers",
                "status": "operational"
            },
            {
                "name": "Free Models",
                "value": models_data.get("free_models", 0),
                "detail": "Cost-effective options",
                "status": "available"
            },
            {
                "name": "Tools Available", 
                "value": tools_data.get("total", 0),
                "detail": f"{tools_data.get('available', 0)} ready",
                "status": "operational"
            },
            {
                "name": "System Status",
                "value": live_stats.get("system_status", "unknown"),
                "detail": "Real-time status",
                "status": live_stats.get("system_status", "unknown")
            }
        ],
        "priority": "high"
    }

def _build_workflow_metrics(dashboard_metrics: Dict, active_workflows: Dict) -> Dict[str, Any]:
    """Build workflow execution metrics section"""
    workflows_data = dashboard_metrics.get("workflows", {})
    
    return {
        "section_type": "workflow_metrics",
        "title": "Workflow Performance",
        "metrics": [
            {
                "name": "Total Workflows",
                "value": workflows_data.get("total", 0),
                "detail": "All time",
                "status": "info"
            },
            {
                "name": "Completed",
                "value": workflows_data.get("completed", 0),
                "detail": f"{workflows_data.get('success_rate', 0):.1f}% success rate",
                "status": "success"
            },
            {
                "name": "Active Now",
                "value": workflows_data.get("in_progress", 0),
                "detail": f"{len(active_workflows)} live executions",
                "status": "in_progress"
            },
            {
                "name": "Failed",
                "value": workflows_data.get("failed", 0),
                "detail": "Requires attention",
                "status": "error" if workflows_data.get("failed", 0) > 0 else "success"
            }
        ],
        "active_workflows": _format_active_workflows(active_workflows),
        "priority": "high"
    }

def _build_cost_analysis(dashboard_metrics: Dict, budget_status: Dict) -> Dict[str, Any]:
    """Build cost tracking and budget analysis section"""
    costs_data = dashboard_metrics.get("costs", {})
    
    return {
        "section_type": "cost_analysis",
        "title": "Cost Analysis",
        "metrics": [
            {
                "name": "Total Spent",
                "value": f"${costs_data.get('total_spent', 0):.4f}",
                "detail": "All time",
                "status": "info"
            },
            {
                "name": "Average Cost",
                "value": f"${costs_data.get('average_cost', 0):.4f}",
                "detail": "Per workflow",
                "status": "info"
            },
            {
                "name": "Today's Cost",
                "value": f"${costs_data.get('today_cost', 0):.4f}",
                "detail": "Current session",
                "status": "info"
            }
        ],
        "budget_status": {
            "daily_budget": f"${budget_status.get('daily_budget', 0):.2f}",
            "spent_today": f"${budget_status.get('spent_today', 0):.4f}",
            "remaining": f"${budget_status.get('remaining', 0):.4f}",
            "percentage_used": f"{budget_status.get('percentage_used', 0):.1f}%",
            "status": budget_status.get('status', 'unknown'),
            "status_color": _get_budget_status_color(budget_status.get('status', 'unknown'))
        },
        "priority": "medium"
    }

def _build_performance_metrics(dashboard_metrics: Dict) -> Dict[str, Any]:
    """Build system performance metrics section"""
    uptime_data = dashboard_metrics.get("uptime", {})
    
    return {
        "section_type": "performance_metrics",
        "title": "Performance Metrics",
        "metrics": [
            {
                "name": "System Uptime",
                "value": uptime_data.get("formatted", "Unknown"),
                "detail": f"{uptime_data.get('seconds', 0):.0f} seconds",
                "status": "operational"
            },
            {
                "name": "Response Time",
                "value": "Real-time",
                "detail": "Live metrics",
                "status": "optimal"
            }
        ],
        "priority": "low"
    }

def _build_cache_metrics(dashboard_metrics: Dict) -> Dict[str, Any]:
    """Build cache performance metrics section"""
    cache_data = dashboard_metrics.get("cache", {})
    
    if cache_data.get("status") == "cache_stats_unavailable":
        return {
            "section_type": "cache_metrics",
            "title": "Cache Performance",
            "status": "unavailable",
            "message": "Cache statistics not available",
            "priority": "low"
        }
    
    return {
        "section_type": "cache_metrics", 
        "title": "Cache Performance",
        "metrics": [
            {
                "name": "Hit Rate",
                "value": f"{cache_data.get('hit_rate', 0):.1f}%",
                "detail": "Cache efficiency",
                "status": "good" if cache_data.get('hit_rate', 0) > 50 else "needs_attention"
            },
            {
                "name": "Cache Size",
                "value": f"{cache_data.get('size_mb', 0):.1f} MB",
                "detail": "Memory usage",
                "status": "info"
            },
            {
                "name": "Total Hits",
                "value": cache_data.get('total_hits', 0),
                "detail": f"{cache_data.get('total_requests', 0)} total requests",
                "status": "info"
            }
        ],
        "priority": "low"
    }

def _build_search_results(filtered_data: Dict, search_params: Dict) -> Dict[str, Any]:
    """Build search and filtering results section"""
    applied_filters = filtered_data.get("applied_filters", {})
    filter_count = applied_filters.get("filter_count", 0)
    
    if filter_count == 0:
        return {
            "section_type": "search_results",
            "title": "Search & Filtering",
            "status": "no_filters",
            "message": "No search filters applied",
            "available_filters": ["user_id", "workflow_id", "model_id", "provider_id"]
        }
    
    return {
        "section_type": "search_results",
        "title": f"Search Results ({filter_count} filters applied)",
        "applied_filters": applied_filters,
        "results": {
            "workflows": len(filtered_data.get("workflows", [])),
            "models": len(filtered_data.get("models", [])),
            "providers": len(filtered_data.get("providers", [])),
            "users": len(filtered_data.get("users", []))
        },
        "filtered_workflows": _format_filtered_workflows(filtered_data.get("workflows", [])),
        "show_clear_filters": True
    }

def _format_active_workflows(active_workflows: Dict) -> List[Dict[str, Any]]:
    """Format active workflows for display"""
    formatted = []
    
    for workflow_id, workflow_data in active_workflows.items():
        workflow_info = workflow_data.get("info", {})
        start_time = workflow_data.get("start_time")
        
        formatted.append({
            "workflow_id": workflow_id,
            "name": workflow_info.get("name", "Unknown"),
            "user_id": workflow_info.get("user_id", "Unknown"),
            "current_phase": workflow_data.get("current_phase", 0),
            "start_time": start_time.strftime("%H:%M:%S") if start_time else "Unknown",
            "status": "running"
        })
    
    return formatted

def _format_filtered_workflows(filtered_workflows: List[Dict]) -> List[Dict[str, Any]]:
    """Format filtered workflows for display"""
    formatted = []
    
    for workflow in filtered_workflows:
        workflow_data = workflow.get("workflow_data", {})
        workflow_info = workflow_data.get("info", {})
        
        formatted.append({
            "workflow_id": workflow.get("workflow_id"),
            "name": workflow_info.get("name", "Unknown"),
            "user_id": workflow.get("user_id"),
            "model_id": workflow.get("model_id"),
            "provider_id": workflow.get("provider_id"),
            "status": "active"
        })
    
    return formatted

def _format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        if timestamp_str:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return "Unknown"
    except (ValueError, TypeError):
        return "Unknown"

def _get_budget_status_color(status: str) -> str:
    """Get color code for budget status"""
    status_colors = {
        "budget_ok": "green",
        "budget_watch": "yellow", 
        "budget_warning": "orange",
        "budget_exceeded": "red"
    }
    return status_colors.get(status, "gray")

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for real-time stats UI implementation.
    
    Returns what a UI designer would need to know for performance metrics.
    """
    return {
        "layout_pattern": "real_time_dashboard",
        "essential_elements": [
            "header_with_refresh_indicator",
            "metrics_sections_grid",
            "system_overview_prominence",
            "workflow_status_monitoring",
            "cost_tracking_display",
            "performance_indicators",
            "search_and_filter_interface",
            "footer_with_system_status"
        ],
        "data_requirements": {
            "real_time_metrics": "live system performance data",
            "workflow_monitoring": "active workflow execution status",
            "cost_tracking": "budget and spending information",
            "search_filters": "user/workflow/model / provider filtering",
            "cache_performance": "system efficiency metrics"
        },
        "content_priorities": [
            "system_status_visibility",
            "active_workflow_monitoring",
            "cost_awareness",
            "performance_transparency",
            "search_functionality"
        ],
        "interaction_needs": [
            "real_time_refresh_capability",
            "search_and_filter_controls",
            "detailed_view_expansion",
            "workflow_progress_tracking",
            "budget_monitoring_alerts"
        ],
        "performance_requirements": [
            "fast_metrics_loading",
            "efficient_data_refresh",
            "minimal_cache_dependency",
            "real_time_data_accuracy"
        ],
        "display_patterns": {
            "metrics_cards": "organized_performance_data",
            "status_indicators": "visual_system_health",
            "progress_bars": "workflow_completion_status",
            "cost_displays": "budget_and_spending_info",
            "search_results": "filtered_data_presentation"
        }
    }

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure for stats command"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "error_type": "metrics_error",
        "suggestions": [
            "Check that orchestrator is running properly",
            "Verify real-time metrics system is accessible",
            "Ensure sufficient permissions for system monitoring",
            "Try running with verbose output for more details"
        ],
        "recovery_actions": [
            "Restart the orchestrator service",
            "Check system resource availability",
            "Verify metrics providers are initialized"
        ],
        "show_help_hint": True
    }

def display_workflow_progress(progress_data: Dict[str, Any]) -> Dict[str, Any]:
    """Display detailed workflow progress information"""
    if not progress_data.get("success", True):
        return display_error(progress_data.get("error", "Unknown progress error"))
    
    return {
        "display_type": "workflow_progress",
        "workflow_id": progress_data.get("workflow_id"),
        "workflow_name": progress_data.get("name"),
        "status": progress_data.get("status"),
        "progress": progress_data.get("progress", {}),
        "costs": progress_data.get("costs", {}),
        "phases": progress_data.get("phases", []),
        "timestamp": progress_data.get("timestamp")
    }

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate stats UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free