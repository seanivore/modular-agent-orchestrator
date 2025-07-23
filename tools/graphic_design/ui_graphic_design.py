"""
GRAPHIC DESIGN TOOL
UI Display Component
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from pathlib import Path

console = Console()


def display_graphic_design_result(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display Graphic Design operation results with beautiful formatting
    
    Args:
        result: Result from graphic design operations
        verbose: Whether to show detailed information
    """
    if result.get("error"):
        display_error(result.get("error", "Unknown error"))
        return
    
    # Determine operation type based on result content
    if "technical_specs" in result and "operations" not in result:
        display_analysis_results(result, verbose)
    elif "operations" in result:
        display_editing_results(result, verbose)
    elif "optimization_results" in result:
        display_optimization_results(result, verbose)
    elif "curated_fonts" in result:
        display_font_collection(result, verbose)
    else:
        # Generic display for other operations
        console.print("🎨 Graphic Design Operation Completed", style="bold green")
        if verbose:
            for key, value in result.items():
                if key != "error":
                    console.print(f"  {key}: {value}")


def display_error(error_msg: str) -> None:
    """Display error with consistent formatting"""
    panel = Panel(
        f"❌ Error: {error_msg}",
        title="Graphic Design Error",
        border_style="red"
    )
    console.print(panel)


