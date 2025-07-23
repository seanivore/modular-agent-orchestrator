#!/usr/bin/env python3
"""
Mao Terminal UI Launch Command - Display Components
UI components for launching the terminal interface
"""

from typing import Dict, Any
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="format_launch_status", return_dict=False)
def format_launch_status(result: Dict[str, Any]) -> str:
    """Format the terminal UI launch status for display"""
    
    if result.get("success"):
        if result.get("interrupted"):
            return "[CLOSED] Terminal UI closed by user"
        elif result.get("user"):
            return f"[LAUNCHED] Terminal UI launched for user: {result['user']}"
        else:
            return "[LAUNCHED] Terminal UI launched successfully"
    else:
        error = result.get("error", "Unknown error")
        return f"[ERROR] Failed to launch terminal UI: {error}"

@handle_errors(operation_name="get_launch_help", return_dict=False)
def get_launch_help() -> str:
    """Get help text for the terminal UI launch command"""
    
    return """
[MAO] Terminal UI Launch Command

USAGE:
  mao --mao                 Launch the beautiful terminal interface

FEATURES:
  • Conversation interface with CLI auto-complete
  • Workflow creation and management
  • Real-time progress visualization
  • User session management
  • Beautiful Mao visual protocol

FIRST TIME USERS:
  • Username setup with theme selection
  • Guided onboarding experience
  • Theme preview with live examples

RETURNING USERS:
  • Quick launch with saved preferences
  • Automatic session restoration
  • Personalized welcome experience

KEYBOARD SHORTCUTS:
  • Ctrl+C or 'q' to quit
  • Tab to navigate
  • ' / ' to trigger auto-complete
  • Esc to go back

The terminal UI provides a complete environment for AI workflow
orchestration with a professional, Claude Code-inspired interface.
"""

@handle_errors(operation_name="create_launch_summary", return_dict=True)
def create_launch_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary of the launch attempt"""
    
    return {
        "status": "success" if result.get("success") else "failed",
        "message": format_launch_status(result),
        "details": {
            "user": result.get("user"),
            "interrupted": result.get("interrupted", False),
            "error": result.get("error") if not result.get("success") else None
        },
        "help_available": True
    }

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free