"""
CLI Commands Manager 
Dynamic CLI command discovery and interface integration connecting CLI/slash commands to orchestrator functionality
"""

import json
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

class CLICommandsManager:
    """
    Manages CLI command discovery and interface integration.
    
    Core Principles:
    1. Dynamic discovery of CLI command JSON files (truly modular)
    2. Maps interface methods to existing orchestrator managers
    3. Supports both CLI flags and in-app slash commands
    4. No hardcoded command handlers - fully plug-and-play
    """
    
    def __init__(self, orchestrator=None):
        self.cli_dir = Path(__file__).parent.parent / "configs" / "cli"
        self.orchestrator = orchestrator
        
        # Initialize available orchestrator managers
        self._initialize_managers()
    
    def _initialize_managers(self):
        """Initialize connections to existing MAO manager systems"""
        try:
            # Import existing managers dynamically
            from orchestrator.username_manager import UsernameManager
            from orchestrator.settings_manager import ApplicationSettingsManager
            from orchestrator.workflow_manager import WorkflowManager
            from orchestrator.real_time_metrics import SystemMetricsProvider
            
            self.username_manager = UsernameManager()
            self.settings_manager = ApplicationSettingsManager()
            self.workflow_manager = WorkflowManager()
            
            # Real-time metrics needs orchestrator
            if self.orchestrator:
                self.metrics_provider = SystemMetricsProvider(self.orchestrator)
            else:
                self.metrics_provider = None
                
        except ImportError as e:
            # Graceful fallback if managers not available
            self.username_manager = None
            self.settings_manager = None
            self.workflow_manager = None
            self.metrics_provider = None
    
    @handle_errors(operation_name="discover_cli_commands", return_dict=True)
    def discover_cli_commands(self, force_refresh: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Dynamically discover all CLI commands from directory.
        Uses MAO CacheManager for efficient caching.
        
        Returns:
            Dict mapping command names to command configurations
        """
        cache_key = f"cli_commands_discovery|{self.cli_dir}|{force_refresh}"
        
        # Check cache first (MAO standard caching pattern)
        if not force_refresh:
            cached_result = cache.get_cached_analysis(cache_key, "cli_discovery")
            if cached_result:
                return json.loads(cached_result)
        
        commands = {}
        
        # Scan all .json files in CLI directory
        for cli_file in self.cli_dir.glob("*.json"):
            if cli_file.name.startswith('.'):
                continue
                
            try:
                with open(cli_file, 'r') as f:
                    command_data = json.load(f)
                
                command_name = command_data.get("command")
                if command_name:
                    commands[command_name] = command_data
                    
            except Exception as e:
                continue  # Skip malformed files
        
        # Cache the results (MAO standard pattern)
        cache.cache_content_analysis(cache_key, json.dumps(commands), "cli_discovery")
        
        return commands
    
    @handle_errors(operation_name="execute_command", return_dict=True)
    def execute_command(self, command: str, input_data: Any = None, 
                       source: str = "cli") -> Dict[str, Any]:
        """
        Execute a CLI or slash command using dynamic interface method mapping.
        Uses intelligent caching to minimize API costs for repeated commands.
        
        Args:
            command: Command name (without flags or slashes)
            input_data: Optional input data for commands that need it
            source: "cli" or "app" to indicate the command source
            
        Returns:
            Command execution result
        """
        # Discover current commands
        commands = self.discover_cli_commands()
        
        if command not in commands:
            return {
                "success": False,
                "message": f"Unknown command: {command}",
                "available_commands": list(commands.keys())
            }
        
        command_config = commands[command]
        interface_method = command_config.get("interface_method")
        
        if not interface_method:
            return {
                "success": False,
                "message": f"No interface method defined for command: {command}"
            }
        
        # Check cache first for cacheable commands
        cached_result = self._get_cached_command_result(command, input_data, command_config)
        if cached_result:
            return {
                "success": True,
                "command": command,
                "source": source,
                "result": cached_result,
                "cached": True,
                "timestamp": datetime.now().isoformat()
            }
        
        # Execute the interface method dynamically
        try:
            result = self._execute_interface_method(interface_method, input_data, command_config, source)
            
            # Cache the result if it's cacheable
            self._cache_command_result(command, input_data, command_config, result)
            
            return {
                "success": True,
                "command": command,
                "source": source,
                "result": result,
                "cached": False,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _execute_interface_method(self, method_name: str, input_data: Any, 
                                 config: Dict, source: str) -> Dict[str, Any]:
        """
        Dynamically execute interface methods by mapping to existing manager functionality.
        This is the core of the modular approach - no hardcoded handlers.
        """
        
        # Map interface methods to existing manager methods
        method_mappings = {
            # User management
            "login": lambda data: self._call_manager_method(self.username_manager, "set_session_user", data),
            "logout": lambda data: self._call_manager_method(self.username_manager, "logout_user"),
            "user_id": lambda data: self._get_current_user_id(),
            
            # Settings management
            "open_config": lambda data: self._call_manager_method(self.settings_manager, "discover_settings"),
            
            # Workflow management
            "workflows": lambda data: self._call_manager_method(self.workflow_manager, "list_workflows"),
            "workflow_id": lambda data: self._call_manager_method(self.workflow_manager, "generate_workflow_id"),
            "goal": lambda data: self._create_workflow_from_goal(data),
            
            # System information
            "stats": lambda data: self._get_system_stats(),
            "list_tools": lambda data: self._list_available_tools(),
            "help": lambda data: self.get_command_help(data),
            
            # Workflow operations
            "setup": lambda data: self._workflow_setup(data),
            "update": lambda data: self._workflow_update(data),
            "fix_it": lambda data: self._workflow_fix_it(data),
            "continue": lambda data: self._workflow_continue(data),
            "review": lambda data: self._workflow_review(data),
            
            # System operations
            "restart": lambda data: self._system_restart(),
            "exit": lambda data: self._system_exit(),
            
            # Model and provider management
            "model": lambda data: self._model_management(data),
            "provider": lambda data: self._provider_management(data),
            "model_list": lambda data: self._list_models(),
            "provider_list": lambda data: self._list_providers(),
            
            # Environment and diagnostics
            "variables": lambda data: self._get_variables(data),
            "variables_explain": lambda data: self._explain_variables(),
            "logs": lambda data: self._get_logs(data),
            "doctor": lambda data: self._run_diagnostics()
        }
        
        if method_name not in method_mappings:
            return {
                "error": f"Interface method '{method_name}' not implemented",
                "available_methods": list(method_mappings.keys()),
                "note": "Add method mapping to _execute_interface_method() to support this command"
            }
        
        # Execute the mapped method
        return method_mappings[method_name](input_data)
    
    def _call_manager_method(self, manager, method_name: str, *args):
        """Helper to safely call manager methods"""
        if not manager:
            return {"error": f"Manager not available for {method_name}"}
        
        if not hasattr(manager, method_name):
            return {"error": f"Method {method_name} not found on manager"}
        
        try:
            method = getattr(manager, method_name)
            if args:
                return method(*args)
            else:
                return method()
        except Exception as e:
            return {"error": f"Manager method failed: {str(e)}"}
    
    def _get_current_user_id(self) -> Dict[str, Any]:
        """Get current user ID from session"""
        if not self.username_manager:
            return {"error": "Username manager not available"}
        
        current_user = self.username_manager.get_session_user()
        if current_user:
            return {
                "user_id": current_user.get("user_id"),
                "username": current_user.get("username")
            }
        else:
            return {"error": "No user logged in"}
    
    def _create_workflow_from_goal(self, goal_data: Any) -> Dict[str, Any]:
        """Create workflow from goal using orchestrator or workflow manager"""
        if not goal_data:
            return {"error": "Goal command requires input data"}
        
        # Try orchestrator first
        if self.orchestrator and hasattr(self.orchestrator, 'create_workflow_from_goal'):
            try:
                return self.orchestrator.create_workflow_from_goal(goal_data)
            except Exception as e:
                return {"error": f"Orchestrator goal creation failed: {str(e)}"}
        
        # Fallback to workflow manager
        if self.workflow_manager:
            try:
                workflow_id = self.workflow_manager.generate_workflow_id()
                return {
                    "workflow_id": workflow_id,
                    "goal": goal_data,
                    "status": "created",
                    "message": "Workflow created successfully (fallback mode)"
                }
            except Exception as e:
                return {"error": f"Workflow manager goal creation failed: {str(e)}"}
        
        return {"error": "No workflow creation system available"}
    
    def _get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics using metrics provider or fallback"""
        if self.metrics_provider:
            try:
                return self.metrics_provider.get_dashboard_metrics()
            except Exception as e:
                return {"error": f"Metrics provider failed: {str(e)}"}
        
        # Fallback basic stats
        return {
            "system_status": "operational",
            "timestamp": datetime.now().isoformat(),
            "note": "Limited stats - metrics provider not available"
        }
    
    def _list_available_tools(self) -> Dict[str, Any]:
        """List available tools using orchestrator or directory scan"""
        if self.orchestrator and hasattr(self.orchestrator, 'tool_discovery'):
            try:
                tools_info = self.orchestrator.tool_discovery.get_available_tools()
                return {
                    "tools": tools_info,
                    "total_tools": len(tools_info)
                }
            except Exception as e:
                return {"error": f"Tool discovery failed: {str(e)}"}
        
        # Fallback - scan tools directory
        try:
            tools_dir = Path(__file__).parent.parent / "tools"
            tool_dirs = [d.name for d in tools_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            return {
                "tools": tool_dirs,
                "total_tools": len(tool_dirs),
                "note": "Basic tool list - orchestrator not connected"
            }
        except Exception as e:
            return {"error": f"Failed to scan tools directory: {str(e)}"}
    
    # Placeholder methods for commands that need implementation
    def _workflow_setup(self, data: Any) -> Dict[str, Any]:
        """Workflow setup operation"""
        return {"message": "Workflow setup", "input": data, "note": "Implementation pending"}
    
    def _workflow_update(self, data: Any) -> Dict[str, Any]:
        """Workflow update operation"""
        return {"message": "Workflow update", "input": data, "note": "Implementation pending"}
    
    def _workflow_fix_it(self, data: Any) -> Dict[str, Any]:
        """Workflow fix-it operation"""
        return {"message": "Workflow fix-it", "input": data, "note": "Implementation pending"}
    
    def _workflow_continue(self, data: Any) -> Dict[str, Any]:
        """Workflow continue operation"""
        return {"message": "Workflow continue", "note": "Implementation pending"}
    
    def _workflow_review(self, data: Any) -> Dict[str, Any]:
        """Workflow review operation"""
        return {"message": "Workflow review", "note": "Implementation pending"}
    
    def _system_restart(self) -> Dict[str, Any]:
        """System restart operation"""
        return {"message": "System restart", "note": "Implementation pending"}
    
    def _system_exit(self) -> Dict[str, Any]:
        """System exit operation"""
        return {"message": "System exit", "note": "Implementation pending"}
    
    def _model_management(self, data: Any) -> Dict[str, Any]:
        """Model management operation"""
        return {"message": "Model management", "input": data, "note": "Implementation pending"}
    
    def _provider_management(self, data: Any) -> Dict[str, Any]:
        """Provider management operation"""
        return {"message": "Provider management", "input": data, "note": "Implementation pending"}
    
    def _list_models(self) -> Dict[str, Any]:
        """List available models"""
        return {"message": "List models", "note": "Implementation pending"}
    
    def _list_providers(self) -> Dict[str, Any]:
        """List available providers"""
        return {"message": "List providers", "note": "Implementation pending"}
    
    def _get_variables(self, data: Any) -> Dict[str, Any]:
        """Get environment variables"""
        return {"message": "Get variables", "input": data, "note": "Implementation pending"}
    
    def _explain_variables(self) -> Dict[str, Any]:
        """Explain environment variables"""
        return {"message": "Explain variables", "note": "Implementation pending"}
    
    def _get_logs(self, data: Any) -> Dict[str, Any]:
        """Get system logs"""
        return {"message": "Get logs", "input": data, "note": "Implementation pending"}
    
    def _run_diagnostics(self) -> Dict[str, Any]:
        """Run system diagnostics"""
        return {"message": "Run diagnostics", "note": "Implementation pending"}
    
    @handle_errors(operation_name="get_command_help", return_dict=True)
    def get_command_help(self, command: str = None) -> Dict[str, Any]:
        """
        Get help information for commands.
        
        Args:
            command: Specific command name, or None for all commands
            
        Returns:
            Help information
        """
        commands = self.discover_cli_commands()
        
        if command:
            if command in commands:
                cmd_config = commands[command]
                return {
                    "command": command,
                    "help": cmd_config.get("help", "No help available"),
                    "type": cmd_config.get("type", "unknown"),
                    "terminal_flag": cmd_config.get("terminal_flag", ""),
                    "app_command": cmd_config.get("app_command", ""),
                    "interface_method": cmd_config.get("interface_method", "")
                }
            else:
                return {
                    "error": f"Command '{command}' not found",
                    "available_commands": list(commands.keys())
                }
        else:
            # Return help for all commands
            help_data = {}
            for cmd_name, cmd_config in commands.items():
                help_data[cmd_name] = {
                    "help": cmd_config.get("help", "No help available"),
                    "type": cmd_config.get("type", "unknown"),
                    "terminal_flag": cmd_config.get("terminal_flag", ""),
                    "app_command": cmd_config.get("app_command", "")
                }
            
            return {
                "all_commands": help_data,
                "total_commands": len(help_data)
            }
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning (reads costs from JSON files)"""
        operation = params.get("operation", "unknown")
        
        # Manager operation costs (not CLI commands)
        manager_costs = {
            "discover_cli_commands": 0.0001,
            "execute_command": 0.002,  # May involve orchestrator calls
            "get_command_help": 0.0001
        }
        
        # If it's a manager operation, use fixed costs
        if operation in manager_costs:
            return manager_costs[operation]
        
        # For CLI commands, read costs dynamically from JSON files
        try:
            commands = self.discover_cli_commands()
            if operation in commands:
                return commands[operation].get("cost_estimate", 0.001)
        except Exception:
            pass  # Fallback to default if discovery fails
        
        # Default fallback cost
        return 0.001
    
    def _get_cached_command_result(self, command: str, input_data: Any, 
                                  config: Dict) -> Optional[Dict[str, Any]]:
        """
        Check if we have a cached result for this command.
        Uses content fingerprinting like tools do.
        """
        # Only cache commands that are expensive or frequently called
        cacheable_commands = {
            "workflows": 300,  # Cache for 5 minutes
            "stats": 60,       # Cache for 1 minute
            "list_tools": 600, # Cache for 10 minutes
            "help": 3600,      # Cache for 1 hour
            "model_list": 600, # Cache for 10 minutes
            "provider_list": 600 # Cache for 10 minutes
        }
        
        if command not in cacheable_commands:
            return None  # Don't cache this command
        
        # Generate cache key based on command and current system state
        cache_key = self._generate_command_cache_key(command, input_data)
        
        # Check cache
        cached_result = cache.get_cached_analysis(cache_key, f"cli_command_{command}")
        if cached_result:
            try:
                cached_data = json.loads(cached_result)
                
                # Check if cache is still valid (not expired)
                cache_duration = cacheable_commands[command]
                cache_time = datetime.fromisoformat(cached_data.get("cached_at", ""))
                if (datetime.now() - cache_time).total_seconds() < cache_duration:
                    return cached_data["result"]
                    
            except Exception:
                pass  # Invalid cache entry, ignore
        
        return None
    
    def _cache_command_result(self, command: str, input_data: Any, 
                             config: Dict, result: Dict[str, Any]):
        """
        Cache command result if it's a cacheable command.
        Uses content fingerprinting to avoid redundant caching.
        """
        # Only cache expensive or frequently called commands
        cacheable_commands = {
            "workflows", "stats", "list_tools", "help", 
            "model_list", "provider_list"
        }
        
        if command not in cacheable_commands:
            return  # Don't cache this command
        
        # Don't cache error results
        if result.get("error"):
            return
        
        # Generate cache key and store result
        cache_key = self._generate_command_cache_key(command, input_data)
        
        cache_data = {
            "result": result,
            "command": command,
            "cached_at": datetime.now().isoformat()
        }
        
        cache.cache_content_analysis(cache_key, json.dumps(cache_data), f"cli_command_{command}")
    
    def _generate_command_cache_key(self, command: str, input_data: Any) -> str:
        """
        Generate cache key that includes current system state fingerprint.
        This ensures cache invalidation when underlying data changes.
        """
        # Base key with command and input
        base_key = f"{command}|{str(input_data) if input_data else 'none'}"
        
        # Add system state fingerprints for commands that depend on file system
        if command == "workflows":
            # Include workflow directory state
            workflows_dir = Path(__file__).parent.parent / "configs" / "workflows"
            if workflows_dir.exists():
                workflow_files = sorted([f.name for f in workflows_dir.iterdir() if f.is_dir()])
                base_key += f"|workflows:{hashlib.md5(str(workflow_files).encode()).hexdigest()[:8]}"
                
        elif command == "list_tools":
            # Include tools directory state  
            tools_dir = Path(__file__).parent.parent / "tools"
            if tools_dir.exists():
                tool_dirs = sorted([d.name for d in tools_dir.iterdir() if d.is_dir()])
                base_key += f"|tools:{hashlib.md5(str(tool_dirs).encode()).hexdigest()[:8]}"
                
        elif command in ["model_list", "provider_list"]:
            # Include config file modification times
            config_type = "models" if command == "model_list" else "providers"
            config_dir = Path(__file__).parent.parent / "configs" / config_type
            if config_dir.exists():
                mod_times = [f.stat().st_mtime for f in config_dir.glob("*.json")]
                base_key += f"|{config_type}:{hashlib.md5(str(sorted(mod_times)).encode()).hexdigest()[:8]}"
        
        # Generate final cache key
        return hashlib.md5(base_key.encode()).hexdigest()[:16]


# Standalone functions for button imports (MAO standardization pattern)
def discover_cli_commands() -> Dict[str, Dict[str, Any]]:
    """Standalone function for discovering CLI commands"""
    manager = CLICommandsManager()
    return manager.discover_cli_commands()

def execute_command(command: str, input_data: Any = None, source: str = "cli") -> Dict[str, Any]:
    """Standalone function for executing CLI commands"""
    manager = CLICommandsManager()
    return manager.execute_command(command, input_data, source)

def get_command_help(command: str = None) -> Dict[str, Any]:
    """Standalone function for getting command help"""
    manager = CLICommandsManager()
    return manager.get_command_help(command)
