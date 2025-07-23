"""
Setup CLI Command - Core Logic
Workflow setup with multi-path support and comprehensive JSON validation
"""

import json
import hashlib
# import os  # Removed - was only used for sys.path.append
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

@handle_errors(operation_name="setup", return_dict=True)
def execute_setup(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main setup command execution with caching and error handling.
    
    Args:
        params: Command parameters including file_path or directory_path
        
    Returns:
        Standardized result dictionary with setup details
    """
    if not params or not params.get("path"):
        return {
            "success": False,
            "error": "Setup command requires a file or directory path",
            "error_type": "missing_path_parameter"
        }
    
    setup_path = params["path"]
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "setup")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute setup logic
    result = _execute_command_logic(params)
    
    # Cache result with shorter duration for setup operations
    cache.cache_content_analysis(cache_key, json.dumps(result), "setup")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if not params:
        return 0.002
    
    setup_path = params.get("path", "")
    path_obj = Path(setup_path)
    
    base_cost = 0.002  # Base setup operation cost
    
    # Add cost based on operation complexity
    if path_obj.is_file():
        # Single JSON file setup
        base_cost += 0.0005  # JSON validation cost
    elif path_obj.is_dir():
        # Directory setup - potentially multiple configs
        try:
            json_files = list(path_obj.glob("*.json"))
            base_cost += len(json_files) * 0.0005  # Per file validation
            base_cost += len(json_files) * 0.0001  # Per directory operation
        except (OSError, PermissionError):
            base_cost += 0.001  # Error handling overhead
    
    # Add state management costs
    base_cost += 0.001  # Workflow state initialization
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including file system state"""
    if not params:
        return "setup_no_params"
    
    setup_path = params.get("path", "")
    base_key = f"setup|{setup_path}"
    
    # Add file system fingerprints
    try:
        path_obj = Path(setup_path)
        if path_obj.exists():
            # Include modification time and size for cache invalidation
            stat_info = path_obj.stat()
            fingerprint = f"{stat_info.st_mtime}_{stat_info.st_size}"
            base_key += f"|{fingerprint}"
            
            # For directories, include content fingerprint
            if path_obj.is_dir():
                json_files = list(path_obj.glob("*.json"))
                content_hash = hashlib.md5(str(sorted([f.name for f in json_files])).encode()).hexdigest()[:8]
                base_key += f"|dir_{content_hash}"
    except (OSError, PermissionError):
        base_key += "|inaccessible"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any]) -> Dict[str, Any]:
    """Core setup logic implementation with multi-path support"""
    setup_path = params["path"]
    path_obj = Path(setup_path).resolve()
    
    # Validate path exists and is accessible
    if not path_obj.exists():
        return {
            "success": False,
            "error": f"Path does not exist: {setup_path}",
            "error_type": "path_not_found"
        }
    
    # Initialize managers
    workflow_manager = WorkflowManager()
    workflow_state = WorkflowStateManager()
    memory_mcp = MemoryMCPManager()
    
    try:
        if path_obj.is_file():
            # Single JSON file setup
            return _setup_from_file(path_obj, workflow_manager, workflow_state, memory_mcp)
        elif path_obj.is_dir():
            # Directory-based setup
            return _setup_from_directory(path_obj, workflow_manager, workflow_state, memory_mcp)
        else:
            return {
                "success": False,
                "error": f"Path is neither file nor directory: {setup_path}",
                "error_type": "invalid_path_type"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Setup failed: {str(e)}",
            "error_type": "setup_execution_error",
            "path": str(path_obj)
        }

def _setup_from_file(config_file: Path, workflow_manager: WorkflowManager, 
                    workflow_state: WorkflowStateManager, memory_mcp: MemoryMCPManager) -> Dict[str, Any]:
    """Setup workflow from single JSON configuration file"""
    
    # Validate JSON file
    validation_result = _validate_workflow_config(config_file)
    if not validation_result["valid"]:
        return {
            "success": False,
            "error": f"Invalid workflow configuration: {validation_result['error']}",
            "error_type": "config_validation_error",
            "file": str(config_file)
        }
    
    config_data = validation_result["config"]
    workflow_data = config_data.get("workflow", [{}])[0] if config_data.get("workflow") else config_data
    
    # Extract workflow information
    workflow_id = workflow_data.get("workflow_id")
    custom_command = workflow_data.get("custom_command")
    workflow_goal = workflow_data.get("workflow_goal", "")
    
    if not workflow_id or not custom_command:
        return {
            "success": False,
            "error": "Configuration missing required fields: workflow_id and / or custom_command",
            "error_type": "missing_required_fields"
        }
    
    # Create workflow directory structure
    workflows_dir = Path(__file__).parent.parent.parent  /  "configs"  /  "workflows"
    workflow_dir = workflows_dir  /  custom_command
    
    setup_result = _create_workflow_structure(workflow_dir, config_data, config_file)
    if not setup_result["success"]:
        return setup_result
    
    # Initialize workflow state tracking
    try:
        # Create workflow context in Memory MCP
        memory_mcp.create_workflow_context(workflow_id, workflow_goal)
        
        # Track setup progress
        workflow_state.track_workflow_progress(workflow_id, f"Setup completed from file: {config_file.name}")
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "custom_command": custom_command,
            "workflow_directory": str(workflow_dir),
            "source_file": str(config_file),
            "setup_type": "single_file",
            "created_structure": setup_result["created_files"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to initialize workflow tracking: {str(e)}",
            "error_type": "tracking_initialization_error"
        }

