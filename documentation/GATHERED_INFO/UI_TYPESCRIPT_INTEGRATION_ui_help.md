# UI TypeScript Integration - ui_help.py

## Overview
Help CLI command UI component that provides Git-style command categorization and structured help display. Organizes commands into logical categories and provides comprehensive usage guidance for the LOCAL application terminal interface.

## Code & Explanation

### Architecture Overview
**Git-Style Command Grouping**: Follows professional CLI conventions with categorized command organization.

- **Category-Based Organization**: Commands grouped into BASICS, CREATION, CONFIGURATION, INFORMATION, OPERATIONS
- **Dual Usage Display**: Shows both terminal flags and in-app commands
- **Structured Data Return**: JSON-serializable help data for Node.js consumption
- **Cache Integration**: Uses CacheManager for performance optimization

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
def display_help_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Primary subprocess interface for help system.
    Returns categorized command structure for Node.js rendering.
    """
    categorized_commands = result.get("categorized_commands", {})
    
    display_data = {
        "display_type": "help_categories",
        "header": {
            "title": "Mao - Modular Agent Orchestrator",
            "subtitle": "These are common Mao commands used in various situations:"
        },
        "categories": [...],  # Structured category data
        "footer": {
            "total_commands": result.get("total_commands", 0),
            "show_tutorial_hint": True
        }
    }
```

#### Data Exchange Formats
- **Input**: Categorized command data from CLI discovery system
- **Output**: Git-style help layout with command categories
- **Category Structure**: Predefined categories with consistent ordering
- **Command Details**: Name, usage patterns, descriptions, and types

#### Terminal UI Rendering
```python
# Category display structure for Node.js terminal rendering:
category_display = {
    "category_name": "BASICS",
    "title": "getting started",
    "description": "(see also: mao help tutorial)",
    "commands": [
        {
            "name": "help",
            "terminal_usage": "--help",
            "app_usage": "/help",
            "description": "Show this help message",
            "type": "core"
        }
    ]
}
```

#### Configuration & State Sharing
- **Command Discovery**: Dynamically discovers available commands
- **Category Definitions**: Structured category metadata and descriptions
- **Usage Patterns**: Dual display for terminal and in-app usage

## Written & Illustrated Data Info

### Data In-Flow
- **CLI Command Registry**: Discovered commands from CLI directory scanning
- **Command Metadata**: Help text, usage patterns, and categorization
- **System State**: Available commands based on current configuration
- **Category Configuration**: Predefined category structure and ordering

### Data Out-Flow
- **Categorized Help Display**: Git-style organized command listing
- **Usage Examples**: Both terminal flags and in-app command formats
- **Navigation Hints**: References to related help topics
- **Command Count Statistics**: Total available commands information

### Integration Touchpoints
- **CLI Discovery System**: Receives discovered command information
- **Help Topic Cross-References**: Links to related help sections
- **Command Execution**: Provides usage patterns for other commands
- **Category Management**: Maintains consistent command organization

## Help System Categories

### Command Organization Structure
```python
category_info = {
    "BASICS": {
        "title": "getting started",
        "description": "(see also: mao help tutorial)"
    },
    "CREATION": {
        "title": "workflow creation", 
        "description": "(see also: mao help workflows)"
    },
    "CONFIGURATION": {
        "title": "user and session management",
        "description": "(see also: mao help config)"
    },
    "INFORMATION": {
        "title": "system information",
        "description": "(see also: mao help stats)"
    },
    "OPERATIONS": {
        "title": "workflow operations",
        "description": "(see also: mao help advanced)"
    }
}
```

### Display Requirements
```python
def get_display_requirements() -> Dict[str, Any]:
    return {
        "layout_pattern": "git_style_grouping",
        "grouping_requirements": {
            "category_headers": "lowercase with optional description",
            "command_alignment": "consistent spacing for readability",
            "description_alignment": "right-aligned or tabbed",
            "visual_hierarchy": "clear separation between categories"
        },
        "content_priorities": [
            "command_name_visibility",
            "description_clarity", 
            "category_organization",
            "usage_format_consistency"
        ]
    }
```

## Professional Software Architecture Notes
This component represents professional CLI help system design:
- **Git Convention Compliance**: Follows established CLI help patterns
- **Category-Based Organization**: Logical grouping for user navigation
- **Dual Usage Support**: Both terminal and in-app command formats
- **Extensible Structure**: Easy to add new commands and categories
- **Cross-Reference System**: Links to related help topics and tutorials

This is exactly how professional CLI tools organize help systems - category-based organization with consistent formatting and comprehensive cross-references.