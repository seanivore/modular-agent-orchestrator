"""
BRAVE SEARCH TOOL
Button Snippet Generators
"""

from typing import Dict, Any


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude execution
    Universal model compatibility via code generation
    
    Args:
        params: Search parameters (query, count, country, search_type)
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    # Extract parameters with defaults
    query = params.get("query", "")
    count = params.get("count", 10)
    country = params.get("country", "US")
    search_type = params.get("search_type", "web")
    
    # Generate snippet that imports and uses the logic file
    snippet = f'''# Brave Search Tool Execution
import sys
import os
sys.path.append(Path(Path(Path(__file__).parent.resolve().parent)))

from tools.brave_search.brave_search import search_web, search_news, search_local, estimate_cost, validate_api_key

def main():
    """Execute Brave search using standardized logic"""
    
    # Search parameters
    query = "{query}"
    count = {count}
    country = "{country}"
    search_type = "{search_type}"
    
    print(f"🔍 Brave {{search_type.title()}} Search: {{query}}")
    
    # Validate API key first
    validation = validate_api_key()
    if not validation["valid"]:
        print(f"❌ API Error: {{validation['error']}}")
        return validation
    
    # Execute search using logic file function
    if search_type == "news":
        result = search_news(query, count, country)
    elif search_type == "local":
        result = search_local(query, count, country)
    else:
        result = search_web(query, count, country, search_type)
    
    # Display results
    if result.get("error"):
        print(f"❌ Search Error: {{result['error']}}")
    else:
        result_key = "articles" if search_type == "news" else "results"
        results_count = result.get("count", 0)
        print(f"✅ Found {{results_count}} results")
        
        # Show top 3 results
        for i, item in enumerate(result.get(result_key, [])[:3], 1):
            print(f"\\n{{i}}. {{item.get(')title', 'No title')}}"
            print(f"   {{item.get('description', 'No description')[:100]}}...")
            print(f"   {{item.get('url', 'No URL')}}")
    
    # Calculate cost
    cost_params = {{"query": query, "count": count, "search_type": search_type}}
    cost = estimate_cost(cost_params)
    print(f"\\n💰 Cost: ${{cost:.4f}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🎯 Search {{\"completed\" if result.get('status') == 'success' else \"failed\"}}")
'''
    
    return snippet


def create_news_search_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """Generate news search specific snippet"""
    news_params = params.copy()
    news_params["search_type"] = "news"
    return create_button_snippet(news_params, model)


def create_local_search_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """Generate local search specific snippet"""
    local_params = params.copy()
    local_params["search_type"] = "local"
    return create_button_snippet(local_params, model)


def create_api_validation_snippet(model: str = "claude-sonnet-4") -> str:
    """Generate API key validation snippet"""
    snippet = f'''# Brave API Key Validation
import sys
import os
sys.path.append(Path(Path(Path(__file__).parent.resolve().parent)))

from tools.brave_search.brave_search import validate_api_key, estimate_cost

def main():
    """Validate Brave API key using standardized logic"""
    
    print("🔑 Brave API Validation...")
    
    result = validate_api_key()
    
    if result["valid"]:
        print("✅ API key is valid and ready")
        print(f"   Key length: {{result['key_length']}} characters")
    else:
        print(f"❌ Validation failed: {{result['error']}}")
    
    # Calculate cost (validation is free)
    cost = estimate_cost({{"operation": "validation"}})
    print(f"💰 Cost: ${{cost:.4f}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🎯 Validation {{\"passed\" if result['valid'] else \"failed\"}}")
'''
    
    return snippet


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for executing this tool - standardized naming"""
    # Import from logic file for consistency
    from tools.brave_search.brave_search import estimate_cost as logic_estimate_cost
    from pathlib import Path
    return logic_estimate_cost(params)
