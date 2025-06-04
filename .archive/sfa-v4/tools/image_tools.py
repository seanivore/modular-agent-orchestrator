"""
Image Tools
Sophisticated image analysis & artistic editing with curated workflow
"""

import json
import base64
import os
from typing import Dict, Any, List, Optional, Union
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "image_tools",
        "name": "Image Analysis & Artistic Editing",
        "description": "Analyze images and perform professional artistic editing",
        "capabilities": ["image_analysis", "artistic_editing", "visual_optimization"],
        "use_cases": ["image analysis", "professional photo editing", "text overlay design", "social media optimization"],
        "cost_estimate": 0.05,  # Estimated per operation
        "model_compatibility": ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-sonnet-4"],
        "tags": ["media", "visual", "analysis", "artistic"],
        "functions": [
            "analyze_image",
            "edit_image",
            "optimize_image"
        ],
        "fonts_included": ["Bebas Neue", "Georgia", "Open Sans", "Montserrat", "Playfair Display"]
    }

def analyze_image(image_path: str, analysis_type: str = "comprehensive") -> str:
    """
    Analyze an image using AI vision capabilities
    This is a placeholder - actual implementation via human button
    """
    return f"""
🖼️ Image Analysis: {analysis_type}
📁 File: {image_path}
⏰ Started: {datetime.now().strftime('%H:%M:%S')}

🎯 Analysis Framework:
- Visual content description
- Key elements and composition
- Colors and artistic quality
- Text readability assessment
- Technical details and optimization potential
- Professional recommendations

Note: Execute the human button snippet for actual AI-powered image analysis.
"""

def create_analyze_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate executable snippet for image analysis"""
    image_path = params.get("image_path", "")
    analysis_type = params.get("analysis_type", "comprehensive")
    
    return f'''
# AI-Powered Image Analysis
import anthropic
import base64

def encode_image(image_path):
    """Encode image to base64 for API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Initialize client
client = anthropic.Anthropic()

image_path = "{image_path}"
analysis_type = "{analysis_type}"

print(f"🖼️ Analyzing image: {{image_path}}")
print(f"🎯 Analysis type: {{analysis_type}}")
print("="*60)

try:
    # Encode image
    image_data = encode_image(image_path)
    
    # Analyze with AI
    response = client.messages.create(
        model="{model}",
        max_tokens=4000,
        messages=[{{
            "role": "user",
            "content": [
                {{
                    "type": "image",
                    "source": {{
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }}
                }},
                {{
                    "type": "text",
                    "text": f"""Please provide a {{analysis_type}} analysis of this image focusing on:

COMPOSITION & DESIGN:
- Visual balance and focal points
- Color harmony and mood
- Lighting and contrast quality
- Overall artistic composition

CONTENT ANALYSIS:
- Key subjects and elements
- Text visibility and readability
- Background/foreground relationship
- Any design improvements needed

TECHNICAL ASSESSMENT:
- Image quality and sharpness
- Resolution and sizing appropriateness
- Format optimization potential
- Cropping or framing suggestions

PROFESSIONAL RECOMMENDATIONS:
- How to enhance visual impact
- Text placement suggestions if adding overlay
- Color adjustments for better appeal
- Format recommendations for intended use

Be specific and actionable in your analysis."""
                }}
            ]
        }}]
    )
    
    # Display analysis
    analysis_result = response.content[0].text
    print(analysis_result)
    
    # Save analysis to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    analysis_file = f"image_analysis_{{timestamp}}.md"
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(f"# Image Analysis\\n")
        f.write(f"**File:** {{image_path}}\\n")
        f.write(f"**Analysis Type:** {{analysis_type}}\\n")
        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
        f.write(analysis_result)
    
    print("\\n" + "="*60)
    print("✅ Image analysis completed")
    print(f"💾 Analysis saved to: {{analysis_file}}")
    
except Exception as e:
    print(f"❌ Image analysis failed: {{str(e)}}")
    print("Note: Ensure image file exists and is a supported format (JPEG, PNG)")
