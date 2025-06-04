#!/usr/bin/env python3
"""
Image Editing Tool for SFA Agents

This script provides a unified tool for artistic image editing,
including resizing, cropping, and adding text with a shade layer.
"""

import os
import json
from typing import Dict, Any, Optional, Union
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def edit_image(
    image_path: str,
    output_path: Optional[str] = None,
    output_format: str = "webp",  # Default to webp, can be jpg, jpeg, png
    
    # Resize
    resize: bool = False,
    width: int = 1200,
    maintain_aspect_ratio: bool = True,
    
    # Crop
    crop: bool = False,
    crop_method: str = "coordinates",  # "coordinates" or "aspect_ratio"
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
    shade_opacity: int = 30  # 0-100
) -> Dict[str, Any]:
    """
    Artistically edit an image with resize, crop, and text operations.
    
    This tool follows a creative workflow for image editing:
    1. Assess the image - identify focus, imagine text placement, consider composition
    2. Resize to appropriate dimensions (typically 900-1200px width)
    3. Apply shade layer and add text, or crop the image first
    4. Finalize with any remaining operations
    5. Save in the desired format (webp recommended)
    
    NOTE: Always use the analyze_image tool before and after editing to assess 
    composition and readability.
    
    Args:
        image_path: Path to the input image
        output_path: Path for the output image (auto-generated if None)
        output_format: Format for the output image (webp by default)
        
        # Resize parameters
        resize: Whether to resize the image
        width: Target width for resizing (default 1200px)
        maintain_aspect_ratio: Whether to maintain aspect ratio when resizing
        
        # Crop parameters
        crop: Whether to crop the image
        crop_method: Method for cropping ("coordinates" or "aspect_ratio")
        x, y: Top-left coordinates for cropping (for crop_method="coordinates")
        crop_width, crop_height: Width and height for cropping (for crop_method="coordinates")
        aspect_ratio: Target aspect ratio as "width:height" (for crop_method="aspect_ratio")
        focus: Focus point for aspect ratio cropping
        
        # Text parameters
        add_text: Whether to add text to the image
        text: Text to add to the image (in white)
        font: Font to use (Bebas Neue, Georgia, Open Sans, Montserrat, Playfair Display)
        font_size: Font size in points (auto-calculated if None)
        text_position: Where to place text on the image (center, top, bottom)
        shade_opacity: Opacity of the dark shade layer (0-100, default 30)
        
    Returns:
        Dictionary with operation results
    """
    try:
        # Check if image exists
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "message": f"Image not found: {image_path}"
            }
            
        # Open the image
        img = Image.open(image_path)
        original_width, original_height = img.size
        original_format = img.format or "JPEG"
        
        # Track operations performed for return info
        operations = []
        current_img = img
        
        # Step 1: Resize if requested
        if resize:
            if width <= 0:
                return {
                    "status": "error",
                    "message": "Width must be a positive number"
                }
                
            if width >= original_width:
                # Don't upscale images by default
                operations.append({
                    "operation": "resize",
                    "status": "skipped",
                    "reason": "Target width is larger than original width"
                })
            else:
                # Calculate height to maintain aspect ratio
                if maintain_aspect_ratio:
                    ratio = original_height / original_width
                    height = int(width * ratio)
                else:
                    height = original_height
                
                # Perform resize
                current_img = current_img.resize((width, height), Image.LANCZOS)
                
                operations.append({
                    "operation": "resize",
                    "original_size": {"width": original_width, "height": original_height},
                    "new_size": {"width": width, "height": height}
                })
        
        # Get current dimensions after potential resize
        current_width, current_height = current_img.size
        
        # Step 2: Crop if requested
        if crop:
            if crop_method == "coordinates":
                # Validate crop coordinates
                if x is None or y is None or crop_width is None or crop_height is None:
                    return {
                        "status": "error",
                        "message": "For coordinate-based cropping, you must provide x, y, crop_width, and crop_height"
                    }
                
                # Ensure crop box is within image dimensions
                x_val = max(0, min(x, current_width - 1))
                y_val = max(0, min(y, current_height - 1))
                width_val = max(1, min(crop_width, current_width - x_val))
                height_val = max(1, min(crop_height, current_height - y_val))
                
                # Perform crop
                crop_box = (x_val, y_val, x_val + width_val, y_val + height_val)
                current_img = current_img.crop(crop_box)
                
                operations.append({
                    "operation": "crop",
                    "method": "coordinates",
                    "crop_box": {
                        "x": x_val,
                        "y": y_val,
                        "width": width_val,
                        "height": height_val
                    }
                })
                
            elif crop_method == "aspect_ratio":
                # Validate aspect ratio
                if not aspect_ratio:
                    return {
                        "status": "error",
                        "message": "For aspect ratio cropping, you must provide aspect_ratio parameter"
                    }
                
                # Parse aspect ratio
                try:
                    aspect_parts = aspect_ratio.split(":")
                    target_width_ratio = int(aspect_parts[0])
                    target_height_ratio = int(aspect_parts[1])
                    target_ratio = target_width_ratio / target_height_ratio
                except (ValueError, IndexError, ZeroDivisionError):
                    return {
                        "status": "error",
                        "message": f"Invalid aspect ratio format: {aspect_ratio}. Use format like '16:9'."
                    }
                
                # Calculate current aspect ratio
                current_ratio = current_width / current_height
                
                # Determine crop dimensions
                if current_ratio > target_ratio:
                    # Image is wider than target ratio, crop width
                    new_width = int(current_height * target_ratio)
                    new_height = current_height
                    
                    # Determine x position based on focus
                    if focus == "left":
                        x_val = 0
                    elif focus == "right":
                        x_val = current_width - new_width
                    else:  # center or any other value
                        x_val = (current_width - new_width) // 2
                    
                    y_val = 0
                else:
                    # Image is taller than target ratio, crop height
                    new_width = current_width
                    new_height = int(current_width / target_ratio)
                    
                    # Determine y position based on focus
                    if focus == "top":
                        y_val = 0
                    elif focus == "bottom":
                        y_val = current_height - new_height
                    else:  # center or any other value
                        y_val = (current_height - new_height) // 2
                    
                    x_val = 0
                
                # Perform crop
                crop_box = (x_val, y_val, x_val + new_width, y_val + new_height)
                current_img = current_img.crop(crop_box)
                
                operations.append({
                    "operation": "crop",
                    "method": "aspect_ratio",
                    "aspect_ratio": aspect_ratio,
                    "focus": focus,
                    "crop_box": {
                        "x": x_val,
                        "y": y_val,
                        "width": new_width,
                        "height": new_height
                    }
                })
            else:
                return {
                    "status": "error",
                    "message": f"Unknown crop_method: {crop_method}"
                }
        
        # Get current dimensions after potential crop
        current_width, current_height = current_img.size
        
        # Step 3: Add text if requested
        if add_text:
            # Validate text parameters
            if not text:
                return {
                    "status": "error",
                    "message": "Text parameter is required when add_text=True"
                }
            
            # Convert to RGBA for text overlay
            if current_img.mode != 'RGBA':
                current_img = current_img.convert('RGBA')
            
            # Always apply dark shade layer with the specified opacity
            overlay = Image.new('RGBA', (current_width, current_height), 
                                (0, 0, 0, int(255 * shade_opacity / 100)))
            
            # Composite the overlay onto the image
            current_img = Image.alpha_composite(current_img, overlay)
            
            # Load font - start by trying to find in the fonts directory
            fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
            
            # Map of font names to filenames
            font_files = {
                "Bebas Neue": "BebasNeue-Regular.ttf",
                "Georgia": "Georgia.ttf",
                "Open Sans": "OpenSans-Regular.ttf",
                "Montserrat": "Montserrat-Regular.ttf",
                "Playfair Display": "PlayfairDisplay-Regular.ttf"
            }
            
            # Try to load from fonts directory
            font_path = None
            if font in font_files:
                potential_path = os.path.join(fonts_dir, font_files[font])
                if os.path.exists(potential_path):
                    font_path = potential_path
            
            # Try to use the font
            try:
                if font_path:
                    # Calculate font size if not specified
                    if font_size is None:
                        # Default to 5% of image width
                        font_size = int(current_width * 0.05)
                    
                    # Load the font
                    pil_font = ImageFont.truetype(font_path, font_size)
                else:
                    # Fall back to default font
                    if font_size is None:
                        font_size = int(current_width * 0.05)
                    
                    # Try to find a default font
                    try:
                        # First try to use a default system font
                        pil_font = ImageFont.truetype("Arial.ttf", font_size)
                    except:
                        # Fall back to PIL's default font
                        pil_font = ImageFont.load_default()
                        # Scale default font
                        font_size = int(current_width * 0.03)  # Default font needs different scaling
            except Exception as font_error:
                return {
                    "status": "error",
                    "message": f"Error loading font: {str(font_error)}"
                }
            
            # Create drawing context
            draw = ImageDraw.Draw(current_img)
            
            # Calculate text size
            text_bbox = draw.textbbox((0, 0), text, font=pil_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Determine text position
            if text_position == "center":
                x_val = (current_width - text_width) // 2
                y_val = (current_height - text_height) // 2
            elif text_position == "top":
                x_val = (current_width - text_width) // 2
                y_val = int(current_height * 0.1)  # 10% from top
            elif text_position == "bottom":
                x_val = (current_width - text_width) // 2
                y_val = int(current_height * 0.9) - text_height  # 10% from bottom
            elif "," in text_position:
                # Parse x,y coordinates
                try:
                    coords = text_position.split(",")
                    x_val = int(coords[0].strip())
                    y_val = int(coords[1].strip())
                except:
                    # Fall back to center if parsing fails
                    x_val = (current_width - text_width) // 2
                    y_val = (current_height - text_height) // 2
            else:
                # Default to center if position not recognized
                x_val = (current_width - text_width) // 2
                y_val = (current_height - text_height) // 2
            
            # Draw text in white
            draw.text((x_val, y_val), text, fill=(255, 255, 255, 255), font=pil_font)
            
            operations.append({
                "operation": "add_text",
                "text": text,
                "font": font,
                "size": font_size,
                "position": (x_val, y_val),
                "shade_opacity": shade_opacity
            })
        
        # Convert back to RGB for saving
        if current_img.mode == 'RGBA':
            current_img = current_img.convert("RGB")
        
        # Step 4: Determine output path and format
        if not output_path:
            # Auto-generate output path based on operations performed
            file_name, file_ext = os.path.splitext(image_path)
            
            # Build descriptive filename based on operations
            parts = []
            
            if resize:
                parts.append(f"{width}w")
                
            if crop:
                if crop_method == "aspect_ratio" and aspect_ratio:
                    parts.append(aspect_ratio.replace(":", "x"))
                else:
                    parts.append("cropped")
                    
            if add_text:
                parts.append("text")
                
            if parts:
                base_name = f"{file_name}_{'_'.join(parts)}"
            else:
                base_name = f"{file_name}_edited"
            
            # Use specified output format or default to webp
            ext = f".{output_format.lower()}"
            if output_format.lower() in ["jpg", "jpeg"]:
                ext = ".jpg"
                
            output_path = f"{base_name}{ext}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Step 5: Save the final image
        # Convert format names to PIL format strings
        format_map = {
            "jpg": "JPEG",
            "jpeg": "JPEG",
            "png": "PNG",
            "webp": "WEBP"
        }
        save_format = format_map.get(output_format.lower(), "WEBP")
        
        # Use save_format
        save_kwargs = {"format": save_format}
            
        # Special handling for JPEG to set quality
        if save_format == "JPEG":
            save_kwargs["quality"] = 95  # High quality
        elif save_format == "WEBP":
            save_kwargs["quality"] = 90  # Good balance of quality and size
            
        current_img.save(output_path, **save_kwargs)
        
        # Return results
        return {
            "status": "success",
            "message": f"Image edited successfully",
            "output_path": output_path,
            "original": {
                "path": image_path,
                "dimensions": {"width": original_width, "height": original_height},
                "format": original_format
            },
            "final": {
                "path": output_path,
                "dimensions": {"width": current_img.width, "height": current_img.height},
                "format": output_format
            },
            "operations": operations
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error editing image: {str(e)}"
        }

def get_tool_definition():
    """Return the tool definition for SFA integration."""
    return {
        "name": "edit_image",
        "description": "Artistically edit an image with resize, crop, and text operations in a single function call.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path for the output image (auto-generated if not provided)"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["webp", "jpg", "jpeg", "png"],
                    "description": "Format for the output image (webp recommended)",
                    "default": "webp"
                },
                
                # Resize parameters
                "resize": {
                    "type": "boolean",
                    "description": "Whether to resize the image",
                    "default": false
                },
                "width": {
                    "type": "integer",
                    "description": "Target width for resizing (900-1200px recommended)",
                    "default": 1200
                },
                "maintain_aspect_ratio": {
                    "type": "boolean",
                    "description": "Whether to maintain aspect ratio when resizing",
                    "default": true
                },
                
                # Crop parameters
                "crop": {
                    "type": "boolean",
                    "description": "Whether to crop the image",
                    "default": false
                },
                "crop_method": {
                    "type": "string",
                    "enum": ["coordinates", "aspect_ratio"],
                    "description": "Method for cropping",
                    "default": "coordinates"
                },
                "x": {
                    "type": "integer",
                    "description": "Left coordinate for cropping"
                },
                "y": {
                    "type": "integer",
                    "description": "Top coordinate for cropping"
                },
                "crop_width": {
                    "type": "integer",
                    "description": "Width for cropping"
                },
                "crop_height": {
                    "type": "integer",
                    "description": "Height for cropping"
                },
                "aspect_ratio": {
                    "type": "string",
                    "description": "Target aspect ratio as \"width:height\" (e.g., \"16:9\")"
                },
                "focus": {
                    "type": "string",
                    "enum": ["center", "top", "bottom", "left", "right"],
                    "description": "Focus point for aspect ratio cropping",
                    "default": "center"
                },
                
                # Text parameters
                "add_text": {
                    "type": "boolean",
                    "description": "Whether to add text to the image",
                    "default": false
                },
                "text": {
                    "type": "string",
                    "description": "Text to add to the image (will be white)"
                },
                "font": {
                    "type": "string",
                    "enum": ["Bebas Neue", "Georgia", "Open Sans", "Montserrat", "Playfair Display"],
                    "description": "Font to use for the text",
                    "default": "Open Sans"
                },
                "font_size": {
                    "type": "integer",
                    "description": "Font size in points (auto-calculated based on image width if not provided)"
                },
                "text_position": {
                    "type": "string",
                    "enum": ["center", "top", "bottom"],
                    "description": "Where to place the text on the image",
                    "default": "center"
                },
                "shade_opacity": {
                    "type": "integer",
                    "description": "Opacity of the dark shade layer (0-100, typical values: 30 for subtle, 60-80 for emphasis)",
                    "default": 30
                }
            },
            "required": ["image_path"]
        }
    }

if __name__ == "__main__":
    # If run directly, print the tool definition
    print(json.dumps(
        {k: v for k, v in get_tool_definition().items() if k != "function"},
        indent=2
    ))