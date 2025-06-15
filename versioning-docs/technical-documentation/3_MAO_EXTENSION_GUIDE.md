# Mao Extension Guide
**Complete Guide to Adding Tools, Models, and Providers**

*Step-by-step instructions for extending Mao capabilities*

---

## 🎯 Overview

Mao's modular architecture enables unlimited extension without performance degradation. This guide provides complete instructions for adding new capabilities to your Mao instance.

### What You Can Add

**Tools** - New capabilities via 4-file architecture pattern
**Models** - Support for additional AI models via JSON configuration  
**Providers** - New API endpoints and services via connection configs

### Prerequisites

- Working Mao installation
- Basic understanding of Python and JSON
- API keys for new providers (if applicable)
- Text editor and terminal access

---

## 🛠️ Adding New Tools

### Complete 6-File Tool Creation Process

Every Mao tool follows the same structure. 

```
tools/your_new_tool/
├── your_new_tool.py          # Core functionality
├── tool_your_new_tool.json   # Configuration and metadata  
├── button_your_new_tool.py   # Human button interface
└── ui_your_new_tool.py       # User interface components
```

Every Mao tool shares two other files. 

```
orchestrator/
└── error_handling.py         # Shared across all files 
    └── cache/
        └── cache_system.py   # Shared across all files 
```

#### Step 1: Create Tool Directory

```bash
# Navigate to tools directory
cd tools/

# Create new tool directory
mkdir your_tool_name
cd your_tool_name
```

#### Step 2: Core Logic File (`your_tool_name.py`)

**Purpose**: Pure functionality with comprehensive error handling  
**Rules**: NO print statements, NO UI dependencies, structured data return

```python
"""
Your Tool Name - Core Logic
Pure functionality with comprehensive error handling
"""

import json
import time
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

def main_function(param1: str, param2: int = 10, param3: str = "default") -> Dict[str, Any]:
    """
    Execute tool functionality with comprehensive error handling
    
    Args:
        param1: Primary input parameter (required)
        param2: Optional numeric parameter (1-20, default 10)
        param3: Optional string parameter (default "default")
        
    Returns:
        Dict with structured results or error information
    """
    try:
        # Input validation
        if not param1.strip():
            return {
                "error": "Primary parameter cannot be empty",
                "timestamp": datetime.now().isoformat(),
                "cost": 0.0
            }
        
        # Parameter normalization
        param2 = min(20, max(1, param2))  # Clamp to valid range
        
        # API Configuration (if needed)
        api_key = os.getenv("YOUR_API_KEY_NAME")
        if not api_key:
            return {
                "error": "API key not found. Set YOUR_API_KEY_NAME environment variable",
                "cost": 0.0
            }
        
        # Main tool logic with retry pattern
        start_time = time.time()
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Your tool implementation here
                result = perform_your_operation(param1, param2, param3, api_key)
                
                if result:
                    break
                    
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {str(e)}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Check final result
        if not result:
            return {
                "error": f"Tool execution failed after {max_retries} attempts. Last error: {last_error}",
                "timestamp": datetime.now().isoformat(),
                "cost": 0.0
            }
        
        processing_time = time.time() - start_time
        
        return {
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": result,
            "metadata": {
                "processing_time": processing_time,
                "parameters_used": {
                    "param1": param1,
                    "param2": param2,
                    "param3": param3
                },
                "api_calls": 1,
                "retries": attempt
            },
            "cost": estimate_cost({"param1": param1, "param2": param2})
        }
        
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1,
            "cost": 0.0
        }

def perform_your_operation(param1: str, param2: int, param3: str, api_key: str):
    """
    Your actual tool implementation
    Replace this with your specific functionality
    """
    # Example implementation
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": param1,
        "intensity": param2,
        "mode": param3
    }
    
    response = requests.post(
        "https://api.yourservice.com/v1/process",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    response.raise_for_status()
    return response.json()

def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Calculate realistic cost estimate for workflow planning
    
    Args:
        params: Tool parameters
        
    Returns:
        Estimated cost in USD
    """
    # Your cost calculation logic
    base_cost = 0.001
    complexity_factor = len(params.get("param1", "")) / 1000
    intensity_multiplier = params.get("param2", 10) / 10
    
    return base_cost + (complexity_factor * intensity_multiplier)

def validate_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize input parameters
    
    Args:
        params: Raw input parameters
        
    Returns:
        Validated and normalized parameters
    """
    validated = {}
    
    # Required parameter validation
    if "param1" not in params or not params["param1"].strip():
        raise ValueError("param1 is required and cannot be empty")
    validated["param1"] = params["param1"].strip()
    
    # Optional parameter validation with defaults
    validated["param2"] = min(20, max(1, params.get("param2", 10)))
    validated["param3"] = params.get("param3", "default")
    
    return validated
```

#### Step 3: UI Display File (`ui_your_tool_name.py`)

**Purpose**: Beautiful terminal output formatting  
**Rules**: Print statements OK here, Rich formatting preferred

