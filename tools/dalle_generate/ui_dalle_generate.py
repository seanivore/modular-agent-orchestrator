"""
DALL-E IMAGE GENERATION
UI Display Component
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.tree import Tree
from typing import Dict, Any, List
import json
from datetime import datetime
from pathlib import Path

console = Console()

def display_dalle_generate_result(result: Dict[str, Any], verbose: bool = False):
    """
    Display DALL-E image generation operation results with beautiful formatting
    
    Args:
        result: Result from DALL-E operations
        verbose: Whether to show detailed information
    """
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    operation = result.get("operation", "dalle_operation")
    
    if operation == "dalle_image_generation":
        _display_generation_result(result, verbose)
    elif operation == "dalle_prompt_enhancement":
        _display_enhancement_result(result, verbose)
    elif operation == "dalle_setup_validation":
        _display_validation_result(result, verbose)
    elif operation == "dalle_batch_generation":
        _display_batch_result(result, verbose)
    elif operation == "dalle_image_info":
        _display_image_info_result(result, verbose)
    else:
        _display_generic_result(result, verbose)

def _display_generation_result(result: Dict[str, Any], verbose: bool):
    """Display image generation results"""
    metadata = result.get("metadata", {})
    generated_images = result.get("generated_images", [])
    download_errors = result.get("download_errors", [])
    
    # Header
    console.print(Panel.fit(
        f"🎨 [bold green]DALL-E Image Generation Complete[ / bold green]",
        style="green"
    ))
    
    # Summary table
    summary_table = Table(show_header=False, box=None, padding=(0, 1))
    summary_table.add_column("Field", style="cyan", width=20)
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("Model", metadata.get("model", "Unknown"))
    summary_table.add_row("Images Generated", str(len(generated_images)))
    summary_table.add_row("Size", metadata.get("size", "Unknown"))
    summary_table.add_row("Quality", metadata.get("quality", "Unknown"))
    summary_table.add_row("Style", metadata.get("style", "Unknown"))
    summary_table.add_row("Cost", f"${metadata.get('actual_cost', 0):.3f}")
    
    console.print(summary_table)
    console.print()
    
    # Generated images
    if generated_images:
        console.print("[bold cyan]📸 Generated Images:[ / bold cyan]")
        
        for i, image in enumerate(generated_images, 1):
            image_panel = Panel(
                f"[bold white]{image['filename']}[" / bold white]\n")
                f"📁 {image['filepath']}\n")
                f"📏 {image['size_bytes']:,} bytes ({image['size_bytes']/1024" / 1024:.1f} MB)\n")
                f"🔗 {image['url'][:60]}..." if len(image['url']) > 60 else f"🔗 {image['url']}",
                title=f"Image {i}",
                border_style="green"
            )
            console.print(image_panel)
        
        console.print()
    
    # Download errors
    if download_errors:
        console.print("[bold red]⚠️  Download Issues:[ / bold red]")
        for error in download_errors:
            console.print(f"  • {error}")
        console.print()
    
    # Verbose details
    if verbose:
        _display_verbose_generation_details(result)

def _display_enhancement_result(result: Dict[str, Any], verbose: bool):
    """Display prompt enhancement results"""
    console.print(Panel.fit(
        f"✨ [bold green]Prompt Enhancement Complete[ / bold green]",
        style="green"
    ))
    
    # Enhancement details
    details_table = Table(show_header=False, box=None, padding=(0, 1))
    details_table.add_column("Field", style="cyan", width=20)
    details_table.add_column("Value", style="white")
    
    details_table.add_row("Approach", result.get("enhancement_approach", "Unknown"))
    details_table.add_row("Focus", result.get("enhancement_focus", "Unknown"))
    details_table.add_row("Original Length", str(result.get("enhancements_applied", {}).get("original_length", 0)))
    details_table.add_row("Enhanced Length", str(result.get("enhancements_applied", {}).get("prompt_length", 0)))
    
    console.print(details_table)
    console.print()
    
    # Prompts comparison
    console.print("[bold cyan]📝 Original Prompt:[ / bold cyan]")
    console.print(Panel(result.get("original_prompt", ""), border_style="blue"))
    
    console.print("[bold cyan]✨ Enhanced Prompt:[ / bold cyan]")
    console.print(Panel(result.get("enhanced_prompt", ""), border_style="green"))
    
    if verbose:
        _display_verbose_enhancement_details(result)

def _display_validation_result(result: Dict[str, Any], verbose: bool):
    """Display setup validation results"""
    setup_complete = result.get("setup_complete", False)
    
    if setup_complete:
        console.print(Panel.fit(
            f"✅ [bold green]DALL-E Setup Valid[ / bold green]",
            style="green"
        ))
    else:
        console.print(Panel.fit(
            f"⚠️  [bold yellow]DALL-E Setup Issues Found[ / bold yellow]",
            style="yellow"
        ))
    
    # Status table
    status_table = Table(show_header=False, box=None, padding=(0, 1))
    status_table.add_column("Check", style="cyan", width=25)
    status_table.add_column("Status", style="white")
    
    status_table.add_row("API Key Present", "✅ Yes" if result.get("api_key_present") else "❌ No")
    status_table.add_row("API Key Format Valid", "✅ Yes" if result.get("api_key_valid_format") else "❌ No")
    status_table.add_row("Setup Complete", "✅ Yes" if setup_complete else "❌ No")
    
    console.print(status_table)
    console.print()
    
    # Issues and suggestions
    issues = result.get("issues", [])
    suggestions = result.get("suggestions", [])
    
    if issues:
        console.print("[bold red]🚨 Issues Found:[ / bold red]")
        for issue in issues:
            console.print(f"  • {issue}")
        console.print()
    
    if suggestions:
        console.print("[bold cyan]💡 Suggestions:[ / bold cyan]")
        for suggestion in suggestions:
            console.print(f"  • {suggestion}")
        console.print()
    
    if verbose:
        _display_verbose_validation_details(result)

def _display_batch_result(result: Dict[str, Any], verbose: bool):
    """Display batch generation results"""
    summary = result.get("summary", {})
    results = result.get("results", [])
    
    console.print(Panel.fit(
        f"🎨 [bold green]Batch Generation Complete[ / bold green]",
        style="green"
    ))
    
    # Summary table
    summary_table = Table(show_header=False, box=None, padding=(0, 1))
    summary_table.add_column("Metric", style="cyan", width=20)
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("Total Prompts", str(summary.get("total_prompts", 0)))
    summary_table.add_row("Successful", f"✅ {summary.get('successful', 0)}")
    summary_table.add_row("Failed", f"❌ {summary.get('failed', 0)}")
    summary_table.add_row("Total Cost", f"${summary.get('total_cost', 0):.3f}")
    summary_table.add_row("Avg Cost / Success", f"${summary.get('average_cost_per_success', 0):.3f}")
    
    console.print(summary_table)
    console.print()
    
    # Individual results
    if verbose or summary.get("failed", 0) > 0:
        console.print("[bold cyan]📋 Individual Results:[ / bold cyan]")
        
        for result_item in results:
            prompt_index = result_item.get("prompt_index", 0)
            prompt = result_item.get("prompt", "")
            item_result = result_item.get("result", {})
            
            status = "✅ Success" if item_result.get("status") == "success" else "❌ Failed"
            
            result_panel = Panel(
                f"[bold white]Prompt {prompt_index + 1}:[" / bold white] {prompt[:50]}...\n")
                f"Status: {status}\n"
                f"Error: {item_result.get('error', 'None'}" if item_result.get('error' else f"Images: {len(item_result.get('generated_images', []))}",
                border_style="green" if item_result.get("status") == "success" else "red"
            )
            console.print(result_panel)
        
        console.print()

def _display_image_info_result(result: Dict[str, Any], verbose: bool):
    """Display image information results"""
    console.print(Panel.fit(
        f"📸 [bold green]Image Information[ / bold green]",
        style="green"
    ))
    
    # Image details table
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column("Property", style="cyan", width=20)
    info_table.add_column("Value", style="white")
    
    info_table.add_row("Filename", result.get("filename", "Unknown"))
    info_table.add_row("Size", f"{result.get('size_mb', 0)} MB ({result.get('size_bytes', 0):,} bytes)")
    info_table.add_row("Created", result.get("created", "Unknown"))
    info_table.add_row("Modified", result.get("modified", "Unknown"))
    info_table.add_row("Extension", result.get("file_extension", "Unknown"))
    
    # Dimensions if available
    dimensions = result.get("dimensions", {})
    if isinstance(dimensions, dict):
        info_table.add_row("Dimensions", f"{dimensions.get('width', 0)} x {dimensions.get('height', 0)}")
        info_table.add_row("Format", dimensions.get("format", "Unknown"))
        info_table.add_row("Mode", dimensions.get("mode", "Unknown"))
    else:
        info_table.add_row("Dimensions", str(dimensions))
    
    console.print(info_table)
    console.print()
    
    if verbose:
        console.print("[bold cyan]📁 Full Path:[ / bold cyan]")
        console.print(Panel(result.get("filepath", ""), border_style="blue"))

def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="DALL-E Generate Error",
        border_style="red"
    )
    console.print(panel)

def _display_generic_result(result: Dict[str, Any], verbose: bool):
    """Display generic result information"""
    console.print(Panel.fit(
        f"🎨 [bold green]DALL-E Operation Complete[ / bold green]",
        style="green"
    ))
    
    if verbose:
        console.print("[bold cyan]📋 Full Result:[ / bold cyan]")
        console.print(Panel(json.dumps(result, indent=2), border_style="blue"))
    else:
        console.print(f"Status: {result.get('status', 'Unknown'}")
        console.print(f"Operation: {result.get('operation', 'Unknown'}")

def _display_verbose_generation_details(result: Dict[str, Any]):
    """Display verbose generation details"""
    console.print("[bold cyan]🔍 Detailed Information:[ / bold cyan]")
    
    metadata = result.get("metadata", {})
    
    # Metadata table
    metadata_table = Table(title="Generation Metadata", show_header=True)
    metadata_table.add_column("Property", style="cyan")
    metadata_table.add_column("Value", style="white")
    
    for key, value in metadata.items():
        if key not in ["prompt"]:  # Skip long prompt in table
            metadata_table.add_row(str(key).replace("_", " ").title(), str(value))
    
    console.print(metadata_table)
    console.print()
    
    # Original prompt
    if metadata.get("prompt"):
        console.print("[bold cyan]📝 Original Prompt:[ / bold cyan]")
        console.print(Panel(metadata["prompt"], border_style="blue"))

def _display_verbose_enhancement_details(result: Dict[str, Any]):
    """Display verbose enhancement details"""
    console.print("[bold cyan]🔍 Enhancement Details:[ / bold cyan]")
    
    enhancements = result.get("enhancements_applied", {})
    
    # Enhancement table
    enhancement_table = Table(title="Applied Enhancements", show_header=True)
    enhancement_table.add_column("Enhancement", style="cyan")
    enhancement_table.add_column("Value", style="white")
    
    for key, value in enhancements.items():
        enhancement_table.add_row(str(key).replace("_", " ").title(), str(value))
    
    console.print(enhancement_table)
    console.print()

def _display_verbose_validation_details(result: Dict[str, Any]):
    """Display verbose validation details"""
    console.print("[bold cyan]🔍 Validation Details:[ / bold cyan]")
    
    # Full validation table
    validation_table = Table(title="Validation Results", show_header=True)
    validation_table.add_column("Check", style="cyan")
    validation_table.add_column("Result", style="white")
    
    for key, value in result.items():
        if key not in ["issues", "suggestions", "timestamp"]:
            validation_table.add_row(str(key).replace("_", " ").title(), str(value))
    
    console.print(validation_table)
    console.print()

def display_dalle_progress(operation: str, current: int = 0, total: int = 1):
    """
    Display progress for DALL-E operations
    
    Args:
        operation: Operation being performed
        current: Current progress
        total: Total items to process
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task(f"🎨 {operation}...", total=total)
        progress.update(task, completed=current)

