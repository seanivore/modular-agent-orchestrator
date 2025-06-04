"""
Think Tool - UI Display
Beautiful terminal formatting for thinking operations
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.markdown import Markdown
from typing import Dict, Any
import time

console = Console()

def display_thinking_session(result: Dict[str, Any], verbose: bool = False):
    """Display thinking session results"""
    
    if result.get("status") == "error":
        console.print(f"❌ [red]Thinking Error:[/red] {result.get('error', 'Unknown error')}")
        return
    
    session_data = result.get("session_data", {})
    
    # Header
    console.print("\n🧠 [bold blue]AI Thinking Session[/bold blue]")
    console.print("=" * 60)
    
    # Session info panel
    session_info = Table.grid(padding=1)
    session_info.add_column(style="cyan", no_wrap=True)
    session_info.add_column()
    
    session_info.add_row("📋 Topic:", session_data.get("topic", ""))
    session_info.add_row("🎯 Approach:", session_data.get("thinking_approach", ""))
    session_info.add_row("🔍 Focus:", session_data.get("thinking_focus", ""))
    
    if session_data.get("context"):
        session_info.add_row("📝 Context:", session_data.get("context", ""))
    
    session_info.add_row("⏰ Session ID:", session_data.get("session_id", ""))
    session_info.add_row("💰 Est. Cost:", f"${session_data.get('estimated_cost', 0):.4f}")
    
    console.print(Panel(session_info, title="Session Details", border_style="blue"))
    
    if verbose:
        # Verbose mode - show all metadata
        console.print("\n📊 [bold]Session Metadata[/bold]")
        metadata_table = Table(show_header=True, header_style="bold magenta")
        metadata_table.add_column("Property")
        metadata_table.add_column("Value")
        
        for key, value in session_data.items():
            if key not in ["topic", "thinking_approach", "thinking_focus", "context"]:
                metadata_table.add_row(str(key), str(value))
        
        console.print(metadata_table)
    
    # Instructions
    console.print(f"\n💡 [yellow]{result.get('message', '')}[/yellow]")
    console.print("🚀 Execute the human button snippet to start AI thinking!")

def display_thinking_progress():
    """Display thinking progress indicator"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("🧠 AI thinking in progress...", total=None)
        
        # Simulate thinking progress
        for i in range(10):
            time.sleep(0.3)
            progress.update(task, description=f"🧠 Processing thoughts... {i+1}/10")
        
        progress.update(task, description="✅ Thinking completed!")

def display_thinking_results(thinking_output: str, session_data: Dict[str, Any], verbose: bool = False):
    """Display completed thinking results"""
    
    console.print("\n🎯 [bold green]Thinking Results[/bold green]")
    console.print("=" * 60)
    
    # Results panel
    if len(thinking_output) > 1000 and not verbose:
        # Truncate for clean mode
        truncated = thinking_output[:1000] + "..."
        console.print(Panel(truncated, title="Thinking Output (Truncated)", border_style="green"))
        console.print("💡 [dim]Use verbose mode to see full results[/dim]")
    else:
        console.print(Panel(thinking_output, title="Thinking Output", border_style="green"))
    
    # Session summary
    summary_table = Table.grid(padding=1)
    summary_table.add_column(style="cyan", no_wrap=True)
    summary_table.add_column()
    
    summary_table.add_row("📋 Topic:", session_data.get("topic", ""))
    summary_table.add_row("🎯 Approach:", session_data.get("thinking_approach", ""))
    summary_table.add_row("⏰ Completed:", session_data.get("timestamp", ""))
    
    if session_data.get("save_results"):
        summary_table.add_row("💾 Saved:", "Results saved to file")
    
    console.print(Panel(summary_table, title="Session Summary", border_style="blue"))

def display_prompt_enhancement(result: Dict[str, Any], verbose: bool = False):
    """Display prompt enhancement results"""
    
    if result.get("status") == "error":
        console.print(f"❌ [red]Enhancement Error:[/red] {result.get('error', 'Unknown error')}")
        return
    
    enhancement_data = result.get("enhancement_data", {})
    
    console.print("\n✨ [bold blue]Prompt Enhancement[/bold blue]")
    console.print("=" * 60)
    
    # Enhancement info
    enhancement_info = Table.grid(padding=1)
    enhancement_info.add_column(style="cyan", no_wrap=True)
    enhancement_info.add_column()
    
    enhancement_info.add_row("📝 Original:", enhancement_data.get("original_topic", ""))
    enhancement_info.add_row("🎯 Approach:", enhancement_data.get("enhancement_approach", ""))
    enhancement_info.add_row("🔍 Focus:", enhancement_data.get("enhancement_focus", ""))
    enhancement_info.add_row("⏰ Timestamp:", enhancement_data.get("timestamp", ""))
    
    console.print(Panel(enhancement_info, title="Enhancement Details", border_style="blue"))
    
    console.print(f"\n💡 [yellow]{result.get('message', '')}[/yellow]")

