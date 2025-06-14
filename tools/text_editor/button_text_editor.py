"""
TEXT EDITOR
Human Button Generators
"""

from typing import Dict, Any, List
import json

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for text editor operations
    Universal model compatibility via code generation
    
    Args:
        params: Text editor parameters
        model: Target model for code generation
        
    Returns:
        Executable code snippet for Claude 4 Code Execution Tool
    """
    operation = params.get("operation", "create_document")
    
    if operation == "create_document":
        return _create_document_snippet(params, model)
    elif operation == "edit_content":
        return _edit_content_snippet(params, model)
    elif operation == "append_content":
        return _append_content_snippet(params, model)
    elif operation == "format_document":
        return _format_document_snippet(params, model)
    elif operation == "get_document_info":
        return _get_document_info_snippet(params, model)
    elif operation == "validate_path":
        return _validate_path_snippet(params, model)
    elif operation == "create_from_template":
        return _create_from_template_snippet(params, model)
    else:
        return _generic_operation_snippet(params, model)

def _create_document_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for document creation"""
    file_path = params.get("file_path", "")
    content = params.get("content", "")
    document_type = params.get("document_type", "general")
    
    # Escape content for safe inclusion in code
    escaped_content = json.dumps(content)
    
    snippet = f'''
# Text Editor - Create Document
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import create_document
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute document creation
result = create_document(
    file_path="{file_path}",
    content={escaped_content},
    document_type="{document_type}"
)

# Display results
display_text_editor_result(result, verbose=True)

# Auto-save status (seamless)
if result.get("status") == "success":
    from interfaces.ui_tools.ui_text_editor import display_autosave_status
    display_autosave_status(result.get("file_path", ""), "created")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _edit_content_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for content editing"""
    file_path = params.get("file_path", "")
    old_text = params.get("old_text", "")
    new_text = params.get("new_text", "")
    create_backup = params.get("create_backup", True)
    
    # Escape text for safe inclusion in code
    escaped_old_text = json.dumps(old_text)
    escaped_new_text = json.dumps(new_text)
    
    snippet = f'''
# Text Editor - Edit Content
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import edit_content
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute content editing
result = edit_content(
    file_path="{file_path}",
    old_text={escaped_old_text},
    new_text={escaped_new_text},
    create_backup={create_backup}
)

# Display results
display_text_editor_result(result, verbose=True)

# Auto-save status (seamless)
if result.get("status") == "success":
    from interfaces.ui_tools.ui_text_editor import display_autosave_status
    display_autosave_status(result.get("file_path", ""), "updated")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _append_content_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for content appending"""
    file_path = params.get("file_path", "")
    content = params.get("content", "")
    separator = params.get("separator", "\\n")
    
    # Escape content for safe inclusion in code
    escaped_content = json.dumps(content)
    escaped_separator = json.dumps(separator)
    
    snippet = f'''
# Text Editor - Append Content
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import append_content
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute content appending
result = append_content(
    file_path="{file_path}",
    content={escaped_content},
    separator={escaped_separator}
)

# Display results
display_text_editor_result(result, verbose=True)

# Auto-save status (seamless)
if result.get("status") == "success":
    from interfaces.ui_tools.ui_text_editor import display_autosave_status
    display_autosave_status(result.get("file_path", ""), "appended")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _format_document_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for document formatting"""
    file_path = params.get("file_path", "")
    format_type = params.get("format_type", "markdown")
    preserve_backup = params.get("preserve_backup", True)
    
    snippet = f'''
# Text Editor - Format Document
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import format_document
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute document formatting preparation
result = format_document(
    file_path="{file_path}",
    format_type="{format_type}",
    preserve_backup={preserve_backup}
)

# Display results
display_text_editor_result(result, verbose=True)

# Note: This prepares the document for AI formatting
# The actual formatting would be done by an AI model
if result.get("status") == "ready_for_ai_formatting":
    print("\\n📝 Document is ready for AI-powered formatting")
    print(f"Format type: {format_type}")
    print(f"Content length: {{result.get('content_length', 0):,}} characters")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _get_document_info_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for document information"""
    file_path = params.get("file_path", "")
    
    snippet = f'''
# Text Editor - Get Document Info
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import get_document_info
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute document info retrieval
result = get_document_info(file_path="{file_path}")

# Display results
display_text_editor_result(result, verbose=True)

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _validate_path_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for path validation"""
    file_path = params.get("file_path", "")
    
    snippet = f'''
# Text Editor - Validate Path
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import validate_document_path
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute path validation
result = validate_document_path(file_path="{file_path}")

# Display results
display_text_editor_result(result, verbose=True)

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _create_from_template_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate code snippet for template-based document creation"""
    file_path = params.get("file_path", "")
    template_type = params.get("template_type", "markdown")
    title = params.get("title", "")
    author = params.get("author", "")
    
    snippet = f'''
# Text Editor - Create from Template
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import create_document_from_template
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Execute template-based document creation
result = create_document_from_template(
    file_path="{file_path}",
    template_type="{template_type}",
    title="{title}",
    author="{author}"
)

# Display results
display_text_editor_result(result, verbose=True)

# Auto-save status (seamless)
if result.get("status") == "success":
    from interfaces.ui_tools.ui_text_editor import display_autosave_status
    display_autosave_status(result.get("file_path", ""), "created")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def _generic_operation_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate generic operation snippet"""
    operation = params.get("operation", "unknown")
    
    snippet = f'''
# Text Editor - Generic Operation
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import *
from interfaces.ui_tools.ui_text_editor import display_text_editor_result

# Note: Operation '{operation}' not specifically implemented
# Available operations:
# - create_document
# - edit_content  
# - append_content
# - format_document
# - get_document_info
# - validate_document_path
# - create_document_from_template

