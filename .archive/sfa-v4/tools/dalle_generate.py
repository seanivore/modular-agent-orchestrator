"""
DALL-E Image Generation Tool
OpenAI-powered image generation with professional workflow and error recovery
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import base64
from pathlib import Path
import time

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "dalle_generate",
        "name": "DALL-E Image Generator",
        "description": "AI-powered image generation using OpenAI's DALL-E with professional workflow and error recovery",
        "capabilities": ["image_generation", "creative_content", "visual_design", "artistic_creation"],
        "use_cases": ["marketing visuals", "concept art", "product mockups", "creative illustrations", "social media content"],
        "cost_estimate": 0.040,  # $0.040 per standard image
        "model_compatibility": ["all"],
        "tags": ["creative", "visual", "ai_generation", "premium"],
        "parameters": {
            "prompt": {"type": "string", "required": True, "description": "Image generation prompt"},
            "size": {"type": "string", "default": "1024x1024", "enum": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], "description": "Image dimensions"},
            "quality": {"type": "string", "default": "standard", "enum": ["standard", "hd"], "description": "Image quality"},
            "style": {"type": "string", "default": "vivid", "enum": ["vivid", "natural"], "description": "Image style"},
            "n": {"type": "integer", "default": 1, "min": 1, "max": 4, "description": "Number of images to generate"},
            "output_dir": {"type": "string", "default": "generated_images", "description": "Output directory for images"}
        },
        "functions": ["generate_image", "generate_variations", "enhance_prompt", "batch_generate"]
    }

def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard", 
                   style: str = "vivid", n: int = 1, output_dir: str = "generated_images") -> Dict[str, Any]:
    """Generate images using DALL-E with comprehensive error handling and safety features"""
    try:
        # Input validation with detailed error messages
        if not prompt.strip():
            return {"error": "Image generation prompt cannot be empty"}
        
        if len(prompt) > 4000:
            return {"error": f"Prompt too long: {len(prompt)} characters. Maximum 4000 characters allowed."}
        
        # Validate parameters with comprehensive checks
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if size not in valid_sizes:
            return {"error": f"Invalid size '{size}'. Must be one of: {', '.join(valid_sizes)}"}
        
        valid_qualities = ["standard", "hd"]
        if quality not in valid_qualities:
            return {"error": f"Invalid quality '{quality}'. Must be one of: {', '.join(valid_qualities)}"}
        
        valid_styles = ["vivid", "natural"]
        if style not in valid_styles:
            return {"error": f"Invalid style '{style}'. Must be one of: {', '.join(valid_styles)}"}
        
        # Clamp number of images with validation
        if n < 1 or n > 4:
            return {"error": f"Invalid number of images '{n}'. Must be between 1 and 4."}
        
        # API Configuration with comprehensive error handling
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "error": "OpenAI API key not found. Set OPENAI_API_KEY environment variable",
                "instructions": "Get your API key from https://platform.openai.com/api-keys"
            }
        
        # Basic API key format validation
        if not api_key.startswith("sk-"):
            return {
                "error": "Invalid OpenAI API key format. Key should start with 'sk-'",
                "instructions": "Verify your API key from https://platform.openai.com/api-keys"
            }
        
        # Calculate cost estimate with detailed breakdown
        cost_per_image = {
            "256x256": {"standard": 0.016, "hd": 0.018},
            "512x512": {"standard": 0.018, "hd": 0.020},
            "1024x1024": {"standard": 0.040, "hd": 0.080},
            "1792x1024": {"standard": 0.080, "hd": 0.120},
            "1024x1792": {"standard": 0.080, "hd": 0.120}
        }
        
        base_cost = cost_per_image.get(size, {}).get(quality, 0.040)
        estimated_cost = base_cost * n
        
        # Create output directory with error handling
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            return {"error": f"Permission denied creating directory: {output_dir}"}
        except Exception as dir_error:
            return {"error": f"Could not create output directory: {str(dir_error)}"}
        
        # Determine model based on size (DALL-E 3 for larger images)
        model = "dall-e-3" if size in ["1024x1024", "1792x1024", "1024x1792"] else "dall-e-2"
        
        # API request configuration
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "SFA-v4-DALLE-Tool/1.0"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "n": min(n, 1) if model == "dall-e-3" else n,  # DALL-E 3 only supports n=1
            "size": size,
            "response_format": "url"
        }
        
        # Add DALL-E 3 specific parameters
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
        
        # Make API request with retry logic and enhanced error handling
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=120
                )
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        wait_time = min(retry_after, 300)  # Cap at 5 minutes
                        time.sleep(wait_time)
                        continue
                elif response.status_code == 400:
                    # Bad request - likely prompt issue
                    try:
                        error_data = response.json()
                        error_message = error_data.get('error', {}).get('message', 'Bad request')
                        return {"error": f"Request error: {error_message}"}
                    except:
                        return {"error": f"Bad request (HTTP 400). Check your prompt for policy violations."}
                elif response.status_code == 401:
                    return {"error": "Invalid API key. Check your OPENAI_API_KEY environment variable."}
                elif response.status_code == 403:
                    return {"error": "API access forbidden. Check your OpenAI account permissions."}
                else:
                    last_error = f"HTTP {response.status_code}"
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 2)
                        continue
                        
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {str(e)}"
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
        
        # Check final response
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
            except:
                error_message = last_error or f"HTTP {response.status_code}"
            
            return {
                "error": f"DALL-E API error: {error_message}",
                "status_code": response.status_code,
                "estimated_cost": estimated_cost
            }
        
        # Process response with error handling
        try:
            data = response.json()
        except Exception as json_error:
            return {"error": f"Could not parse API response: {str(json_error)}"}
        
        if "data" not in data or not data["data"]:
            return {"error": "No images generated by DALL-E API"}
        
        # Download and save images with comprehensive error handling
        generated_images = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        download_errors = []
        
        # Handle multiple images for DALL-E 3 (generate multiple times if n > 1)
        images_to_process = data["data"]
        if model == "dall-e-3" and n > 1:
            # For DALL-E 3, we need to make multiple requests for n > 1
            for additional_request in range(n - 1):
                try:
                    additional_response = requests.post(url, headers=headers, json=payload, timeout=120)
                    if additional_response.status_code == 200:
                        additional_data = additional_response.json()
                        if additional_data.get("data"):
                            images_to_process.extend(additional_data["data"])
                    else:
                        download_errors.append(f"Additional image {additional_request + 2} failed: HTTP {additional_response.status_code}")
                except Exception as additional_error:
                    download_errors.append(f"Additional image {additional_request + 2} failed: {str(additional_error)}")
        
        # Process and download all images
        for i, image_data in enumerate(images_to_process):
            image_url = image_data.get("url")
            if not image_url:
                download_errors.append(f"Image {i+1}: No URL provided")
                continue
            
            try:
                # Download image with timeout and retry
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    # Generate safe filename
                    safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_prompt = safe_prompt.replace(' ', '_')
                    if not safe_prompt:
                        safe_prompt = "generated"
                    
                    filename = f"dalle_{safe_prompt}_{timestamp}_{i+1}.png"
                    filepath = Path(output_dir) / filename
                    
                    # Save image
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    # Verify file was saved correctly
                    if not filepath.exists() or filepath.stat().st_size == 0:
                        download_errors.append(f"Image {i+1}: File save verification failed")
                        continue
                    
                    # Get image info
                    image_size_bytes = len(img_response.content)
                    
                    generated_images.append({
                        "filename": filename,
                        "filepath": str(filepath),
                        "url": image_url,
                        "size_bytes": image_size_bytes,
                        "size_kb": round(image_size_bytes / 1024, 1),
                        "dimensions": size,
                        "prompt": prompt,
                        "model": model,
                        "quality": quality if model == "dall-e-3" else "standard",
                        "style": style if model == "dall-e-3" else "default"
                    })
                else:
                    download_errors.append(f"Image {i+1}: Download failed (HTTP {img_response.status_code})")
                    
            except Exception as download_error:
                download_errors.append(f"Image {i+1}: {str(download_error)}")
        
        if not generated_images:
            return {
                "error": "Failed to download any generated images",
                "download_errors": download_errors,
                "estimated_cost": estimated_cost
            }
        
        # Calculate actual cost based on successful generations
        actual_cost = base_cost * len(generated_images)
        
        # Create comprehensive result data
        result_data = {
            "status": "success",
            "prompt": prompt,
            "parameters": {
                "size": size,
                "quality": quality,
                "style": style,
                "model": model,
                "requested_count": n,
                "actual_count": len(generated_images)
            },
            "images": generated_images,
            "timestamp": datetime.now().isoformat(),
            "output_directory": output_dir,
            "estimated_cost": estimated_cost,
            "actual_cost": actual_cost,
            "cost_savings": estimated_cost - actual_cost if estimated_cost > actual_cost else 0,
            "metadata": {
                "total_size_kb": sum(img["size_kb"] for img in generated_images),
                "generation_time": f"Generated via {model}",
                "download_errors": download_errors if download_errors else None
            }
        }
        
        # Save generation metadata with error handling
        try:
            metadata_file = Path(output_dir) / f"generation_metadata_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            result_data["metadata"]["metadata_file"] = str(metadata_file)
        except Exception as metadata_error:
            result_data["metadata"]["metadata_save_error"] = str(metadata_error)
        
        return result_data
        
    except Exception as e:
        return {
            "error": f"Image generation failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def enhance_prompt(basic_prompt: str, style_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
    """Enhance a basic prompt with professional image generation techniques"""
    try:
        if not basic_prompt.strip():
            return {"error": "Basic prompt cannot be empty"}
        
        # Style enhancement templates
        style_templates = {
            "photorealistic": "photorealistic, high quality, detailed, professional photography, sharp focus, good lighting",
            "artistic": "artistic, creative, stylized, expressive, high quality artwork",
            "minimalist": "clean, minimalist, simple, elegant, uncluttered, modern design",
            "vintage": "vintage style, retro, classic, nostalgic, aged appearance",
            "modern": "modern, contemporary, sleek, professional, clean design",
            "fantasy": "fantasy art, magical, ethereal, imaginative, detailed illustration",
            "corporate": "professional, business, corporate style, clean, modern, polished",
            "cinematic": "cinematic lighting, dramatic, movie-like, professional cinematography",
            "sketch": "pencil sketch, hand-drawn, artistic sketch, detailed line art"
        }
        
        # Quality enhancers
        quality_enhancers = [
            "high resolution",
            "detailed",
            "high quality",
            "professional",
            "crisp",
            "clear",
            "masterpiece"
        ]
        
        # Lighting suggestions
        lighting_options = {
            "natural": "natural lighting, soft daylight",
            "dramatic": "dramatic lighting, high contrast, cinematic lighting",
            "soft": "soft lighting, gentle shadows, diffused light",
            "studio": "studio lighting, professional photography lighting",
            "golden": "golden hour lighting, warm sunset light",
            "ambient": "ambient lighting, atmospheric"
        }
        
        # Default style if none provided
        style_prefs = style_preferences or {
            "style": "photorealistic", 
            "quality": "high", 
            "lighting": "natural"
        }
        
        # Build enhanced prompt
        enhanced_parts = [basic_prompt]
        
        # Add style template
        style = style_prefs.get("style", "photorealistic")
        if style in style_templates:
            enhanced_parts.append(style_templates[style])
        
        # Add quality enhancers
        quality_level = style_prefs.get("quality", "high")
        if quality_level == "high":
            enhanced_parts.extend(quality_enhancers[:4])
        elif quality_level == "medium":
            enhanced_parts.extend(quality_enhancers[:2])
        elif quality_level == "maximum":
            enhanced_parts.extend(quality_enhancers)
        
        # Add lighting
        lighting = style_prefs.get("lighting", "natural")
        if lighting in lighting_options:
            enhanced_parts.append(lighting_options[lighting])
        
        # Add composition suggestions
        composition = style_prefs.get("composition")
        if composition:
            composition_templates = {
                "portrait": "portrait composition, centered subject",
                "landscape": "landscape composition, wide angle",
                "closeup": "close-up shot, detailed focus",
                "fullbody": "full body shot, complete figure"
            }
            if composition in composition_templates:
                enhanced_parts.append(composition_templates[composition])
        
        enhanced_prompt = ", ".join(enhanced_parts)
        
        # Trim if too long while preserving meaning
        if len(enhanced_prompt) > 3800:  # Leave room for final touches
            # Smart truncation - remove from the end but keep core prompt
            enhanced_prompt = enhanced_prompt[:3800].rsplit(',', 1)[0]
            if not basic_prompt in enhanced_prompt[:len(basic_prompt) + 50]:
                # If we lost the original prompt, rebuild more conservatively
                enhanced_parts = [basic_prompt, style_templates.get(style, ""), quality_enhancers[0]]
                enhanced_prompt = ", ".join(filter(None, enhanced_parts))
        
        return {
            "status": "success",
            "original_prompt": basic_prompt,
            "enhanced_prompt": enhanced_prompt,
            "style_applied": style,
            "enhancements": {
                "style_template": style_templates.get(style, ""),
                "quality_level": quality_level,
                "lighting_type": lighting,
                "composition": style_prefs.get("composition"),
                "prompt_length": len(enhanced_prompt)
            },
            "suggestions": {
                "alternative_styles": list(style_templates.keys()),
                "size_recommendations": {
                    "social_media_square": "1024x1024",
                    "social_media_story": "1024x1792", 
                    "banner_wide": "1792x1024",
                    "profile_picture": "512x512",
                    "thumbnail": "256x256"
                },
                "quality_options": ["medium", "high", "maximum"],
                "lighting_options": list(lighting_options.keys())
            }
        }
        
    except Exception as e:
        return {"error": f"Prompt enhancement failed: {str(e)}"}

def validate_api_key() -> Dict[str, Any]:
    """Validate OpenAI API key availability and basic format"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "valid": False,
            "error": "API key not found",
            "instructions": "Set OPENAI_API_KEY environment variable. Get your key from https://platform.openai.com/api-keys"
        }
    
    # Basic format validation
    if not api_key.startswith("sk-"):
        return {
            "valid": False,
            "error": "Invalid API key format",
            "instructions": "OpenAI API keys should start with 'sk-'. Verify your key from https://platform.openai.com/api-keys"
        }
    
    # Length validation (OpenAI keys are typically 51+ characters)
    if len(api_key) < 40:
        return {
            "valid": False,
            "error": "API key appears too short",
            "instructions": "Verify your complete API key from https://platform.openai.com/api-keys"
        }
    
    return {
        "valid": True,
        "key_length": len(api_key),
        "key_prefix": api_key[:7] + "..." if len(api_key) > 7 else "short_key",
        "format": "Valid OpenAI format",
        "instructions": "API key format is valid. Test with a generation to verify permissions."
    }

