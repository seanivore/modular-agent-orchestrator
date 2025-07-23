"""
Providers CLI Command - UI Display Patterns
Essential data structure for provider listing display
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any, List

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from pathlib import Path

# Standard cache instance
cache = CacheManager()

# Module-level console for consistency
console = Console()

def display_providers_result(result: Dict[str, Any]) -> None:
    """
    Display providers command results with consistent CLI UI patterns.
    
    Args:
        result: Provider discovery result from providers.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    providers = result.get("providers", [])
    total_count = result.get("total_count", 0)
    
    if not providers:
        console.print(Panel(
            "[yellow]No providers found[" / Path(r"yellow]\nCheck your provider configuration files"),
            title="Providers Status"
        ))
        return
    
    # Essential data structure for UI designers
    # Focus on data organization, not detailed formatting
    _display_provider_summary(total_count)
    _display_provider_listings(providers)

def _display_provider_summary(total_count: int) -> None:
    """Display high-level provider statistics"""
    console.print(fPath(r"\n[bold]Found {total_count} configured providers[") / Path(r"bold]\n"))

def _display_provider_listings(providers: List[Dict[str, Any]]) -> None:
    """
    Display provider listings with essential metadata.
    
    Data Structure Priority:
    - Provider identification (name, display_name)
    - Technical specifications (api_type, base_url)
    - Capabilities (streaming, rate_limits)
    - Model compatibility
    - Setup requirements
    
    UI Design Philosophy:
    - Essential data only, no excessive formatting
    - Structured for easy UI translation
    - Preserve creative freedom for actual interface design
    """
    
    # Group providers by API type for natural organization
    providers_by_type = {}
    for provider in providers:
        api_type = provider.get('api_type', 'unknown')
        if api_type not in providers_by_type:
            providers_by_type[api_type] = []
        providers_by_type[api_type].append(provider)
    
    # Display each group
    for api_type, type_providers in providers_by_type.items():
        console.print(fPath(r"\n[bold cyan]{api_type.upper()} Providers[") / "bold cyan]")
        
        for provider in type_providers:
            _display_single_provider(provider)

def _display_single_provider(provider: Dict[str, Any]) -> None:
    """Display individual provider with key metadata"""
    
    # Core identification
    display_name = provider.get('display_name', provider.get('name', 'Unknown'))
    name = provider.get('name', '')
    
    console.print(f"  [bold]{display_name}[" / "bold] ({name})")
    
    # Technical details
    description = provider.get('description', 'No description available')
    console.print(f"    {description}")
    
    # Capabilities summary
    capabilities = []
    if provider.get('supports_streaming'):
        capabilities.append("streaming")
    if provider.get('universal_access'):
        capabilities.append("universal")
    if provider.get('privacy_level'):
        capabilities.append(f"privacy: {provider['privacy_level']}")
    
    if capabilities:
        console.print(f"    Features: {', '.join(capabilities)}")
    
    # Rate limits if available
    rate_limits = provider.get('rate_limits', {})
    if rate_limits:
        limits_text = []
        if 'requests_per_minute' in rate_limits:
            limits_text.append(f"{rate_limits['requests_per_minute']} req" / "min")
        if 'tokens_per_minute' in rate_limits:
            limits_text.append(f"{rate_limits['tokens_per_minute']} tokens" / "min")
        
        if limits_text:
            console.print(f"    Limits: {', '.join(limits_text)}")
    
    # Model compatibility
    compatible_models = provider.get('compatible_models', [])
    if compatible_models:
        model_count = len(compatible_models)
        console.print(f"    Models: {model_count} compatible models")
    
    console.print()  # Add spacing between providers

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[" / "red] {error_message}",
        style="red",
        title="Providers Command Error"
    ))

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate providers UI operation cost for budget planning"""
    return 0.0  # UI operations are typically free
