"""
Doctor CLI Command - Core Logic
System health checks and workflow diagnostics
"""

import json
import hashlib
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="doctor", return_dict=True)
def execute_doctor(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main doctor command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary with system health diagnostics
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "doctor")
    if cached_result:
        cached_data = json.loads(cached_result)
        # Check if cached data is still fresh (5 minutes for system diagnostics)
        if _is_cache_fresh(cached_data, minutes=5):
            return cached_data
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 5 minutes (system state changes moderately)
    cache.cache_content_analysis(cache_key, json.dumps(result), "doctor")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure with medium cost for system diagnostics.
    """
    # Medium cost for comprehensive system health checks and diagnostics
    return 0.005

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including system state"""
    base_key = f"doctor|{str(params) if params else 'none'}"
    
    # Add system state fingerprints for system health caching
    config_dir = Path(__file__).parent.parent.parent / "configs"
    orchestrator_dir = Path(__file__).parent.parent.parent / "orchestrator"
    
    fingerprints = []
    
    # Include configuration directory state
    if config_dir.exists():
        dir_stat = config_dir.stat()
        fingerprints.append(f"config:{dir_stat.st_mtime}")
    
    # Include orchestrator directory state
    if orchestrator_dir.exists():
        dir_stat = orchestrator_dir.stat()
        fingerprints.append(f"orchestrator:{dir_stat.st_mtime}")
    
    # Include system Python version and path info
    fingerprints.append(f"python:{sys.version_info.major}.{sys.version_info.minor}")
    
    # Create combined fingerprint
    if fingerprints:
        combined_fingerprint = "|".join(fingerprints)
        base_key += f"|sys:{hashlib.md5(combined_fingerprint.encode()).hexdigest()[:8]}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _is_cache_fresh(cached_data: Dict[str, Any], minutes: int = 5) -> bool:
    """Check if cached data is still fresh for system diagnostics"""
    try:
        from datetime import timedelta
        cached_time = datetime.fromisoformat(cached_data.get("timestamp", ""))
        age_limit = datetime.now() - timedelta(minutes=minutes)
        return cached_time > age_limit
    except (ValueError, TypeError):
        return False

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core doctor command logic implementation"""
    try:
        # Perform comprehensive system health checks
        health_results = {
            "system_info": _check_system_info(),
            "directory_structure": _check_directory_structure(),
            "workflow_manager": _check_workflow_manager(),
            "memory_mcp": _check_memory_mcp(),
            "workflow_state": _check_workflow_state(),
            "cache_system": _check_cache_system(),
            "orchestrator_files": _check_orchestrator_files()
        }
        
        # Analyze overall health status
        overall_status = _analyze_overall_health(health_results)
        
        # Generate actionable insights
        insights = _generate_insights(health_results)
        
        return {
            "success": True,
            "overall_status": overall_status,
            "health_checks": health_results,
            "insights": insights,
            "summary": _generate_summary(health_results, overall_status),
            "timestamp": datetime.now().isoformat(),
            "diagnostic_version": "1.0"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"System diagnostic failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "diagnostic_version": "1.0"
        }

def _check_system_info() -> Dict[str, Any]:
    """Check basic system information and Python environment"""
    try:
        return {
            "status": "healthy",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "python_executable": sys.executable,
            "platform": sys.platform,
            "working_directory": os.getcwd(),
            "path_accessible": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "details": "Failed to gather basic system information"
        }

def _check_directory_structure() -> Dict[str, Any]:
    """Check essential directory structure integrity"""
    try:
        base_path = Path(__file__).parent.parent.parent
        required_dirs = [
            "configs",
            "configs/cli", 
            "configs/workflows",
            "orchestrator",
            "tools",
            "scripts"
        ]
        
        missing_dirs = []
        present_dirs = []
        
        for dir_name in required_dirs:
            dir_path = base_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                present_dirs.append(dir_name)
            else:
                missing_dirs.append(dir_name)
        
        status = "healthy" if not missing_dirs else "warning" if len(missing_dirs) < 3 else "error"
        
        return {
            "status": status,
            "present_directories": present_dirs,
            "missing_directories": missing_dirs,
            "total_required": len(required_dirs),
            "total_present": len(present_dirs)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "details": "Failed to check directory structure"
        }

def _check_workflow_manager() -> Dict[str, Any]:
    """Check workflow manager functionality"""
    try:
        # Import and test workflow manager
        from orchestrator.workflow_manager import WorkflowManager
        
        manager = WorkflowManager()
        
        # Test workflow ID generation
        id_result = manager.generate_workflow_id()
        
        # Check workflow directory
        workflows_dir = Path(__file__).parent.parent.parent / "configs" / "workflows"
        
        return {
            "status": "healthy",
            "import_successful": True,
            "id_generation_working": id_result.get("success", False),
            "workflow_directory_exists": workflows_dir.exists(),
            "manager_instance_created": True,
            "last_test_id": id_result.get("workflow_id", "N/A")
        }
        
    except ImportError as e:
        return {
            "status": "error",
            "import_successful": False,
            "error": f"Import failed: {str(e)}",
            "details": "WorkflowManager could not be imported"
        }
    except Exception as e:
        return {
            "status": "warning",
            "import_successful": True,
            "error": str(e),
            "details": "WorkflowManager imported but functionality test failed"
        }

def _check_memory_mcp() -> Dict[str, Any]:
    """Check Memory MCP manager functionality"""
    try:
        # Import and test memory MCP
        from orchestrator.memory_mcp import MemoryMCPManager
        
        manager = MemoryMCPManager()
        
        # Test cost estimation
        test_params = {"num_workflows": 1, "state_updates": 5}
        cost_estimate = manager.estimate_cost(test_params)
        
        return {
            "status": "healthy",
            "import_successful": True,
            "manager_instance_created": True,
            "cost_estimation_working": isinstance(cost_estimate, (int, float)),
            "cache_system_available": hasattr(manager, 'cache'),
            "test_cost_estimate": cost_estimate
        }
        
    except ImportError as e:
        return {
            "status": "error",
            "import_successful": False,
            "error": f"Import failed: {str(e)}",
            "details": "MemoryMCPManager could not be imported"
        }
    except Exception as e:
        return {
            "status": "warning",
            "import_successful": True,
            "error": str(e),
            "details": "MemoryMCPManager imported but functionality test failed"
        }

def _check_workflow_state() -> Dict[str, Any]:
    """Check workflow state management functionality"""
    try:
        # Import and test workflow state
        from orchestrator.workflow_state import WorkflowState
        
        # Test basic instantiation
        state = WorkflowState()
        
        return {
            "status": "healthy",
            "import_successful": True,
            "state_instance_created": True,
            "memory_integration_available": hasattr(state, 'memory_mcp') if hasattr(state, '__dict__') else True
        }
        
    except ImportError as e:
        return {
            "status": "error", 
            "import_successful": False,
            "error": f"Import failed: {str(e)}",
            "details": "WorkflowState could not be imported"
        }
    except Exception as e:
        return {
            "status": "warning",
            "import_successful": True,
            "error": str(e),
            "details": "WorkflowState imported but instantiation failed"
        }

def _check_cache_system() -> Dict[str, Any]:
    """Check cache system functionality"""
    try:
        # Test cache system operations
        test_key = f"doctor_test_{datetime.now().timestamp()}"
        test_data = {"test": True, "timestamp": datetime.now().isoformat()}
        
        # Test cache set
        cache.cache_content_analysis(test_key, json.dumps(test_data), "doctor_test")
        
        # Test cache get
        cached_result = cache.get_cached_analysis(test_key, "doctor_test")
        
        # Cleanup test data
        try:
            cache.clear_component_cache("doctor_test")
        except:
            pass  # Cleanup not critical for diagnostic
        
        return {
            "status": "healthy",
            "cache_instance_available": True,
            "set_operation_working": True,
            "get_operation_working": cached_result is not None,
            "data_integrity": cached_result == json.dumps(test_data) if cached_result else False
        }
        
    except Exception as e:
        return {
            "status": "error",
            "cache_instance_available": cache is not None,
            "error": str(e),
            "details": "Cache system test operations failed"
        }

def _check_orchestrator_files() -> Dict[str, Any]:
    """Check critical orchestrator files availability"""
    try:
        orchestrator_dir = Path(__file__).parent.parent.parent / "orchestrator"
        critical_files = [
            "core.py",
            "cli_manager.py", 
            "workflow_manager.py",
            "memory_mcp.py",
            "workflow_state.py",
            "error_handling.py",
            "cache/cache_system.py"
        ]
        
        missing_files = []
        present_files = []
        
        for file_name in critical_files:
            file_path = orchestrator_dir / file_name
            if file_path.exists() and file_path.is_file():
                present_files.append(file_name)
            else:
                missing_files.append(file_name)
        
        status = "healthy" if not missing_files else "warning" if len(missing_files) < 3 else "error"
        
        return {
            "status": status,
            "present_files": present_files,
            "missing_files": missing_files,
            "total_critical": len(critical_files),
            "total_present": len(present_files),
            "orchestrator_directory_exists": orchestrator_dir.exists()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "details": "Failed to check orchestrator files"
        }

def _analyze_overall_health(health_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze overall system health from individual check results"""
    status_counts = {"healthy": 0, "warning": 0, "error": 0}
    total_checks = len(health_results)
    
    for check_name, check_result in health_results.items():
        status = check_result.get("status", "error")
        status_counts[status] += 1
    
    # Determine overall status
    if status_counts["error"] > 0:
        overall_status = "critical" if status_counts["error"] > total_checks // 2 else "degraded"
    elif status_counts["warning"] > 0:
        overall_status = "warning"
    else:
        overall_status = "healthy"
    
    return {
        "overall_status": overall_status,
        "health_score": (status_counts["healthy"] / total_checks) * 100,
        "checks_passed": status_counts["healthy"],
        "checks_warning": status_counts["warning"],
        "checks_failed": status_counts["error"],
        "total_checks": total_checks
    }

