#!/usr/bin/env python3
# /// script
# dependencies = [
#   "anthropic>=0.17.0", 
#   "rich>=13.7.0",
#   "python-dotenv>=1.0.0",
#   "beautifulsoup4>=4.12.2",
#   "requests>=2.31.0",
#   "Pillow>=10.1.0",
#   "openai>=1.4.0"  # Added for Requesty API integration
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
import json as json_module  # Rename to avoid conflict

# Constants
DEFAULT_MAX_ITERATIONS = 20
MAX_TOKEN_SAFE_LIMIT = 75000

# Simple cache for script files to prevent redundant reading of large files
script_cache = {}

# Load environment variables
load_dotenv()
console = Console()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
brave_api_key = os.getenv("BRAVE_API_KEY")
brave_subscription_token = os.getenv("X_SUBSCRIPTION_TOKEN")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

# Initialize Requesty client if API key exists
requesty_api_key = os.getenv("requesty_api_key")
requesty_client = None
if requesty_api_key:
    try:
        import openai
        requesty_client = openai.OpenAI(
            api_key=requesty_api_key,
            base_url="https://router.requesty.ai/v1"
        )
        console.print("[green]Requesty API client initialized successfully[/green]")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not initialize Requesty client: {str(e)}[/yellow]")
        requesty_client = None

# Define the Claude model to use
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"  # Updated to the correct Claude 3.7 Sonnet model ID

# Global variables for tracking execution state
max_iterations = DEFAULT_MAX_ITERATIONS
conversation_history = []
current_iteration = 0
phase_loops = 0  # Counter for how many times the phase has been extended
phase_complete = False
should_continue_iterations = True

# Load available tools
available_tools = {}
tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
if os.path.exists(tools_dir):
    sys.path.append(tools_dir)
    
    # Try to load image editing tool
    try:
        from tools.image_editing import edit_image
        available_tools["edit_image"] = edit_image
        console.print("[green]Image editing tool loaded successfully[/green]")
    except ImportError:
        console.print("[yellow]Image editing tool not found[/yellow]")
        
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
        self.workflow_id = None
        self.stats_file_path = None
        
        # Initialize cumulative counters (will be loaded properly when workflow is identified)
        self.cumulative_tokens = 0
        self.cumulative_cost = 0.0
        
    def set_workflow_info(self, config_file_path):
        """Set workflow information to identify the correct stats file"""
        # Create a unique ID based on the config file path
        self.workflow_id = os.path.basename(config_file_path).replace('.json', '')
        
        # Get the directory of the config file for storing stats
        config_dir = os.path.dirname(os.path.abspath(config_file_path))
        self.stats_file_path = os.path.join(config_dir, f"token_stats_{self.workflow_id}.json")
        
        # Now that we have the correct path, load any previous stats
        self._load_previous_counters()
        console.print(f"[blue]Token tracking initialized for workflow:[/blue] {self.workflow_id}")
        
    def _load_previous_counters(self):
        """Attempt to load cumulative counters from previous phase"""
        if not self.stats_file_path:
            # No workflow info set yet, can't load previous counters
            return
            
        try:
            # Check for a token_stats file to persist stats between phases
            if os.path.exists(self.stats_file_path):
                with open(self.stats_file_path, 'r') as f:
                    stats = json.load(f)
                    
                # Check if this is a new run (different day) and reset counters if so
                last_updated = stats.get("last_updated", "")
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                last_date = datetime.datetime.fromisoformat(last_updated).strftime("%Y-%m-%d") if last_updated else ""
                
                if last_date != current_date:
                    # New day, reset the counters
                    self.cumulative_tokens = 0
                    self.cumulative_cost = 0.0
                    console.print(f"[green]New day detected. Resetting token stats for this workflow.[/green]")
                else:
                    # Same day, load previous counters
                    self.cumulative_tokens = stats.get("cumulative_tokens", 0)
                    self.cumulative_cost = stats.get("cumulative_cost", 0.0)
                    console.print(f"[green]Loaded previous token stats: {self.cumulative_tokens:,} tokens, ${self.cumulative_cost:.6f}[/green]")
            else:
                # Initialize if no previous stats
                self.cumulative_tokens = 0
                self.cumulative_cost = 0.0
                console.print(f"[blue]Starting new token tracking for workflow[/blue]")
        except Exception as e:
            console.print(f"[yellow]Error loading previous token stats: {str(e)}. Starting fresh.[/yellow]")
            self.cumulative_tokens = 0
            self.cumulative_cost = 0.0
        
    def _save_counters(self):
        """Save token counters to a file for persistence."""
        if not self.stats_file_path:
            console.print(f"[yellow]Warning: Cannot save token stats - workflow not identified[/yellow]")
            return
        
        stats_data = {
            "workflow_id": self.workflow_id,
            "cumulative_tokens": self.cumulative_tokens,
            "cumulative_cost": self.cumulative_cost,
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        try:
            stats_dir = os.path.dirname(self.stats_file_path)
            if not os.path.exists(stats_dir):
                os.makedirs(stats_dir, exist_ok=True)
            
            # Use the simpler approach to write JSON that always works
            with open(self.stats_file_path, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, indent=2, ensure_ascii=False, sort_keys=False)
                # Add a newline at the end for better readability
                f.write('\n')
                
            console.print(f"[blue]Token stats saved to:[/blue] {self.stats_file_path}")
        except Exception as e:
            console.print(f"[yellow]Error saving token stats: {str(e)}[/yellow]")
        
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
        self.cumulative_tokens += phase_tokens
        self.cumulative_cost += phase_cost
        
        # Add workflow/grand total row
        table.add_row("Workflow", f"{self.cumulative_tokens:,}", f"– ${self.cumulative_cost:.6f}")
        
        console.print(table)
        
        # Save stats for next phase
        self._save_counters()
        
        # Display phase information if available
        if 'args' in globals():
            phase_info = getattr(args, 'phase', 0)
            
            # If phases is defined, use it to show progress
            if 'phases' in globals() and phases:
                console.print(f"         Phase {phase_info+1}/{len(phases)} completed", justify="center")
            else:
                console.print(f"         Phase {phase_info+1} completed", justify="center")
        else:
            console.print(f"         Phase completed", justify="center")

# Create token counter
token_counter = TokenCounter()

def convert_to_openai_format(claude_messages):
    """Convert Claude message format to OpenAI format."""
    openai_messages = []
    
    for msg in claude_messages:
        role = msg["role"]
        content = msg.get("content", "")
        
        # Map Claude roles to OpenAI roles
        if role == "assistant":
            openai_role = "assistant"
        elif role == "user":
            openai_role = "user"
        else:
            openai_role = "system"
            
        # Handle tool results
        if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
            if content[0].get("type") == "tool_result":
                # Convert tool result to OpenAI format
                tool_result = content[0]
                openai_messages.append({
                    "role": "tool",
                    "content": tool_result.get("content", ""),
                    "tool_call_id": tool_result.get("tool_use_id", "")
                })
                continue
        
        # Convert content to string if it's a list of text
        if isinstance(content, list):
            processed_content = ""
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    processed_content += item["text"]
                elif isinstance(item, str):
                    processed_content += item
            if processed_content:
                content = processed_content
        
        # Regular message
        if content:
            openai_messages.append({
                "role": openai_role,
                "content": content
            })
        
    return openai_messages

def convert_tools_to_openai_format(claude_tools):
    """Convert Claude tool format to OpenAI format."""
    openai_tools = []
    
    for tool in claude_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        }
        openai_tools.append(openai_tool)
        
    return openai_tools

