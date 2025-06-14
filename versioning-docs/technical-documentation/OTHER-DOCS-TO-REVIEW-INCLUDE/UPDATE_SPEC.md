# The MAO Philosophy 





#### Use-Case Development Setup  

Because we have an orchestrator, setup of workflows is done with the AI orchestrator to ensure the workflow is created correctly and understood. 

1. User runs a 'Workflow Development' agent that calls Claude 4, our workflow orchestrator 
2. Initially, the user comes prepared with the sections of the JSON config ready, in notes 
3. User provides the notes and describes the project's tasks they need to complete 
4. The orchestrator and User back-and-forth until there is an understanding and the most effective workflow has been created 
5. The orchestrator will then create the complete JSON config file 
6. The orchestrator will run the config file with the setup script for the use-case 
7. The orchestrator will then return the workflow to the user in the form of a README.me that contains the custom commands needed to run the workflow, as well as any other specifics like where to place input resource files or where to expect output completed file. 
8. After this first development session, User can run the workflow whenever they need 

#### Workflow Process 

1. User runs workflow command 
2. Orchestrator starts the workflow 
   - They gather information needed for the fist task 
   - OC calls the first agent 
   - OC records progress notes in their log 
   - OC commits all necessary conversation history, task information, etc. to their 'memory.py' file to maintain context when they are called back in after the first agent has completed their task 
3. Handoff of task to first agent which includes: 
   - Auto-save feature document
   - Live document token counter
   - Reminder of their token limit 
   - 'Human button' snippets to run for any tool use they may need 
   - 'Human button' snippet to run to call the orchestrator when complete (or to handle any other issues they may have)
4. Agent works on and completes their task 
5. Agent calls the OC when finished to hand in their work 
   - Communicates directly their task report 
   - Orchestrator records that report in the log for their workflow report  
   - Agent hands over any deliverables 
   - Orchestrator uses the Anthropic Files API to save draft deliverables  
   - If ever they needed more time or to fix something, the orchestrator can reset the loops to allow the agent to stay in the context and finish the task 
6. Orchestrator coordinates the next agent in the workflow 
...
This continues until the workflow is complete. 

#### Workflow Completion Observations 

- Note that only 'human button' snippets are handed off to agents. 
This allows us to work with LLMs from any provider and require nothing more than the API call to summon the LLM. 

- The orchestrator connects directory with the agent before and after they work on their task. 
This allows us to remove any need for tools that are purely logistical. It also means that there is no need for agents to "save_output" or any other function that would previously have triggered the end of a task phase. 

- The orchestrator is the only one that can save files. 
This is because the orchestrator is the only one that has access to the Anthropic Files API, which is being leveraged because it is free. When the final document is complete, then the OC will save the final version of the document to the user's directory. 

- The agents are provided the same functional convenience in their document tools as humans expect. 
They have auto-save, this prevents the need for them to save their output. And they have a token counter, this prevents the need for them to worry about their token when completing the task. When they received their task, a token limit for that specific LLM or limit as dictated by the Use-Case, is provided. No need to check tokens with a special tool to exit.





## Tool Creation 6-File Architecture Pattern


For each tool, create exactly 4 files, update 2 files: 

```
./components/tools/tool_name/...
├── tool_name.py              # 1. Core Logic
├── ui_tool_name.py           # 2. UI Display
├── button_tool_name.py       # 3. Human Buttons
└── tool_name.json            # 4. Tool Registry
./build/orchestrator/...
├── /master/error_handling.py  # 5. Shared Error Handling
└── /cache/cache_system.py     # 6. Shared Cache System
```

### 🔧 File-by-File Implementation

#### 1. Core Logic File (`tool_name_modular.py`)

**Purpose**: Pure functionality with enhanced error handling
**Rules**: NO UI, NO hardcoded specifics, structured data return

