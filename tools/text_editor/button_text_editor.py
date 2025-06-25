"""
TEXT EDITOR
Human Button Generator - Standardized Single Entry Point
"""

from typing import Dict, Any, List
import json
from tools.text_editor.text_editor import (
    create_document, edit_content, append_content, format_document,
    get_document_info, validate_document_path, create_document_from_template, estimate_cost
)


def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for text editor operations
    
    Args:
        params: Text editor parameters
        model: Target model for code generation
        
    Returns:
        Executable code snippet using MAO logic functions
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
        return _create_document_snippet(params, model)  # Default


def _create_document_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate document creation snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    content = params.get("content", "")
    document_type = params.get("document_type", "general")
    
    escaped_content = json.dumps(content)
    
    return f'''
# Text Editor - Create Document Using MAO Logic Functions
import json
from tools.text_editor.text_editor import create_document, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result, display_autosave_status

def execute_document_creation():
    """Execute document creation using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}",
        "content": {escaped_content},
        "document_type": "{document_type}"
    }}
    
    print("📝 Text Editor - Create Document")
    print(f"📁 File: {{params['file_path']}}")
    print(f"📊 Content: {{len(params['content']):,}} characters")
    print(f"📋 Type: {{params['document_type']}}")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = create_document(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            # Seamless autosave indicator
            display_autosave_status(result.get("file_path", ""), "created")
            print(f"\\n✅ Document created successfully")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Document creation failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure file path is valid and MAO modules are installed")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_document_creation()
'''


def _edit_content_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate content editing snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    old_text = params.get("old_text", "")
    new_text = params.get("new_text", "")
    create_backup = params.get("create_backup", True)
    
    escaped_old_text = json.dumps(old_text)
    escaped_new_text = json.dumps(new_text)
    
    return f'''
# Text Editor - Edit Content Using MAO Logic Functions
import json
from tools.text_editor.text_editor import edit_content, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result, display_autosave_status

def execute_content_editing():
    """Execute content editing using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}",
        "old_text": {escaped_old_text},
        "new_text": {escaped_new_text},
        "create_backup": {create_backup}
    }}
    
    print("📝 Text Editor - Edit Content")
    print(f"📁 File: {{params['file_path']}}")
    print(f"🔄 Replacing: {{params['old_text'][:50]}}...")
    print(f"✨ With: {{params['new_text'][:50]}}...")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = edit_content(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            # Seamless autosave indicator
            display_autosave_status(result.get("file_path", ""), "updated")
            print(f"\\n✅ Content edited successfully")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Content editing failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure file exists and text to replace is found")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_content_editing()
'''


def _append_content_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate content appending snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    content = params.get("content", "")
    separator = params.get("separator", "\\n")
    
    escaped_content = json.dumps(content)
    escaped_separator = json.dumps(separator)
    
    return f'''
# Text Editor - Append Content Using MAO Logic Functions
import json
from tools.text_editor.text_editor import append_content, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result, display_autosave_status

def execute_content_appending():
    """Execute content appending using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}",
        "content": {escaped_content},
        "separator": {escaped_separator}
    }}
    
    print("📝 Text Editor - Append Content")
    print(f"📁 File: {{params['file_path']}}")
    print(f"📊 Adding: {{len(params['content']):,}} characters")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = append_content(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            # Seamless autosave indicator
            display_autosave_status(result.get("file_path", ""), "appended")
            print(f"\\n✅ Content appended successfully")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Content appending failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure file exists and is writable")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_content_appending()
'''


def _format_document_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate document formatting snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    format_type = params.get("format_type", "markdown")
    preserve_backup = params.get("preserve_backup", True)
    
    return f'''
# Text Editor - Format Document Using MAO Logic Functions
import json
from tools.text_editor.text_editor import format_document, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result

def execute_document_formatting():
    """Execute document formatting using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}",
        "format_type": "{format_type}",
        "preserve_backup": {preserve_backup}
    }}
    
    print("📝 Text Editor - Format Document")
    print(f"📁 File: {{params['file_path']}}")
    print(f"🎨 Format: {{params['format_type']}}")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = format_document(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "ready_for_ai_formatting":
            print(f"\\n✅ Document prepared for AI formatting")
            print(f"🎨 Format type: {{params['format_type']}}")
            print(f"📊 Content length: {{result.get('content_length', 0):,}} characters")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Document formatting preparation failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure file exists and is readable")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_document_formatting()
'''


def _get_document_info_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate document info snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    
    return f'''
# Text Editor - Get Document Info Using MAO Logic Functions
from tools.text_editor.text_editor import get_document_info, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result

def execute_document_info():
    """Execute document info retrieval using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}"
    }}
    
    print("📝 Text Editor - Document Analysis")
    print(f"📁 File: {{params['file_path']}}")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = get_document_info(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            print(f"\\n✅ Document analysis complete")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Document analysis failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure file exists and is readable")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_document_info()
'''


def _validate_path_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate path validation snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    
    return f'''
# Text Editor - Validate Path Using MAO Logic Functions
from tools.text_editor.text_editor import validate_document_path, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result

def execute_path_validation():
    """Execute path validation using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}"
    }}
    
    print("📝 Text Editor - Path Validation")
    print(f"📁 Path: {{params['file_path']}}")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = validate_document_path(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            print(f"\\n✅ Path validation complete")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Path validation failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Check path format and permissions")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_path_validation()
'''


def _create_from_template_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate template creation snippet using MAO logic functions"""
    file_path = params.get("file_path", "")
    template_type = params.get("template_type", "markdown")
    title = params.get("title", "")
    author = params.get("author", "")
    
    return f'''
# Text Editor - Create from Template Using MAO Logic Functions
import json
from tools.text_editor.text_editor import create_document_from_template, estimate_cost
from tools.text_editor.ui_text_editor import display_text_editor_result, display_autosave_status

def execute_template_creation():
    """Execute template-based document creation using MAO logic functions"""
    
    params = {{
        "file_path": "{file_path}",
        "template_type": "{template_type}",
        "title": "{title}",
        "author": "{author}"
    }}
    
    print("📝 Text Editor - Create from Template")
    print(f"📁 File: {{params['file_path']}}")
    print(f"📋 Template: {{params['template_type']}}")
    print(f"📄 Title: {{params['title'] or 'Auto-generated'}}")
    print("="*50)
    
    try:
        # Use MAO logic function
        result = create_document_from_template(**params)
        
        # Display results using MAO UI function
        display_text_editor_result(result, verbose=True)
        
        if result.get("status") == "success":
            # Seamless autosave indicator
            display_autosave_status(result.get("file_path", ""), "created")
            print(f"\\n✅ Document created from template")
            print(f"📋 Template: {{params['template_type']}}")
            print(f"💰 Estimated cost: ${estimate_cost(params):.4f}")
        else:
            print("❌ Template document creation failed")
    
    except Exception as e:
        print(f"❌ Error: {{str(e)}}")
        print("💡 Ensure template type is valid and path is writable")

    print("\\n" + "="*50)
    print("TEXT EDITOR OPERATION COMPLETE")
    print("="*50)

execute_template_creation()
'''
