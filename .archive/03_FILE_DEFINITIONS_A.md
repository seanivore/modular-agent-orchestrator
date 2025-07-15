# Catalog & Defined Purpose of System Files 

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

