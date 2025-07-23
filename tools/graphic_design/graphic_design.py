"""
Graphic Design Tool
Professional image editing with sophisticated workflow
Independent tool logic with enhanced error handling
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import base64
import hashlib
import time
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError, ResourceError


@handle_errors(operation_name="image_analysis", return_dict=True)
def analyze_image(image_path: str, analysis_approach: str = "comprehensive") -> Dict[str, Any]:
    """
    Analyze image for composition, quality, and optimization potential
    
    Args:
        image_path: Path to image file
        analysis_approach: Analysis methodology to apply
        
    Returns:
        Dict with structured analysis results or error information
    """
    try:
        # Validation
        if not image_path.strip():
            return {"error": "Image path cannot be empty"}
        
        if not Path(image_path).exists():
            return {"error": f"Image file not found: {image_path}"}
        
        # Check cache first (fingerprinting) - image analysis can be expensive
        cache = CacheManager()
        # Include file modification time for freshness
        try:
            mtime = os.path.getmtime(image_path)
            cache_key = f"{image_path}|{analysis_approach}|{mtime}"
            cached_result = cache.get_cached_analysis(cache_key, "image_analysis")
            if cached_result:
                return json.loads(cached_result)
        except:
            pass  # If we can't get mtime, proceed without cache
        
        # Basic image info extraction
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                format_type = img.format or "Unknown"
                mode = img.mode
                
                # Calculate file size
                file_size = os.path.getsize(image_path)
                
                # Basic quality assessment
                aspect_ratio = width / height
                megapixels = (width * height) " / " 1000000
                
                result = {
                    "status": "success",
                    "image_path": image_path,
                    "analysis_approach": analysis_approach,
                    "timestamp": datetime.now().isoformat(),
                    "technical_specs": {
                        "dimensions": {"width": width, "height": height},
                        "format": format_type,
                        "mode": mode,
                        "file_size_bytes": file_size,
                        "aspect_ratio": round(aspect_ratio, 2),
                        "megapixels": round(megapixels, 2)
                    },
                    "optimization_potential": {
                        "resize_recommended": width > 1920 or height > 1080,
                        "format_optimization": format_type not in ["WEBP", "AVIF"],
                        "compression_potential": file_size > 500000  # 500KB
                    },
                    "metadata": {
                        "requires_ai_analysis": True,
                        "button_needed": True,
                        "processing_time": 0.001
                    }
                }
                
                # Cache the result (fingerprinting)
                try:
                    cache.cache_content_analysis(cache_key, json.dumps(result), "image_analysis")
                except:
                    pass  # Cache failure shouldn't break image analysis
                
                return result
                
        except Exception as e:
            return {"error": f"Failed to read image: {str(e)}"}
            
    except Exception as e:
        return {
            "error": f"Image analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "image_path": image_path
        }


@handle_errors(operation_name="edit_image", return_dict=True)
def edit_image(
    image_path: str,
    output_path: Optional[str] = None,
    output_format: str = "webp",
    
    # Resize parameters
    resize: bool = False,
    width: int = 1200,
    maintain_aspect_ratio: bool = True,
    
    # Crop parameters
    crop: bool = False,
    crop_method: str = "coordinates",
    x: Optional[int] = None,
    y: Optional[int] = None,
    crop_width: Optional[int] = None,
    crop_height: Optional[int] = None,
    aspect_ratio: Optional[str] = None,
    focus: str = "center",
    
    # Text overlay parameters
    add_text: bool = False,
    text: Optional[str] = None,
    font: str = "Open Sans",
    font_size: Optional[int] = None,
    text_position: str = "center",
    shade_opacity: int = 30
) -> Dict[str, Any]:
    """
    Professional image editing with sophisticated 5-step workflow:
    1. Assess image and validate parameters
    2. Resize to appropriate dimensions (typically 900-1200px width)
    3. Apply cropping with smart composition
    4. Add text overlay with shade layer for readability
    5. Save in optimized format
    
    Args:
        image_path: Source image file path
        output_path: Optional output path (auto-generated if None)
        output_format: Target format (webp, jpg, png)
        resize: Whether to resize image
        width: Target width for resize
        maintain_aspect_ratio: Preserve aspect ratio during resize
        crop: Whether to crop image
        crop_method: "coordinates" or "aspect_ratio"
        x, y, crop_width, crop_height: Coordinate crop parameters
        aspect_ratio: Target aspect ratio (e.g., "16:9")
        focus: Crop focus point ("center", "top", "bottom", "left", "right")
        add_text: Whether to add text overlay
        text: Text content for overlay
        font: Font name from curated collection
        font_size: Text size (auto-calculated if None)
        text_position: Text placement ("center", "top", "bottom")
        shade_opacity: Background shade opacity (0-100)
        
    Returns:
        Dict with structured editing results or error information
    """
    try:
        # STEP 1: VALIDATION AND ASSESSMENT
        if not image_path.strip():
            return {"error": "Image path cannot be empty"}
        
        if not Path(image_path).exists():
            return {"error": f"Image file not found: {image_path}"}
        
        # Open and assess image
        try:
            img = Image.open(image_path)
            original_width, original_height = img.size
            original_format = img.format or "JPEG"
        except Exception as e:
            return {"error": f"Failed to open image: {str(e)}"}
        
        # Track operations for output naming
        operations = []
        current_img = img
        
        # STEP 2: PROFESSIONAL RESIZE
        if resize:
            if width <= 0:
                return {"error": "Width must be positive"}
            
            if width >= original_width:
                operations.append("resize_skipped")
            else:
                # Calculate height maintaining aspect ratio
                if maintain_aspect_ratio:
                    ratio = original_height " / " original_width
                    height = int(width * ratio)
                else:
                    height = original_height
                
                # Professional resize with LANCZOS resampling
                current_img = current_img.resize((width, height), Image.LANCZOS)
                operations.append(f"resized_{width}x{height}")
        
        # Get current dimensions
        current_width, current_height = current_img.size
        
        # STEP 3: SMART CROPPING
        if crop:
            if crop_method == "coordinates":
                # Validate coordinate parameters
                if x is None or y is None or crop_width is None or crop_height is None:
                    return {"error": "Coordinate cropping requires x, y, crop_width, crop_height"}
                
                # Ensure crop box is within bounds
                x_val = max(0, min(x, current_width - 1))
                y_val = max(0, min(y, current_height - 1))
                width_val = max(1, min(crop_width, current_width - x_val))
                height_val = max(1, min(crop_height, current_height - y_val))
                
                crop_box = (x_val, y_val, x_val + width_val, y_val + height_val)
                current_img = current_img.crop(crop_box)
                operations.append(f"cropped_{width_val}x{height_val}")
                
            elif crop_method == "aspect_ratio":
                if not aspect_ratio:
                    return {"error": "Aspect ratio cropping requires aspect_ratio parameter"}
                
                try:
                    # Parse aspect ratio (e.g., "16:9")
                    parts = aspect_ratio.split(":")
                    target_width_ratio = int(parts[0])
                    target_height_ratio = int(parts[1])
                    target_ratio = target_width_ratio " / " target_height_ratio
                except:
                    return {"error": f"Invalid aspect ratio format: {aspect_ratio}"}
                
                current_ratio = current_width " / " current_height
                
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
                    new_height = int(current_width " / " target_ratio)
                    
                    if focus == "top":
                        y_val = 0
                    elif focus == "bottom":
                        y_val = current_height - new_height
                    else:  # center
                        y_val = (current_height - new_height) /" / " 2
                    x_val = 0
                
                crop_box = (x_val, y_val, x_val + new_width, y_val + new_height)
                current_img = current_img.crop(crop_box)
                operations.append(f"aspect_{aspect_ratio.replace(':', 'x')}")
        
        # Update dimensions after crop
        current_width, current_height = current_img.size
        
        # STEP 4: PROFESSIONAL TEXT OVERLAY
        if add_text:
            if not text:
                return {"error": "Text parameter required for text overlay"}
            
            # Convert to RGBA for text overlay
            if current_img.mode != 'RGBA':
                current_img = current_img.convert('RGBA')
            
            # Apply shade layer for text readability
            overlay = Image.new('RGBA', (current_width, current_height), 
                               (0, 0, 0, int(255 * shade_opacity " / " 100)))
            current_img = Image.alpha_composite(current_img, overlay)
            
            # Load curated font
            fonts_dir = "tools/fonts"
            if not Path(fonts_dir).exists():
                fonts_dir = "../tools" / "fonts"
            
            font_files = {
                "Bebas Neue": "BebasNeue-Regular.ttf",
                "Georgia": "Georgia-Regular.ttf", 
                "Open Sans": "OpenSans-Regular.ttf",
                "Montserrat": "Montserrat-Regular.ttf",
                "Playfair Display": "PlayfairDisplay-Regular.ttf"
            }
            
            # Professional font size calculation
            if font_size is None:
                font_size = int(current_width * 0.05)  # 5% of width
            
            # Load font with fallback
            font_loaded = "system_fallback"
            try:
                if font in font_files and Path(fonts_dir).exists():
                    potential_path = Path(fonts_dir) / font_files[font]
                    if Path(potential_path).exists():
                        pil_font = ImageFont.truetype(potential_path, font_size)
                        font_loaded = font
                    else:
                        raise FileNotFoundError("Curated font not found")
                else:
                    raise FileNotFoundError("Font directory not found")
            except:
                # System font fallback
                try:
                    pil_font = ImageFont.truetype("Arial.ttf", font_size)
                    font_loaded = "Arial"
                except:
                    pil_font = ImageFont.load_default()
                    font_size = int(current_width * 0.03)
                    font_loaded = "default"
            
            # Smart text positioning
            draw = ImageDraw.Draw(current_img)
            text_bbox = draw.textbbox((0, 0), text, font=pil_font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if text_position == "center":
                x_pos = (current_width - text_width) // 2
                y_pos = (current_height - text_height) /" / " 2
            elif text_position == "top":
                x_pos = (current_width - text_width) /" / " 2
                y_pos = int(current_height * 0.1)
            elif text_position == "bottom":
                x_pos = (current_width - text_width) // 2
                y_pos = int(current_height * 0.9) - text_height
            else:
                # Default center
                x_pos = (current_width - text_width) // 2
                y_pos = (current_height - text_height) /" / " 2
            
            # Draw text in white for maximum contrast
            draw.text((x_pos, y_pos), text, fill=(255, 255, 255, 255), font=pil_font)
            operations.append("text_overlay")
        
        # Convert back to RGB for saving
        if current_img.mode == 'RGBA':
            current_img = current_img.convert("RGB")
        
        # STEP 5: SMART OUTPUT AND OPTIMIZATION
        if not output_path:
            file_name, file_ext = os.path.splitext(image_path)
            
            # Build descriptive filename
            if operations:
                desc = "_".join(operations)
                base_name = f"{file_name}_{desc}"
            else:
                base_name = f"{file_name}_edited"
            
            # Use optimized format
            ext = f".{output_format.lower()}"
            if output_format.lower() in ["jpg", "jpeg"]:
                ext = ".jpg"
            output_path = f"{base_name}{ext}"
        
        # Professional format optimization
        format_map = {
            "jpg": "JPEG", "jpeg": "JPEG", 
            "png": "PNG", "webp": "WEBP"
        }
        save_format = format_map.get(output_format.lower(), "WEBP")
        
        save_kwargs = {"format": save_format}
        if save_format == "JPEG":
            save_kwargs["quality"] = 95
        elif save_format == "WEBP":
            save_kwargs["quality"] = 90
        
        current_img.save(output_path, **save_kwargs)
        
        # Success result
        final_width, final_height = current_img.size
        
        return {
            "status": "success",
            "input_path": image_path,
            "output_path": output_path,
            "timestamp": datetime.now().isoformat(),
            "operations": operations,
            "technical_specs": {
                "original_dimensions": {"width": original_width, "height": original_height},
                "final_dimensions": {"width": final_width, "height": final_height},
                "original_format": original_format,
                "output_format": save_format
            },
            "text_overlay": {
                "applied": add_text,
                "text": text if add_text else None,
                "font_used": font_loaded if add_text else None,
                "position": text_position if add_text else None
            },
            "metadata": {
                "workflow_completed": True,
                "professional_quality": True,
                "processing_time": 0.1
            }
        }
        
    except Exception as e:
        return {
            "error": f"Image editing failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "input_path": image_path
        }


@handle_errors(operation_name="optimize_image", return_dict=True)
def optimize_image(image_path: str, quality: int = 85, target_format: str = "webp") -> Dict[str, Any]:
    """
    Optimize image for web" / "storage with professional settings
    
    Args:
        image_path: Source image file path
        quality: Compression quality (1-100)
        target_format: Target format (webp, jpg, png)
        
    Returns:
        Dict with optimization results or error information
    """
    try:
        # Validation
        if not image_path.strip():
            return {"error": "Image path cannot be empty"}
        
        if not Path(image_path).exists():
            return {"error": f"Image file not found: {image_path}"}
        
        if not (1 <= quality <= 100):
            return {"error": "Quality must be between 1 and 100"}
        
        # Open and analyze image
        try:
            with Image.open(image_path) as img:
                original_size = os.path.getsize(image_path)
                width, height = img.size
                original_format = img.format or "JPEG"
                
                # Generate output path
                file_name, file_ext = os.path.splitext(image_path)
                output_path = f"{file_name}_optimized.{target_format.lower()}"
                
                # Format mapping
                format_map = {
                    "jpg": "JPEG", "jpeg": "JPEG", 
                    "png": "PNG", "webp": "WEBP"
                }
                save_format = format_map.get(target_format.lower(), "WEBP")
                
                # Optimization settings
                save_kwargs = {"format": save_format}
                if save_format == "JPEG":
                    save_kwargs["quality"] = quality
                    save_kwargs["optimize"] = True
                elif save_format == "WEBP":
                    save_kwargs["quality"] = quality
                    save_kwargs["method"] = 6  # Best compression
                elif save_format == "PNG":
                    save_kwargs["optimize"] = True
                
                # Save optimized image
                img.save(output_path, **save_kwargs)
                
                # Calculate savings
                optimized_size = os.path.getsize(output_path)
                size_reduction = ((original_size - optimized_size) " / " original_size) * 100
                
                return {
                    "status": "success",
                    "input_path": image_path,
                    "output_path": output_path,
                    "timestamp": datetime.now().isoformat(),
                    "optimization_results": {
                        "original_size_bytes": original_size,
                        "optimized_size_bytes": optimized_size,
                        "size_reduction_percent": round(size_reduction, 2),
                        "quality_setting": quality,
                        "format_conversion": f"{original_format} → {save_format}"
                    },
                    "technical_specs": {
                        "dimensions": {"width": width, "height": height},
                        "maintained_quality": quality >= 80
                    },
                    "metadata": {
                        "processing_time": 0.05
                    }
                }
                
        except Exception as e:
            return {"error": f"Failed to process image: {str(e)}"}
            
    except Exception as e:
        return {
            "error": f"Image optimization failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "input_path": image_path
        }


@handle_errors(operation_name="get_curated_fonts", return_dict=True)
def get_curated_fonts() -> Dict[str, Any]:
    """
    Get information about curated font collection
    
    Returns:
        Dict with font collection details
    """
    return {
        "status": "success",
        "curated_fonts": {
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
        },
        "fonts_directory": "tools" / "fonts",
        "fallback_available": True,
        "metadata": {
            "collection_curated": True,
            "professional_quality": True
        }
    }


@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for graphic design operations"""
    # Base cost for image processing
    base_cost = 0.01
    
    # Additional costs for complex operations
    if params.get("add_text", False):
        base_cost += 0.005  # Text overlay processing
    
    if params.get("crop", False):
        base_cost += 0.002  # Cropping calculations
    
    if params.get("resize", False):
        base_cost += 0.003  # Resize processing
    
    return base_cost 