def display_dalle_capabilities(capabilities: Dict[str, Any], verbose: bool = False):
    """
    Display DALL-E capabilities and limitations
    
    Args:
        capabilities: Capabilities information
        verbose: Whether to show detailed information
    """
    console.print(Panel.fit(
        f"🎨 [bold green]DALL-E Capabilities[ / bold green]",
        style="green"
    ))
    
    # Operations
    operations = capabilities.get("operations", [])
    if operations:
        console.print("[bold cyan]🔧 Available Operations:[ / bold cyan]")
        for op in operations:
            console.print(f"  • {op}")
        console.print()
    
    # Models and features
    models = capabilities.get("supported_models", [])
    features = capabilities.get("features", [])
    
    if models:
        console.print(f"[bold cyan]🤖 Supported Models:[ / bold cyan] {', '.join(models)}")
    
    if features:
        console.print(f"[bold cyan]✨ Features:[ / bold cyan] {', '.join(features)}")
    
    console.print()
    
    # Limitations
    limitations = capabilities.get("limitations", {})
    if limitations:
        console.print("[bold yellow]⚠️  Limitations:[ / bold yellow]")
        for key, value in limitations.items():
            console.print(f"  • {key.replace('_', ' '.title()}: {value}")
        console.print()
    
    # Verbose details
    if verbose:
        console.print("[bold cyan]🔍 Detailed Specifications:[ / bold cyan]")
        
        # Sizes and qualities
        sizes = capabilities.get("supported_sizes", [])
        qualities = capabilities.get("supported_qualities", [])
        styles = capabilities.get("supported_styles", [])
        
        specs_table = Table(show_header=True)
        specs_table.add_column("Specification", style="cyan")
        specs_table.add_column("Options", style="white")
        
        specs_table.add_row("Image Sizes", ", ".join(sizes))
        specs_table.add_row("Quality Levels", ", ".join(qualities))
        specs_table.add_row("Style Options", ", ".join(styles))
        
        console.print(specs_table)
        console.print()
        
        # Cost structure
        cost_structure = capabilities.get("cost_structure", {})
        if cost_structure:
            console.print("[bold cyan]💰 Cost Structure:[ / bold cyan]")
            costs = cost_structure.get("size_quality_costs", {})
            
            cost_table = Table(show_header=True)
            cost_table.add_column("Size & Quality", style="cyan")
            cost_table.add_column("Cost (USD)", style="white")
            
            for size_quality, cost in costs.items():
                cost_table.add_row(size_quality.replace("_", " "), f"${cost:.3f}")
            
            console.print(cost_table)

