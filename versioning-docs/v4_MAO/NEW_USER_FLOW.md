# UI/UX: Creating a Workflow as a New User 

## Getting Started 

You have a use-case to create a workflow for. Start the Mao application. 
  - By default Mao launches with the last session user's settings 
  - If that isn't you, you can launch with `--login` to choose a new User ID 
  - If you've never used Mao before, you'll need to login and choose a couple settings 

```bash
mao mao # Launches the Mao application 
mao --login # Launches the login screen 
``` 

## Usernames versus User ID 

- A username is for UX; it is what they type into the login screen 
- A user ID is what is created from the username 
- Every time a specific username is used the same user ID populates  
- The user ID connects all the workflows, use-cases, and other data for that user 
- The custom User ID is created by a simple script that can also be run manually as a cli-command 

### User ID Creation 

```bash
meid seanivore # Run command with the Username  
user-1642 # Response is that Username's User ID  
```

#### Forget Your Username? 

```bash
whoami # Run command with nothing else
> seanivore # Response is the username of the logged in user 
```

#### Meid Whoami Help 

```bash
> meid 
meid - Generate user IDs from usernames

Usage:
  meid username       Generate user ID for username
  meid -e username    Generate user ID with explanation
  meid -h             Show this help

Examples:
  meid seanivore      # user-1642
  meid -e alice       # user-1161 | Steps: 5 chars -> ...

Mathematical Operations:
  Uses character count, doubled count, and ASCII values
  Applies fibonacci, golden ratio, spiral, mirror, karmic operations
  Same username always produces the same user ID
```

### New User ID Application Background Setup 

- The application will create a new `user_username.json` file 
- "username" in the filename is the username: `user_seanivore.json`
- This JSON is saved in the `configs/user` directory 
- All user settings are saved to this JSON file 
- Initial settings are set to default 
- Even default settings are recorded on this JSON file
- This ensures then when the app pulls up the JSON settings, it will show their actual settings regardless of them being default or not 

#### User ID Application Session Startup 

- The application will load User ID's settings on subsequent launches 
- The application will allow users to adjust these settings at any time using `/config` or launching with `mao --config` which updates their `user_username.json` file 

#### User ID & Workflow JSON Configs 

- New Workflows created by this User ID are not recorded to the User ID JSON file 
- However, all Workflow JSON's have a User ID field, which is how they can be searched for by the application 

### Login Screen 

*App UI/UX* 
  - A minimalistic screen loads 
  - The welcome message persists throughout new user setup pages 
  - Most lines are bulleted; all bullets have large 3 space indent 
  - Priority visibility messages have no bullet or indent 
  - The `>` prompt is a visual indicator of the user's input 
  - The `●` is a primary message context from Mao 
  - Branched down `└` is a secondary context of the parent message 
  - Active help messages are `?` under the text input field 

```ui_login_id
╭─────────────────────────────╮
│ ~(=^‥^)  Mao welcomes you!  │
╰─────────────────────────────╯

●   What is your name?
    └ Please enter User ID to continue 

╭────────────────────────────────────────────────────────╮
│ >                                                      │
╰────────────────────────────────────────────────────────╯
  ? 6-20 alpha-numeric characters
```

### Theme Selection 

*App UI/UX* 
  - This is **NOT** a new screen
  - The users message enters the conversation thread 
  - The messages above the user's message disappear 
  - Then new messages below the user's message appear 
  - **NOTE** if the User ID was recognized, the theme selection would not be shown 
  - The user's message is `>   seanivore` is always a faded gray text 
  - Any 3rd level context below a secondary `└` context, is also faded gray text 
  - 3rd level context is help text, much like the `?` under the text input field 
  - The `❯` is the user's input; move with up and down arrows and enter to select, this is intuitive and needs no explanation 
  - The `✔` is the user's selected input; it is a visual indicator of the user's selection 
  - The `1`, `2`, `3`, etc. are the options the user can select from 
  - The `Preview` is a visual representation of the user's selection; what they can expect to see from their selection 

```ui_login_theme
╭─────────────────────────────╮
│ ~(=^‥^)  Mao welcomes you!  │
╰─────────────────────────────╯

>   seanivore

●   Mao, seanivore! This is your first time here.
    └ Just a couple setup steps? 

●   We won't ask you again, mao. 
    └ We'll save your settings to your User ID. 
      Change this later with /config 

Which text style looks best on your screen?

   1. Dark mode
   2. Light mode
 ❯ 3. Dark mode (colorblind-friendly)✔
   1. Light mode (colorblind-friendly)
   2. Dark mode (ANSI colors only)
   3. Light mode (ANSI colors only)


 Preview
 ╭───────────────────────────────────────────────────╮
 │   1   standard ~(=^‥^) {                          │
 │   2 -    removed text ("Bye, mao.");              │
 │   2 +    updated text ("Mao!");                   │
 │   3   }                                           │
 ╰───────────────────────────────────────────────────╯
```

### Primary Workspace Page 

*App UI/UX* 
  - This is a new screen 
  - This is the primary workspace page where everything happens
  - Things like "Mao is ready to help!" can be prepared with many different messages to cycle through
  - The tips "Describe your workflow", "Ask a question", and "Share your goal" are all tips that can be prepared with many different messages to cycle through 
  - The /help option shows all of the available commands 
  - The /config option shows all of the current settings, which are still set to default 
  - The `>` bullet is a canned app message; same bullet as User messages, same color text  
  - The "Try" message has many different messages that cycle each time they see this screen

```
╭───────────────────────────────────────────────────╮
│ ~(=^‥^)  Mao is ready to help!                    │
│   user: seanivore                                 │
╰───────────────────────────────────────────────────╯


>   Say "hello" to Mao.
    ├ Describe your workflow 
    ├ Ask a question 
    └ Share your goal 
 

╭───────────────────────────────────────────────────╮
│ > Try "how do we start building?"                 │
╰───────────────────────────────────────────────────╯
  ? /help for help, /config for your current setup
```


### Application Configuration Settings 

*App UI/UX* 
  - Users are prompted to adjust configuration settings on their first launch 
  - Settings are saved to the `user_username.json` file in the `configs/user` directory 
  - Users can adjust these settings at any time using `/config` or launching with `mao --config` 

| **SETTING Name**         | **HOVER DISPLAYED DESCRIPTION**                    | **DEFAULT**        |
| ------------------------ | -------------------------------------------------- | ------------------ |
| Quick launch             | Launch the application with the last used settings | `true`             |
| Default model            | The default model to use for the workflow          | `claude-sonnet-4`  |
| Default provider         | The default provider to use for the workflow       | `anthropic direct` |
| Default output directory | The default output directory for the workflow      |
| Default tools            | The default tools to use for the workflow          |


### The Setup Script

1. Create a new directory in the `configs/use_case` directory 
2. Create a new JSON config file in the new directory 
3. Create a new setup script in the new directory 
4. Create a new README.md file in the new directory 
5. Create a new deliverables directory in the new directory 

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
  - Using Mao app, ; it will always generate the same User ID 
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
