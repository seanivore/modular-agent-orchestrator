# Mao Application UI/UX Design  

## Philosophy 

Building for the future by building for the present. Perfect this terminal UI so that translating it larger, to web and mobile is that much easier and we have that much of a head start. 

### Architecture Concept 

Moving past the passive ticker monitoring agent feed, Mao provides a rich, interactive application experience. With only a few toggle options, majority of the interaction is done through chat. Active workflows are detailed with live monitoring of an animated display, making sure that when your workflow is complete, you can see all the information you need without scrolling up through printed statements forever. 

### Domain Overview 

The Terminal UI/UX System creates MAO's complete **interactive application experience** - transforming MAO from a monitoring utility into a comprehensive platform that rivals professional development tools like Claude Code. This is a **full application interface** designed for UI portability across terminal, web, and mobile platforms.

## Visual Identity Specifics 

- No emojis 
- Minimalist because form is function 
- Four or five colors only with strict usage psychology 
- Indentations and bullets also have strict usage psychology 
- Very little text; simple makes sure things are not overwhelming 

### Typography & Color System
- Leverage existing visual identity research from `6_MAO_VISUAL_IDENTITY.md`
- Apply Claude Code inspired typography principles
- Implement user-selected color preferences throughout interface
- Maintain consistent visual hierarchy and spacing

### Progress Visualization
- Icon-based progress indicators that are intuitive without explanation
- Color coding for different states (pending, in-progress, completed)
- Minimal visual clutter while providing clear status information
- Responsive to different terminal sizes and capabilities

## UX Design Specifications 

### Setup Configurations 

- User preferences stored in Memory MCP for session persistence
- Color choices applied throughout all UI components
- Setup completion tracked for future sessions

### Add To `protocol.md` Document 

- Claude has no script 
  - They are already helpful as they are 
  - They need only know the JSON variables needed 

- Claudes bigger role will be to anticipate needs 
  - Leave someone be if they're already on a role with their idea and laying it all out 
  - Help ask questions if they're hesitant or thinking 

## UX Per User Session 

### First Time Setup 

- First time user gets asked to choose a text color and highlight color
- Concise text below text input field encourages User to describe their project or ask Claude for ideas 
- Icon indicate necessary variables, changing color as they're provided 

#### Implementation Specification

```python
# interfaces/terminal/first_time_setup.py
class FirstTimeSetup:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.visual_config = VisualConfigManager()
        
    def run_first_time_setup(self):
        """Complete first-time user experience"""
        
        # Welcome and introduction
        self._display_welcome()
        
        # Color selection (like Claude Code)
        color_preferences = self._run_color_selection()
        
        # Save preferences
        self.visual_config.save_user_preferences(color_preferences)
        
        # Create user profile in Memory MCP
        self.memory_mcp.create_entities([{
            "name": "user-profile",
            "entityType": "user-config",
            "observations": [
                f"First setup completed: {datetime.now().isoformat()}",
                f"Color preferences: {color_preferences}",
                "Setup status: completed"
            ]
        }])
        
        # Transition to main interface
        return self._transition_to_main_interface(color_preferences)
    
    def _run_color_selection(self):
        """Interactive color selection like Claude Code"""
        colors = {
            "text_colors": [
                ("Default", "#FFFFFF"),
                ("Warm White", "#FFF8E7"),
                ("Cool Blue", "#E6F3FF"),
                ("Soft Green", "#F0FFF0"),
                ("Cream", "#FFFDD0")
            ],
            "highlight_colors": [
                ("Blue", "#0066CC"),
                ("Green", "#00AA44"),
                ("Purple", "#8A2BE2"),
                ("Orange", "#FF8C00"),
                ("Teal", "#008B8B")
            ]
        }
        
        print("🐱 Mao! Choose the colors that look best in your terminal.")
        print("Continue with other settings on default (recommended)?\n")
        
        # Text color selection
        print("📝 Text Colors:")
        for i, (name, hex_code) in enumerate(colors["text_colors"], 1):
            print(f"  {i}. {name} {self._color_preview(hex_code)}")
        
        text_choice = self._get_user_choice(len(colors["text_colors"]))
        selected_text = colors["text_colors"][text_choice - 1]
        
        # Highlight color selection
        print(f"\n✨ Highlight Colors (with {selected_text[0]} text):")
        for i, (name, hex_code) in enumerate(colors["highlight_colors"], 1):
            preview = self._color_combination_preview(selected_text[1], hex_code)
            print(f"  {i}. {name} {preview}")
        
        highlight_choice = self._get_user_choice(len(colors["highlight_colors"]))
        selected_highlight = colors["highlight_colors"][highlight_choice - 1]
        
        return {
            "text_color": selected_text,
            "highlight_color": selected_highlight,
            "theme": "custom"
        }
    
    def _display_welcome(self):
        """Show Mao welcome message"""
        welcome_text = f"""
╭─────────────────────────────────────────────────────────────────────────────╮
│  How Mao I /help you? 🐱          /config for your current setup            │
│  cwd: /Users/seanivore/Development/modular-agent-orchestrator               │
╰─────────────────────────────────────────────────────────────────────────────╯
"""
        print(welcome_text)
```

