# Mao Application Usage Guide
*Using the Mao application*

---

## Get Started 

**Start Application**

```bash
mao mao 
```

- Then just start chatting! No delay, and only one screen. 
- Try `/chat` or `/goal` to jump in quickly 

**Jump In** 

- App Launches 
- Workflow Created From Goal

```bash
mao --goal "create marketing plan for SaaS startup"
```

**Don't Leave Terminal** 

- Have your JSON config ready 
- Run it with the setup script 

```bash
mao --setup ./config.json
```

### **Two Interfaces** 

  - The Mao application is our main user interface 
  - Using terminal is possible; consider it a dev or pro tool secondary experience 

**NOTE:** Running workflows will launch the application where a monitor is displayed. 

---

## Command Reference

1. No input required 
2. Text input required
   - Follow the flag or slash command
   - No quotes are needed 
3. 


For flags or commands that need text input, quotes are not required. 
Want to change directories or check the git status while in the app? Put an `!` in front of your command. 


| **FUNCTION**           | **TERMINAL COMMAND**          | **IN-APP COMMAND**            |
| ---------------------- | ----------------------------- | ----------------------------- |
| **Start Application**  | `mao mao`                     | -                             |
| **Run Your Workflow**  | `custom command`              | `/custom command`             |
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

### **Command Categories**

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

---

## 🎬 **User Experience Flows**

### **New User Journey**
```
1. First Launch → Color Selection → Main Chat Interface
2. Goal Input → Workflow Analysis → JSON Config Generation  
3. Setup Script Creation → Custom Command Installation
4. Workflow Execution → Live Progress Monitoring
5. Results Delivery → Quality Validation → Next Steps
```

### **Experienced User Patterns**

**Quick Workflow:**
```bash
mao --goal "competitor analysis for fintech startup" --output ~/projects
```

**Command-Line Efficiency:**
```bash
mao --setup ./my-workflow.json --verbose
```

### **Application Page Design** 

- **Actual Pages**
  - New user greeting and color selection 
  - Main chat interface (this is the all-purpose page)

- **All Others** 
  - Open as a modal that disappears when complete 
  - Example is the application configuration page 

---

## 🚀 **Setup Script Usage: Simple & Developer-Friendly**

### **The Simple Setup Pattern**

Mao follows the proven SFA pattern that developers love - one simple command creates executable workflows:

```bash
# Create or get a JSON config
mao --setup ./my-workflow-config.json

# Setup script creates custom command
# Result: Custom command installed (e.g., `content-strategy-saas`)

# Execute workflow anytime
content-strategy-saas
```

### **Creating JSON Configs**

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

**Option 3: Copy and Modify Existing Configs**
```bash
# Browse existing workflows
ls configs/use_case/

# Copy and modify
cp configs/use_case/marketing-strategy-startup/config.json ./my-workflow.json
# Edit my-workflow.json
mao --setup ./my-workflow.json
```

### **Command Execution Patterns**

**Direct Execution (Most Common)**:
```bash
# Run the custom command directly  
competitor-analysis-saas

# With arguments (if config defines them)
competitor-analysis-saas --product_category "customer support tools"
```

**Via Mao Orchestrator**:
```bash
# Run through mao (same result)
mao competitor-analysis-saas

# In-app execution
mao mao
> /run competitor-analysis-saas
> ! competitor-analysis-saas
```

**Workflow Management**:
```bash
# List all installed workflows
mao --workflows

# View workflow details  
mao --review competitor-analysis-saas

# Update existing workflow
mao --update ./updated-config.json
```

### **Workflow Directory Structure**

After setup, each workflow gets organized structure:

```
configs/use_case/competitor-analysis-saas/
├── config.json                    # Original configuration
├── README.md                      # Auto-generated usage guide
├── phases/                        # Phase working directories
│   └── 1_market_research/         # Phase 1 materials
└── deliverables/                  # Final outputs
    └── competitor_analysis_report.md
```

