"""
DALL-E IMAGE GENERATION
Human Button Generators
"""

import json
from typing import Dict, Any, List

def create_button_snippet(prompt: str, size: str = "1024x1024", quality: str = "standard", 
                                  style: str = "vivid", n: int = 1, output_dir: str = "generated_images",
                                  model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for DALL-E image generation
    
    Args:
        prompt: Image generation prompt
        size: Image dimensions
        quality: Image quality level
        style: Image style approach
        n: Number of images to generate
        output_dir: Output directory for images
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    
    # Core DALL-E generation code
    core_code = f'''
import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def generate_dalle_image():
    """Generate images using DALL-E API with comprehensive error handling"""
    try:
        # Configuration
        prompt = """{prompt}"""
        size = "{size}"
        quality = "{quality}"
        style = "{style}"
        n = {n}
        output_dir = "{output_dir}"
        
        # Input validation
        if not prompt.strip():
            return {{"error": "Image generation prompt cannot be empty"}}
        
        if len(prompt) > 4000:
            return {{"error": f"Prompt too long: {{len(prompt)}} characters. Maximum 4000 characters allowed."}}
        
        # Validate parameters
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if size not in valid_sizes:
            return {{"error": f"Invalid size '{{size}}'. Must be one of: {{', '.join(valid_sizes)}}"}}
        
        valid_qualities = ["standard", "hd"]
        if quality not in valid_qualities:
            return {{"error": f"Invalid quality '{{quality}}'. Must be one of: {{', '.join(valid_qualities)}}"}}
        
        valid_styles = ["vivid", "natural"]
        if style not in valid_styles:
            return {{"error": f"Invalid style '{{style}}'. Must be one of: {{', '.join(valid_styles)}}"}}
        
        if n < 1 or n > 4:
            return {{"error": f"Invalid number of images '{{n}}'. Must be between 1 and 4."}}
        
        # API Configuration
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {{
                "error": "OpenAI API key not found",
                "setup_required": "Set OPENAI_API_KEY environment variable"
            }}
        
        if not api_key.startswith("sk-"):
            return {{
                "error": "Invalid OpenAI API key format",
                "setup_required": "API key should start with 'sk-'"
            }}
        
        # Calculate cost estimate
        cost_per_image = {{
            "256x256": {{"standard": 0.016, "hd": 0.018}},
            "512x512": {{"standard": 0.018, "hd": 0.020}},
            "1024x1024": {{"standard": 0.040, "hd": 0.080}},
            "1792x1024": {{"standard": 0.080, "hd": 0.120}},
            "1024x1792": {{"standard": 0.080, "hd": 0.120}}
        }}
        
        base_cost = cost_per_image.get(size, {{}}).get(quality, 0.040)
        estimated_cost = base_cost * n
        
        # Create output directory
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            return {{"error": f"Permission denied creating directory: {{output_dir}}"}}
        except Exception as dir_error:
            return {{"error": f"Could not create output directory: {{str(dir_error)}}"}}
        
        # Determine model and prepare request
        model = "dall-e-3" if size in ["1024x1024", "1792x1024", "1024x1792"] else "dall-e-2"
        
        url = "https://api.openai.com/v1/images / generations"
        headers = {{
            "Authorization": f"Bearer {{api_key}}",
            "Content-Type": "application / json",
            "User-Agent": "Mao-DALLE-Tool / 1.0"
        }}
        
        payload = {{
            "model": model,
            "prompt": prompt,
            "n": min(n, 1) if model == "dall-e-3" else n,  # DALL-E 3 only supports n=1
            "size": size,
            "response_format": "url"
        }}
        
        # Add DALL-E 3 specific parameters
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
        
        if HAS_RICH and console:
            console.print(f"[blue]🎨 Generating {{n}} image(s) with DALL-E...[ / blue]")
            console.print(f"[cyan]📐 Size:[/cyan] {{size}} | [cyan]Quality:[/cyan] {{quality}} | [cyan]Style:[ / cyan] {{style}}")
            console.print(f"[yellow]💰 Estimated cost:[ / yellow] ${{estimated_cost:.3f}}")
        else:
            print(f"🎨 Generating {{n}} image(s) with DALL-E...")
            print(f"📐 Size: {{size}} | Quality: {{quality}} | Style: {{style}}")
            print(f"💰 Estimated cost: ${{estimated_cost:.3f}}")
        
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
                        if HAS_RICH and console:
                            console.print(f"[yellow]⏳ Rate limited, waiting {{wait_time}} seconds...[ / yellow]")
                        else:
                            print(f"⏳ Rate limited, waiting {{wait_time}} seconds...")
                        time.sleep(wait_time)
                        continue
                elif response.status_code == 400:
                    try:
                        error_data = response.json()
                        error_message = error_data.get('error', {{}}).get('message', 'Bad request')
                        return {{"error": f"Request error: {{error_message}}"}}
                    except:
                        return {{"error": "Bad request. Check your prompt for policy violations."}}
                elif response.status_code == 401:
                    return {{"error": "Invalid API key. Check your OPENAI_API_KEY environment variable."}}
                elif response.status_code == 403:
                    return {{"error": "API access forbidden. Check your OpenAI account permissions."}}
                else:
                    if attempt < max_retries - 1:
                        if HAS_RICH and console:
                            console.print(f"[yellow]⚠️  Request failed (HTTP {{response.status_code}}), retrying...[ / yellow]")
                        else:
                                                         print(f"⚠️  Request failed (HTTP {{response.status_code}}), retrying...")
                        time.sleep((attempt + 1) * 2)
                        continue
                        
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    if HAS_RICH and console:
                        console.print(f"[yellow]⏳ Request timeout, retrying...[ / yellow]")
                    else:
                        print(f"⏳ Request timeout, retrying...")
                    time.sleep(5)
                    continue
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    if HAS_RICH and console:
                        console.print(f"[red]🌐 Network error, retrying...[ / red]")
                    else:
                        print(f"🌐 Network error, retrying...")
                    time.sleep(3)
                    continue
                else:
                    return {{"error": f"Network error: {{str(e)}}"}}
        
        # Check final response
        if not response or response.status_code != 200:
            try:
                error_data = response.json() if response else {{}}
                error_message = error_data.get('error', {{}}).get('message', f"HTTP {{response.status_code if response else 'No response'}}")
            except:
                error_message = f"HTTP {{response.status_code if response else 'No response'}}"
            
            return {{
                "error": f"DALL-E API error: {{error_message}}",
                "status_code": response.status_code if response else None,
                "estimated_cost": estimated_cost
            }}
        
        # Process response
        try:
            data = response.json()
        except Exception as json_error:
            return {{"error": f"Could not parse API response: {{str(json_error)}}"}}
        
        if "data" not in data or not data["data"]:
            return {{"error": "No images generated by DALL-E API"}}
        
        # Download and save images
        generated_images = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        download_errors = []
        
        if HAS_RICH and console:
            console.print(f"[blue]📥 Downloading {{len(data['data'])}} image(s)...[ / blue]")
        else:
                         print(f"📥 Downloading {{len(data['data'])}} image(s)...")
        
        for i, image_data in enumerate(data["data"]):
            try:
                image_url = image_data.get("url")
                if not image_url:
                    download_errors.append(f"Image {{i+1}}: No URL provided")
                    continue
                
                # Download image
                if HAS_RICH and console:
                    console.print(f"[blue]📥 Downloading image {{i+1}} / {{len(data['data'])}}...[ / blue]")
                else:
                                         print(f"📥 Downloading image {{i+1}} / {{len(data['data'])}}...")
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code != 200:
                    download_errors.append(f"Image {{i+1}}: Download failed (HTTP {{img_response.status_code}})")
                    continue
                
                # Save image
                filename = f"dalle_image_{{timestamp}}_{{i+1}}.png"
                filepath = Path(output_dir)  /  filename
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                generated_images.append({{
                    "filename": filename,
                    "filepath": str(filepath),
                    "url": image_url,
                    "size_bytes": len(img_response.content),
                    "revised_prompt": image_data.get("revised_prompt", prompt)
                }})
                
                if HAS_RICH and console:
                    console.print(f"[green]✅ Saved: {{filename}} ({{len(img_response.content):,}} bytes)[ / green]")
                else:
                                         print(f"✅ Saved: {{filename}} ({{len(img_response.content):,}} bytes)")
                
            except Exception as download_error:
                download_errors.append(f"Image {{i+1}}: {{str(download_error)}}")
        
        # Prepare result
        result_data = {{
            "status": "success",
            "operation": "dalle_image_generation",
            "generated_images": generated_images,
            "download_errors": download_errors,
            "metadata": {{
                "prompt": prompt,
                "model": model,
                "size": size,
                "quality": quality,
                "style": style,
                "requested_count": n,
                "generated_count": len(generated_images),
                "estimated_cost": estimated_cost,
                "actual_cost": estimated_cost,
                "timestamp": datetime.now().isoformat(),
                "output_directory": output_dir
            }}
        }}
        
        # Save generation metadata
        try:
            metadata_file = Path(output_dir)  /  f"generation_metadata_{{timestamp}}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            result_data["metadata"]["metadata_file"] = str(metadata_file)
            if HAS_RICH and console:
                console.print(f"[blue]📄 Metadata saved: {{metadata_file.name}}[ / blue]")
            else:
                                 print(f"📄 Metadata saved: {{metadata_file.name}}")
        except Exception as metadata_error:
            result_data["metadata"]["metadata_save_error"] = str(metadata_error)
        
        # Display results
        if HAS_RICH and console:
            console.print(f"[green]\\n🎨 Generation complete![" / "green]")
            console.print(f"[green]✅ Generated {{len(generated_images)}} image(s)[ / green]")
            console.print(f"[yellow]💰 Total cost: ${{estimated_cost:.3f}}[ / yellow]")
            console.print(f"[blue]📁 Output directory: {{output_dir}}[ / blue]")
        else:
                         print(f"\\n🎨 Generation complete!")
             print(f"✅ Generated {{len(generated_images)}} image(s)")
             print(f"💰 Total cost: ${{estimated_cost:.3f}}")
             print(f"📁 Output directory: {{output_dir}}")
        
        if download_errors:
            if HAS_RICH and console:
                console.print(f"[yellow]⚠️  {{len(download_errors)}} download error(s):[ / yellow]")
            else:
                                 print(f"⚠️  {{len(download_errors)}} download error(s):")
            for error in download_errors:
                if HAS_RICH and console:
                    console.print(f"   • [red]{{error}}[ / red]")
                else:
                                         print(f"   • {{error}}")
        
        return result_data
        
    except Exception as e:
        return {{
            "error": f"Image generation failed: {{str(e)}}",
            "timestamp": datetime.now().isoformat()
        }}

# Execute the generation
result = generate_dalle_image()

# Display final result
if result.get("error"):
    if HAS_RICH and console:
        console.print(f"[red]\\n❌ Error: {{result[')error']}}[ / red]"
    else:
             print(f"\\n❌ Error: {{result[')error']}}"
     if result.get("setup_required"):
         if HAS_RICH and console:
             console.print(f"[yellow]💡 Setup: {{result['setup_required']}}[ / yellow]")
         else:
             print(f"💡 Setup: {{result['setup_required']}}")
else:
    if HAS_RICH and console:
        console.print(f"[green]\\n🎉 DALL-E generation successful![" / "green]")
    else:
        print(f"\n🎉 DALL-E generation successful!")
    if HAS_RICH and console:
        console.print(f"[blue]📊 Result: {{json.dumps(result, indent=2)}}[ / blue]")
    else:
        print(f"📊 Result: {{json.dumps(result, indent=2)}}")
'''
    
    return core_code.strip()

def create_dalle_enhancement_button(basic_prompt: str, enhancement_approach: str = "professional",
                                   enhancement_focus: str = "quality", model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for DALL-E prompt enhancement
    
    Args:
        basic_prompt: Original prompt to enhance
        enhancement_approach: Approach to enhancement
        enhancement_focus: Focus area for enhancement
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    
    core_code = f'''
import json
from datetime import datetime

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def enhance_dalle_prompt():
    """Enhance a basic prompt with flexible enhancement approach and focus"""
    try:
        basic_prompt = """{basic_prompt}"""
        enhancement_approach = "{enhancement_approach}"
        enhancement_focus = "{enhancement_focus}"
        
        if not basic_prompt.strip():
            return {{"error": "Basic prompt cannot be empty"}}
        
        # Build enhanced prompt based on approach and focus
        enhanced_parts = [basic_prompt.strip()]
        
        if HAS_RICH and console:
            console.print(f"[blue]✨ Enhancing prompt with approach: {{enhancement_approach}}[ / blue]")
            console.print(f"[cyan]🎯 Focus area: {{enhancement_focus}}[ / cyan]")
        else:
            print(f"✨ Enhancing prompt with approach: {{enhancement_approach}}")
            print(f"🎯 Focus area: {{enhancement_focus}}")
        
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
                enhanced_prompt = f"{{basic_prompt}}, high quality, detailed"
        
        result = {{
            "status": "success",
            "operation": "dalle_prompt_enhancement",
            "original_prompt": basic_prompt,
            "enhanced_prompt": enhanced_prompt,
            "enhancement_approach": enhancement_approach,
            "enhancement_focus": enhancement_focus,
            "enhancements_applied": {{
                "approach_keywords": enhancement_approach,
                "focus_keywords": enhancement_focus,
                "prompt_length": len(enhanced_prompt),
                "original_length": len(basic_prompt)
            }},
            "timestamp": datetime.now().isoformat()
        }}
        
        # Display results
        if HAS_RICH and console:
            console.print(f"[blue]\\n📝 Original prompt ({{len(basic_prompt)}} chars):[" / "blue]")
                            console.print(f"   [cyan]{{basic_prompt}}[ / cyan]")
            console.print(f"[blue]\\n✨ Enhanced prompt ({{len(enhanced_prompt)}} chars):[" / "blue]")
            console.print(f"   [cyan]{{enhanced_prompt}}[ / cyan]")
            console.print(f"[blue]\\n📊 Enhancement complete![" / "blue]")
        else:
            print(f"\\n📝 Original prompt ({{len(basic_prompt)}} chars):")
            print(f"   {{basic_prompt}}")
            print(f"\\n✨ Enhanced prompt ({{len(enhanced_prompt)}} chars):")
            print(f"   {{enhanced_prompt}}")
            print(f"\\n📊 Enhancement complete!")
        
        return result
        
    except Exception as e:
        return {{"error": f"Prompt enhancement failed: {{str(e)}}"}}

# Execute the enhancement
result = enhance_dalle_prompt()

# Display final result
if result.get("error"):
    if HAS_RICH and console:
        console.print(f"[red]\\n❌ Error: {{result[')error']}}[ / red]"
    else:
        print(f"\\n❌ Error: {{result[')error']}}"
else:
    if HAS_RICH and console:
        console.print(f"[green]\\n🎉 Prompt enhancement successful![" / "green]")
    else:
        print(f"\\n🎉 Prompt enhancement successful!")
    if HAS_RICH and console:
        console.print(f"[blue]📊 Result: {{json.dumps(result, indent=2)}}[ / blue]")
    else:
        print(f"📊 Result: {{json.dumps(result, indent=2)}}")
'''
    
    return core_code.strip()

def create_dalle_validation_button(model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for DALL-E setup validation
    
    Args:
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    
    core_code = '''
import os
import json
from datetime import datetime

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def validate_dalle_setup():
    """Validate DALL-E API setup and configuration"""
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
        
        if HAS_RICH and console:
            console.print("🔑 Validating DALL-E setup...")
        else:
            print("🔑 Validating DALL-E setup...")
        
        # Check API key presence
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            validation_result["issues"].append("OPENAI_API_KEY environment variable not set")
            validation_result["suggestions"].append("Set OPENAI_API_KEY environment variable")
            validation_result["suggestions"].append("Get your API key from https://platform.openai.com / api-keys")
            if HAS_RICH and console:
                console.print("❌ API key not found")
            else:
                print("❌ API key not found")
        else:
            validation_result["api_key_present"] = True
            validation_result["api_key_length"] = len(api_key)
            if HAS_RICH and console:
                console.print("✅ API key found")
            else:
                print("✅ API key found")
            
            # Basic format validation
            if not api_key.startswith("sk-"):
                validation_result["issues"].append("API key format appears invalid")
                validation_result["suggestions"].append("OpenAI API keys should start with 'sk-'")
                if HAS_RICH and console:
                    console.print("❌ Invalid API key format")
                else:
                    print("❌ Invalid API key format")
            else:
                validation_result["api_key_valid_format"] = True
                if HAS_RICH and console:
                    console.print("✅ API key format valid")
                else:
                    print("✅ API key format valid")
            
            # Length validation
            if len(api_key) < 40:
                validation_result["issues"].append("API key appears too short")
                validation_result["suggestions"].append("Verify your complete API key")
                if HAS_RICH and console:
                    console.print("⚠️  API key appears short")
                else:
                    print("⚠️  API key appears short")
            
            if validation_result["api_key_valid_format"] and len(api_key) >= 40:
                validation_result["setup_complete"] = True
                if HAS_RICH and console:
                    console.print("✅ Setup appears complete")
                else:
                    print("✅ Setup appears complete")
        
        # Display results
        if HAS_RICH and console:
            console.print(f"[blue]\\n📊 Validation Summary:[" / "blue]")
            console.print(f"   [cyan]API Key Present:[ / cyan] {{'✅' if validation_result['api_key_present'] else '❌'}}")
            console.print(f"   [cyan]Format Valid:[ / cyan] {{'✅' if validation_result['api_key_valid_format'] else '❌'}}")
            console.print(f"   [cyan]Setup Complete:[ / cyan] {{'✅' if validation_result['setup_complete'] else '❌'}}")
        else:
            print(f"\\n📊 Validation Summary:")
            print(f"   API Key Present: {{'✅' if validation_result['api_key_present'] else '❌'}}")
            print(f"   Format Valid: {{'✅' if validation_result['api_key_valid_format'] else '❌'}}")
            print(f"   Setup Complete: {{'✅' if validation_result['setup_complete'] else '❌'}}")
        
        if validation_result["issues"]:
            if HAS_RICH and console:
                console.print(f"[red]\\n🚨 Issues found:[" / "red]")
            else:
                print(f"\\n🚨 Issues found:")
            for issue in validation_result["issues"]:
                if HAS_RICH and console:
                    console.print(f"   • [red]{{issue}}[ / red]")
                else:
                    print(f"   • {{issue}}")
        
        if validation_result["suggestions"]:
            if HAS_RICH and console:
                console.print(f"[yellow]\\n💡 Suggestions:[" / "yellow]")
            else:
                print(f"\\n💡 Suggestions:")
            for suggestion in validation_result["suggestions"]:
                if HAS_RICH and console:
                    console.print(f"   • [yellow]{{suggestion}}[ / yellow]")
                else:
                    print(f"   • {{suggestion}}")
        
        return validation_result
        
    except Exception as e:
        return {"error": f"Setup validation failed: {str(e)}"}

# Execute the validation
result = validate_dalle_setup()

# Display final result
if result.get("error"):
    if HAS_RICH and console:
        console.print(f"[red]\\n❌ Error: {{result[')error']}}[ / red]"
    else:
        print(f"\\n❌ Error: {{result[')error']}}"
else:
    if HAS_RICH and console:
        console.print(f"[green]\\n🎉 Validation complete![" / "green]")
    else:
        print(f"\\n🎉 Validation complete!")
    if HAS_RICH and console:
        console.print(f"[blue]📊 Result: {{json.dumps(result, indent=2)}}[ / blue]")
    else:
        print(f"📊 Result: {{json.dumps(result, indent=2)}}")
'''
    
    return core_code.strip()

def create_dalle_batch_button(prompts: List[str], shared_params: Dict[str, Any] = None,
                             model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for DALL-E batch generation
    
    Args:
        prompts: List of prompts to generate images for
        shared_params: Shared parameters for all generations
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    
    shared_params = shared_params or {}
    prompts_json = json.dumps(prompts)
    params_json = json.dumps(shared_params)
    
    core_code = f'''
import os
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def batch_generate_images():
    """Generate multiple images with different prompts using shared parameters"""
    try:
        prompts = {prompts_json}
        shared_params = {params_json}
        
        if not prompts:
            return {{"error": "No prompts provided for batch generation"}}
        
        if len(prompts) > 10:
            return {{"error": f"Too many prompts: {{len(prompts)}}. Maximum 10 prompts per batch."}}
        
        if HAS_RICH and console:
            console.print(f"[blue]🎨 Starting batch generation for {{len(prompts)}} prompts...[ / blue]")
        else:
            print(f"🎨 Starting batch generation for {{len(prompts)}} prompts...")
        
        results = []
        successful = 0
        failed = 0
        total_cost = 0.0
        
        for i, prompt in enumerate(prompts):
            try:
                if HAS_RICH and console:
                    console.print(f"[blue]\\n📝 Processing prompt {{i+1}}/{{len(prompts)}}: {{prompt[:50]}}...[" / "blue]")
                else:
                    print(f"\\n📝 Processing prompt {{i+1}}" / "{{len(prompts)}}: {{prompt[:50]}}...")
                
                # Use the same generation logic as single image generation
                result = generate_single_image(
                    prompt=prompt,
                    size=shared_params.get("size", "1024x1024"),
                    quality=shared_params.get("quality", "standard"),
                    style=shared_params.get("style", "vivid"),
                    n=shared_params.get("n", 1),
                    output_dir=shared_params.get("output_dir", "generated_images")
                )
                
                if result.get("status") == "success":
                    successful += 1
                    total_cost += result.get("metadata", {{}}).get("actual_cost", 0.0)
                    if HAS_RICH and console:
                        console.print(f"[green]✅ Success: {{len(result.get('generated_images', []))}} image(s)[ / green]")
                    else:
                                                print(f"✅ Success: {{len(result.get('generated_images', []))}} image(s)")
                    else:
                        failed += 1
                        if HAS_RICH and console:
                            console.print(f"[red]❌ Failed: {{result.get('error', 'Unknown error')}}[ / red]")
                        else:
                            print(f"❌ Failed: {{result.get('error', 'Unknown error')}}")
                
                results.append({{
                    "prompt_index": i,
                    "prompt": prompt,
                    "result": result
                }})
                
                # Small delay between requests to avoid rate limiting
                if i < len(prompts) - 1:
                    if HAS_RICH and console:
                        console.print("[yellow]⏳ Waiting 1 second to avoid rate limits...[ / yellow]")
                    else:
                        print("⏳ Waiting 1 second to avoid rate limits...")
                    time.sleep(1)
                    
            except Exception as e:
                failed += 1
                if HAS_RICH and console:
                    console.print(f"[red]❌ Exception: {{str(e)}}[ / red]")
                else:
                    print(f"❌ Exception: {{str(e)}}")
                results.append({{
                    "prompt_index": i,
                    "prompt": prompt,
                    "result": {{"error": str(e)}}
                }})
        
        batch_result = {{
            "status": "completed",
            "operation": "dalle_batch_generation",
            "summary": {{
                "total_prompts": len(prompts),
                "successful": successful,
                "failed": failed,
                "total_cost": total_cost,
                "average_cost_per_success": total_cost  /  successful if successful > 0 else 0
            }},
            "results": results,
            "timestamp": datetime.now().isoformat()
        }}
        
        # Display summary
        if HAS_RICH and console:
            console.print(f"[green]\\n🎉 Batch generation complete![" / "green]")
        else:
            print(f"\\n🎉 Batch generation complete!")
        if HAS_RICH and console:
            console.print(f"[blue]�� Summary:[ / blue]")
        else:
            print(f"\\n📊 Summary:")
        if HAS_RICH and console:
            console.print(f"   [cyan]Total prompts:[ / cyan] {{len(prompts)}}")
        else:
            print(f"   Total prompts: {{len(prompts)}}")
        if HAS_RICH and console:
            console.print(f"   [green]Successful:[ / green] {{successful}}")
        else:
            print(f"   Successful: {{successful}}")
        if HAS_RICH and console:
            console.print(f"   [red]Failed:[ / red] {{failed}}")
        else:
            print(f"   Failed: {{failed}}")
        if HAS_RICH and console:
            console.print(f"[yellow]Total cost:[ / yellow] ${{total_cost:.3f}}")
        else:
            print(f"   Total cost: ${{total_cost:.3f}}")
        if successful > 0:
            if HAS_RICH and console:
                console.print(f"   [yellow]Average cost per success:[/yellow] ${{total_cost  /  successful:.3f}}")
            else:
                print(f"   Average cost per success: ${{total_cost  /  successful:.3f}}")
        
        return batch_result
        
    except Exception as e:
        return {{"error": f"Batch generation failed: {{str(e)}}"}}

def generate_single_image(prompt, size, quality, style, n, output_dir):
    """Generate a single image (simplified version of main generation function)"""
    # API Configuration
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {{"error": "OpenAI API key not found"}}
    
    # Calculate cost
    cost_per_image = {{
        "256x256": {{"standard": 0.016, "hd": 0.018}},
        "512x512": {{"standard": 0.018, "hd": 0.020}},
        "1024x1024": {{"standard": 0.040, "hd": 0.080}},
        "1792x1024": {{"standard": 0.080, "hd": 0.120}},
        "1024x1792": {{"standard": 0.080, "hd": 0.120}}
    }}
    base_cost = cost_per_image.get(size, {{}}).get(quality, 0.040)
    estimated_cost = base_cost * n
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Determine model
    model = "dall-e-3" if size in ["1024x1024", "1792x1024", "1024x1792"] else "dall-e-2"
    
    # API request
    url = "https://api.openai.com/v1/images / generations"
    headers = {{
        "Authorization": f"Bearer {{api_key}}",
        "Content-Type": "application / json"
    }}
    
    payload = {{
        "model": model,
        "prompt": prompt,
        "n": min(n, 1) if model == "dall-e-3" else n,
        "size": size,
        "response_format": "url"
    }}
    
    if model == "dall-e-3":
        payload["quality"] = quality
        payload["style"] = style
    
    # Make request
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    if response.status_code != 200:
        return {{"error": f"API error: HTTP {{response.status_code}}"}}
    
    data = response.json()
    if "data" not in data:
        return {{"error": "No images generated"}}
    
    # Download images
    generated_images = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for i, image_data in enumerate(data["data"]):
        image_url = image_data.get("url")
        if image_url:
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                filename = f"dalle_batch_{{timestamp}}_{{i+1}}.png"
                filepath = Path(output_dir)  /  filename
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                generated_images.append({{
                    "filename": filename,
                    "filepath": str(filepath),
                    "size_bytes": len(img_response.content)
                }})
    
    return {{
        "status": "success",
        "generated_images": generated_images,
        "metadata": {{
            "actual_cost": estimated_cost,
            "model": model
        }}
    }}

# Execute the batch generation
result = batch_generate_images()

# Display final result
if result.get("error"):
    if HAS_RICH and console:
        console.print(f"[red]\\n❌ Error: {{result[')error']}}[ / red]"
    else:
        print(f"\\n❌ Error: {{result[')error']}}"
else:
    if HAS_RICH and console:
        console.print(f"[green]\\n🎉 Batch generation successful![" / "green]")
    else:
        print(f"\\n🎉 Batch generation successful!")
    if HAS_RICH and console:
        console.print(f"[blue]📊 Result: {{json.dumps(result, indent=2)}}[ / blue]")
    else:
        print(f"📊 Result: {{json.dumps(result, indent=2)}}")
'''
    
    return core_code.strip()

def create_dalle_capabilities_button(model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet to display DALL-E capabilities
    
    Args:
        model: Target model for execution
        
    Returns:
        Executable code snippet
    """
    
    core_code = '''
import json

# Rich import with fallback for graceful degradation
try:
    from rich.console import Console
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def get_dalle_capabilities():
    """Get information about DALL-E capabilities and limitations"""
    capabilities = {
        "operations": [
            "generate_dalle_image",
            "enhance_dalle_prompt", 
            "validate_dalle_setup",
            "batch_generate_images",
            "get_dalle_image_info"
        ],
        "supported_models": [
            "dall-e-2",
            "dall-e-3"
        ],
        "supported_sizes": [
            "256x256",
            "512x512",
            "1024x1024", 
            "1792x1024",
            "1024x1792"
        ],
        "supported_qualities": [
            "standard",
            "hd"
        ],
        "supported_styles": [
            "vivid",
            "natural"
        ],
        "features": [
            "image_generation",
            "prompt_enhancement",
            "batch_processing",
            "cost_estimation",
            "error_recovery",
            "metadata_tracking",
            "file_management"
        ],
        "limitations": {
            "requires_api_key": True,
            "max_prompt_length": 4000,
            "max_images_per_request": 4,
            "max_batch_size": 10,
            "dalle3_single_image_only": True,
            "rate_limits": "subject_to_openai_api_limits"
        },
        "cost_structure": {
            "currency": "USD",
            "size_quality_costs": {
                "256x256_standard": 0.016,
                "256x256_hd": 0.018,
                "512x512_standard": 0.018,
                "512x512_hd": 0.020,
                "1024x1024_standard": 0.040,
                "1024x1024_hd": 0.080,
                "1792x1024_standard": 0.080,
                "1792x1024_hd": 0.120,
                "1024x1792_standard": 0.080,
                "1024x1792_hd": 0.120
            }
        }
    }
    
    # Display capabilities
    if HAS_RICH and console:
        console.print("🎨 DALL-E Capabilities & Limitations")
        console.print("=" * 50)
    else:
        print("🎨 DALL-E Capabilities & Limitations")
        print("=" * 50)
    
    if HAS_RICH and console:
        console.print(r"\\n🔧 Available Operations:")
    else:
        print(r"\\n🔧 Available Operations:")
    for op in capabilities["operations"]:
        if HAS_RICH and console:
            console.print(f"   • [cyan]{{op}}[ / cyan]")
        else:
            print(f"   • {{op}}")
    
    if HAS_RICH and console:
        console.print(f"\\n🤖 Supported Models: {{'), '.join(capabilities['supported_models'])}}"
    else:
        print(f"\\n🤖 Supported Models: {{'), '.join(capabilities['supported_models'])}}"
    if HAS_RICH and console:
        console.print(f"✨ Features: {{', '.join(capabilities['features'])}}")
    else:
        print(f"✨ Features: {{', '.join(capabilities['features'])}}")
    
    if HAS_RICH and console:
        console.print(r"\\n📐 Supported Sizes:")
    else:
        print(r"\\n📐 Supported Sizes:")
    for size in capabilities["supported_sizes"]:
        if HAS_RICH and console:
            console.print(f"   • [cyan]{{size}}[ / cyan]")
        else:
            print(f"   • {{size}}")
    
    if HAS_RICH and console:
        console.print(f"\\n🎭 Quality Levels: {{'), '.join(capabilities['supported_qualities'])}}"
    else:
        print(f"\\n🎭 Quality Levels: {{'), '.join(capabilities['supported_qualities'])}}"
    if HAS_RICH and console:
        console.print(f"🎨 Style Options: {{', '.join(capabilities['supported_styles'])}}")
    else:
        print(f"🎨 Style Options: {{', '.join(capabilities['supported_styles'])}}")
    
    if HAS_RICH and console:
        console.print(r"\\n⚠️  Limitations:")
    else:
        print(r"\\n⚠️  Limitations:")
    for key, value in capabilities["limitations"].items():
        if HAS_RICH and console:
            console.print(f"   • [yellow]{{key.replace('_', ' ').title()}}:[/yellow] [cyan]{{value}}[ / cyan]")
        else:
            print(f"   • {{key.replace('_', ' ').title()}}: {{value}}")
    
    if HAS_RICH and console:
        console.print(r"\\n💰 Cost Structure (USD):")
    else:
        print(r"\\n💰 Cost Structure (USD):")
    costs = capabilities["cost_structure"]["size_quality_costs"]
    for size_quality, cost in costs.items():
        if HAS_RICH and console:
            console.print(f"   • [cyan]{{size_quality.replace('_', ' ')}}:[/cyan] [yellow]${{cost:.3f}}[ / yellow]")
        else:
            print(f"   • {{size_quality.replace('_', ' ')}}: ${{cost:.3f}}")
    
    return capabilities

# Execute and display capabilities
result = get_dalle_capabilities()
if HAS_RICH and console:
    console.print(f"\\n📊 Full capabilities data: [blue]{{json.dumps(result, indent=2)}}[" / "blue]")
else:
    print(f"\\n📊 Full capabilities data: {{json.dumps(result, indent=2)}}")
'''
    
    return core_code.strip()

def get_dalle_button_metadata() -> Dict[str, Any]:
    """
    Get metadata about available DALL-E human buttons
    
    Returns:
        Dict with button metadata
    """
    return {
        "available_buttons": [
            "create_dalle_generation_button",
            "create_dalle_enhancement_button", 
            "create_dalle_validation_button",
            "create_dalle_batch_button",
            "create_dalle_capabilities_button"
        ],
        "button_descriptions": {
            "create_dalle_generation_button": "Generate images using DALL-E API",
            "create_dalle_enhancement_button": "Enhance prompts for better image generation",
            "create_dalle_validation_button": "Validate DALL-E API setup and configuration",
            "create_dalle_batch_button": "Generate multiple images with different prompts",
            "create_dalle_capabilities_button": "Display DALL-E capabilities and limitations"
        },
        "supported_models": [
            "claude-sonnet-4",
            "claude-haiku",
            "gpt-4",
            "gpt-3.5-turbo",
            "gemini-pro"
        ],
        "features": [
            "universal_model_compatibility",
            "self_contained_execution",
            "comprehensive_error_handling",
            "cost_tracking",
            "progress_indicators",
            "retry_logic",
            "metadata_generation"
        ]
    }