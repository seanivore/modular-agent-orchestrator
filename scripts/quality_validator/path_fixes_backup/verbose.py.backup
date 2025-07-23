"""
Verbose CLI Command - Core Logic
Debug mode toggle with enhanced debugging capabilities
"""

import json
import hashlib
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Manager imports for debug mode integration
try:
    from orchestrator.workflow_manager import WorkflowManager
    from orchestrator.workflow_state import WorkflowStateManager
    from orchestrator.memory_mcp import MemoryMCPManager
except ImportError:
    # Graceful fallback if managers not available
    WorkflowManager = None
    WorkflowStateManager = None
    MemoryMCPManager = None

# Standard cache instance
cache = CacheManager()

# Global debug state storage
DEBUG_STATE_FILE = Path.home() / ".mao_debug_state.json"

class VerboseDebugManager:
    """
    Manages verbose and debug mode states with workflow integration
    """
    
    def __init__(self):
        self.workflow_manager = WorkflowManager() if WorkflowManager else None
        self.workflow_state = WorkflowStateManager() if WorkflowStateManager else None
        self.memory_mcp = MemoryMCPManager() if MemoryMCPManager else None
        
        # Load current debug state
        self.debug_state = self._load_debug_state()
    
    def _load_debug_state(self) -> Dict[str, Any]:
        """Load persistent debug state from file"""
        try:
            if DEBUG_STATE_FILE.exists():
                with open(DEBUG_STATE_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default debug state
        return {
            "verbose_enabled": False,
            "debug_mode": False,
            "debug_level": "basic",  # basic, detailed, forensic
            "workflow_debug": False,
            "session_tracking": False,
            "last_toggled": None,
            "session_start": None
        }
    
    def _save_debug_state(self):
        """Persist debug state to file"""
        try:
            with open(DEBUG_STATE_FILE, 'w') as f:
                json.dump(self.debug_state, f, indent=2)
        except Exception as e:
            # Don't fail command if state saving fails
            pass
    
    def toggle_verbose_mode(self) -> Dict[str, Any]:
        """Toggle verbose mode on/off"""
        current_state = self.debug_state["verbose_enabled"]
        new_state = not current_state
        
        self.debug_state["verbose_enabled"] = new_state
        self.debug_state["last_toggled"] = datetime.now().isoformat()
        
        if new_state:
            self.debug_state["session_start"] = datetime.now().isoformat()
        
        self._save_debug_state()
        
        return {
            "action": "toggle_verbose",
            "previous_state": current_state,
            "new_state": new_state,
            "status": "enabled" if new_state else "disabled",
            "timestamp": self.debug_state["last_toggled"]
        }
    
    def toggle_debug_mode(self, level: str = "basic") -> Dict[str, Any]:
        """Toggle debug mode with specified level"""
        valid_levels = ["basic", "detailed", "forensic"]
        if level not in valid_levels:
            level = "basic"
        
        current_debug = self.debug_state["debug_mode"]
        new_debug = not current_debug
        
        self.debug_state["debug_mode"] = new_debug
        self.debug_state["debug_level"] = level if new_debug else "basic"
        self.debug_state["verbose_enabled"] = new_debug  # Auto-enable verbose with debug
        self.debug_state["last_toggled"] = datetime.now().isoformat()
        
        if new_debug:
            self.debug_state["session_start"] = datetime.now().isoformat()
            # Enable workflow debugging for detailed+ levels
            if level in ["detailed", "forensic"]:
                self.debug_state["workflow_debug"] = True
                self.debug_state["session_tracking"] = True
        
        self._save_debug_state()
        
        result = {
            "action": "toggle_debug",
            "previous_state": current_debug,
            "new_state": new_debug,
            "debug_level": self.debug_state["debug_level"],
            "status": f"enabled ({level})" if new_debug else "disabled",
            "timestamp": self.debug_state["last_toggled"]
        }
        
        # Add workflow integration info if available
        if new_debug and self.workflow_manager:
            result["workflow_integration"] = {
                "workflow_debug": self.debug_state["workflow_debug"],
                "session_tracking": self.debug_state["session_tracking"],
                "managers_available": {
                    "workflow_manager": self.workflow_manager is not None,
                    "workflow_state": self.workflow_state is not None,
                    "memory_mcp": self.memory_mcp is not None
                }
            }
        
        return result
    
    def get_debug_status(self) -> Dict[str, Any]:
        """Get current debug and verbose status"""
        status = {
            "verbose_enabled": self.debug_state["verbose_enabled"],
            "debug_mode": self.debug_state["debug_mode"],
            "debug_level": self.debug_state["debug_level"],
            "workflow_debug": self.debug_state["workflow_debug"],
            "session_tracking": self.debug_state["session_tracking"],
            "last_toggled": self.debug_state["last_toggled"],
            "session_start": self.debug_state["session_start"]
        }
        
        # Add session duration if active
        if self.debug_state["session_start"]:
            try:
                start_time = datetime.fromisoformat(self.debug_state["session_start"])
                duration = (datetime.now() - start_time).total_seconds()
                status["session_duration_seconds"] = int(duration)
                status["session_duration_formatted"] = self._format_duration(duration)
            except Exception:
                pass
        
        # Add manager integration status
        status["integration_status"] = {
            "workflow_manager": self.workflow_manager is not None,
            "workflow_state": self.workflow_state is not None,
            "memory_mcp": self.memory_mcp is not None
        }
        
        return status
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get comprehensive debug information for forensic mode"""
        if not self.debug_state["debug_mode"]:
            return {"error": "Debug mode not enabled"}
        
        debug_info = {
            "debug_session": self.get_debug_status(),
            "system_info": {
                "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                "platform": os.name,
                "working_directory": str(Path.cwd()),
                "debug_state_file": str(DEBUG_STATE_FILE),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Add workflow debug info if available and enabled
        if self.debug_state["workflow_debug"] and self.workflow_manager:
            try:
                workflow_info = self.workflow_manager.get_stats() if hasattr(self.workflow_manager, 'get_stats') else {}
                debug_info["workflow_debug"] = workflow_info
            except Exception as e:
                debug_info["workflow_debug"] = {"error": str(e)}
        
        # Add memory MCP debug info if available
        if self.debug_state["session_tracking"] and self.memory_mcp:
            try:
                memory_info = self.memory_mcp.get_stats() if hasattr(self.memory_mcp, 'get_stats') else {}
                debug_info["memory_debug"] = memory_info
            except Exception as e:
                debug_info["memory_debug"] = {"error": str(e)}
        
        return debug_info
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

@handle_errors(operation_name="verbose", return_dict=True)
def execute_verbose(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main verbose command execution with debug mode toggle and caching.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary
    """
    if params is None:
        params = {}
    
    # Check cache first for status requests
    if params.get("action") == "status":
        cache_key = _generate_cache_key({"action": "status"})
        cached_result = cache.get_cached_analysis(cache_key, "verbose_status")
        if cached_result:
            return json.loads(cached_result)
    
    # Initialize debug manager
    debug_manager = VerboseDebugManager()
    
    # Determine action from parameters
    action = params.get("action", "toggle")  # Default action is toggle
    debug_level = params.get("level", "basic")
    
    # Execute appropriate action
    if action == "toggle":
        result = debug_manager.toggle_verbose_mode()
    elif action == "debug":
        result = debug_manager.toggle_debug_mode(debug_level)
    elif action == "status":
        result = debug_manager.get_debug_status()
    elif action == "info":
        result = debug_manager.get_debug_info()
    else:
        result = {
            "error": f"Unknown action: {action}",
            "available_actions": ["toggle", "debug", "status", "info"]
        }
    
    # Add command metadata
    result["success"] = True  # Ensure success field is set
    result["command"] = "verbose"
    result["executed_at"] = datetime.now().isoformat()
    
    # Cache status results for short duration
    if action == "status" and "error" not in result:
        cache_key = _generate_cache_key({"action": "status"})
        cache.cache_content_analysis(cache_key, json.dumps(result), "verbose_status")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    if params is None:
        params = {}
    
    # Base cost for verbose operations (very low - mostly local state management)
    base_cost = 0.0001
    
    # Additional cost for debug info gathering
    action = params.get("action", "toggle")
    if action == "info":
        base_cost += 0.0005  # Slightly higher for comprehensive debug info
    elif action == "debug":
        base_cost += 0.0002  # Debug mode toggle costs slightly more
    
    # Additional cost if workflow integration is requested
    if params.get("workflow_debug", False):
        base_cost += 0.001  # Workflow integration adds small cost
    
    return base_cost

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including system state"""
    base_key = f"verbose|{str(params) if params else 'none'}"
    
    # Add debug state file modification time for cache invalidation
    if DEBUG_STATE_FILE.exists():
        mtime = DEBUG_STATE_FILE.stat().st_mtime
        base_key += f"|state_mtime:{mtime}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_verbose(params)

# Alias for legacy interface method compatibility
def toggle_verbose(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Legacy interface method alias"""
    return execute_verbose(params)
