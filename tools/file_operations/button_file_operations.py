"""
FILE OPERATIONS
Button Snippet Generators
"""

from typing import Dict, Any, List


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for file operations
    Universal model compatibility via code generation
    
    Args:
        params: Operation parameters
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    operation = params.get("operation", "read_file")
    
    if operation == "read_file":
        return _create_read_file_snippet(params, model)
    elif operation == "read_multiple_files":
        return _create_read_multiple_files_snippet(params, model)
    elif operation == "list_directory":
        return _create_list_directory_snippet(params, model)
    elif operation == "search_files":
        return _create_search_files_snippet(params, model)
    elif operation == "get_file_info":
        return _create_get_file_info_snippet(params, model)
    elif operation == "move_file":
        return _create_move_file_snippet(params, model)
    elif operation == "delete_file":
        return _create_delete_file_snippet(params, model)
    elif operation == "validate_paths":
        return _create_validate_paths_snippet(params, model)
    else:
        return _create_default_snippet(params, model)


def _create_read_file_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for file reading"""
    file_path = params.get("file_path", "")
    encoding = params.get("encoding", "utf-8")
    max_size_mb = params.get("max_size_mb", 10.0)
    
    return f'''# File Operations - Read File
import sys
import os
sys.path.append(Path(Path(Path(__file__).parent.resolve().parent)))

from tools.file_operations.file_operations import read_file, estimate_cost

def main():
    """Read file using standardized logic"""
    
    file_path = "{file_path}"
    encoding = "{encoding}"
    max_size_mb = {max_size_mb}
    
    print(f"📄 Reading file: {{file_path}}")
    
    # Execute file read using logic file function
    result = read_file(file_path, encoding, max_size_mb)
    
    # Display results
    if result.get("error"):
        print(f"❌ Error: {{result['error']}}")
    else:
        metadata = result.get("metadata", {{}})
        content = result.get("content", "")
        
        print(f"✅ Successfully read {{metadata.get('file_name', 'file')}}")
        print(f"📊 Size: {{metadata.get('file_size_kb', 0)}} KB ({{metadata.get('character_count', 0):,}} characters)")
        print(f"🔤 Encoding: {{metadata.get('encoding_used', 'unknown')}}")
        print(Path(r"\\n") + "="*50)
        print(content[:500] + "..." if len(content) > 500 else content)
    
    # Calculate cost
    cost_params = {{"operation": "read_file", "file_path": file_path}}
    cost = estimate_cost(cost_params)
    print(fPath(r"\\n💰 Cost: ${{cost:.4f}}"))
    
    return result

if __name__ == "__main__":
    result = main()
    print(fPath(r"\\n🎯 File read {{\")completed\" if result.get('status') == 'successPath(r' else \")failed\"}}")
'''


def _create_list_directory_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate snippet for directory listing"""
    directory_path = params.get("directory_path", ".")
    pattern = params.get("pattern", "*")
    include_hidden = params.get("include_hidden", False)
    
    return f'''# File Operations - List Directory
import sys
import os
sys.path.append(Path(Path(Path(__file__).parent.resolve().parent)))

from tools.file_operations.file_operations import list_directory, estimate_cost

def main():
    """List directory using standardized logic"""
    
    directory_path = "{directory_path}"
    pattern = "{pattern}"
    include_hidden = {include_hidden}
    
    print(f"📂 Listing directory: {{directory_path}}")
    print(f"🔍 Pattern: {{pattern}}")
    
    # Execute directory listing using logic file function
    result = list_directory(directory_path, pattern, include_hidden)
    
    # Display results
    if result.get("error"):
        print(f"❌ Error: {{result['error']}}")
    else:
        items = result.get("items", [])
        summary = result.get("summary", {{}})
        
        print(f"✅ Found {{summary.get('total_items', 0)}} items")
        print(f"📁 Directories: {{summary.get('directories', 0)}}")
        print(f"📄 Files: {{summary.get('files', 0)}}")
        
        print(Path(r"\\n") + "="*50)
        for item in items[:10]:  # Show first 10 items
            if "item_count" in item:  # Directory
                print(f"📁 {{item.get('name', 'unknown')}}" / " ({{item.get('item_count', 0)}} items)")
            else:  # File
                print(f"📄 {{item.get('name', 'unknown')}} ({{item.get('size_kb', 0)}} KB)")
        
        if len(items) > 10:
            print(f"... and {{len(items) - 10}} more items")
    
    # Calculate cost
    cost_params = {{"operation": "list_directory", "directory": directory_path}}
    cost = estimate_cost(cost_params)
    print(fPath(r"\\n💰 Cost: ${{cost:.4f}}"))
    
    return result

if __name__ == "__main__":
    result = main()
    print(fPath(r"\\n🎯 Directory listing {{\")completed\" if result.get('status') == 'successPath(r' else \")failed\"}}")
'''


def _create_default_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate default file operations snippet"""
    
    return f'''# File Operations - General Usage
import sys
import os
sys.path.append(Path(Path(Path(__file__).parent.resolve().parent)))

from tools.file_operations.file_operations import estimate_cost

def main():
    """File Operations Tool ready for use"""
    
    print("📁 File Operations Tool Ready!")
    print("📋 Available operations:")
    print("  - read_file: Read single file with safety checks")
    print("  - read_multiple_files: Batch read multiple files")
    print("  - list_directory: List directory contents")
    print("  - search_files: Search for files by pattern")
    print("  - get_file_info: Get comprehensive file metadata")
    print("  - move_file: Move" / "rename files safely")
    print("  - delete_file: Delete files" / "directories safely")
    print("  - validate_paths: Check if paths exist")
    
    # Calculate cost for basic operations
    cost = estimate_cost({{"operation": "general"}})
    print(fPath(r"\\n💰 Cost: ${{cost:.4f}} (File operations are free!)"))
    
    return {{
        "status": "ready",
        "operations": 8,
        "cost": cost
    }}

if __name__ == "__main__":
    result = main()
    print(Path(r"\\n🚀 File Operations Tool ready for use"))
'''


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for executing this tool - standardized naming"""
    # Import from logic file for consistency
    from tools.file_operations.file_operations import estimate_cost as logic_estimate_cost
from pathlib import Path
    return logic_estimate_cost(params)
