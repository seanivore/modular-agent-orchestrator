**MAO LOGIC AUDIT WORKFLOW COMMAND**

Execute comprehensive logic audit comparing MAO_FLOW.md specifications against orchestrator codebase implementation, then clean up the code to match the intended simple functionality.

**Variables:**
flow_spec: $ARGUMENTS
audit_spec: $ARGUMENTS

**ARGUMENTS PARSING:**
Parse the following arguments from "$ARGUMENTS":
1. `flow_spec` - Path to MAO_FLOW.md document containing intended functionality specifications
2. `audit_spec` - Path to the logic audit specification file defining the audit process

---

**PHASE 1**
- Complete PHASE 1 for one file at a time, for each of the files listed in STEP 3. After finishing one file, steps 1-5, flag the user. 

To be completely clear, this means: 

  1. Look at the `./AUDIT_LOGIC/DETAILS/...` directory
  2. Compare the `<filename>` in the directory with the list of Logic Audit Files in STEP 3, the next in the list that is not is the directory is next 
  3. Confirm this by using the `memory` MCP Project State where the AI lists the completed and remaining files after each round 
  4. Complete STEP 1 through STEP 5 for that next Logic Audit File 
  5. You will see that STEP 5 is updating the Memory MCP and wiping the context window to start with the next file 

This process is necessary because, to audit each file, the AI must have a full understanding of all the documents you will be reading in STEP 1 through STEP 3 which total about 140,000 tokens. 

* **STEP 1: CONTEXT PRIMING & PROJECT STATE MANAGEMENT**

**Sequential Thinking Initialization:**
- Initialize Sequential Thinking MCP tool for complex analysis and decision making
- Use sequential thinking throughout the process to avoid LLM limitations
- Take time to think hard and choose simple solutions

**Memory MCP Project State Setup:**
- Initialize Memory MCP tool for project state tracking
- Create memory entities: `mao-web` and `mao-logic-audit` 
- Update Memory MCP at key milestones to prevent context loss during potential context window limits
- Follow the protocol from prime.md for detailed notes and memory updates

**Prime Protocol Implementation:**
- Read `prime.md` completely for development rules and orchestrator file list
- Read `CLAUDE.md` for complete development rules including UI Development Guidelines
- Read `./documentation/10_AI_DEV_INDEX.md` for Python backend architecture understanding

* **STEP 2: SPECIFICATION DEEP ANALYSIS**

**MAO_FLOW.md Complete Analysis:**
Read and deeply understand the flow specification at `flow_spec`:
- **User Experience Flow**: Complete natural language specifications of intended app functionality
- **System Logic Requirements**: What each piece of functionality should actually do
- **AI Behavior Guidelines**: How Mao should behave and interact with users
- **Workflow Management**: How projects should be created, managed, and executed
- **UI/UX Context**: Visual design specifications that inform backend logic requirements
- **Validation Requirements**: Methods for validating JSON object variables (without examples)

**Logic Audit Specification Analysis:**
Read and thoroughly analyze the audit specification at `audit_spec`:
- **Process Requirements**: Detailed steps for comparing intended vs actual functionality
- **Documentation Standards**: How to document findings and create clean file descriptions
- **Code Editing Approach**: Direct file editing strategy to avoid generating new code
- **Quality Standards**: Requirements for clean, simple, multilingual-friendly logic
- **Deliverable Structure**: Directory organization and naming conventions for audit outputs

**Critical Analysis Framework:**
- Understand exactly what MAO_FLOW.md says each orchestrator file should do
- Identify the simplest core logic required to implement those specifications
- Note where current code over-engineers or adds unnecessary complexity
- Plan removal of ALL hardcoded suggestions, categories, examples, and mock code
- Design approach for trusting AI intelligence completely without constraints

* **STEP 3: ORCHESTRATOR CODEBASE COMPLETE ANALYSIS**

