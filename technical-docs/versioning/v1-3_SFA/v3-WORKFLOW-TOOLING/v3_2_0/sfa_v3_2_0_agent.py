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
import hashlib
import re
from rich.console import Console
from rich.table import Table
from anthropic import Anthropic
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from PIL import Image
import io
import datetime

# Constants
DEFAULT_MAX_ITERATIONS = 20
MAX_TOKEN_SAFE_LIMIT = 75000

# File caching system to prevent redundant file reading
file_cache = {}
file_cache_stats = {"hits": 0, "misses": 0, "bytes_saved": 0}
# Token budget tracking
token_budget = MAX_TOKEN_SAFE_LIMIT * 0.8  # 80% of maximum safe limit
current_token_usage = 0

# Script fingerprinting to avoid re-reading the same script
script_fingerprints = {}
# Smart tool memory to remember previous tool call outcomes
tool_memory = {}

# Load environment variables
load_dotenv()
console = Console()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
brave_api_key = os.getenv("BRAVE_API_KEY")
brave_subscription_token = os.getenv("X_SUBSCRIPTION_TOKEN")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

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

# Define tools with cache control on the last tool for prompt caching
TOOLS = [
    # Prioritize batch operations for file reading
    {
        "name": "batch_read_files",
        "description": "Efficiently read multiple files with a single API call, optimized for token usage. Use this instead of multiple read_file calls when analyzing related files together.",
        "input_schema": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "Array of file paths to process together"
                },
                "batch_mode": {
                    "type": "string",
                    "enum": ["summary", "full", "adaptive"],
                    "description": "How to process the files: 'summary' for short summaries of each file, 'full' for complete content, 'adaptive' to automatically choose based on file size",
                    "default": "adaptive"
                }
            },
            "required": ["files"]
        }
    },
    {
        "name": "script_summary",
        "description": "Get an efficient summary of a script file including its structure, functions, classes, and imports, without reading the entire file. Use this instead of read_file for Python scripts (.py files) when you just need to understand their structure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "script_path": {
                    "type": "string",
                    "description": "Path to the script file (.py) to summarize"
                }
            },
            "required": ["script_path"]
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
                },
                "max_lines_per_file": {
                    "type": "integer",
                    "description": "Maximum lines per file to read",
                    "default": 50
                }
            },
            "required": ["paths"]
        }
    },
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
        "name": "list_directory",
        "description": "List all files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory_path": {"type": "string"},
                "pattern": {"type": "string", "default": "*.*"},
                "include_sizes": {"type": "boolean", "default": True}
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
    {
        "name": "memory_stats",
        "description": "Get statistics about the agent's memory usage, including file cache and tool memory, to optimize token usage and track performance.",
        "input_schema": {
            "type": "object",
            "properties": {
                "detail_level": {
                    "type": "string",
                    "enum": ["basic", "detailed"],
                    "description": "The level of detail to include in the statistics",
                    "default": "basic"
                }
            }
        }
    },
    {
        "name": "optimize_prompt",
        "description": "Optimize a text prompt or message for token efficiency by removing redundancy, simplifying language, and condensing information without losing meaning. Perfect for reducing token usage in API calls.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to optimize for token efficiency"
                },
                "target_reduction": {
                    "type": "integer",
                    "description": "Target percentage reduction (e.g., 30 means aim to reduce by 30%)",
                    "default": 30
                },
                "preserve_key_elements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key phrases or elements that must be preserved in the optimized version",
                    "default": []
                }
            },
            "required": ["text"]
        }
    },
]

