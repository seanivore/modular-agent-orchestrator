# CLI Manager - Clean Implementation Documentation

## Overview

The CLI Manager provides dynamic command discovery and execution for MAO's command-line interface. This implementation follows MAO principles of true modularity, no hardcoded categories, and cultural adaptability.

## Core Architecture

The CLI Manager works by scanning JSON configuration files to discover available commands, then dynamically loading and executing the corresponding Python modules. This approach eliminates hardcoded command mappings and allows for truly plug-and-play command integration.

### Dynamic Discovery Process

Commands are discovered by scanning the `configs/cli/` directory for JSON configuration files. Each command defines its own metadata including file paths, help text, and caching preferences. The system makes no assumptions about command categories or predetermined workflow patterns.

### Modular Execution Pattern

Command execution follows a simple pattern: discover available commands from JSON configs, validate the command exists, load the corresponding Python module dynamically, and execute the appropriate function (execute_command, execute, or main).

## Key Methods

### `discover_cli_commands()`

Scans the CLI directory structure for command JSON files and builds a registry of available commands. Uses MAO's standard caching pattern to avoid repeated file system operations. The discovery process is completely dynamic - no hardcoded command lists or categories.

### `execute_command()`

Executes commands by loading their Python modules dynamically based on the file_path specified in the JSON configuration. Supports intelligent caching based on command-specific cache_duration settings. Returns standardized response format with success status, results, and timing information.

### `_execute_command_dynamically()`

The core execution method that handles dynamic module loading. Converts relative paths to absolute paths, loads Python modules using importlib, and looks for standard execution functions. Provides detailed error reporting when commands fail to load or execute.

### Caching System

Implements simple, configurable caching where individual commands specify their own cache duration in seconds. Commands with cache_duration of 0 or undefined are not cached. Cache keys are generated based on command name and input parameters without hardcoded command categories.

## AI Behavioral Guidance

### Cultural Adaptability

The system makes no assumptions about command naming conventions, workflow patterns, or cultural approaches to problem-solving. Commands can be named in any language and follow any cultural workflow pattern.

### Trust-Based Execution

The system trusts Claude's intelligence to determine optimal command execution patterns. No predetermined categories or suggestions are provided - the AI analyzes the command's purpose and executes accordingly.

### Error Handling Philosophy

Errors are communicated clearly without predetermined suggestions. The system provides available options (like discovered functions in a module) but doesn't force specific paths or workflows.

## MAO Standardization Compliance

### Required Functions
- `estimate_cost()` - Reads cost estimates from command JSON configurations
- Standard error handling with @handle_errors decorators
- CacheManager integration following MAO patterns

### Standalone Functions
- `discover_cli_commands()` - For button imports
- `execute_command()` - For external integrations
- `get_command_help()` - For help system integration
- `estimate_cost()` - For budget planning

### JSON Configuration Format

Commands follow the MAO 3-file structure:
```json
{
    "name": "command_name",
    "help": "Command description", 
    "file_path": "configs/cli/command_name/command_name.py",
    "ui_path": "configs/cli/command_name/ui_command_name.py",
    "cache_duration": 300,
    "cost_estimate": 0.001
}
```

## Implementation Simplicity

The clean implementation is approximately 350 lines compared to the original 966 lines. This reduction was achieved by:

1. **Removing Hardcoded Categories**: Eliminated 200+ lines of predetermined command mappings
2. **Dynamic Loading**: Replaced specific method handlers with generic module loading
3. **Simplified Caching**: Removed complex system state fingerprinting for simple duration-based caching
4. **Eliminated Placeholders**: Removed placeholder methods that provided no actual functionality

## Security Considerations

Commands are loaded from the `configs/cli/` directory structure with validation that file paths exist before execution. The system uses standard Python importlib for module loading, which follows Python's security model for code execution.

## Future Extensibility

New commands can be added by simply creating the 3-file structure (command.py, ui_command.py, command.json) in the appropriate directory. No code changes to the CLI Manager are required. This enables true plug-and-play extensibility while maintaining security and performance.

## Performance Characteristics

The system provides efficient operation through:
- Discovery caching to minimize file system operations
- Command-specific result caching based on JSON configurations
- Dynamic imports only when commands are executed
- Standard MAO error handling patterns for reliability

This implementation demonstrates how following MAO principles creates simpler, more maintainable, and culturally adaptable code while preserving all essential functionality.