# MAO Memory & Analytics System - Claude Code Implementation SPEC
> Bundled implementation: Memory System + User Analytics + System Analytics

## Why Bundled Together

**Shared Touchpoints**: Memory and Analytics systems both interact with:
- `settings_manager.py` - User configuration management
- `username_manager.py` - User identification and directory structure  
- User directory organization in `./configs/user/[username]/`
- Similar JSON storage patterns and discovery methods

**Implementation Efficiency**: Single implementation cycle prevents multiple migrations and ensures all user directory changes happen at once. Claude Code is welcome to adjust the bundling approach as needed.

## High-Level Objective

Add sophisticated memory system and privacy-compliant analytics infrastructure to MAO's solid foundation. Implement user preference storage, contextual suggestions, and comprehensive analytics while maintaining MAO's modular discovery philosophy.

## Mid-Level Objectives

- Create complete memory system with CLI commands and contextual suggestions  
- Build privacy-first analytics infrastructure (user vs system separation)
- Establish foundation for advanced user preference and analytics features
- Maintain MAO's modular discovery patterns for all new systems

## Implementation Notes

- **MAJOR CHANGE**: Restructure user directories from flat to nested organization
- Follow established MAO patterns (CacheManager, @handle_errors, estimate_cost)
- Use collected JSON files for analytics (not individual files per metric)
- Maintain privacy-first architecture with clear user vs system data separation
- Update all existing managers for new directory structure
- Bundle memory + analytics implementation to prevent multiple migrations

## Context

### Beginning Context
- Current user structure: ./configs/user/user_seanivore.json (flat)
- CLI command infrastructure established
- Memory MCP integrated as state persistence layer  
- Settings manager handles user configuration updates
- Username manager discovers and manages users

### Ending Context  
- New user structure: ./configs/user/seanivore/user_seanivore.json + subdirectories
- Functional memory system with /memory CLI commands
- Privacy-compliant analytics infrastructure (user + system)
- All existing managers updated for new directory structure
- Foundation for advanced user preference and analytics features

## Low-Level Tasks

### Phase 1: User Directory Restructure

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

### Phase 3: Analytics Infrastructure

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
```

```
CREATE: ./configs/user/seanivore/analytics/tool_usage.json
Schema: {
  "tool_usage": {
    "brave_search": {
      "total_uses": 15,
      "avg_cost": 0.001,
      "last_used": "2025-01-15T10:30:00Z",
      "efficiency_score": 0.95,
      "avg_response_time": 1.2
    },
    "dalle_generate": {
      "total_uses": 8,
      "avg_cost": 0.05, 
      "last_used": "2025-01-15T09:15:00Z",
      "efficiency_score": 0.88,
      "avg_response_time": 8.5
    }
    // NOTE: New tools automatically added via discovery when first used
  },
  "metadata": {
    "total_tools_tracked": 2,
    "discovery_enabled": true,
    "last_discovery_scan": "2025-01-15T10:30:00Z"
  }
}

IMPLEMENTATION: Dynamic tool discovery in user_analytics_manager.py
- scan_available_tools() method discovers tools via directory scanning
- track_tool_usage() automatically adds new tools to tracking
- Maintains historical data for removed tools
- Follows MAO modular philosophy: everything discoverable, nothing hardcoded
```

```
CREATE: ./configs/user/seanivore/analytics/workflow_metrics.json  
Schema: Workflow activation counts, completion rates, efficiency per user
```

```
CREATE: ./configs/user/seanivore/analytics/cost_tracking.json
Schema: Spend per minute, model costs, cost optimization metrics per user
```

#### Task 3.2: Create System Analytics Architecture
```
CREATE: ./configs/system/analytics/aggregate_usage.json
Schema: Anonymous usage patterns, no user identification
```

```
CREATE: ./configs/system/analytics/tool_performance.json
Schema: Tool efficiency, response times, success rates (anonymized)
```

```
CREATE: ./configs/system/analytics/model_metrics.json
Schema: Model performance, costs, success rates (anonymized)
```

```
CREATE: ./configs/system/analytics/system_health.json  
Schema: Resource usage, error rates, performance metrics
```

#### Task 3.3: Create Analytics Manager Services
```
CREATE: ./orchestrator/user_analytics_manager.py
- Functions: track_session(), track_tool_usage(), track_workflow(), track_costs()
- CRITICAL: Dynamic discovery methods for modular components
  * scan_available_tools() - Discovers tools via directory scanning
  * scan_available_workflows() - Discovers workflow types dynamically  
  * auto_add_component() - Adds new tools/workflows to tracking automatically
- Privacy: All data tied to user_id for deletion compliance
- Modular Philosophy: Everything discoverable, nothing hardcoded
- Standard patterns: CacheManager, @handle_errors, estimate_cost()
```

```
CREATE: ./orchestrator/system_analytics_manager.py
- Functions: aggregate_usage(), track_performance(), track_health()
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
```

#### Task 4.2: Update Existing CLI Commands for New User Structure
```
UPDATE: ./configs/cli/user_id/user_id.py
- Update file paths for new nested directory structure
- Ensure user discovery works with new organization
```

#### Task 4.3: Integration Testing
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
TEST: Analytics functionality  
- Verify: User analytics track correctly to user directories
- Verify: System analytics remain anonymous
- Verify: Privacy compliance deletion workflows work
```

## Integration Touchpoints

**CRITICAL - Files requiring updates for directory restructure:**
- **Settings Manager**: `./orchestrator/settings_manager.py` - User config read/write paths
- **Username Manager**: `./orchestrator/username_manager.py` - User discovery and creation
- **User ID CLI**: `./configs/cli/user_id/user_id.py` - User file references
- **CLI Manager**: `./orchestrator/cli_manager.py` - Memory command routing
- **Any workflow systems**: That store user-specific state

**New integrations:**
- **Memory MCP**: Store and search memory content with user context
- **User Analytics Manager**: Track memory usage, session data, tool usage
- **System Analytics Manager**: Anonymous aggregate analytics
- **Real-time Metrics**: Integration with analytics for live dashboards

## Success Criteria

- **Directory Restructure**: All existing functionality works with new nested user structure
- **Memory System**: `/memory "text"` saves with user_id and workflow_id associations
- **Analytics**: User analytics deletable for privacy, system analytics anonymous
- **Privacy Compliance**: GDPR-ready with single-command user data deletion
- **Performance**: Acceptable with collected JSON files and intelligent caching
- **Integration**: All managers work seamlessly with new architecture
- **Standardization**: All new files follow MAO patterns (CacheManager, @handle_errors, etc.)

## Quality Control

Append MAO Implementation Audit Add-On after completion to verify:
- File standardization compliance across all new files
- Architecture pattern compliance for nested directory structure  
- Integration point validation for all updated managers
- Privacy compliance check for user vs system data separation
- Testing validation for memory, analytics, and directory restructure functionality