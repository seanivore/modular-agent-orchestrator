# Development Planning Next Steps 
STARTED: 3 June 2025 

---

## UI Foundation Build 

- The steps below are to ensure that the UI foundation build plan is complete and up to date
- The goal is to get us into position to build the best possible UI first build we can 
- Of the steps below, any of them may be done agentically if possible 
- The steps below should be reviewed, scrutinized, and refined 
- Do not presume the are complete or accurate as I have not done this before; avoid all confirmation bias, etc. 
- Combine parts, separate, add, remove --> whatever is needed to ensure that the plan is complete and up to date 
- Let's see if we can get to a place where we are planning as much of this as possible as SPECS to be built agentically 

### 1. Review most recent plan 

- `MAO_APP_UI_IMPLEMENTATION.md`
- `foundation_spec.md`
- `advanced_spec.md`

--> Create a technical description of what the plan should look like, what tech will be used, code, etc. so that we can avoid any confusion like the first build where TypeScript and Node.js should have been used, but were not. 

### 2. Review CLI Command Implementation for Inclusion 

- `CLI_COMMAND_STANDARDIZATION_PLAN.md`
- Identify clear list of relevant newly created files and touch-points 
- Create plan on how to integrate into UI plan including what needs to be planned for 

### 3. Integrate New Functionality into UI Plan 

#### Auto-Complete 

- `CLI_AUTOCOMPLETE_IMPLEMENTATION.md` 
- Describe the UX and UI that should result from implementation 
- Create plan on how to integrate into UI plan including what needs to be planned for

#### Auto-Updates for Configuration Changes 

- `GITHUB_INTEGRATION_SETUP.md` 
- Implement this first; requires webhooks, etc. 
- How it works: 
  - New config is added, removed, or updated (model, provider, setting, slash command, etc.)
  - Changes trigger flow that produces auto-documentation and agentic config updates 
  - Documentation will be pushed to a Github PR automatically
  - Claude Code will agentically update any necessary documentation related to the config changes
  - Files are in place to ensure that in-app, digitally, scanning ensure always up to date displays of configs 
- Create plan on how to integrate into UI plan including what needs to be planned for
- Templates have been started for config files
  - We should create a README for each config file type that explains how to create and add that item 
  - Then let's make sure that Mao is an expert on these matters so that Users and go to Mao for help setting up their own configs 
  - Completing this will double as a great way to ensure complete understanding of all config files and their roles, including all their touch-points 

```
~/Development/modular-agent-orchestrator/templates/
├── cli_commands
│   └── cli_command.json
├── models
│   └── model.json
├── providers
│   └── provider.json
├── settings
│   └── setting_name_app_settings.json
├── tools
│   ├── tool_config_template.json
│   ├── tool.json
│   ├── tool.py
│   └── ui_tool.py
├── users
│   └── user_username.json
└── workflows
    ├── example-workflow_handoff_config.json
    ├── example-workflow_phase_config.json
    ├── example-workflow_workflow_config.json
    └── README.md
```

### 4. Review Orchestrator Files 

- Ensure full understanding of all files and their roles 
- Identify if there is any overlap or gaps 
- Complete a standard audit of them, one at a time for `MAO_FILE_STANDARDIZATION_RULES.md` I think I saw some hardcoding 
- Create plan that ensures all touch-points are implemented into the UI plan as needed 
- If it makes sense, create a plan to audit them from the perspective of UI build

  1. `./orchestrator/__init__.py` = "Modular AI workflow orchestration system"
  2. `./orchestrator/agent_callback.py` = "Handles agent returns, execution results, and workflow progression"
  3. `./orchestrator/agent_orchestrator.py` = "Coordinates agent handoffs with context packages via Files API"
  4. `./orchestrator/cache/__init__.py` = "Universal caching infrastructure for modular tools" 
  5. `./orchestrator/cache/cache_system.py` = "Files API for workflow handoffs and Local cache for permanence; fingerprinting" 
  6. `./orchestrator/cli_manager.py` = "Dynamic CLI command discovery and interface integration"
  7. `./orchestrator/conversation_bridge.py` = "Converts natural language goals into executable custom commands"
  8. `./orchestrator/core.py` = "The main brain that turns natural language into intelligent workflows"
  9. `./orchestrator/error_handling.py` = "Professional error handling patterns for all tools"
  10. `./orchestrator/manager_buttons.py` = "Creates executable code snippets for any model/provider combo"
  11. `./orchestrator/manager_models.py` = "Loads JSON configs and provides intelligent model selection"
  12. `./orchestrator/manager_tools.py` = "Dynamic tool suggestion based on goals, not hardcoded categories"
  13. `./orchestrator/mcp_hub.py` = "Integrates Memory MCP, Files API, and MCP Connector into unified system"
  14. `./orchestrator/memory_mcp.py` = "Provides workflow context tracking, state management, and session recovery"
  15. `./orchestrator/protocol.md`
  16. `./orchestrator/real_time_metrics.py` = "Provides live data for UI components; no mock data allowed"
  17. `./orchestrator/settings_manager.py` = "Dynamic settings discovery and management using directory-based scanning"
  18. `./orchestrator/username_manager.py` = "Handles user creation, session persistence, and settings integration"
  19. `./orchestrator/workflow_manager.py` = "Handles workflow ID generation, discovery, and tracking"
  20. `./orchestrator/workflow_state.py` = "Simple state tracking with Memory MCP integration"

### 5. User and Workflow Implementation 

- Handful of tasks that included everything from app configuration settings, to workflow creation 
- Review all integration feedback and ensure that it is completely represented in the plan 
  - `TASK_2_CACHE_USER_CONFIG_SETUP.md`
  - `TASK_2_USERNAME_CONFIG_COMPLETE.md`
  - `TASK_3_INTEGRATION_POINTS.md`
  - `TASK_3_WORKFLOW_ID_COMPLETE.md`
  - `TASK_4_WORKFLOW_CREATION_COMPLETE.md`
- Create plan that ensures all touch-points are implemented into the UI plan as needed

### 6. Review Visual Brand Identity and User Flow to Create Stronger Visual Guide 

- Review and improve to use to build wire-frame:
  - `MAO_VISUAL_BRAND_IDENTITY.md`
  - `NEW_USER_FLOW.md` 

- Create wire-frame for the UI 
- Ensure there is no question about the UI; for example, the previous build ended up with a "navigation" and a "main menu" -- neither of these are things the application requires at all 
- Ensure that the UI is as simple as possible, but still functional and easy to use 

### 7. Of New Plans, Create Comprehensive Plan 

- Put together a comprehensive plan based on the original, plus the noted additions above 
- Step away, then come back and review the plan, providing feedback
  - What is missing 
  - What is not clear and should be expanded on 
  - Etc. 
- Refine plan accordingly 

### 8. Ensure Completion of All Technical Documentation 

- Between all recent implementation mentioned above, and the resulting new plan 
- Review all techincal documentation and ensure that it is complete and up to date 
- It will likely result best from a complete rewrite and restructuring 
- Can be done agentically if possible 

### 9. Plan Agentic Debugging, Testing, Validation 

- What is possible? How can we be as thorough as possible? 
- When we had the previous working UI, every one little thing you tried to do hit a bug that seemed to be system file issues rather than UI issues 
- Regardless, we want to make sure that everything is thoroughly tested and validated 
- That way when we build the UI, we can be confident that it is working as expected, and if it is not, we can be confident of where the look for the issue 

### 10. Finalize New UI Build Plan 

- Create new SPECS 
- Have Claude Code review and provide feedback and ask questions 
- Ensure that the plan is complete and up to date based on all the above steps 