```python
"""
Tool Name
Independent tool logic with enhanced error handling
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import time


def main_function(param1: str, param2: int = 10, param3: str = "default") -> Dict[str, Any]:
    """
    Execute tool functionality with comprehensive error handling
    
    Args:
        param1: Primary input parameter
        param2: Optional numeric parameter
        param3: Optional string parameter
        
    Returns:
        Dict with structured results or error information
    """
    try:
        # Validation
        if not param1.strip():
            return {"error": "Primary parameter cannot be empty"}
        
        # Clamp numeric values to valid ranges
        param2 = min(20, max(1, param2))
        
        # API Configuration (if needed)
        api_key = os.getenv("API_KEY_NAME")
        if not api_key:
            return {"error": "API key not found. Set API_KEY_NAME environment variable"}
        
        # Main logic with retry pattern
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Your main logic here
                result = perform_operation(param1, param2, param3)
                
                if result:
                    break
                    
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {str(e)}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Process and return structured results
        return {
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": processed_results,
            "metadata": {
                "processing_time": processing_time,
                "parameters_used": {"param1": param1, "param2": param2, "param3": param3}
            }
        }
        
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1
        }


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for this operation"""
    # Return realistic cost estimate for workflow planning
    return 0.001
```

#### 2. UI Display File (`ui_tool_name.py`)

**Purpose**: Beautiful terminal output formatting
**Rules**: NO business logic, clean vs verbose modes, Rich console formatting

```python
"""
TOOL NAME
UI Display Component
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def display_tool_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Take structured data → beautiful terminal output
    
    Args:
        result: Tool result data
        verbose: Show detailed technical information
    """
    console = Console()
    
    # Handle error cases
    if "error" in result:
        console.print(f"❌ Tool Error: {result['error']}", style="red")
        if verbose and "timestamp" in result:
            console.print(f"   Timestamp: {result['timestamp']}", style="dim")
        return
    
    # Handle empty results
    if not result.get("results"):
        console.print(f"⚠️ No results found", style="yellow")
        return
    
    # Main results display
    input_param = result.get("input_param", "Unknown input")
    results = result.get("results", [])
    
    # Header
    if verbose:
        header_text = f"🔧 Tool Results: {input_param} ({len(results)} items)"
        console.print(Panel(header_text, style="blue"))
    else:
        console.print(f"🔧 Found {len(results)} results for: {input_param}", style="blue bold")
    
    # Results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item", style="bold")
    table.add_column("Description", style="dim")
    
    if verbose:
        table.add_column("Details", style="link")
    
    for i, item in enumerate(results, 1):
        title = item.get("title", "No title")[:60] + "..." if len(item.get("title", "")) > 60 else item.get("title", "No title")
        description = item.get("description", "No description")[:100] + "..." if len(item.get("description", "")) > 100 else item.get("description", "No description")
        
        if verbose:
            details = item.get("details", "No details")
            table.add_row(str(i), title, description, details)
        else:
            table.add_row(str(i), title, description)
    
    console.print(table)
    
    # Verbose metadata
    if verbose:
        metadata = result.get("metadata", {})
        if metadata:
            console.print("\n📊 Processing Metadata:", style="bold")
            
            if "processing_time" in metadata:
                console.print(f"   Processing Time: {metadata['processing_time']:.2f}s")
            
            console.print(f"   Timestamp: {result.get('timestamp', 'Unknown')}")


def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for tool operation"""
    console = Console()
    
    if cost == 0:
        console.print("💰 Cost: FREE", style="green bold")
    else:
        console.print(f"💰 Estimated cost: ${cost:.4f}", style="yellow")


def format_for_agent_handoff(results: Dict[str, Any]) -> str:
    """Format results for agent-to-agent handoff"""
    if "error" in results:
        return f"Tool execution failed: {results['error']}"
    
    input_param = results.get("input_param", "Unknown input")
    results_list = results.get("results", [])
    
    if not results_list:
        return f"No results found for: {input_param}"
    
    # Format top results for handoff
    formatted_results = [f"Tool results for '{input_param}' ({len(results_list)} items):\n"]
    
    for i, item in enumerate(results_list[:5], 1):  # Top 5 for handoff
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        
        formatted_results.append(f"{i}. {title}")
        formatted_results.append(f"   {description}\n")
    
    return "\n".join(formatted_results)
```

### 3. Human Button File (`button_tool_name.py`)