```python
"""
Your Tool Name - UI Display Component
Beautiful terminal output formatting
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

def display_tool_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Transform structured data into beautiful terminal output
    
    Args:
        result: Tool result data from core logic
        verbose: Show detailed technical information
    """
    console = Console()
    
    # Handle error cases
    if "error" in result:
        console.print(f"❌ [red]Tool Error:[/red] {result['error']}")
        if verbose and "timestamp" in result:
            console.print(f"   [dim]Timestamp: {result['timestamp']}[/dim]")
        return
    
    # Handle empty results
    if not result.get("results"):
        console.print("⚠️ [yellow]No results found[/yellow]")
        return
    
    # Main results display
    input_param = result.get("input_param", "Unknown input")
    results = result.get("results", {})
    
    # Header with input context
    if verbose:
        header_text = f"🔧 Your Tool Results: {input_param}"
    else:
        header_text = "🔧 Your Tool Results"
    
    console.print(f"\n[bold blue]{header_text}[/bold blue]")
    console.print("=" * 60)
    
    # Results presentation based on data structure
    if isinstance(results, dict):
        results_table = Table(show_header=True, header_style="bold magenta")
        results_table.add_column("Property", style="cyan")
        results_table.add_column("Value")
        
        for key, value in results.items():
            # Format different data types appropriately
            if isinstance(value, list):
                formatted_value = ", ".join(str(v) for v in value[:3])
                if len(value) > 3:
                    formatted_value += f" ... (+{len(value) - 3} more)"
            elif isinstance(value, dict):
                formatted_value = f"{len(value)} items"
            else:
                formatted_value = str(value)
            
            results_table.add_row(str(key), formatted_value)
        
        console.print(Panel(results_table, title="Results", border_style="green"))
        
    elif isinstance(results, list):
        console.print(f"📋 [cyan]Found {len(results)} items:[/cyan]")
        for i, item in enumerate(results[:10], 1):  # Show first 10 items
            console.print(f"  {i}. {str(item)}")
        
        if len(results) > 10:
            console.print(f"   [dim]... and {len(results) - 10} more items[/dim]")
            
    else:
        console.print(Panel(str(results), title="Results", border_style="green"))
    
    # Verbose technical details
    if verbose:
        metadata = result.get("metadata", {})
        cost = result.get("cost", 0.0)
        
        details_table = Table(show_header=False)
        details_table.add_column("", style="dim")
        details_table.add_column("")
        
        details_table.add_row("Processing Time:", f"{metadata.get('processing_time', 0):.3f}s")
        details_table.add_row("API Calls Made:", str(metadata.get('api_calls', 0)))
        details_table.add_row("Retries:", str(metadata.get('retries', 0)))
        details_table.add_row("Estimated Cost:", f"${cost:.6f}")
        details_table.add_row("Timestamp:", result.get("timestamp", ""))
        
        console.print(Panel(details_table, title="Technical Details", border_style="blue"))
    
    console.print(f"\n✅ [green]Tool execution completed successfully[/green]")

def display_tool_progress(operation_name: str, steps: List[str]) -> None:
    """
    Display progress for long-running operations
    
    Args:
        operation_name: Name of the operation being performed
        steps: List of step descriptions
    """
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        
        main_task = progress.add_task(f"[cyan]{operation_name}[/cyan]", total=len(steps))
        
        for step in steps:
            step_task = progress.add_task(f"[dim]{step}[/dim]", total=1)
            # Simulate work - replace with actual progress tracking
            time.sleep(0.5)
            progress.update(step_task, completed=1)
            progress.update(main_task, advance=1)

def display_validation_errors(errors: List[str]) -> None:
    """
    Display parameter validation errors
    
    Args:
        errors: List of validation error messages
    """
    console = Console()
    
    console.print("❌ [red]Parameter Validation Failed:[/red]")
    for error in errors:
        console.print(f"   • {error}")
    
    console.print("\n💡 [yellow]Tip:[/yellow] Use --help to see parameter requirements")

def display_cost_estimate(params: Dict[str, Any], estimated_cost: float) -> None:
    """
    Display cost estimate before execution
    
    Args:
        params: Operation parameters
        estimated_cost: Estimated cost in USD
    """
    console = Console()
    
    cost_panel = Panel(
        f"Parameters: {', '.join(f'{k}={v}' for k, v in params.items())}\n"
        f"Estimated Cost: ${estimated_cost:.6f}",
        title="💰 Cost Estimate",
        border_style="yellow"
    )
    
    console.print(cost_panel)
```

#### Step 4: Human Button Generator (`button_your_tool_name.py`)

**Purpose**: Generate executable code snippets for universal model compatibility  
**Rules**: Print statements OK for demo purposes, self-contained snippets

