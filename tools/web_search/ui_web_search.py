"""
WEB SEARCH
UI Display Component
"""

from typing import Dict, Any, List

# Rich import with fallback handling
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.tree import Tree
    from rich.columns import Columns
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

# Standardization imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors


@handle_errors(operation_name="display_error", return_dict=False)
def display_error(error_message: str):
    """Display standardized error message with Panel formatting"""
    if HAS_RICH:
        console.print(Panel(
            f"[red]❌ {error_message}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red"
        ))
    else:
        print(f"❌ Error: {error_message}")


@handle_errors(operation_name="display_web_search_result", return_dict=False)
def display_web_search_result(result: Dict[str, Any], verbose: bool = False):
    """
    Display web search operation results with beautiful formatting
    
    Args:
        result: Result dictionary from web search operations
        verbose: Whether to show detailed information
    """
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    operation = result.get("operation", "unknown")
    
    if operation == "web_search":
        _display_basic_search(result, verbose)
    elif operation == "filtered_web_search":
        _display_filtered_search(result, verbose)
    elif operation == "content_web_search":
        _display_content_search(result, verbose)
    elif operation == "query_validation":
        _display_query_validation(result, verbose)
    elif operation == "search_suggestions":
        _display_search_suggestions(result, verbose)
    else:
        _display_generic_result(result, verbose)


def _display_basic_search(result: Dict[str, Any], verbose: bool):
    """Display basic web search results"""
    query = result.get("query", "Unknown")
    max_results = result.get("max_results", 5)
    estimated_cost = result.get("estimated_cost", 0.01)
    
    if HAS_RICH:
        # Main search message
        console.print(f"[blue]🔍 Web Search Ready: {query}[/blue]")
        
        if verbose:
            # Detailed search configuration
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("🔍 Query", query)
            info_table.add_row("📊 Max Results", str(max_results))
            info_table.add_row("🎯 Context", result.get("search_context", "general").title())
            info_table.add_row("💰 Estimated Cost", f"${estimated_cost:.3f}")
            info_table.add_row("🔧 Method", result.get("execution_method", "unknown"))
            info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Search Configuration[/bold]", border_style="blue"))
        else:
            console.print(f"[dim]📊 {max_results} results • ${estimated_cost:.3f} estimated[/dim]")
    else:
        print(f"🔍 Web Search Ready: {query}")
        if verbose:
            print(f"📊 Max Results: {max_results}")
            print(f"🎯 Context: {result.get('search_context', 'general').title()}")
            print(f"💰 Estimated Cost: ${estimated_cost:.3f}")
            print(f"🔧 Method: {result.get('execution_method', 'unknown')}")
            print(f"⏰ Prepared: {result.get('timestamp', 'Unknown')}")
        else:
            print(f"📊 {max_results} results • ${estimated_cost:.3f} estimated")


def _display_filtered_search(result: Dict[str, Any], verbose: bool):
    """Display filtered web search results"""
    original_query = result.get("original_query", "Unknown")
    enhanced_query = result.get("query", "Unknown")
    filters = result.get("applied_filters", {})
    
    if HAS_RICH:
        console.print(f"[blue]🔍 Filtered Search Ready: {original_query}[/blue]")
        
        # Show applied filters
        filter_parts = []
        if filters.get("domain"):
            filter_parts.append(f"[green]🌐 {filters['domain']}[/green]")
        if filters.get("date_range"):
            filter_parts.append(f"[yellow]📅 {filters['date_range']}[/yellow]")
        
        if filter_parts:
            console.print(f"[dim]Filters: {' • '.join(filter_parts)}[/dim]")
        
        if verbose:
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("🔍 Original Query", original_query)
            info_table.add_row("🔧 Enhanced Query", enhanced_query)
            info_table.add_row("📊 Max Results", str(result.get("max_results", 5)))
            
            if filters.get("domain"):
                info_table.add_row("🌐 Domain Filter", filters["domain"])
            if filters.get("date_range"):
                info_table.add_row("📅 Date Filter", filters["date_range"])
            
            info_table.add_row("💰 Estimated Cost", f"${result.get('estimated_cost', 0.01):.3f}")
            info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Filtered Search Configuration[/bold]", border_style="green"))
    else:
        print(f"🔍 Filtered Search Ready: {original_query}")
        if filters.get("domain"):
            print(f"🌐 Domain: {filters['domain']}")
        if filters.get("date_range"):
            print(f"📅 Date Range: {filters['date_range']}")
        if verbose:
            print(f"🔧 Enhanced Query: {enhanced_query}")
            print(f"📊 Max Results: {result.get('max_results', 5)}")
            print(f"💰 Estimated Cost: ${result.get('estimated_cost', 0.01):.3f}")


