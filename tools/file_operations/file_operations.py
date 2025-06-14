"""
File Operations Tool - Core Logic
Independent file operation logic with enhanced error handling
"""

import os
import json
import glob
import shutil
import hashlib
import fnmatch
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from datetime import datetime
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError, ResourceError

@handle_errors(operation_name="read_file", return_dict=True)
def read_file(file_path: str, encoding: str = "utf-8", max_size_mb: float = 10.0) -> Dict[str, Any]:
    """
    Read a single file with comprehensive safety checks and encoding fallback
    
    Args:
        file_path: Path to the file to read
        encoding: Primary encoding to try (defaults to utf-8)
        max_size_mb: Maximum file size in MB (defaults to 10.0)
        
    Returns:
        Dict with structured results including content, metadata, or error details
    """
    try:
        # Path validation and normalization
        path = Path(file_path).resolve()
        
        # Check cache first (fingerprinting) - file I/O can be expensive
        cache = CacheManager()
        # Include file modification time in cache key for freshness
        try:
            mtime = path.stat().st_mtime if path.exists() else 0
            cache_key = f"{str(path)}|{encoding}|{max_size_mb}|{mtime}"
            cached_result = cache.get_cached_analysis(cache_key, "file_read")
            if cached_result:
                print(f"💾 Cache HIT: File read for '{path.name}' (instant!)")
                return json.loads(cached_result)
        except:
            pass  # If we can't get mtime, proceed without cache
        
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
                result = {
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
                
                # Cache the result (fingerprinting)
                try:
                    cache.cache_content_analysis(cache_key, json.dumps(result), "file_read")
                    print(f"💾 Cached file read for '{path.name}' - future reads will be instant!")
                except:
                    pass  # Cache failure shouldn't break file reading
                
                return result
                
            except UnicodeDecodeError:
                if enc == encodings_to_try[-1]:  # Last encoding failed
                    return {"error": f"Could not decode file with any encoding: {file_path}"}
                continue
                
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading {file_path}: {str(e)}"}

@handle_errors(operation_name="read_multiple_files", return_dict=True)
def read_multiple_files(file_paths: List[str], fail_fast: bool = False) -> Dict[str, Any]:
    """
    Read multiple files with progress tracking and error handling
    
    Args:
        file_paths: List of file paths to read
        fail_fast: Stop on first error if True
        
    Returns:
        Dict with structured results including summary and individual file results
    """
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

@handle_errors(operation_name="list_directory", return_dict=True)
def list_directory(directory_path: str, pattern: str = "*", include_hidden: bool = False) -> Dict[str, Any]:
    """
    List directory contents with metadata and sorting
    
    Args:
        directory_path: Path to directory to list
        pattern: Glob pattern to match (defaults to "*")
        include_hidden: Include hidden files/directories
        
    Returns:
        Dict with structured directory listing and metadata
    """
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

@handle_errors(operation_name="get_file_info", return_dict=True)
def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive file information and metadata
    
    Args:
        file_path: Path to file or directory to analyze
        
    Returns:
        Dict with comprehensive file information or error details
    """
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
            # Determine file type based on extension
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

@handle_errors(operation_name="search_files", return_dict=True)
def search_files(directory: str, pattern: str, recursive: bool = True, case_sensitive: bool = False) -> Dict[str, Any]:
    """
    Search for files and directories matching pattern
    
    Args:
        directory: Directory to search in
        pattern: Search pattern to match against names
        recursive: Search subdirectories if True
        case_sensitive: Case sensitive matching if True
        
    Returns:
        Dict with search results and metadata
    """
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
        return {"error": f"Error searching files: {str(e)}"}

@handle_errors(operation_name="move_file", return_dict=True)
def move_file(source: str, destination: str, overwrite: bool = False) -> Dict[str, Any]:
    """
    Move or rename files and directories safely
    
    Args:
        source: Source file or directory path
        destination: Destination path
        overwrite: Allow overwriting existing files if True
        
    Returns:
        Dict with operation results or error details
    """
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
        return {"error": f"Error moving file: {str(e)}"}

@handle_errors(operation_name="delete_file", return_dict=True)
def delete_file(file_path: str, force: bool = False) -> Dict[str, Any]:
    """
    Delete files or directories safely
    
    Args:
        file_path: Path to file or directory to delete
        force: Force deletion of directories and their contents
        
    Returns:
        Dict with operation results or error details
    """
    try:
        path = Path(file_path).resolve()
        
        if not path.exists():
            return {"error": f"Path not found: {file_path}"}
        
        if path.is_file():
            path.unlink()
            return {
                "status": "success",
                "operation": "delete_file",
                "path": str(path),
                "timestamp": datetime.now().isoformat()
            }
        elif path.is_dir():
            if force:
                shutil.rmtree(str(path))
                return {
                    "status": "success",
                    "operation": "delete_directory",
                    "path": str(path),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                try:
                    path.rmdir()  # Only works if directory is empty
                    return {
                        "status": "success",
                        "operation": "delete_empty_directory",
                        "path": str(path),
                        "timestamp": datetime.now().isoformat()
                    }
                except OSError:
                    return {"error": f"Directory not empty (use force=True): {file_path}"}
        
    except Exception as e:
        return {"error": f"Error deleting file: {str(e)}"}

@handle_errors(operation_name="validate_paths", return_dict=True)
def validate_paths(paths: List[str]) -> Dict[str, Any]:
    """
    Validate multiple file paths and return status information
    
    Args:
        paths: List of file paths to validate
        
    Returns:
        Dict with validation results for each path
    """
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