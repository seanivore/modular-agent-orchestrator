# Core Architecture

This document details the core architecture of the Single-File Agent system, including configuration format, workflow execution, phase management, and context handling.

## Configuration Format [v1_0_0]

### JSON Structure

The SFA configuration uses a JSON structure with specific variables that control the agent's behavior:

```json
{
  "A": "command-name",              // Command name to create
  "F": "use-case/directory-path/",  // Use case directory
  "M": "google/gemini-2.5-pro-exp-03-25", // LLM model to use from Requesty (omit variable to use Claude directly)
  "workflow-key": [                 // Workflow identifier (can be any name)
    {
      "TASK_LABEL": [{              // Task label for this phase
        "U": "System message",      // Agent identity/behavior guidance
        "X": "Task instructions",   // Specific instructions for this phase
        "Y": ["resource1.md"],      // Resources for the agent to use
        "Z": "Output format",       // Description of expected output
        "O": ["output/path.md"]     // Output file paths
      }]
    }
  ]
}
```

### Variable Naming Convention [v1_0_0, enhanced v3_3_0]

The variables are intentionally terse to keep configuration files concise:

| Variable | Description        | Purpose                                |
| -------- | ------------------ | -------------------------------------- |
| **A**    | Command name       | Terminal command for the workflow      |
| **F**    | Use case directory | Root directory for workflow files      |
| **M**    | Requesty LLM model | Only include to use Requesty API Model |
| **U**    | System message     | Agent identity and behavior            |
| **X**    | Instructions       | Specific task instructions             |
| **Y**    | Resources          | References for the agent to use        |
| **Z**    | Output format      | Expected output format/description     |
| **O**    | Output paths       | Where to save output files             |

### Enhanced Format (Sequential Workflows) [v2_0_0, enhanced v3_3_0]

For simple sequential workflows, you can use a list structure:

```json
{
  "A": "research-report",
  "F": "use-case/doc-research/",
  "M": "google/gemini-2.5-pro-exp-03-25", // LLM model to use from Requesty (omit to use Claude directly)
  "research": [                     // Workflow key
    {
      "PHASE_0": [{                 // First phase
        "U": "...",
        "X": "...",
        "Y": ["..."],
        "Z": "...",
        "O": ["..."]
      }]
    },
    {
      "PHASE_1": [{                 // Second phase
        "U": "...",
        "X": "...",
        "Y": ["..."],
        "Z": "...",
        "O": ["..."]
      }]
    }
  ]
}
```

### Branching Workflows [v3_0_0, enhanced v3_3_0]

For workflows with decision-based branching, use a dictionary structure:

```json
{
  "A": "research-report",
  "F": "use-case/doc-research/",
  "M": "google/gemini-2.5-pro-exp-03-25", // LLM model to use from Requesty (omit to use Claude directly)
  "research": {                     // Workflow key as dictionary
    "TASK_1": [{                    // Starting task
      "U": "...",
      "X": "...",
      "Y": ["..."],
      "Z": "...",
      "O": ["...", "decision.json"] // Include decision output
    }],
    "DECISION_1": [{                // Decision task
      "U": "...",
      "X": "Decide which path to take",
      "Y": ["..."],
      "Z": "Decision with justification",
      "O": ["focus-decision.json"]
    }],
    "TASK_OPTION_A": [{             // Branch option A
      "U": "...",
      "X": "...",
      "Y": ["..."],
      "Z": "...",
      "O": ["..."]
    }],
    "TASK_OPTION_B": [{             // Branch option B
      "U": "...",
      "X": "...",
      "Y": ["..."],
      "Z": "...",
      "O": ["..."]
    }]
  }
}
```

The agent will use decision output in JSON format to determine which branch to follow.

### Path Variable Formats [v3_0_0]

You can use different formats for path variables:

```json
"Y": "single-resource.md"           // Single resource as string
"Y": ["resource1.md", "resource2.md"] // Multiple resources as array
"Y_PATH": "/absolute/path/to/resource.md" // Alternative format
"X_PATH": ["/path1", "/path2"]      // Multiple paths
```

## Workflow Execution [v1_0_0, enhanced v3_0_0]

### Main Execution Loop

The workflow execution follows this general pattern:

1. Load configuration from JSON file
2. Parse variables and validate structure
3. Set up API clients and tools
4. For each phase:
   a. Prepare system message and initial prompt
   b. Enter conversation loop with Claude
   c. Process tool calls and handle results
   d. Monitor for phase completion
   e. Generate phase summary if needed
   f. Save outputs and prepare for next phase
5. Execute next phase or complete workflow

### Script Execution [v1_0_0]

The agent is run using:

```bash
python sfa_v*_main.py --config-file path/to/config.json --phase 0
```