```python
"""
Your Tool Name - Human Button Generators
Executable code snippets for universal model compatibility
"""

from typing import Dict, Any
import json

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude 4 execution
    Universal model compatibility via self-contained code generation
    
    Args:
        params: Tool parameters from workflow
        model: Target model for execution optimization
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    # Extract and validate parameters
    param1 = params.get("param1", "")
    param2 = params.get("param2", 10)
    param3 = params.get("param3", "default")
    
    # Escape parameters for safe inclusion in code
    escaped_param1 = json.dumps(param1)
    escaped_param3 = json.dumps(param3)
    
    # Generate self-contained executable snippet
    snippet = f'''# Your Tool Execution
# Model: {model}
# Input: {param1}

import json
import time
import requests
import os
from datetime import datetime

def execute_your_tool():
    """Execute your tool with comprehensive error handling"""
    
    # Tool parameters
    param1 = {escaped_param1}
    param2 = {param2}
    param3 = {escaped_param3}
    
    print(f"🔧 Executing Your Tool...")
    print(f"📝 Input: {{param1}}")
    print(f"⚙️ Parameters: intensity={{param2}}, mode={{param3}}")
    
    try:
        # Input validation
        if not param1.strip():
            return {{
                "error": "Primary parameter cannot be empty",
                "cost": 0.0,
                "timestamp": datetime.now().isoformat()
            }}
        
        # Parameter normalization
        param2 = min(20, max(1, param2))
        
        # API Configuration
        api_key = os.getenv("YOUR_API_KEY_NAME")
        if not api_key:
            return {{
                "error": "API key not found. Set YOUR_API_KEY_NAME environment variable",
                "cost": 0.0,
                "timestamp": datetime.now().isoformat()
            }}
        
        print(f"✅ Validation passed")
        
        # Main execution logic with retry pattern
        start_time = time.time()
        max_retries = 3
        result = None
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 Attempt {{attempt + 1}}/{{max_retries}}")
                
                headers = {{
                    "Authorization": f"Bearer {{api_key}}",
                    "Content-Type": "application/json"
                }}
                
                payload = {{
                    "input": param1,
                    "intensity": param2,
                    "mode": param3
                }}
                
                response = requests.post(
                    "https://api.yourservice.com/v1/process",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()
                
                print(f"✅ API call successful")
                break
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Request timeout on attempt {{attempt + 1}}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
            except requests.exceptions.RequestException as e:
                print(f"🌐 Network error: {{str(e)}}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        if not result:
            return {{
                "error": "Tool execution failed after 3 attempts",
                "cost": 0.0,
                "timestamp": datetime.now().isoformat()
            }}
        
        processing_time = time.time() - start_time
        
        # Cost calculation
        base_cost = 0.001
        complexity_factor = len(param1) / 1000
        intensity_multiplier = param2 / 10
        total_cost = base_cost + (complexity_factor * intensity_multiplier)
        
        print(f"⏱️ Processing completed in {{processing_time:.3f}}s")
        print(f"💰 Estimated cost: ${{total_cost:.6f}}")
        
        return {{
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": result,
            "metadata": {{
                "processing_time": processing_time,
                "parameters_used": {{
                    "param1": param1,
                    "param2": param2,
                    "param3": param3
                }},
                "api_calls": 1,
                "retries": attempt
            }},
            "cost": total_cost
        }}
        
    except Exception as e:
        print(f"❌ Error during execution: {{str(e)}}")
        return {{
            "error": f"Tool execution failed: {{str(e)}}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1,
            "cost": 0.0
        }}

# Execute the tool and display results
result = execute_your_tool()

# Display formatted output
if result.get("status") == "success":
    print("\\n" + "="*50)
    print("🎉 YOUR TOOL EXECUTION SUCCESSFUL")
    print("="*50)
    
    # Display results summary
    results = result.get("results", {{}})
    if isinstance(results, dict):
        for key, value in list(results.items())[:5]:  # Show first 5 items
            print(f"✅ {{key}}: {{value}}")
        if len(results) > 5:
            print(f"   ... and {{len(results) - 5}} more items")
    else:
        print(f"✅ Results: {{results}}")
    
    print(f"💰 Total Cost: ${{result['cost']:.6f}}")
    print(f"⏱️ Duration: {{result['metadata']['processing_time']:.3f}}s")
else:
    print("\\n" + "="*50)  
    print("❌ YOUR TOOL EXECUTION FAILED")
    print("="*50)
    print(f"Error: {{result.get('error', 'Unknown error')}}")

# Return result for orchestrator
result
'''
    
    return snippet.strip()

def create_batch_operation_snippet(operations: List[Dict[str, Any]], model: str = "claude-sonnet-4") -> str:
    """
    Generate code snippet for batch operations
    
    Args:
        operations: List of operation parameters
        model: Target model for execution
        
    Returns:
        Executable code snippet for batch processing
    """
    
    snippet = f'''# Your Tool - Batch Operations
# Model: {model}
# Operations: {len(operations)}

import json
import time
from datetime import datetime

def execute_batch_operations():
    """Execute multiple tool operations in batch"""
    
    operations = {json.dumps(operations, indent=4)}
    
    print(f"🔧 Executing {{len(operations)}} operations in batch...")
    
    results = []
    total_cost = 0.0
    start_time = time.time()
    
    for i, operation in enumerate(operations, 1):
        print(f"\\n📝 Operation {{i}}/{{len(operations)}}: {{operation.get('param1', 'Unknown')}}")
        
        # Execute individual operation
        # (Include simplified version of main execution logic here)
        
        # Simulate operation for demo
        operation_result = {{
            "status": "success",
            "operation_index": i,
            "input": operation.get("param1", ""),
            "results": f"Processed {{operation.get('param1', '')}} successfully",
            "cost": 0.001
        }}
        
        results.append(operation_result)
        total_cost += operation_result["cost"]
        
        print(f"✅ Operation {{i}} completed")
    
    total_time = time.time() - start_time
    
    return {{
        "status": "success",
        "batch_size": len(operations),
        "successful_operations": len([r for r in results if r["status"] == "success"]),
        "total_cost": total_cost,
        "total_time": total_time,
        "results": results
    }}

# Execute batch operations
batch_result = execute_batch_operations()

print("\\n" + "="*50)
print("🎉 BATCH OPERATIONS COMPLETED")
print("="*50)
print(f"✅ Success Rate: {{batch_result['successful_operations']}}/{{batch_result['batch_size']}}")
print(f"💰 Total Cost: ${{batch_result['total_cost']:.6f}}")
print(f"⏱️ Total Duration: {{batch_result['total_time']:.3f}}s")

batch_result
'''
    
    return snippet.strip()

def create_validation_snippet(params: Dict[str, Any]) -> str:
    """
    Generate code snippet for parameter validation testing
    
    Args:
        params: Parameters to validate
        
    Returns:
        Executable validation code snippet
    """
    
    snippet = f'''# Your Tool - Parameter Validation
# Parameters: {json.dumps(params)}

def validate_tool_parameters():
    """Validate tool parameters without execution"""
    
    params = {json.dumps(params, indent=4)}
    errors = []
    
    # Validate required parameters
    if not params.get("param1", "").strip():
        errors.append("param1 is required and cannot be empty")
    
    # Validate numeric parameters
    param2 = params.get("param2", 10)
    if not isinstance(param2, int) or param2 < 1 or param2 > 20:
        errors.append("param2 must be an integer between 1 and 20")
    
    # Validate string parameters
    param3 = params.get("param3", "default")
    if not isinstance(param3, str):
        errors.append("param3 must be a string")
    
    if errors:
        return {{
            "valid": False,
            "errors": errors,
            "message": "Parameter validation failed"
        }}
    else:
        return {{
            "valid": True,
            "message": "All parameters are valid",
            "normalized_params": {{
                "param1": params["param1"].strip(),
                "param2": min(20, max(1, param2)),
                "param3": param3
            }}
        }}

# Validate parameters
validation_result = validate_tool_parameters()

if validation_result["valid"]:
    print("✅ Parameter validation passed")
    print(f"📝 Normalized parameters: {{validation_result['normalized_params']}}")
else:
    print("❌ Parameter validation failed:")
    for error in validation_result["errors"]:
        print(f"   • {{error}}")

validation_result
'''
    
    return snippet.strip()
```

