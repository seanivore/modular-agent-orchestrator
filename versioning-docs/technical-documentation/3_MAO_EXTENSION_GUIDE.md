# Mao Extension Guide
**Complete Guide to Adding Tools, Models, and Providers**

*Step-by-step instructions for extending Mao capabilities*

---

## 🎯 Overview

Mao's modular architecture enables unlimited extension without performance degradation. This guide provides complete instructions for adding new capabilities to your Mao instance.

### What You Can Add

**Tools** - New capabilities via 6-file architecture pattern
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

# Display formatte