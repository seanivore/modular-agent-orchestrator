# MAO Memory & Analytics System - Claude Code Implementation SPEC
> Bundled implementation: Memory System + User Analytics + System Analytics

## Implementation Foundation Reference

**CRITICAL**: This SPEC builds on comprehensive trigger point documentation:
- **📊 Complete Analytics Documentation**: `MAO_ANALYTICS_COMPREHENSIVE_DOCUMENTATION.md`
- **🔧 Exact Trigger Points**: Every metric specifies WHERE/WHEN/HOW data is collected
- **🔒 Privacy Compliance**: User vs system data separation with deletion workflows
- **⚙️ Integration Architecture**: How analytics connect to existing MAO managers

## Why Bundled Together

**Shared Touchpoints**: Memory and Analytics systems both interact with:
- `settings_manager.py` - User configuration management
- `username_manager.py` - User identification and directory structure  
- User directory organization in `./configs/user/[username]/`
- Similar JSON storage patterns and discovery methods

**Implementation Efficiency**: Single implementation cycle prevents multiple migrations and ensures all user directory changes happen at once. Claude Code is welcome to adjust the bundling approach as needed.

## High-Level Objective

Add sophisticated memory system and privacy-compliant analytics infrastructure to MAO's solid foundation. Implement user preference storage, contextual suggestions, and **basic analytics metrics** while maintaining MAO's modular discovery philosophy.

## Mid-Level Objectives

- Create complete memory system with CLI commands and contextual suggestions  
- Build privacy-first analytics infrastructure (user vs system separation)
- Establish **basic metrics foundation** for future marketing-driven analytics expansion
- Maintain MAO's modular discovery patterns for all new systems
- **Focus on core metrics** - session tracking, tool usage, workflow basics, cost accumulation

## Implementation Notes

- **Analytics Strategy**: Start with basic metrics, comprehensive trigger documentation enables easy expansion
- Follow established MAO patterns (CacheManager, @handle_errors, estimate_cost)
- Use collected JSON files for analytics (not individual files per metric)
- Maintain privacy-first architecture with clear user vs system data separation
- **Modular Analytics**: Foundation supports dynamic metric addition via discovery patterns
- Bundle memory + analytics implementation to prevent multiple migrations

## Context

### Beginning Context
- Current user structure: ./configs/user/user_seanivore.json (flat)
- CLI command infrastructure established
- Memory MCP integrated as state persistence layer  
- Settings manager handles user configuration updates
- Username manager discovers and manages users
- **Analytics Documentation**: Complete trigger specifications available for reference

### Ending Context  
- New user structure: ./configs/user/seanivore/user_seanivore.json + subdirectories
- Functional memory system with /memory CLI commands
- Privacy-compliant analytics infrastructure (user + system)
- **Basic metrics operational**: Session, tool usage, workflow, cost tracking
- All existing managers updated for new directory structure
- Foundation for advanced user preference and analytics features

## Low-Level Tasks

### Phase 1: User Directory Enhancement

#### Task 1.1: Create New User Directory Structure
```
CREATE: ./configs/user/seanivore/ directory
MOVE: ./configs/user/user_seanivore.json → ./configs/user/seanivore/user_seanivore.json
CREATE: ./configs/user/seanivore/memories/ subdirectory
CREATE: ./configs/user/seanivore/analytics/ subdirectory
```

#### Task 1.2: Update Settings Manager for New Structure
```
UPDATE: ./orchestrator/settings_manager.py
- Update user file discovery to use nested directory pattern
- Modify user config read/write methods for new paths
- Maintain backward compatibility during transition
- Update delta-only storage for new directory structure
```

#### Task 1.3: Update Username Manager for New Structure  
```
UPDATE: ./orchestrator/username_manager.py
- Update user discovery to scan ./configs/user/[username]/ directories
- Modify user creation/deletion for nested structure
- Update user listing and validation methods
- Ensure UserID generation works with new paths
```

### Phase 2: Memory System Implementation

#### Task 2.1: Create Memory CLI Command Files
```
CREATE: ./configs/cli/memory/memory.py
- Function: execute_memory(params) with save/list/delete operations
- Integration: Memory MCP for persistence, username_manager for user_id lookup
- Operations: save_memory(), list_memories(), delete_memory(), suggest_contextual()
- Standard patterns: CacheManager, @handle_errors, estimate_cost()
```

```
CREATE: ./configs/cli/memory/ui_memory.py  
- Function: display_memory_result(result, verbose=False)
- Display patterns: Memory list with IDs, save confirmations, deletion summaries
- Rich formatting: Panel displays, color coding for memory types
- Error handling: display_error() function with Panel formatting
```

```  
CREATE: ./configs/cli/memory/memory.json
- Schema: Standard CLI command config with 'name' field
- Commands: Both /memory slash command and --memory flag support
- Cost estimate: 0.002 for Memory MCP operations
- Integration: CLI manager routing, user manager touchpoints
```