#### Step 5: Tool Registry Configuration (`tool_your_tool_name.json`)

**Purpose**: Tool metadata and discovery configuration  
**Rules**: Complete metadata, no hardcoded use cases

```json
{
  "id": "your_tool_name",
  "name": "Your Tool Display Name",
  "description": "Comprehensive description of tool functionality and capabilities",
  "version": "1.0.0",
  "capabilities": [
    "data_processing",
    "api_integration", 
    "content_analysis",
    "batch_operations"
  ],
  "tags": [
    "utility",
    "processing",
    "analysis",
    "automation"
  ],
  "cost_estimate": 0.001,
  "models_supported": ["all"],
  "dependencies": [
    "requests",
    "json"
  ],
  "environment_variables": [
    "YOUR_API_KEY_NAME"
  ],
  "parameters": {
    "param1": {
      "type": "string",
      "required": true,
      "description": "Primary input parameter for processing",
      "example": "sample input text"
    },
    "param2": {
      "type": "integer",
      "required": false,
      "default": 10,
      "minimum": 1,
      "maximum": 20,
      "description": "Processing intensity level (1-20)"
    },
    "param3": {
      "type": "string",
      "required": false,
      "default": "default",
      "description": "Processing mode or approach",
      "example": "standard"
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
      "description": "Calculate operation cost estimate",
      "parameters": ["params"]
    },
    {
      "name": "validate_parameters", 
      "description": "Validate and normalize input parameters",
      "parameters": ["params"]
    }
  ],
  "files": {
    "core_logic": "tools/your_tool_name/your_tool_name.py",
    "ui_display": "tools/your_tool_name/ui_your_tool_name.py",
    "buttons": "tools/your_tool_name/button_your_tool_name.py"
  },
  "error_handling": {
    "retry_logic": true,
    "timeout_handling": true,
    "rate_limit_handling": true,
    "graceful_degradation": true
  },
  "performance": {
    "typical_duration": "2-5 seconds",
    "scalability": "linear",
    "memory_usage": "low",
    "cache_compatible": true
  },
  "output_format": {
    "success": {
      "status": "success",
      "input_param": "string",
      "timestamp": "string",
      "results": "object",
      "metadata": "object",
      "cost": "float"
    },
    "error": {
      "error": "string", 
      "timestamp": "string",
      "input_param": "string",
      "cost": "float"
    }
  },
  "examples": [
    {
      "name": "Basic Usage",
      "description": "Simple tool execution with default parameters",
      "input": {
        "param1": "sample input",
        "param2": 10,
        "param3": "default"
      },
      "expected_output": "Processed results based on input"
    },
    {
      "name": "High Intensity Processing",
      "description": "Maximum processing intensity for complex tasks",
      "input": {
        "param1": "complex input data",
        "param2": 20,
        "param3": "intensive"
      },
      "expected_output": "Detailed processed results with maximum analysis"
    }
  ],
  "integration_notes": [
    "Tool requires API key configuration via environment variable",
    "Supports batch operations for multiple inputs",
    "Results are cached for identical inputs to improve performance",
    "Rate limiting is handled automatically with exponential backoff"
  ]
}
```

#### Step 6: Testing and Integration

**Automatic Discovery Test:**
```bash
# Mao automatically discovers new tools on restart
python Mao-v4.py --verbose "Test the new your_tool_name tool"
```

**Integration Verification:**
```python
# Test tool discovery
from orchestrator.manager_tools import ToolManager
tools = ToolManager()
print(tools.get_tool_metadata("your_tool_name"))

# Test tool execution
from tools.your_tool_name.your_tool_name import main_function
result = main_function("test input", 15, "test_mode")
print(result)

# Test UI display
from tools.your_tool_name.ui_your_tool_name import display_tool_results
display_tool_results(result, verbose=True)

# Test button generation
from tools.your_tool_name.button_your_tool_name import create_button_snippet
snippet = create_button_snippet({"param1": "test", "param2": 15})
print(snippet)
```

**Model Compatibility Testing:**
```bash
# Test with different models
python Mao-v4.py --verbose "Use your_tool_name with claude-sonnet-4"
python Mao-v4.py --verbose "Use your_tool_name with gemini-2.5-pro"  
python Mao-v4.py --verbose "Use your_tool_name with gpt-4.1-mini"
```

