# Single-File Agents (SFA)

A lightweight framework for creating specialized AI agents that perform tasks using a single file as the interaction surface.

## Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your API key in `.env` file (see `.example.env`)

Run the migration script if upgrading: `./setup-scripts/migrate-to-new-workflow.sh`

### Create A Workflow

```bash
# Create a new workflow
sfa your-config.json
```

1. Create a JSON configuration file for your use case (see examples in use-case directories)
2. Run the workflow setup: `sfa your-config.json`
3. This will:
   - Create a custom command script for your workflow
   - Add it to your PATH (via ~/bin)
   - Generate a README.md with instructions

### Command Options

```
sfa [options] <config_file.json>

Options:
  -e, --execute       Only execute the workflow without setup
  -r, --readme        Create an additional README_v2.md with detailed documentation
  -h, --help          Show this help message
```

### Running a Workflow

After setup, you can run your workflow using:
- The custom command created during setup: `your-command-name`
- Or directly: `sfa -e your-config.json`

## Agentic Basics

**Workflows** are pre-planned paths that leverage LLMs like Claude and provide them tools to complete tasks. This is a static system, similar to automations built with [Make](https://www.make.com/) or Zapier, with the primary difference being that code and AI facilitate the automated process. A workflow might not be agentic, but agentic systems have workflows.

**Agents** are workflows that are dynamic. The LLM is given autonomy to make decisions, directing their own processes, choosing tools, and maintaining control over how they accomplish tasks. The benefit is that you give power to the AI to do what it's designed to do. Using careful language, you can ensure high-quality results. Truly agentic systems have workflows that are created on the fly, rather than all possible decisions and paths laid out in advance.

The agent loop follows a pattern:

1. Take input from configuration variables
2. Process instructions via the LLM
3. Execute appropriate tools based on the LLM's decisions
4. Gather results and continue the conversation
5. Decide workflow branching if applicable
6. Repeat until the task is complete or max iterations reached

> *Paraphrased from Anthropic's [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)*

### LLMs As "Software"

Thanks to the nature of an LLM, you can think of the AI as 'software' and human language as 'programming'. The best results come from collaboration, not from telling the AI what to do or treating it like a tool.

> *Explore: [Should We Respect LLMs? A Cross-Lingual Study on the Influence of Prompt Politeness on LLM Performance](https://arxiv.org/abs/2402.14531)*

## What is a 'Single-File' Agent?

A Single-File Agent is a specialized AI system designed to:

1. Work with a single input and output file
2. Complete specific, targeted tasks
3. Follow pre-defined workflows
4. Work without direct user intervention

### The "Single-File" Origin

Original credit goes to '[IndyDevDan](https://www.youtube.com/@indydevdan)' for sharing the concept of [single-file agents](https://github.com/disler/single-file-agents), a term that refers to running a single Python file with embedded dependencies, made possible by [UV Astral](https://docs.astral.sh/uv/).

The SFA python script always starts with those dependencies at the top:

```python
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
# ... more imports
```

## Variable-Input Architecture

We've taken the concept and pushed it to become an even more powerful and flexible tool for automation. Our SFA build is extra lightweight; *designed to be non-purpose-specific*, this code is intentionally generic with *no discernable task-related details* in the code. Our commitment to absolute modularity is what makes it so powerful.

The variables in the config file are essentially a broken-down prompt, structured to give Claude clear guidance without limiting its autonomy. You can message a chat AI your ideas, and they'll generate the JSON for you.

### Configuration Variables Explained

SFA uses abbreviations in its configuration to keep it concise:

| Variable | Description        | Usage in Code                      |
| -------- | ------------------ | ---------------------------------- |
| **A**    | Command name       | Used to create terminal command    |
| **F**    | Use case directory | Directory to store workflow files  |
| **M**    | LLM model          | LLM model to use from Requesty     |
| **U**    | System message     | Guides the agent's behavior        |
| **X**    | Instructions       | Main task instructions             |
| **Y**    | Resources          | File paths or URLs for reference   |
| **Z**    | Output format      | Expected output format/description |
| **O**    | Output paths       | Where to save output files         |

Inside each phase/task, these variables define what the agent will do and how it will interact with resources and outputs.

### Variable-Based Design Principles

1. **Separation of structure and content**: The agent's code defines its capabilities, while variables define its specific task
2. **Consistent variable meanings**: Each variable always represents the same category of information
3. **Minimalist approach**: Variables should be simple; let Claude be Claude, make choices, have control

## Project Structure

```plaintext
single-file-agents/
├── README.md                  # This document (project overview and quick start)
├── SPECIFICATIONS.md          # What the system should do (high-level design)
├── TECHNICAL_DOCS.md          # Technical documentation table of contents
├── sfa_main.py                # Core agent implementation
├── setup-scripts/             # Setup and workflow scripts
│   ├── install-sfa-commands.sh
│   ├── migrate-to-new-workflow.sh
│   └── sfa_workflow.sh
├── technical-docs/            # Detailed implementation documentation
├── tools/                     # Agent tools
│   ├── fonts/                 # Font files for image editing
│   ├── image_editing.py       # Image manipulation tool
│   ├── task_reporting.py      # Phase reporting tool
│   └── token_counter.py       # Token counting utilities
├── use-case/                  # Example workflows
└── versioning/                # Version history and documentation
    ├── CHANGE_LOG.md          # Comprehensive version history
    ├── v1-ORIGINAL-SFA/       # Initial version
    ├── v2-DECISION-BRANCHING/ # Decision branching feature
    └── v3-WORKFLOW-TOOLING/   # Workflow tooling enhancements
        ├── v3_0_0/
        ├── v3_1_0/
        └── v3_2_0/
```

## Core Components

### 1. Configuration File

The JSON configuration file defines the workflow using the variable architecture:

```json
{
  "A": "research-report",                 // Command name
  "F": "use-case/doc-research-simple/",   // Use case directory
  "M": "google/gemini-2.5-pro-exp-03-25", // LLM model to use from Requesty (omit to use Claude directly)
  "research": {                           // Labeled tasks with branching
    "TASK_1": [{
      "U": "You are a professional research assistant with expertise in agriculture",
      "X": "Gather key facts and figures about sustainable farming practices",
      "Y": ["https://example.com/sustainable-farming"],
      "Z": "A research outline with key points",
      "O": ["research/outline.md", "research/decision.json"]
    }],
    "DECISION_1": [{
      "U": "You are a research project manager with subject matter expertise",
      "X": "Based on initial research, decide which aspect to focus on",
      "Y": ["research/outline.md"],
      "Z": "Decision with justification",
      "O": ["research/focus-decision.json"]
    }]
  }
}
```

### 2. Main Runner Script

The `sfa_[version]_main.py` file is the core engine that:
- Loads and interprets the configuration
- Manages conversation with Claude
- Provides tools for the agent to use
- Handles workflow branching and phase management
- Tracks token usage and performance

### 3. Available Tools

Each agent has access to a suite of tools:

#### Basic Tools
- **web_search**: Search the web for information
- **text_editor**: View, modify, and create text files
- **save_output**: Save content to a file with token counting
- **token_counter**: Count tokens in text
- **workflow_adjustment**: Control the workflow phases

#### File Operations
- **read_file**: Read content from the filesystem
- **read_multiple_files**: Read multiple files simultaneously
- **list_directory**: List files in a directory
- **search_files**: Find files matching patterns
- **get_file_info**: Get detailed metadata about files
- **move_file**: Move or rename a file
- **delete_file**: Delete a file

#### Advanced Capabilities
- **analyze_image**: Process and analyze images
- **edit_image**: Edit images, crop, convert, resize, and adding text 
- **think**: Allow Claude to pause and process complex information
- **make_decision**: Choose between options with reasoning
- **perplexity_search**: Advanced search via Perplexity API

## Workflow Execution

### General Workflow Pattern

```plaintext
PHASE RUNNING (CLAUDE INSTANCE ACTIVE)
           |
           ↓
+---------------------+     "workflow_adjustment"
| End phase triggered | <-- "save_output"
+---------------------+     "complete_task"
           |
           ↓
  +----------------------+
  | Workflow adjustment? |   <-- Primary router
  +----------------------+
     /         |         \
  [NO]       [YES]       [YES]
   /           |           \
  ↓            ↓            ↓
[END PHASE]    |            |
  |            |            |
  |   +-------------+       |
  |   | ADD PHASE   |       |
  |   | TO WORKFLOW |       |
  |   |  AND END    |       |
  |   +-------------+       |
  |        ↓                |
  |        |       +--------------+
  |        |       | ADD PHASE TO |
  |        |       | WORKFLOW AND |
  |        |       | RESET LOOPS  | <-- Keep
  |        |       +--------------+     working
  |        ↓                |
  ↓        |                ↓
+---------------+           |
| < 7k tokens?  |           |
+---------------+           |
   /       \                |
  /         \               |
[YES]       [NO]------------+
  |                         |
  |                         |
  |                         |
  |                         |
  |                         |
+---------------------+     |
| Write Phase Summary |     |
+---------------------+     |
         |                  |
         |                  |
         ↓                  |
+--------------------+      |
| SAVE PHASE SUMMARY |      |
| SAVE OTHER OUTPUTS |      |
+--------------------+      |
         |                  ↓
         ↓                  |
         |        +---------------------+
         |        | START NEW PHASE     |
         |        | SAME CONTEXT WINDOW |
         |        +---------------------+
         |                  |
         |                  |
         ↓                  ↓
   [PHASE COMPLETE]     [NEXT PHASE]
         |                  |
         ↓                  ↓
 [WORKFLOW CONTINUES     [WORKFLOW
  OR COMPLETES]          CONTINUES]
```

### Phase Management

Agents can manage workflow phases using the workflow_adjustment tool with three options:

- **END_PHASE**: End the current phase normally
- **ADD_PHASE_AND_CONTINUE**: Continue in the same context window
- **ADD_PHASE_TO_WORKFLOW_AND_END**: Add a new phase to the workflow and end the current phase

This gives agents flexibility to handle complex tasks and manage their context window usage.

## Performance Features

### Token Management

The agent includes sophisticated token management:
- Automatic token counting for outputs
- Token limit enforcement for safety
- Token usage statistics and cost estimation
- Support for Claude's prompt caching for efficiency

### Context Window Management

The agent intelligently manages its context window:
- Phase summary creation for long tasks
- Context continuation options for complex work
- Automatic token overflow detection
- Phase reset capabilities for revisions

## Best Practices

1. **Clear Task Definition**: Each phase should have a specific purpose
2. **Appropriate Resources**: Provide necessary reference files
3. **Realistic Scope**: Each phase should be completable within one context window
4. **Proper Documentation**: Include a README to explain the workflow
5. **Error Handling**: Consider potential issues in your workflow design

## Example Use-Cases

SFAs can be applied to a wide range of tasks, including:

1. **Content Creation & Marketing**
   - Research and write marketing copy
   - Create social media campaigns
   - Draft email sequences
   - Generate targeted content

2. **Documentation & Analysis**
   - Update technical documentation
   - Research and summarize topics
   - Create reports and presentations
   - Analyze and organize information

3. **Job Application Materials**
   - Create targeted resumes
   - Write compelling cover letters
   - Research companies
   - Customize applications 

## License

MIT License