**Purpose**: Generate executable code snippets for Claude 4
**Rules**: Self-contained, universal model compatibility, built-in cost tracking

```python
"""
TOOL NAME
Human Button Generators
"""

from typing import Dict, Any


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude 4 execution
    Universal model compatibility via code generation
    
    Args:
        params: Tool parameters
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    # Extract parameters with defaults
    param1 = params.get("param1", "")
    param2 = params.get("param2", 10)
    param3 = params.get("param3", "default")
    
    # Generate self-contained executable snippet
    snippet = f'''# Tool Name Execution
# Model: {model}
# Input: {param1}

import json
import requests
import os
import time
from datetime import datetime

def execute_tool():
    """Execute tool with comprehensive error handling"""
    
    # Tool parameters
    param1 = "{param1}"
    param2 = {param2}
    param3 = "{param3}"
    
    try:
        # Validation
        if not param1.strip():
            return {{"error": "Primary parameter cannot be empty", "cost": 0.0}}
        
        # Clamp values to valid ranges
        param2 = min(20, max(1, param2))
        
        # API Configuration (if needed)
        api_key = os.getenv("API_KEY_NAME")
        if not api_key:
            return {{
                "error": "API key not found. Set API_KEY_NAME environment variable",
                "cost": 0.0
            }}
        
        # Main logic with retry pattern
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Your main logic here
                result = perform_operation(param1, param2, param3)
                
                if result:
                    break
                    
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {{attempt + 1}}/{{max_retries}})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {{str(e)}}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Check final result
        if not result:
            return {{
                "error": f"Tool execution failed after {{max_retries}} attempts. Last error: {{last_error}}",
                "cost": 0.001
            }}
        
        # Process and return structured results
        tool_results = {{
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": result,
            "metadata": {{
                "processing_time": processing_time,
                "parameters_used": {{"param1": param1, "param2": param2, "param3": param3}}
            }},
            "cost": 0.001  # Adjust based on actual API costs
        }}
        
        return tool_results
        
    except Exception as e:
        return {{
            "error": f"Tool execution failed: {{str(e)}}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1,
            "cost": 0.001
        }}

# Execute the tool
result = execute_tool()

# Display results
print("🔧 Tool Execution Results:")
print(f"Input: {param1}")
print(f"Status: {{result.get('status', 'error')}}")
print(f"Cost: ${{result.get('cost', 0.001):.4f}}")

if result.get('error'):
    print(f"❌ Error: {{result['error']}}")
else:
    print("✅ Tool executed successfully")
    print(f"Results: {{len(result.get('results', []))}}")

# Return structured result for orchestrator
result'''
    
    return snippet


def estimate_execution_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for executing this tool"""
    # Return realistic cost estimate
    return 0.001


def get_tool_capabilities() -> Dict[str, Any]:
    """Return tool capabilities for orchestrator discovery"""
    return {
        "name": "tool_name",
        "capabilities": ["capability1", "capability2", "capability3"],
        "cost_estimate": 0.001,
        "models_supported": ["all"],
        "tags": ["tag1", "tag2", "tag3"],
        "parameters": {
            "param1": {"type": "string", "required": True, "description": "Primary input parameter"},
            "param2": {"type": "integer", "default": 10, "description": "Optional numeric parameter"},
            "param3": {"type": "string", "default": "default", "description": "Optional string parameter"}
        }
    }
```

### 4. Tool Registry File (`tool_name.json`)

**Purpose**: Tool metadata and discovery configuration
**Rules**: Clean metadata, NO hardcoded use cases, capability-based discovery

