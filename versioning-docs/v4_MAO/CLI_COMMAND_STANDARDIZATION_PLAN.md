# Task #5 CLI Commands Integration, Standardization, & Implementation Plan

**COMPREHENSIVE IMPLEMENTATION GUIDE**
*Consolidates previous partial plans into complete standardization strategy*

1. Deletegate one command at a time to batches of sub agents. 
2. Have them return a requirements analysis (example: `./versioning-docs/v4_MAO/CLI_COMMAND_NOTES/help.md`, `./versioning-docs/v4_MAO/CLI_COMMAND_NOTES/models.md`, `./versioning-docs/v4_MAO/CLI_COMMAND_NOTES/tools.md`). 
3. Review the requirement analysis; with approval they may begin implementation. 
4. Have them return a detailed report on the completed implementation. 
5. Review the report; with approval they may conduct an audit of all files: touchpoints, new files, etc. 
6. Have them report, for each file, what is good and what is bad; then implement fixes using the `MAO_FILE_STANDARDIZATION_RULES.md` file. 
7. Have them return a final report on the completed implementation. 
8. Upon receiving the final report and approval, have them start on the next command. 
9. Repeat the process until all commands are implemented. 

---

## Implementation Scope

**Current State**: CLI Manager infrastructure complete, JSON configs exist 
**Missing**: Individual .py logic files + UI files for each command  
**Goal**: Complete 3-file structure for all 23 commands with full MAO standardization

**CRITICAL UI IMPLEMENTATION PHILOSOPHY:**

UI files should provide only essential information for future UI development, NOT detailed interface implementation. The goal is to minimize design constraints and maximize creative freedom for the actual UI development phase.

**Why This Matters:**
- Original UI files contained excessive emoji and overly detailed interface specifications
- When Claude Code builds the actual UI, it needs to "translate" from these files to professional application design
- Less purging = better creative accuracy in final UI implementation
- UI files should focus on data structure and essential display requirements only

---

## 3-File Structure Per Command

```
configs/cli/[command]/
├── [command].py          ← Logic file with full MAO standardization  
├── [command].json        ← Enhanced config (already exists)
└── ui_[command].py       ← UI file for command display patterns
```

---

## CLI Reference Chart With Grouping and Ordering 

Please check the chart below for the CLI commands and their corresponding terminal and in-app commands in their most accurate form. If there is a discrepancy between a JSON file, etc. and the chart, please use the chart and update the files. 

| **FUNCTION**             | **TERMINAL COMMAND**                   | **IN-APP COMMAND**                |
| ------------------------ | -------------------------------------- | --------------------------------- |
| *~BASICS~*               | -                                      | -                                 |
| **Start Application**    | `mao mao`                              | -                                 |
| **Run Your Workflow**    | `custom command`                       | `/custom command`                 |
| View these help messages | `mao --help`                           | `/help`                           |
| *~CREATION~*             | -                                      | -                                 |
| Resume last workflow     | `mao --continue`                       | `/continue`                       |
| Build workflow from JSON | `mao --setup ./config.json`            | `/setup ./config.json`            |
| Update workflow via JSON | `mao --update ./phase.json`            | `/update ./phase.json`            |
| Fix deliverable via JSON | `mao --fix-it ./fix.json`              | `/fix-it ./fix.json`              |
| Create entire workflow   | `mao --goal project goal`              | `/goal project goal`              |
| First message to AI      | `mao --chat message`                   | `/chat message`                   |
| *~PERSONALIZATION~*      | -                                      | -                                 |
| Application setup        | `mao --config`                         | `/config`                         |
| Set output directory     | `mao --output ~/downloads`             | `/output ~/downloads`             |
| Set favorite model       | `mao --set-model model-name`           | `/set-model model-name`           |
| Set default provider     | `mao --default-provider provider-name` | `/default-provider provider-name` |
| *~RESOURCES~*            | -                                      | -                                 |
| List workflow variables  | `mao --variables`                      | `/variables`                      |
| Explain variables        | `mao --variables-explain`              | `/variables-explain`              |
| List tools               | `mao --tools`                          | `/tools`                          |
| List models              | `mao --models`                         | `/models`                         |
| List providers           | `mao --providers`                      | `/providers`                      |
| *~WORKFLOWS~*            | -                                      | -                                 |
| List Workflows           | `mao --workflows`                      | `/workflows`                      |
| Review a workflow        | `mao --review custom command`          | `/review custom command`          |
| System Statistics        | `mao --stats`                          | `/stats`                          |
| View workflow logs       | `mao --logs`                           | `/logs`                           |
| *~APPLICATION~*          | -                                      | -                                 |
| Start as new user        | `mao`                                  | -                                 |
| Login Username           | `mao --login`                          | `/login`                          |
| Logout Username          | `mao --logout`                         | `/logout`                         |
| Restart application      | -                                      | `/restart` or `! mao restart`     |
| Exit application         | -                                      | `/exit` or `! mao exit`           |
| Create Workflow ID       | `uid`                                  | `/uid` or `! uid`                 |
| Create User ID           | `meid username`                        | `/meid username`                  |
| *~TROUBLESHOOTING~*      | -                                      | -                                 |
| Start verbose debug mode | `mao --verbose`                        | `/verbose`                        |
| Check system health      | `mao --doctor`                         | `/doctor`                         |
| Simulate a workflow      | `mao --dry-run`                        | `/dry-run`                        |
| Run any terminal command | -                                      | `! ls -la` (any bash/zsh)         |

