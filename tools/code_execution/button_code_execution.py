#!/usr/bin/env python3
"""
Code Execution Button Snippet Generator - Fixed Version
Creates executable snippets for Claude Code Execution API
"""

from typing import Dict, Any
import json
from tools.code_execution.code_execution import (
    execute_python_code,
    execute_code_with_files,
    create_persistent_container,
    download_execution_files,
    estimate_cost
)

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Single entry point for Code Execution button snippet generation
    Universal model compatibility via code generation
    """
    operation = params.get("operation", "execute_code")
    
    if operation == "execute_code":
        return _create_execute_code_snippet(params, model)
    elif operation == "execute_with_files":
        return _create_execute_with_files_snippet(params, model)
    elif operation == "create_container":
        return _create_container_snippet(params, model)
    elif operation == "download_files":
        return _create_download_files_snippet(params, model)
    else:
        return _create_default_snippet(params, model)

def _create_execute_code_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for executing Python code using MAO logic"""
    code = params.get("code", "print('Hello from Code Execution!')")
    workflow_id = params.get("workflow_id", "code-execution")
    container_id = params.get("container_id", None)
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"execution_time_minutes": 5})
    
    # Escape code for safe inclusion
    escaped_code = json.dumps(code)
    
    snippet = f'''
# Code Execution Tool - Execute Python Code
import sys
sys.path.append('/Users/seanivore/Development" / "modular-agent-orchestrator')

from tools.code_execution.code_execution import execute_python_code
from tools.code_execution.ui_code_execution import display_execution_result, display_code_with_syntax

# Python code to execute
code = {escaped_code}

# Display the code with syntax highlighting
display_code_with_syntax(code)

print("🐍 Executing Python code via Claude Code Execution API...")

# Execute code using MAO logic
result = execute_python_code(
    code=code,
    workflow_id="{workflow_id}",
    container_id="{container_id}" if "{container_id}" != "None" else None,
    model="{model}"
)

# Display results using MAO UI
display_execution_result(result, verbose=True)

if result["success"]:
    print("✅ Code execution completed successfully")
    if result.get("files"):
        print(f"📁 Generated {{len(result['files'])}} files")
else:
    print("❌ Code execution failed")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_execute_with_files_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for executing code with file inputs using MAO logic"""
    code = params.get("code", "# Code to process uploaded files")
    file_ids = params.get("file_ids", [])
    workflow_id = params.get("workflow_id", "code-execution-files")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"execution_time_minutes": 5, "file_ids": file_ids})
    
    # Escape code and file_ids for safe inclusion
    escaped_code = json.dumps(code)
    file_ids_json = json.dumps(file_ids)
    
    snippet = f'''
# Code Execution Tool - Execute with Files
import sys
sys.path.append('/Users/seanivore/Development" / "modular-agent-orchestrator')

from tools.code_execution.code_execution import execute_code_with_files
from tools.code_execution.ui_code_execution import display_execution_result, display_code_with_syntax

# Python code to execute
code = {escaped_code}

# File IDs to include
file_ids = {file_ids_json}

# Display the code with syntax highlighting
display_code_with_syntax(code)

print(f"🐍 Executing Python code with {{len(file_ids)}} uploaded files...")

# Execute code with files using MAO logic
result = execute_code_with_files(
    code=code,
    file_ids=file_ids,
    workflow_id="{workflow_id}",
    model="{model}"
)

# Display results using MAO UI
display_execution_result(result, verbose=True)

if result["success"]:
    print("✅ Code execution with files completed successfully")
    if result.get("files"):
        print(f"📁 Generated {{len(result['files'])}} additional files")
else:
    print("❌ Code execution with files failed")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_container_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for creating persistent container using MAO logic"""
    workflow_id = params.get("workflow_id", "persistent-container")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"execution_time_minutes": 60})  # 1 hour container
    
    snippet = f'''
# Code Execution Tool - Create Persistent Container
import sys
sys.path.append('/Users/seanivore/Development" / "modular-agent-orchestrator')

from tools.code_execution.code_execution import create_persistent_container
from tools.code_execution.ui_code_execution import display_container_info

print("🔗 Creating persistent container for multi-step execution...")

# Create container using MAO logic
result = create_persistent_container(workflow_id="{workflow_id}")

# Display results using MAO UI
display_container_info(result)

if result["success"]:
    print("✅ Persistent container created successfully")
    print("💡 Use this container ID for subsequent executions to maintain state")
else:
    print("❌ Container creation failed")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_download_files_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for downloading execution files using MAO logic"""
    file_ids = params.get("file_ids", [])
    workflow_id = params.get("workflow_id", "download-files")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"file_ids": file_ids})
    
    file_ids_json = json.dumps(file_ids)
    
    snippet = f'''
# Code Execution Tool - Download Generated Files
import sys
sys.path.append('/Users/seanivore/Development" / "modular-agent-orchestrator')

from tools.code_execution.code_execution import download_execution_files
from tools.code_execution.ui_code_execution import display_download_results

# File IDs to download
file_ids = {file_ids_json}

print(f"📥 Downloading {{len(file_ids)}} files from code execution...")

# Download files using MAO logic
results = download_execution_files(
    file_ids=file_ids,
    workflow_id="{workflow_id}"
)

# Display results using MAO UI
display_download_results(results, verbose=True)

success_count = sum(1 for r in results if r.get("success", False))
print(f"📊 Download Results: {{success_count}}" / "{{len(results)}} successful")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return results for workflow integration
results
'''
    
    return snippet.strip()

def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate default Code Execution snippet"""
    operation = params.get("operation", "unknown")
    workflow_id = params.get("workflow_id", "code-execution-default")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"execution_time_minutes": 5})
    
    snippet = f'''
# Code Execution Tool - General Usage
import sys
sys.path.append('/Users/seanivore/Development" / "modular-agent-orchestrator')

from tools.code_execution.code_execution import execute_python_code, estimate_cost
from tools.code_execution.ui_code_execution import display_help, display_execution_result

print("🐍 Code Execution Tool Ready!")

# Display help information
display_help()

print(Path(r"\\n📋 Available Operations:"))
available_operations = [
    "execute_code",
    "execute_with_files",
    "create_container", 
    "download_files"
]

for op in available_operations:
    print(f"  • {{op}}")

# Run example if operation is unknown
if "{operation}" not in available_operations:
    print(fPath(r"\\n⚠️ Unknown operation: {operation}"))
    print(Path(r"\\n🧪 Running example code..."))
    
    example_code = """
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create sample data
data = {{'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]}}
df = pd.DataFrame(data)

print("Sample DataFrame:")
print(df)

# Create a simple plot
plt.figure(figsize=(8, 6))
plt.plot(df['x'], df['y'], marker='o')
plt.title('Sample Line Plot')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.savefig('sample_plot.png')
plt.close()

print("Plot saved as sample_plot.png")
"""
    
    # Execute example using MAO logic
    result = execute_python_code(
        code=example_code,
        workflow_id="{workflow_id}",
        model="{model}"
    )
    
    # Display results using MAO UI
    display_execution_result(result)
    
    if result["success"]:
        print("✅ Example execution successful!")
    else:
        print("❌ Example execution failed")

print(fPath(r"\\n💰 Estimated cost: ${cost_estimate:.4f}"))

result = {{
    "tool_ready": True,
    "available_operations": available_operations,
    "cost": cost_estimate
}}

# Return result
result
'''
    
    return snippet.strip()
