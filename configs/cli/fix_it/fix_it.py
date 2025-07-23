"""
Fix_it CLI Command - Core Logic
Workflow correction with automatic JSON copying logic
"""

import json
import hashlib
import shutil
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Orchestrator integration imports
from orchestrator.workflow_manager import WorkflowManager
from orchestrator.workflow_state import WorkflowStateManager
from orchestrator.memory_mcp import MemoryMCPManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="fix_it", return_dict=True)
def execute_fix_it(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main fix_it command execution with caching and error handling.
    Implements automatic JSON copying logic and workflow correction.
    
    Args:
        params: Command parameters including file_path and optional flags
        
    Returns:
        Standardized result dictionary with fix details
    """
    if not params or not params.get("path"):
        return {
            "success": False,
            "error": "Fix_it command requires a JSON file path",
            "error_type": "missing_path_parameter"
        }
    
    fix_path = params["path"]
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "fix_it")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute fix_it logic
    result = _execute_command_logic(params)
    
    # Cache result with shorter duration for fix operations
    cache.cache_content_analysis(cache_key, json.dumps(result), "fix_it")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if not params:
        return 0.005  # Base fix operation cost
    
    base_cost = 0.005  # Base fix operation
    
    # Add cost for JSON file analysis
    fix_path = params.get("path", "")
    if fix_path:
        base_cost += 0.002  # JSON validation and analysis
    
    # Add cost for workflow state operations
    base_cost += 0.003  # Workflow state recovery
    
    # Add cost for file operations if JSON copying is needed
    if _needs_json_copying(params):
        base_cost += 0.001  # File copy operations
    
    # Add cost for workflow correction complexity
    base_cost += 0.004  # Phase re-execution and error recovery
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including file system state"""
    if not params:
        return "fix_it_no_params"
    
    fix_path = params.get("path", "")
    base_key = f"fix_it|{fix_path}"
    
    # Add file modification time for cache invalidation
    try:
        if fix_path and Path(fix_path).exists():
            mtime = Path(fix_path).stat().st_mtime
            base_key += f"|mtime:{mtime}"
    except (OSError, PermissionError):
        base_key += "|no_file_access"
    
    # Add current directory context
    current_dir = Path.cwd()
    base_key += f"|cwd:{str(current_dir)}"
    
    # Add workflow state fingerprint
    try:
        workflow_manager = WorkflowManager()
        workflow_context = workflow_manager.get_current_workflow_context()
        if workflow_context.get("workflow_id"):
            base_key += f"|workflow:{workflow_context['workflow_id']}"
    except Exception:
        base_key += "|no_workflow_context"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any]) -> Dict[str, Any]:
    """Core fix_it command logic implementation"""
    fix_path = params["path"]
    
    try:
        # Initialize managers
        workflow_manager = WorkflowManager()
        state_manager = WorkflowStateManager()
        memory_manager = MemoryMCPManager()
        
        # Step 1: Validate JSON file
        json_validation = _validate_fix_json(fix_path)
        if not json_validation["valid"]:
            return {
                "success": False,
                "error": f"Invalid fix JSON: {json_validation['error']}",
                "error_type": "json_validation_error"
            }
        
        fix_config = json_validation["data"]
        
        # Step 2: Handle automatic JSON copying logic
        copying_result = _handle_json_copying(fix_path, fix_config)
        if not copying_result["success"]:
            return copying_result
        
        # Step 3: Perform workflow correction
        correction_result = _perform_workflow_correction(
            fix_config, 
            workflow_manager, 
            state_manager, 
            memory_manager
        )
        
        # Step 4: Update workflow state
        state_update = _update_workflow_state(
            fix_config, 
            correction_result, 
            state_manager
        )
        
        return {
            "success": True,
            "fix_applied": True,
            "json_copied": copying_result.get("json_copied", False),
            "target_directory": copying_result.get("target_directory"),
            "phases_corrected": correction_result.get("phases_corrected", []),
            "workflow_state": state_update,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Fix operation failed: {str(e)}",
            "error_type": "fix_execution_error"
        }

