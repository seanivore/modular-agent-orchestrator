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
        # Generate real workflow ID
        from orchestrator.workflow_manager import generate_workflow_id
        workflow_result = generate_workflow_id()
        
        if not workflow_result.get("success"):
            self.app.notify("Failed to generate workflow ID", severity="error")
            return
            
        workflow_id = workflow_result["workflow_id"]
        
        self.execution_state = "running"
        self.current_workflow = workflow_id
        
        # Update UI state
        self.query_one("#stop-button", Button).disabled = False
        self.query_one("#select-button", Button).disabled = True
        self.query_one("#quick-button", Button).disabled = True
        
        # Update header status
        self.update_execution_status(f"Initializing workflow {workflow_id}...")
        
        # Post execution started message
        self.post_message(self.ExecutionStarted(workflow_id))
        
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
                self.post_message(self.ExecutionCompleted(workflow_id, True))
            
        except Exception as e:
            self.execution_state = "failed"
            self.update_execution_status(f"Execution failed: {str(e)}")
            self.add_output_line(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}")
            self.post_message(self.ExecutionCompleted(workflow_id, False))
        
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