# Tool implementations
async def handle_tool_call(name, tool_input):
    global saved_outputs, output_path, phase_complete, should_continue_iterations, task_complete
    
    # Parse tool input to string for memory lookups
    if isinstance(tool_input, dict):
        # Sort keys for consistent string representation
        sorted_items = sorted(tool_input.items())
        input_str = json.dumps(sorted_items)
    else:
        input_str = str(tool_input)
    
    # Check if we have a remembered result for this tool call
    remembered_result = get_remembered_tool_result(name, tool_input)
    if remembered_result is not None:
        console.print(f"[green]Using remembered result for tool:[/green] {name}")
        return remembered_result
    
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
        start_line = tool_input.get("start_line", 0)
        max_lines = tool_input.get("max_lines", 100)  # Default to 100 lines
        console.print(f"[blue]Reading file:[/blue] {file_path} (lines {start_line} to {start_line + max_lines})")
        
        # Generate cache key based on file path, start line, and max lines
        cache_key = f"{file_path}:{start_line}:{max_lines}"
        
        # Check if result is in cache
        if cache_key in file_cache:
            file_size = os.path.getsize(file_path)
            file_cache_stats["hits"] += 1
            file_cache_stats["bytes_saved"] += file_size
            console.print(f"[green]Cache hit:[/green] Using cached content for {file_path}")
            return file_cache[cache_key]
        
        # Not in cache, proceed with normal reading
        file_cache_stats["misses"] += 1
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' not found"
                
            # Check file size before reading
            file_size = os.path.getsize(file_path)
            if file_size > 1000000:  # 1MB
                return f"""Warning: File '{file_path}' is very large ({file_size/1000000:.2f}MB).
Please use more targeted parameters:
- Specify start_line (e.g., start_line=100)
- Limit max_lines (e.g., max_lines=50)
- Use specific file sections instead of the entire file"""
            
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                # Read all lines into a list
                all_lines = f.readlines()
                
                # Get total line count
                total_lines = len(all_lines)
                
                # Validate start_line
                if start_line < 0:
                    start_line = 0
                if start_line >= total_lines:
                    return f"Error: start_line {start_line} is beyond the end of file (total lines: {total_lines})"
                
                # Calculate end line (inclusive)
                end_line = min(start_line + max_lines, total_lines)
                
                # Get the requested chunk of lines
                lines_to_return = all_lines[start_line:end_line]
                content = ''.join(lines_to_return)
                
                # Add file statistics
                file_info = f"""File: {file_path}
Lines {start_line}-{end_line-1} of {total_lines} total lines
Size: {file_size/1024:.1f} KB
"""
                
                # Only add navigation hints if file is larger than what we're showing
                if total_lines > max_lines:
                    file_info += f"""
To see more of this file:
- Next chunk: read_file(file_path="{file_path}", start_line={end_line}, max_lines={max_lines})
- Previous chunk: read_file(file_path="{file_path}", start_line={max(0, start_line-max_lines)}, max_lines={max_lines})
"""
                
                result = file_info + "\n" + content
                
                # Cache the result
                file_cache[cache_key] = result
                
                return result
        except Exception as e:
            return f"Error reading file: {str(e)}"
            
    elif name == "read_multiple_files":
        paths = tool_input.get("paths", [])
        max_lines_per_file = tool_input.get("max_lines_per_file", 50)  # Default to 50 lines per file
        console.print(f"[blue]Reading multiple files:[/blue] {len(paths)} files (max {max_lines_per_file} lines each)")
        
        results = {}
        total_size = 0
        skipped_files = []
        cached_files = 0
        
        # First check total size of all files
        for path in paths:
            try:
                if not os.path.exists(path):
                    results[path] = f"Error: File not found"
                    continue
                    
                file_size = os.path.getsize(path)
                total_size += file_size
                
                # Skip very large files
                if file_size > 1000000:  # 1MB
                    skipped_files.append(f"{path} ({file_size/1000000:.2f}MB)")
                    results[path] = f"Skipped: File is too large ({file_size/1000000:.2f}MB). Use read_file with start_line and max_lines."
            except Exception as e:
                results[path] = f"Error checking file: {str(e)}"
        
        # Give warning if total size is too large
        if total_size > 5000000:  # 5MB total
            results["warning"] = f"Total size of files is very large ({total_size/1000000:.2f}MB). Consider reading fewer files or smaller portions."
            return json.dumps(results, indent=2)
        
        # Read content of files that weren't skipped
        for path in paths:
            if path in results and results[path].startswith("Skipped:"):
                continue  # Skip already marked files
            
            # Check if this file is in cache (use start_line=0 for complete file)
            cache_key = f"{path}:0:{max_lines_per_file}"
            if cache_key in file_cache:
                results[path] = file_cache[cache_key]
                file_cache_stats["hits"] += 1
                file_size = os.path.getsize(path) if os.path.exists(path) else 0
                file_cache_stats["bytes_saved"] += file_size
                cached_files += 1
                continue
                
            # Not in cache, read the file
            file_cache_stats["misses"] += 1
            try:
                if not os.path.exists(path):
                    continue  # Already handled above
                    
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    # Read all lines into a list
                    all_lines = f.readlines()
                    
                    # Get total line count
                    total_lines = len(all_lines)
                    
                    # Get the requested chunk of lines (from beginning)
                    lines_to_return = all_lines[:min(max_lines_per_file, total_lines)]
                    content = ''.join(lines_to_return)
                    
                    # Add truncation notice if needed
                    if total_lines > max_lines_per_file:
                        content += f"\n...\n[File truncated, showing {max_lines_per_file} of {total_lines} lines]\n"
                        content += f"To see more, use: read_file(file_path=\"{path}\", start_line={max_lines_per_file}, max_lines=50)"
                    
                    results[path] = content
                    # Cache the result
                    file_cache[cache_key] = content
            except Exception as e:
                results[path] = f"Error reading file: {str(e)}"
        
        # Add summary of skipped files
        if skipped_files:
            results["skipped_files"] = f"Skipped {len(skipped_files)} large files: {', '.join(skipped_files)}"
            
        # Add cache statistics 
        if cached_files > 0:
            results["cache_info"] = f"Retrieved {cached_files} of {len(paths) - len(skipped_files)} files from cache"
            
        return json.dumps(results, indent=2)
            
    elif name == "list_directory":
        directory_path = tool_input.get("directory_path")
        pattern = tool_input.get("pattern", "*.*")
        include_sizes = tool_input.get("include_sizes", True)
        console.print(f"[blue]Listing directory:[/blue] {directory_path}")
        
        try:
            if not os.path.exists(directory_path):
                return f"Error: Directory '{directory_path}' does not exist"
                
            results = []
            
            # Get all matching files
            files = glob_module.glob(os.path.join(directory_path, pattern))
            
            # Calculate total size and count files/dirs
            total_size = 0
            file_count = 0
            dir_count = 0
            
            for file_path in files:
                if os.path.isdir(file_path):
                    dir_count += 1
                    item_type = "DIR"
                    size_info = ""
                else:
                    file_count += 1
                    size = os.path.getsize(file_path)
                    total_size += size
                    item_type = "FILE"
                    
                    # Format size nicely
                    if include_sizes:
                        if size < 1024:
                            size_info = f"({size} B)"
                        elif size < 1024 * 1024:
                            size_info = f"({size/1024:.1f} KB)"
                        else:
                            size_info = f"({size/(1024*1024):.1f} MB)"
                    else:
                        size_info = ""
                
                # Add formatted entry
                if include_sizes:
                    results.append(f"[{item_type}] {file_path} {size_info}")
                else:
                    results.append(f"[{item_type}] {file_path}")
            
            # Add summary at the beginning
            summary = f"Directory: {directory_path}\n"
            summary += f"Found {len(files)} items ({file_count} files, {dir_count} directories)"
            
            if include_sizes and file_count > 0:
                if total_size < 1024 * 1024:
                    summary += f", total size: {total_size/1024:.1f} KB\n"
                else:
                    summary += f", total size: {total_size/(1024*1024):.1f} MB\n"
            else:
                summary += "\n"
                
            # Cap results for very large directories
            if len(files) > 100:
                results = results[:100]
                summary += f"\n[Showing first 100 of {len(files)} items]\n"
                
            return summary + "\n" + "\n".join(results)
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
                ],
                temperature=0.3
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
                    
                    # NEW: Check if this is a save to the output path and mark as completed
                    # This allows text_editor created files to trigger completion
                    if 'output_path' in globals() and path in output_path:
                        saved_outputs.add(path)
                        console.print(f"[green]Output saved to target path:[/green] {path}")
                        
                        # Check if all expected outputs have been saved
                        if set(output_path).issubset(saved_outputs):
                            console.print(f"[green]All {len(output_path)} expected outputs saved.[/green]")
                            console.print("[yellow]Please call workflow_adjustment or task_report to complete the phase.[/yellow]")
                            
                            # Remind the agent to complete the phase
                            return f"""Successfully created file '{path}'

IMPORTANT: All required outputs have been saved. You should now use the workflow_adjustment tool to either:
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
        
        # NEW: Instead of just redirecting, actually use workflow_adjustment to end phase
        console.print("[green]Ending phase based on complete_task request[/green]")
        
        # Set global variables for phase completion
        phase_complete = True
        should_continue_iterations = False
        task_complete = True
        
        return """ENDING PHASE: Your task has been marked as complete. 
        