**Read All Orchestrator Files and Main Entry Point Completely: These are the LOGIC AUDIT FILES**
Following the exact file list from prime.md, plus the main CLI entry point, read each file in full:
- `./mao_v4.py`
- `./orchestrator/__init__.py`
- `./orchestrator/agent_callback.py`
- `./orchestrator/agent_orchestrator.py`
- `./orchestrator/cache/__init__.py`
- `./orchestrator/cache/cache_system.py`
- `./orchestrator/cli_manager.py`
- `./orchestrator/conversation_bridge.py`
- `./orchestrator/core.py`
- `./orchestrator/error_handling.py`
- `./orchestrator/manager_buttons.py`
- `./orchestrator/manager_models.py`
- `./orchestrator/manager_tools.py`
- `./orchestrator/mcp_hub.py`
- `./orchestrator/memory_mcp.py`
- `./orchestrator/real_time_metrics.py`
- `./orchestrator/settings_manager.py`
- `./orchestrator/system_analytics_manager.py`
- `./orchestrator/user_analytics_manager.py`
- `./orchestrator/user_memory_manager.py`
- `./orchestrator/username_manager.py`
- `./orchestrator/workflow_manager.py`
- `./orchestrator/workflow_state.py`

**CRITICAL REQUIREMENT**: Read each file completely - do not cut corners for resource efficiency

**Current Implementation Documentation:**
For each file, take detailed notes on:
- What the current code actually does vs what MAO_FLOW.md specifies
- Specific instances of hardcoded suggestions, categories, or examples
- Mock code implementations that need removal
- Over-engineering that adds unnecessary complexity
- English-specific assumptions that break multilingual functionality
- Areas where the code should trust AI intelligence instead of constraining it

* **STEP 4: ANALYSIS AND COMPARISON DOCUMENTATION**

**File-by-File Analysis Creation:**
Create analysis documents comparing intended vs actual functionality:
- Save as: `./AUDIT_LOGIC/DETAILS/<filename>_analysis.md`
- For cache files: `./AUDIT_LOGIC/DETAILS/cache_<filename>_analysis.md`
- Document specific violations and required changes
- Note AI behavioral guidance needed (without examples)
- Plan the correct simple logic that should be implemented

**STEP 5: Memory MCP Checkpoint - Analysis Complete:**
- Update Memory MCP with details of the completed file 
- Tag entities `mao-web` and `mao-logic-audit` 
- Create a list of COMPLETED FILES, that you add the file name to after each one is finished 
- Update a secondary list a REMAINING FILES maintaining the order of orchestrator Logic Audit Files in STEP 3 
- It should now be clear for a new AI to know where to start and have a general understanding of previous files 

**AT THIS POINT, AFTER EACH FILE IN THE ORCHESTRATOR LOGIC AUDIT FILE LIST, YOU SHOULD:**
  1. Let the User know you have completed a X file 
  2. They will wipe the context window  
  3. A new AI instance and new context window will start at STEP 1 with the next file 
  4. OR the new AI instance will start with STEP 1 in the next phase, PHASE 2 
  5. Do not proceed beyond this point until all 23 ORCHESTRATOR LOGIC AUDIT FILES on the list have been completed 

--- 

**PHASE 2: DIRECT FILE EDITING FOR CLEAN LOGIC**
- Complete PHASE 2 in 3 grouped batches of the 23 Orchestrator Logic Audit Files completed in PHASE 1 
- Complete PHASE 2 for each GROUP 1 through 4 below, one at a time; after finishing a group, STEPS 1 through 4, flag the user

To be completely clear, this means: 

  1. Search the memory MCP project state exact query's `mao-web` and `mao-logic-audit`  to see what group you are working on 
  2. Confirm your group by looking at the files in `./AUDIT_LOGIC/DETAILS/...` to see which "GROUP_X.md" is present and which is not 
  3. If GROUP_1.md is in there and no GROUP_2.md then you have confirmed you need to do GROUP 2, etc. 
  4. Complete STEP 1 through 4 below for all of the files in that GROUP 
  5. You will see that STEP 4 is updating the Memory MCP and wiping the context window to start with the next group or move on 

