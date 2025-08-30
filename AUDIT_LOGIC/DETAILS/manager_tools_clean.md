# manager_tools.py - What This File Does

**This file dynamically discovers and suggests tools based on what someone is trying to accomplish.**

When MAO analyzes a goal like "research market trends," this file figures out which tools (web search, analysis, visualization, etc.) would be helpful for that specific goal, without using predetermined categories.

## Key Functions

**Dynamic Tool Discovery**: Scans the file system to find all available tools by looking for their JSON configuration files and Python implementations.

**Goal-to-Tool Matching**: Uses semantic analysis to figure out which tools are relevant for a specific goal by comparing goal text with tool descriptions and capabilities.

**Tool Validation**: Checks that tools follow the proper 4-file structure (main logic, configuration, button generator, UI components) before making them available.

**MCP Tool Integration**: Discovers and integrates tools from MCP servers in addition to local tools, creating a unified tool ecosystem.

**Analytics Integration**: Tracks tool usage to understand which tools are most helpful, while keeping user data private.

## What Was Fixed

- **Improved text analysis**: The semantic matching now works better across different languages instead of just doing simple English word matching
- **Removed capability assumptions**: Stopped using English keywords like "image," "photo," "visual" to detect when vision tools are needed - now lets AI determine requirements dynamically
- **Better tool structure validation**: Made the file system requirements more flexible while maintaining the 4-file architecture integrity

## How It Integrates

When the core orchestrator creates workflows, it calls this file to find relevant tools. The tool suggestions get built into the workflow phases so agents have the right tools available when they need them.

This file provides the foundation for MAO's extensibility - new tools can be added just by following the 4-file pattern and dropping them into the tools directory. The system discovers them automatically without code changes.

The design trusts AI intelligence to determine what tools are needed instead of forcing tools into predetermined categories or use cases.