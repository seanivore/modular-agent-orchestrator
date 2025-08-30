"""
CLI Commands Manager
Dynamic CLI command discovery and execution - truly modular with no hardcoded categories
"""

import json
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError

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
        self.cli_dir = Path(__file__).parent.parent / "configs/cli"
        self.orchestrator = orchestrator
    
    
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
        
        # Scan all .json files in CLI directory and subdirectories
        for cli_file in self.cli_dir.glob("**/*.json"):
            if cli_file.name.startswith('.'):
                continue
                
            try:
                with open(cli_file, 'r') as f:
                    command_data = json.load(f)
                
                command_name = command_data.get("name")
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
        Execute a CLI or slash command using dynamic command loading.
        Loads command logic from JSON-specified file paths without hardcoded mappings.
        
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
        file_path = command_config.get("file_path")
        
        if not file_path:
            return {
                "success": False,
                "message": f"No file_path defined for command: {command}"
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
        
        # Execute command dynamically by loading its Python file
        try:
            result = self._execute_command_dynamically(command, file_path, input_data, source)
            
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
    
    def _execute_command_dynamically(self, command_name: str, file_path: str, 
                                   input_data: Any, source: str) -> Dict[str, Any]:
        """
        Execute command dynamically by loading its Python module.
        No hardcoded mappings - fully modular and adaptive.
        """
        # Convert relative path to absolute path
        if not file_path.startswith('/'):
            base_path = Path(__file__).parent.parent
            full_path = base_path / file_path
        else:
            full_path = Path(file_path)
        
        if not full_path.exists():
            return {
                "error": f"Command file not found: {full_path}",
                "command": command_name
            }
        
        try:
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(f"cli_{command_name}", full_path)
            if spec is None or spec.loader is None:
                return {
                    "error": f"Cannot load command module: {full_path}",
                    "command": command_name
                }
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for execute_command function (standard MAO CLI pattern)
            if hasattr(module, 'execute_command'):
                return module.execute_command(input_data)
            elif hasattr(module, 'execute'):
                return module.execute(input_data)
            elif hasattr(module, 'main'):
                return module.main(input_data)
            else:
                return {
                    "error": f"No execute_command, execute, or main function found in {command_name}",
                    "available_functions": [name for name in dir(module) if not name.startswith('_')],
                    "command": command_name
                }
                
        except Exception as e:
            return {
                "error": f"Command execution failed: {str(e)}",
                "command": command_name,
                "file_path": str(full_path)
            }
    
    
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
            "get_command_help": 0.0001,
            "memory": 0.001  # Memory operations cost
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
        Uses simple cache duration from command config.
        """
        # Get cache duration from command config
        cache_duration = config.get("cache_duration", 0)
        if cache_duration <= 0:
            return None  # Command not cacheable
        
        # Generate cache key
        cache_key = f"cli_cmd|{command}|{str(input_data) if input_data else 'none'}"
        
        # Check cache
        cached_result = cache.get_cached_analysis(cache_key, f"cli_command_{command}")
        if cached_result:
            try:
                cached_data = json.loads(cached_result)
                
                # Check if cache is still valid (not expired)
                cache_time = datetime.fromisoformat(cached_data.get("cached_at", ""))
                if (datetime.now() - cache_time).total_seconds() < cache_duration:
                    return cached_data["result"]
                    
            except Exception:
                pass  # Invalid cache entry, ignore
        
        return None
    
    def _cache_command_result(self, command: str, input_data: Any, 
                             config: Dict, result: Dict[str, Any]):
        """
        Cache command result if cacheable and successful.
        Simple caching without hardcoded command categories.
        """
        # Check if command is cacheable from config
        cache_duration = config.get("cache_duration", 0)
        if cache_duration <= 0:
            return  # Not cacheable
        
        # Don't cache error results
        if result.get("error"):
            return
        
        # Generate cache key and store result
        cache_key = f"cli_cmd|{command}|{str(input_data) if input_data else 'none'}"
        
        cache_data = {
            "result": result,
            "command": command,
            "cached_at": datetime.now().isoformat()
        }
        
        cache.cache_content_analysis(cache_key, json.dumps(cache_data), f"cli_command_{command}")


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

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Standalone function for cost estimation"""
    manager = CLICommandsManager()
    return manager.estimate_cost(params or {})