As mentioned, this process is necessary because, to audit each file, the AI must have a full understanding of all the documents you will be reading in STEP 1 through STEP 3 which total about 140,000 tokens. 

**STEP 1: Prime Protocol Implementation**
- Read `prime.md` completely for development rules and orchestrator file list
- Read `CLAUDE.md` for complete development rules including UI Development Guidelines
- Read `./documentation/10_AI_DEV_INDEX.md` for Python backend architecture understanding

**STEP 2: Read GROUP files** 
  1. Read each of the python files in the group you are completing, group 1 through 3
  2. One GROUP at a time, use each file's analysis in `./AUDIT_LOGIC/DETAILS/` to edit that file 

**STEP 3: Edit the Files**: 
- CRITICAL EDITING APPROACH: Edit existing orchestrator files directly rather than creating new files 
- This is a git branch specifically for this audit, no worries 
- This avoids Claude Code's tendency to generate new code/classes/functions when we want to clean existing code
- Work with the actual codebase files to implement clean, simple logic 
- Use the  `./AUDIT_LOGIC/DETAILS/` for each specific python file in your group, and make all necessary edits 

**GROUP 1: Core System Files Editing:**
Edit the most critical orchestrator files:
- `core.py`: Remove hardcoded workflow patterns and categories
- `conversation_bridge.py`: Ensure clean natural language processing
- `agent_orchestrator.py`: Implement simple agent coordination  
- `workflow_manager.py`: Clean workflow management logic
- `workflow_state.py`: Simple state tracking with Memory MCP integration
- `./mao_v4.py`
- `./orchestrator/__init__.py`

**GROUP 2: Manager Files Editing:**
- `manager_tools.py`: Dynamic tool discovery without hardcoded categories
- `manager_models.py`: Intelligent model selection without suggestions
- `manager_buttons.py`: Clean code snippet generation
- `settings_manager.py`: Directory-based settings discovery
- `cli_manager.py`: CLI command discovery and integration
- `./orchestrator/agent_callback.py`
- `./orchestrator/system_analytics_manager.py`
- `./orchestrator/user_analytics_manager.py`

**GROUP 3: Support Files Editing:**
- `memory_mcp.py`: Remove mock code, clean Memory MCP integration
- `user_memory_manager.py`: Clean user-specific memory management
- `username_manager.py`: Update for UserID system (not username)
- `mcp_hub.py`: Clean MCP integration
- `cache/cache_system.py`: Clean caching implementation
- `./orchestrator/error_handling.py`
- `./orchestrator/cache/__init__.py`
- `./orchestrator/real_time_metrics.py`

**FOR ALL GROUPS: Universal Editing Principles:**
- Remove ALL hardcoded suggestions, examples, categories
- Remove ALL mock code implementations
- Implement the simplest logic that matches MAO_FLOW.md specifications
- Add AI behavioral guidance as code comments (no examples)
- Preserve error handling and caching patterns
- Maintain integration points with MCP systems
- Focus on multilingual-friendly approaches

**STEP 4: Document Group-by-Group Edit Completion**
  1. Create analysis document confirming changes made and to what files in your group 
  2. Document specific violations fixed, note added behavior guidance added (no examples!)
  3. Confirm just the simple logic of each file remains 
  4. Save as `./AUDIT_LOGIC/DETAILS/<GROUP_X>.md` with X= the group number, 1 through 3 

**UPDATE Memory Project State MCP**
  - Create a memory in the MCP indicated what group is complete and what group remains 
  - Tag your memory entry to `mao-web` and `mao-logic-audit` 
  - It should now be clear for a new AI to know what group to start or to move on next 

**AT THIS POINT, AFTER EACH GROUP, YOU SHOULD:**
  1. Let the User know you have completed a X file 
  2. They will wipe the context window 
  3. A new AI instance and new context window will start at STEP 1 with the next GROUP 
  4. OR the new AI instance will start the next phase, PHASE 3, at step 1  
  4. Do not proceed beyond this point until all 3 GROUPS on the list above been completed 