---

## Data Display, No Complex Logic Commands (6) 

### 1. `mao --help` and `/help` --> ✅
- Pull simple, one-line command details from the `./configs/cli/` directory, and then display them in the UI with helpful git-style grouping. 

### 2. `mao tools` and `/tools` --> ✅
- Pull description and new 'display-name' from tool's JSON file to display in the UI; consider display order and grouping for UX. 

### 3. `mao models` and `/models` --> ✅ 
- Pull notes and model's 'display-name' from model's JSON file in the `./configs/models/` directory to display with helpful UX in UI. 

### 4. `mao providers` and `/providers` --> ✅
- Pull notes and provider's 'display-name' from provider's JSON file in the `./configs/providers/` directory to display with helpful UX in UI. 

### 5. `mao workflows` and `/workflows`
- List workflows, integrate with `/review` command UX; provide easy access to `/logs`, `/stats`; users can search by custom command to search workflow JSON files; can use User ID, Username, or Workflow ID if they have. 

### 6. `mao stats` and `/stats`
- System performance metrics via `real_time_metrics.py` including SystemMetricsProvider, WorkflowMonitor, CostTracker; when implementing this, also implement "Task #5 PHASE 3: Confirm 'Orchestrator Integration' for 'Real-Time Features'" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md` including "Re: **Add real cost tracking and progress monitoring**" and "Re: **Confirm stats ready to connect to actual system metrics**". Should be easy to build out to search for larger metrics using User ID, Workflow ID, Model ID, and Provider ID, etc. as detailed in `./versioning-docs/v4_MAO/DATA_COLLECTION_ARCHITECTURE.md`

---

## Basic Operations, Manager Integration Commands (7)

### 7. `mao config` and `/config`
- Application settings via `settings_manager.py` should be primarily implemented; settings changes auto-update the user config JSON file via their User ID/Username. 

### 8. `mao login` and `/login`
- User authentication via `username_manager.py`; see `NEW_USER_FLOW.md` for more details. 

### 9. `mao logout` and `/logout`
- User session management via `username_manager.py`; see `NEW_USER_FLOW.md` for more details. 

### 10. `mao user_id` and `/user_id`
- Display/generate user ID via `username_manager.py` as part of `NEW_USER_FLOW.md`. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 11. `mao workflow_id` and `/workflow_id`
- Generate workflow ID via `workflow_manager.py` as part of workflow setup flow. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 12. `mao variables` and `/variables`
- Simple UI list of variables needed to setup a workflow, filling out the workflow use-case JSON object. Workflow template `./configs/examples/workflow_templates/README.md`. Includes a `variables-explain` flag.

### 13. User settings set favorite `mao set-model model-name` and `/set-model model-name`, default `mao default-provider provider-name` and `/default-provider provider-name`, or output directory `mao output path/to/location/` and `/output path/to/location/`
- User config JSON updates via `settings_manager.py`, similar to `/config` but to set specific user config values quickly. 

---

## Workflow Operations, File Processing Commands (10) 

### 14. `mao goal` and `/goal`
- Create workflow from single message; when completing this, also implement "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `FINAL_IMPLEMENTATION_DETAILS.md` for the section "Connect `goal()` method to real `WorkflowOrchestrator`". 

### 15. `mao setup` and `/setup`
- Already implemented, needs standardization audit and make sure it has multi-path support; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py` 

