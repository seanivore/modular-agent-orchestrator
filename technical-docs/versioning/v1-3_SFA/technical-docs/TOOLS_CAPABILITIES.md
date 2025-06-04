# Tools and Capabilities

This document provides a comprehensive reference of all tools available to the Single-File Agent, their implementation details, and how to extend the system with new tools.

## Tool System Overview [v1_0_0, enhanced v3_0_0]

The SFA tool system provides a structured way for the agent to interact with its environment. Each tool is defined with a name, description, and input schema, and has a corresponding implementation function.

### Tool Definition Structure

```python
{
    "name": "tool_name",
    "description": "What the tool does and when to use it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string", 
                "description": "Description of parameter"
            },
            "param2": {
                "type": "integer",
                "description": "Description of parameter"
            }
        },
        "required": ["param1"]
    }
}
```

### Tool Implementation Pattern

```python
async def handle_tool_call(name, tool_input):
    if name == "tool_name":
        param1 = tool_input.get("param1")
        param2 = tool_input.get("param2", default_value)
        
        try:
            # Tool implementation
            result = operation(param1, param2)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
```

## File Operation Tools

### read_file [v1_0_0]

Reads content from a file.

```python
{
    "name": "read_file",
    "description": "Read the content of a file from the local filesystem.",
    "input_schema": {
        "type": "object",
        "properties": {"file_path": {"type": "string"}},
        "required": ["file_path"]
    }
}
```

Implementation:
```python
async def handle_tool_call(name, tool_input):
    if name == "read_file":
        file_path = tool_input.get("file_path")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
```

### read_multiple_files [v3_0_0]

Reads content from multiple files simultaneously.

```python
{
    "name": "read_multiple_files",
    "description": "Read the contents of multiple files simultaneously. This is more efficient than reading files one by one when you need to analyze or compare multiple files.",
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
}
```

### list_directory [v1_0_0]

Lists files in a directory.

```python
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
}
```

### search_files [v3_0_0]

Searches for files matching a pattern recursively.

```python
{
    "name": "search_files",
    "description": "Recursively search for files and directories matching a pattern. Searches through all subdirectories from the starting path.",
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
}
```

### get_file_info [v3_0_0]

Retrieves detailed metadata about a file or directory.

```python
{
    "name": "get_file_info",
    "description": "Retrieve detailed metadata about a file or directory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file or directory"}
        },
        "required": ["path"]
    }
}
```

### save_output [v1_0_0]

Saves content to a file.

```python
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
}
```

### text_editor [v3_1_0]

Advanced text editor for creating and modifying files.

```python
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
}
```

### move_file [v3_0_0]

Moves or renames a file.

```python
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
}
```

### delete_file [v3_0_0]

Deletes a file from the filesystem.

```python
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
}
```

## Decision Making Tools

### think [v3_0_0]

Allows Claude to process complex information.

```python
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
}
```

### make_decision [v3_0_0]

Helps Claude choose between options with reasoning.

```python
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
}
```

## Task Management Tools

### complete_task [v3_0_0]

Signals that the task is complete.

```python
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
```

### workflow_adjustment [v3_0_0]

Adjusts the current workflow phase.

```python
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
}
```

## Web Tools

### web_search [v1_0_0]

Searches the web using Brave Search API.

```python
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
}
```

### perplexity_search [v3_2_0]

Advanced search using Perplexity AI.

```python
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
}
```

## Vision Tools

### analyze_image [v3_0_0]

Analyzes images using Claude's vision capabilities.

```python
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
}
```

### edit_image [v3_1_0]

Edits images with resize, crop, and text operations.

```python
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
}
```

## Performance Tools

### token_counter [v3_2_0]

Counts tokens in text or files.

```python
{
    "name": "token_counter",
    "description": "Count tokens in text or files.",
    "input_schema": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Text to count tokens for"
            },
            "file_path": {
                "type": "string",
                "description": "File path to count tokens for"
            },
            "dir_path": {
                "type": "string",
                "description": "Directory path to scan for token counts"
            }
        }
    }
}
```

### task_report [v3_0_0]

Creates a comprehensive task report.

```python
{
    "name": "task_report",
    "description": "Create a phase summary report that includes token counts, accomplishments, and next steps. This will trigger phase completion.",
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Optional content to save to files"
            },
            "file_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of file paths where content will be saved"
            },
            "report": {
                "type": "string",
                "description": "Summary of what was accomplished in this phase"
            },
            "next_steps": {
                "type": "string",
                "description": "Recommendations for the next phase"
            },
            "decision": {
                "type": "object",
                "description": "Decision output if this phase involved making a choice",
                "properties": {
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of options that were considered"
                    },
                    "choice": {
                        "type": "string",
                        "description": "The selected option"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Explanation for the decision"
                    }
                }
            }
        },
        "required": ["report", "next_steps"]
    }
}
```

## Adding Custom Tools

The SFA can be extended with custom tools by adding Python modules to the tools directory. The main agent script automatically detects and loads these tools.

### Tool Module Structure

```python
def my_custom_tool(param1, param2, param3=None):
    """
    Custom tool description.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        param3: Optional parameter with default value
        
    Returns:
        Dictionary with result data or error message
    """
    try:
        # Tool implementation
        result = do_something(param1, param2, param3)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def get_tool_definition():
    """Return the tool definition for SFA integration."""
    return {
        "name": "my_custom_tool",
        "description": "What this tool does and when to use it.",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of first parameter"
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of second parameter"
                },
                "param3": {
                    "type": "boolean",
                    "description": "Optional parameter",
                    "default": False
                }
            },
            "required": ["param1", "param2"]
        },
        "function": my_custom_tool
    }
```

### Tool Registration

The SFA automatically loads tools from the tools directory:

```python
# Load available tools
available_tools = {}
tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
if os.path.exists(tools_dir):
    sys.path.append(tools_dir)
    
    # Try to load custom tool
    try:
        from tools.my_module import my_custom_tool
        available_tools["my_custom_tool"] = my_custom_tool
        console.print("[green]Custom tool loaded successfully[/green]")
    except ImportError:
        console.print("[yellow]Custom tool not found[/yellow]")
```

### Tool Usage Best Practices

1. **Input Validation**: Always validate input parameters
2. **Error Handling**: Wrap tool logic in try/except blocks
3. **Structured Output**: Return consistent dictionary structures
4. **Documentation**: Include detailed descriptions for Claude
5. **Token Awareness**: Consider token usage in tool results
6. **Progress Feedback**: Log progress information for long-running operations
7. **Resource Management**: Properly close files and connections
8. **Context Integration**: Make tool results blend well with conversation context