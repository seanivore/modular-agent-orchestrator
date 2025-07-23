#!/usr/bin/env python3
"""
Real-Time System Metrics Provider
Provides live data for UI components; no mock data allowed
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

class SystemMetricsProvider:
    """Provides real-time system metrics for UI components"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.start_time = datetime.now()
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Live metrics for dashboard display"""
        try:
            model_stats = self.orchestrator.model_manager.get_stats()
            tool_stats = self.orchestrator.tool_discovery.get_stats()
            workflows = self.orchestrator.list_workflows()
            
            # Calculate real statistics
            completed = [w for w in workflows if w['status'] == 'completed']
            in_progress = [w for w in workflows if w['status'] == 'in_progress']
            failed = [w for w in workflows if w['status'] == 'failed']
            
            total_cost = sum(w.get('estimated_cost', 0) for w in completed)
            avg_cost = (total_cost / len(completed)) if completed else 0
            
            return {
                "models": {
                    "total": model_stats['total_models'],
                    "providers": model_stats['total_providers'],
                    "free_models": model_stats.get('free_models', 0)
                },
                "tools": {
                    "total": tool_stats.get('total_tools', 0),
                    "available": tool_stats.get('available_tools', 0)
                },
                "workflows": {
                    "total": len(workflows),
                    "completed": len(completed),
                    "in_progress": len(in_progress),
                    "failed": len(failed),
                    "success_rate": (len(completed) / len(workflows) * 100) if workflows else 0
                },
                "costs": {
                    "total_spent": total_cost,
                    "average_cost": avg_cost,
                    "today_cost": self._calculate_today_cost(workflows)
                },
                "uptime": {
                    "seconds": (datetime.now() - self.start_time).total_seconds(),
                    "formatted": self._format_uptime()
                },
                "cache": self._get_cache_metrics(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_workflow_progress(self, workflow_id: str) -> Dict[str, Any]:
        """Real-time workflow execution progress"""
        try:
            workflow_status = self.orchestrator.get_workflow_status(workflow_id)
            if workflow_status.get('error'):
                return {"error": workflow_status['error']}
            
            # Get execution history for real progress
            execution_history = self.orchestrator.execution_history.get(workflow_id, [])
            
            return {
                "workflow_id": workflow_id,
                "name": workflow_status.get('name', 'Unknown'),
                "status": workflow_status.get('status', 'unknown'),
                "progress": {
                    "completed_phases": workflow_status.get('completed_phases', 0),
                    "total_phases": workflow_status.get('total_phases', 0),
                    "percentage": self._calculate_progress_percentage(workflow_status)
                },
                "costs": {
                    "estimated": workflow_status.get('estimated_cost', 0),
                    "actual": workflow_status.get('actual_cost', 0),
                    "remaining": max(0, workflow_status.get('estimated_cost', 0) - workflow_status.get('actual_cost', 0))
                },
                "phases": self._get_phase_details(workflow_id, execution_history),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_live_stats(self) -> Dict[str, Any]:
        """Simplified live stats for frequent polling"""
        try:
            workflows = self.orchestrator.list_workflows()
            active_count = len([w for w in workflows if w['status'] == 'in_progress'])
            
            return {
                "active_workflows": active_count,
                "total_workflows": len(workflows),
                "system_status": "operational",
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "system_status": "error",
                "error": str(e),
                "last_update": datetime.now().isoformat()
            }
    
    def _calculate_today_cost(self, workflows: List[Dict]) -> float:
        """Calculate cost for workflows executed today"""
        today = datetime.now().date()
        today_cost = 0.0
        
        for workflow in workflows:
            # This would need to be enhanced with actual execution dates
            # For now, estimate based on status
            if workflow.get('status') == 'completed':
                today_cost += workflow.get('estimated_cost', 0)
        
        return today_cost
    
    def _format_uptime(self) -> str:
        """Format uptime as human readable string"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def _get_cache_metrics(self) -> Dict[str, Any]:
        """Get cache performance metrics"""
        try:
            if hasattr(self.orchestrator.cache_manager, 'get_cache_stats'):
                cache_stats = self.orchestrator.cache_manager.get_cache_stats()
                return {
                    "hit_rate": cache_stats.get('hit_rate', 0),
                    "size_mb": cache_stats.get('size_mb', 0),
                    "total_hits": cache_stats.get('total_hits', 0),
                    "total_requests": cache_stats.get('total_requests', 0)
                }
            else:
                return {"status": "cache_stats_unavailable"}
        except Exception:
            return {"status": "cache_error"}
    
    def _calculate_progress_percentage(self, workflow_status: Dict) -> float:
        """Calculate workflow completion percentage"""
        completed = workflow_status.get('completed_phases', 0)
        total = workflow_status.get('total_phases', 1)
        return (completed / total * 100) if total > 0 else 0
    
    def _get_phase_details(self, workflow_id: str, execution_history: List) -> List[Dict]:
        """Get detailed phase information"""
        phase_details = []
        
        for i, result in enumerate(execution_history):
            phase_details.append({
                "phase_number": i + 1,
                "name": result.get('phase_name', f'Phase {i+1}'),
                "status": "completed" if result.get('success', False) else "failed",
                "model": result.get('model_used', 'unknown'),
                "tokens": result.get('tokens_used', 0),
                "cost": result.get('cost', 0),
                "duration": result.get('duration_seconds', 0),
                "error": result.get('error') if not result.get('success', False) else None
            })
        
        return phase_details


