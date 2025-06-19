### **Quality Framework Integration**

**Success Criteria Validation System:**
```python
# orchestrator/quality_framework.py
class QualityFramework:
    """Automated quality validation and improvement system"""
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        
    def validate_deliverable(self, workflow_id: str, deliverable: dict, criteria: dict):
        """Validate deliverable against success criteria"""
        
        validation_results = {
            "workflow_id": workflow_id,
            "deliverable_id": deliverable.get("id"),
            "validation_timestamp": datetime.now().isoformat(),
            "criteria_results": {},
            "overall_score": 0,
            "pass_threshold": criteria.get("pass_threshold", 0.7),
            "recommendations": []
        }
        
        total_weight = 0
        weighted_score = 0
        
        for criterion_name, criterion_config in criteria.get("validation_rules", {}).items():
            result = self._evaluate_criterion(deliverable, criterion_config)
            
            validation_results["criteria_results"][criterion_name] = {
                "score": result["score"],
                "weight": criterion_config.get("weight", 1.0),
                "status": "pass" if result["score"] >= criterion_config.get("threshold", 0.5) else "fail",
                "feedback": result.get("feedback", ""),
                "suggestions": result.get("suggestions", [])
            }
            
            weight = criterion_config.get("weight", 1.0)
            weighted_score += result["score"] * weight
            total_weight += weight
        
        # Calculate overall score
        validation_results["overall_score"] = weighted_score / total_weight if total_weight > 0 else 0
        validation_results["overall_status"] = "pass" if validation_results["overall_score"] >= validation_results["pass_threshold"] else "fail"
        
        # Generate improvement recommendations
        if validation_results["overall_status"] == "fail":
            validation_results["recommendations"] = self._generate_improvement_recommendations(validation_results)
        
        # Log validation results
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Quality validation completed: {validation_results['overall_score']:.2f} ({validation_results['overall_status']})"
        )
        
        return validation_results
    
    def _evaluate_criterion(self, deliverable: dict, criterion_config: dict):
        """Evaluate single quality criterion"""
        criterion_type = criterion_config.get("type")
        
        if criterion_type == "completeness":
            return self._check_completeness(deliverable, criterion_config)
        elif criterion_type == "accuracy":
            return self._check_accuracy(deliverable, criterion_config)
        elif criterion_type == "format":
            return self._check_format(deliverable, criterion_config)
        elif criterion_type == "content_quality":
            return self._check_content_quality(deliverable, criterion_config)
        else:
            return {"score": 0.5, "feedback": f"Unknown criterion type: {criterion_type}"}
    
    def _check_completeness(self, deliverable: dict, config: dict):
        """Check if deliverable meets completeness requirements"""
        required_sections = config.get("required_sections", [])
        content = deliverable.get("content", "")
        
        found_sections = 0
        missing_sections = []
        
        for section in required_sections:
            if section.lower() in content.lower():
                found_sections += 1
            else:
                missing_sections.append(section)
        
        score = found_sections / len(required_sections) if required_sections else 1.0
        
        return {
            "score": score,
            "feedback": f"Found {found_sections}/{len(required_sections)} required sections",
            "suggestions": [f"Add missing section: {section}" for section in missing_sections]
        }
    
    def create_improvement_workflow(self, workflow_id: str, validation_results: dict):
        """Create improvement workflow based on quality validation"""
        
        if validation_results["overall_status"] == "pass":
            return None
        
        improvement_config = {
            "workflow_id": f"{workflow_id}-improvement",
            "parent_workflow": workflow_id,
            "improvement_type": "quality_enhancement",
            "target_deliverable": validation_results["deliverable_id"],
            "quality_issues": validation_results["recommendations"],
            "success_criteria": {
                "min_score": validation_results["pass_threshold"],
                "focus_areas": [
                    criterion for criterion, result in validation_results["criteria_results"].items()
                    if result["status"] == "fail"
                ]
            }
        }
        
        # Save improvement config for setup script execution
        improvement_file_id = self.files_api.save_improvement_config(improvement_config)
        
        # Log improvement workflow creation
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Quality improvement workflow created: {improvement_config['workflow_id']}"
        )
        
        return improvement_config
    
    def track_quality_metrics(self, workflow_id: str, metrics: dict):
        """Track quality metrics for workflow optimization"""
        
        quality_tracking = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "execution_time": metrics.get("execution_time"),
                "token_usage": metrics.get("token_usage"),
                "cost": metrics.get("cost"),
                "user_satisfaction": metrics.get("user_satisfaction"),
                "deliverable_quality": metrics.get("deliverable_quality"),
                "process_efficiency": metrics.get("process_efficiency")
            },
            "benchmarks": {
                "target_quality_score": 0.85,
                "max_cost_per_workflow": 1.00,
                "max_execution_time_minutes": 45
            }
        }
        
        # Calculate performance against benchmarks
        performance_analysis = self._analyze_performance(quality_tracking)
        quality_tracking["performance_analysis"] = performance_analysis
        
        # Save metrics
        self.memory_mcp.create_entities([{
            "name": f"quality-metrics-{workflow_id}",
            "entityType": "quality-metrics",
            "observations": [
                f"Quality score: {metrics.get('deliverable_quality', 'N/A')}",
                f"Cost: ${metrics.get('cost', 0):.2f}",
                f"Execution time: {metrics.get('execution_time', 0)} minutes",
                f"Performance vs benchmarks: {performance_analysis.get('overall_rating', 'unknown')}"
            ]
        }])
        
        return quality_tracking
```

