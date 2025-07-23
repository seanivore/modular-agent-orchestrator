"""
BRAVE SEARCH TOOL
UI Display Component
"""

from typing import Dict, Any

# Rich import with fallback handling
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Standardization imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path


@handle_errors(operation_name="display_brave_search", return_dict=False)
def display_brave_search_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display Brave Search operation results with beautiful formatting
    
    Args:
        result: Search result data from brave_search tool
        verbose: Show detailed technical information
    """
    
    if not HAS_RICH:
        _display_basic_result(result, verbose)
        return
    
    # Handle error cases
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    # Handle empty results
    if result.get("count", 0) == 0:
        console.print(f"🔍 No results found for: {result.get('query', 'unknown query')}", style="yellow")
        return
    
    # Main results display
    query = result.get("query", "Unknown query")
    search_type = result.get("search_type", "web")
    count = result.get("count", 0)
    
    # Header
    if verbose:
        header_text = f"🔍 Brave {search_type.title()} Search: {query} ({count} results)"
        console.print(Panel(header_text, style="blue"))
    else:
        console.print(f"🔍 Found {count} results for: {query}", style="blue bold")
    
    # Results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=4)
    table.add_column("Title", style="bold")
    table.add_column("Description", style="dim")
    
    if verbose:
        table.add_column("URL", style="link")
    
    # Determine result key
    result_key = "articles" if search_type == "news" else "results"
    results = result.get(result_key, [])
    
    for item in results:
        rank = str(item.get("rank", "?"))
        title = item.get("title", "No title")[:60] + "..." if len(item.get("title", "")) > 60 else item.get("title", "No title")
        description = item.get("description", "No description")[:100] + "..." if len(item.get("description", "")) > 100 else item.get("description", "No description")
        
        if verbose:
            url = item.get("url", "No URL")
            table.add_row(rank, title, description, url)
        else:
            table.add_row(rank, title, description)
    
    console.print(table)
    
    # Verbose metadata
    if verbose:
        metadata = result.get("metadata", {})
        if metadata:
            console.print(Path(r"\n📊 Search Metadata:"), style="bold")
            
            if "api_response_time" in metadata and metadata["api_response_time"]:
                console.print(f"   Response Time: {metadata['api_response_time']:.2f}s")
            
            if "total_available" in metadata:
                console.print(f"   Total Available: {metadata['total_available']}")
            
            console.print(f"   Country: {result.get('country', 'Unknown')}")
            console.print(f"   Timestamp: {result.get('timestamp', 'Unknown')}")


def _display_basic_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """Fallback display function when Rich is not available"""
    
    # Handle error cases
    if "error" in result:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    # Handle empty results
    if result.get("count", 0) == 0:
        print(f"🔍 No results found for: {result.get('query', 'unknown query')}")
        return
    
    # Main results display
    query = result.get("query", "Unknown query")
    search_type = result.get("search_type", "web")
    count = result.get("count", 0)
    
    print(f"🔍 Found {count} results for: {query}")
    
    # Determine result key
    result_key = "articles" if search_type == "news" else "results"
    results = result.get(result_key, [])
    
    for item in results:
        rank = item.get("rank", "?")
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        print(f"{rank}. {title}")
        print(f"   {description}")
        if verbose:
            print(f"   URL: {item.get('url', 'No URL')}")
        print()


@handle_errors(operation_name="display_error", return_dict=False)
def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    if HAS_RICH:
        panel = Panel(
            f"❌ Error: {error_msg}",
            title="Brave Search Error",
            border_style="red"
        )
        console.print(panel)
    else:
        print(f"❌ Brave Search Error: {error_msg}")


@handle_errors(operation_name="display_api_validation", return_dict=False)
def display_api_validation(result: Dict[str, Any], verbose: bool = False) -> None:
    """Display API key validation results"""
    
    if result.get("valid", False):
        message = "✅ Brave API key is valid and ready"
        if HAS_RICH:
            console.print(message, style="green")
            if verbose:
                console.print(f"   Key length: {result.get('key_length', 'unknown')} characters", style="dim")
        else:
            print(message)
            if verbose:
                print(f"   Key length: {result.get('key_length', 'unknown')} characters")
    else:
        error_msg = "Brave API key validation failed"
        if "error" in result:
            error_msg += f": {result['error']}"
        display_error(error_msg)


@handle_errors(operation_name="display_cost_estimate", return_dict=False)
def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for search operation"""
    
    if cost == 0:
        message = "💰 Cost: FREE"
        if HAS_RICH:
            console.print(message, style="green bold")
        else:
            print(message)
    else:
        message = f"💰 Estimated cost: ${cost:.4f}"
        if HAS_RICH:
            console.print(message, style="yellow")
        else:
            print(message)
    
    if verbose:
        note = "   Brave Search API is typically free for reasonable usage"
        if HAS_RICH:
            console.print(note, style="dim")
        else:
            print(note)


@handle_errors(operation_name="display_search_summary", return_dict=False)
def display_search_summary(results: Dict[str, Any], verbose: bool = False) -> None:
    """Display a summary of search operation"""
    
    if "error" in results:
        display_error("Search operation failed")
        return
    
    query = results.get("query", "Unknown")
    count = results.get("count", 0)
    search_type = results.get("search_type", "web")
    
    summary_text = f"Searched '{query}' using Brave {search_type} search → {count} results"
    
    if verbose:
        timestamp = results.get("timestamp", "Unknown time")
        summary_text += f" at {timestamp}"
    
    message = f"📋 {summary_text}"
    if HAS_RICH:
        console.print(message, style="green")
    else:
        print(message)


def format_for_agent_handoff(results: Dict[str, Any]) -> str:
    """Format search results for agent-to-agent handoff"""
    if "error" in results:
        return f"Search failed: {results['error']}"
    
    query = results.get("query", "Unknown query")
    count = results.get("count", 0)
    search_type = results.get("search_type", "web")
    
    if count == 0:
        return f"No {search_type} results found for: {query}"
    
    # Format top results for handoff
    result_key = "articles" if search_type == "news" else "results"
    results_list = results.get(result_key, [])
    
    formatted_results = [f"Brave {search_type} search for '{query}Path(r' found {count} results:\n")]
    
    for i, item in enumerate(results_list[:5], 1):  # Top 5 for handoff
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        url = item.get("url", "No URL")
        
        formatted_results.append(f"{i}. {title}")
        formatted_results.append(f"   {description}")
        formatted_results.append(f"   URL: {url}\n")
    
    return Path(r"\n").join(formatted_results)


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for UI operations - standardized naming"""
    return 0.0  # UI operations are free