```json
{
  "id": "tool_name",
  "name": "Tool Display Name",
  "description": "Brief description of tool functionality with enhanced error handling",
  "version": "1.0.0",
  "capabilities": [
    "capability1",
    "capability2", 
    "capability3"
  ],
  "tags": [
    "tag1",
    "tag2", 
    "tag3"
  ],
  "cost_estimate": 0.001,
  "models_supported": ["all"],
  "dependencies": ["requests", "API_KEY_NAME"],
  "parameters": {
    "param1": {
      "type": "string",
      "required": true,
      "description": "Primary input parameter"
    },
    "param2": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 20,
      "description": "Optional numeric parameter"
    },
    "param3": {
      "type": "string",
      "default": "default",
      "description": "Optional string parameter"
    }
  },
  "functions": [
    {
      "name": "main_function",
      "description": "Execute primary tool functionality",
      "parameters": ["param1", "param2", "param3"]
    },
    {
      "name": "estimate_cost",
      "description": "Estimate operation cost",
      "parameters": ["params"]
    }
  ],
  "files": {
    "core_logic": "tools/tool_name_modular.py",
    "ui_display": "interfaces/ui_tools/ui_tool_name.py", 
    "buttons": "utilities/button_tools/button_tool_name.py"
  },
  "error_handling": {
    "retry_logic": true,
    "timeout_handling": true,
    "rate_limit_handling": true,
    "graceful_degradation": true
  },
  "output_format": {
    "success": {
      "status": "success",
      "input_param": "string",
      "timestamp": "string", 
      "results": "array",
      "metadata": "object",
      "cost": "float"
    },
    "error": {
      "error": "string",
      "timestamp": "string",
      "input_param": "string",
      "cost": "float"
    }
  }
}
```

### 5. Shared Error Handling (`build/orchestrator/master/error_handling.py`)

**Purpose**: Common error patterns for all tools
**Rules**: Reusable functions, professional retry logic, graceful degradation

```python
"""
Shared Error Handling Patterns
Common retry logic, validation, and graceful degradation for all SFA v4 tools
"""

import time
import requests
from typing import Callable, Any, Dict, Optional
from functools import wraps


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retry logic with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries (seconds)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.Timeout as e:
                    last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                        continue
                    raise e
                except requests.exceptions.RequestException as e:
                    last_error = f"Network error: {str(e)}"
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                        continue
                    raise e
                except Exception as e:
                    # Don't retry on non-network errors
                    raise e
            
            raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")
        
        return wrapper
    return decorator


def validate_api_response(response: requests.Response) -> Dict[str, Any]:
    """
    Common API response validation
    
    Args:
        response: HTTP response object
        
    Returns:
        Validation result with status and error info
    """
    if response.status_code == 200:
        return {"valid": True, "data": response.json()}
    elif response.status_code == 429:
        return {"valid": False, "error": "Rate limited", "retry_after": response.headers.get("Retry-After")}
    elif response.status_code == 401:
        return {"valid": False, "error": "Authentication failed - check API key"}
    elif response.status_code == 403:
        return {"valid": False, "error": "Access forbidden - insufficient permissions"}
    elif response.status_code >= 500:
        return {"valid": False, "error": f"Server error ({response.status_code}) - try again later"}
    else:
        return {"valid": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}


def handle_rate_limits(response: requests.Response) -> Optional[float]:
    """
    Universal rate limit handling
    
    Args:
        response: HTTP response object
        
    Returns:
        Recommended wait time in seconds, or None if no rate limiting
    """
    if response.status_code == 429:
        # Check for Retry-After header
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
        
        # Default rate limit wait
        return 60.0
    
    return None


def safe_api_call(url: str, headers: Dict[str, str], params: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    """
    Safe API call with comprehensive error handling
    
    Args:
        url: API endpoint URL
        headers: Request headers
        params: Request parameters
        timeout: Request timeout in seconds
        
    Returns:
        Standardized response with error handling
    """
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        
        # Handle rate limiting
        wait_time = handle_rate_limits(response)
        if wait_time:
            time.sleep(wait_time)
            # Retry once after rate limit
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
        
        # Validate response
        validation = validate_api_response(response)
        if validation["valid"]:
            return {"success": True, "data": validation["data"]}
        else:
            return {"success": False, "error": validation["error"]}
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error - check network"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def validate_required_params(params: Dict[str, Any], required: list) -> Dict[str, Any]:
    """
    Validate required parameters are present and non-empty
    
    Args:
        params: Parameter dictionary
        required: List of required parameter names
        
    Returns:
        Validation result
    """
    missing = []
    empty = []
    
    for param in required:
        if param not in params:
            missing.append(param)
        elif not str(params[param]).strip():
            empty.append(param)
    
    if missing or empty:
        error_parts = []
        if missing:
            error_parts.append(f"Missing parameters: {', '.join(missing)}")
        if empty:
            error_parts.append(f"Empty parameters: {', '.join(empty)}")
        
        return {"valid": False, "error": "; ".join(error_parts)}
    
    return {"valid": True}
```

