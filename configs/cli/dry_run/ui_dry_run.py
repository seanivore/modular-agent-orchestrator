"""
Dry Run CLI Command - UI Display Patterns
Provides essential data structure for workflow simulation display
"""

from typing import Dict, Any

def display_dry_run_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Organize dry run command results for UI display.
    
    Returns structured data for simulation results display.
    Focus: Essential data structure for simulation visualization.
    """
    if not result.get("success", True):
        return {
            "display_type": "error",
            "error_message": result.get("error", "Dry run simulation failed"),
            "suggestions": [
                "Check workflow configuration",
                "Verify workflow directory exists",
                "Try running with specific workflow target"
            ],
            "show_help_hint": True
        }
    
    simulation_type = result.get("simulation_type", "system_wide")
    simulation_results = result.get("simulation_results", {})
    
    if simulation_type == "specific_workflow":
        return _format_specific_workflow_display(result, simulation_results)
    else:
        return _format_system_wide_display(result, simulation_results)

def _format_specific_workflow_display(result: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    """Format display data for specific workflow simulation"""
    
    workflow_info = simulation.get("workflow_info", {})
    validation = simulation.get("validation", {})
    execution_plan = simulation.get("execution_plan", {})
    dependencies = simulation.get("dependencies", {})
    estimates = simulation.get("estimates", {})
    
    return {
        "display_type": "workflow_simulation",
        "header": {
            "title": "Workflow Simulation Results",
            "workflow_id": workflow_info.get("id", "Unknown"),
            "workflow_command": workflow_info.get("command", "Unknown"),
            "simulation_status": "completed"
        },
        "sections": [
            {
                "section_name": "workflow_overview",
                "title": "Workflow Overview",
                "data": {
                    "goal": workflow_info.get("goal", "No goal specified"),
                    "directory": workflow_info.get("directory", "No directory specified"),
                    "command": workflow_info.get("command", "No command specified")
                }
            },
            {
                "section_name": "validation_results",
                "title": "Validation Results",
                "status": validation.get("status", "unknown"),
                "data": {
                    "checks_performed": validation.get("checks_performed", []),
                    "warnings": validation.get("warnings", []),
                    "errors": validation.get("errors", [])
                }
            },
            {
                "section_name": "execution_plan",
                "title": "Execution Plan",
                "data": {
                    "phases": execution_plan.get("phases", []),
                    "estimated_total_time": execution_plan.get("estimated_total_time", "Unknown"),
                    "critical_path": execution_plan.get("critical_path", [])
                }
            },
            {
                "section_name": "dependencies",
                "title": "Dependency Check",
                "status": dependencies.get("dependency_status", "unknown"),
                "data": {
                    "system_deps": dependencies.get("system_dependencies", {}),
                    "workflow_deps": dependencies.get("workflow_dependencies", {}),
                    "external_deps": dependencies.get("external_dependencies", {})
                }
            },
            {
                "section_name": "estimates",
                "title": "Execution Estimates",
                "data": {
                    "time_estimates": estimates.get("time_estimates", {}),
                    "cost_estimates": estimates.get("cost_estimates", {}),
                    "resource_usage": estimates.get("resource_usage", {})
                }
            }
        ],
        "footer": {
            "simulation_complete": simulation.get("simulation_complete", False),
            "next_actions": [
                "Review validation warnings and errors",
                "Execute workflow with current configuration",
                "Modify workflow settings if needed"
            ]
        }
    }

def _format_system_wide_display(result: Dict[str, Any], simulation: Dict[str, Any]) -> Dict[str, Any]:
    """Format display data for system-wide simulation"""
    
    system_status = simulation.get("system_status", {})
    workflow_analysis = simulation.get("workflow_analysis", {})
    recommendations = simulation.get("simulation_recommendations", [])
    
    return {
        "display_type": "system_simulation",
        "header": {
            "title": "System Workflow Simulation",
            "available_workflows": result.get("available_workflows_count", 0),
            "simulation_status": "completed"
        },
        "sections": [
            {
                "section_name": "system_status",
                "title": "System Status",
                "data": {
                    "workflow_manager": system_status.get("workflow_manager_status", "unknown"),
                    "state_manager": system_status.get("state_manager_status", "unknown"),
                    "memory_mcp": system_status.get("memory_mcp_status", "unknown"),
                    "workflow_id_generation": system_status.get("workflow_id_generation", "unknown")
                }
            },
            {
                "section_name": "workflow_analysis",
                "title": "Workflow Analysis",
                "data": {
                    "total_workflows": workflow_analysis.get("total_workflows", 0),
                    "workflow_types": workflow_analysis.get("workflow_types", {}),
                    "recent_activity": workflow_analysis.get("recent_activity", {}),
                    "potential_issues": workflow_analysis.get("potential_issues", [])
                }
            },
            {
                "section_name": "recommendations",
                "title": "System Recommendations", 
                "data": {
                    "recommendations": recommendations,
                    "priority": "system_optimization"
                }
            }
        ],
        "footer": {
            "simulation_complete": simulation.get("simulation_complete", False),
            "next_actions": [
                "Address any identified system issues",
                "Create new workflows if needed",
                "Run system health check with 'mao doctor'"
            ]
        }
    }

def get_display_requirements() -> Dict[str, Any]:
    """
    Define essential display requirements for UI implementation.
    
    Returns what a UI designer would need to know.
    """
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
        "interaction_needs": [
            "expandable_sections_for_details",
            "copy_workflow_id_functionality", 
            "navigate_to_workflow_directory",
            "jump_to_related_commands"
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

def display_error(error_message: str) -> Dict[str, Any]:
    """Provide error display structure"""
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