def batch_generate(prompts: List[str], shared_params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate multiple images with different prompts using shared parameters"""
    if not prompts:
        return {"error": "No prompts provided for batch generation"}
    
    if len(prompts) > 10:
        return {"error": f"Too many prompts: {len(prompts)}. Maximum 10 prompts per batch."}
    
    shared_params = shared_params or {}
    results = []
    successful = 0
    failed = 0
    total_cost = 0.0
    
    for i, prompt in enumerate(prompts):
        try:
            result = generate_image(
                prompt=prompt,
                size=shared_params.get("size", "1024x1024"),
                quality=shared_params.get("quality", "standard"),
                style=shared_params.get("style", "vivid"),
                n=shared_params.get("n", 1),
                output_dir=shared_params.get("output_dir", "generated_images")
            )
            
            if result.get("status") == "success":
                successful += 1
                total_cost += result.get("actual_cost", 0.0)
            else:
                failed += 1
            
            results.append({
                "prompt_index": i,
                "prompt": prompt,
                "result": result
            })
            
            # Small delay between requests to avoid rate limiting
            if i < len(prompts) - 1:
                time.sleep(1)
                
        except Exception as e:
            failed += 1
            results.append({
                "prompt_index": i,
                "prompt": prompt,
                "result": {"error": str(e)}
            })
    
    return {
        "status": "completed",
        "summary": {
            "total_prompts": len(prompts),
            "successful": successful,
            "failed": failed,
            "total_cost": total_cost,
            "average_cost_per_success": total_cost / successful if successful > 0 else 0
        },
        "results": results,
        "timestamp": datetime.now().isoformat()
    }