# UI Foundation Build Planning 

## Overview, Goals, and Process 

* Our dated foundation UI build plan: 
  --> Written before implementing core systems; CLI commands, User ID, Workflow Systems, app settings, etc. The AI attempted an update of the SPEC requirements but ended up neglecting more than a few of the top level requirements. The result was unappealing, too buggy to use, and not representative of our brand, the apps potential, nor our dedication to strict standards stemming from our modular philosophy and the detailed nature it requires. 

* We're writing a new UI build plan: 
  --> The following steps are essential to ensure that our new UI build plan is comprehensive, detailed, and up to date. Within the steps below we will also build out the visual descriptions using wireframes and other aids. This will be build using TypeScript and Node.js. The steps below are to ensure that the UI foundation build plan is complete and up to date

* Our overarching goal: 
  --> We need to situate ourselves to build the best possible UI first build we can. We will do everything in our power to avoid as many bugs as possible. We will do everything we can think of to ensure our aesthetic vision is as close to fully realized for a first build as possible. Our first build will be functional. 

* Using our resources intelligently: 
  --> Maximize agentic work so that we can be mindful of the context window issues using Claude OS app; this is not an issue with Claude Code. Note that there is no such thing as something taking too long, a task just is what it is. Every bit of code written or reviewed must be done will paced, grounded intention; use sequential thinking before reach step, document every move before acting, during, and after, both in the Memory MCP Project State tool, and in written form form our 'Versioning' directory. Write or review code as if it is about to be published and sold to the public. There is no such thing as a "TO DO" written in the code --> do it now. You are writing code for a product, not a public audience or repository. You do not need to brand everything with 'Mao' or even 'Modular Agent Orchestrator XYZ File' --> be more specific and precise by being more deliberate and concise. 

* Our pragmatic process: 
  --> Each task below will be organized with fuller, more specific, details. They will be broken down into managable chunks; managable in that we can ensure the number of steps and checks necessary to ensure perfection are manageable. We do not work ahead on other sections out of eagerness; be stoic. You are Virgo, the Editor, Earth. 
  --> This document will serve as our single source of truth, carefully updated with each iteration. The Memory MCP Project State tool should only be used for conceptual information, progress updates, and references back to this document. This prevents issues where LLMs retain outdated information during code audits, which previously required extensive re-auditing.

* The result of this work: 
  --> We will be left with a collection of detailed information that will then be synthesized into our comprehensive UI build plan update. 

---

## Build Steps 

## Step 1: Technical Architecture Clarity
**Task:** Create a technical description of what the plan should look like, what tech will be used, code, etc. so that we can avoid any confusion like the first build where TypeScript and Node.js should have been used, but were not. 
**Approach:** Conversational planning → Artifact creation  
**Delegation:** Manual (requires architectural decisions)  
**Resources:** 
  - `MAO_APP_UI_IMPLEMENTATION.md`
  - `foundation_spec.md`
  - `advanced_spec.md`
**Deliverable:** Complete technical specification artifact for NEXT_STEPS.md  
**Goal:** Prevent any tech stack confusion like previous implementation 

## Step 2: CLI Command Integration Analysis 
**Task:** Identify clear list of relevant newly created files and touch-points, then create plan on how to integrate into UI plan including what needs to be planned for. 
**Approach:** Review scope → Delegate to Claude Code  
**Delegation:** Agentic (systematic file analysis)  
**Resources:** 
  - `CLI_COMMAND_STANDARDIZATION_PLAN.md`
**Deliverable:** Integration touchpoint mapping document  
**Goal:** Identify all 27 remaining CLI commands and their integration needs

## Step 3A: Auto-Complete 
**Task:** Describe the UX and UI that should result from implementation and then create plan on how to integrate into UI plan including what needs to be planned for. 
**Approach:** Requirements analysis → Implementation planning  
**Delegation:** Mixed (planning manual, implementation agentic)  
**Resources:** 
  - `CLI_AUTOCOMPLETE_IMPLEMENTATION.md` --> this is the one we started last week that ended up making more sense as being part of the larger UI Foundation build plan. As such, while we should definitely review it at this point, that will likely be all that is needed until we go to compile the comprehensive build plan after completing all ofther steps. 
