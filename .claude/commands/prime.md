# Context Priming Updated for Logic Audit Sessions 

MINIMIZE LLM LIMITATIONS: 
    Start the `sequential_thinking` MCP tool and use it to think while you review the following between thoughts. 
    Or use the native `think` tool if you are able to use tools between sequential thoughts. 

UNDERSTAND PROJECT-STATE MANAGEMENT:
    Start the `memory` MCP tool. 
    - If starting a project, hold this to last and create the entity. 
    - If returning to a project, then query the entity as an EXACT search term. 
    Create entity `mao-web` and `mao-<project-task-name>`.
    Add entry with relation to those entities at milestones. 
    1. About to start a series of tasks 
    2. Any updates during complete that set of tasks 
    3. Update after completion of those tasks, including what the next set of tasks should be. 
    This is ESSENTIAL for helping our AI work together and across occasionally abrupt context-window-smashing. 

READ FOR PROJECT: 
    `./CLAUDE.md` --> Complete development rules including new UI Development Guidelines section
    `./documentation/10_AI_DEV_INDEX.md` --> Complete Python backend architecture understanding
    `./AUDIT_LOGIC/MAO_FLOW.md`--> Current task at hand

UNDERSTAND: 
    This project requires reading, in full, a large number of files of about 100,000 tokens. 
    This is necessary for the one AI working on the tasks to have this in their context window. 
    It is manageable with diligent record keeping detailed in the SPEC and `memory` MCP updates. 

READ FOR SESSION: 
    `./orchestrator/__init__.py`
    `./orchestrator/agent_callback.py`
    `./orchestrator/agent_orchestrator.py`
    `./orchestrator/cache/__init__.py`
    `./orchestrator/cache/cache_system.py`
    `./orchestrator/cli_manager.py`
    `./orchestrator/conversation_bridge.py`
    `./orchestrator/core.py`
    `./orchestrator/error_handling.py`
    `./orchestrator/manager_buttons.py`
    `./orchestrator/manager_models.py`
    `./orchestrator/manager_tools.py`
    `./orchestrator/mcp_hub.py`
    `./orchestrator/memory_mcp.py`
    `./orchestrator/real_time_metrics.py`
    `./orchestrator/settings_manager.py`
    `./orchestrator/system_analytics_manager.py`
    `./orchestrator/user_analytics_manager.py`
    `./orchestrator/user_memory_manager.py`
    `./orchestrator/username_manager.py`
    `./orchestrator/workflow_manager.py`
    `./orchestrator/workflow_state.py`