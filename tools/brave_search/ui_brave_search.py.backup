"""
BRAVE SEARCH TOOL
UI Display Component
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


def display_brave_search_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display Brave Search operation results with beautiful formatting
    
    Args:
        result: Search result data from brave_search tool
        verbose: Show detailed technical information
    """
    
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
            console.print("\n📊 Search Metadata:", style="bold")
            
            if "api_response_time" in metadata and metadata["api_response_time"]:
                console.print(f"   Response Time: {metadata['api_response_time']:.2f}s")
            
            if "total_available" in metadata:
                console.print(f"   Total Available: {metadata['total_available']}")
            
            console.print(f"   Country: {result.get('country', 'Unknown')}")
            console.print(f"   Timestamp: {result.get('timestamp', 'Unknown')}")


def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="Brave Search Error",
        border_style="red"
    )
    console.print(panel)


def display_api_validation(result: Dict[str, Any], verbose: bool = False) -> None:
    """Display API key validation results"""
    
    if result.get("valid", False):
        console.print("✅ Brave API key is valid and ready", style="green")
        if verbose:
            console.print(f"   Key length: {result.get('key_length', 'unknown')} characters", style="dim")
    else:
        error_msg = "Brave API key validation failed"
        if "error" in result:
            error_msg += f": {result['error']}"
        display_error(error_msg)


def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for search operation"""
    
    if cost == 0:
        console.print("💰 Cost: FREE", style="green bold")
    else:
        console.print(f"💰 Estimated cost: ${cost:.4f}", style="yellow")
    
    if verbose:
        console.print("   Brave Search API is typically free for reasonable usage", style="dim")


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
    
    console.print(f"📋 {summary_text}", style="green")


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
    
    formatted_results = [f"Brave {search_type} search for '{query}' found {count} results:\n"]
    
    for i, item in enumerate(results_list[:5], 1):  # Top 5 for handoff
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        url = item.get("url", "No URL")
        
        formatted_results.append(f"{i}. {title}")
        formatted_results.append(f"   {description}")
        formatted_results.append(f"   URL: {url}\n")
    
    return "\n".join(formatted_results)