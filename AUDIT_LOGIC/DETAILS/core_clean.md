# Core.py Clean Documentation

## What This File Does in Plain Language

This file is the main brain of Mao that takes a user's goal (in any language) and turns it into AI agents that can actually accomplish that goal. Think of it like a smart project manager that understands what you want to do and figures out how to make it happen using AI.

## Core Functions and Their Purposes

### `create_workflow_from_goal()`
**What it does**: Takes whatever the user wants to accomplish and creates a plan for AI agents to execute it.

**Why it's important**: This is where the magic happens - a user says "I want to create a marketing plan" and this function figures out exactly what AI agents need to do to make that happen.

**Key principle**: Trusts AI intelligence completely. No predetermined templates or categories. The AI designs the optimal approach based on the actual user goal, not hardcoded English business patterns.

### `execute_workflow()`
**What it does**: Actually runs the AI agents to accomplish the user's goal.

**Why it's important**: This is where the real work gets done. AI agents execute their tasks, coordinate with each other, and produce results.

**Key principle**: AI agents coordinate naturally. They handle handoffs between each other and adapt based on what actually happens, not predetermined scripts.

### `_ai_analyze_user_goal()`
**What it does**: Helps AI understand what the user really wants without imposing Western or English assumptions.

**Why it's important**: Users from different cultures approach problems differently. This ensures AI adapts to their actual thinking patterns rather than forcing them into predetermined categories.

### `_ai_design_workflow_phases()`
**What it does**: Lets AI create the optimal workflow structure based on the specific user goal.

**Key principle**: No hardcoded "research → analysis → creative" patterns. AI designs whatever workflow structure actually makes sense for this specific goal.

### `_ai_select_optimal_model()`
**What it does**: Chooses the best AI model for each task based on actual requirements.

**Why it's important**: Different AI models are better at different things. This picks the right tool for each job.

## How It Integrates with Other Files

### Integration with Memory MCP (`memory_mcp.py`)
The core orchestrator saves workflow state and progress through Memory MCP so users can resume interrupted work and AI agents have context from previous phases.

### Integration with Tool Manager (`manager_tools.py`)
Gets available tools that AI agents can use to accomplish goals, but lets AI decide which tools to use based on actual needs rather than predetermined suggestions.

### Integration with Model Manager (`manager_models.py`)
Coordinates with the model manager to select optimal AI models for each workflow phase based on actual task requirements.

### Integration with Button Manager (`manager_buttons.py`)
Creates the actual API calls that execute AI agent work, handling the technical details so AI can focus on accomplishing the user's goal.

## Important Behavioral Guidelines for AI Usage

### Trust AI Intelligence
- AI doesn't need hardcoded suggestions or examples
- Let AI design optimal workflows based on actual user needs
- Trust AI to understand goals in any language or cultural context

### Cultural Adaptation
- Don't impose Western linear thinking patterns
- Adapt to user's cultural approach to problem-solving
- Support different cultural methods of organizing work

### Dynamic Workflow Generation
- Design phases based on actual user goal, not templates
- Create workflows that make sense for this specific goal
- Avoid predetermined workflow patterns

### Natural Coordination
- AI agents coordinate execution naturally
- Handle handoffs between agents smoothly
- Adapt workflow execution based on intermediate results

### Error Handling and Recovery
- Use Memory MCP for state persistence and recovery
- Trust AI to handle errors and adapt as needed
- Maintain workflow continuity across sessions

## What Was Removed/Simplified During the Audit

### Eliminated Hardcoded Patterns
- **Before**: Predetermined "research → analysis → creative" workflow templates
- **After**: AI designs optimal workflow structure dynamically

### Removed Mock Code
- **Before**: Simulated execution with placeholder text
- **After**: Real execution framework that AI agents can use

### Simplified Goal Analysis
- **Before**: Complex categorization system with hardcoded English assumptions
- **After**: Simple analysis that lets AI understand goals in any cultural context

### Removed Over-Engineering
- **Before**: Complex phase hashing, predetermined complexity multipliers, extensive demo code
- **After**: Simple, clean logic focused on core orchestration functionality

### Eliminated Cultural Assumptions
- **Before**: English-centric workflow name generation and linguistic assumptions
- **After**: Language-neutral approach that works for any culture

### Added AI Behavioral Guidance
- **Before**: No guidance for AI decision-making
- **After**: Clear behavioral protocols for AI coordination without hardcoded examples

## The Result

The cleaned core.py file provides the simplest possible logic for AI workflow orchestration while trusting AI intelligence completely. It supports true multilingual functionality and cultural adaptation without imposing predetermined patterns. AI can now create any workflow structure that makes sense for the actual user goal, regardless of language or cultural background.

The file serves as a coordination hub that lets AI agents work together naturally while maintaining state persistence through Memory MCP integration. This creates a foundation for truly intelligent, adaptive workflow orchestration that scales globally.