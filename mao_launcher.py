#!/usr/bin/env python3
"""
Mao Terminal Application Launcher
Entry point for the beautiful MAO terminal UI
Handles command-line arguments and launches the appropriate interface
"""

import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from interfaces.terminal.app import MaoTerminalApp
from interfaces.terminal.onboarding.welcome_flow import WelcomeFlow
from interfaces.ui_terminal import TerminalInterface


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        prog='mao',
        description='MAO - AI Workflow Orchestrator Terminal Interface',
        epilog='Examples:\n  mao mao          # Launch beautiful terminal UI\n  mao --login      # Force login screen\n  mao --continue   # Continue last session\n  mao --config     # Open configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main command argument
    parser.add_argument(
        'command',
        nargs='?',
        default='mao',
        help='Command to execute (default: mao)'
    )
    
    # Launch options
    parser.add_argument(
        '--login',
        action='store_true',
        help='Force login screen regardless of quick launch settings'
    )
    
    parser.add_argument(
        '--continue',
        action='store_true',
        help='Continue last session without login prompt'
    )
    
    parser.add_argument(
        '--config',
        action='store_true',
        help='Open configuration settings'
    )
    
    parser.add_argument(
        '--setup',
        metavar='WORKFLOW_DIR',
        help='Setup workflow from directory (e.g., --setup ./marketing_strategy/)'
    )
    
    parser.add_argument(
        '--workflow',
        metavar='WORKFLOW_ID',
        help='Show workflow details for given ID'
    )
    
    parser.add_argument(
        '--model',
        metavar='MODEL_NAME',
        help='Set favorite model'
    )
    
    parser.add_argument(
        '--provider',
        metavar='PROVIDER_NAME',
        help='Set default provider'
    )
    
    # List options
    parser.add_argument(
        '--model-list',
        action='store_true',
        help='List all available models'
    )
    
    parser.add_argument(
        '--provider-list',
        action='store_true',
        help='List all available providers'
    )
    
    # Debug options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='MAO Terminal Interface v4.0.0'
    )
    
    return parser


def handle_cli_arguments(args):
    """Handle command line arguments that don't require the full UI"""
    
    terminal = TerminalInterface(verbose=args.verbose)
    
    # Handle list commands
    if args.model_list:
        result = terminal.execute_cli_command('models')
        print(result.get('message', 'No models available'))
        return True
        
    if args.provider_list:
        result = terminal.execute_cli_command('providers')
        print(result.get('message', 'No providers available'))
        return True
        
    # Handle setting commands
    if args.model:
        result = terminal.execute_cli_command('set_model', args.model)
        print(result.get('message', f'Model set to {args.model}'))
        return True
        
    if args.provider:
        result = terminal.execute_cli_command('default_provider', args.provider)
        print(result.get('message', f'Provider set to {args.provider}'))
        return True
        
    # Handle workflow commands
    if args.workflow:
        result = terminal.execute_cli_command('workflow', args.workflow)
        print(result.get('message', f'Workflow details for {args.workflow}'))
        return True
        
    if args.setup:
        result = terminal.execute_cli_command('setup', args.setup)
        print(result.get('message', f'Setup workflow from {args.setup}'))
        return True
        
    # No CLI command handled
    return False


async def launch_terminal_ui(args):
    """Launch the beautiful terminal UI"""
    
    try:
        # Create the terminal app
        app = MaoTerminalApp()
        
        # Handle different launch modes
        if args.login:
            # Force login flow
            welcome = WelcomeFlow()
            user_data = await welcome.start_login_flow(app)
            app.set_user_data(user_data)
            
        elif args.continue:
            # Try to start last session
            welcome = WelcomeFlow()
            user_data = welcome.get_last_user()
            
            if user_data and welcome.should_auto_login(user_data['settings']):
                app.set_user_data(user_data)
            else:
                # Fall back to login
                user_data = await welcome.start_login_flow(app)
                app.set_user_data(user_data)
                
        elif args.config:
            # Open config directly (after login if needed)
            welcome = WelcomeFlow()
            user_data = welcome.get_last_user()
            
            if not user_data:
                user_data = await welcome.start_login_flow(app)
                
            app.set_user_data(user_data)
            app.show_config_screen()
            
        else:
            # Default launch - check quick launch settings
            welcome = WelcomeFlow()
            user_data = welcome.get_last_user()
            
            if user_data and welcome.should_auto_login(user_data['settings']):
                # Quick launch
                app.set_user_data(user_data)
            else:
                # Need login
                user_data = await welcome.start_login_flow(app)
                app.set_user_data(user_data)
        
        # Launch the beautiful terminal UI
        await app.run_async()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye from MAO!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error launching MAO terminal: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point"""
    
    # Parse command line arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle the special case of 'mao mao'
    if args.command == 'mao':
        # This is the beautiful terminal UI launch
        import asyncio
        asyncio.run(launch_terminal_ui(args))
        return
        
    # Handle other CLI commands that don't need the full UI
    if handle_cli_arguments(args):
        return
        
    # If we get here, the command wasn't recognized
    print(f"❌ Unknown command: {args.command}")
    print("💡 Try 'mao mao' to launch the terminal UI")
    print("💡 Or 'mao --help' for all options")
    sys.exit(1)


if __name__ == "__main__":
    main()