### Returning User & Complete Setup 

- Next screen is the main page with just a few tips and a chat text input field
- Any indicators that change as the workflow is planned are simple and only understood by return users 

#### Implementation Specification

```python
# interfaces/terminal/main_interface.py
class MainInterface:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.workflow_engine = WorkflowEngine()
        self.visual_config = VisualConfigManager()
        self.progress_tracker = ProgressTracker()
        
    def display_main_interface(self):
        """Show main Mao interface with chat and progress tracking"""
        
        # Load user preferences
        preferences = self.visual_config.load_user_preferences()
        
        # Display header with progress icons
        self._display_header_with_progress()
        
        # Show chat interface
        self._display_chat_interface()
        
        # Show guidance
        self._display_guidance()
        
        # Start input loop
        self._start_chat_loop()
    
    def _display_header_with_progress(self):
        """Show Mao header with variable progress icons"""
        
        # Get current workflow context if any
        active_workflows = self.memory_mcp.search_nodes("active-workflow")
        
        if active_workflows:
            workflow_id = active_workflows[0].get("name", "").replace("workflow-", "")
            progress_state = self.progress_tracker.get_progress_state(workflow_id)
        else:
            progress_state = self.progress_tracker.get_initial_state()
        
        # Display header with icons
        header = f"""
╭─────────────────────────────────────────────────────╮
│  Welcome to Mao's House! 🐱                         │
│                                                     │
│  {self._render_progress_icons(progress_state)}      │
╰─────────────────────────────────────────────────────╯
"""
        print(header)
    
    def _render_progress_icons(self, progress_state):
        """Render progress icons with color changes"""
        icons = {
            "goal": ("🎯", "Goal defined"),
            "workflow": ("🔄", "Workflow planned"), 
            "tools": ("🛠️", "Tools configured"),
            "agents": ("🤖", "Agents ready"),
            "execution": ("⚡", "Executing")
        }
        
        rendered_icons = []
        for key, (icon, description) in icons.items():
            status = progress_state.get(key, "pending")
            
            if status == "completed":
                colored_icon = self._apply_highlight_color(icon)
            elif status == "in_progress":
                colored_icon = self._apply_warning_color(icon)
            else:
                colored_icon = self._apply_muted_color(icon)
            
            rendered_icons.append(colored_icon)
        
        return " ".join(rendered_icons)
    
    def _display_chat_interface(self):
        """Show chat interface area as simple, no borders"""
        chat_area = """"""
        print(chat_area)
    
    def _display_guidance(self):
        """Show simple guidance text"""
        guidance = """
Describe your project or ask Claude for ideas. 

Available commands:
  /workflows    - View and select from existing workflows
  /status      - Check current workflow status  
  /help        - Show all available commands
  !command     - Pass command directly to terminal

"""
        print(guidance)
```

### Progress Tracking System

```python
# interfaces/terminal/progress_tracker.py
class ProgressTracker:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        
    def get_progress_state(self, workflow_id: str):
        """Get current progress state for workflow"""
        context = self.memory_mcp.get_workflow_context(workflow_id)
        
        if not context:
            return self.get_initial_state()
        
        # Analyze workflow context to determine progress
        observations = context.get("observations", [])
        
        state = {
            "goal": "completed" if any("User goal:" in obs for obs in observations) else "pending",
            "workflow": "completed" if any("Workflow created" in obs for obs in observations) else "pending", 
            "tools": "completed" if any("Tool requested:" in obs for obs in observations) else "pending",
            "agents": "completed" if any("Agent handoff" in obs for obs in observations) else "pending",
            "execution": "in_progress" if any("execution started" in obs for obs in observations) else "pending"
        }
        
        return state
    
    def get_initial_state(self):
        """Get initial progress state"""
        return {
            "goal": "pending",
            "workflow": "pending", 
            "tools": "pending",
            "agents": "pending",
            "execution": "pending"
        }
    
    def update_progress(self, workflow_id: str, component: str, status: str):
        """Update progress for specific component"""
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Progress update: {component} -> {status}"
        )
```

