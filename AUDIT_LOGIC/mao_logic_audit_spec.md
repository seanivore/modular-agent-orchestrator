# MAO Logic Audit Specification
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Audit the MAO orchestrator codebase by comparing intended functionality from MAO_FLOW.md against actual implementation
- Clean up over-engineering, hardcoded suggestions, and mock code
- Edit orchestrator files directly to implement the simplest core logic that matches the natural language specifications
- Document the cleaned functionality in plain language for each file

## Mid-Level Objectives

- Compare each piece of functionality described in MAO_FLOW.md against the actual orchestrator code implementation
- Identify mismatches, over-engineering, hardcoded categories/suggestions, and mock code violations
- Edit the orchestrator files directly to remove complexity and implement clean, simple logic
- Create comprehensive documentation of what each file actually does vs what it should do
- Generate a plain language overview of the cleaned system architecture
- Use Memory MCP to track progress and maintain context across potential context window limits

## Implementation Notes

- **CRITICAL**: Edit existing orchestrator files directly rather than creating new files to avoid generating unwanted new code/classes/functions
- **SCOPE BOUNDARY**: Reference `./documentation/10_AI_DEV_INDEX.md` for complete architecture understanding. Focus audit ONLY on orchestrator files plus `mao_v4.py` main entry point. DO NOT audit tool files, config collections, or interface files - those are separate systems
- **CONTEXT NOTE**: ui_terminal.py was deleted during web app pivot - this audit focuses on cleaning orchestrator logic only, not interface implementation
- Must read MAO_FLOW.md completely to understand intended functionality before analyzing code
- Must read ALL orchestrator files listed in prime.md to understand current implementation
- Use Sequential Thinking MCP for complex analysis and decision making
- Update Memory MCP at key milestones to prevent context loss
- Entity names: Use `mao-web` and `mao-logic-audit` for Memory MCP updates
- Follow the "double sequence" pattern: document/understand first, then edit/fix
- Remove ALL hardcoded suggestions, categories, examples, and mock code - trust AI intelligence completely
- Focus on multilingual functionality by eliminating English-specific assumptions

## Context

### Beginning Context
- MAO_FLOW.md document exists with complete natural language specifications
- Orchestrator directory with 20+ files containing over-engineered logic
- Main entry point mao_v4.py with complex routing that needs simplification
- ui_terminal.py was deleted during web app pivot - terminal interface needed for testing
- Current codebase has hardcoded English categories, mock implementations, and excessive complexity
- Files contain "suggestions" and "examples" that break modularity and multilingual support

### Ending Context
- All orchestrator files + mao_v4.py edited to implement clean, simple logic matching MAO_FLOW.md specifications
- Documentation files created explaining what each file does in plain language
- Comprehensive audit report showing before/after comparison
- Clean orchestrator logic ready for separate terminal interface implementation and testing

## Low-Level Tasks
> Ordered from start to finish

1. **Setup and Context Priming**
```
Initialize Sequential Thinking and Memory MCP tools
Create memory entities: `mao-web` and `mao-logic-audit`
Read MAO_FLOW.md completely to understand intended functionality
Read prime.md for development rules and file list
Document initial understanding of intended vs actual functionality
```

2. **Read All Orchestrator Files and Main Entry Point**
```
Read each orchestrator file completely (23 files total):
./mao_v4.py
./orchestrator/__init__.py
./orchestrator/agent_callback.py  
./orchestrator/agent_orchestrator.py
./orchestrator/cache/__init__.py
./orchestrator/cache/cache_system.py
./orchestrator/cli_manager.py
./orchestrator/conversation_bridge.py
./orchestrator/core.py
./orchestrator/error_handling.py
./orchestrator/manager_buttons.py
./orchestrator/manager_models.py
./orchestrator/manager_tools.py
./orchestrator/mcp_hub.py
./orchestrator/memory_mcp.py
./orchestrator/real_time_metrics.py
./orchestrator/settings_manager.py
./orchestrator/system_analytics_manager.py
./orchestrator/user_analytics_manager.py
./orchestrator/user_memory_manager.py
./orchestrator/username_manager.py
./orchestrator/workflow_manager.py
./orchestrator/workflow_state.py

Take detailed notes on current implementation of each file
```

