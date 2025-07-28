# Developer Primer; Templates & Creation Guides
*Practical templates and step-by-step guides for creating Mao components*

---

**Purpose:** This document provides concrete examples, templates, and creation guides for building Mao components. Pair this with CLAUDE.md (rules & principles) for complete development context.

**When to use:** Reference this when actually creating new tools, CLI commands, configs, or components.

---

## Quick Reference

### Component Types & File Patterns
- **Tools:** 4 files (logic.py, button_*.py, ui_*.py, tool_*.json)
- **CLI Commands:** 3 files (command.py, ui_command.py, command.json)
- **Providers:** 1 JSON file (provider_name.json)
- **Models:** 1 JSON file (model_name.json)
- **Settings:** 1 JSON file (setting_name_app_settings.json)

### Key Directories
- Tools: `./tools/[tool_name]/`
- CLI Commands: `./configs/cli/[command_name]/`
- Providers: `./configs/providers/`
- Models: `./configs/models/`
- Settings: `./configs/settings/`
- Templates: `./templates/`

### Validation Audits of New Code 
   - Standard Mao imports 
   - CacheManager integration 
   - estimate_cost() function 
   - @handle_errors decorators 
   - Fingerprinting patterns 
   - UI consistency patterns 

---

## Tool Creation Guide

### Step 1: Create Tool Directory
```bash
mkdir ./tools/[tool_name]
cd ./tools/[tool_name]
```

### Step 2: Main Logic File (`[tool_name].py`)
```python
# Required imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError
from typing import Dict, Any
import json

# Standard cache instance
cache = CacheManager()

class ToolNameManager:
    def __init__(self):
        self.tool_name = "tool_name"
    
    @handle_errors(operation_name="main_operation", return_dict=True)
    def main_operation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Main tool operation"""
        # Standard caching pattern
        cache_key = f"tool_name|{params.get('key_param', 'default')}"
        cached = cache.get_cached_analysis(cache_key, "tool_name")
        if cached:
            return json.loads(cached)
        
        # Process data
        result = self._process_data(params)
        
        # Cache result
        cache.cache_content_analysis(cache_key, json.dumps(result), "tool_name")
        return result
    
    def _process_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Internal processing logic"""
        # Implementation here
        return {"status": "success", "data": "processed"}

# Standalone functions for button imports
def standalone_operation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for button file imports"""
    manager = ToolNameManager()
    return manager.main_operation(params)

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate operation cost for budget planning"""
    return 0.001  # Adjust based on complexity
```

### Step 3: Button File (`button_[tool_name].py`)
```python
from typing import Dict, Any
from .tool_name import standalone_operation

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """Single entry point for button snippet generation"""
    operation = params.get("operation", "default_operation")
    
    if operation == "main_operation":
        return _create_main_snippet(params, model)
    else:
        return _create_default_snippet(params, model)

def _create_main_snippet(params: Dict[str, Any], model: str) -> str:
    """Create main operation button snippet"""
    # Use imported functions, don't duplicate logic
    result = standalone_operation(params)
    return f"Button snippet based on: {result['status']}"

def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Default button snippet"""
    return "Default tool button snippet"
```

### Step 4: UI File (`ui_[tool_name].py`)
```python
from typing import Dict, Any, List

def display_results(results: Dict[str, Any]) -> str:
    """Display tool results in formatted output"""
    if not results or results.get("status") != "success":
        return "❌ Operation failed"
    
    output = []
    output.append("✅ Tool operation completed")
    
    # Format data display
    if "data" in results:
        output.append(f"Data: {results['data']}")
    
    return "\n".join(output)

def format_error(error_msg: str) -> str:
    """Format error messages for display"""
    return f"❌ Error: {error_msg}"
```

### Step 5: Configuration File (`tool_[tool_name].json`)
```json
{
    "name": "tool_name",
    "version": "1.0.0",
    "description": "Tool description",
    "file_path": "tools/tool_name/tool_name.py",
    "button_path": "tools/tool_name/button_tool_name.py",
    "ui_path": "tools/tool_name/ui_tool_name.py",
    "operations": {
        "main_operation": {
            "description": "Main tool operation",
            "required_params": ["key_param"],
            "optional_params": ["optional_param"]
        }
    },
    "models_supported": ["all"],
    "cost_estimate": 0.001
}
```

