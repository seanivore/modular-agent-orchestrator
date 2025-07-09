#!/usr/bin/env python3
"""
Mao Onboarding Command - Display Components  
UI components for the new user onboarding experience
"""

from typing import Dict, Any

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

# Standard cache instance
cache = CacheManager()
from orchestrator.cache.cache_system import CacheManager

# Standard cache instance
cache = CacheManager()

def format_onboarding_status(result: Dict[str, Any]) -> str:
    """Format the onboarding status for display"""
    
    if result.get("success"):
        if result.get("interrupted"):
            return "👋 Onboarding interrupted by user"
        elif result.get("user"):
            return f"🎭 Welcome to Mao, {result['user']}! Onboarding complete."
        else:
            return "🎭 Welcome to Mao! Onboarding completed successfully."
    else:
        error = result.get("error", "Unknown error")
        return f"❌ Onboarding failed: {error}"

def get_onboarding_help() -> str:
    """Get help text for the onboarding command"""
    
    return """
🎭 Mao New User Onboarding Experience

USAGE:
  mao --onboard             Always start with full onboarding

ONBOARDING FLOW:
  1. Welcome screen with Mao branding
  2. Username entry and validation  
  3. Theme selection with live previews
  4. Settings configuration
  5. Introduction to main interface

FEATURES:
  • Guided setup for new users
  • Theme preview with diff examples
  • User preferences configuration
  • Introduction to Mao capabilities
  • Smooth transition to main interface

FIRST TIME EXPERIENCE:
  • Learn about Mao's workflow orchestration
  • See visual examples of the interface
  • Configure your preferred settings
  • Get familiar with command structure

This command ensures every user gets the complete Mao
introduction experience, regardless of previous usage.
"""

def create_onboarding_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary of the onboarding experience"""
    
    return {
        "status": "success" if result.get("success") else "failed",
        "message": format_onboarding_status(result),
        "details": {
            "user": result.get("user"),
            "flow": result.get("flow", "full_onboarding"),
            "interrupted": result.get("interrupted", False),
            "error": result.get("error") if not result.get("success") else None
        },
        "next_steps": [
            "Explore the conversation interface",
            "Try creating your first workflow",
            "Use '/' to see available commands",
            "Check out /help for more information"
        ] if result.get("success") else []
    }

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate onboard UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free