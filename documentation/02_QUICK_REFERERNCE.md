# Section II: Quick Reference Materials 

## Chapter 2.1: Catalog & Defined Purpose of System Files 

===Wed be better to group these by type of file. Below is from the old documentation where we only covered the orchestrator files.=== 

1. `./orchestrator/__init__.py` = "Modular AI workflow orchestration system"
2. `./orchestrator/agent_callback.py` = "Handles agent returns, execution results, and workflow progression"
3. `./orchestrator/agent_orchestrator.py` = "Coordinates agent handoffs with context packages via Files API"
4. `./orchestrator/cache/__init__.py` = "Universal caching infrastructure for modular tools" 
5. `./orchestrator/cache/cache_system.py` = "Files API for workflow handoffs and Local cache for permanence; fingerprinting" 
6. `./orchestrator/cli_manager.py` = "Dynamic CLI command discovery and interface integration"
7. `./orchestrator/conversation_bridge.py` = "Converts natural language goals into executable custom commands"
8. `./orchestrator/core.py` = "The main brain that turns natural language into intelligent workflows"
9. `./orchestrator/error_handling.py` = "Professional error handling patterns for all tools"
10. `./orchestrator/manager_buttons.py` = "Creates executable code snippets for any model/provider combo"
11. `./orchestrator/manager_models.py` = "Loads JSON configs and provides intelligent model selection"
12. `./orchestrator/manager_tools.py` = "Dynamic tool suggestion based on goals, not hardcoded categories"
13. `./orchestrator/mcp_hub.py` = "Integrates Memory MCP, Files API, and MCP Connector into unified system"
14. `./orchestrator/memory_mcp.py` = "Provides workflow context tracking, state management, and session recovery"
15. `./orchestrator/protocol.md`
16. `./orchestrator/real_time_metrics.py` = "Provides live data for UI components; no mock data allowed"
17. `./orchestrator/settings_manager.py` = "Dynamic settings discovery and management using directory-based scanning"
18. `./orchestrator/username_manager.py` = "Handles user creation, session persistence, and settings integration"
19. `./orchestrator/workflow_manager.py` = "Handles workflow ID generation, discovery, and tracking"
20. `./orchestrator/workflow_state.py` = "Simple state tracking with Memory MCP integration"

===The second file we had in the old documentation is wildly incomplete. Better formatted than above, but still not formatted great. We don't want this to be the entire section, so no need to space things out like the below resource.=== 

# Mao System File Responsibilities
**Understanding What Each File Does and How They Work Together**

*Clear guide to Mao's file structure and component responsibilities*

---

## The Big Picture

- Mao follows a **clean layered architecture** 
- Each file has a specific, limited responsibility 
- No file tries to do everything 
- They work together like a professional orchestra

```
User Input → Entry Point → Interface Layer → Orchestration Layer → Execution Layer
```

---

### ENTRY POINT: `mao_v4.py` 

**What it does** Pure command-line routing; nothing else

**Responsibilities**

- Load CLI arguments from arguments JSON config
- Parse command-line arguments  
- Route requests to appropriate interface
- Bootstrap interface with minimal error handling

**What it does NOT do**

- Business logic
- Print statements (except critical bootstrap failures)
- Workflow management
- Complex error handling
- User interaction

**Flow** `Command Line → Argument Parsing → Interface Routing`

---

### INTERFACE: The Visual Voice `interfaces/ui_terminal.py` of Mao

**What it does** All user interaction and experience

**Responsibilities**

- User conversation and input handling
- All formatting and display logic
- Workflow setup conversations
- Progress monitoring and status updates
- Error message formatting and user guidance
- Success/failure presentation

**Contains** All the print statements and UI formatting logic

**Flow** `User Interaction ↔ Interface ↔ Orchestrator Calls`

---

### INTERFACE: Building Web `interfaces/ui_web.py` For the Future 

**What it does** Web-based interface (future implementation)

**Same responsibilities as terminal interface, different presentation**

---

### ORCHESTRATION: The Workflow `orchestrator/core.py` Brain 

**What it does** Workflow creation, planning, and orchestration

**Responsibilities**

- Natural language goal processing
- Workflow plan creation and optimization
- Agent spawning and coordination
- Multi-phase workflow management
- Results collection and synthesis