### **CLI Integration Points**
- Command routing through JSON-based argument system
- Interface methods for all CLI commands (`--stats`, `--workflows`, etc.)
- Custom command execution and registration
- In-app command variants (`/stats`, `/workflows`)

#### Mao CLI Flag Arguments & Application Commands 

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

##### Example Terminal Modifier Commands  

```bash
    mao mao                                # Start application
    mao --goal create marketing plan       # Execute goal directly
    mao --stats --verbose                  # Detailed system statistics
    mao --setup ./my-workflow.json         # Setup new workflow
    mao --workflows                        # List all workflows
    mao --doctor                           # Check installation health
```

##### Example Application Commands  

```bash
    /restart                               # Restart application
    /goal create marketing plan            # Execute goal directly
    /stats                                 # Detailed system statistics
    /setup ./my-workflow.json              # Setup new workflow
    /workflows                             # List all workflows
    /doctor                                # Check installation health
```

### CLI Interface Methods  

```python
# interfaces/terminal/interface_methods.py (NEW - Required for CLI)
class TerminalInterfaceMethods:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.workflow_engine = WorkflowEngine()
        self.tool_manager = ToolManager()
        
    def show_stats(self, verbose: bool = False):
        """Display system performance and orchestrator statistics"""
        stats = {
            "active_workflows": len(self.memory_mcp.search_nodes("active-workflow")),
            "completed_workflows": len(self.memory_mcp.search_nodes("completed-workflow")),
            "available_tools": len(self.tool_manager.discover_all_tools()),
            "system_uptime": self._get_system_uptime(),
            "memory_usage": self._get_memory_usage()
        }
        
        if verbose:
            stats.update(self._get_detailed_stats())
            
        self._display_stats_ui(stats, verbose)
    
    def list_workflows(self):
        """Show all configured workflows and their status"""
        workflows = self.memory_mcp.search_nodes("workflow")
        workflow_list = []
        
        for workflow in workflows:
            workflow_id = workflow.get("name", "").replace("workflow-", "")
            status = self._get_workflow_status(workflow_id)
            workflow_list.append({
                "id": workflow_id,
                "goal": self._extract_goal(workflow),
                "status": status,
                "last_activity": self._get_last_activity(workflow)
            })
        
        self._display_workflows_ui(workflow_list)
    
    def setup_workflow(self, config_file: str):
        """Setup new workflow from JSON configuration file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            workflow_id = config.get("workflow_id") or f"workflow-{uuid4().hex[:8]}"
            
            # Create workflow using engine
            result = self.workflow_engine.create_workflow_from_config(workflow_id, config)
            
            self._display_setup_success(workflow_id, result)
            
        except Exception as e:
            self._display_setup_error(config_file, str(e))
    
    def execute_goal(self, goal: str):
        """Create and execute workflow from goal description"""
        workflow_id = f"goal-{uuid4().hex[:8]}"
        
        # Create workflow from goal
        result = self.workflow_engine.create_workflow_from_goal(workflow_id, goal)
        
        # Start execution
        self.workflow_engine.execute_workflow(workflow_id)
        
        self._display_goal_execution(workflow_id, goal)
    
    def start_chat(self, initial_message: str = None):
        """Start interactive chat interface"""
        self._transition_to_chat_mode(initial_message)
    
    def handle_in_app_command(self, command: str, args: list = None):
        """Handle in-app slash commands like /stats, /workflows"""
        command = command.lstrip('/')  # Remove leading slash
        
        if command == "stats":
            self.show_stats(verbose="verbose" in (args or []))
        elif command == "workflows":
            self.list_workflows()
        elif command == "restart":
            self._restart_application()
        elif command == "exit":
            self._exit_application()
        else:
            self._display_unknown_command(command)
    
    def handle_critical_error(self, error: Exception):
        """Handle critical errors with graceful degradation"""
        error_id = uuid4().hex[:8]
        
        # Log error to Memory MCP if possible
        try:
            self.memory_mcp.create_entities([{
                "name": f"critical-error-{error_id}",
                "entityType": "system-error",
                "observations": [
                    f"Error: {str(error)}",
                    f"Type: {type(error).__name__}",
                    f"Timestamp: {datetime.now().isoformat()}"
                ]
            }])
        except:
            pass  # Can't log to Memory MCP, continue with display
        
        self._display_critical_error(error_id, error)
```

