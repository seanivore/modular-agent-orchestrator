# CONTEXT WINDOW SMASHED 

## `05_ORCHESTRATION.md` Changes To Sort Out

### What Stayed

- Dynamic workflow phase construction concept
- Goal analysis and workflow design architecture 
- Multi-agent coordination principles

### What's NEW
- **Parallel Tool Execution Architecture** - Finally gives proper spotlight to parallel execution benefits!
- **Agent Coordination System** - Multi-agent workflow management with real handoff protocols
- **Intelligent Model Selection** - Dynamic model assignment based on task requirements
- **Workflow State Management** - Real-time tracking and session recovery
- **Advanced Orchestration Features** - Cost optimization and quality assurance integration

### What Got Moved to `04_MAOS_ROLE.md`
- Workflow pattern selection code 
- Goal analysis details 

## The Problem And Working Through It 

"execute_parallel_tools" and other code functions, classes, etc. were added to the `05_ORCHESTRATION.md` document for the new abilities before they were implemented. 

- OLD ORCHESTRATOR `./documentation/06_ORCHESTRATION_OLD.md`
- NEW ORCHESTRATOR `./documentation/06_ORCHESTRATION.md`

## How to Sort Out 

A. Remove the "what got moved" items from the `05_ORCHESTRATION_OLD.md` document. 
B. Implement the "what's new" items that code was added for to the `05_ORCHESTRATION.md` document. 

Either way, I like how the old version start off with the goal setting example. 

### To Consider 

  - "parallel_tools" is a variable listed for model selection already 
  - MAIN GOAL: Be able to run agents in parallel 
    - Does this just require two API calls in succession and nothing else? 
    - If so, what is the best way to implement this? 
    - If not, is it the "parallel_tools" variable that needs to be implemented? 
  - Either way, this is a "tool" or ability that only needs to be run by whoever Mao is (next update you'll be able to select Opus or Claude Code as Mao)

---

## The Implementation 

- Implementation doc from Anthropic `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_PARALLEL_USE.md` has been waiting for a while. 

- All of the orchestrator files are at the top here `./documentation/10_DEV_PRIMER.md​` to identify what the touch-points are. 

- I see "manager_tools.py" but that doesn't seem like the place where tool execution is handled. 

- More details below from `./versioning/v4_0_0/AUDIT_ARCHIVE_JULY_2025/03_DEPENDENCY_MATRIX.md` 

### Examples of Mao Only Tools 

- CODE EXECUTION: `./tools/code_execution`
├── button_code_execution.py
├── code_execution.py
├── tool_code_execution.json
└── ui_code_execution.py

- FILES API: `./tools/files_api`
├── button_files_api.py
├── files_api.json
├── files_api.py
├── tool_files_api.json
└── ui_files_api.py

#### 4-File Architecture Compliance

- `tool_name.py` - Core logic with Mao standardization
- `button_tool_name.py` - Executable snippet generation
- `ui_tool_name.py` - Rich console display components
- `tool_tool_name.json` - Configuration and metadata

### Critical Dependencies 

**Cache System Pattern:**
```python
from orchestrator.cache.cache_system import CacheManager
cache = CacheManager()
```
**Error Handling Pattern:**
```python
from orchestrator.error_handling import handle_errors, APIError

@handle_errors(operation_name="function_name", return_dict=True)
def function_name():
    # function implementation
```

### Core Service Dependencies

#### **Agent Orchestrator (orchestrator/agent_orchestrator.py)**
**Dependent Files:** 45 files  
**Dependency Type:** Service + Runtime  
**Impact:** HIGH - Workflow execution  

**Direct Dependencies:**
- Workflow management system
- Tool execution modules
- CLI command handlers
- Terminal UI bridges

**Dependency Chain:**
```
Terminal UI → Interface Bridge → Agent Orchestrator → Tools/Commands
```

#### **Workflow Manager (orchestrator/workflow_manager.py)**
**Dependent Files:** 34 files  
**Dependency Type:** Service + Configuration  
**Impact:** HIGH - Process coordination  

**Direct Dependencies:**
- Workflow configuration files
- Tool execution modules
- State management systems
- Progress tracking systems

### Interface Dependencies 

#### **Claude Interface (interfaces/claude_interface.py)**
**Dependent Files:** 12 files  
**Dependency Type:** Interface + Runtime  
**Impact:** HIGH - System entry point  

**Direct Dependencies:**
- Terminal interface bridge
- CLI manager integration
- Agent orchestrator coordination
- Configuration management

**Integration Pattern:**
```python
from interfaces.claude_interface import ClaudeInterface

interface = ClaudeInterface()
interface.bootstrap_interface()
interface.launch_terminal_ui_smart()
```

### Code Execution Tool-Specific Analysis

**Architecture Excellence:**
- Sophisticated container management with persistence
- Files API integration for upload/download workflows
- Intelligent caching system prevents redundant executions
- Comprehensive sandbox environment configuration

**Key Features:**
- Secure Python 3.11 sandbox with pre-installed libraries
- Container lifecycle management (1-hour expiration)
- Multi-step execution support with state persistence
- File generation and download capabilities

**Integration Points:**
- Memory MCP for workflow state tracking
- Files API for file upload/download
- Anthropic Beta APIs (code-execution, files-api)
- Cache system for execution result optimization

## Integration Touch-points

- Memory MCP Integration: Workflow state tracking for execution sessions
- Custom exception types where appropriate
- All logic files include required imports: `CacheManager`, `@handle_errors`, `estimate_cost()`
- All functions properly decorated with `@handle_errors` 
- All tools have standalone `estimate_cost()` functions
- Cache integration present in all applicable operations

---