#!/usr/bin/env python3
"""
Mao Terminal UI Onboarding Command
Always launches with full NEW_USER_FLOW.md experience
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

@handle_errors(operation_name="launch_terminal_ui_onboarding", return_dict=True)
def execute_command(data: Any = None) -> Dict[str, Any]:
    """Launch Mao terminal UI with full onboarding experience"""
    
    try:
        # Import terminal app components
        from interfaces.terminal.app import MaoTerminalApp
        from interfaces.terminal.onboarding.welcome_flow import WelcomeFlow
        
        # Create and run the terminal app with forced onboarding
        return asyncio.run(launch_terminal_app_onboarding())
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to launch terminal UI: {str(e)}",
            "message": "Could not start the Mao onboarding experience"
        }

async def launch_terminal_app_onboarding() -> Dict[str, Any]:
    """Launch terminal app with FORCED onboarding (NEW_USER_FLOW.md)"""
    
    try:
        # Create the terminal app
        app = MaoTerminalApp()
        
        # ALWAYS run full onboarding flow (like single 'mao' command)
        welcome = WelcomeFlow()
        user_data = await welcome.start_login_flow(app)
        app.set_user_data(user_data)
        
        # Launch the beautiful terminal UI
        await app.run_async()
        
        return {
            "success": True,
            "message": "Terminal UI launched with onboarding",
            "user": user_data.get('username', 'Unknown') if user_data else None,
            "flow": "full_onboarding"
        }
        
    except KeyboardInterrupt:
        return {
            "success": True,
            "message": "Onboarding interrupted by user",
            "interrupted": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Onboarding encountered an error"
        }

# Standalone function for button imports
def launch_terminal_ui_onboarding(params=None):
    """Standalone function for button file imports"""
    return execute_command(params)