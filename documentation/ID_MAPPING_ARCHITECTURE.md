# STEP 2: Section Processing Workflow for Documentation
*Standardized process for adding file mapping and architecture to each documentation section*

---

## Core Documentation Files 
*All concepts should be covered within these middle few files of the documentation suite* 

  - `./documentation/03_USER_FLOW.md`
  - `./documentation/04_INTERFACE.md`
  - `./documentation/05_ORCHESTRATION.md`
  - `./documentation/06_ANALYTICS_MEMORY.md`
  - `./documentation/07_AUTOMATE_INTELLIGENCE.md`

---

## Finding Codebase Architecture Snippets 

  1. All but two concepts in docs 03-07 have been implemented, audited, validated, tested
     - We can and should find and pull directly from the codebase in all cases 
     - Implementation plans might help direct us to the correct file, but use the codebase directly 

  2. Exception #1: Python→TypeScript UI layer 
     - We have documents defining the plans 
     - The full implementation plan should provide all needed code snippets 
     - Implementation plan: `./versioning/v4_0_0/IMPL_UI/UI_IMPLEMENTATION_GUIDE.md` 
     - Make sure anything already in `./documentation/04_INTERFACE.md` is accurate as above 
     - Any other details can be found in the UI implementation directory: `./versioning/v4_0_0/IMPL_UI/`

  3. Exception #2: Repeating workflows 
     - All logic has been detailed in `07_AUTOMATE_INTELLIGENCE.md` 
     - We need to create a full implementation plan based on the logic 
     - Please review and give feedback if it is missing anything or is not clear 
     - The same process as creating the /setup command and setup scripts from the normal workflow should be followed 
     - Each repeating workflow just has a different output format 
     - And there is a single new JSON file for repeating workflows that is the same for all types 

- **PRIMARY TASK**: Complete documentation for all concepts in docs 03-07 according to the outline in `./documentation/CONTENT_ID_OUTLINE.md`
- **SECONDARY GOAL**: Use documentation creation to validate and fix `09_DEV_PRIMER.md` accuracy (step 5)

---

## Standardized Section Processing Workflow 
Follow this flow for each concept that needs to be covered, in each section of the documentation. 

### STEP 1:Section Analysis
- Read the section narrative to understand what concepts need architecture
- Identify the specific technical requirements (classes, functions, systems)
- Note any cross-references to other sections

### STEP 2: File Discovery
Resources to identify relevant files are at the following locations. 

#### **Orchestrator file list** (20+ files with descriptions)
*These are actual codebase files and the ONLY place that any code should be copied from to place in documentation*

./modular-agent-orchestrator/orchestrator/
├── `__init__.py` --> orchestration package modular AI workflow system
├── `agent_callback.py` --> handles agent returns, execution results, and workflow progression
├── `agent_orchestrator.py` --> coordinates agent handoffs with context packages via Files API
├── `cache` --> our dual-layer hybrid caching system 
│   ├── `__init__.py` --> universal caching package for everything 
│   └── `cache_system.py` --> Files API for workflow handoffs; local cache for permanence; fingerprinting
├── `cli_manager.py` --> CLI command discovery, integration of slash commands to orchestrator functionality
├── `conversation_bridge.py` --> Converts natural language goals into executable custom commands
├── `core.py` --> main brain that turns natural language into intelligent workflows
├── `error_handling.py` --> Professional error handling patterns for universal files 
├── `manager_buttons.py` --> "Button" code snippet generator; avoids SDK usage 
├── `manager_models.py` --> Loads JSON configs and provides intelligent model selection
├── `manager_tools.py` --> Dynamic tool discovery; suggestion based on goals, not hardcoded categories
├── `mcp_hub.py` --> Integrates Memory MCP, Files API, and MCP Connector into unified system
├── `memory_mcp.py` --> Provides workflow state persistence for context tracking, state management, session recovery
├── `protocol.md` --> *empty file; guidelines for Mao chat interactions; behavior protocol* 
├── `real_time_metrics.py` --> Provides live data for UI components; no mock data allowed
├── `settings_manager.py` --> settings discovery, management; directory-based scanning of individual setting files
├── `system_analytics_manager.py` --> tracks system-wide performance metrics with full anonymization and privacy compliance
├── `user_analytics_manager.py` --> user-specific analytics with GDPR compliance; dynamic tool discovery
├── `user_memory_manager.py` --> user-specific memory storage, retrieval, management with Memory MCP integration
├── `username_manager.py` --> user creation, session persistence, settings integration
├── `workflow_manager.py` --> workflow ID generation, discovery, tracking
└── `workflow_state.py` --> simple state tracking with Memory MCP integration

#### **Old Implementation Documents** 
*These are the implementation plans or confirmations that we have saved; however, you must still confirm the code in the actual codebase files* 

