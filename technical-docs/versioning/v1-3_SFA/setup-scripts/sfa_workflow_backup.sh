#!/bin/bash
# SFA Workflow - Unified script for both setup and execution
# Usage: sfa_workflow.sh [options] <config_file.json>

# Function to show usage
show_usage() {
    echo "Usage: sfa [options] <config_file.json>"
    echo ""
    echo "Options:"
    echo "  -e, --execute       Only execute the workflow without setup (default: setup and create command)"
    echo "  -r, --readme        Create an additional README_v2.md with detailed workflow documentation"
    echo "  -m, --model         Specify a model for execution"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  sfa config.json            Setup workflow and create command (default)"
    echo "  sfa -e config.json         Execute workflow without setup"
    echo "  sfa -r config.json         Setup workflow and create detailed README"
    exit 1
}

# Default options
EXECUTE_ONLY=false
CREATE_DETAILED_README=false
MODEL=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -e|--execute)
            EXECUTE_ONLY=true
            shift
            ;;
        -r|--readme)
            CREATE_DETAILED_README=true
            shift
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            # If it's not an option, assume it's the config file
            if [[ -z "$CONFIG_FILE" ]]; then
                CONFIG_FILE="$1"
            else
                echo "Error: Unexpected argument: $1"
                show_usage
            fi
            shift
            ;;
    esac
done

# Make sure a config file was provided
if [[ -z "$CONFIG_FILE" ]]; then
    echo "Error: No config file specified"
    show_usage
fi

