# Deployment and Setup

This document details the setup and deployment process for Single-File Agents, including setup scripts, command creation, workflow configuration, and environment setup.

## Installation [v1_0_0]

### Prerequisites

- Python 3.9 or higher
- `pip` for package management
- API keys for Anthropic (and optionally for Brave Search and Perplexity)

### Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/single-file-agents.git
   cd single-file-agents
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   BRAVE_API_KEY=your_brave_api_key  # Optional
   X_SUBSCRIPTION_TOKEN=your_brave_subscription_token  # Optional
   PERPLEXITY_API_KEY=your_perplexity_api_key  # Optional
   ```

   See `.example.env` for a template.

## Setup Scripts [v1_0_0, enhanced v3_0_0]

### Main Scripts

The SFA system includes several setup scripts:

1. `setup-scripts/install-sfa-commands.sh`: Sets up the `sfa` command
2. `setup-scripts/migrate-to-new-workflow.sh`: Migrates existing configurations
3. `setup-scripts/sfa_workflow.sh`: Main workflow script used by the `sfa` command

### Command Installation

The `install-sfa-commands.sh` script:
- Creates the `~/bin` directory if it doesn't exist
- Adds it to your PATH if necessary
- Installs the `sfa` command

```bash
#!/bin/bash
# Install SFA command-line tools

# Get the base directory
BASE_DIR="$(dirname "$(readlink -f "$0")")"
WORKFLOW_SCRIPT="$BASE_DIR/sfa_workflow.sh"
BIN_DIR="$HOME/bin"

# Check if the script exists
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow script not found at $WORKFLOW_SCRIPT"
    exit 1
fi

# Make sure workflow script is executable
chmod +x "$WORKFLOW_SCRIPT"

# Create ~/bin if it doesn't exist
if [ ! -d "$BIN_DIR" ]; then
    echo "Creating $BIN_DIR directory..."
    mkdir -p "$BIN_DIR"
fi

