# User Interface Patterns - Terminal UI and Node.js ↔ Python Communication

## Introduction

MAO implements sophisticated user interface patterns that bridge Node.js terminal applications with Python backend services through structured subprocess communication. These patterns provide professional CLI experiences while maintaining the LOCAL-only architecture and enabling rich terminal interactions.

## Subprocess Communication Architecture

### Terminal Interface Coordination

The main interface coordinates between Node.js frontend and Python backend:

```python
# interfaces/ui_terminal.py
class TerminalInterface:
    def __init__(self):
        self.mcp_hub = None
        self.logger = setup_logger(__name__)
        self.command_registry = {}
        self.display_formatters = {}
        
    async def handle_subprocess_command(self, command: str, data: dict = None):
        """Handle commands from Node.js subprocess with structured responses"""
        try:
            # Route command to appropriate handler
            if command in self.command_registry:
                handler = self.command_registry[command]
                result = await handler(data or {})
                
                # Ensure structured response for subprocess communication
                if not isinstance(result, dict):
                    result = {"content": result, "display_type": "text"}
                    
                # Add metadata for Node.js processing
                result.update({
                    "command": command,
                    "timestamp": datetime.utcnow().isoformat(),
                    "subprocess_safe": True
                })
                
                return result
            else:
                return {
                    "status": "error",
                    "message": f"Unknown command: {command}",
                    "display_type": "error",
                    "subprocess_safe": True
                }
                
        except Exception as e:
            self.logger.error(f"Subprocess command failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "display_type": "error",
                "subprocess_safe": True,
                "error_type": type(e).__name__
            }
            
    def register_command_handler(self, command: str, handler: callable, display_type: str = "default"):
        """Register command handler with display type specification"""
        self.command_registry[command] = handler
        self.display_formatters[command] = display_type
        
    async def format_for_terminal_display(self, data: dict, rich_enabled: bool = True):
        """Format data for rich terminal display when running standalone"""
        display_type = data.get("display_type", "default")
        
        formatters = {
            "workflow_created": self.format_workflow_created,
            "help_categories": self.format_help_categories,
            "real_time_stats": self.format_real_time_stats,
            "tool_results": self.format_tool_results,
            "error": self.format_error_display
        }
        
        formatter = formatters.get(display_type, self.format_default)
        
        if rich_enabled:
            try:
                from rich.console import Console
                from rich.panel import Panel
                from rich.table import Table
                
                console = Console()
                formatted_output = await formatter(data, console)
                console.print(formatted_output)
                
            except ImportError:
                # Fallback to plain text formatting
                formatted_output = await formatter(data, None)
                print(formatted_output)
        else:
            formatted_output = await formatter(data, None)
            print(formatted_output)
            
        return formatted_output
```

### Node.js Integration Patterns

The Node.js frontend implements structured subprocess communication:

```javascript
// Node.js Subprocess Integration Example
const { spawn } = require('child_process');
const path = require('path');

class MAOInterface {
    constructor() {
        this.pythonExecutable = 'python3';
        this.interfacePath = path.join(__dirname, '..', 'interfaces', 'ui_terminal.py');
        this.activeProcesses = new Map();
    }
    
    async executeCommand(command, data = null, options = {}) {
        return new Promise((resolve, reject) => {
            const processId = this.generateProcessId();
            
            // Prepare subprocess arguments
            const args = [
                this.interfacePath,
                '--command', command,
                '--subprocess-mode'
            ];
            
            if (data) {
                args.push('--data', JSON.stringify(data));
            }
            
            // Spawn Python subprocess
            const pythonProcess = spawn(this.pythonExecutable, args, {
                stdio: ['pipe', 'pipe', 'pipe'],
                timeout: options.timeout || 30000
            });
            
            this.activeProcesses.set(processId, pythonProcess);
            
            let stdout = '';
            let stderr = '';
            
            pythonProcess.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            pythonProcess.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            pythonProcess.on('close', (code) => {
                this.activeProcesses.delete(processId);
                
                if (code === 0) {
                    try {
                        // Parse structured response from Python
                        const result = JSON.parse(stdout);
                        
                        // Validate subprocess-safe response
                        if (result.subprocess_safe) {
                            resolve(result);
                        } else {
                            reject(new Error('Invalid subprocess response format'));
                        }
                        
                    } catch (parseError) {
                        reject(new Error(`Failed to parse Python response: ${parseError.message}`));
                    }
                } else {
                    reject(new Error(`Python process exited with code ${code}: ${stderr}`));
                }
            });
            
            pythonProcess.on('error', (error) => {
                this.activeProcesses.delete(processId);
                reject(new Error(`Process spawn failed: ${error.message}`));
            });
        });
    }
    
    async handleWorkflowCommand(goalText, options = {}) {
        """Handle workflow creation with structured response processing"""
        try {
            const result = await this.executeCommand('goal', {
                goal_text: goalText,
                workflow_options: options
            });
            
            // Route based on display_type for appropriate UI rendering
            switch (result.display_type) {
                case 'workflow_created':
                    return this.renderWorkflowCreated(result);
                    
                case 'error':
                    return this.renderError(result);
                    
                default:
                    return this.renderDefault(result);
            }
            
        } catch (error) {
            console.error('Workflow command failed:', error);
            return this.renderError({
                message: error.message,
                display_type: 'error'
            });
        }
    }
    
    renderWorkflowCreated(result) {
        """Render workflow creation success in Node.js terminal"""
        const { workflow_id, goal, status } = result;
        
        console.log(`\n✅ Workflow Created Successfully`);
        console.log(`📋 Workflow ID: ${workflow_id}`);
        console.log(`🎯 Goal: ${goal}`);
        console.log(`📊 Status: ${status}`);
        
        if (result.next_steps) {
            console.log(`\n📝 Next Steps:`);
            result.next_steps.forEach((step, index) => {
                console.log(`   ${index + 1}. ${step}`);
            });
        }
        
        return {
            success: true,
            workflow_id,
            rendered: true
        };
    }
}
```

## CLI Command Patterns

### Git-Style Command Organization

MAO implements professional Git-style CLI patterns:

```python
# CLI command structure with Git-style organization
class CLICommandStructure:
    def __init__(self):
        self.command_categories = {
            "workflow": {
                "commands": ["goal", "continue", "status", "workflows"],
                "description": "Workflow management and execution",
                "icon": "🔄"
            },
            "data": {
                "commands": ["memory", "stats", "logs"],
                "description": "Data and analytics management", 
                "icon": "📊"
            },
            "config": {
                "commands": ["setup", "config", "tools", "models"],
                "description": "Configuration and system setup",
                "icon": "⚙️"
            },
            "utility": {
                "commands": ["help", "dry-run", "output-directory"],
                "description": "Utility and helper commands",
                "icon": "🛠️"
            }
        }
        
    async def generate_help_display(self, category: str = None):
        """Generate Git-style help display with categorization"""
        if category:
            return await self.generate_category_help(category)
            
        # Main help display
        help_structure = {
            "display_type": "help_categories",
            "title": "MAO - Modular Agent Orchestrator",
            "description": "LOCAL AI workflow orchestration and automation",
            "categories": []
        }
        
        for cat_name, cat_info in self.command_categories.items():
            category_entry = {
                "name": cat_name,
                "description": cat_info["description"],
                "icon": cat_info["icon"],
                "commands": []
            }
            
            for command in cat_info["commands"]:
                command_info = await self.get_command_info(command)
                category_entry["commands"].append({
                    "name": command,
                    "description": command_info.get("description", ""),
                    "usage": command_info.get("usage", f"mao {command}")
                })
                
            help_structure["categories"].append(category_entry)
            
        return help_structure
        
    async def generate_category_help(self, category: str):
        """Generate detailed help for specific category"""
        if category not in self.command_categories:
            return {
                "display_type": "error",
                "message": f"Unknown category: {category}"
            }
            
        cat_info = self.command_categories[category]
        
        category_help = {
            "display_type": "category_help",
            "category": category,
            "description": cat_info["description"],
            "icon": cat_info["icon"],
            "commands": []
        }
        
        for command in cat_info["commands"]:
            command_detail = await self.get_detailed_command_info(command)
            category_help["commands"].append(command_detail)
            
        return category_help
```

