# UI TypeScript Integration - ui_terminal.py

## Overview
Primary Python terminal interface that serves as the main subprocess coordination layer between Node.js terminal UI and Python backend. Handles CLI command routing, interactive mode, and standardized communication protocols for the LOCAL application architecture.

## Code & Explanation

### Architecture Overview
**Local Process Communication**: This is the PRIMARY Python interface that a Node.js terminal application would communicate with via subprocess calls. It implements:

- **Subprocess Management**: Designed to be called as a Python subprocess from Node.js terminal app
- **CLI Command Routing**: Routes all commands through standardized CLI manager system 
- **Interactive Mode**: Provides direct terminal interaction when run standalone
- **Error Handling**: Comprehensive error handling with structured responses for subprocess communication
- **Lazy Loading**: Optimized startup with lazy loading of orchestrator and CLI manager components

### Local Terminal Integration Requirements

#### Process Communication Patterns
```python
# Node.js would spawn this as subprocess:
# spawn('python3', ['interfaces/ui_terminal.py', '--interactive'])
# OR execute specific commands:
# spawn('python3', ['-c', 'from interfaces.ui_terminal import TerminalInterface; ...'])

class TerminalInterface:
    def execute_cli_command(self, command: str, input_data: Any = None) -> Dict[str, Any]:
        """Route CLI command through standardized CLI manager"""
        # Returns structured dict for easy JSON parsing by Node.js
        result = self.cli_manager.execute_command(command, input_data, source="app")
        return result  # JSON-serializable response
```

#### Data Exchange Formats
- **Input**: Command strings and JSON-serializable data objects
- **Output**: Structured dictionaries with success/error status and data
- **Error Handling**: Consistent error response format for subprocess communication
- **Configuration**: JSON-based settings shared via local filesystem

#### Terminal UI Rendering
```python
# Built-in terminal UI for standalone operation
def interactive(self):
    """Interactive mode with slash command support"""
    # Provides rich terminal interface when run directly
    # Could be extended/wrapped by Node.js terminal framework
    
def _handle_slash_command(self, command: str):
    """Handle commands through CLI manager"""
    # All commands routed through standardized CLI system
    # Node.js app could implement similar command routing
```

#### Configuration & State Sharing
```python
def _load_settings(self) -> Dict:
    """Load user settings with defaults"""
    settings_file = Path(self.config_dir) / "user_settings.json"
    # Local file system configuration sharing
    # Node.js app reads same configuration files
```

## Written & Illustrated Data Info

### Data In-Flow
- **Command Execution**: CLI commands from Node.js terminal app via subprocess calls
- **Configuration Updates**: Settings changes through local JSON files  
- **User Input**: Interactive mode input when running standalone
- **Orchestrator Requests**: High-level workflow requests through CLI manager

### Data Out-Flow
- **Command Results**: Structured JSON responses with success/error status
- **Terminal Output**: Formatted messages and status information
- **Error Messages**: Standardized error responses for UI display
- **Configuration Updates**: Updated settings written to local files

### Integration Touchpoints
- **Subprocess Interface**: Primary entry point for Node.js terminal app communication
- **CLI Manager Integration**: Routes all commands through standardized CLI system
- **Configuration Sharing**: Local filesystem configuration synchronization
- **Error Handling**: Comprehensive error handling with structured responses

## Local Terminal Integration Requirements

### Process Communication Documentation
```python
# Key methods for subprocess communication:
execute_cli_command(command, input_data) -> Dict  # Main subprocess interface
get_command_help(command) -> Dict                 # Help system integration
bootstrap_interface() -> TerminalInterface       # Initialization for subprocess
```

### Terminal Integration Guide
- **Node.js Integration**: Spawn Python subprocess with this interface
- **Command Routing**: All commands go through CLI manager for consistency
- **Configuration**: Shared local filesystem configuration management
- **Error Recovery**: Built-in error handling and recovery mechanisms

### Local Architecture Patterns
```python
# Lazy loading pattern for subprocess efficiency:
@property
def orchestrator(self):
    """Lazy load orchestrator to avoid import issues"""
    if self._orchestrator is None:
        from orchestrator.core import WorkflowOrchestrator
        self._orchestrator = WorkflowOrchestrator(self.config_dir)
    return self._orchestrator

# Cost estimation for budget planning:
@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(self, params: Dict[str, Any] = None) -> float:
    """Estimate interface operation cost for budget planning"""
```

## Dependencies
- orchestrator.cache.cache_system (CacheManager)
- orchestrator.error_handling (handle_errors, retry_with_backoff)
- orchestrator.core (WorkflowOrchestrator) - lazy loaded
- orchestrator.cli_manager (CLICommandsManager) - lazy loaded
- Standard Python libraries: json, sys, os, pathlib

## Professional Software Architecture Notes
This represents a clean separation of concerns in subprocess architecture:
- **Interface Layer**: Handles communication protocols and formatting
- **Routing Layer**: CLI manager provides standardized command processing  
- **Core Layer**: Orchestrator handles actual business logic
- **Configuration Layer**: Shared local filesystem state management

This is exactly how professional local applications handle Node.js ↔ Python communication - a dedicated interface layer that provides clean subprocess APIs while maintaining separation from core business logic.