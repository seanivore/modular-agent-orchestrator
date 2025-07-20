# UI TypeScript Integration - ui_dry_run.py

## Overview
Dry Run CLI command UI component that provides structured display patterns for workflow simulation display. Handles both specific workflow simulation and system-wide simulation with comprehensive validation and execution planning for the LOCAL application architecture.

## Code & Explanation

### Architecture Overview
**Workflow Simulation Interface**: Sophisticated UI component for workflow simulation and validation without execution.

- **Dual Simulation Modes**: Specific workflow simulation and system-wide analysis
- **Validation Results**: Comprehensive validation with warnings and errors
- **Execution Planning**: Detailed execution plans with time estimates
- **Dependency Analysis**: System, workflow, and external dependency checking

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
def display_dry_run_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Primary subprocess interface for dry run simulation results.
    Returns structured simulation data for Node.js terminal rendering.
    """
    simulation_type = result.get("simulation_type", "system_wide")
    simulation_results = result.get("simulation_results", {})
    
    if simulation_type == "specific_workflow":
        return _format_specific_workflow_display(result, simulation_results)
    else:
        return _format_system_wide_display(result, simulation_results)
```

#### Data Exchange Formats
- **Input**: Simulation results with validation and execution planning
- **Output**: Structured simulation data with sectioned information
- **Display Types**: workflow_simulation, system_simulation, error
- **Sectioned Data**: Overview, validation, execution plan, dependencies, estimates

#### Terminal UI Rendering
```python
# Specific workflow simulation structure:
{
    "display_type": "workflow_simulation",
    "header": {
        "title": "Workflow Simulation Results",
        "workflow_id": "abc123",
        "workflow_command": "user-command",
        "simulation_status": "completed"
    },
    "sections": [
        {
            "section_name": "workflow_overview",
            "title": "Workflow Overview",
            "data": {
                "goal": "Workflow goal description",
                "directory": "/path/to/workflow",
                "command": "custom-command"
            }
        },
        {
            "section_name": "validation_results",
            "title": "Validation Results", 
            "status": "passed",
            "data": {
                "checks_performed": [...],
                "warnings": [...],
                "errors": [...]
            }
        }
    ]
}
```

#### Configuration & State Sharing
- **Simulation State**: Comprehensive workflow and system validation
- **Execution Planning**: Detailed phase-by-phase execution analysis
- **Resource Estimation**: Time, cost, and resource usage projections

## Written & Illustrated Data Info

### Data In-Flow
- **Workflow Configurations**: Target workflow for simulation
- **System State**: Current system status and capabilities
- **Dependency Information**: System, workflow, and external dependencies
- **Resource Context**: Available system resources and constraints

### Data Out-Flow
- **Simulation Results**: Comprehensive validation and execution planning
- **Validation Status**: Detailed checks with warnings and errors
- **Execution Timeline**: Phase-by-phase execution planning
- **Resource Estimates**: Time, cost, and resource usage projections

### Integration Touchpoints
- **Workflow Validation System**: Comprehensive workflow configuration checking
- **Dependency Manager**: System and external dependency analysis
- **Execution Planner**: Detailed execution phase planning
- **Resource Estimation**: Cost and time projection systems

## Simulation Display Types

### Specific Workflow Simulation
```python
def _format_specific_workflow_display(result: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    """Detailed workflow simulation with comprehensive analysis"""
    return {
        "display_type": "workflow_simulation",
        "sections": [
            {
                "section_name": "workflow_overview",
                "data": {
                    "goal": workflow_info.get("goal"),
                    "directory": workflow_info.get("directory"),
                    "command": workflow_info.get("command")
                }
            },
            {
                "section_name": "validation_results",
                "status": validation.get("status"),
                "data": {
                    "checks_performed": validation.get("checks_performed", []),
                    "warnings": validation.get("warnings", []),
                    "errors": validation.get("errors", [])
                }
            },
            {
                "section_name": "execution_plan",
                "data": {
                    "phases": execution_plan.get("phases", []),
                    "estimated_total_time": execution_plan.get("estimated_total_time"),
                    "critical_path": execution_plan.get("critical_path", [])
                }
            }
        ]
    }
```

### System-Wide Simulation
```python
def _format_system_wide_display(result: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    """System-wide workflow analysis and recommendations"""
    return {
        "display_type": "system_simulation",
        "sections": [
            {
                "section_name": "system_status",
                "data": {
                    "workflow_manager": system_status.get("workflow_manager_status"),
                    "state_manager": system_status.get("state_manager_status"),
                    "memory_mcp": system_status.get("memory_mcp_status"),
                    "workflow_id_generation": system_status.get("workflow_id_generation")
                }
            },
            {
                "section_name": "workflow_analysis",
                "data": {
                    "total_workflows": workflow_analysis.get("total_workflows", 0),
                    "workflow_types": workflow_analysis.get("workflow_types", {}),
                    "recent_activity": workflow_analysis.get("recent_activity", {}),
                    "potential_issues": workflow_analysis.get("potential_issues", [])
                }
            }
        ]
    }
```

## Display Requirements System

### UI Implementation Guidance
```python
def get_display_requirements() -> Dict[str, Any]:
    """Comprehensive display requirements for Node.js implementation"""
    return {
        "layout_pattern": "simulation_results",
        "essential_elements": [
            "status_header_with_workflow_info",
            "tabbed_or_sectioned_results_display",
            "validation_status_indicators",
            "execution_plan_timeline_view",
            "dependency_status_grid",
            "estimates_summary_panel"
        ],
        "display_priorities": [
            "validation_status_prominence",
            "error_and_warning_visibility",
            "execution_plan_clarity",
            "cost_and_time_estimates",
            "system_status_overview"
        ],
        "status_indicators": {
            "validation_passed": "clear_success_indication",
            "validation_warnings": "attention_highlighting",
            "validation_failed": "error_state_display",
            "simulation_complete": "completion_confirmation"
        },
        "data_visualization": {
            "execution_phases": "timeline_or_step_display",
            "dependency_status": "grid_or_list_with_status_icons",
            "estimates": "summary_cards_or_panels",
            "system_status": "dashboard_style_overview"
        }
    }
```

## Error Handling and Validation

### Comprehensive Error Display
```python
def display_error(error_message: str) -> Dict[str, Any]:
    """Structured error display with troubleshooting guidance"""
    return {
        "display_type": "error",
        "error_message": error_message,
        "suggestions": [
            "Check that workflow directory exists",
            "Verify workflow configuration files",
            "Try specifying a specific workflow to simulate",
            "Run 'mao workflows' to see available workflows"
        ],
        "related_commands": [
            "mao workflows - List available workflows",
            "mao doctor - System health check", 
            "mao help - Command help"
        ],
        "show_help_hint": True
    }
```

## Professional Software Architecture Notes
This component represents professional simulation and validation patterns:
- **Pre-execution Validation**: Comprehensive checking before workflow execution
- **Resource Planning**: Detailed cost and time estimation for informed decisions
- **Dependency Analysis**: Thorough system, workflow, and external dependency checking
- **Visual Organization**: Sectioned display for complex simulation results
- **Error Prevention**: Proactive identification of potential execution issues

This is exactly how professional workflow management systems handle simulation - comprehensive validation, detailed planning, and clear visualization of execution readiness before committing resources.