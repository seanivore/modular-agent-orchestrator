# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)

--------------------------------

| **SESSION 19 TASK B** |
| --------------------- |

# Mao CLI Flag Arguments & Application Commands 

These are modular, fed into the agent `mao_v4.py` via JSON in the config directory via this file: `/Users/seanivore/Development/modular-agent-orchestrator/configs/cli/arguments.json` -- The chart below is for our technical documentation. 

| **COMMAND**                          | **IN TERMINAL**                     | **IN APPLICATION**             |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| **START APPLICATION**                | `mao mao`                           |                                |
| Restart the application              |                                     | `/restart`  `! mao restart`    |
| Exit the application                 |                                     | `/exit`  `! mao exit`          |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| Terminal command example; add '!'    |                                     | `! cd /Users/*/*/`             |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| **Activate a workflow**              | `custom command`                    | `/custom command`              |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| Setup JSON workflow config           | `mao --setup ./use-case.json`       | `/setup ./use-case.json`       |
| Update additional workflow phase     | `mao --update ./phase-two.json`     | `/update ./phase-two.json`     |
| Fix deliverable from workflow phase  | `mao --fix-it ./fix-doc.json`       | `/fix-it ./fix-doc.json`       |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| Jump into app with first message     | `mao --chat targeted resumes`       | `/chat targeted resumes`       |
| Create entire workflow from goal     | `mao --goal startup marketing plan` | `/goal startup marketing plan` |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| View all workflows                   | `mao --workflows`                   | `/workflows`                   |
| View a workflow's details            | `mao --review custom command`       | `/review custom command`       |
| System performance statistics        | `mao --stats`                       | `/stats`                       |
| Override default output directory    | `mao --output ~/downloads`          | `/output ~/downloads`          |
| ------------------------------------ | ----------------------------------- | ------------------------------ |
| Use free AI agent models only        | `mao --free`                        | `/free`                        |
| Privacy-focused models, providers    | `mao --privacy`                     | `/privacy`                     |
| Show these help messages             | `mao --help`                        | `/help`                        |
| Configuration management interface   | `mao --config`                      | `/config`                      |
| Check health of Mao installation     | `mao --doctor`                      | `/doctor`                      |
| Verbose, developer-tools detail      | `mao --verbose`                     | `/verbose`                     |
| Simulate workflow execution only     | `mao --dry-run`                     | `/dry-run`                     |
| Continue most recent session         | `mao --continue`                    | `/continue`                    |
| View recent workflow logs            | `mao --logs`                        | `/logs`                        |
| ------------------------------------ | ----------------------------------- | ------------------------------ |

## Example Terminal Modifier Commands  

```bash
    mao mao                                # Start application
    mao --goal create marketing plan       # Execute goal directly
    mao --stats --verbose                  # Detailed system statistics
    mao --setup ./my-workflow.json         # Setup new workflow
    mao --workflows                        # List all workflows
    mao --doctor                           # Check installation health
```

## Example Application Commands  

```bash
    /restart                               # Restart application
    /goal create marketing plan            # Execute goal directly
    /stats                                 # Detailed system statistics
    /setup ./my-workflow.json              # Setup new workflow
    /workflows                             # List all workflows
    /doctor                                # Check installation health
```

## Concerns & FYIs 

1. I recommend that when we need to identify a workflow, we use the custom command as the identifier. It is just going to be more fool-proof 
2. For example, to pull up details of a workflow, instead of name, use custom command; should be similar anyway 
3. Error handling for looking up 'Logs" before a workflow is complete (on is in an intermission) because everything will be in the Files API 
4. Just FYI, verbose has robust developer-console-like-tools *for* debugging, so I removed the debugging flag 
5. We need to make sure that bash/zsh commands from inside the application run if '!' is added before the command 
6. Goal and Chat were conceptually overlapping; now goal is "here's my entire project, create a workflow" and chat is "first message to AI" 
7. Figure out how to make sure we track what the most recent session is; this is helpful if you're interrupted or lose internet, for --continue 


--------------------------------

| **SESSION 19 TASK C** |
| --------------------- |

