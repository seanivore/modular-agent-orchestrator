# memory_mcp.py - What This File Does

**This file manages workflow state persistence using Memory MCP - it's the system's memory.**

When workflows are running, this file keeps track of what's happening so that if something gets interrupted, MAO can pick up where it left off. It's like having a notebook that records every step of every workflow.

## Key Functions

**State Persistence**: Records workflow progress, phase completions, and current status so nothing gets lost if the system restarts.

**Session Recovery**: When MAO starts up after being interrupted, this file helps figure out what workflows were running and where they were in their process.

**Context Tracking**: Maintains the full history and context of each workflow so agents can understand what happened in previous phases.

**MCP Integration**: Connects to the Memory MCP server that provides persistent storage across sessions.

## What Was Fixed

- **Removed English parsing**: Used to look for hardcoded English words like "Status:", "Progress:", "Phase completed" when reading workflow observations - this broke for non-English workflows
- **Improved structured parsing**: Now uses more flexible pattern matching that works regardless of language by looking for key-value structures and timestamps
- **Language-neutral recovery**: Status detection now works with a broader range of terms instead of just English status words
- **Better fallback**: When the real MCP server isn't available, provides local storage that maintains the same functionality

## How It Integrates

This file is the single source of truth for workflow state. When the core orchestrator creates workflows, it records them here. When workflow phases complete, the status gets updated here. When someone wants to resume an interrupted workflow, this file provides all the context needed.

It's designed to work silently in the background - other parts of MAO read from and write to this memory system without having to worry about the details of how persistence works.