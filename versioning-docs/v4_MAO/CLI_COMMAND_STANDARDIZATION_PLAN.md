# Task #5 CLI Commands Integration, Standardization, & Implementation Plan

**COMPREHENSIVE IMPLEMENTATION GUIDE**
*Consolidates previous partial plans into complete standardization strategy*

---

## Implementation Scope: 23 CLI Commands

**Current State**: CLI Manager infrastructure complete, JSON configs exist 
**Missing**: Individual .py logic files + UI files for each command  
**Goal**: Complete 3-file structure for all 23 commands with full MAO standardization

---

## 3-File Structure Per Command

```
configs/cli/[command]/
├── [command].py          ← Logic file with full MAO standardization  
├── [command].json        ← Enhanced config (already exists)
└── ui_[command].py       ← UI file for command display patterns
```

---

## Data Display, No Complex Logic Commands (6) 

### 1. `mao --help` and `/help` 
- Pull simple, one-line command details from the `./configs/cli/` directory, and then display them in the UI with helpful git-style grouping. 

### 2. `mao tools` and `/tools`
- Pull description and new 'display-name' from tool's JSON file to display in the UI; consider display order and grouping for UX. 

### 3. `mao models` and `/models`
- Pull notes and model's 'display-name' from model's JSON file in the `./configs/models/` directory to display with helpful UX in UI. 

### 4. `mao providers` and `/providers`
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
- User authentication via `username_manager.py`; see `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` for more details. 

### 9. `mao logout` and `/logout`
- User session management via `username_manager.py`; see `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` for more details. 

### 10. `mao user_id` and `/user_id`
- Display/generate user ID via `username_manager.py` as part of `NEW_USER_FLOW.md`. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 11. `mao workflow_id` and `/workflow_id`
- Generate workflow ID via `workflow_manager.py` as part of workflow setup flow. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 12. `mao variables` and `/variables`
- Simple UI list of variables needed to setup a workflow, filling out the workflow use-case JSON object. Workflow template `./configs/examples/workflow_templates/README.md`. Includes a `variables-explain` flag.

### 13. User settings set favorite `mao model-name` and `/model-name`, default `mao provider-name` and `/provider-name`, or output directory `mao output-name` and `/output-name`
- User config JSON updates via `settings_manager.py`, similar to `/config` but to set specific user config values quickly. 

---

## Workflow Operations, File Processing Commands (10) 

### 14. `mao goal` and `/goal`
- Create workflow from single message; when completing this, also implement "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `FINAL_IMPLEMENTATION_DETAILS.md` for the section "Connect `goal()` method to real `WorkflowOrchestrator`". 

### 15. `mao setup` and `/setup`
- Already implemented, needs standardization audit and make sure it has multi-path support (user config JSON updates via `settings_manager.py`)

### 16. `mao update` and `/update`
- Already implemented but needs updating to accomodate with multi-path support + secondary flags (-add, -remove, -replace, -rename, -chat) (user config JSON updates via `settings_manager.py`)

### 17. `mao fix_it` and `/fix_it`
- Workflow correction with automatic JSON copying logic (user config JSON updates via `settings_manager.py` already implemented, but needs additional logic to copy the JSON object to the appropriate directory)

### 18. `mao continue` and `/continue`
- Workflow state management integration (workflow_state.py)

### 19. `mao review` and `/review`
- Workflow analysis and search capabilities (workflow_state.py)

### 20. `mao chat` and `/chat`
- Jump to main app with message passthrough (conversation_bridge.py)

### 21. `mao doctor` and `/doctor`
- System health checks and workflow diagnostics (workflow_state.py)

### 22. `mao dry_run` and `/dry_run`
- Workflow simulation mode (workflow_state.py)

### 23. `mao verbose` and `/verbose`
- Debug mode toggle (already created, needs to be added to the workflow_state.py)

### 24. `mao logs` and `/logs`
- Workflow log viewing (relates to stats/review/workflows) (workflow_state.py)

---

## Systematic Implementation Process

**DO ONE COMMAND AT A TIME, THEN AUDIT THAT COMMAND**

### Phase 1: Planning (Per Command)
1. **Choose command** from complexity category
2. **Sequential think requirements**:
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
5. **Update integration touchpoints** if required

### Phase 3: Quality Control
6. **Report implementation results** 
7. **Sequential thinking + full audit** using `MAO_FILE_STANDARDIZATION_RULES.md`:
   - Standard MAO imports ✓
   - CacheManager integration ✓  
   - estimate_cost() function ✓
   - @handle_errors decorators ✓
   - Fingerprinting patterns ✓
   - UI consistency patterns ✓
8. **Fix any standardization violations**
9. **Report fix results**
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
    
    # Command-specific display logic with Rich formatting
    # Follow git-style grouping patterns for help-like commands
    
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
User Management: login, logout, user_id → username_manager.py
Settings: config, model, provider, output → settings_manager.py  
Workflows: goal, workflows, workflow_id → workflow_manager.py
System Info: stats, list_tools → real_time_metrics.py, manager_tools.py
Models/Providers: model_list, provider_list → manager_models.py
```

### Full Orchestrator File List
```
orchestrator/agent_callback.py          orchestrator/mcp_hub.py
orchestrator/agent_orchestrator.py      orchestrator/memory_mcp.py  
orchestrator/cli_manager.py             orchestrator/real_time_metrics.py
orchestrator/conversation_bridge.py     orchestrator/settings_manager.py
orchestrator/core.py                    orchestrator/username_manager.py
orchestrator/error_handling.py          orchestrator/workflow_manager.py
orchestrator/manager_buttons.py         orchestrator/workflow_state.py
orchestrator/manager_models.py
orchestrator/manager_tools.py
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

### Tool Nickname Implementation
Add to each `tool_*.json`:
```json
{
  "name": "brave_search",
  "nickname": "Brave Search",
  "description": "Privacy-focused web search capabilities"
}
```

---

## Command-Specific Implementation Notes

### Special Requirements by Command

**list_tools**: Add nickname fields to tool JSON files for display flexibility

**update/fix_it**: Automatic JSON file copying logic to appropriate workflow directories

**variables**: Support optional `--explain` flag for detailed descriptions vs simple listing

**model/provider/output**: Update user config JSON files via settings_manager integration

**help**: Implement git-style command grouping with logical categorization

**stats**: Integration with `real_time_metrics.py` for live system data (no mock data)

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

## Recommended Starting Command

**Suggest: `help` command** - Establishes UI patterns, tests discovery logic, demonstrates git-style grouping, relatively simple but showcases the system.

**Alternative: `list_tools`** - Simple data display, tests JSON enhancement (nickname fields), good template for other listing commands.

**Sean's Suggestion: `stats`** - Good example showing real integration complexity but more involved than starting templates.

---

## Document Status

**REPLACES**: 
- Previous partial `CLI_COMMAND_STANDARDIZATION_PLAN.md` 
- `CLI_IMPLEMENTATION_PLAN_NOTES.md` (can be deleted after consolidation)

**REFERENCES**:
- `MAO_FILE_STANDARDIZATION_RULES.md` for audit checklist
- Task completion docs for integration touchpoints
- `NEW_USER_FLOW.md` for login/logout/config flow details

---

*This comprehensive plan provides everything needed for systematic CLI command implementation with full MAO standardization compliance.*