---

## 🤖 Adding New Models

### Model Configuration Process

Adding support for new AI models requires creating a JSON configuration file and updating connection mappings.

#### Step 1: Create Model Configuration

**File**: `configs/models/new-model-name.json`

```json
{
  "id": "new-model-name",
  "display_name": "New Model Display Name",
  "provider": "provider-id",
  "context_window": 32000,
  "max_output": 4096,
  "input_price": 0.001,
  "output_price": 0.003,
  "capabilities": [
    "text",
    "code", 
    "analysis"
  ],
  "strengths": [
    "reasoning",
    "efficiency", 
    "cost_effectiveness"
  ],
  "limitations": [
    "no_images",
    "english_only",
    "limited_reasoning"
  ],
  "recommended_for": [
    "cost_optimization",
    "basic_analysis",
    "simple_workflows"
  ],
  "avoid_for": [
    "complex_reasoning",
    "creative_tasks",
    "multimodal_content"
  ],
  "specializations": {
    "best_for": [
      "simple_tasks",
      "cost_sensitive_operations",
      "batch_processing"
    ],
    "performance_notes": [
      "Excellent cost/performance ratio",
      "Fast response times",
      "Reliable for straightforward tasks"
    ]
  },
  "rate_limits": {
    "requests_per_minute": 100,
    "tokens_per_minute": 50000,
    "daily_limit": 1000000
  },
  "api_configuration": {
    "model_identifier": "new-model-v1",
    "temperature_range": [0.0, 1.0],
    "supports_streaming": true,
    "supports_function_calling": false,
    "max_tokens_override": true
  }
}
```

#### Step 2: Verify Provider Configuration

**Check if provider exists** in `configs/providers/`:

If provider doesn't exist, create `configs/providers/new-provider.json`:

```json
{
  "id": "new-provider",
  "display_name": "New Provider Name",
  "api_type": "openai_compatible",
  "base_url": "https://api.newprovider.com/v1",
  "auth_type": "api_key",
  "env_var": "NEW_PROVIDER_API_KEY",
  "headers": {
    "User-Agent": "Mao/4.0",
    "Content-Type": "application/json"
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "tokens_per_minute": 100000,
    "concurrent_requests": 5
  },
  "retry_config": {
    "max_retries": 3,
    "backoff_factor": 2,
    "retry_codes": [429, 500, 502, 503, 504]
  },
  "supported_features": [
    "streaming",
    "system_messages"
  ],
  "supported_models": [
    "new-model-name"
  ]
}
```

#### Step 3: Update Connection Mappings

**Update** `configs/connections/providers_x_models.json`:

```json
{
  "anthropic-direct": ["claude-sonnet-4", "claude-opus-4", "claude-3-7-sonnet"],
  "openai-direct": ["gpt-4.1-mini", "gpt-4.1-nano"],
  "gemini-direct": ["gemini-2.5-pro"],
  "litellm": ["claude-sonnet-4", "gpt-4.1-mini", "gemini-2.5-pro"],
  "new-provider": ["new-model-name"]
}
```

**Update** `configs/connections/models_x_tools.json`:

```json
{
  "claude-sonnet-4": {
    "optimal_tools": ["think", "text_editor", "brave_search"],
    "good_tools": ["perplexity_search", "file_operations"],
    "avoid_tools": [],
    "notes": "Excellent for complex reasoning and analysis"
  },
  "new-model-name": {
    "optimal_tools": ["brave_search", "web_search", "file_operations"],
    "good_tools": ["text_editor"],
    "avoid_tools": ["graphic_design", "dalle_generate"],
    "notes": "Cost-effective for simple tasks, avoid complex creative work"
  }
}
```

#### Step 4: Test Model Integration

**Environment Setup:**
```bash
export NEW_PROVIDER_API_KEY="your-api-key"
```

**Integration Testing:**
```bash
# Test model discovery
python Mao-v4.py --verbose --stats

# Test simple workflow with new model
python Mao-v4.py --verbose "Simple test task using the new model"

# Test cost optimization (Mao should select new model for cost-sensitive tasks)
python Mao-v4.py --free-only "Research basic information about renewable energy"
```

**Validation Script:**
```python
# Test model manager integration
from orchestrator.manager_models import ModelManager

models = ModelManager()

# Verify model loaded
model_config = models.get_model_config("new-model-name")
print(f"Model loaded: {model_config}")

# Test cost calculation
cost = models.get_model_cost_estimate("new-model-name", 1000)
print(f"Cost estimate: ${cost:.6f}")

# Test capability validation
can_handle = models.validate_model_capability("new-model-name", ["text", "analysis"])
print(f"Can handle text/analysis: {can_handle}")
```

---

## 🔌 Adding New Providers

### Provider Integration Process

Adding new API providers enables Mao to work with additional model endpoints and services.

#### Step 1: Create Provider Configuration

**File**: `configs/providers/new-provider.json`

