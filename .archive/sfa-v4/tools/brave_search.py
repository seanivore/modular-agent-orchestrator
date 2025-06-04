"""
Brave Web Search Tool
Web search for AI agents via API with enhanced error handling
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import time

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "brave_web_search", 
        "name": "Brave Web Search",
        "description": "Independent web search using Brave Search API with enhanced error handling",
        "capabilities": ["web_search", "research", "current_information", "news_search", "local_search"],
        "use_cases": ["independent research", "fact checking", "alternative search perspective", "privacy-focused search", "real-time information"],
        "cost_estimate": 0.005,
        "model_compatibility": ["all"],
        "tags": ["research", "web", "privacy", "independent", "enhanced"],
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Search query"},
            "count": {"type": "integer", "default": 10, "description": "Number of results (1-20)"},
            "country": {"type": "string", "default": "US", "description": "Country code for localized results"},
            "search_type": {"type": "string", "default": "web", "enum": ["web", "news", "local"], "description": "Type of search"}
        },
        "functions": ["search_web", "search_news", "search_local"]
    }

def search_web(query: str, count: int = 10, country: str = "US", search_type: str = "web") -> Dict[str, Any]:
    """Execute Brave web search with comprehensive error handling"""
    try:
        # Validation
        if not query.strip():
            return {"error": "Search query cannot be empty"}
        
        # Clamp count to valid range
        count = min(20, max(1, count))
        
        # API Configuration
        api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
        if not api_key:
            return {"error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable"}
        
        # Endpoint selection
        endpoints = {
            "web": "https://api.search.brave.com/res/v1/web/search",
            "news": "https://api.search.brave.com/res/v1/news/search", 
            "local": "https://api.search.brave.com/res/v1/web/search"
        }
        
        url = endpoints.get(search_type, endpoints["web"])
        
        # Headers configuration
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }
        
        # Search parameters
        base_params = {
            "q": query,
            "count": count,
            "country": country,
            "search_lang": "en",
            "ui_lang": "en-US",
            "spellcheck": 1
        }
        
        # Type-specific parameters
        if search_type == "news":
            base_params["freshness"] = "pd"  # Past day for news
        elif search_type == "local":
            base_params["result_filter"] = "web"
            base_params["q"] = f"{query} near {country}"
        
        # Perform search with retry logic
        max_retries = 3
        last_error = None
        
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
                    last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                        
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {str(e)}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Check final response
        if response.status_code != 200:
            return {
                "error": f"Search failed after {max_retries} attempts. Last error: {last_error}",
                "status_code": response.status_code
            }
        
        # Parse results
        data = response.json()
        
        # Extract results based on search type
        if search_type == "news":
            results = data.get("results", [])
            result_key = "articles"
        else:
            results = data.get("web", {}).get("results", [])
            result_key = "results"
        
        if not results:
            return {
                "query": query,
                "search_type": search_type,
                "count": 0,
                result_key: [],
                "message": f"No results found for: {query}"
            }
        
        # Process results
        processed_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            description = result.get("description", "No description")
            
            processed_result = {
                "rank": i,
                "title": title,
                "url": url, 
                "description": description
            }
            
            # Additional fields for news
            if search_type == "news":
                processed_result["age"] = result.get("age", "Unknown age")
            
            processed_results.append(processed_result)
        
        # Create comprehensive result data
        search_results = {
            "status": "success",
            "query": query,
            "search_type": search_type,
            "timestamp": datetime.now().isoformat(),
            "count": len(processed_results),
            "country": country,
            result_key: processed_results,
            "metadata": {
                "api_response_time": getattr(response, "elapsed", None).total_seconds() if hasattr(response, "elapsed") else None,
                "total_available": data.get("web", {}).get("total", len(results)) if search_type != "news" else len(results),
                "request_params": base_params
            }
        }
        
        return search_results
        
    except Exception as e:
        return {
            "error": f"Brave search failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "query": query
        }

def search_news(query: str, count: int = 10, country: str = "US") -> Dict[str, Any]:
    """Search for news using Brave News API"""
    return search_web(query, count, country, "news")

def search_local(query: str, count: int = 10, country: str = "US") -> Dict[str, Any]:
    """Search for local results using Brave API"""
    return search_web(query, count, country, "local")

def validate_api_key() -> Dict[str, Any]:
    """Validate Brave API key availability"""
    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
    if not api_key:
        return {
            "valid": False,
            "error": "API key not found",
            "instructions": "Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable"
        }
    
    return {
        "valid": True,
        "key_length": len(api_key),
        "key_prefix": api_key[:8] + "..." if len(api_key) > 8 else "short_key"
    }

"""
PULLED FROM THE OLD SFA: 
"""

# SFA v4.0.0 Enhanced Tools - Complete Implementation
# Extracted best patterns from v3.3.0 and enhanced for v4 architecture

# =============================================================================
# ENHANCED BRAVE SEARCH TOOL
# =============================================================================

"""
Enhanced SFA v4 Brave Web Search Tool
Improved error handling, token efficiency, and human button integration
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "brave_web_search", 
        "name": "Brave Web Search",
        "description": "Independent web search using Brave Search API with enhanced error handling",
        "capabilities": ["web_search", "research", "current_information", "news_search", "local_search"],
        "use_cases": ["independent research", "fact checking", "alternative search perspective", "privacy-focused search", "real-time information"],
        "cost_estimate": 0.005,
        "model_compatibility": ["all"],
        "tags": ["research", "web", "privacy", "independent", "enhanced"],
        "parameters": {
            "query": {"type": "string", "required": True, "description": "Search query"},
            "count": {"type": "integer", "default": 10, "description": "Number of results (1-20)"},
            "country": {"type": "string", "default": "US", "description": "Country code for localized results"},
            "search_type": {"type": "string", "default": "web", "enum": ["web", "news", "local"], "description": "Type of search"}
        }
    }

