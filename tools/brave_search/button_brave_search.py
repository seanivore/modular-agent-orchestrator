"""
BRAVE SEARCH TOOL
Human Button Generators
"""

from typing import Dict, Any


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude 4 execution
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
    
    # Generate self-contained executable snippet
    snippet = f'''# Brave Search Tool Execution
# Model: {model}
# Query: {query}

import json
import requests
import os
import time
from datetime import datetime

def execute_brave_search():
    """Execute Brave web search with comprehensive error handling"""
    
    # Search parameters
    query = "{query}"
    count = {count}
    country = "{country}"
    search_type = "{search_type}"
    
    try:
        # Validation
        if not query.strip():
            return {{"error": "Search query cannot be empty", "cost": 0.0}}
        
        # Clamp count to valid range
        count = min(20, max(1, count))
        
        # API Configuration
        api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
        if not api_key:
            return {{
                "error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable",
                "cost": 0.0
            }}
        
        # Endpoint selection
        endpoints = {{
            "web": "https://api.search.brave.com/res/v1/web/search",
            "news": "https://api.search.brave.com/res/v1/news/search", 
            "local": "https://api.search.brave.com/res/v1/web/search"
        }}
        
        url = endpoints.get(search_type, endpoints["web"])
        
        # Headers configuration
        headers = {{
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }}
        
        # Search parameters
        base_params = {{
            "q": query,
            "count": count,
            "country": country,
            "search_lang": "en",
            "ui_lang": "en-US",
            "spellcheck": 1
        }}
        
        # Type-specific parameters
        if search_type == "news":
            base_params["freshness"] = "pd"  # Past day for news
        elif search_type == "local":
            base_params["result_filter"] = "web"
            base_params["q"] = f"{{query}} near {{country}}"
        
        # Perform search with retry logic
        max_retries = 3
        last_error = None
        response = None
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=base_params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2
                        time.sleep(wait_time)
                        continue
                else:
                    last_error = f"HTTP {{response.status_code}}: {{response.text[:200]}}"
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                        
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {{attempt + 1}}/{{max_retries}})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {{str(e)}}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Check final response
        if response is None or response.status_code != 200:
            return {{
                "error": f"Search failed after {{max_retries}} attempts. Last error: {{last_error}}",
                "status_code": response.status_code if response else None,
                "cost": 0.001  # Minimal cost for failed attempt
            }}
        
        # Parse results
        data = response.json()
        
        # Extract results based on search type
        if search_type == "news":
            results = data.get("results", [])
            result_key = "articles"
        else:
            results = data.get("web", {{}}).get("results", [])
            result_key = "results"
        
        if not results:
            return {{
                "query": query,
                "search_type": search_type,
                "count": 0,
                result_key: [],
                "message": f"No results found for: {{query}}",
                "cost": 0.001
            }}
        
        # Process results
        processed_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            description = result.get("description", "No description")
            
            processed_result = {{
                "rank": i,
                "title": title,
                "url": url, 
                "description": description
            }}
            
            # Additional fields for news
            if search_type == "news":
                processed_result["age"] = result.get("age", "Unknown age")
            
            processed_results.append(processed_result)
        
        # Create comprehensive result data
        search_results = {{
            "status": "success",
            "query": query,
            "search_type": search_type,
            "timestamp": datetime.now().isoformat(),
            "count": len(processed_results),
            "country": country,
            result_key: processed_results,
            "metadata": {{
                "api_response_time": getattr(response, "elapsed", None).total_seconds() if hasattr(response, "elapsed") else None,
                "total_available": data.get("web", {{}}).get("total", len(results)) if search_type != "news" else len(results),
                "request_params": base_params
            }},
            "cost": 0.001  # Brave API is typically free
        }}
        
        return search_results
        
    except Exception as e:
        return {{
            "error": f"Brave search failed: {{str(e)}}",
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "cost": 0.001
        }}

# Execute the search
result = execute_brave_search()

# Display results
print("🔍 Brave Search Results:")
print(f"Query: {query}")
print(f"Type: {search_type}")
print(f"Results: {{result.get('count', 0)}}")
print(f"Cost: ${{result.get('cost', 0.001):.4f}}")

if result.get('error'):
    print(f"❌ Error: {{result['error']}}")
else:
    print("✅ Search completed successfully")

# Return structured result for orchestrator
result'''
    
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
# Model: {model}

import os

def validate_brave_api():
    """Validate Brave API key availability"""
    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
    
    if not api_key:
        return {{
            "valid": False,
            "error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable",
            "cost": 0.0
        }}
    
    return {{
        "valid": True,
        "key_length": len(api_key),
        "message": "API key found and ready",
        "cost": 0.0
    }}

# Execute validation
result = validate_brave_api()

print("🔑 Brave API Validation:")
if result["valid"]:
    print("✅ API key is valid and ready")
else:
    print(f"❌ Validation failed: {{result['error']}}")

print(f"💰 Cost: ${{result['cost']:.4f}}")

# Return result
result'''
    
    return snippet


def estimate_execution_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for executing this tool"""
    # Brave API is typically free for reasonable usage
    return 0.001


def get_tool_capabilities() -> Dict[str, Any]:
    """Return tool capabilities for orchestrator discovery"""
    return {
        "name": "brave_search",
        "capabilities": ["web_search", "news_search", "local_search", "real_time_data"],
        "cost_estimate": 0.001,
        "models_supported": ["all"],
        "tags": ["search", "web", "research", "privacy", "independent"],
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Search query"},
            "count": {"type": "integer", "default": 10, "description": "Number of results (1-20)"},
            "country": {"type": "string", "default": "US", "description": "Country code for localized results"},
            "search_type": {"type": "string", "default": "web", "description": "Type of search (web, news, local)"}
        }
    }