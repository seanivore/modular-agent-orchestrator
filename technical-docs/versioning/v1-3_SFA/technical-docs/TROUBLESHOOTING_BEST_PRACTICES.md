# Troubleshooting and Best Practices

This document provides guidance for troubleshooting common issues and following best practices when working with Single-File Agents.

## Error Handling [v3_0_0]

### Common Error Types

The SFA implements comprehensive error handling for various scenarios:

1. **Configuration Errors**: Issues with the JSON configuration file
2. **File Operation Errors**: Problems with reading, writing, or manipulating files
3. **API Errors**: Issues with Anthropic API or other external services
4. **Tool Execution Errors**: Problems executing specific tools
5. **Workflow Errors**: Issues with workflow execution or phase transitions

### Error Handling Implementation

All tool implementations use try/except blocks:

```python
try:
    # Tool implementation
    result = operation()
    return result
except Exception as e:
    return f"Error: {str(e)}"
```

For critical operations, the error is logged and returned to Claude:

```python
try:
    # Critical operation
    result = critical_operation()
    return result
except Exception as e:
    console.print(f"[red]Critical error in {operation_name}:[/red] {str(e)}")
    import traceback
    console.print(traceback.format_exc())
    return f"Error executing {operation_name}: {str(e)}"
```

### File Backup on Error

For operations that modify files, the agent creates backups:

```python
# Make a backup of the file before editing
backup_path = f"{path}.bak"
try:
    with open(path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
except Exception as e:
    console.print(f"[yellow]Warning: Could not create backup of '{path}': {str(e)}[/yellow]")

# If error occurs during modification
if error_occurred:
    # Try to restore from backup
    if os.path.exists(backup_path):
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            console.print(f"[green]Restored original file from backup after error[/green]")
        except Exception as restore_error:
            console.print(f"[red]Error restoring from backup: {str(restore_error)}[/red]")
```

## Common Issues

### 1. Token Limits [v3_2_0]

**Issue**: Content exceeds token limits, causing phase failure.

**Solution**:
- The agent automatically checks token counts before saving files
- If content exceeds the safe limit (7000 tokens), it initiates a revision phase
- The workflow is reset to allow for content revision

```python
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

### 2. Context Window Limitations [v3_0_0]

**Issue**: Context window fills up during complex tasks.

**Solution**:
- The agent monitors context size and provides warnings
- Options for handling context limitations:
  - Use ADD_PHASE_AND_CONTINUE for related tasks
  - Use ADD_PHASE_TO_WORKFLOW_AND_END for fresh context
  - Create phase summaries for continuity

### 3. API Rate Limits [v3_2_0]

**Issue**: Hitting Anthropic API rate limits.

**Solution**:
- The agent implements exponential backoff for API calls
- Console warnings indicate rate limit issues
- Token usage statistics help monitor API consumption

### 4. File Permission Issues [v3_0_0]

**Issue**: Unable to read or write files due to permissions.

**Solution**:
- The agent checks directory existence before writing
- Clear error messages indicate permission problems
- File operations are wrapped in try/except blocks

```python
# Verify directory exists but never create directories
directory = os.path.dirname(os.path.abspath(file_path))
if not os.path.exists(directory):
    return f"Error: Directory '{directory}' does not exist. File saving aborted. Please use an existing directory path."