---

## CLI Command Creation Guide

### Step 1: Create Command Directory
```bash
mkdir ./configs/cli/[command_name]
cd ./configs/cli/[command_name]
```

### Step 2: Command Logic (`[command_name].py`)
```python
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from typing import Dict, Any

cache = CacheManager()

class CommandNameManager:
    def __init__(self):
        self.command_name = "command_name"
    
    @handle_errors(operation_name="execute_command", return_dict=True)
    def execute_command(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the CLI command"""
        # Command implementation
        return {"status": "success", "message": "Command executed"}

def estimate_cost(params: Dict[str, Any] = None) -> float:
    return 0.001
```

### Step 3: UI Components (`ui_[command_name].py`)
```python
from typing import Dict, Any

def display_command_result(result: Dict[str, Any]) -> str:
    """Display command execution result"""
    if result.get("status") == "success":
        return f"✅ {result.get('message', 'Command completed')}"
    else:
        return f"❌ Command failed: {result.get('error', 'Unknown error')}"
```

### Step 4: Command Configuration (`[command_name].json`)
```json
{
    "name": "command_name",
    "help": "Command description",
    "terminal_flag": "--command-flag",
    "type": "utility",
    "file_path": "configs/cli/command_name/command_name.py",
    "ui_path": "configs/cli/command_name/ui_command_name.py"
}
```

---

## Configuration File Templates

### Provider Configuration
```json
{
    "name": "provider_name",
    "display_name": "Provider Display Name",
    "type": "api_provider",
    "base_url": "https://api.provider.com",
    "api_key_env": "PROVIDER_API_KEY",
    "models_supported": ["model1", "model2"],
    "default_model": "model1",
    "rate_limits": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000
    }
}
```

### Model Configuration
```json
{
    "name": "model_name",
    "display_name": "Model Display Name",
    "provider": "provider_name",
    "model_id": "actual-model-id",
    "context_window": 128000,
    "max_tokens": 4096,
    "cost_per_input_token": 0.003,
    "cost_per_output_token": 0.015,
    "capabilities": ["text", "code", "reasoning"]
}
```

### Settings Configuration
```json
{
    "name": "setting_name",
    "display_name": "Setting Display Name",
    "description": "What this setting controls",
    "type": "boolean",
    "default_value": true,
    "options": [true, false],
    "category": "general"
}
```

---

## Directory Structure Examples

### Tool Directory Structure
```
tools/
└── example_tool/
    ├── example_tool.py          # Main logic
    ├── button_example_tool.py   # Button snippets
    ├── ui_example_tool.py       # Display components
    └── tool_example_tool.json   # Configuration
```

### CLI Command Directory Structure
```
configs/cli/
└── example_command/
    ├── example_command.py       # Command logic
    ├── ui_example_command.py    # UI components
    └── example_command.json     # Configuration
```

---

## File Naming Conventions

### Required Patterns
- Tool files: `[tool_name].py`, `button_[tool_name].py`, `ui_[tool_name].py`, `tool_[tool_name].json`
- CLI files: `[command_name].py`, `ui_[command_name].py`, `[command_name].json`
- Config files: Use underscore separators, not hyphens
- Directory names: Use underscore separators

### Examples
- ✅ `brave_search.py`, `ui_brave_search.py`, `tool_brave_search.json`
- ✅ `help.py`, `ui_help.py`, `help.json`
- ❌ `brave-search.py`, `braveSearch.py`, `brave_search_tool.json`

---

## Implementation Patterns

### Standard Error Handling
```python
@handle_errors(operation_name="function_name", return_dict=True)
def function_name(self, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Operation logic
        result = self._do_operation(params)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

### Standard Caching Pattern
```python
# Cache key format: "component|param1|param2|param3"
cache_key = f"component_name|{param1}|{param2}"
cached_result = cache.get_cached_analysis(cache_key, "component_name")
if cached_result:
    return json.loads(cached_result)