#### Task 2.2: Create Memory JSON Schema and Storage
```
CREATE: ./configs/user/seanivore/memories/personal_preferences.json
Schema: {
  "memories": [
    {
      "id": "mem_001",
      "content": "Always use descriptive variable names", 
      "timestamp": "2025-01-15T10:30:00Z",
      "workflow_id": "wf_comp_analysis_001",
      "memory_type": "coding_preference",
      "tags": ["coding", "variables", "best_practices"],
      "context": "general"
    }
  ],
  "metadata": {
    "user_id": "user-1642",
    "total_memories": 1,
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```

```
CREATE: ./configs/user/seanivore/memories/project_context.json
Schema: Similar structure for project-specific memories and team guidelines
```

#### Task 2.3: Create User Memory Manager Service  
```
CREATE: ./orchestrator/user_memory_manager.py
- Class: UserMemoryManager with standard MAO patterns
- Functions: store_memory(), retrieve_memories(), delete_memory(), suggest_contextual()
- Integration: Memory MCP for persistence, username_manager for user_id lookup
- Caching: User-specific cache keys with 5-minute duration
- Standard patterns: CacheManager, @handle_errors, estimate_cost()
```

### Phase 3: Basic Analytics Infrastructure

#### Task 3.1: Create User Analytics System
```
CREATE: ./configs/user/seanivore/analytics/session_metrics.json
Schema: {
  "sessions": [
    {
      "session_id": "sess_001",
      "start_time": "2025-01-15T09:00:00Z",
      "end_time": "2025-01-15T11:30:00Z", 
      "duration_minutes": 150,
      "workflow_count": 3,
      "tool_activations": 12
    }
  ],
  "aggregates": {
    "total_sessions": 1,
    "average_duration": 150,
    "total_time_minutes": 150
  }
}

TRIGGER POINTS (see comprehensive documentation):
- Session start: ui_terminal.py app initialization
- Session end: ui_terminal.py cleanup/shutdown
- Workflow count: workflow_manager.py completion events
- Tool activations: manager_tools.py execution completions
```

```
CREATE: ./configs/user/seanivore/analytics/tool_usage.json
Schema: {
  "tool_usage": {
    "brave_search": {
      "total_uses": 15,
      "success_rate": 0.95,
      "avg_response_time": 1.2,
      "last_used": "2025-01-15T10:30:00Z"
    },
    "dalle_generate": {
      "total_uses": 8,
      "success_rate": 0.88,
      "avg_response_time": 8.5,
      "last_used": "2025-01-15T09:15:00Z"
    }
    // NOTE: New tools automatically added via discovery
  },
  "metadata": {
    "total_tools_tracked": 2,
    "discovery_enabled": true,
    "last_discovery_scan": "2025-01-15T10:30:00Z"
  }
}

TRIGGER POINTS (see comprehensive documentation):
- Tool usage: manager_tools.py execute_tool() start/completion
- Success tracking: manager_tools.py success/failure handlers
- Discovery: manager_tools.py discover_all_tools() scanning
```

```
CREATE: ./configs/user/seanivore/analytics/workflow_metrics.json  
Schema: {
  "workflows": [
    {
      "workflow_id": "wf_001",
      "workflow_command": "competitor_analysis",
      "start_time": "2025-01-15T09:00:00Z",
      "completion_time": "2025-01-15T10:30:00Z",
      "success": true,
      "workflow_tags": ["parallel", "research", "analysis"]
    }
  ],
  "tag_analytics": {
    "parallel": {"usage_count": 5, "avg_duration": 45},
    "research": {"usage_count": 8, "success_rate": 0.92}
  }
}

TRIGGER POINTS (see comprehensive documentation):
- Workflow start: workflow_manager.py setup script execution
- Workflow completion: workflow_manager.py finalization
- Tag extraction: README.md scanning during setup
```

```
CREATE: ./configs/user/seanivore/analytics/cost_tracking.json
Schema: {
  "daily_costs": [
    {
      "date": "2025-01-15",
      "total_spend": 2.45,
      "model_breakdown": {
        "claude-sonnet-4": 1.80,
        "gpt-4": 0.65
      },
      "session_count": 3
    }
  ],
  "totals": {
    "monthly_spend": 45.67,
    "avg_daily": 1.52
  }
}

TRIGGER POINTS (see comprehensive documentation):
- API costs: Model managers during API calls
- Daily rollup: End-of-day aggregation process
- Model tracking: Provider-specific cost accumulation
```

#### Task 3.2: Create Basic System Analytics
```
CREATE: ./configs/system/analytics/aggregate_usage.json
Schema: Anonymous usage patterns across all users
- Popular workflow types (by tags, no user identification)
- Tool usage frequency (anonymized)
- Success rate patterns (anonymized)

PRIVACY: All user identifiers removed before aggregation
```

```
CREATE: ./configs/system/analytics/tool_performance.json
Schema: Tool efficiency metrics (anonymized)
- Average response times per tool
- Success rates across all users
- Performance trends over time

PRIVACY: No user identification, statistical aggregation only
```

