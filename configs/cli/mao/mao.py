#!/usr/bin/env python3
"""
Mao Terminal UI Launch Command
Launches the beautiful terminal interface with conversation system
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    return 0.0  # No cost for launching UI

@handle_errors(operation_name="launch_terminal_ui", return_dict=True)
def execute_command(data: Any = None) -> Dict[str, Any]:
    """Launch the beautiful Mao terminal UI"""
    
    try:
        # Import terminal app components
        from interfaces.terminal.app import MaoTerminalApp
        from interfaces.terminal.onboarding.welcome_flow import WelcomeFlow
        
        # Create and run the terminal app
        return asyncio.run(launch_terminal_app())
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to launch terminal UI: {str(e)}",
            "message": "Could not start the Mao terminal interface"
        }

async def launch_terminal_app() -> Dict[str, Any]:
    """Launch the terminal app with proper async handling"""
    
    try:
        # Create the terminal app
        app = MaoTerminalApp()
        
        # Handle user authentication
        welcome = WelcomeFlow()
        user_data = welcome.get_last_user()
        
        if user_data and welcome.should_auto_login(user_data['settings']):
            # Quick launch for returning users
            app.set_user_data(user_data)
        else:
            # New user or forced login flow
            user_data = await welcome.start_login_flow(app)
            app.set_user_data(user_data)
        
        # Launch the beautiful terminal UI
        await app.run_async()
        
        return {
            "success": True,
            "message": "Terminal UI launched successfully",
            "user": user_data.get('username', 'Unknown') if user_data else None
        }
        
    except KeyboardInterrupt:
        return {
            "success": True,
            "message": "Terminal UI closed by user",
            "interrupted": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Terminal UI encountered an error"
        }

# Standalone function for button imports
def launch_terminal_ui(params=None):
    """Standalone function for button file imports"""
    return execute_command(params)