#!/usr/bin/env python3
"""
Self-contained token counter command-line tool
Usage:
    token_standalone.py "text in quotes"  - Count tokens in text
    token_standalone.py file.md           - Count tokens in file
    token_standalone.py directory/        - Count tokens in directory
"""

import sys
import os
import re
from typing import Dict, Union, Optional, Any, List

# ----------- Token Counter Core Functions -----------

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

# ----------- Pretty Printing Functions -----------

def pretty_print_results(title, result):
    """Print token count results in a more readable format."""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50)
    
    if "token_count" in result:
        print(f"Token count: {result['token_count']:,}")
        safe_status = "✓ Within limits" if result.get("is_safe", False) else "⚠ Exceeds recommended limit"
        print(f"Status: {safe_status}")
    
    if "files_checked" in result:
        print(f"\nChecked {result['files_checked']} files")
        print(f"Total tokens: {result['total_tokens']:,}")
        if result["risky_files"]:
            print(f"\n⚠ {len(result['risky_files'])} files exceed the recommended limit:")
            for file in result["risky_files"]:
                print(f"  - {file['file']}: {file['token_count']:,} tokens")
        else:
            print("\n✓ All files are within the recommended limit")
    
    print("=" * 50)

# ----------- Main Function -----------

def main():
    # Check for arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  token \"text to count\"  - Count tokens in text")
        print("  token file.md          - Count tokens in a file")
        print("  token directory/       - Count tokens in all files in directory")
        sys.exit(1)
    
    # Get the argument (joining all args to handle spaces)
    arg = " ".join(sys.argv[1:])
    
    # Check if it's quoted text
    quoted_match = re.match(r'^["\'](.*)["\']$', arg)
    if quoted_match:
        text = quoted_match.group(1)
        token_count = count_text_tokens(text)
        result = {
            "token_count": token_count,
            "is_safe": token_count < 7500 and token_count > 0
        }
        pretty_print_results("Text Token Count", result)
        return
    
    # Check for a file or directory
    path = os.path.expanduser(arg)  # Handle ~ in paths
    
    if os.path.isfile(path):
        result = count_file_tokens(path)
        pretty_print_results(f"File: {os.path.basename(path)}", result)
    elif os.path.isdir(path):
        result = count_directory_tokens(path)
        pretty_print_results(f"Directory: {os.path.basename(path)}", result)
    else:
        print(f"Error: '{arg}' is not valid text in quotes, a file, or a directory")
        print("")
        print("Usage:")
        print("  token \"text to count\"  - Count tokens in text")
        print("  token file.md          - Count tokens in a file")
        print("  token directory/       - Count tokens in all files in directory")
        sys.exit(1)

if __name__ == "__main__":
    main()