# Process and cache
result = process_data()
cache.cache_content_analysis(cache_key, json.dumps(result), "component_name")
return result
```

### JSON Schema Validation
```python
def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration against schema"""
    required_fields = ["name", "file_path"]
    return all(field in config for field in required_fields)
```

---

## Class & Function Reference
*Quick lookup for all Mao components to prevent coding mistakes*

### Core Classes

#### Orchestrator Classes
```python
# orchestrator/conversation_bridge.py  
class ConversationToWorkflowBridge:
    def estimate_cost(self, params: Dict[str, Any]) -> float

# orchestrator/cli_manager.py
class CLICommandsManager:
    def execute_slash_command(self, command: str, args: str) -> Dict[str, Any]
    def get_autocomplete_suggestions(self, partial: str) -> List[str]

# orchestrator/settings_manager.py
class ApplicationSettingsManager:
    def discover_settings(self, force_refresh: bool = False) -> Dict[str, SettingDefinition]
    def get_default_settings(self) -> Dict[str, Any]
    def get_user_settings(self, username: str) -> Dict[str, Any]
    def get_settings_by_section(self) -> Dict[str, List[str]]

# orchestrator/real_time_metrics.py
class SystemMetricsProvider:
    def get_dashboard_metrics(self) -> Dict[str, Any]

# orchestrator/memory_mcp.py
class MemoryMCPManager

# orchestrator/user_memory_manager.py
class UserMemoryManager

# orchestrator/workflow_manager.py
class WorkflowManager
class WorkflowExecutor

# orchestrator/workflow_state.py
class WorkflowStateManager

# orchestrator/settings_manager.py
class SettingsManager

# orchestrator/manager_models.py
class ModelManager

# orchestrator/manager_tools.py
class ToolManager

# orchestrator/manager_buttons.py
class ButtonManager

# orchestrator/cache/cache_system.py
class CacheManager

# orchestrator/error_handling.py
class OrchestrationError  # Base exception for orchestration tools
class ValidationError(OrchestrationError)  # Input validation failures
class ProcessingError(OrchestrationError)  # Tool processing failures
class ResourceError(OrchestrationError)   # Resource access failures
class APIError(OrchestrationError)        # External API call failures
```

#### Analytics Classes
```python
# orchestrator/user_analytics_manager.py
class UserAnalyticsManager:
    def __init__(self, user_dir: str = "./configs/user/")
    def estimate_cost(self, operation: str = "analytics_operation") -> float
    def track_session(self, username: str, session_id: str, action: str, **kwargs) -> bool
    def track_tool_usage(self, username: str, tool_name: str, success: bool, response_time: float) -> bool
    def track_workflow(self, username: str, workflow_id: str, workflow_command: str, action: str, **kwargs) -> bool
    def track_costs(self, username: str, date: str, model_name: str, cost: float, session_id: str = None) -> bool
    def scan_available_tools(self, username: str) -> List[str]
    def _get_user_analytics_dir(self, username: str) -> Path
    def _ensure_analytics_dir(self, username: str) -> Path
    def _read_analytics_file(self, username: str, filename: str) -> Dict[str, Any]
    def _write_analytics_file(self, username: str, filename: str, data: Dict[str, Any]) -> bool

**Data Classes**:
- `SessionMetric` - Individual session tracking data
- `ToolUsageMetric` - Individual tool usage tracking data  
- `WorkflowMetric` - Individual workflow tracking data
- `CostMetric` - Daily cost tracking data

### orchestrator/user_memory_manager.py
**Real Class**: `UserMemoryManager`
**Key Methods**:
- `__init__(self)`
- `store_memory(self, user_id: str, content: str, category: str = None, tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]`
- `retrieve_memories(self, user_id: str, query: str, category: str = None, limit: int = 10, include_metadata: bool = False) -> List[Dict[str, Any]]`
- `delete_memory(self, user_id: str, memory_id: str) -> Dict[str, Any]`
- `suggest_contextual_memories(self, user_id: str, current_context: str, workflow_type: str = None) -> List[Dict[str, Any]]`
- `_store_memory_to_file(self, username: str, memory: Dict[str, Any], category: str)`
- `_store_memory_to_mcp(self, user_id: str, memory: Dict[str, Any])`
- `_delete_memory_from_mcp(self, user_id: str, memory_id: str)`
- `_auto_categorize_content(self, content: str) -> str`
- `_auto_generate_tags(self, content: str) -> List[str]`
- `_extract_context_triggers(self, content: str) -> List[str]`

### orchestrator/memory_mcp.py  
**Real Class**: `MemoryMCPManager`
**Key Methods**:
- `__init__(self, config_path: str = None)`
- `initialize(self) -> bool`
- `test_connection(self) -> bool`
- `estimate_cost(self, operation: str = "memory_operation") -> float`
- `create_workflow(self, workflow_data: Dict[str, Any]) -> str`
- `prepare_agent_handoff(self, workflow_id: str, agent_context: Dict[str, Any]) -> bool`
- `restore_agent_context(self, workflow_id: str) -> Dict[str, Any]`
- `recover_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]`

**Real Class**: `LocalMemoryFallback`
**Key Methods**:
- `__init__(self)`
- `create_entities(self, entities: List[Dict]) -> List[str]`
- `add_observations(self, observations: List[Dict]) -> bool`
- `_load_json(self, file_path, default)`
- `_save_data(self)`

### orchestrator/mcp_hub.py
**Real Class**: `MCPIntegrationHub`
**Key Methods**:
- `__init__(self)`
- `create_workflow(self, workflow_config: Dict[str, Any]) -> str`
- `update_workflow_state(self, workflow_id: str, state_update: Dict[str, Any]) -> bool`
- `get_workflow_state(self, workflow_id: str) -> Dict[str, Any]`
- `store_session_context(self, session_data: Dict[str, Any]) -> bool`
- `restore_session_context(self, session_id: str) -> Dict[str, Any]`
- `health_check(self) -> Dict[str, bool]`
- `_initialize_servers(self)`
- `_setup_memory_mcp(self)`
- `_setup_files_api(self)`
- `_setup_mcp_connector(self)`

## Analytics Data Schemas

### Session Metrics Schema
```json
{
  "sessions": [
    {
      "session_id": "sess_001",
      "start_time": "2025-01-15T09:00:00Z",
      "end_time": "2025-01-15T11:30:00Z",
      "duration_minutes": 150,
      "workflow_count": 3,
      "tool_activations": 12
    }
  ],
  "aggregates": {
    "total_sessions": 1,
    "average_duration": 150,
    "total_time_minutes": 150
  }
}
```

### Tool Usage Schema
```json
{
  "tool_usage": {
    "brave_search": {
      "total_uses": 15,
      "success_rate": 0.95,
      "avg_response_time": 1.2,
      "last_used": "2025-01-15T10:30:00Z"
    }
  },
  "metadata": {
    "discovery_enabled": true,
    "last_discovery_scan": "2025-01-15T10:30:00Z"
  }
}
```

### Memory Schema
```json
{
  "memories": [
    {
      "memory_id": "mem_a1b2c3d4",
      "content": "Always use descriptive variable names",
      "category": "coding_preference", 
      "tags": ["coding", "variables", "best_practices"],
      "priority": "medium",
      "created_at": "2025-01-15T10:30:00Z",
      "access_count": 0,
      "relevance_score": 1.0,
      "context_triggers": ["variable", "naming", "code"]
    }
  ]
}
```

## Analytics Trigger Points

### Session Triggers
- **File**: `interfaces/ui_terminal.py`
- **Methods**: `track_session(username, session_id, "start"|"end"|"update_workflow_count"|"update_tool_activations")`

### Tool Usage Triggers  
- **File**: `orchestrator/manager_tools.py`
- **Methods**: `track_tool_usage(username, tool_name, success, response_time)`

### Workflow Triggers
- **File**: `orchestrator/workflow_manager.py`
- **Methods**: `track_workflow(username, workflow_id, command, "start"|"complete", tags=tags, success=True/False)`

### Cost Triggers
- **Files**: `orchestrator/manager_models.py`, `orchestrator/real_time_metrics.py`
- **Methods**: `track_costs(username, date, model_name, cost, session_id)`

### Memory Triggers
- **File**: `configs/cli/memory/memory.py`
- **CLI Commands**: `/memory "content"`, `/memory --list`, `/memory --delete [ID]`

#### Script Tools
```python
# scripts/user_id_generator/user_id_generator.py
def estimate_cost(generation_params: Dict[str, Any] = None) -> Dict[str, float]
def generate_user_id(username) -> str  # Standalone function
class UserIDGenerator:
    def generate_user_id(self, username)  # Deterministic ID generation

# scripts/unique_id_generator/unique_id_generator.py  
def estimate_cost(generation_params: Dict[str, Any] = None) -> Dict[str, float]
def generate_workflow_id() -> str  # Collision-free workflow identifiers
```

### Core Functions

#### Error Handling & Decorators
```python
# orchestrator/error_handling.py
@handle_errors(operation_name: str, return_dict: bool = True)
def retry_with_backoff(func, max_retries: int = 3)
def log_error(error: Exception, context: str)
```

#### Memory & State Management
```python
# orchestrator/memory_mcp.py
class MemoryMCPManager:
    def estimate_cost(self, params: Dict[str, Any]) -> float
    def client(self) -> property  # Lazy load MCP client
    # Note: Actual MCP integration methods available via property

# orchestrator/user_memory_manager.py
def save_session_state(session_data: Dict[str, Any])
def get_user_context() -> Dict[str, Any]
def load_user_preferences(username: str) -> Dict[str, Any]
```

#### Workflow Management
```python
# orchestrator/core.py - WorkflowOrchestrator
async def create_workflow_from_goal(user_goal: str, preferences: Optional[Dict] = None) -> WorkflowPlan
def _analyze_goal(goal: str) -> Dict[str, Any]
async def _design_workflow_phases(analysis: Dict[str, Any], preferences: Dict[str, Any], tool_suggestions: Dict[str, Any]) -> List[WorkflowPhase]
async def _execute_phase_with_caching(phase: WorkflowPhase, workflow: WorkflowPlan, workflow_memory: Dict, anthropic_client) -> ExecutionResult
async def execute_workflow(workflow_id: str, anthropic_client=None) -> Dict[str, Any]

# orchestrator/workflow_state.py - WorkflowStatus (dataclass)
workflow_id: str
status: str  # 'initialized', 'active', 'paused', 'completed', 'failed'
phases_total: int
phases_completed: int
phases_active: int
last_activity: str
created_at: str
updated_at: str
health: str  # 'healthy', 'warning', 'error'

# orchestrator/workflow_state.py - RecoveryPlan (dataclass)
workflow_id: str
recovery_type: str  # 'resume_phase', 'restart_phase', 'continue_next', 'restart_workflow'
current_phase: Optional[str]
next_phase: Optional[str]
context_available: bool
files_accessible: bool
recovery_actions: List[str]
estimated_recovery_time: str

# orchestrator/workflow_state.py - WorkflowStateManager
def track_workflow_progress(workflow_id: str, update: str) -> bool
def get_workflow_status(workflow_id: str) -> Optional[WorkflowStatus]
def recover_interrupted_workflow(workflow_id: str) -> Optional[RecoveryPlan]
def estimate_cost(params: Dict[str, Any]) -> float

# orchestrator/agent_orchestrator.py - AgentOrchestrator
def execute_workflow_phase(workflow_id: str, phase: dict) -> Dict[str, Any]
def _create_agent_package(workflow_id: str, phase: dict, context: dict) -> dict
def recover_interrupted_workflow(workflow_id: str) -> dict

# orchestrator/real_time_metrics.py - SystemMetricsProvider
def get_dashboard_metrics() -> Dict[str, Any]
def get_workflow_progress(workflow_id: str) -> Dict[str, Any]
def get_live_stats() -> Dict[str, Any]
def _calculate_progress_percentage(workflow_status: Dict) -> float
def _get_phase_details(workflow_id: str, execution_history: List) -> List[Dict]

# orchestrator/real_time_metrics.py - WorkflowMonitor
def subscribe(callback)
def on_workflow_start(workflow_id: str, workflow_info: Dict)
def on_phase_start(workflow_id: str, phase_info: Dict)
def on_phase_progress(workflow_id: str, progress_info: Dict)
def on_phase_complete(workflow_id: str, result_info: Dict)

# orchestrator/mcp_hub.py - MCPIntegrationHub
def create_workflow(workflow_id: str, user_goal: str) -> str
def save_workflow_draft(workflow_id: str, content: str, draft_type: str, phase: str = None) -> str
def prepare_agent_handoff(workflow_id: str, agent_materials: Dict[str, Any]) -> str
def restore_agent_context(workflow_id: str, handoff_file_id: str) -> Dict[str, Any]
def complete_workflow(workflow_id: str, final_results: Dict[str, Any]) -> bool
def recover_session(workflow_id: str) -> Optional[Dict[str, Any]]
def list_recoverable_workflows() -> List[Dict[str, Any]]
def execute_mcp_tool(server_name: str, tool_name: str, params: Dict[str, Any], workflow_id: str = None) -> Dict[str, Any]
```

#### Cache Management
```python
# orchestrator/cache/cache_system.py
def get_cached_analysis(cache_key: str, component_name: str) -> str
def cache_content_analysis(cache_key: str, content: str, component_name: str)
def clear_cache(pattern: str = None)
def get_cache_stats() -> Dict[str, Any]
```

#### Configuration & Settings
```python
# orchestrator/settings_manager.py
def load_user_settings(user_id: str) -> Dict[str, Any]
def save_user_settings(user_id: str, settings: Dict[str, Any])
def get_default_settings() -> Dict[str, Any]
def validate_settings(settings: Dict[str, Any]) -> bool

# orchestrator/manager_models.py
def get_available_models() -> List[Dict[str, Any]]
def select_optimal_model(task_type: str) -> str
def get_model_config(model_name: str) -> Dict[str, Any]

# orchestrator/manager_tools.py
def get_available_tools() -> List[Dict[str, Any]]
def load_tool_config(tool_name: str) -> Dict[str, Any]
def validate_tool_requirements(tool_name: str) -> bool
```

#### User Management
```python
# orchestrator/username_manager.py
def generate_user_id(username: str) -> str
def validate_username(username: str) -> bool
def create_user_profile(username: str) -> Dict[str, Any]
def get_user_profile(user_id: str) -> Dict[str, Any]
```

#### Analytics Functions
```python
# orchestrator/user_analytics_manager.py
def track_user_action(user_id: str, action: str, metadata: Dict)
def get_user_metrics(user_id: str) -> Dict[str, Any]
def generate_user_report(user_id: str) -> Dict[str, Any]

# orchestrator/system_analytics_manager.py
def track_system_event(event_type: str, data: Dict[str, Any])
def get_system_metrics() -> Dict[str, Any]
def generate_performance_report() -> Dict[str, Any]
```

### Standard Function Patterns

#### Required in Every Component
```python
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate operation cost for budget planning"""
    return 0.001  # Adjust based on complexity