### 16. `mao update` and `/update`
- Already implemented but needs updating to accomodate with multi-path support + secondary flags (-add, -remove, -replace, -rename, -chat), plus update of the workflow JSON object in the appropriate directory if the path provided wasn't the workflow's directory; so that it can be run from any directory; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 17. `mao fix_it` and `/fix_it`
- Already implemented but needs additional logic for workflow correction with automatic JSON copying logic if the JSON object wasn't executed from the workflow's directory; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 18. `mao continue` and `/continue`
- Workflow state management to jump back into an interrupted workflow; when completing this, also implement "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `FINAL_IMPLEMENTATION_DETAILS.md` for the section "Workflow state management for `continue/review`" via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 19. `mao review` and `/review`
- Workflow state management to review and search workflows; when completing this, also implement "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `FINAL_IMPLEMENTATION_DETAILS.md` for the section "Workflow state management for `continue/review`" via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 20. `mao chat` and `/chat`
- Jump to main app with message passthrough via `conversation_bridge.py`

### 21. `mao doctor` and `/doctor`
- System health checks and workflow diagnostics; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 22. `mao dry_run` and `/dry_run`
- Workflow simulation mode; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 23. `mao verbose` and `/verbose`
- Verbose mode is already written, just needs a debug mode toggle added to, via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

### 24. `mao logs` and `/logs`
- Workflow log viewing; relates to stats/review/workflows; via `workflow_manager.py`, `workflow_state.py`, `memory_mcp.py`

---

## Systematic Implementation Process

**DO ONE COMMAND AT A TIME, THEN AUDIT THAT COMMAND**

### Phase 1: Planning (Per Command)
1. **Next command** 
2. **Sequential think requirements**
   - What functionality does this CLI command provide?
   - Which orchestrator files need integration?
   - What manager methods will be called?
   - What UI patterns are needed for display?
   - Cost estimation approach (Claude Sonnet 4 costs)
   - Caching strategy and fingerprinting needs

### Phase 2: Implementation 
3. **Detail implementation plan** to Sean
4. **Create 3 files**:
   - `[command].py` - Logic with full MAO standardization
   - `ui_[command].py` - Display patterns for command output
   - Update `[command].json` if needed (cost_estimate, etc.)
5. **Update integration touchpoints** 
6. **Report implementation results** 

### Phase 3: Quality Control
7. **Sequential thinking + full audit** using `MAO_FILE_STANDARDIZATION_RULES.md`:
   - Standard MAO imports ✓
   - CacheManager integration ✓  
   - estimate_cost() function ✓
   - @handle_errors decorators ✓
   - Fingerprinting patterns ✓
   - UI consistency patterns ✓
8. **Fix any standardization violations**
9. **Report of fixes**
10. **Move to next command**

---

## File Templates & Patterns

### Logic File Template
```python
# configs/cli/[command]/[command].py
"""
[Command] CLI Command - Core Logic
[Brief description of command functionality]
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="[command]", return_dict=True)
def execute_[command](params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result with appropriate duration
    cache.set(cache_key, result, duration=300)  # 5 minutes default
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Read from JSON config or calculate based on complexity
    return 0.001  # Default low cost for CLI commands

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including system state"""
    base_key = f"[command]|{str(params) if params else 'none'}"
    
    # Add system state fingerprints for commands that depend on files
    # Example: Include directory modification times, file counts, etc.
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core command logic implementation"""
    # Command-specific implementation here
    pass

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_[command](params)
```

### UI File Template
```python
# configs/cli/[command]/ui_[command].py
"""
[Command] CLI Command - UI Display Patterns
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any

# Module-level console for consistency
console = Console()

def display_[command]_result(result: Dict[str, Any]) -> None:
    """
    Display command results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Essential data display requirements only
    # Provide data structure and display priorities
    # Avoid detailed interface specifications - leave creative freedom for UI development
    
    pass

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="Command Error"
    ))
```

