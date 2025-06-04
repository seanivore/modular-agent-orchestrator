# v3_3_0: Requesty API Integration and Model Selection

## Overview

This update adds support for using multiple LLM providers through the Requesty API and implements the agent file variable feature for improved version management.

Start date: May 21, 2025
Completion date: [TBD]

## Key Features

1. **Requesty API Integration**: Added support for Requesty API, allowing the use of models from various providers:
   - Google Gemini models (e.g., `google/gemini-2.5-pro-exp-03-25`)
   - Anthropic Claude models (e.g., `anthropic/claude-3-7-sonnet-latest`)
   - OpenAI GPT models (e.g., `openai/gpt-4.1-nano`)
   - Vertex AI models (e.g., `vertex/anthropic/claude-3-7-sonnet-latest`)

2. **Model Selection Parameter**: Added the `M` configuration variable and `--model` flag for selecting models.

3. **Agent File Variable Support**: Implemented logic to automatically use the appropriate agent file version.

## Implementation Details

### OpenAI Dependency Addition
Added OpenAI SDK to dependencies for communicating with Requesty API:
```python
# /// script
# dependencies = [
#   ...
#   "openai>=1.4.0"  # Added for Requesty API integration
# ]
# ///
```

### Requesty Client Initialization
Added initialization code for the Requesty client:
```python
requesty_api_key = os.getenv("ROUTER_API_KEY")
requesty_client = None
if requesty_api_key:
    import openai
    requesty_client = openai.OpenAI(
        api_key=requesty_api_key,
        base_url="https://router.requesty.ai/v1",
        default_headers={"Authorization": f"Bearer {requesty_api_key}"}
    )
```

### Format Conversion Functions
Added functions to convert between Claude and OpenAI formats:
- `convert_to_openai_format()`: Converts Claude message format to OpenAI format
- `convert_tools_to_openai_format()`: Converts Claude tool format to OpenAI format
- `process_openai_response()`: Processes OpenAI-format responses
- `extract_openai_tool_inputs()`: Extracts tool inputs from OpenAI format

### Agent Loop Modifications
Modified the agent loop to use the appropriate client based on model selection:
- Added model detection from config or command line
- Added conditional logic to use Requesty or Claude
- Added fallback to Claude if Requesty fails

### Setup Script Changes
Modified `sfa_workflow.sh` to:
- Accept model parameter (`-m` or `--model`)
- Extract model from config file
- Find the appropriate agent file
- Pass model parameter to the agent

## Configuration Examples

Example configuration with model selection:
```json
{
  "A": "research-report",
  "F": "use-case/doc-research-simple/",
  "M": "google/gemini-2.5-pro-exp-03-25",
  "research": {
    // ... tasks as before
  }
}
```

## Usage Examples

Using a specific model with an existing workflow:
```bash
research-report --model google/gemini-2.5-pro-exp-03-25
```

Or directly:
```bash
sfa -e use-case/doc-research-simple/doc-research-simple-config.json --model google/gemini-2.5-pro-exp-03-25
```

## Environment Setup

Add the Requesty API key to your `.env` file:
```
ROUTER_API_KEY=your_requesty_api_key
```

## Tests

1. Integration Test (test_requesty_integration.py):

  - Tests end-to-end functionality with different models
  - Compares performance between Requesty models and Claude
  - Verifies proper model selection from config and command line
  - Tests fallback behavior with invalid models

2. Unit Test (test_requesty_format_conversion.py):

  - Tests the format conversion functions between Claude and OpenAI formats
  - Ensures correct handling of different message and tool formats

3. Agent File Selection Test (test_agent_file_selection.sh):

  - Verifies the sfa_workflow.sh selects the correct agent file version


## Known Limitations

1. No streaming support for Requesty models initially
2. Tool behavior may vary slightly between models
3. Some specialized tools may not work identically across all models

## Future Enhancements