# Add ~/bin to PATH if not already
if ! [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo "Adding $BIN_DIR to PATH..."
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.zshrc"
fi

# Create sfa command
SFA_CMD="$BIN_DIR/sfa"
echo "Installing sfa command..."
cat > "$SFA_CMD" << 'EOF'
#!/bin/bash
# SFA - Single-File Agent Command

# Get this script's path
SFA_COMMAND_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
# Get the Development directory (parent of parent of bin)
DEV_DIR="$(dirname "$(dirname "$SFA_COMMAND_PATH")")"
# Path to SFA directory
SFA_DIR="$DEV_DIR/single-file-agents"

# Default path to workflow script
WORKFLOW_SCRIPT="${SFA_DIR}/setup-scripts/sfa_workflow.sh"

# Check if the workflow script exists
if [ ! -f "$WORKFLOW_SCRIPT" ]; then
    echo "Error: Workflow script not found at $WORKFLOW_SCRIPT"
    echo "Please ensure the path is correct or reinstall SFA"
    exit 1
fi

# Show usage if no arguments provided
if [ $# -lt 1 ]; then
    echo "Usage: sfa [options] <config_file.json>"
    echo ""
    echo "Options:"
    echo "  -e, --execute       Only execute the workflow without setup"
    echo "  -r, --readme        Create an additional README_v2.md with detailed documentation"
    echo "  -h, --help          Show this help message"
    exit 1
fi

# Pass all arguments to the workflow script
exec "$WORKFLOW_SCRIPT" "$@"
EOF

chmod +x "$SFA_CMD"

echo "SFA commands installed successfully!"
```

## Workflow Creation [v3_0_0]

### The Main Workflow Script

The `sfa_workflow.sh` script handles both setup and execution:

```bash
#!/bin/bash
# SFA Workflow - Unified script for both setup and execution
# Usage: sfa_workflow.sh [options] <config_file.json>

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
```

### Workflow Configuration Validation

The script validates configuration files:

```bash
# Extract config info using Python
CONFIG_INFO=$(python3 -c "
import json, os, sys
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

# Get command name
command = config.get('A', '')
use_case_dir = config.get('F', '')
if not command or not use_case_dir:
    print('Error: Invalid config file format - missing required A and F variables')
    sys.exit(1)
")
```

### Custom Command Creation

The script creates a custom command for the workflow:

```bash
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
```

## Workflow Execution [v3_0_0]

### Execution Mode

In execution mode, the script processes the workflow:

```bash
# For execution mode, just run the workflow
if [ "$EXECUTE_ONLY" = true ]; then
    echo "Executing workflow directly without setup..."
    
    # Check if reports directory exists
    if [ ! -d "reports" ]; then
        echo "Creating reports directory to store task reports..."
        mkdir -p reports
    fi
    
    # Function to run a specific task
    run_task() {
        local task_index="$1"
        local task_label=$(echo $TASK_LABELS | python3 -c "import json, sys; print(json.loads(sys.stdin.read())[$task_index])")
        
        echo ""
        echo "=================================================="
        echo "Running task: $task_label (index: $task_index)"
        echo "=================================================="
        
        # Run the task
        python3 "$PARENT_DIR/sfa_main.py" --config-file "$CONFIG_FILE" --phase "$task_index"
    }
    
    # Start with the first task
    run_task 0
```

### Branching Workflow Execution [v3_0_0]

The script supports branching based on decision output:

```bash
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
        fi
    }
fi
```

## README Generation [v3_0_0]

The script can generate README files for workflows:

```bash
# Create README using Claude if anthropic module is available
README_PATH="$USE_CASE_DIR/README.md"
DETAILED_README_PATH="$USE_CASE_DIR/README_v2.md"

echo "Generating README.md for $USE_CASE..."

if python3 -c "import anthropic" 2>/dev/null; then
    # If detailed README requested or original doesn't exist, generate README
    if [ "$CREATE_DETAILED_README" = "true" ] || [ ! -f "$README_PATH" ]; then
        TARGET_PATH=$([ "$CREATE_DETAILED_README" = "true" ] && echo "$DETAILED_README_PATH" || echo "$README_PATH")
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
3. List of the tasks/phases and what each does
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
readme_path = '$TARGET_PATH'
with open(readme_path, 'w') as f:
    f.write(response.content[0].text)

print(f'README generated at {readme_path}')
"
    fi
fi
```

## UV Support [v1_0_0]

The SFA is compatible with UV for package management:

```bash
# Run the task
if command -v uv &> /dev/null; then
    uv run "$PARENT_DIR/sfa_main.py" --config-file "$CONFIG_FILE" --phase "$task_index"
else
    python3 "$PARENT_DIR/sfa_main.py" --config-file "$CONFIG_FILE" --phase "$task_index"
fi
```

## Setup Protocol [v2_0_0]

### Standard Setup Protocol

Follow these steps when setting up a new SFA workflow:

1. **Identify Use Case**: Determine what task the agent will perform
2. **Create Use Case Directory**: Create a directory in `use-case/` with a descriptive name
3. **Design Workflow**: Plan the phases and their interactions
4. **Create Configuration**: Create a JSON configuration file with:
   - Command name (A)
   - Use case directory (F)
   - Workflow structure with tasks
   - System messages, instructions, and resources
   - Output paths

5. **Run Setup**: Execute `sfa your-config.json` to set up the workflow
6. **Test Workflow**: Run the created command to verify functionality
7. **Refine Configuration**: Adjust as needed based on testing

### Configuration Example

```json
{
  "A": "research-article",
  "F": "use-case/doc-research/",
  "research": {
    "TASK_INITIAL": [{
      "U": "You are a research assistant specializing in technology trends",
      "X": "Analyze the provided articles and extract key technology trends",
      "Y": ["research-articles/tech-trends-2025.md"],
      "Z": "A summary of key technology trends with evidence from the articles",
      "O": ["output/trends-summary.md"]
    }],
    "TASK_DETAILED": [{
      "U": "You are a technology analyst with expertise in future forecasting",
      "X": "Create a detailed analysis of each identified trend",
      "Y": ["output/trends-summary.md"],
      "Z": "Detailed analysis with forecasts for each trend",
      "O": ["output/detailed-analysis.md"]
    }],
    "TASK_FINAL": [{
      "U": "You are a professional technology writer",
      "X": "Create a polished research article based on the analysis",
      "Y": ["output/detailed-analysis.md"],
      "Z": "Publication-ready article with sections for each trend",
      "O": ["final/tech-trends-article.md"]
    }]
  }
}
```

### Directory Structure Conventions

Use these conventions for organizational clarity:

```
use-case/your-workflow/
├── README.md                    # Auto-generated by setup
├── your-workflow.sh             # Generated command script
├── your-workflow-config.json    # Configuration file
├── research/                    # Input resources
│   └── input-files.md           # Input content
├── output/                      # Intermediate outputs
│   ├── phase1-output.md
│   └── phase2-output.md
└── final/                       # Final outputs
    └── final-output.md
```

## Customization Options [v3_0_0]

### Custom Tools Integration

To add custom tools:

1. Create a Python module in the `tools/` directory
2. Implement the tool function
3. Provide a `get_tool_definition` function
4. The agent will automatically load the tool

Example structure:

```
tools/
├── my_custom_tool.py
└── README.md
```

### Environment Customization

Customize the environment by modifying:

1. `.env` file for API keys and other secrets
2. `setup-scripts/sfa_workflow.sh` for workflow behavior
3. Custom tools for additional capabilities
4. The `sfa_main.py` file for core behavior changes