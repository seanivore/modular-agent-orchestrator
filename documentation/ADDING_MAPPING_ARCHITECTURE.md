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

### **For Each Documentation Section (🔧 Architecture Needed):**

#### **Step 1: Section Analysis**
- Read the section narrative to understand what concepts need architecture
- Identify the specific technical requirements (classes, functions, systems)
- Note any cross-references to other sections

#### **Step 2: File Discovery** 
Use Sean's resources to identify relevant files:
- **Orchestrator file list** (20 files with descriptions)
- **FILE_BATCH_DEFINITION_PROMPTS/** (6 category groupings)
- **ARCHITECTURE_SECTIONS/** (6 pattern documents) 
- **FULL_CODEBASE_AUDIT/** results
- **QUALITY_VALIDATOR_RESULTS/** findings

#### **Step 3: Code Verification**
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