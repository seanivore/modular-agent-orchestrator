# ui/components/menu_widget.py - Reusable Menu Component

from textual.widgets import Static
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from ..styles import MAO_COLORS, get_panel_style


class MenuWidget(Static):
    """
    Beautiful, reusable menu component with hover effects and descriptions.
    Professional styling that works across different contexts.
    """
    
    selected_index = reactive(0)
    
    class OptionSelected(Message):
        """Message sent when a menu option is selected."""
        def __init__(self, option: str) -> None:
            self.option = option
            super().__init__()
    
    def __init__(self, options, title="Menu", **kwargs):
        super().__init__(**kwargs)
        self.options = options
        self.title = title
        
    def compose(self):
        """Compose the menu widget."""
        # Create menu table
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style=f"bold {MAO_COLORS['text_primary']}")
        menu_table.add_column("Description", style=MAO_COLORS['text_secondary'])
        
        for i, (key, label, description) in enumerate(self.options):
            if i == self.selected_index:
                # Highlighted row
                menu_table.add_row(
                    f"▶ {label}",
                    description,
                    style=f"bold {MAO_COLORS['primary']} on {MAO_COLORS['surface_hover']}"
                )
            else:
                menu_table.add_row(f"  {label}", description)
        
        menu_panel = Panel(
            menu_table,
            title=self.title,
            **get_panel_style("default")
        )
        
        yield Static(menu_panel)
    
    def on_key(self, event) -> None:
        """Handle keyboard navigation."""
        if event.key == "down" or event.key == "j":
            self.selected_index = min(self.selected_index + 1, len(self.options) - 1)
            self.refresh()
        elif event.key == "up" or event.key == "k":
            self.selected_index = max(self.selected_index - 1, 0)
            self.refresh()
        elif event.key == "enter":
            option_key = self.options[self.selected_index][0]
            self.post_message(self.OptionSelected(option_key))


# ui/components/conversation_widget.py - Chat-like Interface

from textual.widgets import Static
from textual.containers import Vertical, ScrollableContainer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from datetime import datetime

from ..styles import MAO_COLORS, get_panel_style


