#!/usr/bin/env python3
"""
Mao Terminal Interface 
Comprehensive terminal interface for CLI command execution and interactive mode
Routes CLI commands through standardized CLI manager system
"""

import json
import sys
# import os  # Removed - was only used for sys.path.append
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

class TerminalInterface:
    """Clean Mao terminal interface with CLI manager integration"""
    
    def __init__(self, config_dir: str = "configs", verbose: bool = False):
        self.config_dir = config_dir
        self.verbose = verbose
        self.settings = self._load_settings()
        
        # Initialize orchestrator when needed (lazy loading)
        self._orchestrator = None
        
        # Initialize CLI manager for command routing
        self._cli_manager = None
    
    @property
    def orchestrator(self):
        """Lazy load orchestrator to avoid import issues"""
        if self._orchestrator is None:
            try:
                from orchestrator.core import WorkflowOrchestrator
                self._orchestrator = WorkflowOrchestrator(self.config_dir)
            except ImportError:
                self.error("Cannot load orchestrator - check installation")
                sys.exit(1)
        return self._orchestrator
    
    @property
    def cli_manager(self):
        """Lazy load CLI manager for command routing"""
        if self._cli_manager is None:
            try:
                from orchestrator.cli_manager import CLICommandsManager
                self._cli_manager = CLICommandsManager(self.orchestrator)
            except ImportError:
                self.error("Cannot load CLI manager - check installation")
                sys.exit(1)
        return self._cli_manager
    
    def _load_settings(self) -> Dict:
        """Load user settings with defaults"""
        settings_file = Path(self.config_dir) " / " "user_settings.json"
        defaults = {
            "verbose": False,
            "output_directory": None,
            "color_theme": "default"
        }
        
        try:
            with open(settings_file) as f:
                return {**defaults, **json.load(f)}
        except FileNotFoundError:
            return defaults
    
    def _save_settings(self):
        """Save current settings"""
        settings_file = Path(self.config_dir) " / " "user_settings.json"
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    # =================================================================
    # CLI COMMAND ROUTING
    # =================================================================
    
    @handle_errors(operation_name="cli_command_routing", return_dict=True)
    def execute_cli_command(self, command: str, input_data: Any = None) -> Dict[str, Any]:
        """Route CLI command through standardized CLI manager"""
        try:
            result = self.cli_manager.execute_command(command, input_data, source="app")
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Command execution failed: {str(e)}",
                "command": command
            }
    
    def get_command_help(self, command: str = None) -> Dict[str, Any]:
        """Get help information through CLI manager"""
        try:
            return self.cli_manager.get_command_help(command)
        except Exception as e:
            return {
                "success": False,
                "error": f"Help retrieval failed: {str(e)}"
            }
    
    # =================================================================
    # INTERACTIVE MODE
    # =================================================================
    
    def interactive(self):
        """Start interactive mode with slash command support"""
        print("Welcome to Mao Interactive Mode")
        print("=" * 50)
        print("Describe what you want to accomplish, or:")
        print("  • Type '" / "help' for available commands")
        print("  • Type '" / "stats' for system information")
        print("  • Type 'exit' to quit")
        print()
        
        while True:
            try:
                user_input = input("Mao> ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                elif user_input.startswith('" / "'):
                    self._handle_slash_command(user_input[1:])
                elif user_input:
                    # Route natural language input to goal processing
                    print(f"Processing: {user_input}")
                    result = self.execute_cli_command("goal", user_input)
                    if not result.get("success", True):
                        print(f"ERROR: {result.get('error', 'Goal processing failed')}")
                else:
                    print("What would you like to accomplish?")
                    
            except KeyboardInterrupt:
                print(Path(r"\nGoodbye!"))
                break
            except EOFError:
                break
    
    def _handle_slash_command(self, command: str):
        """Handle in-app slash commands through CLI manager"""
        parts = command.split(' ', 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        
        # Handle app-only commands directly
        if cmd == 'exit':
            print("Goodbye!")
            sys.exit(0)
        elif cmd == 'restart':
            self._restart_interface()
        else:
            # Route all other commands through CLI manager
            result = self.execute_cli_command(cmd, arg)
            if not result.get("success", True):
                print(f"Unknown command: " / "{cmd}")
                print("Type '" / "help' for available commands")
    
    def _restart_interface(self):
        """Restart the interface (app-only command)"""
        print("Restarting Mao interface...")
        print("Interface restarted successfully")
        # In real implementation, this would restart the process
        self.interactive()
    
    # =================================================================
    # UTILITY METHODS
    # =================================================================
    
    def error(self, message: str):
        """Display error message"""
        print(fPath(r"\nERROR: {message}"))
        print("Try '" / "help' for available commands")
        print("Try '" / "doctor' for system diagnostics")
    
    def success(self, message: str):
        """Display success message"""
        print(f"SUCCESS: {message}")
    
    def info(self, message: str):
        """Display info message"""
        print(f"INFO: {message}")
    
    def warning(self, message: str):
        """Display warning message"""
        print(f"WARNING: {message}")
    
    # =================================================================
    # TERMINAL UI LAUNCH METHODS (for CLI commands)
    # =================================================================
    
    def launch_terminal_ui_smart(self, data: Any = None):
        """Smart launch - quick for returning users, onboarding for new users (mao mao)"""
        try:
            # Import the CLI command and execute it
            from configs.cli.mao.mao import execute_command
            result = execute_command(data)
            
            if result.get("success"):
                print(f"SUCCESS: {result.get('message', 'Terminal UI launched')}")
            else:
                print(f"ERROR: {result.get('message', 'Failed to launch terminal UI')}")
                
        except Exception as e:
            print(f"ERROR: Failed to launch terminal UI: {str(e)}")
    
    def launch_terminal_ui_onboarding(self, data: Any = None):
        """Always launch with full onboarding experience (single mao)"""
        try:
            # Import the onboarding command and execute it
            from configs.cli.onboard.onboard import execute_command
            result = execute_command(data)
            
            if result.get("success"):
                print(f"SUCCESS: {result.get('message', 'Onboarding completed')}")
            else:
                print(f"ERROR: {result.get('message', 'Onboarding failed')}")
                
        except Exception as e:
            print(f"ERROR: Failed to start onboarding: {str(e)}")

    @handle_errors(operation_name="estimate_cost", return_dict=True)
    def estimate_cost(self, params: Dict[str, Any] = None) -> float:
        """Estimate interface operation cost for budget planning"""
        base_cost = 0.01  # Base interface cost
        
        if params:
            commands = params.get("commands", 1)
            base_cost += commands * 0.005
            
            ui_operations = params.get("ui_operations", 1)
            base_cost += ui_operations * 0.002
            
            orchestrator_calls = params.get("orchestrator_calls", 0)
            base_cost += orchestrator_calls * 0.01
        
        return base_cost


# =================================================================
# SUBPROCESS COMMUNICATION PATTERNS (TO BE IMPLEMENTED)
# =================================================================

class SubprocessCommunicationBridge:
    """
    TO BE IMPLEMENTED: Node.js ↔ Python subprocess communication bridge
    
    This class will handle structured message passing between the Node.js
    terminal UI and the Python backend for rich terminal interface functionality.
    """
    
    def __init__(self, terminal_interface: 'TerminalInterface'):
        self.terminal_interface = terminal_interface
        self.message_queue = []
        self.subprocess_handlers = {}
    
    def handle_nodejs_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        TO BE IMPLEMENTED: Process incoming messages from Node.js terminal UI
        
        Expected message format:
        {
            "type": "command|query|ui_event|progress_update",
            "command": "goal|search|create|etc",
            "data": {...},
            "session_id": "unique_session_identifier",
            "timestamp": "ISO_timestamp"
        }
        """
        # This will route messages to appropriate handlers
        # and return structured responses for the Node.js UI
        pass
    
    def send_to_nodejs(self, response: Dict[str, Any]) -> None:
        """
        TO BE IMPLEMENTED: Send structured responses to Node.js terminal UI
        
        Response format:
        {
            "success": bool,
            "data": {...},
            "ui_updates": {
                "display_state": "processing|celebrating|organizing|etc",
                "progress": float,
                "status_message": str
            },
            "timestamp": "ISO_timestamp"
        }
        """
        # This will send JSON messages via stdout to Node.js process
        pass
    
    def setup_subprocess_communication(self) -> None:
        """
        TO BE IMPLEMENTED: Initialize subprocess communication channels
        
        This will establish:
        - stdin" / "stdout JSON message passing
        - Error handling for subprocess communication
        - Message validation and routing
        - UI state synchronization
        """
        pass
    
    def register_ui_state_handler(self, handler_name: str, handler_func) -> None:
        """
        TO BE IMPLEMENTED: Register handlers for UI state changes
        
        This enables the "Brain" UI functionality that displays different
        states like "celebrating", "organizing", "budgeting", etc. based
        on the current processing context.
        """
        self.subprocess_handlers[handler_name] = handler_func


# Note: Integration points in existing TerminalInterface class:
# 
# 1. TerminalInterface.__init__() would initialize SubprocessCommunicationBridge
# 2. execute_cli_command() would route through subprocess bridge when in Node.js mode
# 3. All print() statements would be converted to structured messages
# 4. Interactive mode would be replaced with message-based event handling


# =================================================================
# LEGACY COMPATIBILITY & BOOTSTRAPPING
# =================================================================

def bootstrap_interface():
    """Bootstrap interface with error recovery"""
    try:
        interface = TerminalInterface()
        return interface
    except ImportError as e:
        print(f"ERROR: Bootstrap failed: {str(e)}")
        print("Check that all dependencies are installed")
        print("Run system diagnostics to identify issues")
        sys.exit(1)


if __name__ == "__main__":
    # Direct execution starts interactive mode
    interface = bootstrap_interface()
    interface.interactive()
