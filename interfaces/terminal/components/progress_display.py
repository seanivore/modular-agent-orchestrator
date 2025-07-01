#!/usr/bin/env python3
"""
MAO Progress Display Component
Shows workflow execution progress with visual indicators
"""

from textual.widget import Widget
from textual.widgets import Static, ProgressBar
from textual.containers import Vertical
from rich.panel import Panel
from rich.text import Text

from ..styles import MAO_COLORS, get_panel_style


class ProgressDisplay(Widget):
    """
    Progress display widget for workflow execution
    Shows current task, progress bar, and status updates
    """
    
    def __init__(self, workflow_name: str = "Workflow"):
        super().__init__()
        self.workflow_name = workflow_name
        self.current_task = "Initializing..."
        self.progress = 0.0
        self.status = "pending"
        
    def compose(self):
        """Compose progress display layout"""
        
        # Progress header
        header_text = Text.assemble(
            ("Progress: ", "white"),
            (self.workflow_name, f"bold {MAO_COLORS['primary']}")
        )
        
        # Current task
        task_text = Text.assemble(
            ("Current: ", f"{MAO_COLORS['text_secondary']}"),
            (self.current_task, f"{MAO_COLORS['text_primary']}")
        )
        
        # Status indicator
        status_colors = {
            'pending': MAO_COLORS['pending'],
            'active': MAO_COLORS['active'], 
            'completed': MAO_COLORS['completed'],
            'failed': MAO_COLORS['failed']
        }
        
        status_text = Text.assemble(
            ("Status: ", f"{MAO_COLORS['text_secondary']}"),
            (self.status.title(), f"bold {status_colors.get(self.status, MAO_COLORS['text_primary'])}")
        )
        
        yield Vertical(
            Static(Panel(header_text, **get_panel_style("primary"))),
            Static(task_text),
            ProgressBar(total=100, progress=self.progress * 100),
            Static(status_text),
            id="progress-display"
        )
        
    def update_progress(self, task: str, progress: float, status: str = None):
        """Update progress display"""
        self.current_task = task
        self.progress = min(1.0, max(0.0, progress))
        if status:
            self.status = status
        self.refresh()
        
    def set_completed(self):
        """Mark progress as completed"""
        self.progress = 1.0
        self.status = "completed"
        self.current_task = "Completed successfully"
        self.refresh()
        
    def set_failed(self, error_msg: str = "Failed"):
        """Mark progress as failed"""
        self.status = "failed"
        self.current_task = error_msg
        self.refresh()