class ConversationWidget(Static):
    """
    Chat-like interface for AI conversations.
    Clean, readable conversation flow with proper message styling.
    """
    
    def __init__(self, initial_message=None, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
        if initial_message:
            self.messages.append({
                "role": "assistant",
                "content": initial_message,
                "timestamp": datetime.now()
            })
    
    def compose(self):
        """Compose the conversation widget."""
        conversation_container = ScrollableContainer(
            *self.render_messages(),
            id="conversation-scroll"
        )
        yield conversation_container
    
    def render_messages(self):
        """Render all messages in the conversation."""
        rendered_messages = []
        
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            timestamp = message["timestamp"].strftime("%H:%M")
            
            if role == "user":
                # User message - right aligned, different color
                message_text = Text.assemble(
                    (f"You ({timestamp})", f"bold {MAO_COLORS['secondary']}"),
                    ("\n", ""),
                    (content, MAO_COLORS['text_primary'])
                )
                message_panel = Panel(
                    message_text,
                    border_style=MAO_COLORS['secondary'],
                    width=80
                )
            else:
                # Assistant message - left aligned, primary color
                message_text = Text.assemble(
                    (f"Mao ({timestamp})", f"bold {MAO_COLORS['primary']}"),
                    ("\n", ""),
                    (content, MAO_COLORS['text_primary'])
                )
                message_panel = Panel(
                    message_text,
                    border_style=MAO_COLORS['primary'],
                    width=80
                )
            
            rendered_messages.append(Static(message_panel))
        
        return rendered_messages
    
    def add_message(self, role: str, content: str):
        """Add a new message to the conversation."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        self.refresh_conversation()
    
    def refresh_conversation(self):
        """Refresh the conversation display."""
        container = self.query_one("#conversation-scroll", ScrollableContainer)
        
        # Clear existing messages
        for child in container.children:
            child.remove()
        
        # Add updated messages
        for message_widget in self.render_messages():
            container.mount(message_widget)
        
        # Scroll to bottom
        container.scroll_end()


# ui/components/workflow_list.py - Workflow Listing Widget

from textual.widgets import Static, DataTable
from textual.message import Message
from rich.console import Console
from rich.table import Table
from rich.text import Text

from ..styles import MAO_COLORS


class WorkflowList(Static):
    """
    Professional workflow listing with status indicators and sorting.
    Clean table interface for workflow management.
    """
    
    class WorkflowSelected(Message):
        """Message sent when a workflow is selected."""
        def __init__(self, workflow_id: str) -> None:
            self.workflow_id = workflow_id
            super().__init__()
    
    def __init__(self, workflows=None, **kwargs):
        super().__init__(**kwargs)
        self.workflows = workflows or []
        self.selected_workflow = None
    
    def compose(self):
        """Compose the workflow list."""
        # Create data table
        table = DataTable(id="workflow-table")
        
        # Add columns
        table.add_column("Name", width=25)
        table.add_column("Status", width=12)
        table.add_column("Created", width=15)
        table.add_column("Last Run", width=15)
        table.add_column("Description", width=40)
        
        # Add workflow rows
        for workflow in self.workflows:
            status_style = self.get_status_style(workflow.get('status', 'unknown'))
            
            table.add_row(
                workflow.get('name', 'Unnamed'),
                Text(workflow.get('status', 'Unknown'), style=status_style),
                workflow.get('created', 'Unknown'),
                workflow.get('last_run', 'Never'),
                workflow.get('description', 'No description')[:40] + "..." if len(workflow.get('description', '')) > 40 else workflow.get('description', '')
            )
        
        yield table
    
    def get_status_style(self, status: str) -> str:
        """Get the appropriate style for a workflow status."""
        status_styles = {
            'active': f"bold {MAO_COLORS['success']}",
            'draft': f"bold {MAO_COLORS['pending']}",
            'completed': f"bold {MAO_COLORS['completed']}",
            'failed': f"bold {MAO_COLORS['failed']}",
            'stopped': f"bold {MAO_COLORS['warning']}",
        }
        return status_styles.get(status.lower(), MAO_COLORS['text_secondary'])
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        if event.row_index < len(self.workflows):
            workflow = self.workflows[event.row_index]
            workflow_id = workflow.get('id', workflow.get('name', f'workflow_{event.row_index}'))
            self.selected_workflow = workflow_id
            self.post_message(self.WorkflowSelected(workflow_id))
    
    def update_workflows(self, workflows):
        """Update the workflow list with new data."""
        self.workflows = workflows
        
        # Get the table and clear it
        table = self.query_one("#workflow-table", DataTable)
        table.clear()
        
        # Re-add rows
        for workflow in self.workflows:
            status_style = self.get_status_style(workflow.get('status', 'unknown'))
            
            table.add_row(
                workflow.get('name', 'Unnamed'),
                Text(workflow.get('status', 'Unknown'), style=status_style),
                workflow.get('created', 'Unknown'),
                workflow.get('last_run', 'Never'),
                workflow.get('description', 'No description')[:40] + "..." if len(workflow.get('description', '')) > 40 else workflow.get('description', '')
            )


# ui/components/progress_display.py - Progress Tracking Widget

from textual.widgets import Static, ProgressBar
from textual.containers import Vertical, Horizontal
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

from ..styles import MAO_COLORS, get_panel_style


class ProgressDisplay(Static):
    """
    Beautiful progress tracking with real-time updates.
    Professional progress indicators for workflow execution.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_progress = 0.0
        self.current_step = "Ready"
        self.token_count = 0
        self.estimated_tokens = 1000
    
    def compose(self):
        """Compose the progress display."""
        # Main progress bar
        progress_bar = ProgressBar(
            total=100,
            show_eta=True,
            id="main-progress"
        )
        
        # Step indicator
        step_text = Text.assemble(
            ("Current Step: ", ""),
            (self.current_step, f"bold {MAO_COLORS['primary']}")
        )
        
        # Token usage indicator
        token_text = Text.assemble(
            ("Tokens: ", ""),
            (f"{self.token_count}", f"bold {MAO_COLORS['accent']}"),
            (" / ", ""),
            (f"{self.estimated_tokens}", MAO_COLORS['text_secondary'])
        )
        
        # Progress panel
        progress_content = Vertical(
            Static(step_text, id="step-indicator"),
            progress_bar,
            Static(token_text, id="token-indicator")
        )
        
        progress_panel = Panel(
            progress_content,
            title="Execution Progress",
            **get_panel_style("info")
        )
        
        yield Static(progress_panel)
    
    def update_progress(self, progress: float, step: str = None, tokens: int = None):
        """Update progress display with new values."""
        self.current_progress = progress
        
        if step:
            self.current_step = step
            
        if tokens:
            self.token_count = tokens
        
        # Update progress bar
        progress_bar = self.query_one("#main-progress", ProgressBar)
        progress_bar.progress = int(progress * 100)
        
        # Update step text
        step_text = Text.assemble(
            ("Current Step: ", ""),
            (self.current_step, f"bold {MAO_COLORS['primary']}")
        )
        step_indicator = self.query_one("#step-indicator")
        step_indicator.update(step_text)
        
        # Update token text
        token_text = Text.assemble(
            ("Tokens: ", ""),
            (f"{self.token_count}", f"bold {MAO_COLORS['accent']}"),
            (" / ", ""),
            (f"{self.estimated_tokens}", MAO_COLORS['text_secondary'])
        )
        token_indicator = self.query_one("#token-indicator")
        token_indicator.update(token_text)


# workflows/manager.py - Workflow File Operations

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import shutil

from config import get_config


class WorkflowManager:
    """
    Manages workflow files, configurations, and operations.
    Handles CRUD operations for AI workflow definitions.
    """
    
    def __init__(self):
        self.config = get_config()
        self.workflow_dir = self.config.get_workflow_directory()
        self.backup_dir = self.config.get_backup_directory()
        
        # Ensure directories exist
        self.workflow_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows."""
        workflows = []
        
        for workflow_file in self.workflow_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    workflow_data = json.load(f)
                    
                # Add file metadata
                stat = workflow_file.stat()
                workflow_data.update({
                    'id': workflow_file.stem,
                    'file_path': str(workflow_file),
                    'file_size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                })
                
                workflows.append(workflow_data)
                
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Warning: Could not load workflow {workflow_file}: {e}")
                continue
        
        # Sort by creation date (newest first)
        workflows.sort(key=lambda w: w.get('created', ''), reverse=True)
        return workflows
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific workflow by ID."""
        workflow_file = self.workflow_dir / f"{workflow_id}.json"
        
        if not workflow_file.exists():
            return None
            
        try:
            with open(workflow_file, 'r') as f:
                workflow_data = json.load(f)
                
            # Add metadata
            stat = workflow_file.stat()
            workflow_data.update({
                'id': workflow_id,
                'file_path': str(workflow_file),
                'file_size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
            })
            
            return workflow_data
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading workflow {workflow_id}: {e}")
            return None
    
    def save_workflow(self, workflow_data: Dict[str, Any], workflow_id: str = None) -> str:
        """Save a workflow configuration."""
        if not workflow_id:
            # Generate new ID
            existing_ids = [w['id'] for w in self.list_workflows()]
            counter = 1
            while f"workflow_{counter}" in existing_ids:
                counter += 1
            workflow_id = f"workflow_{counter}"
        
        # Add metadata
        workflow_data.update({
            'id': workflow_id,
            'created': workflow_data.get('created', datetime.now().strftime('%Y-%m-%d %H:%M')),
            'modified': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'version': '1.0'
        })
        
        # Save to file
        workflow_file = self.workflow_dir / f"{workflow_id}.json"
        
        try:
            with open(workflow_file, 'w') as f:
                json.dump(workflow_data, f, indent=2)
                
            return workflow_id
            
        except Exception as e:
            print(f"Error saving workflow {workflow_id}: {e}")
            raise
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow."""
        workflow_file = self.workflow_dir / f"{workflow_id}.json"
        
        if not workflow_file.exists():
            return False
        
        try:
            # Create backup if enabled
            if self.config.workflow.auto_backup:
                self.backup_workflow(workflow_id)
            
            # Delete the file
            workflow_file.unlink()
            return True
            
        except Exception as e:
            print(f"Error deleting workflow {workflow_id}: {e}")
            return False
    
    def duplicate_workflow(self, workflow_id: str) -> Optional[str]:
        """Duplicate an existing workflow."""
        original_workflow = self.get_workflow(workflow_id)
        
        if not original_workflow:
            return None
        
        # Modify for duplication
        original_workflow['name'] = f"{original_workflow.get('name', 'Unnamed')} (Copy)"
        original_workflow['status'] = 'draft'
        
        # Remove metadata that shouldn't be copied
        for key in ['id', 'file_path', 'file_size', 'modified']:
            original_workflow.pop(key, None)
        
        try:
            new_id = self.save_workflow(original_workflow)
            return new_id
            
        except Exception as e:
            print(f"Error duplicating workflow {workflow_id}: {e}")
            return None
    
    def backup_workflow(self, workflow_id: str) -> bool:
        """Create a backup of a workflow."""
        workflow_file = self.workflow_dir / f"{workflow_id}.json"
        
        if not workflow_file.exists():
            return False
        
        # Create timestamped backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"{workflow_id}_{timestamp}.json"
        
        try:
            shutil.copy2(workflow_file, backup_file)
            return True
            
        except Exception as e:
            print(f"Error backing up workflow {workflow_id}: {e}")
            return False
    
    def import_workflow(self, file_path: Path) -> Optional[str]:
        """Import a workflow from an external file."""
        try:
            with open(file_path, 'r') as f:
                workflow_data = json.load(f)
            
            # Validate basic structure
            if not isinstance(workflow_data, dict):
                raise ValueError("Invalid workflow format")
            
            # Save as new workflow
            workflow_id = self.save_workflow(workflow_data)
            return workflow_id
            
        except Exception as e:
            print(f"Error importing workflow from {file_path}: {e}")
            return None
    
    def export_workflow(self, workflow_id: str, export_path: Path) -> bool:
        """Export a workflow to an external file."""
        workflow = self.get_workflow(workflow_id)
        
        if not workflow:
            return False
        
        # Remove internal metadata
        export_data = workflow.copy()
        for key in ['id', 'file_path', 'file_size', 'modified']:
            export_data.pop(key, None)
        
        try:
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            return True
            
        except Exception as e:
            print(f"Error exporting workflow {workflow_id}: {e}")
            return False
    
    def validate_workflow(self, workflow_data: Dict[str, Any]) -> List[str]:
        """Validate a workflow configuration and return any errors."""
        errors = []
        
        # Required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if not workflow_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate agents configuration
        agents = workflow_data.get('agents', [])
        if not agents:
            errors.append("Workflow must have at least one agent")
        
        # Validate workflow structure
        tasks = workflow_data.get('tasks', [])
        if not tasks:
            errors.append("Workflow must have at least one task")
        
        return errors


# ui/navigation.py - Navigation State Manager

from typing import List, Optional


class NavigationManager:
    """
    Manages navigation state and history for the terminal application.
    Provides clean back/forward navigation patterns.
    """
    
    def __init__(self):
        self.history: List[str] = []
        self.current_index = -1
        self.max_history = 50
    
    def push(self, screen_name: str) -> None:
        """Push a new screen to navigation history."""
        # Remove any forward history when pushing new screen
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        # Add new screen
        self.history.append(screen_name)
        self.current_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.current_index = len(self.history) - 1
    
    def pop(self) -> Optional[str]:
        """Go back to previous screen."""
        if self.can_go_back():
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def forward(self) -> Optional[str]:
        """Go forward to next screen."""
        if self.can_go_forward():
            self.current_index += 1
            return self.history[self.current_index]
        return None
    
    def can_go_back(self) -> bool:
        """Check if we can go back."""
        return self.current_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if we can go forward."""
        return self.current_index < len(self.history) - 1
    
    def current_screen(self) -> Optional[str]:
        """Get the current screen name."""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None
    
    def clear_history(self) -> None:
        """Clear navigation history."""
        self.history.clear()
        self.current_index = -1
    
    def get_breadcrumbs(self) -> List[str]:
        """Get breadcrumb trail for current navigation."""
        if self.current_index >= 0:
            return self.history[:self.current_index + 1]
        return []


# ui/settings_screen.py - Settings Interface

from textual.widgets import Static, Input, Button, Checkbox, Select
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.text import Text

from .styles import MAO_COLORS, get_panel_style
from config import get_config


class SettingsScreen(Static):
    """
    Configuration interface for Mao preferences and connections.
    Clean, organized settings with immediate feedback.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = get_config()
        self.changes_made = False
    
    def compose(self):
        """Compose the settings screen."""
        # Header
        header_text = Text.assemble(
            ("Mao Configuration", f"bold {MAO_COLORS['text_primary']}"),
            (" | ", ""),
            ("Customize your AI workflow experience", MAO_COLORS['text_secondary'])
        )
        
        header_panel = Panel(
            header_text,
            title="Settings",
            **get_panel_style("default")
        )
        
        # LLM Settings
        llm_settings = Vertical(
            Static(Text("Default Model", style=f"bold {MAO_COLORS['text_primary']}")),
            Select([
                ("claude-sonnet-4", "Claude Sonnet 4"),
                ("claude-opus-4", "Claude Opus 4"),
                ("claude-haiku-3.5", "Claude Haiku 3.5")
            ], value=self.config.llm.default_model, id="model-select"),
            
            Static(Text("Max Tokens", style=f"bold {MAO_COLORS['text_primary']}")),
            Input(value=str(self.config.llm.max_tokens), id="max-tokens"),
            
            Static(Text("Temperature", style=f"bold {MAO_COLORS['text_primary']}")),
            Input(value=str(self.config.llm.temperature), id="temperature"),
            
            id="llm-section"
        )
        
        # UI Settings
        ui_settings = Vertical(
            Checkbox("Enable Animations", value=self.config.ui.animations, id="animations-check"),
            Checkbox("Show Notifications", value=self.config.ui.notifications, id="notifications-check"),
            Checkbox("Auto-save Workflows", value=self.config.ui.auto_save, id="autosave-check"),
            
            id="ui-section"
        )
        
        # Workflow Settings
        workflow_settings = Vertical(
            Static(Text("Default Directory", style=f"bold {MAO_COLORS['text_primary']}")),
            Input(value=self.config.workflow.default_directory, id="workflow-dir"),
            
            Static(Text("Max Parallel Agents", style=f"bold {MAO_COLORS['text_primary']}")),
            Input(value=str(self.config.workflow.max_parallel_agents), id="max-agents"),
            
            Checkbox("Auto Backup", value=self.config.workflow.auto_backup, id="backup-check"),
            
            id="workflow-section"
        )
        
        # Action buttons
        with Horizontal(id="action-buttons"):
            yield Button("Save Changes", variant="primary", id="save-button")
            yield Button("Reset to Defaults", variant="default", id="reset-button")
            yield Button("Cancel", variant="default", id="cancel-button")
        
        with Vertical():
            yield Static(header_panel, id="settings-header")
            yield Panel(llm_settings, title="LLM Configuration", **get_panel_style("info"))
            yield Panel(ui_settings, title="User Interface", **get_panel_style("info"))
            yield Panel(workflow_settings, title="Workflow Settings", **get_panel_style("info"))
            yield Static(self.action_buttons, id="actions-section")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button interactions."""
        if event.button.id == "save-button":
            self.save_settings()
        elif event.button.id == "reset-button":
            self.reset_settings()
        elif event.button.id == "cancel-button":
            self.cancel_settings()
    
    def save_settings(self) -> None:
        """Save current settings."""
        try:
            # Update config with form values
            self.config.llm.default_model = self.query_one("#model-select", Select).value
            self.config.llm.max_tokens = int(self.query_one("#max-tokens", Input).value)
            self.config.llm.temperature = float(self.query_one("#temperature", Input).value)
            
            self.config.ui.animations = self.query_one("#animations-check", Checkbox).value
            self.config.ui.notifications = self.query_one("#notifications-check", Checkbox).value
            self.config.ui.auto_save = self.query_one("#autosave-check", Checkbox).value
            
            self.config.workflow.default_directory = self.query_one("#workflow-dir", Input).value
            self.config.workflow.max_parallel_agents = int(self.query_one("#max-agents", Input).value)
            self.config.workflow.auto_backup = self.query_one("#backup-check", Checkbox).value
            
            # Save to file
            self.config.save()
            
            self.app.notify("Settings saved successfully", severity="success")
            self.changes_made = False
            
        except Exception as e:
            self.app.notify(f"Error saving settings: {e}", severity="error")
    
    def reset_settings(self) -> None:
        """Reset settings to defaults."""
        # TODO: Show confirmation dialog
        self.app.notify("Reset functionality coming soon")
    
    def cancel_settings(self) -> None:
        """Cancel settings changes."""
        if self.changes_made:
            # TODO: Show confirmation dialog
            pass
        self.app.switch_to_screen("main-menu")