# "Phase 2 Implementation Planning" Document Feedback 

This is for reference with the feedback. When we edit and use the things we need to plan from this, we'll do it together. 
`/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/v4_PHASE_2_IMPLEMENTATION_PLANNING.md`

## Project Workflow JSON Config File

The intention is that it is easily done by a User. 

  - Claude is an extra convenience, not a reason to make it more complicated 
  - Most of it looks like what comes up after planning the workflow anyway, like cost, time, etc. 

So let's make this simpler by creating two. 

  1. The simple one without details that aren't known until the workflow is chosen 
  2. A second one that has the finer details and is only completed after the workflow is chosen 

There is also some stuff that is just a bit extra over the top in general. Like maybe something for an update, but I don't think we need things like version numbers for Use-Cases yet. 

I also don't like the date in the master directory folder name. Ideally it will be the same name as the Use-Case and as the command except with hyphens instead of spaces. This would allow the Use-Cases with the same first word to the command to be grouped next to each other. So like `job target docs` and `job find openings` could have been built months apart but will sit next to each other. And if I remember correctly regarding how the command is created, it will basically be the same command but with different args. 

The idea of tags is nice, but again, let's not get too far ahead of ourselves. You know I like to build for myself in the future, but not as much when it is something that can be done easily -- or like in the case of tags, agentically. 

### New Version Needs 

  1. Unique ID space left open to be filled in by setup script 
  2. Desired command with spaces, not hyphens 
  3. Model and then fallback model, then failsafe model 

### Project Use-Case Directory Structure Pattern 

 - The directory structure pattern for workflows is okay 
     - Intricate and very detailed 
       - Seems like there might be spots for drafts? 
       - We are keeping drafts in the Files API 
       - Then deleting drafts when the final deliverables are saved 
       - It's a big token save 
     - Whatever we end up with 
       - Let's have the setup script create the entire thing 
       - We won't even create the named folder for the use-case 


## Regarding the Interactive Command Builder 

 - This is all categorical, themed, hard-coding. 
 - I mentioned in the walkthrough my thoughts, which was that we let Claude be Claude and not give them any kind of script at all. 
   - All they need to know is what variables they need to get filled out. 
   - Their primary role should be to try to anticipate the user's needs to give the best UX possible. 
   - We want them to be able to tell if someone needs help or not. 
   - We can always change this over time, but based on working on these things with you in the SFA, the setup assistant stuff just seems like it is way overthinking it. 

--> The 'Natural Language Goal Processing' looks like it is the same issue. It's code, but still seems like we're scripting Claude Sonnet 4, which just seems crazy. 

## UI Terminal Display Stuff 

I love this as a starting point. I'm not sure I'll be too much help until I'm actual in the terminal and can see it and move stuff around. 

You mentioned somewhere about how Claude Code is really simple and then referenced my comment about how it doesn't roll up like a receipt as if the receipt thing was what we'd want. But newsflash, AI, humans hate receipts. People always hate them to us just so we can throw them out a second later it is so annoying. When you think about employees needing to keep receipts it becomes easily memorable that the are not good. 

My point was just that I liked how the entire session of Claude Code, with  my terminal from top of screen to bottom and 70 character wide or 120 or something like that, it just barely filled up more than that when done because when the information you don't need anymore is done, it disappears. We don't want it to "print" on the terminal because if it is something we'd want to see later then we'd want it somewhere convenient like automatically saved to the use case directory. 


--------------------------------

| **SESSION 20 TASK A** |
| --------------------- |

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


--------------------------------

| **SESSION 21 TASK** |
| ------------------- |


### **PHASE 1: Core Integrations** (Session 19)
**Status**: 🔴 NOT STARTED

#### A. MCP API Connector ⭐ **NEW PRIORITY**
- **What**: Model Context Protocol Server API Connector (recent Anthropic release)
- **File**: Based on `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_API_MCP_CONNECT.md`
- **Why Critical**: Latest Anthropic standard for AI tool integration

#### B. Code Execution Tool 🎯 **CORE FEATURE**
- **What**: Direct integration with Claude 4 Code Execution for human buttons
- **File**: Based on `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_CODE_EXECUTION.md`
- **Why Critical**: Makes human buttons actually executable vs just code snippets
- **Dependencies**: Must work with button system

