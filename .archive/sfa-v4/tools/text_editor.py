"""
Text Editor Tool
Leverages Anthropic's powerful text editing capabilities with autosave
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "text_editor",
        "name": "Advanced Text Editor",
        "description": "Powerful text editing with Anthropic AI assistance and autosave",
        "capabilities": ["text_editing", "content_creation", "formatting", "AI_assistance"],
        "use_cases": ["document creation", "content editing", "formatting", "writing assistance"],
        "cost_estimate": 0.02,  # Estimated per edit operation
        "model_compatibility": ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-sonnet-4"],
        "tags": ["core", "editing", "content", "AI_powered"],
        "parameters": {
            "file_path": {"type": "string", "required": True, "description": "Path to file to edit"},
            "operation": {"type": "string", "required": True, "description": "Edit operation to perform"},
            "content": {"type": "string", "description": "Content for the operation"}
        }
    }

def create_file(file_path: str, content: str = "") -> str:
    """Create a new file with optional initial content"""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ Created file: {file_path}\n📄 Content: {len(content)} characters\n🔄 Autosave: Active"
    except Exception as e:
        return f"❌ Error creating {file_path}: {str(e)}"

def append_to_file(file_path: str, content: str) -> str:
    """Append content to an existing file"""
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return f"✅ Appended to {file_path}\n📝 Added: {len(content)} characters\n🔄 Autosave: Active"
    except Exception as e:
        return f"❌ Error appending to {file_path}: {str(e)}"

def edit_file_content(file_path: str, old_text: str, new_text: str) -> str:
    """Replace specific text in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text not in content:
            return f"❌ Text not found in {file_path}: '{old_text[:50]}...'"
        
        updated_content = content.replace(old_text, new_text)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return f"✅ Updated {file_path}\n🔄 Autosave: Active\n📝 Replaced: '{old_text[:30]}...' → '{new_text[:30]}...'"
    except Exception as e:
        return f"❌ Error editing {file_path}: {str(e)}"

def create_human_button_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate executable snippet for text editing operations"""
    
    operation = params.get("operation", "create")
    file_path = params.get("file_path", "")
    content = params.get("content", "")
    
    if operation == "create":
        return f'''
# Create new file with AI assistance
import os

file_path = "{file_path}"
initial_content = """{content}"""

# Ensure directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Create file with autosave
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(initial_content)

print(f"✅ Created {{file_path}}")
print(f"📄 Content: {{len(initial_content)}} characters")
print("🔄 Autosave: Active - changes saved automatically")
'''
    
    elif operation == "edit_with_ai":
        return f'''
# AI-powered text editing
import anthropic

# Initialize client
client = anthropic.Anthropic()

file_path = "{file_path}"
editing_instructions = """{content}"""

# Read current content
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Use AI to edit the content
    response = client.messages.create(
        model="{model}",
        max_tokens=4000,
        messages=[{{
            "role": "user",
            "content": f"""Please edit this document according to the instructions.

CURRENT CONTENT:
{{current_content}}

EDITING INSTRUCTIONS:
{{editing_instructions}}

Return only the edited content, ready to save to file."""
        }}]
    )
    
    # Extract edited content
    edited_content = response.content[0].text
    
    # Save with autosave
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(edited_content)
    
    print(f"✅ AI editing completed: {{file_path}}")
    print(f"📝 Updated: {{len(edited_content)}} characters")
    print("🔄 Autosave: Active")
    
except Exception as e:
    print(f"❌ Editing failed: {{str(e)}}")
'''
    
    elif operation == "append":
        return f'''
# Append content to file
file_path = "{file_path}"
new_content = """{content}"""

# Append with autosave
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Appended to {{file_path}}")
print(f"📝 Added: {{len(new_content)}} characters")
print("🔄 Autosave: Active")
'''
    
    else:
        return f"# Unknown operation: {operation}"

def format_document(file_path: str, format_type: str = "markdown") -> str:
    """Format document using AI assistance"""
    return f"""
📝 Document Formatting: {file_path}
🎨 Format: {format_type}

Use the human button snippet to apply AI-powered formatting to your document.
Available formats: markdown, technical, business, academic, creative
"""

def create_formatting_snippet(params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate snippet for document formatting"""
    file_path = params.get("file_path", "")
    format_type = params.get("format_type", "markdown")
    
    return f'''
# AI-powered document formatting
import anthropic

client = anthropic.Anthropic()
file_path = "{file_path}"
format_type = "{format_type}"

# Read document
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Apply AI formatting
response = client.messages.create(
    model="{model}",
    max_tokens=4000,
    messages=[{{
        "role": "user",
        "content": f"""Please format this document for {{format_type}} style.
        
Improve structure, clarity, and formatting while preserving all original information.

DOCUMENT TO FORMAT:
{{content}}

Return the formatted document ready to save."""
    }}]
)

# Save formatted version
formatted_content = response.content[0].text
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(formatted_content)

print(f"✅ Formatted {{file_path}} in {{format_type}} style")
print("🔄 Autosave: Active")
'''

