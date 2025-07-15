# Mao's Comprehensive Analytics System
> Complete specifications for analytics collection, triggers, and implementation

## Table of Contents
1. [Analytics Architecture Overview](#analytics-architecture-overview)
2. [Trigger Point Specifications](#trigger-point-specifications)  
3. [Data Collection Matrix](#data-collection-matrix)
4. [Privacy Compliance Matrix](#privacy-compliance-matrix)
5. [Implementation Phases](#implementation-phases)
6. [Integration Architecture](#integration-architecture)
7. [Testing & Validation](#testing--validation)
8. [Future Extensibility](#future-extensibility)

---

## Analytics Architecture Overview

### Core Principles
- **Privacy-First**: User analytics deletable, system analytics anonymous
- **Non-Intrusive**: Analytics never break main functionality
- **Modular Discovery**: Dynamic detection of tools, workflows, and patterns
- **Real-time + Batch**: Immediate tracking with periodic aggregation

### Data Flow Architecture
```
User Actions → Trigger Points → Analytics Managers → JSON Storage → Aggregation → Insights
     ↓              ↓                    ↓               ↓             ↓           ↓
CLI Commands    Tool Manager     User Analytics    User Directory   System     Dashboard
Workflows      Workflow Mgr      System Analytics  System Directory Analytics    APIs
Tool Usage     Settings Mgr      Memory Analytics   Memory MCP      Privacy    Reports
```

### Storage Architecture
```
./configs/user/[username]/analytics/     # User-specific analytics (deletable)
./configs/system/analytics/              # Anonymous aggregate analytics
./memory_mcp/                           # Analytics patterns and insights
```

---

## Trigger Point Specifications

### Session Analytics Triggers

#### Session Start Detection
**Trigger Point**: `./interfaces/ui_terminal.py` - App initialization
**Code Location**: `main()` function entry point
**Data Collected**: 
- `session_id` (generated uuid)
- `start_time` (ISO timestamp)
- `user_id` (from username_manager)
- `app_version` (from version config)

**Implementation Hook**:
```python
# In ui_terminal.py main()
session_id = str(uuid.uuid4())
user_analytics_manager.track_session_start(session_id, user_id)
```

#### Session End Detection  
**Trigger Point**: `./interfaces/ui_terminal.py` - App shutdown
**Code Location**: Exit handlers, cleanup functions
**Data Collected**:
- `session_id` (from session start)
- `end_time` (ISO timestamp) 
- `total_duration` (calculated)
- `commands_executed` (counter)
- `workflows_run` (counter)

**Implementation Hook**:
```python
# In ui_terminal.py cleanup/exit
user_analytics_manager.track_session_end(session_id, end_time, session_stats)
```

#### Session Timeout Detection
**Trigger Point**: Inactivity monitoring (if implemented)
**Code Location**: Session management middleware
**Timeout Period**: 30 minutes inactivity
**Action**: Mark session as timed out, save partial data

### Tool Usage Analytics Triggers

#### Tool Invocation Start
**Trigger Point**: `./orchestrator/manager_tools.py` - Tool execution begins
**Code Location**: `execute_tool()` method entry
**Data Collected**:
- `tool_name` (discovered dynamically)
- `invocation_id` (generated uuid)
- `start_time` (ISO timestamp)
- `user_id` (from session context)
- `cost_estimate` (from tool's estimate_cost())
- `input_parameters` (sanitized, no sensitive data)

**Implementation Hook**:
```python
# In manager_tools.py execute_tool()
invocation_id = str(uuid.uuid4())
start_time = datetime.utcnow().isoformat()
user_analytics_manager.track_tool_start(tool_name, invocation_id, start_time, user_id)
```

#### Tool Execution Completion
**Trigger Point**: `./orchestrator/manager_tools.py` - Tool execution ends
**Code Location**: `execute_tool()` method completion (success/failure)
**Data Collected**:
- `invocation_id` (from start)
- `end_time` (ISO timestamp)
- `duration_seconds` (calculated)
- `success_status` (boolean)
- `actual_cost` (from real API usage)
- `error_type` (if failed)
- `output_size` (sanitized metrics)

**Implementation Hook**:
```python
# In manager_tools.py execute_tool() completion
end_time = datetime.utcnow().isoformat()
duration = (end_time - start_time).total_seconds()
user_analytics_manager.track_tool_completion(invocation_id, end_time, duration, success, actual_cost)
```

#### Tool Discovery Updates
**Trigger Point**: `./orchestrator/manager_tools.py` - Tool directory scanning
**Code Location**: `discover_all_tools()` method
**Frequency**: On app startup, manual refresh, periodic scanning
**Data Collected**:
- `available_tools` (list of discovered tools)
- `new_tools` (tools added since last scan)
- `removed_tools` (tools no longer available)
- `scan_timestamp` (ISO timestamp)

### Workflow Analytics Triggers

#### Workflow Setup Start
**Trigger Point**: Workflow setup script execution
**Code Location**: `./orchestrator/workflow_manager.py` - Workflow creation
**Data Collected**:
- `workflow_id` (generated uuid)
- `workflow_command` (command name)
- `setup_start_time` (ISO timestamp)
- `user_id` (from session context)
- `workflow_tags` (extracted from README.md)

**Implementation Hook**:
```python
# In workflow setup script
workflow_id = str(uuid.uuid4())
tags = extract_tags_from_readme(f"{workflow_command}_README.md")
user_analytics_manager.track_workflow_setup_start(workflow_id, workflow_command, tags, user_id)
```

#### Workflow Execution Start
**Trigger Point**: First agent activation in workflow
**Code Location**: `./orchestrator/agent_orchestrator.py` - Agent spawning
**Data Collected**:
- `workflow_id` (from setup)
- `execution_start_time` (ISO timestamp)
- `agent_count` (total agents planned)
- `parallel_agents` (boolean from workflow config)
- `estimated_duration` (from workflow metadata)

#### Workflow Phase Completion
**Trigger Point**: Each workflow phase completion
**Code Location**: `./orchestrator/workflow_state.py` - Phase transitions
**Data Collected**:
- `workflow_id` (from context)
- `phase_name` (from workflow config)
- `phase_completion_time` (ISO timestamp)
- `phase_duration` (calculated)
- `phase_success` (boolean)
- `deliverables_created` (file count/types)

#### Workflow Final Completion
**Trigger Point**: Workflow cleanup and finalization
**Code Location**: `./orchestrator/workflow_manager.py` - Workflow completion
**Data Collected**:
- `workflow_id` (from context)
- `final_completion_time` (ISO timestamp)
- `total_duration` (from start to finish)
- `success_status` (boolean)
- `total_cost` (accumulated from all operations)
- `deliverable_summary` (types and counts)
- `efficiency_score` (calculated metric)

### CLI Command Analytics Triggers

#### Command Invocation
**Trigger Point**: `./orchestrator/cli_manager.py` - Command routing
**Code Location**: Command dispatch methods
**Data Collected**:
- `command_name` (discovered dynamically)
- `execution_start_time` (ISO timestamp)
- `user_id` (from session context)
- `command_type` (slash vs flag)
- `parameters_count` (sanitized count, not values)

#### Command Completion
**Trigger Point**: `./orchestrator/cli_manager.py` - Command completion
**Code Location**: Command completion handlers
**Data Collected**:
- `command_name` (from start)
- `execution_end_time` (ISO timestamp)
- `duration_seconds` (calculated)
- `success_status` (boolean)
- `error_type` (if failed)

### Memory System Analytics Triggers

#### Memory Creation
**Trigger Point**: `./orchestrator/user_memory_manager.py` - Memory storage
**Code Location**: `store_memory()` method
**Data Collected**:
- `memory_id` (generated uuid)
- `creation_time` (ISO timestamp)
- `user_id` (from context)
- `memory_type` (from tags)
- `workflow_context` (if applicable)
- `content_length` (character count)

#### Memory Retrieval
**Trigger Point**: `./orchestrator/user_memory_manager.py` - Memory access
**Code Location**: `retrieve_memories()` method
**Data Collected**:
- `retrieval_time` (ISO timestamp)
- `user_id` (from context)
- `query_type` (list all, search, contextual)
- `results_count` (number of memories returned)
- `workflow_context` (if applicable)

#### Memory Suggestion Usage
**Trigger Point**: `./orchestrator/user_memory_manager.py` - Contextual suggestions
**Code Location**: `suggest_contextual()` method
**Data Collected**:
- `suggestion_time` (ISO timestamp)
- `user_id` (from context)
- `workflow_context` (current workflow)
- `suggestions_offered` (count)
- `suggestions_accepted` (user feedback)

### Cost Tracking Analytics Triggers

#### API Cost Accumulation
**Trigger Point**: Model API calls across all managers
**Code Location**: Model managers, API wrappers
**Data Collected**:
- `api_call_time` (ISO timestamp)
- `model_name` (provider + model)
- `operation_type` (completion, embeddings, etc.)
- `token_count` (input + output)
- `actual_cost` (calculated from provider rates)
- `user_id` (from session context)

#### Cost Optimization Events
**Trigger Point**: Model selection decisions
**Code Location**: Model managers, cost optimization logic
**Data Collected**:
- `optimization_time` (ISO timestamp)
- `original_model` (what would have been used)
- `selected_model` (what was actually used)
- `cost_savings` (calculated difference)
- `performance_impact` (if measurable)

---

## Data Collection Matrix

### Session Metrics (`session_metrics.json`)

| Metric              | Trigger Point        | Calculation Method             | Update Frequency | Privacy Level |
| ------------------- | -------------------- | ------------------------------ | ---------------- | ------------- |
| `session_id`        | App start            | UUID generation                | Once per session | User-tied     |
| `start_time`        | App initialization   | ISO timestamp                  | Once per session | User-tied     |
| `end_time`          | App shutdown/timeout | ISO timestamp                  | Once per session | User-tied     |
| `duration_minutes`  | Session end          | `(end_time - start_time) / 60` | Once per session | User-tied     |
| `workflow_count`    | Workflow completion  | Increment counter              | Real-time        | User-tied     |
| `tool_activations`  | Tool completion      | Increment counter              | Real-time        | User-tied     |
| `commands_executed` | CLI completion       | Increment counter              | Real-time        | User-tied     |
| `cost_total`        | API calls            | Accumulate costs               | Real-time        | User-tied     |

### Tool Usage Metrics (`tool_usage.json`)

| Metric              | Trigger Point   | Calculation Method                | Update Frequency | Privacy Level |
| ------------------- | --------------- | --------------------------------- | ---------------- | ------------- |
| `total_uses`        | Tool completion | Increment counter                 | Real-time        | User-tied     |
| `avg_cost`          | Tool completion | `total_cost / total_uses`         | Each completion  | User-tied     |
| `last_used`         | Tool completion | ISO timestamp                     | Each completion  | User-tied     |
| `efficiency_score`  | Tool completion | `success_rate * (1/avg_duration)` | Each completion  | User-tied     |
| `avg_response_time` | Tool completion | Running average of durations      | Each completion  | User-tied     |
| `success_rate`      | Tool completion | `successes / total_attempts`      | Each completion  | User-tied     |
| `error_patterns`    | Tool failure    | Categorize error types            | Each failure     | User-tied     |

### Workflow Metrics (`workflow_metrics.json`)

| Metric              | Trigger Point  | Calculation Method    | Update Frequency | Privacy Level |
| ------------------- | -------------- | --------------------- | ---------------- | ------------- |
| `workflow_runs`     | Workflow start | Increment counter     | Real-time        | User-tied     |
| `completion_rate`   | Workflow end   | `completed / started` | Each completion  | User-tied     |
| `avg_duration`      | Workflow end   | Running average       | Each completion  | User-tied     |
| `workflow_tags`     | Setup script   | Extract from README   | Each setup       | User-tied     |
| `tag_success_rates` | Workflow end   | Group by tags         | Each completion  | User-tied     |
| `cost_per_workflow` | Workflow end   | Accumulate costs      | Each completion  | User-tied     |
| `deliverable_types` | Workflow end   | Extract from outputs  | Each completion  | User-tied     |

### Cost Tracking Metrics (`cost_tracking.json`)

| Metric                 | Trigger Point   | Calculation Method              | Update Frequency  | Privacy Level |
| ---------------------- | --------------- | ------------------------------- | ----------------- | ------------- |
| `daily_spend`          | API calls       | Accumulate by date              | Real-time         | User-tied     |
| `model_breakdown`      | API calls       | Group by model                  | Real-time         | User-tied     |
| `cost_per_minute`      | Session end     | `total_cost / session_duration` | Each session      | User-tied     |
| `optimization_savings` | Model selection | Track alternative costs         | Each optimization | User-tied     |
| `spending_trends`      | Daily rollup    | Calculate trends                | Daily batch       | User-tied     |

---

## Privacy Compliance Matrix

### User Analytics (Deletable Data)
| Data Category | Storage Location                                            | User Identifier | Deletion Method       | Retention Policy |
| ------------- | ----------------------------------------------------------- | --------------- | --------------------- | ---------------- |
| Session Data  | `./configs/user/[username]/analytics/session_metrics.json`  | `user_id`       | Delete user directory | User-controlled  |
| Tool Usage    | `./configs/user/[username]/analytics/tool_usage.json`       | `user_id`       | Delete user directory | User-controlled  |
| Workflow Data | `./configs/user/[username]/analytics/workflow_metrics.json` | `user_id`       | Delete user directory | User-controlled  |
| Cost Data     | `./configs/user/[username]/analytics/cost_tracking.json`    | `user_id`       | Delete user directory | User-controlled  |
| Memory Data   | `./configs/user/[username]/memories/`                       | `user_id`       | Delete user directory | User-controlled  |

### System Analytics (Anonymous Data)
| Data Category    | Storage Location                                   | Anonymization Method         | Retention Policy | Purpose                  |
| ---------------- | -------------------------------------------------- | ---------------------------- | ---------------- | ------------------------ |
| Tool Performance | `./configs/system/analytics/tool_performance.json` | Remove all user identifiers  | 1 year rolling   | Performance optimization |
| Aggregate Usage  | `./configs/system/analytics/aggregate_usage.json`  | Statistical aggregation only | 1 year rolling   | Product insights         |
| Model Metrics    | `./configs/system/analytics/model_metrics.json`    | Remove user context          | 1 year rolling   | Model optimization       |
| System Health    | `./configs/system/analytics/system_health.json`    | No user data included        | 1 year rolling   | System monitoring        |

### Data Flow Privacy Controls
1. **Collection Phase**: All user analytics include `user_id` for easy identification
2. **Processing Phase**: User data stays in user directories, system data aggregated anonymously
3. **Anonymization Phase**: System analytics strip all user identifiers before storage
4. **Deletion Phase**: Single command deletes entire user directory and all associated data

---

## Implementation Phases

### Phase 1: Foundation Analytics (v4.0)
**Scope**: Basic tracking for core metrics
**Implementation Priority**: 
1. Session tracking (start/end/duration)
2. Tool usage counting (uses, success rate)
3. Basic workflow metrics (runs, completion)
4. Simple cost accumulation

**Integration Points**:
- `ui_terminal.py` - Session boundaries
- `manager_tools.py` - Tool invocation/completion
- `workflow_manager.py` - Workflow lifecycle
- Model managers - Cost accumulation

### Phase 2: Advanced Analytics (v4.1)
**Scope**: Calculated metrics and pattern analysis
**Implementation Priority**:
1. Efficiency scoring and optimization suggestions
2. Workflow tag analysis and categorization
3. Predictive cost optimization
4. Usage pattern recognition

### Phase 3: Intelligence Layer (v4.2+)
**Scope**: AI-powered insights and recommendations
**Implementation Priority**:
1. Workflow optimization suggestions
2. Tool recommendation engine
3. Cost optimization automation
4. Productivity insights

---

## Integration Architecture

### Analytics Manager Hierarchy
```
UserAnalyticsManager
├── SessionTracker
├── ToolUsageTracker  
├── WorkflowTracker
├── CostTracker
└── MemoryTracker

SystemAnalyticsManager
├── AggregateAnalyzer
├── PerformanceMonitor
├── HealthChecker
└── TrendAnalyzer
```

### Integration with Existing MAO Systems

#### CLI Manager Integration
**File**: `./orchestrator/cli_manager.py`
**Integration Points**:
- Command dispatch: Track command usage
- Command completion: Track success/failure rates
- Help requests: Track user assistance patterns

**Code Changes Required**:
```python
# In cli_manager.py execute_command()
analytics.track_command_start(command_name, user_id)
try:
    result = execute_actual_command()
    analytics.track_command_success(command_name, duration)
except Exception as e:
    analytics.track_command_failure(command_name, error_type)
```

#### Tool Manager Integration  
**File**: `./orchestrator/manager_tools.py`
**Integration Points**:
- Tool discovery: Track available tools
- Tool execution: Track usage and performance
- Tool errors: Track failure patterns

**Code Changes Required**:
```python
# In manager_tools.py execute_tool()
invocation_id = analytics.track_tool_start(tool_name, user_id)
try:
    result = tool.execute()
    analytics.track_tool_success(invocation_id, duration, cost)
except Exception as e:
    analytics.track_tool_failure(invocation_id, error_type)
```

#### Workflow Manager Integration
**File**: `./orchestrator/workflow_manager.py`
**Integration Points**:
- Workflow creation: Track workflow setup
- Workflow execution: Track progress and completion
- Workflow cleanup: Track final results

#### Settings Manager Integration
**File**: `./orchestrator/settings_manager.py`
**Integration Points**:
- User config changes: Track preference modifications
- Settings validation: Track configuration errors

### Error Handling Integration
**Principle**: Analytics failures never break main functionality

**Implementation Pattern**:
```python
def track_analytics_safely(analytics_function, *args, **kwargs):
    try:
        return analytics_function(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Analytics tracking failed: {e}")
        # Continue execution without analytics
        return None
```

---

## Testing & Validation

### Unit Testing Requirements
1. **Analytics Manager Tests**:
   - Verify each trigger point captures correct data
   - Test privacy compliance (user vs system data separation)
   - Validate error handling (analytics failures don't break functionality)

2. **Integration Tests**:
   - End-to-end workflow with analytics tracking
   - Tool execution with complete analytics capture
   - Session lifecycle with proper data collection

3. **Privacy Tests**:
   - User data deletion removes all associated analytics
   - System analytics contain no user identifiers
   - Data flow validation from user to anonymous aggregation

### Validation Metrics
- **Data Completeness**: All specified metrics are captured
- **Data Accuracy**: Calculated metrics are mathematically correct
- **Performance Impact**: Analytics add <5% overhead to operations
- **Privacy Compliance**: User data is properly segregated and deletable

### Testing Data Scenarios
1. **Single User Session**: Complete analytics lifecycle
2. **Multi-User Environment**: Data separation validation
3. **Error Conditions**: Analytics robustness testing
4. **High Load**: Performance impact assessment

---

## Future Extensibility

### Adding New Analytics Metrics
**Pattern to Follow**:
1. **Define Trigger Point**: Identify exact code location for data collection
2. **Specify Data Schema**: Define JSON structure and data types
3. **Implement Privacy Classification**: User-tied or anonymous
4. **Add Integration Hook**: Modify relevant manager to collect data
5. **Update Documentation**: Add to this comprehensive specification

### New Analytics Categories
**Preparation for Future Features**:
- **Collaboration Analytics**: Multi-user workflow patterns
- **Learning Analytics**: User skill development tracking
- **Optimization Analytics**: System performance tuning
- **Business Analytics**: ROI and productivity measurements

### Extensibility Patterns
1. **Discoverable Metrics**: New metrics auto-discovered like tools/workflows
2. **Plugin Architecture**: Analytics modules as discoverable components
3. **Configuration-Driven**: Analytics behavior controlled by JSON configs
4. **API-Ready**: Analytics designed for external system integration

---

## Summary

This comprehensive analytics system provides:
- **Complete Trigger Specification**: Exact integration points for every metric
- **Privacy-First Architecture**: User data deletable, system data anonymous
- **Modular Implementation**: Follows MAO principles of discoverability
- **Future-Proof Design**: Extensible patterns for growing analytics needs
- **Quality Assurance**: Comprehensive testing and validation approach

The documentation serves as both implementation guide and ongoing reference for maintaining and extending MAO's analytics capabilities while preserving user privacy and system modularity.

---

*Last Updated: 2025-01-15*
*Version: 1.0 - Initial Comprehensive Specification*