### **Complete Terminal UI Integration**

**Real-Time Progress Monitoring:**
```python
# interfaces/terminal/progress_monitor.py
class ProgressMonitor:
    """Real-time workflow progress tracking with live updates"""
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.current_workflow = None
        self.progress_state = {}
        
    def start_monitoring(self, workflow_id: str):
        """Begin real-time monitoring of workflow progress"""
        self.current_workflow = workflow_id
        self.progress_state = self._initialize_progress_state(workflow_id)
        
        # Start monitoring loop
        self._display_initial_state()
        self._start_update_loop()
    
    def _initialize_progress_state(self, workflow_id: str):
        """Initialize progress tracking from workflow context"""
        context = self.memory_mcp.get_workflow_context(workflow_id)
        
        if not context:
            return self._get_initial_state()
        
        # Analyze workflow context to determine progress
        observations = context.get("observations", [])
        
        state = {
            "goal": "completed" if any("User goal:" in obs for obs in observations) else "pending",
            "workflow": "completed" if any("Workflow created" in obs for obs in observations) else "pending", 
            "tools": "completed" if any("Tool requested:" in obs for obs in observations) else "pending",
            "agents": "completed" if any("Agent handoff" in obs for obs in observations) else "pending",
            "execution": "in_progress" if any("execution started" in obs for obs in observations) else "pending",
            "quality": "pending",
            "completion": "pending"
        }
        
        return state
    
    def _display_initial_state(self):
        """Display initial progress state"""
        print("\n" + "="*60)
        print(f"🚀 MAO Workflow Monitor - {self.current_workflow}")
        print("="*60)
        self._render_progress_display()
    
    def _render_progress_display(self):
        """Render live progress display without reprinting"""
        progress_items = [
            ("🎯 Goal Analysis", self.progress_state.get("goal", "pending")),
            ("📋 Workflow Planning", self.progress_state.get("workflow", "pending")),
            ("🔧 Tool Preparation", self.progress_state.get("tools", "pending")),
            ("🤖 Agent Coordination", self.progress_state.get("agents", "pending")),
            ("⚡ Execution", self.progress_state.get("execution", "pending")),
            ("🎯 Quality Validation", self.progress_state.get("quality", "pending")),
            ("✅ Completion", self.progress_state.get("completion", "pending"))
        ]
        
        for item_name, status in progress_items:
            status_icon = self._get_status_icon(status)
            print(f"{status_icon} {item_name}")
        
        # Live sub-task tracking
        if self.progress_state.get("current_phase"):
            print(f"\n📍 Current: {self.progress_state['current_phase']}")
            
        if self.progress_state.get("sub_tasks"):
            print("   Sub-tasks:")
            for sub_task, sub_status in self.progress_state["sub_tasks"].items():
                sub_icon = self._get_status_icon(sub_status)
                print(f"   {sub_icon} {sub_task}")
    
    def _get_status_icon(self, status: str):
        """Get appropriate icon for status"""
        icons = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "failed": "❌",
            "waiting": "⏸️"
        }
        return icons.get(status, "❓")
    
    def update_progress(self, component: str, status: str, sub_task: str = None):
        """Update progress for specific component"""
        self.progress_state[component] = status
        
        if sub_task:
            if "sub_tasks" not in self.progress_state:
                self.progress_state["sub_tasks"] = {}
            self.progress_state["sub_tasks"][sub_task] = status
        
        # Update Memory MCP
        self.memory_mcp.update_workflow_state(
            self.current_workflow,
            f"Progress update: {component} -> {status}"
        )
        
        # Re-render display
        self._clear_and_rerender()
    
    def _clear_and_rerender(self):
        """Clear and re-render progress display"""
        # Move cursor up and clear lines
        print("\033[F" * 10, end="")  # Move up
        print("\033[J", end="")       # Clear to end
        self._render_progress_display()
    
    def show_completion_summary(self, workflow_results: dict):
        """Display comprehensive completion summary"""
        print("\n" + "="*60)
        print("🎉 WORKFLOW COMPLETED")
        print("="*60)
        
        # Results summary
        print(f"📊 Results Summary:")
        print(f"   • Duration: {workflow_results.get('duration', 'Unknown')}")
        print(f"   • Cost: ${workflow_results.get('cost', 0):.2f}")
        print(f"   • Quality Score: {workflow_results.get('quality_score', 'N/A')}")
        print(f"   • Deliverables: {len(workflow_results.get('deliverables', []))}")
        
        # Quick actions
        print(f"\n🚀 Quick Actions:")
        print(f"   • View Results: open {workflow_results.get('workspace_path', '')}")
        print(f"   • Re-run: {workflow_results.get('custom_command', 'N/A')}")
        print(f"   • Email Results: [Feature pending]")
        print(f"   • Copy to Clipboard: [Feature pending]")
        
        # Performance insights
        if workflow_results.get('performance_insights'):
            print(f"\n💡 Performance Insights:")
            for insight in workflow_results['performance_insights']:
                print(f"   • {insight}")
```

