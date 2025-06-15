# ui/main_menu.py - Interactive Main Menu Interface

from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.message import Message
from textual.reactive import reactive
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from .styles import MAO_COLORS, get_panel_style
from .components.menu_widget import MenuWidget


class MainMenu(Static):
    """
    Beautiful main menu interface with clear options and elegant design.
    Serves as the primary navigation hub for Mao workflows.
    """
    
    selected_option = reactive(0)
    
    class OptionSelected(Message):
        """Message sent when a menu option is selected."""
        def __init__(self, option: str) -> None:
            self.option = option
            super().__init__()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = [
            ("new_workflow", "Create New Workflow", "Set up a new AI workflow with guided assistance"),
            ("manage_workflows", "Manage Workflows", "View, edit, and organize your existing workflows"),
            ("run_workflow", "Run Workflow", "Execute a workflow and monitor progress"),
            ("settings", "Settings", "Configure Mao preferences and connections"),
            ("help", "Help & Documentation", "Learn how to use Mao effectively"),
            ("quit", "Quit", "Exit Mao")
        ]
    
    def compose(self):
        """Compose the main menu layout."""
        # Create welcome header
        welcome_text = Text.assemble(
            ("Welcome to ", "white"),
            ("Mao", f"bold {MAO_COLORS['primary']}"),
            ("\n", "white"),
            ("AI Workflow Orchestrator", f"{MAO_COLORS['text_secondary']} italic"),
        )
        
        welcome_panel = Panel(
            Align.center(welcome_text),
            title="AI-Powered Development",
            title_align="center",
            **get_panel_style("info")
        )
        
        # Create menu widget
        menu_widget = MenuWidget(
            options=self.options,
            title="What would you like to do?",
            id="main-menu-widget"
        )
        
        # Status information
        status_text = Text.assemble(
            ("Status: ", "bold"),
            ("Ready", f"bold {MAO_COLORS['success']}"),
            (" | Workflows: ", ""),
            ("3 active", f"{MAO_COLORS['info']}"),
            (" | Version: ", ""),
            ("0.1.0", f"{MAO_COLORS['text_dim']}")
        )
        
        status_panel = Panel(
            Align.center(status_text),
            title="System Status",
            **get_panel_style("default")
        )
        
        with Vertical():
            yield Static(welcome_panel, id="welcome-header")
            yield Static(menu_widget, id="menu-section")
            yield Static(status_panel, id="status-footer")
    
    def on_menu_widget_option_selected(self, message: MenuWidget.OptionSelected) -> None:
        """Handle menu option selection."""
        self.post_message(self.OptionSelected(message.option))


# ui/workflow_wizard.py - Workflow Setup Wizard

from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from .styles import MAO_COLORS, get_panel_style
from .components.conversation_widget import ConversationWidget


