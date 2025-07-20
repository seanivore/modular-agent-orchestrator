# CLI Command System - Logs System Documentation

## File Information
- **Files Analyzed**: 
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/logs/logs.py`
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/logs/ui_logs.py`
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/logs/logs.json`
- **Total Files**: 3
- **Documentation Date**: 2025-07-19

## Simple Sentence Form

**Overview**: The Logs system provides comprehensive workflow log viewing with advanced filtering, search capabilities, and Rich console-based professional display patterns. It integrates with Memory MCP and workflow managers to provide detailed workflow history, status tracking, and sophisticated log analysis with multiple display modes.

## Code & Explanation

### Architecture Overview

**Workflow Log Management Architecture**:
- Integration with Memory MCP and workflow state managers
- Advanced filtering by workflow ID, status, content search, and date ranges
- Multi-format display (single log details, table view, empty state guidance)
- Real-time log statistics and analytics
- Professional Rich console UI with trees, tables, and panels

**4-File Command Structure Implementation**:
- `logs.py` - Core log retrieval logic with advanced filtering capabilities
- `ui_logs.py` - Rich console UI with professional display patterns
- `logs.json` - Command configuration with comprehensive filter options
- No button file needed for this information display command

**Manager Integration Patterns**:
- `MemoryMCPManager` for workflow context and observation retrieval
- `WorkflowStateManager` for workflow status and summary data
- `WorkflowManager` for active workflow state fingerprinting
- Graceful fallback when managers unavailable

### Advanced Filtering Implementation

**Multi-Parameter Filtering System**:
```python
def _apply_filters(logs: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply filtering based on parameters"""
    filtered_logs = logs
    
    # Filter by status
    if params.get("status_filter"):
        status_filter = params["status_filter"]
        filtered_logs = [log for log in filtered_logs if log.get("status") == status_filter]
    
    # Filter by search query
    if params.get("search_query"):
        search_query = params["search_query"].lower()
        filtered_logs = [
            log for log in filtered_logs 
            if search_query in log.get("message", "").lower() 
            or search_query in str(log.get("details", {})).lower()
            or search_query in log.get("workflow_id", "").lower()
        ]
    
    # Filter by date range
    if params.get("date_range"):
        filtered_logs = _filter_by_date_range(filtered_logs, params["date_range"])
    
    # Apply limit with sorting
    limit = params.get("limit", 50)
    if limit and len(filtered_logs) > limit:
        filtered_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        filtered_logs = filtered_logs[:limit]
    
    return filtered_logs
```

**Date Range Filtering**:
- Flexible format support (1d, 7d, 30d for days; 1h, 12h, 24h for hours)
- Robust timestamp parsing with fallback handling
- Inclusive filtering with proper error handling

**Cost Estimation with Usage Scaling**:
- Base cost: 0.001 for standard log viewing
- Search operations: +0.0005 additional cost
- Large limit scaling: +(limit-50) * 0.0001 per extra entry
- Date range filtering: +0.0003 for processing complexity

### Rich Console UI Architecture

**Multi-Display Pattern System**:
```python
def display_logs_result(result: Dict[str, Any]) -> None:
    """Display logs command results with consistent CLI UI patterns"""
    # Display header with summary
    _display_logs_header(total_logs, statistics, filters_applied)
    
    # Display logs based on content
    if not logs:
        _display_empty_logs()
    elif len(logs) == 1:
        _display_single_log_details(logs[0])
    else:
        _display_logs_table(logs)
    
    # Display footer with navigation hints
    _display_logs_footer(filters_applied)
```

**Professional Display Components**:
- Panel-based headers with statistics and filter summaries
- Tree structures for detailed log data visualization
- Color-coded table displays with status styling
- Contextual help and usage guidance
- Empty state messaging with actionable suggestions

### Log Statistics and Analytics

**Comprehensive Log Analytics**:
```python
def _get_log_statistics(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate statistics for log summary"""
    stats = {
        "total": len(logs),
        "by_status": {},
        "by_type": {},
        "date_range": {
            "oldest": None,
            "newest": None
        }
    }
    
    # Status and type counting
    # Date range calculation
    # Timestamp analysis
```

## Written & Illustrated Data Info

### Data In-Flow

**Log Filtering Parameters**:
```json
{
  "workflow_id": "string (specific workflow filter)",
  "search_query": "string (content search term)",
  "status_filter": "string (active, completed, error, etc.)",
  "date_range": "string (1d, 7d, 30d, 1h, 12h, 24h)",
  "limit": "integer (max entries, default: 50)"
}
```

**Manager Integration Calls**:
- Memory MCP workflow context retrieval
- Workflow state manager summary queries
- Active workflow status checking
- System state fingerprinting for cache keys

### Data Out-Flow

**Comprehensive Log Response**:
```json
{
  "success": true,
  "logs": [
    {
      "workflow_id": "uuid-string",
      "status": "active|completed|error",
      "message": "Workflow log entry description",
      "timestamp": "2025-07-19T...",
      "type": "workflow_log|system_log|error_log",
      "details": {
        "phases_total": 5,
        "phases_completed": 3,
        "health": "good",
        "last_activity": "2025-07-19T...",
        "context_available": true,
        "recent_observations": ["obs1", "obs2"]
      }
    }
  ],
  "total_logs": 15,
  "statistics": {
    "total": 15,
    "by_status": {
      "active": 3,
      "completed": 10,
      "error": 2
    },
    "by_type": {
      "workflow_log": 12,
      "system_log": 2,
      "error_log": 1
    },
    "date_range": {
      "oldest": "2025-07-18T...",
      "newest": "2025-07-19T..."
    }
  },
  "filters_applied": {
    "search": "error",
    "date_range": "1d",
    "limit": 50
  },
  "timestamp": "2025-07-19T..."
}
```

**Rich Console Display Elements**:
- **Header Panel**: Summary with filter status and statistics
- **Table Display**: Workflow ID, Status, Type, Message, Timestamp columns
- **Single Log Detail**: Expanded view with tree structure for details
- **Footer Panel**: Usage hints and related command suggestions
- **Color Coding**: Status-based styling (red=error, green=completed, yellow=active)

**Professional Error Display**:
```json
{
  "display_type": "error_panel",
  "title": "Logs Command Error",
  "content": "Error message with troubleshooting",
  "suggestions": [
    "Check if workflow managers are available",
    "Verify workflow directory permissions",
    "Try /doctor for system diagnostics"
  ]
}
```

## Dependencies

### Core System Architecture Dependencies
- **Batch 01**: Application Foundation - terminal interface integration
- **Batch 02**: Orchestrator Core - cache system, error handling, Memory MCP integration
- **Batch 03**: Orchestrator Managers - workflow_manager, workflow_state, memory_mcp managers

### Specific Integration Points
- `orchestrator.memory_mcp.MemoryMCPManager` - Workflow context and observation data
- `orchestrator.workflow_state.WorkflowStateManager` - Workflow status and summaries
- `orchestrator.workflow_manager.WorkflowManager` - System state fingerprinting
- `orchestrator.cache.cache_system.CacheManager` - Short-term caching (2 minutes)

### Rich Console Dependencies
- `rich.console.Console` - Terminal output management
- `rich.table.Table` - Professional log table display
- `rich.panel.Panel` - Header, footer, and error formatting
- `rich.tree.Tree` - Hierarchical detail display
- `rich.columns.Columns` - Layout management

## Technical Implementation Notes

### Memory MCP Integration Excellence
- Workflow context retrieval with observation history
- Recent observations limiting (last 5) for performance
- Graceful handling when context unavailable
- Single source of truth for workflow state

### Advanced Search Capabilities
- Multi-field search (message, details, workflow_id)
- Case-insensitive matching across all searchable fields
- Flexible date range parsing with multiple formats
- Combined filter support with logical AND operations

### Performance Optimization
- Short cache duration (2 minutes) for frequently changing logs
- Timestamp-based sorting for relevance
- Limit-based pagination with proper ordering
- System state fingerprinting for intelligent cache invalidation

### Professional UI Design
- Adaptive display based on result count (empty/single/multiple)
- Contextual help based on current filter state
- Color-coded status indicators for quick scanning
- Progressive disclosure with expandable detail views

### Error Handling Excellence
- Graceful fallback when managers unavailable
- Invalid timestamp handling in filters
- Manager import error recovery
- Clear user guidance for troubleshooting

This Logs system demonstrates MAO's sophisticated approach to workflow monitoring with professional-grade filtering, Rich console integration, and comprehensive manager coordination for complete workflow visibility.