Perfect! Now the technical documentation has proper code patterns and implementation details from the comprehensive implementation plans. The gaps are clearly marked without implementation plan language, and users can see exactly what the architecture will look like when complete.

<function_calls>
<invoke name="Chain-of-Thought Tool for Sequential-Thinking:sequentialthinking">
<parameter name="nextThoughtNeeded">true## 🔧 **Tool Integration Framework**

### **Executable Human Button System**

MAO transforms human buttons from static code snippets into executable workflow components with complete tracking integration.

**Current Button Generation Pattern:**
```python
# tools/*/button_*.py - Standard pattern across all tools
def create_button_snippet(tool_name: str, params: dict, workflow_id: str = None):
    """Generate executable code with workflow tracking"""
    
    base_snippet = f"""
# Executable {tool_name} with workflow integration
import json
from datetime import datetime

# Tool execution with tracking
def execute_with_tracking():
    workflow_id = "{workflow_id}"
    execution_id = generate_execution_id()
    
    # Log execution start
    if workflow_id:
        update_workflow_state(workflow_id, f"Tool execution started: {execution_id}")
    
    try:
        # Execute tool logic
        result = {tool_name}_main({json.dumps(params)})
        
        # Save results to Files API for agent access
        save_execution_results(workflow_id, execution_id, result)
        
        # Call back to orchestrator
        if workflow_id:
            callback_orchestrator(workflow_id, execution_id, result)
            
        return result
        
    except Exception as e:
        log_execution_error(workflow_id, execution_id, str(e))
        raise

execute_with_tracking()
"""
    return base_snippet
```