'''

def edit_image(
    image_path: str,
    output_path: Optional[str] = None,
    output_format: str = "webp",
    
    # Resize
    resize: bool = False,
    width: int = 1200,
    maintain_aspect_ratio: bool = True,
    
    # Crop
    crop: bool = False,
    crop_method: str = "coordinates",
    x: Optional[int] = None,
    y: Optional[int] = None,
    crop_width: Optional[int] = None,
    crop_height: Optional[int] = None,
    aspect_ratio: Optional[str] = None,
    focus: str = "center",
    
    # Text
    add_text: bool = False,
    text: Optional[str] = None,
    font: str = "Open Sans",
    font_size: Optional[int] = None,
    text_position: str = "center",
    shade_opacity: int = 30
) -> str:
    """
    Artistically edit an image with professional workflow.
    
    This tool follows a creative workflow for perfect results:
    1. Assess the image - identify focus, imagine text placement, consider composition
    2. Resize to appropriate dimensions (typically 900-1200px width)
    3. Apply shade layer and add text, or crop the image first
    4. Finalize with any remaining operations
    5. Save in optimized format (webp recommended)
    
    NOTE: Always use analyze_image before and after editing to assess 
    composition and readability.
    """
    return f"""
🎨 Artistic Image Editing
📁 Source: {image_path}
🎯 Philosophy: Only perfect pictures created
⏰ Started: {datetime.now().strftime('%H:%M:%S')}

🛠️ Professional Operations Available:
- **Resize**: Smart scaling with aspect ratio preservation
- **Crop**: Coordinate-based or aspect ratio with focus points
- **Text Overlay**: Curated fonts with automatic shade layers
- **Format Optimization**: WebP default for best quality/size

📚 Curated Font Collection:
- **Bebas Neue**: Bold, modern impact
- **Georgia**: Classic serif elegance  
- **Open Sans**: Clean, readable sans-serif
- **Montserrat**: Modern geometric sans-serif
- **Playfair Display**: Elegant display serif

Note: Execute the human button snippet for professional image editing.
"""

def create_edit_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate executable snippet for artistic image editing"""
    
    # Extract all parameters with defaults
    image_path = params.get("image_path", "")
    output_path = params.get("output_path", "None")
    output_format = params.get("output_format", "webp")
    
    resize = params.get("resize", "False")
    width = params.get("width", 1200)
    maintain_aspect_ratio = params.get("maintain_aspect_ratio", "True")
    
    crop = params.get("crop", "False")
    crop_method = params.get("crop_method", "coordinates")
    x = params.get("x", "None")
    y = params.get("y", "None")
    crop_width = params.get("crop_width", "None")
    crop_height = params.get("crop_height", "None")
    aspect_ratio = params.get("aspect_ratio", "None")
    focus = params.get("focus", "center")
    
    add_text = params.get("add_text", "False")
    text = params.get("text", "")
    font = params.get("font", "Open Sans")
    font_size = params.get("font_size", "None")
    text_position = params.get("text_position", "center")
    shade_opacity = params.get("shade_opacity", 30)
    
    return f'''
# Professional Artistic Image Editing
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime

