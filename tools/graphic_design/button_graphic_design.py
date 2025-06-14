"""
GRAPHIC DESIGN TOOL
Human Button Generators
"""

from typing import Dict, Any, Optional


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for AI-powered image analysis
    
    Args:
        params: Analysis parameters including image_path and analysis_approach
        model: Target model for code generation
        
    Returns:
        Self-contained executable code snippet
    """
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
                        "media_type": "image/jpeg",
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
                            "url": f"data:image/jpeg;base64,{image_data}"
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
                        "media_type": "image/jpeg",
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
    if not os.path.exists(image_path):
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
- Background/foreground relationship
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
    
    print("\\n" + "="*60)
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
        f.write(f"**Date:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}\\n")
        f.write(f"**Model:** {model}\\n\\n")
        f.write("## Analysis Results\\n\\n")
        f.write(analysis_result)
        f.write("\\n\\n---\\n*Generated by SFA v4 Graphic Design Tool*")
    
    print("\\n" + "="*60)
    print("✅ Analysis completed successfully!")
    print(f"💾 Detailed analysis saved to: {{analysis_file}}")
    print(f"💰 Estimated cost: $0.02")
    
except Exception as e:
    print(f"❌ Analysis failed: {{str(e)}}")
    print("💡 Ensure image file exists and is a supported format (JPEG, PNG, WebP)")
'''


def create_editing_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for professional image editing
    
    Args:
        params: Editing parameters for the 5-step workflow
        model: Target model (not used for local processing)
        
    Returns:
        Self-contained executable code snippet
    """
    # Extract parameters with defaults
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
# Professional Image Editing - 5-Step Workflow
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime

def professional_image_editing():
    """Execute the sophisticated 5-step image editing workflow"""
    
    # Configuration
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
    aspect_ratio = {f'"{aspect_ratio}"' if aspect_ratio else "None"}
    focus = "{focus}"
    
    # Text parameters
    add_text = {add_text}
    text = "{text}"
    font = "{font}"
    font_size = {font_size}
    text_position = "{text_position}"
    shade_opacity = {shade_opacity}
    
    print("🎨 Professional Image Editing - 5-Step Workflow")
    print(f"📁 Source: {{image_path}}")
    print("🎯 Philosophy: Only perfect pictures created")
    print("="*60)
    
    try:
        # STEP 1: VALIDATION AND ASSESSMENT
        print("1️⃣ STEP 1: Assessment & Validation")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {{image_path}}")
            return
            
        # Open and assess image
        img = Image.open(image_path)
        original_width, original_height = img.size
        original_format = img.format or "JPEG"
        
        print(f"📐 Original: {{original_width}}x{{original_height}} {{original_format}}")
        
        # Track operations for output naming
        operations = []
        current_img = img
        
        # STEP 2: PROFESSIONAL RESIZE
        if resize:
            print("\\n2️⃣ STEP 2: Professional Resize")
            
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
                
                # Professional resize with LANCZOS resampling
                current_img = current_img.resize((width, height), Image.LANCZOS)
                operations.append(f"resized_{{width}}x{{height}}")
                print(f"✅ Resized to {{width}}x{{height}} using LANCZOS")
        else:
            print("\\n2️⃣ STEP 2: Resize (Skipped)")
        
        # Get current dimensions
        current_width, current_height = current_img.size
        
        # STEP 3: SMART CROPPING
        if crop:
            print("\\n3️⃣ STEP 3: Smart Cropping")
            
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
                print(f"✅ Cropped to {{width_val}}x{{height_val}} at ({{x_val}}, {{y_val}})")
                
            elif crop_method == "aspect_ratio":
                if not aspect_ratio or aspect_ratio == "None":
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
                print(f"✅ Cropped to {{aspect_ratio}} ratio with {{focus}} focus")
        else:
            print("\\n3️⃣ STEP 3: Cropping (Skipped)")
        
        # Update dimensions after crop
        current_width, current_height = current_img.size
        
        # STEP 4: PROFESSIONAL TEXT OVERLAY
        if add_text:
            print("\\n4️⃣ STEP 4: Professional Text Overlay")
            
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
            print(f"✅ Applied {{shade_opacity}}% shade layer for readability")
            
            # FONT LOADING - Curated collection
            fonts_dir = "tools/fonts"
            if not os.path.exists(fonts_dir):
                fonts_dir = "../tools/fonts"
            
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
            
            # Load font with fallback
            font_loaded = "system_fallback"
            try:
                if font_path:
                    pil_font = ImageFont.truetype(font_path, font_size)
                    font_loaded = font
                    print(f"✅ Loaded curated font: {{font}}")
                else:
                    # Fallback to system fonts
                    try:
                        pil_font = ImageFont.truetype("Arial.ttf", font_size)
                        font_loaded = "Arial"
                    except:
                        pil_font = ImageFont.load_default()
                        font_size = int(current_width * 0.03)
                        font_loaded = "default"
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
            
            # Draw text in white for maximum contrast
            draw.text((x_pos, y_pos), text, fill=(255, 255, 255, 255), font=pil_font)
            operations.append("text_overlay")
            print(f"✅ Added text: '{{text}}' using {{font_loaded}} at {{text_position}}")
        else:
            print("\\n4️⃣ STEP 4: Text Overlay (Skipped)")
        
        # Convert back to RGB for saving
        if current_img.mode == 'RGBA':
            current_img = current_img.convert("RGB")
        
        # STEP 5: SMART OUTPUT AND OPTIMIZATION
        print("\\n5️⃣ STEP 5: Smart Output & Optimization")
        
        if not output_path or output_path == "None":
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
        
        # Professional format optimization
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
        print(f"💰 Estimated cost: $0.01")
        
    except Exception as e:
        print(f"❌ Editing failed: {{str(e)}}")
        print("💡 Ensure image file exists and PIL dependencies are installed")