def display_analysis_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display image analysis results with beautiful terminal output
    
    Args:
        result: Analysis result data from graphic_design tool
        verbose: Show detailed technical information
    """
    # Handle error cases
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    # Main analysis display
    image_path = result.get("image_path", "Unknown image")
    analysis_approach = result.get("analysis_approach", "Unknown approach")
    specs = result.get("technical_specs", {})
    optimization = result.get("optimization_potential", {})
    
    # Header
    if verbose:
        header_text = f"🖼️ Image Analysis: {analysis_approach}"
        console.print(Panel(header_text, style="blue"))
        console.print(f"📁 File: {image_path}", style="dim")
    else:
        console.print(f"🖼️ Analyzed: {image_path.split(' / ')[-1]}", style="blue bold")
    
    # Technical specifications table
    if specs:
        table = Table(show_header=True, header_style="bold magenta", title="Technical Specifications")
        table.add_column("Property", style="bold")
        table.add_column("Value", style="cyan")
        
        dims = specs.get("dimensions", {})
        if dims:
            table.add_row("Dimensions", f"{dims.get('width', 0)} × {dims.get('height', 0)} pixels")
        
        table.add_row("Format", specs.get("format", "Unknown"))
        table.add_row("Color Mode", specs.get("mode", "Unknown"))
        table.add_row("File Size", f"{specs.get('file_size_bytes', 0):,} bytes")
        table.add_row("Aspect Ratio", str(specs.get("aspect_ratio", "Unknown")))
        table.add_row("Megapixels", f"{specs.get('megapixels', 0):.1f} MP")
        
        console.print(table)
    
    # Optimization recommendations
    if optimization and verbose:
        console.print(Path(r"\n📊 Optimization Recommendations:"), style="bold yellow")
        
        if optimization.get("resize_recommended"):
            console.print("   📐 Resize recommended (large dimensions)", style="yellow")
        
        if optimization.get("format_optimization"):
            console.print("   📦 Format optimization available (consider WebP)", style="yellow")
        
        if optimization.get("compression_potential"):
            console.print("   🗜️ Compression potential detected", style="yellow")
    
    # AI analysis note
    metadata = result.get("metadata", {})
    if metadata.get("requires_ai_analysis"):
        console.print(Path(r"\n💡 For detailed composition analysis, use the AI-powered human button"), style="green")


def display_editing_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display image editing results with professional formatting
    
    Args:
        result: Editing result data from graphic_design tool
        verbose: Show detailed technical information
    """
    # Handle error cases
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    # Success header
    input_path = result.get("input_path", "Unknown input")
    output_path = result.get("output_path", "Unknown output")
    operations = result.get("operations", [])
    
    if verbose:
        header_text = f"🎨 Professional Image Editing Complete"
        console.print(Panel(header_text, style="green"))
    else:
        console.print("🎨 Image editing completed successfully!", style="green bold")
    
    # File paths
    console.print(f"📁 Input:  {input_path}", style="dim")
    console.print(f"📁 Output: {output_path}", style="cyan")
    
    # Operations performed
    if operations:
        console.print(fPath(r"\n🛠️ Operations: {'), '.join(operations)}", style="blue")
    
    # Technical specifications
    specs = result.get("technical_specs", {})
    if specs and verbose:
        table = Table(show_header=True, header_style="bold magenta", title="Processing Details")
        table.add_column("Stage", style="bold")
        table.add_column("Dimensions", style="cyan")
        table.add_column("Format", style="yellow")
        
        orig_dims = specs.get("original_dimensions", {})
        final_dims = specs.get("final_dimensions", {})
        
        table.add_row(
            "Original",
            f"{orig_dims.get('width', 0)} × {orig_dims.get('height', 0)}",
            specs.get("original_format", "Unknown")
        )
        table.add_row(
            "Final",
            f"{final_dims.get('width', 0)} × {final_dims.get('height', 0)}",
            specs.get("output_format", "Unknown")
        )
        
        console.print(table)
    
    # Text overlay details
    text_info = result.get("text_overlay", {})
    if text_info.get("applied") and verbose:
        console.print(Path(r"\n✨ Text Overlay Details:"), style="bold")
        console.print(f"   Text: '{text_info.get('text', 'Unknown')}'", style="white")
        console.print(f"   Font: {text_info.get('font_used', 'Unknown')}", style="cyan")
        console.print(f"   Position: {text_info.get('position', 'Unknown')}", style="dim")
    
    # Professional quality indicator
    metadata = result.get("metadata", {})
    if metadata.get("professional_quality"):
        console.print(Path(r"\n✅ Professional quality workflow completed"), style="green")


def display_optimization_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display image optimization results
    
    Args:
        result: Optimization result data from graphic_design tool
        verbose: Show detailed technical information
    """
    # Handle error cases
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    # Success header
    input_path = result.get("input_path", "Unknown input")
    output_path = result.get("output_path", "Unknown output")
    
    console.print("🔧 Image optimization completed!", style="green bold")
    console.print(f"📁 Optimized: {output_path}", style="cyan")
    
    # Optimization results
    opt_results = result.get("optimization_results", {})
    if opt_results:
        # Size comparison
        original_size = opt_results.get("original_size_bytes", 0)
        optimized_size = opt_results.get("optimized_size_bytes", 0)
        reduction = opt_results.get("size_reduction_percent", 0)
        
        console.print(f"\n📊 Size Reduction: {reduction:.1f}%", style="yellow bold")
        
        if verbose:
            table = Table(show_header=True, header_style="bold magenta", title="Optimization Details")
            table.add_column("Metric", style="bold")
            table.add_column("Before", style="red")
            table.add_column("After", style="green")
            
            table.add_row("File Size", f"{original_size:,} bytes", f"{optimized_size:,} bytes")
            table.add_row("Format", 
                         opt_results.get("format_conversion", "Unknown").split(" → ")[0],
                         opt_results.get("format_conversion", "Unknown").split(" → ")[-1])
            table.add_row("Quality", "Original", f"{opt_results.get('quality_setting', 0)}%")
            
            console.print(table)
        else:
            console.print(f"   Original: {original_size:,} bytes", style="red")
            console.print(f"   Optimized: {optimized_size:,} bytes", style="green")


def display_font_collection(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display curated font collection information
    
    Args:
        result: Font collection data from graphic_design tool
        verbose: Show detailed font information
    """
    # Handle error cases
    if "error" in result:
        display_error(result.get("error", "Unknown error"))
        return
    
    console.print("🎨 Curated Font Collection", style="blue bold")
    
    fonts = result.get("curated_fonts", {})
    if fonts:
        if verbose:
            # Detailed font table
            table = Table(show_header=True, header_style="bold magenta", title="Professional Typography")
            table.add_column("Font Name", style="bold")
            table.add_column("Style", style="cyan")
            table.add_column("Best For", style="yellow")
            table.add_column("File", style="dim")
            
            for font_name, font_info in fonts.items():
                table.add_row(
                    font_name,
                    font_info.get("style", "Unknown"),
                    font_info.get("use_case", "General use"),
                    font_info.get("file", "Unknown")
                )
            
            console.print(table)
        else:
            # Simple font list
            font_names = list(fonts.keys())
            console.print(f"📚 Available fonts: {', '.join(font_names)}", style="cyan")
    
    # Directory info
    fonts_dir = result.get("fonts_directory", "Unknown")
    fallback = result.get("fallback_available", False)
    
    if verbose:
        console.print(f"\n📁 Font Directory: {fonts_dir}", style="dim")
        console.print(f"🔄 System Fallback: {'Available' if fallback else 'Not available'}", style="dim")


def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for graphic design operations"""
    
    if cost == 0:
        console.print("💰 Cost: FREE", style="green bold")
    else:
        console.print(f"💰 Estimated cost: ${cost:.4f}", style="yellow")
    
    if verbose:
        console.print("   Professional image processing with curated workflows", style="dim")


def format_for_agent_handoff(results: Dict[str, Any]) -> str:
    """Format graphic design results for agent-to-agent handoff"""
    if "error" in results:
        return f"Graphic design operation failed: {results['error']}"
    
    # Determine operation type
    if "operations" in results:
        # Editing results
        input_path = results.get("input_path", "Unknown input")
        output_path = results.get("output_path", "Unknown output")
        operations = results.get("operations", [])
        
        formatted_results = [f"Image editing completed for: {input_path}"]
        formatted_results.append(f"Output saved to: {output_path}")
        
        if operations:
            formatted_results.append(f"Operations performed: {', '.join(operations)}")
        
        # Technical specs
        specs = results.get("technical_specs", {})
        if specs:
            orig_dims = specs.get("original_dimensions", {})
            final_dims = specs.get("final_dimensions", {})
            if orig_dims and final_dims:
                formatted_results.append(f"Dimensions: {orig_dims.get('width')}×{orig_dims.get('height')} → {final_dims.get('width')}×{final_dims.get('height')}")
        
        # Text overlay info
        text_info = results.get("text_overlay", {})
        if text_info.get("applied"):
            formatted_results.append(f"Text added: '{text_info.get('text')}' using {text_info.get('font_used')}")
        
        return Path(r"\n").join(formatted_results)
    
    elif "optimization_results" in results:
        # Optimization results
        input_path = results.get("input_path", "Unknown input")
        output_path = results.get("output_path", "Unknown output")
        opt_results = results.get("optimization_results", {})
        
        formatted_results = [f"Image optimization completed for: {input_path}"]
        formatted_results.append(f"Optimized file: {output_path}")
        
        if opt_results:
            reduction = opt_results.get("size_reduction_percent", 0)
            formatted_results.append(f"Size reduction: {reduction:.1f}%")
            
            format_conversion = opt_results.get("format_conversion", "")
            if format_conversion:
                formatted_results.append(f"Format: {format_conversion}")
        
        return Path(r"\n").join(formatted_results)
    
    elif "technical_specs" in results:
        # Analysis results
        image_path = results.get("image_path", "Unknown image")
        specs = results.get("technical_specs", {})
        
        formatted_results = [f"Image analysis completed for: {image_path}"]
        
        if specs:
            dims = specs.get("dimensions", {})
            if dims:
                formatted_results.append(f"Dimensions: {dims.get('width')}×{dims.get('height')} pixels")
            
            formatted_results.append(f"Format: {specs.get('format', 'Unknown')}")
            formatted_results.append(f"File size: {specs.get('file_size_bytes', 0):,} bytes")
        
        return Path(r"\n").join(formatted_results)
    
    else:
        return "Graphic design operation completed successfully"


def display_workflow_guide(verbose: bool = False) -> None:
    """Display the professional 5-step workflow guide"""
    
    console.print("🎨 Professional Image Editing Workflow", style="blue bold")
    
    if verbose:
        workflow_steps = [
            ("1. Assess", "Analyze image composition, quality, and optimization potential"),
            ("2. Resize", "Scale to appropriate dimensions (typically 900-1200px width)"),
            ("3. Crop", "Apply smart cropping with composition focus"),
            ("4. Text", "Add professional text overlay with shade layer"),
            ("5. Save", "Export in optimized format (WebP recommended)")
        ]
        
        table = Table(show_header=True, header_style="bold magenta", title="5-Step Professional Workflow")
        table.add_column("Step", style="bold cyan")
        table.add_column("Description", style="white")
        
        for step, description in workflow_steps:
            table.add_row(step, description)
        
        console.print(table)
        
        console.print(Path(r"\n💡 Pro Tip: Always analyze before and after editing to assess composition and readability"), style="green")
    else:
        console.print("📋 5-Step Process: Assess → Resize → Crop → Text → Save", style="cyan")
        console.print("💡 Use analyze_image before and after editing for best results", style="green") 