```json
{
  "id": "new-provider",
  "display_name": "New Provider Display Name",
  "api_type": "openai_compatible",
  "base_url": "https://api.newprovider.com/v1",
  "auth_type": "api_key",
  "env_var": "NEW_PROVIDER_API_KEY",
  "headers": {
    "User-Agent": "Mao/4.0",
    "Content-Type": "application/json",
    "X-Custom-Header": "custom-value"
  },
  "authentication": {
    "method": "bearer_token",
    "header_name": "Authorization",
    "prefix": "Bearer"
  },
  "endpoints": {
    "chat_completions": "/chat/completions",
    "models": "/models",
    "usage": "/usage"
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "tokens_per_minute": 100000,
    "concurrent_requests": 5,
    "burst_allowance": 10
  },
  "retry_config": {
    "max_retries": 3,
    "backoff_factor": 2,
    "base_delay": 1,
    "retry_codes": [429, 500, 502, 503, 504],
    "timeout": 30
  },
  "supported_features": [
    "streaming",
    "function_calling", 
    "system_messages",
    "temperature_control",
    "max_tokens_control"
  ],
  "request_format": {
    "model_param": "model",
    "messages_param": "messages", 
    "temperature_param": "temperature",
    "max_tokens_param": "max_tokens",
    "stream_param": "stream"
  },
  "response_format": {
    "content_path": "choices.0.message.content",
    "usage_path": "usage",
    "error_path": "error"
  },
  "supported_models": [],
  "cost_tracking": {
    "enabled": true,
    "input_token_field": "prompt_tokens",
    "output_token_field": "completion_tokens"
  },
  "health_check": {
    "endpoint": "/health",
    "method": "GET",
    "timeout": 5
  }
}
```

#### Step 2: Provider-Specific Configurations

**For OpenAI-Compatible Providers:**
```json
{
  "api_type": "openai_compatible",
  "request_format": {
    "model_param": "model",
    "messages_param": "messages",
    "temperature_param": "temperature",
    "max_tokens_param": "max_tokens"
  }
}
```

**For Anthropic-Compatible Providers:**
```json
{
  "api_type": "anthropic_compatible", 
  "request_format": {
    "model_param": "model",
    "messages_param": "messages",
    "max_tokens_param": "max_tokens",
    "system_param": "system"
  }
}
```

**For Custom API Providers:**
```json
{
  "api_type": "custom",
  "custom_adapter": "custom_provider_adapter.py",
  "request_format": {
    "custom_mapping": "provider_specific_format"
  }
}
```

#### Step 3: Test Provider Connection

**Environment Setup:**
```bash
export NEW_PROVIDER_API_KEY="your-provider-api-key"
```

**Connection Test:**
```python
# Test provider connectivity
import requests
import os

def test_provider_connection():
    """Test basic connectivity to new provider"""
    
    api_key = os.getenv("NEW_PROVIDER_API_KEY")
    if not api_key:
        print("❌ API key not found")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.newprovider.com/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Provider connection successful")
            models = response.json()
            print(f"📋 Available models: {len(models.get('data', []))}")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

# Run connection test
test_provider_connection()
```

#### Step 4: Integration Testing

**Provider Discovery Test:**
```bash
# Verify provider is discovered
python Mao-v4.py --verbose --stats
```

**End-to-End Test:**
```bash
# Test workflow with new provider
python Mao-v4.py --verbose "Simple task to test new provider integration"
```

**Performance Validation:**
```python
# Test provider performance
from orchestrator.manager_models import ModelManager
import time

def test_provider_performance():
    """Test response time and reliability"""
    
    models = ModelManager()
    
    # Test multiple requests
    response_times = []
    success_count = 0
    
    for i in range(5):
        start_time = time.time()
        try:
            # Simulate model request through Mao
            result = models.test_model_request("new-model-name", "Simple test")
            response_time = time.time() - start_time
            response_times.append(response_time)
            success_count += 1
            print(f"✅ Request {i+1}: {response_time:.3f}s")
        except Exception as e:
            print(f"❌ Request {i+1} failed: {str(e)}")
    
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        print(f"📊 Average response time: {avg_response:.3f}s")
        print(f"📊 Success rate: {success_count}/5")
    
test_provider_performance()
```

---

## 🔧 Advanced Extension Patterns

### Multi-Tool Workflows

**Creating tools that coordinate with other tools:**

```python
# In your tool's core logic
def coordinate_with_other_tools(self, tool_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coordinate with other tools in multi-step workflows
    
    Args:
        tool_results: Results from previous tools in workflow
        
    Returns:
        Enhanced results incorporating previous tool outputs
    """
    
    # Access previous tool results
    research_data = tool_results.get("brave_search", {})
    analysis_data = tool_results.get("think", {})
    
    # Combine with current tool functionality
    enhanced_result = self.process_with_context(research_data, analysis_data)
    
    return enhanced_result
```

### Custom Model Adapters

**For providers with unique API formats:**

```python
# custom_provider_adapter.py
class CustomProviderAdapter:
    """
    Custom adapter for non-standard API formats
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_url = config["base_url"]
        self.api_key = config["api_key"]
    
    def format_request(self, model: str, messages: List[Dict], **kwargs) -> Dict:
        """Convert Mao request format to provider format"""
        
        # Custom request formatting
        return {
            "model_id": model,
            "conversation": self._convert_messages(messages),
            "parameters": {
                "creativity": kwargs.get("temperature", 0.7),
                "length": kwargs.get("max_tokens", 1000)
            }
        }
    
    def parse_response(self, response: Dict) -> Dict:
        """Convert provider response to Mao format"""
        
        # Custom response parsing
        return {
            "content": response["generated_text"],
            "usage": {
                "prompt_tokens": response["input_length"],
                "completion_tokens": response["output_length"]
            }
        }
```

### Tool Dependencies

**Managing dependencies between tools:**

```json
{
  "id": "advanced_tool",
  "dependencies": {
    "required_tools": ["brave_search", "think"],
    "optional_tools": ["graphic_design"],
    "execution_order": ["brave_search", "think", "advanced_tool"]
  },
  "workflow_integration": {
    "can_start_workflow": false,
    "requires_context": true,
    "provides_context": true
  }
}
```

