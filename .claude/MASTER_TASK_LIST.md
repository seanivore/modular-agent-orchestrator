# Master Task List 

## Marketing Naming 

- We are not a 'single-file-agent' any longer
- New project directory to clean things up and avoid path mistakes 
- Current name update: OC for Orchestrator Claude 
- But I'm leaning towards something like 
  - OA = orchestrated agents / OAW / WOA  
  - Some combination of W (workflow) F (flow) A (agent/ic) O (orchestrated) 
  - Very good collection of consonants and vowels 
  - Might find something really good; goal = use it as a verb 

workflow orchestrated agentic claude
orchestrator built agentic workflow obaf
agentic built orchestrated workflow abow abowf foab afob foab fao oaf 
flow orchestrated agentic builder 
aof aod oa opaw 
foas 
soaf
spaof
modoaf
maos 
mao


## Configs 

### API Setup Phase 

Just want to be sure that when we start this, we are building it as modular as possible by creating variables on the providers and models JSON files, creating connector JSON files, and anything else that will make sure the API files in that directory are just as clean and specifics free as the rest of our codebase. 

### Creating A Unified System 

I foresee our current groups of modular JSON integrated information to expand over time. Let's structure the directory in a way that better allows for this. It should be clear how to set things up just by looking at how other JSON configs are organized and named. 

  1. Let's use `./configs/tool_registry/...` with `tool_tool_name.json` as the example case  
     - Is there a way to enforce a structure? A script? Or just cursor rules? 
     - Update one JSON with a new variable, update all files? A script that would create that space? 
     - Perhaps relevant or helpful to have templates first 
  2. In `./configs/examples/...` create templates for each config file type 
     - Tool registered and defined 
     - Model registered and defined 
     - Provider registered and defined 
  3. Create a `./configs/config_connectors/...` with `connect_model_tool.json` as the model 
     - For showing connections between two config files 
     - Avoiding hardcoding in either of those files 
     - Makes updating connections simple 
     - Presumably will be needed to connect providers and models 
  4. Create a `./configs/model_registry/...` with `model_model_name.json` for each model 
  5. Create a `./configs/provider_registry/...` with `provider_provider_name.json` for each provider 

### Modularity Questions or Proving Points 

As I'm going through everything and processing it, organizing, condensing files, and setting up stronger modularity like below, I'm left with questions that relate to how the codebase works in referencing files, etc. 

1. How important is the path across the codebase, like if I changed 'the_oc' to something else? 
2. Similarly, changing the name of the agent 
   - For example from OC to OCA 
   - Adding versioning to the name, etc. 
3. Similarly again, changing the directory structure 
   - For example if there was a more obvious way to organize the files that make it clear how they are used with each other 
   - Now and then I learn about a structure that is more beneficial for AI use and updates based on the layout 
4. If I add a new tool with the main files, can / will that be pulled in along with all other tools? 
   - As in, is that end of story? 
   - And if not, what would it take to make that end of story? 
   - This should be the case for all models, providers, and connectors. 
5. Similarly, changing the name of the tool 
   - For example from brave_search to brave_search_v4 I have a feeling might not be okay
   - What parts of the tool JSON *can* be changed? And what holds back the intention of the JSON modularity form being complete? 

### Interfaces 

This is more a point of curiosity that I imagine would come in helpful in the future. In what way could our UI be organized into groups of information that could be cataloged by a CONFIG file JSON system, and would something like that make different UI setup in the future very plug and play? Would it make updating things easier? 

### Error Handling 

- To what degree do our tools have error handling that isn't on the `./utilities/error_handling.py` share file? 
- Is this somewhere that would benefit from having an error handling file for each tool as well? 

## Directory 
```
~/Development/the_oc/...
├── mao_v4.py
├── build/...
│   ├── api/...
│   │   ├── auth.py
│   │   └── service.py
│   ├── interfaces/...
│   │   ├── ui_terminal.py
│   │   └── ui_web.py
│   └── orchestrator/...
│       ├── core.py
│       ├── protocol.md
│       ├── memory.py
│       └── master/...
│           ├── buttons_manager.py
│           ├── cache_system.py
│           ├── error_handling.py
│           ├── model_manager.py
│           └── tool_manager.py
├── components/...
│   ├── ai/...
│   │   ├── connections/...
│   │   │   ├── models_x_tools.json
│   │   │   └── providers_x_models.json
│   │   ├── model_registry/...
│   │   │   ├── model_name.json
│   │   │   └── model_name.json
│   │   └── provider_registry/...
│   │       ├── provider_name.json
│   │       └── provider_name.json
│   └── tools/...
│       ├── tool_name/...
│       │   ├── tool_name.py
│       │   ├── button_tool.py
│       │   ├── model_tool.json
│       │   ├── cache_tool.py
│       │   └── ui_tool.py
│       └── tool_name/...
│           ├── tool_name.py
│           ├── button_tool.py
│           ├── model_tool.json
│           ├── cache_tool.py
│           └── ui_tool.py
└── technical-docs/...
    ├── introduction/...
    │   ├── SPECIFICATIONS.md  <-- an overview with a 'how' focus
    │   ├── MODULAR_PHILOSOPHY.md  <-- all of the important reasons 
    │   └── MODULAR_STRUCTURE.md  <-- modular layout doubling as table of contents
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
    │   ├── INTELLIGENCE.md  <-- model, provider JSON, API 
    │   ├── BEHAVIOR.md  <-- an overview, re: core.py, protocol.md, memory.py 
    │   ├── AGENCY.md  <-- UI, setup scripts, use-cases, workflow JSON config 
    │   ├── ABILITY.md  <-- tools, JSON registry, buttons, cache, error handling 
    │   └── MANAGEMENT.md <-- workflow and file management, ending tasks, recording 
    ├── agents/...
    │   ├── ASSIGNMENT.md <-- get task, token count max reminder and live counter, auto-save docs, 
    │   └── COMPLETION.md <-- calling MAO, reporting, hand-off 
    ├── human/... 
    │   ├── UI_MODULARITY.md 
    │   ├── VERBOSE_ARGS.md
    │   ├── TOOL_CREATION_GUIDE.md 
    │   └── WORKFLOW_SELF_SETUP.md 
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

## Project Structure 

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