3. **Analysis and Documentation Phase**
```
For each orchestrator file, create analysis document comparing:
- What MAO_FLOW.md says this functionality should do
- What the current code actually does
- Identify specific violations: hardcoded suggestions, mock code, over-engineering
- Document the correct simple logic that should be implemented
- Note AI behavioral guidance and validation methods needed (without examples)

Save analysis documents as:
./AUDIT_LOGIC/DETAILS/<filename>_analysis.md (e.g., core_analysis.md, workflow_manager_analysis.md)

For cache files use: ./AUDIT_LOGIC/DETAILS/cache_<filename>_analysis.md
Group related files logically but maintain individual file analysis
```

4. **Memory MCP Checkpoint - Analysis Complete**
```
Update Memory MCP with analysis findings
Document critical issues found across all files
Secure analysis data against context window loss
Note which files need the most significant changes
```

5. **File Editing Phase - Core System Files**
```
Edit the core orchestrator files to implement clean logic:
- core.py: Remove hardcoded workflow patterns and categories
- conversation_bridge.py: Ensure clean natural language processing  
- agent_orchestrator.py: Implement simple agent coordination
- workflow_manager.py: Clean workflow management logic
- workflow_state.py: Simple state tracking with Memory MCP integration

For each edit:
- Remove ALL hardcoded suggestions, examples, categories
- Remove ALL mock code implementations
- Implement the simplest logic that matches MAO_FLOW.md specifications
- Add AI behavioral guidance as code comments (no examples)
- Preserve error handling and caching patterns
- Maintain integration points with MCP systems
```

6. **File Editing Phase - Manager Files**
```
Edit the manager files to implement clean logic:
- manager_tools.py: Dynamic tool discovery without hardcoded categories
- manager_models.py: Intelligent model selection without suggestions
- manager_buttons.py: Clean code snippet generation
- settings_manager.py: Directory-based settings discovery
- cli_manager.py: CLI command discovery and integration

Remove complexity, hardcoded lists, and mock implementations
Focus on modular, multilingual-friendly approaches
```

7. **File Editing Phase - Support Files**
```
Edit remaining orchestrator files:
- memory_mcp.py: Remove mock code, clean Memory MCP integration
- user_memory_manager.py: Clean user-specific memory management  
- username_manager.py: Update for UserID system to use email or phone (not username)
- mcp_hub.py: Clean MCP integration
- cache/cache_system.py: Clean caching implementation
- All remaining files: Remove mock code and over-engineering
```

8. **Memory MCP Checkpoint - Editing Complete**
```
Update Memory MCP with editing results
Document all changes made to each file
Note any issues encountered during editing
Prepare for final documentation phase
```

10. **Create File Documentation and Conceptual Review**
```
FIRST: Re-read MAO_FLOW.md completely to refresh understanding of the intended app functionality

THEN: For each edited orchestrator file, perform conceptual review:
- Look at the edited code
- Compare it against the written app functionality from MAO_FLOW.md  
- Confirm the file's code is functionally as simple, direct, and complete as necessary with nothing more
- Write in plain language what each file does based on understanding the app

Create documentation explaining in simple terms:
- "This file is what takes all the notes that Mao took during the chat and puts them into workflow JSON objects"
- Brief description of what the file does in the context of the overall app
- Key functions and their purposes in plain language
- How it integrates with other files to create the MAO_FLOW.md experience
- Any important behavioral guidelines for AI usage
- What was removed/simplified during the audit

Save as: AUDIT_LOGIC/DETAILS/<filename>_clean.md (e.g., core_clean.md, workflow_manager_clean.md)
For cache files use: AUDIT_LOGIC/DETAILS/cache_<filename>_clean.md
```

10. **Create System Overview and Final Assessment**
```
Create comprehensive overview document explaining:
- What the audit process discovered about the gap between intended vs actual functionality
- Summary of changes made to each file with before/after complexity comparison
- How the cleaned system now works in the context of MAO_FLOW.md specifications
- Plain language architecture description showing the flow from user login to workflow execution
- Assessment of whether the code is now functionally as simple, direct, and complete as necessary
- Readiness assessment for terminal implementation testing
- Any remaining concerns or recommendations

Save as: AUDIT_LOGIC/SYSTEM_OVERVIEW.md
```

11. **Final Memory MCP Update and Quality Check**
```
Final Memory MCP update with complete results
Review all edited files for consistency
Verify all mock code and hardcoded suggestions removed
Confirm system maintains essential functionality while being dramatically simplified  
Document next steps for terminal implementation testing
```