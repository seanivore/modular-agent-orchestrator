"""
File Operations Tool
Safe, efficient file and directory operations with comprehensive error handling
"""

import os
import json
import glob
import shutil
from pathlib import Path
from typing import List, Dict, Any, Union
from datetime import datetime

def get_tool_definition() -> Dict[str, Any]:
    """Enhanced tool definition for OC discovery"""
    return {
        "id": "file_operations",
        "name": "Enhanced File Operations",
        "description": "Safe, efficient file and directory operations with comprehensive error handling",
        "capabilities": ["file_management", "data_access", "directory_navigation", "file_safety"],
        "use_cases": ["reading resources", "organizing work", "file discovery", "safe file operations"],
        "cost_estimate": 0.0,
        "model_compatibility": ["all"],
        "tags": ["core", "files", "essential", "enhanced"],
        "functions": [
            "read_file",
            "read_multiple_files", 
            "list_directory",
            "get_file_info",
            "move_file",
            "delete_file",
            "search_files"
        ]
    }

def read_file(file_path: str, encoding: str = "utf-8", max_size_mb: float = 10.0) -> Dict[str, Any]:
    """Enhanced file reading with safety checks and better error handling"""
    try:
        # Path validation and normalization
        path = Path(file_path).resolve()
        
        # Safety checks
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        if not path.is_file():
            return {"error": f"Path is not a file: {file_path}"}
        
        # Size check
        file_size = path.stat().st_size
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        if file_size > max_size_bytes:
            return {"error": f"File too large: {file_size / (1024*1024):.1f}MB > {max_size_mb}MB limit"}
        
        # Read with encoding fallback
        encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252']
        
        for enc in encodings_to_try:
            try:
                with open(path, 'r', encoding=enc) as f:
                    content = f.read()
                
                # Return success with metadata
                return {
                    "status": "success",
                    "content": content,
                    "metadata": {
                        "file_path": str(path),
                        "file_name": path.name,
                        "file_size_bytes": file_size,
                        "file_size_kb": round(file_size / 1024, 1),
                        "encoding_used": enc,
                        "character_count": len(content),
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
            except UnicodeDecodeError:
                if enc == encodings_to_try[-1]:  # Last encoding failed
                    return {"error": f"Could not decode file with any encoding: {file_path}"}
                continue
                
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading {file_path}: {str(e)}"}

def read_multiple_files(file_paths: List[str], fail_fast: bool = False) -> Dict[str, Any]:
    """Enhanced multiple file reading with better error handling and progress tracking"""
    if not file_paths:
        return {"error": "No file paths provided"}
    
    results = []
    successful_reads = 0
    failed_reads = 0
    total_size_kb = 0
    
    for i, path in enumerate(file_paths):
        try:
            # Use read_file for consistent behavior
            result = read_file(path)
            
            if result.get("status") == "success":
                successful_reads += 1
                total_size_kb += result["metadata"]["file_size_kb"]
            else:
                failed_reads += 1
                if fail_fast:
                    return {
                        "error": f"Failed fast on: {path}",
                        "failure_details": result
                    }
            
            results.append({
                "file_path": path,
                "result": result
            })
            
        except Exception as e:
            failed_reads += 1
            error_result = {"error": f"Exception reading {path}: {str(e)}"}
            results.append({
                "file_path": path,
                "result": error_result
            })
            
            if fail_fast:
                return {
                    "error": f"Failed fast on: {path}",
                    "failure_details": error_result
                }
    
    return {
        "status": "completed",
        "summary": {
            "total_files": len(file_paths),
            "successful_reads": successful_reads,
            "failed_reads": failed_reads,
            "total_size_kb": round(total_size_kb, 1)
        },
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

def list_directory(directory_path: str, pattern: str = "*", include_hidden: bool = False) -> Dict[str, Any]:
    """Enhanced directory listing with metadata and sorting"""
    try:
        path = Path(directory_path).resolve()
        
        if not path.exists():
            return {"error": f"Directory not found: {directory_path}"}
        
        if not path.is_dir():
            return {"error": f"Path is not a directory: {directory_path}"}
        
        # Get all items matching pattern
        if include_hidden:
            items = list(path.glob(pattern))
        else:
            items = [item for item in path.glob(pattern) if not item.name.startswith('.')]
        
        if not items:
            return {
                "status": "success",
                "directory": str(path),
                "pattern": pattern,
                "items": [],
                "summary": {"total_items": 0, "files": 0, "directories": 0}
            }
        
        # Process items
        files = []
        directories = []
        
        for item in items:
            try:
                stat = item.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
                item_data = {
                    "name": item.name,
                    "path": str(item),
                    "modified": modified,
                    "permissions": oct(stat.st_mode)[-3:]
                }
                
                if item.is_dir():
                    # Count items in directory
                    try:
                        dir_count = len(list(item.iterdir()))
                        item_data["item_count"] = dir_count
                    except PermissionError:
                        item_data["item_count"] = "access_denied"
                    
                    directories.append(item_data)
                else:
                    item_data["size_bytes"] = size
                    item_data["size_kb"] = round(size / 1024, 1)
                    item_data["size_mb"] = round(size / (1024 * 1024), 2) if size > 1024 * 1024 else None
                    files.append(item_data)
                    
            except Exception as e:
                # Add items that had errors
                error_item = {
                    "name": item.name,
                    "path": str(item),
                    "error": str(e)
                }
                files.append(error_item)
        
        # Sort results
        directories.sort(key=lambda x: x["name"].lower())
        files.sort(key=lambda x: x["name"].lower())
        
        return {
            "status": "success",
            "directory": str(path),
            "pattern": pattern,
            "items": directories + files,
            "summary": {
                "total_items": len(directories) + len(files),
                "directories": len(directories),
                "files": len(files)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Error listing directory: {str(e)}"}

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive file information"""
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        stat = path.stat()
        
        file_info = {
            "status": "success",
            "path": str(path),
            "name": path.name,
            "parent": str(path.parent),
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 1),
            "size_mb": round(stat.st_size / (1024 * 1024), 2) if stat.st_size > 1024 * 1024 else None,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:],
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "is_symlink": path.is_symlink(),
            "suffix": path.suffix,
            "stem": path.stem
        }
        
        # Add file type specific info
        if path.is_file():
            # Try to determine file type
            if path.suffix.lower() in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']:
                file_info["file_type"] = "text"
            elif path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                file_info["file_type"] = "image"
            elif path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                file_info["file_type"] = "video"
            elif path.suffix.lower() in ['.mp3', '.wav', '.flac', '.aac', '.ogg']:
                file_info["file_type"] = "audio"
            else:
                file_info["file_type"] = "unknown"
        
        return file_info
        
    except Exception as e:
        return {"error": f"Error getting file info: {str(e)}"}

def search_files(directory: str, pattern: str, recursive: bool = True, case_sensitive: bool = False) -> Dict[str, Any]:
    """Search for files matching pattern"""
    try:
        path = Path(directory).resolve()
        
        if not path.exists():
            return {"error": f"Directory not found: {directory}"}
        
        if not path.is_dir():
            return {"error": f"Path is not a directory: {directory}"}
        
        # Prepare search pattern
        search_pattern = pattern if case_sensitive else pattern.lower()
        
        found_files = []
        found_directories = []
        
        # Search function
        def search_in_directory(search_path: Path, depth: int = 0):
            try:
                for item in search_path.iterdir():
                    item_name = item.name if case_sensitive else item.name.lower()
                    
                    # Check if item matches pattern
                    if search_pattern in item_name:
                        item_info = {
                            "name": item.name,
                            "path": str(item),
                            "relative_path": str(item.relative_to(path)),
                            "depth": depth
                        }
                        
                        if item.is_file():
                            stat = item.stat()
                            item_info["size_bytes"] = stat.st_size
                            item_info["size_kb"] = round(stat.st_size / 1024, 1)
                            item_info["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                            found_files.append(item_info)
                        elif item.is_dir():
                            found_directories.append(item_info)
                    
                    # Recurse into subdirectories if recursive
                    if recursive and item.is_dir() and not item.name.startswith('.'):
                        search_in_directory(item, depth + 1)
                        
            except PermissionError:
                # Skip directories we can't access
                pass
        
        # Perform search
        search_in_directory(path)
        
        # Sort results
        found_files.sort(key=lambda x: x["path"])
        found_directories.sort(key=lambda x: x["path"])
        
        return {
            "status": "success",
            "search_directory": str(path),
            "pattern": pattern,
            "case_sensitive": case_sensitive,
            "recursive": recursive,
            "results": {
                "files": found_files,
                "directories": found_directories
            },
            "summary": {
                "total_found": len(found_files) + len(found_directories),
                "files_found": len(found_files),
                "directories_found": len(found_directories)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

def move_file(source: str, destination: str, overwrite: bool = False) -> Dict[str, Any]:
    """Move or rename files and directories safely"""
    try:
        source_path = Path(source).resolve()
        dest_path = Path(destination).resolve()
        
        if not source_path.exists():
            return {"error": f"Source not found: {source}"}
        
        if dest_path.exists() and not overwrite:
            return {"error": f"Destination exists and overwrite=False: {destination}"}
        
        # Perform move
        shutil.move(str(source_path), str(dest_path))
        
        return {
            "status": "success",
            "operation": "move",
            "source": str(source_path),
            "destination": str(dest_path),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Move failed: {str(e)}"}

def validate_paths(paths: List[str]) -> Dict[str, Any]:
    """Validate multiple file paths"""
    results = []
    
    for path in paths:
        path_obj = Path(path)
        result = {
            "path": path,
            "exists": path_obj.exists(),
            "is_file": path_obj.is_file() if path_obj.exists() else None,
            "is_directory": path_obj.is_dir() if path_obj.exists() else None,
            "absolute_path": str(path_obj.resolve())
        }
        results.append(result)
    
    return {
        "status": "success",
        "validation_results": results,
        "summary": {
            "total_paths": len(paths),
            "existing_paths": sum(1 for r in results if r["exists"]),
            "missing_paths": sum(1 for r in results if not r["exists"])
        }
    }

"""
PULL FROM OLD SFA: 
"""

# SFA v4.0.0 Enhanced Tools - Complete Implementation
# Extracted best patterns from v3.3.0 and enhanced for v4 architecture

# =============================================================================
# ENHANCED FILE OPERATIONS TOOL  
# =============================================================================

"""
Enhanced SFA v4 File Operations Tool
Improved error handling, safety checks, and token efficiency
"""

import os
import json
import glob
import shutil
from pathlib import Path
from typing import List, Dict, Any, Union

def get_file_operations_definition() -> Dict[str, Any]:
    """Enhanced tool definition for OC discovery"""
    return {
        "id": "file_operations",
        "name": "Enhanced File Operations",
        "description": "Safe, efficient file and directory operations with comprehensive error handling",
        "capabilities": ["file_management", "data_access", "directory_navigation", "file_safety"],
        "use_cases": ["reading resources", "organizing work", "file discovery", "safe file operations"],
        "cost_estimate": 0.0,
        "model_compatibility": ["all"],
        "tags": ["core", "files", "essential", "enhanced"],
        "functions": [
            "read_file",
            "read_multiple_files", 
            "list_directory",
            "get_file_info",
            "move_file",
            "delete_file",
            "search_files"
        ]
    }

def enhanced_read_file(file_path: str, encoding: str = "utf-8", max_size_mb: float = 10.0) -> str:
    """Enhanced file reading with safety checks and better error handling"""
    try:
        # Path validation and normalization
        path = Path(file_path).resolve()
        
        # Safety checks
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        if not path.is_file():
            return f"❌ Path is not a file: {file_path}"
        
        # Size check
        file_size = path.stat().st_size
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        if file_size > max_size_bytes:
            return f"❌ File too large: {file_size / (1024*1024):.1f}MB > {max_size_mb}MB limit"
        
        # Read with encoding fallback
        encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252']
        
        for enc in encodings_to_try:
            try:
                with open(path, 'r', encoding=enc) as f:
                    content = f.read()
                
                # Success message with metadata
                return f"✅ Read {len(content):,} chars from {path.name} ({file_size / 1024:.1f} KB)\\n\\n{content}"
                
            except UnicodeDecodeError:
                if enc == encodings_to_try[-1]:  # Last encoding failed
                    return f"❌ Could not decode file with any encoding: {file_path}"
                continue
                
    except PermissionError:
        return f"❌ Permission denied: {file_path}"
    except Exception as e:
        return f"❌ Error reading {file_path}: {str(e)}"

def enhanced_read_multiple_files(file_paths: List[str], fail_fast: bool = False) -> str:
    """Enhanced multiple file reading with better error handling and progress tracking"""
    if not file_paths:
        return "❌ No file paths provided"
    
    results = []
    successful_reads = 0
    failed_reads = 0
    total_size = 0
    
    console_output = [f"📚 Reading {len(file_paths)} files..."]
    
    for i, path in enumerate(file_paths, 1):
        try:
            console_output.append(f"[{i}/{len(file_paths)}] {Path(path).name}")
            
            # Use enhanced_read_file for consistent behavior
            result = enhanced_read_file(path)
            
            if result.startswith("✅"):
                successful_reads += 1
                # Extract size info if available
                try:
                    size_kb = float(result.split("(")[1].split(" KB)")[0])
                    total_size += size_kb
                except:
                    pass
            else:
                failed_reads += 1
                if fail_fast:
                    return f"❌ Failed fast on: {path}\\n{result}"
            
            results.append(f"📄 {path}\\n{'='*50}\\n{result}\\n\\n")
            
        except Exception as e:
            failed_reads += 1
            error_msg = f"❌ {path}: {str(e)}"
            results.append(f"📄 {path}\\n{'='*50}\\n{error_msg}\\n\\n")
            
            if fail_fast:
                return error_msg
    
    # Summary header
    summary = f"""✅ Completed reading {len(file_paths)} files
📊 Success: {successful_reads} | Failed: {failed_reads} | Total: {total_size:.1f} KB

"""
    
    return summary + "".join(results)

def create_file_operations_snippet(operation: str, params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate enhanced executable code snippets for file operations"""
    
    if operation == "read_file":
        file_path = params.get("file_path", "")
        return f'''
# Enhanced file reading with safety checks
import os
from pathlib import Path

def safe_read_file(file_path, max_size_mb=10.0):
    """Read file with comprehensive safety checks"""
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return f"❌ File not found: {{file_path}}"
        
        if not path.is_file():
            return f"❌ Not a file: {{file_path}}"
        
        # Size check
        file_size = path.stat().st_size
        if file_size > max_size_mb * 1024 * 1024:
            return f"❌ File too large: {{file_size / (1024*1024):.1f}}MB"
        
        # Try multiple encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✅ Read {{len(content):,}} characters using {{encoding}}")
                print(f"📁 File: {{path.name}} ({{file_size / 1024:.1f}} KB)")
                return content
            except UnicodeDecodeError:
                continue
        
        return f"❌ Could not decode file with any encoding"
        
    except Exception as e:
        return f"❌ Error: {{str(e)}}"

# Execute
result = safe_read_file("{file_path}")
if isinstance(result, str) and not result.startswith("❌"):
    print("\\n" + "="*50)
    print(result)
else:
    print(result)
'''

    elif operation == "list_directory":
        directory_path = params.get("directory_path", ".")
        pattern = params.get("pattern", "*")
        
        return f'''
# Enhanced directory listing with metadata
import os
import glob
from pathlib import Path
from datetime import datetime

def enhanced_list_directory(directory_path, pattern="*"):
    """List directory with enhanced metadata and sorting"""
    try:
        path = Path(directory_path).resolve()
        
        if not path.exists():
            return f"❌ Directory not found: {{directory_path}}"
        
        if not path.is_dir():
            return f"❌ Not a directory: {{directory_path}}"
        
        # Get all items matching pattern
        pattern_path = path / pattern
        items = list(path.glob(pattern))
        
        if not items:
            return f"📂 No items found matching '{{pattern}}' in {{directory_path}}"
        
        # Separate files and directories
        files = []
        directories = []
        
        for item in items:
            try:
                stat = item.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                
                if item.is_dir():
                    # Count items in directory
                    try:
                        dir_count = len(list(item.iterdir()))
                        directories.append(f"📁 {{item.name}}/ ({{dir_count}} items) - {{modified}}")
                    except PermissionError:
                        directories.append(f"📁 {{item.name}}/ (access denied) - {{modified}}")
                else:
                    size_str = f"{{size:,}} bytes" if size < 1024 else f"{{size/1024:.1f}} KB" if size < 1024*1024 else f"{{size/(1024*1024):.1f}} MB"
                    files.append(f"📄 {{item.name}} ({{size_str}}) - {{modified}}")
                    
            except Exception as e:
                files.append(f"❓ {{item.name}} (error: {{str(e)}})")
        
        # Sort and combine results
        directories.sort()
        files.sort()
        
        result = [f"📂 Contents of {{directory_path}} ({{len(items)}} items):"]
        result.extend(directories)
        result.extend(files)
        
        return "\\n".join(result)
        
    except Exception as e:
        return f"❌ Error listing directory: {{str(e)}}"

# Execute
result = enhanced_list_directory("{directory_path}", "{pattern}")
print(result)
'''

    else:
        return f"# Unknown file operation: {operation}"
