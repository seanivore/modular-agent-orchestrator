# Master Task List

|----------------------|
| **SESSION 13 TASKS** |
| -------------------- |

## Codebase Structure & File Name Updates 

  1. Review changes, logic, and intention 
  2. Provide feedback, suggestions, better naming 
  3. Help finalize new system setup 
  4. Create prompt for file updates as a result 

#### Codebase Structure Logic  

- Make more modular 
  - Group files by element not file type 
  - All tool files in that tool's directory 
- AI context friendly 
  - Not working across directories 
  - Update and implementation ready 
- Human navigation friendly 
  - Minimize files, directories at root 
  - Hierarchy still shallow 
- Similar modular documentation directory 
  - Accessible names for grouping concepts 
  - Convert old implementation docs 

#### Agentic Product Name  

--> MAO (Modular Agent Orchestrator)

- Accuracy 
  - Certainly no longer single file 
  - emphasizes actual agentic ability 
- Understandable 
  - Know what it does immediately 
  - Common terms; not trite 
- Marketing 
  - Can be used as a verb 
  - Flow, punchy, multi-meaning 

  > Create a new MAO workflow for that data analysis next week. 
  > Sure, let me message the OA (Orchestrator Agent) and chat it out. 
  > Did you MAO that research assignment we got in class yesterday? 
  > That's a great idea, let's MAO it. We'll be so prepared. 

### Simplified Version --- FULL VERSIONS BELOW

```
├── build/...
│   ├── api/...
│   ├── interfaces/...
│   └── orchestrator/...
│       ├── cache/...
│       ├── core.py
│       ├── master/...
│       │   ├── buttons_manager.py
│       │   ├── error_handling.py
│       │   ├── model_manager.py
│       │   └── tool_manager.py
│       ├── memory.py
│       └── protocol.md
├── components/...
│   ├── ai/...
│   │   ├── connections/...
│   │   │   ├── models_x_tools.json
│   │   │   └── providers_x_models.json
│   │   ├── model_registry/...
│   │   │   ├── model_name.json
│   │   │   └── models.json                <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART
│   │   └── provider_registry/...
│   │       ├── provider_name.json
│   │       └── providers.json             <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART
│   └── tools/...
│       └── tool_name/...                  <-- ‼️ EXAMPLE; every tool file now like this
│           ├── tool_name.py
│           ├── button_tool.py
│           ├── model_tool.json
│           ├── cache_tool.py  <-- I guess we don't have this so will delete if we don't need
│           └── ui_tool.py
└── technical-docs/...
```

### New Version
```
~/Development/modular-agent-orchestrator/...
├── mao_v4.py
├── build/...
│   ├── api/...
│   │   ├── auth.py
│   │   ├── models.py
│   │   └── service.py
│   ├── interfaces/...
│   │   ├── ui_terminal.py                 <-- ‼️ updated filename; added 'ui_' master
│   │   └── ui_web.py                      <-- ‼️ updated filename; added 'ui_'
│   └── orchestrator/...
│       ├── cache/...
│       │   ├── __init__.py
│       │   ├── cache_system.py            <-- ‼️ updated filename; was hybrid_cache
│       │   └── xTEMP
│       │       ├── cache_coordinator.py   <-- 💀 duplicates need to be fixed
│       │       └── universal_cache.py     <-- 💀 duplicates need to be fixed
│       ├── core.py
│       ├── master/...
│       │   ├── buttons_manager.py         <-- ‼️ updated filename; was human_buttons master
│       │   ├── error_handling.py          <-- Shared error handling utility
│       │   ├── model_manager.py
│       │   └── tool_manager.py            <-- ‼️ updated filename; was tool_discovery
│       ├── memory.py                      <-- MAO added conversation history for context
│       └── protocol.md
├── components/...
│   ├── ai/...
│   │   ├── connections/...
│   │   │   ├── models_x_tools.json        <-- Matching up models to tools
│   │   │   └── providers_x_models.json    <-- 👻 doesn't exist, example only
│   │   ├── model_registry/...
│   │   │   ├── model_name.json            <-- 👻 doesn't exist, example only
│   │   │   ├── model_name.json            <-- 👻 doesn't exist, example only
│   │   │   └── models.json                <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART
│   │   └── provider_registry/...
│   │       ├── provider_name.json         <-- 👻 doesn't exist, example only
│   │       ├── provider_name.json         <-- 👻 doesn't exist, example only
│   │       └── providers.json             <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART
│   └── tools/...
│       └── tool_name/...                  <-- ‼️ EXAMPLE; every tool file now like this
│           ├── tool_name.py
│           ├── button_tool.py             <-- 🔄 Human buttons for tools
│           ├── model_tool.json            <-- 🔄 Tool definitions and metadata
│           ├── cache_tool.py
│           └── ui_tool.py
└── technical-docs/...
    ├── introduction/...
    │   ├── SPECIFICATIONS.md              <-- 📓 an overview with a 'how' focus
    │   ├── MODULAR_PHILOSOPHY.md          <-- 📓  all of the important reasons
    │   └── MODULAR_STRUCTURE.md           <-- 📓 modular layout doubling as table of contents
```
IMPORTANT FUNCTION I-X
  - What component is
  - The file organization
  - Logic benefits and tips
  - How it is integrated
