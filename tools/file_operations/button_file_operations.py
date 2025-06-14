"""
FILE OPERATIONS
Human Button Generators
"""

from typing import Dict, Any, List

def create_read_file_snippet(file_path: str, encoding: str = "utf-8", max_size_mb: float = 10.0, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for file reading"""
    
    return f'''
# Enhanced file reading with comprehensive safety checks
import os
from pathlib import Path

def safe_read_file(file_path, encoding="{encoding}", max_size_mb={max_size_mb}):
    """Read file with comprehensive safety checks and encoding fallback"""
    try:
        path = Path(file_path).resolve()
        
        # Safety checks
        if not path.exists():
            return {{"error": f"File not found: {{file_path}}"}}
        
        if not path.is_file():
            return {{"error": f"Path is not a file: {{file_path}}"}}
        
        # Size check
        file_size = path.stat().st_size
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        if file_size > max_size_bytes:
            return {{"error": f"File too large: {{file_size / (1024*1024):.1f}}MB > {{max_size_mb}}MB limit"}}
        
        # Read with encoding fallback
        encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252']
        
        for enc in encodings_to_try:
            try:
                with open(path, 'r', encoding=enc) as f:
                    content = f.read()
                
                # Return success with metadata
                return {{
                    "status": "success",
                    "content": content,
                    "metadata": {{
                        "file_path": str(path),
                        "file_name": path.name,
                        "file_size_bytes": file_size,
                        "file_size_kb": round(file_size / 1024, 1),
                        "encoding_used": enc,
                        "character_count": len(content),
                        "timestamp": "{{datetime.now().isoformat()}}"
                    }}
                }}
                
            except UnicodeDecodeError:
                if enc == encodings_to_try[-1]:
                    return {{"error": f"Could not decode file with any encoding: {{file_path}}"}}
                continue
                
    except PermissionError:
        return {{"error": f"Permission denied: {{file_path}}"}}
    except Exception as e:
        return {{"error": f"Error reading {{file_path}}: {{str(e)}}"}}

# Execute file reading
result = safe_read_file("{file_path}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    metadata = result.get("metadata", {{}})
    content = result.get("content", "")
    
    print(f"✅ Successfully read {{metadata.get('file_name', 'file')}}")
    print(f"📊 Size: {{metadata.get('file_size_kb', 0)}} KB ({{metadata.get('character_count', 0):,}} characters)")
    print(f"🔤 Encoding: {{metadata.get('encoding_used', 'unknown')}}")
    print(f"📍 Path: {{metadata.get('file_path', 'unknown')}}")
    print("\\n" + "="*50)
    print(content)
'''

def create_list_directory_snippet(directory_path: str, pattern: str = "*", include_hidden: bool = False, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for directory listing"""
    
    return f'''
# Enhanced directory listing with metadata and sorting
import os
from pathlib import Path
from datetime import datetime

def list_directory_enhanced(directory_path, pattern="{pattern}", include_hidden={include_hidden}):
    """List directory contents with metadata and sorting"""
    try:
        path = Path(directory_path).resolve()
        
        if not path.exists():
            return {{"error": f"Directory not found: {{directory_path}}"}}
        
        if not path.is_dir():
            return {{"error": f"Path is not a directory: {{directory_path}}"}}
        
        # Get all items matching pattern
        if include_hidden:
            items = list(path.glob(pattern))
        else:
            items = [item for item in path.glob(pattern) if not item.name.startswith('.')]
        
        if not items:
            return {{
                "status": "success",
                "directory": str(path),
                "pattern": pattern,
                "items": [],
                "summary": {{"total_items": 0, "files": 0, "directories": 0}}
            }}
        
        # Process items
        files = []
        directories = []
        
        for item in items:
            try:
                stat = item.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
                item_data = {{
                    "name": item.name,
                    "path": str(item),
                    "modified": modified,
                    "permissions": oct(stat.st_mode)[-3:]
                }}
                
                if item.is_dir():
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
                error_item = {{
                    "name": item.name,
                    "path": str(item),
                    "error": str(e)
                }}
                files.append(error_item)
        
        # Sort results
        directories.sort(key=lambda x: x["name"].lower())
        files.sort(key=lambda x: x["name"].lower())
        
        return {{
            "status": "success",
            "directory": str(path),
            "pattern": pattern,
            "items": directories + files,
            "summary": {{
                "total_items": len(directories) + len(files),
                "directories": len(directories),
                "files": len(files)
            }},
            "timestamp": datetime.now().isoformat()
        }}
        
    except Exception as e:
        return {{"error": f"Error listing directory: {{str(e)}}"}}

# Execute directory listing
result = list_directory_enhanced("{directory_path}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    directory = result.get("directory", "unknown")
    pattern = result.get("pattern", "*")
    items = result.get("items", [])
    summary = result.get("summary", {{}})
    
    print(f"📂 Directory: {{directory}}")
    print(f"🔍 Pattern: {{pattern}}")
    print(f"📊 Total Items: {{summary.get('total_items', 0)}} ({{summary.get('directories', 0)}} dirs, {{summary.get('files', 0)}} files)")
    print("\\n" + "="*60)
    
    if not items:
        print("📭 No items found matching pattern")
    else:
        # Show directories first
        directories = [item for item in items if "item_count" in item]
        files = [item for item in items if "item_count" not in item]
        
        for directory_item in directories:
            name = directory_item.get("name", "unknown")
            count = directory_item.get("item_count", 0)
            print(f"📁 {{name}}/ ({{count}} items)")
        
        for file_item in files:
            name = file_item.get("name", "unknown")
            size_kb = file_item.get("size_kb", 0)
            print(f"📄 {{name}} ({{size_kb}} KB)")
'''

def create_search_files_snippet(directory: str, pattern: str, recursive: bool = True, case_sensitive: bool = False, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for file searching"""
    
    return f'''
# Enhanced file search with pattern matching
import os
from pathlib import Path
from datetime import datetime

def search_files_enhanced(directory, pattern, recursive={recursive}, case_sensitive={case_sensitive}):
    """Search for files and directories matching pattern"""
    try:
        path = Path(directory).resolve()
        
        if not path.exists():
            return {{"error": f"Directory not found: {{directory}}"}}
        
        if not path.is_dir():
            return {{"error": f"Path is not a directory: {{directory}}"}}
        
        # Prepare search pattern
        search_pattern = pattern if case_sensitive else pattern.lower()
        
        found_files = []
        found_directories = []
        
        # Search function
        def search_in_directory(search_path, depth=0):
            try:
                for item in search_path.iterdir():
                    item_name = item.name if case_sensitive else item.name.lower()
                    
                    # Check if item matches pattern
                    if search_pattern in item_name:
                        item_info = {{
                            "name": item.name,
                            "path": str(item),
                            "relative_path": str(item.relative_to(path)),
                            "depth": depth
                        }}
                        
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
                pass  # Skip directories we can't access
        
        # Perform search
        search_in_directory(path)
        
        # Sort results
        found_files.sort(key=lambda x: x["path"])
        found_directories.sort(key=lambda x: x["path"])
        
        return {{
            "status": "success",
            "search_directory": str(path),
            "pattern": pattern,
            "case_sensitive": case_sensitive,
            "recursive": recursive,
            "results": {{
                "files": found_files,
                "directories": found_directories
            }},
            "summary": {{
                "total_found": len(found_files) + len(found_directories),
                "files_found": len(found_files),
                "directories_found": len(found_directories)
            }},
            "timestamp": datetime.now().isoformat()
        }}
        
    except Exception as e:
        return {{"error": f"Search failed: {{str(e)}}"}}

# Execute file search
result = search_files_enhanced("{directory}", "{pattern}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    search_dir = result.get("search_directory", "unknown")
    pattern = result.get("pattern", "unknown")
    summary = result.get("summary", {{}})
    results_data = result.get("results", {{}})
    
    print(f"🔍 Search Directory: {{search_dir}}")
    print(f"🎯 Pattern: '{{pattern}}'")
    print(f"📊 Total Found: {{summary.get('total_found', 0)}} ({{summary.get('files_found', 0)}} files, {{summary.get('directories_found', 0)}} dirs)")
    print(f"🔄 Recursive: {{result.get('recursive', False)}}")
    print(f"🔤 Case Sensitive: {{result.get('case_sensitive', False)}}")
    print("\\n" + "="*60)
    
    files = results_data.get("files", [])
    directories = results_data.get("directories", [])
    
    if not files and not directories:
        print("📭 No matches found")
    else:
        if directories:
            print("\\n📁 Directories:")
            for directory in directories:
                print(f"  📁 {{directory.get('relative_path', 'unknown')}}")
        
        if files:
            print("\\n📄 Files:")
            for file_item in files:
                size = f"{{file_item.get('size_kb', 0)}} KB"
                print(f"  📄 {{file_item.get('relative_path', 'unknown')}} ({{size}})")
'''

def create_get_file_info_snippet(file_path: str, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for getting file information"""
    
    return f'''
# Get comprehensive file information and metadata
import os
from pathlib import Path
from datetime import datetime

def get_file_info_enhanced(file_path):
    """Get comprehensive file information and metadata"""
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return {{"error": f"File not found: {{file_path}}"}}
        
        stat = path.stat()
        
        file_info = {{
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
        }}
        
        # Add file type specific info
        if path.is_file():
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
        return {{"error": f"Error getting file info: {{str(e)}}"}}

# Execute file info gathering
result = get_file_info_enhanced("{file_path}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    name = result.get("name", "unknown")
    path = result.get("path", "unknown")
    file_type = "📁 Directory" if result.get("is_directory") else f"📄 {{result.get('file_type', 'File').title()}}"
    
    print(f"📛 Name: {{name}}")
    print(f"🏷️ Type: {{file_type}}")
    print(f"📍 Path: {{path}}")
    
    if result.get("is_file"):
        size_kb = result.get("size_kb", 0)
        size_mb = result.get("size_mb")
        if size_mb:
            print(f"📊 Size: {{size_mb}} MB ({{size_kb}} KB)")
        else:
            print(f"📊 Size: {{size_kb}} KB")
    
    print(f"📂 Parent: {{result.get('parent', 'unknown')}}")
    print(f"📅 Created: {{result.get('created', 'unknown')[:19]}}")
    print(f"✏️ Modified: {{result.get('modified', 'unknown')[:19]}}")
    print(f"👁️ Accessed: {{result.get('accessed', 'unknown')[:19]}}")
    print(f"🔒 Permissions: {{result.get('permissions', 'unknown')}}")
    print(f"🔗 Symlink: {{result.get('is_symlink', False)}}")
    
    if result.get("is_file"):
        print(f"📎 Extension: {{result.get('suffix', 'none')}}")
        print(f"📝 Stem: {{result.get('stem', 'unknown')}}")
        print(f"📊 Size (bytes): {{result.get('size_bytes', 0):,}}")
'''

def create_move_file_snippet(source: str, destination: str, overwrite: bool = False, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for moving files"""
    
    return f'''
# Safe file moving/renaming with comprehensive checks
import shutil
from pathlib import Path
from datetime import datetime

def move_file_safe(source, destination, overwrite={overwrite}):
    """Move or rename files and directories safely"""
    try:
        source_path = Path(source).resolve()
        dest_path = Path(destination).resolve()
        
        if not source_path.exists():
            return {{"error": f"Source not found: {{source}}"}}
        
        if dest_path.exists() and not overwrite:
            return {{"error": f"Destination exists and overwrite=False: {{destination}}"}}
        
        # Perform move
        shutil.move(str(source_path), str(dest_path))
        
        return {{
            "status": "success",
            "operation": "move",
            "source": str(source_path),
            "destination": str(dest_path),
            "timestamp": datetime.now().isoformat()
        }}
        
    except Exception as e:
        return {{"error": f"Move failed: {{str(e)}}"}}

# Execute file move
result = move_file_safe("{source}", "{destination}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    source = result.get("source", "unknown")
    destination = result.get("destination", "unknown")
    print(f"✅ Successfully moved:")
    print(f"   📤 From: {{source}}")
    print(f"   📥 To: {{destination}}")
    print(f"⏰ Completed at: {{result.get('timestamp', 'unknown')}}")
'''

def create_delete_file_snippet(file_path: str, force: bool = False, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for deleting files"""
    
    return f'''
# Safe file/directory deletion with comprehensive checks
import shutil
from pathlib import Path
from datetime import datetime

def delete_file_safe(file_path, force={force}):
    """Delete files or directories safely"""
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return {{"error": f"Path not found: {{file_path}}"}}
        
        if path.is_file():
            path.unlink()
            return {{
                "status": "success",
                "operation": "delete_file",
                "path": str(path),
                "timestamp": datetime.now().isoformat()
            }}
        elif path.is_dir():
            if force:
                shutil.rmtree(str(path))
                return {{
                    "status": "success",
                    "operation": "delete_directory",
                    "path": str(path),
                    "timestamp": datetime.now().isoformat()
                }}
            else:
                try:
                    path.rmdir()  # Only works if directory is empty
                    return {{
                        "status": "success",
                        "operation": "delete_empty_directory",
                        "path": str(path),
                        "timestamp": datetime.now().isoformat()
                    }}
                except OSError:
                    return {{"error": f"Directory not empty (use force=True): {{file_path}}"}}
        
    except Exception as e:
        return {{"error": f"Delete failed: {{str(e)}}"}}

# Execute file deletion
result = delete_file_safe("{file_path}")

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    operation = result.get("operation", "delete")
    path = result.get("path", "unknown")
    print(f"✅ Successfully deleted: {{path}}")
    print(f"🔧 Operation: {{operation}}")
    print(f"⏰ Completed at: {{result.get('timestamp', 'unknown')}}")
'''

def create_read_multiple_files_snippet(file_paths: List[str], fail_fast: bool = False, model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for reading multiple files"""
    
    file_paths_str = str(file_paths).replace("'", '"')
    
    return f'''
# Enhanced multiple file reading with progress tracking
import os
from pathlib import Path
from datetime import datetime

def read_file_single(file_path, encoding="utf-8", max_size_mb=10.0):
    """Read a single file with safety checks"""
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return {{"error": f"File not found: {{file_path}}"}}
        
        if not path.is_file():
            return {{"error": f"Path is not a file: {{file_path}}"}}
        
        file_size = path.stat().st_size
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        if file_size > max_size_bytes:
            return {{"error": f"File too large: {{file_size / (1024*1024):.1f}}MB > {{max_size_mb}}MB limit"}}
        
        encodings_to_try = [encoding, 'utf-8', 'latin-1', 'cp1252']
        
        for enc in encodings_to_try:
            try:
                with open(path, 'r', encoding=enc) as f:
                    content = f.read()
                
                return {{
                    "status": "success",
                    "content": content,
                    "metadata": {{
                        "file_path": str(path),
                        "file_name": path.name,
                        "file_size_bytes": file_size,
                        "file_size_kb": round(file_size / 1024, 1),
                        "encoding_used": enc,
                        "character_count": len(content),
                        "timestamp": datetime.now().isoformat()
                    }}
                }}
                
            except UnicodeDecodeError:
                if enc == encodings_to_try[-1]:
                    return {{"error": f"Could not decode file with any encoding: {{file_path}}"}}
                continue
                
    except PermissionError:
        return {{"error": f"Permission denied: {{file_path}}"}}
    except Exception as e:
        return {{"error": f"Error reading {{file_path}}: {{str(e)}}"}}

def read_multiple_files_enhanced(file_paths, fail_fast={fail_fast}):
    """Read multiple files with progress tracking and error handling"""
    if not file_paths:
        return {{"error": "No file paths provided"}}
    
    results = []
    successful_reads = 0
    failed_reads = 0
    total_size_kb = 0
    
    for i, path in enumerate(file_paths):
        try:
            result = read_file_single(path)
            
            if result.get("status") == "success":
                successful_reads += 1
                total_size_kb += result["metadata"]["file_size_kb"]
            else:
                failed_reads += 1
                if fail_fast:
                    return {{
                        "error": f"Failed fast on: {{path}}",
                        "failure_details": result
                    }}
            
            results.append({{
                "file_path": path,
                "result": result
            }})
            
        except Exception as e:
            failed_reads += 1
            error_result = {{"error": f"Exception reading {{path}}: {{str(e)}}"}}
            results.append({{
                "file_path": path,
                "result": error_result
            }})
            
            if fail_fast:
                return {{
                    "error": f"Failed fast on: {{path}}",
                    "failure_details": error_result
                }}
    
    return {{
        "status": "completed",
        "summary": {{
            "total_files": len(file_paths),
            "successful_reads": successful_reads,
            "failed_reads": failed_reads,
            "total_size_kb": round(total_size_kb, 1)
        }},
        "results": results,
        "timestamp": datetime.now().isoformat()
    }}

# Execute multiple file reading
file_paths = {file_paths_str}
result = read_multiple_files_enhanced(file_paths)

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    summary = result.get("summary", {{}})
    results = result.get("results", [])
    
    print(f"📚 Total Files: {{summary.get('total_files', 0)}}")
    print(f"✅ Successful: {{summary.get('successful_reads', 0)}}")
    print(f"❌ Failed: {{summary.get('failed_reads', 0)}}")
    print(f"📊 Total Size: {{summary.get('total_size_kb', 0)}} KB")
    print("\\n" + "="*60)
    
    for file_result in results:
        file_path = file_result.get("file_path", "unknown")
        file_data = file_result.get("result", {{}})
        
        print(f"\\n📄 {{file_path}}")
        print("─" * 40)
        
        if file_data.get("error"):
            print(f"❌ {{file_data['error']}}")
        else:
            metadata = file_data.get("metadata", {{}})
            print(f"✅ {{metadata.get('file_size_kb', 0)}} KB, {{metadata.get('character_count', 0):,}} chars")
            print(f"🔤 Encoding: {{metadata.get('encoding_used', 'unknown')}}")
'''

def create_validate_paths_snippet(paths: List[str], model: str = "claude-sonnet-4") -> str:
    """Generate executable code snippet for path validation"""
    
    paths_str = str(paths).replace("'", '"')
    
    return f'''
# Validate multiple file paths and return status information
from pathlib import Path

def validate_paths_enhanced(paths):
    """Validate multiple file paths and return status information"""
    results = []
    
    for path in paths:
        path_obj = Path(path)
        result = {{
            "path": path,
            "exists": path_obj.exists(),
            "is_file": path_obj.is_file() if path_obj.exists() else None,
            "is_directory": path_obj.is_dir() if path_obj.exists() else None,
            "absolute_path": str(path_obj.resolve())
        }}
        results.append(result)
    
    return {{
        "status": "success",
        "validation_results": results,
        "summary": {{
            "total_paths": len(paths),
            "existing_paths": sum(1 for r in results if r["exists"]),
            "missing_paths": sum(1 for r in results if not r["exists"])
        }}
    }}

# Execute path validation
paths = {paths_str}
result = validate_paths_enhanced(paths)

# Display results
if result.get("error"):
    print(f"❌ Error: {{result['error']}}")
else:
    summary = result.get("summary", {{}})
    validation_results = result.get("validation_results", [])
    
    print(f"📊 Total Paths: {{summary.get('total_paths', 0)}}")
    print(f"✅ Existing: {{summary.get('existing_paths', 0)}}")
    print(f"❌ Missing: {{summary.get('missing_paths', 0)}}")
    print("\\n" + "="*60)
    
    for validation in validation_results:
        path = validation.get("path", "unknown")
        if validation.get("exists"):
            if validation.get("is_file"):
                file_type = "📄 File"
            elif validation.get("is_directory"):
                file_type = "📁 Directory"
            else:
                file_type = "❓ Unknown"
            print(f"✅ {{path}} ({{file_type}})")
        else:
            print(f"❌ {{path}} (Not found)")
'''

def create_button_snippet(operation: str, params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for any file operation
    Universal model compatibility via code generation
    """
    
    if operation == "read_file":
        return create_read_file_snippet(
            params.get("file_path", ""),
            params.get("encoding", "utf-8"),
            params.get("max_size_mb", 10.0),
            model
        )
    
    elif operation == "list_directory":
        return create_list_directory_snippet(
            params.get("directory_path", "."),
            params.get("pattern", "*"),
            params.get("include_hidden", False),
            model
        )
    
    elif operation == "search_files":
        return create_search_files_snippet(
            params.get("directory", "."),
            params.get("pattern", ""),
            params.get("recursive", True),
            params.get("case_sensitive", False),
            model
        )
    
    elif operation == "get_file_info":
        return create_get_file_info_snippet(
            params.get("file_path", ""),
            model
        )
    
    elif operation == "move_file":
        return create_move_file_snippet(
            params.get("source", ""),
            params.get("destination", ""),
            params.get("overwrite", False),
            model
        )
    
    elif operation == "delete_file":
        return create_delete_file_snippet(
            params.get("file_path", ""),
            params.get("force", False),
            model
        )
    
    elif operation == "read_multiple_files":
        return create_read_multiple_files_snippet(
            params.get("file_paths", []),
            params.get("fail_fast", False),
            model
        )
    
    elif operation == "validate_paths":
        return create_validate_paths_snippet(
            params.get("paths", []),
            model
        )
    
    else:
        return f'''
# Unknown file operation: {operation}
print("❌ Error: Unknown file operation '{operation}'")
print("Available operations: read_file, list_directory, search_files, get_file_info, move_file, delete_file, read_multiple_files, validate_paths")
'''