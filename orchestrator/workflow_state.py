"""
Workflow State Management
Simple state tracking with Memory MCP integration
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Import MCP components built in previous phases
from .memory_mcp import MemoryMCPManager
from tools.files_api.files_api import FilesAPIManager
from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError
from pathlib import Path


@dataclass
class WorkflowStatus:
    """Current workflow status summary"""
    workflow_id: str
    status: str  # 'initialized', 'active', 'paused', 'completed', 'failed'
    phases_total: int
    phases_completed: int
    phases_active: int
    last_activity: str
    created_at: str
    updated_at: str
    health: str  # 'healthy', 'warning', 'error'


@dataclass
class RecoveryPlan:
    """Recovery plan for interrupted workflows"""
    workflow_id: str
    recovery_type: str  # 'resume_phase', 'restart_phase', 'continue_next', 'restart_workflow'
    current_phase: Optional[str]
    next_phase: Optional[str]
    context_available: bool
    files_accessible: bool
    recovery_actions: List[str]
    estimated_recovery_time: str


class WorkflowStateManager:
    """
    Simple state tracking with Memory MCP
    Handles workflow progress, status, and session recovery
    """
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Workflow state operations are generally low cost
        base_cost = 0.0
        
        # Add cost for status checks
        status_checks = params.get("status_checks", 3)
        base_cost += status_checks * 0.0005  # $0.0005 per status check
        
        # Add cost for progress tracking
        progress_updates = params.get("progress_updates", 5)
        base_cost += progress_updates * 0.0001  # $0.0001 per update
        
        # Add cost for recovery operations
        recovery_operations = params.get("recovery_operations", 1)
        base_cost += recovery_operations * 0.002  # $0.002 per recovery (more complex)
        
        # Add cost for state analysis
        analysis_operations = params.get("analysis_operations", 1)
        base_cost += analysis_operations * 0.001  # $0.001 per analysis
        
        return base_cost
    
    def track_workflow_progress(self, workflow_id: str, update: str) -> bool:
        """Simple progress tracking with timestamps for logging (not filenames)"""
        
        try:
            # Timestamps for LOGGING, not filenames - clean separation
            timestamp = datetime.now().isoformat()
            
            # Single source of truth: Memory MCP
            success = self.memory_mcp.update_workflow_state(
                workflow_id,
                f"{timestamp}: {update}"
            )
            
            return success
            
        except Exception as e:
            # Graceful degradation - log locally if MCP unavailable
            print(f"Warning: State tracking failed for {workflow_id}: {str(e)}")
            return False
    
    @handle_errors(operation_name="get_workflow_status", return_dict=False)
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get current workflow status with comprehensive analysis"""
        
        # Check cache for recent status
        cache_key = f"workflow_status|{workflow_id}"
        cached_result = self.cache.get_cached_analysis(cache_key, "workflow_status")
        if cached_result:
            status_data = json.loads(cached_result)
            return WorkflowStatus(**status_data)
        
        try:
            # Get complete context from Memory MCP
            context = self.memory_mcp.get_workflow_context(workflow_id)
            if not context:
                return None
            
            # Parse observations to determine status
            observations = context.get("observations", [])
            if not observations:
                return WorkflowStatus(
                    workflow_id=workflow_id,
                    status="unknown",
                    phases_total=0,
                    phases_completed=0,
                    phases_active=0,
                    last_activity="No activity recorded",
                    created_at="Unknown",
                    updated_at=datetime.now().isoformat(),
                    health="warning"
                )
            
            # Analyze workflow state from observations
            analysis = self._analyze_workflow_observations(observations)
            
            status = WorkflowStatus(
                workflow_id=workflow_id,
                status=analysis["status"],
                phases_total=analysis["phases_total"],
                phases_completed=analysis["phases_completed"],
                phases_active=analysis["phases_active"],
                last_activity=analysis["last_activity"],
                created_at=analysis["created_at"],
                updated_at=datetime.now().isoformat(),
                health=analysis["health"]
            )
            
            # Cache the result for future use
            self.cache.cache_content_analysis(cache_key, json.dumps(asdict(status)), "workflow_status")
            
            return status
            
        except Exception as e:
            print(f"Error getting workflow status: {str(e)}")
            return None
    
    def _analyze_workflow_observations(self, observations: List[str]) -> Dict[str, Any]:
        """Analyze observations to extract workflow state"""
        
        phases_started = 0
        phases_completed = 0
        phases_failed = 0
        created_at = "Unknown"
        last_activity = "No activity"
        
        # Parse observations for state information
        for obs in observations:
            obs_lower = obs.lower()
            
            # Track creation
            if "created:" in obs_lower or "initialized" in obs_lower:
                created_at = obs
            
            # Track phase activity
            if "phase started:" in obs_lower:
                phases_started += 1
            elif "phase completed:" in obs_lower:
                phases_completed += 1
            elif "phase failed:" in obs_lower:
                phases_failed += 1
            
            # Track latest activity
            last_activity = obs
        
        # Determine overall status
        if phases_failed > 0:
            status = "failed"
            health = "error"
        elif phases_started > phases_completed:
            status = "active"
            health = "healthy"
        elif phases_completed > 0:
            status = "completed" if phases_started == phases_completed else "paused"
            health = "healthy"
        else:
            status = "initialized"
            health = "healthy"
        
        return {
            "status": status,
            "phases_total": max(phases_started, phases_completed),
            "phases_completed": phases_completed,
            "phases_active": max(0, phases_started - phases_completed),
            "last_activity": last_activity,
            "created_at": created_at,
            "health": health
        }
    
    @handle_errors(operation_name="recover_interrupted_workflow", return_dict=False)
    def recover_interrupted_workflow(self, workflow_id: str) -> Optional[RecoveryPlan]:
        """Handle session recovery with comprehensive analysis"""
        
        try:
            # Get workflow context from Memory MCP
            context = self.memory_mcp.get_workflow_context(workflow_id)
            if not context:
                return RecoveryPlan(
                    workflow_id=workflow_id,
                    recovery_type="not_found",
                    current_phase=None,
                    next_phase=None,
                    context_available=False,
                    files_accessible=False,
                    recovery_actions=["Workflow not found - may need to recreate"],
                    estimated_recovery_time="N" / "A"
                )
            
            # Analyze context to determine recovery strategy
            observations = context.get("observations", [])
            workflow_config = context.get("workflow_config", {})
            
            # Determine current state
            current_phase_info = self._determine_current_phase(observations)
            next_phase_info = self._determine_next_phase(current_phase_info, workflow_config)
            
            # Check file accessibility
            files_accessible = self._check_files_accessibility(workflow_id, context)
            
            # Generate recovery plan
            recovery_plan = self._generate_recovery_plan(
                workflow_id,
                current_phase_info,
                next_phase_info,
                context,
                files_accessible
            )
            
            return recovery_plan
            
        except Exception as e:
            print(f"Recovery analysis failed for {workflow_id}: {str(e)}")
            return RecoveryPlan(
                workflow_id=workflow_id,
                recovery_type="error",
                current_phase=None,
                next_phase=None,
                context_available=False,
                files_accessible=False,
                recovery_actions=[f"Recovery failed: {str(e)}"],
                estimated_recovery_time="Manual intervention required"
            )
    
    def _determine_current_phase(self, observations: List[str]) -> Dict[str, Any]:
        """Determine current phase from observations"""
        
        started_phases = []
        completed_phases = []
        
        for obs in observations:
            if "phase started:" in obs.lower():
                # Extract phase name
                parts = obs.split("Phase started:")
                if len(parts) > 1:
                    phase_name = parts[1].split("(")[0].strip()
                    started_phases.append(phase_name)
            elif "phase completed:" in obs.lower():
                parts = obs.split("Phase completed:")
                if len(parts) > 1:
                    phase_name = parts[1].split(" |")[0].strip()
                    completed_phases.append(phase_name)
        
        # Determine current phase state
        if not started_phases:
            return {"phase": None, "status": "not_started"}
        
        current_phase = started_phases[-1]  # Most recent started phase
        
        if current_phase in completed_phases:
            return {"phase": current_phase, "status": "completed"}
        else:
            return {"phase": current_phase, "status": "interrupted"}
    
    def _determine_next_phase(self, current_phase_info: Dict[str, Any], workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Determine next phase based on current state"""
        
        phases = workflow_config.get("phases", [])
        if not phases:
            return {"phase": None, "available": False}
        
        current_phase = current_phase_info.get("phase")
        current_status = current_phase_info.get("status")
        
        if current_status == "not_started":
            # Start with first phase
            return {"phase": phases[0].get("name"), "available": True}
        elif current_status == "interrupted":
            # Resume current phase
            return {"phase": current_phase, "available": True}
        elif current_status == "completed":
            # Find next phase
            for i, phase in enumerate(phases):
                if phase.get("name") == current_phase and i + 1 < len(phases):
                    return {"phase": phases[i + 1].get("name"), "available": True}
            
            # All phases completed
            return {"phase": None, "available": False}
        
        return {"phase": None, "available": False}
    
    def _check_files_accessibility(self, workflow_id: str, context: Dict[str, Any]) -> bool:
        """Check if workflow files are accessible"""
        
        try:
            # Simple accessibility check via Files API
            # In real implementation, this would check actual file references
            workspace_info = context.get("workspace_info", {})
            if workspace_info:
                return True
            
            # Try to access any stored files for this workflow
            file_refs = [obs for obs in context.get("observations", []) if "file:" in obs.lower()]
            return len(file_refs) > 0
            
        except Exception:
            return False
    
    def _generate_recovery_plan(self, 
                               workflow_id: str, 
                               current_phase_info: Dict[str, Any], 
                               next_phase_info: Dict[str, Any], 
                               context: Dict[str, Any], 
                               files_accessible: bool) -> RecoveryPlan:
        """Generate comprehensive recovery plan"""
        
        current_phase = current_phase_info.get("phase")
        current_status = current_phase_info.get("status")
        next_phase = next_phase_info.get("phase")
        next_available = next_phase_info.get("available", False)
        
        # Determine recovery type
        if current_status == "not_started":
            recovery_type = "restart_workflow"
            recovery_actions = [
                "Load workflow configuration",
                "Initialize first phase",
                "Set up workspace"
            ]
            estimated_time = "1-2 minutes"
            
        elif current_status == "interrupted":
            recovery_type = "resume_phase"
            recovery_actions = [
                f"Resume interrupted phase: {current_phase}",
                "Restore agent context from Files API",
                "Continue from last checkpoint"
            ]
            estimated_time = "30 seconds"
            
        elif current_status == "completed" and next_available:
            recovery_type = "continue_next"
            recovery_actions = [
                f"Start next phase: {next_phase}",
                "Load previous deliverables",
                "Initialize agent context"
            ]
            estimated_time = "1 minute"
            
        else:
            recovery_type = "workflow_complete"
            recovery_actions = [
                "Workflow appears complete",
                "Review final deliverables",
                "Archive workflow context"
            ]
            estimated_time = "Complete"
        
        # Add file recovery actions if needed
        if not files_accessible and recovery_type != "workflow_complete":
            recovery_actions.append("WARNING: Some files may be inaccessible")
            recovery_actions.append("Verify workspace and Files API connectivity")
        
        return RecoveryPlan(
            workflow_id=workflow_id,
            recovery_type=recovery_type,
            current_phase=current_phase,
            next_phase=next_phase,
            context_available=True,
            files_accessible=files_accessible,
            recovery_actions=recovery_actions,
            estimated_recovery_time=estimated_time
        )
    
    @handle_errors(operation_name="export_workflow_summary", return_dict=False)
    def export_workflow_summary(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Export complete workflow summary for archival or reporting"""
        
        try:
            status = self.get_workflow_status(workflow_id)
            context = self.memory_mcp.get_workflow_context(workflow_id)
            
            if not status or not context:
                return None
            
            return {
                "workflow_id": workflow_id,
                "status": asdict(status),
                "full_context": context,
                "export_timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_phases": status.phases_total,
                    "completed_phases": status.phases_completed,
                    "success_rate": (status.phases_completed " / " status.phases_total * 100) if status.phases_total > 0 else 0,
                    "health_status": status.health
                }
            }
            
        except Exception as e:
            print(f"Export failed for {workflow_id}: {str(e)}")
            return None
    
    def cleanup_completed_workflows(self, older_than_days: int = 30) -> Dict[str, Any]:
        """Clean up old completed workflows (optional maintenance)"""
        
        # This would implement cleanup logic for old workflows
        # For now, return a placeholder response
        return {
            "cleanup_performed": False,
            "reason": "Manual cleanup recommended - automated cleanup not implemented",
            "suggestion": f"Review workflows older than {older_than_days} days manually"
        }
    
    def get_all_workflow_summaries(self) -> List[Dict[str, Any]]:
        """Get summaries of all workflows (for dashboard" / "overview)"""
        
        try:
            # This would search Memory MCP for all workflow entities
            # For now, return placeholder
            return [
                {
                    "message": "Workflow discovery not yet implemented",
                    "suggestion": "Access workflows by specific workflow_id"
                }
            ]
            
        except Exception as e:
            print(f"Workflow discovery failed: {str(e)}")
            return []