Organized into tangible categories like below examples
- --> Process: sequential thinking list parts organized like below
- --> Think: review, critique, break-down, any separated,
- --> Think: make clear where each file fits, write intro. for each section
- --> Think: review section intros., make final organization
- --> Write in full, review in full, critique, made final edits
```
    ├── orchestrator/...
    │   ├── INTELLIGENCE.md                <-- model, provider JSON, API
    │   ├── BEHAVIOR.md                    <-- an overview, re: core.py, protocol.md, memory.py
    │   ├── AGENCY.md                      <-- user-chat setup scripts, use-cases, workflow JSON config
    │   ├── ABILITY.md                     <-- tools, JSON registry, buttons, cache, error handling
    │   └── MANAGEMENT.md                  <-- workflow and file management, ending tasks, recording
    ├── agents/...
    │   ├── ASSIGNMENT.md                  <-- get task, token count max reminder and live counter, auto-save docs,
    │   └── COMPLETION.md                  <-- calling MAO, reporting, hand-off
    ├── human/...
    │   ├── UI_MODULARITY.md               <-- UI files and master file
    │   ├── VERBOSE_ARGS.md                <-- file exists in part; expand
    │   ├── TOOL_CREATION_GUIDE.md         <-- file exists; review for accuracy
    │   └── WORKFLOW_SELF_SETUP.md         <-- setup script, use-case JSON, how to skip orchestrator
    └── versioning/...
        ├── CHANGE_LOG.md
        ├── v1_v2_v3_SFA/...
        │   ├── v1/...
        │   ├── v2/...
        │   └── v3/...
        │       ├── v3_0_0_0
        │       ├── v3_1_0_0
        │       └── v3_1_1_2
        └── v4_MAO/...
            └── v4_0_0_0
```

