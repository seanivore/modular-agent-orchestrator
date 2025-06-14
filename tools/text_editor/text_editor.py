"""
Text Editor Tool - Core Logic
Advanced text editing with AI assistance and seamless autosave
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError, ResourceError

@handle_errors(operation_name="create_document", return_dict=True)
def create_document(file_path: str, content: str = "", document_type: str = "general") -> Dict[str, Any]:
    """
    Create a new document with optional initial content
    
    Args:
        file_path: Path where the document should be created
        content: Initial content for the document
        document_type: Type of document for formatting hints
        
    Returns:
        Dict with creation results or error details
    """
    # Validation
    if not file_path or not file_path.strip():
        raise ValidationError("File path cannot be empty", "file_path", file_path)
    
    # Ensure directory exists
    directory = Path(file_path).parent
    directory.mkdir(parents=True, exist_ok=True)
    
    # Check if file already exists
    if Path(file_path).exists():
        raise ResourceError(f"File already exists: {file_path}", "file", file_path)
    
    # Create file with content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return {
        "status": "success",
        "operation": "create_document",
        "file_path": str(Path(file_path).resolve()),
        "file_name": Path(file_path).name,
        "content_length": len(content),
        "document_type": document_type,
        "timestamp": datetime.now().isoformat()
    }

@handle_errors(operation_name="edit_content", return_dict=True)
def edit_content(file_path: str, old_text: str, new_text: str, create_backup: bool = True) -> Dict[str, Any]:
    """
    Edit specific content in a document with automatic backup
    
    Args:
        file_path: Path to the document to edit
        old_text: Text to find and replace
        new_text: Replacement text
        create_backup: Whether to create a backup before editing
        
    Returns:
        Dict with edit results or error details
    """
    # Validation
    if not file_path or not file_path.strip():
        raise ValidationError("File path cannot be empty", "file_path", file_path)
    
    file_path = Path(file_path).resolve()
    
    if not file_path.exists():
        raise ResourceError(f"File not found: {file_path}", "file", str(file_path))
    
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text not in content:
        return {"error": f"Text not found in document: '{old_text[:50]}...'"}
    
    # Create backup if requested
    backup_path = None
    if create_backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{file_path}.backup_{timestamp}"
        try:
            shutil.copy2(file_path, backup_path)
        except Exception as backup_error:
            return {"error": f"Backup creation failed: {str(backup_error)}"}
    
    # Perform replacement
    updated_content = content.replace(old_text, new_text)
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return {
        "status": "success",
        "operation": "edit_content",
        "file_path": str(file_path),
        "file_name": file_path.name,
        "original_length": len(content),
        "updated_length": len(updated_content),
        "change_delta": len(updated_content) - len(content),
        "backup_path": backup_path,
        "timestamp": datetime.now().isoformat()
    }

@handle_errors(operation_name="append_content", return_dict=True)
def append_content(file_path: str, content: str, separator: str = "\n") -> Dict[str, Any]:
    """
    Append content to an existing document
    
    Args:
        file_path: Path to the document
        content: Content to append
        separator: Separator to use before new content
        
    Returns:
        Dict with append results or error details
    """
    # Validation
    if not file_path or not file_path.strip():
        raise ValidationError("File path cannot be empty", "file_path", file_path)
    
    file_path = Path(file_path).resolve()
    
    if not file_path.exists():
        raise ResourceError(f"File not found: {file_path}", "file", str(file_path))
    
    # Read current content to get original length
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Append new content
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(separator + content)
    
    return {
        "status": "success",
        "operation": "append_content",
        "file_path": str(file_path),
        "file_name": file_path.name,
        "original_length": len(original_content),
        "appended_length": len(content),
        "total_length": len(original_content) + len(separator) + len(content),
        "timestamp": datetime.now().isoformat()
    }

@handle_errors(operation_name="format_document", return_dict=True)
def format_document(file_path: str, format_type: str = "markdown", preserve_backup: bool = True) -> Dict[str, Any]:
    """
    Apply formatting to a document (placeholder for AI formatting)
    
    Args:
        file_path: Path to the document to format
        format_type: Type of formatting to apply
        preserve_backup: Whether to create a backup before formatting
        
    Returns:
        Dict with formatting instructions or error details
    """
    try:
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup if requested
        backup_path = None
        if preserve_backup:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{file_path}.backup_{timestamp}"
            try:
                shutil.copy2(file_path, backup_path)
            except Exception as backup_error:
                return {"error": f"Backup creation failed: {str(backup_error)}"}
        
        return {
            "status": "ready_for_ai_formatting",
            "operation": "format_document",
            "file_path": str(file_path),
            "file_name": file_path.name,
            "format_type": format_type,
            "content_length": len(content),
            "backup_path": backup_path,
            "content": content,  # For AI processing
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Document formatting preparation failed: {str(e)}"}

@handle_errors(operation_name="get_document_info", return_dict=True)
def get_document_info(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a document
    
    Args:
        file_path: Path to the document
        
    Returns:
        Dict with document information or error details
    """
    try:
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        # Get file stats
        stat = file_path.stat()
        
        # Read content for analysis
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic content analysis
        lines = content.splitlines()
        words = len(content.split())
        characters = len(content)
        characters_no_spaces = len(content.replace(' ', ''))
        
        return {
            "status": "success",
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size_bytes": stat.st_size,
            "file_size_kb": round(stat.st_size / 1024, 1),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "content_stats": {
                "characters": characters,
                "characters_no_spaces": characters_no_spaces,
                "words": words,
                "lines": len(lines),
                "paragraphs": len([line for line in lines if line.strip()]),
                "empty_lines": len([line for line in lines if not line.strip()])
            },
            "document_type": _detect_document_type(file_path, content),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Document info retrieval failed: {str(e)}"}

def _detect_document_type(file_path: Path, content: str) -> str:
    """
    Detect document type based on file extension and content
    
    Args:
        file_path: Path to the document
        content: Document content
        
    Returns:
        Detected document type
    """
    extension = file_path.suffix.lower()
    
    # Extension-based detection
    if extension in ['.md', '.markdown']:
        return "markdown"
    elif extension in ['.txt']:
        return "plain_text"
    elif extension in ['.py']:
        return "python_code"
    elif extension in ['.js']:
        return "javascript_code"
    elif extension in ['.html']:
        return "html"
    elif extension in ['.css']:
        return "css"
    elif extension in ['.json']:
        return "json"
    elif extension in ['.xml']:
        return "xml"
    elif extension in ['.yaml', '.yml']:
        return "yaml"
    
    # Content-based detection for unknown extensions
    content_lower = content.lower()
    if content_lower.startswith('# ') or '## ' in content_lower:
        return "markdown"
    elif content_lower.startswith('<!doctype') or '<html' in content_lower:
        return "html"
    elif 'def ' in content_lower and 'import ' in content_lower:
        return "python_code"
    elif 'function ' in content_lower and 'var ' in content_lower:
        return "javascript_code"
    
    return "general"

@handle_errors(operation_name="validate_document_path", return_dict=True)
def validate_document_path(file_path: str) -> Dict[str, Any]:
    """
    Validate a document path for editing operations
    
    Args:
        file_path: Path to validate
        
    Returns:
        Dict with validation results
    """
    try:
        path = Path(file_path).resolve()
        
        return {
            "status": "success",
            "file_path": str(path),
            "file_name": path.name,
            "directory": str(path.parent),
            "exists": path.exists(),
            "is_file": path.is_file() if path.exists() else None,
            "is_writable": os.access(path.parent, os.W_OK),
            "extension": path.suffix,
            "absolute_path": str(path)
        }
        
    except Exception as e:
        return {"error": f"Path validation failed: {str(e)}"}

@handle_errors(operation_name="create_document_from_template", return_dict=True)
def create_document_from_template(file_path: str, template_type: str, title: str = "", author: str = "") -> Dict[str, Any]:
    """
    Create a document from a predefined template
    
    Args:
        file_path: Path where the document should be created
        template_type: Type of template to use
        title: Document title
        author: Document author
        
    Returns:
        Dict with creation results or error details
    """
    templates = {
        "markdown": f"""# {title or "Document Title"}

**Author:** {author or "Author Name"}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Introduction

Write your introduction here.

## Main Content

Add your main content here.

## Conclusion

Summarize your key points here.
""",
        
        "technical": f"""# {title or "Technical Document"}

**Author:** {author or "Author Name"}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Version:** 1.0

## Overview

Brief overview of the technical topic.

## Requirements

- Requirement 1
- Requirement 2
- Requirement 3

## Implementation

Detailed implementation steps.

## Testing

Testing procedures and validation.

## Conclusion

Summary and next steps.
""",
        
        "business": f"""# {title or "Business Document"}

**Author:** {author or "Author Name"}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary

Key points and recommendations.

## Background

Context and background information.

## Analysis

Detailed analysis and findings.

## Recommendations

Actionable recommendations.

## Next Steps

Implementation plan and timeline.
""",
        
        "report": f"""# {title or "Report Title"}

**Author:** {author or "Author Name"}  
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Abstract

Brief summary of the report.

## Introduction

Background and objectives.

## Methodology

Approach and methods used.

## Results

Key findings and results.

## Discussion

Analysis and interpretation.

## Conclusions

Summary and implications.

## References

Sources and citations.
""",
        
        "plain": f"""{title or "Document Title"}

Author: {author or "Author Name"}
Date: {datetime.now().strftime('%Y-%m-%d')}

Introduction:

Main Content:

Conclusion:
"""
    }
    
    template_content = templates.get(template_type, templates["plain"])
    
    return create_document(file_path, template_content, template_type) 