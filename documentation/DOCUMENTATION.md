# Documentation Preparation Guide

---

## Session Setup 

  1. Start a `sequential_thinking` session 
  2. Review what is written in our Project State use of the `memory` MCP: 
     - Search for exact entity `mao-v4-docs` for project state 
     - Search for exact entity `Mao` for app updates 
  3. Read standardization rule guides created for context priming each session:
     - `CLAUDE.md` 
     - `./documentation/09_DEV_PRIMER.md` 

---

## NOT LOUD IN THE DOCS 

- Types of workflows that Mao can do. ✅ ADDED! 
- Being able to execute tools in parallel and what benefits that can provide in the immediate scope. 💀 CONTEXT WINDOW SMASHED: `./documentation/CONTEXT_WINDOW_SMASHED.md`
- Bigger noise about the "human" buttons ⏳ NOT YET. 

## OTHER THOUGHTS 

- If so many things including analytics are modular, drop in files, then how do we make sure they get touch points for analytics when a user adds new tools themselves? Do we make it part of the necessary build? For every configuration collection file like inspection before upload to share? What about not shared tools they create on their own. 

## Create "HOW TO ADD" For All Configs to README in TEMPLATES 

Trying to figure out how to add a new tool to the system that was a bit more complex (parallel tool use) was so very complicated that we should make this a top priority. We can reference it in the documentation. 

I've added back these old documentation files in case they might help us. 

- `./documentation/OGDOCS_2_SYSTEM_FILES.md`
- `./documentation/OGDOCS_3_ARCHITECTURE.md`
- `./documentation/OGDOCS_4_CONFIG_GUIDE.md`
- `./documentation/OGDOCS_5_FILE_INTEGRITY.md`

- DIRECTORY: `./templates`
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

---

## Intention 

The codebase is rather large and complex which is making it difficult to construct documentation because of AI context window limitations. As a result, I've been struggling, have dealt with multiple issues where Claude Code completely made up code and consistently complained about needing to read files and do things "manually". This led to broken pages of each section of documentation, and an inability to see how to close the gap when there is so much code to keep track of. Initially the idea was to write the text of the documentation first and then add code snippets. By creating the outline first, we can do just that, but without the need to read the codebase at the time of writing to know what code to add and from where to find it. 

### Strategic Content & Writing Style 

* Create documentation that is less dense and more accessible, modeling the style of Anthropic's documentation, for example. 
* Employ a pattern of writing using very brief paragraphs and long-form bullet points, that is proceeded by the code architecture related to the topics just discussed. This then continues with a patter of writing about the tool, then code about what was just written, etc. 
* Still ensure comprehensive coverage of the Mao system 

### Flow of Documentation VS Our Outline/Writing Process 

- **Core documentation** is intended to use the implied narrative, much of which has been written and edited down, to create a flow of the documentation that covers the entirety of the system. All concepts and features are intended to be addressed here. 

- `03_USER_FLOW.md`
- `04_INTERFACE.md`
- `05_ORCHESTRATION.md`
- `06_ANALYTICS_MEMORY.md`
- `07_AUTOMATE_INTELLIGENCE.md`

- **Secondary documentation** is has the following intentions to address after the completion of the core documentation. 
  1. Overview = a more narrative version of a simple table of contents 
  2. Evolving AI = an actual introduction to the product, brand story, and vision 
  3. Reference = comprehensive user-guide references of the system, including commands and other need to reference information 

- `00_OVERVIEW.md`
- `01_EVOLVING_AI.md`
- `02_REFERENCE.md`
- `08_FUTURE_THINKING.md`

- **AI Development Resource** created to help ensure future updates to the Mao codebase are done in a way that might minimize the need for auditing and validation of the codebase after the fact. 
- `09_DEV_PRIMER.md`

### Conceptual Flow of Core Documentation 

End-to-end UX flow --> `03_USER_FLOW.md` --> User creates data...
Inward flow of data --> `04_INTERFACE.md` --> Processing of data `05_ORCHESTRATION.md` --> data sent back out to the User. 
Data + AI = Enhanced UX --> `06_ANALYTICS_MEMORY.md` --> As well as addressing the inherent value of data collection. 
Value builds into climax --> `07_AUTOMATE_INTELLIGENCE.md` --> By showing the sheer scale of what Mao does that other agentic systems do not. 
Pushing that value further --> `08_FUTURE_THINKING.md` --> Showing planned future as well as what is possible. 

---

## Key Steps Updated For This Session

### STEP 1: Outline Building ✅
### STEP 2: Outline Completion ✅

### STEP 3: Writing ⏳
*enter with comprehensive outline, exit with completed documentation as well as implementation docs for trigger system and UI plans* 

**IMPLEMENTATION FOR TRIGGER SYSTEM** 
- `./versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md` ✅
--> Ready for implementation 

**IMPLEMENTATION FOR UI LAYER** 
- `./versioning/v4_0_0/IMPL_UI/UI_IMPLEMENTATION_GUIDE.md` ✅ 
--> Ready for implementation 