**Deliverable:** UX/UI specification for new functionality  
**Goal:** Plan how these features integrate into conversation-driven interface

## Step 3B: Auto-Updates Integration
**Task:** First, we need to fully understand how this works exactly. Then we need to create all of the necessary templates and README for each describing what is necessary to create that new config. Does the auto-documentation know what it needs, or is this something that we hand off to Mao? Either way it seems like Mao should end up being the expert on this matter. Possibly most importantly, what are all the touch-points for each config file? We should also include audit information or task Mao with delegating an audit of any new config submitted. Eventually we can also have Mao delegate the posting of configs to our collection for subscribers to use. 
**Approach:** Requirements analysis → Implementation planning  
**Delegation:** Mixed (planning manual, implementation agentic)  
**Resources:** 
  - `GITHUB_INTEGRATION_SETUP.md` --> definitely needs us to review it; I have a feeling much of it is manual; more of a guide than implementation. 
**Deliverable:** UX/UI specification for new functionality  
**Goal:** Plan how these features integrate into conversation-driven interface

```
~/Development/modular-agent-orchestrator/templates/
├── cli_commands        ← See below for all files necessary to create a new command; also needs a README 
│   └── cli_command.json
├── models                ← needs a README 
│   └── model.json
├── providers                ← needs a README 
│   └── provider.json
├── settings                ← needs a README 
│   └── setting_name_app_settings.json
├── tools                ← needs a README 
│   ├── tool_config_template.json
│   ├── tool.json
│   ├── tool.py
│   └── ui_tool.py
├── users                ← needs a README 
│   └── user_username.json
└── workflows
    ├── example-workflow_handoff_config.json
    ├── example-workflow_phase_config.json
    ├── example-workflow_workflow_config.json
    └── README.md
```

```
configs/cli/[command]/
├── [command].py          ← Logic file with full MAO standardization  
├── [command].json        ← Enhanced config (already exists)
└── ui_[command].py       ← UI file for command display patterns
```

## Step 4: Workflow & User System Integration
**Task:** The user and workflow file were a handful of tasks that included everything from app configuration settings, to workflow creation. We need to fully document EVERY touch-point for EVERY file in our codebase. This section is for Workflow & User System Integration with the UI, which is a large bulk of everything. The results of this section will be needed the documentation task and then the testing and validation task, as this is where we will need be be more thorough than just the UI touch-points, important, proper class names, etc. 
**Approach:** Document review → Integration mapping  
**Delegation:** Manual (requires understanding of Tasks 1-4)  
**Resources:** 
  - `TASK_2_CACHE_USER_CONFIG_SETUP.md`
  - `TASK_2_USERNAME_CONFIG_COMPLETE.md`
  - `TASK_3_INTEGRATION_POINTS.md`
  - `TASK_3_WORKFLOW_ID_COMPLETE.md`
  - `TASK_4_WORKFLOW_CREATION_COMPLETE.md`
  - `MAO_FILE_STANDARDIZATION_RULES.md`
  - List of all the orchestrator files in documentation section below  
**Deliverable:** Comprehensive integration requirements document  
**Goal:** Ensure all previous work properly connects to UI

## Step 5: Technical Documentation Completion & Audit 
**Task:** The intention of this step is multi-pronged. We need to ensure that we have a complete understanding of all files and their roles, identify any overlap or gaps, and create a plan that ensures all touch-points are implemented across the entire source code, NOT just the UI as in the previous step. The reprecussions of not one is the same as not doing the other when it comes to running the UI. The other purpose is that these orchestrator files and other files all need an audit; I saw hardcoding in the CLI files below, and I'm sure we'll find other issues. The third prong is ensuring that our code is as simple implement as possible. We have come across SO MANY redundancies in files and across files which is just unacceptable. We already have the world critisizing and watching any AI-Pair programming, and "pointless code" or adding a funciton instead of import and vice versa is something they specifically call out. We will not be the butt of their joke. We just won't publish if we cannot assure this essential standard. The FINAL prong is simple: We need our documentation to be complete and up to date. Much of it will likely be easier to rewrite than to edit. But I am moving this task up because it needs to be done before the rest of the steps. 
**Approach:** Documentation audit → Updates  
**Delegation:** Agentic (systematic documentation work)  
**Resources:** 
  - `MAO_FILE_STANDARDIZATION_RULES.md`
  - List of all the orchestrator files in documentation section below  
