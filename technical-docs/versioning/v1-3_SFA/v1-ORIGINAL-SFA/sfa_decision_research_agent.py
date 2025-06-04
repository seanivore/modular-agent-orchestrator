#!/usr/bin/env python3
# /// script
# dependencies = [
#   "anthropic>=0.17.0", 
#   "rich>=13.7.0",
#   "python-dotenv>=1.0.0",
#   "beautifulsoup4>=4.12.2",
#   "requests>=2.31.0",
#   "Pillow>=10.1.0"
# ]
# ///

import os
import sys
import json
import base64
import argparse
import asyncio
import requests
import glob as glob_module
import fnmatch
from rich.console import Console
from rich.table import Table
from anthropic import Anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from PIL import Image
import io
import datetime

# Load environment variables
load_dotenv()
console = Console()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
brave_api_key = os.getenv("BRAVE_API_KEY")
brave_subscription_token = os.getenv("X_SUBSCRIPTION_TOKEN")

# Token usage tracking
class TokenCounter:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cached_tokens = 0
        self.total_cost = 0.0
        self.cached_tokens_savings = 0.0
        
    def update(self, input_tokens, output_tokens, cached_tokens=0):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cached_tokens += cached_tokens
        
        # Calculate costs (approximate values)
        input_cost = input_tokens * 0.000003  # $3 per million tokens
        output_cost = output_tokens * 0.000015  # $15 per million tokens
        cached_cost_savings = cached_tokens * 0.000003 * 0.9  # 90% discount on cached tokens
        
        self.total_cost += input_cost + output_cost
        self.cached_tokens_savings += cached_cost_savings
        
    def display_stats(self):
        table = Table(title="Token Usage Statistics")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Cost", style="yellow")
        
        table.add_row("Input Tokens", f"{self.total_input_tokens:,}", f"${self.total_input_tokens * 0.000003:.6f}")
        table.add_row("Output Tokens", f"{self.total_output_tokens:,}", f"${self.total_output_tokens * 0.000015:.6f}")
        table.add_row("Total Tokens", f"{self.total_input_tokens + self.total_output_tokens:,}", f"${self.total_cost:.6f}")
        table.add_row("Cached Tokens", f"{self.total_cached_tokens:,}", f"Saved ${self.cached_tokens_savings:.6f}")
        
        console.print(table)

# Create token counter
token_counter = TokenCounter()

# Define tools with cache control on the last tool for prompt caching
TOOLS = [
    # Basic file tools
    {
        "name": "read_file",
        "description": "Read the content of a file from the local filesystem.",
        "input_schema": {
            "type": "object",
            "properties": {"file_path": {"type": "string"}},
            "required": ["file_path"]
        }
    },
    {
        "name": "read_multiple_files",
        "description": "Read the contents of multiple files simultaneously. This is more efficient than reading files one by one when you need to analyze or compare multiple files. Each file's content is returned with its path as a reference.",
        "input_schema": {
            "type": "object",
            "properties": {
                "paths": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "Array of file paths to read"
                }
            },
            "required": ["paths"]
        }
    },
    {
        "name": "list_directory",
        "description": "List all files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory_path": {"type": "string"},
                "pattern": {"type": "string", "default": "*.*"}
            },
            "required": ["directory_path"]
        }
    },
    {
        "name": "search_files",
        "description": "Recursively search for files and directories matching a pattern. Searches through all subdirectories from the starting path. Returns full paths to all matching items.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Starting directory path"},
                "pattern": {"type": "string", "description": "Search pattern to match files/directories"},
                "exclude_patterns": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "Patterns to exclude from results",
                    "default": []
                }
            },
            "required": ["path", "pattern"]
        }
    },
    {
        "name": "get_file_info",
        "description": "Retrieve detailed metadata about a file or directory. Returns information including size, creation time, last modified time, and type.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file or directory"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "save_output",
        "description": "Save content to the output file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "file_path": {"type": "string"}
            },
            "required": ["content", "file_path"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing text that matches the search pattern.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "search_text": {"type": "string"},
                "replace_text": {"type": "string"}
            },
            "required": ["file_path", "search_text", "replace_text"]
        }
    },
    {
        "name": "move_file",
        "description": "Move or rename a file from source to destination.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_path": {"type": "string"},
                "destination_path": {"type": "string"}
            },
            "required": ["source_path", "destination_path"]
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a file from the filesystem.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "think",
        "description": "Use this tool to think about the information you've gathered and plan your approach. It doesn't retrieve new information, but helps you process existing information and make decisions. Use when handling complex information from multiple files or when you need to organize your thoughts before taking action.",
        "input_schema": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "Your thought process"
                }
            },
            "required": ["thought"]
        }
    },
    # Decision making tool
    {
        "name": "make_decision",
        "description": "Make a decision between multiple options with reasoning. Use this to determine the next course of action or to make important choices during the workflow.",
        "input_schema": {
            "type": "object",
            "properties": {
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of available options to choose from"
                },
                "decision": {
                    "type": "string",
                    "description": "The selected option"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why this decision was made"
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Confidence level in the decision (0.0 to 1.0)"
                }
            },
            "required": ["options", "decision", "reasoning", "confidence"]
        }
    },
    # Web search tool
    {
        "name": "web_search",
        "description": "Search the web using Brave Search API to find current information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (1-5)",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    },
    # Vision tool
    {
        "name": "analyze_image",
        "description": "Analyze an image from the local filesystem. The image will be processed and its content described.",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file to analyze"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["general", "detailed", "text_extraction", "visual_elements", "subject_focus"],
                    "description": "Type of analysis to perform on the image",
                    "default": "general"
                }
            },
            "required": ["image_path"]
        }
    },
    {
        "name": "complete_task",
        "description": "Signal that the task is complete.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"}
            },
            "required": ["reason"]
        }
    }
]