#### Integration Points 

- CLI commands route through these interface methods
- Memory MCP provides data for statistics and workflow listing
- Workflow Engine handles execution and setup operations
- Error handling maintains application stability
- In-app commands provide alternative interaction patterns

### Tone Bell Chime

- Two or three different tones for different things 
- Completed phase with agent's return 
- Next agent discharged 
- Workflow completion 
- Planned human touch-point 

## Design Specifications 

### Language Is TypeScript/Node.js 

  - For the rich ecosystem 
  - Libraries `ink` React for terminals or `blessed`
  - Easy npm distribution 
  - Dev smart because they have node 
  - Works everywhere Node works 
  - Good type safety for complex tools
  - Easy to integrate with Claude's APIs

  - AI mentioned that the python versus TypeScript would be complicated work. I questioned it because I didn't understand the logic of how, with python running the insides, and TypeScript the UI, why it would matter or make things complicated. They said they were overthinking it; so I'm mentioning it here so no one overthinks it. 

## UI Details 

### Real-Time Progress UI System 
- Progress indicators 
- Connect to orchestrator execution monitoring
- Needs terminal UI foundation, orchestrator core

### UI Details During Workflow Execution 

The terminal UI foundation is **exceptionally well-prepared** with:
- **Professional foundation files** ready for integration
- **Comprehensive implementation SPEC** with clear task breakdown  
- **Clean architectural approach** preserving existing functionality
- **Direct integration path** to orchestrator without complex interception

This represents **excellent preparation work** that significantly reduces implementation risk. The foundation quality rivals professional terminal applications, and the integration approach is architecturally sound.

### Workflow Monitoring System Requirements 

- Live tracking UI for the User so they can watch everything that is happening
- Agent(s) have a live token counter just like we have in the IDE when I'm typing
- Bell tone when the agent is done so that the User can do other things
- Agent and Claude meet and talk directly

### Implementation Specification