**Deliverable:** Complete and current technical docs  
**Goal:** Ensure everything is properly documented

```
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
```

## Step 6: Visual Brand & Wireframe Creation
**Task:** We need to reivew and improve our visual brand identity document especially to make it clearer and more decisive; there must be no question as to what a certain bit of typography should look like. Then we need to go through our New User Flow document and turn it into a wire frame. It is imporant to include both by illustration and directly, that the VISUALS and the build of the app ARE THE TYPOGRAPHY. In the previous UI there was framing and containers. We need to REMEMBER that this UI is for a terminal and we need to design it to play welL with ANYONE'S terminal design. Claude Code's didn't change a single bit of my zsh terminal settings and I think that is extremely important. The initial build had backgrounds which is pointless. We have no idea what the background of the users terminal is and we definitely do not want to overwrite it. Nor do we want to overwrite their primary color. 
**Approach:** Review → Wireframe design → Validation  
**Delegation:** Manual (creative/design decisions)  
**Resources:** 
  - `MAO_VISUAL_BRAND_IDENTITY.md`
  - `NEW_USER_FLOW.md` 
**Deliverable:** Complete wireframe with zero ambiguity  
**Goal:** Prevent any "navigation menu" architecture mistakes

## Step 7: Comprehensive Plan Assembly
**Task:** Through all the points above, we have pulled what is best from the origiginal plan, and we have detailed what is needed in our final plan. Now we need to put it all together. Much of this might overlap with the previous step when creating a wire frame. But as we do this we also need to ask ourself if anything is missing, should be expanded on, etc. 
**Approach:** Synthesize all above into unified plan  
**Delegation:** Manual (requires architectural oversight)  
**Resources:** 
  - All of the above information from each step 
**Deliverable:** Master UI build specification  
**Goal:** Single source of truth for implementation

## Step 8: Plan Review & Refinement
**Task:** This is when you stop working and stop thinking about everything related to the task at hand. If there are big undecided questions, write those clearly, and then stop and move on. This is how the best work is done. It comes when it is ready. 
**Approach:** Step back → Critical review → Refinements  
**Delegation:** Manual (requires judgment and experience)  
**Resources:** 
  - Our cognative abilities  
**Deliverable:** Validated and refined plan  
**Goal:** Quality gate before implementation

## Step 9: Testing & Validation Planning
**Task:** Okay, not going to lie, this freaks me out a lot after experiencing the UI of the previous build. You could not do one single thing without hitting a bug, which I made a report for, then gave to the AI, who fixed it, then I documented the patch. I AM NOT DOING THIS. Idk what is the norm, what is possible, or if we need to get innovative with new AI tools, but we aren't dealing with that. This is why we are being a thorough from the start as possible: To hopefully avoid that number of bugs. But we cannot plan for success, we must plan for all possible contingencies, and the big terrible one is a bug at every step. What do we do about it. 
**Approach:** Strategy design → Test plan creation  
**Delegation:** Mixed (strategy manual, test creation agentic)  
**Resources:** 
  - AI wisdom 
  - Whatever we need   
**Deliverable:** Comprehensive testing strategy  
**Goal:** Prevent bugs that plagued previous implementation

## Step 10: Claude Code SPEC Creation
**Task:** Not only do we need to create the new SPECS, but we need to decide on which custom command workflow to use. Here I want to prepare our plan for the SPECS and see if there is a command to improve, then have Claude Code review it in full. They had a lot of interest in our custom command workflows, like, got really excited about using them. They also were able to identify when they should be specific to the use case and when they don't need to be. I am imagining that this will be more than a couple commands and handful of SPECS. Sort of like the funnel command idea, but I think we'll end up building them specifically for the use case for this project. 
**Approach:** Convert plan to executable specifications  
**Delegation:** Manual (requires understanding of Claude Code patterns)  
**Resources:** 
  - The "resources" file in .claude folder with SPECS for examples 
  - Our commands in the .claude/commands directory 
  - Claude Code themselves 
**Deliverable:** Ready-to-execute Claude Code specifications  
**Goal:** Enable efficient agentic implementation 