class WorkflowWizard(Static):
    """
    Guided workflow creation interface with AI conversation simulation.
    Feels like chatting with Claude to set up your perfect workflow.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_step = 1
        self.total_steps = 4
        self.workflow_data = {}
        
    class WorkflowCreated(Message):
        """Message sent when workflow is successfully created."""
        def __init__(self, workflow_data: dict) -> None:
            self.workflow_data = workflow_data
            super().__init__()
    
    def compose(self):
        """Compose the workflow wizard layout."""
        # Header with progress
        header_text = Text.assemble(
            ("Step ", ""),
            (f"{self.current_step}", f"bold {MAO_COLORS['primary']}"),
            (" of ", ""),
            (f"{self.total_steps}", f"bold {MAO_COLORS['text_secondary']}"),
            (" | ", ""),
            ("Workflow Setup Wizard", f"bold {MAO_COLORS['text_primary']}")
        )
        
        header_panel = Panel(
            header_text,
            title="Workflow Wizard",
            **get_panel_style("info")
        )
        
        # Main conversation area
        conversation = ConversationWidget(
            initial_message="Hi! I'm here to help you create a new AI workflow. Let's start with the basics - what would you like your workflow to accomplish?",
            id="wizard-conversation"
        )
        
        # Input area
        with Horizontal(id="input-area"):
            yield Input(
                placeholder="Describe what you want your workflow to do...",
                id="workflow-input"
            )
            yield Button("Send", variant="primary", id="send-button")
            yield Button("Skip", variant="default", id="skip-button")
        
        # Navigation buttons
        with Horizontal(id="navigation"):
            yield Button("← Back", variant="default", id="back-button")
            yield Button("Next →", variant="primary", id="next-button")
            yield Button("Cancel", variant="error", id="cancel-button")
        
        with Vertical():
            yield Static(header_panel, id="wizard-header")
            yield conversation
            yield Static(self.input_area, id="input-section")
            yield Static(self.navigation, id="nav-section")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button interactions."""
        if event.button.id == "send-button":
            self.handle_user_input()
        elif event.button.id == "next-button":
            self.next_step()
        elif event.button.id == "back-button":
            self.previous_step()
        elif event.button.id == "skip-button":
            self.skip_step()
        elif event.button.id == "cancel-button":
            self.cancel_wizard()
    
    def handle_user_input(self) -> None:
        """Process user input and simulate AI response."""
        input_widget = self.query_one("#workflow-input", Input)
        user_message = input_widget.value.strip()
        
        if not user_message:
            return
            
        # Add user message to conversation
        conversation = self.query_one("#wizard-conversation", ConversationWidget)
        conversation.add_message("user", user_message)
        
        # Simulate AI response based on current step
        ai_response = self.get_ai_response(user_message)
        conversation.add_message("assistant", ai_response)
        
        # Clear input
        input_widget.value = ""
        
        # Store workflow data
        self.store_step_data(user_message)
    
    def get_ai_response(self, user_input: str) -> str:
        """Generate contextual AI response based on current step."""
        responses = {
            1: f"Great! I understand you want to create a workflow for: '{user_input}'. This sounds like it could involve multiple AI agents working together. \n\nWhat specific tasks or steps should this workflow include?",
            2: "Perfect! Now I have a better understanding of the steps involved. Let me ask about the agents - what types of AI capabilities do you need? For example: writing, analysis, research, coding, etc.",
            3: "Excellent! I can see how the different AI agents will work together. Finally, what should the output look like? Should it be files, reports, code, or something else?",
            4: "Perfect! I have all the information I need. Let me create your workflow configuration..."
        }
        return responses.get(self.current_step, "Thank you for that information. Let's continue...")
    
    def store_step_data(self, user_input: str) -> None:
        """Store data from current step."""
        step_keys = {
            1: "description",
            2: "tasks", 
            3: "agents",
            4: "output"
        }
        key = step_keys.get(self.current_step)
        if key:
            self.workflow_data[key] = user_input
    
    def next_step(self) -> None:
        """Advance to next step."""
        if self.current_step < self.total_steps:
            self.current_step += 1
            self.update_step_display()
        else:
            self.complete_wizard()
    
    def previous_step(self) -> None:
        """Go back to previous step."""
        if self.current_step > 1:
            self.current_step -= 1
            self.update_step_display()
    
    def skip_step(self) -> None:
        """Skip current step with default values."""
        defaults = {
            1: "General AI workflow",
            2: "Multi-step AI processing",
            3: "General purpose AI agents", 
            4: "Text files and reports"
        }
        self.workflow_data[f"step_{self.current_step}"] = defaults.get(self.current_step, "Skipped")
        self.next_step()
    
    def cancel_wizard(self) -> None:
        """Cancel wizard and return to main menu."""
        # TODO: Show confirmation dialog
        self.post_message(WorkflowWizard.WorkflowCreated({}))
    
    def complete_wizard(self) -> None:
        """Complete wizard and create workflow."""
        # Generate workflow configuration
        workflow_config = {
            "name": f"workflow_{len(self.workflow_data)}",
            "description": self.workflow_data.get("description", ""),
            "tasks": self.workflow_data.get("tasks", ""),
            "agents": self.workflow_data.get("agents", ""),
            "output": self.workflow_data.get("output", ""),
            "created": "2025-06-15",
            "status": "draft"
        }
        
        self.post_message(WorkflowWizard.WorkflowCreated(workflow_config))
    
    def update_step_display(self) -> None:
        """Update the step indicator and content."""
        # Update header
        header_text = Text.assemble(
            ("Step ", ""),
            (f"{self.current_step}", f"bold {MAO_COLORS['primary']}"),
            (" of ", ""),
            (f"{self.total_steps}", f"bold {MAO_COLORS['text_secondary']}"),
            (" | ", ""),
            ("Workflow Setup Wizard", f"bold {MAO_COLORS['text_primary']}")
        )
        
        # Add contextual prompt for current step
        conversation = self.query_one("#wizard-conversation", ConversationWidget)
        prompts = {
            1: "Let's start fresh! What would you like your new workflow to accomplish?",
            2: "Now, what specific tasks or steps should this workflow include?", 
            3: "What types of AI capabilities do you need for this workflow?",
            4: "Finally, what should the output look like when the workflow completes?"
        }
        
        if self.current_step in prompts:
            conversation.add_message("assistant", prompts[self.current_step])


