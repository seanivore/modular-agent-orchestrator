# workflow_manager.py - What This File Does

**This file handles workflow ID generation, discovery, and tracking.**

When workflows get created, this file gives them unique IDs, helps find existing workflows, and tracks their progress. Think of it like a filing system for all the workflows MAO creates.

## Key Functions

**Unique ID Generation**: Creates mathematically unique identifiers for each workflow so they never conflict with each other.

**Workflow Discovery**: Scans the file system to find all existing workflows and provides search functionality to locate specific ones.

**Status Tracking**: Monitors whether workflows are active, completed, failed, or in some other state.

**Analytics Integration**: Tracks workflow usage patterns for understanding how MAO is being used, while keeping user data private and deletable.

## What Was Fixed

- **Removed English keyword tagging**: Used to automatically tag workflows as "research," "analysis," or "parallel" based on English keywords in their documentation - this broke multilingual support and forced Western business categories
- **Clean tag extraction**: Now only extracts explicit tags that users add themselves (like #hashtags or "Tags: something") instead of assuming categories
- **Improved search**: Made workflow discovery work better across different languages by not depending on exact English term matching

## How It Integrates

Other parts of MAO call this file when they need to create new workflows, find existing ones, or track progress. The core orchestrator uses it to generate IDs for new workflows. The analytics system uses it to understand usage patterns.

This file provides the organizational backbone that lets MAO keep track of potentially thousands of workflows without getting confused about which is which. It works in any language because it doesn't make assumptions about how people describe their work.