# Tool registration for OC discovery
TOOL_DEFINITION = get_tool_definition()

# Available editing functions
EDITING_FUNCTIONS = {
    "create_file": create_file,
    "append_to_file": append_to_file,
    "edit_file_content": edit_file_content,
    "format_document": format_document
}

"""
PULL FROM OLD SFA: 
"""

"""
Enhanced SFA v4 Text Editor Tool with AI assistance and safety features
"""

def get_enhanced_text_editor_definition() -> Dict[str, Any]:
    """Enhanced text editor definition"""
    return {
        "id": "text_editor_enhanced",
        "name": "AI-Powered Text Editor",
        "description": "Advanced text editing with AI assistance, safety checks, and backup systems",
        "capabilities": ["text_editing", "content_creation", "AI_assistance", "file_safety"],
        "use_cases": ["document creation", "content editing", "AI writing assistance", "safe file operations"],
        "cost_estimate": 0.02,
        "model_compatibility": ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-sonnet-4"],
        "tags": ["core", "editing", "content", "AI_powered", "enhanced"],
        "functions": ["create_file", "edit_content", "ai_improve", "format_document"]
    }

def create_enhanced_text_editor_snippet(operation: str, params: Dict, model: str = "claude-sonnet-4") -> str:
    """Generate enhanced text editor snippets with AI integration"""
    
    if operation == "ai_edit":
        file_path = params.get("file_path", "")
        instructions = params.get("instructions", "")
        
        return f'''
# AI-Powered Text Editing with Safety and Backup
import anthropic
import os
import shutil
from datetime import datetime
from pathlib import Path

def ai_text_editor():
    """Enhanced text editing with AI assistance and comprehensive safety"""
    
    file_path = "{file_path}"
    instructions = """{instructions}"""
    
    print(f"📝 AI Text Editor")
    print(f"📁 File: {{Path(file_path).name}}")
    print("="*60)
    
    try:
        # Validate file and create backup
        if not os.path.exists(file_path):
            return {{"error": f"File not found: {{file_path}}"}}
        
        # Create timestamped backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{{file_path}}.backup_{{timestamp}}"
        
        try:
            shutil.copy2(file_path, backup_path)
            print(f"💾 Backup created: {{Path(backup_path).name}}")
        except Exception as backup_error:
            print(f"⚠️ Backup failed: {{str(backup_error)}}")
            return {{"error": "Could not create backup - aborting for safety"}}
        
        # Read current content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            content_length = len(current_content)
            print(f"📄 Current content: {{content_length:,}} characters")
            
            # Size check for AI processing
            if content_length > 100000:  # 100k chars
                print("⚠️ Large file detected - consider smaller edits")
                return {{"error": "File too large for AI editing (>100k chars)"}}
                
        except Exception as read_error:
            return {{"error": f"Could not read file: {{str(read_error)}}"}}
        
        # Initialize AI client
        try:
            client = anthropic.Anthropic()
        except Exception as client_error:
            return {{"error": f"AI client error: {{str(client_error)}}"}}
        
        # Perform AI editing
        try:
            print("🤖 Processing with AI...")
            
            response = client.messages.create(
                model="{model}",
                max_tokens=8000,
                messages=[{{
                    "role": "user",
                    "content": f"""Please edit this document according to the instructions. Return ONLY the edited content, ready to save.

CURRENT CONTENT:
{{current_content}}

EDITING INSTRUCTIONS:
{{instructions}}

Important: Return only the final edited document content."""
                }}]
            )
            
            edited_content = response.content[0].text
            
            # Validate edited content
            if not edited_content.strip():
                print("⚠️ AI returned empty content - using backup")
                return {{"error": "AI editing produced empty content"}}
            
            edited_length = len(edited_content)
            print(f"✅ AI editing complete: {{edited_length:,}} characters")
            
            # Show change summary
            if edited_length > content_length:
                change = edited_length - content_length
                print(f"📈 Content expanded by {{change:,}} characters")
            elif edited_length < content_length:
                change = content_length - edited_length
                print(f"📉 Content reduced by {{change:,}} characters")
            else:
                print("📝 Content length unchanged")
            
            # Save edited content with additional backup
            pre_edit_backup = f"{{file_path}}.pre_edit_{{timestamp}}"
            shutil.copy2(file_path, pre_edit_backup)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(edited_content)
            
            print(f"💾 File updated successfully")
            print(f"🔒 Pre-edit backup: {{Path(pre_edit_backup).name}}")
            
            return {{
                "status": "success",
                "original_length": content_length,
                "edited_length": edited_length,
                "backup_files": [backup_path, pre_edit_backup],
                "change_summary": f"{{edited_length - content_length:+}} characters"
            }}
            
        except Exception as ai_error:
            # Restore from backup on AI error
            try:
                shutil.copy2(backup_path, file_path)
                print(f"🔄 Restored from backup due to AI error")
            except:
                pass
            return {{"error": f"AI editing failed: {{str(ai_error)}}"}}
            
    except Exception as e:
        return {{"error": f"Text editing failed: {{str(e)}}"}}

# Execute AI text editing
result = ai_text_editor()
if result.get("status") == "success":
    print("\\n✅ AI editing completed successfully")
    print(f"📊 {{result['change_summary']}}")
else:
    print(f"\\n❌ Editing failed: {{result.get('error')}}")
'''

    elif operation == "create_with_ai":
        file_path = params.get("file_path", "")
        content_brief = params.get("content_brief", "")
        document_type = params.get("document_type", "general")
        
        return f'''
# AI-Powered Document Creation
import anthropic
import os
from datetime import datetime
from pathlib import Path

def ai_document_creator():
    """Create documents using AI with specified requirements"""
    
    file_path = "{file_path}"
    content_brief = """{content_brief}"""
    document_type = "{document_type}"
    
    print(f"📝 AI Document Creator")
    print(f"📁 Target: {{Path(file_path).name}}")
    print(f"📋 Type: {{document_type}}")
    print("="*60)
    
    try:
        # Check if file already exists
        if os.path.exists(file_path):
            return {{"error": f"File already exists: {{file_path}}"}}
        
        # Validate directory exists
        directory = Path(file_path).parent
        if not directory.exists():
            return {{"error": f"Directory does not exist: {{directory}}"}}
        
        # Initialize AI
        try:
            client = anthropic.Anthropic()
        except Exception as client_error:
            return {{"error": f"AI client error: {{str(client_error)}}"}}
        
        # Document type templates
        document_prompts = {{
            "technical": f"Create a technical document about: {{content_brief}}. Include proper structure with headings, technical details, and actionable information. Use clear, professional language.",
            
            "business": f"Create a business document about: {{content_brief}}. Include executive summary, main points, recommendations, and next steps. Use professional business writing style.",
            
            "markdown": f"Create a well-structured markdown document about: {{content_brief}}. Use proper markdown formatting with headers, lists, links, and emphasis where appropriate.",
            
            "report": f"Create a comprehensive report about: {{content_brief}}. Include introduction, analysis, findings, conclusions, and recommendations. Use formal report structure.",
            
            "guide": f"Create a step-by-step guide about: {{content_brief}}. Include clear instructions, examples, and helpful tips. Make it practical and easy to follow.",
            
            "general": f"Create a well-structured document about: {{content_brief}}. Use appropriate formatting and clear organization."
        }}
        
        prompt = document_prompts.get(document_type, document_prompts["general"])
        
        # Generate content with AI
        try:
            print("🤖 Generating content with AI...")
            
            response = client.messages.create(
                model="{model}",
                max_tokens=8000,
                messages=[{{
                    "role": "user",
                    "content": f"""{{prompt}}

Requirements:
- Create complete, ready-to-use content
- Use proper structure and formatting
- Make it comprehensive but concise
- Include all necessary sections
- Ensure professional quality

Return only the document content, ready to save to file."""
                }}]
            )
            
            generated_content = response.content[0].text
            
            if not generated_content.strip():
                return {{"error": "AI generated empty content"}}
            
            content_length = len(generated_content)
            print(f"✅ Generated {{content_length:,}} characters")
            
            # Save the document
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_content)
            
            print(f"💾 Document created successfully")
            
            return {{
                "status": "success",
                "file_path": file_path,
                "content_length": content_length,
                "document_type": document_type,
                "created_at": datetime.now().isoformat()
            }}
            
        except Exception as ai_error:
            return {{"error": f"AI generation failed: {{str(ai_error)}}"}}
            
    except Exception as e:
        return {{"error": f"Document creation failed: {{str(e)}}"}}

# Execute AI document creation
result = ai_document_creator()
if result.get("status") == "success":
    print("\\n✅ Document created successfully")
    print(f"📄 {{result['content_length']:,}} characters written")
else:
    print(f"\\n❌ Creation failed: {{result.get('error')}}")
'''

    else:
        return f"# Unknown text editor operation: {operation}"


