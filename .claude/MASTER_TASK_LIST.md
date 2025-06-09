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
│   ├── connections/         <-- ⚠️ models_x_tools.json, providers_x_models.json eliminate config hardcoding 
│   │   ├── models_x_tools.json
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
    ├── v1-3_SFA
    └── v4_MAO
```

----

## Planning Technical Documentation 

### Strategy Intention 

Simplify the entry point and flow for non-tech users who are just into AI agents. Build out from there. The plan below creates a logic flow that builds on itself, helping non-tech users understand

### Building the Strategy 

1. Structure  
- Place industry buzzwords on the top level for visibility 
- Make the flow of the document mirror the flow of using the tool 

2. Content 
- Go through structure and identify where each file should be added 
- In the first loop, stay at the surface with top-level concepts 
- When the flow loops, add in the more in-depth and under-the-hood concepts  

3. File Review 
- Review files as they're added to the document 
- Some may need to be updated depending on how they reference other files 
- Documentation should explain how the code references the many modular files 

4. Finalization 
- Complete the documentation before the remaining build tasks 
- Use building the documentation as a way to create our "final stretch" task list 

### Document Outline 

- **1.INTRODUCTION** 
  - About agents; what makes a true agentic workflow 
    - Explain our structure, using an Orchestrator; 'What is MAO?' 
    - Types of common workflows 
    - Examples of tasks in each type of workflow  
  - Overview of what MAO does; role of the orchestrator 
    - Where does the human fit in 
    - Build together or JSON/setup script 
    - How planned is the workflow, as in how much agency MAO has 
    - Role of the agent; how they're chosen
  - Activation of workflow 
    - User input of already prepared workflow 
    - What MAO prepares for agent(s)
    - Handoff to agent(s) 
  - Management of workflow 
    - Describe the Agent's flow 
    - MAO's role between agents 
  - MAO's workflow agency and mechanics 
    - Changes and updates MAO might plan on needing to make 
    - Records the agent's report in their workflow report 
    - Updating memory history 
    - Saving documents in the Files API as "working" documents 
    - Human touch-point if planned to have one; how to use it 
  - Completion of a workflow 
    - What different things this could mean 
    - Durations of workflows; many human touch-points, maybe over weeks 
    - Short workflow, example of workflows we had the SFA do 

- **2.{SUBSEQUENT-SECTIONS}**

### Outline Heading Numbering 

To maintain a proper order of documents in the directory, please number the headings by using a single digit number for the top level (I'm assuming that we won't have more than 9 sections). Subsections get a decimal point, i.e. 1.1, 1.2, etc. 

### Recent Documentation Attempt 

Last session I attempted to create documentation. We used a creative 'biological' metaphor to describe and categorize the different functions and flow of MAO. I was planning on using them and just toning them down quite a bit; as in, I like the metaphor but the AI leaned in a bit more than necessary, where it starts to get cringe. 

That reason I'm not starting with these documents in this session's task introduction is because I can't for the life of me figure out how they intended the files to be grouped and ordered. I think this is because they saw an example of the documentation structure I had created in the Project Directory Tree and might have thought that those were actual, complete files? But I wasn't even sure if I was being comprehensive enough, etc. as I had just created them to illustrate the metaphorical concept and how the actual files could be grouped in that kind of structure. 

We can totally use as much of them as we want, but I have not been able to get through all of them as they are detailed. Detailed but somehow missing the actual code examples, etc. It seems like they just sort of referenced the actual files in the architecture. But you'll note that there are also files the note that are note part of the architecture and are presumably part of that AI's mental documentation model. 

`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/0.MAO_DOCS.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/1.MODULAR_AGENT_ORCHESTRATOR.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/2.SETUP_GUIDE.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/3.CORE_ENGINE.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/4.CORE_TOOLKIT.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/5.MODEL_SELECTION.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/6.AGENTIC_PLANNING.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/7.WORKFLOW_MANAGEMENT.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/8.AGENT_DELEGATION.md`

### Other Documentation Resources 

This is what is left of the various implementation plans. We had quite a few. I tried to pull them together and ended up with a few documents. 

This one identifies some fixes that need to be made to the codebase. It then walks through the double checking that we did of each file looking for "print()" functions that should be moved to the UI layer. I though leaving that might be helpful because we should go through them each again and make sure they all make full sense with the new codebase structure and file name changes. 
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/PROJECT_STATUS.md`

This is some of the remaining next steps from the implementation plan. Notably, it is missing implementing Files API, Code 
Execution, and the API MCP Connector, all of which are built in tools from Anthropic that were released with Sonnet 4. 
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/NEXT_STEPS.md`

I have details for the three missing pieces I mentioned here. 
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_API_MCP_CONNECT.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_CODE_EXECUTION.md`
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_FILES_API.md`

This is the messiest of the documents but possibly the most important. The reason it is messy is because I read through all the old implementation plans can pulled what was still accurate, any examples or phrasing I liked, etc. and placed it in this document. I did my *human* best at trying to place things in a logical order. I also wrote about the philosophy for a while so please don't delete that. 
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/UPDATE_SPEC.md` 

Presumably all of these documents will end up in our documentation. Let's keep all documents in the versioning-docs directory. But please indicate that the top of each when they've been processed and added to the documentation so we can keep track of what is left to be added. 

### Directions 

1. Please build out the documentation outline as detailed above. 
   - I'd like to review before you start expanding on the different sections. 
   - The structure should be according to the 'Building the Strategy' above 
2. Add a reference to where each file would be explained throughout the outline 
   - At this point is when I'd like to review 
   - I have some other files I can plug in that should help building out the documentation 
3. Then review the 'Recent Documentation Attempt' 
   - Integrate what is useful to start building out the documentation 
   - I am interested in potentially using some of the metaphorical concept structure from the previous attempt 
   - But I leave that up to you because I really just got lost in them 
   - I'll review after step three, before we add in the most technical details 
4. Then review the 'Other Documentation Resources' 
   - This is probably where we'll find the bulk of the technical details prepared 
   - As you proceed through, please leave spaces for spots where we need to add technical details, or fill them in as you go. 
5. I was going to separate session 14 from this document, but 
   - It seems likely that whatever is below this section in session 15 we might need to add to the documentation 
   - Please keep me in the loop after each step of the documentation build 
6. We'll add in the most technical details last 
   - Filling in the gaps! Is what I'd call this phase
   - We want to make sure it has that flow described at the start
   - Makes sure everything is organized logically 
   - Reference other parts of the documentation as needed, etc. you know the drill 
   - Let's make these documents just like WOW! 
7. At this point we'll also want to be creating our final stretch task list because we'll have a comprehensive overview of everything 
   - Anthropic recently provided access to "10-40 prompts" of Claude Code with the Claude OS Pro subscription I have 
   - I've added the Claude Code documentation to your Cursor documents that are indexed 
   - I've also added the Cursor Rules documentation 
   - I mention this because after we're done we should create real cursor rules for this project (the AI previously used the legacy format)
   - And because I think it might be worth setting up our remaining home stretch task list as a set of prompts; I'm curious about using Claude Code because I watch IndyDevDan use it a lot, but I need assistance because I write a lot and he writes very concise prompts that are actually prompts about writing prompts that they pass off to multiple instances of Claude Code to run in parallel. Anyway just mentioning this to be aware, we'll obviously chat before we do anything. 

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
