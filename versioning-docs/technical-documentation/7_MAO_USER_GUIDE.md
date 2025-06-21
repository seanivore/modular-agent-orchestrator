# Mao Application Usage Guide
*Using the Mao application*

---

## Start Application

```bash
mao mao 
```

- Then just start chatting! No delay, and only one screen. 
- Try `/chat` or `/goal` to jump in quickly 

### Create Workflow From Goal

```bash
mao --goal "create marketing plan for SaaS startup"
```

- App Launches 
- Workflow Created From Goal

### Don't Leave Terminal

```bash
mao --setup ./config.json
```

- Have your JSON config ready 
- Run it with the setup script 


## Two Interfaces

  - The Mao application is our main user interface 
  - Using terminal is possible; consider it a dev or pro tool secondary experience 

**NOTE:** Running workflows will launch the application where a monitor is displayed. 

---

## Terminal Arguments & Command Reference

1. "Standalone" = Nothing needs to follow the flag or slash command 
2. "Text input required"
   - Follow the flag or slash command
   - No quotes are needed 
3. "File input required"
   - Put file path after the flag or slash command
   - Be in that directory or use full path 
4. "App Only" 
   - Use the slash command 
   - Or use the `!` prefix in app 
   - Won't work and isn't needed in terminal 

### Command Chart

| **FUNCTION**           | **TERMINAL COMMAND**          | **IN-APP COMMAND**            |
| ---------------------- | ----------------------------- | ----------------------------- |
| **Start Application**  | `mao mao`                     | -                             |
| **Run Your Workflow**  | `custom command`              | `/custom command`             |
| **Create Workflow ID** | `uid`                         | `/uid` or `! uid`             |
| **Create User ID**     | `meid username`               | `/meid username`              |
| Restart application    | -                             | `/restart` or `! mao restart` |
| Exit application       | -                             | `/exit` or `! mao exit`       |
| Open app config        | `mao --config`                | `/config`                     |
| Resume last workflow   | `mao --continue`              | `/continue`                   |
| First message to AI    | `mao --chat message`          | `/chat message`               |
| Create entire workflow | `mao --goal project goal`     | `/goal project goal`          |
| System Statistics      | `mao --stats`                 | `/stats`                      |
| List Workflows         | `mao --workflows`             | `/workflows`                  |
| Review Workflow        | `mao --review custom command` | `/review custom command`      |
| Setup from JSON        | `mao --setup ./config.json`   | `/setup ./config.json`        |
| Update Workflow        | `mao --update ./phase.json`   | `/update ./phase.json`        |
| Fix Deliverable        | `mao --fix-it ./fix.json`     | `/fix-it ./fix.json`          |
| Set output directory   | `mao --output ~/downloads`    | `/output ~/downloads`         |
| Use only free models   | `mao --free`                  | `/free`                       |
| Privacy models only    | `mao --privacy`               | `/privacy`                    |
| Verbose Debug Mode     | `mao --verbose`               | `/verbose`                    |
| View workflow logs     | `mao --logs`                  | `/logs`                       |
| Show workflow stats    | `mao --stats`                 | `/stats`                      |
| Check Health           | `mao --doctor`                | `/doctor`                     |
| View help messages     | `mao --help`                  | `/help`                       |
| Simulate Workflow      | `mao --dry-run`               | `/dry-run`                    |
| Terminal Commands      | -                             | `! ls -la` (any bash/zsh)     |

### Command Categories

**🚀 Workflow Creation**
- `--goal` / `/goal` - Complete workflow from natural language
- `--chat` / `/chat` - Interactive conversation to build workflow  
- `--setup` / `/setup` - Install workflow from JSON configuration

**📊 System Management**  
- `--stats` / `/stats` - Performance metrics and system status
- `--workflows` / `/workflows` - List all configured workflows
- `--verbose` / `/verbose` - Developer-level debugging information