**Agent Callback Integration:**
```python
# orchestrator/agent_callback_handler.py
class AgentCallbackHandler:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        
    def handle_agent_return(self, workflow_id: str, execution_data: dict):
        """Process agent return with execution results"""
        
        # Retrieve workflow context
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Process execution results and files
        if execution_data.get('file_ids'):
            processed_files = []
            for file_id in execution_data['file_ids']:
                file_content = self.files_api.retrieve_execution_file(file_id)
                processed_files.append({
                    "id": file_id,
                    "content": file_content
                })
            
            execution_data['processed_files'] = processed_files
        
        # Update workflow state
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent returned with {len(execution_data.get('file_ids', []))} files"
        )
        
        return {
            "workflow_context": workflow_context,
            "execution_results": execution_data,
            "next_phase": self._determine_next_phase(workflow_context, execution_data)
        }
```

### **Dynamic Tool Discovery System**

**Tool Manager Enhancement:**
```python
# orchestrator/manager_tools.py (enhanced)
class ToolManager:
    def __init__(self):
        self.discovered_tools = {}
        self.mcp_connector = None  # Set when MCP integration complete
        self.memory_mcp = MemoryMCPManager()
        
    def discover_all_tools(self):
        """Discover tools from multiple sources"""
        tools = {}
        
        # Local MAO tools
        local_tools = self._discover_local_tools()
        tools.update(local_tools)
        
        # MCP server tools (when available)
        if self.mcp_connector:
            mcp_tools = self.mcp_connector.get_available_tools()
            tools.update(mcp_tools)
        
        # Cache and log discovery
        self.discovered_tools = tools
        self._log_discovery_results(tools)
        
        return tools
    
    def _discover_local_tools(self):
        """Analyze local tool directories for standardized structure"""
        tools = {}
        tools_dir = Path("tools")
        
        for tool_dir in tools_dir.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith('_'):
                tool_info = self._analyze_tool_structure(tool_dir)
                if tool_info:
                    tools[tool_dir.name] = tool_info
        
        return tools
    
    def _analyze_tool_structure(self, tool_dir: Path):
        """Validate tool follows 6-file pattern"""
        tool_name = tool_dir.name
        required_files = [
            f"{tool_name}.py",           # Core logic
            f"tool_{tool_name}.json",    # Configuration
            f"button_{tool_name}.py",    # Button generator
            f"ui_{tool_name}.py"         # UI components
        ]
        
        # Check file structure
        missing_files = []
        for req_file in required_files:
            if not (tool_dir / req_file).exists():
                missing_files.append(req_file)
        
        if missing_files:
            return None
        
        # Load configuration
        try:
            with open(tool_dir / f"tool_{tool_name}.json") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        
        # Verify button function exists
        button_module_path = tool_dir / f"button_{tool_name}.py"
        if not self._validate_button_module(button_module_path):
            return None
        
        return {
            "type": "local",
            "path": str(tool_dir),
            "config": config,
            "validated": True
        }
    
    def _validate_button_module(self, module_path: Path):
        """Ensure button module has required create_button_snippet function"""
        try:
            spec = importlib.util.spec_from_file_location("button_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return hasattr(module, 'create_button_snippet')
        except Exception:
            return False
```

### **Workflow Engine Core Integration**

