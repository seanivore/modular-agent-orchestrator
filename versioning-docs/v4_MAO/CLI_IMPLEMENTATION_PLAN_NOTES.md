# CLI Implementation Plan Notes 

## Phase 1: Categorize by Complexity

**Simple Commands (data display, no complex logic)**

### 1. help 
Pull simple, one-line command details from the `./configs/cli/` directory, and then display them in the UI; consider display order and grouping for UX. 

### 2. list_tools
Pull description and 'nickname' from tool's JSON file to display in the UI; consider display order and grouping for UX. 

### 3. model_list
Pull notes and model's 'display-name' from model's JSON file in the `./configs/models/` directory to display in the UI; consider display order and grouping for UX. 

### 4. provider_list
Pull notes and provider's 'display-name' from provider's JSON file in the `./configs/providers/` directory to display in the UI; consider display order and grouping for UX. 

### 5. workflows 
List workflows, integrate with `/review` command UX; provide easy access to `/logs`, `/stats`; users can search by custom command to search workflow JSON files; can use User ID, Username, or Workflow ID if they have.

### 6. stats 
System performance metrics via `real_time_metrics.py` including SystemMetricsProvider, WorkflowMonitor, CostTracker; when implementing this, also implement "Task #5 PHASE 3: Confirm 'Orchestrator Integration' for 'Real-Time Features'" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md` including "Re: **Add real cost tracking and progress monitoring**" and "Re: **Confirm stats ready to connect to actual system metrics**". Should be easy to build out to search for larger metrics using User ID, Workflow ID, Model ID, and Provider ID, etc. as detailed in `./versioning-docs/v4_MAO/DATA_COLLECTION_ARCHITECTURE.md`

**Medium Commands (basic operations, some manager integration)**

### 7. config 
Application settings via `settings_manager.py` should be primarily implemented; settings changes auto-update the user config JSON file via their User ID/Username. 

### 8. login 
User authentication via `username_manager.py`; see `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` for more details. 

### 9. logout 
User session management via `username_manager.py`; see `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` for more details. 

### 10. user_id 
Display/generate user ID via `username_manager.py` as part of `NEW_USER_FLOW.md`. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 11. workflow_id 
Generate workflow ID via `workflow_manager.py` as part of workflow setup flow. Workflow state management via `workflow_state.py` and `memory_mcp.py`. 

### 12. variables 
Simple UI list of variables needed to setup a workflow, filling out the workflow use-case JSON object. Workflow template `./configs/examples/workflow_templates/README.md`. Includes a `variables-explain` flag. 

**Complex Commands (workflow operations, file processing)**

### 13. goal 
Create workflow from single message; when completing this, also implement "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `FINAL_IMPLEMENTATION_DETAILS.md` for the section "Connect `goal()` method to real `WorkflowOrchestrator`". 

### 14. setup
Already implemented, needs standardization audit and make sure it has multi-path support (user config JSON updates via `settings_manager.py`).

### 15. update
Already implemented but needs updating to accomodate with multi-path support + secondary flags (-add, -remove, -replace, -rename, -chat) (user config JSON updates via `settings_manager.py`)

### 16. fix_it
   - This is already implemented --> new specifics below need to be added to the implementation 
   - It is used when the user or Mao has a prepared workflow already and they need to fix-it 
   - The most common instance and intended use is when Mao is called to recieve the deliverables from an Agent's phase; Mao reviews it and decides that it needs to be fixed; on the fly the create a new JSON object describing the fix, and then the path for it is placed behind the flag or slash command
   - NOTE: we should set up logic so that it automatically looks to see if the path for the JSON object being added is in the appropriate directory for that workflow, and if not, rather than throwing an error or asking the user to move it, it should copy the JSON object to the appropriate directory as the last step of the update process 

### 17. continue
   - This is defined "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md` for the section "**Workflow state management for `continue/review**`"

### 18. review
   - This is defined "Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md` for the section "**Workflow state management for `continue/review**`"

### 19. chat
   - This is very simple, it merely jumps to the main application screen (which is the chat) and sends whatever follows the flag or slash command as a message to the chat; it is probably in the wrong complexity category 

### 20. doctor
   - Used to check the health of the system and the User's workflow 
   - It has not yet been elaborated on but probably could use more information to be more useful 

### 21. dry-run 
   - This is used to simulate the workflow without actually running it 

### 22. verbose
   - This is used to turn on verbose mode for the workflow for debugging purposes, which has developer-style tools included -- the mode has been created. 

### 23. logs
   - This is used to view the logs for the workflow (see stats and review and workflows)

### CLI Commands That Are Updates to the User Config JSON File

| Set favorite model     | `mao --model model-name`       | `/model model-name`           |
| Set default provider   | `mao --provider provider-name` | `/provider provider-name`     |
| Set output directory   | `mao --output ~/downloads`     | `/output ~/downloads`         |

### Removed Commands Pushed to Next Update 

| Use only free models   | `mao --free`                   | `/free`                       |

## Phase 2: Implementation Template 

Each .py file needs. 

```python
# configs/cli/[command]/[command].py
"""
[Command] CLI Command - Core Logic
"""
# Standard MAO imports 
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

cache = CacheManager()

@handle_errors(operation_name="[command]", return_dict=True)
def execute_[command](params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main command execution with caching and error handling"""
    pass

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    pass

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    return execute_[command](params)
``` 

## Files 

   - JSON files 
   - Create python logic file for each command 
   - Create UI file for each command (or a shared UI file for CLI commands)

## Items Every File Needs 

For audits: `./versioning-docs/technical-documentation/MAO_FILE_STANDARDIZATION_RULES.md`

1. Standard Mao Imports  
2. Standard Cache Instance 
3. 'def estimate_cost(params: Dict[str, Any]) -> float:'
4. Error Handling Decorator 
5. Standard Caching Pattern 

## Touch-Points 

### Before each command implementation, please review the Orchestrator files and what touch points are needed. 

```
User Management: login, logout → username_manager.py
Settings: config, privacy → settings_manager.py
Workflows: goal, workflows → workflow_manager.py
System Info: stats, list_tools → real_time_metrics.py, manager_tools.py
Models/Providers: model, provider → manager_models.py
```

### The Full List 

```
orchestrator/agent_callback.py
orchestrator/agent_orchestrator.py
orchestrator/cli_manager.py
orchestrator/conversation_bridge.py
orchestrator/core.py
orchestrator/error_handling.py
orchestrator/manager_buttons.py
orchestrator/manager_models.py
orchestrator/manager_tools.py
orchestrator/mcp_hub.py
orchestrator/memory_mcp.py
orchestrator/real_time_metrics.py
orchestrator/settings_manager.py
orchestrator/username_manager.py
orchestrator/workflow_manager.py
orchestrator/workflow_state.py
```

### UI Consideration 

I like the grouping when you search help in the git command line tool, Re: Spacing, etc. 

```bash
> ~/Dev/modular-agent-orchestrator > git --help                        23:39:20
usage: git [-v | --version] [-h | --help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--no-lazy-fetch]
           <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone      Clone a repository into a new directory
   init       Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add        Add file contents to the index
   mv         Move or rename a file, a directory, or a symlink
   restore    Restore working tree files
   rm         Remove files from the working tree and from the index
```