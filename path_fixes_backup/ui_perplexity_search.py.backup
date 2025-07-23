"""
PERPLEXITY SEARCH
UI Display Component
"""

# Rich import with fallback for graceful degradation
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
    # Fallback classes for when Rich is not available
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    class Panel:
        def __init__(self, *args, **kwargs):
            pass
    
    class Table:
        def __init__(self, *args, **kwargs):
            pass
        def add_column(self, *args, **kwargs):
            pass
        def add_row(self, *args, **kwargs):
            pass
    
    console = Console()

from typing import Dict, Any, List

# Standardization imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Estimate cost for UI operations (always free)
    
    Args:
        params: Operation parameters
        
    Returns:
        Cost estimate (0.0 for UI operations)
    """
    return 0.0  # UI operations are free

@handle_errors(operation_name="display_perplexity_result", return_dict=False)
def display_perplexity_result(result: Dict[str, Any], verbose: bool = False):
    """
    Standardized display function alias for consistency
    
    Args:
        result: Result dictionary from Perplexity operations
        verbose: Whether to show detailed information
    """
    return display_perplexity_search_result(result, verbose)

@handle_errors(operation_name="display_perplexity_search_result", return_dict=False)
def display_perplexity_search_result(result: Dict[str, Any], verbose: bool = False):
    """
    Display Perplexity Search operation results with beautiful formatting
    
    Args:
        result: Result dictionary from Perplexity operations
        verbose: Whether to show detailed information
    """
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    operation = result.get("operation", "unknown")
    
    if operation == "perplexity_search":
        _display_basic_search(result, verbose)
    elif operation == "enhanced_perplexity_research":
        _display_enhanced_research(result, verbose)
    elif operation == "perplexity_query_validation":
        _display_query_validation(result, verbose)
    elif operation == "perplexity_research_suggestions":
        _display_research_suggestions(result, verbose)
    elif operation == "api_configuration_check":
        _display_api_configuration(result, verbose)
    else:
        _display_generic_result(result, verbose)

@handle_errors(operation_name="display_error", return_dict=False)
def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    if HAS_RICH:
        panel = Panel(
            f"❌ Error: {error_msg}",
            title="Perplexity Search Error",
            border_style="red"
        )
        console.print(panel)
    else:
        print(f"❌ Perplexity Search Error: {error_msg}")


@handle_errors(operation_name="_display_basic_search", return_dict=False)
def _display_basic_search(result: Dict[str, Any], verbose: bool):
    """Display basic Perplexity search results"""
    query = result.get("query", "Unknown")
    model = result.get("model", "Unknown")
    estimated_cost = result.get("estimated_cost", 0.025)
    search_context = result.get("search_context", "general")
    
    # Main search message
    if HAS_RICH:
        console.print(f"[blue]🧠 Perplexity Search Ready: {query}[/blue]")
    else:
        print(f"🧠 Perplexity Search Ready: {query}")
    
    if verbose:
        if HAS_RICH:
            # Detailed search configuration
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="white")
            
            info_table.add_row("🧠 Query", query)
            info_table.add_row("🤖 Model", model)
            info_table.add_row("🎯 Context", search_context.title())
            info_table.add_row("💰 Estimated Cost", f"${estimated_cost:.3f}")
            info_table.add_row("🔧 Method", result.get("execution_method", "unknown"))
            info_table.add_row("🌐 Endpoint", result.get("api_endpoint", "unknown"))
            info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
            
            console.print(Panel(info_table, title="[bold]Perplexity Search Configuration[/bold]", border_style="blue"))
        else:
            print(f"🧠 Query: {query}")
            print(f"🤖 Model: {model}")
            print(f"🎯 Context: {search_context.title()}")
            print(f"💰 Estimated Cost: ${estimated_cost:.3f}")
            print(f"🔧 Method: {result.get('execution_method', 'unknown')}")
            print(f"🌐 Endpoint: {result.get('api_endpoint', 'unknown')}")
            print(f"⏰ Prepared: {result.get('timestamp', 'Unknown')}")
    else:
        if HAS_RICH:
            console.print(f"[dim]🤖 {model} • ${estimated_cost:.3f} estimated[/dim]")
        else:
            print(f"🤖 {model} • ${estimated_cost:.3f} estimated")

@handle_errors(operation_name="_display_enhanced_research", return_dict=False)
def _display_enhanced_research(result: Dict[str, Any], verbose: bool):
    """Display enhanced research results"""
    query = result.get("query", "Unknown")
    research_approach = result.get("research_approach", "comprehensive")
    analysis_focus = result.get("analysis_focus", "general")
    model = result.get("model", "Unknown")
    estimated_cost = result.get("estimated_cost", 0.025)
    
    console.print(f"[blue]🧠 Enhanced Research Ready: {query}[/blue]")
    console.print(f"[dim]Approach: {research_approach.title()} • Focus: {analysis_focus.title()}[/dim]")
    
    if verbose:
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("🧠 Query", query)
        info_table.add_row("📊 Research Approach", research_approach.title())
        info_table.add_row("🎯 Analysis Focus", analysis_focus.title())
        info_table.add_row("🤖 Model", model)
        info_table.add_row("💰 Estimated Cost", f"${estimated_cost:.3f}")
        info_table.add_row("🔧 Method", result.get("execution_method", "unknown"))
        info_table.add_row("⏰ Prepared", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Enhanced Research Configuration[/bold]", border_style="purple"))

@handle_errors(operation_name="_display_query_validation", return_dict=False)
def _display_query_validation(result: Dict[str, Any], verbose: bool):
    """Display query validation results"""
    query = result.get("query", "Unknown")
    is_valid = result.get("is_valid", False)
    issues = result.get("issues", [])
    suggestions = result.get("suggestions", [])
    estimated_quality = result.get("estimated_quality", "unknown")
    
    # Validation status
    if is_valid:
        status_icon = "[green]✅[/green]"
        status_text = "Valid"
    else:
        status_icon = "[red]❌[/red]"
        status_text = "Invalid"
    
    console.print(f"{status_icon} Query Validation: {status_text}")
    console.print(f"[dim]Query: {query}[/dim]")
    console.print(f"[dim]Estimated Quality: {estimated_quality.title()}[/dim]")
    
    # Show issues if any
    if issues:
        console.print("\n[yellow]⚠️ Issues Found:[/yellow]")
        for issue in issues:
            console.print(f"  • {issue}")
    
    # Show suggestions if any
    if suggestions:
        console.print("\n[blue]💡 Suggestions:[/blue]")
        for suggestion in suggestions[:3 if not verbose else len(suggestions)]:
            console.print(f"  • {suggestion}")
        
        if not verbose and len(suggestions) > 3:
            console.print(f"  [dim]... and {len(suggestions) - 3} more (use verbose mode)[/dim]")
    
    if verbose:
        # Detailed validation info
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Metric", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Word Count", str(result.get("word_count", 0)))
        info_table.add_row("Character Count", str(result.get("character_count", 0)))
        info_table.add_row("Question Format", "Yes" if result.get("has_question_format") else "No")
        info_table.add_row("Estimated Quality", estimated_quality.title())
        info_table.add_row("Validation Time", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]Validation Details[/bold]", border_style="yellow"))

@handle_errors(operation_name="_display_research_suggestions", return_dict=False)
def _display_research_suggestions(result: Dict[str, Any], verbose: bool):
    """Display research suggestions"""
    original_query = result.get("original_query", "Unknown")
    suggestion_type = result.get("suggestion_type", "enhancement")
    suggestions = result.get("suggestions", [])
    
    console.print(f"[blue]💡 Research Suggestions for: {original_query}[/blue]")
    console.print(f"[dim]Type: {suggestion_type.title()}[/dim]")
    
    if suggestions:
        console.print(f"\n[green]📝 Suggested Research Queries:[/green]")
        display_count = len(suggestions) if verbose else min(5, len(suggestions))
        
        for i, suggestion in enumerate(suggestions[:display_count], 1):
            console.print(f"  {i}. {suggestion}")
        
        if not verbose and len(suggestions) > 5:
            console.print(f"  [dim]... and {len(suggestions) - 5} more (use verbose mode)[/dim]")
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

@handle_errors(operation_name="_display_api_configuration", return_dict=False)
def _display_api_configuration(result: Dict[str, Any], verbose: bool):
    """Display API configuration status"""
    api_key_present = result.get("api_key_present", False)
    api_endpoint = result.get("api_endpoint", "Unknown")
    supported_models = result.get("supported_models", [])
    issues = result.get("issues", [])
    suggestions = result.get("suggestions", [])
    
    # API status
    if api_key_present:
        status_icon = "[green]✅[/green]"
        status_text = "API Key Present"
    else:
        status_icon = "[red]❌[/red]"
        status_text = "API Key Missing"
    
    console.print(f"{status_icon} Perplexity API Configuration: {status_text}")
    
    if issues:
        console.print("\n[yellow]⚠️ Configuration Issues:[/yellow]")
        for issue in issues:
            console.print(f"  • {issue}")
    
    if suggestions:
        console.print("\n[blue]💡 Setup Instructions:[/blue]")
        for suggestion in suggestions:
            console.print(f"  • {suggestion}")
    
    if verbose:
        # Detailed API info
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("API Endpoint", api_endpoint)
        info_table.add_row("API Key Present", "Yes" if api_key_present else "No")
        
        if api_key_present and "api_key_length" in result:
            info_table.add_row("API Key Length", str(result["api_key_length"]))
        
        info_table.add_row("Supported Models", str(len(supported_models)))
        info_table.add_row("Check Time", result.get("timestamp", "Unknown"))
        
        console.print(Panel(info_table, title="[bold]API Configuration Details[/bold]", border_style="cyan"))
        
        # Models table
        if supported_models:
            models_table = Table(title="Supported Models", show_header=True)
            models_table.add_column("Model", style="cyan")
            models_table.add_column("Type", style="white")
            
            for model in supported_models:
                if "small" in model:
                    model_type = "Small (Fast, Lower Cost)"
                elif "large" in model:
                    model_type = "Large (Balanced)"
                elif "huge" in model:
                    model_type = "Huge (Most Capable)"
                else:
                    model_type = "Unknown"
                
                models_table.add_row(model, model_type)
            
            console.print(models_table)

@handle_errors(operation_name="_display_generic_result", return_dict=False)
def _display_generic_result(result: Dict[str, Any], verbose: bool):
    """Display generic operation results"""
    status = result.get("status", "unknown")
    operation = result.get("operation", "operation")
    
    if status == "ready_for_execution":
        console.print(f"[green]✅ {operation.replace('_', ' ').title()} ready for execution[/green]")
    elif status == "success":
        console.print(f"[green]✅ {operation.replace('_', ' ').title()} completed successfully[/green]")
    else:
        console.print(f"[yellow]⚠️ {operation.replace('_', ' ').title()}: {status}[/yellow]")
    
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
        
        console.print(Panel(info_table, title="[bold]Operation Details[/bold]", border_style="blue"))

@handle_errors(operation_name="display_search_execution_status", return_dict=False)
def display_search_execution_status(query: str, status: str = "executing"):
    """
    Display search execution status
    
    Args:
        query: Search query being executed
        status: Current execution status
    """
    status_icons = {
        "executing": "🧠",
        "completed": "✅",
        "failed": "❌",
        "preparing": "⚙️",
        "analyzing": "🔍"
    }
    
    icon = status_icons.get(status, "🧠")
    console.print(f"{icon} {status.title()}: {query}")

@handle_errors(operation_name="display_perplexity_capabilities", return_dict=False)
def display_perplexity_capabilities(capabilities: Dict[str, Any]):
    """
    Display Perplexity search capabilities and limitations
    
    Args:
        capabilities: Capabilities dictionary from get_perplexity_capabilities()
    """
    console.print("[blue]🧠 Perplexity AI Capabilities[/blue]")
    
    # Operations table
    ops_table = Table(title="Available Operations", show_header=True)
    ops_table.add_column("Operation", style="cyan")
    ops_table.add_column("Description", style="white")
    
    operation_descriptions = {
        "perform_perplexity_search": "Basic AI-powered search with reasoning",
        "perform_enhanced_research": "Advanced research with flexible approach",
        "validate_perplexity_query": "Validate query for optimal results",
        "get_research_suggestions": "Generate query improvements and alternatives",
        "check_api_configuration": "Check API setup and configuration"
    }
    
    for op in capabilities.get("operations", []):
        desc = operation_descriptions.get(op, "No description available")
        ops_table.add_row(op, desc)
    
    # Features table
    features_table = Table(title="AI Features", show_header=True)
    features_table.add_column("Feature", style="green")
    features_table.add_column("Description", style="white")
    
    feature_descriptions = {
        "ai_reasoning": "Advanced AI reasoning and analysis",
        "source_citations": "Automatic source citations and references",
        "real_time_information": "Access to current web information",
        "comprehensive_analysis": "Multi-perspective comprehensive analysis",
        "related_questions": "Generates related research questions",
        "multi_perspective_analysis": "Multiple viewpoints and perspectives"
    }
    
    for feature in capabilities.get("features", []):
        desc = feature_descriptions.get(feature, "Advanced AI capability")
        features_table.add_row(feature.replace('_', ' ').title(), desc)
    
    # Display in columns
    console.print(Columns([ops_table, features_table]))
    
    # Models and cost information
    models = capabilities.get("supported_models", [])
    if models:
        console.print(f"\n[green]🤖 Supported Models:[/green]")
        for model in models:
            if "small" in model:
                console.print(f"  • {model} [dim](Fast, Lower Cost)[/dim]")
            elif "large" in model:
                console.print(f"  • {model} [dim](Balanced Performance)[/dim]")
            elif "huge" in model:
                console.print(f"  • {model} [dim](Most Capable)[/dim]")
    
    # Cost information
    cost_info = capabilities.get("cost_structure", {})
    if cost_info:
        console.print(f"\n[green]💰 Cost Structure:[/green]")
        console.print(f"  Small Model: ${cost_info.get('small_model', 0.015):.3f}")
        console.print(f"  Large Model: ${cost_info.get('large_model', 0.025):.3f}")
        console.print(f"  Huge Model: ${cost_info.get('huge_model', 0.040):.3f}")
        console.print(f"  Enhanced Research: +{int((cost_info.get('enhanced_multiplier', 1.5) - 1) * 100)}%")

@handle_errors(operation_name="display_agent_handoff_format", return_dict=False)
def display_agent_handoff_format(result: Dict[str, Any]):
    """
    Format result for agent-to-agent handoff
    
    Args:
        result: Result dictionary to format for handoff
    """
    if "error" in result:
        return f"❌ Perplexity Error: {result['error']}"
    
    operation = result.get("operation", "unknown")
    query = result.get("query", "Unknown")
    
    if operation == "perplexity_search":
        model = result.get("model", "unknown")
        cost = result.get("estimated_cost", 0.025)
        return f"🧠 Perplexity Search Ready: {query} ({model}, ${cost:.3f})"
    elif operation == "enhanced_perplexity_research":
        approach = result.get("research_approach", "comprehensive")
        focus = result.get("analysis_focus", "general")
        return f"🧠 Enhanced Research Ready: {query} ({approach}, {focus})"
    elif operation == "perplexity_query_validation":
        is_valid = result.get("is_valid", False)
        quality = result.get("estimated_quality", "unknown")
        status = f"✅ Valid ({quality})" if is_valid else "❌ Invalid"
        return f"🧠 Query Validation: {query} ({status})"
    elif operation == "api_configuration_check":
        api_status = "✅ Ready" if result.get("api_key_present") else "❌ Setup Required"
        return f"🧠 API Configuration: {api_status}"
    else:
        return f"🧠 {operation.replace('_', ' ').title()}: {query}"

@handle_errors(operation_name="display_research_progress", return_dict=False)
def display_research_progress(stage: str, details: str = ""):
    """
    Display research progress indicator
    
    Args:
        stage: Current research stage
        details: Additional details about the stage
    """
    stage_icons = {
        "preparing": "⚙️",
        "querying": "🧠",
        "analyzing": "🔍",
        "citing": "📚",
        "finalizing": "✨",
        "complete": "✅"
    }
    
    icon = stage_icons.get(stage.lower(), "🧠")
    stage_text = stage.replace('_', ' ').title()
    
    if details:
        console.print(f"{icon} {stage_text}: {details}")
    else:
        console.print(f"{icon} {stage_text}...") 