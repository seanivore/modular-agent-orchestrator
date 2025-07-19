# Core System Architecture (25 files)

## 🚨 **CRITICAL: LOCAL APPLICATION ONLY** 🚨
**See `/ARCHITECTURE_PRINCIPLES.md` - Mao is LOCAL ONLY, not web-based**

This document defines the files and information needed to document the foundational architecture of the Mao system.

---

# Batch 01: Root Files (1 file)

## File to Analyze:
- `./mao_v4.py` - Main application entry point and system initialization

### Simple Sentence Form: 

* **Overview:** 
- 1-2 sentences about the file and what it does for the system architecture. 

### Code & Explanation: 

* **Architecture Overview:** 
- Core application initialization patterns and entry point design
- System bootstrapping procedures and dependency initialization
- Main execution flow and system lifecycle management
- Recommended documentation location for architecture diagrams

### Written & Illustrated Data Info.: 

* **Data In-Flow:** 
- System startup sequences and initialization parameters
- Configuration loading and validation patterns
- External dependency connections and verification

* **Data Out-Flow:** 
- System state propagation to subsystems
- Logging and monitoring data flows
- Error handling and shutdown procedures

### Dependencies:
- None (foundation files)

---

# Batch 02: Interfaces (1 file)

## File to Analyze:
- `./interfaces/ui_terminal.py` - Terminal UI interface implementation

### Simple Sentence Form: 

* **Overview:** 
- 1-2 sentences about the file and what it does for system interfaces.

### Code & Explanation: 

* **Architecture Overview:** 
- Interface abstraction patterns and implementation strategies
- Communication protocols between UI layers and core system
- Interface standardization and consistency patterns
- Recommended documentation location for interface specifications

### UI for TypeScript/Node.js Integration:
- Provide UI interface patterns and design principles
- Identify touchpoints for TypeScript integration 
- Define interface standardization method across different UI implementations
- Identify UI integration guide requirements and specifications
- Define Interface specifications for external consumption
- Python --> TypeScript mappings and data transformation

### Provide Written & Illustrated Data Info.: 

* **Data In-Flow:** 
- User input processing and validation
- Command parsing and interpretation
- UI state management and synchronization

* **Data Out-Flow:** 
- Response formatting and presentation
- UI updates and state changes
- Error messaging and user feedback

### Dependencies:
- Depends on Batch 01 (root files)

---

# Batch 03: Orchestrator Core (12 files)

## Files to Analyze:
- `./orchestrator/__init__.py` - Package initialization and exports
- `./orchestrator/core.py` - Core orchestration logic and main coordinator
- `./orchestrator/agent_callback.py` - Agent callback handling and response processing
- `./orchestrator/agent_orchestrator.py` - Main orchestrator implementation
- `./orchestrator/conversation_bridge.py` - Conversation bridging and context management
- `./orchestrator/error_handling.py` - Centralized error handling system
- `./orchestrator/mcp_hub.py` - MCP hub management and coordination
- `./orchestrator/memory_mcp.py` - Memory MCP integration and state persistence
- `./orchestrator/workflow_manager.py` - Workflow management and execution
- `./orchestrator/workflow_state.py` - Workflow state management and tracking
- `./orchestrator/cli_manager.py` - CLI command management and dispatch
- `./orchestrator/protocol.md` - Protocol documentation and specifications

### Simple Sentence Form: 

* **Overview:** 
- 1-2 sentences about each file and its role in the orchestration system.

### Code & Explanation: 

* **Architecture Overview:** 
- Core orchestration patterns and coordination strategies
- State management across distributed components
- Event-driven architecture and message passing
- Component lifecycle management and dependency injection
- Recommended documentation location for orchestration diagrams

### Written & Illustrated Data Info.: 

* **Data In-Flow:** 
- Command dispatch and routing patterns
- Agent communication and coordination flows
- State synchronization and consistency management

* **Data Out-Flow:** 
- Orchestrated responses and result aggregation
- State propagation to dependent systems
- Monitoring and analytics data collection

### Dependencies:
- Depends on Batch 02 (interfaces)

---

# Batch 04: Orchestrator Managers (9 files)

## Files to Analyze:
- `./orchestrator/manager_buttons.py` - Button management and UI controls
- `./orchestrator/manager_models.py` - Model management and configuration
- `./orchestrator/manager_tools.py` - Tool management and integration
- `./orchestrator/settings_manager.py` - Settings management and persistence
- `./orchestrator/system_analytics_manager.py` - System analytics and monitoring
- `./orchestrator/user_analytics_manager.py` - User analytics and tracking
- `./orchestrator/username_manager.py` - Username management and authentication
- `./orchestrator/user_memory_manager.py` - User memory management
- `./orchestrator/real_time_metrics.py` - Real-time metrics collection and reporting

### Simple Sentence Form: 

* **Overview:** 
- 1-2 sentences about each manager's responsibility in the system.

### Code & Explanation: 

* **Architecture Overview:** 
- Manager pattern implementation and coordination
- Cross-manager communication and data sharing
- Configuration management and persistence strategies
- Analytics and monitoring architecture
- Recommended documentation location for manager interaction diagrams

### Written & Illustrated Data Info.: 

* **Data In-Flow:** 
- Configuration updates and system changes
- User interactions and behavior tracking
- System performance metrics and health data

* **Data Out-Flow:** 
- Managed configuration distribution
- Analytics data aggregation and reporting
- System health and status information

### Dependencies:
- Depends on Batch 03 (orchestrator core)

---

# Batch 05: Cache System (2 files)

## Files to Analyze:
- `./orchestrator/cache/__init__.py` - Cache package initialization
- `./orchestrator/cache/cache_system.py` - Core caching implementation and strategies

### Simple Sentence Form: 

* **Overview:** 
- 1-2 sentences about each file's role in the caching system.

### Code & Explanation: 

* **Architecture Overview:** 
- Caching strategies and implementation patterns
- Cache invalidation and consistency management
- Performance optimization and memory management
- Cache hierarchy and storage strategies
- Recommended documentation location for cache architecture diagrams

### Written & Illustrated Data Info.: 

* **Data In-Flow:** 
- Cache key generation and data storage patterns
- Cache invalidation triggers and policies
- Performance metrics and cache hit rates

* **Data Out-Flow:** 
- Cached data retrieval and response optimization
- Cache statistics and performance monitoring
- Memory usage and cleanup operations

### Dependencies:
- Depends on Batch 04 (orchestrator managers)
