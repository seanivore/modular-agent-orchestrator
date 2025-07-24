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

**MAO Visual Protocol** (from `6_MAO_VISUAL_IDENTITY.md`):

**Core Color System**:
- **Pink** `#ff49ff` → AI actions requiring attention (ONLY BOLD COLOR)
- **Yellow** `#f1d771` → AI explanations and primary content
- **Light Blue** `#82d0ff` → AI-highlighted URLs/commands and checkmarks
- **White** `#ffffff` → System responses and AI content bullets
- **Gray** `#bbbcbb` → User input and secondary information
- **Light Brown** `#7b714a` → Tree characters and metadata

**MAO's Orchestration Innovation**:
```
△   Mao analyzing your goal...              ← Yellow (AI explaining)
├── ●   Creating workflow structure         ← Light brown tree + yellow content  
├── ●   Selecting optimal models           ← Status information
└── ▲   Ready to begin execution           ← Pink bold (action required)
```

**Shape Language for Workflow States**:
- **Triangle (△/▲)** = Orchestrator (Mao) - outline/filled for waiting/active
- **Circle (○/●)** = Agent - outline/filled for waiting/active
- **Checkmark overlay** = Completed states while preserving shape identity

---

## Core Application Components

### Foundation Structure
```
interfaces/terminal/
├── app.py                          # Main application entry point
├── conversation_interface.py       # Unified conversation system
├── content_translator.py          # ui_terminal.py → beautiful UI
├── visual_language.py             # MAO visual protocol implementation
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
│   ├── command_dropdown.py        # Auto-complete dropdown with categories
│   ├── command_scanner.py         # Dynamic command discovery from configs/cli/
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
- **Unified input system**: Single text field for all interactions with contextual tips
- **CLI Auto-Complete System**: Claude Code-style command discovery with fuzzy search
- **Message routing**: Determine intent (workflow creation, execution, help)
- **Context awareness**: Maintain conversation history and workflow state
- **Response formatting**: Apply MAO visual protocol with cycling tip messages
- **Auto-complete dropdown**: Categorized commands with keyboard navigation
- **Real-time suggestions**: Dynamic command filtering as user types
- **Workflow creation flow**: Natural goal → variables → JSON config → execution
- **Double-texting support**: Interrupt Mao like messenger experience

#### 3. Conversational Tool Access (`conversation_interface.py`)
- **Transparent tool usage**: Mao automatically uses available tools during chat
- **Freshness detection**: Automatically searches for current information when needed
- **Familiar UX**: Same experience users expect from Claude web interface
- **No workflow overhead**: Tools used conversationally, not as formal steps

#### 4. Welcome Flow (`onboarding/welcome_flow.py`)
- **New user onboarding**: Username entry, theme selection with preview
- **Return user detection**: Load existing preferences from `user_username.json`
- **Quick launch options**: Support for `--login`, `--continue`, `--config` modes
- **Theme preview**: Show visual examples with diff removal/addition colors
- **Cat vibes integration**: Configurable meow levels from serious to playful

#### 5. Workflow Creation Interface (`workflow/creation_interface.py`)
- **Goal conversation**: Natural language workflow creation with MAO visual protocol
- **Progressive refinement**: Clarify requirements through dialogue
- **Configuration options**: Model selection, preferences, constraints
- **Workflow preview**: Show planned phases with orchestration tree visualization
- **Live status cycling**: Dynamic activity messages during workflow creation

#### 6. Execution Monitor (`workflow/execution_monitor.py`)
- **Live progress tracking**: Real-time workflow execution with cycling status messages
- **Agent spawning visualization**: Triangle/circle shape progression
- **Phase transitions**: Tree structure showing workflow relationships
- **Interactive monitoring**: Accordion collapse/expand, pause, resume, modify execution
- **Mission control experience**: Multi-agent coordination display

---

## CLI Auto-Complete System Implementation

### Auto-Complete Architecture

#### Command Discovery System
```python
class CLICommandScanner:
    """Dynamic CLI command discovery from configs/cli/ directory"""
    
    def __init__(self, config_path: str = "./configs/cli/"):
        self.config_path = Path(config_path)
        self.commands = {}
        self.last_scan = None
        
    def scan_commands(self) -> Dict[str, Any]:
        """Scan configs/cli/ directory for all command configurations"""
        commands = {}
        
        for command_dir in self.config_path.iterdir():
            if command_dir.is_dir():
                json_file = command_dir / f"{command_dir.name}.json"
                if json_file.exists():
                    with open(json_file) as f:
                        command_data = json.load(f)
                        commands[command_dir.name] = {
                            **command_data,
                            "category": self.categorize_command(command_data)
                        }
        
        self.commands = commands
        self.last_scan = datetime.now()
        return commands
        
    def categorize_command(self, command_data: dict) -> str:
        """Categorize commands for organized display"""
        categories = {
            'BASICS': ['help', 'tools', 'models', 'providers'],
            'WORKFLOW_CREATION': ['goal', 'setup', 'update', 'fix_it'],
            'WORKFLOW_MANAGEMENT': ['continue', 'review', 'workflows', 'stats'],
            'USER_SETTINGS': ['config', 'login', 'logout', 'user_id', 'workflow_id', 'variables'],
            'QUICK_SETTINGS': ['set_model', 'default_provider', 'output'],
            'SYSTEM_OPERATIONS': ['chat', 'doctor', 'dry_run', 'verbose', 'logs']
        }
        
        command_name = command_data.get('command', '')
        for category, commands in categories.items():
            if command_name in commands:
                return category
        return 'OTHER'