#### Task 3.3: Create Analytics Manager Services
```
CREATE: ./orchestrator/user_analytics_manager.py
- Functions: track_session(), track_tool_usage(), track_workflow(), track_costs()
- BASIC METRICS FOCUS: Session, tool, workflow, cost fundamentals
- Dynamic discovery: scan_available_tools(), auto_add_component()
- Privacy: All data tied to user_id for deletion compliance
- Standard patterns: CacheManager, @handle_errors, estimate_cost()
- Error handling: Analytics failures never break main functionality
```

```
CREATE: ./orchestrator/system_analytics_manager.py
- Functions: aggregate_usage(), track_performance(), track_health()
- BASIC METRICS FOCUS: Core performance and usage patterns
- Privacy: NO user identification, secondary anonymization
- Standard patterns: CacheManager, @handle_errors, estimate_cost()
```

### Phase 4: Integration and Testing

#### Task 4.1: Update CLI Manager Integration
```
UPDATE: ./orchestrator/cli_manager.py
- Add memory command to dynamic discovery
- Route /memory and --memory to user_memory_manager
- Handle memory command caching (5-minute duration)  
- Update _get_command_help() to include memory operations
- BASIC analytics hooks: Track command usage (following trigger documentation)
```

#### Task 4.2: Update Tool Manager Integration
```
UPDATE: ./orchestrator/manager_tools.py
- Add analytics trigger points (see comprehensive documentation)
- Track tool_start(), tool_completion(), tool_failure()
- Implement dynamic tool discovery for analytics
- Error handling: Analytics failures don't break tool execution
```

#### Task 4.3: Update Workflow Manager Integration
```
UPDATE: ./orchestrator/workflow_manager.py
- Add analytics trigger points (see comprehensive documentation)  
- Track workflow_start(), workflow_completion(), tag extraction
- Implement README.md tag scanning during setup
- Error handling: Analytics failures don't break workflows
```

#### Task 4.4: Integration Testing
```
TEST: User directory restructure
- Verify: Settings manager reads/writes to new locations
- Verify: Username manager discovers users correctly
- Verify: Existing user data accessible after migration
```

```
TEST: Memory system functionality
- TEST: /memory "Always use descriptive variable names"
- Verify: Memory saved to user directory and Memory MCP
- TEST: /memory --list
- Verify: All user memories displayed with proper formatting
- TEST: /memory --delete [ID]
- Verify: Memory removed from all storage locations
```

```
TEST: Basic Analytics functionality  
- Verify: Session metrics track correctly
- Verify: Tool usage analytics capture basic metrics
- Verify: Workflow metrics include tag extraction
- Verify: Cost tracking accumulates properly
- Verify: Privacy compliance - user data deletable, system data anonymous
```

## Integration Touchpoints

**CRITICAL - Files requiring updates for directory restructure:**
- **Settings Manager**: `./orchestrator/settings_manager.py` - User config read/write paths
- **Username Manager**: `./orchestrator/username_manager.py` - User discovery and creation
- **User ID CLI**: `./configs/cli/user_id/user_id.py` - User file references
- **CLI Manager**: `./orchestrator/cli_manager.py` - Memory command routing + basic analytics
- **Tool Manager**: `./orchestrator/manager_tools.py` - Analytics trigger integration
- **Workflow Manager**: `./orchestrator/workflow_manager.py` - Analytics trigger integration

**New integrations:**
- **Memory MCP**: Store and search memory content with user context
- **User Analytics Manager**: Track basic metrics with comprehensive trigger points
- **System Analytics Manager**: Anonymous aggregate analytics
- **Real-time Metrics**: Integration with analytics for live dashboards

## Success Criteria

- **Directory Restructure**: All existing functionality works with new nested user structure
- **Memory System**: `/memory "text"` saves with user_id and workflow_id associations
- **Basic Analytics**: Session, tool, workflow, cost metrics operational with proper triggers
- **Privacy Compliance**: GDPR-ready with single-command user data deletion
- **Performance**: Acceptable with collected JSON files and intelligent caching
- **Integration**: All managers work seamlessly with new architecture
- **Standardization**: All new files follow MAO patterns (CacheManager, @handle_errors, etc.)
- **Foundation Ready**: Analytics infrastructure supports easy metric expansion

## Quality Control

**Automatic Audit Integration**: Use MAO Implementation + Automatic Audit Pattern
1. **Implement** - Execute this SPEC completely
2. **Audit** - Run MAO Implementation Audit Add-On automatically  
3. **Fix** - Address all non-compliance items identified
4. **Validate** - Confirm fixes resolve audit findings
5. **Complete** - Mark implementation as audit-passed and production-ready

**Reference Documentation**: `MAO_ANALYTICS_COMPREHENSIVE_DOCUMENTATION.md` provides complete trigger specifications and privacy compliance guidance for any implementation questions.