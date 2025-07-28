# STEP 2: Section Processing Workflow for Documentation
*Standardized process for adding file mapping and architecture to each documentation section*

---

## **CRITICAL CONTEXT**
- **ALL concepts in docs 03-07 have been implemented, audited, validated, tested**
- **Only missing**: Python→TypeScript UI layer + repeating workflows from 07_AUTOMATE_INTELLIGENCE  
- **Goal**: Use documentation creation to fix 09_DEV_PRIMER.md accuracy and create proper implementation guides
- **Challenge**: Context window limitations require systematic one-section-at-a-time approach

---

## **STANDARDIZED SECTION PROCESSING WORKFLOW**
For Each Documentation Section (🔧 Architecture Needed)

### **STEP 1:** Section Analysis
- Read the section narrative to understand what concepts need architecture
- Identify the specific technical requirements (classes, functions, systems)
- Note any cross-references to other sections

### **STEP 2:** File Discovery
Resources to identify relevant files are at the following locations. 

#### **Orchestrator file list** (20 files with descriptions)
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

#### **FILE_BATCH_DEFINITION_PROMPTS/** (6 category groupings)
*These files may be used as a guide, but DO NOT COPY CODE FROM THEM. The AI did not copy accurately at all times*

./modular-agent-orchestrator/documentation/FILE_BATCH_DEFINITIONS/FILE_BATCH_DEFINITION_PROMPTS
├── `CLI_COMMAND_SYSTEM.md` --> defines files & info collected on comprehensive CLI command system 
├── `CONFIGURATION_MANAGEMENT.md` --> files & info collected on comprehensive configuration management system
├── `CORE_SYSTEM_ARCHITECTURE.md` --> files & info collected on the foundational system architecture
├── `TEMPLATES_AND_SCRIPTS.md` --> files & info collected on template system and utility scripts
├── `TOOLS_ECOSYSTEM.md` --> files & info collected to document comprehensive tool ecosystem 
└── *`UI_TYPESCRIPT_INTEGRATION.md`* --> files & info to document local terminal UI integration between TypeScript/Node.js and the Python backend

#### **ARCHITECTURE_SECTIONS/** (6 pattern documents) 
*These files may be used as a guide, but DO NOT COPY CODE FROM THEM. The AI did not copy accurately at all times*

./modular-agent-orchestrator/documentation/FILE_BATCH_DEFINITIONS/ARCHITECTURE_SECTIONS
├── `ARCH_01_Architecture_Overview.md` --> architecture pattern emphasizes subprocess communication, dynamic discovery, privacy
├── `ARCH_02_Core_System_Patterns.md` --> data from everywhere come together for sophisticated processing 
├── `ARCH_03_Tool_Integration_Patterns.md` --> dynamic tool discovery, generation, and execution
├── `ARCH_04_Configuration_Data_Patterns.md` --> configuration management, data storage, and retrieval
├── *`ARCH_05_User_Interface_Patterns.md`* --> local terminal UI integration between TypeScript/Node.js and the Python backend
└── `ARCH_06_Extension_Automation_Patterns.md` --> extension ecosystem map, extension automation patterns

   *Note:*
   - This (UI_TYPESCRIPT_INTEGRATION.md and ARCH_05_User_Interface_Patterns.md) information does not currently exist in the codebase.
   - It has been prepared to create a full implementation plan and implementation.
   - Implementation plan directory: `./versioning/v4_0_0/DEV_IMPL_UI`

#### **FULL_CODEBASE_AUDIT/** results
*These files may be used as a guide, but DO NOT COPY CODE FROM THEM. The AI did not copy accurately at all times*

./modular-agent-orchestrator/tests/FULL_CODEBASE_AUDIT
├── `00_EXECUTIVE_SUMMARY.md`
├── `01_CRITICAL_VIOLATIONS.md`
├── `02_UI_INTEGRATION_MAP.md`
├── `03_DEPENDENCY_MATRIX.md`
├── `04_STANDARDIZATION_REPORT.md`
├── `05_DUPLICATE_CODE_REPORT.md`
└── `07_UPDATED_DOCUMENTATION.md`

The above are in reference to the following directories of files. 

- `./tests/FULL_CODEBASE_AUDIT/file_analysis_reports/`
- `./tests/FULL_CODEBASE_AUDIT/file_batch_definitions/`

### **STEP 3:** Code Verification
- Read the actual implementation files using file system tools
- Verify classes/functions exist and match their descriptions
- Note actual function signatures, file locations, dependencies
- Cross-check against quality audit results

#### **Step 4: Documentation Creation**
- Write accurate architecture section with real code references
- Include actual class names, function signatures, file paths
- Add code examples from real implementation
- Note any implementation gaps (only UI layer + repeating workflows)

#### **Step 5: 09_DEV_PRIMER.md Updates**
- Fix any accuracy issues discovered (like non-existent CommandNameManager)
- Add missing but important classes/functions found
- Update file location references
- Verify import patterns are correct

#### **Step 6: Cross-Reference Validation**
- Ensure section links properly to other documentation sections
- Verify no contradictions with other architecture sections
- Check against Sean's finalized outline for consistency

---

## **RESOURCE MAPPING**

### **Key File Groups for Documentation Sections:**

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

## **VALIDATION CHECKLIST**

For each completed section:
- [ ] All code references point to actual files/functions
- [ ] Function signatures match reality
- [ ] Import paths are correct
- [ ] No non-existent classes referenced
- [ ] 09_DEV_PRIMER.md updated with discoveries
- [ ] Cross-references work with other sections
- [ ] Gaps clearly marked (UI layer + repeating workflows only)

---

## **CONTEXT WINDOW MANAGEMENT**

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

## **SUCCESS METRICS**

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