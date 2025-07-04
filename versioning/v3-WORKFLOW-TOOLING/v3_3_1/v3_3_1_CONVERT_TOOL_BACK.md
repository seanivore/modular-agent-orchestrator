# Convert OpenAI API Tool Call Back to Anthropic 

More comprehensive solution for the Requesty tool call conversion issue.

Here's the complete set of changes needed to properly handle tool calls from Requesty:

## 1. Add a New Conversion Function for OpenAI to Claude Format

```python
def convert_openai_tool_calls_to_claude_format(openai_tool_calls):
    """Convert OpenAI format tool calls to Claude format."""
    claude_format_tool_calls = []
    
    for tool_call in openai_tool_calls:
        try:
            # Extract the function arguments as a Python dict
            arguments = json.loads(tool_call.function.arguments)
            
            # Create Claude-format tool call
            claude_tool_call = {
                "type": "tool_use",
                "id": tool_call.id,
                "name": tool_call.function.name,
                "input": arguments
            }
            claude_format_tool_calls.append(claude_tool_call)
        except Exception as e:
            console.print(f"[yellow]Warning: Error converting tool call: {str(e)}[/yellow]")
            # Create a simplified version if JSON parsing fails
            claude_tool_call = {
                "type": "tool_use",
                "id": tool_call.id,
                "name": tool_call.function.name,
                "input": {"raw_arguments": tool_call.function.arguments}
            }
            claude_format_tool_calls.append(claude_tool_call)
    
    return claude_format_tool_calls
```

## 2. Modify the OpenAI Response Processing

Replace the existing `process_openai_response` function with this more robust version:

```python
def process_openai_response(response, conversation_history):
    """Process OpenAI-format response and update conversation history."""
    # Extract the message content
    message_content = response.choices[0].message.content or ""
    
    # Check for tool calls
    openai_tool_calls = []
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        openai_tool_calls = response.choices[0].message.tool_calls
        
        # Convert OpenAI tool calls to Claude format
        claude_tool_calls = convert_openai_tool_calls_to_claude_format(openai_tool_calls)
        
        # Add assistant message with converted tool calls to conversation history
        content_items = []
        if message_content:
            content_items.append({"type": "text", "text": message_content})
        content_items.extend(claude_tool_calls)
        
        conversation_history.append({
            "role": "assistant",
            "content": content_items
        })
    else:
        # No tool calls, just add the content response
        conversation_history.append({
            "role": "assistant",
            "content": message_content
        })
    
    return openai_tool_calls
```

## 3. Fix the Requesty API Tool Handling Section

Replace the existing Requesty tool handling code with this improved version:

```python
# In the main agent loop, replace this section:
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
        
        # Get tokens if available - use safer access method with defaults
        input_tokens = 0
        output_tokens = 0
        
        # Handle potential differences in usage reporting format
        if hasattr(response, 'usage'):
            usage = response.usage
            if hasattr(usage, 'prompt_tokens'):
                input_tokens = usage.prompt_tokens
            elif hasattr(usage, 'get') and callable(usage.get):
                input_tokens = usage.get('prompt_tokens', 0)
                
            if hasattr(usage, 'completion_tokens'):
                output_tokens = usage.completion_tokens
            elif hasattr(usage, 'get') and callable(usage.get):
                output_tokens = usage.get('completion_tokens', 0)
        
        # Update token counter
        token_counter.update(
            input_tokens=input_tokens, 
            output_tokens=output_tokens
        )
        
        console.print(f"[magenta]Token Usage - Current:[/magenta] Input: {input_tokens:,} | Output: {output_tokens:,}")
        console.print(f"[magenta]Token Usage - Total:[/magenta] Input: {token_counter.total_input_tokens:,} | Output: {token_counter.total_output_tokens:,} | Cost: ${token_counter.total_cost:.6f}")
        
        # Process the response - this now handles converting tool calls
        tool_calls = process_openai_response(response, conversation_history)
        
        # Handle tool calls - the processing now matches Claude's expected format
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_id = tool_call.id
                tool_input = extract_openai_tool_inputs(tool_call)
                
                console.print(f"[blue]Tool request from Requesty:[/blue] {tool_name}")
                
                # Process tool call as before
                tool_result = await handle_tool_call(tool_name, tool_input)
                
                # Add tool result to conversation in Claude format
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
                # [KEEP EXISTING LOGIC HERE]
                
    except Exception as e:
        console.print(f"[red]Error with Requesty API:[/red] {str(e)}")
        console.print(f"[yellow]Falling back to Claude...[/yellow]")
        using_requesty = False
        # Only fall back if we have a valid Claude client
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise e
```

## 4. Add Error Handling for CompletionUsage Issues

Add this helper function to safely handle various response formats:

```python
def safe_get_token_usage(response):
    """Safely extract token usage from various response formats."""
    input_tokens = 0
    output_tokens = 0
    
    try:
        # Handle OpenAI/Requesty format
        if hasattr(response, 'usage'):
            usage = response.usage
            # Try different access methods
            if hasattr(usage, 'prompt_tokens'):
                input_tokens = usage.prompt_tokens
            elif hasattr(usage, 'get') and callable(usage.get):
                input_tokens = usage.get('prompt_tokens', 0)
            elif isinstance(usage, dict):
                input_tokens = usage.get('prompt_tokens', 0)
                
            if hasattr(usage, 'completion_tokens'):
                output_tokens = usage.completion_tokens
            elif hasattr(usage, 'get') and callable(usage.get):
                output_tokens = usage.get('completion_tokens', 0)
            elif isinstance(usage, dict):
                output_tokens = usage.get('completion_tokens', 0)
        
        # Handle Anthropic format
        elif hasattr(response, 'usage'):
            input_tokens = getattr(response.usage, 'input_tokens', 0)
            output_tokens = getattr(response.usage, 'output_tokens', 0)
    except Exception as e:
        console.print(f"[yellow]Warning: Error extracting token usage: {str(e)}[/yellow]")
        # Continue with default values
    
    return input_tokens, output_tokens
```

## Implementation Details

1. These changes maintain backward compatibility with the existing code
2. They add robust error handling to prevent crashes when unexpected formats are encountered
3. The format conversion is bidirectional now - Claude to OpenAI for requests, OpenAI to Claude for responses
4. Token usage extraction is made more flexible to handle different response formats

This approach should solve the issue with Requesty tool calls and make your system more robust for future integrations with other API providers. The key insight was recognizing that we need to convert both ways between the formats.

Let me know if you'd like me to expand on any part of this solution or if there are other aspects of the system you'd like me to help with!
