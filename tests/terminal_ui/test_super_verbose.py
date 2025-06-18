#!/usr/bin/env python3
"""
Test the SUPER verbose mode - show ALL the technical details!
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent))
from interfaces.terminal import SFATerminalInterface

async def test_super_verbose():
    """Test the enhanced verbose mode"""
    
    print("🔍 TESTING SUPER VERBOSE MODE")
    print("="*80)
    
    sfa = SFATerminalInterface(config_dir="../configs", verbose=True)
    
    goal = "Create a simple logo design strategy"
    
    with patch('builtins.input', return_value='y'):
        result = await sfa.execute_goal(goal, workspace="super_verbose_test")
    
    print("\n" + "="*80)
    print("🎯 VERBOSE MODE TEST COMPLETE!")
    print("Check all the technical details above! 🔍✨")

if __name__ == "__main__":
    asyncio.run(test_super_verbose())