def process_openai_response(response, conversation_history):
    """Process OpenAI-format response and update conversation history."""
    # Add assistant message to history
    message_content = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": message_content
    })
    
    # Process tool calls if any
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        return response.choices[0].message.tool_calls
    return []

def extract_openai_tool_inputs(tool_call):
    """Extract tool inputs from OpenAI format tool call."""
    function_args = tool_call.function.arguments
    try:
        return json_module.loads(function_args)
    except:
        return {}

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
        "description": "Read the contents of multiple files simultaneously. Always use this to be more efficient if you have more than one file to read, especially if you need to analyze or compare multiple files. Each file's content is returned with its path as a reference.",
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
        "description": "Use this sparingly and look at other file names in the same directory first if your file is missing. Recursively search for files and directories matching a pattern. Searches through all subdirectories from the starting path. Returns full paths to all matching items.",
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
        "description": "Note that there is a more robust text editing tool towards the bottom of this list. Edit a file by replacing text that matches the search pattern.",
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
    # Decision making tools
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
    # Complete task tool
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
    # Workflow adjustment tool
    {
        "name": "workflow_adjustment",
        "description": "Adjust the current workflow phase. Use this when you're ready to end the current phase, or if you need an additional phase to complete the task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["END_PHASE", "ADD_PHASE_AND_CONTINUE", "ADD_PHASE_TO_WORKFLOW_AND_END"],
                    "description": "The action to take on the workflow"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the adjustment"
                }
            },
            "required": ["action", "reason"]
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
    # Perplexity search tool
    {
        "name": "perplexity_search",
        "description": "This is the fastest way to troubleshoot problems or make sure you're using the most up to date implementation of code. Message and Ask Preplexity. They will scour the internet for the most up to date information and even use sentiment analysis from reddit. Get detailed answer with sources for complex questions. This provides deeper context than native web search.",
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
    # Image editing tool
    {
        "name": "edit_image",
        "description": "Artistically edit an image with resize, crop, and text operations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the input image"
                },
                "output_path": {
                    "type": "string",
                    "description": "Path for the output image (auto-generated if None)"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["webp", "jpg", "jpeg", "png"],
                    "description": "Format for the output image (webp by default)"
                },
                "resize": {
                    "type": "boolean",
                    "description": "Whether to resize the image"
                },
                "width": {
                    "type": "integer",
                    "description": "Target width for resizing (default 1200px)"
                },
                "maintain_aspect_ratio": {
                    "type": "boolean",
                    "description": "Whether to maintain aspect ratio when resizing"
                },
                "crop": {
                    "type": "boolean",
                    "description": "Whether to crop the image"
                },
                "crop_method": {
                    "type": "string",
                    "enum": ["coordinates", "aspect_ratio"],
                    "description": "Method for cropping"
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
                    "description": "Focus point for aspect ratio cropping"
                },
                "add_text": {
                    "type": "boolean",
                    "description": "Whether to add text to the image"
                },
                "text": {
                    "type": "string",
                    "description": "Text to add to the image (will be white)"
                },
                "font": {
                    "type": "string",
                    "enum": ["Bebas Neue", "Georgia", "Open Sans", "Montserrat", "Playfair Display"],
                    "description": "Font to use for the text"
                },
                "font_size": {
                    "type": "integer",
                    "description": "Font size in points (auto-calculated if None)"
                },
                "text_position": {
                    "type": "string",
                    "enum": ["center", "top", "bottom"],
                    "description": "Where to place text on the image"
                },
                "shade_opacity": {
                    "type": "integer",
                    "description": "Opacity of the dark shade layer (0-100, default 30)"
                }
            },
            "required": ["image_path"]
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
    
    # Image editing tool
    elif name == "edit_image":
        from tools.image_editing import edit_image
        console.print(f"[blue]Editing image:[/blue] {tool_input.get('image_path')}")
        try:
            result = edit_image(**tool_input)
            if result.get("status") == "success":
                console.print(f"[green]Image edited successfully:[/green] {result.get('output_path')}")
            else:
                console.print(f"[yellow]Image editing warning:[/yellow] {result.get('message')}")
            return json.dumps(result, indent=2)
        except Exception as e:
            error_message = f"Error editing image: {str(e)}"
            console.print(f"[red]{error_message}[/red]")
            return error_message  
          
    elif name == "workflow_adjustment":
        action = tool_input.get("action")
        reason = tool_input.get("reason", "No reason provided")
        
        if action == "END_PHASE":
            # Proceed with normal phase ending
            console.print(f"[green]Ending phase: {reason}[/green]")
            return "ENDING PHASE: Please prepare a phase summary that includes:\n1. What you accomplished\n2. Token counts for any documents created\n3. Any decisions made\n4. Next steps for the following phase"
        
        elif action == "ADD_PHASE_AND_CONTINUE":
            # Reset loops but keep Claude instance - warn about context window
            # Estimate rough token count of conversation history
            history_tokens = sum(len(msg.get("content", "")) for msg in conversation_history) / 4  # rough estimate
            
            if history_tokens > 50000:
                return f"""WARNING: Your context window is getting full (approx. {int(history_tokens)} tokens).
Continuing may lead to context limitations. Consider:
1. Using 'ADD_PHASE_TO_WORKFLOW_AND_END' instead to get a fresh context window
2. If you continue, focus only on the most critical remaining tasks
3. Prepare handoff information in case you reach token limits

Your loops have been reset to 0/{max_iterations}. Continue with caution."""
            else:
                message = f"Adding phase and continuing: {reason}"
                reset_phase_loops(message)
                return message
        
        elif action == "ADD_PHASE_TO_WORKFLOW_AND_END":
            # End phase and recommend starting a new one
            console.print(f"[bold green]✓ WORKFLOW ADJUSTMENT USED: Adding new phase and ending current phase: {reason}[/bold green]")
            phase_complete = True
            should_continue_iterations = False
            return f"""✓ SUCCESSFULLY ADDED PHASE: {reason}

ENDING PHASE AND STARTING NEW: Please prepare a detailed handoff for the next phase that includes:
1. What you accomplished in this phase
2. Token counts for any documents created
3. Detailed instructions for the next phase
4. Any specific files that need attention
5. Any known issues or challenges to be addressed

The next phase will start with a fresh context window."""
        
        else:
            console.print(f"[bold red]Invalid workflow adjustment action: {action}[/bold red]")
            return f"Invalid action: {action}. Valid options are END_PHASE, ADD_PHASE_AND_CONTINUE, or ADD_PHASE_TO_WORKFLOW_AND_END."

    elif name == "read_file":
        file_path = tool_input.get("file_path")
        console.print(f"[blue]Reading file:[/blue] {file_path}")
        
        # Skip reading the SFA main script file directly to save tokens
        if file_path.endswith('sfa_main.py'):
            console.print(f"[yellow]Warning: Attempt to read sfa_main.py directly. Returning tool information instead.[/yellow]")
            
            # Generate documentation that includes loaded custom tools
            tool_docs = """# SFA Tool Documentation
            
The SFA system provides the following tools:

1. File Operations:
   - read_file: Read a single file 
   - read_multiple_files: Read multiple files at once
   - list_directory: List files in a directory
   - save_output: Save content to a file
   - text_editor: Create, view or edit files
   - search_files: Find files matching a pattern

2. Workflow Control:
   - workflow_adjustment: Control phase completion
   - complete_task: Mark a task as complete (uses workflow_adjustment)
   - think: Process complex information
   - make_decision: Choose between options with reasoning

3. Information Tools:
   - web_search: Search the web using Brave Search
   - perplexity_search: Detailed research using Perplexity
   - analyze_image: Analyze images
"""
            
            # Add custom tools section if any are loaded
            if available_tools:
                tool_docs += "\n4. Custom Tools:\n"
                for tool_name in available_tools:
                    tool_docs += f"   - {tool_name}: Available as a custom tool\n"
            
            tool_docs += """
To save tokens, reading the entire script file is discouraged. If you absolutely need specific information, use:

read_file(file_path="sfa_main.py", offset=X, limit=Y)

Where:
- offset: Starting line number (1-indexed)
- limit: Number of lines to read

Common useful sections:
- Tools definition: offset=300, limit=50
- Workflow adjustment: offset=1900, limit=50 
- Text editor tool: offset=1300, limit=50
- Token counter: offset=650, limit=50

This approach is much more token-efficient than reading the entire 2000+ line file.
"""
            
            return tool_docs
        
        # Check if this is a script file (.py, .js, etc.)
        is_script = file_path.endswith('.py') or file_path.endswith('.js') or file_path.endswith('.ts')
        
        # If it's a script file, use our script caching mechanism
        if is_script:
            try:
                # Get file modification time for cache invalidation
                mod_time = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)
                cache_key = f"{file_path}:{mod_time}"
                
                # Check if we have a cached version
                if cache_key in script_cache:
                    console.print(f"[green]Using cached version of script:[/green] {file_path} ({file_size/1024:.1f} KB)")
                    return script_cache[cache_key]
                    
                # Not in cache, read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Store in cache
                script_cache[cache_key] = content
                console.print(f"[blue]Cached script ([/blue][green]{file_size/1024:.1f} KB saved on future reads[/green][blue]):[/blue] {file_path}")
                return content
            except Exception as e:
                return f"Error reading script file: {str(e)}"
        
        # For non-script files, proceed with normal reading
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    elif name == "read_multiple_files":
        paths = tool_input.get("paths", [])
        console.print(f"[blue]Reading multiple files:[/blue] {len(paths)} files")
        
        results = {}
        scripts_cached = 0
        scripts_bytes_saved = 0
        
        for path in paths:
            # Check if this is a script file (.py, .js, etc.)
            is_script = path.endswith('.py') or path.endswith('.js') or path.endswith('.ts')
            
            # If it's a script file, use our script caching mechanism
            if is_script:
                try:
                    # Get file modification time for cache invalidation
                    mod_time = os.path.getmtime(path)
                    file_size = os.path.getsize(path)
                    cache_key = f"{path}:{mod_time}"
                    
                    # Check if we have a cached version
                    if cache_key in script_cache:
                        results[path] = script_cache[cache_key]
                        scripts_cached += 1
                        scripts_bytes_saved += file_size
                        continue
                        
                    # Not in cache, read the file
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Store in cache
                    script_cache[cache_key] = content
                    results[path] = content
                    console.print(f"[blue]Cached script ([/blue][green]{file_size/1024:.1f} KB[/green][blue]):[/blue] {path}")
                except Exception as e:
                    results[path] = f"Error reading script file: {str(e)}"
                continue
            
            # For non-script files, proceed with normal reading
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    results[path] = f.read()
            except Exception as e:
                results[path] = f"Error reading file: {str(e)}"
        
        # Add cache statistics if we cached any scripts
        if scripts_cached > 0:
            results["_cache_stats"] = f"Used cached versions of {scripts_cached} scripts, saving {scripts_bytes_saved/1024:.1f} KB."
            console.print(f"[green]Used cached versions of {scripts_cached} scripts, saving {scripts_bytes_saved/1024:.1f} KB.[/green]")
                
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
        
        # Always check token count before saving
        token_result = None
        if "token_counter" in available_tools:
            try:
                # Count tokens
                token_result = available_tools["token_counter"](text=content)
                console.print(f"[blue]Token count result:[/blue] {json.dumps(token_result, indent=2)}")
                
                if not token_result["is_safe"]:
                    # Token count exceeds safe limit
                    console.print(f"[yellow]Warning:[/yellow] Content exceeds safe token limit ({token_result['token_count']} tokens)")
                    console.print("[yellow]Starting revision phase...[/yellow]")
                    
                    # Reset phase loops instead of ending
                    task_complete = reset_phase_loops(
                        f"Document exceeds token limit ({token_result['token_count']} tokens). Please revise to reduce content while maintaining key information."
                    )
                    
                    return f"⚠️ CRITICAL: Your content ({token_result['token_count']} tokens) exceeds the safe limit (7000 tokens). The file was NOT saved. Please revise your content to be under 7000 tokens, then try saving again. Remember to include your token count in your phase summary report."
            except Exception as e:
                console.print(f"[yellow]Error in token counting:[/yellow] {str(e)}")
                # Continue with save attempt despite token counting error
        
        try:
            # Verify directory exists but never create directories
            directory = os.path.dirname(os.path.abspath(file_path))
            if not os.path.exists(directory):
                return f"Error: Directory '{directory}' does not exist. File saving aborted. Please use an existing directory path."
            
            # Save file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Track output files
            if file_path in output_path:
                saved_outputs.add(file_path)
                
                # Check if all expected outputs have been saved
                if set(output_path).issubset(saved_outputs):
                    console.print(f"[green]All {len(output_path)} expected outputs saved.[/green]")
                    console.print("[yellow]Now you must call workflow_adjustment to end this phase or continue to the next one.[/yellow]")
                    
                    # Return success message that prompts for workflow_adjustment
                    if token_result:
                        return f"""File saved successfully to {file_path} ({token_result['token_count']} tokens).

IMPORTANT: All required outputs have been saved. You must now use the workflow_adjustment tool to either:
1. workflow_adjustment(action="END_PHASE", reason="Phase complete")
2. workflow_adjustment(action="ADD_PHASE_AND_CONTINUE", reason="Need more time in same context")
3. workflow_adjustment(action="ADD_PHASE_TO_WORKFLOW_AND_END", reason="Need a fresh context window")

Please call one of these options to complete the workflow properly."""
                    else:
                        return f"""File saved successfully to {file_path}.

IMPORTANT: All required outputs have been saved. You must now use the workflow_adjustment tool to either:
1. workflow_adjustment(action="END_PHASE", reason="Phase complete")
2. workflow_adjustment(action="ADD_PHASE_AND_CONTINUE", reason="Need more time in same context")
3. workflow_adjustment(action="ADD_PHASE_TO_WORKFLOW_AND_END", reason="Need a fresh context window")

Please call one of these options to complete the workflow properly."""
                else:
                    remaining = len(output_path) - len(saved_outputs)
                    console.print(f"[yellow]Progress: {len(saved_outputs)}/{len(output_path)} outputs saved. {remaining} remaining.[/yellow]")
                    
                    # Return normal success message
                    if token_result:
                        return f"Successfully saved to {file_path} ({token_result['token_count']} tokens). Continue with your remaining tasks."
                    else:
                        return f"Successfully saved to {file_path}. Continue with your remaining tasks."
            else:
                # Return basic success message for non-output path files
                if token_result:
                    return f"Successfully saved to {file_path} ({token_result['token_count']} tokens)."
                else:
                    return f"Successfully saved to {file_path}."
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
            
            # Check if source exists
            if not os.path.exists(source_path):
                return f"Error: Source file '{source_path}' does not exist"
                
            # Check if destination directory exists
            destination_dir = os.path.dirname(os.path.abspath(destination_path))
            if not os.path.exists(destination_dir):
                return f"Error: Destination directory '{destination_dir}' does not exist. File moving aborted. Please use an existing directory path."
            
            # Move the file
            shutil.move(source_path, destination_path)
            
            # Check if this counts as saving to an output path
            if destination_path in output_path:
                saved_outputs.add(destination_path)
                console.print(f"[green]Output saved to target path via move operation:[/green] {destination_path}")
                
                # Check if all expected outputs have been saved
                if set(output_path).issubset(saved_outputs):
                    console.print(f"[green]All {len(output_path)} expected outputs saved via move operations.[/green]")
                    console.print("[yellow]Now you must call workflow_adjustment to end this phase or continue to the next one.[/yellow]")
                    
                    # Return success message that prompts for workflow_adjustment
                    return f"""File moved successfully to {destination_path}.

IMPORTANT: All required outputs have been saved. You must now use the workflow_adjustment tool to either:
1. workflow_adjustment(action="END_PHASE", reason="Phase complete")
2. workflow_adjustment(action="ADD_PHASE_AND_CONTINUE", reason="Need more time in same context")
3. workflow_adjustment(action="ADD_PHASE_TO_WORKFLOW_AND_END", reason="Need a fresh context window")

Please call one of these options to complete the workflow properly."""
                else:
                    remaining = len(output_path) - len(saved_outputs)
                    console.print(f"[yellow]Progress: {len(saved_outputs)}/{len(output_path)} outputs saved. {remaining} remaining.[/yellow]")
            
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
                model=CLAUDE_MODEL,  # Use the global model variable
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
        
        console.print(f"[blue]Text Editor:[/blue] {command} operation on {path}")
        
        try:
            # Command: view - Read and return file content
            if command == "view":
                if not os.path.exists(path):
                    return f"Error: File '{path}' not found"
                    
                try:
                    # Check file size first
                    file_size = os.path.getsize(path)
                    if file_size > 1000000:  # 1MB file size limit for view
                        return f"""Warning: File '{path}' is very large ({file_size/1000000:.2f}MB).
For large files, follow these steps:
1. First use read_file to examine a specific section
2. Make targeted edits with very specific search text
3. If you're adding significant content, consider creating a new file with just your additions
4. Include details in your task report about large files that couldn't be edited"""
                    
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check token count if token_counter is available
                    if "token_counter" in available_tools:
                        token_result = available_tools["token_counter"](text=content)
                        if not token_result["is_safe"]:
                            return f"""Warning: File '{path}' exceeds token limit ({token_result['token_count']} tokens).
Consider making very targeted edits with str_replace using small sections, or create a new file instead."""
                    
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
                    # Check file size first
                    file_size = os.path.getsize(path)
                    if file_size > 1000000:  # 1MB file size limit for non-targeted edits
                        # For large files, suggest a more cautious approach
                        if len(old_str) < 100 or len(new_str) > len(old_str) * 2:
                            return f"""Warning: File '{path}' is very large ({file_size/1000000:.2f}MB).
For large files, follow these steps:
1. First use read_file to examine a specific section
2. Make targeted edits with very specific search text
3. If you're adding significant content, consider creating a new file with just your additions
4. Include details in your task report about large files that couldn't be edited"""
                    
                    # Make a backup of the file before editing
                    backup_path = f"{path}.bak"
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            original_content = f.read()
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not create backup of '{path}': {str(e)}[/yellow]")
                    
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
                            # If not safe, restore from backup and suggest alternatives
                            console.print(f"[yellow]Warning: Edited content would exceed token limit. Restoring original file.[/yellow]")
                            return f"""Error: The resulting content would exceed the token limit ({token_result['token_count']} tokens).
Alternatives for large file editing:
1. Make smaller, more targeted edits
2. Create a new file with your changes (recommended)
3. Note the changes in your task report for human implementation
The original file has not been modified."""
                    
                    # Save the modified content
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    # Count replacements
                    replacements = content.count(old_str)
                    return f"Successfully replaced '{old_str}' with '{new_str}' in '{path}' ({replacements} occurrences)"
                except Exception as e:
                    # Try to restore from backup if anything goes wrong
                    if os.path.exists(backup_path):
                        try:
                            with open(backup_path, 'r', encoding='utf-8') as f:
                                backup_content = f.read()
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(backup_content)
                            console.print(f"[green]Restored original file from backup after error[/green]")
                        except Exception as restore_error:
                            console.print(f"[red]Error restoring from backup: {str(restore_error)}[/red]")
                    
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
                    # Check file size first
                    file_size = os.path.getsize(path)
                    if file_size > 1000000:  # 1MB file size limit
                        return f"""Warning: File '{path}' is very large ({file_size/1000000:.2f}MB).
For inserting content in large files:
1. Consider creating a separate file with your additions
2. Include a note in your task report about what changes are needed
This prevents risking the original file's integrity."""
                    
                    # Make a backup of the file before editing
                    backup_path = f"{path}.bak"
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            original_content = f.read()
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not create backup of '{path}': {str(e)}[/yellow]")
                    
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
                            # If not safe, restore from backup and suggest alternatives
                            console.print(f"[yellow]Warning: Edited content would exceed token limit. Restoring original file.[/yellow]")
                            return f"""Error: The resulting content would exceed the token limit ({token_result['token_count']} tokens).
Alternatives for large file editing:
1. Create a new file with your changes (recommended)
2. Note the changes in your task report for human implementation
The original file has not been modified."""
                    
                    # Save the modified content
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    return f"Successfully inserted text at line {line_number} in '{path}'"
                except Exception as e:
                    # Try to restore from backup if anything goes wrong
                    if os.path.exists(backup_path):
                        try:
                            with open(backup_path, 'r', encoding='utf-8') as f:
                                backup_content = f.read()
                            with open(path, 'w', encoding='utf-8') as f:
                                f.write(backup_content)
                            console.print(f"[green]Restored original file from backup after error[/green]")
                        except Exception as restore_error:
                            console.print(f"[red]Error restoring from backup: {str(restore_error)}[/red]")
                    
                    return f"Error performing insert: {str(e)}"
            
            # Command: create - Create a new file
            elif command == "create":
                file_text = tool_input.get("file_text")
                
                if file_text is None:
                    return "Error: file_text is required for create"
                    
                try:
                    # Check if file already exists
                    if os.path.exists(path):
                        return f"Warning: File '{path}' already exists. Use str_replace or insert to modify it, or choose a different path."
                    
                    # Check token count if token_counter is available
                    if "token_counter" in available_tools:
                        token_result = available_tools["token_counter"](text=file_text)
                        if not token_result["is_safe"]:
                            return f"Error: The content exceeds the token limit ({token_result['token_count']} tokens). Please reduce content size."
                    
                    # Make sure the directory exists, but NEVER create directories
                    directory = os.path.dirname(os.path.abspath(path))
                    if not os.path.exists(directory):
                        return f"Error: Directory '{directory}' does not exist. File creation aborted."
                    
                    # Create the file
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(file_text)
                    
                    # Check if this is an output path - if so, mark it as saved
                    if path in output_path:
                        saved_outputs.add(path)
                        console.print(f"[green]Output saved to target path via text_editor create:[/green] {path}")
                        
                        # Check if all expected outputs have been saved
                        if set(output_path).issubset(saved_outputs):
                            console.print(f"[green]All {len(output_path)} expected outputs saved.[/green]")
                            console.print("[yellow]Now you must call workflow_adjustment to end this phase or continue to the next one.[/yellow]")
                            
                            # Prompt for workflow adjustment
                            return f"""Successfully created file '{path}'.

IMPORTANT: All required outputs have been saved. You must now use the workflow_adjustment tool to either:
1. workflow_adjustment(action="END_PHASE", reason="Phase complete")
2. workflow_adjustment(action="ADD_PHASE_AND_CONTINUE", reason="Need more time in same context")
3. workflow_adjustment(action="ADD_PHASE_TO_WORKFLOW_AND_END", reason="Need a fresh context window")

Please call one of these options to complete the workflow properly."""
                        else:
                            remaining = len(output_path) - len(saved_outputs)
                            console.print(f"[yellow]Progress: {len(saved_outputs)}/{len(output_path)} outputs saved. {remaining} remaining.[/yellow]")
                    
                    return f"Successfully created file '{path}'"
                except Exception as e:
                    return f"Error creating file: {str(e)}"
            
            else:
                return f"Error: Unsupported command '{command}'"
                
        except Exception as e:
            return f"Error in text_editor tool: {str(e)}"
            
    elif name == "complete_task":
        reason = tool_input.get("reason")
        console.print(f"[green]Task complete request:[/green] {reason}")
        
        # Call workflow_adjustment to end the phase correctly
        await workflow_adjustment("END_PHASE", reason)
        
        console.print(f"[bold green]Task completed: {reason}[/bold green]")
        return f"""Task completed successfully: {reason}

Phase is ending. Here's a summary of what was accomplished:
1. Your requested task has been completed
2. Any files saved have been tracked
3. The next phase will start with a fresh context window

Thank you for using the SFA system!"""
    
    elif name == "perplexity_search":
        query = tool_input.get("query")
        focus = tool_input.get("focus", "normal")
        console.print(f"[blue]Searching with Perplexity AI:[/blue] {query} (focus: {focus})")
        
        try:
            if not perplexity_api_key:
                return "Error: Perplexity API key not found in environment variables. Set the PERPLEXITY_API_KEY variable."
                
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {perplexity_api_key}"
            }
            
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