### 6. Shared Cache Integration (`build/orchestrator/cache/cache_system.py`) 

```python
"""
Cache Integration Example
Shows how modular tools integrate with universal cache and error handling
"""

from typing import Dict, Any
from ..error_handling import handle_errors, retry_with_backoff, ValidationError
from .universal_cache import get_global_cache, cache_operation, CacheFingerprint, ModelToolMapper

# Example: How a modular tool integrates with infrastructure

@handle_errors(operation_name="web_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0)
@cache_operation(operation="web_search", ttl_hours=6, estimated_cost=0.003)
def perform_web_search(query: str, search_type: str = "comprehensive", 
                      model: str = "claude-3-5-sonnet", context: str = "") -> Dict[str, Any]:
    """
    Example of modular tool function with full infrastructure integration
    
    This shows how a tool function can use:
    - Error handling with professional patterns
    - Retry logic with exponential backoff  
    - Universal caching with fingerprinting
    - Cost tracking and optimization
    """
    
    # Validate parameters (error handling will catch ValidationError)
    if not query.strip():
        raise ValidationError("Query cannot be empty", "query", query)
    
    # Simulate web search operation
    # In real implementation, this would call actual web search API
    search_results = {
        "query": query,
        "search_type": search_type,
        "model_used": model,
        "results": [
            {"title": f"Result for {query}", "url": "https://example.com", "snippet": "Example snippet"},
            {"title": f"Another result for {query}", "url": "https://example2.com", "snippet": "Another snippet"}
        ],
        "metadata": {
            "total_results": 2,
            "search_time": 0.5,
            "cached": False  # Will be updated by cache system
        }
    }
    
    return {
        "status": "success",
        "search_data": search_results,
        "message": "Web search completed successfully"
    }

def demonstrate_cache_integration():
    """Demonstrate how cache integration works"""
    
    # Get global cache instance
    cache = get_global_cache()
    
    # Get model-tool mapper
    mapper = ModelToolMapper(cache)
    
    print("🗄️ SFA v4 Cache Integration Demo")
    print("=" * 50)
    
    # Example 1: Basic operation with caching
    print("\n1. First search (will be cached):")
    result1 = perform_web_search(
        query="AI orchestration tools",
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result1['status']}")
    print(f"   Results: {len(result1['search_data']['results'])}")
    
    # Example 2: Same search (should hit cache)
    print("\n2. Same search (should hit cache):")
    result2 = perform_web_search(
        query="AI orchestration tools", 
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result2['status']}")
    print(f"   Results: {len(result2['search_data']['results'])}")
    
    # Example 3: Show cache statistics
    print("\n3. Cache Statistics:")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Example 4: Model optimization
    print("\n4. Model Optimization:")
    optimal_model = mapper.get_optimal_model("web_search", budget_limit=0.01)
    print(f"   Optimal model for budget $0.01: {optimal_model}")
    
    cost_estimate = mapper.get_cost_estimate("web_search", "claude-3-5-sonnet", "medium")
    print(f"   Estimated cost for claude-3-5-sonnet: ${cost_estimate:.4f}")
    
    # Example 5: Manual cache fingerprinting
    print("\n5. Manual Cache Fingerprinting:")
    fingerprint = CacheFingerprint.generate_fingerprint(
        operation="web_search",
        params={"query": "test", "search_type": "quick"},
        model="claude-3-haiku"
    )
    print(f"   Generated fingerprint: {fingerprint}")
    
    print("\n✅ Cache integration demo completed!")

def demonstrate_error_handling():
    """Demonstrate error handling integration"""
    
    print("\n⚠️ Error Handling Demo")
    print("=" * 30)
    
    # Example 1: Validation error
    print("\n1. Testing validation error:")
    result = perform_web_search(query="", search_type="comprehensive")
    if "error" in result:
        print(f"   Caught validation error: {result['error']}")
        print(f"   Error code: {result['error_code']}")
    
    # Example 2: Show how retry logic would work
    print("\n2. Retry logic is built-in for network failures")
    print("   (Would automatically retry with exponential backoff)")
    
    print("\n✅ Error handling demo completed!")

if __name__ == "__main__":
    # Run demonstrations
    demonstrate_cache_integration()
    demonstrate_error_handling() 
```