def _display_content_search(result: Dict[str, Any], verbose: bool):
    """Display content-specific search results"""
    original_query = result.get("original_query", "Unknown")
    content_type = result.get("content_type", "general")
    enhanced_query = result.get("query", "Unknown")
    
    # Content type icon mapping
    content_icons = {
        "video": "🎥",
        "youtube": "🎥", 
        "academic": "📚",
        "research": "📚",
        "news": "📰",
        "recent": "📰",
        "general": "📄"
    }
    
    icon = content_icons.get(content_type.lower(), "📄")
    
    if HAS_RICH:
        console.print(f"[blue]{icon} Content Search Ready: {original_query}[/blue]")
        console.print(f"[dim]Content Type: {content_type.title()}[/dim]")
        
        if verbose:
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("🔍 Original Query", original_query)
            info_table.add_row("🎯 Content Type", content_type.title())
            info_table.add_row("🔧 Enhanced Query", enhanced_query)
            info_table.add_row("📊 Max Results", str(result.get("max_results", 5)))
            info_table.add_row("💰 Estimated Cost", f"${result.get('estimated_cost', 0.01):.3f}")
            info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Content Search Configuration[/bold]", border_style="purple"))
    else:
        print(f"{icon} Content Search Ready: {original_query}")
        print(f"Content Type: {content_type.title()}")
        if verbose:
            print(f"🔧 Enhanced Query: {enhanced_query}")
            print(f"📊 Max Results: {result.get('max_results', 5)}")
            print(f"💰 Estimated Cost: ${result.get('estimated_cost', 0.01):.3f}")