```

#### Fuzzy Search Engine
```python
class FuzzySearchEngine:
    """Intelligent fuzzy search for command suggestions"""
    
    def search(self, query: str, commands: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Search commands with fuzzy matching and scoring"""
        if not query:
            return list(commands.values())[:limit]
            
        scored = []
        for cmd_name, cmd_data in commands.items():
            score = self.calculate_score(query, cmd_data)
            if score > 0:
                scored.append({**cmd_data, 'score': score})
                
        return sorted(scored, key=lambda x: x['score'], reverse=True)[:limit]
        
    def calculate_score(self, query: str, command: Dict[str, Any]) -> float:
        """Calculate relevance score for command"""
        searchable_text = f"{command.get('name', '')} {command.get('command', '')} {command.get('help', '')}".lower()
        query_lower = query.lower()
        
        # Exact match gets highest score
        if query_lower in searchable_text:
            return 100.0
            
        # Fuzzy matching based on character presence and order
        score = 0.0
        query_index = 0
        
        for char in searchable_text:
            if query_index < len(query_lower) and char == query_lower[query_index]:
                score += len(query_lower) - query_index
                query_index += 1
                
        return score if query_index == len(query_lower) else 0.0
```

#### Auto-Complete UI Component
```python
class CLIAutoCompleteSystem(Widget):
    """Claude Code-style auto-complete system for MAO CLI commands"""
    
    def __init__(self, config_dir: str):
        super().__init__()
        self.scanner = CLICommandScanner(f"{config_dir}/cli")
        self.fuzzy_search = FuzzySearchEngine()
        self.suggestions = []
        self.selected_index = 0
        self.is_visible = False
        
    async def get_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """Get auto-complete suggestions for query"""
        # Refresh commands if needed
        commands = self.scanner.scan_commands()
        
        # Get fuzzy search results
        suggestions = self.fuzzy_search.search(query, commands)
        
        self.suggestions = suggestions
        return suggestions
        
    def compose(self):
        """Compose auto-complete dropdown"""
        if not self.is_visible or not self.suggestions:
            return
            
        yield Container(
            *[self.create_command_item(cmd, idx) for idx, cmd in enumerate(self.suggestions)],
            id="autocomplete-dropdown"
        )
        
    def create_command_item(self, command: Dict[str, Any], index: int):
        """Create individual command item for dropdown"""
        is_selected = index == self.selected_index
        
        return Container(
            Horizontal(
                Static(f"/{command.get('command', '')}", classes="command-name"),
                Static(command.get('terminal_flag', ''), classes="command-flag"),
            ),
            Static(command.get('help', ''), classes="command-help"),
            classes="command-item selected" if is_selected else "command-item"
        )
        
    async def handle_key_navigation(self, key: str) -> bool:
        """Handle keyboard navigation in dropdown"""
        if not self.is_visible or not self.suggestions:
            return False
            
        if key == "down":
            self.selected_index = min(len(self.suggestions) - 1, self.selected_index + 1)
            await self.refresh()
            return True
        elif key == "up":
            self.selected_index = max(0, self.selected_index - 1)
            await self.refresh()
            return True
        elif key == "enter":
            if self.suggestions:
                selected_cmd = self.suggestions[self.selected_index]
                await self.select_command(selected_cmd)
            return True
        elif key == "escape":
            await self.hide()
            return True
            
        return False
        
    async def select_command(self, command: Dict[str, Any]):
        """Handle command selection"""
        # Emit command selection event
        self.post_message(CommandSelected(command))
        await self.hide()
        
    async def show(self, suggestions: List[Dict[str, Any]]):
        """Show auto-complete dropdown"""
        self.suggestions = suggestions
        self.selected_index = 0
        self.is_visible = True
        await self.refresh()
        
    async def hide(self):
        """Hide auto-complete dropdown"""
        self.is_visible = False
        self.suggestions = []
        await self.refresh()


class CommandSelected(Message):
    """Message sent when command is selected from auto-complete"""
    
    def __init__(self, command: Dict[str, Any]):
        super().__init__()
        self.command = command
```

#### CSS Styling for Auto-Complete
```css
#autocomplete-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: $surface;
    border: 1px solid $primary;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    max-height: 300px;
    overflow-y: auto;
    z-index: 1000;
}

.command-item {
    padding: 8px 12px;
    border-bottom: 1px solid $surface-variant;
    cursor: pointer;
    transition: background-color 0.2s;
}

.command-item:hover,
.command-item.selected {
    background: $primary-container;
    border-left: 3px solid $primary;
}

.command-name {
    color: $primary;
    font-family: monospace;
    font-weight: bold;
}

.command-flag {
    color: $on-surface-variant;
    font-size: 0.85em;
    margin-left: 8px;
}

.command-help {
    color: $on-surface-variant;
    font-size: 0.85em;
    margin-top: 4px;
}
```

---

## Implementation Tasks

### Phase 1: Foundation Application
1. **Create main application shell** with MAO visual protocol implementation
2. **Implement welcome flow** with username entry, theme selection with previews
3. **Build unified conversation interface** with workflow creation flow
4. **Implement CLI auto-complete system** with fuzzy search and categorized dropdown
5. **Create content translator** for ui_terminal.py with MAO orchestration trees
6. **Implement visual language system** with shape-based role identity
7. **Add user session management** with `user_username.json` configurations

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
# Preserve all ui_terminal.py functionality with MAO visual protocol
class ContentTranslator:
    def __init__(self, display_manager: DisplayManager):
        self.display = display_manager
        self.mao_colors = {
            'pink': '#ff49ff',      # AI actions requiring attention (ONLY BOLD)
            'yellow': '#f1d771',    # AI explanations and primary content  
            'light_blue': '#82d0ff', # AI-highlighted URLs/commands
            'white': '#ffffff',     # System responses
            'gray': '#bbbcbb',      # User input and secondary info
            'light_brown': '#7b714a' # Tree characters and metadata
        }
        
    def translate_workflow_status(self, status_message: str, role: str = 'orchestrator'):
        # Convert print statements to MAO visual protocol
        if role == 'orchestrator':
            shape = '▲' if 'active' in status_message else '△'
            color = self.mao_colors['pink'] if 'active' in status_message else self.mao_colors['yellow']
        else:
            shape = '●' if 'active' in status_message else '○' 
            color = self.mao_colors['yellow']
            
        return self.display.show_workflow_status(
            shape=shape,
            message=status_message,
            color=color,
            tree_prefix=self.determine_tree_position(status_message)
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