Thank you for completing this phase of the workflow. The system will now transition to the next phase (if any) or end the workflow."""
    
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
    
    elif name == "batch_read_files":
        files = tool_input.get("files", [])
        batch_mode = tool_input.get("batch_mode", "adaptive")
        console.print(f"[blue]Batch reading files:[/blue] {len(files)} files in {batch_mode} mode")
        
        if not files:
            return "Error: No files provided for batch reading"
            
        # Calculate hash of files list to use as cache key
        files_hash = hashlib.md5(str(sorted(files)).encode()).hexdigest()
        cache_key = f"batch:{files_hash}:{batch_mode}"
        
        # Check if result is in cache
        if cache_key in file_cache:
            file_cache_stats["hits"] += 1
            console.print(f"[green]Cache hit:[/green] Using cached batch results")
            return file_cache[cache_key]
            
        file_cache_stats["misses"] += 1
        
        # Process each file based on the batch mode
        results = {}
        file_sizes = {}
        total_chars = 0
        
        # First pass - collect file metadata and determine processing approach
        for file_path in files:
            if not os.path.exists(file_path):
                results[file_path] = {"status": "error", "reason": "File not found"}
                continue
                
            try:
                file_size = os.path.getsize(file_path)
                file_sizes[file_path] = file_size
                
                # In adaptive mode, make decisions based on file size
                if batch_mode == "adaptive":
                    # Assume very large files need different treatment
                    if file_size > 500000:  # 500KB
                        results[file_path] = {"status": "large_file", "size": file_size}
                    else:
                        results[file_path] = {"status": "process_full", "size": file_size}
                elif batch_mode == "summary":
                    results[file_path] = {"status": "process_summary", "size": file_size}
                else:  # full mode
                    results[file_path] = {"status": "process_full", "size": file_size}
                    
            except Exception as e:
                results[file_path] = {"status": "error", "reason": str(e)}
        
        # Second pass - process each file according to its determined status
        for file_path, info in results.items():
            if info["status"] in ["error", "skipped"]:
                continue
                
            try:
                # Handle differently based on status
                if info["status"] == "large_file":
                    # For large files, just read the beginning and end
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        head_lines = [next(f) for _ in range(50) if f]
                        
                    # Get file extension for better processing
                    _, ext = os.path.splitext(file_path)
                    file_type = ext.lower()[1:] if ext else "unknown"
                    
                    # If it's code, try to extract function/class definitions
                    if file_type in ["py", "js", "java", "c", "cpp", "h", "cs"]:
                        # Use grep to find important structures like functions and classes
                        import subprocess
                        try:
                            # Try to extract function/class definitions
                            if file_type == "py":
                                grep_cmd = ["grep", "-n", "^def\\|^class", file_path]
                            elif file_type in ["js", "java", "c", "cpp", "cs"]:
                                grep_cmd = ["grep", "-n", "function\\|class", file_path]
                                
                            result = subprocess.run(grep_cmd, capture_output=True, text=True)
                            struct_defs = result.stdout.strip().split('\n')
                            
                            # Include a limited number of definitions
                            if struct_defs and struct_defs[0]:
                                info["definitions"] = struct_defs[:20]  # Limit to 20 definitions
                        except:
                            pass  # Ignore grep errors, it's just an enhancement
                    
                    # Include file beginning
                    info["content"] = "".join(head_lines)
                    info["note"] = f"Large file ({info['size']/1024:.1f} KB). Showing first 50 lines only."
                    
                elif info["status"] == "process_summary":
                    # Just count lines and provide metadata for summary mode
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        line_count = sum(1 for _ in f)
                        
                    info["line_count"] = line_count
                    info["file_name"] = os.path.basename(file_path)
                    info["directory"] = os.path.dirname(os.path.abspath(file_path))
                    info["note"] = "Summary mode - file content not included"
                    
                elif info["status"] == "process_full":
                    # Full content for reasonably sized files
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    # Check if the content is too large still
                    if len(content) > 100000:  # ~25K tokens
                        # Truncate very large content
                        content = content[:100000] + f"\n\n... [Content truncated, showing first ~25K tokens of {len(content)/4000:.1f}K tokens]"
                        
                    info["content"] = content
                    info["content_length"] = len(content)
                    info["note"] = "Full content included"
                    total_chars += len(content)
                    
            except Exception as e:
                info["status"] = "error"
                info["reason"] = str(e)
        
        # Estimate token usage (rough approximation: ~4 chars per token)
        results["metadata"] = {
            "files_processed": len(files),
            "estimated_tokens": int(total_chars / 4),
            "batch_mode": batch_mode,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Cache the results
        result_json = json.dumps(results, indent=2)
        file_cache[cache_key] = result_json
        
        return result_json
    
    elif name == "script_summary":
        script_path = tool_input.get("script_path")
        console.print(f"[blue]Generating script summary for:[/blue] {script_path}")
        
        try:
            if not os.path.exists(script_path):
                return f"Error: Script file '{script_path}' not found"
            
            # Read the script file
            with open(script_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Identify key sections in the script
            functions = []
            classes = []
            imports = []
            constants = []
            current_section = None
            
            # Simple line-by-line parser to extract key elements
            for line in content.splitlines():
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Extract imports
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
                
                # Extract functions
                elif line.startswith('def '):
                    # Capture function signature
                    function_def = line
                    if function_def.endswith(':'):
                        function_def = function_def[:-1]  # Remove trailing colon
                    functions.append(function_def)
                
                # Extract classes
                elif line.startswith('class '):
                    # Capture class definition
                    class_def = line
                    if class_def.endswith(':'):
                        class_def = class_def[:-1]  # Remove trailing colon
                    classes.append(class_def)
                
                # Extract constants (uppercase variables)
                elif '=' in line and not line.startswith(' ') and not line.startswith('\t'):
                    var_name = line.split('=')[0].strip()
                    if var_name.isupper() and len(var_name) > 1:
                        constants.append(line)
            
            # Create a structured summary
            summary_parts = []
            
            # Add imports section
            if imports:
                summary_parts.append("# IMPORTS")
                summary_parts.extend(imports[:20])  # Limit to first 20 imports
                if len(imports) > 20:
                    summary_parts.append(f"# ... and {len(imports) - 20} more imports")
                summary_parts.append("")
            
            # Add constants section
            if constants:
                summary_parts.append("# CONSTANTS")
                summary_parts.extend(constants[:20])  # Limit to first 20 constants
                if len(constants) > 20:
                    summary_parts.append(f"# ... and {len(constants) - 20} more constants")
                summary_parts.append("")
            
            # Add functions section
            if functions:
                summary_parts.append("# FUNCTIONS")
                summary_parts.extend(functions[:30])  # Limit to first 30 functions
                if len(functions) > 30:
                    summary_parts.append(f"# ... and {len(functions) - 30} more functions")
                summary_parts.append("")
            
            # Add classes section
            if classes:
                summary_parts.append("# CLASSES")
                summary_parts.extend(classes)
                summary_parts.append("")
            
            # Create overall summary
            file_summary = f"""SCRIPT SUMMARY FOR: {script_path}
