# CLI Implementation Plan Notes 

## Phase 1: Categorize by Complexity

**Simple Commands (data display, no complex logic)**

### 1. help 
   - Pull all of the commands from the `./configs/cli/` directory 
   - Display the commands with the information shown in the table as each command's function 
   - Simple one-line help text 
   - We should determine what order to display the commands based on what will be the most useful for the user 
   - Make notation for the UI regarding spacing, etc. 

### 2. list_tools
   - Pull all of the tools from the `./tools/*.json` in each tool's directory 
   - Ensure that the "description" in the JSON file is what we want to display as the tool's function 
   - The current ID looks like: `"name": "brave_search"` 
     - Create a 'nickname' variable on each tool's JSON file to give flexibility to how we want to display the tool's name 
     - Start initially by filling the 'nickname' variable just using a space and initial caps on the "name" variable 
   - Consider what kind of grouping and headings will be most useful for the user 
   - Make notation for the UI regarding spacing, etc. 

### 3. stats 
   - This is listed as "Show system performance and orchestrator statistics" in the JSON file 
   - We should consider first what exactly that means and where is it pulling from 
     - See "Task #5 PHASE 3: Confirm 'Orchestrator Integration' for 'Real-Time Features'" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md`
     - "Re: **Add real cost tracking and progress monitoring**"
     - "Re: **Confirm stats ready to connect to actual system metrics**"
   - Then we should consider building to that it is easy to build out 
     - Pull in the User ID and provide those kind of stats 
     - Pull in the Workflow ID and provide those kind of stats 
     - Pull in the Model ID and provide those kind of stats 
     - Pull in the Provider ID and provide those kind of stats 
     - Basically I think we want to be thinking about this kind of stuff; not to do immediately, but we should make it easy for us to build out in this way in the next update: 
       - `./versioning-docs/v4_MAO/DATA_COLLECTION.md`
       - `./versioning-docs/v4_MAO/DATA_COLLECTION_ARCHITECTURE.md` 
    - For whatever stats we start with, provide ideas for the UI 
      - Create something that fits the UX/UI design aesthetics 
      - Make sure that there is enough creative freedom room 
    - `orchestrator/real_time_metrics.py` provides live data for UI
      - No mock data - all metrics come from real system state
      - Foundation build can use SystemMetricsProvider, WorkflowMonitor, CostTracker
      - This is mentioned in `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 
    - The command -logs is realted along with -workflows and -stats and -review 

### 4. model_list
   - Should be simple, pulling all of the models according to the colleciton of JSON files in the `./models/` directory 
   - Display the models with the information shown in the table as each model's function 
   - Opportunity for us to see if there are any new variables we want to add to the model JSON files for this UI information 
   - Consider grouping logic, etc. and what will be passed on to the UI 

### 5. provider_list
   - Should be simple, pulling all of the providers according to the colleciton of JSON files in the `./providers/` directory 
   - Display the providers with the information shown in the table as each provider's function 
   - Opportunity for us to see if there are any new variables we want to add to the provider JSON files for this UI information 
   - Consider grouping logic, etc. and what will be passed on to the UI 

### 6. workflows 
   - The original intention of this is just to "list workflows" 
   - We have a "Review Workflow" command that we should acknowledge and then pair next to this option 
   - "Review Workflow" is intended to search and get a group based on including custom command, workflow ID, or User ID 
     - However we should consider how we want the two to work together 
     - Ideally someone could use /workflows and then decide to search (and thus group) by using custom commands, workflow IDs, or User IDs once they are in /workflows because this is natural UX based on how human thinking works 
   - Again, and UI notes to pass along for that development in addition to the UI needs that should go in a specific shared UI files for CLI commands 
   - There are two other commands on the list that are related to the workflow and are not listed here: 
     - `-logs`
     - `-stats`

**Medium Commands (basic operations, some manager integration)**

### 7. config 
   - This is listed as "Open app config" in the JSON file 
   - The implementation details of setting up application settings, how they save to a JSON for the Username/User ID that is created on their first login, is documented: `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 
   - We should also review `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` to ensure everything is clear and that we are not missing any steps 

### 8. login 
   - The logic of how and when this screen shows is detailed in `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` 
   - Most of it should all be implemented already, should confirm: 
     - Username > User ID Config Setup" `./versioning-docs/v4_MAO/TASK_2_USERNAME_CONFIG_COMPLETE.md`
     - Workflow Unique ID - COMPLETE WITH FULL INTEGRATION ✅" `./versioning-docs/v4_MAO/TASK_3_WORKFLOW_ID_COMPLETE.md` 
     - Workflow ID Integration" `./versioning-docs/v4_MAO/TASK_3_INTEGRATION_POINTS.md` 
     - Workflow Creation - Implementation Complete" `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md` 
     - "User Configuration & Setup Script Implementation" `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 

