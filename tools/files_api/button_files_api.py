"""
FILES API TOOL
Button Snippet Generators - Fixed Version
"""

from typing import Dict, Any
import json
from tools.files_api.files_api import (
    create_workflow_workspace,
    save_workflow_draft,
    prepare_agent_handoff,
    save_agent_deliverables,
    get_workflow_files,
    estimate_cost
)

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Files API operations
    Universal model compatibility via code generation
    
    Args:
        params: Files API parameters
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    operation = params.get("operation", "create_workspace")
    
    if operation == "create_workspace":
        return _create_workspace_snippet(params, model)
    elif operation == "save_draft":
        return _create_draft_snippet(params, model)
    elif operation == "prepare_handoff":
        return _create_handoff_snippet(params, model)
    elif operation == "save_deliverables":
        return _create_deliverables_snippet(params, model)
    elif operation == "get_workflow_files":
        return _create_files_snippet(params, model)
    else:
        return _create_generic_snippet(params, model)

def _create_workspace_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate workspace creation snippet using MAO logic"""
    workflow_id = params.get("workflow_id", "")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"operation": "create_workspace"})
    
    snippet = f'''
# Files API - Create Workflow Workspace
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import create_workflow_workspace
from tools.files_api.ui_files_api import display_files_api_result

# Execute workspace creation using MAO logic
result = create_workflow_workspace("{workflow_id}")

# Display results using MAO UI
display_files_api_result(result, "terminal")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_draft_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate draft saving snippet using MAO logic"""
    workflow_id = params.get("workflow_id", "")
    content = params.get("content", "")
    draft_type = params.get("draft_type", "general")
    phase = params.get("phase", "")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"operation": "save_draft"})
    
    # Escape content for safe inclusion in code
    escaped_content = json.dumps(content)
    
    snippet = f'''
# Files API - Save Draft
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import save_workflow_draft
from tools.files_api.ui_files_api import display_files_api_result

# Execute draft save using MAO logic
result = save_workflow_draft(
    workflow_id="{workflow_id}",
    content={escaped_content},
    draft_type="{draft_type}",
    phase="{phase}" if "{phase}" else None
)

# Display results using MAO UI
display_files_api_result(result, "terminal")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_handoff_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate agent handoff preparation snippet using MAO logic"""
    workflow_id = params.get("workflow_id", "")
    agent_materials = params.get("agent_materials", {})
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"operation": "prepare_handoff"})
    
    snippet = f'''
# Files API - Prepare Agent Handoff
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import prepare_agent_handoff
from tools.files_api.ui_files_api import display_files_api_result

# Agent materials to package for handoff
agent_materials = {agent_materials}

# Execute handoff preparation using MAO logic
result = prepare_agent_handoff(
    workflow_id="{workflow_id}",
    agent_materials=agent_materials
)

# Display results using MAO UI
display_files_api_result(result, "terminal")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_deliverables_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate deliverables saving snippet using MAO logic"""
    workflow_id = params.get("workflow_id", "")
    phase = params.get("phase", "")
    deliverables = params.get("deliverables", {})
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"operation": "save_deliverables"})
    
    snippet = f'''
# Files API - Save Deliverables
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import save_agent_deliverables
from tools.files_api.ui_files_api import display_files_api_result

# Deliverables to save
deliverables = {deliverables}

# Execute deliverables save using MAO logic
result = save_agent_deliverables(
    workflow_id="{workflow_id}",
    phase="{phase}",
    deliverables=deliverables
)

# Display results using MAO UI
display_files_api_result(result, "terminal")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_files_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate workflow files listing snippet using MAO logic"""
    workflow_id = params.get("workflow_id", "")
    
    # Get cost estimate from MAO logic
    cost_estimate = estimate_cost({"operation": "get_workflow_files"})
    
    snippet = f'''
# Files API - Get Workflow Files
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import get_workflow_files
from tools.files_api.ui_files_api import display_files_api_result

# Execute workflow files listing using MAO logic
result = get_workflow_files("{workflow_id}")

# Display results using MAO UI
display_files_api_result(result, "terminal")

print(f"💰 Estimated cost: ${cost_estimate:.4f}")

# Return result for workflow integration
result
'''
    
    return snippet.strip()

def _create_generic_snippet(params: Dict[str, Any], model: str) -> str:
    """Generate generic Files API snippet"""
    operation = params.get("operation", "unknown")
    
    snippet = f'''
# Files API - {operation.title()}
import sys
sys.path.append('/Users/seanivore/Development/modular-agent-orchestrator')

from tools.files_api.files_api import estimate_cost

# Get available operations and cost
cost_estimate = estimate_cost({{"operation": "{operation}"}})

result = {{
    "error": f"Unknown Files API operation: {operation}",
    "available_operations": [
        "create_workspace",
        "save_draft", 
        "prepare_handoff",
        "save_deliverables",
        "get_workflow_files"
    ],
    "cost": cost_estimate
}}

print("📁 Files API Operation:")
print(f"❌ Error: {{result['error']}}")
print("Available operations:")
for op in result["available_operations"]:
    print(f"  • {{op}}")
    
print(f"💰 Estimated cost: ${{cost_estimate:.4f}}")

# Return result
result
'''
    
    return snippet.strip()
