"""
Update CLI Command - Core Logic
Enhanced workflow update with multi-path support and secondary flags
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
from orchestrator.workflow_manager import WorkflowManager
from orchestrator.workflow_state import WorkflowStateManager
from orchestrator.memory_mcp import MemoryMCPManager

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="update", return_dict=True)
def execute_update(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main update command execution with caching and error handling.
    Supports multi-path and secondary flags for comprehensive workflow updates.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary
    """
    if not params:
        params = {}
    
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result with appropriate duration (5 minutes for file operations)
    cache.set(cache_key, result, duration=300)
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if not params:
        return 0.005  # Base update operation cost
    
    base_cost = 0.005  # Base update operation
    
    # Add cost for JSON analysis
    if params.get("json_file"):
        base_cost += 0.002
    
    # Add cost for multi-path operations
    if params.get("source_path") != params.get("target_path"):
        base_cost += 0.001
    
    # Add cost for secondary flags
    secondary_flags = ["add", "remove", "replace", "rename", "chat"]
    for flag in secondary_flags:
        if params.get(flag):
            flag_costs = {
                "add": 0.003,
                "remove": 0.002,
                "replace": 0.005,
                "rename": 0.003,
                "chat": 0.008
            }
            base_cost += flag_costs.get(flag, 0.003)
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including system state"""
    if not params:
        params = {}
    
    base_key = f"update|{str(params)}"
    
    # Add file modification times for dependency tracking
    file_path = params.get("json_file")
    if file_path and Path(file_path).exists():
        mtime = Path(file_path).stat().st_mtime
        base_key += f"|mtime:{mtime}"
    
    # Add directory state fingerprint
    target_dir = params.get("target_directory")
    if target_dir and Path(target_dir).exists():
        dir_mtime = Path(target_dir).stat().st_mtime
        base_key += f"|dir_mtime:{dir_mtime}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core command logic implementation"""
    if not params:
        return {"success": False, "error": "No parameters provided"}
    
    try:
        # Initialize managers
        workflow_manager = WorkflowManager()
        workflow_state = WorkflowStateManager()
        memory_mcp = MemoryMCPManager()
        
        # Extract parameters
        json_file = params.get("json_file")
        target_directory = params.get("target_directory")
        secondary_flags = _extract_secondary_flags(params)
        
        if not json_file:
            return {"success": False, "error": "JSON file path required"}
        
        # Validate and resolve paths
        path_info = _resolve_paths(json_file, target_directory)
        if not path_info["success"]:
            return path_info
        
        # Load and validate JSON
        json_data = _load_and_validate_json(path_info["json_path"])
        if not json_data["success"]:
            return json_data
        
        # Apply secondary flag modifications
        if secondary_flags:
            json_data = _apply_secondary_flags(json_data["data"], secondary_flags)
            if not json_data["success"]:
                return json_data
        
        # Execute the update
        result = _execute_workflow_update(
            json_data["data"], 
            path_info["target_path"], 
            workflow_manager, 
            workflow_state, 
            memory_mcp
        )
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Update execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def _extract_secondary_flags(params: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and organize secondary flags"""
    flags = {}
    
    secondary_flag_keys = ["add", "remove", "replace", "rename", "chat"]
    for flag in secondary_flag_keys:
        if flag in params and params[flag]:
            flags[flag] = params[flag]
    
    return flags

def _resolve_paths(json_file: str, target_directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Resolve and validate JSON file and target directory paths.
    Implements multi-path support logic.
    """
    try:
        json_path = Path(json_file).resolve()
        
        # Validate JSON file exists
        if not json_path.exists():
            return {"success": False, "error": f"JSON file not found: {json_file}"}
        
        if not json_path.suffix.lower() == ".json":
            return {"success": False, "error": f"File must be JSON: {json_file}"}
        
        # Determine target directory
        if target_directory:
            target_path = Path(target_directory).resolve()
        else:
            # Use JSON file's directory as target
            target_path = json_path.parent
        
        # Validate target directory
        if not target_path.exists():
            return {"success": False, "error": f"Target directory not found: {target_path}"}
        
        if not target_path.is_dir():
            return {"success": False, "error": f"Target path is not a directory: {target_path}"}
        
        # Check if target is a workflow directory
        is_workflow_dir = _is_workflow_directory(target_path)
        
        return {
            "success": True,
            "json_path": str(json_path),
            "target_path": str(target_path),
            "is_workflow_directory": is_workflow_dir,
            "requires_json_copy": str(json_path.parent) != str(target_path) and is_workflow_dir
        }
        
    except Exception as e:
        return {"success": False, "error": f"Path resolution failed: {str(e)}"}

def _is_workflow_directory(directory: Path) -> bool:
    """Check if directory is a workflow directory"""
    try:
        # Look for workflow indicators
        config_dir = directory / "config-files"
        if config_dir.exists():
            # Check for workflow config files
            workflow_configs = list(config_dir.glob("*_workflow_config.json"))
            return len(workflow_configs) > 0
        
        # Alternative: check for direct workflow JSON files
        workflow_jsons = list(directory.glob("*workflow*.json"))
        return len(workflow_jsons) > 0
        
    except Exception:
        return False

def _load_and_validate_json(json_path: str) -> Dict[str, Any]:
    """Load and validate JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation - ensure it's workflow-related JSON
        if not isinstance(data, dict):
            return {"success": False, "error": "JSON must be an object"}
        
        # Check for workflow indicators
        workflow_indicators = ["workflow", "phases", "agents", "workflow_id", "custom_command"]
        has_workflow_data = any(indicator in data for indicator in workflow_indicators)
        
        if not has_workflow_data:
            return {
                "success": False, 
                "error": "JSON does not appear to contain workflow data"
            }
        
        return {
            "success": True,
            "data": data,
            "indicators_found": [ind for ind in workflow_indicators if ind in data]
        }
        
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON format: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to load JSON: {str(e)}"}

def _apply_secondary_flags(json_data: Dict[str, Any], flags: Dict[str, Any]) -> Dict[str, Any]:
    """Apply secondary flag modifications to JSON data"""
    try:
        modified_data = json_data.copy()
        modifications_applied = []
        
        # Handle -add flag
        if "add" in flags:
            result = _handle_add_flag(modified_data, flags["add"])
            if not result["success"]:
                return result
            modified_data = result["data"]
            modifications_applied.append(f"Added: {result['description']}")
        
        # Handle -remove flag
        if "remove" in flags:
            result = _handle_remove_flag(modified_data, flags["remove"])
            if not result["success"]:
                return result
            modified_data = result["data"]
            modifications_applied.append(f"Removed: {result['description']}")
        
        # Handle -replace flag
        if "replace" in flags:
            result = _handle_replace_flag(modified_data, flags["replace"])
            if not result["success"]:
                return result
            modified_data = result["data"]
            modifications_applied.append(f"Replaced: {result['description']}")
        
        # Handle -rename flag
        if "rename" in flags:
            result = _handle_rename_flag(modified_data, flags["rename"])
            if not result["success"]:
                return result
            modified_data = result["data"]
            modifications_applied.append(f"Renamed: {result['description']}")
        
        # Handle -chat flag
        if "chat" in flags:
            result = _handle_chat_flag(modified_data, flags["chat"])
            if not result["success"]:
                return result
            modified_data = result["data"]
            modifications_applied.append(f"Chat update: {result['description']}")
        
        return {
            "success": True,
            "data": modified_data,
            "modifications": modifications_applied
        }
        
    except Exception as e:
        return {"success": False, "error": f"Secondary flag processing failed: {str(e)}"}

def _handle_add_flag(data: Dict[str, Any], add_spec: str) -> Dict[str, Any]:
    """Handle -add flag: Add new phases or agents"""
    try:
        # Parse add specification (e.g., "phase:new_phase_name" or "agent:new_agent")
        if ":" not in add_spec:
            return {"success": False, "error": "Add flag requires format 'type:name'"}
        
        add_type, add_name = add_spec.split(":", 1)
        
        if add_type.lower() == "phase":
            # Add new phase
            if "phases" not in data:
                data["phases"] = []
            
            new_phase = {
                "name": add_name,
                "description": f"New phase added via update command",
                "added_at": datetime.now().isoformat()
            }
            data["phases"].append(new_phase)
            
            return {
                "success": True,
                "data": data,
                "description": f"phase '{add_name}'"
            }
        
        elif add_type.lower() == "agent":
            # Add new agent
            if "agents" not in data:
                data["agents"] = []
            
            new_agent = {
                "name": add_name,
                "role": f"Agent added via update command",
                "added_at": datetime.now().isoformat()
            }
            data["agents"].append(new_agent)
            
            return {
                "success": True,
                "data": data,
                "description": f"agent '{add_name}'"
            }
        
        else:
            return {"success": False, "error": f"Unsupported add type: {add_type}"}
        
    except Exception as e:
        return {"success": False, "error": f"Add operation failed: {str(e)}"}

def _handle_remove_flag(data: Dict[str, Any], remove_spec: str) -> Dict[str, Any]:
    """Handle -remove flag: Remove phases or agents"""
    try:
        if ":" not in remove_spec:
            return {"success": False, "error": "Remove flag requires format 'type:name'"}
        
        remove_type, remove_name = remove_spec.split(":", 1)
        
        if remove_type.lower() == "phase":
            if "phases" in data and isinstance(data["phases"], list):
                original_count = len(data["phases"])
                data["phases"] = [p for p in data["phases"] if p.get("name") != remove_name]
                removed_count = original_count - len(data["phases"])
                
                if removed_count > 0:
                    return {
                        "success": True,
                        "data": data,
                        "description": f"phase '{remove_name}' ({removed_count} instances)"
                    }
                else:
                    return {"success": False, "error": f"Phase '{remove_name}' not found"}
        
        elif remove_type.lower() == "agent":
            if "agents" in data and isinstance(data["agents"], list):
                original_count = len(data["agents"])
                data["agents"] = [a for a in data["agents"] if a.get("name") != remove_name]
                removed_count = original_count - len(data["agents"])
                
                if removed_count > 0:
                    return {
                        "success": True,
                        "data": data,
                        "description": f"agent '{remove_name}' ({removed_count} instances)"
                    }
                else:
                    return {"success": False, "error": f"Agent '{remove_name}' not found"}
        
        else:
            return {"success": False, "error": f"Unsupported remove type: {remove_type}"}
        
    except Exception as e:
        return {"success": False, "error": f"Remove operation failed: {str(e)}"}

def _handle_replace_flag(data: Dict[str, Any], replace_spec: str) -> Dict[str, Any]:
    """Handle -replace flag: Replace existing elements"""
    try:
        # Format: "type:old_name:new_name" or "type:name:new_config"
        parts = replace_spec.split(":", 2)
        if len(parts) < 3:
            return {"success": False, "error": "Replace flag requires format 'type:old:new'"}
        
        replace_type, old_name, new_spec = parts
        
        if replace_type.lower() == "phase":
            if "phases" in data and isinstance(data["phases"], list):
                for phase in data["phases"]:
                    if phase.get("name") == old_name:
                        phase["name"] = new_spec
                        phase["updated_at"] = datetime.now().isoformat()
                        return {
                            "success": True,
                            "data": data,
                            "description": f"phase '{old_name}' -> '{new_spec}'"
                        }
                return {"success": False, "error": f"Phase '{old_name}' not found"}
        
        elif replace_type.lower() == "agent":
            if "agents" in data and isinstance(data["agents"], list):
                for agent in data["agents"]:
                    if agent.get("name") == old_name:
                        agent["name"] = new_spec
                        agent["updated_at"] = datetime.now().isoformat()
                        return {
                            "success": True,
                            "data": data,
                            "description": f"agent '{old_name}' -> '{new_spec}'"
                        }
                return {"success": False, "error": f"Agent '{old_name}' not found"}
        
        else:
            return {"success": False, "error": f"Unsupported replace type: {replace_type}"}
        
    except Exception as e:
        return {"success": False, "error": f"Replace operation failed: {str(e)}"}

def _handle_rename_flag(data: Dict[str, Any], rename_spec: str) -> Dict[str, Any]:
    """Handle -rename flag: Rename workflow elements"""
    try:
        if ":" not in rename_spec:
            return {"success": False, "error": "Rename flag requires format 'old_name:new_name'"}
        
        old_name, new_name = rename_spec.split(":", 1)
        
        renamed_items = []
        
        # Check workflow metadata
        if data.get("custom_command") == old_name:
            data["custom_command"] = new_name
            renamed_items.append("custom_command")
        
        if data.get("workflow_goal", "").lower().find(old_name.lower()) != -1:
            data["workflow_goal"] = data["workflow_goal"].replace(old_name, new_name)
            renamed_items.append("workflow_goal")
        
        # Check phases
        if "phases" in data:
            for phase in data["phases"]:
                if phase.get("name") == old_name:
                    phase["name"] = new_name
                    renamed_items.append(f"phase:{old_name}")
        
        # Check agents
        if "agents" in data:
            for agent in data["agents"]:
                if agent.get("name") == old_name:
                    agent["name"] = new_name
                    renamed_items.append(f"agent:{old_name}")
        
        if renamed_items:
            return {
                "success": True,
                "data": data,
                "description": f"'{old_name}' -> '{new_name}' in {', '.join(renamed_items)}"
            }
        else:
            return {"success": False, "error": f"No instances of '{old_name}' found to rename"}
        
    except Exception as e:
        return {"success": False, "error": f"Rename operation failed: {str(e)}"}

def _handle_chat_flag(data: Dict[str, Any], chat_message: str) -> Dict[str, Any]:
    """Handle -chat flag: Interactive updates based on natural language"""
    try:
        # This would integrate with conversation_bridge.py for natural language processing
        # For now, implement basic keyword-based updates
        
        message_lower = chat_message.lower()
        
        # Add timestamp to workflow for audit trail
        if "chat_updates" not in data:
            data["chat_updates"] = []
        
        data["chat_updates"].append({
            "message": chat_message,
            "timestamp": datetime.now().isoformat(),
            "processed": True
        })
        
        # Basic natural language processing
        modifications = []
        
        if "add phase" in message_lower:
            # Extract phase name from message
            if "called" in message_lower or "named" in message_lower:
                words = chat_message.split()
                phase_name = None
                for i, word in enumerate(words):
                    if word.lower() in ["called", "named"] and i + 1 < len(words):
                        phase_name = words[i + 1].strip("'\"")
                        break
                
                if phase_name:
                    if "phases" not in data:
                        data["phases"] = []
                    data["phases"].append({
                        "name": phase_name,
                        "description": f"Added via chat: {chat_message}",
                        "added_at": datetime.now().isoformat()
                    })
                    modifications.append(f"added phase '{phase_name}'")
        
        if "update goal" in message_lower or "change goal" in message_lower:
            # Update workflow goal
            goal_start = max(message_lower.find("update goal"), 
                            message_lower.find("change goal"))
            if goal_start != -1:
                new_goal = chat_message[goal_start:].split(":", 1)
                if len(new_goal) > 1:
                    data["workflow_goal"] = new_goal[1].strip()
                    modifications.append("updated workflow goal")
        
        return {
            "success": True,
            "data": data,
            "description": f"chat modifications: {', '.join(modifications) if modifications else 'logged message'}"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Chat processing failed: {str(e)}"}

def _execute_workflow_update(json_data: Dict[str, Any], 
                           target_path: str, 
                           workflow_manager: WorkflowManager,
                           workflow_state: WorkflowStateManager, 
                           memory_mcp: MemoryMCPManager) -> Dict[str, Any]:
    """Execute the actual workflow update"""
    try:
        target_dir = Path(target_path)
        
        # Determine output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Check if target is workflow directory
        if _is_workflow_directory(target_dir):
            # Save to config-files subdirectory
            config_dir = target_dir / "config-files"
            config_dir.mkdir(exist_ok=True)
            
            output_file = config_dir / f"updated_workflow_config_{timestamp}.json"
        else:
            # Save directly to target directory
            output_file = target_dir / f"updated_workflow_{timestamp}.json"
        
        # Add update metadata
        json_data["update_metadata"] = {
            "updated_at": datetime.now().isoformat(),
            "update_method": "cli_update_command",
            "original_file_preserved": True
        }
        
        # Write updated JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Update workflow state if workflow_id is available
        workflow_id = json_data.get("workflow_id")
        if workflow_id:
            try:
                workflow_state.track_workflow_progress(
                    workflow_id, 
                    f"Workflow updated via CLI update command - output: {output_file.name}"
                )
                
                memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Configuration updated with new JSON file: {output_file.name}"
                )
            except Exception as e:
                # Continue even if state tracking fails
                print(f"Warning: State tracking failed: {e}")
        
        return {
            "success": True,
            "message": "Workflow successfully updated",
            "output_file": str(output_file),
            "target_directory": target_path,
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "modifications_applied": json_data.get("update_metadata", {})
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Update execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_update(params)