### 9. logout 
   - The logic of how and when this screen shows is detailed in `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` 
   - Most of it should all be implemented already, should confirm: 
     - Username > User ID Config Setup" `./versioning-docs/v4_MAO/TASK_2_USERNAME_CONFIG_COMPLETE.md`
     - Workflow Unique ID - COMPLETE WITH FULL INTEGRATION ✅" `./versioning-docs/v4_MAO/TASK_3_WORKFLOW_ID_COMPLETE.md` 
     - Workflow ID Integration" `./versioning-docs/v4_MAO/TASK_3_INTEGRATION_POINTS.md` 
     - Workflow Creation - Implementation Complete" `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md` 
     - "User Configuration & Setup Script Implementation" `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 

### 10. user_id 
   - The logic of how and when this screen shows is detailed in `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` 
   - Most of it should all be implemented already, should confirm: 
     - Username > User ID Config Setup" `./versioning-docs/v4_MAO/TASK_2_USERNAME_CONFIG_COMPLETE.md`
     - Workflow Unique ID - COMPLETE WITH FULL INTEGRATION ✅" `./versioning-docs/v4_MAO/TASK_3_WORKFLOW_ID_COMPLETE.md` 
     - Workflow ID Integration" `./versioning-docs/v4_MAO/TASK_3_INTEGRATION_POINTS.md` 
     - Workflow Creation - Implementation Complete" `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md` 
     - "User Configuration & Setup Script Implementation" `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 

### 11. workflow_id 
   - The logic of how and when this screen shows is detailed in `./versioning-docs/v4_MAO/NEW_USER_FLOW.md` 
   - Most of it should all be implemented already, should confirm: 
     - Username > User ID Config Setup" `./versioning-docs/v4_MAO/TASK_2_USERNAME_CONFIG_COMPLETE.md`
     - Workflow Unique ID - COMPLETE WITH FULL INTEGRATION ✅" `./versioning-docs/v4_MAO/TASK_3_WORKFLOW_ID_COMPLETE.md` 
     - Workflow ID Integration" `./versioning-docs/v4_MAO/TASK_3_INTEGRATION_POINTS.md` 
     - Workflow Creation - Implementation Complete" `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md` 
     - "User Configuration & Setup Script Implementation" `./versioning-docs/v4_MAO/NEEDS_UPDATE_CACHE_USER_CONFIG_SETUP.md` 

### 12. variables 
   - This is intended to list the variables for the User as a reminder when they are setting up a new workflow 
   - These are the same variables that are on the JSON 
   - Templates can be seen here: 
     - `./configs/examples/workflow_templates/example-workflow/example-workflow_handoff_config.json`
     - `./configs/examples/workflow_templates/example-workflow/example-workflow_phase_config.json`
     - `./configs/examples/workflow_templates/example-workflow/example-workflow_workflow_config.json`
   - A README.md was included with those example files: `./configs/examples/workflow_templates/README.md` 
   - There is a secondary -explain flag that can follow the variables flag to explain the variables in more detail; when just the --variables flag is used, it is just meant to list the variables without any explaination or descriptions necessary; a simple command UX reminder if the user needs

~~### 13. privacy~~
   - I have removed this and added notes that are needed to implement it in the next update. 

**Complex Commands (workflow operations, file processing)**

### 13. goal 
   - This is to be used by the user when they want to create an entire workflow from one message
   - That message can be sent from the command line using the `mao --goal` command or from within the app 
   - It has yet to be determined how little influence the user will have over building the workflow or when they can check and adjust it 
   - See "## Task #5 PHASE 2: Confirm 'Orchestrator Integration' for CLI Related Features" in `./versioning-docs/v4_MAO/FINAL_IMPLEMENTATION_DETAILS.md` for the section "### **Connect `goal()` method to real `WorkflowOrchestrator`**"  

### 14. setup
   - This is already implemented
   - It is used when the user or Mao has a complete .temp directory of JSON config files prepared 
   - It is executed with that path behind the flag or slash command 

### 15. update
   - This is already implemented --> new specifics below need to be added to the implementation 
   - It is used when the user or Mao has a prepared workflow already and they need to update 
   - This logic is not planned but should be simple in that it should mirror the setup logic for normal workflows, as in: `./versioning-docs/v4_MAO/TASK_4_WORKFLOW_CREATION_COMPLETE.md`
   - In this case, they will place the new JSON object that is being added using its path behind the flag or slash command 
   - We should be able to add multiple paths behind the flag or slash command 
   - I think we should also consider creating -add, -remove, -replace, -rename, -chat as secondary flags that can be used with the --update flag or following the slash command 
   - Each one does what it says and would be followed by a path to a new JSON object or a JSON object that is already in the workflow 
   - The "-chat" flag would instead jump to the chat with Mao, sending them a message that they want to adjust the workflow; this message needs to include the workflow ID which we should include by pulling it from the JSON object using the custom command if the User provides that, or by providing the actual workflow ID 
   - NOTE: we should set up logic so that it automatically looks to see if the path for the JSON object being added is in the appropriate directory for that workflow, and if not, rather than throwing an error or asking the user to move it, it should copy the JSON object to the appropriate directory as the last step of the update process 

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