# This must be a global function to be accessible from handle_tool_call
def reset_phase_loops(message):
    """Reset the phase loop counter to extend iterations."""
    global max_iterations, current_iteration, phase_loops
    
    phase_loops += 1
    prev_max = max_iterations
    current_iteration = 0
    max_iterations = DEFAULT_MAX_ITERATIONS
    
    console.print(f"[green]Extension #{phase_loops}: {message}[/green]")
    console.print(f"[blue]Reset iteration counter: {prev_max}/{prev_max} → 0/{max_iterations}[/blue]")
    
    # Don't add a message to conversation history here - the tool result will be added properly
    # by the tool handling code
    
    return f"Extended processing time: {message}"

# Define workflow_adjustment function
async def workflow_adjustment(action, reason=""):
    """Adjust workflow execution based on agent decision.
    
    Args:
        action: "END_PHASE" or "ADD_PHASE_AND_CONTINUE" or "ADD_PHASE_TO_WORKFLOW_AND_END"
        reason: Explanation for adjustment
        
    Returns:
        Status message
    """
    global phase_complete, should_continue_iterations
    
    if action == "END_PHASE":
        phase_complete = True
        should_continue_iterations = False
        console.print(f"[green]Phase ending: {reason}[/green]")
        return f"Phase will end: {reason}"
    
    elif action == "ADD_PHASE_AND_CONTINUE":
        message = f"Adding phase and continuing: {reason}"
        reset_phase_loops(message)
        return message
    
    elif action == "ADD_PHASE_TO_WORKFLOW_AND_END":
        phase_complete = True
        should_continue_iterations = False
        console.print(f"[green]Adding new phase to workflow and ending current phase: {reason}[/green]")
        return f"Added new phase to workflow and ending current phase: {reason}"
    
    else:
        console.print(f"[bold red]Invalid workflow adjustment action: {action}[/bold red]")
        return f"Invalid action: {action}. Valid options are END_PHASE, ADD_PHASE_AND_CONTINUE, or ADD_PHASE_TO_WORKFLOW_AND_END."