# ui/workflow_manager.py - Workflow Management Interface

from textual.widgets import Static, DataTable, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from pathlib import Path
import json

from .styles import MAO_COLORS, get_panel_style
from .components.workflow_list import WorkflowList
from workflows.manager import WorkflowManager as WFManager


class WorkflowManager(Static):
    """
    Workflow listing, editing, and organization interface.
    Clean, professional interface for managing all your AI workflows.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.workflow_manager = WFManager()
        self.selected_workflow = None
        
    class WorkflowSelected(Message):
        """Message sent when a workflow is selected."""
        def __init__(self, workflow_id: str) -> None:
            self.workflow_id = workflow_id
            super().__init__()
    
    def compose(self):
        """Compose the workflow manager layout."""
        # Header with summary stats
        workflows = self.workflow_manager.list_workflows()
        active_count = len([w for w in workflows if w.get('status') == 'active'])
        total_count = len(workflows)
        
        header_text = Text.assemble(
            ("Workflow Management", f"bold {MAO_COLORS['text_primary']}"),
            (" | ", ""),
            (f"{total_count}", f"bold {MAO_COLORS['primary']}"),
            (" total workflows, ", ""),
            (f"{active_count}", f"bold {MAO_COLORS['success']}"),
            (" active", "")
        )
        
        header_panel = Panel(
            header_text,
            title="Manage AI Workflows",
            **get_panel_style("default")
        )
        
        # Main workflow list
        workflow_list = WorkflowList(
            workflows=workflows,
            id="workflow-list"
        )
        
        # Action buttons
        with Horizontal(id="action-buttons"):
            yield Button("New Workflow", variant="primary", id="new-button")
            yield Button("Edit Selected", variant="default", id="edit-button")
            yield Button("Duplicate", variant="default", id="duplicate-button")
            yield Button("Delete", variant="error", id="delete-button")
            yield Button("Refresh", variant="default", id="refresh-button")
        
        # Details panel for selected workflow
        details_panel = Panel(
            "Select a workflow to view details",
            title="Workflow Details",
            **get_panel_style("info")
        )
        
        with Vertical():
            yield Static(header_panel, id="manager-header")
            yield workflow_list
            yield Static(self.action_buttons, id="actions-section")
            yield Static(details_panel, id="details-section")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle action button interactions."""
        if event.button.id == "new-button":
            self.create_new_workflow()
        elif event.button.id == "edit-button":
            self.edit_selected_workflow()
        elif event.button.id == "duplicate-button":
            self.duplicate_selected_workflow()
        elif event.button.id == "delete-button":
            self.delete_selected_workflow()
        elif event.button.id == "refresh-button":
            self.refresh_workflow_list()
    
    def on_workflow_list_workflow_selected(self, message) -> None:
        """Handle workflow selection."""
        self.selected_workflow = message.workflow_id
        self.update_details_panel()
        self.post_message(self.WorkflowSelected(message.workflow_id))
    
    def update_details_panel(self) -> None:
        """Update the details panel with selected workflow info."""
        if not self.selected_workflow:
            return
            
        workflow = self.workflow_manager.get_workflow(self.selected_workflow)
        if not workflow:
            return
            
        # Create detailed view
        details_table = Table(show_header=False, box=None)
        details_table.add_column("Property", style=f"bold {MAO_COLORS['text_secondary']}")
        details_table.add_column("Value", style=MAO_COLORS['text_primary'])
        
        details_table.add_row("Name", workflow.get('name', 'Unnamed'))
        details_table.add_row("Status", workflow.get('status', 'Unknown'))
        details_table.add_row("Created", workflow.get('created', 'Unknown'))
        details_table.add_row("Last Run", workflow.get('last_run', 'Never'))
        details_table.add_row("Description", workflow.get('description', 'No description'))
        
        # Update the details panel
        details_panel = Panel(
            details_table,
            title=f"Workflow: {workflow.get('name', 'Unknown')}",
            **get_panel_style("info")
        )
        
        details_section = self.query_one("#details-section")
        details_section.update(details_panel)
    
    def create_new_workflow(self) -> None:
        """Create a new workflow."""
        # Navigate to workflow wizard
        self.app.switch_to_screen("workflow-wizard")
    
    def edit_selected_workflow(self) -> None:
        """Edit the selected workflow."""
        if not self.selected_workflow:
            self.app.notify("No workflow selected", severity="warning")
            return
            
        # TODO: Open workflow editor
        self.app.notify(f"Editing workflow: {self.selected_workflow}")
    
    def duplicate_selected_workflow(self) -> None:
        """Duplicate the selected workflow."""
        if not self.selected_workflow:
            self.app.notify("No workflow selected", severity="warning")
            return
            
        success = self.workflow_manager.duplicate_workflow(self.selected_workflow)
        if success:
            self.app.notify("Workflow duplicated successfully", severity="success")
            self.refresh_workflow_list()
        else:
            self.app.notify("Failed to duplicate workflow", severity="error")
    
    def delete_selected_workflow(self) -> None:
        """Delete the selected workflow."""
        if not self.selected_workflow:
            self.app.notify("No workflow selected", severity="warning")
            return
            
        # TODO: Show confirmation dialog
        success = self.workflow_manager.delete_workflow(self.selected_workflow)
        if success:
            self.app.notify("Workflow deleted", severity="success")
            self.selected_workflow = None
            self.refresh_workflow_list()
        else:
            self.app.notify("Failed to delete workflow", severity="error")
    
    def refresh_workflow_list(self) -> None:
        """Refresh the workflow list."""
        workflows = self.workflow_manager.list_workflows()
        workflow_list = self.query_one("#workflow-list", WorkflowList)
        workflow_list.update_workflows(workflows)
        
        # Update header stats
        active_count = len([w for w in workflows if w.get('status') == 'active'])
        total_count = len(workflows)
        
        header_text = Text.assemble(
            ("Workflow Management", f"bold {MAO_COLORS['text_primary']}"),
            (" | ", ""),
            (f"{total_count}", f"bold {MAO_COLORS['primary']}"),
            (" total workflows, ", ""),
            (f"{active_count}", f"bold {MAO_COLORS['success']}"),
            (" active", "")
        )