# Get absolute path of JSON file
if [[ "$CONFIG_FILE" != /* ]]; then
    CONFIG_FILE="$(pwd)/$CONFIG_FILE"
fi

# Make sure the config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="${PARENT_DIR}/tools"

# Check for required tools directory and files
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

# Check for task reporting tool (warning only)
if [ ! -f "$TOOLS_DIR/task_reporting.py" ]; then
    echo "Warning: Task reporting tool not found at $TOOLS_DIR/task_reporting.py"
    echo "Task reporting features will not be available."
fi

# Extract config info using Python
CONFIG_INFO=$(python3 -c "
import json, os, sys
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f'Error: Failed to load config file: {str(e)}')
    sys.exit(1)

# Find the workflow key (first key that's not 'A' or 'F' or 'M')
workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F' and k != 'M'), None)
if not workflow_key:
    print('Error: Invalid config file format - no workflow key found')
    sys.exit(1)

# Get command name
command = config.get('A', '')
use_case_dir = config.get('F', '')
model = config.get('M', '')  # Extract model if present
if not command or not use_case_dir:
    print('Error: Invalid config file format - missing required A and F variables')
    sys.exit(1)

# Get use case name for display
use_case = command.split(' ')[1] if ' ' in command else command

# Remove trailing slash from use_case_dir if present
use_case_dir = use_case_dir.rstrip('/')

# Extract the tasks
tasks = config[workflow_key]

# Check if this is the new or old format
if isinstance(tasks, list):
    # Old format - flat list of phases
    format_type = 'sequential'
    num_tasks = len(tasks)
    task_labels = [f'PHASE_{i}' for i in range(num_tasks)]
else:
    # New format - structured tasks with labels
    format_type = 'branching'
    num_tasks = len(tasks)
    task_labels = list(tasks.keys())

# Create output
print(json.dumps({
    'format': format_type,
    'workflow_key': workflow_key,
    'command': command,
    'use_case': use_case,
    'use_case_dir': use_case_dir,
    'model': model,  # Include model in output
    'num_tasks': num_tasks,
    'task_labels': task_labels
}))
")

# Check for any errors in the Python output
if [[ $CONFIG_INFO == Error* ]]; then
    echo "$CONFIG_INFO"
    exit 1
fi

# Parse the JSON output
FORMAT=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['format'])")
WORKFLOW_KEY=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_key'])")
COMMAND=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['command'])")
USE_CASE=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['use_case'])")
USE_CASE_DIR=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['use_case_dir'])")
NUM_TASKS=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['num_tasks'])")
TASK_LABELS=$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.dumps(json.load(sys.stdin)['task_labels']))")

# Extract model from config
MODEL=${MODEL:-"$(echo $CONFIG_INFO | python3 -c "import json, sys; print(json.load(sys.stdin).get('model', ''))"}"}

# Find agent file
AGENT_FILE=""
for file in $(find "$PARENT_DIR" -maxdepth 1 -name "sfa_v*.py" | sort -V); do
    # If we find an exact match for v3_3_0, use it directly
    if [[ $(basename "$file") == "sfa_v3_3_0_main.py" ]]; then
        AGENT_FILE=$(basename "$file")
        break
    fi
    # Otherwise keep track of the oldest version
    if [ -z "$AGENT_FILE" ]; then
        AGENT_FILE=$(basename "$file")
    fi
done

if [ -z "$AGENT_FILE" ]; then
    echo "Error: No agent file found in project root. Please ensure at least one agent file exists."
    exit 1
fi

echo "Using agent file: $AGENT_FILE"

# Verify use case directory exists
if [ ! -d "$USE_CASE_DIR" ]; then
    echo "Error: Use case directory does not exist: $USE_CASE_DIR"
    echo "Please ensure the 'F' variable in the JSON config points to an existing directory."
    exit 1
fi

echo "Workflow format: $FORMAT"
echo "Workflow key: $WORKFLOW_KEY"
echo "Command name: $COMMAND"
echo "Use case: $USE_CASE"
echo "Number of tasks: $NUM_TASKS"
echo "Task labels: $(echo $TASK_LABELS | python3 -c "import json, sys; print(', '.join(json.loads(sys.stdin.read())))")"

# For execution mode, just run the workflow
if [ "$EXECUTE_ONLY" = true ]; then
    echo "Executing workflow directly without setup..."
    
    # Check if reports directory exists
    if [ ! -d "reports" ]; then
        echo "Creating reports directory to store task reports..."
        mkdir -p reports
    fi
    
    # Function to get task index from label
    get_task_index() {
        local task_label="$1"
        python3 -c "
import json
task_labels = json.loads('$TASK_LABELS')
try:
    print(task_labels.index('$task_label'))
except ValueError:
    print('-1')
"
    }
    
    # Function to run a specific task
    run_task() {
        local task_index="$1"
        local task_label=$(echo $TASK_LABELS | python3 -c "import json, sys; print(json.loads(sys.stdin.read())[$task_index])")
        
        echo ""
        echo "=================================================="
        echo "Running task: $task_label (index: $task_index)"
        echo "=================================================="
        
        # Run the task
        if command -v uv &> /dev/null; then
            if [ -n "$MODEL" ]; then
                echo "Using model: $MODEL"
                uv run "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index" --model "$MODEL"
            else
                uv run "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index"
            fi
        else
            if [ -n "$MODEL" ]; then
                echo "Using model: $MODEL"
                python3 "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index" --model "$MODEL"
            else
                python3 "$PARENT_DIR/$AGENT_FILE" --config-file "$CONFIG_FILE" --phase "$task_index"
            fi
        fi
        
        # Check if task completed successfully
        if [ $? -ne 0 ]; then
            echo "Error: Task $task_label failed"
            exit 1
        fi
        
        echo "Task $task_label completed successfully"
        
        # Check for task report
        local report_file="task_report_phase_${task_index}.json"
        if [ -f "$report_file" ]; then
            echo "Found task report: $report_file"
            
            # Move report to reports directory
            mv "$report_file" "reports/$(basename $report_file)"
            report_file="reports/$(basename $report_file)"
            
            # Check if there's a decision to determine next task
            local has_decision=$(jq 'has("decision")' "$report_file")
            
            if [ "$has_decision" = "true" ]; then
                local decision_choice=$(jq -r '.decision.choice' "$report_file")
                echo "Decision made: $decision_choice"
                
                # Try to find a matching task based on the decision
                local next_task=""
                
                # Look for DECISION_X where X is the choice number or string
                if [[ "$decision_choice" =~ ^[0-9]+$ ]]; then
                    # It's a number
                    next_task="DECISION_${decision_choice}"
                else
                    # It's a string - convert to uppercase with underscores
                    local decision_key=$(echo "$decision_choice" | tr '[:lower:]' '[:upper:]' | tr ' ' '_')
                    next_task="DECISION_${decision_key}"
                fi
                
                echo "Looking for matching task: $next_task"
                
                # Check if this task exists in our configuration
                local next_index=$(get_task_index "$next_task")
                
                if [ "$next_index" != "-1" ]; then
                    echo "Found matching task: $next_task (index: $next_index)"
                    run_task "$next_index"
                    return
                else
                    echo "No exact match found for decision: $next_task"
                    
                    # Try a more flexible search - any task starting with DECISION_
                    local found_decision_task=false
                    
                    for label in $(echo $TASK_LABELS | python3 -c "import json, sys; print(' '.join(json.loads(sys.stdin.read())))"); do
                        if [[ "$label" == DECISION_* ]]; then
                            local label_index=$(get_task_index "$label")
                            echo "Found decision task: $label (index: $label_index)"
                            run_task "$label_index"
                            found_decision_task=true
                            break
                        fi
                    done
                    
                    # If no decision task found, look for REVIEW_TASK
                    if [ "$found_decision_task" = "false" ]; then
                        local review_index=$(get_task_index "REVIEW_TASK")
                        if [ "$review_index" != "-1" ]; then
                            echo "No matching decision task, proceeding to REVIEW_TASK"
                            run_task "$review_index"
                            return
                        fi
                    fi
                fi
            fi
            
            # If no decision or no matching task, check if there's a next task in sequence
            if [ $(($task_index + 1)) -lt $NUM_TASKS ]; then
                local next_index=$(($task_index + 1))
                local next_label=$(echo $TASK_LABELS | python3 -c "import json, sys; print(json.loads(sys.stdin.read())[$next_index])")
                echo "No branching condition matched, continuing to next task: $next_label"
                run_task "$next_index"
            else
                echo "Reached end of workflow sequence."
            fi
        else
            echo "No task report found. Assuming sequential execution."
            
            # Continue to next task in sequence
            if [ $(($task_index + 1)) -lt $NUM_TASKS ]; then
                local next_index=$(($task_index + 1))
                local next_label=$(echo $TASK_LABELS | python3 -c "import json, sys; print(json.loads(sys.stdin.read())[$next_index])")
                echo "Continuing to next task: $next_label"
                run_task "$next_index"
            else
                echo "Reached end of workflow sequence."
            fi
        fi
    }
    
    # Find the first task to run
    if [ "$FORMAT" = "branching" ]; then
        # For branching format, start with the first task labeled TASK_
        for label in $(echo $TASK_LABELS | python3 -c "import json, sys; print(' '.join(json.loads(sys.stdin.read())))"); do
            if [[ "$label" == TASK_* ]]; then
                first_index=$(get_task_index "$label")
                echo "Starting with task: $label (index: $first_index)"
                run_task "$first_index"
                break
            fi
        done
        
        # If no TASK_ label found, start with the first task
        if [ -z "$first_index" ]; then
            echo "No task labeled TASK_* found, starting with first task"
            run_task 0
        fi
    else
        # For sequential format, always start with the first task
        echo "Sequential workflow, starting with first task"
        run_task 0
    fi
    
    echo ""
    echo "Workflow completed successfully!"
    exit 0
fi

# If we're here, we're in setup mode
echo "Setting up workflow for use case '$USE_CASE' with $NUM_TASKS tasks..."

# Create the wrapper script
WORKFLOW_SCRIPT="$USE_CASE_DIR/$COMMAND.sh"

# Extract the first word as the main command
MAIN_COMMAND=$(echo "$COMMAND" | cut -d ' ' -f1)
COMMAND_ARGS=$(echo "$COMMAND" | cut -d ' ' -f2-)

cat > "$WORKFLOW_SCRIPT" << EOF
#!/bin/bash

# SFA workflow for $USE_CASE
# Generated from $(basename $CONFIG_FILE)

# Check if arguments were provided
if [ \$# -eq 0 ]; then
    # No arguments provided, use the default arguments from config
    ARGS="$COMMAND_ARGS"
else
    # Use the provided arguments
    ARGS="\$@"
fi

echo "Running $USE_CASE workflow with args: \$ARGS"

CONFIG_FILE="$CONFIG_FILE"
SCRIPT_DIR="\$(dirname "\$(readlink -f "\$0")")"
PARENT_DIR="\$(dirname "\$(dirname "\$SCRIPT_DIR")")"
SFA_WORKFLOW="\$PARENT_DIR/setup-scripts/sfa_workflow.sh"

# Run the workflow in execute mode
exec "\$SFA_WORKFLOW" -e "\$CONFIG_FILE"
EOF

# Make the script executable
chmod +x "$WORKFLOW_SCRIPT"

# Create a symlink to make the command available in user's bin directory
USER_BIN="$(cd ~ && pwd)/bin"
mkdir -p "$USER_BIN"  # Ensure ~/bin exists

COMMAND_PATH="$USER_BIN/$MAIN_COMMAND"
# Always create or update the symlink, even if it already exists
if ln -sf "$WORKFLOW_SCRIPT" "$COMMAND_PATH" 2>/dev/null; then
    if [ -L "$COMMAND_PATH" ] || [ -e "$COMMAND_PATH" ]; then
        echo "Command '$MAIN_COMMAND' updated and linked to workflow script."
    else
        echo "Command '$MAIN_COMMAND' created and linked to workflow script."
    fi
else
    echo "Note: Could not create/update user bin command."
    echo "To create it manually, run: ln -sf \"$WORKFLOW_SCRIPT\" \"$COMMAND_PATH\""
    echo "You can still run the workflow with: $WORKFLOW_SCRIPT"
fi

# Create README using Claude if anthropic module is available
README_PATH="$USE_CASE_DIR/README.md"
DETAILED_README_PATH="$USE_CASE_DIR/README_v2.md"

echo "Generating README.md for $USE_CASE..."

if [ -f "$README_PATH" ] && [ "$CREATE_DETAILED_README" = "false" ]; then
    echo "README.md already exists. Skipping generation."
    echo "Use -r flag to create a detailed README_v2.md alongside existing README."
else
    if python3 -c "import anthropic" 2>/dev/null; then
        # If detailed README requested or original doesn't exist, generate README
        if [ "$CREATE_DETAILED_README" = "true" ] || [ ! -f "$README_PATH" ]; then
            TARGET_PATH=$([ "$CREATE_DETAILED_README" = "true" ] && echo "$DETAILED_README_PATH" || echo "$README_PATH")
            
            # Create README content using a different approach to avoid bash interpretation issues
cat > /tmp/readme_generator.py << 'PYTHON_SCRIPT_END'
import json
import os
import sys
from anthropic import Anthropic

# Load the JSON config from command line argument
config_file = sys.argv[1]
target_path = sys.argv[2]

with open(config_file, 'r') as f:
    config = json.load(f)

# Setup Anthropic client
client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Prepare the prompt
config_json = json.dumps(config, indent=2)
prompt = f'Generate a README.md file for a Single-File Agent workflow based on this JSON configuration:\n\n```json\n{config_json}\n```\n\nThe README should include:\n1. Title based on the use case name\n2. Overview of what the workflow does\n3. List of the tasks/phases and what each does\n4. Usage instructions (command to run)\n5. Expected outputs\n\nFormat it as a clean, well-structured markdown document.'

# Generate the README using Claude
response = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=1500,
    messages=[{'role': 'user', 'content': prompt}]
)

# Write the README
with open(target_path, 'w') as f:
    f.write(response.content[0].text)

print(f'README generated at {target_path}')
PYTHON_SCRIPT_END

            # Run the Python script
            python3 /tmp/readme_generator.py "$CONFIG_FILE" "$TARGET_PATH"
            
            # Clean up temporary file
            rm /tmp/readme_generator.py
        else
            echo "README.md already exists and no detailed README requested."
        fi
    else
        echo "Warning: Cannot generate README - anthropic Python module not found."
        echo "To generate README later, install anthropic module: pip install anthropic"
    fi
fi

echo "Setup complete for $USE_CASE workflow."
echo "To run the workflow, use the command: $MAIN_COMMAND $COMMAND_ARGS"