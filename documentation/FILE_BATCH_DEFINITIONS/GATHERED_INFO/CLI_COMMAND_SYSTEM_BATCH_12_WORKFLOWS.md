# CLI Command System - Workflows System Documentation

## File Information
- **Files Analyzed**: 
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/workflows/workflows.py`
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/workflows/ui_workflows.py`
  - `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/workflows/workflows.json`
- **Total Files**: 3
- **Documentation Date**: 2025-07-19

## Simple Sentence Form

**Overview**: The Workflows system provides comprehensive workflow discovery and management with advanced search, filtering, and categorization capabilities. It integrates with WorkflowManager to display active, temporary, and completed workflows with Rich console-based professional display patterns and detailed statistics.

## Code & Explanation

### Architecture Overview

**Workflow Discovery Architecture**:
- WorkflowManager integration for comprehensive workflow data access
- Multi-category workflow organization (active, temporary, completed, created)
- Advanced filtering by search terms, status, user ID, and custom commands
- Directory-based caching with fingerprinting for performance optimization
- Professional Rich console UI with grouped displays and statistics

**4-File Command Structure Implementation**:
- `workflows.py` - Core workflow discovery logic with WorkflowManager integration
- `ui_workflows.py` - Rich console UI with status-grouped displays and statistics
- `workflows.json` - Command configuration with comprehensive operation definitions
- No button file needed for this information display command

**WorkflowManager Integration Patterns**:
- `manager.list_workflows()` for comprehensive workflow discovery
- `manager.find_workflows(search_term)` for search functionality
- `manager.list_active_workflows()` for currently running workflows
- `manager.list_temp_workflows()` for workflows in creation process

### Advanced Filtering Implementation

**Multi-Parameter Filtering System**:
```python
def _discover_workflows(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core workflow discovery implementation"""
    manager = WorkflowManager()
    
    # Get search parameters
    search_term = params.get("search", "") if params else ""
    status_filter = params.get("status", "") if params else ""
    user_id_filter = params.get("user_id", "") if params else ""
    command_filter = params.get("command", "") if params else ""
    
    # Get all workflows first
    if search_term:
        workflows = manager.find_workflows(search_term)
    else:
        workflows = manager.list_workflows()
    
    # Apply additional filters
    filtered_workflows = workflows
    
    if status_filter:
        filtered_workflows = [w for w in filtered_workflows 
                            if w.get("status", "").lower() == status_filter.lower()]
    
    if user_id_filter:
        filtered_workflows = [w for w in filtered_workflows 
                            if w.get("user_id", "").lower() == user_id_filter.lower()]
    
    if command_filter:
        filtered_workflows = [w for w in filtered_workflows 
                            if command_filter.lower() in w.get("custom_command", "").lower()]
```

**Intelligent Caching with Directory Fingerprinting**:
- 15-minute cache duration for workflow data
- Directory state fingerprinting including modification times
- Exclusion of temporary and template directories
- File count and last modification timestamp tracking

### Professional Statistics and Analytics

**Comprehensive Workflow Statistics**:
```python
def _compile_workflow_stats(workflows: List[Dict], active: List[Dict], temp: List[Dict]) -> Dict[str, Any]:
    """Compile workflow statistics for overview"""
    
    # Status distribution
    status_counts = {}
    for workflow in workflows:
        status = workflow.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # User distribution
    user_counts = {}
    for workflow in workflows:
        user_id = workflow.get("user_id", "unknown")
        user_counts[user_id] = user_counts.get(user_id, 0) + 1
    
    # Recent activity (workflows modified in last 7 days)
    recent_threshold = datetime.now().timestamp() - (7 * 24 * 3600)
    recent_workflows = []
    
    # ... activity analysis logic
    
    return {
        "status_distribution": status_counts,
        "user_distribution": user_counts,
        "command_distribution": command_counts,
        "recent_activity_count": len(recent_workflows),
        "has_deliverables_count": len([w for w in workflows if w.get("has_deliverables", False)]),
        "has_metadata_count": len([w for w in workflows if w.get("has_metadata", False)])
    }
```

### Rich Console UI Architecture

**Status-Grouped Display Pattern**:
- Active workflows highlighted with green styling
- Temporary workflows highlighted with yellow styling
- Completed workflows grouped with organized status sections
- Individual workflow details with comprehensive metadata display

**Professional Display Components**:
```python
def _display_single_workflow(workflow: Dict[str, Any], highlight_active: bool = False, highlight_temp: bool = False) -> None:
    """Display individual workflow with key metadata"""
    
    # Core identification
    workflow_id = workflow.get("workflow_id", "unknown")
    custom_command = workflow.get("custom_command", "unknown")
    status = workflow.get("status", "unknown")
    
    # Status styling
    status_color = "green" if highlight_active else ("yellow" if highlight_temp else "blue")
    status_text = f"[{status_color}]{status}[/{status_color}]"
    
    console.print(f"  [bold]{custom_command}[/bold] ({workflow_id}) - {status_text}")
    
    # Goal and description display
    # User and timestamp information
    # Directory and deliverable status indicators
```

## Written & Illustrated Data Info

### Data In-Flow

