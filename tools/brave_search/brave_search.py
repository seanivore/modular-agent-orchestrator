"""
Brave Web Search Tool
Independent tool logic with enhanced error handling and fingerprint caching
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import time
import hashlib
from orchestrator.cache.cache_system import CacheManager


def search_web(query: str, count: int = 10, country: str = "US", search_type: str = "web") -> Dict[str, Any]:
    """
    Execute Brave web search with comprehensive error handling and fingerprint caching
    
    Args:
        query: Search query string
        count: Number of results (1-20)
        country: Country code for localized results
        search_type: Type of search (web, news, local)
        
    Returns:
        Dict with structured search results or error information
    """
    try:
        # Validation
        if not query.strip():
            return {"error": "Search query cannot be empty"}
        
        # Clamp count to valid range
        count = min(20, max(1, count))
        
        # 🔍 FINGERPRINT CACHING - Check cache first
        cache = CacheManager()
        cache_key = f"{query}|{count}|{country}|{search_type}"
        
        cached_result = cache.get_cached_analysis(cache_key, "brave_search")
        if cached_result:
            return json.loads(cached_result)
        
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
        if response is None or response.status_code != 200:
            return {
                "error": f"Search failed after {max_retries} attempts. Last error: {last_error}",
                "status_code": response.status_code if response else None
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
        
        # 💾 FINGERPRINT CACHING - Cache successful results
        cache.cache_content_analysis(cache_key, json.dumps(search_results), "brave_search")
        
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
            "error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable"
        }
    
    return {
        "valid": True,
        "key_length": len(api_key),
        "message": "API key found and ready"
    }


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for this search operation"""
    # Brave API is typically free for reasonable usage
    # Return minimal cost for workflow planning
    return 0.001 