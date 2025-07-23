"""
DALL-E Image Generation Tool - Core Logic
AI-powered image generation with professional workflow and error recovery
"""

import os
import json
import base64
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
import hashlib
from pathlib import Path
import time
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError, ValidationError

@handle_errors(operation_name="dalle_image_generation", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=2.0, exceptions=(requests.exceptions.RequestException, APIError))
def generate_dalle_image(prompt: str, size: str = "1024x1024", quality: str = "standard", 
                        style: str = "vivid", n: int = 1, output_dir: str = "generated_images") -> Dict[str, Any]:
    """
    Generate images using DALL-E API with comprehensive error handling
    
    Args:
        prompt: Image generation prompt
        size: Image dimensions
        quality: Image quality level
        style: Image style approach
        n: Number of images to generate
        output_dir: Output directory for images
        
    Returns:
        Dict with generation results and metadata
    """
    try:
        # Input validation
        if not prompt or not prompt.strip():
            return {"error": "Image generation prompt cannot be empty"}
        
        # Check cache first (fingerprinting) - DALL-E is expensive!
        cache = CacheManager()
        cache_key = f"{prompt.strip()}|{size}|{quality}|{style}|{n}|{output_dir}"
        cached_result = cache.get_cached_analysis(cache_key, "dalle_generation")
        if cached_result:
            return json.loads(cached_result)
        
        if len(prompt) > 4000:
            return {"error": f"Prompt too long: {len(prompt)} characters. Maximum 4000 characters allowed."}
        
        # Validate parameters
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if size not in valid_sizes:
            return {"error": f"Invalid size '{size}'. Must be one of: {', '.join(valid_sizes)}"}
        
        valid_qualities = ["standard", "hd"]
        if quality not in valid_qualities:
            return {"error": f"Invalid quality '{quality}'. Must be one of: {', '.join(valid_qualities)}"}
        
        valid_styles = ["vivid", "natural"]
        if style not in valid_styles:
            return {"error": f"Invalid style '{style}'. Must be one of: {', '.join(valid_styles)}"}
        
        if n < 1 or n > 4:
            return {"error": f"Invalid number of images '{n}'. Must be between 1 and 4."}
        
        # API Configuration
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "error": "OpenAI API key not found",
                "setup_required": "Set OPENAI_API_KEY environment variable"
            }
        
        if not api_key.startswith("sk-"):
            return {
                "error": "Invalid OpenAI API key format",
                "setup_required": "API key should start with 'sk-'"
            }
        
        # Calculate cost estimate
        estimated_cost = estimate_cost({"size": size, "quality": quality, "n": n})
        
        # Create output directory
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            return {"error": f"Permission denied creating directory: {output_dir}"}
        except Exception as dir_error:
            return {"error": f"Could not create output directory: {str(dir_error)}"}
        
        # Determine model and prepare request
        model = "dall-e-3" if size in ["1024x1024", "1792x1024", "1024x1792"] else "dall-e-2"
        
        url = "https://api.openai.com/v1/images" / "generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application" / "json",
            "User-Agent": "Mao-DALLE-Tool" / "1.0"
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
        
        # Make API request with retry logic
        max_retries = 3
        response = None
        
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        wait_time = min(retry_after, 300)  # Cap at 5 minutes
                        time.sleep(wait_time)
                        continue
                elif response.status_code == 400:
                    try:
                        error_data = response.json()
                        error_message = error_data.get('error', {}).get('message', 'Bad request')
                        return {"error": f"Request error: {error_message}"}
                    except:
                        return {"error": "Bad request. Check your prompt for policy violations."}
                elif response.status_code == 401:
                    return {"error": "Invalid API key. Check your OPENAI_API_KEY environment variable."}
                elif response.status_code == 403:
                    return {"error": "API access forbidden. Check your OpenAI account permissions."}
                else:
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 2)
                        continue
                        
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                else:
                    return {"error": f"Network error: {str(e)}"}
        
        # Check final response
        if not response or response.status_code != 200:
            try:
                error_data = response.json() if response else {}
                error_message = error_data.get('error', {}).get('message', f"HTTP {response.status_code if response else 'No response'}")
            except:
                error_message = f"HTTP {response.status_code if response else 'No response'}"
            
            return {
                "error": f"DALL-E API error: {error_message}",
                "status_code": response.status_code if response else None,
                "estimated_cost": estimated_cost
            }
        
        # Process response
        try:
            data = response.json()
        except Exception as json_error:
            return {"error": f"Could not parse API response: {str(json_error)}"}
        
        if "data" not in data or not data["data"]:
            return {"error": "No images generated by DALL-E API"}
        
        # Download and save images
        generated_images = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        download_errors = []
        
        for i, image_data in enumerate(data["data"]):
            try:
                image_url = image_data.get("url")
                if not image_url:
                    download_errors.append(f"Image {i+1}: No URL provided")
                    continue
                
                # Download image
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code != 200:
                    download_errors.append(f"Image {i+1}: Download failed (HTTP {img_response.status_code})")
                    continue
                
                # Save image
                filename = f"dalle_image_{timestamp}_{i+1}.png"
                filepath = Path(output_dir) " / " filename
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                generated_images.append({
                    "filename": filename,
                    "filepath": str(filepath),
                    "url": image_url,
                    "size_bytes": len(img_response.content),
                    "revised_prompt": image_data.get("revised_prompt", prompt)
                })
                
            except Exception as download_error:
                download_errors.append(f"Image {i+1}: {str(download_error)}")
        
        # Prepare result
        result_data = {
            "status": "success",
            "operation": "dalle_image_generation",
            "generated_images": generated_images,
            "download_errors": download_errors,
            "metadata": {
                "prompt": prompt,
                "model": model,
                "size": size,
                "quality": quality,
                "style": style,
                "requested_count": n,
                "generated_count": len(generated_images),
                "estimated_cost": estimated_cost,
                "actual_cost": estimated_cost,  # Actual cost same as estimated for successful generation
                "timestamp": datetime.now().isoformat(),
                "output_directory": output_dir
            }
        }
        
        # Save generation metadata
        try:
            metadata_file = Path(output_dir) " / " f"generation_metadata_{timestamp}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            result_data["metadata"]["metadata_file"] = str(metadata_file)
        except Exception as metadata_error:
            result_data["metadata"]["metadata_save_error"] = str(metadata_error)
        
        # Cache the result (fingerprinting) - DALL-E is expensive!
        cache.cache_content_analysis(cache_key, json.dumps(result_data), "dalle_generation")
        
        return result_data
        
    except Exception as e:
        return {
            "error": f"Image generation failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@handle_errors(operation_name="enhance_dalle_prompt", return_dict=True)
def enhance_dalle_prompt(basic_prompt: str, enhancement_approach: str = "professional", 
                        enhancement_focus: str = "quality") -> Dict[str, Any]:
    """
    Enhance a basic prompt with flexible enhancement approach and focus
    
    Args:
        basic_prompt: Original prompt to enhance
        enhancement_approach: Approach to enhancement (flexible, user-defined)
        enhancement_focus: Focus area for enhancement (flexible, user-defined)
        
    Returns:
        Dict with enhanced prompt and enhancement details
    """
    try:
        if not basic_prompt or not basic_prompt.strip():
            return {"error": "Basic prompt cannot be empty"}
        
        # Check cache first (fingerprinting)
        cache = CacheManager()
        cache_key = f"{basic_prompt.strip()}|{enhancement_approach}|{enhancement_focus}"
        cached_result = cache.get_cached_analysis(cache_key, "dalle_prompt_enhancement")
        if cached_result:
            return json.loads(cached_result)
        
        # Build enhanced prompt based on approach and focus
        enhanced_parts = [basic_prompt.strip()]
        
        # Apply enhancement based on approach
        if enhancement_approach.lower() in ["professional", "high-quality", "detailed"]:
            enhanced_parts.append("high quality, detailed, professional")
        elif enhancement_approach.lower() in ["artistic", "creative", "stylized"]:
            enhanced_parts.append("artistic, creative, stylized, expressive")
        elif enhancement_approach.lower() in ["realistic", "photorealistic", "lifelike"]:
            enhanced_parts.append("photorealistic, realistic, lifelike, detailed")
        elif enhancement_approach.lower() in ["minimal", "clean", "simple"]:
            enhanced_parts.append("clean, minimal, simple, elegant")
        
        # Apply enhancement based on focus
        if enhancement_focus.lower() in ["quality", "resolution", "clarity"]:
            enhanced_parts.append("high resolution, crisp, clear")
        elif enhancement_focus.lower() in ["lighting", "illumination", "atmosphere"]:
            enhanced_parts.append("professional lighting, good illumination")
        elif enhancement_focus.lower() in ["composition", "framing", "layout"]:
            enhanced_parts.append("well composed, good framing")
        elif enhancement_focus.lower() in ["color", "vibrant", "colorful"]:
            enhanced_parts.append("vibrant colors, rich color palette")
        
        enhanced_prompt = ", ".join(enhanced_parts)
        
        # Trim if too long while preserving meaning
        if len(enhanced_prompt) > 3800:
            enhanced_prompt = enhanced_prompt[:3800].rsplit(',', 1)[0]
            if basic_prompt not in enhanced_prompt[:len(basic_prompt) + 50]:
                # If we lost the original prompt, rebuild more conservatively
                enhanced_prompt = f"{basic_prompt}, high quality, detailed"
        
        enhancement_result = {
            "status": "success",
            "operation": "dalle_prompt_enhancement",
            "original_prompt": basic_prompt,
            "enhanced_prompt": enhanced_prompt,
            "enhancement_approach": enhancement_approach,
            "enhancement_focus": enhancement_focus,
            "enhancements_applied": {
                "approach_keywords": enhancement_approach,
                "focus_keywords": enhancement_focus,
                "prompt_length": len(enhanced_prompt),
                "original_length": len(basic_prompt)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result (fingerprinting)
        cache.cache_content_analysis(cache_key, json.dumps(enhancement_result), "dalle_prompt_enhancement")
        
        return enhancement_result
        
    except Exception as e:
        return {"error": f"Prompt enhancement failed: {str(e)}"}

@handle_errors(operation_name="validate_dalle_setup", return_dict=True)
def validate_dalle_setup() -> Dict[str, Any]:
    """
    Validate DALL-E API setup and configuration
    
    Returns:
        Dict with validation results and setup guidance
    """
    try:
        validation_result = {
            "status": "success",
            "operation": "dalle_setup_validation",
            "api_key_present": False,
            "api_key_valid_format": False,
            "setup_complete": False,
            "issues": [],
            "suggestions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check API key presence
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            validation_result["issues"].append("OPENAI_API_KEY environment variable not set")
            validation_result["suggestions"].append("Set OPENAI_API_KEY environment variable")
            validation_result["suggestions"].append("Get your API key from https://platform.openai.com" / "api-keys")
        else:
            validation_result["api_key_present"] = True
            validation_result["api_key_length"] = len(api_key)
            
            # Basic format validation
            if not api_key.startswith("sk-"):
                validation_result["issues"].append("API key format appears invalid")
                validation_result["suggestions"].append("OpenAI API keys should start with 'sk-'")
            else:
                validation_result["api_key_valid_format"] = True
            
            # Length validation
            if len(api_key) < 40:
                validation_result["issues"].append("API key appears too short")
                validation_result["suggestions"].append("Verify your complete API key")
            
            if validation_result["api_key_valid_format"] and len(api_key) >= 40:
                validation_result["setup_complete"] = True
        
        return validation_result
        
    except Exception as e:
        return {"error": f"Setup validation failed: {str(e)}"}

@handle_errors(operation_name="batch_generate_images", return_dict=True)
def batch_generate_images(prompts: List[str], shared_params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate multiple images with different prompts using shared parameters
    
    Args:
        prompts: List of prompts to generate images for
        shared_params: Shared parameters for all generations
        
    Returns:
        Dict with batch generation results
    """
    try:
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
                result = generate_dalle_image(
                    prompt=prompt,
                    size=shared_params.get("size", "1024x1024"),
                    quality=shared_params.get("quality", "standard"),
                    style=shared_params.get("style", "vivid"),
                    n=shared_params.get("n", 1),
                    output_dir=shared_params.get("output_dir", "generated_images")
                )
                
                if result.get("status") == "success":
                    successful += 1
                    total_cost += result.get("metadata", {}).get("actual_cost", 0.0)
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
            "operation": "dalle_batch_generation",
            "summary": {
                "total_prompts": len(prompts),
                "successful": successful,
                "failed": failed,
                "total_cost": total_cost,
                "average_cost_per_success": total_cost " / " successful if successful > 0 else 0
            },
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Batch generation failed: {str(e)}"}

@handle_errors(operation_name="get_dalle_image_info", return_dict=True)
def get_dalle_image_info(image_path: str) -> Dict[str, Any]:
    """
    Get information about a generated image file
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dict with image information
    """
    try:
        image_file = Path(image_path)
        
        if not image_file.exists():
            return {"error": f"Image file not found: {image_path}"}
        
        if not image_file.is_file():
            return {"error": f"Path is not a file: {image_path}"}
        
        # Get file stats
        stat = image_file.stat()
        
        image_info = {
            "status": "success",
            "operation": "dalle_image_info",
            "filepath": str(image_file.absolute()),
            "filename": image_file.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size " / " (1024 * 1024), 2),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_extension": image_file.suffix,
            "timestamp": datetime.now().isoformat()
        }
        
        # Try to get image dimensions if possible
        try:
            from PIL import Image
            with Image.open(image_file) as img:
                image_info["dimensions"] = {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode
                }
        except ImportError:
            image_info["dimensions"] = "PIL not available for dimension detection"
        except Exception as img_error:
            image_info["dimensions"] = f"Could not read image: {str(img_error)}"
        
        return image_info
        
    except Exception as e:
        return {"error": f"Image info retrieval failed: {str(e)}"}

def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Estimate cost for DALL-E image generation
    
    Args:
        params: Dict with size, quality, n parameters
        
    Returns:
        Estimated cost in USD
    """
    size = params.get("size", "1024x1024")
    quality = params.get("quality", "standard") 
    n = params.get("n", 1)
    # Cost per image based on size and quality
    cost_per_image = {
        "256x256": {"standard": 0.016, "hd": 0.018},
        "512x512": {"standard": 0.018, "hd": 0.020},
        "1024x1024": {"standard": 0.040, "hd": 0.080},
        "1792x1024": {"standard": 0.080, "hd": 0.120},
        "1024x1792": {"standard": 0.080, "hd": 0.120}
    }
    
    base_cost = cost_per_image.get(size, {}).get(quality, 0.040)
    return base_cost * n

# Capabilities moved to tool_dalle_generate.json 