# Tool implementations
async def handle_tool_call(name, tool_input):
    if name == "think":
        thought = tool_input.get("thought")
        # Show more of the thinking content (200 tokens ~ 150-250 words)
        display_length = min(len(thought), 1000)
        console.print(f"[yellow]Thinking:[/yellow] {thought[:display_length]}")
        if display_length < len(thought):
            console.print(f"[yellow]... (truncated, full thought is {len(thought)} characters)[/yellow]")
        return "Thought processed"
        
    elif name == "read_file":
        file_path = tool_input.get("file_path")
        console.print(f"[blue]Reading file:[/blue] {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    elif name == "read_multiple_files":
        paths = tool_input.get("paths", [])
        console.print(f"[blue]Reading multiple files:[/blue] {len(paths)} files")
        
        results = {}
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    results[path] = f.read()
            except Exception as e:
                results[path] = f"Error reading file: {str(e)}"
                
        return json.dumps(results, indent=2)
            
    elif name == "list_directory":
        directory_path = tool_input.get("directory_path")
        pattern = tool_input.get("pattern", "*.*")
        console.print(f"[blue]Listing directory:[/blue] {directory_path}")
        try:
            files = glob_module.glob(os.path.join(directory_path, pattern))
            return "\n".join(files)
        except Exception as e:
            return f"Error listing directory: {str(e)}"
            
    elif name == "search_files":
        path = tool_input.get("path")
        pattern = tool_input.get("pattern")
        exclude_patterns = tool_input.get("exclude_patterns", [])
        console.print(f"[blue]Searching files:[/blue] {pattern} in {path}")
        
        try:
            if not os.path.exists(path):
                return f"Error: Path '{path}' does not exist"
                
            results = []
            
            for root, dirs, files in os.walk(path):
                # Check if any part of the path matches exclude patterns
                skip = False
                for exclude in exclude_patterns:
                    if fnmatch.fnmatch(root, exclude):
                        skip = True
                        break
                if skip:
                    continue
                    
                # Process directories
                for dirname in dirs:
                    full_path = os.path.join(root, dirname)
                    if fnmatch.fnmatch(dirname, pattern) or fnmatch.fnmatch(full_path, pattern):
                        results.append(f"[DIR] {full_path}")
                
                # Process files
                for filename in files:
                    full_path = os.path.join(root, filename)
                    if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(full_path, pattern):
                        # Check excludes
                        excluded = False
                        for exclude in exclude_patterns:
                            if fnmatch.fnmatch(filename, exclude) or fnmatch.fnmatch(full_path, exclude):
                                excluded = True
                                break
                        if not excluded:
                            results.append(f"[FILE] {full_path}")
            
            # Cap results to avoid overwhelming output
            if len(results) > 50:
                return "\n".join(results[:50]) + f"\n\n... and {len(results) - 50} more results (showing first 50 only)"
            elif len(results) == 0:
                return f"No files found matching '{pattern}' in '{path}'"
            else:
                return "\n".join(results)
                
        except Exception as e:
            return f"Error searching files: {str(e)}"
            
    elif name == "get_file_info":
        path = tool_input.get("path")
        console.print(f"[blue]Getting file info:[/blue] {path}")
        
        try:
            if not os.path.exists(path):
                return f"Error: Path '{path}' does not exist"
                
            info = {}
            stats = os.stat(path)
            
            # Basic info
            info["path"] = path
            info["exists"] = True
            info["is_file"] = os.path.isfile(path)
            info["is_directory"] = os.path.isdir(path)
            info["is_symlink"] = os.path.islink(path)
            
            # Size info
            info["size_bytes"] = stats.st_size
            info["size_human"] = f"{stats.st_size / 1024:.1f} KB" if stats.st_size < 1024 * 1024 else f"{stats.st_size / (1024 * 1024):.1f} MB"
            
            # Time info
            info["created_at"] = datetime.datetime.fromtimestamp(stats.st_ctime).isoformat()
            info["modified_at"] = datetime.datetime.fromtimestamp(stats.st_mtime).isoformat()
            info["accessed_at"] = datetime.datetime.fromtimestamp(stats.st_atime).isoformat()
            
            # File type info
            if info["is_file"]:
                file_ext = os.path.splitext(path)[1].lower()
                info["extension"] = file_ext
                
                # Determine basic file type
                if file_ext in ['.txt', '.md', '.csv', '.json', '.xml', '.html', '.js', '.py', '.java', '.c', '.cpp', '.h', '.cs', '.php', '.rb', '.pl', '.sh']:
                    info["type"] = "Text/Code"
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']:
                    info["type"] = "Image"
                elif file_ext in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma']:
                    info["type"] = "Audio"
                elif file_ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']:
                    info["type"] = "Video"
                elif file_ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                    info["type"] = "Document"
                elif file_ext in ['.zip', '.rar', '.tar', '.gz', '.7z']:
                    info["type"] = "Archive"
                else:
                    info["type"] = "Other"
            
            return json.dumps(info, indent=2)
            
        except Exception as e:
            return f"Error getting file info: {str(e)}"
            
    elif name == "save_output":
        content = tool_input.get("content")
        file_path = tool_input.get("file_path")
        console.print(f"[blue]Saving to:[/blue] {file_path}")
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully saved to {file_path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
            
    elif name == "edit_file":
        file_path = tool_input.get("file_path")
        search_text = tool_input.get("search_text")
        replace_text = tool_input.get("replace_text")
        console.print(f"[blue]Editing file:[/blue] {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace the text
            new_content = content.replace(search_text, replace_text)
            
            # Save the modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            # Count replacements
            replacements = content.count(search_text)
            return f"Successfully edited {file_path} with {replacements} replacements"
        except Exception as e:
            return f"Error editing file: {str(e)}"
            
    elif name == "move_file":
        source_path = tool_input.get("source_path")
        destination_path = tool_input.get("destination_path")
        console.print(f"[blue]Moving file:[/blue] {source_path} to {destination_path}")
        try:
            import shutil
            os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            shutil.move(source_path, destination_path)
            return f"Successfully moved file from {source_path} to {destination_path}"
        except Exception as e:
            return f"Error moving file: {str(e)}"
            
    elif name == "delete_file":
        file_path = tool_input.get("file_path")
        console.print(f"[blue]Deleting file:[/blue] {file_path}")
        try:
            os.remove(file_path)
            return f"Successfully deleted {file_path}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"
            
    elif name == "make_decision":
        options = tool_input.get("options", [])
        decision = tool_input.get("decision")
        reasoning = tool_input.get("reasoning")
        confidence = tool_input.get("confidence", 0.0)
        
        # Save the decision to a JSON file for potential use in workflow branching
        decision_output = {
            "options": options,
            "decision": decision,
            "reasoning": reasoning,
            "confidence": confidence,
            "timestamp": str(datetime.datetime.now())
        }
        
        decision_path = "last_decision.json"
        with open(decision_path, 'w') as f:
            json.dump(decision_output, f, indent=2)
            
        console.print(f"[green]Decision made:[/green] {decision} (confidence: {confidence:.2f})")
        # Show more of the reasoning
        console.print(f"[blue]Reasoning:[/blue] {reasoning[:500]}..." if len(reasoning) > 500 else f"[blue]Reasoning:[/blue] {reasoning}")
        
        return json.dumps(decision_output)
    
    elif name == "web_search":
        query = tool_input.get("query")
        num_results = min(5, max(1, tool_input.get("num_results", 3)))
        console.print(f"[blue]Searching web:[/blue] {query}")
        
        try:
            api_key = brave_subscription_token or brave_api_key
            if not api_key:
                return "Error: Neither Brave API key nor X-Subscription-Token found in environment variables"
                
            headers = {"Accept": "application/json", "X-Subscription-Token": api_key}
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query, "count": num_results},
                headers=headers,
                timeout=30
            )
            
            if not response.ok:
                return f"Error: HTTP error {response.status_code} from Brave API"
                
            results = response.json().get("web", {}).get("results", [])
            
            if not results:
                return f"No results found for query: {query}"
                
            formatted_results = []
            
            for i, result in enumerate(results, 1):
                title = result.get("title", "No Title")
                url = result.get("url", "No URL")
                description = result.get("description", "No description available")
                
                # Try to get the actual content if possible
                try:
                    page_response = requests.get(url, timeout=5)
                    if page_response.ok:
                        soup = BeautifulSoup(page_response.text, 'html.parser')
                        # Extract main content (this is simplified and may need improvement)
                        content = soup.get_text(separator=' ', strip=True)
                        # Truncate to a reasonable length
                        content = content[:5000] + "..." if len(content) > 5000 else content
                    else:
                        content = description
                except Exception:
                    content = description
                    
                formatted_results.append(
                    f"[Result {i}]\nTitle: {title}\nURL: {url}\nContent:\n{content}\n"
                )
                
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
            
    elif name == "analyze_image":
        image_path = tool_input.get("image_path")
        analysis_type = tool_input.get("analysis_type", "general")
        console.print(f"[blue]Analyzing image:[/blue] {image_path} (type: {analysis_type})")
        
        try:
            if not os.path.exists(image_path):
                return f"Error: Image file not found at {image_path}"
                
            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")
                
            # Determine image format for media_type
            image_format = image_path.split(".")[-1].lower()
            if image_format == "jpg":
                image_format = "jpeg"
            media_type = f"image/{image_format}"
            
            # Get image dimensions for info
            with Image.open(image_path) as img:
                width, height = img.size
                
            # Create a simpler prompt that just passes the analysis type
            prompt = f"Please analyze this image. Analysis type: {analysis_type}. Image dimensions: {width}x{height} pixels."
            
            # Call Claude to analyze the image
            response = anthropic_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data
                                }
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )
            
            # Extract Claude's analysis
            analysis = response.content[0].text if response.content else "No analysis provided"
            
            # Include additional image metadata
            image_info = {
                "path": image_path,
                "dimensions": f"{width}x{height} pixels",
                "format": image_format.upper(),
                "size": f"{os.path.getsize(image_path) / 1024:.1f} KB",
                "analysis_type": analysis_type,
                "analysis": analysis
            }
            
            return json.dumps(image_info, indent=2)
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
            
    elif name == "complete_task":
        reason = tool_input.get("reason")
        console.print(f"[green]Task complete:[/green] {reason}")
        return f"Task completed: {reason}"
        
    return f"Unknown tool: {name}"

