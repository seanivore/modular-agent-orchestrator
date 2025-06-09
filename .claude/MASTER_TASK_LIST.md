# Master Task List

|----------------------|
| **SESSION 13 TASKS** |
| -------------------- |

## Codebase Structure & File Name Updates 

```
~/Development/seanivore/modular-agent-orchestrator/ <-- all files moved if that effects any script files
├── configs/
│   ├── connections/
│   ├── models/
│   └── providers/
├── interfaces/               <-- UI managers
│   ├── terminal.py     
│   └── web.py
├── mao_v4.py                <-- ‼️ updated filename; no hardcoding anyway
├── orchestrator/ 
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── cache_system.py          <-- ‼️ updated filename; was hybrid_cache
│   │   └── xTEMP/
│   │       ├── cache_coordinator.py    <-- 💀 duplicates need to be fixed
│   │       └── universal_cache.py      <-- 💀 duplicates need to be fixed
│   ├── core.py
│   ├── error_handling.py           <-- Shared error handling utility
│   ├── manager_buttons.py           <-- ‼️ updated filename; was human_buttons master
│   ├── manager_models.py            <-- ‼️ updated filename; was model_manager
│   ├── manager_tools.py            <-- ‼️ updated filename; was tool_discovery
│   ├── memory.py               <-- ‼️ empty; conversation history for context
│   └── protocol.md               <-- ‼️ empty; guide for setup chat 
└── tools/ 
```

----

## Planning Technical Documentation 

### **What is the best way to organize the documentation?**
  - Start with the most important terms at the top, clearly visible 
  - Create a flow that mirrors the flow of using the tool 
  - Fill in the gaps, adding each concept and file where they make the most sense 
  - Use the flow's 'loop' from running multiple agents for tasks to introduce under-the-hood concepts 
  - This creates a logic flow 
  - It builds on itself, helping non-tech users understand


- How the workflow is setup with the user --> 
  - Human communication UI/UX 
  - Option to have human in the loop touch-point 
- How much agency MAO has --> 
  - Normalized to be open ended to be reviewed and planned in the flow 
  - Deciding who to delegate to 
- What MAO does to put the enough of a workflow together to start --> 
  - Putting together the plan, the use-case workflow CONFIG 
  - Using the setup script to create the workflow 
  - Starts memory history for when they're called back in 
- How MAO starts the workflow --> 
  - Calling in the agent 
  - Handing off the work
  - Providing them with buttons 
  - Updates their workflow report 
- The role of the agent --> 
  - Completing the work 
  - Using the tools; auto-save so no saving output; live token counter UI as they work 
  - Calling OC when finished or if needed 
  - Handing in deliverables 
  - Providing a report of their task in the moment 
- How MAO manages the workflow --> 
  - Returns when agent calls to hand in task 
  - Reviews work and decides the next phase 
  - Saves documents in the Files API as "working" documents 
  - Human touch-point if planned to have one 
  - Records the agent's report in their workflow report 
  - Updates memory history 
- MAO continues workflow --> 
  - Same content as 'How MAO starts the workflow' 
  - Same content as 'The role of the agent' 
  - Same content as 'How MAO manages the workflow' until the tasks are complete 
  - WHAT IS HAPPENING UNDER THE HOOD? 

----


### File Updates  

What code to be updated when the following are changed? 

  1. Files are moved 
  2. Structure changed 
  3. Files are renamed 
  4. New modular addition 
     - Tool directory with all files 
     - New model JSON 
     - Updated connection between model and tool JSON 
     - Updated costs, etc. 

- Once I understand I want to contemplate, is this as modular as possible? 
- Again, totally also open to changing wording if there are more appropriate terms or better ways to group other things
- Cache folder is like that because we had a separate directory with the init py file, but then the main cache_system was in orchestrator
- We might want to pull them out of master and out of cache if we want less deep of a structure


------------------------------------

**End this phase with new structure planned and ready for the next session of documentation and planning the final stretch.**

**Below is the next session task.**

------------------------------------

|----------------------|
| **SESSION 14 TASKS** |
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
