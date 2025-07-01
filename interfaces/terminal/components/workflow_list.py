#!/usr/bin/env python3
"""
MAO Workflow List Component
Displays and manages workflow list with status indicators
"""

from textual.widget import Widget
from textual.widgets import Static, DataTable
from textual.containers import Vertical
from textual.message import Message
from rich.panel import Panel
from rich.text import Text

from ..styles import MAO_COLORS, get_panel_style


class WorkflowSelected(Message):
    """Message sent when workflow is selected"""
    
    def __init__(self, workflow_id: str):
        super().__init__()
        self.workflow_id = workflow_id


class WorkflowList(Widget):
    """
    Workflow list widget showing available workflows with status
    """
    
    def __init__(self):
        super().__init__()
        self.workflows = []
        self.selected_workflow = None
        
    def compose(self):
        """Compose workflow list layout"""
        
        # Header
        header_text = Text.assemble(
            ("Your Workflows", f"bold {MAO_COLORS['primary']}")
        )
        
        # Create data table
        table = DataTable()
        table.add_columns("Name", "Status", "Created", "Last Run")
        
        # Add workflow rows
        for workflow in self.workflows:
            status_color = self.get_status_color(workflow.get('status', 'draft'))
            table.add_row(
                workflow.get('name', 'Untitled'),
                Text(workflow.get('status', 'draft').title(), style=status_color),
                workflow.get('created', 'Unknown'),
                workflow.get('last_run', 'Never')
            )
        
        # If no workflows, show placeholder
        if not self.workflows:
            table.add_row(
                Text("No workflows yet", style=MAO_COLORS['text_dim']),
                Text("—", style=MAO_COLORS['text_dim']),
                Text("—", style=MAO_COLORS['text_dim']),
                Text("—", style=MAO_COLORS['text_dim'])
            )
        
        yield Vertical(
            Static(Panel(header_text, **get_panel_style("primary"))),
            table,
            id="workflow-list"
        )
        
    def get_status_color(self, status: str) -> str:
        """Get color for workflow status"""
        status_colors = {
            'active': MAO_COLORS['active'],
            'pending': MAO_COLORS['pending'],
            'completed': MAO_COLORS['completed'],
            'failed': MAO_COLORS['failed'],
            'draft': MAO_COLORS['draft']
        }
        return status_colors.get(status.lower(), MAO_COLORS['text_primary'])
        
    def load_workflows(self, workflows: list):
        """Load workflows into the list"""
        self.workflows = workflows
        self.refresh()
        
    def add_workflow(self, workflow: dict):
        """Add a new workflow to the list"""
        self.workflows.append(workflow)
        self.refresh()
        
    def update_workflow_status(self, workflow_id: str, status: str):
        """Update status of a specific workflow"""
        for workflow in self.workflows:
            if workflow.get('id') == workflow_id:
                workflow['status'] = status
                break
        self.refresh()
        
    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle workflow selection"""
        if event.row_index < len(self.workflows):
            workflow = self.workflows[event.row_index]
            workflow_id = workflow.get('id', str(event.row_index))
            self.selected_workflow = workflow_id
            self.post_message(WorkflowSelected(workflow_id))