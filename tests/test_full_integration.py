#!/usr/bin/env python3
"""
🎯 Phase 1 Integration Test
Tests orchestrator + tool discovery + cache coordinator working together
"""

from orchestrator.core import WorkflowOrchestrator
from orchestrator.manager_tools import discover_tools_for_goal

def test_full_integration():
    """Test the complete Phase 1 integration"""
    print('🧪 Testing Full Phase 1 Integration...')
    print('=' * 60)
    
    # Test 1: Orchestrator initialization
    print('🔍 Test 1: Orchestrator Initialization...')
    try:
        orchestrator = WorkflowOrchestrator()
        print('✅ Orchestrator initialized with cache coordinator!')
    except Exception as e:
        print(f'❌ Orchestrator error: {e}')
        return False
    
    # Test 2: Tool discovery
    print('\n🔍 Test 2: Tool Discovery...')
    try:
        result = discover_tools_for_goal('research AI trends', 'claude-sonnet-4', 'balanced')
        core_tools = result.get('core_tools', [])
        print(f'✅ Tool discovery working! Found {len(core_tools)} core tools')
        if core_tools:
            print(f'   Core tools: {", ".join(core_tools)}')
    except Exception as e:
        print(f'❌ Tool discovery error: {e}')
        return False
    
    # Test 3: Cache coordinator integration
    print('\n🔍 Test 3: Cache Coordinator Integration...')
    try:
        # Test cache through orchestrator
        test_data = {"test": "integration_data"}
        cache_key = "integration_test"
        
        # This should go through the cache coordinator
        orchestrator.cache_coordinator.cache_goal_analysis(cache_key, test_data, "test")
        retrieved = orchestrator.cache_coordinator.get_cached_goal_analysis(cache_key, "test")
        
        if retrieved == test_data:
            print('✅ Cache coordinator integration working!')
        else:
            print('❌ Cache data mismatch')
            return False
    except Exception as e:
        print(f'❌ Cache integration error: {e}')
        return False
    
    # Test 4: Model manager integration
    print('\n🔍 Test 4: Model Manager Integration...')
    try:
        best_model = orchestrator.model_manager.get_best_model_for_task('research')
        if best_model:
            print(f'✅ Model manager working! Best research model: {best_model}')
        else:
            print('❌ No model found for research task')
            return False
    except Exception as e:
        print(f'❌ Model manager error: {e}')
        return False
    
    print('\n' + '=' * 60)
    print('🎉 PHASE 1 INTEGRATION COMPLETE!')
    print('🏭 Ready for the kinects big ball factory!')
    print('✅ All systems working together beautifully!')
    return True

if __name__ == "__main__":
    success = test_full_integration()
    exit(0 if success else 1) 