**Setup Script Bridge:**
```python
# orchestrator/setup_script_bridge.py
class SetupScriptBridge:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        
    def create_workflow_from_conversation(self, user_goal: str, conversation_context: dict):
        """Transform conversation into executable workflow"""
        workflow_id = self._generate_workflow_id()
        
        # Create workflow entity
        self.memory_mcp.create_workflow_context(workflow_id, user_goal)
        
        # Analyze conversation for workflow requirements
        workflow_spec = self._analyze_conversation(user_goal, conversation_context)
        
        # Generate JSON configuration
        config = self._generate_workflow_config(workflow_id, workflow_spec)
        
        # Create custom command (spaces not hyphens!)
        custom_command = self._generate_custom_command(workflow_spec)
        
        # Generate setup script
        setup_script = self._create_setup_script(workflow_id, custom_command, config)
        
        # Create use-case directory structure
        use_case_path = self._create_use_case_directory(custom_command, config)
        
        return {
            "workflow_id": workflow_id,
            "custom_command": custom_command,
            "config": config,
            "setup_script": setup_script,
            "use_case_path": use_case_path
        }
    
    def _generate_custom_command(self, workflow_spec: dict):
        """Generate natural language command with spaces"""
        base_name = workflow_spec.get("name", "workflow")
        # Ensure spaces, not hyphens for natural language
        return base_name.replace("-", " ").replace("_", " ")
    
    def _create_setup_script(self, workflow_id: str, custom_command: str, config: dict):
        """Generate executable setup script"""
        command_filename = custom_command.replace(" ", "-")
        
        script_content = f"""#!/bin/bash
# MAO Workflow Setup Script
# Generated for workflow: {workflow_id}
# Custom command: {custom_command}

set -e

echo "🚀 Setting up MAO workflow: {custom_command}"

# Create executable command
cat > "/usr/local/bin/{command_filename}" << 'EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, "{os.path.abspath('.')}")

from orchestrator.core import MaoOrchestrator

orchestrator = MaoOrchestrator()
orchestrator.execute_workflow("{workflow_id}", sys.argv[1:])
EOF

chmod +x "/usr/local/bin/{command_filename}"

echo "✅ Custom command installed: {custom_command}"
echo "🧪 Test: which {command_filename}"
echo "🚀 Usage: {custom_command} [args...]"
"""
        return script_content
```

### **MCP Connector Integration**

**External MCP Server Connectivity:**
```python
# orchestrator/mcp_connector.py
class MCPConnector:
    """Anthropic MCP API Connector for external tool integration"""
    
    def __init__(self):
        self.servers = {}
        self.memory_manager = MemoryMCPManager()
        self.registered_tools = {}
        
    def register_server(self, server_config: dict):
        """Register external MCP server"""
        server_name = server_config["name"]
        self.servers[server_name] = MCPServerConnection(server_config)
        
        # Discover available tools
        tools = self.servers[server_name].list_tools()
        self.registered_tools[server_name] = tools
        
        # Log server registration
        self.memory_manager.create_entities([{
            "name": f"mcp-server-{server_name}",
            "entityType": "mcp-server",
            "observations": [
                f"Registered: {server_config}",
                f"Available tools: {list(tools.keys())}"
            ]
        }])
        
        return tools
    
    def execute_tool(self, server_name: str, tool_name: str, params: dict, workflow_id: str = None):
        """Execute tool on external MCP server"""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not registered")
            
        if tool_name not in self.registered_tools[server_name]:
            raise ValueError(f"Tool {tool_name} not available on {server_name}")
            
        result = self.servers[server_name].execute_tool(tool_name, params)
        
        # Log tool execution if part of workflow
        if workflow_id:
            self.memory_manager.update_workflow_state(
                workflow_id,
                f"MCP tool executed: {server_name}.{tool_name} -> Success"
            )
            
        return result
    
    def get_available_tools(self):
        """Get all available tools across all servers"""
        all_tools = {}
        for server_name, tools in self.registered_tools.items():
            for tool_name, tool_info in tools.items():
                all_tools[f"{server_name}.{tool_name}"] = tool_info
        return all_tools

class MCPServerConnection:
    """Individual MCP server connection handler"""
    
    def __init__(self, config: dict):
        self.config = config
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        """Initialize MCP client with server configuration"""
        return anthropic.beta.messages.create(
            model="claude-sonnet-4-20250514",
            mcp_servers=[{
                "type": "url",
                "url": self.config["url"],
                "name": self.config["name"],
                "authorization_token": self.config.get("authorization_token")
            }],
            betas=["mcp-client-2025-04-04"]
        )
    
    def list_tools(self):
        """Discover available tools on this server"""
        response = self.client.messages.create(
            messages=[{"role": "user", "content": "What tools do you have available?"}]
        )
        return self._parse_available_tools(response)
    
    def execute_tool(self, tool_name: str, params: dict):
        """Execute specific tool with parameters"""
        response = self.client.messages.create(
            messages=[{
                "role": "user", 
                "content": f"Use {tool_name} with parameters: {json.dumps(params)}"
            }]
        )
        return self._parse_tool_response(response)
```

