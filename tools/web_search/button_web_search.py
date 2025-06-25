"""
WEB SEARCH
Human Button Generators - Fixed Version
"""

from typing import Dict, Any, List
import json
from tools.web_search.web_search import (
    perform_web_search, 
    perform_filtered_search, 
    perform_content_search,
    validate_search_query,
    get_search_suggestions,
    estimate_cost
)

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for web search operations
    Universal model compatibility via code generation
    
    Args:
        params: Web search parameters
        model: Target model for code generation
        
    Returns:
        Executable code snippet for Claude 4 Code Execution Tool
    """
    operation = params.get("operation", "web_search")
    
    if operation == "web_search":
        return _create_basic_search_snippet(params, model)
    elif operation == "filtered_web_search":
        return _create_filtered_search_snippet(params, model)
    elif operation == "content_web_search":
        return _create_content_search_snippet(params, model)
    elif operation == "query_validation":
        return _create_validation_snippet(params, model)
    elif operation == "search_suggestions":
        return _create_suggestions_snippet(params, model)
    else:
        return _create_generic_search_snippet(params, model)

def _create_basic_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for basic web search"""
    query = params.get("query", "")
    max_results = params.get("max_results", 5)
    search_context = params.get("search_context", "general")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"max_results": max_results})
    
    # Escape query for safe inclusion in code
    escaped_query = json.dumps(query)
    
    snippet = f'''
# Web Search - Basic Search
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import perform_web_search
from tools.web_search.ui_web_search import display_web_search_result, display_search_execution_status
import anthropic
from datetime import datetime
import json

# Prepare search configuration using MAO logic
search_config = perform_web_search(
    query={escaped_query},
    max_results={max_results},
    search_context="{search_context}"
)

# Display search preparation
display_web_search_result(search_config, verbose=True)

if search_config.get("status") == "ready_for_execution":
    print("\\n🔍 Executing Anthropic Native Web Search...")
    display_search_execution_status(search_config["query"], "executing")
    
    try:
        # Initialize Anthropic client
        client = anthropic.Anthropic()
        
        # Configure web search tool
        tools = [{{
            "type": "web_search_20250305", 
            "name": "web_search",
            "max_uses": {max_results}
        }}]
        
        # Create search prompt
        search_prompt = f"Search for: {escaped_query}\\n\\nProvide comprehensive results with key findings, source URLs, and publication dates where available."
        
        # Perform search
        response = client.messages.create(
            model="{model}",
            max_tokens=6000,
            tools=tools,
            messages=[{{
                "role": "user", 
                "content": search_prompt
            }}]
        )
        
        # Process results
        search_content = ""
        for content in response.content:
            if content.type == "text":
                search_content += content.text
                print(content.text)
            elif content.type == "tool_use":
                print(f"\\n🔧 Tool Used: {{content.name}}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"web_search_{{timestamp}}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({{
                "query": search_config["query"],
                "search_content": search_content,
                "timestamp": datetime.now().isoformat(),
                "model_used": "{model}",
                "estimated_cost": {cost_estimate:.3f}
            }}, f, indent=2, ensure_ascii=False)
        
        print(f"\\n💾 Results saved: {{json_file}}")
        print(f"💰 Estimated cost: ${cost_estimate:.3f}")
        
    except Exception as e:
        print(f"❌ Search failed: {{str(e)}}")

print("\\nWEB SEARCH OPERATION COMPLETE")
'''
    
    return snippet.strip()

def _create_filtered_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for filtered web search"""
    query = params.get("query", "")
    domain = params.get("domain", "")
    date_range = params.get("date_range", "")
    max_results = params.get("max_results", 5)
    
    cost_estimate = estimate_cost({"max_results": max_results})
    
    snippet = f'''
# Web Search - Filtered Search  
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import perform_filtered_search
from tools.web_search.ui_web_search import display_web_search_result
import anthropic
from datetime import datetime
import json

# Prepare filtered search using MAO logic
search_config = perform_filtered_search(
    query="{query}",
    domain="{domain}" if "{domain}" else None,
    date_range="{date_range}" if "{date_range}" else None,
    max_results={max_results}
)

display_web_search_result(search_config, verbose=True)

if search_config.get("status") == "ready_for_execution":
    try:
        client = anthropic.Anthropic()
        tools = [{{"type": "web_search_20250305", "name": "web_search", "max_uses": {max_results}}}]
        
        response = client.messages.create(
            model="{model}",
            max_tokens=6000,
            tools=tools,
            messages=[{{"role": "user", "content": f"Search for: {{search_config['query']}}"}}]
        )
        
        search_content = ""
        for content in response.content:
            if content.type == "text":
                search_content += content.text
                print(content.text)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"filtered_search_{{timestamp}}.json", 'w') as f:
            json.dump({{"query": search_config["query"], "content": search_content, "cost": {cost_estimate:.3f}}}, f, indent=2)
        
        print(f"💰 Estimated cost: ${cost_estimate:.3f}")
        
    except Exception as e:
        print(f"❌ Search failed: {{str(e)}}")

print("FILTERED SEARCH COMPLETE")
'''
    
    return snippet.strip()

def _create_content_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for content-specific search"""
    query = params.get("query", "")
    content_type = params.get("content_type", "general")
    max_results = params.get("max_results", 5)
    
    cost_estimate = estimate_cost({"max_results": max_results})
    
    snippet = f'''
# Web Search - Content Search
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import perform_content_search
from tools.web_search.ui_web_search import display_web_search_result

search_config = perform_content_search(
    query="{query}",
    content_type="{content_type}",
    max_results={max_results}
)

display_web_search_result(search_config, verbose=True)
print(f"💰 Estimated cost: ${cost_estimate:.3f}")
'''
    
    return snippet.strip()

def _create_validation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for query validation"""
    query = params.get("query", "")
    
    snippet = f'''
# Web Search - Query Validation
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import validate_search_query
from tools.web_search.ui_web_search import display_web_search_result

validation_result = validate_search_query("{query}")
display_web_search_result(validation_result, verbose=True)
'''
    
    return snippet.strip()

def _create_suggestions_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for search suggestions"""
    query = params.get("query", "")
    suggestion_type = params.get("suggestion_type", "enhancement")
    
    snippet = f'''
# Web Search - Query Suggestions
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import get_search_suggestions
from tools.web_search.ui_web_search import display_web_search_result

suggestions_result = get_search_suggestions("{query}", "{suggestion_type}")
display_web_search_result(suggestions_result, verbose=True)
'''
    
    return snippet.strip()

def _create_generic_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for generic web search operations"""
    
    snippet = '''
# Web Search - Capabilities
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.web_search.web_search import get_search_capabilities
from tools.web_search.ui_web_search import display_search_capabilities

capabilities = get_search_capabilities()
display_search_capabilities(capabilities)
'''
    
    return snippet.strip()