### Error Recovery Strategies

**Advanced error handling patterns:**

```python
def create_resilient_button_snippet(params: Dict[str, Any], model: str) -> str:
    """
    Generate button with advanced error recovery
    """
    
    snippet = f'''
def execute_with_recovery():
    """Execute tool with comprehensive error recovery"""
    
    # Primary execution attempt
    try:
        return primary_execution()
    except PrimaryError as e:
        print(f"⚠️ Primary method failed: {{e}}")
        
        # Fallback strategy 1: Alternative API endpoint
        try:
            return fallback_api_execution()
        except FallbackError as e:
            print(f"⚠️ Fallback API failed: {{e}}")
            
            # Fallback strategy 2: Cached/simplified results
            try:
                return cached_or_simplified_execution()
            except Exception as e:
                print(f"❌ All methods failed: {{e}}")
                
                # Graceful degradation
                return {{
                    "status": "partial_failure",
                    "error": str(e),
                    "fallback_data": "minimal_useful_output"
                }}
'''
    
    return snippet

### Performance Optimization

**Tool-specific optimization patterns:**

```python
def optimize_for_batch_operations(items: List[Any]) -> Dict[str, Any]:
    """
    Optimize tool execution for batch operations
    """
    
    # Batch size optimization
    optimal_batch_size = min(50, len(items))
    batches = [items[i:i + optimal_batch_size] 
               for i in range(0, len(items), optimal_batch_size)]
    
    # Parallel processing where safe
    results = []
    for batch in batches:
        batch_result = process_batch(batch)
        results.extend(batch_result)
    
    return {
        "total_items": len(items),
        "batches_processed": len(batches),
        "results": results
    }
```

---

## 🧪 Testing and Validation

### Comprehensive Testing Strategy

#### Unit Testing for Tools

```python
# test_your_tool.py
import unittest
from tools.your_tool_name.your_tool_name import main_function, estimate_cost

class TestYourTool(unittest.TestCase):
    
    def test_main_function_success(self):
        """Test successful tool execution"""
        result = main_function("test input", 10, "default")
        
        self.assertEqual(result["status"], "success")
        self.assertIn("results", result)
        self.assertIsInstance(result["cost"], float)
        self.assertGreater(result["cost"], 0)
    
    def test_main_function_empty_input(self):
        """Test error handling for empty input"""
        result = main_function("", 10, "default")
        
        self.assertIn("error", result)
        self.assertEqual(result["cost"], 0.0)
    
    def test_parameter_validation(self):
        """Test parameter validation and normalization"""
        result = main_function("test", 25, "default")  # param2 over limit
        
        # Should clamp param2 to maximum value
        metadata = result.get("metadata", {})
        params_used = metadata.get("parameters_used", {})
        self.assertEqual(params_used.get("param2"), 20)
    
    def test_cost_estimation(self):
        """Test cost calculation accuracy"""
        params = {"param1": "test input", "param2": 10}
        cost = estimate_cost(params)
        
        self.assertIsInstance(cost, float)
        self.assertGreater(cost, 0)
        self.assertLess(cost, 1.0)  # Reasonable upper bound

if __name__ == "__main__":
    unittest.main()
```

#### Integration Testing

```python
# test_integration.py
def test_tool_workflow_integration():
    """Test tool integration with Mao orchestrator"""
    
    from orchestrator.core import WorkflowOrchestrator
    
    orchestrator = WorkflowOrchestrator()
    
    # Test tool discovery
    tools = orchestrator.tools.discover_available_tools()
    assert "your_tool_name" in tools
    
    # Test workflow planning with new tool
    goal = "Use your_tool_name to process sample data"
    analysis = orchestrator.analyze_goal(goal)
    workflow = orchestrator.design_workflow(analysis)
    
    # Verify tool is included in workflow
    tool_names = []
    for phase in workflow.phases:
        tool_names.extend(phase.tools)
    
    assert "your_tool_name" in tool_names

def test_model_compatibility():
    """Test tool works with different models"""
    
    from tools.your_tool_name.button_your_tool_name import create_button_snippet
    
    models = ["claude-sonnet-4", "gemini-2.5-pro", "gpt-4.1-mini"]
    params = {"param1": "test", "param2": 10}
    
    for model in models:
        snippet = create_button_snippet(params, model)
        
        # Verify snippet is generated and contains model reference
        assert snippet
        assert model in snippet
        assert "execute" in snippet.lower()
```

#### Performance Testing

```python
# test_performance.py
import time
import statistics

def test_tool_performance():
    """Test tool performance characteristics"""
    
    from tools.your_tool_name.your_tool_name import main_function
    
    # Test response times
    response_times = []
    
    for i in range(10):
        start_time = time.time()
        result = main_function(f"test input {i}", 10, "default")
        response_time = time.time() - start_time
        
        response_times.append(response_time)
        assert result["status"] == "success"
    
    # Performance assertions
    avg_response = statistics.mean(response_times)
    max_response = max(response_times)
    
    print(f"Average response time: {avg_response:.3f}s")
    print(f"Maximum response time: {max_response:.3f}s")
    
    # Performance thresholds
    assert avg_response < 5.0  # Average under 5 seconds
    assert max_response < 10.0  # No response over 10 seconds