```python
# interfaces/terminal/live_monitor.py
class LiveWorkflowMonitor:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        self.audio_notifier = AudioNotifier()
        self.token_tracker = TokenTracker()
        
    def start_monitoring(self, workflow_id: str):
        """Start live monitoring for workflow execution"""
        
        print("🔴 Live Monitoring Started")
        print("╭─────────────────────────────────────────────────────╮")
        print("│                 MAO Live Monitor                   │") 
        print("╰─────────────────────────────────────────────────────╯")
        
        # Initialize monitoring display
        self._initialize_monitor_display(workflow_id)
        
        # Start monitoring loop
        self._start_monitoring_loop(workflow_id)
    
    def _initialize_monitor_display(self, workflow_id: str):
        """Set up the monitoring display"""
        
        # Get workflow context
        context = self.memory_mcp.get_workflow_context(workflow_id)
        workflow_info = self._extract_workflow_info(context)
        
        # Display workflow overview
        overview = f"""
┌─ Workflow Overview ────────────────────────────────┐
│ Goal: {workflow_info['goal'][:45]}...                 │
│ Phases: {workflow_info['total_phases']} | Current: {workflow_info['current_phase']}              │
│ Estimated Cost: ${workflow_info['estimated_cost']:.2f}                      │
└────────────────────────────────────────────────────┘

┌─ Agent Status ─────────────────────────────────────┐
│                                                    │
│  🤖 Agents: Preparing...                          │
│  📝 Tokens: 0 / 200,000                           │
│  ⏱️  Time: 00:00:00                               │
│                                                    │
└────────────────────────────────────────────────────┘

┌─ Live Activity Feed ───────────────────────────────┐
│                                                    │
│  [Live updates will appear here]                   │
│                                                    │
└────────────────────────────────────────────────────┘
"""
        print(overview)
    
    def _start_monitoring_loop(self, workflow_id: str):
        """Main monitoring loop with live updates"""
        
        start_time = time.time()
        last_update = None
        
        while True:
            try:
                # Check for workflow updates
                current_state = self.memory_mcp.get_workflow_context(workflow_id)
                
                if self._has_new_activity(current_state, last_update):
                    self._update_display(workflow_id, current_state, start_time)
                    last_update = current_state
                
                # Check if workflow completed
                if self._is_workflow_complete(current_state):
                    self._show_completion_notification(workflow_id)
                    self.audio_notifier.play_completion_sound()
                    break
                
                # Check for agent completion
                if self._agent_completed(current_state, last_update):
                    self.audio_notifier.play_notification_sound()
                    self._update_agent_status(current_state)
                
                time.sleep(2)  # Update every 2 seconds
                
            except KeyboardInterrupt:
                print("\n⏸️  Monitoring paused. Workflow continues in background.")
                break
            except Exception as e:
                print(f"\n⚠️  Monitoring error: {e}")
                time.sleep(5)
    
    def _update_display(self, workflow_id: str, current_state: dict, start_time: float):
        """Update the live display with current status"""
        
        # Calculate runtime
        runtime = time.time() - start_time
        runtime_str = self._format_runtime(runtime)
        
        # Get token usage
        token_usage = self.token_tracker.get_current_usage(workflow_id)
        
        # Get latest activity
        latest_activities = self._extract_latest_activities(current_state, limit=5)
        
        # Clear and redraw (simplified approach)
        print("\033[H\033[J")  # Clear screen
        
        # Redraw header
        print("🔴 Live Monitoring - Workflow Active")
        print("╭─────────────────────────────────────────────────────╮")
        print("│                 MAO Live Monitor                   │")
        print("╰─────────────────────────────────────────────────────╯")
        
        # Update agent status
        agent_status = f"""
┌─ Agent Status ─────────────────────────────────────┐
│                                                    │
│  🤖 Agents: {self._get_agent_status(current_state)}                        │
│  📝 Tokens: {token_usage['used']:,} / {token_usage['limit']:,}                     │
│  ⏱️  Time: {runtime_str}                               │
│  💰 Cost: ${token_usage['cost']:.2f}                               │
│                                                    │
└────────────────────────────────────────────────────┘
"""
        print(agent_status)
        
        # Update activity feed
        activity_feed = "┌─ Live Activity Feed ───────────────────────────────┐\n"
        activity_feed += "│                                                    │\n"
        
        for activity in latest_activities:
            timestamp = activity['timestamp'][-8:-3]  # Get HH:MM from ISO timestamp
            message = activity['message'][:44]  # Truncate to fit
            activity_feed += f"│  {timestamp} | {message:<44} │\n"
        
        activity_feed += "│                                                    │\n"
        activity_feed += "└────────────────────────────────────────────────────┘"
        
        print(activity_feed)
        
        # Control instructions
        print("\n💡 Press Ctrl+C to pause monitoring (workflow continues)")
```

### **Audio Notification System**

```python
# interfaces/terminal/audio_notifier.py
class AudioNotifier:
    def __init__(self):
        self.enabled = True
        self.sound_library = SoundLibrary()
    
    def play_completion_sound(self):
        """Play sound when workflow completes"""
        if self.enabled:
            # Pleasant completion chime
            self._play_sound("completion_chime.wav")
            print("🔔 Workflow completed!")
    
    def play_notification_sound(self):
        """Play sound when agent completes phase"""
        if self.enabled:
            # Gentle notification bell
            self._play_sound("notification_bell.wav")
            print("🔔 Agent phase completed!")
    
    def play_error_sound(self):
        """Play sound for errors"""
        if self.enabled:
            # Subtle error tone
            self._play_sound("error_tone.wav")
    
    def _play_sound(self, sound_file: str):
        """Play sound file (implementation depends on platform)"""
        try:
            # Platform-specific implementation
            if sys.platform == "darwin":  # macOS
                os.system(f"afplay {sound_file}")
            elif sys.platform == "linux":  # Linux
                os.system(f"aplay {sound_file}")
            elif sys.platform == "win32":  # Windows
                import winsound
                winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        except Exception:
            # Fallback to system bell
            print("\a")  # ASCII bell character
```

### **Token Tracking System**

