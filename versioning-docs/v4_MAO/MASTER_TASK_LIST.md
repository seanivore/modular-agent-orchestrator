# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)

For args that are "needs input" I don't want to require having quotes because the terminal can be so frustrating with quotes. 

Re: these two especially: 

| **First message to AI**     | `mao --chat message`        | `/chat message`              |
| **Create entire workflow**  | `mao --goal "project goal"` | `/goal project goal`         |


--------------------------------

NOTES: Things I notice as we work that also need to be in the documentation. 
- Adding a new command: Just drop new_command.json in configs/cli/ - entry point automatically discovers it!

--------------------------------

I saw this in the docs while reviewing them and had an idea. We should make sure that the orchestrator can search the web or use any other tools during chat sessions. It should be the same UX that everyone is already used to. Plus, when someone is suspicious about the freshness of information, or knows that there is new information that came out after the training data cutoff date, our Claude needs to be able to deal with that just like users will expect. 

```
### Smart Freshness Assessment

Mao understands that different types of information have different freshness requirements:

Mao: "I found cached research on B2B SaaS trends from 45 days ago.

Freshness Analysis:
✅ Industry analysis: Still valid (180-day freshness window)
⚠️ Market trends: Partially stale (30-day window, 50% confidence)
❌ Pricing data: Expired (7-day window, requires refresh)

Optimization Strategy:
- Reuse: Industry analysis and competitive framework
- Refresh: Current market trends and pricing data
- Effort Reduction: 60% vs. full research
- Quality Maintained: Fresh data where it matters most"
```

--------------------------------

I deleted the pretend case studies from 1_MAO_OVERVIEW.md. It was a bunch in two different sections, one offering examples and the other framed as actual case studies. Instead it just mentions that we're building a database for workflows, tools, and model information. <-- All of which Claude Orchestrator should have direct access to instead of users having to look it up on some website somewhere as if it was 2020. 

--------------------------------

On the doc: `2_MAO_SYSTEM_FILES.md`. 
After this heading / section: 

```
## 🎭 **Entry Point Layer**

### `mao_v4.py` - The Router
**What it does:** Pure command-line routing; nothing else
**Responsibilities:**
- Load CLI arguments from arguments JSON config
- Parse command-line arguments  
- Route requests to appropriate interface
- Bootstrap interface with minimal error handling

**What it does NOT do:**
- Business logic
- Print statements (except critical bootstrap failures)
- Workflow management
- Complex error handling
- User interaction

**Flow:** `Command Line → Argument Parsing → Interface Routing`
```

How about the fact that it runs the workflow script? Like when you use the setup script with the JSON, and it creates a new script and puts in into the workflow use-case directory, and then makes it executable. So when the user runs the workflow, it runs the script. Isn't that handled by this entry point? is it mentioned somewhere else? Feels like it should be here because I'm left wondering like, how other things happen. Like it feels overly simplistic. Needs a secondary flow. We should be up front from the start that the entry point either leads you to setup a workflow, or it activates and runs a workflow. Right? 

--------------------------------

This is for my own clarification. On the doc: `2_MAO_SYSTEM_FILES.md`. This section: 

```
## 🖥️ **Interface Layer**

### `interfaces/ui_terminal.py` - The UX Brain
**What it does:** All user interaction and experience
**Responsibilities:**
- User conversation and input handling
- All formatting and display logic
- Workflow setup conversations
- Progress monitoring and status updates
- Error message formatting and user guidance
- Success/failure presentation

**Contains:** All the print statements and UI formatting logic

**Flow:** `User Interaction ↔ Interface ↔ Orchestrator Calls`

### `interfaces/ui_web.py` - Future Web Interface
**What it does:** Web-based interface (future implementation)
**Same responsibilities as terminal interface, different presentation**
```

That file does thinking / logic? I was under the impression that it just sort of held all of the print statements for any situation. Also I changed it to "the workflow voice" 

--------------------------------

On the doc: `2_MAO_SYSTEM_FILES.md`. This section: 

```
### `orchestrator/memory.py` - Workflow Context
**What it does:** Workflow state and context management
**Responsibilities:**
- Workflow memory and context preservation
- Agent handoff coordination
- State persistence across workflow phases
```

We are using the Memory MCP to store the workflow state and context now. This needs to be updated. 

--------------------------------

On the doc: `2_MAO_SYSTEM_FILES.md`. This section: 