### **Code Execution Tool Integration**

**Direct Claude 4 Code Execution Integration:**
```python
# tools/code_execution/code_execution.py
class CodeExecutionTool:
    """Integration with Claude 4 Code Execution for workflow tracking"""
    
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.files_api = FilesAPIManager()
        
    def execute_human_button(self, button_code: str, workflow_id: str, context: dict = None):
        """Execute human button code with workflow tracking"""
        execution_id = f"exec-{uuid4().hex[:8]}"
        
        # Log execution start
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Code execution started: {execution_id}"
        )
        
        try:
            # Prepare execution environment
            exec_env = self._prepare_environment(workflow_id, context)
            
            # Execute code with Claude Code Execution
            result = self._execute_code(button_code, exec_env)
            
            # Save files via Code Execution (only way to make them downloadable)
            if result.get('generated_files'):
                file_ids = []
                for file_info in result['generated_files']:
                    file_id = self._upload_via_code_execution(file_info)
                    file_ids.append(file_id)
                result['file_ids'] = file_ids
            
            # Update workflow state
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Code execution completed: {execution_id}"
            )
            
            return {
                "execution_id": execution_id,
                "result": result,
                "workflow_id": workflow_id
            }
            
        except Exception as e:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Code execution failed: {execution_id} - {str(e)}"
            )
            raise
    
    def _prepare_environment(self, workflow_id: str, context: dict):
        """Prepare execution environment with workflow context"""
        return {
            "workflow_id": workflow_id,
            "context": context,
            "memory_mcp_available": True,
            "files_api_available": True
        }
    
    def _upload_via_code_execution(self, file_info: dict):
        """Upload file via Code Execution tool for later download"""
        # Only files uploaded via Code Execution are downloadable
        # This is a critical Anthropic API requirement
        upload_code = f"""
import anthropic
client = anthropic.Anthropic()

with open("{file_info['path']}", "rb") as f:
    file_response = client.files.create(
        file=f,
        purpose="workflow_execution"
    )
    
print(f"File uploaded: {{file_response.id}}")
"""
        # Execute upload via Code Execution
        result = self._execute_code(upload_code, {})
        return self._extract_file_id(result)

def create_executable_button_snippet(tool_name: str, params: dict, workflow_id: str):
    """Generate executable human button with workflow tracking"""
    
    imports = """
import json
import uuid
from datetime import datetime
"""
    
    tool_code = f"""
# Import the specific tool
from tools.{tool_name}.{tool_name} import {tool_name.title()}Tool

# Initialize tool
tool = {tool_name.title()}Tool()
"""
    
    wrapper = f"""
def execute_with_tracking():
    workflow_id = "{workflow_id}"
    execution_id = f"exec-{{uuid.uuid4().hex[:8]}}"
    
    try:
        # Execute tool with parameters
        result = tool.execute({json.dumps(params)})
        
        # Save results to Files API via Code Execution
        # (Critical: Only files saved via Code Execution are downloadable)
        if result.get('files'):
            file_ids = []
            for file_path in result['files']:
                # Upload via Code Execution
                with open(file_path, 'rb') as f:
                    import anthropic
                    client = anthropic.Anthropic()
                    file_response = client.files.create(file=f, purpose="workflow")
                    file_ids.append(file_response.id)
            result['file_ids'] = file_ids
        
        # Call back to orchestrator with workflow ID
        callback_data = {{
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "result": result,
            "status": "completed"
        }}
        
        # This triggers agent callback handling
        print(f"CALLBACK: {{json.dumps(callback_data)}}")
        
        return result
        
    except Exception as e:
        error_data = {{
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "error": str(e),
            "status": "failed"
        }}
        print(f"ERROR: {{json.dumps(error_data)}}")
        raise

# Execute the tool
execute_with_tracking()
"""
    
    return imports + tool_code + wrapper
```

