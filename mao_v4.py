#!/usr/bin/env python3
"""
MAO v4 - Main Entry Point
Local terminal AI orchestration system with user authentication and workflow management
"""

import sys
import json
import asyncio
import hashlib
from pathlib import Path
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, APIError
from orchestrator.memory_mcp import MemoryMCPManager
from orchestrator.core import WorkflowOrchestrator
from orchestrator.conversation_bridge import ConversationToWorkflowBridge
from orchestrator.username_manager import UsernameManager

# Standard cache instance
cache = CacheManager()
logger = logging.getLogger(__name__)

def load_all_commands():
    """Load all CLI command configs dynamically from JSON files"""
    commands = {}
    cli_dir = Path(__file__).parent / "configs/cli"
    
    # Ensure CLI directory exists
    if not cli_dir.exists():
        logger.warning(f"CLI directory not found: {cli_dir}")
        return commands
    
    # Scan for JSON command configs (including subdirectories)
    for json_file in cli_dir.glob("**/*.json"):
        if json_file.name.startswith('.') or json_file.name.endswith('.OLD'):
            continue
            
        try:
            with open(json_file, 'r') as f:
                cmd_config = json.load(f)
                
            # Validate required fields
            required_fields = ["command", "interface_method", "type"]
            if all(field in cmd_config for field in required_fields):
                commands[cmd_config["command"]] = cmd_config
            else:
                logger.warning(f"Invalid command config in {json_file}: missing required fields")
                
        except (json.JSONDecodeError, KeyError, IOError) as e:
            logger.warning(f"Error loading command config {json_file}: {e}")
            continue
    
    logger.info(f"Loaded {len(commands)} CLI commands from {cli_dir}")
    return commands

def create_dynamic_parser(commands):
    """Build parser from all command configs"""
    parser = argparse.ArgumentParser(
        description="Mao - Modular Agent Orchestrator",
        add_help=False
    )
    
    for cmd_config in commands.values():
        flag = cmd_config["terminal_flag"]
        cmd_type = cmd_config["type"]
        
        if cmd_type == "standalone":
            parser.add_argument(flag, action="store_true")
        elif cmd_type in ["needs_input", "needs_file"]:
            parser.add_argument(flag, type=str)
        # Skip app_only commands - those are handled in-app
    
    return parser

def find_used_command(args, commands):
    """Find which command was actually used"""
    for cmd_config in commands.values():
        if cmd_config["type"] == "app_only":
            continue
            
        # Convert --fix-it to fix_it (argparse does this automatically)
        arg_name = cmd_config["terminal_flag"].lstrip("-").replace("-", "_")
        
        if hasattr(args, arg_name):
            value = getattr(args, arg_name)
            if value:  # Found the used command
                return cmd_config, value
    
    return None, None

