"""
Web Search Tool - Core Logic
Real-time web search using Anthropic's native capabilities
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from orchestrator.hybrid_cache import HybridCacheManager

def perform_web_search(query: str, max_results: int = 5, search_context: str = "general") -> Dict[str, Any]:
    """
    Perform web search operation (returns structured data for human button execution)
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        search_context: Context or approach for the search
        
    Returns:
        Dict with search configuration and metadata
    """
    try:
        # Validate inputs
        if not query or not query.strip():
            return {"error": "Search query cannot be empty"}
        
        if max_results < 1 or max_results > 20:
            return {"error": "Max results must be between 1 and 20"}
        
        # Check cache first (fingerprinting)
        cache = HybridCacheManager()
        cache_key = f"{query.strip()}|{max_results}|{search_context}"
        cached_result = cache.get_cached_analysis(cache_key, "web_search")
        if cached_result:
            print(f"💾 Cache HIT: Web search config for '{query}' (instant!)")
            return json.loads(cached_result)
        
        # Prepare search configuration
        search_config = {
            "status": "ready_for_execution",
            "operation": "web_search",
            "query": query.strip(),
            "max_results": max_results,
            "search_context": search_context,
            "timestamp": datetime.now().isoformat(),
            "estimated_cost": _calculate_search_cost(max_results),
            "execution_method": "anthropic_native_web_search"
        }
        
        # Cache the result (fingerprinting)
        cache.cache_content_analysis(cache_key, json.dumps(search_config), "web_search")
        print(f"💾 Cached web search config for '{query}' - future identical searches will be instant!")
        
        return search_config
        
    except Exception as e:
        return {"error": f"Search preparation failed: {str(e)}"}

def perform_filtered_search(query: str, domain: Optional[str] = None, 
                          date_range: Optional[str] = None, max_results: int = 5) -> Dict[str, Any]:
    """
    Perform filtered web search with domain and date constraints
    
    Args:
        query: Base search query
        domain: Specific domain to search within
        date_range: Date range filter (e.g., "2024", "2023-01-01")
        max_results: Maximum number of results
        
    Returns:
        Dict with filtered search configuration
    """
    try:
        # Check cache first (fingerprinting)
        cache = HybridCacheManager()
        cache_key = f"{query.strip()}|{domain}|{date_range}|{max_results}"
        cached_result = cache.get_cached_analysis(cache_key, "web_search_filtered")
        if cached_result:
            print(f"💾 Cache HIT: Filtered search config for '{query}' (instant!)")
            return json.loads(cached_result)
        
        # Build enhanced query with filters
        enhanced_query = query.strip()
        
        if domain:
            enhanced_query += f" site:{domain.strip()}"
        
        if date_range:
            enhanced_query += f" after:{date_range.strip()}"
        
        # Use base search function with enhanced query
        result = perform_web_search(enhanced_query, max_results, "filtered")
        
        if "error" not in result:
            result["original_query"] = query
            result["applied_filters"] = {
                "domain": domain,
                "date_range": date_range
            }
            result["operation"] = "filtered_web_search"
            
            # Cache the result (fingerprinting)
            cache.cache_content_analysis(cache_key, json.dumps(result), "web_search_filtered")
            print(f"💾 Cached filtered search config for '{query}' - future identical searches will be instant!")
        
        return result
        
    except Exception as e:
        return {"error": f"Filtered search preparation failed: {str(e)}"}

def perform_content_search(query: str, content_type: str = "general", max_results: int = 5) -> Dict[str, Any]:
    """
    Perform content-specific web search
    
    Args:
        query: Search query
        content_type: Type of content to search for
        max_results: Maximum number of results
        
    Returns:
        Dict with content search configuration
    """
    try:
        # Check cache first (fingerprinting)
        cache = HybridCacheManager()
        cache_key = f"{query.strip()}|{content_type}|{max_results}"
        cached_result = cache.get_cached_analysis(cache_key, "web_search_content")
        if cached_result:
            print(f"💾 Cache HIT: Content search config for '{query}' (instant!)")
            return json.loads(cached_result)
        
        # Enhance query based on content type
        enhanced_query = query.strip()
        
        # Add content-specific search modifiers (but keep flexible)
        if content_type.lower() in ["video", "youtube"]:
            enhanced_query += " site:youtube.com"
        elif content_type.lower() in ["academic", "research"]:
            enhanced_query += " filetype:pdf OR site:scholar.google.com"
        elif content_type.lower() in ["news", "recent"]:
            enhanced_query += " after:2024"
        
        result = perform_web_search(enhanced_query, max_results, f"content_{content_type}")
        
        if "error" not in result:
            result["content_type"] = content_type
            result["original_query"] = query
            result["operation"] = "content_web_search"
            
            # Cache the result (fingerprinting)
            cache.cache_content_analysis(cache_key, json.dumps(result), "web_search_content")
            print(f"💾 Cached content search config for '{query}' - future identical searches will be instant!")
        
        return result
        
    except Exception as e:
        return {"error": f"Content search preparation failed: {str(e)}"}

def validate_search_query(query: str) -> Dict[str, Any]:
    """
    Validate a search query for potential issues
    
    Args:
        query: Search query to validate
        
    Returns:
        Dict with validation results
    """
    try:
        validation_result = {
            "status": "success",
            "operation": "query_validation",
            "query": query,
            "is_valid": True,
            "issues": [],
            "suggestions": [],
            "estimated_results": "unknown"
        }
        
        # Basic validation checks
        if not query or not query.strip():
            validation_result["is_valid"] = False
            validation_result["issues"].append("Query is empty")
            return validation_result
        
        query = query.strip()
        
        # Length checks
        if len(query) < 3:
            validation_result["issues"].append("Query is very short - may return broad results")
            validation_result["suggestions"].append("Consider adding more specific terms")
        
        if len(query) > 200:
            validation_result["issues"].append("Query is very long - may be too specific")
            validation_result["suggestions"].append("Consider simplifying the query")
        
        # Content analysis
        word_count = len(query.split())
        if word_count == 1:
            validation_result["suggestions"].append("Single word queries may return broad results")
        elif word_count > 20:
            validation_result["suggestions"].append("Very long queries may be too restrictive")
        
        # Special character analysis
        if any(char in query for char in ['<', '>', '{', '}', '[', ']']):
            validation_result["issues"].append("Query contains special characters that may cause issues")
        
        # Estimate result quality
        if 3 <= word_count <= 8:
            validation_result["estimated_results"] = "good"
        elif word_count < 3:
            validation_result["estimated_results"] = "broad"
        else:
            validation_result["estimated_results"] = "specific"
        
        validation_result["word_count"] = word_count
        validation_result["character_count"] = len(query)
        validation_result["timestamp"] = datetime.now().isoformat()
        
        return validation_result
        
    except Exception as e:
        return {"error": f"Query validation failed: {str(e)}"}

def get_search_suggestions(query: str, suggestion_type: str = "enhancement") -> Dict[str, Any]:
    """
    Generate search query suggestions and improvements
    
    Args:
        query: Original search query
        suggestion_type: Type of suggestions to generate
        
    Returns:
        Dict with search suggestions
    """
    try:
        suggestions_result = {
            "status": "success",
            "operation": "search_suggestions",
            "original_query": query,
            "suggestion_type": suggestion_type,
            "suggestions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        if not query or not query.strip():
            return {"error": "Cannot generate suggestions for empty query"}
        
        query = query.strip()
        
        # Generate different types of suggestions
        if suggestion_type == "enhancement":
            suggestions_result["suggestions"] = [
                f'"{query}" exact phrase',
                f"{query} 2024",
                f"{query} guide",
                f"{query} tutorial",
                f"{query} best practices"
            ]
        elif suggestion_type == "related":
            # Basic related term suggestions
            words = query.split()
            if len(words) > 1:
                suggestions_result["suggestions"] = [
                    " ".join(words[:-1]),  # Remove last word
                    " ".join(words[1:]),   # Remove first word
                    f"{query} alternatives",
                    f"{query} comparison",
                    f"{query} vs"
                ]
        elif suggestion_type == "specific":
            suggestions_result["suggestions"] = [
                f"{query} step by step",
                f"{query} detailed guide",
                f"{query} comprehensive",
                f"{query} in-depth analysis",
                f"{query} case study"
            ]
        
        return suggestions_result
        
    except Exception as e:
        return {"error": f"Suggestion generation failed: {str(e)}"}

def _calculate_search_cost(max_results: int) -> float:
    """
    Calculate estimated cost for web search operation
    
    Args:
        max_results: Number of results requested
        
    Returns:
        Estimated cost in USD
    """
    # Base cost for web search operation
    base_cost = 0.01
    
    # Additional cost per result
    per_result_cost = 0.002
    
    return base_cost + (max_results * per_result_cost)

def get_search_capabilities() -> Dict[str, Any]:
    """
    Get information about web search capabilities and limitations
    
    Returns:
        Dict with capability information
    """
    return {
        "operations": [
            "perform_web_search",
            "perform_filtered_search", 
            "perform_content_search",
            "validate_search_query",
            "get_search_suggestions"
        ],
        "search_types": [
            "general",
            "filtered",
            "content_specific",
            "academic",
            "news",
            "video"
        ],
        "filters": [
            "domain_restriction",
            "date_range",
            "content_type",
            "file_type"
        ],
        "limitations": {
            "max_results_per_search": 20,
            "min_query_length": 1,
            "max_query_length": 200,
            "rate_limits": "subject_to_anthropic_limits"
        },
        "cost_structure": {
            "base_cost": 0.01,
            "per_result_cost": 0.002,
            "currency": "USD"
        }
    } 