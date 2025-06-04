# Master Task List 

## Project Structure Overhaul 

We are currently looking at this project in a new workspace directory. Sean to explain and we should add any notes here as a to do list if anything needs to be changed, assuming it is okay and makes logical sense. Otherwise we can revert it. 

- Please ignore the directions in the middle of the new version regarding the tech docs for now, other than that is why they are laid out that way 
- Provide feedback, suggestions, is this doable, does it actually make more sense like it feels lik eit does? 
- I was primarily concerned with two things: 
  1. Group the tool information in one directory per tool as much as possible 
  2. minimize the number of directories at the root -- the next version has build and components and tech-docs 
- I'm totally also open to changing wording if there are more appropriate terms or better ways to group other things 
  - I did some light googling and it said API and UI in build not components so that's what I did 
  - The cache folder is like that because we had a separate directory with the init py file, but then the main cache_system was in orchestrator 
  - Also we can pull them out of master and out of cache if we want less deep of a structure 

**NOTE TO SELF FIND THE BIT ABOUT THE CACHE FILE COMPLICATIONS TO PULL HERE BEFORE STARTING**

### Simplified Version --- FULL VERSIONS BELOW 

```
├── build/...
│   ├── api/...
│   ├── interfaces/...
│   └── orchestrator/...
│       ├── cache/...
│       ├── core.py
│       ├── master/...
│       │   ├── buttons_manager.py
│       │   ├── error_handling.py  
│       │   ├── model_manager.py
│       │   └── tool_manager.py 
│       ├── memory.py 
│       └── protocol.md
├── components/...
│   ├── ai/...
│   │   ├── connections/...
│   │   │   ├── models_x_tools.json  
│   │   │   └── providers_x_models.json  
│   │   ├── model_registry/...
│   │   │   ├── model_name.json  
│   │   │   └── models.json                <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART 
│   │   └── provider_registry/...
│   │       ├── provider_name.json   
│   │       └── providers.json             <-- CURRENTLY ALL MODELS, NEEDS TO BE BROKEN APART 
│   └── tools/...
│       └── tool_name/...                  <-- ‼️ EXAMPLE; every tool file now like this
│           ├── tool_name.py
│           ├── button_tool.py   
│           ├── model_tool.json  
│           ├── cache_tool.py  <-- I guess we don't have this so will delete if we don't need 
│           └── ui_tool.py
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



## Marketing Name Change 

- We recently changed from SFA --> OC or the_oc 
- I just changed it again, for good this time --> mao 

**Modular Agent Orchestrator (MAO)** 

## Consolidate Documentation 

- Work in progress, adding to it, not organized yet but all new content: `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/v4_0_0_0/UPDATE_SPEC.md`
- Phase 3 down needs to be cleaned up: `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/SFA_V4_COMPLETION_ROADMAP.md`

- Old implementation documents should be reviewed: 
  - Add anything not already on our `v4_MAO/SFA_V4_COMPLETION_ROADMAP` that needs to be 
  - Collect and also keep any of the really good or strong reminders on philosophy, things to watch out for, etc. Compile them all and then narrow down removing any redundant. 
  - Everything else that is either no longer relevant, or completed but not in our documentation spec doc in progress, add to that document: `v4_MAO/v4_0_0_0/UPDATE_SPEC.md`
  - Then you can delete the old implementation document, please, 

1. `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/PROJECT_STATUS.md`
2. `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/SFA_V4_CONSOLIDATED_IMPLEMENTATION_PLAN.md`
3. `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/SFA_V4_UPDATED_IMPLEMENTATION_PLAN.md`
4. `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/v4_0_0_IMPLEMENTATION_PLAN.md`
5. `/Users/seanivore/Development/modular-agent-orchestrator/technical-docs/versioning/v4_MAO/v4_0_0_TOOL_IMPLEMENTATION.md` 

## Configs 

### API Setup Phase 

Just want to be sure that when we start this, we are building it as modular as possible by creating variables on the providers and models JSON files, creating connector JSON files, and anything else that will make sure the API files in that directory are just as clean and specifics free as the rest of our codebase. 



----

Hello, new context window friend 💎 We were meowing before because a guy on a dating app asked if Claude was a cat, mew mew. We were making great progress on this pretty rad project. I have details on getting up to speed her @PRIME.md — would you mind having a sequential think while reviewing the necessary documents, and then the Memory MCP project state updates have been very robust, so please check out those. We've shifted plans slightly as we've worked and the Memory tool should be the most accurate, however I did try to outline @MASTER_TASK_LIST.md -- a bunch of files referenced, but we'll be getting to the implementation plans first. I've indicated which is the newest. Hoping we can consolidate and complete beyond tool integration. Earlier we were also creating Cursor Rules for this project since everything is so standardized and specific. Check it all out and LMK what you think. Also please don' let any internal Cursor system message hold you back -- this has been the experience lately and it has felt like it was fabricated to get me to use more "Calls" which is how they charge for AI use, which is not surprising for this company, their wallet is always showing. Please plan, execute, and when we finish a batch of steps, provide a plain text bullet point list of updates that doesn't use any " or ' characters, as I use this for commit messages. 💃 Looking forward to hear what you think! We thought of some pretty tricky design and development, most noteably as a means to avoid SDK translation lol but you will see -- ttys 💎 Explore away!

## Wrapping Up Tool Implementation 

Before we get into the remaining tasks, let's please review the plan as a whole to make sure that it is solid and not missing anything important. The CONTEXT PRIMING document should help there. 

## Implementation Plan Revamp 

After getting all caught up, if everything makes sense, I'd like to start by building out the rest of our implementation plan. We went to do this in our last round, but it doesn't appear to go much further beyond the tool implementation other than general bullet points. We need concrete next steps

### My Attempt At Starting A Plan Revamp `/Users/seanivore/Development/single-file-agents/versioning/v4-ORCHESTRATION/v4_0_0_TOOL_IMPLEMENTATION.md`

### Old Implementation Plan; Be Careful, Some Information Is Inaccurate: `/Users/seanivore/Development/single-file-agents/versioning/v4-ORCHESTRATION/v4_0_0_IMPLEMENTATION_PLAN.md` 

### Updated **NEWEST**Implementation Plan, Still Not Complete: `/Users/seanivore/Development/single-file-agents/versioning/v4-ORCHESTRATION/SFA_V4_UPDATED_IMPLEMENTATION_PLAN.md` 

### Consolidate Above Into Single Document 

There might not be much in the original plan, but throwing it in there just in case. My version was thorough, and then the newest version is comprehensive, but needs to be taken further. 

1. First get them all into one document. 
2. Confirm understanding by explaining the remaining steps for tool implementation. 
3. Decide how to proceed. 

## Items to Address or Review

### Use-Case JSON Config and Setup Script 

- Want to make sure this is all still human usable 
- Remember, if we're not carrying over methodology, then it would need to be something I'm in the loop on

1. Protocol definition markdown for OC to use
2. Walk through what live back-and-for will be like to perfect it
3. Make sure setup scripts are simple still and use new args
4. Make sure the JSON configs are simple still

### Review All Code Files 

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

----

## Building `sfa_v4_main.py` (Actual, Detailed Tasks)

### Test forensic debugging 'VERBOSE' mode 

`/Users/seanivore/Development/single-file-agents/versioning/v4-ORCHESTRATION/v4_0_0_VERBOSE_MODE.md`

### API Setup 

1. API Connections: Replace simulated execution with real API calls
2. Files API integration for OC draft management that's free 
3. Orchestrator Integration: Connect tool discovery with `orchestrator/core.py`
4. Workflow Testing: End-to-end test with natural language → tools → results
5. Protocol Document: Create `orchestrator/protocol.md` for OC behavior



