#!/usr/bin/env python3
"""
Main CLI Entry Point
Pure dynamic routing with zero hardcoded arguments
"""

import sys
import json
from pathlib import Path
import argparse
import logging
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Required Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

# Standard cache instance
cache = CacheManager()
logger = logging.getLogger(__name__)

def load_all_commands():
    """Load all command configs dynamically"""
    commands = {}
    cli_dir = Path(__file__).parent / "configs / cli"
    
    for json_file in cli_dir.glob("*.json"):
        if json_file.name.endswith('.OLD'):
            continue
        try:
            with open(json_file) as f:
                cmd_config = json.load(f)
                commands[cmd_config["command"]] = cmd_config
        except (json.JSONDecodeError, KeyError):
            continue  # Skip malformed files
    
    return commands

def create_dynamic_parser(commands):
    """Build parser from all command configs"""
    parser = argparse.ArgumentParser(
        description="Mao - Modular Agent Orchestrator",
        add_help=False
    )
    
    for cmd_config in commands.values():
        flag = cmd_config["terminal_flag"]
        cmd_type = cmd_config["type"]
        
        if cmd_type == "standalone":
            parser.add_argument(flag, action="store_true")
        elif cmd_type in ["needs_input", "needs_file"]:
            parser.add_argument(flag, type=str)
        # Skip app_only commands - those are handled in-app
    
    return parser

def find_used_command(args, commands):
    """Find which command was actually used"""
    for cmd_config in commands.values():
        if cmd_config["type"] == "app_only":
            continue
            
        # Convert --fix-it to fix_it (argparse does this automatically)
        arg_name = cmd_config["terminal_flag"].lstrip("-").replace("-", "_")
        
        if hasattr(args, arg_name):
            value = getattr(args, arg_name)
            if value:  # Found the used command
                return cmd_config, value
    
    return None, None

def bootstrap_interface():
    """Bootstrap interface with error recovery"""
    try:
        from interfaces.ui_terminal import TerminalInterface
        
        # Initialize MCP Integration Hub during bootstrap
        logger.info("Initializing MCP Integration Hub...")
        from orchestrator.mcp_hub import create_mcp_hub
        mcp_hub = create_mcp_hub()
        
        interface = TerminalInterface()
        interface.mcp_hub = mcp_hub  # Provide MCP Hub access to interface
        
        return interface
    except ImportError:
        sys.stderr.write("Bootstrap error: Cannot import Mao interface\n")
        sys.exit(1)

@handle_errors(operation_name="main", return_dict=True)
def main():
    """Pure dynamic routing - zero hardcoding"""
    
    # Special handling for UI mode (TypeScript frontend communication)
    if len(sys.argv) >= 2 and '--ui-mode' in sys.argv:
        from interfaces.ui_terminal import TerminalInterface
        interface = TerminalInterface()
        interface.start_ui_mode()
        return
    
    # Special handling for 'mao mao' command
    if len(sys.argv) == 2 and sys.argv[1] == "mao":
        # User typed 'mao mao' - trigger smart launch
        interface = bootstrap_interface()
        interface.launch_terminal_ui_smart()
        return
    
    # Load all commands and create parser
    commands = load_all_commands()
    parser = create_dynamic_parser(commands)
    args = parser.parse_args()
    
    # Bootstrap interface
    interface = bootstrap_interface()
    
    # Find which command was used
    cmd_config, value = find_used_command(args, commands)
    
    try:
        if cmd_config:
            # Route to the interface method specified in JSON
            method_name = cmd_config["interface_method"]
            method = getattr(interface, method_name)
            
            # Call with appropriate arguments based on type
            if cmd_config["type"] == "standalone":
                method()
            else:
                method(value)
        else:
            # No command provided - default to onboarding (single 'mao' command)
            interface.launch_terminal_ui_onboarding()
            
    except KeyboardInterrupt:
        sys.exit(0)
    except AttributeError as e:
        # Method doesn't exist on interface
        interface.error(f"Command not implemented: {cmd_config['command']}")
    except Exception as e:
        interface.error(str(e))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate system startup cost for budget planning"""
    base_cost = 0.01  # Base system startup cost
    
    if params:
        interfaces = params.get("interfaces", 1)
        base_cost += interfaces * 0.005
        
        cli_commands = params.get("cli_commands", 50)
        base_cost += cli_commands * 0.001
        
        mcp_hubs = params.get("mcp_hubs", 1)
        base_cost += mcp_hubs * 0.003
    
    return base_cost

if __name__ == "__main__":
    main()
