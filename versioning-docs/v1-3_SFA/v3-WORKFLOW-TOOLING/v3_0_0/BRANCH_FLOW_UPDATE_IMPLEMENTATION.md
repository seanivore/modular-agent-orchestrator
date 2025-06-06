# SFA Token Counter and Task Reporting Implementation Guide

This guide explains how to implement the token counter and task reporting system in your Single-File Agents (SFA) workflow.

## Overview

We've created several components that work together:

1. **Token Counter Tool** - For accurately counting tokens in text, files, and directories
2. **Task Reporting Tool** - For generating comprehensive task reports with decision-making
3. **Branching Workflow Script** - For executing workflows with conditional branching

## File Structure

Place these files in the appropriate directories:

```
single-file-agents/
├── tools/
│   ├── token_counter.py         - Token counter core functions
│   └── task_reporting.py        - Task reporting tool
├── bin/
│   └── token                    - Standalone token counter command
└── branching_workflow.sh        - Workflow script with branching support
```

## Implementation Steps 

~~1. Install the standalone token counter for your personal use~~
~~2. Add the token counter and task reporting tools to your SFA tools directory~~
3. Update the SFA agent to load these tools
4. Add guidance in the system message about task reporting
5. Create a sample branching workflow JSON
6. Use the branching workflow script instead of the standard script

### 1. Install the Standalone Token Counter

This gives you a convenient command-line tool for counting tokens.

```bash
chmod +x install_standalone_token.sh
./install_standalone_token.sh
```

### 2. Add the Token Counter Tool to SFA

Copy the `token_counter.py` file to the `tools` directory:

```bash
mkdir -p /Users/seanivore/Development/single-file-agents/tools
cp token_counter.py /Users/seanivore/Development/single-file-agents/tools/
```

### 3. Add the Task Reporting Tool to SFA

Copy the `task_reporting.py` file to the `tools` directory:

```bash
cp task_reporting.py /Users/seanivore/Development/single-file-agents/tools/
```

### 4. Update the SFA Agent to Load the New Tools

Edit the `sfa_agent.py` file to load and register the new tools. Add these lines to the tool initialization section:

```python
# Load token counter tool
try:
    from token_counter_tool import get_tool_definition as get_token_tool
    token_tool = get_token_tool()
    if token_tool and "function" in token_tool:
        available_tools["token_counter"] = token_tool["function"]
        TOOLS.append(token_tool)
        console.print("[green]Token counter tool loaded successfully[/green]")
except ImportError:
    console.print("[yellow]Token counter tool not found, token counting features disabled[/yellow]")
except Exception as e:
    console.print(f"[yellow]Error loading token counter tool: {str(e)}[/yellow]")

# Load task reporting tool
try:
    from task_reporting import get_tool_definition as get_task_report_tool
    task_report_tool = get_task_report_tool()
    if task_report_tool and "function" in task_report_tool:
        available_tools["task_report"] = task_report_tool["function"]
        TOOLS.append(task_report_tool)
        console.print("[green]Task reporting tool loaded successfully[/green]")
except ImportError:
    console.print("[yellow]Task reporting tool not found, task reporting features disabled[/yellow]")
except Exception as e:
    console.print(f"[yellow]Error loading task reporting tool: {str(e)}[/yellow]")
```

### 5. Add a System Message for Task Reporting

Add this section to the system message generation in `sfa_agent.py`:

```python
task_reporting_guidance = """
At the end of each task generate a task report using the task_report tool:

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
- Signal task completion automatically when all outputs are saved
"""

# Add this to the system message if task report tool is available
if "task_report" in available_tools:
    system_message += task_reporting_guidance
```

### 6. Create a Sample Branching Workflow JSON

Create a JSON config file that follows the new structure with labeled tasks and decisions:

```json
{
  "workflow-name.sh": {
    "TASK_1": [
      {
        "S": ["sfa_agent.py"],
        "U": "You are a researcher analyzing a document.",
        "X": "At the 'X_PATH' please find document.md. Identify the key points.",
        "X_PATH": ["/path/to/document.md"],
        "Y": "After analysis, decide between three options: (1) Needs more research, (2) Ready for publishing, or (3) Requires revision.",
        "Y_PATH": [],
        "Z": "Analysis Report with Decision",
        "O": ["/path/to/output/analysis.md"]
      }
    ],
    "DECISION_1": [
      {
        "S": ["sfa_agent.py"],
        "U": "You are a research assistant gathering additional information.",
        "X": "Check the resource files for the initial analysis and add more research.",
        "X_PATH": ["/path/to/output/analysis.md"],
        "Y": "Expand the analysis with additional sources and examples.",
        "Y_PATH": [],
        "Z": "Enhanced Research Report",
        "O": ["/path/to/output/enhanced_analysis.md"]
      }
    ],
    "DECISION_2": [
      {
        "S": ["sfa_agent.py"],
        "U": "You are a copy editor preparing a document for publishing.",
        "X": "Check the resource files for the analysis that's ready for publishing.",
        "X_PATH": ["/path/to/output/analysis.md"],
        "Y": "Format the document according to publishing standards.",
        "Y_PATH": [],
        "Z": "Publication-Ready Document",
        "O": ["/path/to/output/publish_ready.md"]
      }
    ],
    "DECISION_3": [
      {
        "S": ["sfa_agent.py"],
        "U": "You are an editor revising a document.",
        "X": "Check the resource files for the analysis that needs revision.",
        "X_PATH": ["/path/to/output/analysis.md"],
        "Y": "Improve the clarity, structure, and flow of the document.",
        "Y_PATH": [],
        "Z": "Revised Document",
        "O": ["/path/to/output/revised_analysis.md"]
      }
    ],
    "REVIEW_TASK": [
      {
        "S": ["sfa_agent.py"],
        "U": "You are a quality assurance reviewer.",
        "X": "Review the final document from the previous phase.",
        "X_PATH": ["PREVIOUS_OUTPUT_FILE"],
        "Y": "Perform a final review for accuracy and completeness.",
        "Y_PATH": [],
        "Z": "Final Review Report",
        "O": ["/path/to/output/final_report.md"]
      }
    ]
  },
  "A": "workflow-name",
  "F": "/path/to/workflow/directory"
}
```

### 7. Install the Branching Workflow Script

```bash
cp branching_workflow.sh /Users/seanivore/Development/single-file-agents/
chmod +x /Users/seanivore/Development/single-file-agents/branching_workflow.sh
```

### 8. Use the Branching Workflow Script

```bash
cd /Users/seanivore/Development/single-file-agents/
./branching_workflow.sh /path/to/your/config.json
```

## How It Works

1. **Token Counting**:
   - The token counter uses a character-based approximation (3.5-4 chars per token)
   - It ensures documents stay under the 7,500 token limit
   - Claude must reduce content if it exceeds the limit

2. **Task Reporting**:
   - At the end of each task, Claude calls the task_report tool
   - The tool saves content to files ONLY if token counts are within limits
   - A structured JSON report is generated with the task summary, next steps, and any decisions
   - The report is used by the workflow script to determine the next task

3. **Branching Workflows**:
   - The workflow script reads decisions from task reports
   - It uses decision values to branch to the appropriate next task
   - Tasks are labeled (TASK_1, DECISION_1, etc.) for clear organization
   - If no matching task is found, it falls back to sequential execution

## Examples

### Example Task Report Output

```json
{
  "timestamp": "2025-04-19T14:30:45.123456",
  "token_count": 3251,
  "report": "Analyzed the document and identified 5 key points related to AI voice telemarketing strategies. The document provides a comprehensive overview of different approaches with examples.",
  "next_steps": "The document is ready for publishing with minor formatting adjustments.",
  "decision": {
    "options": ["Needs more research", "Ready for publishing", "Requires revision"],
    "choice": "Ready for publishing",
    "reasoning": "The document covers all necessary topics with sufficient detail and examples."
  },
  "files_saved": ["/path/to/output/analysis.md"]
}
```

### Example Task Report Tool Call

```python
task_report(
    content=document_content,
    file_paths=["/path/to/output/analysis.md"],
    report="Analyzed the document and identified 5 key points related to AI voice telemarketing strategies. The document provides a comprehensive overview of different approaches with examples.",
    next_steps="The document is ready for publishing with minor formatting adjustments.",
    decision={
        "options": ["Needs more research", "Ready for publishing", "Requires revision"],
        "choice": "Ready for publishing",
        "reasoning": "The document covers all necessary topics with sufficient detail and examples."
    }
)
```

## Troubleshooting

1. **Token counting not working**:
   - Ensure token_counter.py is in the tools directory
   - Check that the tool is being loaded in sfa_agent.py
   - Verify the anthropic package is installed

2. **Task reporting not working**:
   - Ensure task_reporting.py is in the tools directory
   - Check that it's being loaded in sfa_agent.py
   - Verify the required fields are included in the call

3. **Branching not working**:
   - Check that the JSON structure follows the new format with labeled tasks
   - Verify task reports are being generated with decision information
   - Ensure the branching_workflow.sh script is being used instead of the standard workflow script