```

#### Standard Import Pattern
```python
# At top of every file
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError
from typing import Dict, Any, List
import json

# Standard cache instance
cache = CacheManager()
```

#### Standard Caching Pattern
```python
# Cache key format: "component|param1|param2|param3"
cache_key = f"component_name|{param1}|{param2}"
cached_result = cache.get_cached_analysis(cache_key, "component_name")
if cached_result:
    return json.loads(cached_result)

# Process and cache
result = process_data()
cache.cache_content_analysis(cache_key, json.dumps(result), "component_name")
return result
```

#### Standard Error Handling
```python
@handle_errors(operation_name="function_name", return_dict=True)
def function_name(self, params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Operation logic
        result = self._do_operation(params)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

### Common Mistakes to Avoid

**Import Errors:**
- ❌ `from orchestrator import cache` 
- ✅ `from orchestrator.cache.cache_system import CacheManager`

**Function Naming:**
- ❌ `def processData()` or `def process_Data()`
- ✅ `def process_data()`

**Cache Key Format:**
- ❌ `cache_key = f"{param1}-{param2}"`
- ✅ `cache_key = f"component|{param1}|{param2}"`

**Error Decorator:**
- ❌ `@handle_errors("function_name")`
- ✅ `@handle_errors(operation_name="function_name", return_dict=True)`

**JSON Config Fields:**
- ❌ `"id": "tool_name"` or `"tool_id": "tool_name"`
- ✅ `"name": "tool_name"`

---

*This primer provides the foundation for creating Mao components. Reference CLAUDE.md for development principles and standards.*