1. Add support for model-specific features (e.g., OpenAI's image generation)
2. Implement streaming responses for Requesty models
3. Add model-specific performance optimizations
4. Create model fallback chains

----
----

### SFA v3_3_0 Changes

```python
# Changes needed for sfa_v3_3_0_main.py

# 1. Update dependencies - add OpenAI
# Find the dependencies section at the top of the file and add openai
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

# 2. Add imports and client setup logic
# After the "import datetime" line, add:
import json as json_module  # Rename to avoid conflict

# 2.5. After the "Load environment variables" section, add:
# Initialize Requesty client if API key exists
requesty_api_key = os.getenv("ROUTER_API_KEY")
requesty_client = None
if requesty_api_key:
    try:
        import openai
        requesty_client = openai.OpenAI(
            api_key=requesty_api_key,
            base_url="https://router.requesty.ai/v1",
            default_headers={"Authorization": f"Bearer {requesty_api_key}"}
        )
        console.print("[green]Requesty API client initialized successfully[/green]")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not initialize Requesty client: {str(e)}[/yellow]")

# 3. Add conversion functions
# Add these after the token counter class

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

# 4. Modify main function to accept model parameter
# Find the argparse section and add model argument
parser.add_argument("--model", type=str, help="Model to use for the agent")

# 5. Update main() function to handle model parameter
# In the main function, after parsing arguments:
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

# 6. Update agent loop to use appropriate client
# Replace the Claude API call in the agent loop:

# Inside your main loop where you call Claude
try:
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
                    
                    # Check for workflow adjustment, etc. as in original code
                    
        except Exception as e:
            console.print(f"[red]Error with Requesty API:[/red] {str(e)}")
            console.print(f"[yellow]Falling back to Claude...[/yellow]")
            using_requesty = False
            # Only fall back if we have a valid Claude client
            if os.getenv("ANTHROPIC_API_KEY"):
                # Continue to Claude code
            else:
                raise e
    
    # If not using Requesty or fallback to Claude
    if not using_requesty:
        # Original Claude code
        # [Keep the original Claude API call here]

except Exception as e:
    console.print(f"[red]Error in agent loop:[/red] {str(e)}")
    import traceback
    console.print(traceback.format_exc())

# 7. Update sfa_workflow.sh script
# This will be in a separate file
``` 

### SFA Workflow Script Updates 

```bash
# Changes needed for setup-scripts/sfa_workflow.sh

# 1. Add model parameter to the argument parser section
# Find the argument parsing section and add:

# Parse arguments
# After the "-r|--readme)" section, add:
-m|--model)
    MODEL="$2"
    shift 2
    ;;

# 2. Extract model from config file
# Inside the CONFIG_INFO extraction, add model extraction:

# Find the workflow key (first key that's not 'A' or 'F' or 'M')
workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F' and k != 'M'), None)
if not workflow_key:
    print('Error: Invalid config file format - no workflow key found')
    sys.exit(1)

# Get command name
command = config.get('A', '')
use_case_dir = config.get('F', '')
model = config.get('M', '')  # Extract model if present
if not command or not use_case_dir:
    print('Error: Invalid config file format - missing required A and F variables')
    sys.exit(1)

# Add model to output
print(json.dumps({
    'format': format_type,
    'workflow_key': workflow_key,
    'command': command,
    'use_case': use_case,
    'use_case_dir': use_case_dir,
    'model': model,  # Include model in output
    'num_tasks': num_tasks,
    'task_labels': task_labels
}))

# 3. Add agent file logic
# After extracting CONFIG_INFO, add:

# Extract model from config
MODEL=${MODEL:-"$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin).get('model', ''))"}"}

# Find agent file
AGENT_FILE=""
for file in $(find "$PARENT_DIR" -maxdepth 1 -name "sfa_v*.py" | sort -V); do
    # If we find an exact match for v3_3_0, use it directly
    if [[ $(basename "$file") == "sfa_v3_3_0_main.py" ]]; then
        AGENT_FILE=$(basename "$file")
        break
    fi
    # Otherwise keep track of the oldest version
    if [ -z "$AGENT_FILE" ]; then
        AGENT_FILE=$(basename "$file")
    fi
done

if [ -z "$AGENT_FILE" ]; then
    echo "Error: No agent file found in project root. Please ensure at least one agent file exists."
    exit 1
fi

echo "Using agent file: $AGENT_FILE"

# 4. Update run_task function to pass model parameter
# Find the run_task function and update the Python call:

# Run the task
if [ -n "$MODEL" ]; then
    echo "Using model: $MODEL"
    python3 "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index" --model "$MODEL"
else
    python3 "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index"
fi
```