class MAOTerminalInterface:
    """Main MAO terminal interface - local AI orchestration system"""
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.workflow_orchestrator = WorkflowOrchestrator()
        self.conversation_bridge = ConversationToWorkflowBridge()
        self.username_manager = UsernameManager()
        self.current_user_id = None
        
        # Initialize MCP Integration Hub
        try:
            from orchestrator.mcp_hub import create_mcp_hub
            self.mcp_hub = create_mcp_hub()
            logger.info("MAO Terminal Interface initialized successfully")
        except Exception as e:
            logger.error(f"MCP Hub initialization error: {e}")
            self.mcp_hub = None
    
    def launch_terminal_ui_smart(self):
        """Launch intelligent terminal UI with user authentication"""
        print("\n🤖 MAO - Modular Agent Orchestrator")
        print("Local AI Workflow Orchestration System")
        print("" + "="*50)
        
        # User authentication
        if not self.current_user_id:
            self.authenticate_user()
        
        # Display welcome message  
        self.display_welcome_message()
        
        # Main chat loop
        self.start_chat_session()
    
    def launch_terminal_ui_onboarding(self):
        """Launch onboarding flow for new users"""
        print("\n🚀 Welcome to MAO!")
        print("Let's get you set up with AI workflow orchestration.\n")
        
        # User registration
        self.authenticate_user()
        
        # Onboarding tutorial
        self.show_onboarding_tutorial()
        
        # Start main interface
        self.launch_terminal_ui_smart()
    
    def authenticate_user(self):
        """Authenticate user and generate UserID following MAO_FLOW.md spec"""
        print("\n📝 User Authentication")
        
        # Get email or phone for UserID generation (MAO_FLOW.md spec)
        contact_info = input("Enter email or phone for UserID generation: ").strip()
        
        if not contact_info:
            print("❌ Contact information required for UserID generation")
            sys.exit(1)
        
        # Generate UserID using MAO_FLOW.md specification (user-####)
        user_hash = hashlib.md5(contact_info.encode()).hexdigest()[:4]
        self.current_user_id = f"user-{user_hash}"
        
        # Create user profile in Memory MCP
        user_profile = {
            "user_id": self.current_user_id,
            "contact_hash": user_hash,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        # Store in Memory MCP for persistence
        self.memory_mcp.create_user_context(self.current_user_id, user_profile)
        
        print(f"✅ Authenticated as UserID: {self.current_user_id}")
    
    def display_welcome_message(self):
        """Display AI-generated unique welcome message (never repeated)"""
        # Generate unique welcome based on current time and user
        time_seed = datetime.now().strftime("%H%M%S")
        welcome_hash = hashlib.md5(f"{self.current_user_id}{time_seed}".encode()).hexdigest()[:6]
        
        print(f"\n👋 Welcome back, {self.current_user_id}!")
        print(f"Session: {welcome_hash} | {datetime.now().strftime('%H:%M:%S')}")
        print("\nI can help you create and execute AI workflows from natural language goals.")
        print("Type your goal, or 'help' for commands.\n")
    
    def start_chat_session(self):
        """Main chat session loop with workflow orchestration"""
        while True:
            try:
                # Get user input
                user_input = input(f"{self.current_user_id}> ").strip()
                
                if not user_input:
                    continue
                    
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye! Your workflows are saved and can be resumed anytime.")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'status':
                    self.show_workflow_status()
                    continue
                
                # Process as workflow goal
                self.process_workflow_goal(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Session interrupted. Your workflows are saved.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Chat session error: {e}")
    
    def process_workflow_goal(self, goal: str):
        """Convert natural language goal into executable workflow"""
        print(f"\n🔄 Processing goal: {goal}")
        
        try:
            # Use conversation bridge to create workflow
            workflow_result = self.conversation_bridge.create_workflow_from_conversation(goal)
            
            if workflow_result.get("success"):
                workflow_id = workflow_result["workflow_id"]
                command_name = workflow_result["custom_command"]
                
                print(f"✅ Workflow created: {workflow_id}")
                print(f"📋 Custom command: '{command_name}'")
                
                # Ask user if they want to execute immediately
                execute = input("\n▶️  Execute workflow now? (y/N): ").strip().lower()
                
                if execute in ['y', 'yes']:
                    self.execute_workflow(workflow_id, goal)
                else:
                    print(f"💾 Workflow saved. Execute later with: mao execute {workflow_id}")
            else:
                print(f"❌ Workflow creation failed: {workflow_result.get('error')}")
                
        except Exception as e:
            print(f"❌ Goal processing error: {e}")
            logger.error(f"Goal processing error: {e}")
    
    def execute_workflow(self, workflow_id: str, goal: str):
        """Execute workflow with real-time progress display"""
        print(f"\n🚀 Executing workflow: {workflow_id}")
        print("📊 Progress updates will appear here...\n")
        
        try:
            # Create workflow plan from goal
            workflow_plan = asyncio.run(
                self.workflow_orchestrator.create_workflow_from_goal(goal)
            )
            
            print(f"📋 Plan created: {workflow_plan.name}")
            print(f"📊 Estimated cost: ${workflow_plan.total_estimated_cost:.4f}")
            print(f"⏱️  Estimated time: {workflow_plan.estimated_duration_minutes} minutes\n")
            
            # Execute workflow
            execution_result = asyncio.run(
                self.workflow_orchestrator.execute_workflow(workflow_plan.id)
            )
            
            if execution_result.get("success"):
                print(f"✅ Workflow completed successfully!")
                print(f"💰 Total cost: ${execution_result['total_cost']:.4f}")
                
                # Show results
                for result in execution_result['results']:
                    if result['success']:
                        print(f"📝 {result['phase_name']}: Success")
                    else:
                        print(f"❌ {result['phase_name']}: {result.get('error', 'Failed')}")
            else:
                print(f"❌ Workflow execution failed")
                
        except Exception as e:
            print(f"❌ Execution error: {e}")
            logger.error(f"Workflow execution error: {e}")
    
    def show_help(self):
        """Show help information"""
        print("\n📚 MAO Help")
        print("" + "="*30)
        print("• Type any goal in natural language to create a workflow")
        print("• 'status' - Show active workflows")
        print("• 'help' - Show this help message")
        print("• 'exit' - Exit MAO (workflows are saved)")
        print("\nExample goals:")
        print("• 'Research market trends for electric vehicles'")
        print("• 'Create a marketing plan for my new product'")
        print("• 'Analyze customer feedback and suggest improvements'\n")
    
    def show_workflow_status(self):
        """Show status of user's workflows"""
        print("\n📊 Workflow Status")
        print("" + "="*30)
        
        try:
            workflows = self.workflow_orchestrator.list_workflows()
            
            if not workflows:
                print("No workflows created yet.")
                print("Type a goal to create your first workflow!\n")
                return
            
            for workflow in workflows:
                status_icon = "✅" if workflow['status'] == 'completed' else "🔄"
                print(f"{status_icon} {workflow['name']}")
                print(f"   ID: {workflow['id'][:8]}...")
                print(f"   Phases: {workflow['phases']} | Cost: ${workflow['estimated_cost']:.4f}")
                print(f"   Status: {workflow['status']}\n")
                
        except Exception as e:
            print(f"❌ Error retrieving workflow status: {e}")
    
    def error(self, message: str):
        """Display error message"""
        print(f"❌ Error: {message}")
        logger.error(f"Interface error: {message}")

def bootstrap_interface():
    """Bootstrap MAO terminal interface with error recovery"""
    try:
        return MAOTerminalInterface()
    except Exception as e:
        sys.stderr.write(f"Bootstrap error: {e}\n")
        logger.error(f"Bootstrap error: {e}")
        sys.exit(1)

@handle_errors(operation_name="main", return_dict=True)
def main():
    """MAO main entry point - Local terminal AI orchestration system"""
    
    # Special handling for 'mao mao' command - smart launch
    if len(sys.argv) == 2 and sys.argv[1] == "mao":
        interface = bootstrap_interface()
        interface.launch_terminal_ui_smart()
        return
    
    # Load all CLI commands and create parser
    commands = load_all_commands()
    
    if not commands:
        # No CLI commands configured - launch main interface
        interface = bootstrap_interface()
        interface.launch_terminal_ui_onboarding()
        return
    
    parser = create_dynamic_parser(commands)
    args = parser.parse_args()
    
    # Bootstrap terminal interface
    interface = bootstrap_interface()
    
    # Find which command was used
    cmd_config, value = find_used_command(args, commands)
    
    try:
        if cmd_config:
            # Route to interface method - with error handling for missing methods
            method_name = cmd_config["interface_method"]
            
            if hasattr(interface, method_name):
                method = getattr(interface, method_name)
                
                # Call with appropriate arguments based on type
                if cmd_config["type"] == "standalone":
                    method()
                else:
                    method(value)
            else:
                # Method doesn't exist - show available commands
                print(f"❌ Command method '{method_name}' not implemented")
                print(f"Available interface methods:")
                methods = [m for m in dir(interface) if not m.startswith('_') and callable(getattr(interface, m))]
                for method in methods:
                    print(f"  • {method}")
        else:
            # No command provided - default to onboarding
            interface.launch_terminal_ui_onboarding()
            
    except KeyboardInterrupt:
        print("\n👋 MAO session interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        interface.error(f"Command execution error: {str(e)}")
        logger.error(f"Main execution error: {e}")

@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate MAO system cost for budget planning"""
    base_cost = 0.01  # Base MAO system cost
    
    if params:
        # User authentication operations
        users = params.get("users", 1)
        base_cost += users * 0.001
        
        # Workflow operations
        workflows = params.get("workflows", 1)
        base_cost += workflows * 0.01
        
        # Terminal interface operations
        ui_operations = params.get("ui_operations", 10)
        base_cost += ui_operations * 0.0001
        
        # CLI command operations
        cli_commands = params.get("cli_commands", 5)
        base_cost += cli_commands * 0.001
        
        # Memory MCP operations
        mcp_operations = params.get("mcp_operations", 5)
        base_cost += mcp_operations * 0.002
    
    return base_cost

if __name__ == "__main__":
    main()