# Execute the professional workflow
professional_image_editing()
'''


def create_optimization_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for image optimization
    
    Args:
        params: Optimization parameters
        model: Target model (not used for local processing)
        
    Returns:
        Self-contained executable code snippet
    """
    image_path = params.get("image_path", "")
    quality = params.get("quality", 85)
    target_format = params.get("target_format", "webp")
    
    return f'''
# Professional Image Optimization
import os
from PIL import Image
from datetime import datetime

def optimize_image_professionally():
    """Execute professional image optimization"""
    
    # Configuration
    image_path = "{image_path}"
    quality = {quality}
    target_format = "{target_format}"
    
    print("🔧 Professional Image Optimization")
    print(f"📁 Source: {{image_path}}")
    print(f"🎯 Quality: {{quality}}%")
    print(f"📦 Target Format: {{target_format.upper()}}")
    print("="*60)
    
    try:
        # Validate input
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {{image_path}}")
            return
        
        if not (1 <= quality <= 100):
            print("❌ Quality must be between 1 and 100")
            return
        
        # Open and analyze image
        with Image.open(image_path) as img:
            original_size = os.path.getsize(image_path)
            width, height = img.size
            original_format = img.format or "JPEG"
            
            print(f"📐 Dimensions: {{width}}x{{height}}")
            print(f"📦 Original Format: {{original_format}}")
            print(f"📊 Original Size: {{original_size:,}} bytes")
            
            # Generate output path
            file_name, file_ext = os.path.splitext(image_path)
            output_path = f"{{file_name}}_optimized.{{target_format.lower()}}"
            
            # Format mapping and optimization settings
            format_map = {{
                "jpg": "JPEG", "jpeg": "JPEG", 
                "png": "PNG", "webp": "WEBP"
            }}
            save_format = format_map.get(target_format.lower(), "WEBP")
            
            save_kwargs = {{"format": save_format}}
            if save_format == "JPEG":
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif save_format == "WEBP":
                save_kwargs["quality"] = quality
                save_kwargs["method"] = 6  # Best compression
            elif save_format == "PNG":
                save_kwargs["optimize"] = True
            
            print(f"\\n🔄 Optimizing to {{save_format}}...")
            
            # Save optimized image
            img.save(output_path, **save_kwargs)
            
            # Calculate results
            optimized_size = os.path.getsize(output_path)
            size_reduction = ((original_size - optimized_size) / original_size) * 100
            
            print("\\n" + "="*60)
            print("🔧 OPTIMIZATION COMPLETE")
            print(f"📁 Output: {{output_path}}")
            print(f"📊 Size Reduction: {{size_reduction:.1f}}%")
            print(f"📦 Format: {{original_format}} → {{save_format}}")
            print(f"💾 Final Size: {{optimized_size:,}} bytes")
            print("✅ Professional optimization completed!")
            print(f"💰 Estimated cost: $0.005")
            
    except Exception as e:
        print(f"❌ Optimization failed: {{str(e)}}")
        print("💡 Ensure image file exists and PIL is installed")

