#!/usr/bin/env python3
"""
MAO CLI Auto-Complete System
Claude Code-style command discovery with fuzzy search and categorization
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.message import Message
from textual.reactive import reactive

from ..visual_language import MAO_COLORS, MAOVisualProtocol


class CLICommandScanner:
    """Dynamic CLI command discovery from configs/cli/ directory"""
    
    def __init__(self, config_path: str = "./configs/cli/"):
        self.config_path = Path(config_path)
        self.commands = {}
        self.last_scan = None
        
    def scan_commands(self) -> Dict[str, Any]:
        """Scan configs/cli/ directory for all command configurations"""
        commands = {}
        
        if not self.config_path.exists():
            return commands
            
        for command_dir in self.config_path.iterdir():
            if command_dir.is_dir():
                json_file = command_dir / f"{command_dir.name}.json"
                if json_file.exists():
                    try:
                        with open(json_file) as f:
                            command_data = json.load(f)
                            commands[command_dir.name] = {
                                **command_data,
                                "category": self.categorize_command(command_data)
                            }
                    except (json.JSONDecodeError, IOError):
                        continue
        
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
        
    def get_commands(self, refresh: bool = False) -> Dict[str, Any]:
        """Get cached commands or refresh if needed"""
        if refresh or not self.commands or not self.last_scan:
            return self.scan_commands()
        return self.commands


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
                scored.append({**cmd_data, 'score': score, 'name': cmd_name})
                
        return sorted(scored, key=lambda x: x['score'], reverse=True)[:limit]
        
    def calculate_score(self, query: str, command: Dict[str, Any]) -> float:
        """Calculate relevance score for command"""
        searchable_text = f"{command.get('name', '')} {command.get('command', '')} {command.get('help', '')}".lower()
        query_lower = query.lower()
        
        # Exact match gets highest score
        if query_lower in searchable_text:
            return 100.0
            
        # Command name starts with query gets high score
        if command.get('command', '').lower().startswith(query_lower):
            return 90.0
            
        # Fuzzy matching based on character presence and order
        score = 0.0
        query_index = 0
        
        for char in searchable_text:
            if query_index < len(query_lower) and char == query_lower[query_index]:
                score += len(query_lower) - query_index
                query_index += 1
                
        return score if query_index == len(query_lower) else 0.0


class CommandSelected(Message):
    """Message sent when command is selected from auto-complete"""
    
    def __init__(self, command: Dict[str, Any]):
        super().__init__()
        self.command = command


class AutoCompleteDropdown(Widget):
    """Dropdown widget showing categorized command suggestions"""
    
    suggestions = reactive([])
    selected_index = reactive(0)
    
    def __init__(self, suggestions: List[Dict[str, Any]] = None):
        super().__init__()
        self.visual_protocol = MAOVisualProtocol()
        self.suggestions = suggestions or []
        self.selected_index = 0
        
    def compose(self):
        """Compose dropdown layout with categorized commands"""
        if not self.suggestions:
            return
            
        # Group suggestions by category
        categories = {}
        for i, suggestion in enumerate(self.suggestions):
            category = suggestion.get('category', 'OTHER')
            if category not in categories:
                categories[category] = []
            categories[category].append((i, suggestion))
            
        containers = []
        
        for category, commands in categories.items():
            # Category header
            category_header = Static(
                f"[{MAO_COLORS['light_brown']}]{category}[/]",
                classes="category-header"
            )
            containers.append(category_header)
            
            # Commands in category
            for global_index, command in commands:
                is_selected = global_index == self.selected_index
                command_item = self.create_command_item(command, is_selected)
                containers.append(command_item)
                
        yield Vertical(*containers, id="dropdown-content")
        
    def create_command_item(self, command: Dict[str, Any], is_selected: bool):
        """Create individual command item widget"""
        
        cmd_name = command.get('command', '')
        cmd_flag = command.get('terminal_flag', '')
        cmd_help = command.get('help', '')
        cmd_type = command.get('type', 'standalone')
        
        # Format command display
        if is_selected:
            name_text = f"[{MAO_COLORS['white']} on {MAO_COLORS['light_blue']}]/{cmd_name}[/]"
            flag_text = f"[{MAO_COLORS['gray']} on {MAO_COLORS['light_blue']}]{cmd_flag}[/]"
            help_text = f"[{MAO_COLORS['gray']} on {MAO_COLORS['light_blue']}]{cmd_help}[/]"
        else:
            name_text = f"[{MAO_COLORS['light_blue']}]/{cmd_name}[/]"
            flag_text = f"[{MAO_COLORS['gray']}]{cmd_flag}[/]"
            help_text = f"[{MAO_COLORS['gray']}]{cmd_help}[/]"
            
        # Create type badge
        type_badge = self.create_type_badge(cmd_type, is_selected)
        
        return Container(
            Horizontal(
                Static(name_text, classes="command-name"),
                Static(flag_text, classes="command-flag"),
                Static(type_badge, classes="type-badge"),
            ),
            Static(help_text, classes="command-help"),
            classes="command-item selected" if is_selected else "command-item"
        )
        
    def create_type_badge(self, cmd_type: str, is_selected: bool) -> str:
        """Create type badge for command"""
        
        type_colors = {
            'standalone': MAO_COLORS['light_blue'],
            'needs_input': MAO_COLORS['yellow'], 
            'needs_file_or_directory': MAO_COLORS['pink']
        }
        
        color = type_colors.get(cmd_type, MAO_COLORS['gray'])
        badge_text = cmd_type.replace('_', ' ').title()
        
        if is_selected:
            return f"[{MAO_COLORS['white']} on {color}]{badge_text}[/]"
        else:
            return f"[{color}]{badge_text}[/]"
            
    async def handle_key_navigation(self, key: str) -> bool:
        """Handle keyboard navigation in dropdown"""
        if not self.suggestions:
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
                self.post_message(CommandSelected(selected_cmd))
            return True
        elif key == "escape":
            self.post_message(CommandSelected({}))  # Empty command to close
            return True
            
        return False


class CLIAutoCompleteSystem(Widget):
    """
    Complete CLI auto-complete system with Claude Code-style interface
    Integrates command discovery, fuzzy search, and dropdown display
    """
    
    is_visible = reactive(False)
    current_query = reactive("")
    suggestions = reactive([])
    selected_index = reactive(0)
    
    def __init__(self, config_dir: str):
        super().__init__()
        self.scanner = CLICommandScanner(f"{config_dir}/cli")
        self.fuzzy_search = FuzzySearchEngine()
        self.visual_protocol = MAOVisualProtocol()
        self.dropdown = None
        
    async def get_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """Get auto-complete suggestions for query"""
        # Refresh commands if needed
        commands = self.scanner.get_commands(refresh=False)
        
        # Get fuzzy search results
        suggestions = self.fuzzy_search.search(query, commands, limit=10)
        
        self.suggestions = suggestions
        self.current_query = query
        return suggestions
        
    async def show_suggestions(self, query: str):
        """Show auto-complete dropdown with suggestions"""
        suggestions = await self.get_suggestions(query)
        
        if suggestions:
            self.is_visible = True
            self.suggestions = suggestions
            self.selected_index = 0
            
            # Create or update dropdown
            if self.dropdown:
                await self.dropdown.remove()
                
            self.dropdown = AutoCompleteDropdown(suggestions)
            await self.mount(self.dropdown)
        else:
            await self.hide_suggestions()
            
    async def hide_suggestions(self):
        """Hide auto-complete dropdown"""
        self.is_visible = False
        self.suggestions = []
        
        if self.dropdown:
            await self.dropdown.remove()
            self.dropdown = None
            
    async def handle_key_navigation(self, key: str) -> bool:
        """Handle keyboard navigation"""
        if not self.is_visible or not self.dropdown:
            return False
            
        return await self.dropdown.handle_key_navigation(key)
        
    async def select_current_command(self) -> Optional[Dict[str, Any]]:
        """Select the currently highlighted command"""
        if self.is_visible and self.suggestions and self.selected_index < len(self.suggestions):
            return self.suggestions[self.selected_index]
        return None
        
    def compose(self):
        """Compose auto-complete system layout"""
        if self.is_visible and self.dropdown:
            yield self.dropdown


# Context-aware command suggestions (for advanced integration)
class ContextualCommandSuggester:
    """Provides contextual command suggestions based on workflow state"""
    
    def __init__(self):
        self.context_patterns = {
            'workflow_creation': ['setup', 'update', 'review', 'goal'],
            'workflow_execution': ['stats', 'logs', 'continue', 'verbose'],
            'workflow_complete': ['review', 'workflows', 'stats'],
            'user_setup': ['config', 'login', 'logout', 'user_id']
        }
        
    def suggest_for_context(self, context: str, available_commands: List[Dict]) -> List[Dict]:
        """Get command suggestions for specific context"""
        
        suggested_command_names = self.context_patterns.get(context, [])
        
        # Filter available commands to match suggestions
        contextual_commands = []
        for cmd in available_commands:
            if cmd.get('command', '') in suggested_command_names:
                contextual_commands.append(cmd)
                
        return contextual_commands
        
    def detect_context_from_conversation(self, messages: List[Dict]) -> str:
        """Analyze conversation to determine current context"""
        
        if not messages:
            return 'user_setup'
            
        recent_content = ' '.join([
            msg.get('content', '').lower() 
            for msg in messages[-5:]  # Last 5 messages
        ])
        
        if any(keyword in recent_content for keyword in ['create', 'build', 'implement', 'goal']):
            return 'workflow_creation'
        elif any(keyword in recent_content for keyword in ['executing', 'running', 'progress']):
            return 'workflow_execution'  
        elif any(keyword in recent_content for keyword in ['completed', 'finished', 'done']):
            return 'workflow_complete'
        else:
            return 'user_setup'


# Export key components
__all__ = [
    'CLICommandScanner',
    'FuzzySearchEngine', 
    'CLIAutoCompleteSystem',
    'AutoCompleteDropdown',
    'CommandSelected',
    'ContextualCommandSuggester'
]