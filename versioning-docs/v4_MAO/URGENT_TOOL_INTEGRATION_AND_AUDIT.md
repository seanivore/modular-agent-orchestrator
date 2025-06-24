# URGENT TOOL INTEGRATION AND AUDIT 

## **PHASE 1** Incomplete implementation: Tool Integration Framework Plan 
   - Plan file: `./versioning-docs/v4_MAO/1.3_TOOL_INTEGRATION_FRAMEWORK_PLAN.md`
   - It references 'human buttons' but we purged that terminology from the codebase 

### Missing, Misplaced, And Incomplete Tool Files 

1. Currently the only file in the code_execution directory is the logic file `./tools/code_execution/code_execution.py` 
   - This file has a lot of strange things in it 
   - TODO: Load actual tool implementation
     - `tool_module = importlib.import_module(f"tools.{tool_name}.button_{tool_name}")`
     - `return tool_module.get_implementation_code()`
   - It then says 
      - "In real implementation, this would:
        1. Use Claude Code Execution tool
        2. Inject environment variables
        3. Capture output and files
        4. Return structured results"
     - This makes no sense to me because "Claude Code" and the execution tool have nothing to do with each other. Code Execution Tool is a tool that came out with Claude 4.0. 
   - This seems potentially related to the implementation plan. The plan was not completed and the code execution tool is clearly not complete.
   - Please review the plan and the code execution tool and make sure that they are complete. 

2. Should this tool be in the `./tools/` directory? 
   - Files API is in Orchestrator 
   - MCP Connector API is in Orchestrator 
   - I think the answer is in if the agents will use it or not 

3. No matter where it lives, Code Execution tool needs 
   - Propper cache management and analysis 
   - Proper cost calculations 
   - Proper error handling 

4. Why is the MCP Connector API not in the `./tools/` directory? 
   - I assumed the separation was that tools that agents use are in the `./tools/` directory and tools that are used by the orchestrator are in the `./orchestrator/` directory. 
   - But MCP Connector API is in the `./orchestrator/` directory, and this is for ALL MODEL CONTEXT PROVIDER SERVER TOOLS. Meaning that it is a tool that agents use. 
   - It seems like it might have been placed in Orchestrator just because of the use of the Memory MCP tool
   - Regardless, this needs to be fixed. 

5. When the MCP Connector API tool is moved to the `./tools/` directory, it needs 
   - Proper cache management and analysis 
   - Proper cost calculations 
   - Proper error handling 

6. No matter where the Files API tool lives, it needs 
   - Proper cache management and analysis 
   - Proper cost calculations 
   - Proper error handling 

### Tool Logic File Audit 

In figuring out what was going on with the MCP connector, the Code Execution tool, and the Files API, I came across a lot of inconsistencies in the tool logic files in general. 
- They are missing things like cost calculations and error handling. 
- Please review the tool logic files and make sure that they are complete. 

1. `brave_search.py`
   - `cache = CacheManager()`
   - `cache.cache_content_analysis` 
   - `def estimate_cost`
2. `dalle_generate.py` 
   - `cache = CacheManager()`
   - `cache = CacheManager()`
   - `cache.cache_content_analysis`
   - `def _calculate_dalle_cost` <-- not usin gthe same 
3. `file_operations.py`
   - `cache = CacheManager()`
   - `cache.get_cached_analysis`
   - `cache.cache_content_analysis`
   - Missing anything about cost 
4. `graphic_design.py`
   - `cache = CacheManager()`
   - `cache.get_cached_analysis`
   - `cache.cache_content_analysis`
   - `def estimate_cost`
5. `perplexity_search.py`
   - `cache = CacheManager()`
   - `cache.get_cached_analysis`
   - `cache.cache_content_analysis`
   - (all three cached repeat a second time)
   - `def _calculate_perplexity_cost` <-- not using the same 
6. `text_editor.py`
   - Cache is imported but not used 
   - Missing anything about cost calculations 
7. `think.py`
   - Cache is imported but not used 
   - Has tool metadata that should not be there 
   - Has hardcoded model capabilities that should not be there 
   - The entire file probably could be cleaned up 
   - The cost calculations are incomplete 
