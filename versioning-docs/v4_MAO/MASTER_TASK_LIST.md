# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)

## Terminal UI Design 

- **Primary Language: TypeScript/Node.js**
  - Regarding the language change: 
  - AI told me that it would be complicated because we'd have to change files 
  - I asked them to clarify because the python does the work and then the typescript does the UI
  - I didn't see the conflict 
  - Then they said I was right and they were over thinking it 
- **Mentioning this in case it comes up again**

- **TypeScript/Node.js** with npm distribution - that's actually really smart for a developer tool.
- **Easy distribution** via npm (developers already have Node)
- **Cross-platform** (works everywhere Node works)
- **Rich ecosystem** for terminal UIs and APIs
- **TypeScript** gives them good type safety for a complex tool

- Use libraries like `ink` (React for terminal) or `blessed`
- Easy to integrate with Claude's APIs
- Familiar if you know JavaScript

- Primarily developed using TypeScript and Node.js
- Evident from the installation instructions using Node package manager (npm install -g @anthropic-ai/claude-code)

---------------------------------

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