**Key Classes** 

  - `WorkflowOrchestrator`
  - `WorkflowPlan`
  - `WorkflowPhase`

**Flow** `Goal → Workflow Plan → Agent Coordination → Results`

---

### ORCHESTRATION: The Model's `orchestrator/manager_models.py` Intelligence

**What it does** AI model management and selection

**Responsibilities**

- Model configuration loading
- Dynamic model selection based on task requirements
- Cost optimization and efficiency calculations
- Provider compatibility management
- Fallback strategies for model unavailability

---

### ORCHESTRATION: Human Buttons `orchestrator/manager_buttons.py` Mean Universal Compatibility

**What it does** Human button generation for any AI model

**Responsibilities**

- Self-contained code snippet generation
- Universal model compatibility via executable code
- Provider-agnostic tool execution
- SDK complexity elimination

---

### ORCHESTRATION: The Tool `orchestrator/manager_tools.py` Ecosystem

**What it does** Tool discovery and management

**Responsibilities**

- Dynamic tool discovery from file system
- Tool capability matching for goals
- Tool metadata and configuration management
- Integration with workflow planning

---

### ORCHESTRATION: Caching Performance `orchestrator/cache/cache_system.py` Optimization

**What it does** Intelligent caching for 5,108x speed improvements

**Responsibilities**

- Content fingerprinting and cache management
- Smart freshness assessment
- Performance optimization across all tools
- Token efficiency maximization

---

### ORCHESTRATION: Resilience `orchestrator/error_handling.py` For The Human

**What it does** Professional error handling and recovery

**Responsibilities**

- Comprehensive retry logic with exponential backoff
- Graceful degradation strategies
- Multi-level fallback systems
- User-friendly error communication

---

### ORCHESTRATION: Epic Memory `orchestrator/memory_mcp.py` Recall 

---

## CONFIGURATIONS 

### Model Definitions in `configs/models/` 

**What it does** AI model specifications and capabilities
**Contains** JSON files defining model parameters, costs, capabilities

### Provider Configurations in `configs/providers/` 

**What it does** API provider settings and authentication
**Contains** JSON files with provider endpoints, auth methods, features

### Dynamic Relationships in `configs/connections/` 

**What it does** Flexible mapping between models, providers, and tools
**Contains** JSON files defining optimal combinations and compatibility

### Command Interface in `configs/cli/arguments.json` **this is not accurate**

**What it does** CLI argument definitions for both terminal and in-app use
**Contains** All command-line flags and their in-app command equivalents

---

## TOOL EXECUTION 

### Core Tool Logic in `./tools/*/[tool_name].py` 

**What it does** Pure tool functionality with no UI dependencies

**Responsibilities**

- Core processing logic
- Input validation and normalization
- Structured data return (never print statements)
- Cost estimation and performance metrics

### Tool Display in `tools/*/ui_[tool_name].py` 

**What it does** Beautiful formatting for tool results

**Responsibilities**

- Rich terminal output formatting
- Progress indicators and status displays
- Error message formatting
- Result presentation

### Universal Execution in `tools/*/button_[tool_name].py` 

**What it does** Generate executable code for any AI model

**Responsibilities**

- Self-contained executable snippet generation
- Universal model compatibility
- Demo mode examples and testing

### Tool Metadata in `tools/*/tool_[tool_name].json` 

**What it does** Tool discovery and integration information

**Contains** Capabilities, parameters, cost estimates, examples

---

## How They Work Together

### Example: User Runs "Create marketing strategy"

1. **Entry Point:** `mao_v4.py` parses command, routes to interface
2. **Interface Layer:** `ui_terminal.py` processes goal, displays progress
3. **Orchestration:** `core.py` creates workflow plan, spawns agents
4. **Model Selection:** `manager_models.py` selects optimal models
5. **Tool Discovery:** `manager_tools.py` finds relevant tools
6. **Execution:** Tools run via `button_*.py` snippets
7. **Results:** Interface displays beautiful formatted output

### Key Principle: Clean Separation

- **No file does everything** - each has specific, limited responsibilities
- **No print statements** in orchestration or execution layers
- **Interface layer handles ALL user interaction**
- **Orchestration layer coordinates workflow logic**
- **Execution layer does the actual work**

---

## What This Prevents

### Common Anti-Patterns Mao Avoids

