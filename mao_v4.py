#!/usr/bin/env python3
"""
MAO v4 - Main Entry Point
Web UI AI orchestration system with user authentication and workflow management
Prepares backend logic for web UI integration (UI implementation to follow)
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

class MAOBackendInterface:
    """Main MAO backend interface - prepares for web UI integration"""
    
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
    
    def initialize_web_session(self, user_contact_info: str = None) -> Dict[str, Any]:
        """Initialize web session with user authentication - returns session data for web UI"""
        session_data = {
            "status": "initializing",
            "timestamp": datetime.now().isoformat(),
            "system_name": "MAO - Modular Agent Orchestrator",
            "system_description": "Web AI Workflow Orchestration System"
        }
        
        # User authentication if contact info provided
        if user_contact_info and not self.current_user_id:
            auth_result = self.authenticate_user_web(user_contact_info)
            session_data.update(auth_result)
        
        # Generate welcome message data
        if self.current_user_id:
            welcome_data = self.generate_welcome_data()
            session_data.update(welcome_data)
            session_data["status"] = "authenticated"
        else:
            session_data["status"] = "awaiting_authentication"
        
        return session_data
    
    def initialize_onboarding(self) -> Dict[str, Any]:
        """Initialize onboarding flow for new users - returns onboarding data for web UI"""
        onboarding_data = {
            "status": "onboarding",
            "welcome_message": "🚀 Welcome to MAO!",
            "description": "Let's get you set up with AI workflow orchestration.",
            "steps": [
                {
                    "step": 1,
                    "title": "Authentication",
                    "description": "Provide email or phone for UserID generation",
                    "status": "pending"
                },
                {
                    "step": 2,
                    "title": "Tutorial",
                    "description": "Learn how to create AI workflows",
                    "status": "pending"
                },
                {
                    "step": 3,
                    "title": "First Workflow",
                    "description": "Try creating your first AI workflow",
                    "status": "pending"
                }
            ],
            "current_step": 1
        }
        
        return onboarding_data
    
    def authenticate_user_web(self, contact_info: str) -> Dict[str, Any]:
        """Authenticate user and generate UserID following MAO_FLOW.md spec - returns auth data for web UI"""
        auth_result = {
            "authentication_status": "processing",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if not contact_info or not contact_info.strip():
                auth_result.update({
                    "authentication_status": "failed",
                    "error": "Contact information required for UserID generation"
                })
                return auth_result
            
            # Generate UserID using MAO_FLOW.md specification (user-####)
            user_hash = hashlib.md5(contact_info.strip().encode()).hexdigest()[:4]
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
            
            auth_result.update({
                "authentication_status": "success",
                "user_id": self.current_user_id,
                "user_profile": user_profile
            })
            
        except Exception as e:
            auth_result.update({
                "authentication_status": "error",
                "error": str(e)
            })
            logger.error(f"Authentication error: {e}")
        
        return auth_result
    
    def generate_welcome_data(self) -> Dict[str, Any]:
        """Generate AI-generated unique welcome data (never repeated) - returns welcome data for web UI"""
        # Generate unique welcome based on current time and user
        time_seed = datetime.now().strftime("%H%M%S")
        welcome_hash = hashlib.md5(f"{self.current_user_id}{time_seed}".encode()).hexdigest()[:6]
        
        welcome_data = {
            "welcome_message": f"👋 Welcome back, {self.current_user_id}!",
            "session_id": welcome_hash,
            "session_time": datetime.now().strftime('%H:%M:%S'),
            "system_message": "I can help you create and execute AI workflows from natural language goals.",
            "helpful_hints": [
                "Describe any goal in natural language",
                "Try 'help' for available commands",
                "View 'status' for your workflows"
            ],
            "user_id": self.current_user_id
        }
        
        return welcome_data
    
    def process_user_message(self, user_input: str, message_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user message and return response data for web UI"""
        response_data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self.current_user_id,
            "message_type": "response",
            "status": "processing"
        }
        
        try:
            if not user_input or not user_input.strip():
                response_data.update({
                    "status": "empty_input",
                    "message": "Please provide a message or goal to process."
                })
                return response_data
            
            user_input = user_input.strip()
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                response_data.update({
                    "status": "session_end",
                    "message": "👋 Goodbye! Your workflows are saved and can be resumed anytime."
                })
            elif user_input.lower() == 'help':
                response_data.update({
                    "status": "help",
                    "data": self.get_help_data()
                })
            elif user_input.lower() == 'status':
                response_data.update({
                    "status": "workflow_status",
                    "data": self.get_workflow_status_data()
                })
            else:
                # Process as workflow goal
                workflow_result = self.process_workflow_goal_web(user_input)
                response_data.update({
                    "status": "workflow_processed",
                    "data": workflow_result
                })
                
        except Exception as e:
            response_data.update({
                "status": "error",
                "error": str(e)
            })
            logger.error(f"Message processing error: {e}")
        
        return response_data
    
    def process_workflow_goal_web(self, goal: str) -> Dict[str, Any]:
        """Convert natural language goal into executable workflow - returns workflow data for web UI"""
        workflow_data = {
            "processing_status": "started",
            "goal": goal,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Use conversation bridge to create workflow
            workflow_result = self.conversation_bridge.create_workflow_from_conversation(goal)
            
            if workflow_result.get("success"):
                workflow_id = workflow_result["workflow_id"]
                command_name = workflow_result["custom_command"]
                
                workflow_data.update({
                    "processing_status": "success",
                    "workflow_id": workflow_id,
                    "custom_command": command_name,
                    "workflow_result": workflow_result,
                    "message": f"✅ Workflow created: {workflow_id}",
                    "actions_available": [
                        {
                            "action": "execute",
                            "label": "Execute workflow now",
                            "workflow_id": workflow_id
                        },
                        {
                            "action": "save",
                            "label": "Save for later execution",
                            "workflow_id": workflow_id
                        }
                    ]
                })
            else:
                workflow_data.update({
                    "processing_status": "failed",
                    "error": workflow_result.get('error', 'Unknown error'),
                    "message": f"❌ Workflow creation failed: {workflow_result.get('error')}"
                })
                
        except Exception as e:
            workflow_data.update({
                "processing_status": "error",
                "error": str(e),
                "message": f"❌ Goal processing error: {str(e)}"
            })
            logger.error(f"Goal processing error: {e}")
        
        return workflow_data
    
    def execute_workflow_web(self, workflow_id: str, goal: str) -> Dict[str, Any]:
        """Execute workflow and return execution data for web UI real-time updates"""
        execution_data = {
            "execution_status": "started",
            "workflow_id": workflow_id,
            "goal": goal,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Create workflow plan from goal
            workflow_plan = asyncio.run(
                self.workflow_orchestrator.create_workflow_from_goal(goal)
            )
            
            execution_data.update({
                "execution_status": "plan_created",
                "plan_name": workflow_plan.name,
                "estimated_cost": workflow_plan.total_estimated_cost,
                "estimated_duration_minutes": workflow_plan.estimated_duration_minutes,
                "phases": len(workflow_plan.phases)
            })
            
            # Execute workflow
            execution_result = asyncio.run(
                self.workflow_orchestrator.execute_workflow(workflow_plan.id)
            )
            
            if execution_result.get("success"):
                execution_data.update({
                    "execution_status": "completed",
                    "success": True,
                    "total_cost": execution_result['total_cost'],
                    "results": execution_result['results'],
                    "message": "✅ Workflow completed successfully!"
                })
            else:
                execution_data.update({
                    "execution_status": "failed",
                    "success": False,
                    "message": "❌ Workflow execution failed"
                })
                
        except Exception as e:
            execution_data.update({
                "execution_status": "error",
                "success": False,
                "error": str(e),
                "message": f"❌ Execution error: {str(e)}"
            })
            logger.error(f"Workflow execution error: {e}")
        
        return execution_data
    
    def get_help_data(self) -> Dict[str, Any]:
        """Get help information data for web UI"""
        help_data = {
            "title": "📚 MAO Help",
            "commands": [
                {
                    "command": "Natural Language Goals",
                    "description": "Type any goal in natural language to create a workflow",
                    "example": "Research market trends for electric vehicles"
                },
                {
                    "command": "status", 
                    "description": "Show active workflows",
                    "example": "status"
                },
                {
                    "command": "help",
                    "description": "Show this help message",
                    "example": "help"
                }
            ],
            "example_goals": [
                "Research market trends for electric vehicles",
                "Create a marketing plan for my new product", 
                "Analyze customer feedback and suggest improvements",
                "Write a business proposal for sustainable packaging",
                "Develop a social media strategy for my startup"
            ],
            "tips": [
                "Be specific about your goals for better results",
                "You can create multiple workflows simultaneously", 
                "All workflows are saved and can be resumed anytime",
                "Costs are estimated upfront for transparency"
            ]
        }
        
        return help_data
    
    def get_workflow_status_data(self) -> Dict[str, Any]:
        """Get workflow status data for web UI"""
        status_data = {
            "title": "📊 Workflow Status",
            "timestamp": datetime.now().isoformat(),
            "user_id": self.current_user_id
        }
        
        try:
            workflows = self.workflow_orchestrator.list_workflows()
            
            if not workflows:
                status_data.update({
                    "status": "no_workflows",
                    "message": "No workflows created yet.",
                    "suggestion": "Type a goal to create your first workflow!",
                    "workflows": []
                })
            else:
                formatted_workflows = []
                for workflow in workflows:
                    status_icon = "✅" if workflow['status'] == 'completed' else "🔄"
                    formatted_workflows.append({
                        "id": workflow['id'],
                        "name": workflow['name'],
                        "short_id": workflow['id'][:8] + "...",
                        "phases": workflow['phases'],
                        "estimated_cost": workflow['estimated_cost'],
                        "status": workflow['status'],
                        "status_icon": status_icon,
                        "description": workflow.get('description', '')
                    })
                
                status_data.update({
                    "status": "workflows_found",
                    "total_workflows": len(workflows),
                    "workflows": formatted_workflows
                })
                
        except Exception as e:
            status_data.update({
                "status": "error",
                "error": str(e),
                "message": f"❌ Error retrieving workflow status: {str(e)}"
            })
            logger.error(f"Workflow status error: {e}")
        
        return status_data
    
    def get_error_response(self, message: str) -> Dict[str, Any]:
        """Generate error response data for web UI"""
        error_response = {
            "status": "error",
            "message": f"❌ Error: {message}",
            "timestamp": datetime.now().isoformat(),
            "user_id": self.current_user_id
        }
        
        logger.error(f"Interface error: {message}")
        return error_response

def bootstrap_interface():
    """Bootstrap MAO backend interface with error recovery - prepares for web UI integration"""
    try:
        return MAOBackendInterface()
    except Exception as e:
        sys.stderr.write(f"Bootstrap error: {e}\n")
        logger.error(f"Bootstrap error: {e}")
        sys.exit(1)

@handle_errors(operation_name="main", return_dict=True)
def main():
    """MAO main entry point - Local terminal AI orchestration system"""
    
    # Special handling for 'mao mao' command - return session initialization data
    if len(sys.argv) == 2 and sys.argv[1] == "mao":
        interface = bootstrap_interface()
        session_data = interface.initialize_web_session()
        print(json.dumps(session_data, indent=2))
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
                    result = method()
                else:
                    result = method(value)
                
                # For web UI integration, print results as JSON if they're data structures
                if isinstance(result, dict):
                    print(json.dumps(result, indent=2))
                elif result:
                    print(result)
            else:
                # Method doesn't exist - show available commands
                error_data = {
                    "status": "method_not_found",
                    "error": f"Command method '{method_name}' not implemented",
                    "available_methods": [m for m in dir(interface) if not m.startswith('_') and callable(getattr(interface, m))]
                }
                print(json.dumps(error_data, indent=2))
        else:
            # No command provided - return onboarding data
            onboarding_data = interface.initialize_onboarding()
            print(json.dumps(onboarding_data, indent=2))
            
    except KeyboardInterrupt:
        goodbye_data = {
            "status": "interrupted",
            "message": "👋 MAO session interrupted. Goodbye!"
        }
        print(json.dumps(goodbye_data, indent=2))
        sys.exit(0)
    except Exception as e:
        error_data = interface.get_error_response(f"Command execution error: {str(e)}")
        print(json.dumps(error_data, indent=2))
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
