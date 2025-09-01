# Manager Tools - Clean Implementation Guide

## What This File Does

The `manager_tools.py` file is the brain behind Mao's intelligent tool discovery system. Instead of forcing users into predetermined categories like "research tools" or "creative tools," this file dynamically matches user goals to available tools based on pure semantic analysis.

Think of it as Mao's way of saying "I understand what you're trying to accomplish" and then intelligently figuring out which tools can help, rather than asking you to pick from predefined buckets.

## Core Functions and Their Purposes

### Tool Discovery Engine (`suggest_tools_for_goal`)
This function takes a user's natural language goal and intelligently matches it to available tools by analyzing word overlap between the goal and each tool's capabilities. No hardcoded categories; just smart semantic matching.

### Cross-Compatible Button Generation (`create_executable_tool_button`) 
Creates executable code snippets that work across any AI provider or model. This eliminates SDK dependencies and ensures true modularity - when new AI models are released, they instantly work with all existing tools.

### Dynamic Tool Discovery (`discover_all_tools`)
Automatically finds tools from multiple sources: local MAO tools following the 4-file pattern, and external MCP (Model Context Protocol) servers. Everything is discovered at runtime, not hardcoded.

### Intelligent Cost Analysis (`interactive_tool_selection`)
Provides natural conversation data about tool suggestions, respecting user budget preferences without forcing artificial limitations.

## How It Integrates with MAO_FLOW.md Experience

This file enables the seamless tool selection experience described in MAO_FLOW.md where:

1. **User states their goal naturally** - no need to understand tool categories
2. **Mao intelligently suggests relevant tools** - based on semantic analysis, not predetermined patterns  
3. **Cross-provider compatibility works automatically** - through generated code snippets
4. **Tool discovery happens dynamically** - supporting the modular "plug-and-play" architecture

## Key Behavioral Guidelines for AI Usage

### Trust AI Intelligence Completely
The file implements MAO_FLOW.md's core principle: "AI is fully capable of making that judgement." It provides semantic matching algorithms but lets AI determine the best tools for each unique situation.

### Support Cultural Adaptability  
By avoiding hardcoded English workflow categories, this implementation supports users from different cultural backgrounds who may approach problems differently than Western "research → analysis → creative" patterns.

### Maintain True Modularity
Tools are validated by structure (4-file pattern) and capabilities, not by fitting into predetermined categories. This allows new types of tools and workflows to emerge naturally.

## What Was Removed/Simplified During Audit

**Nothing was removed** - this file was already implemented correctly according to MAO_FLOW.md specifications. It exemplifies proper implementation:

- No hardcoded workflow categories
- No predetermined tool suggestions  
- No cultural assumptions about problem-solving approaches
- No SDK dependencies through cross-compatible code generation

## Implementation Guidance for Similar Components

When creating new managers or discovery systems:

1. **Use semantic analysis** rather than hardcoded categories
2. **Generate executable code snippets** for cross-compatibility
3. **Discover capabilities dynamically** from configuration files
4. **Trust AI intelligence** without providing fallback suggestions
5. **Support cultural diversity** by avoiding English-specific patterns

This file demonstrates exactly how to build truly intelligent, adaptive systems that work globally while maintaining the technical excellence Mao requires.