**🔧 Workflow Control**
- `--update` / `/update` - Add phases to existing workflows
- `--fix-it` / `/fix-it` - Re-run failed workflow phases
- `--output` / `/output` - Override default workspace directories

**💻 In-App Special**
- `/restart` - Restart MAO application
- `/exit` - Exit MAO application  
- `! command` - Execute any terminal command from within MAO

### Important Command Specifics 

1. Reviewing Workflows --> follow flag or slash command with: 
   - The custom command for your workflow brings up that workflow 
   - Using the Unique Workflow ID brings up that workflow 
   - Use your Unique User ID to bring up all of your workflows 

---

## User Experience Flows

### New User Journey
```
1. First Launch → Color Selection → Main Chat Interface
2. Goal Input → Workflow Analysis → JSON Config Generation  
3. Setup JSON Workflow → Execute with Setup Script for Custom Command
4. Workflow Execution → Live Progress Monitoring
5. Results Delivery → Quality Validation → Next Steps
```

### Experienced User Patterns

**Quick Workflow Creation**
```bash
mao --goal "competitor analysis for fintech startup" --output ~/projects
```

**Setting Up Workflow Using Setup Scrip with JSON:**
```bash
mao --setup ./my-workflow.json --verbose
```

### Application Page Design

- **Actual Pages**
  - New user greeting and color selection 
  - Main chat interface (this is the all-purpose page)

- **All Others** 
  - Open as a modal that disappears when complete 
  - Example is the application configuration page 

---

## Setup Script Utility 

**WE NEED THE SETUP SCRIPT CREATED AND THEN THE PATTERN HERE**

1. Creates the entire workflow use-case directory named after your custom command 
2. Also writes a README_my_workflow.md and a use-case specific script 
3. Uses your custom command in the JSON to make the new workflow executable
4. Result: Custom command installed (e.g., `content strategy saas`)

**NOTE:** The setup script does not put hyphens in the command line, only spaces. 
- Use the naming convention of the custom command for your JSON config, too 

---

## Setup Script Usage: Simple & Developer-Friendly

### The Simple Setup Pattern

Mao follows the proven SFA pattern that developers love; one simple command creates executable workflows:

```bash
# Create or get a JSON config
mao --setup ./my-workflow-config.json

# Setup script builds the entire workflow use-case directory 
# Also writes a README_my_workflow.md and a use-case specific script 
# Uses your custom command in the JSON to make the new workflow executable
# Result: Custom command installed (e.g., `content strategy saas`)

# Execute workflow anytime
content strategy saas
```

### Creating JSON Configs

**Option 1: Let Claude Create It**

```bash
mao mao
> "I need a competitor analysis workflow for B2B SaaS"
> [Claude creates config and runs setup automatically]
```

**Option 2: Create Your Own (Developer Pattern)**

```json
{
  "workflow_id": "uid-def-456",
  "custom_command": "competitor analysis saas",
  "goal": "Comprehensive competitor analysis for B2B SaaS tools",
  "phases": [
    {
      "name": "market_research",
      "description": "Research competitive landscape",
      "tools": ["web_search", "text_editor"],
      "deliverable": "Competitor analysis report",
      "model": "claude-sonnet-4"
    }
  ],
  "variables": {
    "required": {
      "product_category": {
        "description": "SaaS product category to analyze",
        "example": "project management"
      }
    }
  }
}
```

### Command Execution Patterns

**Direct Execution**

```bash
competitor analysis saas
```
1. Run the command directly in terminal 
2. App will open and show the monitor and workflow 
3. Workflow will run and complete 
4. App will close and return to terminal 

**In-app execution**

```bash
mao mao
/competitor analysis saas
```

1. Start the app 
2. Use a slash command placing your command after it 
3. Workflow will run and complete 
4. App will close and return to terminal 

**Workflow Management**

```bash
# List all installed workflows in order of creation 
mao --workflows

# View workflow details using custom command as ID 
mao --review competitor analysis saas

# Update existing workflow; typically for Mao to add new phases 
mao --update ./updated-config.json
```

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

