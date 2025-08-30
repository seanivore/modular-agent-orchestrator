# core.py - What This File Does

**This is the main brain that turns natural language goals into intelligent workflows.**

When someone says "I want to research renewable energy trends and create a marketing strategy," this file figures out how to break that down into executable steps that different AI agents can work on.

## Key Functions

**Goal Analysis**: Takes whatever someone writes in any language and analyzes what they're trying to accomplish without making assumptions about English keywords or business categories.

**Dynamic Workflow Creation**: Instead of having predetermined templates like "research → analysis → creative," this file lets AI design the optimal workflow structure for each specific goal.

**Smart Model Selection**: Chooses the best AI model for each part of the workflow based on what capabilities are actually needed, not based on hardcoded assumptions.

**Intelligent Caching**: Remembers similar goals and workflow patterns so it doesn't have to recreate everything from scratch every time.

## What Was Fixed

- **Removed English task categories**: Used to have hardcoded multipliers for "research," "creative," "coding" etc. that only worked in English and forced Western business thinking patterns
- **Fixed multilingual naming**: Stopped filtering out "English stop words" when creating workflow names, so it works properly for goals written in any language  
- **Dynamic cost estimation**: Now estimates complexity based on actual task characteristics instead of predetermined English categories
- **Removed forced patterns**: Stopped forcing "planning + execution" phases for complex goals - now trusts AI to design optimal structure

## How It Integrates

This file gets called when someone wants to create a new workflow. It takes their natural language goal, analyzes it, figures out what tools and AI models are needed, creates a plan with multiple phases, and then coordinates the execution. All the other orchestrator files support this main brain.

The file follows the principle of trusting AI intelligence completely - it doesn't try to predetermine what workflows should look like or force them into English business categories.