def edit_image_professionally():
    """Execute the sophisticated image editing workflow"""
    
    # Parameters
    image_path = "{image_path}"
    output_path = {output_path}
    output_format = "{output_format}"
    
    # Resize parameters
    resize = {resize}
    width = {width}
    maintain_aspect_ratio = {maintain_aspect_ratio}
    
    # Crop parameters  
    crop = {crop}
    crop_method = "{crop_method}"
    x = {x}
    y = {y}
    crop_width = {crop_width}
    crop_height = {crop_height}
    aspect_ratio = {f'"{aspect_ratio}"' if aspect_ratio != "None" else "None"}
    focus = "{focus}"
    
    # Text parameters
    add_text = {add_text}
    text = "{text}"
    font = "{font}"
    font_size = {font_size}
    text_position = "{text_position}"
    shade_opacity = {shade_opacity}
    
    print("🎨 Starting professional image editing...")
    print(f"📁 Source: {{image_path}}")
    print("="*60)
    
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {{image_path}}")
            return
            
        # Open the image
        img = Image.open(image_path)
        original_width, original_height = img.size
        original_format = img.format or "JPEG"
        
        print(f"📐 Original: {{original_width}}x{{original_height}} {{original_format}}")
        
        # Track operations
        operations = []
        current_img = img
        
        # STEP 1: RESIZE (Professional scaling)
        if resize:
            if width <= 0:
                print("❌ Width must be positive")
                return
                
            if width >= original_width:
                print("⚠️ Skipping resize - target larger than original")
                operations.append("resize_skipped")
            else:
                # Calculate height maintaining aspect ratio
                if maintain_aspect_ratio:
                    ratio = original_height / original_width
                    height = int(width * ratio)
                else:
                    height = original_height
                
                # Professional resize with LANCZOS
                current_img = current_img.resize((width, height), Image.LANCZOS)
                operations.append(f"resized_to_{{width}}x{{height}}")
                print(f"✅ Resized to {{width}}x{{height}}")
        
        # Get current dimensions
        current_width, current_height = current_img.size
        
        # STEP 2: CROP (Smart composition)
        if crop:
            if crop_method == "coordinates":
                if x is None or y is None or crop_width is None or crop_height is None:
                    print("❌ Coordinate cropping requires x, y, crop_width, crop_height")
                    return
                
                # Ensure crop box is within bounds
                x_val = max(0, min(x, current_width - 1))
                y_val = max(0, min(y, current_height - 1))
                width_val = max(1, min(crop_width, current_width - x_val))
                height_val = max(1, min(crop_height, current_height - y_val))
                
                crop_box = (x_val, y_val, x_val + width_val, y_val + height_val)
                current_img = current_img.crop(crop_box)
                operations.append(f"cropped_{{width_val}}x{{height_val}}")
                print(f"✅ Cropped to {{width_val}}x{{height_val}}")
                
            elif crop_method == "aspect_ratio":
                if not aspect_ratio:
                    print("❌ Aspect ratio cropping requires aspect_ratio parameter")
                    return
                
                try:
                    # Parse aspect ratio (e.g., "16:9")
                    parts = aspect_ratio.split(":")
                    target_width_ratio = int(parts[0])
                    target_height_ratio = int(parts[1])
                    target_ratio = target_width_ratio / target_height_ratio
                except:
                    print(f"❌ Invalid aspect ratio: {{aspect_ratio}}")
                    return
                
                current_ratio = current_width / current_height
                
                if current_ratio > target_ratio:
                    # Crop width
                    new_width = int(current_height * target_ratio)
                    new_height = current_height
                    
                    if focus == "left":
                        x_val = 0
                    elif focus == "right":
                        x_val = current_width - new_width
                    else:  # center
                        x_val = (current_width - new_width) // 2
                    y_val = 0
                else:
                    # Crop height
                    new_width = current_width
                    new_height = int(current_width / target_ratio)
                    
                    if focus == "top":
                        y_val = 0
                    elif focus == "bottom":
                        y_val = current_height - new_height
                    else:  # center
                        y_val = (current_height - new_height) // 2
                    x_val = 0
                
                crop_box = (x_val, y_val, x_val + new_width, y_val + new_height)
                current_img = current_img.crop(crop_box)
                operations.append(f"aspect_{{aspect_ratio.replace(':', 'x')}}")
                print(f"✅ Cropped to {{aspect_ratio}} ratio")
        
        # Update dimensions after crop
        current_width, current_height = current_img.size
        
        # STEP 3: TEXT OVERLAY (Professional typography)
        if add_text:
            if not text:
                print("❌ Text parameter required for text overlay")
                return
            
            # Convert to RGBA for text overlay
            if current_img.mode != 'RGBA':
                current_img = current_img.convert('RGBA')
            
            # SHADE LAYER - Ensures perfect text readability
            overlay = Image.new('RGBA', (current_width, current_height), 
                               (0, 0, 0, int(255 * shade_opacity / 100)))
            current_img = Image.alpha_composite(current_img, overlay)
            
            # FONT LOADING - Curated collection
            fonts_dir = "tools/fonts"  # Relative to project root
            if not os.path.exists(fonts_dir):
                fonts_dir = "../tools/fonts"  # Try parent directory
            
            font_files = {{
                "Bebas Neue": "BebasNeue-Regular.ttf",
                "Georgia": "Georgia-Regular.ttf", 
                "Open Sans": "OpenSans-Regular.ttf",
                "Montserrat": "Montserrat-Regular.ttf",
                "Playfair Display": "PlayfairDisplay-Regular.ttf"
            }}
            
            # Try to load curated font
            font_path = None
            if font in font_files and os.path.exists(fonts_dir):
                potential_path = os.path.join(fonts_dir, font_files[font])
                if os.path.exists(potential_path):
                    font_path = potential_path
            
            # FONT SIZE - Professional auto-sizing
            if font_size is None:
                font_size = int(current_width * 0.05)  # 5% of width
            
            # Load font
            try:
                if font_path:
                    pil_font = ImageFont.truetype(font_path, font_size)
                    print(f"✅ Loaded curated font: {{font}}")
                else:
                    # Fallback to system fonts
                    try:
                        pil_font = ImageFont.truetype("Arial.ttf", font_size)
                    except:
                        pil_font = ImageFont.load_default()
                        font_size = int(current_width * 0.03)
                    print("⚠️ Using fallback font")
            except Exception as e:
                print(f"❌ Font loading error: {{e}}")
                return
            
            # TEXT POSITIONING - Smart placement
            draw = ImageDraw.Draw(current_img)
            text_bbox = draw.textbbox((0, 0), text, font=pil_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if text_position == "center":
                x_pos = (current_width - text_width) // 2
                y_pos = (current_height - text_height) // 2
            elif text_position == "top":
                x_pos = (current_width - text_width) // 2
                y_pos = int(current_height * 0.1)
            elif text_position == "bottom":
                x_pos = (current_width - text_width) // 2
                y_pos = int(current_height * 0.9) - text_height
            else:
                # Default center
                x_pos = (current_width - text_width) // 2
                y_pos = (current_height - text_height) // 2
            
            # Draw text in white
            draw.text((x_pos, y_pos), text, fill=(255, 255, 255, 255), font=pil_font)
            operations.append("text_overlay")
            print(f"✅ Added text: '{{text}}' using {{font}}")
        
        # Convert back to RGB for saving
        if current_img.mode == 'RGBA':
            current_img = current_img.convert("RGB")
        
        # STEP 4: SMART OUTPUT PATH
        if not output_path:
            file_name, file_ext = os.path.splitext(image_path)
            
            # Build descriptive filename
            if operations:
                desc = "_".join(operations)
                base_name = f"{{file_name}}_{{desc}}"
            else:
                base_name = f"{{file_name}}_edited"
            
            # Use optimized format
            ext = f".{{output_format.lower()}}"
            if output_format.lower() in ["jpg", "jpeg"]:
                ext = ".jpg"
            output_path = f"{{base_name}}{{ext}}"
        
        # STEP 5: OPTIMIZED SAVING
        format_map = {{
            "jpg": "JPEG", "jpeg": "JPEG", 
            "png": "PNG", "webp": "WEBP"
        }}
        save_format = format_map.get(output_format.lower(), "WEBP")
        
        save_kwargs = {{"format": save_format}}
        if save_format == "JPEG":
            save_kwargs["quality"] = 95
        elif save_format == "WEBP":
            save_kwargs["quality"] = 90
        
        current_img.save(output_path, **save_kwargs)
        
        # SUCCESS REPORT
        final_width, final_height = current_img.size
        print("\\n" + "="*60)
        print("🎨 PROFESSIONAL EDITING COMPLETE")
        print(f"📁 Output: {{output_path}}")
        print(f"📐 Final: {{final_width}}x{{final_height}} {{save_format}}")
        print(f"🛠️ Operations: {{', '.join(operations) if operations else 'optimization'}}")
        print("✨ Perfect picture created!")
        
    except Exception as e:
        print(f"❌ Editing failed: {{str(e)}}")

# Execute the professional workflow
edit_image_professionally()
'''

def optimize_image(image_path: str, quality: int = 85, target_format: str = "webp") -> str:
    """Optimize image for web/storage with professional settings"""
    return f"""
🔧 Professional Image Optimization
📁 File: {image_path}
🎯 Target Quality: {quality}%
📦 Format: {target_format}

Use the human button snippet to optimize with professional settings.
"""

def create_optimization_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate snippet for professional image optimization"""
    image_path = params.get("image_path", "")
    quality = params.get("quality", 85)
    target_format = params.get("target_format", "webp")
    
    return f'''
# Professional Image Optimization
from PIL import Image
import os

image_path = "{image_path}"
quality = {quality}
target_format = "{target_format}"

print(f"🔧 Optimizing: {{image_path}}")
print(f"🎯 Quality: {{quality}}% | Format: {{target_format}}")
print("="*50)

try:
    # Get original stats
    original_size = os.path.getsize(image_path)
    print(f"📊 Original: {{original_size:,}} bytes")
    
    # Open and optimize
    with Image.open(image_path) as img:
        # Convert mode if needed for target format
        if target_format.lower() in ["jpg", "jpeg"] and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Generate optimized filename
        name, ext = os.path.splitext(image_path)
        output_path = f"{{name}}_optimized.{{target_format.lower()}}"
        
        # Save with professional settings
        save_kwargs = {{"optimize": True}}
        
        if target_format.lower() in ["jpg", "jpeg"]:
            save_kwargs.update({{"format": "JPEG", "quality": quality}})
        elif target_format.lower() == "webp":
            save_kwargs.update({{"format": "WEBP", "quality": quality}})
        elif target_format.lower() == "png":
            save_kwargs.update({{"format": "PNG", "compress_level": 9}})
        
        img.save(output_path, **save_kwargs)
        
        # Calculate savings
        new_size = os.path.getsize(output_path)
        savings = original_size - new_size
        savings_percent = (savings / original_size) * 100
        
        print(f"📊 Optimized: {{new_size:,}} bytes")
        print(f"💾 Saved: {{savings:,}} bytes ({{savings_percent:.1f}}%)")
        print(f"✅ Output: {{output_path}}")
        
except Exception as e:
    print(f"❌ Optimization failed: {{str(e)}}")
'''

# Tool registration for OC discovery
TOOL_DEFINITION = get_tool_definition()

# Available image functions
IMAGE_FUNCTIONS = {
    "analyze_image": analyze_image,
    "edit_image": edit_image,
    "optimize_image": optimize_image
}

"""
PULL FROM OLD SFA: 
"""

# SFA v4.0.0 Enhanced Tools - Complete Implementation
# Extracted best patterns from v3.3.0 and enhanced for v4 architecture

# =============================================================================
# ENHANCED IMAGE TOOLS
# =============================================================================

"""
Enhanced SFA v4 Image Tools with professional workflow and error recovery
"""

def get_enhanced_image_definition() -> Dict[str, Any]:
    """Enhanced image tools definition"""
    return {
        "id": "image_tools_enhanced",
        "name": "Professional Image Suite",
        "description": "AI-powered image analysis and professional editing with error recovery",
        "capabilities": ["image_analysis", "artistic_editing", "visual_optimization", "error_recovery"],
        "use_cases": ["image analysis", "professional editing", "social media optimization", "brand visuals"],
        "cost_estimate": 0.05,
        "model_compatibility": ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-sonnet-4"],
        "tags": ["media", "visual", "analysis", "artistic", "professional"],
        "functions": ["analyze_image", "edit_image", "optimize_image", "batch_process"],
        "fonts_included": ["Bebas Neue", "Georgia", "Open Sans", "Montserrat", "Playfair Display"]
    }

def create_enhanced_image_snippet(operation: str, params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate enhanced image processing snippets with error recovery"""
    
    if operation == "analyze_image":
        image_path = params.get("image_path", "")
        analysis_type = params.get("analysis_type", "comprehensive")
        
        return f'''
# Enhanced AI Image Analysis with Error Recovery
import anthropic
import base64
import os
from pathlib import Path
from PIL import Image
import json
from datetime import datetime

def enhanced_image_analysis():
    """Analyze image with comprehensive error handling and validation"""
    
    image_path = "{image_path}"
    analysis_type = "{analysis_type}"
    
    print(f"🖼️ Analyzing: {{Path(image_path).name}}")
    print(f"🎯 Analysis: {{analysis_type}}")
    print("="*60)
    
    try:
        # Validate image file
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {{image_path}}")
            return None
        
        # Check file size (limit to 20MB for API)
        file_size = os.path.getsize(image_path)
        max_size = 20 * 1024 * 1024  # 20MB
        
        if file_size > max_size:
            print(f"❌ Image too large: {{file_size / (1024*1024):.1f}}MB > 20MB")
            return None
        
        # Validate image format
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
                
            print(f"📐 Dimensions: {{width}}x{{height}}")
            print(f"📄 Format: {{format_name}} ({{mode}})")
            print(f"💾 Size: {{file_size / 1024:.1f}} KB")
            
        except Exception as img_error:
            print(f"❌ Invalid image file: {{str(img_error)}}")
            return None
        
        # Initialize AI client
        try:
            client = anthropic.Anthropic()
        except Exception as client_error:
            print(f"❌ Could not initialize AI client: {{str(client_error)}}")
            print("Check ANTHROPIC_API_KEY environment variable")
            return None
        
        # Encode image for API
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as encode_error:
            print(f"❌ Could not encode image: {{str(encode_error)}}")
            return None
        
        # Determine media type
        extension = Path(image_path).suffix.lower()
        media_type_map = {{
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.webp': 'image/webp',
            '.gif': 'image/gif'
        }}
        media_type = media_type_map.get(extension, 'image/jpeg')
        
        # Create analysis prompt based on type
        analysis_prompts = {{
            "comprehensive": f"""Provide a comprehensive analysis of this image:

COMPOSITION & DESIGN:
- Visual balance and focal points
- Color harmony and mood  
- Lighting and contrast quality
- Overall artistic composition

CONTENT ANALYSIS:
- Key subjects and elements
- Text visibility and readability
- Background/foreground relationship
- Emotional impact and messaging

TECHNICAL ASSESSMENT:
- Image quality and sharpness ({{width}}x{{height}})
- Resolution appropriateness for use
- Format optimization potential
- Cropping or framing suggestions

PROFESSIONAL RECOMMENDATIONS:
- How to enhance visual impact
- Text placement suggestions for overlays
- Color adjustments for better appeal
- Specific improvements for intended use

Be specific and actionable.""",

            "technical": f"Analyze this image's technical properties: resolution ({{width}}x{{height}}), compression quality, color space, sharpness, noise levels, and optimization potential. Provide specific technical recommendations.",
            
            "composition": "Focus on compositional elements: rule of thirds, leading lines, symmetry, balance, focal points, depth of field, and framing. Suggest improvements.",
            
            "content": "Describe the image content in detail: subjects, objects, text, colors, style, mood, and context. Focus on what the image communicates.",
            
            "quick": "Provide a concise analysis covering the main visual elements, overall quality, and 2-3 key improvement suggestions."
        }}
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts["comprehensive"])
        
        # Perform AI analysis with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.messages.create(
                    model="{model}",
                    max_tokens=4000,
                    messages=[{{
                        "role": "user",
                        "content": [
                            {{
                                "type": "image",
                                "source": {{
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data
                                }}
                            }},
                            {{
                                "type": "text",
                                "text": prompt
                            }}
                        ]
                    }}]
                )
                
                # Extract analysis
                analysis_result = response.content[0].text
                
                print("🎯 AI ANALYSIS COMPLETE")
                print("="*60)
                print(analysis_result)
                
                # Save comprehensive results
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                # JSON results
                results_data = {{
                    "image_path": image_path,
                    "analysis_type": analysis_type,
                    "timestamp": datetime.now().isoformat(),
                    "image_metadata": {{
                        "width": width,
                        "height": height,
                        "format": format_name,
                        "mode": mode,
                        "file_size_bytes": file_size,
                        "file_size_kb": round(file_size / 1024, 1)
                    }},
                    "analysis": analysis_result,
                    "api_model": "{model}"
                }}
                
                json_file = f"image_analysis_{{timestamp}}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(results_data, f, indent=2, ensure_ascii=False)
                
                # Markdown report
                md_file = f"image_analysis_report_{{timestamp}}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Image Analysis Report\\n\\n")
                    f.write(f"**File:** {{Path(image_path).name}}\\n")
                    f.write(f"**Path:** {{image_path}}\\n")
                    f.write(f"**Analysis Type:** {{analysis_type}}\\n")
                    f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n\\n")
                    f.write(f"## Image Details\\n\\n")
                    f.write(f"- **Dimensions:** {{width}}x{{height}} pixels\\n")
                    f.write(f"- **Format:** {{format_name}} ({{mode}})\\n")
                    f.write(f"- **File Size:** {{file_size / 1024:.1f}} KB\\n\\n")
                    f.write(f"## Analysis\\n\\n")
                    f.write(analysis_result)
                
                print("\\n" + "="*60)
                print("✅ Image analysis completed successfully")
                print(f"💾 JSON data: {{json_file}}")
                print(f"📄 Report: {{md_file}}")
                
                return results_data
                
            except Exception as api_error:
                print(f"⚠️ API attempt {{attempt + 1}}/{{max_retries}} failed: {{str(api_error)}}")
                if attempt < max_retries - 1:
                    print("🔄 Retrying in 2 seconds...")
                    import time
                    time.sleep(2)
                else:
                    print(f"❌ Analysis failed after {{max_retries}} attempts")
                    return None
                    
    except Exception as e:
        print(f"❌ Unexpected error: {{str(e)}}")
        return None