def display_thinking_validation(result: Dict[str, Any], verbose: bool = False):
    """Display thinking tool validation results"""
    
    if result.get("status") == "error":
        console.print(f"❌ [red]Validation Error:[/red] {result.get('error', 'Unknown error')}")
        return
    
    validation = result.get("validation", {})
    
    console.print("\n🔍 [bold blue]Think Tool Validation[/bold blue]")
    console.print("=" * 60)
    
    # Core functions status
    functions_table = Table(show_header=True, header_style="bold magenta")
    functions_table.add_column("Function")
    functions_table.add_column("Status")
    
    for func, status in validation.get("core_functions", {}).items():
        status_icon = "✅" if status == "available" else "❌"
        functions_table.add_row(func, f"{status_icon} {status}")
    
    console.print(Panel(functions_table, title="Core Functions", border_style="green"))
    
    if verbose:
        # Requirements details
        req_table = Table(show_header=True, header_style="bold cyan")
        req_table.add_column("Requirement")
        req_table.add_column("Status")
        
        for req, status in validation.get("requirements", {}).items():
            req_table.add_row(req, status)
        
        console.print(Panel(req_table, title="Requirements", border_style="blue"))
    
    console.print(f"\n✅ [green]{result.get('message', '')}[/green]")

def display_thinking_capabilities(result: Dict[str, Any], verbose: bool = False):
    """Display thinking tool capabilities"""
    
    if result.get("status") == "error":
        console.print(f"❌ [red]Capabilities Error:[/red] {result.get('error', 'Unknown error')}")
        return
    
    capabilities = result.get("capabilities", {})
    
    console.print("\n🚀 [bold blue]Think Tool Capabilities[/bold blue]")
    console.print("=" * 60)
    
    # Core operations
    ops_table = Table(show_header=True, header_style="bold magenta")
    ops_table.add_column("Operation", style="cyan")
    
    for op in capabilities.get("core_operations", []):
        ops_table.add_row(op)
    
    console.print(Panel(ops_table, title="Core Operations", border_style="green"))
    
    # Features
    features_text = "\n".join([f"• {feature}" for feature in capabilities.get("thinking_features", [])])
    console.print(Panel(features_text, title="Thinking Features", border_style="blue"))
    
    if verbose:
        # Flexibility features
        flex_text = "\n".join([f"• {flex}" for flex in capabilities.get("flexibility", [])])
        console.print(Panel(flex_text, title="Flexibility", border_style="yellow"))
        
        # Model compatibility
        models_text = "\n".join([f"• {model}" for model in capabilities.get("model_compatibility", [])])
        console.print(Panel(models_text, title="Model Compatibility", border_style="cyan"))
        
        # Cost structure
        cost_info = capabilities.get("cost_structure", {})
        cost_text = f"Base Cost: {cost_info.get('base_cost', 'N/A')}\n"
        cost_text += "Factors: " + ", ".join(cost_info.get("factors", []))
        console.print(Panel(cost_text, title="Cost Structure", border_style="red"))

def display_agent_handoff(operation: str, params: Dict[str, Any]):
    """Display formatted handoff for agent-to-agent communication"""
    
    console.print(f"\n🤖 [bold blue]Agent Handoff - Think Tool[/bold blue]")
    console.print("=" * 50)
    
    handoff_table = Table.grid(padding=1)
    handoff_table.add_column(style="cyan", no_wrap=True)
    handoff_table.add_column()
    
    handoff_table.add_row("🔧 Operation:", operation)
    handoff_table.add_row("📋 Topic:", params.get("topic", ""))
    handoff_table.add_row("🎯 Approach:", params.get("thinking_approach", ""))
    handoff_table.add_row("🔍 Focus:", params.get("thinking_focus", ""))
    
    if params.get("context"):
        handoff_table.add_row("📝 Context:", params.get("context", ""))
    
    console.print(Panel(handoff_table, title="Handoff Details", border_style="blue"))
    console.print("🚀 Ready for execution via human button") 