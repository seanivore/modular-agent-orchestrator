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

The system uses a sophisticated subprocess communication pattern between Node.js frontend and Python backend:

```python
# Python Interface Layer - ui_terminal.py
class TerminalInterface:
    def __init__(self):
        self.mcp_hub = None
        self.logger = setup_logger(__name__)
    
    async def handle_subprocess_command(self, command, data=None):
        """Handle commands from Node.js subprocess calls"""
        try:
            result = await self.route_command(command, data)
            return {"status": "success", "data": result, "display_type": result.get("display_type")}
        except Exception as e:
            return {"status": "error", "message": str(e), "display_type": "error"}
```

```javascript
// Node.js Subprocess Integration
const { spawn } = require('child_process');

function executeCommand(command, data) {
    const python = spawn('python3', [
        'interfaces/ui_terminal.py', 
        '--command', command, 
        '--data', JSON.stringify(data)
    ]);
    
    python.stdout.on('data', (data) => {
        const result = JSON.parse(data.toString());
        handleResponse(result.display_type, result);
    });
}
```

### Dynamic Discovery Patterns

Mao implements comprehensive dynamic discovery to eliminate hardcoded dependencies:

```python
# Dynamic Command Discovery - mao_v4.py
def load_all_commands():
    """Dynamically discover all CLI commands from JSON configurations"""
    commands = {}
    config_dir = Path(__file__).parent / "configs" / "cli"
    
    for config_file in config_dir.glob("*.json"):
        if ".OLD" in config_file.name:
            continue
            
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                commands[config['command']] = config
        except json.JSONDecodeError as e:
            logger.warning(f"Malformed JSON in {config_file}: {e}")
            
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
async def main():
    # 1. Special case handling for smart launch
    if len(sys.argv) == 2 and sys.argv[1] == "mao":
        return await handle_smart_launch()
    
    # 2. Dynamic command discovery
    commands = load_all_commands()
    
    # 3. Argument parser creation from configurations
    parser = create_parser_from_configs(commands)
    args = parser.parse_args()
    
    # 4. Interface and MCP hub initialization
    interface = bootstrap_interface()
    
    # 5. Command routing and execution
    await route_to_interface_method(interface, args, commands)
```

### MCP Hub Integration

The Memory Control Protocol (MCP) hub provides centralized state management:

```python
# MCP Hub Bootstrap - orchestrator/mcp_hub.py
class MCPHub:
    def __init__(self):
        self.memory_mcp = None
        self.files_api = None
        self.workflow_state = {}
        
    async def initialize(self):
        """Initialize MCP connections and workflow state"""
        try:
            self.memory_mcp = await self.setup_memory_mcp()
            self.files_api = await self.setup_files_api()
            await self.restore_workflow_state()
        except Exception as e:
            logger.warning(f"MCP initialization failed: {e}")
            # Graceful fallback to local state management
```

## Component Architecture Patterns

### Four-File Tool Structure

Every tool in Mao follows a standardized four-file architecture pattern:

```
tools/
├── tool_name/
│   ├── logic.py              # Core tool implementation
│   ├── button_tool_name.py   # Button generation for UI
│   ├── ui_tool_name.py       # UI integration and display
│   └── tool_name.json        # Configuration and metadata
```

Example tool implementation:

```python
# tools/web_search/logic.py
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

class WebSearchTool:
    def __init__(self):
        self.cache = CacheManager()
        
    @handle_errors
    async def execute(self, query: str, **kwargs):
        """Execute web search with caching and error handling"""
        cache_key = f"web_search:{hash(query)}"
        
        if cached_result := await self.cache.get(cache_key):
            return cached_result
            
        result = await self.perform_search(query)
        await self.cache.set(cache_key, result)
        return result
        
    def estimate_cost(self, query: str):
        """Estimate resource cost for budget planning"""
        return {
            "tokens": len(query.split()) * 1.2,
            "time_ms": 2000,
            "api_calls": 1,
            "complexity": "medium"
        }
```

### CLI Command Architecture

CLI commands follow a three-file pattern with JSON-driven configuration:

```python
# cli/goal/command.py
@handle_errors
async def execute_goal_command(args, interface):
    """Execute goal command with user input processing"""
    goal_text = args.goal_text or await prompt_for_goal()
    
    workflow = await interface.create_workflow(goal_text)
    
    return {
        "display_type": "workflow_created",
        "workflow_id": workflow.id,
        "goal": goal_text,
        "status": "initialized"
    }
```

```json
// configs/cli/goal.json
{
    "command": "goal",
    "terminal_flag": "--goal",
    "type": "workflow",
    "interface_method": "handle_goal_command",
    "description": "Create or modify workflow goals",
    "examples": [
        "mao goal \"Build a website\"",
        "mao --goal \"Analyze data\""
    ]
}
```

## Error Handling and Resilience

### Comprehensive Error Management

Mao implements layered error handling ensuring system resilience:

```python
# orchestrator/error_handling.py
class MAOError(Exception):
    """Base exception for all MAO-specific errors"""
    pass

class ToolExecutionError(MAOError):
    """Raised when tool execution fails"""
    pass

class ConfigurationError(MAOError):
    """Raised when configuration is invalid"""
    pass

def handle_errors(func):
    """Decorator for comprehensive error handling"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except MAOError as e:
            logger.error(f"MAO Error in {func.__name__}: {e}")
            return {"status": "error", "type": "mao_error", "message": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return {"status": "error", "type": "system_error", "message": "An unexpected error occurred"}
    return wrapper
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
# User Data Isolation - orchestrator/username_manager.py
class UsernameManager:
    def __init__(self):
        self.user_data_dir = Path.home() / ".mao" / "users"
        
    def get_user_directory(self, username):
        """Get isolated directory for user data"""
        user_dir = self.user_data_dir / username
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
        
    def delete_user_data(self, username):
        """Complete user data deletion for GDPR compliance"""
        user_dir = self.get_user_directory(username)
        if user_dir.exists():
            shutil.rmtree(user_dir)
            logger.info(f"User data deleted for: {username}")
```

## Performance Optimization Patterns

### Caching Architecture

MAO implements intelligent dual-layer caching for optimal performance:

```python
# orchestrator/cache/cache_system.py
class CacheManager:
    def __init__(self):
        self.memory_cache = {}
        self.files_api = None
        
    async def get(self, key: str):
        """Intelligent cache retrieval with fingerprinting"""
        # Layer 1: Memory cache
        if key in self.memory_cache:
            return self.memory_cache[key]
            
        # Layer 2: Files API cache
        if self.files_api:
            try:
                content = await self.files_api.read_file(f"cache/{key}")
                self.memory_cache[key] = content
                return content
            except FileNotFoundError:
                pass
                
        return None
        
    async def set(self, key: str, value: any):
        """Intelligent cache storage with deduplication"""
        content_hash = hashlib.sha256(str(value).encode()).hexdigest()
        
        # Memory cache
        self.memory_cache[key] = value
        
        # Files API cache with deduplication
        if self.files_api:
            await self.files_api.write_file(f"cache/{key}", value)
            await self.files_api.write_file(f"cache/{key}.hash", content_hash)
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