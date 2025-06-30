#!/usr/bin/env python3
"""
MAO Visual Protocol Implementation
Complete visual language system based on 6_MAO_VISUAL_IDENTITY.md
"""

from typing import Dict, Any, Optional
from rich.console import Console
from rich.text import Text
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table
from textual.color import Color

# MAO Visual Protocol Colors (from 6_MAO_VISUAL_IDENTITY.md)
MAO_COLORS = {
    'pink': '#ff49ff',      # AI actions requiring attention (ONLY BOLD COLOR)
    'yellow': '#f1d771',    # AI explanations and primary content  
    'light_blue': '#82d0ff', # AI-highlighted URLs/commands and checkmarks
    'white': '#ffffff',     # System responses and AI content bullets
    'gray': '#bbbcbb',      # User input and secondary information
    'light_brown': '#7b714a', # Tree characters and metadata
    'error': '#ff6b6b'      # Error states
}

# Shape Language for Workflow States
WORKFLOW_SHAPES = {
    'orchestrator_waiting': '△',      # Mao waiting
    'orchestrator_active': '▲',       # Mao active (pulsing)
    'orchestrator_complete': '△̃',     # Mao complete (with checkmark)
    'agent_waiting': '○',             # Agent waiting
    'agent_active': '●',              # Agent active (pulsing)  
    'agent_complete': '○̃',            # Agent complete (with checkmark)
}

# Tree Characters for Relationship Mapping
TREE_CHARS = {
    'branch': '├──',      # "This flows from the parent task"
    'continue': '│',      # "Continuation of the same branch"
    'final': '└──',       # "This completes the current branch"
    'nested': '    '      # Nested indentation
}

