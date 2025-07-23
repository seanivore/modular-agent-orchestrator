"""
GRAPHIC DESIGN TOOL
Human Button Generator - Standardized Single Entry Point
"""

from typing import Dict, Any, Optional
from tools.graphic_design.graphic_design import (
    analyze_image, edit_image, optimize_image, get_curated_fonts, estimate_cost
)


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for graphic design operations
    
    Args:
        params: Operation parameters including operation type and specific params
        model: Target model for code generation
        
    Returns:
        Self-contained executable code snippet
    """
    operation = params.get("operation", "analyze")
    
    if operation == "analyze":
        return _create_analysis_snippet(params, model)
    elif operation == "edit":
        return _create_editing_snippet(params, model)
    elif operation == "optimize":
        return _create_optimization_snippet(params, model)
    elif operation == "fonts":
        return _create_font_info_snippet(params, model)
    else:
        return _create_analysis_snippet(params, model)  # Default


def _create_analysis_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate AI-powered image analysis snippet"""
    image_path = params.get("image_path", "")
    analysis_approach = params.get("analysis_approach", "comprehensive")
    
    # Model-specific API formatting
    if "claude" in model.lower() or "anthropic" in model.lower():
        api_client = "anthropic"
        client_init = "client = anthropic.Anthropic()"
        model_param = f'model="{model}"'
        message_format = """messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image / jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": analysis_prompt
                }
            ]
        }]"""
        response_access = "response.content[0].text"
    
    elif "gpt" in model.lower() or "openai" in model.lower():
        api_client = "openai"
        client_init = "client = openai.OpenAI()"
        model_param = f'model="{model}"'
        message_format = """messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image / jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": analysis_prompt
                    }
                ]
            }
        ]"""
        response_access = "response.choices[0].message.content"
    
    else:
        # Generic format
        api_client = "anthropic"
        client_init = "client = anthropic.Anthropic()"
        model_param = f'model="{model}"'
        message_format = """messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image / jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": analysis_prompt
                }
            ]
        }]"""
        response_access = "response.content[0].text"
    
    return f'''
# AI-Powered Image Analysis - Professional Graphic Design
import {api_client}
import base64
import os
from datetime import datetime

def encode_image(image_path):
    """Encode image to base64 for API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Configuration
image_path = "{image_path}"
analysis_approach = "{analysis_approach}"

print("🖼️ AI-Powered Image Analysis")
print(f"📁 Image: {{image_path}}")
print(f"🎯 Approach: {{analysis_approach}}")
print("="*60)

try:
    # Validate image file
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {{image_path}}")
        exit(1)
    
    # Initialize AI client
    {client_init}
    
    # Encode image
    print("📷 Encoding image...")
    image_data = encode_image(image_path)
    
    # Create analysis prompt based on approach
    analysis_prompt = f"""Please provide a {{analysis_approach}} analysis of this image focusing on:

COMPOSITION & DESIGN:
- Visual balance and focal points
- Color harmony and mood
- Lighting and contrast quality
- Overall artistic composition
- Rule of thirds and visual flow

CONTENT ANALYSIS:
- Key subjects and elements
- Text visibility and readability (if any)
- Background / foreground relationship
- Visual hierarchy and emphasis
- Emotional impact and messaging

TECHNICAL ASSESSMENT:
- Image quality and sharpness
- Resolution and sizing appropriateness
- Format optimization potential
- Cropping or framing suggestions
- Color space and saturation

PROFESSIONAL RECOMMENDATIONS:
- How to enhance visual impact
- Text placement suggestions if adding overlay
- Color adjustments for better appeal
- Format recommendations for intended use
- Specific editing workflow suggestions

GRAPHIC DESIGN PERSPECTIVE:
- Typography considerations (if text present)
- Brand consistency potential
- Target audience appropriateness
- Platform optimization (web, print, social)
- Professional quality assessment

Be specific, actionable, and professional in your analysis. Focus on practical improvements that can be implemented."""
    
    # Make API call
    print("🤖 Analyzing with AI...")
    response = {api_client}.messages.create(
        {model_param},
        max_tokens=4000,
        {message_format}
    )
    
    # Extract and display analysis
    analysis_result = {response_access}
    
    print(Path(r"\\n") + "="*60)
    print("🎨 PROFESSIONAL IMAGE ANALYSIS")
    print("="*60)
    print(analysis_result)
    
    # Save analysis to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    analysis_file = f"image_analysis_{{timestamp}}.md"
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(f"# Professional Image Analysis\\n")
        f.write(f"**File:** {{image_path}}\\n")
        f.write(f"**Analysis Approach:** {{analysis_approach}}\\n")
        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%SPath(r')}}\\n"))
        f.write(f"**Model:** {model}\\n\\n")
        f.write(Path(r"## Analysis Results\\n\\n"))
        f.write(analysis_result)
        f.write(Path(r"\\n\\n---\\n*Generated by MAO Graphic Design Tool*"))
    
    print(Path(r"\\n") + "="*60)
    print("✅ Analysis completed successfully!")
    print(f"💾 Detailed analysis saved to: {{analysis_file}}")
    print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
    
except Exception as e:
    print(f"❌ Analysis failed: {{str(e)}}")
    print("💡 Ensure image file exists and is a supported format (JPEG, PNG, WebP)")
'''


