"""
WEB SEARCH
Human Button Generators
"""

from typing import Dict, Any, List
import json

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
    
    # Escape query for safe inclusion in code
    escaped_query = json.dumps(query)
    
    snippet = f'''
# Web Search - Basic Search
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import perform_web_search
from interfaces.ui_tools.ui_web_search import display_web_search_result, display_search_execution_status
import anthropic
from datetime import datetime
import json

# Prepare search configuration
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
        
        # Create search prompt based on context
        context_prompts = {{
            "general": f"Search for: {escaped_query}\\n\\nProvide comprehensive results with key findings, source URLs, and publication dates where available.",
            "research": f"Conduct research on: {escaped_query}\\n\\nFocus on authoritative sources, expert opinions, statistical data, and credible information. Include source URLs and publication dates.",
            "news": f"Search for recent news about: {escaped_query}\\n\\nPrioritize recent developments, breaking news, and current events. Include publication dates and source credibility.",
            "academic": f"Search for academic information on: {escaped_query}\\n\\nFocus on scholarly sources, research papers, and educational content. Include source URLs and publication information.",
            "competitive": f"Research competitive landscape for: {escaped_query}\\n\\nAnalyze market players, recent developments, trends, and industry insights. Include company information and market data."
        }}
        
        search_prompt = context_prompts.get("{search_context}", context_prompts["general"])
        
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
        
        # Process and display results
        print("\\n" + "="*70)
        print("🔍 SEARCH RESULTS")
        print("="*70)
        print(f"Query: {search_config['query']}")
        print(f"Context: {search_config['search_context'].title()}")
        print(f"Max Results: {search_config['max_results']}")
        print("="*70)
        
        search_content = ""
        tool_usage = []
        
        for content in response.content:
            if content.type == "text":
                search_content += content.text
                print(content.text)
            elif content.type == "tool_use":
                tool_info = {{
                    "tool": content.name,
                    "timestamp": datetime.now().isoformat()
                }}
                tool_usage.append(tool_info)
                print(f"\\n🔧 Tool Used: {{content.name}}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        search_results = {{
            "query": search_config["query"],
            "search_context": search_config["search_context"],
            "max_results": search_config["max_results"],
            "timestamp": datetime.now().isoformat(),
            "search_content": search_content,
            "tool_usage": tool_usage,
            "model_used": "{model}",
            "estimated_cost": search_config.get("estimated_cost", 0.01)
        }}
        
        # Save JSON data
        json_file = f"web_search_{{search_config['search_context']}}_{{timestamp}}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print("\\n" + "="*70)
        display_search_execution_status(search_config["query"], "completed")
        print(f"💾 Results saved: {{json_file}}")
        print(f"💰 Estimated cost: ${{search_config.get('estimated_cost', 0.01):.3f}}")
        
    except Exception as e:
        display_search_execution_status(search_config["query"], "failed")
        print(f"❌ Search failed: {{str(e)}}")
        print("Note: Web search requires compatible Claude model and API access")

print("\\n" + "="*50)
print("WEB SEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_filtered_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for filtered web search"""
    query = params.get("query", "")
    domain = params.get("domain", "")
    date_range = params.get("date_range", "")
    max_results = params.get("max_results", 5)
    
    snippet = f'''
# Web Search - Filtered Search
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import perform_filtered_search
from interfaces.ui_tools.ui_web_search import display_web_search_result, display_search_execution_status
import anthropic
from datetime import datetime
import json

# Prepare filtered search
search_config = perform_filtered_search(
    query="{query}",
    domain="{domain}" if "{domain}" else None,
    date_range="{date_range}" if "{date_range}" else None,
    max_results={max_results}
)

# Display search preparation
display_web_search_result(search_config, verbose=True)

