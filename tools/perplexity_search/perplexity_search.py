"""
Perplexity Search Tool - Core Logic
AI-powered search with reasoning and source citations
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError, ValidationError

@handle_errors(operation_name="perplexity_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(requests.exceptions.RequestException, APIError))
def perform_perplexity_search(query: str, model: str = "llama-3.1-sonar-large-128k-online", 
                            search_context: str = "general") -> Dict[str, Any]:
    """
    Perform AI-powered search using Perplexity API (returns structured data for human button execution)
    
    Args:
        query: Search/research query
        model: Perplexity model to use
        search_context: Context or approach for the search
        
    Returns:
        Dict with search configuration and metadata
    """
    try:
        # Validate inputs
        if not query or not query.strip():
            return {"error": "Search query cannot be empty"}
        
        # Check cache first (fingerprinting)
        cache = CacheManager()
        cache_key = f"{query.strip()}|{model}|{search_context}"
        cached_result = cache.get_cached_analysis(cache_key, "perplexity_search")
        if cached_result:
            return json.loads(cached_result)
        
        # Validate model
        valid_models = [
            "llama-3.1-sonar-small-128k-online",
            "llama-3.1-sonar-large-128k-online", 
            "llama-3.1-sonar-huge-128k-online"
        ]
        
        if model not in valid_models:
            return {"error": f"Invalid model. Must be one of: {', '.join(valid_models)}"}
        
        # Prepare search configuration
        search_config = {
            "status": "ready_for_execution",
            "operation": "perplexity_search",
            "query": query.strip(),
            "model": model,
            "search_context": search_context,
            "timestamp": datetime.now().isoformat(),
            "estimated_cost": _calculate_perplexity_cost(model),
            "execution_method": "perplexity_api",
            "api_endpoint": "https://api.perplexity.ai/chat/completions"
        }
        
        # Cache the result (fingerprinting)
        cache.cache_content_analysis(cache_key, json.dumps(search_config), "perplexity_search")
        
        return search_config
        
    except Exception as e:
        return {"error": f"Perplexity search preparation failed: {str(e)}"}

@handle_errors(operation_name="enhanced_research", return_dict=True)
def perform_enhanced_research(query: str, research_approach: str = "comprehensive", 
                            analysis_focus: str = "general", model: str = "llama-3.1-sonar-large-128k-online") -> Dict[str, Any]:
    """
    Perform enhanced research with flexible approach and focus
    
    Args:
        query: Research query
        research_approach: Approach to research (flexible, user-defined)
        analysis_focus: Focus area for analysis (flexible, user-defined)
        model: Perplexity model to use
        
    Returns:
        Dict with enhanced research configuration
    """
    try:
        # Validate inputs
        if not query or not query.strip():
            return {"error": "Research query cannot be empty"}
        
        # Check cache first (fingerprinting)
        cache = CacheManager()
        cache_key = f"{query.strip()}|{research_approach}|{analysis_focus}|{model}"
        cached_result = cache.get_cached_analysis(cache_key, "perplexity_enhanced_research")
        if cached_result:
            return json.loads(cached_result)
        
        # Prepare enhanced research configuration
        research_config = {
            "status": "ready_for_execution",
            "operation": "enhanced_perplexity_research",
            "query": query.strip(),
            "research_approach": research_approach,
            "analysis_focus": analysis_focus,
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "estimated_cost": _calculate_perplexity_cost(model, enhanced=True),
            "execution_method": "perplexity_api_enhanced",
            "api_endpoint": "https://api.perplexity.ai/chat/completions"
        }
        
        # Cache the result (fingerprinting)
        cache.cache_content_analysis(cache_key, json.dumps(research_config), "perplexity_enhanced_research")
        
        return research_config
        
    except Exception as e:
        return {"error": f"Enhanced research preparation failed: {str(e)}"}

@handle_errors(operation_name="validate_perplexity_query", return_dict=True)
def validate_perplexity_query(query: str) -> Dict[str, Any]:
    """
    Validate a Perplexity search query for potential issues
    
    Args:
        query: Search query to validate
        
    Returns:
        Dict with validation results
    """
    try:
        validation_result = {
            "status": "success",
            "operation": "perplexity_query_validation",
            "query": query,
            "is_valid": True,
            "issues": [],
            "suggestions": [],
            "estimated_quality": "unknown"
        }
        
        # Basic validation checks
        if not query or not query.strip():
            validation_result["is_valid"] = False
            validation_result["issues"].append("Query is empty")
            return validation_result
        
        query = query.strip()
        
        # Length checks
        if len(query) < 5:
            validation_result["issues"].append("Query is very short - may not provide detailed analysis")
            validation_result["suggestions"].append("Consider adding more context or specific details")
        
        if len(query) > 500:
            validation_result["issues"].append("Query is very long - may exceed API limits")
            validation_result["suggestions"].append("Consider breaking into multiple focused queries")
        
        # Content analysis
        word_count = len(query.split())
        if word_count == 1:
            validation_result["suggestions"].append("Single word queries work better with additional context")
        elif word_count > 100:
            validation_result["suggestions"].append("Very long queries may be better split into parts")
        
        # Question format analysis
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        has_question_word = any(word.lower() in query.lower() for word in question_words)
        
        if not has_question_word and not query.endswith('?'):
            validation_result["suggestions"].append("Consider framing as a question for better AI analysis")
        
        # Estimate result quality
        if 5 <= word_count <= 30 and (has_question_word or query.endswith('?')):
            validation_result["estimated_quality"] = "excellent"
        elif 3 <= word_count <= 50:
            validation_result["estimated_quality"] = "good"
        elif word_count < 3:
            validation_result["estimated_quality"] = "basic"
        else:
            validation_result["estimated_quality"] = "complex"
        
        validation_result["word_count"] = word_count
        validation_result["character_count"] = len(query)
        validation_result["has_question_format"] = has_question_word or query.endswith('?')
        validation_result["timestamp"] = datetime.now().isoformat()
        
        return validation_result
        
    except Exception as e:
        return {"error": f"Query validation failed: {str(e)}"}

@handle_errors(operation_name="get_research_suggestions", return_dict=True)
def get_research_suggestions(query: str, suggestion_type: str = "enhancement") -> Dict[str, Any]:
    """
    Generate research query suggestions and improvements
    
    Args:
        query: Original research query
        suggestion_type: Type of suggestions to generate
        
    Returns:
        Dict with research suggestions
    """
    try:
        suggestions_result = {
            "status": "success",
            "operation": "perplexity_research_suggestions",
            "original_query": query,
            "suggestion_type": suggestion_type,
            "suggestions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        if not query or not query.strip():
            return {"error": "Cannot generate suggestions for empty query"}
        
        query = query.strip()
        
        # Generate different types of suggestions based on type
        if suggestion_type == "enhancement":
            suggestions_result["suggestions"] = [
                f"What are the latest developments in {query}?",
                f"How does {query} impact current industry trends?",
                f"What are the pros and cons of {query}?",
                f"What do experts say about {query}?",
                f"What are the future implications of {query}?"
            ]
        elif suggestion_type == "analytical":
            suggestions_result["suggestions"] = [
                f"Analyze the competitive landscape of {query}",
                f"What are the key challenges facing {query}?",
                f"Compare different approaches to {query}",
                f"What metrics are used to measure {query}?",
                f"What are the success factors for {query}?"
            ]
        elif suggestion_type == "contextual":
            suggestions_result["suggestions"] = [
                f"How has {query} evolved over the past 5 years?",
                f"What regulatory considerations affect {query}?",
                f"How do different regions approach {query}?",
                f"What are the economic implications of {query}?",
                f"How does {query} relate to sustainability goals?"
            ]
        elif suggestion_type == "practical":
            suggestions_result["suggestions"] = [
                f"What are the implementation steps for {query}?",
                f"What tools and resources are needed for {query}?",
                f"What are common mistakes to avoid with {query}?",
                f"What are the cost considerations for {query}?",
                f"How can organizations get started with {query}?"
            ]
        else:
            # Default to enhancement suggestions
            suggestions_result["suggestions"] = [
                f"Provide comprehensive analysis of {query}",
                f"What are the current trends in {query}?",
                f"How can {query} be optimized or improved?",
                f"What are the best practices for {query}?",
                f"What research exists on {query}?"
            ]
        
        return suggestions_result
        
    except Exception as e:
        return {"error": f"Suggestion generation failed: {str(e)}"}

@handle_errors(operation_name="check_api_configuration", return_dict=True)
def check_api_configuration() -> Dict[str, Any]:
    """
    Check Perplexity API configuration and availability
    
    Returns:
        Dict with API configuration status
    """
    try:
        config_result = {
            "status": "success",
            "operation": "api_configuration_check",
            "api_key_present": False,
            "api_endpoint": "https://api.perplexity.ai/chat/completions",
            "supported_models": [
                "llama-3.1-sonar-small-128k-online",
                "llama-3.1-sonar-large-128k-online", 
                "llama-3.1-sonar-huge-128k-online"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check for API key
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if api_key:
            config_result["api_key_present"] = True
            config_result["api_key_length"] = len(api_key)
        else:
            config_result["issues"] = ["PERPLEXITY_API_KEY environment variable not set"]
            config_result["suggestions"] = ["Set PERPLEXITY_API_KEY environment variable with your API key"]
        
        return config_result
        
    except Exception as e:
        return {"error": f"API configuration check failed: {str(e)}"}

def _calculate_perplexity_cost(model: str, enhanced: bool = False) -> float:
    """
    Calculate estimated cost for Perplexity search operation
    
    Args:
        model: Perplexity model being used
        enhanced: Whether this is an enhanced research operation
        
    Returns:
        Estimated cost in USD
    """
    # Base costs by model (estimated)
    model_costs = {
        "llama-3.1-sonar-small-128k-online": 0.015,
        "llama-3.1-sonar-large-128k-online": 0.025,
        "llama-3.1-sonar-huge-128k-online": 0.040
    }
    
    base_cost = model_costs.get(model, 0.025)
    
    # Enhanced research typically uses more tokens
    if enhanced:
        base_cost *= 1.5
    
    return base_cost

@handle_errors(operation_name="get_perplexity_capabilities", return_dict=True)
def get_perplexity_capabilities() -> Dict[str, Any]:
    """
    Get information about Perplexity search capabilities and limitations
    
    Returns:
        Dict with capability information
    """
    return {
        "operations": [
            "perform_perplexity_search",
            "perform_enhanced_research",
            "validate_perplexity_query",
            "get_research_suggestions",
            "check_api_configuration"
        ],
        "search_approach": "variable_input_philosophy",
        "research_types": "user_defined_no_restrictions",
        "supported_models": [
            "llama-3.1-sonar-small-128k-online",
            "llama-3.1-sonar-large-128k-online", 
            "llama-3.1-sonar-huge-128k-online"
        ],
        "features": [
            "ai_reasoning",
            "source_citations",
            "real_time_information",
            "comprehensive_analysis",
            "related_questions",
            "multi_perspective_analysis"
        ],
        "limitations": {
            "requires_api_key": True,
            "rate_limits": "subject_to_perplexity_api_limits",
            "max_query_length": 500,
            "min_query_length": 1,
            "timeout_seconds": 120
        },
        "cost_structure": {
            "small_model": 0.015,
            "large_model": 0.025,
            "huge_model": 0.040,
            "enhanced_multiplier": 1.5,
            "currency": "USD"
        }
    } 