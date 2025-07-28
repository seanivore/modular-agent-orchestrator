# Developer Primer: Templates & Creation Guides
*The complete AI development index for MAO - stop grepping, start building*

---

## Purpose & Usage

**This Document:** Complete file/class/function index + creation templates for MAO components
**Pair With:** `CLAUDE.md` (rules & principles) for complete development context
**Goal:** Eliminate AI guessing and file exploration - everything is indexed here

**When to Reference:**
- Creating new tools, CLI commands, configs, or components
- Need to know which file contains what class/function  
- Understanding orchestrator file responsibilities
- Implementing features like parallel agents

---

# Quick Navigation

## [🏗️ Creation Guides](#creation-guides)
- [Tool Creation](#tool-creation-guide)
- [CLI Command Creation](#cli-command-creation-guide) 
- [Configuration Files](#configuration-file-templates)

## [📁 Complete File Index](#complete-file-index)
- [Orchestrator Files](#orchestrator-file-index)
- [Tool Files](#tool-file-index)
- [Interface Files](#interface-file-index)

## [🧠 Architecture Insights](#architecture-insights)
- [File Responsibilities](#file-responsibilities---the-stop-grepping-guide)
- [Parallel Agent Implementation](#parallel-agent-execution-system)
- [Data Flow Patterns](#data-flow-patterns)

---

# Creation Guides

## Tool Creation Guide

### Step 1: Create Tool Directory
```bash
mkdir ./tools/[tool_name]
cd ./tools/[tool_name]
```

### Step 2: Main Logic File (`[tool_name].py`)
```python
# Required imports for ALL tool files
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
        """Main tool operation with standard caching pattern"""
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
        return {"status": "success", "data": "processed"}

# Standalone functions for button imports (REQUIRED)
def standalone_operation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for button file imports"""
    manager = ToolNameManager()
    return manager.main_operation(params)

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """REQUIRED: Estimate operation cost for budget planning"""
    return 0.001  # Adjust based on complexity
```

### Step 3: Button File (`button_[tool_name].py`)
```python
from typing import Dict, Any
from .tool_name import standalone_operation

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """REQUIRED: Single entry point for button snippet generation"""
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
from typing import Dict, Any
from rich.console import Console

# Module-level console (STANDARD PATTERN)
console = Console()

def display_tool_name_result(results: Dict[str, Any]) -> str:
    """REQUIRED: Main display function with standard naming"""
    if not results or results.get("status") != "success":
        return display_error("Operation failed")
    
    output = []
    output.append("✅ Tool operation completed")
    
    if "data" in results:
        output.append(f"Data: {results['data']}")
    
    return "\n".join(output)

def display_error(error_msg: str) -> str:
    """REQUIRED: Standard error display function"""
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
        return {"status": "success", "message": "Command executed"}

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """REQUIRED: Cost estimation"""
    return 0.001
```

### Step 3: UI Components (`ui_[command_name].py`)
```python
from typing import Dict, Any

def display_command_name_result(result: Dict[str, Any]) -> str:
    """REQUIRED: Display command execution result"""
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

# Complete File Index

## Orchestrator File Index

### File Responsibilities - The "Stop Grepping" Guide

**When you need to:**
- **Execute workflows** → `core.py` → `WorkflowOrchestrator` → `execute_workflow()`
- **Coordinate agents** → `agent_orchestrator.py` → `AgentOrchestrator` → `coordinate_agent_handoff()`
- **Track workflow state** → `workflow_state.py` → `WorkflowStateManager` → `update_workflow_state()`
- **Handle tool discovery** → `manager_tools.py` → `ToolManager` → `get_available_tools()`
- **Manage models** → `manager_models.py` → `ModelManager` → `select_optimal_model()`
- **Cache operations** → `cache/cache_system.py` → `CacheManager` → `get_cached_analysis()`
- **Process CLI commands** → `cli_manager.py` → `CLICommandsManager` → `execute_slash_command()`
- **Store user memory** → `user_memory_manager.py` → `UserMemoryManager` → `store_memory()`
- **Track analytics** → `user_analytics_manager.py` → `UserAnalyticsManager` → `track_session()`

### Core Workflow Execution

#### `orchestrator/core.py` - Main Workflow Brain
**Classes:**
- `WorkflowOrchestrator` - Primary workflow orchestration engine

**Key Methods:**
```python
async def create_workflow_from_goal(user_goal: str, preferences: Optional[Dict] = None) -> WorkflowPlan
def _analyze_goal(goal: str) -> Dict[str, Any]
async def _design_workflow_phases(analysis: Dict, preferences: Dict, tool_suggestions: Dict) -> List[WorkflowPhase]
async def execute_workflow(workflow_id: str, anthropic_client=None) -> Dict[str, Any]
async def _execute_phase_with_caching(phase: WorkflowPhase, workflow: WorkflowPlan, workflow_memory: Dict, anthropic_client) -> ExecutionResult
def _generate_phase_hash(phase: WorkflowPhase, workflow_description: str) -> str
def _select_optimal_model(phase: WorkflowPhase, preferences: Dict) -> str
def _estimate_phase_cost(phase: WorkflowPhase) -> Tuple[int, float]
```

**Parallel Agent Implementation Points:**
- `execute_workflow()` - Convert to `execute_workflow_async()` with phase grouping
- Add `_group_parallel_phases()` for phase number parsing ("01a", "01b" → group "01")
- Add `_execute_phase_async()` for AsyncAnthropic integration

#### `orchestrator/agent_orchestrator.py` - Agent Coordination
**Classes:**
- `AgentOrchestrator` - Agent handoff and coordination system

**Key Methods:**
```python
def __init__(self)
def execute_workflow_phase(workflow_id: str, phase: dict) -> Dict[str, Any]
def _create_agent_package(workflow_id: str, phase: dict, context: dict) -> dict
def recover_interrupted_workflow(workflow_id: str) -> dict
def estimate_cost(params: Dict[str, Any]) -> float
```

**Parallel Agent Role:**
- Handle multiple simultaneous agent completions
- Coordinate concurrent Files API operations
- Manage parallel handoff package creation

#### `orchestrator/workflow_state.py` - State Tracking
**Classes:**
- `WorkflowStateManager` - Workflow state persistence and tracking

**Data Classes:**
```python
@dataclass
class WorkflowStatus:
    workflow_id: str
    status: str  # 'initialized', 'active', 'paused', 'completed', 'failed'
    phases_total: int
    phases_completed: int
    phases_active: int
    last_activity: str
    created_at: str
    updated_at: str
    health: str  # 'healthy', 'warning', 'error'

@dataclass  
class RecoveryPlan:
    workflow_id: str
    recovery_type: str  # 'resume_phase', 'restart_phase', 'continue_next', 'restart_workflow'
    current_phase: Optional[str]
    next_phase: Optional[str]
    context_available: bool
    files_accessible: bool
    recovery_actions: List[str]
    estimated_recovery_time: str
```

**Key Methods:**
```python
def track_workflow_progress(workflow_id: str, update: str) -> bool
def get_workflow_status(workflow_id: str) -> Optional[WorkflowStatus]
def recover_interrupted_workflow(workflow_id: str) -> Optional[RecoveryPlan]
def estimate_cost(params: Dict[str, Any]) -> float
```

**Parallel Agent Role:**
- Track multiple phases executing simultaneously
- Coordinate parallel state updates in Memory MCP
- Handle session recovery for parallel workflows

#### `orchestrator/agent_callback.py` - Result Processing
**Classes:**
- `AgentCallbackManager` - Agent completion and result processing

**Key Methods:**
```python
def process_agent_result(agent_id: str, result: Dict[str, Any]) -> Dict[str, Any]
def handle_agent_completion(agent_id: str, deliverables: Dict[str, Any]) -> Dict[str, Any]
```

**Parallel Agent Role:**
- Process multiple simultaneous results
- Aggregate parallel deliverables
- Coordinate completion detection

### Tool and Model Management

#### `orchestrator/manager_tools.py` - Tool Discovery & Management
**Classes:**
- `ToolManager` - Dynamic tool discovery and execution

**Key Methods:**
```python
def __init__(self, tools_directory: str = "./tools")
def discover_tools(self) -> Dict[str, Any]
def get_available_tools(self) -> List[Dict[str, Any]]
def get_tool_details(self, tool_name: str) -> Dict[str, Any]
def interactive_tool_selection(user_goal: str, model: str, budget_preference: str) -> Dict[str, Any]
def create_tool_button(tool_name: str, workflow_id: str, context: Dict = None) -> str
def load_tool_config(self, tool_name: str) -> Dict[str, Any]
def validate_tool_requirements(self, tool_name: str) -> bool
def _create_mcp_tool_button(self, tool_info: Dict, workflow_id: str, context: Dict) -> str
```

#### `orchestrator/manager_models.py` - Model Selection & Management
**Classes:**
- `ModelManager` - Model configuration and selection

**Key Methods:**
```python
def get_available_models() -> List[Dict[str, Any]]
def select_optimal_model(task_type: str, preferences: Dict = None) -> str
def get_model_config(model_name: str) -> Dict[str, Any]
def estimate_model_cost(model_name: str, estimated_tokens: int) -> float
def get_model_capabilities(model_name: str) -> Dict[str, Any]
```

#### `orchestrator/manager_buttons.py` - Button Generation
**Classes:**
- `ButtonManager` - Code snippet generation system

**Key Methods:**
```python
def create_api_call_snippet(model: str, instructions: str, system_message: str = None) -> str
def create_tool_execution_snippet(tool_name: str, params: Dict[str, Any]) -> str
```

### Memory and State Management

#### `orchestrator/memory_mcp.py` - Memory MCP Integration
**Classes:**
- `MemoryMCPManager` - Memory MCP integration and coordination
- `LocalMemoryFallback` - Local fallback when MCP unavailable

**MemoryMCPManager Methods:**
```python
def __init__(self, config_path: str = None)
def initialize() -> bool
def test_connection() -> bool
def estimate_cost(operation: str = "memory_operation") -> float
def create_workflow(workflow_data: Dict[str, Any]) -> str
def prepare_agent_handoff(workflow_id: str, agent_context: Dict[str, Any]) -> bool
def restore_agent_context(workflow_id: str) -> Dict[str, Any]
def recover_session(session_data: Dict[str, Any]) -> Dict[str, Any]
```

**LocalMemoryFallback Methods:**
```python
def __init__(self)
def create_entities(entities: List[Dict]) -> List[str]
def add_observations(observations: List[Dict]) -> bool
def _load_json(file_path, default)
def _save_data()
```

#### `orchestrator/user_memory_manager.py` - User Memory Storage
**Classes:**
- `UserMemoryManager` - User-specific memory storage and retrieval

**Key Methods:**
```python
def __init__(self)
def store_memory(user_id: str, content: str, category: str = None, tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]
def retrieve_memories(user_id: str, query: str, category: str = None, limit: int = 10, include_metadata: bool = False) -> List[Dict[str, Any]]
def delete_memory(user_id: str, memory_id: str) -> Dict[str, Any]
def suggest_contextual_memories(user_id: str, current_context: str, workflow_type: str = None) -> List[Dict[str, Any]]
def _store_memory_to_file(username: str, memory: Dict[str, Any], category: str)
def _store_memory_to_mcp(user_id: str, memory: Dict[str, Any])
def _delete_memory_from_mcp(user_id: str, memory_id: str)
def _auto_categorize_content(content: str) -> str
def _auto_generate_tags(content: str) -> List[str]
def _extract_context_triggers(content: str) -> List[str]
```

#### `orchestrator/mcp_hub.py` - MCP Integration Hub
**Classes:**
- `MCPIntegrationHub` - Unified MCP system coordination

**Key Methods:**
```python
def __init__(self)
def create_workflow(workflow_config: Dict[str, Any]) -> str
def update_workflow_state(workflow_id: str, state_update: Dict[str, Any]) -> bool
def get_workflow_state(workflow_id: str) -> Dict[str, Any]
def store_session_context(session_data: Dict[str, Any]) -> bool
def restore_session_context(session_id: str) -> Dict[str, Any]
def health_check() -> Dict[str, bool]
def _initialize_servers()
def _setup_memory_mcp()
def _setup_files_api()
def _setup_mcp_connector()
```

### Analytics and Metrics

#### `orchestrator/user_analytics_manager.py` - User Analytics
**Classes:**
- `UserAnalyticsManager` - User-specific analytics with GDPR compliance

**Data Classes:**
```python
@dataclass
class SessionMetric:
    session_id: str
    start_time: str
    end_time: str = None
    duration_minutes: int = 0
    workflow_count: int = 0
    tool_activations: int = 0

@dataclass
class ToolUsageMetric:
    tool_name: str
    total_uses: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    last_used: str = None

@dataclass
class WorkflowMetric:
    workflow_id: str
    workflow_command: str
    start_time: str
    end_time: str = None
    duration_minutes: int = 0
    success: bool = False
    tags: List[str] = None

@dataclass
class CostMetric:
    date: str
    model_name: str
    total_cost: float
    session_count: int = 1
    session_ids: List[str] = None
```

**Key Methods:**
```python
def __init__(self, user_dir: str = "./configs/user/")
def estimate_cost(operation: str = "analytics_operation") -> float
def track_session(username: str, session_id: str, action: str, **kwargs) -> bool
def track_tool_usage(username: str, tool_name: str, success: bool, response_time: float) -> bool
def track_workflow(username: str, workflow_id: str, workflow_command: str, action: str, **kwargs) -> bool
def track_costs(username: str, date: str, model_name: str, cost: float, session_id: str = None) -> bool
def scan_available_tools(username: str) -> List[str]
def _get_user_analytics_dir(username: str) -> Path
def _ensure_analytics_dir(username: str) -> Path
def _read_analytics_file(username: str, filename: str) -> Dict[str, Any]
def _write_analytics_file(username: str, filename: str, data: Dict[str, Any]) -> bool
```

#### `orchestrator/system_analytics_manager.py` - System Analytics
**Classes:**
- `SystemAnalyticsManager` - System-wide performance tracking

**Key Methods:**
```python
def track_performance(tool_name: str, response_time: float, success: bool, error_type: str)
def track_health(metric_name: str, value: float, trend: str)
def calculate_time_patterns(user_analytics_data: List[Dict]) -> Dict
def _anonymize_user_data(user_data: Dict) -> Dict
```

#### `orchestrator/real_time_metrics.py` - Live Metrics
**Classes:**
- `SystemMetricsProvider` - Live system metrics for UI
- `WorkflowMonitor` - Real-time workflow progress tracking

**SystemMetricsProvider Methods:**
```python
def get_dashboard_metrics() -> Dict[str, Any]
def get_workflow_progress(workflow_id: str) -> Dict[str, Any]
def get_live_stats() -> Dict[str, Any]
def _calculate_progress_percentage(workflow_status: Dict) -> float
def _get_phase_details(workflow_id: str, execution_history: List) -> List[Dict]
```

**WorkflowMonitor Methods:**
```python
def subscribe(callback)
def on_workflow_start(workflow_id: str, workflow_info: Dict)
def on_phase_start(workflow_id: str, phase_info: Dict)
def on_phase_progress(workflow_id: str, progress_info: Dict)
def on_phase_complete(workflow_id: str, result_info: Dict)
```

### Configuration and Management

#### `orchestrator/settings_manager.py` - Settings Management
**Classes:**
- `ApplicationSettingsManager` - Application settings discovery and management
- `SettingDefinition` - Settings schema definition

**Key Methods:**
```python
def discover_settings(force_refresh: bool = False) -> Dict[str, SettingDefinition]
def get_default_settings() -> Dict[str, Any]
def get_user_settings(username: str) -> Dict[str, Any]
def get_settings_by_section() -> Dict[str, List[str]]
def load_user_settings(user_id: str) -> Dict[str, Any]
def save_user_settings(user_id: str, settings: Dict[str, Any])
def validate_settings(settings: Dict[str, Any]) -> bool
```

#### `orchestrator/cli_manager.py` - CLI Command Management
**Classes:**
- `CLICommandsManager` - CLI command discovery and execution

**Key Methods:**
```python
def execute_slash_command(command: str, args: str) -> Dict[str, Any]
def get_autocomplete_suggestions(partial: str) -> List[str]
def discover_cli_commands() -> Dict[str, Any]
def execute_command(command_name: str, args: List[str], session_context: Dict) -> Dict[str, Any]
```

#### `orchestrator/username_manager.py` - User Management
**Classes:**
- `UserManager` - User creation and session management

**Key Methods:**
```python
def generate_user_id(username: str) -> str
def validate_username(username: str) -> bool
def create_user_profile(username: str) -> Dict[str, Any]
def get_user_profile(user_id: str) -> Dict[str, Any]
```

#### `orchestrator/workflow_manager.py` - Workflow Management
**Classes:**
- `WorkflowManager` - Workflow ID generation and tracking
- `WorkflowExecutor` - Workflow execution coordination

**Key Methods:**
```python
def generate_workflow_id(with_explanation: bool = False) -> str
def track_workflow(workflow_id: str, action: str, metadata: Dict = None)
def get_workflow_status(workflow_id: str) -> Dict[str, Any]
```

### Conversation and Bridge Systems

#### `orchestrator/conversation_bridge.py` - Natural Language Processing
**Classes:**
- `ConversationToWorkflowBridge` - Convert natural language to workflow configs
- `JSONConfigNormalizer` - Schema validation and normalization

**Key Methods:**
```python
def estimate_cost(params: Dict[str, Any]) -> float
def create_workflow_from_conversation(user_goal: str) -> Dict[str, Any]
def normalize_config(config_data: Dict, config_type: str) -> Dict[str, Any]
```

### Infrastructure

#### `orchestrator/cache/cache_system.py` - Caching System
**Classes:**
- `CacheManager` - Dual-layer hybrid caching system

**Key Methods:**
```python
def __init__(self, cache_dir: str = "./.cache", verbose: bool = False)
def get_cached_analysis(cache_key: str, component_name: str) -> Optional[str]
def cache_content_analysis(cache_key: str, content: str, component_name: str)
def get_cached_tool_result(tool_name: str, tool_hash: str) -> Optional[Dict[str, Any]]
def cache_tool_result(tool_name: str, tool_hash: str, result: Dict[str, Any])
async def store_workflow_file(content: str, filename: str, anthropic_client) -> str
async def retrieve_workflow_file(file_id: str, anthropic_client) -> Optional[str]
def clear_cache(pattern: str = None)
def get_cache_stats() -> Dict[str, Any]
def generate_content_hash(content: str) -> str
```

#### `orchestrator/error_handling.py` - Error Management
**Classes:**
```python
class OrchestrationError(Exception):  # Base exception
class ValidationError(OrchestrationError):  # Input validation failures
class ProcessingError(OrchestrationError):  # Tool processing failures
class ResourceError(OrchestrationError):   # Resource access failures
class APIError(OrchestrationError):        # External API call failures
```

**Decorators and Functions:**
```python
@handle_errors(operation_name: str, return_dict: bool = True)
def retry_with_backoff(func, max_retries: int = 3)
def log_error(error: Exception, context: str)
def setup_orchestrator_logging()
```

## Tool File Index

### Current Tool Structure (4-File Pattern)

Each tool follows the same pattern:
- `[tool_name].py` - Main logic with class and standalone functions
- `button_[tool_name].py` - Button snippet generation
- `ui_[tool_name].py` - Display and formatting
- `tool_[tool_name].json` - Configuration

### Tool Files by Directory

#### `tools/brave_search/`
- **Main Class:** `BraveSearchManager`
- **Key Functions:** `search()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_brave_search_result()`

#### `tools/code_execution/`
- **Main Class:** `CodeExecutionManager`
- **Key Functions:** `execute_python_code()`, `execute_code_with_files()`, `create_persistent_container()`, `download_execution_files()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_code_execution_result()`

#### `tools/dalle_generate/`
- **Main Class:** `DalleManager`
- **Key Functions:** `generate_image()`, `batch_generate()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_dalle_generate_result()`

#### `tools/file_operations/`
- **Main Class:** `FileOperationsManager`
- **Key Functions:** `read_file()`, `write_file()`, `list_directory()`, `search_files()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_file_operations_result()`

#### `tools/files_api/`
- **Main Class:** `FilesAPIManager`
- **Key Functions:** `create_file()`, `retrieve_file()`, `delete_file()`, `list_files()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_files_api_result()`

#### `tools/graphic_design/`
- **Main Class:** `GraphicDesignManager`
- **Key Functions:** `analyze_image()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_graphic_design_result()`

#### `tools/mcp_connector/`
- **Main Class:** `MCPConnectorManager`
- **Key Functions:** `list_mcp_servers()`, `execute_mcp_tool()`, `register_mcp_server()`, `get_mcp_server_status()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_mcp_connector_result()`

#### `tools/perplexity_search/`
- **Main Class:** `PerplexitySearchManager`
- **Key Functions:** `search()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_perplexity_search_result()`

#### `tools/text_editor/`
- **Main Class:** `TextEditorManager`
- **Key Functions:** `edit_text()`, `format_text()`, `analyze_text()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_text_editor_result()`

#### `tools/think/`
- **Main Class:** `ThinkingManager`
- **Key Functions:** `think()`, `analyze_problem()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_think_result()`

#### `tools/web_search/`
- **Main Class:** `WebSearchManager`
- **Key Functions:** `search()`, `estimate_cost()`
- **Button Function:** `create_button_snippet()`
- **UI Function:** `display_web_search_result()`

## Interface File Index

### `interfaces/ui_terminal.py` - Terminal Interface
**Classes:**
- `TerminalInterface` - Main terminal UI coordination
- `SubprocessCommunicationBridge` - Node.js bridge communication

**Key Methods:**
```python
def process_user_input(user_input: str, session_context: Dict) -> Dict[str, Any]
def generate_contextual_tips(session_state: Dict) -> List[str]
def handle_nodejs_message(message: Dict) -> Dict[str, Any]
def send_to_nodejs(response: Dict) -> bool
def execution_start() -> None
def phase_start(phase_num: int, total_phases: int, phase_name: str, model: str, estimated_cost: float) -> None
def phase_complete(result: ExecutionResult) -> None
def workflow_complete(workflow: WorkflowPlan, results: Dict[str, Any]) -> None
```

### `interfaces/ui_web.py` - Web Interface
**Classes:**
- `WebInterface` - Web-based UI coordination

---

# Architecture Insights

## Parallel Agent Execution System

### Phase Number Pattern Recognition
```python
# Sequential phases
"01", "02", "03" → Execute one after another

# Parallel phases  
"01a", "01b", "01c" → Execute simultaneously in group "01"

# Mixed workflow
Group "01" (parallel) → Group "02" (sequential) → Group "03a", "03b" (parallel)
```

### Implementation Pattern for Parallel Agents
```python
def _group_parallel_phases(self, phases: List[WorkflowPhase]) -> List[List[WorkflowPhase]]:
    """Group phases by their base phase number for parallel execution"""
    phase_groups = {}
    
    for phase in phases:
        # Extract base phase number (01a -> 01, 02b -> 02, 03 -> 03)
        phase_num = getattr(phase, 'phase_number', str(phases.index(phase) + 1))
        base_num = ''.join(filter(str.isdigit, phase_num))
        
        if base_num not in phase_groups:
            phase_groups[base_num] = []
        phase_groups[base_num].append(phase)
    
    return [phase_groups[key] for key in sorted(phase_groups.keys())]

async def execute_workflow_async(self, workflow_id: str) -> Dict[str, Any]:
    """Execute workflow with parallel phase support using AsyncAnthropic"""
    from anthropic import AsyncAnthropic
    import asyncio
    
    async_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    workflow = self.active_workflows[workflow_id]
    
    # Group phases for parallel execution
    phase_groups = self._group_parallel_phases(workflow.phases)
    
    results = []
    workflow_memory = {}
    
    for group in phase_groups:
        if len(group) > 1:
            # Execute multiple phases in parallel
            tasks = [
                self._execute_phase_async(phase, workflow, workflow_memory, async_client)
                for phase in group
            ]
            parallel_results = await asyncio.gather(*tasks)
            results.extend(parallel_results)
        else:
            # Single phase execution
            result = await self._execute_phase_async(group[0], workflow, workflow_memory, async_client)
            results.append(result)
    
    return {"results": results, "parallel_groups": len([g for g in phase_groups if len(g) > 1])}
```

### Key Files for Parallel Implementation
1. **`core.py`** - Add async execution logic and phase grouping
2. **`agent_orchestrator.py`** - Handle multiple simultaneous agent completions
3. **`workflow_state.py`** - Track parallel execution states
4. **`agent_callback.py`** - Process multiple simultaneous results
5. **`ui_terminal.py`** - Display parallel execution progress

## Data Flow Patterns

### Standard Caching Flow
```
User Input → Cache Check → Process (if miss) → Cache Result → Return
```

### Workflow Execution Flow
```
Goal → Analysis → Phase Design → Model Selection → Execution → Results → Caching
```

### Tool Integration Flow
```
Discovery → Configuration → Execution → Button Generation → UI Display → Analytics
```

### Memory Integration Flow
```
Store → Memory MCP → Local Fallback → Retrieval → Context Integration
```

## Standard Patterns

### Required Imports (All Files)
```python
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError
from typing import Dict, Any, List
import json

cache = CacheManager()
```

### Required Functions (All Components)
```python
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """REQUIRED: Estimate operation cost for budget planning"""
    return 0.001  # Adjust based on complexity

@handle_errors(operation_name="function_name", return_dict=True)
def main_function(self, params: Dict[str, Any]) -> Dict[str, Any]:
    """Standard error handling pattern"""
    # Implementation here
    pass
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

### Standard UI Display Pattern
```python
from rich.console import Console

# Module-level console
console = Console()

def display_component_result(results: Dict[str, Any]) -> str:
    """REQUIRED: Main display function with standard naming"""
    if not results or results.get("status") != "success":
        return display_error("Operation failed")
    
    # Format results
    return formatted_output

def display_error(error_msg: str) -> str:
    """REQUIRED: Standard error display function"""
    return f"❌ Error: {error_msg}"
```

## Analytics Trigger Points

### Session Analytics
- **Trigger Location:** `interfaces/ui_terminal.py`
- **Methods:** `track_session(username, session_id, action, **kwargs)`
- **Actions:** "start", "end", "update_workflow_count", "update_tool_activations"

### Tool Usage Analytics
- **Trigger Location:** `orchestrator/manager_tools.py`
- **Methods:** `track_tool_usage(username, tool_name, success, response_time)`
- **Tracked:** Usage count, success rate, response time, last used

### Workflow Analytics
- **Trigger Location:** `orchestrator/workflow_manager.py`
- **Methods:** `track_workflow(username, workflow_id, command, action, **kwargs)`
- **Actions:** "start", "complete"
- **Metadata:** Tags, success status, duration

### Cost Analytics
- **Trigger Locations:** `orchestrator/manager_models.py`, `orchestrator/real_time_metrics.py`
- **Methods:** `track_costs(username, date, model_name, cost, session_id)`
- **Tracked:** Daily costs by model, session attribution

### Memory Analytics
- **Trigger Location:** `configs/cli/memory/memory.py`
- **Commands:** `/memory "content"`, `/memory --list`, `/memory --delete [ID]`
- **Tracked:** Memory creation, retrieval, deletion

## JSON Configuration Schemas

### Workflow Configuration Schema
```json
{
  "workflow": [
    {
      "user_id": "user-0663",
      "workflow_id": "uid-qmt-465",
      "custom_command": "marketing strategy startup",
      "workflow_goal": "Create comprehensive marketing strategy",
      "workflow_deliverable": "Marketing strategy report",
      "workflow_description": "Detailed workflow description",
      "temp_directory": "configs/workflows/.temp/marketing-strategy-startup/"
    }
  ]
}
```

### Phase Configuration Schema (Parallel Support)
```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01a",
      "phase_goal": "Market research - Demographics",
      "phase_deliverable": "Demographics report",
      "phase_description": "Research target demographics",
      "resources": ["web_search", "data_analysis"],
      "tools": ["brave_search", "perplexity_search"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-opus-4",
      "provider_1": "anthropic-direct"
    },
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01b", 
      "phase_goal": "Market research - Competitors",
      "phase_deliverable": "Competitor analysis",
      "phase_description": "Analyze competitor landscape",
      "resources": ["web_search", "competitive_analysis"],
      "tools": ["web_search", "text_editor"],
      "model_1": "claude-sonnet-4"
    }
  ]
}
```

### Handoff Configuration Schema
```json
{
  "handoff": [
    {
      "workflow_id": "uid-qmt-465",
      "handoff_number": "01",
      "assessment_questions": [
        "Is the market research complete?",
        "Are demographics clearly defined?",
        "Is competitor analysis thorough?"
      ],
      "human_in_loop": false,
      "next_phase_conditions": {
        "all_parallel_complete": true,
        "quality_threshold": "acceptable"
      }
    }
  ]
}
```

## Directory Structure Reference

### Tool Directory Structure
```
tools/
└── [tool_name]/
    ├── [tool_name].py          # Main logic with class + standalone functions
    ├── button_[tool_name].py   # Button snippet generation
    ├── ui_[tool_name].py       # Display and formatting  
    └── tool_[tool_name].json   # Configuration
```

### CLI Command Directory Structure
```
configs/cli/
└── [command_name]/
    ├── [command_name].py       # Command logic
    ├── ui_[command_name].py    # UI components
    └── [command_name].json     # Configuration
```

### Configuration Directory Structure
```
configs/
├── cli/                        # CLI command configurations
├── models/                     # Model configurations
├── providers/                  # Provider configurations  
├── settings/                   # Application settings
├── user/[username]/           # User-specific configurations
└── workflows/                 # Workflow templates and configs
```

## File Naming Conventions

### Required Patterns
- **Tool files:** `[tool_name].py`, `button_[tool_name].py`, `ui_[tool_name].py`, `tool_[tool_name].json`
- **CLI files:** `[command_name].py`, `ui_[command_name].py`, `[command_name].json`
- **Config files:** Use underscore separators, not hyphens
- **Directory names:** Use underscore separators

### Examples
- ✅ `brave_search.py`, `ui_brave_search.py`, `tool_brave_search.json`
- ✅ `help.py`, `ui_help.py`, `help.json`
- ❌ `brave-search.py`, `braveSearch.py`, `brave_search_tool.json`

## Common Implementation Mistakes

### Import Errors
- ❌ `from orchestrator import cache`
- ✅ `from orchestrator.cache.cache_system import CacheManager`

### Function Naming
- ❌ `def processData()` or `def process_Data()`
- ✅ `def process_data()`

### Cache Key Format
- ❌ `cache_key = f"{param1}-{param2}"`
- ✅ `cache_key = f"component|{param1}|{param2}"`

### Error Decorator Usage
- ❌ `@handle_errors("function_name")`
- ✅ `@handle_errors(operation_name="function_name", return_dict=True)`

### JSON Config Fields
- ❌ `"id": "tool_name"` or `"tool_id": "tool_name"`
- ✅ `"name": "tool_name"`

### Button File Entry Points
- ❌ Multiple functions: `create_search_snippet()`, `create_analysis_snippet()`
- ✅ Single entry point: `create_button_snippet()` with operation dispatch

### UI Function Naming
- ❌ `display_results()`, `show_output()`
- ✅ `display_[component_name]_result()` (matches component name)

## Validation Checklist for New Components

### Required Elements
- [ ] `estimate_cost()` function with proper signature
- [ ] `@handle_errors` decorators on main functions
- [ ] `CacheManager` integration with standard patterns
- [ ] Standard import structure
- [ ] Proper error handling with specific error types
- [ ] JSON config with `"name"` field (not `"id"`)
- [ ] UI functions follow display pattern
- [ ] File naming follows conventions

### Tool-Specific Requirements
- [ ] Main class with manager suffix (`ToolNameManager`)
- [ ] Standalone functions for button imports
- [ ] Single `create_button_snippet()` entry point
- [ ] 4-file structure complete
- [ ] Tool JSON config includes operations and cost estimate

### CLI-Specific Requirements
- [ ] Command class with manager suffix (`CommandNameManager`)
- [ ] UI display function matches command name
- [ ] 3-file structure complete
- [ ] Command JSON config includes terminal_flag and type

---

This primer eliminates the need for AI file exploration and provides the complete development context for MAO. Reference `CLAUDE.md` for coding standards and principles.