#!/usr/bin/env python3
"""
Mao - Main CLI Entry Point
Pure dynamic routing - zero hardcoded arguments
"""

import sys
import json
from pathlib import Path
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def load_all_commands():
    """Load all command configs dynamically"""
    commands = {}
    cli_dir = Path(__file__).parent / "configs" / "cli"
    
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
        return TerminalInterface()
    except ImportError:
        sys.stderr.write("Bootstrap error: Cannot import Mao interface\n")
        sys.exit(1)

def main():
    """Pure dynamic routing - zero hardcoding"""
    
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
            # No command provided - default behavior
            interface.interactive()
            
    except KeyboardInterrupt:
        sys.exit(0)
    except AttributeError as e:
        # Method doesn't exist on interface
        interface.error(f"Command not implemented: {cmd_config['command']}")
    except Exception as e:
        interface.error(str(e))

if __name__ == "__main__":
    main()