### Advanced Setup Patterns

**Batch Setup**

```bash
# Setup multiple workflows
for config in ./workflow-configs/*.json; do
    mao --setup "$config"
done
```

**Environment-Specific Configs**

```bash
# Development setup
mao --setup ./workflows/dev/content-strategy.json

# Production setup  
mao --setup ./workflows/prod/content-strategy.json
```

**Custom Workspace Directory**

```bash
# Specify workspace location
mao --setup ./config.json --output ~/my-projects/workflows
```

### Troubleshooting Setup

**Common Issues**

1. **Command Not Found**

   ```bash
   # Check if command installed
   which my-custom-command

   # Verify /usr/local/bin is in PATH
   echo $PATH | grep /usr/local/bin

   # Re-run setup if needed
   mao --setup ./config.json
   ```

2. **Permission Issues**

   ```bash
   # Make sure you have sudo access for /usr/local/bin
   sudo chmod +x /usr/local/bin/my-command

   # Or use ~/bin instead (update setup script)
   mkdir -p ~/bin
   # Add to ~/.bashrc: export PATH="$HOME/bin:$PATH"
   ```

3. **JSON Validation**

   ```bash
   # Validate JSON syntax
   python -m json.tool my-config.json

   # Check required fields
   jq '.workflow_id, .custom_command, .phases' my-config.json
   ```

### Debug Mode

```bash
# Verbose setup output
mao --setup ./config.json --verbose

# Check setup script directly
bash -x scripts/setup_workflow.sh ./config.json
```

### Why This Approach Works

✅ **Simple**: One command creates executable workflows  
✅ **Familiar**: Follows proven Unix patterns developers know  
✅ **Flexible**: JSON configs are human-readable and editable  
✅ **Portable**: Share configs easily across teams and environments  
✅ **No Lock-in**: Standard JSON and shell scripts, no proprietary formats  
✅ **Discoverable**: `which my-command` shows exactly what's installed

---

## Complete Workflow Experience

### Unique Workflow ID Generation 

1. If you're creating the JSON yourself, you'll need to generate the UID for one of the variables 
2. If you're working with Mao to create the workflow, Mao will generate the UID for you 

**To Generate An Always Unique ID** 

```bash 
uid     # That's literally it. Just run that tiny command. 
``` 

### Setting Up A New Project's Workflow

1. **Application Launch**: User runs `mao mao` and MAO application launches
2. **First-Time Setup**: New users choose text color and highlight color for their terminal or colorblind mode 
3. **Main Interface**: Chat interface with simple directions: "Describe your project or ask Claude to guide you"
4. **Visual Progress**: Icons below title indicate necessary variables, changing color when provided
5. **Natural Conversation**: Claude adapts to user experience level; users can provide just a goal or full JSON config
6. **Workflow Unique ID**: Claude generates a unique ID for the workflow, their memory, etc.  
7. **Workflow Planning**: Claude steps away to plan workflow solutions, considering multiple draft options
8. **User Confirmation**: Claude presents workflow with cost/time estimates for user review and refinement
9. **Setup Script Execution**: Claude creates custom command, USE_CASE_README.md, and unique workflow ID
10. **Memory System**: Workflow context saved with unique ID for later activation
11. **Handoff Complete**: User receives custom command and workflow directory path

### Activating A Project's Workflow

**Activation Options:**

- Run custom command directly in terminal
- Start application with `mao mao` and use chat
- Use `! custom command` within application
- Run `/workflows` to select from all workflows
- Start with `mao --workflows` for workflow selection screen

**Activation Process:**

1. **Context Retrieval**: Claude pulls workflow memory and logs using unique ID
2. **Agent Preparation**: Creates button snippets for tools and callbacks
3. **Material Handoff**: Provides agents with deliverables, token limits, auto-save reminders
4. **Live Monitoring**: Real-time UI tracking with audio notifications
5. **Agent Coordination**: Direct communication between agents and orchestrator Claude

