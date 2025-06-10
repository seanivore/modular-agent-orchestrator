# Master Task List
MAO v4.0.0.0 (Modular Agent Orchestrator)

|----------------------|
| **SESSION 14 TASKS** |
| -------------------- |

* New codebase structure 
* Agent/product name change 
* Technical documentation creation 

## Project Structure & File Name Updates 

- All files moved directories 
- No code has been changed 

```
~/Development/seanivore/modular-agent-orchestrator/ <-- all files moved if that effects any script files
├── configs/
│   ├── connections/
│   │   ├── models_x_tools.json      <-- ⚠️ new file; eliminates cross-config file reference hardcoding
│   │   └── providers_x_models.json  <-- ‼️ new file
│   ├── models/              <-- ⚠️ model registry, models.json broken into per-model JSON files
│   │   ├── claude-3-7-sonnet.json
│   │   ├── claude-opus-4.json
│   │   ├── claude-sonnet-4.json
│   │   ├── gemini-2.5-pro.json
│   │   ├── gpt-4.1-mini.json
│   │   ├── gpt-4.1-nano.json
│   │   └── local-llama-3.1-8b.json
│   └── providers/           <-- ⚠️ providers.json broken into per-provider JSON files
│       ├── anthropic-direct.json
│       ├── gemini-direct.json
│       ├── litellm.json
│       ├── lm-studio.json
│       ├── openai-direct.json
│       └── requesty.json
├── interfaces/
│   ├── terminal.py          <-- 👻 updated filename; was ui_terminal.py
│   └── web.py               <-- 👻 updated filename; was ui_web.py
├── mao_v4.py                <-- 👻 updated filename 
├── orchestrator/ 
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── cache_system.py          <-- 👻 updated filename from 'hybrid_cache'
│   │   └── xTEMP/
│   │       ├── cache_coordinator.py <-- 💀 duplicates need to be fixed
│   │       └── universal_cache.py   <-- 💀 duplicates need to be fixed
│   ├── core.py
│   ├── error_handling.py     <-- Shared error handling utility 
│   ├── manager_buttons.py    <-- 👻 updated filename from 'human_buttons' 
│   ├── manager_models.py     <-- 👻 updated filename from 'model_manager' 
│   ├── manager_tools.py      <-- 👻 updated filename from 'tool_discovery'
│   ├── memory.py             <-- ‼️ empty; conversation history for context
│   └── protocol.md           <-- ‼️ empty; guide for setup chat 
├── tests
├── tools
│   ├── brave_search
│   │   ├── brave_search.py
│   │   ├── button_brave_search.py
│   │   ├── tool_brave_search.json
│   │   └── ui_brave_search.py
│   ├── dalle_generate
│   │   ├── button_dalle_generate.py
│   │   ├── dalle_generate.py
│   │   ├── tool_dalle_generate.json
│   │   └── ui_dalle_generate.py
│   ├── file_operations
│   │   ├── button_file_operations.py
│   │   ├── file_operations.py
│   │   ├── tool_file_operations.json
│   │   └── ui_file_operations.py
│   ├── graphic_design
│   │   ├── button_graphic_design.py
│   │   ├── fonts
│   │   ├── graphic_design.py
│   │   ├── tool_graphic_design.json
│   │   └── ui_graphic_design.py
│   ├── perplexity_search
│   │   ├── button_perplexity_search.py
│   │   ├── perplexity_search.py
│   │   ├── tool_perplexity_search.json
│   │   └── ui_perplexity_search.py
│   ├── text_editor
│   │   ├── button_text_editor.py
│   │   ├── text_editor.py
│   │   ├── tool_text_editor.json
│   │   └── ui_text_editor.py
│   ├── think
│   │   ├── button_think.py
│   │   ├── think.py
│   │   ├── tool_think.json
│   │   └── ui_think.py
│   └── web_search
│       ├── button_web_search.py
│       ├── tool_web_search.json
│       ├── ui_web_search.py
│       └── web_search.py
└── versioning-docs
    ├── CHANGE_LOG.md
    ├── technical-documentation
    │   ├── 1.INTRODUCTION
    │   │   ├── 1.1_MEET_MAO.md
    │   │   ├── 1.2_THE_AGENT_HYPE.md  
    │   │   └── 1.3_MODULAR_PHILOSOPHY.md
    │   ├── 2.BUILDING_WITH_MAO
    │   │   ├── 2.1_COMMUNICATION.md
    │   │   ├── 2.2_WORKFLOW_PLANNING.md
    │   │   ├── 2.3_TOOL_IMPLEMENTATION_GUIDE.md
    │   │   └── 2.4_ITS_ALL_VARIABLE.md
    │   ├── 3.AGENCY
    │   │   ├── 3.1_BEHAVIOR.md
    │   │   ├── 3.2_SPAWN.md
    │   │   ├── 3.3_ORCHESTRATION.md
    │   │   └── 3.4_WORKFLOW_MANAGEMENT.md
    │   ├── 4.COST_OF_MAO
    │   │   ├── 4.1_FINGERPRINTING.md
    │   │   └── 4.2_RESOURCE_EFFICIENCY.md
    │   └── 5.SET_UP_FOR_SUCCESS
    │       ├── 5.1_RUNNING_ESTABLISHED_WORKFLOWS
    │       ├── 5.2_WORKFLOW_MONITOR.md
    │       ├── 5.3_WORKFLOW_REPORT.md
    │       ├── 5.4_VERBOSE_MODE.md
    │       └── 5.5_ERROR_HANDLING.md
    ├── v1-3_SFA
    └── v4_MAO
```

