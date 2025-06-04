#!/bin/bash
# Branching workflow script for SFA
# Usage: branching_workflow.sh <config_file.json>

if [ $# -lt 1 ]; then
    echo "Usage: $0 <config_file.json>"
    exit 1
fi

CONFIG_FILE="$1"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SFA_SCRIPT="${PARENT_DIR}/sfa_main.py"
TOOLS_DIR="${PARENT_DIR}/tools"

# Check for tools directory
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

# Extract task labels and structure using Python
TASKS_INFO=$(python3 -c "
import json, os, sys
import re

# Load the config file
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f'Error: Failed to load config file: {str(e)}')
    sys.exit(1)

# Find the workflow key (first key that's not 'A' or 'F')
workflow_key = next((k for k in config.keys() if k != 'A' and k != 'F'), None)
if not workflow_key:
    print('Error: Invalid config file format - no workflow key found')
    sys.exit(1)

# Extract the tasks
tasks = config[workflow_key]

# Check if this is the new or old format
if isinstance(tasks, list):
    # Old format - flat list of phases
    print(json.dumps({
        'format': 'sequential',
        'workflow_key': workflow_key,
        'num_tasks': len(tasks),
        'task_labels': [f'PHASE_{i}' for i in range(len(tasks))]
    }))
else:
    # New format - structured tasks with labels
    print(json.dumps({
        'format': 'branching',
        'workflow_key': workflow_key,
        'num_tasks': len(tasks),
        'task_labels': list(tasks.keys())
    }))
")

# Check for any errors in the Python output
if [[ $TASKS_INFO == Error* ]]; then
    echo "$TASKS_INFO"
    exit 1
fi

# Parse the JSON output
FORMAT=$(echo $TASKS_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['format'])")
WORKFLOW_KEY=$(echo $TASKS_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['workflow_key'])")
NUM_TASKS=$(echo $TASKS_INFO | python3 -c "import json, sys; print(json.load(sys.stdin)['num_tasks'])")
TASK_LABELS=$(echo $TASKS_INFO | python3 -c "import json, sys; print(json.dumps(json.load(sys.stdin)['task_labels']))")

echo "Workflow format: $FORMAT"
echo "Workflow key: $WORKFLOW_KEY"
echo "Number of tasks: $NUM_TASKS"
echo "Task labels: $(echo $TASK_LABELS | python3 -c "import json, sys; print(', '.join(json.loads(sys.stdin.read())))")"

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
        uv run "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase "$task_index"
    else
        python3 "$SFA_SCRIPT" --config-file "$CONFIG_FILE" --phase "$task_index"
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