# Execute analysis
result = enhanced_image_analysis()
if result:
    print("\\n🎯 Analysis completed successfully")
else:
    print("\\n❌ Analysis failed")
'''

    elif operation == "edit_image":
        image_path = params.get("image_path", "")
        output_path = params.get("output_path", "auto")
        operations = params.get("operations", {})
        
        return f'''
# Professional Image Editing with Error Recovery
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime
from pathlib import Path

def professional_image_edit():
    """Execute professional image editing workflow with comprehensive error handling"""
    
    # Configuration
    image_path = "{image_path}"
    output_path = "{output_path}"
    operations = {json.dumps(operations, indent=4)}
    
    print(f"🎨 Professional Image Editing")
    print(f"📁 Source: {{Path(image_path).name}}")
    print("="*60)
    
    try:
        # Validate input image
        if not os.path.exists(image_path):
            return {{"error": f"Image not found: {{image_path}}"}}
        
        # Open and validate image
        try:
            with Image.open(image_path) as img:
                original_img = img.copy()
                original_format = img.format or "JPEG"
                original_width, original_height = img.size
                
            print(f"📐 Original: {{original_width}}x{{original_height}} {{original_format}}")
            
        except Exception as img_error:
            return {{"error": f"Could not open image: {{str(img_error)}}"}}
        
        # Create working copy
        current_img = original_img.copy()
        operation_log = []
        
        # RESIZE OPERATION
        if operations.get("resize", False):
            try:
                target_width = operations.get("width", 1200)
                maintain_ratio = operations.get("maintain_aspect_ratio", True)
                
                if target_width <= 0:
                    print("⚠️ Invalid width, skipping resize")
                elif target_width >= original_width:
                    print("⚠️ Target larger than original, skipping resize")
                    operation_log.append("resize_skipped")
                else:
                    if maintain_ratio:
                        ratio = original_height / original_width
                        target_height = int(target_width * ratio)
                    else:
                        target_height = operations.get("height", original_height)
                    
                    current_img = current_img.resize((target_width, target_height), Image.LANCZOS)
                    operation_log.append(f"resized_{{target_width}}x{{target_height}}")
                    print(f"✅ Resized to {{target_width}}x{{target_height}}")
                    
            except Exception as resize_error:
                print(f"⚠️ Resize failed: {{str(resize_error)}}")
        
        # CROP OPERATION
        if operations.get("crop", False):
            try:
                crop_method = operations.get("crop_method", "coordinates")
                current_width, current_height = current_img.size
                
                if crop_method == "coordinates":
                    x = operations.get("x", 0)
                    y = operations.get("y", 0)
                    crop_width = operations.get("crop_width", current_width)
                    crop_height = operations.get("crop_height", current_height)
                    
                    # Validate coordinates
                    x = max(0, min(x, current_width - 1))
                    y = max(0, min(y, current_height - 1))
                    crop_width = max(1, min(crop_width, current_width - x))
                    crop_height = max(1, min(crop_height, current_height - y))
                    
                    crop_box = (x, y, x + crop_width, y + crop_height)
                    current_img = current_img.crop(crop_box)
                    operation_log.append(f"cropped_{{crop_width}}x{{crop_height}}")
                    print(f"✅ Cropped to {{crop_width}}x{{crop_height}}")
                    
                elif crop_method == "aspect_ratio":
                    aspect_ratio = operations.get("aspect_ratio", "16:9")
                    focus = operations.get("focus", "center")
                    
                    try:
                        ratio_parts = aspect_ratio.split(":")
                        target_ratio = int(ratio_parts[0]) / int(ratio_parts[1])
                        current_ratio = current_width / current_height
                        
                        if current_ratio > target_ratio:
                            # Crop width
                            new_width = int(current_height * target_ratio)
                            new_height = current_height
                            
                            if focus == "left":
                                x = 0
                            elif focus == "right":
                                x = current_width - new_width
                            else:  # center
                                x = (current_width - new_width) // 2
                            y = 0
                        else:
                            # Crop height
                            new_width = current_width
                            new_height = int(current_width / target_ratio)
                            
                            if focus == "top":
                                y = 0
                            elif focus == "bottom":
                                y = current_height - new_height
                            else:  # center
                                y = (current_height - new_height) // 2
                            x = 0
                        
                        crop_box = (x, y, x + new_width, y + new_height)
                        current_img = current_img.crop(crop_box)
                        operation_log.append(f"aspect_{{aspect_ratio.replace(':', 'x')}}")
                        print(f"✅ Cropped to {{aspect_ratio}} ratio")
                        
                    except Exception as aspect_error:
                        print(f"⚠️ Aspect ratio crop failed: {{str(aspect_error)}}")
                        
            except Exception as crop_error:
                print(f"⚠️ Crop failed: {{str(crop_error)}}")
        
        # TEXT OVERLAY OPERATION
        if operations.get("add_text", False):
            try:
                text = operations.get("text", "")
                if not text:
                    print("⚠️ No text provided, skipping text overlay")
                else:
                    # Convert to RGBA for text overlay
                    if current_img.mode != 'RGBA':
                        current_img = current_img.convert('RGBA')
                    
                    current_width, current_height = current_img.size
                    
                    # Add shade layer for text readability
                    shade_opacity = operations.get("shade_opacity", 30)
                    overlay = Image.new('RGBA', (current_width, current_height), 
                                       (0, 0, 0, int(255 * shade_opacity / 100)))
                    current_img = Image.alpha_composite(current_img, overlay)
                    
                    # Font configuration
                    font_name = operations.get("font", "Open Sans")
                    font_size = operations.get("font_size")
                    
                    if font_size is None:
                        font_size = int(current_width * 0.05)  # 5% of width
                    
                    # Load font with fallbacks
                    font_loaded = False
                    fonts_dir = "tools/fonts"
                    font_files = {{
                        "Bebas Neue": "BebasNeue-Regular.ttf",
                        "Georgia": "Georgia-Regular.ttf", 
                        "Open Sans": "OpenSans-Regular.ttf",
                        "Montserrat": "Montserrat-Regular.ttf",
                        "Playfair Display": "PlayfairDisplay-Regular.ttf"
                    }}
                    
                    # Try curated fonts first
                    if font_name in font_files and os.path.exists(fonts_dir):
                        font_path = os.path.join(fonts_dir, font_files[font_name])
                        if os.path.exists(font_path):
                            try:
                                pil_font = ImageFont.truetype(font_path, font_size)
                                font_loaded = True
                                print(f"✅ Loaded curated font: {{font_name}}")
                            except Exception:
                                pass
                    
                    # Fallback fonts
                    if not font_loaded:
                        try:
                            pil_font = ImageFont.truetype("Arial.ttf", font_size)
                            print("✅ Using Arial font")
                        except:
                            pil_font = ImageFont.load_default()
                            print("✅ Using default font")
                    
                    # Position text
                    draw = ImageDraw.Draw(current_img)
                    text_bbox = draw.textbbox((0, 0), text, font=pil_font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    text_position = operations.get("text_position", "center")
                    if text_position == "center":
                        x_pos = (current_width - text_width) // 2
                        y_pos = (current_height - text_height) // 2
                    elif text_position == "top":
                        x_pos = (current_width - text_width) // 2
                        y_pos = int(current_height * 0.1)
                    elif text_position == "bottom":
                        x_pos = (current_width - text_width) // 2
                        y_pos = int(current_height * 0.9) - text_height
                    else:
                        x_pos = (current_width - text_width) // 2
                        y_pos = (current_height - text_height) // 2
                    
                    # Draw text
                    draw.text((x_pos, y_pos), text, fill=(255, 255, 255, 255), font=pil_font)
                    operation_log.append("text_overlay")
                    print(f"✅ Added text: '{{text}}'")
                    
            except Exception as text_error:
                print(f"⚠️ Text overlay failed: {{str(text_error)}}")
        
        # SAVE OPERATION
        try:
            # Convert back to RGB if needed
            if current_img.mode == 'RGBA':
                current_img = current_img.convert("RGB")
            
            # Determine output path
            if output_path == "auto" or not output_path:
                input_path = Path(image_path)
                base_name = input_path.stem
                
                if operation_log:
                    desc = "_".join(operation_log)
                    output_name = f"{{base_name}}_{{desc}}"
                else:
                    output_name = f"{{base_name}}_edited"
                
                output_format = operations.get("output_format", "webp")
                ext = f".{{output_format.lower()}}"
                if output_format.lower() in ["jpg", "jpeg"]:
                    ext = ".jpg"
                
                final_output_path = input_path.parent / f"{{output_name}}{{ext}}"
            else:
                final_output_path = Path(output_path)
            
            # Save with format-specific options
            output_format = operations.get("output_format", "webp")
            format_map = {{
                "jpg": "JPEG", "jpeg": "JPEG", 
                "png": "PNG", "webp": "WEBP"
            }}
            save_format = format_map.get(output_format.lower(), "WEBP")
            
            save_kwargs = {{"format": save_format}}
            if save_format == "JPEG":
                save_kwargs["quality"] = 95
                save_kwargs["optimize"] = True
            elif save_format == "WEBP":
                save_kwargs["quality"] = 90
                save_kwargs["optimize"] = True
            elif save_format == "PNG":
                save_kwargs["optimize"] = True
            
            current_img.save(final_output_path, **save_kwargs)
            
            # Success report
            final_width, final_height = current_img.size
            file_size = os.path.getsize(final_output_path)
            
            result = {{
                "status": "success",
                "output_path": str(final_output_path),
                "original_size": f"{{original_width}}x{{original_height}}",
                "final_size": f"{{final_width}}x{{final_height}}",
                "operations": operation_log,
                "file_size_kb": round(file_size / 1024, 1),
                "format": save_format
            }}
            
            print("\\n" + "="*60)
            print("🎨 PROFESSIONAL EDITING COMPLETE")
            print(f"📁 Output: {{final_output_path.name}}")
            print(f"📐 Final: {{final_width}}x{{final_height}} {{save_format}}")
            print(f"💾 Size: {{file_size / 1024:.1f}} KB")
            print(f"🛠️ Operations: {{', '.join(operation_log) if operation_log else 'optimization'}}")
            print("✨ Perfect picture created!")
            
            return result
            
        except Exception as save_error:
            return {{"error": f"Save failed: {{str(save_error)}}"}}
            
    except Exception as e:
        return {{"error": f"Editing failed: {{str(e)}}"}}

# Execute the professional editing workflow
result = professional_image_edit()
if result.get("status") == "success":
    print("\\n🎯 Editing completed successfully")
else:
    print(f"\\n❌ Editing failed: {{result.get('error', 'Unknown error')}}")
'''

    else:
        return f"# Unknown image operation: {operation}"