# ui/command_runner.py - Command Execution Display

from textual.widgets import Static, ProgressBar, Button
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.message import Message
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
import asyncio
from datetime import datetime

from .styles import MAO_COLORS, get_panel_style
from .components.progress_display import ProgressDisplay


class CommandRunner(Static):
    """
    Beautiful interface for running workflows with real-time feedback.
    Professional execution display with live progress tracking.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_workflow = None
        self.execution_state = "idle"  # idle, running, completed, failed
        self.progress_data = {}
        
    class ExecutionStarted(Message):
        """Message sent when workflow execution starts."""
        def __init__(self, workflow_id: str) -> None:
            self.workflow_id = workflow_id
            super().__init__()
    
    class ExecutionCompleted(Message):
        """Message sent when workflow execution completes."""
        def __init__(self, workflow_id: str, success: bool) -> None:
            self.workflow_id = workflow_id
            self.success = success
            super().__init__()
    
    def compose(self):
        """Compose the command runner layout."""
        # Header with execution status
        status_text = Text.assemble(
            ("Workflow Execution", f"bold {MAO_COLORS['text_primary']}"),
            (" | Status: ", ""),
            ("Ready", f"bold {MAO_COLORS['success']}")
        )
        
        header_panel = Panel(
            status_text,
            title="AI Workflow Runner",
            **get_panel_style("default")
        )
        
        # Workflow selection
        with Horizontal(id="workflow-selection"):
            yield Button("Select Workflow", variant="primary", id="select-button")
            yield Button("Quick Run", variant="default", id="quick-button")
            yield Button("Stop Execution", variant="error", id="stop-button", disabled=True)
        
        # Progress display area
        progress_display = ProgressDisplay(id="progress-display")
        
        # Output console area
        output_panel = Panel(
            "No workflow running. Select a workflow to begin execution.",
            title="Execution Output",
            **get_panel_style("info")
        )
        
        with Vertical():
            yield Static(header_panel, id="runner-header")
            yield Static(self.workflow_selection, id="selection-section")
            yield progress_display
            yield ScrollableContainer(
                Static(output_panel, id="output-panel"),
                id="output-section"
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button interactions."""
        if event.button.id == "select-button":
            self.select_workflow()
        elif event.button.id == "quick-button":
            self.quick_run()
        elif event.button.id == "stop-button":
            self.stop_execution()
    
    def select_workflow(self) -> None:
        """Open workflow selection dialog."""
        # TODO: Implement workflow selection dialog
        self.app.notify("Workflow selection coming soon")
    
    def quick_run(self) -> None:
        """Quick run with default workflow."""
        if self.execution_state == "running":
            self.app.notify("Workflow already running", severity="warning")
            return
            
        # Start demo execution
        self.start_demo_execution()
    
    def stop_execution(self) -> None:
        """Stop current workflow execution."""
        if self.execution_state != "running":
            self.app.notify("No workflow running", severity="warning")
            return
            
        self.execution_state = "stopped"
        self.update_execution_status("Execution stopped by user")
        
        # Re-enable buttons
        self.query_one("#stop-button", Button).disabled = True
        self.query_one("#select-button", Button).disabled = False
        self.query_one("#quick-button", Button).disabled = False
    
    async def start_demo_execution(self) -> None:
        """Start a demo workflow execution."""
        self.execution_state = "running"
        self.current_workflow = "demo_workflow"
        
        # Update UI state
        self.query_one("#stop-button", Button).disabled = False
        self.query_one("#select-button", Button).disabled = True
        self.query_one("#quick-button", Button).disabled = True
        
        # Update header status
        self.update_execution_status("Initializing workflow...")
        
        # Post execution started message
        self.post_message(self.ExecutionStarted("demo_workflow"))
        
        try:
            # Simulate workflow execution steps
            steps = [
                ("Initializing agents", 0.1),
                ("Loading workflow configuration", 0.2),
                ("Starting primary agent", 0.3),
                ("Processing task 1 of 3", 0.5),
                ("Processing task 2 of 3", 0.7),
                ("Processing task 3 of 3", 0.9),
                ("Finalizing results", 1.0)
            ]
            
            progress_display = self.query_one("#progress-display", ProgressDisplay)
            
            for step_name, progress in steps:
                if self.execution_state != "running":
                    break
                    
                self.update_execution_status(step_name)
                progress_display.update_progress(progress, step_name)
                self.add_output_line(f"[{datetime.now().strftime('%H:%M:%S')}] {step_name}")
                
                # Simulate work time
                await asyncio.sleep(2.0)
            
            if self.execution_state == "running":
                self.execution_state = "completed"
                self.update_execution_status("Workflow completed successfully")
                self.add_output_line(f"[{datetime.now().strftime('%H:%M:%S')}] Workflow execution completed!")
                self.post_message(self.ExecutionCompleted("demo_workflow", True))
            
        except Exception as e:
            self.execution_state = "failed"
            self.update_execution_status(f"Execution failed: {str(e)}")
            self.add_output_line(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}")
            self.post_message(self.ExecutionCompleted("demo_workflow", False))
        
        finally:
            # Re-enable buttons
            self.query_one("#stop-button", Button).disabled = True
            self.query_one("#select-button", Button).disabled = False
            self.query_one("#quick-button", Button).disabled = False
    
    def update_execution_status(self, status: str) -> None:
        """Update the execution status in the header."""
        status_color = {
            "idle": MAO_COLORS['text_secondary'],
            "running": MAO_COLORS['primary'],
            "completed": MAO_COLORS['success'],
            "failed": MAO_COLORS['error'],
            "stopped": MAO_COLORS['warning']
        }.get(self.execution_state, MAO_COLORS['text_secondary'])
        
        status_text = Text.assemble(
            ("Workflow Execution", f"bold {MAO_COLORS['text_primary']}"),
            (" | Status: ", ""),
            (status, f"bold {status_color}")
        )
        
        header_panel = Panel(
            status_text,
            title="AI Workflow Runner",
            **get_panel_style("default")
        )
        
        header_section = self.query_one("#runner-header")
        header_section.update(header_panel)
    
    def add_output_line(self, line: str) -> None:
        """Add a line to the output console."""
        output_panel = self.query_one("#output-panel")
        
        # Get current content and add new line
        current_lines = getattr(self, '_output_lines', [])
        current_lines.append(line)
        
        # Keep only last 100 lines
        if len(current_lines) > 100:
            current_lines = current_lines[-100:]
        
        self._output_lines = current_lines
        
        # Update output panel
        output_text = "\n".join(current_lines)
        new_panel = Panel(
            output_text,
            title="Execution Output",
            **get_panel_style("info")
        )
        
        output_panel.update(new_panel)