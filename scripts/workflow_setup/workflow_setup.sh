#!/bin/bash
# Mao Workflow Setup - Process 3-type JSON workflow system
# Usage: workflow_setup.sh <temp_directory_path>

# Function to show usage
show_usage() {
    echo "Usage: setup <temp_directory_path>"
    echo ""
    echo "Process 3-type JSON workflow from temp directory:"
    echo "  - Workflow JSON (high-level workflow definition)"
    echo "  - Phase JSON (individual workflow phases)"  
    echo "  - Handoff JSON (assessment and transition logic)"
    echo ""
    echo "Examples:"
    echo "  setup ./configs/workflows/.temp/market-research/"
    echo "  setup /absolute/path/to/.temp/workflow-name/"
    echo ""
    echo "The temp directory should contain:"
    echo "  - *_workflow_config.json"
    echo "  - *_phase_config.json" 
    echo "  - *_handoff_config.json"
    exit 1
}

# Check if temp directory path provided
if [[ $# -lt 1 ]]; then
    echo "Error: No temp directory path specified"
    show_usage
fi

TEMP_DIR="$1"

# Get absolute path of temp directory
if [[ "$TEMP_DIR" != /* ]]; then
    TEMP_DIR="$(pwd)/$TEMP_DIR"
fi

# Make sure the temp directory exists
if [ ! -d "$TEMP_DIR" ]; then
    echo "Error: Temp directory not found: $TEMP_DIR"
    exit 1
fi

# Get script directory and MAO root
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
MAO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
ORCHESTRATOR_DIR="${MAO_ROOT}/orchestrator"

echo "Mao Workflow Setup"
echo "=================="
echo "Processing temp directory: $TEMP_DIR"
echo "MAO root: $MAO_ROOT"
echo ""

# Find the three required JSON files
WORKFLOW_JSON=$(find "$TEMP_DIR" -name "*_workflow_config.json" | head -1)
PHASE_JSON=$(find "$TEMP_DIR" -name "*_phase_config.json" | head -1)
HANDOFF_JSON=$(find "$TEMP_DIR" -name "*_handoff_config.json" | head -1)

# Verify all three JSON files exist
if [ -z "$WORKFLOW_JSON" ]; then
    echo "Error: No workflow config JSON found (*_workflow_config.json)"
    echo "Expected pattern: [name]_workflow_config.json"
    exit 1
fi

if [ -z "$PHASE_JSON" ]; then
    echo "Error: No phase config JSON found (*_phase_config.json)"
    echo "Expected pattern: [name]_phase_config.json"
    exit 1
fi

if [ -z "$HANDOFF_JSON" ]; then
    echo "Error: No handoff config JSON found (*_handoff_config.json)"
    echo "Expected pattern: [name]_handoff_config.json"
    exit 1
fi

echo "Found JSON files:"
echo "  Workflow: $(basename "$WORKFLOW_JSON")"
echo "  Phase: $(basename "$PHASE_JSON")"
echo "  Handoff: $(basename "$HANDOFF_JSON")"
echo ""

# Extract workflow information using Python
WORKFLOW_INFO=$(python3 -c "
import json, os, sys
try:
    with open('$WORKFLOW_JSON', 'r') as f:
        workflow_config = json.load(f)
    
    # Extract workflow data (first item in workflow array)
    workflow_data = workflow_config['workflow'][0]
    
    # Required fields
    custom_command = workflow_data['custom_command']
    workflow_id = workflow_data['workflow_id']
    user_id = workflow_data['user_id']
    workflow_goal = workflow_data['workflow_goal']
    workflow_deliverable = workflow_data['workflow_deliverable']
    
    # Create output
    print(json.dumps({
        'custom_command': custom_command,
        'workflow_id': workflow_id,
        'user_id': user_id,
        'workflow_goal': workflow_goal,
        'workflow_deliverable': workflow_deliverable
    }))
    
except Exception as e:
    print(f'Error: Failed to parse workflow JSON: {str(e)}')
    sys.exit(1)
")

# Check for any errors in the Python output
if [[ $WORKFLOW_INFO == Error* ]]; then
    echo "$WORKFLOW_INFO"
    exit 1
fi

# Parse the JSON output
CUSTOM_COMMAND=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['custom_command'])")
WORKFLOW_ID=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_id'])")
USER_ID=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['user_id'])")
WORKFLOW_GOAL=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_goal'])")
WORKFLOW_DELIVERABLE=$(echo $WORKFLOW_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_deliverable'])")

echo "Workflow Details:"
echo "  Custom Command: $CUSTOM_COMMAND"
echo "  Workflow ID: $WORKFLOW_ID"
echo "  User ID: $USER_ID"
echo "  Goal: $WORKFLOW_GOAL"
echo "  Deliverable: $WORKFLOW_DELIVERABLE"
echo ""

# Create the workflow directory
WORKFLOW_DIR="${MAO_ROOT}/configs/workflows/${CUSTOM_COMMAND}"
echo "Creating workflow directory: $WORKFLOW_DIR"

if [ -d "$WORKFLOW_DIR" ]; then
    echo "Warning: Workflow directory already exists. Overwriting..."
    rm -rf "$WORKFLOW_DIR"
fi

mkdir -p "$WORKFLOW_DIR"

# Copy JSON files to workflow directory
echo "Copying JSON files to workflow directory..."
cp "$WORKFLOW_JSON" "$WORKFLOW_DIR/"
cp "$PHASE_JSON" "$WORKFLOW_DIR/"
cp "$HANDOFF_JSON" "$WORKFLOW_DIR/"

# Create the custom executable command
USER_BIN="$(cd ~ && pwd)/bin"
mkdir -p "$USER_BIN"

# Extract first word as command name (no hyphens, spaces only)
COMMAND_NAME=$(echo "$CUSTOM_COMMAND" | cut -d ' ' -f1)
COMMAND_ARGS=$(echo "$CUSTOM_COMMAND" | cut -d ' ' -f2-)

COMMAND_PATH="$USER_BIN/$COMMAND_NAME"

echo "Creating custom command: $COMMAND_NAME"

cat > "$COMMAND_PATH" << EOF
#!/bin/bash
# Mao workflow command for $CUSTOM_COMMAND
# Generated from workflow ID: $WORKFLOW_ID

# Workflow configuration
WORKFLOW_ID="$WORKFLOW_ID"
USER_ID="$USER_ID"
WORKFLOW_DIR="$WORKFLOW_DIR"
MAO_ROOT="$MAO_ROOT"

echo "~(=^‥^) Starting workflow: $CUSTOM_COMMAND"
echo "Workflow ID: \$WORKFLOW_ID"
echo "User ID: \$USER_ID"
echo ""

# Check if arguments were provided
if [ \$# -eq 0 ]; then
    # No arguments provided, use the default arguments from config
    if [ -n "$COMMAND_ARGS" ]; then
        ARGS="$COMMAND_ARGS"
        echo "Using default arguments: \$ARGS"
    else
        ARGS=""
    fi
else
    # Use the provided arguments
    ARGS="\$@"
    echo "Using provided arguments: \$ARGS"
fi

# Execute the workflow using MAO orchestrator
cd "\$MAO_ROOT"
python3 -c "
import sys
sys.path.append('.')
from orchestrator.workflow_manager import WorkflowManager

# Initialize workflow manager
workflow_manager = WorkflowManager()

# Execute workflow
try:
    result = workflow_manager.execute_workflow('\$WORKFLOW_ID', '\$USER_ID')
    print('Workflow completed successfully!')
    if result:
        print('Result:', result)
except Exception as e:
    print(f'Error executing workflow: {e}')
    sys.exit(1)
"
EOF

chmod +x "$COMMAND_PATH"

echo "Custom command created: $COMMAND_NAME"
echo "Command path: $COMMAND_PATH"
echo ""

# Generate README for the workflow
README_PATH="$WORKFLOW_DIR/README.md"
echo "Generating README.md..."

cat > "$README_PATH" << EOF
# $CUSTOM_COMMAND

**Workflow ID**: $WORKFLOW_ID  
**User ID**: $USER_ID

## Overview

$WORKFLOW_GOAL

## Deliverable

$WORKFLOW_DELIVERABLE

## Usage

Run the workflow with:
\`\`\`bash
$CUSTOM_COMMAND
\`\`\`

## Files

- **Workflow Config**: $(basename "$WORKFLOW_JSON")
- **Phase Config**: $(basename "$PHASE_JSON")  
- **Handoff Config**: $(basename "$HANDOFF_JSON")

## Integration

This workflow integrates with:
- MAO Orchestrator for execution
- Memory MCP for state management
- Real-time metrics for monitoring
- User configuration system

---
*Generated by Mao Workflow Setup*
EOF

echo "README.md created: $README_PATH"
echo ""

# Clean up temp directory
echo "Cleaning up temp directory: $TEMP_DIR"
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 Workflow setup complete!"
echo ""
echo "Summary:"
echo "  ✅ Workflow directory created: $WORKFLOW_DIR"
echo "  ✅ JSON files copied and organized"
echo "  ✅ Custom command created: $COMMAND_NAME"
echo "  ✅ README.md generated"
echo "  ✅ Temp directory cleaned up"
echo ""
echo "To run your workflow:"
echo "  $CUSTOM_COMMAND"
echo ""
echo "The command is now available system-wide!"
