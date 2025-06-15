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
