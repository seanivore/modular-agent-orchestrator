#!/usr/bin/env python3
"""
Token Counter Tool for SFA Agents

This script provides a tool that can be called by SFA agents
to check token counts before saving files.
"""

import os
import sys
import json
from typing import Dict, Any, Optional, Union, List

def count_text_tokens(text: str) -> int:
    """Count tokens in a text string using approximate counting."""
    if not text or text.strip() == "":
        print("Warning: Empty text provided to token counter")
        return 0
        
    try:
        # Simple approximation: ~3.5 chars per token on average
        has_code = '```' in text or any(tag in text for tag in ['def ', 'class ', 'function', 'var ', 'const '])
        chars_per_token = 4.0 if has_code else 3.5
        
        return max(1, int(len(text) / chars_per_token))
    except Exception as e:
        print(f"Error counting tokens: {str(e)}")
        return 0

def count_file_tokens(file_path: str) -> Dict[str, Union[int, str, bool]]:
    """Count tokens in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content or content.strip() == "":
            print(f"Warning: File {file_path} is empty")
            return {
                "file_path": file_path,
                "token_count": 0,
                "status": "warning: empty file",
                "is_safe": True  # Empty files are technically "safe" from a token limit perspective
            }
            
        token_count = count_text_tokens(content)
        print(f"Token count for {file_path}: {token_count} tokens")
        return {
            "file_path": file_path,
            "token_count": token_count,
            "status": "success",
            "is_safe": token_count < 7500 and token_count > 0  # Must be positive and below limit
        }
    except Exception as e:
        print(f"Error counting tokens in file: {str(e)}")
        return {
            "file_path": file_path,
            "token_count": 0,
            "status": f"error: {str(e)}",
            "is_safe": False
        }

def count_directory_tokens(dir_path: str) -> Dict[str, Union[List, int, bool]]:
    """Count tokens in all files in a directory."""
    if not os.path.isdir(dir_path):
        return {
            "status": "error",
            "message": f"{dir_path} is not a directory",
            "is_safe": False,
            "total_tokens": 0,
            "files_checked": 0,
            "results": [],
            "risky_files": []
        }
    
    results = []
    risky_files = []
    total_tokens = 0
    files_checked = 0
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.md', '.txt', '.py', '.json', '.sh')):
                files_checked += 1
                file_path = os.path.join(root, file)
                result = count_file_tokens(file_path)
                rel_path = os.path.relpath(file_path, dir_path)
                
                file_result = {
                    "file": rel_path,
                    "token_count": result["token_count"],
                    "is_safe": result["is_safe"]
                }
                
                results.append(file_result)
                total_tokens += result["token_count"]
                
                if not result["is_safe"]:
                    risky_files.append(file_result)
    
    return {
        "status": "success",
        "directory": dir_path,
        "files_checked": files_checked,
        "total_tokens": total_tokens,
        "results": results,
        "risky_files": risky_files,
        "is_safe": len(risky_files) == 0
    }

def token_counter_tool(text: Optional[str] = None, 
                      file_path: Optional[str] = None,
                      dir_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Token counter tool function that interfaces with the SFA agent.
    
    Args:
        text: Optional text to count tokens for
        file_path: Optional file path to count tokens for
        dir_path: Optional directory path to scan for token counts
        
    Returns:
        Dictionary with token count results
    """
    try:
        if not any([text, file_path, dir_path]):
            return {
                "status": "error",
                "message": "Must provide either text, file_path, or dir_path",
                "token_count": 0,
                "is_safe": False
            }
            
        if text:
            token_count = count_text_tokens(text)
            return {
                "status": "success",
                "token_count": token_count,
                "is_safe": token_count < 7500 and token_count > 0,
                "message": f"Token count: {token_count}"
            }
            
        elif file_path:
            return count_file_tokens(file_path)
            
        elif dir_path:
            return count_directory_tokens(dir_path)
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "token_count": 0,
            "is_safe": False
        }

# Tool registration information
def get_tool_definition():
    """Return the tool definition for SFA integration."""
    return {
        "name": "token_counter",
        "description": "Count tokens in text or files to check if they're within the safe limit for Claude",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to count tokens for"
                },
                "file_path": {
                    "type": "string",
                    "description": "File path to count tokens for"
                },
                "dir_path": {
                    "type": "string",
                    "description": "Directory path to scan for token counts"
                }
            }
        },
        "function": token_counter_tool
    }

if __name__ == "__main__":
    # If run directly, print the tool definition
    print(json.dumps(
        {k: v for k, v in get_tool_definition().items() if k != "function"},
        indent=2
    ))