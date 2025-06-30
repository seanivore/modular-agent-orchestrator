#!/usr/bin/env python3
"""
MAO Content Translator
Converts ui_terminal.py information into beautiful MAO visual protocol components
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

from .visual_language import MAO_COLORS, WORKFLOW_SHAPES, MAOVisualProtocol


class UIContentTranslator:
    """
    Converts ui_terminal.py print statements into MAO visual protocol components
    Preserves all functionality while enhancing with beautiful interface design
    """
    
    def __init__(self):
        self.visual_protocol = MAOVisualProtocol()
        self.console = Console()
        
    def translate_command_result(self, result: Dict[str, Any]) -> str:
        """Translate CLI command execution results"""
        
        if result.get('success'):
            message = result.get('message', 'Command executed successfully')
            return self.visual_protocol.format_message('assistant', message)
        else:
            error = result.get('error', 'Command failed')
            return self.visual_protocol.format_message('error', error)
            
    def translate_workflow_creation(self, goal: str) -> str:
        """Translate workflow creation process"""
        
        messages = [
            self.visual_protocol.format_workflow_status(
                'orchestrator', 
                'Analyzing your goal...', 
                'active'
            ),
            self.visual_protocol.format_workflow_status(
                'orchestrator',
                'Creating workflow structure',
                'active', 
                'branch'
            ),
            self.visual_protocol.format_workflow_status(
                'orchestrator',
                'Selecting optimal models',
                'active',
                'branch'  
            ),
            self.visual_protocol.format_workflow_status(
                'orchestrator',
                'Ready to begin execution',
                'complete',
                'final'
            )
        ]
        
        return '\n'.join(messages)
        
    def translate_workflow_preview(self, workflow_result: Dict[str, Any]) -> str:
        """Translate workflow preview display"""
        
        workflow = workflow_result.get('workflow')
        phases = workflow_result.get('phases', [])
        
        preview_lines = [
            f"[{MAO_COLORS['pink']}]Workflow Created![/]",
            f"[{MAO_COLORS['yellow']}]ID:[/] {workflow_result.get('workflow_id')}",
            f"[{MAO_COLORS['yellow']}]Phases:[/] {len(phases)}",
            f"[{MAO_COLORS['yellow']}]Estimated Cost:[/] {workflow_result.get('estimated_cost', 'Unknown')}",
            ""
        ]
        
        # Add phase overview
        for i, phase in enumerate(phases, 1):
            phase_line = self.visual_protocol.format_workflow_status(
                'agent',
                f"Phase {i}: {phase.get('description', f'Phase {i}')}",
                'waiting',
                'branch' if i < len(phases) else 'final'
            )
            preview_lines.append(phase_line)
            
        return '\n'.join(preview_lines)
        
    def translate_execution_progress(self, phase_data: Dict[str, Any]) -> str:
        """Translate execution progress into live progress display"""
        
        phase_name = phase_data.get('name', 'Unknown Phase')
        progress_percent = phase_data.get('progress', 0)
        current_task = phase_data.get('current_task', 'Processing...')
        
        # Create cycling status message
        base_message = f"Phase: {phase_name}"
        activity_messages = phase_data.get('activities', [current_task])
        current_index = phase_data.get('activity_index', 0)
        
        status_message = self.visual_protocol.format_cycling_status(
            base_message, activity_messages, current_index
        )
        
        progress_line = self.visual_protocol.format_workflow_status(
            'agent',
            f"{status_message} ({progress_percent}% complete)",
            'active'
        )
        
        return progress_line
        
    def translate_agent_spawning(self, agent_data: Dict[str, Any]) -> str:
        """Translate agent spawning visualization"""
        
        agent_name = agent_data.get('name', 'New Agent')
        agent_role = agent_data.get('role', 'Agent')
        tools = agent_data.get('tools', [])
        
        spawn_lines = [
            self.visual_protocol.format_workflow_status(
                'orchestrator',
                f'Spawning {agent_role}',
                'active'
            ),
            self.visual_protocol.format_workflow_status(
                'agent',
                f'Setting up workspace',
                'waiting',
                'branch'
            ),
            self.visual_protocol.format_workflow_status(
                'agent', 
                f'Loading tools: {", ".join(tools[:3])}{"..." if len(tools) > 3 else ""}',
                'waiting',
                'final'
            )
        ]
        
        return '\n'.join(spawn_lines)
        
    def translate_completion_summary(self, completion_data: Dict[str, Any]) -> str:
        """Translate workflow completion summary"""
        
        workflow_id = completion_data.get('workflow_id')
        deliverables = completion_data.get('deliverables', [])
        total_cost = completion_data.get('total_cost', 'Unknown')
        duration = completion_data.get('duration', 'Unknown')
        
        summary_lines = [
            f"[{MAO_COLORS['pink']}]Workflow Complete![/]",
            f"[{MAO_COLORS['yellow']}]ID:[/] {workflow_id}",
            f"[{MAO_COLORS['yellow']}]Duration:[/] {duration}",
            f"[{MAO_COLORS['yellow']}]Total Cost:[/] {total_cost}",
            "",
            f"[{MAO_COLORS['yellow']}]Deliverables:[/]"
        ]
        
        for deliverable in deliverables:
            deliv_line = f"[{MAO_COLORS['light_brown']}]├──[/] [{MAO_COLORS['light_blue']}]{deliverable}[/]"
            summary_lines.append(deliv_line)
            
        return '\n'.join(summary_lines)
        
    def translate_error(self, error_message: str) -> str:
        """Translate error messages with proper formatting"""
        
        return self.visual_protocol.format_message('error', f"Error: {error_message}")
        
    def translate_general_response(self, user_input: str) -> str:
        """Translate general conversational responses"""
        
        # Analyze input to provide helpful response
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm ready to help you create and execute AI workflows. What would you like to build?"
        elif any(word in input_lower for word in ['help', 'how', 'what']):
            response = "I can help you create workflows for any task. Try describing what you want to accomplish, or type /help to see available commands."
        else:
            response = "I'd be happy to help! It sounds like you might want to create a workflow. Could you describe your goal in more detail?"
            
        return self.visual_protocol.format_message('assistant', response)
        
    def translate_cost_tracking(self, cost_data: Dict[str, Any]) -> str:
        """Translate cost tracking information"""
        
        current_cost = cost_data.get('current_cost', 0)
        estimated_total = cost_data.get('estimated_total', 0)
        budget_limit = cost_data.get('budget_limit')
        
        cost_line = f"[{MAO_COLORS['yellow']}]Cost:[/] ${current_cost:.4f}"
        
        if estimated_total:
            cost_line += f" / ${estimated_total:.4f} estimated"
            
        if budget_limit:
            percentage = (current_cost / budget_limit) * 100
            if percentage > 80:
                color = MAO_COLORS['error']
            elif percentage > 60:
                color = MAO_COLORS['yellow']
            else:
                color = MAO_COLORS['light_blue']
                
            cost_line += f" ([{color}]{percentage:.1f}% of budget[/])"
            
        return cost_line
        
    def translate_user_settings(self, settings: Dict[str, Any]) -> str:
        """Translate user settings display"""
        
        settings_lines = [
            f"[{MAO_COLORS['pink']}]Current Settings[/]",
            ""
        ]
        
        for setting, value in settings.items():
            setting_display = setting.replace('_', ' ').title()
            value_display = str(value)
            
            setting_line = f"[{MAO_COLORS['yellow']}]{setting_display}:[/] [{MAO_COLORS['light_blue']}]{value_display}[/]"
            settings_lines.append(setting_line)
            
        settings_lines.append("")
        settings_lines.append(f"[{MAO_COLORS['gray']}]Use /config to modify settings[/]")
        
        return '\n'.join(settings_lines)
        
    def translate_workflow_list(self, workflows: List[Dict[str, Any]]) -> str:
        """Translate workflow list display"""
        
        if not workflows:
            return self.visual_protocol.format_message('assistant', 'No workflows found. Create your first workflow by describing a goal!')
            
        list_lines = [
            f"[{MAO_COLORS['pink']}]Your Workflows[/]",
            ""
        ]
        
        for workflow in workflows:
            workflow_id = workflow.get('workflow_id', 'Unknown')
            goal = workflow.get('goal', 'No goal specified')
            status = workflow.get('status', 'unknown')
            
            # Determine status symbol and color
            if status == 'completed':
                symbol = '○̃'
                color = MAO_COLORS['light_blue']
            elif status == 'running':
                symbol = '●'
                color = MAO_COLORS['yellow']
            elif status == 'failed':
                symbol = '○'
                color = MAO_COLORS['error']
            else:
                symbol = '○'
                color = MAO_COLORS['gray']
                
            workflow_line = f"[{color}]{symbol}[/]   [{MAO_COLORS['light_blue']}]{workflow_id}[/] - {goal}"
            list_lines.append(workflow_line)
            
        return '\n'.join(list_lines)
        
    def translate_tool_activities(self, tools: List[Dict[str, Any]]) -> str:
        """Translate tool usage into elegant status indicators"""
        
        if not tools:
            return ""
            
        tool_lines = []
        for tool in tools:
            tool_name = tool.get('name', 'Unknown Tool')
            tool_status = tool.get('status', 'idle')
            tool_activity = tool.get('current_activity', '')
            
            if tool_status == 'active':
                symbol = '●'
                color = MAO_COLORS['yellow']
                status_text = tool_activity or 'Working...'
            elif tool_status == 'complete':
                symbol = '○̃'
                color = MAO_COLORS['light_blue']
                status_text = 'Complete'
            else:
                symbol = '○'
                color = MAO_COLORS['gray']
                status_text = 'Ready'
                
            tool_line = f"[{MAO_COLORS['light_brown']}]├──[/] [{color}]{symbol}[/] {tool_name}: {status_text}"
            tool_lines.append(tool_line)
            
        return '\n'.join(tool_lines)
        
    def translate_memory_status(self, memory_data: Dict[str, Any]) -> str:
        """Translate Memory MCP status and information"""
        
        status = memory_data.get('status', 'unknown')
        stored_items = memory_data.get('stored_items', 0)
        last_update = memory_data.get('last_update')
        
        if status == 'connected':
            color = MAO_COLORS['light_blue']
            status_text = 'Connected'
        elif status == 'error':
            color = MAO_COLORS['error']
            status_text = 'Error'
        else:
            color = MAO_COLORS['gray']
            status_text = 'Disconnected'
            
        memory_line = f"[{color}]Memory MCP:[/] {status_text}"
        
        if stored_items:
            memory_line += f" ({stored_items} items stored)"
            
        if last_update:
            memory_line += f" [Last update: {last_update}]"
            
        return memory_line


# Export key components
__all__ = [
    'UIContentTranslator'
]