def test_cost_accuracy():
    """Test cost estimation accuracy"""
    
    from tools.your_tool_name.your_tool_name import main_function, estimate_cost
    
    params = {"param1": "test input", "param2": 15}
    
    # Get estimated cost
    estimated = estimate_cost(params)
    
    # Get actual cost from execution
    result = main_function("test input", 15, "default")
    actual = result.get("cost", 0)
    
    # Cost estimation should be within 20% of actual
    variance = abs(estimated - actual) / actual if actual > 0 else 0
    assert variance < 0.2, f"Cost variance too high: {variance:.2%}"
```

### Quality Assurance Checklist

**Before deploying new tools/models/providers:**

#### Functionality Testing
- [ ] Core functionality works as expected
- [ ] Error handling covers edge cases
- [ ] Parameter validation prevents invalid inputs
- [ ] Cost estimation is accurate within 20%
- [ ] Performance meets response time requirements

#### Integration Testing  
- [ ] Tool discovered automatically by Mao
- [ ] Works with multiple AI models
- [ ] Integrates properly in multi-tool workflows
- [ ] Button generation produces valid executable code
- [ ] UI display formats results correctly

#### Security Testing
- [ ] Input validation prevents injection attacks
- [ ] API keys and secrets handled securely
- [ ] No sensitive data logged or exposed
- [ ] Rate limiting prevents abuse
- [ ] Error messages don't leak sensitive information

#### Documentation Testing
- [ ] Tool registry JSON is complete and accurate
- [ ] Examples in documentation work correctly
- [ ] Parameter descriptions are clear and helpful
- [ ] Integration notes are up to date
- [ ] Version information is current

---

## 🚀 Best Practices

### Tool Development Guidelines

**1. Follow the Variable-Input Philosophy**
- Never hardcode categories, templates, or domain-specific assumptions
- Let prompts define specifics, not code
- Return structured data, not predetermined choices

**2. Maintain Clean Architecture**  
- Keep 4-file separation strict (logic, UI, buttons, registry)
- No print statements in core logic files
- Handle all errors gracefully with meaningful messages

**3. Optimize for Performance**
- Implement intelligent caching where appropriate
- Use efficient algorithms and data structures
- Provide accurate cost and time estimates

**4. Ensure Universal Compatibility**
- Test with multiple AI models and providers
- Generate self-contained executable button snippets
- Handle different execution environments gracefully

**5. Document Thoroughly**
- Complete tool registry with accurate metadata
- Include usage examples and integration notes
- Document any special requirements or limitations

### Model Integration Guidelines

**1. Accurate Configuration**
- Provide realistic cost and capability information
- Document limitations and strengths honestly
- Include proper rate limit and usage information

**2. Provider Compatibility**
- Ensure provider configuration matches model requirements
- Test connection and authentication thoroughly
- Implement proper error handling for API issues

**3. Performance Optimization**
- Configure models for their optimal use cases
- Avoid recommending models for tasks they handle poorly
- Balance cost optimization with quality requirements

### Provider Integration Guidelines

**1. Robust Connection Handling**
- Implement comprehensive retry logic
- Handle rate limiting and API errors gracefully
- Provide clear error messages for connection issues

**2. Security Best Practices**
- Store API keys securely in environment variables
- Never log or expose sensitive authentication data
- Implement proper request/response validation

**3. Monitoring and Health Checks**
- Include health check endpoints where available
- Monitor response times and error rates
- Implement alerting for provider issues

---

## 🔮 Advanced Features

### Dynamic Tool Creation

**Runtime tool generation based on user requirements:**

```python
def generate_custom_tool(specification: Dict[str, Any]) -> str:
    """
    Generate custom tool code based on user specification
    Enables creating one-off tools for specific needs
    """
    
    tool_template = """
def dynamic_tool_{tool_id}(input_data: str) -> Dict[str, Any]:
    '''Dynamically generated tool for: {purpose}'''
    
    try:
        # Custom logic based on specification
        {custom_logic}
        
        return {{
            "status": "success",
            "results": result,
            "cost": {estimated_cost}
        }}
    except Exception as e:
        return {{"error": str(e), "cost": 0.0}}
    """
    
    # Generate tool code based on specification
    return tool_template.format(**specification)
```

### Workflow Templates

**Reusable workflow patterns for common use cases:**

```python
def create_workflow_template(pattern_name: str, customizations: Dict) -> Dict:
    """
    Create customized workflow from proven patterns
    """
    
    templates = {
        "content_strategy": {
            "phases": ["research", "analysis", "strategy", "content"],
            "tools": ["brave_search", "think", "text_editor", "graphic_design"],
            "models": ["gemini-2.5-pro", "claude-sonnet-4"],
            "estimated_cost": 0.45
        },
        "market_research": {
            "phases": ["research", "analysis", "synthesis"],
            "tools": ["perplexity_search", "brave_search", "think"],
            "models": ["claude-sonnet-4"],
            "estimated_cost": 0.30
        }
    }
    
    base_template = templates[pattern_name]
    
    # Apply customizations
    for key, value in customizations.items():
        if key in base_template:
            base_template[key] = value
    
    return base_template
```

### Community Integration

**Framework for sharing and discovering community tools:**

```python
def discover_community_tools(source: str = "official_registry") -> List[Dict]:
    """
    Discover tools from community sources
    Enables ecosystem growth and collaboration
    """
    
    registries = {
        "official_registry": "https://registry.Mao.tools/tools",
        "community_hub": "https://community.Mao.tools/api/tools",
        "github_releases": "https://api.github.com/orgs/Mao-tools/repos"
    }
    
    # Fetch and validate community tools
    available_tools = fetch_and_validate_tools(registries[source])
    
    return available_tools
```

---

*This extension guide provides everything needed to expand Mao's capabilities while maintaining its architectural integrity and performance characteristics.*