### **Files API Integration**

**Anthropic Files API for Agent Handoffs:**
```python
# orchestrator/files_api_manager.py
class FilesAPIManager:
    """Complete Files API integration for workflow management"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.memory_mcp = MemoryMCPManager()
        
    def create_agent_handoff_package(self, workflow_id: str, agent_data: dict):
        """Create complete agent handoff package"""
        
        # Retrieve workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Bundle complete handoff package
        handoff_package = {
            "workflow_id": workflow_id,
            "workflow_context": workflow_context,
            "agent_instructions": agent_data.get("instructions"),
            "deliverable_requirements": agent_data.get("deliverables"),
            "tool_access": agent_data.get("tools", []),
            "token_limit": agent_data.get("token_limit", 150000),
            "callback_info": {
                "workflow_id": workflow_id,
                "orchestrator_callback": True
            },
            "created_at": datetime.now().isoformat()
        }
        
        # Upload to Files API
        package_content = json.dumps(handoff_package, indent=2)
        file_response = self.client.files.create(
            file=package_content.encode(),
            purpose="agent_handoff"
        )
        
        # Track in Memory MCP
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent handoff package created: {file_response.id}"
        )
        
        return file_response.id
    
    def retrieve_agent_package(self, file_id: str):
        """Retrieve and parse agent handoff package"""
        try:
            file_content = self.client.files.content(file_id)
            package_data = json.loads(file_content.content.decode())
            return package_data
        except Exception as e:
            raise AgentHandoffError(f"Failed to retrieve package {file_id}: {str(e)}")
    
    def save_agent_deliverables(self, workflow_id: str, agent_results: dict):
        """Save agent deliverables for orchestrator review"""
        
        deliverable_package = {
            "workflow_id": workflow_id,
            "agent_id": agent_results.get("agent_id"),
            "deliverables": agent_results.get("deliverables"),
            "execution_summary": agent_results.get("summary"),
            "quality_metrics": agent_results.get("metrics"),
            "next_phase_recommendations": agent_results.get("recommendations"),
            "completed_at": datetime.now().isoformat()
        }
        
        # Save to Files API
        content = json.dumps(deliverable_package, indent=2)
        file_response = self.client.files.create(
            file=content.encode(),
            purpose="agent_deliverables"
        )
        
        # Update workflow state
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent deliverables saved: {file_response.id}"
        )
        
        return file_response.id
    
    def create_workspace_structure(self, workflow_id: str, workspace_config: dict):
        """Create organized workspace for workflow execution"""
        
        workspace_data = {
            "workflow_id": workflow_id,
            "base_path": workspace_config.get("base_path"),
            "directory_structure": {
                "phases": workspace_config.get("phases", []),
                "deliverables": "DELIVERABLES/",
                "metadata": "METADATA/",
                "drafts": "DRAFTS/"
            },
            "file_organization": workspace_config.get("organization", {}),
            "created_at": datetime.now().isoformat()
        }
        
        # Save workspace configuration
        content = json.dumps(workspace_data, indent=2)
        file_response = self.client.files.create(
            file=content.encode(),
            purpose="workspace_config"
        )
        
        return {
            "workspace_file_id": file_response.id,
            "workspace_path": workspace_data["base_path"],
            "structure": workspace_data["directory_structure"]
        }
    
    def download_execution_file(self, file_id: str):
        """Download file from previous execution (only works for Code Execution uploads)"""
        try:
            file_content = self.client.files.content(file_id)
            return file_content.content
        except Exception as e:
            raise FileAccessError(f"Cannot access file {file_id}: {str(e)}")
```Current Limitation:**
- No automated quality validation
- Manual quality assessment required
- No improvement feedback loops

