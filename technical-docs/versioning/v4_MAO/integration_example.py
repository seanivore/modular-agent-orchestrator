"""
Cache Integration Example
Shows how modular tools integrate with universal cache and error handling
"""

from typing import Dict, Any
from ..error_handling import handle_errors, retry_with_backoff, ValidationError
from .universal_cache import get_global_cache, cache_operation, CacheFingerprint, ModelToolMapper

# Example: How a modular tool integrates with infrastructure

@handle_errors(operation_name="web_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0)
@cache_operation(operation="web_search", ttl_hours=6, estimated_cost=0.003)
def perform_web_search(query: str, search_type: str = "comprehensive", 
                      model: str = "claude-3-5-sonnet", context: str = "") -> Dict[str, Any]:
    """
    Example of modular tool function with full infrastructure integration
    
    This shows how a tool function can use:
    - Error handling with professional patterns
    - Retry logic with exponential backoff  
    - Universal caching with fingerprinting
    - Cost tracking and optimization
    """
    
    # Validate parameters (error handling will catch ValidationError)
    if not query.strip():
        raise ValidationError("Query cannot be empty", "query", query)
    
    # Simulate web search operation
    # In real implementation, this would call actual web search API
    search_results = {
        "query": query,
        "search_type": search_type,
        "model_used": model,
        "results": [
            {"title": f"Result for {query}", "url": "https://example.com", "snippet": "Example snippet"},
            {"title": f"Another result for {query}", "url": "https://example2.com", "snippet": "Another snippet"}
        ],
        "metadata": {
            "total_results": 2,
            "search_time": 0.5,
            "cached": False  # Will be updated by cache system
        }
    }
    
    return {
        "status": "success",
        "search_data": search_results,
        "message": "Web search completed successfully"
    }

def demonstrate_cache_integration():
    """Demonstrate how cache integration works"""
    
    # Get global cache instance
    cache = get_global_cache()
    
    # Get model-tool mapper
    mapper = ModelToolMapper(cache)
    
    print("🗄️ SFA v4 Cache Integration Demo")
    print("=" * 50)
    
    # Example 1: Basic operation with caching
    print("\n1. First search (will be cached):")
    result1 = perform_web_search(
        query="AI orchestration tools",
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result1['status']}")
    print(f"   Results: {len(result1['search_data']['results'])}")
    
    # Example 2: Same search (should hit cache)
    print("\n2. Same search (should hit cache):")
    result2 = perform_web_search(
        query="AI orchestration tools", 
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result2['status']}")
    print(f"   Results: {len(result2['search_data']['results'])}")
    
    # Example 3: Show cache statistics
    print("\n3. Cache Statistics:")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Example 4: Model optimization
    print("\n4. Model Optimization:")
    optimal_model = mapper.get_optimal_model("web_search", budget_limit=0.01)
    print(f"   Optimal model for budget $0.01: {optimal_model}")
    
    cost_estimate = mapper.get_cost_estimate("web_search", "claude-3-5-sonnet", "medium")
    print(f"   Estimated cost for claude-3-5-sonnet: ${cost_estimate:.4f}")
    
    # Example 5: Manual cache fingerprinting
    print("\n5. Manual Cache Fingerprinting:")
    fingerprint = CacheFingerprint.generate_fingerprint(
        operation="web_search",
        params={"query": "test", "search_type": "quick"},
        model="claude-3-haiku"
    )
    print(f"   Generated fingerprint: {fingerprint}")
    
    print("\n✅ Cache integration demo completed!")

def demonstrate_error_handling():
    """Demonstrate error handling integration"""
    
    print("\n⚠️ Error Handling Demo")
    print("=" * 30)
    
    # Example 1: Validation error
    print("\n1. Testing validation error:")
    result = perform_web_search(query="", search_type="comprehensive")
    if "error" in result:
        print(f"   Caught validation error: {result['error']}")
        print(f"   Error code: {result['error_code']}")
    
    # Example 2: Show how retry logic would work
    print("\n2. Retry logic is built-in for network failures")
    print("   (Would automatically retry with exponential backoff)")
    
    print("\n✅ Error handling demo completed!")

if __name__ == "__main__":
    # Run demonstrations
    demonstrate_cache_integration()
    demonstrate_error_handling() 