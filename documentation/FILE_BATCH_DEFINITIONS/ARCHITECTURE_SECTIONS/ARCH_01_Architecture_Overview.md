# Architecture Overview - LOCAL Application Patterns

## Introduction

The Modular Agent Orchestrator (Mao) implements a LOCAL-only application architecture designed as a professional terminal application that runs entirely on the user's machine. This architecture pattern emphasizes subprocess communication, dynamic discovery, and privacy-first design while avoiding any web service capabilities.

## Core Architectural Principles

### LOCAL Application Architecture

Mao follows a fundamental architectural principle that distinguishes it from web-based systems:

- **❌ MAO does NOT provide APIs** - No web server, no endpoints for external clients
- **✅ MAO CONSUMES APIs** - Calls OpenAI, Anthropic, search services, and other external providers
- **✅ Like Claude Code** - Local terminal application that integrates with external services

This LOCAL-first approach ensures user privacy, reduces attack surface, and provides reliable offline capabilities while maintaining access to powerful cloud-based AI services.

### Subprocess Communication Architecture

**TO BE IMPLEMENTED**: The system is designed to support sophisticated subprocess communication patterns between Node.js frontend and Python backend. The current terminal interface includes placeholder structures for this functionality:

```python
# TO BE IMPLEMENTED: SubprocessCommunicationBridge in ui_terminal.py
class SubprocessCommunicationBridge:
    """
    TO BE IMPLEMENTED: Node.js ↔ Python subprocess communication bridge
    
    This class will handle structured message passing between the Node.js
    terminal UI and the Python backend for rich terminal interface functionality.
    """
    
    def __init__(self, terminal_interface: 'TerminalInterface'):
        self.terminal_interface = terminal_interface
        self.message_queue = []
        self.subprocess_handlers = {}
    
    def handle_nodejs_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """TO BE IMPLEMENTED: Process incoming messages from Node.js terminal UI"""
        pass
    
    def send_to_nodejs(self, response: Dict[str, Any]) -> None:
        """TO BE IMPLEMENTED: Send structured responses to Node.js terminal UI"""
        pass
```

### Dynamic Discovery Patterns

Mao implements comprehensive dynamic discovery to eliminate hardcoded dependencies:

```python
# Dynamic Command Discovery - mao_v4.py
def load_all_commands():
    """Load all command configs dynamically"""
    commands = {}
    cli_dir = Path(__file__).parent / "configs" / "cli"
    
    for json_file in cli_dir.glob("*.json"):
        if json_file.name.endswith('.OLD'):
            continue
        try:
            with open(json_file) as f:
                cmd_config = json.load(f)
                commands[cmd_config["command"]] = cmd_config
        except (json.JSONDecodeError, KeyError):
            continue  # Skip malformed files
    
    return commands
```

This pattern enables:
- Automatic registration of new components
- Zero-configuration module addition
- Extensible architecture without code changes
- Maintenance-free system expansion

## System Bootstrap Sequence

### Application Initialization Flow

The system follows a carefully orchestrated bootstrap sequence ensuring proper initialization order:

```python
# Main Bootstrap Sequence - mao_v4.py
@handle_errors(operation_name="main", return_dict=True)
def main():
    """Pure dynamic routing - zero hardcoding"""
    
    # Special handling for 'mao mao' command
    if len(sys.argv) == 2 and sys.argv[1] == "mao":
        # User typed 'mao mao' - trigger smart launch
        interface = bootstrap_interface()
        interface.launch_terminal_ui_smart()
        return
    
    # Load all commands and create parser
    commands = load_all_commands()
    parser = create_dynamic_parser(commands)
    args = parser.parse_args()
    
    # Bootstrap interface
    interface = bootstrap_interface()
    
    # Find which command was used
    cmd_config, value = find_used_command(args, commands)
    
    try:
        if cmd_config:
            # Route to the interface method specified in JSON
            method_name = cmd_config["interface_method"]
            method = getattr(interface, method_name)
            
            # Call with appropriate arguments based on type
            if cmd_config["type"] == "standalone":
                method()
            else:
                method(value)
        else:
            # No command provided - default to onboarding
            interface.launch_terminal_ui_onboarding()
```

### MCP Hub Integration

The Memory Control Protocol (MCP) hub provides centralized state management:

```python
# MCP Hub - orchestrator/mcp_hub.py
class MCPIntegrationHub:
    """Unified MCP system providing state persistence, file management, and tool connectivity"""
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        # Initialize core components
        self.memory = MemoryMCPManager()
        self.files = FilesAPIManager()
        self.connector = MCPConnector()
        
        # Wire components together
        self.files.set_memory_mcp(self.memory)
        self.connector.set_memory_manager(self.memory)
        
        # Initialize external servers
        self._initialize_servers()
    
    def _initialize_servers(self):
        """Initialize default MCP servers"""
        try:
            results = self.connector.initialize_default_servers()
            for server_name, result in results.items():
                if result["status"] == "registered":
                    print(f"✅ MCP server {server_name}: {result['tools_count']} tools")
                else:
                    print(f"⚠️  MCP server {server_name}: {result.get('error', 'failed')}")
        except Exception as e:
            print(f"Warning: Failed to initialize MCP servers: {e}")
```

## Component Architecture Patterns

### Four-File Tool Structure

Every tool in Mao follows a standardized four-file architecture pattern:

```
tools/
├── tool_name/
│   ├── tool_name.py          # Core tool implementation
│   ├── button_tool_name.py   # Button generation for UI
│   ├── ui_tool_name.py       # UI integration and display
│   └── tool_tool_name.json   # Configuration and metadata
```

Example tool implementation:

```python
# tools/web_search/web_search.py
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

@handle_errors(operation_name="web_search", return_dict=True)
def perform_web_search(query: str, max_results: int = 5, search_context: str = "general") -> Dict[str, Any]:
    """
    Perform web search operation (returns structured data for human button execution)
    """
    # Validate inputs
    if not query or not query.strip():
        raise ValidationError("Search query cannot be empty", "query", query)
    
    if max_results < 1 or max_results > 20:
        raise ValidationError("Max results must be between 1 and 20", "max_results", max_results)
    
    # Check cache first (fingerprinting)
    cache = CacheManager()
    cache_key = f"{query.strip()}|{max_results}|{search_context}"
    cached_result = cache.get_cached_analysis(cache_key, "web_search")
    if cached_result:
        return json.loads(cached_result)
    
    # Prepare search configuration
    search_config = {
        "status": "ready_for_execution",
        "operation": "web_search",
        "query": query.strip(),
        "max_results": max_results,
        "search_context": search_context,
        "timestamp": datetime.now().isoformat(),
        "estimated_cost": _calculate_search_cost(max_results),
        "execution_method": "anthropic_native_web_search"
    }
    
    # Cache the result (fingerprinting)
    cache.cache_content_analysis(cache_key, json.dumps(search_config), "web_search")
    
    return search_config

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    max_results = params.get("max_results", 5)
    return _calculate_search_cost(max_results)
```

### CLI Command Architecture

CLI commands follow a three-file pattern with JSON-driven configuration:

```python
# configs/cli/goal/goal.py
@handle_errors(operation_name="goal", return_dict=True)
def execute_goal(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main goal command execution with caching and error handling.
    
    Args:
        params: Command parameters containing user goal text
        
    Returns:
        Standardized result dictionary with workflow creation results
    """
    if not params or not params.get("goal"):
        raise ValidationError("Goal text is required", "goal", params.get("goal") if params else None)
    
    goal_text = params["goal"].strip()
    user_id = params.get("user_id", "default_user")
    
    # Create workflow through conversation bridge
    bridge = ConversationToWorkflowBridge()
    workflow_result = bridge.create_workflow_from_goal(goal_text, user_id)
    
    if workflow_result.get("success"):
        return {
            "success": True,
            "workflow_id": workflow_result["workflow_id"],
            "goal": goal_text,
            "status": "created",
            "next_steps": workflow_result.get("next_steps", [])
        }
    else:
        return workflow_result
```

```json
// configs/cli/goal.json
{
  "command": "goal",
  "type": "needs_input",
  "terminal_flag": "--goal",
  "app_command": "/goal",
  "interface_method": "goal",
  "help": "Create entire workflow from goal description",
  "cost_estimate": 0.008,
  "logic_file": "configs/cli/goal/goal.py",
  "ui_file": "configs/cli/goal/ui_goal.py",
  "operations": {
    "execute": {
      "description": "Create workflow from natural language goal",
      "required_params": ["goal"],
      "optional_params": ["user_id", "complexity_hint"]
    }
  },
  "integration": {
    "memory_mcp": true,
    "cache_system": true,
    "error_handling": true,
    "manager_touchpoints": ["conversation_bridge", "workflow_manager", "workflow_state"]
  }
}
```