**DOCUMENTATION FOR CORE ARCHITECTURE** ⏳ 
--> final review for flow and content accuracy, code placement, etc. 
- `./documentation/03_USER_FLOW.md` ✅
- `./documentation/04_INTERFACE.md` ✅
- `./documentation/05_ORCHESTRATION.md` ✅
- `./documentation/06_ANALYTICS_MEMORY.md` ✅
- `./documentation/07_AUTOMATE_INTELLIGENCE.md` ✅

**DOCUMENTATION FOR SECONDARY ARCHITECTURE** 

1. Developer Context Priming and Reference Documentation 
   - `./documentation/09_DEV_PRIMER.md` 
   - Clean up the document 
   - Make it flow better and easier to read 
   - Code snippets might instead be removed and we reference the actual documentation location instead 
   - File Index 
     - Classes and functions need to be completed 
     - Organized better 
     - Missing file descriptions 
```
File: orchestrator/core.py - "Main brain that turns natural language into intelligent workflows"
Classes: WorkflowOrchestrator, GoalAnalyzer, PhaseBuilder
Functions: def estimate_cost(), def analyze_goal(), def create_workflow_plan()
```

2. Future Implementation Overview of Prepared Updates & Beyond 

* **CLEAN UP THE DOCUMENT** so that it flows and is easier to process 
  - `./documentation/08_FUTURE_THINKING.md`
  - I've added notes after "-->" symbols next to headers; please review and make necessary changes 

* Include the **MULTI-INSTANCE DATA COLLECTION** implementation plan that is ready for development 
  - `./versioning/v4_1_0/IMPL_ANALYTICS/IMPL_ANALYTICS_ACCESSIBILITY.md`
  - `./versioning/v4_1_0/IMPL_ANALYTICS/MULTI_INSTANCE_DATA.md`

* Include the **CLAUDE CODE** option as Mao is ready for development 
  - `./versioning/v4_1_0/IMPL_CLAUDE_CODE/IMPL_CLAUDE_CODE.md` 

* Include the **MULTI-LINGUAL** implementation plan that is ready for development 
  - `./versioning/v4_1_0/IMPL_MULTILINGUAL/IMPL_MULTILINGUAL.md` 

* Include the **SECURE LOGIN** implementation plan that is ready for development as part of the **WEBSITE STOREFRONT** larger plan; initial build will have website pop-up to login (like Claude Code), and then we'll add user space for adding API keys, etc. 
  - `./versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` 
  - `./versioning/v4_1_0/IMPL_WEBSITE/IMPL_WEBSITE_STOREFRONT.md` 

* Include the new **ANTHROPIC TOOLS** ready for development 
  - Bash Command Tool: `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_BASH.md`
  - Parallel Tool Use: `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_PARALLEL.md`
  - Fine-Grained Streaming: `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_FINE_GRAINED_STREAMING.md`

3. The **OVERVIEW** document needs to be updated to reflect the new documentation flow and content 
   - This stands as our "table of contents" but with more compelling reasons to click through each link included 
   - `./documentation/00_OVERVIEW.md`
   - `./documentation/00_OVERVIEW_2.md`
   - I like all of the text under the following headers in the 00_OVERVIEW.md document; I'd like to keep it as is, with adjustments for flow and links to sections throughout the documents: AI 'Assistant' Gets Their Promotion, Mao Is The 'Modular Agent Orchestrator', Security In Longevity, Complete Compatibility & Flexibility, and Cost Innovation Optimization

4. The **EVOLVING AI** document needs to be cleaned up 
   - It stands as the introduction to the product, brand story, and vision 
   - `./documentation/01_EVOLVING_AI.md`
   - `./documentation/01_EVOLVING_AI_2.md`
   - Self-Evolving AI-Project Manager, Exponentially Uncomprehendable (with numbers made visual), Small Players Need To Be Smart (but made shorter), Our Problem Is Clear all the way down to the end right before -- all up to here is the STORY about the brand -- up to the start of "Chapter 1.2" -- which I like these small sections but am curious about if we should look at the content we have across this document and the OVERVIEW document and better organize the content that I do like and want to keep, then build out from there. 

5. The **REFERENCE** document needs to be cleaned up 
   - `./documentation/02_REFERENCE.md`
   - `./documentation/02_REFERENCE_2.md`
   - The items in "_2" are great 
   - The items in the main no addendum file name version are from the old documentation and might have concepts worth keeping 
   - This is best done last, after looking over all the documentation and deciding what could be made small and compact and added to this section 

6. Our **VISUAL AIDS** must be identified and created  
   - As yourself 
     - Which could be done and be the most powerful? 
     - The most helpful? 
     - The most engaging? 
     - Which could be combined to have one super informative visual instead of a few? 
     - Which could be done to be the most visually impressive? 
   - The following are the items that could be created as visual aids: 
```
- Tool architecture diagrams
- Extension ecosystem map
- System architecture diagrams 
- Data flow visualizations
- Integration touch-point maps
- Performance metrics dashboards
- Security and privacy flow charts
- User journey flow diagram
- Scalability demonstration charts
- Orchestrator communication flow diagram showing component information passing
- Cross-session state management showing memory state persistence flow
- Tool integration data exchange flow chart showing how 'button snippets' are created and used
- Flow chart showing analytics trigger points and data flow 
```

---