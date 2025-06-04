# Performance Optimization

This document details the performance optimization techniques used in the Single-File Agent, including token management, caching strategies, and optimization techniques.

## Token Management [v3_0_0, enhanced v3_2_0]

The SFA implements sophisticated token management to optimize cost and efficiency.

### Token Counting

The TokenCounter class tracks both input and output tokens, as well as associated costs:

```python
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
        
        # Initialize cumulative counters
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
```

### Token Output Validation [v3_2_0]

The system automatically checks if output content exceeds token limits before saving:

```python
# Check token count before saving
token_result = available_tools["token_counter"](text=content)

if not token_result["is_safe"]:
    # Token count exceeds safe limit
    console.print(f"[yellow]Warning:[/yellow] Content exceeds safe token limit ({token_result['token_count']} tokens)")
    console.print("[yellow]Starting revision phase...[/yellow]")
    
    # Reset phase loops instead of ending
    task_complete = reset_phase_loops(
        f"Document exceeds token limit ({token_result['token_count']} tokens). Please revise to reduce content while maintaining key information."
    )
    
    return f"⚠️ CRITICAL: Your content ({token_result['token_count']} tokens) exceeds the safe limit (7000 tokens). The file was NOT saved. Please revise your content to be under 7000 tokens."
```

### Token Statistics Tracking [v3_2_0]

The agent tracks token usage statistics across workflow runs:

```python
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
        
        # Write JSON that always works
        with open(self.stats_file_path, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False, sort_keys=False)
            # Add a newline at the end for better readability
            f.write('\n')
            
        console.print(f"[blue]Token stats saved to:[/blue] {self.stats_file_path}")
    except Exception as e:
        console.print(f"[yellow]Error saving token stats: {str(e)}[/yellow]")
```

### Token Display and Reporting [v3_2_0]

Token usage is presented in a clear, tabular format:

```python
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
```

## Prompt Caching [v3_2_0]

The SFA utilizes Claude's prompt caching feature to reduce token usage and improve response time.

### Enabling Prompt Caching

```python
response = anthropic_client.beta.messages.create(
    model=CLAUDE_MODEL,
    system=system_message,
    messages=conversation_history,
    max_tokens=8192,
    tools=TOOLS,
    temperature=0.3,
    betas=["token-efficient-tools-2025-02-19", "prompt-caching-2024-07-31"]
)
```

### Cache Performance Tracking

```python
# Track cache performance metrics
cache_creation_tokens = getattr(response.usage, 'cache_creation_input_tokens', 0)
cache_read_tokens = getattr(response.usage, 'cache_read_input_tokens', 0)
input_tokens = getattr(response.usage, 'input_tokens', 0)
output_tokens = getattr(response.usage, 'output_tokens', 0)

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
```

### Cache Control for System Messages

```python
system_message = [{
    "type": "text",
    "text": task,
    "cache_control": {"type": "ephemeral"}
}]
```

## Script Caching [v3_2_0]

The SFA implements a caching mechanism for script files to avoid repeatedly tokenizing large code files.

### Script Cache Implementation

```python
# Simple cache for script files to prevent redundant reading of large files
script_cache = {}

# In read_file tool implementation
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
```

### Script Cache Statistics

```python
# Display script cache statistics
if len(script_cache) > 0:
    total_bytes = sum(len(content) for content in script_cache.values())
    console.print("\n[bold green]Script Cache Performance:[/bold green]")
    console.print(f"[green]Scripts cached:[/green] {len(script_cache)}")
    console.print(f"[green]Total size:[/green] {total_bytes/1024:.1f} KB")
```

## Context Window Management [v3_0_0]

The SFA implements several strategies to manage the context window efficiently.

### Context Estimation

```python
# Estimate rough token count of conversation history
history_tokens = sum(len(msg.get("content", "")) for msg in conversation_history) / 4  # rough estimate
            
if history_tokens > 50000:
    return f"""WARNING: Your context window is getting full (approx. {int(history_tokens)} tokens).
Continuing may lead to context limitations. Consider:
1. Using 'ADD_PHASE_TO_WORKFLOW_AND_END' instead to get a fresh context window
2. If you continue, focus only on the most critical remaining tasks
3. Prepare handoff information in case you reach token limits

Your loops have been reset to 0/{max_iterations}. Continue with caution."""
```

### Phase Continuation

The agent can reset its loop counter to continue in the same context window:

```python
def reset_phase_loops(message):
    """Reset the phase loop counter to extend iterations."""
    global max_iterations, current_iteration, phase_loops
    
    phase_loops += 1
    prev_max = max_iterations
    current_iteration = 0
    max_iterations = DEFAULT_MAX_ITERATIONS
    
    console.print(f"[green]Extension #{phase_loops}: {message}[/green]")
    console.print(f"[blue]Reset iteration counter: {prev_max}/{prev_max} → 0/{max_iterations}[/blue]")
    
    return f"Extended processing time: {message}"
```

## Token-Efficient Tools [v3_2_0]

The SFA leverages Claude's token-efficient-tools beta, which can reduce token usage by up to 70% for tool-heavy interactions.

```python
response = anthropic_client.beta.messages.create(
    model=CLAUDE_MODEL,
    system=system_message,
    messages=conversation_history,
    max_tokens=8192,
    tools=TOOLS,
    temperature=0.3,
    betas=["token-efficient-tools-2025-02-19", "prompt-caching-2024-07-31"]
)
```

### Fallback Mechanism

```python
try:
    # Try with beta client for token-efficient-tools and prompt caching
    response = anthropic_client.beta.messages.create(
        model=CLAUDE_MODEL,
        system=system_message,
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
        model=CLAUDE_MODEL,
        system=task,
        messages=conversation_history,
        max_tokens=8192,
        tools=TOOLS,
        temperature=0.3
    )
```

## Batch Processing [v3_0_0]

The SFA supports batch operations to reduce context window usage and API calls.

### Reading Multiple Files

```python
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
}
```

### Implementation

```python
def read_multiple_files(paths):
    """Read the contents of multiple files simultaneously."""
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
```

## Performance Best Practices

1. **Use Token-Efficient Features**: Enable token-efficient-tools and prompt caching betas when available
2. **Batch Operations**: Use batch operations like read_multiple_files instead of multiple single reads
3. **Monitor Context Size**: Track conversation history size and use phase adjustment when needed
4. **Cache Heavy Content**: Use caching for script files and other large content
5. **Script Protection**: Avoid reading large scripts directly, use summaries or targeted sections
6. **Output Validation**: Always check token counts before saving large outputs
7. **Efficient Responses**: Structure tool responses to minimize token usage while maintaining clarity
8. **Phase Management**: Use phase continuation for related tasks, new phases for context reset
9. **Performance Stats**: Track token usage and cache performance metrics
10. **Optimize Images**: Use efficient formats (webp) and appropriate compression for images