**Working Directory (During Execution)**:
```
~/mao_workflows/competitor-analysis-saas/
├── 1_market_research/             # Phase execution
├── 2_analysis_synthesis/
├── DELIVERABLES/                  # Final outputs  
├── METADATA/                      # Workflow tracking
├── README_competitor_analysis_saas.md
└── WORKFLOW_REPORT_competitor_analysis_saas.json
```

### **Configuration Management**

**Updating Workflows**:
```bash
# Edit the config
vim configs/use_case/competitor-analysis-saas/config.json

# Re-run setup to update command
mao --setup configs/use_case/competitor-analysis-saas/config.json
```

**Sharing Workflows**:
```bash
# Package for sharing
tar -czf marketing-workflow.tar.gz configs/use_case/marketing-strategy-startup/

# Install shared workflow
tar -xzf shared-workflow.tar.gz
mao --setup configs/use_case/shared-workflow/config.json
```

**Version Control**:
```bash
# Configs are git-friendly
git add configs/use_case/my-workflow/
git commit -m "Add competitor analysis workflow"

# Share via git
git push origin main
```

### **Advanced Setup Patterns**

**Batch Setup**:
```bash
# Setup multiple workflows
for config in ./workflow-configs/*.json; do
    mao --setup "$config"
done
```

**Environment-Specific Configs**:
```bash
# Development setup
mao --setup ./workflows/dev/content-strategy.json

# Production setup  
mao --setup ./workflows/prod/content-strategy.json
```

**Custom Workspace Directory**:
```bash
# Specify workspace location
mao --setup ./config.json --output ~/my-projects/workflows
```

### **Troubleshooting Setup**

**Common Issues**:

1. **Command Not Found**:
```bash
# Check if command installed
which my-custom-command

# Verify /usr/local/bin is in PATH
echo $PATH | grep /usr/local/bin

# Re-run setup if needed
mao --setup ./config.json
```

2. **Permission Issues**:
```bash
# Make sure you have sudo access for /usr/local/bin
sudo chmod +x /usr/local/bin/my-command

# Or use ~/bin instead (update setup script)
mkdir -p ~/bin
# Add to ~/.bashrc: export PATH="$HOME/bin:$PATH"
```

3. **JSON Validation**:
```bash
# Validate JSON syntax
python -m json.tool my-config.json

# Check required fields
jq '.workflow_id, .custom_command, .phases' my-config.json
```

**Debug Mode**:
```bash
# Verbose setup output
mao --setup ./config.json --verbose

# Check setup script directly
bash -x scripts/setup_workflow.sh ./config.json
```

### **Why This Approach Works**

✅ **Simple**: One command creates executable workflows  
✅ **Familiar**: Follows proven Unix patterns developers know  
✅ **Flexible**: JSON configs are human-readable and editable  
✅ **Portable**: Share configs easily across teams and environments  
✅ **No Lock-in**: Standard JSON and shell scripts, no proprietary formats  
✅ **Discoverable**: `which my-command` shows exactly what's installed

**Setup scripts aren't complex - they're the elegant solution that gives you exactly what you need with zero fuss.** 🚀

---

## 🎬 **Complete Workflow Experience**

### **Setting Up A New Project's Workflow**

1. **Application Launch**: User runs `mao mao` and MAO application launches
2. **First-Time Setup**: New users choose text color and highlight color (like Claude Code)
3. **Main Interface**: Chat interface with simple directions: "Describe your project or ask Claude to guide you"
4. **Visual Progress**: Icons below title indicate necessary variables, changing color when provided
5. **Natural Conversation**: Claude adapts to user experience level - users can provide just a goal or full JSON config
6. **Workflow Planning**: Claude steps away to plan workflow solutions, considering multiple draft options
7. **User Confirmation**: Claude presents workflow with cost/time estimates for user review and refinement
8. **Setup Script Execution**: Claude creates custom command, USE_CASE_README.md, and unique workflow ID
9. **Memory System**: Workflow context saved with unique ID for later activation
10. **Handoff Complete**: User receives custom command and workflow directory path

### **Activating A Project's Workflow**

**Activation Options:**
- Run custom command directly in terminal
- Start application with `mao mao` and use chat
- Use `!custom-command` within application
- Run `/workflows` to select from all workflows
- Start with `mao --workflows` for workflow selection screen

