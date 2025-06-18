#!/usr/bin/env python3
"""
Test the integrated conversational tool discovery in action!
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent))
from interfaces.terminal import SFATerminalInterface

async def test_integrated_tools():
    """Test the full conversational tool discovery integration"""
    
    print("🎭 INTEGRATED TOOL DISCOVERY TEST")
    print("="*80)
    
    sfa = SFATerminalInterface(config_dir="../configs", verbose=True)
    
    # Test with a goal that should trigger tool suggestions
    goal = "Create a comprehensive marketing strategy for a tech startup including competitor analysis and visual assets"
    
    print(f"🎯 Goal: {goal}")
    print("-"*60)
    
    with patch('builtins.input', return_value='y'):
        result = await sfa.execute_goal(goal, workspace="integrated_tools_test")
    
    print("\n" + "="*80)
    print("🎯 INTEGRATION TEST COMPLETE!")
    print("Check the workflow above for tool integration! 🔧✨")

if __name__ == "__main__":
    asyncio.run(test_integrated_tools())
