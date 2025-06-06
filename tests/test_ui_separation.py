#!/usr/bin/env python3
"""
Test the clean interface separation with verbose vs normal display
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from interfaces.terminal import SFATerminalInterface

async def test_clean_ui():
    """Test both normal and verbose interfaces"""
    
    goal = "Create a simple content marketing plan"
    
    print("🎨 TESTING CLEAN UI SEPARATION")
    print("="*80)
    
    # Test 1: Normal user interface (clean, simple)
    print("\n👤 NORMAL USER EXPERIENCE:")
    print("-"*40)
    sfa_normal = SFATerminalInterface(config_dir="../configs", verbose=False)
    
    # Mock the input to auto-confirm
    from unittest.mock import patch
    with patch('builtins.input', return_value='y'):
        result1 = await sfa_normal.execute_goal(goal, workspace="tests/normal_ui_test")
    
    print("\n" + "="*80)
    
    # Test 2: Developer interface (verbose, technical)
    print("\n🛠️  DEVELOPER EXPERIENCE (--verbose):")
    print("-"*40)
    sfa_verbose = SFATerminalInterface(config_dir="../configs", verbose=True)
    
    with patch('builtins.input', return_value='y'):
        result2 = await sfa_verbose.execute_goal(goal, workspace="tests/verbose_ui_test")
    
    print("\n" + "="*80)
    print("🎯 UI SEPARATION TEST COMPLETE!")
    print("Check the difference in output above! 🎨✨")

if __name__ == "__main__":
    asyncio.run(test_clean_ui())