def display_agent_handoff_dalle(result: Dict[str, Any], target_agent: str = "OC"):
    """
    Display DALL-E results formatted for agent-to-agent handoff
    
    Args:
        result: DALL-E operation result
        target_agent: Target agent receiving the handoff
    """
    console.print(Panel.fit(
        f"🤝 [bold green]Handoff to {target_agent}[ / bold green]",
        style="green"
    ))
    
    if result.get("error"):
        console.print(f"[red]❌ DALL-E Error:[ / red] {result['error']}")
        return
    
    operation = result.get("operation", "dalle_operation")
    
    if operation == "dalle_image_generation":
        generated_images = result.get("generated_images", [])
        metadata = result.get("metadata", {})
        
        console.print(f"[bold cyan]🎨 Generated {len(generated_images)} image(s)[ / bold cyan]")
        console.print(f"Model: {metadata.get('model', 'Unknown'}")
        console.print(f"Size: {metadata.get('size', 'Unknown'}")
        console.print(f"Cost: ${metadata.get('actual_cost', 0):.3f}")
        
        if generated_images:
            console.print(r"\n[bold cyan]📁 Image Files:[") / "bold cyan]")
            for i, image in enumerate(generated_images, 1):
                console.print(f"  {i}. {image['filename']} ({image['size_bytes']:,} bytes)")
    
    elif operation == "dalle_prompt_enhancement":
        console.print(f"[bold cyan]✨ Enhanced prompt ready[ / bold cyan]")
        console.print(f"Length: {len(result.get('enhanced_prompt', '')} characters")
        console.print(f"Approach: {result.get('enhancement_approach', 'Unknown'}")
    
    elif operation == "dalle_batch_generation":
        summary = result.get("summary", {})
        console.print(f"[bold cyan]🎨 Batch generation complete[ / bold cyan]")
        console.print(f"Successful: {summary.get('successful', 0)}")
        console.print(f"Failed: {summary.get('failed', 0)}")
        console.print(f"Total Cost: ${summary.get('total_cost', 0):.3f}")
    
    console.print()