**Workflow Search and Filter Parameters**:
```json
{
  "search": "string (search term for ID, command, goal, description)",
  "status": "string (active, completed, created, temp)",
  "user_id": "string (filter by specific user)",
  "command": "string (filter by custom command pattern)"
}
```

**WorkflowManager Integration Calls**:
- `manager.list_workflows()` - All configured workflows
- `manager.find_workflows(search_term)` - Search-based discovery
- `manager.list_active_workflows()` - Currently running workflows
- `manager.list_temp_workflows()` - Workflows in creation process

### Data Out-Flow

**Comprehensive Workflows Response**:
```json
{
  "success": true,
  "workflows": [
    {
      "workflow_id": "uuid-string",
      "custom_command": "analyze_project",
      "status": "completed",
      "workflow_goal": "Analyze project structure and dependencies",
      "workflow_description": "Complete analysis of codebase",
      "user_id": "user123",
      "created_at": "2025-07-19T10:00:00Z",
      "last_modified": "2025-07-19T15:30:00Z",
      "directory_name": "analysis_2025_07_19",
      "has_deliverables": true,
      "has_metadata": true
    }
  ],
  "active_workflows": [
    {
      "workflow_id": "active-uuid",
      "custom_command": "current_task",
      "status": "active",
      "user_id": "user123"
    }
  ],
  "temp_workflows": [
    {
      "workflow_id": "temp-uuid",
      "custom_command": "creating_workflow",
      "status": "temp",
      "user_id": "user123"
    }
  ],
  "total_count": 25,
  "filtered_count": 15,
  "active_count": 2,
  "temp_count": 1,
  "stats": {
    "status_distribution": {
      "completed": 20,
      "active": 2,
      "created": 3
    },
    "user_distribution": {
      "user123": 15,
      "user456": 10
    },
    "command_distribution": {
      "analyze_project": 8,
      "review_code": 5,
      "generate_docs": 12
    },
    "recent_activity_count": 8,
    "has_deliverables_count": 18,
    "has_metadata_count": 22
  },
  "filters_applied": {
    "search": "analyze",
    "status": "",
    "user_id": "",
    "command": ""
  },
  "discovery_time": "2025-07-19T..."
}
```

**Rich Console Display Structure**:
- **Summary Header**: Total counts with filter status and active indicators
- **Active Workflows Section**: Green-highlighted currently running workflows
- **Temporary Workflows Section**: Yellow-highlighted workflows in creation
- **Status-Grouped Listings**: Organized by completed, active, created, unknown
- **Individual Workflow Display**: Custom command, workflow ID, status, goal/description, user info, directory status
- **Statistics Section**: Status distribution, top users, recent activity, completion indicators

**Professional Error Display**:
```json
{
  "display_type": "error_panel",
  "title": "Workflows Command Error",
  "content": "Workflow discovery failed: [error details]",
  "style": "red"
}
```

## Dependencies

### Core System Architecture Dependencies
- **Batch 01**: Application Foundation - terminal interface integration
- **Batch 02**: Orchestrator Core - cache system, error handling, workflow manager
- **Batch 03**: Orchestrator Managers - workflow_manager for data access

### Specific Integration Points
- `orchestrator.workflow_manager.WorkflowManager` - Primary workflow data source
- `orchestrator.cache.cache_system.CacheManager` - Directory-based caching (15 minutes)
- `orchestrator.error_handling` - Comprehensive error patterns

### Rich Console Dependencies
- `rich.console.Console` - Terminal output management
- `rich.table.Table` - Structured workflow data display
- `rich.panel.Panel` - Summary headers and error formatting
- `rich.text.Text` - Styled text output
- `rich.progress.Progress` - Loading indicators for long operations

### Related Command Integration
- `/logs` command for workflow log viewing
- `/stats` command for system performance metrics
- `/review` command for detailed workflow analysis

## Technical Implementation Notes

### WorkflowManager Excellence
- Comprehensive workflow discovery with multiple data sources
- Search functionality with intelligent matching
- Active workflow tracking for real-time status
- Temporary workflow management during creation process

### Advanced Filtering Capabilities
- Multi-parameter filtering with logical AND operations
- Case-insensitive search across multiple fields
- Status-based filtering with exact matching
- User-based filtering for multi-user environments
- Custom command pattern matching

### Performance Optimization
- Intelligent caching with directory fingerprinting (15 minutes)
- Exclusion of temporary and template directories from fingerprinting
- Workflow directory state tracking for cache invalidation
- Cost estimation: 0.002 (low complexity for file system operations)

### Professional UI Design
- Status-based workflow grouping for natural organization
- Color-coded status indicators for quick visual scanning
- Comprehensive metadata display with formatted timestamps
- Empty state messaging with actionable guidance
- Statistical insights with user activity analysis

### Workflow Lifecycle Support
- Active workflow highlighting for operational awareness
- Temporary workflow tracking during creation process
- Completed workflow organization with metadata indicators
- Recent activity analysis (7-day window) for productivity insights

This Workflows system demonstrates MAO's sophisticated approach to workflow management with comprehensive discovery, professional Rich console integration, and detailed statistical analysis for complete workflow lifecycle visibility.