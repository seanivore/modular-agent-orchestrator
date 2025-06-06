# Single-File Agent Specifications

This document defines what the Single-File Agent (SFA) system should do, including its architecture, capabilities, and expected behavior. It focuses on the "what" rather than the "how" of implementation.

## Core Architecture

### Architectural Overview [v1_0_0]

The Single-File Agent is designed as a modular, configurable system with these key components:

1. **Configuration Layer**: JSON-based configuration system defining variables for tasks
2. **Execution Engine**: Core runner script that processes configurations and manages execution
3. **Tool System**: Extensible set of tools that the agent can use to accomplish tasks
4. **Conversation Manager**: Interface with Claude API that handles messaging and context
5. **Workflow Controller**: System for managing phases and workflow transitions
6. **Output Processor**: Handles saving outputs and managing token limits

### Design Principles [v2_0_0]

The SFA follows these core design principles:

1. **Variable-Input Architecture**: The agent's behavior is defined through variables, not code changes
2. **Modularity**: Components are separated and can be individually extended or modified
3. **Single Responsibility**: Each component has a clear, focused purpose
4. **Configuration Over Code**: Behavior changes should be achievable through configuration
5. **Agentic Autonomy**: The agent has decision-making power within its defined scope
6. **Task Focus**: Each agent focuses on a specific, well-defined task
7. **Context Efficiency**: Careful management of context windows for optimal token usage
8. **Graceful Degradation**: Robust error handling and recovery mechanisms

## Configuration System

### Variable Structure [v1_0_0, enhanced v3_3_0]

The configuration uses variables with specific meanings:

| Variable | Description        | Role in System                    |
| -------- | ------------------ | --------------------------------- |
| **A**    | Command name       | Terminal command name             |
| **F**    | Use case directory | Base directory for workflow files |
| **M**    | LLM model          | LLM model to use from Requesty    |
| **U**    | System message     | Defines agent's role and behavior |
| **X**    | Instructions       | Specific task instructions        |
| **Y**    | Resources          | Input files or references         |
| **Z**    | Output format      | Expected output description       |
| **O**    | Output paths       | Where outputs should be saved     |

### Workflow Structure [v2_0_0, enhanced v3_0_0]

The SFA should support both sequential and branching workflows:

1. **Sequential Workflows**: Linear progression through predefined phases
2. **Branching Workflows**: Decision-based paths that can follow different routes
3. **Dynamic Workflows**: Agent-created phases based on task requirements

### Phase Management [v3_0_0]

The SFA should provide three phase transition options:

1. **END_PHASE**: Complete current phase and start next phase with fresh context
2. **ADD_PHASE_AND_CONTINUE**: Reset iteration counter but continue in same context
3. **ADD_PHASE_TO_WORKFLOW_AND_END**: Add custom phase and end current phase

## Tool System

### Tool Categories

The SFA should provide tools in these categories:

1. **File Operations**: Read, write, and manipulate files and directories
2. **Web Interactions**: Search, fetch, and process web content
3. **Decision Making**: Assist with reasoning and decision processes
4. **Workflow Control**: Manage phase transitions and workflow execution
5. **Media Processing**: Handle images and potentially other media
6. **Performance Management**: Monitor and optimize token usage and costs

### Required File Operation Tools [v1_0_0, enhanced v3_0_0]

1. **read_file**: Read content from a file
2. **read_multiple_files**: Read multiple files simultaneously
3. **list_directory**: List files in a directory
4. **search_files**: Find files matching patterns
5. **get_file_info**: Get metadata about a file
6. **save_output**: Save content to a file
7. **text_editor**: View, modify, and create text files
8. **move_file**: Move or rename a file
9. **delete_file**: Delete a file

### Required Decision Tools [v3_0_0]

1. **think**: Process complex information internally
2. **make_decision**: Choose between options with reasoning

### Required Workflow Tools [v3_0_0]

1. **complete_task**: Signal that a task is complete
2. **workflow_adjustment**: Adjust workflow execution

### Required Web Tools [v1_0_0, enhanced v3_0_0]

1. **web_search**: Search the web for information
2. **perplexity_search**: Advanced search using Perplexity AI

### Required Vision Tools [v3_0_0, enhanced v3_1_0]

1. **analyze_image**: Process and describe images
2. **edit_image**: Edit images with resize, crop, and text operations

### Required Performance Tools [v3_2_0]

1. **token_counter**: Count tokens in text or files
2. **task_report**: Create phase summaries with token statistics

## Conversation Management

### Claude Integration [v1_0_0]

The SFA should:

1. Integrate with Claude API for language model capabilities
2. Support the latest available Claude models
3. Properly handle tool calls and results
4. Maintain conversation history for context
5. Track token usage and costs

### Context Management [v3_0_0]

The system should:

1. Monitor context window size
2. Provide warnings when approaching limits
3. Support continuation within same context when appropriate
4. Create summaries to maintain continuity between phases
5. Optimize token usage through caching and efficient operations

## Performance Requirements

### Token Efficiency [v3_2_0]

The SFA should implement:

1. Prompt caching to reduce redundant token usage
2. Script caching for large code files
3. Token-efficient tools for reduced token consumption
4. Token counting before saving large outputs
5. Optimal context management for long tasks
6. Comprehensive token usage statistics

### Error Handling [v3_0_0]

The system should:

1. Implement robust error handling for all operations
2. Provide clear, actionable error messages
3. Create backups when modifying important files
4. Recover gracefully from API failures
5. Preserve state during error recovery

## Setup and Deployment

### Installation Process [v1_0_0]

The SFA should:

1. Provide simple installation via setup scripts
2. Create necessary command-line tools
3. Configure environment variables
4. Verify dependencies and requirements
5. Provide clear setup instructions

### Workflow Creation [v3_0_0]

The system should support:

1. Creating workflows from JSON configurations
2. Generating custom commands for workflows
3. Creating README documentation for workflows
4. Validating workflow configurations
5. Providing feedback on configuration issues

## Version Management

### Versioning System [v3_0_0]

The SFA should:

1. Follow semantic versioning (MAJOR.MINOR.PATCH)
2. Document changes in version-specific directories
3. Maintain backward compatibility when possible
4. Provide migration paths for breaking changes
5. Keep comprehensive change logs

### Version Documentation [v3_2_0]

Each version should document:

1. Added features and capabilities
2. Changed behavior or implementation
3. Fixed issues or bugs
4. Potential breaking changes
5. Technical notes on implementation

## Output Requirements

### Output Validation [v3_2_0]

The SFA should:

1. Validate token counts before saving
2. Enforce safe token limits
3. Provide revision opportunities for oversized content
4. Track token usage for outputs

### Output Formats [v3_0_0]

The system should support:

1. Text file outputs
2. Markdown formatting
3. JSON for structured data
4. Image editing and transformation
5. Directory structures for organized output

## Extension Capabilities

### Custom Tool Support [v3_0_0]

The SFA should:

1. Allow adding custom tools as Python modules
2. Automatically load tools from the tools directory
3. Provide a standard interface for tool definition
4. Document tool parameters and return values
5. Support error handling in custom tools

### Configuration Extensions [v3_0_0]

The system should support:

1. Extended variable formats (e.g., X_PATH, Y_PATH)
2. Custom workflow structures
3. Dynamic phase creation
4. Decision-based branching
5. Complex multi-stage workflows