class WorkflowMonitor:
    """Real-time workflow execution monitoring"""
    
    def __init__(self):
        self.subscribers = []
        self.active_workflows = {}
    
    def subscribe(self, callback):
        """Subscribe to workflow events"""
        self.subscribers.append(callback)
    
    def on_workflow_start(self, workflow_id: str, workflow_info: Dict):
        """Workflow execution started"""
        self.active_workflows[workflow_id] = {
            "start_time": datetime.now(),
            "info": workflow_info,
            "current_phase": 0
        }
        self._notify_subscribers("workflow_start", {
            "workflow_id": workflow_id,
            "workflow_info": workflow_info,
            "timestamp": datetime.now().isoformat()
        })
    
    def on_phase_start(self, workflow_id: str, phase_info: Dict):
        """Phase execution started"""
        if workflow_id in self.active_workflows:
            self.active_workflows[workflow_id]["current_phase"] = phase_info.get("phase_number", 0)
        
        self._notify_subscribers("phase_start", {
            "workflow_id": workflow_id,
            "phase_info": phase_info,
            "timestamp": datetime.now().isoformat()
        })
    
    def on_phase_progress(self, workflow_id: str, progress_info: Dict):
        """Phase progress update"""
        self._notify_subscribers("phase_progress", {
            "workflow_id": workflow_id,
            "progress_info": progress_info,
            "timestamp": datetime.now().isoformat()
        })
    
    def on_phase_complete(self, workflow_id: str, result_info: Dict):
        """Phase execution completed"""
        self._notify_subscribers("phase_complete", {
            "workflow_id": workflow_id,
            "result_info": result_info,
            "timestamp": datetime.now().isoformat()
        })
    
    def on_workflow_complete(self, workflow_id: str, final_result: Dict):
        """Workflow execution completed"""
        if workflow_id in self.active_workflows:
            start_time = self.active_workflows[workflow_id]["start_time"]
            duration = (datetime.now() - start_time).total_seconds()
            final_result["total_duration"] = duration
            del self.active_workflows[workflow_id]
        
        self._notify_subscribers("workflow_complete", {
            "workflow_id": workflow_id,
            "final_result": final_result,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_active_workflows(self) -> Dict[str, Dict]:
        """Get currently active workflows"""
        return self.active_workflows.copy()
    
    def _notify_subscribers(self, event_type: str, data: Dict):
        """Notify all subscribers of an event"""
        for callback in self.subscribers:
            try:
                callback(event_type, data)
            except Exception as e:
                # Log error but don't break other subscribers
                print(f"Error notifying subscriber: {e}")


class CostTracker:
    """Real-time cost tracking and budget management"""
    
    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.costs_today = 0.0
        self.cost_history = []
        self.last_reset = datetime.now().date()
    
    def add_cost(self, amount: float, workflow_id: str, phase_name: str = None):
        """Add a cost entry"""
        self._check_daily_reset()
        
        cost_entry = {
            "amount": amount,
            "workflow_id": workflow_id,
            "phase_name": phase_name,
            "timestamp": datetime.now()
        }
        
        self.cost_history.append(cost_entry)
        self.costs_today += amount
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status"""
        self._check_daily_reset()
        
        remaining = max(0, self.daily_budget - self.costs_today)
        percentage_used = (self.costs_today / self.daily_budget * 100) if self.daily_budget > 0 else 0
        
        return {
            "daily_budget": self.daily_budget,
            "spent_today": self.costs_today,
            "remaining": remaining,
            "percentage_used": percentage_used,
            "status": self._get_budget_status_level(percentage_used),
            "last_reset": self.last_reset.isoformat(),
            "entries_today": len([c for c in self.cost_history if c["timestamp"].date() == datetime.now().date()])
        }
    
    def _check_daily_reset(self):
        """Reset daily costs if it's a new day"""
        today = datetime.now().date()
        if today > self.last_reset:
            self.costs_today = 0.0
            self.last_reset = today
    
    def _get_budget_status_level(self, percentage_used: float) -> str:
        """Get budget status level"""
        if percentage_used >= 100:
            return "budget_exceeded"
        elif percentage_used >= 80:
            return "budget_warning"
        elif percentage_used >= 50:
            return "budget_watch"
        else:
            return "budget_ok"
