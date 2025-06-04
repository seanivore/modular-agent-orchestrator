#!/bin/bash

# SFA workflow setup script
# Usage: setup-sfa-workflow.sh <json_config_file>

if [ $# -lt 1 ]; then
    echo "Usage: $0 <config_file.json>"
    exit 1
fi

CONFIG_FILE="$1"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="${PARENT_DIR}/tools"

# Check if the tools directory exists at the root level
if [ ! -d "$TOOLS_DIR" ]; then
    echo "Error: Tools directory not found at $TOOLS_DIR"
    echo "Please make sure the tools directory exists and contains required tools."
    exit 1
fi

# Check for token counter tool
if [ ! -f "$TOOLS_DIR/token_counter.py" ]; then
    echo "Error: Token counter tool not found at $TOOLS_DIR/token_counter.py"
    echo "This tool is required for reliable output saving."
    exit 1
fi

# Check for task reporting tool
if [ ! -f "$TOOLS_DIR/task_reporting.py" ]; then
    echo "Warning: Task reporting tool not found at $TOOLS_DIR/task_reporting.py"
    echo "Task reporting features will not be available."
fi

# Get absolute path of JSON file
if [[ "$CONFIG_FILE" != /* ]]; then
    CONFIG_FILE="$(pwd)/$CONFIG_FILE"
fi

BASE_DIR="$(dirname "$(readlink -f "$0")")"

# Check for token counter tools
if [ ! -f "${TOOLS_DIR}/token_counter.py" ]; then
    echo "Token counter tools not found in main tools directory."
    echo "For reliable output saving, please ensure token_counter.py exists in ${TOOLS_DIR}"
    echo "Would you like to check if these tools exist in the setup scripts? (y/n)"
    read -r setup_token_counter
    if [[ "$setup_token_counter" =~ ^[Yy]$ ]]; then
        # This assumes token_counter.py might exist in the same directory as this script
        if [ -f "${BASE_DIR}/token_counter.py" ]; then
            echo "Found token_counter.py in setup scripts directory."
            echo "To install it to the tools directory, run:"
            echo "  cp \"${BASE_DIR}/token_counter.py\" \"${TOOLS_DIR}/\""
            echo "  chmod +x \"${TOOLS_DIR}/token_counter.py\""
        else
            echo "Warning: Token counter files not found in ${BASE_DIR}"
            echo "Please ensure token_counter.py exists in ${TOOLS_DIR} for token review features."
        fi
    fi
fi

# Extract info using Python
CONFIG_INFO=$(python3 -c "
import json, os, sys
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

# Get the script name and command
script_name = next((k for k in config.keys() if k != 'A' and k != 'F'), None)
command = config.get('A', '').replace(' ', '-')
use_case_dir = config.get('F', '')
if not script_name or not command or not use_case_dir:
    print('Error: Invalid config file format - missing required A and F variables')
    sys.exit(1)

# Get use case name
use_case = command.split('-')[1] if '-' in command else command

# Remove trailing slash from use_case_dir if present
use_case_dir = use_case_dir.rstrip('/')

# Get number of phases - handle both old and new formats
tasks = config[script_name]
if isinstance(tasks, list):
    # Old format - flat list of phases
    num_phases = len(tasks)
else:
    # New format - structured tasks with labels
    num_phases = len(tasks)

# Create output
print(json.dumps({
    'script_name': script_name,
    'command': command,
    'use_case': use_case,
    'use_case_dir': use_case_dir,
    'num_phases': num_phases,
    'format': 'branching' if not isinstance(tasks, list) else 'sequential'
}))
")

# Exit if Python script reported an error
if [[ $CONFIG_INFO == Error* ]]; then
    echo $CONFIG_INFO
    exit 1
fi

# Parse the JSON output
SCRIPT_NAME=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['script_name'])")
COMMAND=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['command'])")
# Keep original command with spaces for display and symlink
ORIGINAL_COMMAND=$COMMAND
# Replace spaces with underscores for filename (bash scripts can't have spaces)
COMMAND=$(echo $COMMAND | tr ' ' '_')
USE_CASE=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['use_case'])")
USE_CASE_DIR=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['use_case_dir'])")
NUM_PHASES=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['num_phases'])")
FORMAT=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['format'])")

# Verify use case directory exists
if [ ! -d "$USE_CASE_DIR" ]; then
    echo "Error: Use case directory does not exist: $USE_CASE_DIR"
    echo "Please ensure the 'F' variable in the JSON config points to an existing directory."
    exit 1
fi

echo "Setting up workflow for use case '$USE_CASE' with $NUM_PHASES phases..."
echo "Workflow format: $FORMAT"

# Create the wrapper script
WORKFLOW_SCRIPT="$USE_CASE_DIR/$COMMAND.sh"

cat > "$WORKFLOW_SCRIPT" << EOF
#!/bin/bash

# SFA workflow for $USE_CASE
# Generated from $(basename $CONFIG_FILE)

echo "Running $USE_CASE workflow with $NUM_PHASES phases..."

CONFIG_FILE="$CONFIG_FILE"
SCRIPT_DIR="\$(dirname "\$(readlink -f "\$0")")"
PARENT_DIR="\$(dirname "\$(dirname "\$SCRIPT_DIR")")"
BRANCHING_SCRIPT="\$PARENT_DIR/setup-scripts/branching_workflow.sh"

# Run the workflow using the branching workflow script (works for both formats)
exec "\$BRANCHING_SCRIPT" "\$CONFIG_FILE"
EOF

# Make the script executable
chmod +x "$WORKFLOW_SCRIPT"

# Create a symlink to make the command available in user's bin directory
USER_BIN="$HOME/bin"
mkdir -p "$USER_BIN"  # Ensure ~/bin exists

COMMAND_PATH="$USER_BIN/$ORIGINAL_COMMAND"
# Always create or update the symlink, even if it already exists
if ln -sf "$WORKFLOW_SCRIPT" "$COMMAND_PATH" 2>/dev/null; then
    if [ -L "$COMMAND_PATH" ] || [ -e "$COMMAND_PATH" ]; then
        echo "Command '$ORIGINAL_COMMAND' updated and linked to workflow script."
    else
        echo "Command '$ORIGINAL_COMMAND' created and linked to workflow script."
    fi
else
    echo "Note: Could not create/update user bin command."
    echo "To create it manually, run: ln -sf \"$WORKFLOW_SCRIPT\" \"$COMMAND_PATH\""
    echo "You can still run the workflow with: $WORKFLOW_SCRIPT"
fi

# Create README using Claude if anthropic module is available
echo "Generating README.md for $USE_CASE..."
README_PATH="$USE_CASE_DIR/README.md"

if [ -f "$README_PATH" ]; then
    echo "README.md already exists. Skipping generation."
else
    if python3 -c "import anthropic" 2>/dev/null; then
        python3 -c "
import json
import os
import sys
from anthropic import Anthropic

# Load the JSON config
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

# Setup Anthropic client
client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Prepare the prompt
prompt = f'''Generate a README.md file for a Single-File Agent workflow based on this JSON configuration:

\`\`\`json
{json.dumps(config, indent=2)}
\`\`\`

The README should include:
1. Title based on the use case name
2. Overview of what the workflow does
3. List of the phases and what each does
4. Usage instructions (command to run)
5. Expected outputs

Format it as a clean, well-structured markdown document.
'''

# Generate the README using Claude
response = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=1500,
    messages=[{'role': 'user', 'content': prompt}]
)

# Write the README
readme_path = '$README_PATH'
with open(readme_path, 'w') as f:
    f.write(response.content[0].text)

print(f'README.md generated at {readme_path}')
"
    else
        echo "Warning: Cannot generate README.md - anthropic Python module not found."
        echo "To generate README later, install anthropic module: pip install anthropic"
    fi
fi

echo "Setup complete for $USE_CASE workflow."
echo "To run the workflow, use the command: $ORIGINAL_COMMAND"