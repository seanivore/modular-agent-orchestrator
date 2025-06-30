# Mao Terminal Application Foundation Specification

**Professional Terminal Interface for AI Workflow Orchestration**

*Claude Code Execution Specification - Part 1: Foundation*

---

## Mission Statement

Create a professional terminal application that rivals Claude Code's quality and elegance. Mao is a unified terminal interface where users launch the application and interact through a single, beautiful interface for workflow creation, execution monitoring, and management.

**Architecture Reference**: Use Claude Code's proven interface patterns as the foundation - this gives us an excellent starting point that we can customize for Mao's unique workflow orchestration capabilities.

---

## Application Architecture Overview

### Core Concept
Mao is a **unified terminal application** - users run `mao mao` and enter a beautiful interface similar to Claude Code. Everything happens in one cohesive screen through conversation-based interaction.

### User Flow
1. **Launch**: User runs `mao mao` command
2. **Onboarding**: Progressive setup (theme selection, user identification) 
3. **Unified Interface**: Single text input for ALL interactions
4. **Workflow Operations**: Create, execute, and monitor workflows through conversation
5. **Session Persistence**: State maintained across application restarts

### Interface Philosophy
- **Single screen experience**: Everything happens in one unified interface
- **Conversation-driven**: Users chat with Mao for all functionality
- **Progressive disclosure**: Complex features revealed as needed
- **Professional quality**: Matches Claude Code's elegant design standards

---

## UI Content Translation System

### Translation Principle
The existing `interfaces/ui_terminal.py` contains print statements that represent **what information to display and when**. These must be systematically converted into beautiful interface components while preserving all functionality.

### Content Translation Framework

Create `interfaces/terminal/content_translator.py`:

```python
class UIContentTranslator:
    """Converts ui_terminal.py information into visual interface components"""
    
    def translate_workflow_creation(self, goal: str) -> ConversationDisplay:
        """Convert goal input into conversational workflow creation"""
        
    def translate_execution_progress(self, phase_data: dict) -> ProgressVisualization:
        """Convert phase execution into live progress display"""
        
    def translate_tool_activities(self, tools: list) -> ToolStatusDisplay:
        """Convert tool usage into elegant status indicators"""
        
    def translate_cost_monitoring(self, cost_info: dict) -> CostTracker:
        """Convert cost tracking into professional cost display"""
        
    def translate_deliverables(self, outputs: list) -> DeliverablesSummary:
        """Convert file outputs into organized deliverables display"""
```

### Visual Language Implementation

**Claude Code Foundation Colors**:
- **Pink** `#ff6b9d` → AI actions requiring attention
- **Yellow** `#c69500` → AI explanations and analysis
- **Light Blue** `#54c7ec` → Interactive elements and commands
- **White** `#ffffff` → Primary content and responses
- **Gray** `#6e6a86` → Secondary information and metadata
- **Light Brown** `#7b714a` → Tree structure and organizational elements

**Mao's Workflow Innovation**:
```
△   Mao analyzing your goal...              ← Yellow (AI processing)
├── ●   Creating workflow structure         ← Light brown tree + white content  
├── ●   Selecting optimal models           ← Status information
└── ▲   Ready to begin execution           ← Pink (action required)
```

---

## Core Application Components

### Foundation Structure
```
interfaces/terminal/
├── app.py                          # Main application entry point
├── conversation_interface.py       # Unified conversation system
├── content_translator.py          # ui_terminal.py → beautiful UI
├── visual_language.py             # Color system and typography
├── onboarding/
│   ├── welcome_flow.py            # Initial app setup
│   ├── theme_selector.py          # User theme preferences
│   └── user_identification.py     # User ID generation
├── workflow/
│   ├── creation_interface.py      # Goal → workflow conversation
│   ├── execution_monitor.py       # Live execution display
│   ├── progress_visualization.py  # Tree-based progress tracking
│   └── completion_summary.py      # Results and deliverables
├── components/
│   ├── input_handler.py           # Unified text input system
│   ├── autocomplete_system.py     # CLI command auto-complete with fuzzy search
│   ├── display_manager.py         # Screen content management
│   ├── cost_tracker.py           # Real-time cost monitoring
│   └── help_system.py            # Contextual guidance
└── integrations/
    ├── orchestrator_bridge.py     # Direct core.py integration
    ├── memory_persistence.py      # Session state management
    └── config_manager.py          # Settings and preferences
```

### Key Component Specifications

#### 1. Main Application (`app.py`)
- **Startup sequence**: Welcome message, onboarding check, theme loading
- **Session management**: Restore previous state, user preferences
- **Navigation routing**: Handle all interface transitions
- **Error handling**: Graceful error display and recovery

#### 2. Conversation Interface (`conversation_interface.py`)
- **Unified input system**: Single text field for all interactions
- **CLI Auto-Complete System**: Claude Code-style command discovery and suggestion
- **Message routing**: Determine intent (workflow creation, execution, help)
- **Context awareness**: Maintain conversation history and workflow state
- **Response formatting**: Apply visual language to all responses

#### 3. Conversational Tool Access (`conversation_interface.py`)
- **Transparent tool usage**: Mao automatically uses available tools during chat
- **Freshness detection**: Automatically searches for current information when needed
- **Familiar UX**: Same experience users expect from Claude web interface
- **No workflow overhead**: Tools used conversationally, not as formal steps