async def main():
    parser = argparse.ArgumentParser(description="Single-File Agent (SFA)")
    parser.add_argument("--config-file", required=True, help="Path to the JSON config file")
    parser.add_argument("--phase", type=int, default=0, help="Phase index in the config file")
    parser.add_argument("--model", type=str, help="Model to use for the agent")
    args = parser.parse_args()

    # Load the JSON config
    try:
        with open(args.config_file, 'r') as f:
            config = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading config file:[/red] {str(e)}")
        return
    
    # Set up token counter with workflow information
    token_counter.set_workflow_info(args.config_file)
    
    # Get model from args or config
    model_name = args.model
    if not model_name and 'config' in locals():
        model_name = config.get("M")
    if not model_name:
        model_name = CLAUDE_MODEL

    # Using Requesty?
    using_requesty = requesty_client is not None and model_name != CLAUDE_MODEL
    if using_requesty:
        console.print(f"[blue]Using Requesty with model:[/blue] {model_name}")
    else:
        console.print(f"[blue]Using Claude model:[/blue] {CLAUDE_MODEL}")

    # Extract the workflow key (first key that's not 'A' or 'F' or 'M')
    workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F' and k != 'M'), None)
    if not workflow_key:
        console.print("[red]Error: Invalid config file format - no workflow key found[/red]")
        return
    
    # Get the phase config
    phases = config[workflow_key]
    
    # Check if phases is a list (legacy format) or dictionary (new format)
    if isinstance(phases, list):
        # Format: [{PHASE_0: [...]}, {PHASE_1: [...]}, ...]
        if args.phase >= len(phases):
            console.print(f"[red]Error: Phase index {args.phase} out of range (0-{len(phases)-1})[/red]")
            return
            
        # Get the current phase dictionary
        phase_dict = phases[args.phase]
        
        # Get the task label (should be the only key in the dictionary)
        if len(phase_dict.keys()) != 1:
            console.print(f"[red]Error: Expected one task label in phase {args.phase}, found {len(phase_dict.keys())}[/red]")
            return
            
        current_task_label = list(phase_dict.keys())[0]
        console.print(f"[blue]Using task label:[/blue] {current_task_label}")
        
        # Get the phase configuration
        task_array = phase_dict[current_task_label]
        if isinstance(task_array, list) and len(task_array) > 0:
            phase_config = task_array[0]
            console.print(f"[green]Found configuration for task {current_task_label}[/green]")
        else:
            console.print(f"[red]Error: Invalid task array for {current_task_label}[/red]")
            return
    else:
        # New format (dictionary with labeled tasks)
        # Get all the task labels
        task_labels = list(phases.keys())
        
        # Check if the phase index is valid
        if args.phase >= len(task_labels):
            console.print(f"[red]Error: Phase index {args.phase} out of range (0-{len(task_labels)-1})[/red]")
            return
        
        # Get the label for the current phase
        current_task_label = task_labels[args.phase]
        console.print(f"[blue]Using task label:[/blue] {current_task_label}")
        
        # Get the phase configuration for the current task
        try:
            # Access the task array
            task_array = phases[current_task_label]
            
            if isinstance(task_array, list) and len(task_array) > 0:
                phase_config = task_array[0]
                console.print(f"[green]Found configuration for task {current_task_label}[/green]")
            else:
                console.print(f"[red]Error: Invalid task array for {current_task_label}[/red]")
                return
        except Exception as e:
            console.print(f"[red]Error loading phase config: {str(e)}[/red]")
            return
    
    # Extract variables
    task = phase_config.get('U', '')
    instructions = phase_config.get('X', '')
    resources = phase_config.get('Y', [])
    output_format = phase_config.get('Z', '')
    
    # Define global variables for tracking file output
    global output_path, saved_outputs
    output_path = phase_config.get('O', [])
    saved_outputs = set()
    
    # Ensure output_path is always a list for consistent handling
    if not isinstance(output_path, list):
        output_path = [output_path]
    
    console.print(f"[blue]Output paths:[/blue] {output_path}")
    
    # Prepare system message with cache control for prompt caching
    system_message = [{
        "type": "text",
        "text": task,
    }]
    
    # Only add cache_control if task is not empty
    if task.strip():
        system_message[0]["cache_control"] = {"type": "ephemeral"}
    
    # Prepare initial message with path information
    initial_message = f"""Instructions: {instructions}
Output Format: {output_format}

Resources available:
"""

    # Add resources if available
    if resources and resources != ["N/A"]:
        if isinstance(resources, list):
            initial_message += "Resources:\n"
            for resource in resources:
                if resource != "N/A":
                    initial_message += f"- {resource}\n"
        else:
            initial_message += f"Resource: {resources}\n"
    
    # Add output path
    initial_message += f"\nYour output should be saved to: {output_path}\n"
    
    # Add this to the initial_message
    initial_message += """
    Available Workflow Tools:
    - workflow_adjustment: Adjust the current workflow phase
      - END_PHASE: Complete current phase and prepare summary before ending
      - ADD_PHASE_AND_CONTINUE: Reset iteration counter and continue in same context window
      - ADD_PHASE_TO_WORKFLOW_AND_END: End current phase and prepare handoff for completely new phase
    
    Examples:
    - workflow_adjustment(action="END_PHASE", reason="Task completed successfully")
    - workflow_adjustment(action="ADD_PHASE_AND_CONTINUE", reason="Need more time to finish")
    - workflow_adjustment(action="ADD_PHASE_TO_WORKFLOW_AND_END", reason="Next batch requires fresh context")

    - task_report: Create a phase summary to complete the phase
    - task_report(
        report="Summary of what was accomplished...",
        next_steps="Recommendations for next phase...",
        decision={"options": [...], "choice": "...", "reasoning": "..."}
        )

    End-of-Phase Process:
    1. Save all required output files using save_output
    2. Create a phase summary with task_report that includes:
       - Summary of what you accomplished
       - Token counts for any documents created
       - Any decisions made
       - Next steps for the following phase
    3. This will automatically complete the current phase
    
    Iteration and Context Window Management:
    1. You have a maximum of {max_iterations} iterations per phase
    2. When approaching the limit (last 2-3 iterations), prepare to either:
       - Complete your task and end the phase
       - Request more iterations with ADD_PHASE_AND_CONTINUE
       - Prepare handoff information for the next phase with ADD_PHASE_TO_WORKFLOW_AND_END
    3. Your context window has a limit - if working with large files or many iterations:
       - Consider using ADD_PHASE_TO_WORKFLOW_AND_END to get a fresh context
       - Prioritize critical information for handoff to the next phase
       - Document what's been done and what remains to be done
"""

    # Add information about available tools
    if available_tools:
        initial_message += "\nAvailable Tools:\n"
        if "token_counter" in available_tools:
            initial_message += """- token_counter: Use this to check token counts before saving
  - Call with: tools["token_counter"](text="your text") or tools["token_counter"](file_path="path/to/file")
  - Returns a dictionary with: token_count, is_safe (boolean), status, and message
  - Example: result = tools["token_counter"](file_path=output_path[0])
  - Always check if the content is safe to save with: if result["is_safe"]
  - For large files that exceed token limits, create a new file with your changes and document in your task report
"""
        # Add text_editor tool documentation
        initial_message += """- text_editor: Advanced text editor with multiple commands:
  - text_editor(command="view", path="/path/to/file.txt") - View file content
  - text_editor(command="str_replace", path="/path/to/file.txt", old_str="text to replace", new_str="new text") - Replace text
  - text_editor(command="insert", path="/path/to/file.txt", line_number=10, new_str="text to insert") - Insert at specific line
  - text_editor(command="create", path="/path/to/newfile.txt", file_text="content") - Create new file
  - Note: For large files, the text_editor will create backups and prevent file loss
  - For files too large to edit safely, document changes needed in your task report
"""
    
    initial_message += "\nPlease explore these resources as needed using the provided tools. Use the 'think' tool to process complex information from multiple files before making decisions."

    # Display configuration
    console.print(f"[bold]Running SFA Phase {args.phase + 1}{f' of {len(phases)}' if isinstance(phases, list) else ''}[/bold]")  # Show 1-based phase number with fallback
    # Limit the task display to just the first line or 80 chars
    truncated_task = task.split('\n')[0][:80] + ("..." if len(task) > 80 or '\n' in task else "")
    console.print(f"[blue]Task:[/blue] {truncated_task}")
    # Similarly limit the instructions display
    truncated_instructions = instructions.split('\n')[0][:80] + ("..." if len(instructions) > 80 or '\n' in instructions else "")
    console.print(f"[blue]Topic:[/blue] {truncated_instructions}")
    console.print(f"[blue]Output:[/blue] {output_path}")
    
    # Start conversation with Claude
    global conversation_history
    conversation_history = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": initial_message,
        }]
    }]
    
    # Only add cache_control if initial_message is not empty
    if initial_message.strip():
        conversation_history[0]["content"][0]["cache_control"] = {"type": "ephemeral"}
    
    # Create a global tools variable for the agent to use
    globals()["tools"] = available_tools.copy()
    
    # Agent loop
    task_complete = False
    max_iterations = DEFAULT_MAX_ITERATIONS
    iterations = 0
    
    # Stats tracking for prompt caching
    total_tokens_saved = 0
    total_cost_saved = 0.0
    
    # Add this before reaching max iterations in the main loop
    if iterations >= max_iterations - 3:  # About to hit max with 3 or fewer iterations left
        console.print(f"[yellow]Warning: Only {max_iterations - iterations} iterations remaining. Notifying Claude...[/yellow]")
        
        # Add a message to conversation history
        max_loops_message = {
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"""ITERATION LIMIT WARNING: You have only {max_iterations - iterations} iterations left before reaching the maximum.

Please assess your current progress and decide on one of these options:
1. Complete your task quickly in the remaining iterations and end the phase
2. Call workflow_adjustment with action="ADD_PHASE_AND_CONTINUE" to reset your iterations and continue in the same context window
3. Call workflow_adjustment with action="ADD_PHASE_TO_WORKFLOW_AND_END" to prepare handoff information for a new phase with a fresh context window

If you're working with large files or have accumulated a large context window, option #3 is recommended.
If you're close to completing your task, option #1 is best.
If you need more iterations but have a manageable context size, option #2 works well.

Regardless of your choice, prepare a summary of what you've accomplished so far and what remains to be done."""
            }]
        }
        
        # Add cache_control only if text is not empty
        if max_loops_message["content"][0]["text"].strip():
            max_loops_message["content"][0]["cache_control"] = {"type": "ephemeral"}
        
        conversation_history.append(max_loops_message)

    while not task_complete and iterations < max_iterations:
        iterations += 1
        console.rule(f"[yellow]Phase {args.phase + 1}{f'/{len(phases)}' if isinstance(phases, list) else ''} • Loop {iterations}/{max_iterations}[/yellow]")
        
        try:
            # Call Claude
            console.print("[blue]Calling AI model...[/blue]")
            
            if using_requesty:
                # Convert to OpenAI format for Requesty
                openai_messages = convert_to_openai_format(conversation_history)
                openai_tools = convert_tools_to_openai_format(TOOLS)
                
                try:
                    response = requesty_client.chat.completions.create(
                        model=model_name,
                        messages=openai_messages,
                        tools=openai_tools,
                        temperature=0.3,
                        stream=False  # No streaming support for now
                    )
                    
                    # Get tokens if available
                    input_tokens = getattr(response, 'usage', {}).get('prompt_tokens', 0)
                    output_tokens = getattr(response, 'usage', {}).get('completion_tokens', 0)
                    
                    # Update token counter
                    token_counter.update(
                        input_tokens=input_tokens, 
                        output_tokens=output_tokens
                    )
                    
                    console.print(f"[magenta]Token Usage - Current:[/magenta] Input: {input_tokens:,} | Output: {output_tokens:,}")
                    console.print(f"[magenta]Token Usage - Total:[/magenta] Input: {token_counter.total_input_tokens:,} | Output: {token_counter.total_output_tokens:,} | Cost: ${token_counter.total_cost:.6f}")
                    
                    # Process the response
                    tool_calls = process_openai_response(response, conversation_history)
                    
                    # Handle tool calls
                    if tool_calls:
                        for tool_call in tool_calls:
                            tool_name = tool_call.function.name
                            tool_id = tool_call.id
                            tool_input = extract_openai_tool_inputs(tool_call)
                            
                            console.print(f"[blue]Tool request:[/blue] {tool_name}")
                            
                            # Process tool call as before
                            tool_result = await handle_tool_call(tool_name, tool_input)
                            
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
                            
                            # Special handling for workflow_adjustment tool
                            if tool_name == "workflow_adjustment":
                                action = tool_input.get("action", "")
                                
                                # Reset iteration counter if using ADD_PHASE_AND_CONTINUE
                                if action == "ADD_PHASE_AND_CONTINUE":
                                    iterations = 0
                                    # Add a confirmation message to conversation history
                                    conversation_history.append({
                                        "role": "user",
                                        "content": [{
                                            "type": "text",
                                            "text": f"PHASE CONTINUATION: Your loops have been reset to 0/{max_iterations}. Continue working on the current task with the same context window."
                                        }]
                                    })
                                
                                # Trigger phase completion for any workflow_adjustment action
                                if action in ["END_PHASE", "ADD_PHASE_TO_WORKFLOW_AND_END"]:
                                    output_saved = True # Assuming output_saved is defined elsewhere or needs to be part of this logic
                            
                            # Check if task complete
                            if tool_name == "complete_task" or output_saved:
                                task_complete = True
                except Exception as e:
                    console.print(f"[red]Error with Requesty API:[/red] {str(e)}")
                    console.print(f"[yellow]Falling back to Claude...[/yellow]")
                    using_requesty = False
                    # Only fall back if we have a valid Claude client
                    if not os.getenv("ANTHROPIC_API_KEY"):
                        raise e
            
            # If not using Requesty or fallback to Claude
            if not using_requesty:                
                # Ensure system message is never empty
                if not task.strip():
                    task = "Assistant is a helpful AI agent designed to complete tasks."
                    
                current_system_message = [{
                    "type": "text",
                    "text": task
                }]
                
                # Only add cache_control if task is not empty
                if task.strip():
                    current_system_message[0]["cache_control"] = {"type": "ephemeral"}
                
                # Try with beta client for token-efficient-tools and prompt caching
                try:
                    response = anthropic_client.beta.messages.create(
                        model=CLAUDE_MODEL,  # Use the global model variable
                        system=current_system_message,
                        messages=conversation_history,
                        max_tokens=8192,
                        tools=TOOLS,
                        temperature=0.3,
                        betas=["token-efficient-tools-2025-02-19", "prompt-caching-2024-07-31"]
                    )
                except Exception as beta_error:
                    # Handle specific error about token-efficient tool use not being supported
                    console.print(f"[yellow]Beta API error: {str(beta_error)}[/yellow]")
                    console.print("[yellow]Using API without beta features...[/yellow]")
                    
                    # Fall back to standard client without betas
                    response = anthropic_client.messages.create(
                        model=CLAUDE_MODEL,  # Use the global model variable
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
            
            # Update token counter (This was part of Requesty logic, ensure it's here for Claude too if not already)
            if not using_requesty: # Redundant if already handled, but ensure it is if Claude path taken
                 token_counter.update(
                    input_tokens=input_tokens, 
                    output_tokens=output_tokens,
                    cached_tokens=cache_read_tokens,
                    cache_creation_tokens=cache_creation_tokens
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
                # Calculate extra cost due to 25% premium
                base_cost = cache_creation_tokens * 0.000003
                premium_cost = cache_creation_tokens * 0.000003 * 0.25
                console.print(f"[yellow]Cache Creation:[/yellow] Added {cache_creation_tokens} tokens to cache (extra cost: ~${premium_cost:.6f})")
            
            # Add Claude's response to conversation history
            conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Display Claude's text responses with more content visible
            for item in response.content:
                if item.type == "text":
                    text = item.text
                    display_length = min(len(text), 1000)  # Show more of Claude's thinking (increased from 500)
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
                    
                    # Check if this is a request for a custom tool
                    if tool_name in globals()["tools"]:
                        try:
                            # Call the custom tool
                            custom_tool_result = globals()["tools"][tool_name](**tool_input)
                            # Convert result to string if it's not already
                            if isinstance(custom_tool_result, dict):
                                tool_result = json.dumps(custom_tool_result, indent=2)
                            else:
                                tool_result = str(custom_tool_result)
                            console.print(f"[blue]Custom tool:[/blue] {tool_name} executed successfully")
                        except Exception as e:
                            tool_result = f"Error executing {tool_name}: {str(e)}"
                            console.print(f"[red]Custom tool error:[/red] {tool_result}")
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
                            console.print(f"[green]Output saved to target path:[/green] {saved_path}")
                            
                            # Check if all expected outputs have been saved
                            if set(output_path).issubset(saved_outputs):
                                # Don't set output_saved to True anymore - let workflow_adjustment handle completion
                                console.print(f"[green]All {len(output_path)} expected outputs saved.[/green]")
                                console.print("[yellow]Please call workflow_adjustment or task_report to complete the phase.[/yellow]")
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
                    
                    # Special handling for workflow_adjustment tool
                    if tool_name == "workflow_adjustment":
                        action = tool_input.get("action", "")
                        
                        # Reset iteration counter if using ADD_PHASE_AND_CONTINUE
                        if action == "ADD_PHASE_AND_CONTINUE":
                            iterations = 0
                            # Add a confirmation message to conversation history
                            conversation_history.append({
                                "role": "user",
                                "content": [{
                                    "type": "text",
                                    "text": f"PHASE CONTINUATION: Your loops have been reset to 0/{max_iterations}. Continue working on the current task with the same context window."
                                }]
                            })
                        
                        # Trigger phase completion for any workflow_adjustment action
                        if action in ["END_PHASE", "ADD_PHASE_TO_WORKFLOW_AND_END"]:
                            output_saved = True
                    
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

    # Display total cache creation premium costs
    total_cache_creation_premium = token_counter.cache_creation_extra_cost
    if total_cache_creation_premium > 0:
        console.print(f"[yellow]Total Cache Creation Premium:[/yellow] Extra cost of ${total_cache_creation_premium:.6f} for cache writes")
    
    # Display script cache statistics
    if len(script_cache) > 0:
        total_bytes = sum(len(content) for content in script_cache.values())
        console.print("\n[bold green]Script Cache Performance:[/bold green]")
        console.print(f"[green]Scripts cached:[/green] {len(script_cache)}")
        console.print(f"[green]Total size:[/green] {total_bytes/1024:.1f} KB")
        console.print(f"[green]Estimated tokens saved on reuse:[/green] ~{int(total_bytes/4):,}")
        console.print(f"[green]Estimated cost savings:[/green] ${int(total_bytes/4) * 0.000003:.6f}")
    
    console.print(f"[green]Agent process completed![/green]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        console.print(f"[red]Fatal error:[/red] {str(e)}")
        console.print(traceback.format_exc())
        sys.exit(1)