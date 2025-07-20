# Core System Architecture - Batch 01: Root Files

## File: ./mao_v4.py - Main application entry point and system initialization

### Simple Sentence Form:

**Overview:** 
The `mao_v4.py` file serves as the main CLI entry point for the Mao system, implementing pure dynamic routing with zero hardcoded arguments by discovering all commands from JSON configuration files. It bootstraps the entire system including the terminal interface and MCP (Memory Control Protocol) hub initialization, providing flexible command dispatch to various interface methods based on user input.

### Code & Explanation:

**Architecture Overview:**
- **Core application initialization patterns and entry point design**: Uses a modular bootstrap pattern where the main entry point (`main()`) dynamically loads all CLI commands from JSON config files in `configs/cli/` directory. The system avoids hardcoded command definitions, instead using JSON-driven configuration discovery via `load_all_commands()` function.

- **System bootstrapping procedures and dependency initialization**: The `bootstrap_interface()` function implements error-resistant initialization, first importing the `TerminalInterface`, then creating and attaching an MCP hub via `create_mcp_hub()`. This ensures proper initialization order and provides the interface with access to the MCP system for state management.

- **Main execution flow and system lifecycle management**: The entry point follows a clear flow: 1) Handle special case 'mao mao' command for smart launch, 2) Load all command configurations dynamically, 3) Create argument parser from configurations, 4) Bootstrap interface and MCP hub, 5) Route commands to appropriate interface methods based on JSON configuration, 6) Graceful error handling and user feedback.

- **Recommended documentation location for architecture diagrams**: System initialization flow diagrams should be documented in `/documentation/ARCHITECTURE/` showing the bootstrap sequence, MCP hub initialization, and command routing patterns.

### Written & Illustrated Data Info.:

**Data In-Flow:**
- **System startup sequences and initialization parameters**: The system accepts command-line arguments dynamically parsed from JSON configurations. Special handling for 'mao mao' command triggers smart launch mode. All CLI commands are discovered from `configs/cli/*.json` files during startup.

- **Configuration loading and validation patterns**: Command configurations are loaded via `load_all_commands()` which scans for `.json` files, skips `.OLD` files, and gracefully handles malformed JSON with try-catch blocks. Each configuration must contain `command`, `terminal_flag`, `type`, and `interface_method` fields.

- **External dependency connections and verification**: The system imports and initializes the TerminalInterface and MCP hub during bootstrap. Error handling ensures graceful degradation if imports fail, with specific error messages for bootstrap failures.

**Data Out-Flow:**
- **System state propagation to subsystems**: The initialized MCP hub is attached to the terminal interface (`interface.mcp_hub = mcp_hub`) enabling state sharing between system components. Command routing passes execution control to specific interface methods based on command type.

- **Logging and monitoring data flows**: Uses standard Python logging with logger instance. Error handling decorators (`@handle_errors`) provide structured error reporting. Cost estimation function (`estimate_cost()`) provides budget planning data for system operations.

- **Error handling and shutdown procedures**: Implements keyboard interrupt handling for graceful shutdown. AttributeError handling for missing interface methods with user-friendly error messages. Exception handling with error propagation to the interface error system.

### Dependencies:
- None (foundation files)

**Key Architectural Patterns Identified:**
1. **Pure Dynamic Routing**: Zero hardcoded commands, all discovered from JSON configs
2. **Modular Bootstrap**: Interface and MCP hub initialization with error recovery
3. **JSON-Driven Configuration**: Command definitions stored as discoverable JSON files
4. **Error-Resistant Initialization**: Graceful handling of import and configuration errors
5. **Cost Estimation Integration**: Built-in budget planning for system operations