#### **Complete Terminal UI/UX** 🖥️
**Status**: 🚧 **[Implementation Plan 1.5]**

**Missing Components:**
- Real-time progress monitoring with sub-task tracking
- Live workflow status updates without reprinting
- Enhanced completion summaries with quick actions
- Professional application experience integration

**Current State:**
- Basic terminal interface exists
- Limited progress visualization
- No live monitoring capabilities

### **Implementation Dependencies**

```
Phase 1: MCP Integration Hub (Foundation)
   ↓
Phase 2: Tool Integration Framework (Building Blocks)  
   ↓
Phase 3: Workflow Engine Core (Orchestration)
   ↓
Phase 4: Terminal UI/UX System (User Experience)
   ↓
Phase 5: Integration Testing (Quality Assurance)
```

### **Critical Fixes Required Before Implementation**

#### **🚨 Entry Point Crisis (`mao_v4.py`)**
**Issue**: Only handles 2 of 20+ defined arguments
**Impact**: Blocks all CLI functionality  
**Status**: 🔴 **BLOCKING**

#### **🚨 Missing Interface Methods (`ui_terminal.py`)**
**Issue**: Parser routes to non-existent methods
**Impact**: Runtime errors for most commands
**Status**: 🔴 **BLOCKING**

#### **🚨 JSON Configuration Standardization**
**Issue**: Inconsistent property naming and structure
**Impact**: Parser generation failures
**Status**: 🟡 **MEDIUM PRIORITY**

### **Success Criteria for Complete Implementation**

**User Experience:**
- [ ] New user can create working workflow in <10 minutes
- [ ] Natural language goal → executable custom command
- [ ] Session interruption/recovery works seamlessly

**Performance:**
- [ ] <$0.01 per workflow execution cost
- [ ] <5 second cache hit response times
- [ ] 99%+ success rate for standard workflow patterns

**Technical Integration:**
- [ ] All human buttons generate executable code
- [ ] Memory MCP provides persistent workflow state
- [ ] Files API enables seamless agent handoffs
- [ ] Quality framework validates all deliverables

### **Estimated Implementation Timeline**

**Phase 1 (MCP Integration)**: 2-3 weeks
- Memory MCP integration and testing
- Files API workflow handoff implementation
- MCP Connector for external tool integration

**Phase 2 (Tool Framework)**: 1-2 weeks  
- Executable human button enhancement
- Dynamic tool discovery connection
- Agent callback system implementation

**Phase 3 (Workflow Engine)**: 2-3 weeks
- Setup script generation system
- Quality framework integration
- Custom command creation and installation

**Phase 4 (Terminal UI/UX)**: 1-2 weeks
- Real-time progress monitoring
- Professional application experience
- Live workflow status integration

**Phase 5 (Testing & Polish)**: 1 week
- End-to-end integration testing
- Performance validation
- User experience refinement

**Total Estimated Timeline**: 7-11 weeks for complete implementation