### Enhanced JSON Config
```json
{
  "command": "[command]",
  "type": "standalone",
  "terminal_flag": "--[command]",
  "app_command": "/[command]",
  "interface_method": "[command]", 
  "help": "Brief description for help display",
  "cost_estimate": 0.001,
  "logic_file": "configs/cli/[command]/[command].py",
  "ui_file": "configs/cli/[command]/ui_[command].py",
  "operations": {
    "execute": {
      "description": "Main command operation",
      "required_params": [],
      "optional_params": []
    }
  },
  "integration": {
    "memory_mcp": true,
    "cache_system": true,
    "error_handling": true,
    "manager_touchpoints": ["username_manager", "workflow_manager"]
  },
  "cache_settings": {
    "enabled": true,
    "duration_seconds": 300,
    "cache_key_includes": ["system_state", "user_context"]
  }
}
```

---

## Integration Touchpoints

### Manager Integration Map
```
Universal Touchpoints: ALL commands → cli_manager.py (routing), ui_terminal.py (slash commands)
User Management: login, logout, user_id → username_manager.py
Settings: config, model, provider, output → settings_manager.py  
Workflows: goal, workflows, workflow_id → workflow_manager.py
System Info: stats, list_tools → real_time_metrics.py, manager_tools.py
Models/Providers: model_list, provider_list → manager_models.py
Workflow Operations: setup, update, fix_it → workflow_manager.py, workflow_state.py, memory_mcp.py
```

### Full Orchestrator File List
```
orchestrator/agent_callback.py - "Handles agent returns, execution results, and workflow progression"
orchestrator/agent_orchestrator.py - "Coordinates agent handoffs with context packages via Files API"
orchestrator/cli_manager.py - "Dynamic CLI command discovery and interface integration"
orchestrator/conversation_bridge.py - "Converts natural language goals into executable custom commands"
orchestrator/core.py - "The main brain that turns natural language into intelligent workflows"
orchestrator/error_handling.py - "Professional error handling patterns for all tools"
orchestrator/manager_buttons.py - "Creates executable code snippets for any model/provider combo"
orchestrator/manager_models.py - "Loads JSON configs and provides intelligent model selection"
orchestrator/manager_tools.py - "Dynamic tool suggestion based on goals, not hardcoded categories"
orchestrator/mcp_hub.py - "Integrates Memory MCP, Files API, and MCP Connector into unified system"
orchestrator/memory_mcp.py - "Provides workflow context tracking, state management, and session recovery"
orchestrator/real_time_metrics.py - "Provides live data for UI components; no mock data allowed"
orchestrator/settings_manager.py - "Dynamic settings discovery and management using directory-based scanning"
orchestrator/username_manager.py - "Handles user creation, session persistence, and settings integration"
orchestrator/workflow_manager.py - "Handles workflow ID generation, discovery, and tracking"
orchestrator/workflow_state.py - "Simple state tracking with Memory MCP integration"
```

---

## UI Design Considerations

### Git-Style Command Grouping
```bash
mao --help
Mao - Modular Agent Orchestrator

These are common Mao commands used in various situations:

start working (see also: mao help tutorial)  
   login      Authenticate user and start session
   config     Configure application settings
   
manage workflows (see also: mao help workflows)
   goal       Create entire workflow from goal description
   setup      Set up workflow from prepared JSON configs
   workflows  List existing workflows
   
system information
   stats      Show system performance and orchestrator statistics  
   list-tools List all available tools
   help       View these help messages
```

### Tool Display Name Implementation
Add to each `tool_*.json`:
```json
{
  "name": "brave_search",
  "display_name": "Brave Search",
  "description": "Privacy-focused web search capabilities"
}
```

---

## Success Criteria

**Per Command Implementation:**
- [ ] Logic file follows MAO standardization exactly
- [ ] UI file provides consistent display patterns  
- [ ] JSON config enhanced with required fields
- [ ] Caching with intelligent fingerprinting
- [ ] Integration touchpoints properly connected
- [ ] Cost estimation accurate for Sonnet 4
- [ ] Error handling comprehensive
- [ ] Audit checklist 100% compliant

**Overall Project Success:**
- [ ] All 23 commands implemented with 3-file structure
- [ ] CLI Manager routing updated for all commands
- [ ] Shared UI patterns established
- [ ] No hardcoded command references anywhere
- [ ] Complete integration with Tasks 1-4 systems
- [ ] Documentation consolidated into single plan

---

*This comprehensive plan provides everything needed for systematic CLI command implementation with full MAO standardization compliance.*

---