# Execute optimization
optimize_image_professionally()
'''


def create_font_info_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet to display font collection info
    
    Args:
        params: Parameters (not used for font info)
        model: Target model (not used for local processing)
        
    Returns:
        Self-contained executable code snippet
    """
    return '''
# Curated Font Collection Information
import os
from datetime import datetime

def display_font_collection():
    """Display professional font collection details"""
    
    print("🎨 Professional Font Collection")
    print("SFA v4 Graphic Design Tool")
    print("="*60)
    
    # Curated font collection
    fonts = {
        "Bebas Neue": {
            "style": "Bold, modern impact",
            "use_case": "Headlines, bold statements",
            "file": "BebasNeue-Regular.ttf"
        },
        "Georgia": {
            "style": "Classic serif elegance",
            "use_case": "Traditional, readable text",
            "file": "Georgia-Regular.ttf"
        },
        "Open Sans": {
            "style": "Clean, readable sans-serif",
            "use_case": "General purpose, web-friendly",
            "file": "OpenSans-Regular.ttf"
        },
        "Montserrat": {
            "style": "Modern geometric sans-serif",
            "use_case": "Contemporary, professional",
            "file": "Montserrat-Regular.ttf"
        },
        "Playfair Display": {
            "style": "Elegant display serif",
            "use_case": "Luxury, sophisticated designs",
            "file": "PlayfairDisplay-Regular.ttf"
        }
    }
    
    # Check font directory
    fonts_dir = "tools/fonts"
    if not os.path.exists(fonts_dir):
        fonts_dir = "../tools/fonts"
    
    print(f"📁 Font Directory: {fonts_dir}")
    print(f"📂 Directory Exists: {'Yes' if os.path.exists(fonts_dir) else 'No'}")
    print()
    
    # Display each font
    for font_name, font_info in fonts.items():
        print(f"🔤 {font_name}")
        print(f"   Style: {font_info['style']}")
        print(f"   Best For: {font_info['use_case']}")
        print(f"   File: {font_info['file']}")
        
        # Check if font file exists
        if os.path.exists(fonts_dir):
            font_path = os.path.join(fonts_dir, font_info['file'])
            status = "✅ Available" if os.path.exists(font_path) else "❌ Missing"
            print(f"   Status: {status}")
        else:
            print(f"   Status: ❓ Directory not found")
        print()
    
    print("🔄 Fallback Options:")
    print("   • System Arial font")
    print("   • PIL default font")
    print("   • Automatic font size calculation (5% of image width)")
    print()
    print("💡 Professional Typography Tips:")
    print("   • Use Bebas Neue for bold impact headlines")
    print("   • Choose Georgia for traditional elegance")
    print("   • Open Sans works great for general text")
    print("   • Montserrat for modern, clean designs")
    print("   • Playfair Display for luxury branding")
    print()
    print("✨ All fonts include automatic shade layer for readability")
    print(f"💰 Font usage cost: FREE")

# Display font collection
display_font_collection()
'''


def estimate_cost(operation: str, params: Dict[str, Any]) -> float:
    """Estimate cost for graphic design operations"""
    base_costs = {
        "analyze": 0.02,  # AI analysis
        "edit": 0.01,     # Local processing
        "optimize": 0.005, # Local processing
        "fonts": 0.0      # Information only
    }
    
    cost = base_costs.get(operation, 0.01)
    
    # Additional costs for complex operations
    if operation == "edit":
        if params.get("add_text", False):
            cost += 0.005  # Text overlay processing
        if params.get("crop", False):
            cost += 0.002  # Cropping calculations
        if params.get("resize", False):
            cost += 0.003  # Resize processing
    
    return cost


def get_model_compatibility() -> Dict[str, Any]:
    """Get model compatibility information for graphic design tool"""
    return {
        "supported_models": [
            "claude-sonnet-4",
            "claude-3-5-sonnet", 
            "claude-3-haiku",
            "gpt-4-vision-preview",
            "gpt-4o",
            "gemini-pro-vision"
        ],
        "analysis_models": [
            "claude-sonnet-4",
            "claude-3-5-sonnet",
            "gpt-4-vision-preview",
            "gpt-4o",
            "gemini-pro-vision"
        ],
        "local_processing": [
            "edit_image",
            "optimize_image", 
            "get_curated_fonts"
        ],
        "ai_required": [
            "analyze_image"
        ],
        "universal_compatibility": True,
        "auto_format_conversion": True
    } 