File size: {os.path.getsize(script_path)/1024:.1f} KB
Last modified: {datetime.datetime.fromtimestamp(os.path.getmtime(script_path)).isoformat()}
Contains: {len(imports)} imports, {len(functions)} functions, {len(classes)} classes, {len(constants)} constants

{os.path.basename(script_path)} STRUCTURE:
{''.join(f"{part}\n" for part in summary_parts)}
"""

            return file_summary
        
        except Exception as e:
            console.print(f"[red]Error generating script summary: {str(e)}[/red]")
            return f"Error generating script summary: {str(e)}"
    
    elif name == "memory_stats":
        detail_level = tool_input.get("detail_level", "basic")
        console.print(f"[blue]Generating memory statistics:[/blue] {detail_level} level")
        
        # Calculate current cache and memory stats
        stats = {
            "file_cache": {
                "entries": len(file_cache),
                "hits": file_cache_stats["hits"],
                "misses": file_cache_stats["misses"],
                "bytes_saved": file_cache_stats["bytes_saved"],
                "estimated_tokens_saved": int(file_cache_stats["bytes_saved"] / 4) if file_cache_stats["bytes_saved"] > 0 else 0
            },
            "script_fingerprints": {
                "entries": len(script_fingerprints)
            },
            "tool_memory": {
                "entries": len(tool_memory)
            },
            "token_usage": {
                "current": current_token_usage,
                "budget": token_budget,
                "percentage_used": (current_token_usage / token_budget) * 100 if token_budget > 0 else 0,
                "remaining": token_budget - current_token_usage
            },
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Add cache hit rate
        total_requests = stats["file_cache"]["hits"] + stats["file_cache"]["misses"]
        if total_requests > 0:
            stats["file_cache"]["hit_rate"] = (stats["file_cache"]["hits"] / total_requests) * 100
        else:
            stats["file_cache"]["hit_rate"] = 0
        
        # Add estimated cost savings
        if stats["file_cache"]["estimated_tokens_saved"] > 0:
            tokens_saved = stats["file_cache"]["estimated_tokens_saved"]
            estimated_cost = tokens_saved * 0.000003  # $3 per million tokens
            stats["file_cache"]["estimated_cost_saved"] = estimated_cost
        
        # For detailed level, include recent tool invocations
        if detail_level == "detailed":
            # Add recent tool invocations (last 10)
            recent_tools = []
            
            for fingerprint, entry in sorted(
                tool_memory.items(), 
                key=lambda x: x[1]["timestamp"],
                reverse=True
            )[:10]:  # Get most recent 10
                # Include only safe information 
                recent_tools.append({
                    "name": entry["name"],
                    "timestamp": entry["timestamp"]
                })
                
            stats["tool_memory"]["recent_invocations"] = recent_tools
            
            # Add file cache keys (up to 20)
            file_cache_keys = list(file_cache.keys())[:20]
            stats["file_cache"]["recent_entries"] = file_cache_keys
            
        # Format response
        if detail_level == "basic":
            response = f"""MEMORY STATISTICS:

File Cache:
- Entries: {stats["file_cache"]["entries"]}
- Hits: {stats["file_cache"]["hits"]}
- Misses: {stats["file_cache"]["misses"]}
- Hit Rate: {stats["file_cache"]["hit_rate"]:.1f}%
- Bytes Saved: {stats["file_cache"]["bytes_saved"] / 1024:.1f} KB
- Estimated Tokens Saved: ~{stats["file_cache"]["estimated_tokens_saved"]:,}

Token Usage:
- Current Usage: {stats["token_usage"]["current"]:,} tokens
- Budget: {stats["token_usage"]["budget"]:,} tokens
- Used: {stats["token_usage"]["percentage_used"]:.1f}%
- Remaining: {stats["token_usage"]["remaining"]:,} tokens

Tool Memory:
- Cached Tool Results: {stats["tool_memory"]["entries"]}
- Script Fingerprints: {stats["script_fingerprints"]["entries"]}
"""
        else:
            # Detailed response
            response = f"""DETAILED MEMORY STATISTICS:

File Cache:
- Entries: {stats["file_cache"]["entries"]}
- Hits: {stats["file_cache"]["hits"]}
- Misses: {stats["file_cache"]["misses"]}
- Hit Rate: {stats["file_cache"]["hit_rate"]:.1f}%
- Bytes Saved: {stats["file_cache"]["bytes_saved"] / 1024:.1f} KB
- Estimated Tokens Saved: ~{stats["file_cache"]["estimated_tokens_saved"]:,}
- Estimated Cost Saved: ${stats["file_cache"].get("estimated_cost_saved", 0):.6f}

Token Usage:
- Current Usage: {stats["token_usage"]["current"]:,} tokens
- Budget: {stats["token_usage"]["budget"]:,} tokens
- Used: {stats["token_usage"]["percentage_used"]:.1f}%
- Remaining: {stats["token_usage"]["remaining"]:,} tokens

Tool Memory:
- Cached Tool Results: {stats["tool_memory"]["entries"]}
- Script Fingerprints: {stats["script_fingerprints"]["entries"]}