```

### 5. Large File Handling [v3_2_0]

**Issue**: Very large files causing token overflow or slow processing.

**Solution**:
- Script caching mechanism for large code files
- Size checks before loading large files
- Targeted reading of specific sections

```python
# Check file size first
file_size = os.path.getsize(path)
if file_size > 1000000:  # 1MB file size limit for view
    return f"""Warning: File '{path}' is very large ({file_size/1000000:.2f}MB).
For large files, follow these steps:
1. First use read_file to examine a specific section
2. Make targeted edits with very specific search text
3. If you're adding significant content, consider creating a new file with just your additions
4. Include details in your task report about large files that couldn't be edited"""
```

## Best Practices

### 1. Configuration Design [v2_0_0]

#### Effective System Messages

- Be specific about the agent's role and expertise
- Include relevant background knowledge
- Specify the scope and constraints
- Define the expected tone and output style

Example:
```json
"U": "You are a professional research analyst with expertise in financial markets. Your task is to analyze financial data and produce clear, actionable insights. Focus on identifying trends, anomalies, and potential opportunities. Use a professional tone and provide well-structured analysis with clear sections and bullet points where appropriate."
```

#### Task Instructions

- Provide clear, specific instructions
- Break complex tasks into steps
- Specify input sources and expected output
- Include validation criteria

Example:
```json
"X": "Analyze the quarterly financial reports in the provided files. Identify revenue trends, profitability metrics, and any significant changes from previous quarters. Compare performance against industry benchmarks. Create a summary that includes: 1) Executive overview of financial health, 2) Key performance indicators with trends, 3) Areas of concern or opportunity, and 4) Recommendations for next quarter."
```

#### Resource Management

- Provide only necessary resources
- Use descriptive file names
- Organize resources logically
- Consider token usage when including large files

Example:
```json
"Y": [
  "financial-data/q3-2025-report.md",
  "financial-data/industry-benchmarks.json",
  "financial-data/previous-analysis.md"
]
```

### 2. Workflow Design [v3_0_0]

#### Phase Organization

- Keep phases focused on specific tasks
- Ensure each phase can complete within token limits
- Design clear transitions between phases
- Use consistent naming conventions

Sequential workflow example:
```json
"research": [
  {
    "PHASE_0": [{
      "U": "You are a research assistant...",
      "X": "Gather initial data...",
      "Y": ["initial-sources.md"],
      "Z": "Initial research outline",
      "O": ["research/outline.md"]
    }]
  },
  {
    "PHASE_1": [{
      "U": "You are a data analyst...",
      "X": "Analyze the research outline...",
      "Y": ["research/outline.md"],
      "Z": "Detailed analysis",
      "O": ["research/analysis.md"]
    }]
  }
]
```

#### Branching Workflows

- Create clear decision points
- Use consistent naming for branches
- Ensure all paths lead to valid outcomes
- Document decision criteria

Branching workflow example:
```json
"research": {
  "TASK_1": [{
    "U": "You are a research assistant...",
    "X": "Gather key facts and decide research direction...",
    "Y": ["sources.md"],
    "Z": "Research outline with direction decision",
    "O": ["research/outline.md", "research/decision.json"]
  }],
  "TASK_ECONOMIC": [{
    "U": "You are an economic analyst...",
    "X": "Research economic impacts...",
    "Y": ["research/outline.md", "research/decision.json"],
    "Z": "Economic analysis report",
    "O": ["research/economic.md"]
  }],
  "TASK_ENVIRONMENTAL": [{
    "U": "You are an environmental scientist...",
    "X": "Research environmental impacts...",
    "Y": ["research/outline.md", "research/decision.json"],
    "Z": "Environmental impact report",
    "O": ["research/environmental.md"]
  }]
}
```

### 3. Tool Usage [v3_0_0]

#### Efficient File Operations

- Use batch operations when possible
- Verify file existence before operations
- Handle large files appropriately
- Create backups for critical files

#### Decision Making

- Use the think tool for complex decisions
- Document reasoning in decisions
- Set appropriate confidence levels
- Consider all relevant factors

#### Context Management

- Monitor context window usage
- Use phase continuation strategically
- Create clear handoffs between phases
- Document context state in transitions

### 4. Output Validation [v3_2_0]

#### Token Counting

- Always count tokens for large outputs
- Stay within safe token limits
- Use revision phases for content that exceeds limits
- Document token counts in phase summaries

#### Content Verification

- Verify output against requirements
- Check for completeness and accuracy
- Ensure proper formatting
- Validate file paths and structure

#### Phase Summaries

Create comprehensive phase summaries:
```json
{
  "timestamp": "2025-05-21T14:30:45.123Z",
  "token_count": 4532,
  "report": "In this phase, I analyzed the financial data and identified three key trends...",
  "next_steps": "The next phase should focus on comparing these trends with industry benchmarks and creating visualizations.",
  "files_saved": [
    "output/financial-analysis.md",
    "output/key-metrics.json"
  ],
  "decision": {
    "options": ["economic focus", "market focus", "regulatory focus"],
    "choice": "economic focus",
    "reasoning": "The economic indicators show the most significant anomalies and potential opportunities..."
  }
}
```

## Agent Update Workflow [v3_0_0]

### Testing Updates

1. **Unit Testing**: Test individual components
2. **Integration Testing**: Test tool interactions
3. **Workflow Testing**: Test complete workflows
4. **Edge Case Testing**: Test error handling and recovery
5. **Performance Testing**: Test token usage and optimization

### Safe Deployment

1. Create a backup of the current agent
2. Make incremental changes
3. Test thoroughly after each change
4. Document all changes in version notes
5. Update the CHANGE_LOG.md
6. Verify compatibility with existing workflows

## Configuration Validation

### JSON Schema Validation [v3_2_0]

Validate configuration against the JSON schema:

```python
def validate_config(config):
    """Validate the configuration against the JSON schema."""
    schema = {
        "type": "object",
        "required": ["A", "F"],
        "properties": {
            "A": {"type": "string"},
            "F": {"type": "string"}
        },
        "additionalProperties": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "U": {"type": "string"},
                        "X": {"type": "string"},
                        "Y": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "array", "items": {"type": "string"}}
                            ]
                        },
                        "Z": {"type": "string"},
                        "O": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "array", "items": {"type": "string"}}
                            ]
                        }
                    },
                    "required": ["U", "X", "Z", "O"]
                }
            }
        }
    }
    
    try:
        validate(instance=config, schema=schema)
        return True, "Configuration is valid"
    except Exception as e:
        return False, f"Configuration validation error: {str(e)}"
