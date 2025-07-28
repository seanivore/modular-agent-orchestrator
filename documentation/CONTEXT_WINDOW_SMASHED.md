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