def create_human_button_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate enhanced executable snippet for Brave web search"""
    query = params.get("query", "")
    count = min(20, max(1, params.get("count", 10)))  # Clamp to valid range
    country = params.get("country", "US") 
    search_type = params.get("search_type", "web")
    
    return f'''
# Enhanced Brave Web Search with Error Handling
import requests
import json
import os
from datetime import datetime
import time

def safe_brave_search():
    """Execute Brave search with comprehensive error handling"""
    
    # Configuration
    query = "{query}"
    count = {count}
    country = "{country}"
    search_type = "{search_type}"
    
    print(f"🔍 Brave {{search_type.title()}} Search: {{query}}")
    print(f"📊 Results: {{count}} | Region: {{country}}")
    print("="*70)
    
    # API Configuration
    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
    if not api_key:
        print("❌ Error: Brave API key not found in environment")
        print("Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable")
        return None
    
    # Endpoint selection
    endpoints = {{
        "web": "https://api.search.brave.com/res/v1/web/search",
        "news": "https://api.search.brave.com/res/v1/news/search", 
        "local": "https://api.search.brave.com/res/v1/web/search"  # Use web for local with location
    }}
    
    url = endpoints.get(search_type, endpoints["web"])
    
    # Headers with fallback
    headers = {{
        "Accept": "application/json",
        "Accept-Encoding": "gzip"
    }}
    
    # Try X-Subscription-Token first, then Authorization
    if api_key:
        headers["X-Subscription-Token"] = api_key
    
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
        base_params["q"] = f"{{query}} near {{country}}"  # Location modifier
    
    try:
        # Perform search with timeout and retries
        max_retries = 3
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
                        print(f"⏱️ Rate limited, waiting {{wait_time}} seconds...")
                        time.sleep(wait_time)
                        continue
                else:
                    print(f"⚠️ HTTP {{response.status_code}}: {{response.text[:200]}}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                        
            except requests.exceptions.Timeout:
                print(f"⏱️ Request timeout (attempt {{attempt + 1}}/{{max_retries}})")
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                print(f"🌐 Network error: {{str(e)}}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                    
        # Check final response
        if response.status_code != 200:
            print(f"❌ Search failed after {{max_retries}} attempts")
            print(f"Final status: {{response.status_code}}")
            return None
        
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
            print(f"ℹ️ No results found for: {{query}}")
            return {{"query": query, "count": 0, result_key: []}}
        
        # Display results with enhanced formatting
        print(f"📋 Found {{len(results)}} results:")
        print("="*70)
        
        processed_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            description = result.get("description", "No description")
            
            # Additional fields for news
            if search_type == "news":
                age = result.get("age", "Unknown age")
                print(f"{{i}}. **{{title}}**")
                print(f"   🔗 {{url}}")
                print(f"   📝 {{description}}")
                print(f"   ⏰ {{age}}")
            else:
                print(f"{{i}}. **{{title}}**")
                print(f"   🔗 {{url}}")
                print(f"   📝 {{description}}")
            print()
            
            # Store processed result
            processed_results.append({{
                "rank": i,
                "title": title,
                "url": url, 
                "description": description,
                **({{"age": result.get("age")}} if search_type == "news" else {{}})
            }})
        
        # Save results with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"brave_{{search_type}}_search_{{timestamp}}.json"
        
        search_results = {{
            "query": query,
            "search_type": search_type,
            "timestamp": datetime.now().isoformat(),
            "count": len(processed_results),
            "country": country,
            result_key: processed_results,
            "metadata": {{
                "api_response_time": getattr(response, "elapsed", {{}}).total_seconds() if hasattr(response, "elapsed") else None,
                "total_available": data.get("web", {{}}).get("total", len(results)) if search_type != "news" else len(results)
            }}
        }}
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(search_results, f, indent=2, ensure_ascii=False)
            
            print("="*70)
            print("✅ Brave search completed successfully")
            print(f"💾 Results saved to: {{filename}}")
            print(f"📊 Found {{len(processed_results)}} {{search_type}} results")
            
            return search_results
            
        except Exception as save_error:
            print(f"⚠️ Results retrieved but save failed: {{str(save_error)}}")
            return search_results
            
    except Exception as e:
        print(f"❌ Search failed: {{str(e)}}")
        return None

# Execute the search
result = safe_brave_search()
if result:
    print("\\n🎯 Search completed successfully")
else:
    print("\\n❌ Search failed - check API credentials and network connection")
'''
