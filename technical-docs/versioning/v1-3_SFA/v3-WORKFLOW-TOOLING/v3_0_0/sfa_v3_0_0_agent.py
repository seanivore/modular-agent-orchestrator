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
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

# Initialize global conversation history
conversation_history = []

# Load available tools
available_tools = {}
tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
if os.path.exists(tools_dir):
    sys.path.append(tools_dir)
    
    # Try to load token counter tool
    try:
        from token_counter import count_text_tokens, count_file_tokens
        
        def token_counter_tool(text=None, file_path=None, dir_path=None):
            """Count tokens in text or files."""
            if text:
                token_count = count_text_tokens(text)
                return {
                    "token_count": token_count,
                    "is_safe": token_count < 7500 and token_count > 0,
                    "status": "success"
                }
            elif file_path:
                return count_file_tokens(file_path)
            else:
                return {
                    "token_count": 0,
                    "is_safe": False,
                    "status": "error: No input provided"
                }
                
        available_tools["token_counter"] = token_counter_tool
        console.print("[green]Token counter tool loaded successfully[/green]")
        
    except ImportError:
        console.print("[yellow]Token counter tool not found[/yellow]")
        
    # Try to load task reporting tool
    try:
        from task_reporting import task_report
        available_tools["task_report"] = task_report
        console.print("[green]Task reporting tool loaded successfully[/green]")
    except ImportError:
        console.print("[yellow]Task reporting tool not found[/yellow]")