def _create_editing_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate professional image editing snippet using logic file functions"""
    image_path = params.get("image_path", "")
    output_path = params.get("output_path", "None")
    output_format = params.get("output_format", "webp")
    
    resize = params.get("resize", False)
    width = params.get("width", 1200)
    maintain_aspect_ratio = params.get("maintain_aspect_ratio", True)
    
    crop = params.get("crop", False)
    crop_method = params.get("crop_method", "coordinates")
    x = params.get("x", None)
    y = params.get("y", None)
    crop_width = params.get("crop_width", None)
    crop_height = params.get("crop_height", None)
    aspect_ratio = params.get("aspect_ratio", None)
    focus = params.get("focus", "center")
    
    add_text = params.get("add_text", False)
    text = params.get("text", "")
    font = params.get("font", "Open Sans")
    font_size = params.get("font_size", None)
    text_position = params.get("text_position", "center")
    shade_opacity = params.get("shade_opacity", 30)
    
    return f'''
# Professional Image Editing - Using MAO Logic Functions
import json
from tools.graphic_design.graphic_design import edit_image, estimate_cost

def execute_professional_editing():
    """Execute professional image editing using MAO logic functions"""
    
    # Configuration
    params = {{
        "image_path": "{image_path}",
        "output_path": {output_path},
        "output_format": "{output_format}",
        "resize": {resize},
        "width": {width},
        "maintain_aspect_ratio": {maintain_aspect_ratio},
        "crop": {crop},
        "crop_method": "{crop_method}",
        "x": {x},
        "y": {y},
        "crop_width": {crop_width},
        "crop_height": {crop_height},
        "aspect_ratio": {f'"{aspect_ratio}"' if aspect_ratio else "None"},
        "focus": "{focus}",
        "add_text": {add_text},
        "text": "{text}",
        "font": "{font}",
        "font_size": {font_size},
        "text_position": "{text_position}",
        "shade_opacity": {shade_opacity}
    }}
    
    print("🎨 Professional Image Editing - 5-Step Workflow")
    print(f"📁 Source: {{params['image_path']}}")
    print("🎯 Philosophy: Only perfect pictures created")
    print("="*60)
    
    try:
        # Use MAO logic function for editing
        result = edit_image(**params)
        
        if "error" in result:
            print(f"❌ Editing failed: {{result['error']}}")
            return
        
        # Display results
        print(Path(r"\\n") + "="*60)
        print("🎨 PROFESSIONAL EDITING COMPLETE")
        print("="*60)
        
        print(f"📁 Input: {{result.get('input_path', 'Unknown')}}")
        print(f"📁 Output: {{result.get('output_path', 'Unknown')}}")
        
        operations = result.get("operations", [])
        if operations:
            print(f"🛠️ Operations: {{', '.join(operations)}}")
        
        specs = result.get("technical_specs", {{}})
        if specs:
            orig_dims = specs.get("original_dimensions", {{}})
            final_dims = specs.get("final_dimensions", {{}})
            if orig_dims and final_dims:
                print(f"📐 Dimensions: {{orig_dims.get('width')}}×{{orig_dims.get('height')}} → {{final_dims.get('width')}}×{{final_dims.get('height')}}")
        
        text_info = result.get("text_overlay", {{}})
        if text_info.get("applied"):
            print(f"✨ Text: '{{text_info.get('text')}}' using {{text_info.get('font_used')}}")
        
        print("✅ Professional quality workflow completed!")
        print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        
        # Save result details
        with open("editing_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print("💾 Detailed results saved to editing_results.json")
        
    except Exception as e:
        print(f"❌ Editing failed: {{str(e)}}")
        print("💡 Ensure image file exists and parameters are valid")

# Execute editing
execute_professional_editing()
'''


def _create_optimization_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate image optimization snippet using logic file functions"""
    image_path = params.get("image_path", "")
    quality = params.get("quality", 85)
    target_format = params.get("target_format", "webp")
    
    return f'''
# Professional Image Optimization - Using MAO Logic Functions
import json
from tools.graphic_design.graphic_design import optimize_image, estimate_cost

def execute_optimization():
    """Execute professional image optimization using MAO logic functions"""
    
    # Configuration
    params = {{
        "image_path": "{image_path}",
        "quality": {quality},
        "target_format": "{target_format}"
    }}
    
    print("🔧 Professional Image Optimization")
    print(f"📁 Source: {{params['image_path']}}")
    print(f"🎯 Quality: {{params['quality']}}%")
    print(f"📦 Target Format: {{params['target_format'].upper()}}")
    print("="*60)
    
    try:
        # Use MAO logic function for optimization
        result = optimize_image(**params)
        
        if "error" in result:
            print(f"❌ Optimization failed: {{result['error']}}")
            return
        
        # Display results
        print(Path(r"\\n") + "="*60)
        print("🔧 OPTIMIZATION COMPLETE")
        print("="*60)
        
        print(f"📁 Input: {{result.get('input_path', 'Unknown')}}")
        print(f"📁 Output: {{result.get('output_path', 'Unknown')}}")
        
        opt_results = result.get("optimization_results", {{}})
        if opt_results:
            original_size = opt_results.get("original_size_bytes", 0)
            optimized_size = opt_results.get("optimized_size_bytes", 0)
            reduction = opt_results.get("size_reduction_percent", 0)
            
            print(f"📊 Size Reduction: {{reduction:.1f}}%")
            print(f"📦 Format: {{opt_results.get('format_conversion', 'Unknown')}}")
            print(f"💾 Original: {{original_size:,}} bytes")
            print(f"💾 Optimized: {{optimized_size:,}} bytes")
        
        print("✅ Professional optimization completed!")
        print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        
        # Save result details
        with open("optimization_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print("💾 Detailed results saved to optimization_results.json")
        
    except Exception as e:
        print(f"❌ Optimization failed: {{str(e)}}")
        print("💡 Ensure image file exists and parameters are valid")

# Execute optimization
execute_optimization()
'''