## Error Handling and Resilience

### Comprehensive Error Management

Mao implements layered error handling ensuring system resilience:

```python
# orchestrator/error_handling.py
class OrchestrationError(Exception):
    """Base exception for orchestration tools"""
    def __init__(self, message: str, error_code: str = "ORCHESTRATION_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

class ValidationError(OrchestrationError):
    """Raised when input validation fails"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        details = {"field": field, "value": str(value) if value is not None else None}
        super().__init__(message, "VALIDATION_ERROR", details)

class ProcessingError(OrchestrationError):
    """Raised when tool processing fails"""
    def __init__(self, message: str, operation: str = None, stage: str = None):
        details = {"operation": operation, "stage": stage}
        super().__init__(message, "PROCESSING_ERROR", details)

class ResourceError(OrchestrationError):
    """Raised when resource access fails"""
    def __init__(self, message: str, resource_type: str = None, resource_path: str = None):
        details = {"resource_type": resource_type, "resource_path": resource_path}
        super().__init__(message, "RESOURCE_ERROR", details)

class APIError(OrchestrationError):
    """Raised when external API calls fail"""
    def __init__(self, message: str, api_name: str = None, status_code: int = None):
        details = {"api_name": api_name, "status_code": status_code}
        super().__init__(message, "API_ERROR", details)

def handle_errors(operation_name: str = "operation", 
                 return_dict: bool = True,
                 log_errors: bool = True) -> Callable:
    """Decorator for comprehensive error handling with professional patterns"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except OrchestrationError as e:
                # Handle known orchestration errors
                error_info = {
                    "error": e.message,
                    "error_code": e.error_code,
                    "operation": operation_name,
                    "timestamp": e.timestamp,
                    "details": e.details
                }
                
                if log_errors:
                    logging.error(f"Orchestration Error in {operation_name}: {e.message}", extra=e.details)
                
                if return_dict:
                    return error_info
                else:
                    raise
            
            except Exception as e:
                # Handle unexpected errors
                error_info = {
                    "error": f"Unexpected error: {str(e)}",
                    "error_code": "UNEXPECTED_ERROR",
                    "operation": operation_name,
                    "timestamp": datetime.now().isoformat(),
                    "details": {
                        "exception_type": type(e).__name__,
                        "traceback": traceback.format_exc()
                    }
                }
                
                if log_errors:
                    logging.error(f"Unexpected error in {operation_name}: {str(e)}", exc_info=True)
                
                if return_dict:
                    return error_info
                else:
                    raise ProcessingError(f"Unexpected error: {str(e)}", operation_name, "exception")
        
        return wrapper
    return decorator
```

### Graceful Degradation Patterns

The system implements fallback mechanisms for robust operation:

```python
# MCP Hub Fallback Example
async def get_workflow_state(self, workflow_id):
    """Get workflow state with MCP and local fallbacks"""
    try:
        # Primary: Memory MCP
        if self.memory_mcp:
            return await self.memory_mcp.get_workflow(workflow_id)
    except Exception as e:
        logger.warning(f"MCP unavailable: {e}")
    
    try:
        # Secondary: Local file system
        return await self.load_local_workflow(workflow_id)
    except Exception as e:
        logger.warning(f"Local storage unavailable: {e}")
    
    # Tertiary: Empty state with recovery planning
    return self.create_recovery_workflow(workflow_id)
```

## Privacy and Security Architecture

### LOCAL-First Privacy Design

The architecture prioritizes user privacy through LOCAL-only operation:

- **No data transmission** except to user-chosen AI providers
- **Local storage only** for all user data and configurations
- **User-controlled deletion** with GDPR compliance
- **No analytics servers** - all metrics stored locally

### Data Isolation Patterns