---

**PHASE 3: CONCEPTUAL REVIEW AND CLEAN DOCUMENTATION** 

This is the only phase that may be completed in a single, fresh context window. 

**STEP 1: Re-read MAO_FLOW.md for Conceptual Verification:**
- Refresh complete understanding of intended app functionality
- Compare edited code against written app functionality specifications
- Confirm each file's code is functionally as simple, direct, and complete as necessary with nothing more

**STEP 2: Plain Language File Documentation:**
Review each of the 23 orchestrator files and for each one create clean documentation:

- `./mao_v4.py`
- `./orchestrator/__init__.py`
- `./orchestrator/agent_callback.py`
- `./orchestrator/agent_orchestrator.py`
- `./orchestrator/cache/__init__.py`
- `./orchestrator/cache/cache_system.py`
- `./orchestrator/cli_manager.py`
- `./orchestrator/conversation_bridge.py`
- `./orchestrator/core.py`
- `./orchestrator/error_handling.py`
- `./orchestrator/manager_buttons.py`
- `./orchestrator/manager_models.py`
- `./orchestrator/manager_tools.py`
- `./orchestrator/mcp_hub.py`
- `./orchestrator/memory_mcp.py`
- `./orchestrator/real_time_metrics.py`
- `./orchestrator/settings_manager.py`
- `./orchestrator/system_analytics_manager.py`
- `./orchestrator/user_analytics_manager.py`
- `./orchestrator/user_memory_manager.py`
- `./orchestrator/username_manager.py`
- `./orchestrator/workflow_manager.py`
- `./orchestrator/workflow_state.py`

- "This file is what takes all the notes that Mao took during the chat and puts them into workflow JSON objects"
- Brief description of what the file does in the context of the overall app
- Key functions and their purposes in plain language
- How it integrates with other files to create the MAO_FLOW.md experience
- What was removed/simplified during the audit

Save as: `./AUDIT_LOGIC/DETAILS/<filename>_clean.md`
For cache files: `./AUDIT_LOGIC/DETAILS/cache_<filename>_clean.md`

**STEP 3: FINAL SYSTEM OVERVIEW AND QUALITY VERIFICATION**

**Memory MCP Final Update:**
- Final Memory MCP update with complete results
- Document all changes made and their impact
- Prepare context for next steps in terminal implementation

**System Overview Creation:**
Create comprehensive overview document:
- What the audit process discovered about intended vs actual functionality gaps
- Summary of changes made to each file with before/after complexity comparison
- How the cleaned system now works in context of MAO_FLOW.md specifications
- Plain language architecture description showing flow from user login to workflow execution
- Assessment of whether code is now functionally as simple, direct, and complete as necessary
- Readiness assessment for terminal implementation testing

Save as: `./AUDIT_LOGIC/SYSTEM_OVERVIEW.md`

**STEP 4: Final Quality Verification:**
- Review all edited files for consistency with MAO_FLOW.md specifications
- Verify all mock code and hardcoded suggestions removed
- Confirm system maintains essential functionality while being dramatically simplified
- Validate multilingual capability through removal of English-specific assumptions
- Document next steps for terminal implementation testing

**EXECUTION PRINCIPLES:**

**Double Sequence Pattern:**
- First sequence: Document and understand (analysis phase)
- Second sequence: Edit and verify (implementation and review phase)
- Natural stopping points prevent LLM stream-of-consciousness issues

**Context Preservation Strategy:**
- Use Memory MCP checkpoints throughout process
- Secure all work to prevent context window loss
- Detailed progress documentation for session recovery

**Quality Standards:**
- Trust AI intelligence completely - remove all hardcoded constraints
- Implement simplest logic that satisfies MAO_FLOW.md specifications
- Focus on multilingual functionality and true modularity
- Maintain professional code quality and integration patterns

Execute this logic audit workflow with careful attention to the vision of clean, simple orchestrator code that matches the natural language specifications in MAO_FLOW.md while removing all unnecessary complexity and hardcoded assumptions.