8. `web_search.py`
   - `cache = CacheManager()`
   - `cache.get_cached_analysis`
   - `cache.cache_content_analysis`
   - These are repeated about 6 times! 
   - `def _calculate_search_cost` <-- not using the same 


| END OF PHASE 1 |
| -------------- |


## **PHASE 2** Button Snippet Tool Files 

Next we need to do the same for the button snippet tool files. I only glanced and found one says `def create_read_file_snippet` when they all should say `def create_button_snippet`. 

### Create Missing Button Snippet Tool Files 

  1. Does code execution tool need a button snippet tool file? 
  2. Does Files API Tool need a button snippet tool file? 
  3. Create button snippet tool file for MCP Connector API Tool --> this one definitely does need one if it is in the `./tools/` directory because it is a tool that agents use, is that correct? 

### Audit Button Snippet Tool Files 

  1. Audit `button_brave_search.py`
  2. Audit `button_dalle_generate.py`
  3. Audit `button_file_operations.py`
  4. Audit `button_graphic_design.py`
  5. Audit `button_perplexity_search.py`
  6. Audit `button_text_editor.py`
  7. Audit `button_think.py`
  8. Audit `button_web_search.py`

Please don't create a list of all the missing things. Just audit the files and make sure that they are complete. Thank you. 

| END OF PHASE 2 |
| -------------- |

## **PHASE 3** UI Tool Files 

### Create Missing UI Tool Files 

1. Create UI tool file for Code Execution Tool 
2. Create UI tool file for Files API Tool 
3. Create UI tool file for MCP Connector API Tool

### Audit UI Tool Files 

1. Audit `ui_brave_search.py`
2. Audit `ui_dalle_generate.py`
3. Audit `ui_file_operations.py`
4. Audit `ui_graphic_design.py`
5. Audit `ui_perplexity_search.py`
6. Audit `ui_text_editor.py`
7. Audit `ui_think.py`
8. Audit `ui_web_search.py`

Please don't create a list of all the missing things. Just audit the files and make sure that they are complete. Thank you. 

| END OF PHASE 3 |
| -------------- |

## **PHASE 4** Tool JSON Files 

### Create Missing Tool JSON Files 

1. Create tool JSON file for Code Execution Tool 
2. Create tool JSON file for Files API Tool 
3. Create tool JSON file for MCP Connector API Tool

### Audit Tool JSON Files 

1. Audit `tool_brave_search.json`
2. Audit `tool_dalle_generate.json`
3. Audit `tool_file_operations.json`
4. Audit `tool_graphic_design.json`
5. Audit `tool_perplexity_search.json`
6. Audit `tool_text_editor.json`
7. Audit `tool_think.json`
8. Audit `tool_web_search.json`

Please don't create a list of all the missing things. Just audit the files and make sure that they are complete. Thank you. 

| END OF PHASE 4 |
| -------------- |

## **PHASE 5** Tool Touchpoints in Orchestrator Files 

1. Please review all of the orchestrator files and make sure that all tool touchpoints are complete and accurate. 
2. All 8 tools have shared error handling 
3. The three new tools should have shared error handling 
4. All 8 tools have shared cache management and analysis 
5. The three new tools should have shared cache management and analysis 
6. Delete the `memory.py` file 

Ensure any and all files that should be integrated with tools are integrated with tools. 

  - `orchestrator/__init__.py`
  - `orchestrator/agent_callback.py`
  - `orchestrator/agent_orchestrator.py`
  - `orchestrator/conversation_bridge.py`
  - `orchestrator/core.py`
  - `orchestrator/error_handling.py`
  - `orchestrator/files_api.py`
  - `orchestrator/manager_buttons.py`
  - `orchestrator/manager_models.py`
  - `orchestrator/manager_tools.py`
  - `orchestrator/mcp_connector.py`
  - `orchestrator/mcp_hub.py`
  - `orchestrator/memory_mcp.py`
  - `orchestrator/memory.py`
  - `orchestrator/protocol.md`
  - `orchestrator/workflow_state.py`

| END OF PHASE 5 |
| -------------- |