### Agent Task Execution

**Agent Environment**

- Live token counter during work
- Button snippets for each tool
- Direct Claude callback for help
- Auto-save document tools
- Parallel execution support

**Orchestrator Coordination:**

- Claude reviews deliverables for completeness
- Plans next tasks based on results
- Creates addendum configs for workflow updates
- Handles three scenarios:
  - **Planned Next Task**: Continue as designed
  - **Adaptive Planning**: Create new phases with `mao --update`
  - **Quality Issues**: Re-run phases with `mao --fix-it`
  - **Workflow Completion**: Final deliverable organization

### Custom Command Patterns

**Command Structure**: Always spaces, never hyphens
```bash
# Correct patterns:
blog content strategy startup
market research fintech
competitor analysis saas tool

# Generated as executables in /Users/seanivore/bin/
```
---

## Advanced Configuration

### Memory MCP Integration
**Status**: 🚧 **[TBD - Implementation Plan 1.2]**

**Specification**: Persistent workflow state across sessions using Memory MCP for entity-based project tracking.

**Future Documentation**:
- Session recovery and continuation
- Workflow state persistence
- Project entity management
- Cross-session context retrieval

### Files API Workflow Handoffs
**Status**: 🚧 **[TBD - Implementation Plan 1.2]**

**Specification**: Agent-to-agent communication via Anthropic Files API for seamless workflow progression.

**Future Documentation**:
- Agent handoff packages
- Workflow continuity mechanisms
- File-based state management
- Multi-phase execution coordination

---

## Usage Notes 

### Goal vs Chat Distinction

- **Goal**: "Here's my entire project, create a workflow"
- **Chat**: "First message to AI for interactive building"

### Workflow Identification

- **Primary ID**: Custom command name (more foolproof than workflow names)
- **Lookup**: Use custom command for workflow details and status

### Application vs Monitoring

MAO is a **full interactive application platform**, not a monitoring utility. 

- Rich chat interfaces for natural workflow creation
- Live workflow monitoring with real-time progress
- Settings management and user preferences
- Professional application experience rivaling Claude Code

---

### Conversational Tool Integration

**Mao Chat Tool Access**: During conversation, Mao has seamless access to all available tools for enhanced responses.

**Architecture**:
```python
# interfaces/terminal/conversation_interface.py
class ConversationInterface:
    def __init__(self):
        self.tool_manager = ToolManager()
        self.available_tools = self.tool_manager.get_all_tools()
        
    async def process_user_message(self, message: str):
        # Analyze if tools needed for better response
        tool_requirements = self._analyze_tool_needs(message)
        
        if tool_requirements:
            # Execute tools transparently 
            tool_results = await self._execute_tools(tool_requirements)
            response = self._generate_enhanced_response(message, tool_results)
        else:
            response = self._generate_standard_response(message)
            
        return response
    
    def _analyze_tool_needs(self, message: str):
        """Detect when fresh info, file ops, or other tools would improve response"""
        if self._needs_current_info(message):
            return ["web_search"]
        elif self._references_files(message):
            return ["file_operations"] 
        # etc.
```

#### User Experience

- Transparent tool usage: User asks questions, Mao automatically uses tools when helpful
- Fresh information: Mao detects when current data would improve responses
- Familiar UX: Same experience users expect from Claude web interface or Claude Code
- No workflow overhead: Tools used conversationally, not as formal workflow steps

#### Integration Points

- Uses existing Tool Integration Framework
- Leverages button snippet system for tool execution
- Integrates with conversation interface for seamless UX
- Maintains tool tracking via Memory MCP integration


---

*MAO provides a complete workflow orchestration experience that adapts to your working style - from casual conversation to professional development workflows. The setup script system gives you the best of both worlds: simple automation when you want it, complete control when you need it.*