class MAOVisualProtocol:
    """
    Complete MAO visual language implementation
    Handles all formatting, colors, shapes, and tree structures
    """
    
    def __init__(self):
        self.console = Console()
        
    def format_message(self, role: str, content: str, **kwargs) -> str:
        """Format message according to MAO visual protocol"""
        
        if role == "user":
            bullet = "●"
            color = MAO_COLORS['gray']
            
        elif role == "assistant":
            bullet = "●"  
            color = MAO_COLORS['yellow']
            
        elif role == "action":  # AI taking action
            bullet = "●"
            color = MAO_COLORS['pink']
            bold = True
            
        elif role == "system":
            bullet = "●"
            color = MAO_COLORS['white']
            
        elif role == "error":
            bullet = "●"
            color = MAO_COLORS['error']
            
        else:
            bullet = "●"
            color = MAO_COLORS['white']
            
        # Format with proper spacing (3 space indent for bullets)
        formatted = f"[{color}]{bullet}[/]   {content}"
        
        return formatted
        
    def format_workflow_status(self, role: str, message: str, state: str = 'waiting', 
                              tree_position: Optional[str] = None) -> str:
        """Format workflow status with shape language and tree structure"""
        
        # Determine shape based on role and state
        if role == 'orchestrator':
            if state == 'active':
                shape = WORKFLOW_SHAPES['orchestrator_active']
                color = MAO_COLORS['pink']  # Action requiring attention
            elif state == 'complete':
                shape = WORKFLOW_SHAPES['orchestrator_complete']
                color = MAO_COLORS['light_blue']  # Completed
            else:
                shape = WORKFLOW_SHAPES['orchestrator_waiting']
                color = MAO_COLORS['yellow']  # Explanation
                
        else:  # agent
            if state == 'active':
                shape = WORKFLOW_SHAPES['agent_active']
                color = MAO_COLORS['yellow']  # Work in progress
            elif state == 'complete':
                shape = WORKFLOW_SHAPES['agent_complete'] 
                color = MAO_COLORS['light_blue']  # Completed
            else:
                shape = WORKFLOW_SHAPES['agent_waiting']
                color = MAO_COLORS['gray']  # Waiting
                
        # Add tree structure if specified
        tree_prefix = ""
        if tree_position:
            tree_char = TREE_CHARS.get(tree_position, "")
            tree_prefix = f"[{MAO_COLORS['light_brown']}]{tree_char}[/] "
            
        formatted = f"{tree_prefix}[{color}]{shape}[/]   {message}"
        
        return formatted
        
    def format_autocomplete_command(self, command: Dict[str, Any], is_selected: bool = False) -> str:
        """Format auto-complete command item"""
        
        cmd_name = command.get('command', '')
        cmd_flag = command.get('terminal_flag', '')
        cmd_help = command.get('help', '')
        
        # Color coding
        if is_selected:
            bg_color = f"on {MAO_COLORS['light_blue']}"
            cmd_color = MAO_COLORS['white']
        else:
            bg_color = ""
            cmd_color = MAO_COLORS['light_blue']  # AI-highlighted commands
            
        formatted = f"[{cmd_color}]/{cmd_name}[/] [{MAO_COLORS['gray']}]{cmd_flag}[/]\n"
        formatted += f"    [{MAO_COLORS['gray']}]{cmd_help}[/]"
        
        if bg_color:
            formatted = f"[{bg_color}]{formatted}[/]"
            
        return formatted
        
    def create_conversation_panel(self, title: str = "Mao - AI Workflow Orchestrator") -> Panel:
        """Create main conversation panel with MAO branding"""
        
        title_text = f"[{MAO_COLORS['pink']}]~(=^‥^)[/]  {title}"
        
        return Panel(
            "",
            title=title_text,
            border_style=MAO_COLORS['light_brown'],
            padding=(0, 1)
        )
        
    def create_workflow_tree(self, workflow_data: Dict[str, Any]) -> Tree:
        """Create visual workflow tree with orchestration relationships"""
        
        # Root workflow
        root_text = f"[{MAO_COLORS['pink']}]▲[/] {workflow_data.get('goal', 'Workflow Planning')}"
        tree = Tree(root_text, style=MAO_COLORS['light_brown'])
        
        # Add phases
        phases = workflow_data.get('phases', [])
        for i, phase in enumerate(phases):
            phase_state = phase.get('state', 'waiting')
            
            if phase_state == 'active':
                shape = '●'
                color = MAO_COLORS['yellow']
            elif phase_state == 'complete':
                shape = '○̃'
                color = MAO_COLORS['light_blue']
            else:
                shape = '○'
                color = MAO_COLORS['gray']
                
            phase_text = f"[{color}]{shape}[/] {phase.get('description', f'Phase {i+1}')}"
            phase_node = tree.add(phase_text)
            
            # Add deliverables as sub-items
            deliverables = phase.get('deliverables', [])
            for deliverable in deliverables:
                deliv_text = f"[{MAO_COLORS['gray']}]{deliverable}[/]"
                phase_node.add(deliv_text)
                
        return tree
        
    def format_cycling_status(self, base_message: str, activity_messages: list, 
                             current_index: int = 0) -> str:
        """Format cycling status messages for live activity monitoring"""
        
        if not activity_messages or current_index >= len(activity_messages):
            return base_message
            
        activity = activity_messages[current_index]
        return f"{base_message}: {activity}"
        
    def create_settings_table(self, settings: Dict[str, Any]) -> Table:
        """Create settings display table with MAO styling"""
        
        table = Table(title="MAO Configuration", 
                     title_style=MAO_COLORS['pink'],
                     border_style=MAO_COLORS['light_brown'])
                     
        table.add_column("Setting", style=MAO_COLORS['yellow'])
        table.add_column("Value", style=MAO_COLORS['light_blue'])
        table.add_column("Description", style=MAO_COLORS['gray'])
        
        for setting, value in settings.items():
            desc = self.get_setting_description(setting)
            table.add_row(setting, str(value), desc)
            
        return table
        
    def get_setting_description(self, setting: str) -> str:
        """Get description for configuration settings"""
        
        descriptions = {
            'quick_launch': 'Launch app with last user logged in',
            'favorite_model': 'Use for workflows unless discussed',
            'default_provider': 'Preferred API provider for requests',
            'theme': 'Visual theme and color accessibility',
            'tone_notification': 'Workflow completion notifications',
            'cat_vibes': 'Level of cat-themed interface elements',
            'double_texting': 'Allow interrupting Mao responses'
        }
        
        return descriptions.get(setting, 'Configuration setting')
        
    def format_help_message(self, commands: list) -> str:
        """Format help message with command categories"""
        
        categories = {
            'BASICS': [],
            'WORKFLOW_CREATION': [],
            'WORKFLOW_MANAGEMENT': [],
            'USER_SETTINGS': [],
            'SYSTEM_OPERATIONS': []
        }
        
        # Categorize commands
        for cmd in commands:
            category = cmd.get('category', 'OTHER')
            if category in categories:
                categories[category].append(cmd)
                
        formatted = f"[{MAO_COLORS['pink']}]Available Commands[/]\n\n"
        
        for category, cmd_list in categories.items():
            if cmd_list:
                formatted += f"[{MAO_COLORS['yellow']}]{category}[/]\n"
                for cmd in cmd_list:
                    cmd_text = f"[{MAO_COLORS['light_blue']}]/{cmd['command']}[/]"
                    help_text = f"[{MAO_COLORS['gray']}]{cmd.get('help', '')}[/]"
                    formatted += f"   {cmd_text} - {help_text}\n"
                formatted += "\n"
                
        return formatted


def format_workflow_message(message: str, role: str = 'assistant', **kwargs) -> str:
    """Convenience function for formatting workflow messages"""
    
    protocol = MAOVisualProtocol()
    return protocol.format_message(role, message, **kwargs)
    

def create_mao_welcome_panel() -> Panel:
    """Create the main MAO welcome panel"""
    
    protocol = MAOVisualProtocol()
    return protocol.create_conversation_panel()


# Export key components for easy import
__all__ = [
    'MAO_COLORS',
    'WORKFLOW_SHAPES', 
    'TREE_CHARS',
    'MAOVisualProtocol',
    'format_workflow_message',
    'create_mao_welcome_panel'
]