#### C. Files API Integration 💾 **WORKFLOW ESSENTIAL**
- **What**: Anthropic Files API for workflow handoffs and temp storage
- **File**: Based on `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/TOOL_FILES_API.md`
- **Why Critical**: Agent-to-agent communication and workflow continuity

#### D. Tool Discovery Connection 🔗 **MISSING LINK**
- **What**: Connect `manager_tools.py` to `core.py` for dynamic tool discovery
- **Why Critical**: Orchestrator can't currently discover tools automatically
- **Status**: Files exist but not connected

#### E. Protocol Document 📋 **BEHAVIOR GUIDE**
- **What**: Create `protocol.md` defining MAO's orchestrator behavior patterns
- **Why Critical**: Consistent, predictable AI behavior across workflows
- **File**: `orchestrator/protocol.md` (currently empty)


--------------------------------

| **SESSION 22 TASK** |
| ------------------- |

### **PHASE 2: Complete UX Flow** 
**Status**: 🔴 NOT STARTED

#### A. First-Time Setup Experience 🎬 **USER ONBOARDING**
```
Goal → MAO Setup → JSON Config → Custom Command → Ready!
```
- **Missing**: Setup conversation interface
- **Missing**: JSON config generation
- **Missing**: Custom command creation

#### B. Workflow Execution UX 🚀 **CORE EXPERIENCE**
```
Custom Command → Workflow Execution → Results
```
- **Missing**: Seamless execution from custom commands
- **Missing**: Progress monitoring during execution
- **Missing**: Results presentation and storage

#### C. Use Case Configuration System 📁 **WORKFLOW PERSISTENCE**
- **What**: `./configs/use_case/*/` directory structure
- **What**: JSON variable-input config files
- **What**: Use case README generation


--------------------------------

| **SESSION 23 TASK** |
| ------------------- |

### **PHASE 3: Testing & Validation** (Session 20)
**Status**: 🔴 NOT STARTED

#### A. End-to-End Testing 🧪 **QUALITY ASSURANCE**
- **What**: Complete user journey testing (new user → working workflow)
- **What**: Multi-tool workflow testing
- **What**: Error handling and edge case testing
- **Effort**: 3-4 hours comprehensive testing

#### B. Performance Validation 📊 **EFFICIENCY CLAIMS**
- **What**: Verify 95% token reduction vs v3.3.0
- **What**: Confirm <$0.01 per workflow execution
- **What**: Cache hit rate analysis
- **Effort**: 2-3 hours measurement and optimization

#### C. Human Button Integration Testing 🔘 **CORE FEATURE**
- **What**: Test button generation across all models (Anthropic, OpenAI, Gemini)
- **What**: Verify Claude 4 Code Execution integration
- **What**: Error handling and retry logic testing
- **Effort**: 2-3 hours cross-platform testing


--------------------------------

| **SESSION 24 TASK** |
| ------------------- |

## 📊 COMPLETION STATUS

### ✅ **COMPLETED** (Sessions 1-17)
- **Revolutionary Architecture**: Human buttons, variable-input philosophy, modular design
- **Tool Standardization**: All 8 tools with 4-file pattern, consistent interfaces
- **Cache System**: Fingerprinting, 5,108x speed improvements
- **Manager Components**: Models, buttons, tools, error handling
- **Cost Optimization**: JSON configs, dynamic model selection
- **Token Efficiency**: 95% reduction architecture proven

### 🚧 **REMAINING WORK** (Sessions 18-20)
- **Critical Path**: MCP + Code Execution + Files API → UX Flow → Testing
- **Key Dependencies**: Tool discovery connection, protocol documentation
- **Success Criteria**: New user can create and run workflow in <10 minutes

### 🎯 **SUCCESS METRICS**
- **User Experience**: Natural language goal → working custom command
- **Performance**: <$0.01 per workflow, <5 second cache hits
- **Adoption**: Zero technical knowledge required for basic usage
- **Reliability**: 99%+ success rate for standard workflow patterns