```
### `configs/cli/arguments.json` - Command Interface
**What it does:** CLI argument definitions for both terminal and in-app use
**Contains:** All command-line flags and their in-app command equivalents
```

Re: "arguments.json".... we broke it down so that every single argument/command has its own JSON file. More modular. Needs to be updated. 


--------------------------------




| **SESSION 22 TASK** |
| ------------------- |

# Terminal UI Foundation

A few little tasks before activating a SPEC in Claude Code. 

## Beautiful Interface for MAO

**Status:** Foundation prepared, awaiting walkthrough completion  
**Complexity:** Medium-High integration task  

## What We Have Ready:
- ✅ Terminal UI foundation files (app.py, styles.py, styles.css, main_menu.py)
- ✅ Professional color palette and styling system (Anthropic-inspired, no emojis)
- ✅ Navigation system architecture
- ✅ Integration specification for Claude Code
- ✅ Clear understanding of Mao codebase structure (from cursor audit)

### What This "Replaces"
- Current print-statement based `interfaces/ui_terminal.py`
- **IMPORTANT:** Print functions contain valuable UI requirements 
  - These should be integrated into new UI, NOT discarded 
  - So not really "replace" but rather "update" 

### Directory Structure to Continue Creating 
```
interfaces/
├── ui_terminal.py          # KEEP existing print functions - add beautiful UI option
├── ui_web.py              # (existing)
└── terminal/              # NEW - beautiful UI system
    ├── app.py             # Main terminal application
    ├── styles.py          # Professional color schemes
    ├── styles.css         # Textual CSS styling
    ├── navigation.py      # Navigation management
    ├── orchestrator_bridge.py # Direct integration with MAO core
    ├── workflow_bridge.py # UI to workflow execution
    ├── config_bridge.py   # Integration with configs/ system
    └── components/        # UI components
        ├── main_menu.py   # Main navigation
        ├── workflow_wizard.py # Workflow creation
        ├── workflow_manager.py # Workflow management  
        ├── command_runner.py # Execution interface
        ├── settings_screen.py # Configuration
        ├── base_widgets.py # Reusable components
        ├── progress_display.py # Progress tracking
        └── notification_system.py # Status messages
```

### Foundation Files That Exist ✅
1. `app.py` - Main terminal application 
2. `styles.py` - Color schemes and styling 
3. `styles.css` - Textual CSS styling 
4. `navigation.py` - Navigation system 
5. `main_menu.py` - Main navigation component

### Setup Steps (When Ready):
1. **Create directory structure:**
   ```bash
   mkdir -p interfaces/terminal/components
   touch interfaces/terminal/__init__.py
   touch interfaces/terminal/components/__init__.py
   ```

2. **Install dependencies:**
   ```bash
   pip install rich textual
   ```

3. **Copy foundation files** to `interfaces/terminal/` directory

4. **Modify ui_terminal.py** to offer both modes:
   ```python
   def main():
       import sys
       if "--ui" in sys.argv:
           from interfaces.terminal.app import MaoTerminalApp
           app = MaoTerminalApp()
           app.run()
       else:
           # Existing print-based interface
           launch_print_interface()
   ```

5. **Run integration in Claude Code** using integration spec

### Integration Requirements:
- **Use existing print function content** as UI requirements (don't discard)
- **Direct integration** with orchestrator core (no print interception needed)
- **Preserve button snippet prints** (functional, keep unchanged)
- **Preserve demo prints** (examples, keep unchanged)
- **Use existing configs/** for model/provider management
- **Integrate with existing workflow patterns**

### Key Architectural Decisions Made:
- **Professional aesthetic** - Clean, Anthropic-inspired, no emojis
- **Modular memory system** - workflow-specific memory.py in each use-case directory
- **Direct orchestrator calls** - UI calls core functions directly
- **Print function preservation** - Existing prints are UI requirements, not waste

### Dependencies:
- Must complete walkthrough first (contains true holistic UI/UX planning)
- Requires integration spec (see spec comparison below)
- Needs clean MAO codebase structure (already audited with cursor)

### Expected Outcome:
Beautiful, professional terminal interface that:
- Rivals Claude Code quality
- Integrates seamlessly with existing MAO functionality  
- Uses print function content as elegant UI components
- Provides smooth workflow creation, management, execution
- Maintains all existing functionality while enhancing UX

### Notes:
- This is foundational work prepared during planning phase
- Implementation should wait for walkthrough completion
- Print functions contain valuable UI requirements - integrate, don't replace
- Foundation is solid but integration requires full context from walkthrough 