def _create_font_info_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate font collection info snippet using logic file functions"""
    return '''
# Curated Font Collection - Using MAO Logic Functions
import json
from tools.graphic_design.graphic_design import get_curated_fonts, estimate_cost
from pathlib import Path

def display_font_collection():
    """Display professional font collection using MAO logic functions"""
    
    print("🎨 Professional Font Collection")
    print("MAO Graphic Design Tool")
    print("="*60)
    
    try:
        # Use MAO logic function for font info
        result = get_curated_fonts()
        
        if "error" in result:
            print(f"❌ Font collection error: {result['error']}")
            return
        
        fonts = result.get("curated_fonts", {})
        
        # Display each font
        for font_name, font_info in fonts.items():
            print(f"🔤 {font_name}")
            print(f"   Style: {font_info.get('style', 'Unknown')}")
            print(f"   Best For: {font_info.get('use_case', 'General use')}")
            print(f"   File: {font_info.get('file', 'Unknown')}")
            print()
        
        print("🔄 Features:")
        print("   • Automatic font fallback system")
        print("   • Smart font size calculation (5% of image width)")
        print("   • Professional text overlay with shade layer")
        print("   • Cross-platform compatibility")
        print()
        
        print("💡 Professional Typography Tips:")
        print("   • Use Bebas Neue for bold impact headlines")
        print("   • Choose Georgia for traditional elegance")
        print("   • Open Sans works great for general text")
        print("   • Montserrat for modern, clean designs")
        print("   • Playfair Display for luxury branding")
        print()
        
        print("✨ All fonts include automatic readability enhancements")
        print(f"💰 Font usage cost: FREE")
        
        # Save font details
        with open("font_collection.json", "w") as f:
            json.dump(result, f, indent=2)
        print("💾 Font details saved to font_collection.json")
        
    except Exception as e:
        print(f"❌ Font collection display failed: {str(e)}")
        print("💡 Ensure MAO graphic design module is properly installed")

# Display font collection
display_font_collection()
'''
