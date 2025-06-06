#!/usr/bin/env python3
"""
Quick test of SFA v4 functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent))

from sfa_v4_main import SFATerminal

async def test_sfa():
    """Test the SFA with a realistic goal"""
    
    sfa = SFATerminal()
    
    goal = "Create a marketing strategy for a sustainable packaging startup"
    
    print("🧪 TESTING SFA v4 WITH REAL GOAL")
    print("=" * 60)
    
    result = await sfa.execute_goal(goal, workspace="test_workspace")
    
    if result.get("success"):
        print("\n🎉 SUCCESS! SFA v4 is working!")
        print(f"📁 Check: {result['workspace']}")
        print(f"💰 Cost: ${result['total_cost']:.4f}")
    else:
        print(f"\n❌ FAILED: {result}")

if __name__ == "__main__":
    asyncio.run(test_sfa())