def _validate_fix_json(json_path: str) -> Dict[str, Any]:
    """Validate fix JSON file structure and content"""
    try:
        json_file = Path(json_path)
        if not json_file.exists():
            return {"valid": False, "error": f"JSON file not found: {json_path}"}
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Required fields for fix operations
        required_fields = ["workflow_id", "phase_to_fix", "fix_type"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                "valid": False, 
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        # Validate fix_type
        valid_fix_types = ["re_run_phase", "correct_deliverable", "update_parameters", "resume_workflow"]
        if data["fix_type"] not in valid_fix_types:
            return {
                "valid": False,
                "error": f"Invalid fix_type. Must be one of: {', '.join(valid_fix_types)}"
            }
        
        return {"valid": True, "data": data}
        
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"Invalid JSON format: {str(e)}"}
    except Exception as e:
        return {"valid": False, "error": f"JSON validation error: {str(e)}"}

def _needs_json_copying(params: Dict[str, Any]) -> bool:
    """Determine if JSON copying is needed based on execution context"""
    fix_path = params.get("path", "")
    if not fix_path:
        return False
    
    try:
        # Check if we're in a workflow directory
        current_dir = Path.cwd()
        json_file = Path(fix_path)
        
        # If JSON file is not in current directory, copying might be needed
        if json_file.parent != current_dir:
            # Check if current directory has workflow indicators
            workflow_indicators = [
                "workflow_config.json",
                "workflow_state.json",
                ".workflow_id",
                "phases" / ""
            ]
            
            has_workflow_indicators = any(
                (current_dir / indicator).exists() 
                for indicator in workflow_indicators
            )
            
            return not has_workflow_indicators
        
        return False
        
    except Exception:
        return False

def _handle_json_copying(json_path: str, fix_config: Dict[str, Any]) -> Dict[str, Any]:
    """Handle automatic JSON copying logic if needed"""
    try:
        json_file = Path(json_path)
        current_dir = Path.cwd()
        
        # Check if copying is needed
        if not _needs_json_copying({"path": json_path}):
            return {
                "success": True,
                "json_copied": False,
                "target_directory": str(current_dir)
            }
        
        # Determine target directory based on workflow_id
        workflow_id = fix_config.get("workflow_id")
        if not workflow_id:
            return {
                "success": False,
                "error": "Cannot determine target directory without workflow_id"
            }
        
        # Find or create workflow directory
        workflow_manager = WorkflowManager()
        workflow_dir = workflow_manager.get_workflow_directory(workflow_id)
        
        if not workflow_dir:
            # Create workflow directory if it doesn't exist
            workflows_base = Path(__file__).parent.parent.parent " / " "workflows"
            workflow_dir = workflows_base / workflow_id
            workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy JSON file to workflow directory
        target_path = Path(workflow_dir) " / " json_file.name
        shutil.copy2(json_file, target_path)
        
        return {
            "success": True,
            "json_copied": True,
            "source_path": str(json_file),
            "target_path": str(target_path),
            "target_directory": str(workflow_dir)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"JSON copying failed: {str(e)}"
        }

def _perform_workflow_correction(
    fix_config: Dict[str, Any], 
    workflow_manager: WorkflowManager,
    state_manager: WorkflowStateManager,
    memory_manager: MemoryMCPManager
) -> Dict[str, Any]:
    """Perform the actual workflow correction based on fix configuration"""
    try:
        workflow_id = fix_config["workflow_id"]
        phase_to_fix = fix_config["phase_to_fix"]
        fix_type = fix_config["fix_type"]
        
        # Get current workflow state
        workflow_state = state_manager.get_workflow_state(workflow_id)
        if not workflow_state:
            return {
                "success": False,
                "error": f"Workflow state not found for ID: {workflow_id}"
            }
        
        phases_corrected = []
        
        if fix_type == "re_run_phase":
            # Re-run the specified phase
            phase_result = _re_run_workflow_phase(
                workflow_id, phase_to_fix, fix_config, workflow_manager
            )
            if phase_result["success"]:
                phases_corrected.append(phase_to_fix)
        
        elif fix_type == "correct_deliverable":
            # Correct specific deliverable issues
            deliverable_result = _correct_phase_deliverable(
                workflow_id, phase_to_fix, fix_config, workflow_manager
            )
            if deliverable_result["success"]:
                phases_corrected.append(phase_to_fix)
        
        elif fix_type == "update_parameters":
            # Update phase parameters and re-run
            param_result = _update_phase_parameters(
                workflow_id, phase_to_fix, fix_config, workflow_manager
            )
            if param_result["success"]:
                phases_corrected.append(phase_to_fix)
        
        elif fix_type == "resume_workflow":
            # Resume workflow from specified phase
            resume_result = _resume_workflow_from_phase(
                workflow_id, phase_to_fix, fix_config, state_manager
            )
            if resume_result["success"]:
                phases_corrected.extend(resume_result.get("phases_resumed", []))
        
        return {
            "success": True,
            "phases_corrected": phases_corrected,
            "fix_type": fix_type,
            "workflow_id": workflow_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Workflow correction failed: {str(e)}"
        }

