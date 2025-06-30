#!/usr/bin/env python3
"""
Mao Unified Conversation Interface
Single text input for all interactions with CLI auto-complete integration
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from rich.console import Console
from textual.widget import Widget
from textual.widgets import Input, Static
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive

# MAO imports
from .content_translator import UIContentTranslator
from .visual_language import MAO_COLORS, MAOVisualProtocol, format_workflow_message
from .components.autocomplete_system import CLIAutoCompleteSystem, CommandSelected, ContextualCommandSuggester
from ..ui_terminal import TerminalInterface


class ConversationInterface(Widget):
    """
    Unified conversation interface for all MAO interactions
    Features CLI auto-complete, workflow creation, and execution monitoring
    """
    
    conversation_history = reactive([])
    current_input = reactive("")
    
    def __init__(self, config_dir: str = "configs"):
        super().__init__()
        self.config_dir = config_dir
        self.console = Console()
        
        # Initialize core systems
        self.terminal_interface = TerminalInterface(config_dir)
        self.content_translator = UIContentTranslator()
        self.autocomplete = CLIAutoCompleteSystem(config_dir)
        self.contextual_suggester = ContextualCommandSuggester()
        self.visual_protocol = MAOVisualProtocol()
        
        # Conversation state
        self.in_workflow_creation = False
        self.current_workflow_id = None
        self.context_history = []
        self.current_context = 'user_setup'
        
    def compose(self):
        """Compose the conversation interface layout"""
        yield Vertical(
            # Conversation display area
            Container(
                Static("Welcome to Mao! Type / to see available commands or describe what you'd like to accomplish.", 
                      id="welcome-message"),
                id="conversation-display"
            ),
            
            # Input area with auto-complete
            Horizontal(
                Input(
                    placeholder="Chat with Mao or type / for commands...",
                    id="main-input"
                ),
                id="input-container"
            ),
            
            id="conversation-container"
        )
        
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission"""
        user_input = event.value.strip()
        if not user_input:
            return
            
        # Clear input
        event.input.value = ""
        
        # Add to conversation history
        await self.add_message("user", user_input)
        
        # Process the input
        await self.process_user_input(user_input)
        
    async def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for auto-complete with contextual intelligence"""
        if event.value.startswith("/"):
            # Show CLI auto-complete with contextual suggestions
            query = event.value[1:]
            base_suggestions = await self.autocomplete.get_suggestions(query)
            
            # Enhance with contextual suggestions
            contextual_suggestions = self.contextual_suggester.suggest_for_context(
                self.current_context, base_suggestions
            )
            
            # Combine and prioritize contextual suggestions
            if contextual_suggestions:
                # Put contextual suggestions first
                all_suggestions = contextual_suggestions + [
                    s for s in base_suggestions if s not in contextual_suggestions
                ]
            else:
                all_suggestions = base_suggestions
                
            await self.show_autocomplete(all_suggestions)
        else:
            await self.hide_autocomplete()
            
    async def process_user_input(self, user_input: str) -> None:
        """Process user input - CLI commands or conversational goals"""
        
        if user_input.startswith("/"):
            # CLI command
            await self.handle_cli_command(user_input[1:])
        else:
            # Conversational input - determine intent
            await self.handle_conversational_input(user_input)
            
    async def handle_cli_command(self, command: str) -> None:
        """Handle CLI command execution"""
        try:
            # Parse command and arguments
            parts = command.split()
            cmd_name = parts[0] if parts else ""
            cmd_args = " ".join(parts[1:]) if len(parts) > 1 else None
            
            # Execute through terminal interface
            result = self.terminal_interface.execute_cli_command(cmd_name, cmd_args)
            
            # Display results using content translator
            formatted_result = self.content_translator.translate_command_result(result)
            await self.add_message("assistant", formatted_result)
            
        except Exception as e:
            error_msg = self.content_translator.translate_error(str(e))
            await self.add_message("error", error_msg)
            
    async def handle_conversational_input(self, user_input: str) -> None:
        """Handle conversational workflow creation and management"""
        
        # Determine if this is workflow creation or general chat
        if self.is_workflow_goal(user_input):
            await self.start_workflow_creation(user_input)
        else:
            await self.handle_general_conversation(user_input)
            
    def is_workflow_goal(self, input_text: str) -> bool:
        """Determine if input is a workflow goal"""
        workflow_indicators = [
            "create", "build", "implement", "develop", "write", "generate",
            "help me", "i need", "can you", "make a", "design"
        ]
        
        text_lower = input_text.lower()
        return any(indicator in text_lower for indicator in workflow_indicators)
        
    async def start_workflow_creation(self, goal: str) -> None:
        """Start workflow creation process"""
        
        self.in_workflow_creation = True
        
        # Show workflow creation interface
        creation_message = self.content_translator.translate_workflow_creation(goal)
        await self.add_message("assistant", creation_message)
        
        try:
            # Create workflow through orchestrator
            workflow_result = await self.create_workflow_from_goal(goal)
            
            if workflow_result.get("success"):
                self.current_workflow_id = workflow_result.get("workflow_id")
                
                # Show workflow preview
                preview = self.content_translator.translate_workflow_preview(workflow_result)
                await self.add_message("assistant", preview)
                
                # Ask for execution confirmation
                await self.add_message("assistant", "Would you like to execute this workflow? (yes/no)")
            else:
                error_msg = self.content_translator.translate_error(workflow_result.get("error", "Unknown error"))
                await self.add_message("error", error_msg)
                
        except Exception as e:
            error_msg = self.content_translator.translate_error(str(e))
            await self.add_message("error", error_msg)
            
    async def handle_general_conversation(self, user_input: str) -> None:
        """Handle general conversational interactions"""
        
        # For now, provide helpful response directing to workflow creation
        response = self.content_translator.translate_general_response(user_input)
        await self.add_message("assistant", response)
        
    async def create_workflow_from_goal(self, goal: str) -> Dict[str, Any]:
        """Create workflow from user goal"""
        try:
            # Use orchestrator to create workflow
            workflow = await self.terminal_interface.orchestrator.create_workflow_from_goal(goal)
            return {
                "success": True,
                "workflow_id": workflow.workflow_id,
                "workflow": workflow,
                "phases": workflow.phases,
                "estimated_cost": getattr(workflow, 'estimated_cost', 'Unknown')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    async def add_message(self, role: str, content: str) -> None:
        """Add message to conversation display with MAO visual protocol"""
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Use MAO visual protocol for formatting
        formatted = self.visual_protocol.format_message(role, content)
        
        # Add to conversation history
        message_data = {
            "timestamp": timestamp,
            "role": role,
            "content": content,
            "formatted": formatted
        }
        
        self.conversation_history.append(message_data)
        
        # Update context based on conversation
        self.current_context = self.contextual_suggester.detect_context_from_conversation(
            self.conversation_history
        )
        
        # Update display
        await self.update_conversation_display()
        
    async def update_conversation_display(self) -> None:
        """Update the conversation display with latest messages"""
        
        display_container = self.query_one("#conversation-display")
        
        # Build conversation content
        conversation_content = "\n\n".join([
            msg["formatted"] for msg in self.conversation_history[-20:]  # Show last 20 messages
        ])
        
        # Update display
        display_container.update(Static(conversation_content, markup=True))
        
        # Scroll to bottom
        display_container.scroll_end()
        
    async def on_command_selected(self, message: CommandSelected) -> None:
        """Handle command selection from auto-complete"""
        command = message.command
        
        if not command:  # Empty command means close dropdown
            await self.hide_autocomplete()
            return
            
        # Insert selected command into input
        input_widget = self.query_one("#main-input")
        command_text = f"/{command.get('command', '')}"
        
        # Add space if command needs input
        if command.get('type') != 'standalone':
            command_text += " "
            
        input_widget.value = command_text
        await self.hide_autocomplete()
        
        # Focus back to input
        input_widget.focus()
        
    async def show_autocomplete(self, suggestions: List[Dict[str, Any]]) -> None:
        """Show CLI auto-complete suggestions"""
        await self.autocomplete.show_suggestions("")
        
    async def hide_autocomplete(self) -> None:
        """Hide auto-complete suggestions"""
        await self.autocomplete.hide_suggestions()
        
    async def handle_keyboard_input(self, key: str) -> bool:
        """Handle keyboard navigation for auto-complete"""
        if self.autocomplete.is_visible:
            return await self.autocomplete.handle_key_navigation(key)
        return False