----

## Integration Points

### OC Discovery
```python
# OC can query tools by capability
tools = tool_discovery.find_tools_by_capability("research")
tools = tool_discovery.find_tools_by_tag("business")
tools = tool_discovery.find_tools_by_budget(max_cost=0.10)
```

### Human Button Generation
```python
# Each tool generates executable snippets
snippet = tool.create_button_snippet(
    params={"query": "renewable energy trends"},
    model="claude-sonnet-4"
)

# Claude 4 Code Execution Tool runs the snippet
result = execute_code_snippet(snippet)
```

### Cost Integration
```python
# Tools report their costs for workflow planning
estimated_cost = tool.estimate_cost(params)
actual_cost = tool.get_last_execution_cost()
```

### Dynamic Workflow Generation
```python
def generate_workflow(goal: str) -> dict:
    return {
        "command_name": auto_generated_name,
        "workspace": f"projects/{sanitized_goal}/",
        "workflow": {
            "research_phase": {
                "model": model_manager.get_best_model_for_task("research"),
                "execution_snippet": buttons.create_api_call_snippet(...),
                "deliverables": ["research-summary.md"]
            },
            "analysis_phase": {
                "model": model_manager.get_best_model_for_task("reasoning"), 
                "execution_snippet": buttons.create_api_call_snippet(...),
                "deliverables": ["strategy-plan.md"]
            }
        }
    }
```

### Workflow Orchestrator

```python
class WorkflowOrchestrator:
    def __init__(self, model_manager: ModelManager):
        self.models = model_manager
        self.protocol = self.load_protocol()
    
    async def create_workflow_from_goal(self, user_goal: str) -> dict:
        # "Research renewable energy and create marketing strategy"
        # ↓
        # Auto-generated optimal workflow with model selection
    
    async def execute_workflow(self, workflow: dict) -> dict:
        # Coordinate specialist agents via human button snippets
```

## Tool Metadata System

### Dynamic Tool Registry (`configs/tool_registry.json`)
```json
{
  "tools": {
    "web_search": {
      "id": "web_search",
      "name": "Native Web Search",
      "description": "Real-time web search with citations",
      "capabilities": ["research", "current_information"],
      "use_cases": ["market research", "news analysis", "fact checking"],
      "cost_per_use": 0.01,
      "tags": ["research", "web", "realtime"],
      "dependencies": ["anthropic_api"],
      "version": "1.0.0"
    }
  }
}
```

### OC Integration Pattern
```python
class ToolDiscovery:
    def interactive_tool_selection(self, goal: str, model: str, budget: str) -> Dict:
        # 1. Analyze goal for required capabilities
        capabilities = self.extract_capabilities_from_goal(goal)
        
        # 2. Find compatible tools
        compatible_tools = self.find_tools_by_capabilities(capabilities)
        compatible_tools = self.filter_by_model_compatibility(compatible_tools, model)
        compatible_tools = self.filter_by_budget(compatible_tools, budget)
        
        # 3. Generate suggestion with explanation
        return {
            "core_tools": ["web_search", "financial_analysis"],
            "optional_tools": ["competitor_analysis", "image_generation"],
            "core_explanation": "I recommend web search for research and financial analysis for ROI calculations",
            "estimated_tool_cost": 0.16,
            "user_choice_prompt": "Would you like to add any optional tools?"
        }
```

## Testing Strategy 

