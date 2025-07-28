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
# orchestrator/core.py
class WorkflowOrchestrator
class AgentManager
class TaskCoordinator

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
class ErrorHandler
class APIError
```

#### Analytics Classes
```python
# orchestrator/user_analytics_manager.py
class UserAnalyticsManager

# orchestrator/system_analytics_manager.py
class SystemAnalyticsManager

# orchestrator/real_time_metrics.py
class MetricsCollector
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
async def save_workflow_context(workflow_id: str, context: Dict[str, Any])
async def restore_workflow_context(workflow_id: str) -> Dict[str, Any]
async def create_entities(entities: List[Dict])
async def search_nodes(query: str)

# orchestrator/user_memory_manager.py
def save_session_state(session_data: Dict[str, Any])
def get_user_context() -> Dict[str, Any]
def load_user_preferences(username: str) -> Dict[str, Any]
```

#### Workflow Management
```python
# orchestrator/workflow_manager.py
def generate_workflow_id() -> str
def create_workflow_context(goal: str, user_id: str) -> Dict[str, Any]
def execute_workflow(workflow_id: str) -> Dict[str, Any]
def validate_workflow_config(config: Dict[str, Any]) -> bool

# orchestrator/workflow_state.py
def save_workflow_state(workflow_id: str, state: Dict)
def load_workflow_state(workflow_id: str) -> Dict
def update_phase_status(workflow_id: str, phase: str, status: str)
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