def _setup_from_directory(workflow_dir: Path, workflow_manager: WorkflowManager,
                         workflow_state: WorkflowStateManager, memory_mcp: MemoryMCPManager) -> Dict[str, Any]:
    """Setup workflow from directory containing configuration files"""
    
    # Find workflow configuration files
    config_files = list(workflow_dir.glob("*_workflow_config.json"))
    if not config_files:
        # Look for any workflow-related JSON files
        config_files = [f for f in workflow_dir.glob("*.json") if "workflow" in f.name.lower()]
    
    if not config_files:
        return {
            "success": False,
            "error": "No workflow configuration files found in directory",
            "error_type": "no_config_files",
            "directory": str(workflow_dir)
        }
    
    # Use the first valid configuration file
    main_config = None
    validation_errors = []
    
    for config_file in config_files:
        validation_result = _validate_workflow_config(config_file)
        if validation_result["valid"]:
            main_config = config_file
            config_data = validation_result["config"]
            break
        else:
            validation_errors.append(f"{config_file.name}: {validation_result['error']}")
    
    if not main_config:
        return {
            "success": False,
            "error": "No valid workflow configuration found",
            "error_type": "no_valid_config",
            "validation_errors": validation_errors
        }
    
    # Extract workflow information
    workflow_data = config_data.get("workflow", [{}])[0] if config_data.get("workflow") else config_data
    workflow_id = workflow_data.get("workflow_id")
    custom_command = workflow_data.get("custom_command")
    workflow_goal = workflow_data.get("workflow_goal", "")
    
    if not workflow_id or not custom_command:
        return {
            "success": False,
            "error": "Configuration missing required fields: workflow_id and / or custom_command",
            "error_type": "missing_required_fields"
        }
    
    # Create proper workflow directory structure if not already in workflows directory
    workflows_base_dir = Path(__file__).parent.parent.parent  /  "configs"  /  "workflows"
    
    if workflow_dir.parent != workflows_base_dir:
        # Copy/move to proper location
        target_dir = workflows_base_dir  /  custom_command
        copy_result = _copy_workflow_directory(workflow_dir, target_dir)
        if not copy_result["success"]:
            return copy_result
        final_workflow_dir = target_dir
    else:
        final_workflow_dir = workflow_dir
    
    # Initialize workflow state tracking
    try:
        # Create workflow context in Memory MCP
        memory_mcp.create_workflow_context(workflow_id, workflow_goal)
        
        # Track setup progress
        workflow_state.track_workflow_progress(workflow_id, f"Setup completed from directory: {workflow_dir.name}")
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "custom_command": custom_command,
            "workflow_directory": str(final_workflow_dir),
            "source_directory": str(workflow_dir),
            "main_config_file": main_config.name,
            "setup_type": "directory",
            "config_files_found": [f.name for f in config_files],
            "validation_errors": validation_errors if validation_errors else None,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to initialize workflow tracking: {str(e)}",
            "error_type": "tracking_initialization_error"
        }

def _validate_workflow_config(config_file: Path) -> Dict[str, Any]:
    """Validate workflow configuration JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Basic structure validation
        if not isinstance(config_data, dict):
            return {"valid": False, "error": "Configuration must be a JSON object"}
        
        # Check for workflow data
        workflow_data = config_data.get("workflow", [{}])[0] if config_data.get("workflow") else config_data
        
        required_fields = ["workflow_id", "custom_command"]
        missing_fields = [field for field in required_fields if not workflow_data.get(field)]
        
        if missing_fields:
            return {
                "valid": False, 
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        return {"valid": True, "config": config_data}
        
    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"Invalid JSON: {str(e)}"}
    except (OSError, PermissionError) as e:
        return {"valid": False, "error": f"Cannot read file: {str(e)}"}

def _create_workflow_structure(workflow_dir: Path, config_data: Dict, source_file: Path) -> Dict[str, Any]:
    """Create proper workflow directory structure"""
    try:
        # Create main workflow directory
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard subdirectories
        subdirs = ["config-files", "deliverables", "metadata"]
        created_files = []
        
        for subdir in subdirs:
            subdir_path = workflow_dir / subdir
            subdir_path.mkdir(exist_ok=True)
            created_files.append(str(subdir_path))
        
        # Copy configuration file to config-files directory
        config_dir = workflow_dir  /  "config-files"
        target_config = config_dir  /  source_file.name
        
        import shutil
        shutil.copy2(source_file, target_config)
        created_files.append(str(target_config))
        
        return {
            "success": True,
            "created_files": created_files
        }
        
    except (OSError, PermissionError) as e:
        return {
            "success": False,
            "error": f"Failed to create workflow structure: {str(e)}",
            "error_type": "directory_creation_error"
        }

def _copy_workflow_directory(source_dir: Path, target_dir: Path) -> Dict[str, Any]:
    """Copy workflow directory to proper location"""
    try:
        import shutil
        
        if target_dir.exists():
            return {
                "success": False,
                "error": f"Target directory already exists: {target_dir}",
                "error_type": "target_exists"
            }
        
        shutil.copytree(source_dir, target_dir)
        
        return {
            "success": True,
            "source": str(source_dir),
            "target": str(target_dir)
        }
        
    except (OSError, PermissionError, shutil.Error) as e:
        return {
            "success": False,
            "error": f"Failed to copy workflow directory: {str(e)}",
            "error_type": "directory_copy_error"
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_setup(params)