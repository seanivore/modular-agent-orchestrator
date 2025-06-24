# Setting Up A New Workflow Use-Case 

## Intention 
Let's make the `7_MAO_USER_GUIDE.md` document more complete and clear by setting it up as an example use-case creating a workflow from start to finish. 

## Updates And Where To Put Them 
1. User ID and Workflow ID
   - Created a new cli JSONs 
   - Created a template JSON in the examples directory here `./configs/examples/cli_command.json` 
   - Both need to be added to tech docs where appropriate
   - Add to UI doc if needed; cache, error handling, etc.? 
2. Update JSON on `7_MAO_USER_GUIDE.md` after it is finalized below 
   - Anywhere else it needs to go 
   - Should be cached? 
   - Error handling probably right? 
   - UI doc? 
3. Setup Script produced workflow use-case directory structure 
   - I've updated it below 
   - Already updated on `7_MAO_USER_GUIDE.md` 
   - Update anywhere else it needs to go 
   - Add to any of the other important files 
   - Document that if they want drafts or other docs it needs to say so in deliverables 
4. Setup Script found on `3_MAO_ARCHITECTURE.md` 
   - Not sure at all if it is accurate
   - Pull from working SFA scripts 
   - the first is to setup the setup script itself 
   - the second creates a new script for a workflow in the directory and makes it executable 
   - `versioning-docs/v1-3_SFA/setup-scripts/install-sfa-commands.sh`
   - `versioning-docs/v1-3_SFA/setup-scripts/sfa_workflow.sh`


## User ID and Workflow ID 

**User ID**
  - Using Mao app, use a 6-20 alpha-numeric username; it will always generate the same User ID 
  - Every JSON object you create will need this same generated number 
  - Run the `meid` command with your Username to get your User ID
  - Keeps all of the use-cases you've created and each workflow you've ran together and easy to look up 
  - Always results in the same 'user-0000' --> the examples below is `user-0663` 
  - Run the --workflow command followed by your User ID to see all of your workflows 

```bash 
meid whoami 
mao --workflow whoami 
```
```zsh
> /meid whoami
> /workflow whoami 
```

**Workflow ID**
  - When you create a workflow alone or with Mao's help, the JSON object will need a workflow ID 
  - Run the `uid` command to get a collision-free (never repeated) unique ID --> `uid-abc-000` 
  - Follow --workflow command with this ID for that workflow's details; custom command might be easier to remember 

```bash 
uid 
mao --workflow uid-abc-000
```
```zsh
> /uid 
> /workflow uid-abc-000 
```

## New, Old JSON Config File Needs 

1. User ID 
2. Workflow ID 
3. Model, fallback model, fail-safe model 
4. Provider, fallback provider, fail-safe provider 
5. Deliverable 
6. Resources (paths, URLs, etc.)
7. custom command 
8. goal 
9. phase_name
10. description (is usually pretty long)
11. tools

### JSON Questions Remaining 

1. What about when a phase has agents working in parallel? 

### JSON Config Schemas


```json
{
  "workflow": [
    {
      "user_id": "user-0663",
      "workflow_id": "uid-qmt-465",
      "custom_command": "marketing strategy startup",
      "workflow_directory": "./configs/workflows/marketing-strategy-startup/",
      "workflow_goal": "Create comprehensive marketing strategy for my fintech startup",
      "workflow_deliverable": "Marketing strategy report",
      "workflow_description": "Identify what is needed to complete the goal. Build a workflow that delegates the work to the appropriate agents, having them work in parallel if needed. Leave the last phase opened-ended. Detail that handoff before the last phase with a list of questions Orchestrator will use to assess if the deliverable is complete, and if not, what is needed to complete it."
    }
  ]
}
```