def _re_run_workflow_phase(
    workflow_id: str, 
    phase_name: str, 
    fix_config: Dict[str, Any],
    workflow_manager: WorkflowManager
) -> Dict[str, Any]:
    """Re-run a specific workflow phase"""
    try:
        # Get phase configuration
        phase_config = workflow_manager.get_phase_config(workflow_id, phase_name)
        if not phase_config:
            return {
                "success": False,
                "error": f"Phase configuration not found: {phase_name}"
            }
        
        # Apply any parameter overrides from fix config
        if "parameter_overrides" in fix_config:
            phase_config.update(fix_config["parameter_overrides"])
        
        # Execute phase re-run
        execution_result = workflow_manager.execute_phase(
            workflow_id, phase_name, phase_config
        )
        
        return {
            "success": execution_result.get("success", False),
            "phase_name": phase_name,
            "execution_details": execution_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Phase re-run failed: {str(e)}"
        }

def _correct_phase_deliverable(
    workflow_id: str, 
    phase_name: str, 
    fix_config: Dict[str, Any],
    workflow_manager: WorkflowManager
) -> Dict[str, Any]:
    """Correct specific deliverable issues in a phase"""
    try:
        # Get deliverable corrections from fix config
        corrections = fix_config.get("deliverable_corrections", {})
        if not corrections:
            return {
                "success": False,
                "error": "No deliverable corrections specified in fix config"
            }
        
        # Apply corrections to phase deliverables
        correction_result = workflow_manager.apply_deliverable_corrections(
            workflow_id, phase_name, corrections
        )
        
        return {
            "success": correction_result.get("success", False),
            "phase_name": phase_name,
            "corrections_applied": corrections,
            "correction_details": correction_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Deliverable correction failed: {str(e)}"
        }

def _update_phase_parameters(
    workflow_id: str, 
    phase_name: str, 
    fix_config: Dict[str, Any],
    workflow_manager: WorkflowManager
) -> Dict[str, Any]:
    """Update phase parameters and re-run"""
    try:
        # Get parameter updates from fix config
        parameter_updates = fix_config.get("parameter_updates", {})
        if not parameter_updates:
            return {
                "success": False,
                "error": "No parameter updates specified in fix config"
            }
        
        # Update phase parameters
        update_result = workflow_manager.update_phase_parameters(
            workflow_id, phase_name, parameter_updates
        )
        
        if update_result.get("success"):
            # Re-run phase with updated parameters
            rerun_result = _re_run_workflow_phase(
                workflow_id, phase_name, fix_config, workflow_manager
            )
            return rerun_result
        
        return update_result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Parameter update failed: {str(e)}"
        }

def _resume_workflow_from_phase(
    workflow_id: str, 
    phase_name: str, 
    fix_config: Dict[str, Any],
    state_manager: WorkflowStateManager
) -> Dict[str, Any]:
    """Resume workflow execution from specified phase"""
    try:
        # Resume workflow state from the specified phase
        resume_result = state_manager.resume_workflow_from_phase(
            workflow_id, phase_name
        )
        
        return {
            "success": resume_result.get("success", False),
            "phases_resumed": resume_result.get("phases_resumed", []),
            "resume_details": resume_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Workflow resume failed: {str(e)}"
        }

def _update_workflow_state(
    fix_config: Dict[str, Any],
    correction_result: Dict[str, Any],
    state_manager: WorkflowStateManager
) -> Dict[str, Any]:
    """Update workflow state after fix operations"""
    try:
        workflow_id = fix_config["workflow_id"]
        
        # Prepare state update
        state_update = {
            "last_fix_applied": datetime.now().isoformat(),
            "fix_type": fix_config["fix_type"],
            "phases_corrected": correction_result.get("phases_corrected", []),
            "fix_successful": correction_result.get("success", False)
        }
        
        # Apply state update
        update_result = state_manager.update_workflow_state(
            workflow_id, state_update
        )
        
        return update_result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"State update failed: {str(e)}"
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_fix_it(params)