----



-------------------------------------

|----------------------|
| **SESSION 15 TASKS** |
| -------------------- |

## MUST CLEAN UP DOCUMENTATION

1. Plan end state of documents
2. Review what we have
3. Pull what we need
4. Outline and leave space for what is missing
5. DELETE everything we do not -- not deleting is how this mess got started
6. Using documents plan out remaining build tasks and testing
7. Double back to fill in gaps as fits the plan
8. Clean up documentation by separating out task list
9. Be finishing build and testing with polished documentation

### Documentation Plan Based on New Structure

1. Review new plan
2. Adjust, feedback, change
3. Layout and input the following documents in logical way

### Current Documentation State

#### Newest File 
- `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/v4_0_0_0/UPDATE_SPEC.md`
- Wildly unorganized 
- Don't want to delete the stuff I wrote new

#### Last Remaining Other Document 
- `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/v4_0_0/PROJECT_STATUS.md`
- Needs to be consolidated into other doc and organized 

## New Documentation & Final Stretch

1. Use new documents
2. Double back to the planned out documentation outline
3. Build documentation outline
4. Leave spaces where needed
5. Once complete create final stretch plan
6. Complete both in unison

Also update the CHANGE_LOG.md `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/CHANGE_LOG.md`

**End this phase with documentation for the project that is perfect and a plan for everything that is remaining for this build, in a detailed way that any other AI could pick it up, always including references to CONTEXT PRIMING where needed.**

------------------------------------

**BELOW ARE NOTES TO BE CONSOLIDATED INTO FINAL STRETCH PLAN WHEN AND IF NEEDED OTHERWISE DELETED**

------------------------------------

## Other

We never ran a test of the verbose output --> add to list for UI tasks

### API Setup Phase

1. API Connections: Replace simulated execution with real API calls
2. Files API integration for OC draft management that's free `./.claude/TOOL_FILES_API.md`
3. Orchestrator Integration: 
   - Connect tool discovery with `core.py`
   - Implement code execution tool via documentation here: `./.claude/TOOL_CODE_EXECUTION.md`
4. Workflow Testing: End-to-end test with natural language → tools → results
5. Protocol Document: Create `protocol.md` for OC behavior

### Review All Code Files

### Make ARGs JSON

- Get them into proper modular shape
- Our SFA has 'print ()' functions all over the place: `./sfa-v4/sfa_v4_main.py`
- Flag arguments -- I love the custom ones but that means we need a config file and JSON for them -- which would be rad

```python
Examples:
  python sfa_v4_main.py "Create a marketing strategy for my startup"
  python sfa_v4_main.py --job-app "job_description.txt" --company "TechCorp"
  python sfa_v4_main.py --list-workflows
  python sfa_v4_main.py --stats --verbose
        """
    )

    parser.add_argument("goal", nargs="?", help="Natural language goal to execute")
    parser.add_argument("--workspace", "-w", help="Custom workspace directory")
    parser.add_argument("--job-app", help="Job description file for job application workflow")
    parser.add_argument("--company", help="Company name for job application")
    parser.add_argument("--list-workflows", action="store_true", help="List all workflows")
    parser.add_argument("--stats", action="store_true", help="Show orchestrator stats")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show technical details")
    parser.add_argument("--free-only", action="store_true", help="Use only free models")
    parser.add_argument("--privacy", action="store_true", help="Use privacy-focused models")
```
- How hardcoded does the UI terminal interface file need to be? I saw stuff from job submissions: `./sfa-v4/interfaces/terminal.py`
- Make model names human-friendly line is similar --> love the idea but we can put the nicknames as a variable in the JSON config for models
- Saw this header: `self.display.header("SFA v4.0.0 - AI Workflow Orchestrator", goal)` --> we shouldn't date ourselves by saying what version we're on in the code.
- What are "modes" ... I see creative, etc. type topics in: `./sfa-v4/orchestrator/core.py`
- Ask ourselves, what value does identifying the domain of the task provide... The user? The agents or orchestrator?
- The `_get_agent_role` function makes me realize I need to see the JSON config and variables