```python
# User Data Management - orchestrator/username_manager.py
class UsernameManager:
    """
    Manages user accounts, session persistence, and settings integration
    Implements delta-only storage for user settings
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "configs"
        self.user_dir = self.base_path / "user"
        self.examples_dir = self.base_path / "examples"
        self.session_file = self.user_dir / ".last_session"
        
        # Ensure directories exist
        self.user_dir.mkdir(exist_ok=True)
    
    @handle_errors(operation_name="create_user", return_dict=True)
    def create_user(self, username: str, first_name: str = "", last_name: str = "", 
                   email: str = "", dob: str = "") -> Dict[str, Any]:
        """Create a new user with generated user_id"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        clean_username = username.strip().lower()
        
        # Generate user_id using meid script
        try:
            user_id = generate_user_id(username)
        except Exception as e:
            raise APIError(f"Failed to generate user ID: {str(e)}")
        
        # Create user data
        user_data = {
            "username": username,
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "dob": dob,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        # Create nested directory structure
        user_dir = self.user_dir / clean_username
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Create memories and analytics subdirectories
        (user_dir / "memories").mkdir(exist_ok=True)
        (user_dir / "analytics").mkdir(exist_ok=True)
        
        # Save user file in nested structure
        user_file = user_dir / f"user_{clean_username}.json"
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return {
            "success": True,
            "message": f"User '{username}' created successfully",
            "user_data": user_data
        }
```

## Performance Optimization Patterns

### Caching Architecture

MAO implements intelligent dual-layer caching for optimal performance:

```python
# orchestrator/cache/cache_system.py
class CacheManager:
    """🔄 Dual-layer caching: Files API + Local fingerprinting"""
    
    def __init__(self, cache_dir: str = "~/.oc_cache", verbose: bool = False):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(exist_ok=True)
        self.verbose = verbose
        
        # Create cache subdirectories
        (self.cache_dir / "content_analysis").mkdir(exist_ok=True)
        (self.cache_dir / "tool_definitions").mkdir(exist_ok=True)
        (self.cache_dir / "workflow_memory").mkdir(exist_ok=True)
        
        # Active workflow file tracking
        self.workflow_files: Dict[str, str] = {}  # file_id -> content_hash
        self.session_memory: Dict[str, Any] = {}
    
    def generate_content_hash(self, content: str) -> str:
        """📄 Generate fingerprint for content"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def cache_content_analysis(self, content: str, analysis: str, cache_type: str = "content_analysis") -> str:
        """💾 Cache content analysis permanently"""
        content_hash = self.generate_content_hash(content)
        
        cache_entry = CacheEntry(
            content=analysis,
            created_at=datetime.now().isoformat(),
            content_hash=content_hash,
            cache_type=cache_type
        )
        
        cache_file = self.cache_dir / cache_type / f"{content_hash}.json"
        cache_file.parent.mkdir(exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(asdict(cache_entry), f, indent=2)
        
        return content_hash
    
    def get_cached_analysis(self, content: str, cache_type: str = "content_analysis") -> Optional[str]:
        """📄 Get cached content analysis"""
        content_hash = self.generate_content_hash(content)
        cache_file = self.cache_dir / cache_type / f"{content_hash}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache_entry = json.load(f)
            return cache_entry["content"]
        
        return None
```

### Cost Estimation Integration

Every operation includes cost estimation for budget planning:

```python
def estimate_cost(operation_type: str, **params):
    """Universal cost estimation for budget planning"""
    base_costs = {
        "tool_execution": {"time_ms": 1000, "complexity": "low"},
        "ai_request": {"tokens": 100, "time_ms": 2000, "complexity": "medium"},
        "file_operation": {"time_ms": 50, "complexity": "low"}
    }
    
    base = base_costs.get(operation_type, {"time_ms": 500, "complexity": "low"})
    
    # Dynamic cost calculation based on parameters
    if "query_length" in params:
        base["time_ms"] *= (params["query_length"] / 100)
        
    if "file_size" in params:
        base["time_ms"] += params["file_size"] / 1000
        
    return base
```

## Integration Guidelines

### Adding New Tools

To add a new tool to the system:

1. **Create tool directory** following four-file structure
2. **Implement logic.py** with error handling and caching
3. **Create configuration JSON** with proper metadata
4. **Add UI components** for display and interaction
5. **Generate button snippets** for workflow integration

The system will automatically discover and integrate the new tool through dynamic discovery patterns.

### Extending CLI Commands

New CLI commands integrate automatically:

1. **Create command directory** with three-file structure
2. **Add JSON configuration** to configs/cli/
3. **Implement command logic** with standardized interfaces
4. **Add UI integration** for display formatting

The dynamic command discovery system will automatically register and route the new command.

## Conclusion

MAO's LOCAL application architecture provides a robust, privacy-first foundation for AI orchestration. The combination of subprocess communication, dynamic discovery, comprehensive error handling, and performance optimization creates a professional-grade system that scales efficiently while maintaining user privacy and system reliability.

This architecture enables developers to extend the system seamlessly while maintaining consistency, performance, and privacy standards across all components.