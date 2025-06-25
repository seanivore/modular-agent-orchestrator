"""
PERPLEXITY SEARCH
Human Button Generator - Standardized Single Entry Point
"""

from typing import Dict, Any, List
import json
from tools.perplexity_search.perplexity_search import (
    perform_perplexity_search, perform_enhanced_research, validate_perplexity_query,
    get_research_suggestions, check_api_configuration, estimate_cost
)


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Perplexity search operations
    
    Args:
        params: Perplexity search parameters
        model: Target model for code generation
        
    Returns:
        Executable code snippet using MAO logic functions
    """
    operation = params.get("operation", "perplexity_search")
    
    if operation == "perplexity_search":
        return _create_basic_search_snippet(params, model)
    elif operation == "enhanced_perplexity_research":
        return _create_enhanced_research_snippet(params, model)
    elif operation == "perplexity_query_validation":
        return _create_validation_snippet(params, model)
    elif operation == "perplexity_research_suggestions":
        return _create_suggestions_snippet(params, model)
    elif operation == "api_configuration_check":
        return _create_api_check_snippet(params, model)
    else:
        return _create_basic_search_snippet(params, model)  # Default


def _create_basic_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate basic search snippet using MAO logic functions"""
    query = params.get("query", "")
    perplexity_model = params.get("model", "llama-3.1-sonar-large-128k-online")
    search_context = params.get("search_context", "general")
    
    escaped_query = json.dumps(query)
    
    return f'''
# Perplexity AI Search - Using MAO Logic Functions
import json
from tools.perplexity_search.perplexity_search import perform_perplexity_search, estimate_cost
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def execute_search():
    """Execute Perplexity search using MAO functions"""
    
    params = {{
        "query": {escaped_query},
        "model": "{perplexity_model}",
        "search_context": "{search_context}"
    }}
    
    print("🧠 Perplexity AI Search")
    print(f"📝 Query: {{params['query']}}")
    print(f"🤖 Model: {{params['model']}}")
    print("="*60)
    
    # Use MAO logic function
    result = perform_perplexity_search(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("status") == "ready_for_execution":
        print("✅ Search configuration ready")
        print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        print("💡 Now execute with Perplexity API using the configuration above")
    else:
        print("❌ Search preparation failed")

execute_search()
'''


def _create_enhanced_research_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate enhanced research snippet using MAO logic functions"""
    query = params.get("query", "")
    research_approach = params.get("research_approach", "comprehensive")
    analysis_focus = params.get("analysis_focus", "general")
    perplexity_model = params.get("model", "llama-3.1-sonar-large-128k-online")
    
    escaped_query = json.dumps(query)
    
    return f'''
# Enhanced Perplexity Research - Using MAO Logic Functions
import json
from tools.perplexity_search.perplexity_search import perform_enhanced_research, estimate_cost
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def execute_enhanced_research():
    """Execute enhanced research using MAO functions"""
    
    params = {{
        "query": {escaped_query},
        "research_approach": "{research_approach}",
        "analysis_focus": "{analysis_focus}",
        "model": "{perplexity_model}"
    }}
    
    print("🧠 Enhanced Perplexity Research")
    print(f"📝 Query: {{params['query']}}")
    print(f"📊 Approach: {{params['research_approach']}}")
    print(f"🎯 Focus: {{params['analysis_focus']}}")
    print("="*80)
    
    # Use MAO logic function
    result = perform_enhanced_research(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("status") == "ready_for_execution":
        print("✅ Enhanced research configuration ready")
        print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        print("💡 Now execute with Perplexity API using the enhanced configuration above")
    else:
        print("❌ Research preparation failed")

execute_enhanced_research()
'''


def _create_validation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate validation snippet using MAO logic functions"""
    query = params.get("query", "")
    escaped_query = json.dumps(query)
    
    return f'''
# Perplexity Query Validation - Using MAO Logic Functions
import json
from tools.perplexity_search.perplexity_search import validate_perplexity_query
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def validate_query():
    """Validate Perplexity query using MAO functions"""
    
    query = {escaped_query}
    
    print("🧠 Perplexity Query Validation")
    print(f"📝 Query: {{query}}")
    print("="*60)
    
    # Use MAO logic function
    result = validate_perplexity_query(query)
    display_perplexity_result(result, verbose=True)
    
    if result.get("is_valid"):
        print("✅ Query is optimized for Perplexity AI")
    else:
        print("⚠️ Query could be improved for better results")

validate_query()
'''


def _create_suggestions_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate suggestions snippet using MAO logic functions"""
    query = params.get("query", "")
    suggestion_type = params.get("suggestion_type", "enhancement")
    
    escaped_query = json.dumps(query)
    
    return f'''
# Perplexity Research Suggestions - Using MAO Logic Functions
import json
from tools.perplexity_search.perplexity_search import get_research_suggestions
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def generate_suggestions():
    """Generate research suggestions using MAO functions"""
    
    params = {{
        "query": {escaped_query},
        "suggestion_type": "{suggestion_type}"
    }}
    
    print("🧠 Perplexity Research Suggestions")
    print(f"📝 Query: {{params['query']}}")
    print(f"🎯 Type: {{params['suggestion_type']}}")
    print("="*60)
    
    # Use MAO logic function
    result = get_research_suggestions(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("suggestions"):
        print(f"✅ Generated {{len(result['suggestions'])}} research suggestions")
    else:
        print("⚠️ No suggestions could be generated")

generate_suggestions()
'''


def _create_api_check_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate API check snippet using MAO logic functions"""
    
    return '''
# Perplexity API Configuration Check - Using MAO Logic Functions
from tools.perplexity_search.perplexity_search import check_api_configuration
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def check_api_setup():
    """Check Perplexity API configuration using MAO functions"""
    
    print("🧠 Perplexity API Configuration Check")
    print("="*60)
    
    # Use MAO logic function
    result = check_api_configuration()
    display_perplexity_result(result, verbose=True)
    
    if result.get("api_key_present"):
        print("✅ Perplexity API is properly configured")
        print("🚀 Ready to perform AI-powered searches")
    else:
        print("❌ API key not found - setup required")
        print("💡 Set PERPLEXITY_API_KEY environment variable")
        print("🔗 Get your API key at: https://www.perplexity.ai/settings/api")

check_api_setup()
'''
