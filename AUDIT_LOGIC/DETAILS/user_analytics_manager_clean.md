# User Analytics Manager - Clean Documentation

## What This File Does

This file is what captures and stores real-time user behavior data while maintaining complete privacy and GDPR compliance. It tracks everything a user does in Mao without constraining AI behavior with predetermined patterns.

## Core Purpose in Mao App Context

**Privacy-First User Analytics**: Creates detailed behavior tracking tied to UserID for easy deletion while supporting true AI personalization without hardcoded assumptions about user patterns.

**Integration Points**: Receives analytics triggers from orchestrator files when users interact with workflows, tools, models, and sessions - then stores this data for AI-driven personalization.

## Key Functions and Their Purpose

### Session Tracking (`track_session`)
- **What it does**: Records when users start/end sessions and tracks workflow/tool activity counts
- **Why important**: Enables AI to understand user engagement patterns for personalized greeting and workflow recommendations
- **Real-time use**: Called from UI when user logs in/out or completes workflows

### Tool Usage Analytics (`track_tool_usage`) 
- **What it does**: Tracks which tools users actually use, success rates, and response times
- **Why important**: Allows AI to recommend tools based on actual usage patterns, not predetermined categories
- **Integration**: Automatically discovers new tools via ToolManager and adds them to tracking

### Workflow Tracking (`track_workflow`)
- **What it does**: Records workflow creation, completion, and success rates with user-defined tags
- **Why important**: Enables AI to suggest similar workflows or identify patterns in user project types
- **Avoids hardcoding**: Tags come from user input, not predetermined workflow categories

### Cost Tracking (`track_costs`)
- **What it does**: Records daily spending by model and provider for budget awareness
- **Why important**: Supports cost transparency and budget planning features in MAO_FLOW.md
- **Real-time updates**: Tracks costs as they occur during workflow execution

### Dynamic Tool Discovery (`scan_available_tools`)
- **What it does**: Integrates with ToolManager to automatically discover and track newly available tools
- **Why important**: Ensures analytics adapts to user's actual tool ecosystem instead of hardcoded tool lists
- **Auto-expansion**: Automatically adds new tools to analytics tracking when discovered

## How It Integrates with Other Files

### UserID-First Architecture
- **With username_manager.py**: Uses UserID system for all data storage and operations
- **Directory structure**: Stores data in `./configs/user/user-1234/analytics/` format
- **GDPR compliance**: All user data tied to UserID for easy deletion

### Orchestrator Integration Points
- **manager_tools.py**: Receives tool usage triggers and discovers available tools
- **workflow_manager.py**: Receives workflow start/completion triggers  
- **manager_models.py**: Receives cost information from model usage
- **real_time_metrics.py**: May provide live analytics data to UI

### AI Behavioral Integration
- **memory_mcp.py**: Analytics data can inform AI memory storage decisions
- **core.py**: Workflow preferences can be informed by usage analytics
- **No predetermined patterns**: Analytics capture actual user behavior for AI personalization

## What Was Removed/Simplified During Audit

### Critical Bug Fixes
- **Fixed syntax errors**: Division operators and directory paths that prevented execution
- **Fixed circular import**: Removed incorrect import of UsernameManager
- **UserID migration**: Changed from username-based to UserID-based operations

### Architecture Improvements  
- **Tool integration**: Connected scan_available_tools() to real ToolManager discovery
- **Standalone functions**: Added proper standalone functions for button imports
- **Error isolation**: Ensured analytics failures never break main Mao functionality

### Hardcoding Elimination
- **No examples removed**: File correctly avoided hardcoded suggestions from the start
- **Dynamic discovery**: Tool tracking adapts to actual available tools, not predetermined lists
- **User-driven tags**: Workflow analytics use user-provided tags, not system categories

## Important Behavioral Guidelines for AI

### Privacy Principles
- **Never persist data without UserID**: All analytics tied to UserID for GDPR deletion
- **Fail gracefully**: Analytics errors must never interrupt main Mao functionality
- **User control**: Users can delete all their analytics data at any time

### AI Personalization Guidelines  
- **Trust user patterns**: Use actual usage data, not predetermined user behavior assumptions
- **Adapt dynamically**: Analytics should discover and adapt to user's actual tool/workflow preferences
- **Cultural neutrality**: Avoid hardcoded workflow patterns that assume Western business practices

### Integration Behavior
- **Real-time only**: No mock data - all analytics from actual user interactions
- **Auto-discovery**: New tools/workflows automatically added to tracking without hardcoded lists
- **Performance conscious**: Analytics operations designed to be fast and non-blocking

## File Integration Map

```
User Interaction → Orchestrator Files → user_analytics_manager.py → UserID Directory Storage
                                    ↓
UI/Terminal ──→ track_session() ──→ ./configs/user/user-1234/analytics/session_metrics.json
manager_tools.py ──→ track_tool_usage() ──→ ./configs/user/user-1234/analytics/tool_usage.json  
workflow_manager.py ──→ track_workflow() ──→ ./configs/user/user-1234/analytics/workflow_metrics.json
manager_models.py ──→ track_costs() ──→ ./configs/user/user-1234/analytics/cost_tracking.json
```

This file now provides the foundation for AI-driven personalization in Mao while maintaining complete user privacy and avoiding any hardcoded assumptions about user behavior patterns.