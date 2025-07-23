"""
PERPLEXITY SEARCH
Button Generator - Standardized Single Entry Point
"""

from typing import Dict, Any, List
import json

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

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
try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

from tools.perplexity_search.perplexity_search import perform_perplexity_search, estimate_cost
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def execute_search():
    """Execute Perplexity search using MAO functions"""
    
    params = {{
        "query": {escaped_query},
        "model": "{perplexity_model}",
        "search_context": "{search_context}"
    }}
    
    if HAS_RICH and console:
        console.print("[blue]🧠 Perplexity AI Search[" / "blue]")
        console.print(f"[cyan]📝 Query:[" / "cyan] {{params['query']}}")
        console.print(f"[cyan]🤖 Model:[" / "cyan] {{params['model']}}")
        console.print("=" * 60)
    else:
        print("🧠 Perplexity AI Search")
        print(f"📝 Query: {{params['query']}}")
        print(f"🤖 Model: {{params['model']}}")
        print("="*60)
    
    # Use MAO logic function
    result = perform_perplexity_search(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("status") == "ready_for_execution":
        if HAS_RICH and console:
            console.print("[green]✅ Search configuration ready[" / "green]")
            console.print(f"[yellow]💰 Estimated cost:[" / "yellow] ${{estimate_cost(params):.4f}}")
            console.print("[dim]💡 Now execute with Perplexity API using the configuration above[" / "dim]")
        else:
            print("✅ Search configuration ready")
            print(f"💰 Estimated cost: ${{estimate_cost(params):.4f}}")
            print("💡 Now execute with Perplexity API using the configuration above")
    else:
        if HAS_RICH and console:
            console.print("[red]❌ Search preparation failed[" / "red]")
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
try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

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
    
    if HAS_RICH and console:
        console.print("[blue]🧠 Enhanced Perplexity Research[" / "blue]")
        console.print(f"[cyan]📝 Query:[" / "cyan] {{params['query']}}")
        console.print(f"[cyan]📊 Approach:[" / "cyan] {{params['research_approach']}}")
        console.print(f"[cyan]🎯 Focus:[" / "cyan] {{params['analysis_focus']}}")
        console.print("=" * 80)
    else:
        print("🧠 Enhanced Perplexity Research")
        print(f"📝 Query: {{params['query']}}")
        print(f"📊 Approach: {{params['research_approach']}}")
        print(f"🎯 Focus: {{params['analysis_focus']}}")
        print("="*80)
    
    # Use MAO logic function
    result = perform_enhanced_research(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("status") == "ready_for_execution":
        if HAS_RICH and console:
            console.print("[green]✅ Enhanced research configuration ready[" / "green]")
            console.print(f"[yellow]💰 Estimated cost:[" / "yellow] ${{estimate_cost(params):.4f}}")
            console.print("[dim]💡 Now execute with Perplexity API using the enhanced configuration above[" / "dim]")
        else:
            print("✅ Enhanced research configuration ready")
            print(f"💰 Estimated cost: ${{estimate_cost(params):.4f}}")
            print("💡 Now execute with Perplexity API using the enhanced configuration above")
    else:
        if HAS_RICH and console:
            console.print("[red]❌ Research preparation failed[" / "red]")
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
try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

from tools.perplexity_search.perplexity_search import validate_perplexity_query
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def validate_query():
    """Validate Perplexity query using MAO functions"""
    
    query = {escaped_query}
    
    if HAS_RICH and console:
        console.print("[blue]🧠 Perplexity Query Validation[" / "blue]")
        console.print(f"[cyan]📝 Query:[" / "cyan] {{query}}")
        console.print("=" * 60)
    else:
        print("🧠 Perplexity Query Validation")
        print(f"📝 Query: {{query}}")
        print("="*60)
    
    # Use MAO logic function
    result = validate_perplexity_query(query)
    display_perplexity_result(result, verbose=True)
    
    if result.get("is_valid"):
        if HAS_RICH and console:
            console.print("[green]✅ Query is optimized for Perplexity AI[" / "green]")
        else:
            print("✅ Query is optimized for Perplexity AI")
    else:
        if HAS_RICH and console:
            console.print("[yellow]⚠️ Query could be improved for better results[" / "yellow]")
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
try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

from tools.perplexity_search.perplexity_search import get_research_suggestions
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result

def generate_suggestions():
    """Generate research suggestions using MAO functions"""
    
    params = {{
        "query": {escaped_query},
        "suggestion_type": "{suggestion_type}"
    }}
    
    if HAS_RICH and console:
        console.print("[blue]🧠 Perplexity Research Suggestions[" / "blue]")
        console.print(f"[cyan]📝 Query:[" / "cyan] {{params['query']}}")
        console.print(f"[cyan]🎯 Type:[" / "cyan] {{params['suggestion_type']}}")
        console.print("=" * 60)
    else:
        print("🧠 Perplexity Research Suggestions")
        print(f"📝 Query: {{params['query']}}")
        print(f"🎯 Type: {{params['suggestion_type']}}")
        print("="*60)
    
    # Use MAO logic function
    result = get_research_suggestions(**params)
    display_perplexity_result(result, verbose=True)
    
    if result.get("suggestions"):
        if HAS_RICH and console:
            console.print(f"[green]✅ Generated {{len(result['suggestions'])}} research suggestions[" / "green]")
        else:
            print(f"✅ Generated {{len(result['suggestions'])}} research suggestions")
    else:
        if HAS_RICH and console:
            console.print("[yellow]⚠️ No suggestions could be generated[" / "yellow]")
        else:
            print("⚠️ No suggestions could be generated")

generate_suggestions()
'''


def _create_api_check_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate API check snippet using MAO logic functions"""
    
    return f'''
# Perplexity API Configuration Check - Using MAO Logic Functions
import json
try:
    from rich.console import Console
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

from tools.perplexity_search.perplexity_search import check_api_configuration
from tools.perplexity_search.ui_perplexity_search import display_perplexity_result
from pathlib import Path

def check_api():
    """Check Perplexity API configuration using MAO functions"""
    
    if HAS_RICH and console:
        console.print("[blue]🧠 Perplexity API Configuration Check[" / "blue]")
        console.print("=" * 60)
    else:
        print("🧠 Perplexity API Configuration Check")
        print("="*60)
    
    # Use MAO logic function
    result = check_api_configuration()
    display_perplexity_result(result, verbose=True)
    
    if result.get("is_configured"):
        if HAS_RICH and console:
            console.print("[green]✅ Perplexity API is properly configured[" / "green]")
        else:
            print("✅ Perplexity API is properly configured")
    else:
        if HAS_RICH and console:
            console.print("[red]❌ API configuration needs attention[" / "red]")
        else:
            print("❌ API configuration needs attention")

check_api()
'''
