#!/usr/bin/env python3
"""
Mao - Main CLI Entry Point
Pure routing - no business logic, no print statements, no hardcoded args
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def load_cli_config():
    """Load CLI configuration from JSON"""
    config_path = Path(__file__).parent / "configs" / "cli" / "arguments.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        # Bootstrap fallback - minimal config
        return {
            "arguments": {
                "goal": {"type": "positional", "nargs": "?"},
                "interactive": {"type": "flag", "terminal_flag": "--interactive"}
            }
        }

def create_parser_from_config(config):
    """Create argument parser from JSON configuration"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Mao - Modular Agent Orchestrator",
        add_help=False  # We'll handle help through interface
    )
    
    for arg_name, arg_config in config["arguments"].items():
        if arg_config["type"] == "positional":
            parser.add_argument(arg_name, nargs=arg_config.get("nargs", None))
        elif arg_config["type"] == "flag":
            flags = arg_config["terminal_flag"]
            if isinstance(flags, str):
                flags = [flags]
            parser.add_argument(*flags, action="store_true")
        elif arg_config["type"] == "value":
            flags = arg_config["terminal_flag"]
            if isinstance(flags, str):
                flags = [flags]
            parser.add_argument(*flags)
    
    return parser

def bootstrap_interface():
    """Bootstrap interface with error recovery"""
    try:
        from interfaces.ui_terminal import MaoTerminalInterface
        return MaoTerminalInterface()
    except ImportError:
        # Critical bootstrap failure - minimal fallback
        import sys
        sys.stderr.write("Bootstrap error: Cannot import Mao interface\n")
        sys.stderr.write("Run: pip install -r requirements.txt\n")
        sys.exit(1)

def main():
    """Ultra-minimal entry point - pure routing only"""
    
    # Load configuration and create parser
    config = load_cli_config()
    parser = create_parser_from_config(config)
    args = parser.parse_args()
    
    # Bootstrap interface - let it handle ALL logic and output
    interface = bootstrap_interface()
    
    # Route request - interface handles everything else
    # This is the ONLY logic in this file
    try:
        if hasattr(args, 'interactive') and args.interactive:
            interface.start_interactive_mode()
        elif hasattr(args, 'goal') and args.goal:
            interface.execute_goal(args.goal)
        else:
            interface.start_interactive_mode()  # Default to interactive
            
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        # Even this should go through interface eventually
        interface.handle_critical_error(e)

if __name__ == "__main__":
    main()