### Old Version
```
/single-file-agents/sfa-v4/              <-- This is inside the SFA folder
├── sfa_v4_main.py
├── api
│   ├── auth.py
│   ├── models.py
│   └── service.py
├── configs
│   ├── model_tool.json                  <-- Matching up models to tools
│   ├── models.json
│   ├── providers.json
│   └── tool_registry                    <-- Tool definitions and metadata
│       ├── tool_brave_search.json
│       ├── tool_dalle_generate.json
│       ├── tool_file_operations.json
│       ├── tool_graphic_design.json
│       ├── tool_perplexity_search.json
│       ├── tool_text_editor.json
│       ├── tool_think.json
│       └── tool_web_search.json
├── interfaces
│   ├── terminal.py                      <-- Master UI file
│   ├── ui_tools
│   │   ├── ui_brave_search.py
│   │   ├── ui_dalle_generate.py
│   │   ├── ui_file_operations.py
│   │   ├── ui_graphic_design.py
│   │   ├── ui_perplexity_search.py
│   │   ├── ui_text_editor.py
│   │   ├── ui_think.py
│   │   └── ui_web_search.py
│   └── web.py
├── orchestrator
│   ├── core.py
│   ├── human_buttons.py                <-- Master human button file
│   ├── hybrid_cache.py                 <-- Original cache, confirm re: utility cache below
│   ├── memory.py                       <-- OC adds history like conversation for context
│   ├── model_manager.py
│   ├── protocol.md
│   └── tool_discovery.py
├── tests                              <-- Testing suite
├── tools
│   ├── brave_search.py
│   ├── dalle_generate.py
│   ├── file_operations.py
│   ├── fonts
│   ├── graphic_design.py
│   ├── perplexity_search.py
│   ├── text_editor.py
│   ├── think.py
│   └── web_search.py
└── utilities
    ├── cache_tools
    │   ├── __init__.py
    │   ├── integration_example.py
    │   └── universal_cache.py         <-- Possibly made by mistake, re: original above
    ├── error_handling.py              <-- Shared error handling utility
    └── human_button_tools             <-- Human buttons for tools
        ├── button_brave_search.py
        ├── button_dalle_generate.py
        ├── button_file_operations.py
        ├── button_graphic_design.py
        ├── button_perplexity_search.py
        ├── button_text_editor.py
        ├── button_think.py
        └── button_web_search.py
```

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

Let's talk through ideas and find what is most logical. The idea is the codebase is structured so that an AI will immediately understand it, a human can get around, and most importantly, an AI can do work and make updates without needing files spread all over the place. 

**NOTE TO SELF FIND THE BIT ABOUT THE CACHE FILE COMPLICATIONS TO PULL HERE BEFORE STARTING**

### Discuss Logic & Finalize 

Let's break this into parts. First the actual product, meanwhile me learning how or where they are referencing each other, then we'll think about documentation after. 

#### Codebase Structure Feedback 

1. Consider modular grouping 
2. Consider placement and directory naming 
3. Any groupings I missed 

I think of it like this: 

> Modular groups of files, like the tool directories and their 4 (5 or 6) files, then the Model JSONs. I do think we should break down the models.json and providers.json into individual files. And then if there were or are other files that should go with each model to make it work, like the tools, then we should do the same as tools. 

(GROUP TYPE A NO. 1) (GROUP TYPE A NO. 2) (GROUP TYPE A NO. 3) 
(GROUP TYPE B NO. 1) (GROUP TYPE B NO. 2)

> I think of it like this because in an ideal world we'll be able to add or remove a whole tool directory or model directory, and not have to change any system files at all. I'll be curious too see if it is like that now and pushing for that when we review to accommodate my changes. 

> Then I think about the system files, presumably with each having a 'MASTER' or 'SHARED' file that pulls from the different parts across the tool directories or models, etc. 

(MAIN SYSTEM TOOL)
(MASTER THAT PULLS X FROM EACH GROUP TYPE A)
(MASTER THAT PULLS X FROM EACH GROUP TYPE B)

> Etc. and so on. Again, my curiosity and goal here is to see how they reference each other and think about how it could be as plug-and-play as possible. 

> Like... NEW MODEL COMES OUT TODAY ... I drop in the CONFIG. When I run my setup JSON I reference using that agent for whatever task, and it is useable just by placing all the necessary pieces exactly where they should be, but NOT by pointing to a specific number of or named item in those necessary pieces where they should be. If that makes sense. 

> I keep thinking about one function I remember vaguely in the SFA that listed all the tools when requested. Ideally that is all that is ever necessary, for each modular grouping, regardless of the file type or data. 

#### Discuss Codebase 

1. Feedback, decisions, and codebase changes made 
2. List any necessary 'to do' updates because of these changes to address after this next task 
3. Now let's structure the documentation; my example is a loose concept 
4. Then files update

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