if search_config.get("status") == "ready_for_execution":
    print("\\n🔍 Executing Filtered Web Search...")
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
        
        # Create filtered search prompt
        filters_applied = search_config.get("applied_filters", {{}})
        filter_description = []
        if filters_applied.get("domain"):
            filter_description.append(f"domain: {{filters_applied['domain']}}")
        if filters_applied.get("date_range"):
            filter_description.append(f"date range: {{filters_applied['date_range']}}")
        
        filter_text = " with filters: " + ", ".join(filter_description) if filter_description else ""
        
        search_prompt = f"""Search for: {{search_config['query']}}{{filter_text}}

Provide comprehensive results focusing on the specified filters. Include:
1. Relevant information matching the search criteria
2. Source URLs and publication dates
3. Credibility assessment of sources
4. Key findings and insights
5. Any limitations due to applied filters

Original query: {{search_config.get('original_query', search_config['query'])}}
Enhanced query: {{search_config['query']}}"""
        
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
        
        # Process and display results
        print("\\n" + "="*70)
        print("🔍 FILTERED SEARCH RESULTS")
        print("="*70)
        print(f"Original Query: {{search_config.get('original_query', 'N/A')}}")
        print(f"Enhanced Query: {{search_config['query']}}")
        if filters_applied.get("domain"):
            print(f"Domain Filter: {{filters_applied['domain']}}")
        if filters_applied.get("date_range"):
            print(f"Date Filter: {{filters_applied['date_range']}}")
        print("="*70)
        
        search_content = ""
        for content in response.content:
            if content.type == "text":
                search_content += content.text
                print(content.text)
            elif content.type == "tool_use":
                print(f"\\n🔧 Tool Used: {{content.name}}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"filtered_search_{{timestamp}}.json"
        
        search_results = {{
            "original_query": search_config.get("original_query"),
            "enhanced_query": search_config["query"],
            "applied_filters": filters_applied,
            "max_results": {max_results},
            "timestamp": datetime.now().isoformat(),
            "search_content": search_content,
            "model_used": "{model}"
        }}
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print("\\n" + "="*70)
        display_search_execution_status(search_config["query"], "completed")
        print(f"💾 Results saved: {{json_file}}")
        
    except Exception as e:
        display_search_execution_status(search_config["query"], "failed")
        print(f"❌ Filtered search failed: {{str(e)}}")

print("\\n" + "="*50)
print("FILTERED SEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_content_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for content-specific search"""
    query = params.get("query", "")
    content_type = params.get("content_type", "general")
    max_results = params.get("max_results", 5)
    
    snippet = f'''
# Web Search - Content-Specific Search
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import perform_content_search
from interfaces.ui_tools.ui_web_search import display_web_search_result, display_search_execution_status
import anthropic
from datetime import datetime
import json

# Prepare content search
search_config = perform_content_search(
    query="{query}",
    content_type="{content_type}",
    max_results={max_results}
)

# Display search preparation
display_web_search_result(search_config, verbose=True)

if search_config.get("status") == "ready_for_execution":
    print("\\n🔍 Executing Content-Specific Search...")
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
        
        # Create content-specific search prompt
        content_prompts = {{
            "video": f"Search for video content about: {{search_config['query']}}\\n\\nFocus on YouTube videos, tutorials, and video-based content. Include video titles, channel information, and descriptions.",
            "academic": f"Search for academic content on: {{search_config['query']}}\\n\\nFocus on research papers, scholarly articles, and educational resources. Include publication information and academic sources.",
            "news": f"Search for news content about: {{search_config['query']}}\\n\\nFocus on recent news articles, press releases, and current events. Include publication dates and news sources.",
            "research": f"Search for research content on: {{search_config['query']}}\\n\\nFocus on research studies, data, and analytical content. Include methodology and source credibility.",
            "general": f"Search for: {{search_config['query']}}\\n\\nProvide comprehensive results with diverse content types and reliable sources."
        }}
        
        search_prompt = content_prompts.get("{content_type}", content_prompts["general"])
        
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
        
        # Process and display results
        print("\\n" + "="*70)
        print(f"🔍 {{search_config['content_type'].upper()}} SEARCH RESULTS")
        print("="*70)
        print(f"Original Query: {{search_config.get('original_query', 'N/A')}}")
        print(f"Enhanced Query: {{search_config['query']}}")
        print(f"Content Type: {{search_config['content_type'].title()}}")
        print("="*70)
        
        search_content = ""
        for content in response.content:
            if content.type == "text":
                search_content += content.text
                print(content.text)
            elif content.type == "tool_use":
                print(f"\\n🔧 Tool Used: {{content.name}}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"content_search_{{search_config['content_type']}}_{{timestamp}}.json"
        
        search_results = {{
            "original_query": search_config.get("original_query"),
            "enhanced_query": search_config["query"],
            "content_type": search_config["content_type"],
            "max_results": {max_results},
            "timestamp": datetime.now().isoformat(),
            "search_content": search_content,
            "model_used": "{model}"
        }}
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print("\\n" + "="*70)
        display_search_execution_status(search_config["query"], "completed")
        print(f"💾 Results saved: {{json_file}}")
        
    except Exception as e:
        display_search_execution_status(search_config["query"], "failed")
        print(f"❌ Content search failed: {{str(e)}}")

print("\\n" + "="*50)
print("CONTENT SEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_validation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for query validation"""
    query = params.get("query", "")
    
    snippet = f'''
# Web Search - Query Validation
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import validate_search_query
from interfaces.ui_tools.ui_web_search import display_web_search_result

# Validate search query
validation_result = validate_search_query("{query}")

# Display validation results
display_web_search_result(validation_result, verbose=True)

# Additional validation insights
if validation_result.get("status") == "success":
    is_valid = validation_result.get("is_valid", False)
    issues = validation_result.get("issues", [])
    suggestions = validation_result.get("suggestions", [])
    
    print("\\n" + "="*50)
    print("QUERY VALIDATION SUMMARY")
    print("="*50)
    
    if is_valid:
        print("✅ Query is valid and ready for search")
    else:
        print("❌ Query has issues that should be addressed")
    
    if issues:
        print("\\n⚠️ Issues identified:")
        for i, issue in enumerate(issues, 1):
            print(f"  {{i}}. {{issue}}")
    
    if suggestions:
        print("\\n💡 Suggestions for improvement:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {{i}}. {{suggestion}}")
    
    print(f"\\n📊 Query metrics:")
    print(f"  • Word count: {{validation_result.get('word_count', 0)}}")
    print(f"  • Character count: {{validation_result.get('character_count', 0)}}")
    print(f"  • Expected result quality: {{validation_result.get('estimated_results', 'unknown').title()}}")

print("\\n" + "="*50)
print("QUERY VALIDATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_suggestions_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for search suggestions"""
    query = params.get("query", "")
    suggestion_type = params.get("suggestion_type", "enhancement")
    
    snippet = f'''
# Web Search - Search Suggestions
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import get_search_suggestions
from interfaces.ui_tools.ui_web_search import display_web_search_result

# Generate search suggestions
suggestions_result = get_search_suggestions(
    query="{query}",
    suggestion_type="{suggestion_type}"
)

# Display suggestions
display_web_search_result(suggestions_result, verbose=True)

# Additional suggestion processing
if suggestions_result.get("status") == "success":
    suggestions = suggestions_result.get("suggestions", [])
    
    print("\\n" + "="*50)
    print("SEARCH SUGGESTIONS SUMMARY")
    print("="*50)
    print(f"Original query: {{suggestions_result.get('original_query')}}")
    print(f"Suggestion type: {{suggestions_result.get('suggestion_type').title()}}")
    
    if suggestions:
        print(f"\\n📝 Generated {{len(suggestions)}} suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {{i}}. {{suggestion}}")
        
        print("\\n💡 Usage tips:")
        print("  • Try different suggestion types for varied results")
        print("  • Combine suggestions with filters for targeted searches")
        print("  • Use suggestions as starting points for further refinement")
    else:
        print("\\n⚠️ No suggestions could be generated for this query")

print("\\n" + "="*50)
print("SEARCH SUGGESTIONS COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_generic_search_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate generic search snippet"""
    operation = params.get("operation", "unknown")
    query = params.get("query", "")
    
    snippet = f'''
# Web Search - Generic Operation
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import *
from interfaces.ui_tools.ui_web_search import display_web_search_result

# Note: Operation '{operation}' not specifically implemented
# Available operations:
# - web_search (basic search)
# - filtered_web_search (with domain/date filters)
# - content_web_search (content-type specific)
# - query_validation (validate search queries)
# - search_suggestions (generate query suggestions)

print("❌ Operation '{operation}' not recognized")
print("\\nAvailable web search operations:")
print("• web_search - Basic web search with query and result limit")
print("• filtered_web_search - Search with domain and date filters")
print("• content_web_search - Content-type specific search")
print("• query_validation - Validate query for potential issues")
print("• search_suggestions - Generate query suggestions")

# Show search capabilities
print("\\n🔍 Web Search Capabilities:")
capabilities = get_search_capabilities()
display_web_search_result({{"operation": "capabilities", "capabilities": capabilities}}, verbose=True)

print("\\n" + "="*50)
print("WEB SEARCH OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def create_multi_search_snippet(searches: List[Dict[str, Any]], model: str = "claude-sonnet-4") -> str:
    """
    Generate code snippet for multiple search operations
    
    Args:
        searches: List of search operations to perform
        model: Target model for code generation
        
    Returns:
        Executable code snippet for multiple searches
    """
    snippet_parts = ['''
# Web Search - Multiple Search Operations
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/Mao')

from tools.web_search_modular import *
from interfaces.ui_tools.ui_web_search import *
import anthropic
from datetime import datetime
import json
import time

# Initialize search session
print("🚀 Starting Multi-Search Session")
print("="*70)

search_results = []
total_estimated_cost = 0
''']
    
    for i, search in enumerate(searches):
        search_type = search.get("operation", "web_search")
        query = search.get("query", "")
        
        snippet_parts.append(f'''
# Search {i+1}: {search_type}
print(f"\\n🔍 Search {i+1}: {search_type.replace('_', ' ').title()}")
print(f"Query: {query}")
''')
        
        if search_type == "web_search":
            max_results = search.get("max_results", 5)
            search_context = search.get("search_context", "general")
            
            snippet_parts.append(f'''
search_config_{i} = perform_web_search(
    query="{query}",
    max_results={max_results},
    search_context="{search_context}"
)
display_web_search_result(search_config_{i})
search_results.append(search_config_{i})
total_estimated_cost += search_config_{i}.get("estimated_cost", 0.01)
''')
        
        elif search_type == "filtered_web_search":
            domain = search.get("domain", "")
            date_range = search.get("date_range", "")
            max_results = search.get("max_results", 5)
            
            snippet_parts.append(f'''
search_config_{i} = perform_filtered_search(
    query="{query}",
    domain="{domain}" if "{domain}" else None,
    date_range="{date_range}" if "{date_range}" else None,
    max_results={max_results}
)
display_web_search_result(search_config_{i})
search_results.append(search_config_{i})
total_estimated_cost += search_config_{i}.get("estimated_cost", 0.01)
''')
    
    snippet_parts.append('''
# Session summary
print("\\n" + "="*70)
print("MULTI-SEARCH SESSION SUMMARY")
print("="*70)
print(f"Total searches: {len(search_results)}")
print(f"Total estimated cost: ${total_estimated_cost:.3f}")

successful_searches = [s for s in search_results if s.get("status") == "ready_for_execution"]
print(f"Successful preparations: {len(successful_searches)}")

if successful_searches:
    print("\\n✅ All searches prepared successfully")
    print("💡 Execute individual search snippets to perform actual searches")
else:
    print("\\n⚠️ Some searches had preparation issues")

print("="*70)
''')
    
    return '\\n'.join(snippet_parts).strip()

def get_model_compatibility_info() -> Dict[str, Any]:
    """
    Get information about model compatibility for web search operations
    
    Returns:
        Dict with compatibility information
    """
    return {
        "supported_models": [
            "claude-sonnet-4",
            "claude-3-5-sonnet",
            "claude-3-7-sonnet"
        ],
        "operation_costs": {
            "web_search": 0.01,
            "filtered_web_search": 0.012,
            "content_web_search": 0.015,
            "query_validation": 0.001,
            "search_suggestions": 0.002
        },
        "features": {
            "anthropic_native_search": True,
            "real_time_results": True,
            "source_urls": True,
            "publication_dates": True,
            "content_filtering": True,
            "query_validation": True
        },
        "limitations": {
            "max_results_per_search": 20,
            "rate_limits": "subject_to_anthropic_api_limits",
            "search_regions": "global",
            "language_support": "multi_language"
        }
    } 