print("❌ Operation '{operation}' not recognized")
print("\\nAvailable text editor operations:")
print("• create_document - Create new document")
print("• edit_content - Edit existing content")
print("• append_content - Add content to document")
print("• format_document - Prepare for AI formatting")
print("• get_document_info - Analyze document")
print("• validate_document_path - Check path validity")
print("• create_document_from_template - Create from template")

print("\\n" + "="*50)
print("TEXT EDITOR OPERATION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def create_editing_session_snippet(operations: List[Dict[str, Any]], model: str = "claude-sonnet-4") -> str:
    """
    Generate code snippet for a complete editing session with multiple operations
    
    Args:
        operations: List of text editor operations to perform
        model: Target model for code generation
        
    Returns:
        Executable code snippet for editing session
    """
    snippet_parts = ['''
# Text Editor - Complete Editing Session
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import *
from interfaces.ui_tools.ui_text_editor import *
import time

# Start editing session
start_time = time.time()
results = []

print("🚀 Starting Text Editor Session")
print("="*50)
''']
    
    for i, operation in enumerate(operations):
        op_type = operation.get("operation", "unknown")
        
        snippet_parts.append(f'''
# Operation {i+1}: {op_type}
print(f"\\n📝 Operation {i+1}: {op_type.replace('_', ' ').title()}")
''')
        
        if op_type == "create_document":
            file_path = operation.get("file_path", "")
            content = operation.get("content", "")
            document_type = operation.get("document_type", "general")
            escaped_content = json.dumps(content)
            
            snippet_parts.append(f'''
result_{i} = create_document(
    file_path="{file_path}",
    content={escaped_content},
    document_type="{document_type}"
)
display_text_editor_result(result_{i})
results.append(result_{i})
''')
        
        elif op_type == "edit_content":
            file_path = operation.get("file_path", "")
            old_text = operation.get("old_text", "")
            new_text = operation.get("new_text", "")
            escaped_old_text = json.dumps(old_text)
            escaped_new_text = json.dumps(new_text)
            
            snippet_parts.append(f'''
result_{i} = edit_content(
    file_path="{file_path}",
    old_text={escaped_old_text},
    new_text={escaped_new_text}
)
display_text_editor_result(result_{i})
results.append(result_{i})
''')
        
        elif op_type == "append_content":
            file_path = operation.get("file_path", "")
            content = operation.get("content", "")
            escaped_content = json.dumps(content)
            
            snippet_parts.append(f'''
result_{i} = append_content(
    file_path="{file_path}",
    content={escaped_content}
)
display_text_editor_result(result_{i})
results.append(result_{i})
''')
    
    snippet_parts.append('''
# Session summary
end_time = time.time()
session_duration = end_time - start_time

print("\\n" + "="*50)
display_editing_session_summary(results, session_duration)
print("="*50)
''')
    
    return '\\n'.join(snippet_parts).strip()

def create_autosave_workflow_snippet(file_path: str, content_updates: List[str], model: str = "claude-sonnet-4") -> str:
    """
    Generate code snippet for seamless autosave workflow
    
    Args:
        file_path: Path to the document being edited
        content_updates: List of content updates to apply
        model: Target model for code generation
        
    Returns:
        Executable code snippet for autosave workflow
    """
    snippet = f'''
# Text Editor - Seamless Autosave Workflow
import sys
sys.path.append('/Users/seanivore/Development/single-file-agents/sfa-v4')

from tools.text_editor_modular import *
from interfaces.ui_tools.ui_text_editor import *
import time

# Initialize document
file_path = "{file_path}"
print(f"📝 Starting seamless editing session: {{file_path.split('/')[-1]}}")

# Validate path first
path_result = validate_document_path(file_path)
if "error" in path_result:
    print(f"❌ Path validation failed: {{path_result['error']}}")
    exit(1)

# Content updates (simulating real-time editing)
content_updates = {json.dumps(content_updates)}

current_content = ""
for i, update in enumerate(content_updates):
    print(f"\\n✏️ Update {{i+1}}/{{len(content_updates)}}")
    
    if i == 0:
        # Create initial document
        result = create_document(file_path, update, "general")
        current_content = update
    else:
        # Append new content
        result = append_content(file_path, update, "\\n\\n")
        current_content += "\\n\\n" + update
    
    # Seamless autosave indicator (very subtle)
    if result.get("status") == "success":
        display_autosave_status(file_path, "saved")
        print()  # New line after autosave indicator
    
    # Small delay to simulate real editing
    time.sleep(0.5)

# Final document info
print("\\n📊 Final Document Analysis:")
final_info = get_document_info(file_path)
display_text_editor_result(final_info, verbose=True)

print("\\n" + "="*50)
print("SEAMLESS EDITING SESSION COMPLETE")
print("="*50)
'''
    
    return snippet.strip()

def get_model_compatibility_info() -> Dict[str, Any]:
    """
    Get information about model compatibility for text editor operations
    
    Returns:
        Dict with compatibility information
    """
    return {
        "supported_models": [
            "claude-sonnet-4",
            "claude-haiku-4", 
            "gpt-4",
            "gpt-4-turbo",
            "gemini-pro"
        ],
        "operation_costs": {
            "create_document": 0.001,
            "edit_content": 0.002,
            "append_content": 0.001,
            "format_document": 0.003,
            "get_document_info": 0.001,
            "validate_path": 0.0005,
            "create_from_template": 0.002
        },
        "features": {
            "seamless_autosave": True,
            "backup_creation": True,
            "ai_formatting_prep": True,
            "template_support": True,
            "content_analysis": True,
            "path_validation": True
        },
        "limitations": {
            "max_file_size_mb": 10,
            "supported_encodings": ["utf-8"],
            "backup_retention": "session_only"
        }
    } 