### Tool Validation Tests
```python
# Each tool must pass:
def test_tool_definition():
    """Validate tool definition structure"""
    definition = tool.get_tool_definition()
    assert "id" in definition
    assert "button_generator" in definition
    
def test_button_generation():
    """Test snippet generation"""
    snippet = tool.create_button_snippet(test_params, "claude-sonnet-4")
    assert snippet.startswith("# Tool:")
    assert "import" in snippet
    assert "return" in snippet

def test_cost_estimation():
    """Validate cost calculations"""
    cost = tool.estimate_cost(test_params)
    assert isinstance(cost, float)
    assert cost > 0
```

### Integration Tests
```python
def test_oc_tool_discovery():
    """Test OC can find and suggest tools"""
    tools = tool_discovery.find_tools_for_goal("Create marketing strategy")
    assert "web_search" in [t["id"] for t in tools]
    
def test_workflow_integration():
    """Test tools work in complete workflows"""
    workflow = orchestrator.create_workflow_from_goal("Research competitors")
    assert any("competitor_analysis" in phase.tools for phase in workflow.phases)
```

## Top Level Integrations

### Code Execution Tool (THE GAME CHANGER)
```python
# Instead of complex SDK management:
async def execute_model_call(snippet: str) -> dict:
    # Claude 4 executes the snippet directly!
    result = await anthropic_client.beta.messages.create(
        model="claude-sonnet-4",
        tools=[{"type": "code_execution_20241022", "name": "execute"}],
        messages=[{"role": "user", "content": f"Execute: {snippet}"}]
    )
    return parse_execution_result(result)
```

### Files API for Cost Optimization
```python
class DraftManager:
    async def save_draft(self, content: str, name: str):
        # FREE Files API storage!
        await anthropic_client.files.create(content=content, name=name)
    
    async def promote_to_final(self, draft_id: str, final_path: str):
        # Only final results hit expensive filesystem
        content = await anthropic_client.files.retrieve(draft_id)
        save_to_real_filesystem(content, final_path)
```

### Parallel Tool Execution
```python
async def parallel_specialists(tasks: List[Task]) -> List[Result]:
    # Multiple agents working simultaneously!
    snippets = [
        buttons.create_api_call_snippet(task.optimal_model, task.prompt)
        for task in tasks
    ]
    
    # Claude 4 can execute tools in parallel
    results = await asyncio.gather(*[
        execute_code_snippet(snippet) for snippet in snippets
    ])
    
    return orchestrator.synthesize_results(results)
```

### Extended Thinking + Tools
```python
# Orchestrator can think while coordinating
orchestrator_response = await anthropic_client.beta.messages.create(
    model="claude-sonnet-4",
    tools=orchestrator_tools,
    thinking=True,  # Extended thinking while using tools!
    messages=[{"role": "user", "content": "Plan and execute this complex workflow..."}]
)
```

### Memory Files for Workflow State
```python
class WorkflowMemory:
    async def save_workflow_state(self, workflow_id: str, state: dict):
        # Claude 4's memory capabilities
        memory_content = json.dumps(state)
        await anthropic_client.files.create(
            content=memory_content,
            name=f"workflow_{workflow_id}_state.json"
        )
```


### Dynamic Tool Loading
```python
class ToolManager:
    def get_tools_for_task(self, task_type: str) -> List[ToolDefinition]:
        # Only load relevant tools, not everything!
        toolkits = self.config.get_toolkits_for_task(task_type)
        return self.load_minimal_tool_set(toolkits)
    
    def generate_tool_snippet(self, tool_name: str, params: dict) -> str:
        # Generate executable snippet for tool use
        return f"result = {tool_name}({json.dumps(params)})"
```

### Code Execution Tool Integration
```python
# Instead of complex tool implementations:
def web_search_snippet(query: str) -> str:
    return f'''
import requests
response = requests.get("https://api.brave.com/search", 
                       params={{"q": "{query}"}})
result = response.json()
print(result)
'''

def image_optimization_snippet(image_path: str) -> str:
    return f'''
from PIL import Image
img = Image.open("{image_path}")
optimized = img.resize((1200, 800), Image.Resampling.LANCZOS)
optimized.save("optimized_" + "{image_path}")
print("Image optimized successfully")
'''
```