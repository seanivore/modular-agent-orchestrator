#!/usr/bin/env python3
"""
Code Execution Button Snippet Generator
Creates executable snippets for Claude Code Execution API
"""

from typing import Dict, Any
import json

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
    """Generate snippet for executing Python code"""
    code = params.get("code", "print('Hello from Code Execution!')")
    workflow_id = params.get("workflow_id", "code-execution")
    container_id = params.get("container_id", None)
    
    container_param = f'container_id="{container_id}"' if container_id else 'container_id=None'
    
    return f'''
# Code Execution Tool - Execute Python Code
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_execution.code_execution import CodeExecutionTool

def main():
    # Initialize Code Execution Tool
    tool = CodeExecutionTool()
    
    # Python code to execute
    code = """{code}"""
    
    print("🐍 Executing Python code via Claude Code Execution API...")
    
    result = tool.execute_code(
        code=code,
        workflow_id="{workflow_id}",
        {container_param},
        model="{model}"
    )
    
    if result["success"]:
        print("✅ Code execution successful!")
        print(f"📊 Output:\\n{{result['stdout']}}")
        
        if result.get("files"):
            print(f"📁 Files created: {{len(result['files'])}}")
            for file_info in result["files"]:
                print(f"  - {{file_info['filename']}} (ID: {{file_info['file_id']}})")
        
        if result.get("container_id"):
            print(f"🔗 Container ID: {{result['container_id']}}")
    else:
        print("❌ Code execution failed!")
        if result.get("stderr"):
            print(f"⚠️ Error: {{result['stderr']}}")
        if result.get("error"):
            print(f"🚨 Exception: {{result['error']}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🎯 Execution {{\"completed\" if result[\"success\"] else \"failed\"}}")
'''


def _create_execute_with_files_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for executing code with file inputs"""
    code = params.get("code", "# Code to process uploaded files")
    file_ids = params.get("file_ids", [])
    workflow_id = params.get("workflow_id", "code-execution-files")
    
    file_ids_str = json.dumps(file_ids)
    
    return f'''
# Code Execution Tool - Execute with Files
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_execution.code_execution import CodeExecutionTool

def main():
    # Initialize Code Execution Tool
    tool = CodeExecutionTool()
    
    # Python code to execute
    code = """{code}"""
    
    # File IDs to include
    file_ids = {file_ids_str}
    
    print(f"🐍 Executing Python code with {{len(file_ids)}} uploaded files...")
    
    result = tool.execute_code_with_files(
        code=code,
        file_ids=file_ids,
        workflow_id="{workflow_id}",
        model="{model}"
    )
    
    if result["success"]:
        print("✅ Code execution with files successful!")
        print(f"📊 Output:\\n{{result['stdout']}}")
        
        if result.get("files"):
            print(f"📁 Generated files: {{len(result['files'])}}")
            for file_info in result["files"]:
                print(f"  - {{file_info['filename']}} (ID: {{file_info['file_id']}})")
    else:
        print("❌ Code execution failed!")
        if result.get("stderr"):
            print(f"⚠️ Error: {{result['stderr']}}")
        if result.get("error"):
            print(f"🚨 Exception: {{result['error']}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🎯 Execution {{\"completed\" if result[\"success\"] else \"failed\"}}")
'''


def _create_container_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for creating persistent container"""
    workflow_id = params.get("workflow_id", "persistent-container")
    
    return f'''
# Code Execution Tool - Create Persistent Container
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_execution.code_execution import CodeExecutionTool

def main():
    # Initialize Code Execution Tool
    tool = CodeExecutionTool()
    
    print("🔗 Creating persistent container for multi-step execution...")
    
    result = tool.create_persistent_container(workflow_id="{workflow_id}")
    
    if result["success"]:
        print("✅ Persistent container created!")
        print(f"🆔 Container ID: {{result['container_id']}}")
        print(f"⏰ Expires at: {{result['expires_at']}}")
        print("\\n💡 Use this container ID for subsequent executions to maintain state")
    else:
        print("❌ Container creation failed!")
        print(f"🚨 Error: {{result.get('error', 'Unknown error')}}")
    
    return result

if __name__ == "__main__":
    result = main()
    if result["success"]:
        print(f"\\n🎯 Container ready: {{result['container_id']}}")
    else:
        print("\\n🚫 Container creation failed")
'''


def _create_download_files_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for downloading execution files"""
    file_ids = params.get("file_ids", [])
    workflow_id = params.get("workflow_id", "download-files")
    
    file_ids_str = json.dumps(file_ids)
    
    return f'''
# Code Execution Tool - Download Generated Files
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_execution.code_execution import CodeExecutionTool

def main():
    # Initialize Code Execution Tool
    tool = CodeExecutionTool()
    
    # File IDs to download
    file_ids = {file_ids_str}
    
    print(f"📥 Downloading {{len(file_ids)}} files from code execution...")
    
    results = tool.download_execution_files(
        file_ids=file_ids,
        workflow_id="{workflow_id}"
    )
    
    success_count = sum(1 for r in results if r["success"])
    
    print(f"📊 Download Results: {{success_count}}/{{len(results)}} successful")
    
    for result in results:
        if result["success"]:
            print(f"✅ {{result['filename']}} - {{result['size']}} bytes")
        else:
            print(f"❌ {{result['file_id']}} - Error: {{result['error']}}")
    
    return results

if __name__ == "__main__":
    results = main()
    successful = [r for r in results if r["success"]]
    print(f"\\n🎯 Downloaded {{len(successful)}} files successfully")
'''


def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate default Code Execution snippet"""
    workflow_id = params.get("workflow_id", "code-execution-default")
    
    return f'''
# Code Execution Tool - General Usage
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.code_execution.code_execution import CodeExecutionTool

def main():
    # Initialize Code Execution Tool
    tool = CodeExecutionTool()
    
    print("🐍 Code Execution Tool Ready!")
    print("📋 Available operations:")
    print("  - execute_code: Run Python code in Claude's sandbox")
    print("  - execute_with_files: Run code with uploaded files")
    print("  - create_container: Create persistent execution environment")
    print("  - download_files: Download files created during execution")
    
    # Example execution
    example_code = """
import pandas as pd
import matplotlib.pyplot as plt

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
    
    print("\\n🧪 Running example code...")
    result = tool.execute_code(
        code=example_code,
        workflow_id="{workflow_id}",
        model="{model}"
    )
    
    if result["success"]:
        print("✅ Example execution successful!")
        if result.get("files"):
            print(f"📁 Generated {{len(result['files'])}} files")
    else:
        print("❌ Example execution failed")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\\n🚀 Code Execution Tool ready for use")
'''