**Activation Process:**
1. **Context Retrieval**: Claude pulls workflow memory and logs using unique ID
2. **Agent Preparation**: Creates button snippets for tools and callbacks
3. **Material Handoff**: Provides agents with deliverables, token limits, auto-save reminders
4. **Live Monitoring**: Real-time UI tracking with audio notifications
5. **Agent Coordination**: Direct communication between agents and orchestrator Claude

### **Agent Task Execution**

**Agent Environment:**
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

### **Custom Command Patterns**

**Command Structure**: Always spaces, never hyphens
```bash
# Correct patterns:
blog content strategy startup
market research fintech
competitor analysis saas tool

# Generated as executables in /usr/local/bin/
```

**Directory Organization**:
```
configs/use_case/blog-content-strategy-startup/
├── config.json
├── USE_CASE_README.md
├── setup_script.sh
├── WORKFLOW_PT_2_README.md (if updated)
└── deliverables/
```

### **Memory & State Management**

**Workflow Memory Files**:
- `memory_[unique_id].py` - Complete workflow context
- `Workflow Log` - Phase progression and decisions
- Files API integration for agent handoffs
- Session recovery using unique workflow IDs

**Quality Assurance Process**:
- Deliverable completeness review
- Human-in-the-loop checkpoints
- Auto-improvement feedback loops
- Performance metrics tracking

---

## 🎯 **Quality Framework Integration**  
**Status**: 🚧 **[TBD - Implementation Plan 1.4]**

**Specification**: Automated quality validation with success criteria and improvement loops.

**Future Documentation**:
- Success criteria validation
- Quality scoring system
- Auto-improvement workflow triggers
- Performance metrics tracking

---

## 🔧 **Advanced Configuration**

### **Memory MCP Integration**
**Status**: 🚧 **[TBD - Implementation Plan 1.2]**

**Specification**: Persistent workflow state across sessions using Memory MCP for entity-based project tracking.

**Future Documentation**:
- Session recovery and continuation
- Workflow state persistence
- Project entity management
- Cross-session context retrieval

### **Files API Workflow Handoffs**
**Status**: 🚧 **[TBD - Implementation Plan 1.2]**

**Specification**: Agent-to-agent communication via Anthropic Files API for seamless workflow progression.

**Future Documentation**:
- Agent handoff packages
- Workflow continuity mechanisms
- File-based state management
- Multi-phase execution coordination

---

## 🚨 **Troubleshooting**

### **Common Issues**

**Error: "Logs not found before workflow completion"**
- **Cause**: Attempting to access logs during workflow intermission
- **Solution**: Wait for workflow completion or check Files API for intermediate results

**Custom command not found**
- **Cause**: Setup script execution failed or PATH not updated
- **Solution**: Re-run setup script or manually check `/usr/local/bin/`

**Verbose mode overwhelming**
- **Note**: Verbose provides developer-console-level debugging (replaces old debug flag)
- **Solution**: Use standard mode for normal operation

### **Terminal Integration**

**Bash/Zsh Commands**: Use `!` prefix within MAO to execute terminal commands:
```
> !ls -la
> !git status  
> !npm install
```

**Session Tracking**: MAO tracks most recent session for `--continue` functionality after interruptions.

---

## 📝 **Usage Philosophy**

### **Goal vs Chat Distinction**
- **Goal**: "Here's my entire project, create a workflow"
- **Chat**: "First message to AI for interactive building"

### **Workflow Identification**
- **Primary ID**: Custom command name (more foolproof than workflow names)
- **Lookup**: Use custom command for workflow details and status

### **Application vs Monitoring**
MAO is a **full interactive application platform**, not a monitoring utility:
- Rich chat interfaces for natural workflow creation
- Live workflow monitoring with real-time progress
- Settings management and user preferences
- Professional application experience rivaling Claude Code

---

*MAO provides a complete workflow orchestration experience that adapts to your working style - from casual conversation to professional development workflows. The setup script system gives you the best of both worlds: simple automation when you want it, complete control when you need it.*