def _display_query_validation(result: Dict[str, Any], verbose: bool):
    """Display query validation results"""
    query = result.get("query", "Unknown")
    is_valid = result.get("is_valid", False)
    issues = result.get("issues", [])
    suggestions = result.get("suggestions", [])
    
    # Validation status
    status_icon = "✅" if is_valid else "❌"
    status_text = "Valid" if is_valid else "Invalid"
    
    if HAS_RICH:
        console.print(f"[{'green' if is_valid else 'red'}]{status_icon}[/{'green' if is_valid else 'red'}] Query Validation: {status_text}")
        console.print(f"[dim]Query: {query}[/dim]")
        
        # Show issues if any
        if issues:
            console.print("\n[yellow]⚠️ Issues Found:[/yellow]")
            for issue in issues:
                console.print(f"  • {issue}")
        
        # Show suggestions if any
        if suggestions and verbose:
            console.print("\n[blue]💡 Suggestions:[/blue]")
            for suggestion in suggestions:
                console.print(f"  • {suggestion}")
        
        if verbose:
            # Detailed validation info
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Metric", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("Word Count", str(result.get("word_count", 0)))
            info_table.add_row("Character Count", str(result.get("character_count", 0)))
            info_table.add_row("Estimated Results", result.get("estimated_results", "unknown").title())
            info_table.add_row("Validation Time", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Validation Details[/bold]", border_style="yellow"))
    else:
        print(f"{status_icon} Query Validation: {status_text}")
        print(f"Query: {query}")
        
        if issues:
            print("\n⚠️ Issues Found:")
            for issue in issues:
                print(f"  • {issue}")
        
        if suggestions and verbose:
            print("\n💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        
        if verbose:
            print(f"Word Count: {result.get('word_count', 0)}")
            print(f"Estimated Results: {result.get('estimated_results', 'unknown').title()}")


def _display_search_suggestions(result: Dict[str, Any], verbose: bool):
    """Display search suggestions"""
    original_query = result.get("original_query", "Unknown")
    suggestion_type = result.get("suggestion_type", "enhancement")
    suggestions = result.get("suggestions", [])
    
    if HAS_RICH:
        console.print(f"[blue]💡 Search Suggestions for: {original_query}[/blue]")
        console.print(f"[dim]Type: {suggestion_type.title()}[/dim]")
        
        if suggestions:
            console.print(f"\n[green]📝 Suggested Queries:[/green]")
            for i, suggestion in enumerate(suggestions, 1):
                console.print(f"  {i}. {suggestion}")
        else:
            console.print("[yellow]No suggestions available[/yellow]")
        
        if verbose:
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("Original Query", original_query)
            info_table.add_row("Suggestion Type", suggestion_type.title())
            info_table.add_row("Suggestions Count", str(len(suggestions)))
            info_table.add_row("Generated", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Suggestion Details[/bold]", border_style="green"))
    else:
        print(f"💡 Search Suggestions for: {original_query}")
        print(f"Type: {suggestion_type.title()}")
        if suggestions:
            print("\n📝 Suggested Queries:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("No suggestions available")
        
        if verbose:
            print(f"Original Query: {original_query}")
            print(f"Suggestion Type: {suggestion_type.title()}")
            print(f"Suggestions Count: {len(suggestions)}")
            print(f"Generated: {result.get('timestamp', 'Unknown')}")


def _display_generic_result(result: Dict[str, Any], verbose: bool):
    """Display generic operation results"""
    status = result.get("status", "unknown")
    operation = result.get("operation", "operation")
    
    if status == "ready_for_execution":
        if HAS_RICH:
            console.print(f"[green]✅ {operation.replace('_', ' ').title()} ready for execution[/green]")
        else:
            print(f"✅ {operation.replace('_', ' ').title()} ready for execution")
    elif status == "success":
        if HAS_RICH:
            console.print(f"[green]✅ {operation.replace('_', ' ').title()} completed successfully[/green]")
        else:
            print(f"✅ {operation.replace('_', ' ').title()} completed successfully")
    else:
        if HAS_RICH:
            console.print(f"[yellow]⚠️ {operation.replace('_', ' ').title()}: {status}[/yellow]")
        else:
            print(f"⚠️ {operation.replace('_', ' ').title()}: {status}")
    
    if verbose:
        # Display all available information
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        for key, value in result.items():
            if key not in ["status", "operation"]:
                display_key = key.replace('_', ' ').title()
                display_value = str(value)
                if len(display_value) > 50:
                    display_value = display_value[:47] + "..."
                info_table.add_row(display_key, display_value)
        
        if HAS_RICH:
            console.print(Panel(info_table, title="[bold]Operation Details[/bold]", border_style="blue"))
        else:
            print("\nOperation Details:")
            for key, value in result.items():
                if key not in ["status", "operation"]:
                    print(f"  {key.replace('_', ' ').title()}: {value}")


def display_search_execution_status(query: str, status: str = "executing"):
    """
    Display search execution status
    
    Args:
        query: Search query being executed
        status: Current execution status
    """
    status_icons = {
        "executing": "🔍",
        "completed": "✅",
        "failed": "❌",
        "preparing": "⚙️"
    }
    
    icon = status_icons.get(status, "🔍")
    if HAS_RICH:
        console.print(f"{icon} {status.title()}: {query}")
    else:
        print(f"{icon} {status.title()}: {query}")


def display_search_capabilities(capabilities: Dict[str, Any]):
    """
    Display web search capabilities and limitations
    
    Args:
        capabilities: Capabilities dictionary from get_search_capabilities()
    """
    if HAS_RICH:
        console.print("[blue]🔍 Web Search Capabilities[/blue]")
        
        # Operations table
        ops_table = Table(title="Available Operations", show_header=True)
        ops_table.add_column("Operation", style="cyan")
        ops_table.add_column("Description", style="white")
        
        operation_descriptions = {
            "perform_web_search": "Basic web search with query and result limit",
            "perform_filtered_search": "Search with domain and date filters",
            "perform_content_search": "Content-type specific search",
            "validate_search_query": "Validate query for potential issues",
            "get_search_suggestions": "Generate query suggestions and improvements"
        }
        
        for op in capabilities.get("operations", []):
            desc = operation_descriptions.get(op, "No description available")
            ops_table.add_row(op, desc)
        
        # Limitations table
        limits_table = Table(title="Limitations", show_header=True)
        limits_table.add_column("Limit", style="yellow")
        limits_table.add_column("Value", style="white")
        
        limitations = capabilities.get("limitations", {})
        for limit, value in limitations.items():
            limit_display = limit.replace('_', ' ').title()
            limits_table.add_row(limit_display, str(value))
        
        # Display in columns
        console.print(Columns([ops_table, limits_table]))
        
        # Cost information
        cost_info = capabilities.get("cost_structure", {})
        if cost_info:
            console.print(f"\n[green]💰 Cost Structure:[/green]")
            console.print(f"  Base Cost: ${cost_info.get('base_cost', 0.01):.3f}")
            console.print(f"  Per Result: ${cost_info.get('per_result_cost', 0.002):.3f}")
    else:
        print("[blue]🔍 Web Search Capabilities[/blue]")
        print("Available Operations:")
        for op in capabilities.get("operations", []):
            print(f"  - {op}")
        print("\nLimitations:")
        for limit, value in capabilities.get("limitations", {}).items():
            print(f"  - {limit.replace('_', ' ').title()}: {value}")
        if capabilities.get("cost_structure"):
            print("\nCost Structure:")
            print(f"  - Base Cost: ${capabilities['cost_structure'].get('base_cost', 0.01):.3f}")
            print(f"  - Per Result: ${capabilities['cost_structure'].get('per_result_cost', 0.002):.3f}")


def display_agent_handoff_format(result: Dict[str, Any]):
    """
    Format result for agent-to-agent handoff
    
    Args:
        result: Result dictionary to format for handoff
    """
    if "error" in result:
        return f"❌ Web Search Error: {result['error']}"
    
    operation = result.get("operation", "unknown")
    query = result.get("query", "Unknown")
    
    if operation == "web_search":
        max_results = result.get("max_results", 5)
        cost = result.get("estimated_cost", 0.01)
        return f"🔍 Search Ready: {query} ({max_results} results, ${cost:.3f})"
    elif operation == "filtered_web_search":
        filters = result.get("applied_filters", {})
        filter_text = []
        if filters.get("domain"):
            filter_text.append(f"domain:{filters['domain']}")
        if filters.get("date_range"):
            filter_text.append(f"date:{filters['date_range']}")
        filter_str = " • ".join(filter_text) if filter_text else "no filters"
        return f"🔍 Filtered Search Ready: {query} ({filter_str})"
    elif operation == "query_validation":
        is_valid = result.get("is_valid", False)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        return f"🔍 Query Validation: {query} ({status})"
    else:
        return f"🔍 {operation.replace('_', ' ').title()}: {query}"


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for UI operations - standardized naming"""
    return 0.0  # UI operations are free 