def _generate_insights(health_results: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate actionable insights based on health check results"""
    insights = []
    
    for check_name, check_result in health_results.items():
        status = check_result.get("status", "error")
        
        if status == "error":
            insights.append({
                "type": "error",
                "component": check_name,
                "message": f"{check_name.replace('_', ' ').title()} requires immediate attention",
                "details": check_result.get("error", "Unknown error"),
                "action": _get_remediation_action(check_name, check_result)
            })
        elif status == "warning":
            insights.append({
                "type": "warning",
                "component": check_name,
                "message": f"{check_name.replace('_', ' ').title()} has minor issues",
                "details": check_result.get("error", "Check results show warnings"),
                "action": _get_remediation_action(check_name, check_result)
            })
    
    # Add positive insights for healthy systems
    if not insights:
        insights.append({
            "type": "success",
            "component": "overall",
            "message": "All system components are functioning properly",
            "details": "No issues detected in system health diagnostics",
            "action": "Continue normal operations"
        })
    
    return insights

def _get_remediation_action(check_name: str, check_result: Dict[str, Any]) -> str:
    """Get specific remediation actions for failed checks"""
    remediation_map = {
        "system_info": "Check Python installation and system environment",
        "directory_structure": "Verify Mao installation integrity and recreate missing directories",
        "workflow_manager": "Check orchestrator.workflow_manager module installation and dependencies",
        "memory_mcp": "Verify orchestrator.memory_mcp module installation and configuration",
        "workflow_state": "Check orchestrator.workflow_state module installation",
        "cache_system": "Verify cache system configuration and permissions",
        "orchestrator_files": "Reinstall or repair missing orchestrator components"
    }
    
    return remediation_map.get(check_name, "Consult system documentation for troubleshooting steps")

def _generate_summary(health_results: Dict[str, Dict[str, Any]], overall_status: Dict[str, Any]) -> str:
    """Generate human-readable summary of system health"""
    status = overall_status["overall_status"]
    health_score = overall_status["health_score"]
    
    if status == "healthy":
        return f"System is healthy with {health_score:.1f}% of checks passing. All components are functioning properly."
    elif status == "warning":
        return f"System is functional with {health_score:.1f}% health score, but some components have warnings that should be addressed."
    elif status == "degraded":
        return f"System is degraded with {health_score:.1f}% health score. Multiple components have issues that may affect functionality."
    else:  # critical
        return f"System is in critical condition with {health_score:.1f}% health score. Immediate attention required to restore functionality."

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_doctor(params)