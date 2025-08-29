**MAO LOGIC AUDIT WORKFLOW COMMAND**

Execute comprehensive logic audit comparing MAO_FLOW.md specifications against orchestrator codebase implementation, then clean up the code to match the intended simple functionality.

**Variables:**
flow_spec: $ARGUMENTS
audit_spec: $ARGUMENTS

**ARGUMENTS PARSING:**
Parse the following arguments from "$ARGUMENTS":
1. `flow_spec` - Path to MAO_FLOW.md document containing intended functionality specifications
2. `audit_spec` - Path to the logic audit specification file defining the audit process

**PHASE 1: CONTEXT PRIMING & PROJECT STATE MANAGEMENT**

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

**PHASE 2: SPECIFICATION DEEP ANALYSIS**

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

**PHASE 3: ORCHESTRATOR CODEBASE COMPLETE ANALYSIS**

**Read All Orchestrator Files and Main Entry Point Completely:**
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

**PHASE 4: ANALYSIS AND COMPARISON DOCUMENTATION**

**File-by-File Analysis Creation:**
Create analysis documents comparing intended vs actual functionality:
- Save as: `./AUDIT_LOGIC/DETAILS/<filename>_analysis.md`
- For cache files: `./AUDIT_LOGIC/DETAILS/cache_<filename>_analysis.md`
- Document specific violations and required changes
- Note AI behavioral guidance needed (without examples)
- Plan the correct simple logic that should be implemented

**Memory MCP Checkpoint - Analysis Complete:**
- Update Memory MCP with comprehensive analysis findings
- Document critical issues found across all files  
- Secure analysis data against context window loss
- Note which files need the most significant changes

**PHASE 5: DIRECT FILE EDITING FOR CLEAN LOGIC**

**CRITICAL EDITING APPROACH**: Edit existing orchestrator files directly rather than creating new files
- This avoids Claude Code's tendency to generate new code/classes/functions when we want to clean existing code
- Work with the actual codebase files to implement clean, simple logic

**Core System Files Editing:**
Edit the most critical orchestrator files:
- `core.py`: Remove hardcoded workflow patterns and categories
- `conversation_bridge.py`: Ensure clean natural language processing
- `agent_orchestrator.py`: Implement simple agent coordination  
- `workflow_manager.py`: Clean workflow management logic
- `workflow_state.py`: Simple state tracking with Memory MCP integration

**Manager Files Editing:**
- `manager_tools.py`: Dynamic tool discovery without hardcoded categories
- `manager_models.py`: Intelligent model selection without suggestions
- `manager_buttons.py`: Clean code snippet generation
- `settings_manager.py`: Directory-based settings discovery
- `cli_manager.py`: CLI command discovery and integration

**Support Files Editing:**
- `memory_mcp.py`: Remove mock code, clean Memory MCP integration
- `user_memory_manager.py`: Clean user-specific memory management
- `username_manager.py`: Update for UserID system (not username)
- `mcp_hub.py`: Clean MCP integration
- `cache/cache_system.py`: Clean caching implementation
- All remaining files: Remove mock code and over-engineering

**Universal Editing Principles:**
- Remove ALL hardcoded suggestions, examples, categories
- Remove ALL mock code implementations
- Implement the simplest logic that matches MAO_FLOW.md specifications
- Add AI behavioral guidance as code comments (no examples)
- Preserve error handling and caching patterns
- Maintain integration points with MCP systems
- Focus on multilingual-friendly approaches

**PHASE 6: CONCEPTUAL REVIEW AND CLEAN DOCUMENTATION**

**Re-read MAO_FLOW.md for Conceptual Verification:**
- Refresh complete understanding of intended app functionality
- Compare edited code against written app functionality specifications
- Confirm each file's code is functionally as simple, direct, and complete as necessary with nothing more

**Plain Language File Documentation:**
Create clean documentation for each edited file:
- "This file is what takes all the notes that Mao took during the chat and puts them into workflow JSON objects"
- Brief description of what the file does in the context of the overall app
- Key functions and their purposes in plain language
- How it integrates with other files to create the MAO_FLOW.md experience
- What was removed/simplified during the audit

Save as: `./AUDIT_LOGIC/DETAILS/<filename>_clean.md`
For cache files: `./AUDIT_LOGIC/DETAILS/cache_<filename>_clean.md`

**PHASE 7: FINAL SYSTEM OVERVIEW AND QUALITY VERIFICATION**

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

**Final Quality Verification:**
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