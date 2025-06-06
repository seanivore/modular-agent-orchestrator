#!/usr/bin/env python3
"""
Quick test of SFA v4 functionality - auto confirm
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent))

from sfa_v4_main import SFATerminal

async def test_sfa():
    """Test the SFA with a realistic goal"""
    
    sfa = SFATerminal()
    
    goal = "Create a simple marketing plan for a tech startup"
    
    print("🧪 TESTING SFA v4 WITH REAL GOAL")
    print("=" * 60)
    
    # Mock the input to automatically confirm
    with patch('builtins.input', return_value='y'):
        result = await sfa.execute_goal(goal, workspace="test_workspace")
    
    if result.get("success"):
        print("\n🎉 SUCCESS! SFA v4 is WORKING!")
        print(f"📁 Check: {result['workspace']}")
        print(f"💰 Cost: ${result['total_cost']:.4f}")
        print(f"📄 Deliverables: {len(result['deliverables'])} files created")
        
        # List the actual files created
        workspace = Path(result['workspace'])
        if workspace.exists():
            print(f"\n📁 FILES CREATED:")
            for file in workspace.iterdir():
                if file.is_file():
                    print(f"  ✅ {file.name}")
        
    else:
        print(f"\n❌ FAILED: {result}")

if __name__ == "__main__":
    asyncio.run(test_sfa())