async def main():
    parser = argparse.ArgumentParser(description="Single-File Agent (SFA)")
    parser.add_argument("--config-file", required=True, help="Path to the JSON config file")
    parser.add_argument("--phase", type=int, default=0, help="Phase index in the config file")
    args = parser.parse_args()
    
    # Load the JSON config
    try:
        with open(args.config_file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading config file:[/red] {str(e)}")
        return
    
    # Extract the workflow key (first key that's not 'A' or 'F')
    workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F'), None)
    if not workflow_key:
        console.print("[red]Error: Invalid config file format - no workflow key found[/red]")
        return
    
    # Get the phase config
    phases = config[workflow_key]
    if args.phase >= len(phases):
        console.print(f"[red]Error: Phase index {args.phase} out of range (0-{len(phases)-1})[/red]")
        return
    
    phase_config = phases[args.phase]
    
    # Extract variables
    task = phase_config.get('U', '')
    topic = phase_config.get('X', '')
    topic_paths = phase_config.get('X_PATH', [])
    details = phase_config.get('Y', '')
    details_paths = phase_config.get('Y_PATH', [])
    output_format = phase_config.get('Z', '')
    output_path = phase_config.get('O', [])
    
    # Ensure output_path is always a list for consistent handling
    if not isinstance(output_path, list):
        output_path = [output_path]
    
    # Track which output files have been saved
    saved_outputs = set()
    
    # Prepare system message with cache control for prompt caching
    system_message = [{
        "type": "text",
        "text": task,
        "cache_control": {"type": "ephemeral"}
    }]
    
    # Prepare initial message with path information
    initial_message = f"""Topic: {topic}
Details: {details}
Output Format: {output_format}

Resources available:
"""

    # Add topic paths if available
    if topic_paths and topic_paths != ["N/A"]:
        if isinstance(topic_paths, list):
            initial_message += "Topic Resources:\n"
            for path in topic_paths:
                if path != "N/A":
                    initial_message += f"- {path}\n"
        else:
            initial_message += f"Topic Resource: {topic_paths}\n"
    
    # Add details paths if available
    if details_paths and details_paths != ["N/A"]:
        if isinstance(details_paths, list):
            initial_message += "Details Resources:\n"
            for path in details_paths:
                if path != "N/A":
                    initial_message += f"- {path}\n"
        else:
            initial_message += f"Details Resource: {details_paths}\n"
    
    # Add output path
    initial_message += f"\nYour output should be saved to: {output_path}\n"
    initial_message += "\nPlease explore these resources as needed using the provided tools. Use the 'think' tool to process complex information from multiple files before making decisions."

    # Display configuration
    console.print(f"[bold]Running SFA Phase {args.phase}[/bold]")
    console.print(f"[blue]Task:[/blue] {task}")
    console.print(f"[blue]Topic:[/blue] {topic}")
    console.print(f"[blue]Output:[/blue] {output_path}")
    
    # Start conversation with Claude
    conversation_history = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": initial_message,
            "cache_control": {"type": "ephemeral"}
        }]
    }]
    
    # Agent loop
    task_complete = False
    max_iterations = 20
    iterations = 0
    
    # Stats tracking for prompt caching
    total_tokens_saved = 0
    total_cost_saved = 0.0
    
    while not task_complete and iterations < max_iterations:
        iterations += 1
        console.rule(f"[yellow]Agent Loop {iterations}/{max_iterations}[/yellow]")
        
        try:
            # Call Claude
            console.print("[blue]Calling Claude...[/blue]")
            try:
                # Try with beta client for token-efficient-tools and prompt caching
                response = anthropic_client.beta.messages.create(
                    model="claude-3-7-sonnet-20250219",
                    system=system_message,
                    messages=conversation_history,
                    max_tokens=8192,
                    tools=TOOLS,
                    temperature=0.3,
                    betas=["token-efficient-tools-2025-02-19", "prompt-caching-2024-07-31"]
                )
            except (TypeError, ValueError, AttributeError) as e:
                # Fall back to standard client if beta not available
                console.print("[yellow]Using API without beta features...[/yellow]")
                response = anthropic_client.messages.create(
                    model="claude-3-7-sonnet-20250219",
                    system=task,
                    messages=conversation_history,
                    max_tokens=8192,
                    tools=TOOLS,
                    temperature=0.3
                )
            
            # Track cache performance metrics
            cache_creation_tokens = getattr(response.usage, 'cache_creation_input_tokens', 0)
            cache_read_tokens = getattr(response.usage, 'cache_read_input_tokens', 0)
            input_tokens = getattr(response.usage, 'input_tokens', 0)
            output_tokens = getattr(response.usage, 'output_tokens', 0)
            
            # Update token counter
            token_counter.update(
                input_tokens=input_tokens, 
                output_tokens=output_tokens,
                cached_tokens=cache_read_tokens
            )
            
            # Display running token usage
            console.print(f"[magenta]Token Usage - Current:[/magenta] Input: {input_tokens:,} | Output: {output_tokens:,}")
            console.print(f"[magenta]Token Usage - Total:[/magenta] Input: {token_counter.total_input_tokens:,} | Output: {token_counter.total_output_tokens:,} | Cost: ${token_counter.total_cost:.6f}")
            
            # Calculate savings
            if cache_read_tokens > 0:
                tokens_saved = cache_read_tokens
                cost_saved = (tokens_saved * 0.000003 * 0.9)  # 90% discount on cached tokens
                total_tokens_saved += tokens_saved
                total_cost_saved += cost_saved
                console.print(f"[green]Cache Performance:[/green] Read {cache_read_tokens} tokens from cache (saved ~${cost_saved:.6f})")
            
            if cache_creation_tokens > 0:
                console.print(f"[green]Cache Creation:[/green] Added {cache_creation_tokens} tokens to cache")
            
            # Add Claude's response to conversation history
            conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Display Claude's text responses with more content visible
            for item in response.content:
                if item.type == "text":
                    text = item.text
                    display_length = min(len(text), 500)  # Show more text
                    console.print(f"[cyan]Claude:[/cyan] {text[:display_length]}...")
                    if display_length < len(text):
                        console.print(f"[cyan]... (truncated, full response is {len(text)} characters)[/cyan]")
            
            # Check for tool use
            tool_use_items = [item for item in response.content if item.type == "tool_use"]
            
            if tool_use_items:
                for tool_item in tool_use_items:
                    tool_name = tool_item.name
                    tool_input = tool_item.input
                    tool_id = tool_item.id
                    
                    console.print(f"[blue]Tool request:[/blue] {tool_name}")
                    
                    # Execute the tool
                    tool_result = await handle_tool_call(tool_name, tool_input)
                    
                    # Check if this is a save to the output path
                    output_saved = False
                    if tool_name == "save_output":
                        saved_path = tool_input.get("file_path", "")
                        if saved_path in output_path:
                            saved_outputs.add(saved_path)
                            console.print(f"[green]Output saved to target path:[/green] {saved_path}")
                            
                            # Check if all expected outputs have been saved
                            if set(output_path).issubset(saved_outputs):
                                output_saved = True
                                console.print(f"[green]All {len(output_path)} expected outputs saved. Phase completion triggered automatically[/green]")
                            else:
                                remaining = len(output_path) - len(saved_outputs)
                                console.print(f"[yellow]Progress: {len(saved_outputs)}/{len(output_path)} outputs saved. {remaining} remaining.[/yellow]")
                    
                    # Add tool result to conversation
                    # Last user content should not be cached to allow for variation
                    conversation_history.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_id,
                                "content": tool_result
                            }
                        ]
                    })
                    
                    # Check if task complete
                    if tool_name == "complete_task" or output_saved:
                        task_complete = True
            
        except Exception as e:
            console.print(f"[red]Error in agent loop:[/red] {str(e)}")
            import traceback
            console.print(traceback.format_exc())
    
    if iterations >= max_iterations and not task_complete:
        console.print("[yellow]Reached maximum iterations without completing the task[/yellow]")
    
    # Display full token usage statistics
    token_counter.display_stats()
    
    # Display total cache savings
    if total_tokens_saved > 0:
        console.print(f"[green]Total Cache Savings:[/green] {total_tokens_saved} tokens saved (approximately ${total_cost_saved:.6f})")
    
    console.print(f"[green]Agent process completed![/green]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        console.print(f"[red]Fatal error:[/red] {str(e)}")
        console.print(traceback.format_exc())
        sys.exit(1)