Or using the generated command:

```bash
your-command-name
```

### Token Usage Tracking [v3_2_0]

The system carefully tracks token usage:

```python
class TokenCounter:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        
    def update(self, input_tokens, output_tokens):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        # Calculate costs
        input_cost = input_tokens * 0.000003  # $3 per million tokens
        output_cost = output_tokens * 0.000015  # $15 per million tokens
        self.total_cost += input_cost + output_cost
```

## Phase Management [v3_0_0]

### Phase Transition Types

The workflow_adjustment tool allows for three types of phase transitions:

1. **END_PHASE**: Complete the current phase and move to the next phase with a fresh context window
2. **ADD_PHASE_AND_CONTINUE**: Reset loops but continue in the same context window
3. **ADD_PHASE_TO_WORKFLOW_AND_END**: Add a custom phase to the workflow and end the current phase

### Implementation

```python
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
```

### Phase Loop Control

The agent manages its loops with a reset function:

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

### Automatic Phase Completion [v3_2_0]

The agent can automatically complete a phase when output files are saved:

```python
# Check if all expected outputs have been saved
if set(output_path).issubset(saved_outputs):
    console.print(f"[green]All {len(output_path)} expected outputs saved.[/green]")
    console.print("[yellow]Now you must call workflow_adjustment to end this phase or continue to the next one.[/yellow]")
```

## Context Management [v3_0_0]

### Context Window Management

The agent carefully manages its context window to avoid hitting token limits:

1. **Token Counting**: Monitors input and output tokens
2. **Context Estimation**: Approximates context size
3. **Phase Reset Option**: Allows continuing in same context
4. **Phase Completion**: Ending phase and starting fresh

### Context Window Warning

When the context window gets large:

```python
if history_tokens > 50000:
    return f"""WARNING: Your context window is getting full (approx. {int(history_tokens)} tokens).
Continuing may lead to context limitations. Consider:
1. Using 'ADD_PHASE_TO_WORKFLOW_AND_END' instead to get a fresh context window
2. If you continue, focus only on the most critical remaining tasks
3. Prepare handoff information in case you reach token limits

Your loops have been reset to 0/{max_iterations}. Continue with caution."""
```

### Conversation History Management

The agent maintains the conversation history as a list of messages:

```python
conversation_history = [{
    "role": "user",
    "content": [{
        "type": "text",
        "text": initial_message,
        "cache_control": {"type": "ephemeral"}
    }]
}]
```

Tool results are added to the history:

```python
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
```

## Standardization Protocol [v2_0_0]

### Workflow Standardization

Workflows should follow these standardization practices:

1. **Consistent Task Labeling**:
   - `TASK_*`: Standard processing tasks
   - `DECISION_*`: Decision points
   - `REVIEW_*`: Review and finalization tasks

2. **Directory Structure**:
   - Use consistent paths for resources
   - Output to standardized locations
   - Maintain workflow state in appropriate directories

3. **Configuration Patterns**:
   - Use nested dictionaries for complex workflows
   - Use task arrays for simple linear workflows
   - Follow variable naming conventions strictly

4. **Phase Organization**:
   - Group related tasks
   - Provide clear transitions
   - Design for token efficiency

### JSON Configuration Example

```json
{
  "A": "example-workflow",
  "F": "use-case/example/",
  "M": "google/gemini-2.5-pro-exp-03-25", 
  "workflow": {
    "TASK_INITIAL": [{
      "U": "You are a research assistant with expertise in data analysis",
      "X": "Gather key information from the provided documents",
      "Y": ["documents/research.md", "documents/data.json"],
      "Z": "A summary of key findings with analysis",
      "O": ["output/summary.md", "output/decision.json"]
    }],
    "DECISION_FOCUS": [{
      "U": "You are a project manager with decision-making authority",
      "X": "Decide which aspect of the research to focus on for deeper analysis",
      "Y": ["output/summary.md"],
      "Z": "Decision with justification",
      "O": ["output/focus-decision.json"]
    }],
    "TASK_DETAILED": [{
      "U": "You are a specialized analyst with deep domain knowledge",
      "X": "Conduct in-depth analysis of the selected focus area",
      "Y": ["output/summary.md", "output/focus-decision.json"],
      "Z": "Detailed analysis report",
      "O": ["output/detailed-analysis.md"]
    }],
    "REVIEW_FINAL": [{
      "U": "You are a senior editor with expertise in the subject matter",
      "X": "Review, polish, and finalize the detailed analysis",
      "Y": ["output/detailed-analysis.md"],
      "Z": "Publication-ready analysis document",
      "O": ["final/report.md"]
    }]
  }
}
```

This standardized approach ensures consistency across workflows and makes it easier to maintain and extend the system.