- CLI COMMANDS: `./versioning/v4_0_0/IMPL_CLI_COMMANDS/CLI_COMMAND_STANDARDIZATION.md`
- USER CONFIG SETUP: `./versioning/v4_0_0/IMPL_OG_WORKFLOW_SETUP/IMPL_USER_CONFIG_SETUP_SCRIPT.md`
- WORKFLOW CREATION: `./versioning/v4_0_0/IMPL_OG_WORKFLOW_SETUP/IMPL_WORKFLOW_CREATION.md`
- INTEGRATION POINTS: `./versioning/v4_0_0/IMPL_OG_WORKFLOW_SETUP/INTEGRATION_POINTS_BY_FILE.md`
- USER ID CONFIG SETUP: `./versioning/v4_0_0/IMPL_OG_WORKFLOW_SETUP/USER_ID_CONFIG_SETUP.md`
- WORKFLOW ID SETUP: `./versioning/v4_0_0/IMPL_OG_WORKFLOW_SETUP/WORKFLOW_ID_SETUP.md`

#### **New Implementation Documents** 
*These are the implementation plans that we are creating for the next steps* 

- UI LAYER: `./versioning/v4_0_0/IMPL_UI/UI_IMPLEMENTATION_GUIDE.md`
- TRIGGER WORKFLOWS: `./versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md`
- TIMER PROPOSED SKETCH: `./versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/timer_architecture.md`

### STEP 3: Code Verification
- Read the actual codebase files using file system tools
- Verify classes/functions exist and match their descriptions
- Note actual function signatures, file locations, dependencies
- Cross-check against quality audit results

### STEP 4: Documentation Creation
- Write accurate architecture section with real code references
- Include actual class names, function signatures, file paths
- Add code examples from real implementation
- Note any implementation gaps (only UI layer + repeating workflows)

### STEP 5: 09_DEV_PRIMER.md Updates
- Look out for items to fix (like non-existent CommandNameManager)
- For each relevant file: purpose + all classes + all functions
- Add any touch-points, dependencies, or integration notes
- Create robust reference that prevents AI code hallucination
- Verify import patterns are correct

```
File: orchestrator/core.py - "Main brain that turns natural language into intelligent workflows"
Classes: WorkflowOrchestrator, GoalAnalyzer, PhaseBuilder
Functions: def estimate_cost(), def analyze_goal(), def create_workflow_plan()
```

### STEP 6: Cross-Reference Validation
- Ensure section links properly to other documentation sections
- Verify no contradictions with other architecture sections
- Check against Sean's finalized outline for consistency

---

## Resource Mapping

### Key File Groups for Documentation Sections:

**V. ORCHESTRATION (Core Magic)**
- Primary: `orchestrator/core.py`, `conversation_bridge.py`, `workflow_manager.py`
- Supporting: `agent_orchestrator.py`, `workflow_state.py`, `mcp_hub.py`
- Cache: `cache/cache_system.py`
- Managers: `manager_models.py`, `manager_tools.py`, `manager_buttons.py`

**IV. INTERFACE (CLI Architecture Additions)**
- Primary: `cli_manager.py`, `interfaces/ui_terminal.py`
- CLI Configs: `configs/cli/*/` structure
- Supporting: `settings_manager.py`, `username_manager.py`

**III. USER_FLOW (Setup Script Architecture Additions)**
- Scripts: `scripts/workflow_setup/`, `scripts/user_id_generator/`
- Memory: `memory_mcp.py`, `user_memory_manager.py`
- Supporting: `conversation_bridge.py`

**VII. AUTOMATE_INTELLIGENCE (Repeating Workflows - Implementation Needed)**
- Reference existing: `workflow_manager.py`, setup scripts
- New implementation needed: Calendaring system, triggered execution

---

## Validation Checklist

For each completed section:
- [ ] All code references point to actual files/functions
- [ ] Function signatures match reality
- [ ] Import paths are correct
- [ ] No non-existent classes referenced
- [ ] 09_DEV_PRIMER.md updated with discoveries
- [ ] Cross-references work with other sections
- [ ] Gaps clearly marked (UI layer + repeating workflows only)

---

## Context Window Management

**Per Session Approach:**
1. Choose ONE documentation section (e.g., V-M "Goal Analysis")
2. Read ONLY the 3-5 files relevant to that section
3. Complete entire workflow for that section
4. Save progress and section completion status
5. Next session: Pick up with next section

**Session Handoff Requirements:**
- Update mao-v4-docs memory with section completion status
- Note any 09_DEV_PRIMER.md fixes made
- Flag any cross-section dependencies discovered
- Document any implementation gaps found

---

## Success Metrics

**Per Section:**
- Architecture section complete with real code references
- 09_DEV_PRIMER.md accuracy improved
- No broken references or non-existent classes

**Overall Project:**
- All 🔧 sections have accurate implementation details
- 09_DEV_PRIMER.md is completely accurate
- Clear separation between "exists" vs "needs implementation"
- Ready for UI layer development and repeating workflow implementation

---

*This workflow ensures systematic, accurate documentation while working within context window constraints and fixing accumulated accuracy issues.*