- **Monolithic files** that try to do everything
- **Print statements scattered** throughout business logic
- **Hardcoded configurations** mixed with logic
- **Tight coupling** between UI and business logic
- **Complex error handling** in multiple places

### The Result

- **Testable components** - each file can be tested in isolation
- **Multiple interfaces** - terminal, web, API without code changes
- **Clean maintenance** - changes to one concern don't affect others
- **Professional architecture** - follows industry best practices

---

*This separation ensures Mao remains modular, maintainable, and extensible as it grows.*


---


===I think really we ust want the name of the file and no bullet points but an actual sentence or two of what it does. Perhap for config files we can just explain the types there are for each type of config.=== 

---

===Next I really like the idea of the "extension guide" though the one I'll past a path to is a bit over the top, and I think created early, possibly mostly only tools. ALSO this would be where we address whatever that thing is for setting up configs that I keep seing metioned everywhere. See the note under the # Overview section on our CC_DOCS_FEEDBACK.md file to understand what I'm' referencing. I don't know if it is something real or something made up in the documentation.=== 

---

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

| **FUNCTION**           | **TERMINAL COMMAND**           | **IN-APP COMMAND**            |
| ---------------------- | ------------------------------ | ----------------------------- |
| **Start Application**  | `mao mao`                      | -                             |
| **Run Your Workflow**  | `custom command`               | `/custom command`             |
| **Create Workflow ID** | `uid`                          | `/uid` or `! uid`             |
| **Create User ID**     | `meid username`                | `/meid username`              |
| Restart application    | -                              | `/restart` or `! mao restart` |
| Exit application       | -                              | `/exit` or `! mao exit`       |
| Login User ID          | `mao --login`                  | `/login`                      |
| Logout User ID         | `mao --logout`                 | `/logout`                     |
| Open app config        | `mao --config`                 | `/config`                     |
| Resume last workflow   | `mao --continue`               | `/continue`                   |
| First message to AI    | `mao --chat message`           | `/chat message`               |
| Create entire workflow | `mao --goal project goal`      | `/goal project goal`          |
| System Statistics      | `mao --stats`                  | `/stats`                      |
| List Workflows         | `mao --workflows`              | `/workflows`                  |
| Review Workflow        | `mao --review custom command`  | `/review custom command`      |
| Setup from JSON        | `mao --setup ./config.json`    | `/setup ./config.json`        |
| Update Workflow        | `mao --update ./phase.json`    | `/update ./phase.json`        |
| Fix Deliverable        | `mao --fix-it ./fix.json`      | `/fix-it ./fix.json`          |
| Set output directory   | `mao --output ~/downloads`     | `/output ~/downloads`         |
| Use only free models   | `mao --free`                   | `/free`                       |
| Privacy models only    | `mao --privacy`                | `/privacy`                    |
| Verbose Debug Mode     | `mao --verbose`                | `/verbose`                    |
| View workflow logs     | `mao --logs`                   | `/logs`                       |
| Show workflow stats    | `mao --stats`                  | `/stats`                      |
| Check Health           | `mao --doctor`                 | `/doctor`                     |
| View help messages     | `mao --help`                   | `/help`                       |
| Simulate Workflow      | `mao --dry-run`                | `/dry-run`                    |
| Set favorite model     | `mao --model model-name`       | `/model model-name`           |
| Set default provider   | `mao --provider provider-name` | `/provider provider-name`     |
| List models            | `mao --model-list`             | `/model-list`                 |
| List providers         | `mao --provider-list`          | `/provider-list`              |
| List tools             | `mao --list-tools`             | `/list-tools`                 |
| List variables         | `mao --variables`              | `/variables`                  |
| Explain variables      | `mao --variables-explain`      | `/variables-explain`          |
| Terminal Commands      | -                              | `! ls -la` (any bash/zsh)     |

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
# Also writes a WORKFLOW_NAME_README.md and a use-case specific script 
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
configs/use_case/analysis-saas-competition/
├── competitor_analysis_saas_config.json     # Original configuration; this is the JSON config file 
├── COMPETITOR_ANALYSIS_SASS_README.md       # Auto-generated usage guide
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

1. **Context Retrieval**: Claude pulls workflow memory and logs using unique workflow ID
2. **Agent Preparation**: Creates button snippets for tools and callbacks
3. **Material Handoff**: Provides agents with deliverables, token limits, auto-save reminders, and live token counter document tool 
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