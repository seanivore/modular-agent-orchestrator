#!/usr/bin/env python3
"""
Mao Main CLI Entry Point
Modular Agent Orchestrator - Revolutionary AI Workflow System

Clean, simple routing following Mao protection rules:
- Variable-input philosophy (no hardcoded workflows)
- Print statements only for critical errors
- Simple argument parsing and interface routing
- Universal compatibility and modularity
"""

import sys
import argparse
from pathlib import Path

# Add project root to path for clean imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from interfaces.ui_terminal import MaoTerminalInterface
except ImportError as e:
    print(f"❌ Failed to import MAO interface: {e}")
    print("💡 Run: pip install -r requirements.txt")
    sys.exit(1)


def create_argument_parser():
    """Create argument parser following variable-input philosophy"""
    
    parser = argparse.ArgumentParser(
        description="MAO - Modular Agent Orchestrator v4.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mao_v4.py "Create a marketing strategy for my startup"
  python mao_v4.py "Help me prepare for job interviews"
  python mao_v4.py --stats
  python mao_v4.py --workflows
  python mao_v4.py --interactive

MAO uses variable-input philosophy - describe any goal in natural language.
No predefined categories or workflows. Maximum flexibility.
        """
    )
    
    # Core execution modes
    parser.add_argument(
        "goal", 
        nargs="?", 
        help="Natural language goal - any task, any domain, any approach"
    )
    
    # System management
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Show system performance and orchestrator statistics"
    )
    parser.add_argument(
        "--workflows", 
        action="store_true", 
        help="List all configured workflows and their status"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Start interactive chat mode for workflow creation"
    )
    
    # Execution preferences
    parser.add_argument(
        "--workspace", "-w", 
        help="Custom workspace directory for outputs"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Show detailed technical information"
    )
    parser.add_argument(
        "--free-only", 
        action="store_true", 
        help="Use only free models (cost optimization)"
    )
    parser.add_argument(
        "--privacy", 
        action="store_true", 
        help="Use privacy-focused models and providers"
    )
    
    # Development and debugging
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode with detailed logging"
    )
    parser.add_argument(
        "--config", 
        action="store_true", 
        help="Show configuration management interface"
    )
    
    return parser


def main():
    """🚀 Clean entry point with simple routing"""
    
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Initialize MAO interface with minimal error handling
    try:
        mao = MaoTerminalInterface(verbose=args.verbose)
    except Exception as e:
        print(f"❌ Failed to initialize MAO: {e}")
        sys.exit(1)
    
    # Simple request routing - let interface handle all formatting and logic
    try:
        # System information requests
        if args.stats:
            mao.show_stats()
            return
        
        if args.workflows:
            mao.list_workflows()
            return
        
        if args.config:
            mao.show_config()
            return
        
        # Interactive mode
        if args.interactive:
            mao.start_interactive_mode()
            return
        
        # Goal execution (variable-input - any natural language goal)
        if args.goal:
            # Create preferences dictionary
            preferences = {}
            if args.free_only:
                preferences["cost_optimization"] = "free_models_only"
            if args.privacy:
                preferences["privacy_focus"] = True
            if args.debug:
                preferences["debug_mode"] = True
            
            # Route to interface - let it handle all formatting and workflow logic
            result = mao.execute_goal(
                goal=args.goal,
                workspace=args.workspace,
                preferences=preferences
            )
            
            # Simple success/failure - interface handles all detailed output
            if not result.get("success", True):
                sys.exit(1)
            return
        
        # No arguments - show help or start interactive mode
        if len(sys.argv) == 1:
            mao.start_interactive_mode()
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        # Clean exit on Ctrl+C - no output needed
        sys.exit(0)
    except Exception as e:
        # Critical error - minimal output only
        print(f"❌ Critical error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()