#### 4. Welcome Flow (`onboarding/welcome_flow.py`)
- **First-time setup**: Theme selection, user identification
- **Return user detection**: Load existing preferences
- **Introduction sequence**: Guide users through Mao capabilities
- **Theme preview**: Show visual examples like Claude Code

#### 5. Workflow Creation Interface (`workflow/creation_interface.py`)
- **Goal conversation**: Natural language workflow creation
- **Progressive refinement**: Clarify requirements through dialogue
- **Configuration options**: Model selection, preferences, constraints
- **Workflow preview**: Show planned phases and estimated costs

#### 6. Execution Monitor (`workflow/execution_monitor.py`)
- **Live progress tracking**: Real-time workflow execution display
- **Agent spawning visualization**: Show orchestrator decisions
- **Phase transitions**: Clear visual progression through workflow
- **Interactive monitoring**: Pause, resume, modify execution

---

## Implementation Tasks

### Phase 1: Foundation Application
1. **Create main application shell** based on Claude Code patterns
2. **Implement welcome flow** with theme selection and user setup
3. **Build unified conversation interface** with single input field
4. **Create content translator** for ui_terminal.py information
5. **Implement visual language system** with Claude Code colors

### Phase 2: Workflow Integration  
1. **Build workflow creation interface** through conversation
2. **Integrate orchestrator bridge** for direct core.py calls
3. **Implement execution monitoring** with live progress display
4. **Create completion summaries** with deliverables organization
5. **Add session persistence** using Memory MCP integration

### Phase 3: Advanced Features
1. **Enhance progress visualization** with tree-based workflow display
2. **Implement cost tracking** with real-time budget monitoring
3. **Add help and guidance** system with contextual assistance
4. **Create settings interface** for user preferences
5. **Optimize performance** and polish user experience

---

## Integration Requirements

### Orchestrator Core Connection
```python
# Direct integration pattern
from orchestrator.core import WorkflowOrchestrator
from orchestrator.memory_mcp import MemoryMCPManager

class ConversationInterface:
    def __init__(self):
        self.orchestrator = WorkflowOrchestrator()
        self.memory = MemoryMCPManager()
        
    async def handle_goal_input(self, goal: str):
        workflow = await self.orchestrator.create_workflow_from_goal(goal)
        await self.memory.save_workflow_state(workflow.id, workflow)
        return self.display_workflow_preview(workflow)
```

### Conversational Tool Access

```python
class ConversationInterface:
    def __init__(self):
        self.tool_manager = ToolManager()
        self.available_tools = self.tool_manager.get_all_tools()
        
    async def process_user_message(self, message: str):
        # Analyze if tools would improve response
        if self._needs_current_info(message):
            search_results = await self.web_search_tool.search(message)
            return self._enhanced_response(message, search_results)
        elif self._references_files(message):
            file_data = await self.file_tool.analyze_files(message) 
            return self._enhanced_response(message, file_data)
        else:
            return self._standard_response(message)
```

### Content Translation Integration
```python
# Preserve all ui_terminal.py functionality
class ContentTranslator:
    def __init__(self, display_manager: DisplayManager):
        self.display = display_manager
        
    def translate_workflow_status(self, status_message: str):
        # Convert print statements to beautiful UI components
        return self.display.show_workflow_status(
            message=status_message,
            style=self.determine_visual_style(status_message)
        )
```

---

## Success Criteria

### Functional Requirements
- Launch `mao` command enters beautiful terminal application
- Progressive onboarding for first-time users
- Unified conversation interface handles all user interactions
- All ui_terminal.py functionality preserved and enhanced
- Seamless workflow creation through natural conversation
- Live execution monitoring with professional progress display

### Quality Standards
- **Visual excellence**: Matches Claude Code's professional aesthetic
- **Responsive performance**: Smooth animations and state transitions
- **Intuitive navigation**: Users understand interface without training
- **Error resilience**: Graceful handling of all error conditions
- **Session continuity**: State preserved across application restarts

### Technical Excellence
- **Clean architecture**: Modular components supporting future expansion
- **Direct integration**: Seamless connection to existing orchestrator core
- **Future-ready**: Foundation prepared for web and mobile interfaces
- **Professional code**: Clear documentation and maintainable structure

---

## Dependencies and Setup

### Required Libraries
```bash
pip install rich textual asyncio pathlib dataclasses typing
```

### Foundation Files
- Existing orchestrator core system (`orchestrator/core.py`)
- Memory MCP integration (`orchestrator/memory_mcp.py`)
- Configuration system (`configs/` directory structure)
- Tool integration system (`tools/` with button snippets)

### Development Approach
1. **Start with Claude Code patterns** - use proven interface design
2. **Implement content translator** - systematically convert ui_terminal.py
3. **Build incrementally** - working application from first implementation
4. **Test continuously** - verify all existing functionality preserved
5. **Polish progressively** - enhance visual quality and user experience

---

*This specification creates Mao as a professional terminal application that rivals Claude Code's quality while providing unique AI workflow orchestration capabilities through beautiful, conversation-driven interface design.*