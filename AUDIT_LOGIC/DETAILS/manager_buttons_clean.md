# Manager Buttons Clean Documentation

## What This File Does

The `manager_buttons.py` file creates executable code snippets that eliminate SDK dependencies and enable true cross-compatibility across different AI model providers. This file implements the "human button" concept specified in MAO_FLOW.md.

## Core Purpose

Instead of forcing agents or users to understand different SDK patterns, this manager generates working Python code that can be executed in any environment to call AI models. Each generated snippet is a self-contained button that handles:

- API client initialization
- Request formatting
- Response parsing  
- Cost calculation
- Error handling

## How It Works

### ButtonManager Class

The main class that coordinates all snippet generation operations.

**Key Methods:**

- `create_api_call_snippet()` - Generates executable code for any model/provider combination
- `create_workflow_snippet()` - Creates code for multi-phase workflow execution
- `create_tool_execution_snippet()` - Provides working code patterns for tool operations
- `get_execution_summary()` - Returns model capability and cost information

### Provider Support

The manager dynamically supports different API providers:

**Anthropic Provider:**
- Handles Claude models with proper message formatting
- Includes caching support for Claude 4
- Provides accurate token counting and cost calculation

**OpenAI Provider:**  
- Supports OpenAI-compatible APIs (OpenAI, Requesty, LM Studio)
- Adapts to different base URLs and authentication patterns
- Converts Anthropic tool format to OpenAI tool format

**Gemini Provider:**
- Uses Google's GenerativeAI SDK patterns
- Handles Gemini-specific configuration requirements
- Estimates costs with token approximation

### Cross-Compatibility Architecture

The manager discovers available models and providers from JSON configuration files rather than hardcoding support. When a new model is added to the system:

1. JSON configuration files are updated with model/provider information
2. ButtonManager automatically detects the new provider type
3. Appropriate snippet generation method is selected
4. Working code is generated immediately

This eliminates SDK version conflicts, dependency management, and platform-specific issues.

## What Code Snippets Include

Every generated snippet contains:

**Essential Components:**
- Proper API client initialization with environment variable handling
- Request parameter setup with all required fields
- Error handling with structured result format
- Cost calculation using model-specific pricing
- Token usage tracking for budget management

**Output Format:**
- Human-readable execution status
- Structured JSON result for agent consumption
- Cost transparency with input/output token counts
- Tool call extraction when applicable

## Agent Integration

Agents receive these snippets as working code they can execute directly. The snippets:

- Require no additional dependencies beyond basic client libraries
- Work in any Python environment (local, cloud, containers)  
- Provide consistent result format across all providers
- Include cost tracking for budget-conscious usage

## Workflow Orchestration

The workflow snippet generator creates code that:

- Executes multiple model calls in sequence
- Accumulates results and costs across phases  
- Provides real-time execution status
- Returns comprehensive workflow results

This enables complex multi-model workflows without requiring agents to understand orchestration logic.

## Tool Execution Patterns

Tool execution snippets provide working code templates for common operations:

- Web search integration patterns
- File operation examples
- Structured error handling
- Result formatting for agent consumption

These serve as reference implementations that agents can adapt for specific use cases.

## Cost Management

Every snippet includes transparent cost calculation:

- Model-specific pricing from configuration files
- Real-time token counting where possible  
- Total cost accumulation across operations
- Budget-friendly execution patterns

This enables cost-conscious AI usage without requiring agents to understand pricing models.

## Error Handling

All generated snippets include comprehensive error handling:

- Network failure recovery
- API error interpretation
- Structured error responses
- Graceful degradation patterns

This ensures reliable operation even when underlying services experience issues.

## Why This Approach Works

**SDK Independence:** No version conflicts or dependency hell
**Universal Compatibility:** Works across different deployment environments
**Cost Transparency:** Real-time budget tracking built into every operation
**Agent Simplicity:** Agents get working code without complexity
**Dynamic Discovery:** New models available immediately through configuration
**Error Resilience:** Built-in error handling reduces operational complexity

This design perfectly implements the MAO principle of trusting AI intelligence while providing necessary tools without logistical burden.