Recent Tool Invocations:
"""
            if "recent_invocations" in stats["tool_memory"]:
                for i, tool in enumerate(stats["tool_memory"]["recent_invocations"], 1):
                    response += f"{i}. {tool['name']} - {tool['timestamp']}\n"
            else:
                response += "No recent tool invocations\n"
                
            response += "\nRecent File Cache Entries:\n"
            if "recent_entries" in stats["file_cache"]:
                for i, key in enumerate(stats["file_cache"]["recent_entries"], 1):
                    response += f"{i}. {key}\n"
            else:
                response += "No recent file cache entries\n"
                
        return response
    
    elif name == "optimize_prompt":
        text = tool_input.get("text", "")
        target_reduction = tool_input.get("target_reduction", 30)
        preserve_key_elements = tool_input.get("preserve_key_elements", [])
        
        console.print(f"[blue]Optimizing prompt for token efficiency:[/blue] Target {target_reduction}% reduction")
        
        if not text:
            return "Error: No text provided to optimize"
            
        original_length = len(text)
        original_token_estimate = int(original_length / 4)  # Rough estimate
        
        # Function to count tokens more precisely (rough approximation)
        def estimate_tokens(text):
            # Very rough approximation: ~4 characters per token on average
            return int(len(text) / 4)
        
        # Create a fingerprint for this optimization request
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cache_key = f"optimize:{text_hash}:{target_reduction}"
        
        # Check if we've optimized this text before
        if cache_key in tool_memory:
            console.print(f"[green]Using cached optimization result[/green]")
            return tool_memory[cache_key]["result"]
        
        # Not cached, optimize the text manually with simple approaches
        
        # 1. Remove redundant whitespace
        optimized = ' '.join(text.split())
        
        # 2. Remove common filler phrases
        filler_phrases = [
            "please note that", "it's important to note that", "keep in mind that",
            "I would like to", "I want to", "I'd like to", "I need to",
            "in order to", "for the purpose of", "with the goal of",
            "in my opinion", "from my perspective", "as far as I can tell",
            "to be honest", "to tell you the truth", "frankly speaking",
            "basically", "essentially", "fundamentally", "generally speaking",
            "more or less", "for the most part", "as a matter of fact"
        ]
        
        for phrase in filler_phrases:
            optimized = optimized.replace(phrase, "")
            optimized = optimized.replace(phrase.capitalize(), "")
        
        # 3. Replace verbose expressions with concise ones
        replacements = {
            "due to the fact that": "because",
            "in spite of the fact that": "although",
            "in the event that": "if",
            "in the case of": "for",
            "a large number of": "many",
            "a majority of": "most",
            "a substantial amount of": "much",
            "at the present time": "now",
            "for the reason that": "since",
            "in the near future": "soon",
            "in close proximity to": "near",
            "it is necessary that": "must",
            "it is possible that": "may",
            "it is important to": "importantly",
            "prior to": "before",
            "subsequent to": "after",
            "with reference to": "about",
            "with regard to": "about",
            "in relation to": "about",
            "in connection with": "about",
            "in the process of": "",
            "on the basis of": "from",
            "in light of": "given",
            "with the exception of": "except",
            "for the purpose of": "to",
            "in order to": "to",
            "take into consideration": "consider",
            "utilize": "use",
            "modification": "change",
            "facilitate": "help",
            "demonstrate": "show",
            "sufficient": "enough",
            "approximately": "about",
            "additional": "more",
            "remainder": "rest",
            "has the ability to": "can",
            "has the capacity to": "can",
            "has the opportunity to": "can",
            "is able to": "can"
        }
        
        for verbose, concise in replacements.items():
            optimized = optimized.replace(verbose, concise)
            optimized = optimized.replace(verbose.capitalize(), concise.capitalize() if concise else "")
        
        # 4. Ensure key elements are preserved
        for element in preserve_key_elements:
            if element in text and element not in optimized:
                optimized = optimized.replace(element[:len(element)//2], element)
        
        # 5. Clean up any double spaces from replacements
        while "  " in optimized:
            optimized = optimized.replace("  ", " ")
        
        # Calculate how much we reduced
        optimized_length = len(optimized)
        reduction_percentage = ((original_length - optimized_length) / original_length) * 100
        original_tokens = estimate_tokens(text)
        optimized_tokens = estimate_tokens(optimized)
        tokens_saved = original_tokens - optimized_tokens
        
        # If we didn't hit our target, add a note
        target_note = ""
        if reduction_percentage < target_reduction:
            target_note = f"\nNote: Could only achieve {reduction_percentage:.1f}% reduction against target of {target_reduction}%. Further reduction might require semantic changes."
        
        # Format the response
        result = f"""OPTIMIZED PROMPT:

{optimized}

