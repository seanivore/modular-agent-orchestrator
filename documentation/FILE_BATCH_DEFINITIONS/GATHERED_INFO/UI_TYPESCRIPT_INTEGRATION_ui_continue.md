# UI TypeScript Integration - ui_continue.py

## Overview
Continue CLI command UI component that provides complex workflow continuation interface with multiple display states. Handles interrupted workflow recovery, workflow selection, and continuation status for the LOCAL application subprocess architecture.

## Code & Explanation

### Architecture Overview
**Workflow Continuation Management**: Sophisticated UI component for managing workflow recovery and continuation.

- **Multiple Display States**: Handles various continuation scenarios (recent interrupted, specific workflow, selection interface)
- **Recovery Planning**: Displays workflow recovery plans and readiness status
- **Progress Tracking**: Shows workflow progress and completion status
- **Selection Interface**: Provides workflow selection when multiple options are available

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
def display_continue_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Primary subprocess interface for workflow continuation.
    Returns structured data based on continuation type.
    """
    continuation_type = result.get("continuation_type", "unknown")
    
    if continuation_type == "recent_interrupted":
        return _format_recent_interrupted_display(result)
    elif continuation_type == "specific_workflow":
        return _format_specific_workflow_display(result)
    elif continuation_type == "workflow_selection":
        return _format_workflow_selection_display(result)
    elif continuation_type == "no_interrupted_workflows":
        return _format_no_workflows_display(result)
```

#### Data Exchange Formats
- **Input**: Workflow continuation results with recovery analysis
- **Output**: Structured display data categorized by continuation type
- **Display Types**: recent_interrupted, specific_workflow, workflow_selection, no_workflows, error
- **Recovery Planning**: Detailed recovery information and readiness status

#### Terminal UI Rendering
```python
# Recent interrupted workflow display structure:
{
    "display_type": "recent_interrupted",
    "workflow_info": {
        "workflow_id": "abc123",
        "custom_command": "user-friendly-command",
        "workflow_goal": "Original user goal",
        "phases_completed": 3,
        "phases_total": 5
    },
    "recovery_info": {
        "ready_to_continue": True,
        "recovery_type": "resume_from_interruption",
        "current_phase": "Phase 4: Implementation",
        "estimated_time": "15 minutes",
        "recovery_actions": [...]
    },
    "action_buttons": {
        "primary": "Continue This Workflow",
        "secondary": "View All Interrupted Workflows"
    }
}
```

#### Configuration & State Sharing
- **Workflow Status Integration**: Connects with workflow status tracking
- **Recovery Planning**: Provides detailed recovery analysis
- **Progress Visualization**: Shows completion status and remaining work

## Written & Illustrated Data Info

### Data In-Flow
- **Workflow Discovery Results**: Available workflows for continuation
- **Recovery Analysis**: Workflow health and continuation readiness
- **Progress Status**: Current workflow state and completion information
- **User Context**: Authentication and workflow access permissions

### Data Out-Flow
- **Continuation Options**: Available workflows with recovery status
- **Progress Visualization**: Workflow completion and next steps
- **Recovery Guidance**: Specific instructions for workflow continuation
- **Selection Interface**: Multi-workflow selection when needed

### Integration Touchpoints
- **Workflow Manager Integration**: Receives workflow discovery results
- **Recovery System**: Analyzes workflow continuation readiness
- **Progress Tracking**: Shows workflow status and completion
- **Error Recovery**: Handles authentication and access issues

## Workflow Continuation Display Types

### Recent Interrupted Workflow
```python
def _format_recent_interrupted_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Most recent interrupted workflow with immediate continuation option"""
    return {
        "display_type": "recent_interrupted",
        "workflow_info": {
            "workflow_id": workflow.get("workflow_id"),
            "custom_command": workflow.get("custom_command"),
            "workflow_goal": workflow.get("workflow_goal"),
            "phases_completed": workflow_status.phases_completed,
            "phases_total": workflow_status.phases_total
        },
        "recovery_info": {
            "ready_to_continue": recovery_plan.get("ready_to_continue"),
            "recovery_type": recovery_plan.get("recovery_type"),
            "current_phase": recovery_plan.get("current_phase"),
            "estimated_time": recovery_plan.get("estimated_recovery_time")
        }
    }
```

### Workflow Selection Interface
```python
def _format_workflow_selection_display(result: Dict[str, Any]) -> Dict[str, Any]:
    """Multiple workflow selection with categorization"""
    return {
        "display_type": "workflow_selection",
        "workflow_categories": {
            "interrupted": {
                "title": "Interrupted Workflows",
                "description": "Workflows that were paused or interrupted",
                "workflows": _format_workflow_list(result.get("interrupted_workflows")),
                "priority": "high"
            },
            "active": {
                "title": "Active Workflows",
                "workflows": _format_workflow_list(result.get("active_workflows")),
                "priority": "medium"
            }
        },
        "display_options": {
            "show_interrupted_prominently": True,
            "group_by_recency": True,
            "enable_search": True
        }
    }
```

### Progress Calculation
```python
def _calculate_progress_percentage(workflow_status) -> int:
    """Calculate workflow completion percentage"""
    if not workflow_status or not workflow_status.phases_total:
        return 0
    
    return int((workflow_status.phases_completed / workflow_status.phases_total) * 100)
```

## Error Handling Patterns

### Authentication Errors
```python
if error_type == "authentication_required":
    display_data.update({
        "show_login_suggestion": True,
        "suggested_actions": [
            "Run 'mao --login' to authenticate",
            "Check user session status"
        ]
    })
```

### Workflow Not Found
```python
elif error_type == "workflow_not_found":
    display_data.update({
        "show_workflow_suggestions": True,
        "suggested_actions": result.get("suggestions", [])
    })
```

## Professional Software Architecture Notes
This component represents professional workflow management patterns:
- **State Machine Design**: Different display modes based on continuation context
- **Recovery Planning**: Sophisticated analysis of workflow continuation readiness
- **Progress Visualization**: Clear indication of workflow completion status
- **Error Context**: Specific error handling for workflow access and authentication
- **User Experience**: Prioritizes interrupted workflows and provides clear continuation paths

This is exactly how professional workflow management systems handle continuation - context-aware interfaces with detailed recovery planning and clear user guidance.