```python
# interfaces/terminal/token_tracker.py
class TokenTracker:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        
    def get_current_usage(self, workflow_id: str):
        """Get current token usage for workflow"""
        
        # Get workflow context
        context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Extract token usage from observations
        observations = context.get("observations", [])
        
        token_data = {
            "used": 0,
            "limit": 200000,  # Default context limit
            "cost": 0.0,
            "efficiency": 1.0
        }
        
        # Parse token usage from activity log
        for obs in observations:
            if "tokens used:" in obs.lower():
                # Extract token count from observation
                try:
                    token_count = int(re.search(r'tokens used: (\d+)', obs.lower()).group(1))
                    token_data["used"] += token_count
                except (AttributeError, ValueError):
                    pass
            
            if "cost:" in obs.lower():
                # Extract cost from observation
                try:
                    cost = float(re.search(r'cost: \$?([\d.]+)', obs.lower()).group(1))
                    token_data["cost"] += cost
                except (AttributeError, ValueError):
                    pass
        
        # Calculate efficiency
        if token_data["limit"] > 0:
            token_data["efficiency"] = token_data["used"] / token_data["limit"]
        
        return token_data
    
    def update_token_usage(self, workflow_id: str, tokens_used: int, cost: float):
        """Update token usage tracking"""
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Token usage: {tokens_used} tokens, cost: ${cost:.2f}"
        )
```
### Integration Points

- Live monitoring pulls state from Memory MCP real-time
- Token tracking integrates with tool execution costs
- Audio notifications provide non-intrusive awareness
- Display updates preserve workflow execution focus

## Implementation Sequence

1. Create `interfaces/terminal/first_time_setup.py` with color selection
2. Implement user preference storage with Memory MCP
3. Build transition to main interface
4. Test complete first-time user flow
5. Create `interfaces/terminal/main_interface.py` with progress tracking
6. Implement progress icon system with visual state management
7. Add chat interface integration with Workflow Engine
8. Test interface responsiveness and visual feedback
9. Create `interfaces/terminal/live_monitor.py` with real-time tracking
10. Implement audio notification system
11. Add token tracking with cost monitoring
12. Test complete monitoring experience with agent workflows
13. Integrate all components with existing domains
14. Test complete user journey from setup to monitoring
15. Polish visual elements and transitions
16. Validate accessibility and user experience

## **Configuration Requirements**

### **Visual Configuration Schema**
```json
{
  "user_preferences": {
    "text_color": ["Warm White", "#FFF8E7"],
    "highlight_color": ["Blue", "#0066CC"], 
    "theme": "custom",
    "first_setup_completed": true,
    "accessibility": {
      "high_contrast": false,
      "large_text": false,
      "reduced_motion": false
    }
  },
  "interface_settings": {
    "progress_icons": true,
    "audio_notifications": true,
    "live_monitoring": true,
    "token_display": true,
    "demeanor_adaptation": true
  },
  "monitoring_config": {
    "update_interval": 2000,
    "max_activity_items": 5,
    "token_warning_threshold": 0.8,
    "cost_alert_threshold": 10.00
  }
}
```

### **Audio Assets Required**
- `completion_chime.wav` - Pleasant workflow completion sound
- `notification_bell.wav` - Gentle agent phase completion sound  
- `error_tone.wav` - Subtle error notification sound
- Platform-specific fallbacks for accessibility

## Visual Design Sketches 

```
Phase 2: Content Analysis [████████████░░░░░░░░] 65% 🔄 In progress...
├─ Market Gap Analysis   [███████████████████] ✅ 15 gaps identified
├─ Voice & Tone Study   [███████████░░░░░░░░░] 🔄 In progress...
├─ Channel Assessment   [░░░░░░░░░░░░░░░░░░░░] ⏳ Queued
└─ Framework Selection  [░░░░░░░░░░░░░░░░░░░░] ⏳ Queued

💰 Cost: $0.23/$0.75 budget | 🎯 Quality: 8.7/10 target | ⏱️ ETA: 8m 45s
🧠 Agent: Content Strategy Analyst using claude-sonnet-4 via anthropic-direct
```
```
🎉 WORKFLOW COMPLETED SUCCESSFULLY
════════════════════════════════════════════════

📊 Performance Summary:
├─ Total Duration:     11m 47s (estimated: 12-15m)
├─ Total Cost:         $0.34 (budgeted: $0.75) 
├─ Quality Score:      9.2/10 (target: 8.0+)
├─ Cache Hits:         23% (saved $0.11)
└─ Success Rate:       100% (4/4 phases completed)

📁 Deliverables Created:
├─ 📄 Content_Strategy_Executive_Summary.md
├─ 📄 Market_Research_Analysis.md
└─ 🔗 Quick Actions: [📧 Email Summary] [📋 Copy Key Points]
```
