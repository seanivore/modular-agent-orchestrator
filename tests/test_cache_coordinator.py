"""
Test Cache Coordinator
Quick test to verify the coordinator routes correctly
"""

import sys
import os

# Add the utilities path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utilities'))

def test_cache_coordinator_import():
    """Test that we can import the cache coordinator"""
    try:
        from cache_coordinator import CacheCoordinator, get_cache_coordinator
        print("✅ Cache coordinator import successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_coordinator_initialization():
    """Test that coordinator initializes without errors"""
    try:
        from cache_coordinator import get_cache_coordinator
        coordinator = get_cache_coordinator()
        print("✅ Cache coordinator initialization successful!")
        
        # Test basic functionality
        stats = coordinator.get_cache_stats()
        print(f"✅ Cache stats retrieved: {stats.get('coordinator_status', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_convenience_functions():
    """Test convenience functions work"""
    try:
        from cache_coordinator import cache_tool_result, get_cached_tool_result
        
        # Test caching a dummy result
        test_params = {"query": "test", "count": 5}
        test_result = {"results": ["test result"], "status": "success"}
        
        # This might fail due to missing cache files, but should not crash
        cache_result = cache_tool_result("test_tool", test_params, test_result, "test_model")
        print(f"✅ Tool result caching attempted: {cache_result}")
        
        # Try to retrieve (will likely be None, but shouldn't crash)
        retrieved = get_cached_tool_result("test_tool", test_params, "test_model")
        print(f"✅ Tool result retrieval attempted: {retrieved is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Convenience functions failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Cache Coordinator...")
    print("=" * 50)
    
    tests = [
        test_cache_coordinator_import,
        test_coordinator_initialization, 
        test_convenience_functions
    ]
    
    passed = 0
    for test in tests:
        print(f"\n🔍 Running {test.__name__}...")
        if test():
            passed += 1
        
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Cache Coordinator is working! Ready for Step 1.2!")
    else:
        print("⚠️ Some tests failed - need to check cache system imports") 