```

### Path Verification

Verify all paths before execution:

```python
def verify_paths(config):
    """Verify that all paths in the configuration exist."""
    # Extract workflow key
    workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F'), None)
    if not workflow_key:
        return False, "No workflow key found"
        
    # Get use case directory
    use_case_dir = config.get('F', '')
    if not os.path.exists(use_case_dir):
        return False, f"Use case directory '{use_case_dir}' does not exist"
        
    # Check resource paths
    for phase in config[workflow_key]:
        for task_label, task_array in phase.items():
            for task in task_array:
                # Check resource paths
                resources = task.get('Y', [])
                if isinstance(resources, str):
                    resources = [resources]
                
                for resource in resources:
                    if resource != "N/A" and not os.path.exists(resource):
                        return False, f"Resource path '{resource}' does not exist"
                        
                # Check output directory paths
                outputs = task.get('O', [])
                if isinstance(outputs, str):
                    outputs = [outputs]
                    
                for output in outputs:
                    output_dir = os.path.dirname(output)
                    if not os.path.exists(output_dir):
                        return False, f"Output directory '{output_dir}' does not exist"
                        
    return True, "All paths verified"
```

## Performance Optimization

### Token Usage Tips [v3_2_0]

1. **Batched Operations**: Use batch operations rather than multiple individual operations
2. **Caching**: Enable prompt caching and use script caching
3. **Efficient Tools**: Use token-efficient-tools beta when available
4. **Context Management**: Be strategic about context windows and phase transitions
5. **Resource Selection**: Only include necessary resources
6. **Output Compression**: Create concise, focused outputs
7. **Tool Selection**: Use the most efficient tool for each task
8. **Phase Separation**: Break complex tasks into appropriate phases
9. **System Message Design**: Keep system messages focused and efficient
10. **Script Protection**: Avoid loading large scripts directly

### Token Optimization Patterns

```python
# Example of efficient token usage pattern
def get_file_summary(file_path):
    """Get a summary of a file without loading the entire content."""
    try:
        # Get file stats
        stats = os.stat(file_path)
        file_size = stats.st_size
        
        if file_size > 100000:  # Large file
            # Read just the beginning and end
            with open(file_path, 'r', encoding='utf-8') as f:
                beginning = f.read(5000)
                f.seek(max(0, file_size - 5000))
                end = f.read(5000)
                
            return f"""File: {os.path.basename(file_path)}
Size: {file_size/1024:.1f} KB
First 5000 bytes:
{beginning}

...

Last 5000 bytes:
{end}
"""
        else:
            # Read the entire file for small files
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"
```