### Command Execution with Progress Tracking

Commands provide real-time progress feedback:

```python
# Progress tracking for long-running commands
class ProgressTrackingCommand:
    def __init__(self, command_name: str):
        self.command_name = command_name
        self.progress_callback = None
        self.progress_data = {
            "current_step": 0,
            "total_steps": 0,
            "status": "initializing",
            "details": ""
        }
        
    async def execute_with_progress(self, parameters: dict, progress_callback=None):
        """Execute command with progress tracking for UI feedback"""
        self.progress_callback = progress_callback
        
        try:
            # Initialize progress tracking
            await self.update_progress(0, 5, "Initializing command", "Setting up environment")
            
            # Step 1: Validate parameters
            await self.update_progress(1, 5, "Validating parameters", "Checking input parameters")
            validation_result = await self.validate_parameters(parameters)
            
            if not validation_result["valid"]:
                return {
                    "status": "error",
                    "message": "Parameter validation failed",
                    "errors": validation_result["errors"],
                    "display_type": "error"
                }
                
            # Step 2: Initialize dependencies
            await self.update_progress(2, 5, "Initializing dependencies", "Setting up required services")
            await self.initialize_dependencies()
            
            # Step 3: Execute main logic
            await self.update_progress(3, 5, "Executing command", "Running main command logic")
            result = await self.execute_main_logic(parameters)
            
            # Step 4: Process results
            await self.update_progress(4, 5, "Processing results", "Formatting output")
            formatted_result = await self.format_command_result(result)
            
            # Step 5: Complete
            await self.update_progress(5, 5, "Complete", "Command execution finished")
            
            return {
                "status": "success",
                "result": formatted_result,
                "display_type": self.determine_display_type(formatted_result),
                "execution_metadata": {
                    "command": self.command_name,
                    "duration_ms": self.calculate_execution_duration(),
                    "steps_completed": 5
                }
            }
            
        except Exception as e:
            await self.update_progress(
                self.progress_data["current_step"], 
                self.progress_data["total_steps"],
                "Error",
                f"Command failed: {str(e)}"
            )
            
            return {
                "status": "error",
                "message": str(e),
                "display_type": "error",
                "progress_data": self.progress_data
            }
            
    async def update_progress(self, current: int, total: int, status: str, details: str):
        """Update progress and notify callback"""
        self.progress_data.update({
            "current_step": current,
            "total_steps": total,
            "status": status,
            "details": details,
            "percentage": (current / total) * 100 if total > 0 else 0
        })
        
        # Notify Node.js frontend of progress update
        if self.progress_callback:
            await self.progress_callback(self.progress_data)
            
        # Log progress for terminal display
        logger.info(f"{self.command_name} Progress: {status} ({current}/{total}) - {details}")
```

## Rich Terminal Integration

### Advanced Formatting with Graceful Fallback

The system provides rich terminal formatting with automatic fallback:

```python
# Rich terminal formatting with graceful fallback
class RichTerminalFormatter:
    def __init__(self):
        self.rich_available = False
        self.console = None
        
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich.progress import Progress, SpinnerColumn, TextColumn
            from rich.syntax import Syntax
            
            self.console = Console()
            self.rich_available = True
            self.rich_components = {
                "Console": Console,
                "Table": Table,
                "Panel": Panel,
                "Progress": Progress,
                "Syntax": Syntax,
                "SpinnerColumn": SpinnerColumn,
                "TextColumn": TextColumn
            }
            
        except ImportError:
            # Graceful fallback to plain text
            self.rich_available = False
            logger.info("Rich library not available, using plain text formatting")
            
    async def format_workflow_status(self, workflow_data: dict):
        """Format workflow status with rich display or plain text fallback"""
        if self.rich_available:
            return await self.format_workflow_status_rich(workflow_data)
        else:
            return await self.format_workflow_status_plain(workflow_data)
            
    async def format_workflow_status_rich(self, workflow_data: dict):
        """Rich terminal formatting for workflow status"""
        Table = self.rich_components["Table"]
        Panel = self.rich_components["Panel"]
        
        # Create main workflow table
        workflow_table = Table(title=f"Workflow: {workflow_data['workflow_id']}")
        workflow_table.add_column("Property", style="bold blue")
        workflow_table.add_column("Value", style="green")
        
        workflow_table.add_row("Goal", workflow_data["goal"])
        workflow_table.add_row("Status", workflow_data["status"])
        workflow_table.add_row("Progress", f"{workflow_data.get('progress', 0)}%")
        workflow_table.add_row("Created", workflow_data.get("created_at", "Unknown"))
        
        # Create agents table if available
        if "agents" in workflow_data:
            agents_table = Table(title="Active Agents")
            agents_table.add_column("Agent", style="bold cyan")
            agents_table.add_column("Status", style="yellow")
            agents_table.add_column("Last Action", style="white")
            
            for agent in workflow_data["agents"]:
                agents_table.add_row(
                    agent["name"],
                    agent["status"],
                    agent.get("last_action", "N/A")
                )
                
        # Create panel with both tables
        main_panel = Panel(
            workflow_table,
            title="🔄 Workflow Status",
            border_style="blue"
        )
        
        # Print using rich console
        self.console.print(main_panel)
        
        if "agents" in workflow_data:
            agents_panel = Panel(
                agents_table,
                title="🤖 Agent Status",
                border_style="cyan"
            )
            self.console.print(agents_panel)
            
        return {
            "formatted": True,
            "display_type": "rich_workflow_status",
            "components_used": ["Table", "Panel"]
        }
        
    async def format_workflow_status_plain(self, workflow_data: dict):
        """Plain text fallback formatting for workflow status"""
        output_lines = [
            f"\n🔄 Workflow Status: {workflow_data['workflow_id']}",
            "=" * 50,
            f"📋 Goal: {workflow_data['goal']}",
            f"📊 Status: {workflow_data['status']}",
            f"📈 Progress: {workflow_data.get('progress', 0)}%",
            f"📅 Created: {workflow_data.get('created_at', 'Unknown')}"
        ]
        
        # Add agents information if available
        if "agents" in workflow_data:
            output_lines.extend([
                "\n🤖 Active Agents:",
                "-" * 30
            ])
            
            for agent in workflow_data["agents"]:
                output_lines.append(f"  • {agent['name']}: {agent['status']}")
                if agent.get("last_action"):
                    output_lines.append(f"    Last: {agent['last_action']}")
                    
        formatted_output = "\n".join(output_lines)
        print(formatted_output)
        
        return {
            "formatted": True,
            "display_type": "plain_workflow_status",
            "fallback_used": True
        }
```

### Interactive Command Prompts

The system provides interactive prompts for enhanced user experience:

```python
# Interactive prompts for user input
class InteractivePrompts:
    def __init__(self):
        self.rich_available = self.check_rich_availability()
        
    async def prompt_for_goal(self, context: dict = None):
        """Interactive goal prompting with validation"""
        if self.rich_available:
            return await self.prompt_for_goal_rich(context)
        else:
            return await self.prompt_for_goal_plain(context)
            
    async def prompt_for_goal_rich(self, context: dict = None):
        """Rich interactive goal prompting"""
        from rich.prompt import Prompt
        from rich.panel import Panel
        from rich.console import Console
        
        console = Console()
        
        # Display context if available
        if context:
            context_panel = Panel(
                f"Current Context: {context.get('description', 'No context available')}",
                title="💡 Context",
                border_style="yellow"
            )
            console.print(context_panel)
            
        # Goal input prompt
        goal_prompt = Panel(
            "Please describe your goal or objective.\n"
            "Be specific about what you want to accomplish.\n\n"
            "Examples:\n"
            "• 'Build a website for my business'\n"
            "• 'Analyze sales data and create a report'\n"
            "• 'Set up automated testing for my project'",
            title="🎯 Goal Definition",
            border_style="blue"
        )
        
        console.print(goal_prompt)
        
        # Get user input with validation
        while True:
            goal_text = Prompt.ask(
                "\n[bold blue]Enter your goal[/bold blue]",
                default="",
                show_default=False
            )
            
            if goal_text.strip():
                # Validate goal
                validation = await self.validate_goal_input(goal_text)
                
                if validation["valid"]:
                    # Confirm goal
                    confirmation_panel = Panel(
                        f"Goal: {goal_text}\n\n"
                        f"Estimated complexity: {validation['complexity']}\n"
                        f"Suggested tools: {', '.join(validation['suggested_tools'])}",
                        title="📋 Goal Confirmation",
                        border_style="green"
                    )
                    console.print(confirmation_panel)
                    
                    confirm = Prompt.ask(
                        "\n[bold green]Proceed with this goal? (y/n)[/bold green]",
                        choices=["y", "n"],
                        default="y"
                    )
                    
                    if confirm.lower() == "y":
                        return {
                            "goal_text": goal_text,
                            "validation": validation,
                            "confirmed": True
                        }
                else:
                    console.print(f"[red]⚠️  {validation['error']}[/red]")
            else:
                console.print("[red]⚠️  Goal cannot be empty[/red]")
                
    async def prompt_for_goal_plain(self, context: dict = None):
        """Plain text interactive goal prompting"""
        print("\n🎯 Goal Definition")
        print("=" * 50)
        
        if context:
            print(f"💡 Current Context: {context.get('description', 'No context available')}")
            print()
            
        print("Please describe your goal or objective.")
        print("Be specific about what you want to accomplish.")
        print("\nExamples:")
        print("• 'Build a website for my business'")
        print("• 'Analyze sales data and create a report'")
        print("• 'Set up automated testing for my project'")
        
        while True:
            goal_text = input("\nEnter your goal: ").strip()
            
            if goal_text:
                # Validate goal
                validation = await self.validate_goal_input(goal_text)
                
                if validation["valid"]:
                    print(f"\n📋 Goal: {goal_text}")
                    print(f"📊 Estimated complexity: {validation['complexity']}")
                    print(f"🔧 Suggested tools: {', '.join(validation['suggested_tools'])}")
                    
                    confirm = input("\nProceed with this goal? (y/n): ").strip().lower()
                    
                    if confirm in ["y", "yes"]:
                        return {
                            "goal_text": goal_text,
                            "validation": validation,
                            "confirmed": True
                        }
                    elif confirm in ["n", "no"]:
                        continue
                else:
                    print(f"⚠️  {validation['error']}")
            else:
                print("⚠️  Goal cannot be empty")
```

## Display Type Routing

### Structured Display Management

The system routes different content types to appropriate display handlers:

```python
# Display type routing for Node.js integration
class DisplayTypeRouter:
    def __init__(self):
        self.display_handlers = {
            "workflow_created": self.handle_workflow_created_display,
            "help_categories": self.handle_help_categories_display,
            "real_time_stats": self.handle_real_time_stats_display,
            "tool_results": self.handle_tool_results_display,
            "error": self.handle_error_display,
            "progress_update": self.handle_progress_update_display,
            "confirmation_prompt": self.handle_confirmation_prompt_display
        }
        
    async def route_display(self, display_data: dict, output_format: str = "terminal"):
        """Route display data to appropriate handler based on display_type"""
        display_type = display_data.get("display_type", "default")
        
        handler = self.display_handlers.get(display_type, self.handle_default_display)
        
        # Format for different output targets
        if output_format == "subprocess":
            return await self.format_for_subprocess(display_data, handler)
        elif output_format == "terminal":
            return await handler(display_data)
        elif output_format == "json":
            return await self.format_as_json(display_data)
        else:
            return await handler(display_data)
            
    async def format_for_subprocess(self, display_data: dict, handler: callable):
        """Format display data for Node.js subprocess consumption"""
        # Ensure subprocess-safe formatting
        subprocess_data = {
            "display_type": display_data.get("display_type"),
            "content": display_data,
            "subprocess_safe": True,
            "timestamp": datetime.utcnow().isoformat(),
            "formatting_hints": {
                "suggested_renderer": self.suggest_nodejs_renderer(display_data),
                "interactive_elements": self.extract_interactive_elements(display_data),
                "styling_suggestions": self.generate_styling_suggestions(display_data)
            }
        }
        
        return subprocess_data
        
    def suggest_nodejs_renderer(self, display_data: dict):
        """Suggest appropriate Node.js renderer based on content"""
        display_type = display_data.get("display_type")
        
        renderer_suggestions = {
            "workflow_created": "workflow_success_renderer",
            "help_categories": "git_style_help_renderer", 
            "real_time_stats": "metrics_dashboard_renderer",
            "tool_results": "tool_output_renderer",
            "error": "error_display_renderer",
            "progress_update": "progress_bar_renderer"
        }
        
        return renderer_suggestions.get(display_type, "default_renderer")
        
    def extract_interactive_elements(self, display_data: dict):
        """Extract interactive elements for Node.js handling"""
        interactive_elements = []
        
        # Check for prompts
        if "prompt" in display_data:
            interactive_elements.append({
                "type": "prompt",
                "message": display_data["prompt"]["message"],
                "input_type": display_data["prompt"].get("type", "text"),
                "validation": display_data["prompt"].get("validation", {})
            })
            
        # Check for selection options
        if "options" in display_data:
            interactive_elements.append({
                "type": "selection",
                "options": display_data["options"],
                "multiple": display_data.get("multiple_selection", False)
            })
            
        # Check for confirmation requests
        if "confirmation_required" in display_data:
            interactive_elements.append({
                "type": "confirmation",
                "message": display_data["confirmation_required"]["message"],
                "default": display_data["confirmation_required"].get("default", False)
            })
            
        return interactive_elements
```

## Integration Guidelines

### Adding New UI Components

To add new UI components to the system:

1. **Create Display Handler**
   ```python
   async def handle_new_component_display(self, display_data: dict):
       """Handle new component display formatting"""
       return {
           "formatted_content": "formatted_output",
           "display_type": "new_component",
           "subprocess_safe": True
       }
   ```

2. **Register Display Type**
   ```python
   self.display_handlers["new_component"] = self.handle_new_component_display
   ```

3. **Add Node.js Renderer**
   ```javascript
   function renderNewComponent(data) {
       // Implement Node.js rendering logic
       console.log(data.formatted_content);
   }
   ```

### Subprocess Communication Guidelines

For reliable subprocess communication:

1. **Always Return Structured Data**
   - Include `subprocess_safe: true`
   - Provide `display_type` for routing
   - Add error handling metadata

2. **Handle Timeouts Gracefully**
   - Set appropriate timeouts for operations
   - Provide progress updates for long operations
   - Implement graceful cancellation

3. **Maintain State Consistency**
   - Use MCP hub for shared state
   - Handle process interruption scenarios
   - Provide recovery mechanisms

## Conclusion

MAO's user interface patterns provide a comprehensive framework for professional terminal applications with seamless Node.js integration. The subprocess communication architecture enables rich interactive experiences while maintaining the LOCAL-only architecture.

The Git-style CLI patterns provide familiar professional interfaces, while the rich terminal formatting with graceful fallback ensures consistent user experience across different environments. The structured display routing enables flexible UI rendering while maintaining compatibility with different output formats.

These patterns work together to create a professional, accessible, and extensible user interface system that bridges modern web technologies with traditional command-line interfaces.