#!/usr/bin/env python3
"""
Test the fully integrated hybrid caching system!
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent))
from interfaces.terminal import SFATerminalInterface

async def test_integrated_caching():
    """Test the complete caching integration"""
    
    print("💾 INTEGRATED CACHING SYSTEM TEST")
    print("="*80)
    
    sfa = SFATerminalInterface(config_dir="../configs", verbose=True)
    
    # Test with a goal that should trigger caching
    goal = "Create a marketing strategy for a sustainable tech startup"
    
    print(f"🎯 Goal: {goal}")
    print("-"*60)
    
    print("\n🔄 FIRST RUN (Building Caches):")
    with patch('builtins.input', return_value='y'):
        result1 = await sfa.execute_goal(goal, workspace="cache_test_1")
    
    print(f"\n💰 First run cost: ${result1.get('total_cost', 0):.4f}")
    
    print("\n" + "="*60)
    print("🔄 SECOND RUN (Using Caches):")
    
    # Same goal should use cached analysis
    with patch('builtins.input', return_value='y'):
        result2 = await sfa.execute_goal(goal, workspace="cache_test_2")
    
    print(f"\n💰 Second run cost: ${result2.get('total_cost', 0):.4f}")
    
    # Show cache savings
    if result1.get('total_cost') and result2.get('total_cost'):
        savings = result1['total_cost'] - result2['total_cost']
        savings_pct = (savings / result1['total_cost']) * 100
        print(f"\n🎉 CACHE SAVINGS: ${savings:.4f} ({savings_pct:.1f}% reduction!)")
    
    print("\n" + "="*80)
    print("🎯 CACHING INTEGRATION TEST COMPLETE!")
    print("Check cache directory: ~/.sfa_cache/ 💾")

if __name__ == "__main__":
    asyncio.run(test_integrated_caching())