# Token usage tracking
class TokenCounter:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cached_tokens = 0
        self.total_cache_creation_tokens = 0
        self.total_cost = 0.0
        self.cached_tokens_savings = 0.0
        self.cache_creation_extra_cost = 0.0
        self.cumulative_tokens = 0
        self.cumulative_cost = 0.0
        
    def update(self, input_tokens, output_tokens, cached_tokens=0, cache_creation_tokens=0):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cached_tokens += cached_tokens
        self.total_cache_creation_tokens += cache_creation_tokens
        
        # Calculate costs (approximate values)
        base_input_cost = 0.000003  # $3 per million tokens
        input_cost = input_tokens * base_input_cost
        output_cost = output_tokens * 0.000015  # $15 per million tokens
        cached_cost_savings = cached_tokens * base_input_cost * 0.9  # 90% discount on cached tokens
        
        # Add 25% extra cost for cache creation tokens
        cache_creation_cost = cache_creation_tokens * base_input_cost
        cache_creation_premium = cache_creation_tokens * base_input_cost * 0.25  # 25% premium
        self.cache_creation_extra_cost += cache_creation_premium
        
        self.total_cost += input_cost + output_cost + cache_creation_cost + cache_creation_premium
        self.cached_tokens_savings += cached_cost_savings
        
    def display_stats(self):
        """Display token usage statistics in a cleaner format."""
        table = Table(title="Token Usage")
        
        table.add_column("Tokens", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Cost", style="yellow")
        
        # Input tokens
        input_cost = self.total_input_tokens * 0.000003  # $3 per million tokens
        table.add_row("Input", f"{self.total_input_tokens:,}", f"– ${input_cost:.6f}")
        
        # Output tokens
        output_cost = self.total_output_tokens * 0.000015  # $15 per million tokens
        table.add_row("Output", f"{self.total_output_tokens:,}", f"– ${output_cost:.6f}")
        
        # Cached savings if any
        if self.total_cached_tokens > 0:
            cached_savings = self.cached_tokens_savings
            table.add_row("Cached Savings", f"{self.total_cached_tokens:,}", f"+ ${cached_savings:.6f}")
        
        # Phase totals
        phase_tokens = self.total_input_tokens + self.total_output_tokens
        phase_cost = input_cost + output_cost - self.cached_tokens_savings
        table.add_row("Phase", f"{phase_tokens:,}", f"– ${phase_cost:.6f}")
        
        # Calculate and store cumulative totals
        if hasattr(self, 'cumulative_tokens'):
            self.cumulative_tokens += phase_tokens
            self.cumulative_cost += phase_cost
        else:
            self.cumulative_tokens = phase_tokens
            self.cumulative_cost = phase_cost
        
        table.add_row("Workflow", f"{self.cumulative_tokens:,}", f"– ${self.cumulative_cost:.6f}")
        
        console.print(table)
        
        # No more "Phase completed" text - the horizontal line handles that visually

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
    # Text editor tool
    {
        "name": "text_editor",
        "description": "Powerful text editor for creating and modifying files. Supports multiple operations including viewing files, making targeted replacements, inserting text at specific lines, and creating new files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string", 
                    "enum": ["view", "str_replace", "insert", "create"],
                    "description": "The operation to perform on the file"
                },
                "path": {
                    "type": "string",
                    "description": "Path to the file to edit or create"
                },
                "old_str": {
                    "type": "string", 
                    "description": "Text to replace (required for str_replace command)"
                },
                "new_str": {
                    "type": "string",
                    "description": "New text to insert (required for str_replace command)"
                },
                "line_number": {
                    "type": "integer",
                    "description": "Line where to insert text (required for insert command)"
                },
                "file_text": {
                    "type": "string",
                    "description": "Content for the new file (required for create command)"
                }
            },
            "required": ["command", "path"]
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
    },
    # Perplexity search tool
    {
        "name": "perplexity_search",
        "description": "Search using Perplexity AI to get detailed, source-backed answers to complex questions. This provides more thorough research and deeper context than regular web search.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The research question or query to investigate"
                },
                "focus": {
                    "type": "string",
                    "enum": ["academic", "normal", "concise", "creative"],
                    "description": "The focus mode for the search",
                    "default": "normal"
                }
            },
            "required": ["query"]
        }
    },
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
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    elif name == "read_multiple_files":
        paths = tool_input.get("paths", [])
        
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
        try:
            files = glob_module.glob(os.path.join(directory_path, pattern))
            return "\n".join(files)
        except Exception as e:
            return f"Error listing directory: {str(e)}"
            
    elif name == "search_files":
        path = tool_input.get("path")
        pattern = tool_input.get("pattern")
        exclude_patterns = tool_input.get("exclude_patterns", [])
        
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
        
        # Check token count before saving
        if "token_counter" in available_tools:
            try:
                # Print a small preview of the content to help with debugging
                preview_length = min(100, len(content) if content else 0)
                console.print(f"[blue]Content preview:[/blue] {content[:preview_length]}...")
                
                # Count tokens
                token_result = available_tools["token_counter"](text=content)
                console.print(f"[blue]Token count result:[/blue] {json.dumps(token_result, indent=2)}")
                
                if not token_result["is_safe"]:
                    # Check for specific error cases
                    if token_result["token_count"] == 0:
                        console.print("[yellow]Warning:[/yellow] Token count returned 0 tokens. This may indicate an error or empty content.")
                        # If content seems non-empty but token count is 0, attempt to save anyway
                        if content and len(content.strip()) > 0:
                            console.print("[yellow]Content seems non-empty but token count is 0. Attempting to save anyway.[/yellow]")
                            # Proceed to save below
                        else:
                            return f"ERROR: Empty content. Nothing to save to {file_path}."
                    else:
                        console.print(f"[yellow]Warning:[/yellow] Content exceeds safe token limit ({token_result['token_count']} tokens)")
                        console.print("[yellow]Asking Claude to optimize content before saving...[/yellow]")
                        
                        # Create a message asking Claude to optimize the content
                        optimization_message = f"⚠️ CRITICAL: Your content ({token_result['token_count']} tokens) exceeds the safe limit (7000 tokens). **The file will NOT be saved until the content is optimized to under 7000 tokens.** Please optimize your content by: (1) Identifying verbose sections that can be condensed. (2) Rewriting those sections to be more concise while preserving key information. (3) Checking the token count again using the token_counter tool. (4) Saving the optimized version only when it's under 7000 tokens. This is not optional - if you don't optimize the content, the file will save as empty (0 bytes) or get truncated. Your valuable work will be lost. Once optimized, call save_output again with the optimized content to successfully save to {file_path}."
                        
                        # Don't modify the conversation directly - instead return the message so it's handled properly
                        return f"ERROR: Content exceeds token limit ({token_result['token_count']} tokens). File NOT saved. {optimization_message}"
            except Exception as e:
                console.print(f"[yellow]Error in token counting:[/yellow] {str(e)}")
                # Continue with save attempt despite token counting error
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # Check if content is non-empty before saving
            if content and len(content.strip()) > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully saved to {file_path}"
            else:
                console.print("[red]Error:[/red] Cannot save empty content.")
                return f"Error: Attempt to save empty content to {file_path}. File NOT saved."
        except Exception as e:
            return f"Error saving file: {str(e)}"
            
    elif name == "edit_file":
        file_path = tool_input.get("file_path")
        search_text = tool_input.get("search_text")
        replace_text = tool_input.get("replace_text")
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
        try:
            import shutil
            os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            shutil.move(source_path, destination_path)
            return f"Successfully moved file from {source_path} to {destination_path}"
        except Exception as e:
            return f"Error moving file: {str(e)}"
            
    elif name == "delete_file":
        file_path = tool_input.get("file_path")
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
            
    elif name == "text_editor":
        """Handle text editor tool commands: view, str_replace, insert, create."""
        command = tool_input.get("command")
        path = tool_input.get("path")
        
        try:
            # Command: view - Read and return file content
            if command == "view":
                if not os.path.exists(path):
                    return f"Error: File '{path}' not found"
                    
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return content
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            
            # Command: str_replace - Replace text in a file
            elif command == "str_replace":
                old_str = tool_input.get("old_str")
                new_str = tool_input.get("new_str")
                
                if not old_str or new_str is None:
                    return "Error: Both old_str and new_str are required for str_replace"
                    
                if not os.path.exists(path):
                    return f"Error: File '{path}' not found"
                    
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if the old_str exists in the file
                    if old_str not in content:
                        return f"Error: Text '{old_str}' not found in '{path}'"
                    
                    # Perform the replacement
                    new_content = content.replace(old_str, new_str)
                    
                    # Check token count if token_counter is available
                    if "token_counter" in available_tools:
                        token_result = available_tools["token_counter"](text=new_content)
                        if not token_result["is_safe"]:
                            return f"Error: The resulting content would exceed the token limit ({token_result['token_count']} tokens). Please make smaller edits."
                    
                    # Save the modified content
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    # Count replacements
                    replacements = content.count(old_str)
                    return f"Successfully replaced '{old_str}' with '{new_str}' in '{path}' ({replacements} occurrences)"
                except Exception as e:
                    return f"Error performing str_replace: {str(e)}"
            
            # Command: insert - Insert text at a specific line
            elif command == "insert":
                line_number = tool_input.get("line_number")
                new_str = tool_input.get("new_str")
                
                if line_number is None or new_str is None:
                    return "Error: Both line_number and new_str are required for insert"
                    
                if not os.path.exists(path):
                    return f"Error: File '{path}' not found"
                    
                try:
                    # Read the file content as lines
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Check if line_number is valid
                    if line_number < 0 or line_number > len(lines):
                        return f"Error: Line number {line_number} is out of range (0-{len(lines)})"
                    
                    # Add newline to the inserted text if needed
                    if not new_str.endswith('\n'):
                        new_str += '\n'
                    
                    # Insert the new text
                    lines.insert(line_number, new_str)
                    new_content = ''.join(lines)
                    
                    # Check token count if token_counter is available
                    if "token_counter" in available_tools:
                        token_result = available_tools["token_counter"](text=new_content)
                        if not token_result["is_safe"]:
                            return f"Error: The resulting content would exceed the token limit ({token_result['token_count']} tokens). Please make smaller edits."
                    
                    # Save the modified content
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    return f"Successfully inserted text at line {line_number} in '{path}'"
                except Exception as e:
                    return f"Error performing insert: {str(e)}"
            
            # Command: create - Create a new file
            elif command == "create":
                file_text = tool_input.get("file_text")
                
                if file_text is None:
                    return "Error: file_text is required for create"
                    
                try:
                    # Check token count if token_counter is available
                    if "token_counter" in available_tools:
                        token_result = available_tools["token_counter"](text=file_text)
                        if not token_result["is_safe"]:
                            return f"Error: The content exceeds the token limit ({token_result['token_count']} tokens). Please reduce content size."
                    
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                    
                    # Create the file
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(file_text)
                    
                    return f"Successfully created file '{path}'"
                except Exception as e:
                    return f"Error creating file: {str(e)}"
            
            else:
                return f"Error: Unsupported command '{command}'"
                
        except Exception as e:
            return f"Error in text_editor tool: {str(e)}"
            
    elif name == "complete_task":
        reason = tool_input.get("reason")
        console.print(f"[green]Task complete:[/green] {reason}")
        return f"Task completed: {reason}"
    
    elif name == "perplexity_search":
        query = tool_input.get("query")
        focus = tool_input.get("focus", "normal")
        
        try:
            if not perplexity_api_key:
                return "Error: Perplexity API key not found in environment variables. Set the PERPLEXITY_API_KEY variable."
                
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {perplexity_api_key}"
            }
            
            # Create appropriate system message based on focus mode
            system_message = """At the end of each task generate a task report using the task_report tool:

1. Verify token counts to save content:
   - 7,500 tokens max; any more and the document will save empty 
   - If content exceeds the limit, revise it to be more concise

2. Include in task report:
   - Summary of accomplishments
   - Key findings or insights
   - Challenges encountered; how they were addressed

3. Include specific Next Steps for the following phase:
   - Clearly define what happens next
   - Provide actionable recommendations
   - Include all necessary context 

4. If your task involved making a decision, structure it like this:

   decision = {
       "options": ["Option 1", "Option 2", "Option 3"],
       "choice": "Option 2",
       "reasoning": "Detailed explanation for choosing Option 2..."
   }

5. Call the task_report tool with all required information:

   task_report(
       content=your_content,
       file_paths=["/path/to/output.md"],
       report="Detailed summary of accomplishments...",
       next_steps="Specific recommendations for the next phase...",
       decision={...}  # Optional, include if your task involved making a decision
   )

The task_report tool will:
- Verify token counts are within limits
- Save your content to the specified file paths
- Generate a structured JSON report for the workflow system
- Signal task completion automatically when all outputs are saved"""
            
            # Create the payload
            payload = {
                "model": "sonar-pro-online",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ]
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if not response.ok:
                return f"Error: HTTP error {response.status_code} from Perplexity API: {response.text}"
            
            response_data = response.json()
            
            # Extract the main content from the response
            if "choices" in response_data and len(response_data["choices"]) > 0:
                answer = response_data["choices"][0]["message"]["content"]
                
                # Extract citations if available
                citations = response_data.get("citations", [])
                citation_text = ""
                
                if citations:
                    citation_text = "\n\n## Sources\n"
                    for i, citation in enumerate(citations, 1):
                        title = citation.get("title", "No Title")
                        url = citation.get("url", "No URL")
                        citation_text += f"{i}. [{title}]({url})\n"
                
                return f"{answer}{citation_text}"
            else:
                return "Error: Could not extract answer from Perplexity response"
                
        except Exception as e:
            return f"Error performing Perplexity search: {str(e)}"
    
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
    
    # Check if phases is a dictionary with labeled tasks (new format)
    if isinstance(phases, dict):
        # Get all the task labels
        task_labels = list(phases.keys())
        
        # Check if the phase index is valid
        if args.phase >= len(task_labels):
            console.print(f"[red]Error: Phase index {args.phase} out of range (0-{len(task_labels)-1})[/red]")
            return
        
        # Get the label for the current phase
        current_task_label = task_labels[args.phase]
        
        # Get the phase configuration for the current task
        phase_config = phases[current_task_label][0]  # Get the first item in the task's array
        
        # Store total number of phases for display
        num_phases = len(task_labels)
    else:
        # Legacy format (array of phases)
        if args.phase >= len(phases):
            console.print(f"[red]Error: Phase index {args.phase} out of range (0-{len(phases)-1})[/red]")
            return
        
        phase_config = phases[args.phase]
        
        # Store total number of phases for display
        num_phases = len(phases)
    
    # Extract variables
    task = phase_config.get('U', '')
    topic = phase_config.get('X', '')
    topic_paths = phase_config.get('X_PATH', [])
    details = phase_config.get('Y', '')
    details_paths = phase_config.get('Y_PATH', [])
    output_format = phase_config.get('Z', '')
    output_path = phase_config.get('O', [])
    
    # Make all tools available by default
    tools_for_phase = available_tools.copy()
    
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
    
    # Add information about available tools
    if tools_for_phase:
        initial_message += "\nAvailable Tools:\n"
        if "token_counter" in tools_for_phase:
            initial_message += """- token_counter: Use this to check token counts before saving
  - Call with: tools["token_counter"](text="your text") or tools["token_counter"](file_path="path/to/file")
  - Returns a dictionary with: token_count, is_safe (boolean), status, and message
  - Example: result = tools["token_counter"](file_path=output_path[0])
  - Always check if the content is safe to save with: if result["is_safe"]
"""
        # Add text_editor tool documentation
        initial_message += """- text_editor: Advanced text editor with multiple commands:
  - text_editor(command="view", path="/path/to/file.txt") - View file content
  - text_editor(command="str_replace", path="/path/to/file.txt", old_str="text to replace", new_str="new text") - Replace text
  - text_editor(command="insert", path="/path/to/file.txt", line_number=10, new_str="text to insert") - Insert at specific line
  - text_editor(command="create", path="/path/to/newfile.txt", file_text="content") - Create new file
"""
    
    initial_message += "\nPlease explore these resources as needed using the provided tools. Use the 'think' tool to process complex information from multiple files before making decisions."

    # Function to truncate text to a specific length
    def truncate_text(text, max_length=100):
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    # Format relative paths for display
    def format_path(path):
        # Convert paths to relative if they're absolute
        cwd = os.getcwd()
        if path.startswith(cwd):
            return "." + path[len(cwd):]
        return path
    
    # Improved display configuration with half-width horizontal rule
    console.print("───────────────────────")
    console.print(f"Workflow: `{workflow_key}`")
    console.print(f"Agent: `{phase_config.get('S', ['sfa_agent.py'])[0]}`")
    console.print(f"Phase: {args.phase+1} of {num_phases}")
    console.print("───────────────────────")
    
    # Display output paths in a cleaner format
    console.print("Output: ")
    for path in output_path:
        console.print(f"- {format_path(path)}")
    
    # Display truncated task and topic
    console.print(f"Task: {truncate_text(task)}")
    console.print(f"Topic: {truncate_text(topic)}")
    
    # Start conversation with Claude
    global conversation_history
    conversation_history = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": initial_message,
            "cache_control": {"type": "ephemeral"}
        }]
    }]
    
    # Create a global tools variable for the agent to use
    globals()["tools"] = tools_for_phase
    
    # Agent loop
    task_complete = False
    max_iterations = 20
    iterations = 0
    
    # Stats tracking for prompt caching
    total_tokens_saved = 0
    total_cost_saved = 0.0
    
    while not task_complete and iterations < max_iterations:
        iterations += 1
        # Full-width horizontal rule for loop iterations
        console.print(f"─────────────────────────────  Loop {iterations}/{max_iterations}  ─────────────────────────────")
        
        try:
            # Call Claude
            console.print("[cyan]Claude:[/cyan]")
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
                cached_tokens=cache_read_tokens,
                cache_creation_tokens=cache_creation_tokens
            )
            
            # Add Claude's response to conversation history
            conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Display Claude's text responses with more content visible (but still compact)
            for item in response.content:
                if item.type == "text":
                    text = item.text
                    # Show more text (300 words is approximately 100-400 tokens)
                    display_length = min(len(text), 1500)
                    claude_text = text[:display_length]
                    if display_length < len(text):
                        claude_text += "..."
                    console.print(f"{claude_text}")
            
            # Check for tool use
            tool_use_items = [item for item in response.content if item.type == "tool_use"]
            
            if tool_use_items:
                for tool_item in tool_use_items:
                    tool_name = tool_item.name
                    tool_input = tool_item.input
                    tool_id = tool_item.id
                    
                    console.print(f"[blue]Tool:[/blue] {tool_name}")
                    
                    # Format tool operation for display in a more compact way
                    if tool_name == "read_file":
                        file_path = tool_input.get("file_path", "")
                        console.print(f"[blue]Reading:[/blue] {format_path(file_path)}")
                    elif tool_name == "save_output":
                        file_path = tool_input.get("file_path", "")
                        console.print(f"[blue]Saving:[/blue] {format_path(file_path)}")
                    elif tool_name == "text_editor":
                        command = tool_input.get("command", "")
                        path = tool_input.get("path", "")
                        console.print(f"[blue]Editing:[/blue] {command} {format_path(path)}")
                    elif tool_name == "think":
                        thought = tool_input.get("thought", "")
                        display_length = min(len(thought), 200)
                        truncated_thought = thought[:display_length] + "..." if len(thought) > display_length else thought
                        console.print(f"[blue]Thinking:[/blue] {truncated_thought}")
                    
                    # Check if this is a request for a custom tool
                    if tool_name in tools_for_phase:
                        try:
                            # Call the custom tool
                            custom_tool_result = tools_for_phase[tool_name](**tool_input)
                            # Convert result to string if it's not already
                            if isinstance(custom_tool_result, dict):
                                tool_result = json.dumps(custom_tool_result, indent=2)
                            else:
                                tool_result = str(custom_tool_result)
                        except Exception as e:
                            tool_result = f"Error executing {tool_name}: {str(e)}"
                    else:
                        # Execute the built-in tool
                        tool_result = await handle_tool_call(tool_name, tool_input)
                    
                    # Check if this is a save to the output path
                    output_saved = False
                    if tool_name == "save_output":
                        saved_path = tool_input.get("file_path", "")
                        # Only mark as saved if there was no error about token limits
                        if saved_path in output_path and not tool_result.startswith("ERROR:"):
                            saved_outputs.add(saved_path)
                            
                            # Check if all expected outputs have been saved
                            if set(output_path).issubset(saved_outputs):
                                output_saved = True
                            
                    # Add tool result to conversation
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
    
    # Half-width horizontal rule to end the phase
    console.print("───────────────────────")
    
    # Display full token usage statistics
    token_counter.display_stats()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        console.print(f"[red]Fatal error:[/red] {str(e)}")
        console.print(traceback.format_exc())
        sys.exit(1)