```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01",
      "phase_name": "market_research",
      "phase_goal": "Do research, create report",
      "phase_deliverable": "Market research report",
      "phase_description": "Research target market. Explore demographics in all socioeconomic status ranges, all geo-locations, all education level, but only females, married, and with a birthday coming up in the next 5 months. Research competitors; detail their marketing strategy.",
      "resources":[
        "./directory/folder/file.md",
        "https://file.com/folder"
      ],
      "tools": ["web_search", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-sonnet-3.7",
      "model_3": "claude-sonnet-3.5",
      "provider_1": "requesty",
      "provider_2": "anthropic direct",
      "provider_3": "anthropic direct"
    }
  ]
}
```

```json
{
  "handoff": [
    {
      "workflow_id": "uid-qmt-465",
      "handoff_number": "01",
      "assessment_questions": [
        "How can I assess if this deliverable is complete?",
        "What is needed to complete that assessment?",
        "Do I have what I need to complete the assessment?"
      ],
      "human_in_loop": "no"
    }
  ]
}
```
### Questions About JSON Object 

1. What does it look like when... 
   - Mao leaves the workflows next phase open-ended? 

2. Do we need to create JSON objects for the two workflow adjustment situations? 
   - Update Workflow to fill in a TBD 
   - Update workflow to cancel a TBD
   - Fix-it Workflow to have deliverables recreated 
3. Where does the output directory go if it is manipulated by a command? 
4. What about verbose, stats, dry-run? 

## Setup Script 

### Generated Workflow Use-Case Directory Structure 

### Workflow Directory Structure

The setup script creates the following directory structure for your workflow use-case. Note that the same naming structure of the custom command is also the name of the directory, appended to your README.md, added to the config.json file, and used in the setup script. 

It is important to remember that the drafting documents used in the workflow are kept in the Files API and not passed along with the deliverables. If you need them, you need to indicate them as one of the deliverables. 

```
configs/use_case/competitor-analysis-saas/
├── competitor_analysis_saas_config.json     # Original configuration; this is the JSON config file 
├── README_competitor_analysis_saas.md       # Auto-generated usage guide
├── competitor_analysis_saas.sh              # Auto-generated use-case specific script that your command activates 
├── metadata/                                # Workflow tracking details  
└── deliverables/                            # Final outputs; this is where the deliverables are stored 
    └── competitor_analysis_report.md        # This is the final deliverable; it is the report 
```

### Script Draft or Real? Why does it say "ONE" -- change path to `./scripts/setup_workflow/setup_workflow.sh`

**ONE Setup Script** 
- `scripts/setup_workflow.sh`

```bash
#!/bin/bash
# MAO Workflow Setup Script
# Processes any JSON config and creates executable commands

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Parse JSON config
WORKFLOW_ID=$(jq -r '.workflow_id' "$CONFIG_FILE")
COMMAND_NAME=$(jq -r '.custom_command' "$CONFIG_FILE")
COMMAND_FILE="${COMMAND_NAME// /-}"  # Replace spaces with hyphens for filesystem

echo "🚀 Setting up MAO workflow: $COMMAND_NAME"

# Create use-case directory
USE_CASE_DIR="configs/use_case/${COMMAND_FILE}"
mkdir -p "$USE_CASE_DIR"
cp "$CONFIG_FILE" "$USE_CASE_DIR/config.json"

# Generate executable command
cat > "/usr/local/bin/${COMMAND_FILE}" << EOF
#!/usr/bin/env python3
"""
MAO Custom Command: $COMMAND_NAME
Workflow ID: $WORKFLOW_ID
"""

import sys
import os

# Add MAO to path
sys.path.insert(0, "$(pwd)")

from orchestrator.core import WorkflowOrchestrator
import json

def main():
    config_path = "$USE_CASE_DIR/config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    orchestrator = WorkflowOrchestrator()
    orchestrator.execute_workflow_from_config(config)

if __name__ == "__main__":
    main()
EOF

# Make executable
chmod +x "/usr/local/bin/${COMMAND_FILE}"

echo "✅ Custom command installed: $COMMAND_NAME"
echo "📁 Use-case directory: $USE_CASE_DIR"
echo "🧪 Test: which ${COMMAND_FILE}"
echo "🚀 Ready: ${COMMAND_FILE}"
```
