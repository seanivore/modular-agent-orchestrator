# MAO User Guide
**Complete Application Usage Reference**

*How to use MAO as an interactive application platform*

---

## 🎯 **Quick Start**

### **First Launch**
```bash
mao mao  # Starts interactive application
```

**First-time users** see color contrast selection, then main chat interface.

### **Basic Usage Patterns**

**Goal-Driven Workflow Creation:**
```bash
mao --goal "create marketing plan for SaaS startup"
```

**Interactive Chat Session:**
```bash
mao --chat "let's build a targeted resume maker"
```

**Direct Application Start:**
```bash
mao mao  # Interactive mode with full UI
```

---

## 📋 **Command Reference**

### **Dual Interface Philosophy**
MAO provides **two ways** to execute every command:
- **Terminal**: `mao --command` (before launching app)
- **In-App**: `/command` or `!command` (while app is running)

### **Complete Command Chart**

| **FUNCTION**                | **TERMINAL COMMAND**        | **IN-APP COMMAND**           |
| --------------------------- | --------------------------- | ---------------------------- |
| **Start Application**       | `mao mao`                   | -                            |
| Restart application         | -                           | `/restart` or `!mao restart` |
| Exit application            | -                           | `/exit` or `!mao exit`       |
| **First message to AI**     | `mao --chat "message"`      | `/chat message`              |
| **Create entire workflow**  | `mao --goal "project goal"` | `/goal project goal`         |
| **System Statistics**       | `mao --stats`               | `/stats`                     |
| **List Workflows**          | `mao --workflows`           | `/workflows`                 |
| **Setup from JSON**         | `mao --setup ./config.json` | `/setup ./config.json`       |
| **Update Workflow**         | `mao --update ./phase.json` | `/update ./phase.json`       |
| **Fix Deliverable**         | `mao --fix-it ./fix.json`   | `/fix-it ./fix.json`         |
| **Custom Output Directory** | `mao --output ~/downloads`  | `/output ~/downloads`        |
| **Verbose Debug Mode**      | `mao --verbose`             | `/verbose`                   |
| **Terminal Commands**       | -                           | `!ls -la` (any bash/zsh)     |

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
- `!command` - Execute any terminal command from within MAO

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

**Interactive Building:**
```bash
mao mao
> /chat I need help with content strategy
> [conversation builds workflow]
> [automatic setup script generation]
```

**Command-Line Efficiency:**
```bash
mao --setup ./my-workflow.json --verbose
```

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