EFFICIENCY SUMMARY:
- Original length: {original_length} chars (~{original_tokens} tokens)
- Optimized length: {optimized_length} chars (~{optimized_tokens} tokens)
- Reduction: {reduction_percentage:.1f}% ({tokens_saved} tokens saved)
- Estimated cost savings: ${tokens_saved * 0.000003:.6f}{target_note}"""
        
        # Remember this optimization
        remember_tool_result(name, tool_input, result)
        
        return result
    
    # Create a fingerprint of the tool call
    call_fingerprint = hashlib.md5(f"{name}:{input_str}".encode()).hexdigest()
    
    # Store in tool memory
    tool_memory[call_fingerprint] = {
        "name": name,
        "input": tool_input,
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Limit memory size to prevent unbounded growth
    if len(tool_memory) > 100:  # Keep last 100 tool calls
        oldest_key = sorted(tool_memory.keys(), 
                            key=lambda k: tool_memory[k]["timestamp"])[0]
        del tool_memory[oldest_key]
        
    return True

def get_remembered_tool_result(name, tool_input):
    """Try to retrieve a remembered result for an identical previous tool call."""
    if not name or not tool_input:
        return None
        
    # Convert tool_input to a stable string representation for hashing
    if isinstance(tool_input, dict):
        sorted_items = sorted(tool_input.items())
        input_str = json.dumps(sorted_items)
    else:
        input_str = str(tool_input)
        
    # Create a fingerprint of the tool call
    call_fingerprint = hashlib.md5(f"{name}:{input_str}".encode()).hexdigest()
    
    # Check if we have this call in memory
    if call_fingerprint in tool_memory:
        # Only reuse recent results (within the last hour)
        timestamp = datetime.datetime.fromisoformat(tool_memory[call_fingerprint]["timestamp"])
        now = datetime.datetime.now()
        if (now - timestamp).total_seconds() < 3600:  # 1 hour
            return tool_memory[call_fingerprint]["result"]
            
    # Not found or too old
    return None

def reset_phase_loops(reason="Reset requested"):
    """Reset iteration counters to allow more processing within the same phase."""
    global current_iteration, phase_loops
    
    # Increment phase loop counter
    phase_loops += 1
    
    # Check if we've already looped too many times
    if phase_loops > 3:
        console.print(f"[yellow]Warning: Maximum phase loops reached ({phase_loops})[/yellow]")
        return "PHASE LOOPS EXCEEDED: You've already extended this phase multiple times. Please complete it or use workflow_adjustment to end it and continue to a new phase."
    
    # Reset iteration counter
    original_iterations = current_iteration
    current_iteration = 0
    
    console.print(f"[blue]Phase reset at iteration {original_iterations}. Starting new loop (phase loop {phase_loops}).[/blue]")
    console.print(f"[blue]Reason: {reason}[/blue]")
    
    return f"Phase reset successful. You now have {max_iterations} new iterations. Reason: {reason}"

def extract_tool_calls(text):
    """
    Extract tool calls from Claude's response text.
    
    Args:
        text (str): Claude's response text
        
    Returns:
        list: List of dictionaries with tool name and input
    """
    tool_calls = []
    
    # Various patterns Claude might use for tool calls
    patterns = [
        r'<tool:([^>]+)>\s*(\{.+?\})\s*</tool>',  # <tool:name> {json} </tool>
        r'tools\["([^"]+)"\]\((.*?)\)',  # tools["name"](args)
        r'tools\[\'([^\']+)\'\]\((.*?)\)',  # tools['name'](args)
        r'tools\.([A-Za-z0-9_]+)\((.*?)\)',  # tools.name(args)
        r'<function_calls>\s*<invoke name="([^"]+)">(.*?)</invoke>\s*'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            tool_name, tool_input_str = match
            
            # Try to parse the tool input as JSON
            try:
                # Handle keyword arguments format
                if '=' in tool_input_str and not (tool_input_str.strip().startswith('{') and tool_input_str.strip().endswith('}')):
                    # Convert keyword arguments to a dictionary
                    kwargs = {}
                    parts = tool_input_str.split(',')
                    for part in parts:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Remove quotes if present
                            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                                value = value[1:-1]
                            
                            # Try to convert value to appropriate type
                            if value.lower() == 'true':
                                value = True
                            elif value.lower() == 'false':
                                value = False
                            elif value.lower() == 'none':
                                value = None
                            else:
                                try:
                                    value = int(value)
                                except ValueError:
                                    try:
                                        value = float(value)
                                    except ValueError:
                                        pass  # Keep as string
                            
                            kwargs[key] = value
                    
                    tool_input = kwargs
                else:
                    # Clean the JSON string
                    clean_input = tool_input_str.strip()
                    if clean_input.startswith("```json"):
                        clean_input = clean_input[7:]
                    if clean_input.endswith("```"):
                        clean_input = clean_input[:-3]
                    
                    tool_input = json.loads(clean_input)
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to parse tool input: {str(e)}[/yellow]")
                # Fallback to the raw string
                tool_input = {"raw_input": tool_input_str}
            
            tool_calls.append({
                "name": tool_name,
                "input": tool_input
            })
    
    return tool_calls

async def main():
    """Main function for the SFA agent."""
    parser = argparse.ArgumentParser(description="Single-File Agent (SFA)")
    parser.add_argument("--config-file", required=True, help="Path to the JSON config file")
    parser.add_argument("--phase", type=int, default=0, help="Phase index in the config file")
    args = parser.parse_args()
    
    # Initialize token counter and set workflow info
    token_counter = TokenCounter()
    token_counter.set_workflow_info(args.config_file)
    
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
    
    # Reset global state variables
    global conversation_history, current_iteration, max_iterations, phase_loops
    global should_continue_iterations, saved_outputs, phase_complete, task_complete
    
    # Initialize/reset global variables
    conversation_history = []
    current_iteration = 0
    phase_loops = 0
    should_continue_iterations = True
    phase_complete = False
    task_complete = False
    saved_outputs = set()
    
    # Prepare system message with cache control for prompt caching
    system_message = task
    
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
    initial_message += f"\nYour output should be saved to: {', '.join(output_path)}\n"
    
    # Add information about available tools
    if tools_for_phase:
        initial_message += "\nAvailable Tools:\n"
        if "token_counter" in tools_for_phase:
            initial_message += "- token_counter: Use this to check token counts before saving\n"
        if "task_report" in tools_for_phase:
            initial_message += "- task_report: Use this to generate a structured report of your progress\n"
    
    initial_message += "\nPlease explore these resources as needed using the provided tools."

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
    
    # Improved display configuration with horizontal rule
    console.print("───────────────────────")
    console.print(f"Workflow: `{workflow_key}`")
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
    conversation_history = []
    
    # Add the user message
    conversation_history.append({
        "role": "user",
        "content": initial_message
    })
    
    # Create a global tools variable for the agent to use
    globals()["tools"] = tools_for_phase
    
    # Run the agent loop
    while current_iteration < max_iterations and should_continue_iterations:
        current_iteration += 1
        console.print(f"─────────────────────────────  Loop {current_iteration}/{max_iterations}  ─────────────────────────────")
        
        try:
            # Call Claude
            console.print("[cyan]Calling Claude...[/cyan]")
            try:
                # Try with beta features first
                response = anthropic_client.beta.messages.create(
                    model="claude-3-sonnet-20240229",  # Use a known working model
                    system=system_message,
                    messages=conversation_history,
                    max_tokens=4096,
                    temperature=0.3,
                    betas=["output-128k-2025-02-19"]  # Add 128k token beta
                )
            except (AttributeError, ValueError) as e:
                # Fall back to standard client if beta not available
                console.print(f"[yellow]Beta API error: {str(e)}[/yellow]")
                console.print("[yellow]Using API without beta features...[/yellow]")
                response = anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",  # Use a known working model
                    system=system_message,
                    messages=conversation_history,
                    max_tokens=4096,
                    temperature=0.3
                )
            
            # Extract the response content - handle different response formats
            assistant_message = {"role": "assistant"}
            
            # Check the response structure and extract content accordingly
            if hasattr(response, 'content') and response.content:
                if isinstance(response.content, list) and len(response.content) > 0:
                    if hasattr(response.content[0], 'text'):
                        assistant_message["content"] = response.content[0].text
                    elif isinstance(response.content[0], dict) and 'text' in response.content[0]:
                        assistant_message["content"] = response.content[0]['text']
                elif isinstance(response.content, str):
                    assistant_message["content"] = response.content
            # Fallback if normal content extraction fails
            elif hasattr(response, 'text'):
                assistant_message["content"] = response.text
            elif hasattr(response, 'message') and hasattr(response.message, 'content'):
                assistant_message["content"] = response.message.content
            else:
                # Last resort - convert the entire response to a string
                assistant_message["content"] = str(response)
                console.print("[yellow]Warning: Could not extract content properly from Claude response[/yellow]")
            
            # Add Claude's response to conversation history
            conversation_history.append(assistant_message)
            
            # Display a portion of Claude's response
            text = assistant_message["content"]
            display_length = min(len(text), 1500)
            claude_text = text[:display_length]
            if display_length < len(text):
                claude_text += "..."
            console.print(claude_text)
            
            # Process any tool calls in the response
            tool_calls = extract_tool_calls(text)
            
            if tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call["name"]
                    tool_input = tool_call["input"]
                    
                    console.print(f"[blue]Tool:[/blue] {tool_name}")
                    
                    # Execute the tool
                    tool_result = await handle_tool_call(tool_name, tool_input)
                    
                    # Add the tool result to the conversation history
                    conversation_history.append({
                        "role": "user",
                        "content": f"TOOL RESULT: {tool_result}"
                    })
                    
                    # Check if this is a task completion or workflow adjustment
                    if tool_name == "complete_task" or tool_name == "workflow_adjustment":
                        should_continue_iterations = False
                        break
            
            # Check if we're approaching the maximum number of iterations
            if current_iteration >= max_iterations - 3 and current_iteration < max_iterations:
                console.print(f"[yellow]Warning: Approaching maximum iterations ({current_iteration}/{max_iterations})[/yellow]")
                
        except Exception as e:
            console.print(f"[red]Error in agent loop:[/red] {str(e)}")
            import traceback
            console.print(traceback.format_exc())
    
    if current_iteration >= max_iterations and should_continue_iterations:
        console.print("[yellow]Reached maximum iterations without completing the task[/yellow]")
    
    # Half-width horizontal rule to end the phase
    console.print("───────────────────────")
    
    # Display token usage statistics
    token_counter.display_stats()
    token_counter._save_counters()  # Save token stats for cross-phase tracking

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        import traceback
        console.print(f"[red]Fatal error:[/red] {str(e)}")
        console.print(traceback.format_exc())
        sys.exit(1)