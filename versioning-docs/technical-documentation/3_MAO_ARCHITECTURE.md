# MAO Architecture
**Complete System Architecture & Integration Guide**

*Deep technical understanding of how MAO components work together*

---

## 🎯 **Architectural Philosophy: Full Interactive Application Platform**

### **MAO v4 vs Legacy SFA Approach**

MAO represents a **fundamental paradigm shift** from traditional AI workflow tools:

**Legacy SFA Approach (What We Moved Beyond):**
- Passive monitoring and ticker-style interfaces
- Minimal user interaction during execution  
- Single-purpose, terminal-only utilities
- Status updates without rich interaction capabilities

**MAO v4 Revolutionary Approach:**
- **Complete interactive application experience** with rich UI/UX
- **Multi-platform architecture** designed for seamless UI portability
- **Professional application quality** rivaling tools like Claude Code
- **Comprehensive workflow management** with live monitoring, settings, chat interfaces
- **User-centric design** that adapts to experience levels and preferences

### **UI Portability by Design**

MAO's architecture is specifically designed for **cross-platform compatibility**:

- **Terminal-first implementation** with full application features
- **Clean separation** between logic and presentation layers
- **Modular interface system** enabling web, mobile, desktop expansion
- **Professional polish** that translates across platforms

### **Interactive Application Features**

Unlike monitoring utilities, MAO provides:

- **Rich chat interfaces** for natural workflow creation
- **Live workflow monitoring** with real-time progress tracking
- **Settings management** with user preferences and customization
- **Dynamic command system** with both CLI and in-app variants
- **Visual progress indicators** and status management
- **Audio notifications** and non-intrusive awareness systems
- **Error recovery interfaces** with guided resolution options

This architectural philosophy influences every component design decision and ensures MAO delivers a **complete application experience** rather than a simple workflow execution tool.

---

## 🏗️ **System Overview**

MAO's architecture is built on **principled modularity** - every component is independent, replaceable, and universally compatible. This enables infinite extensibility without performance degradation.

### **Core Architectural Principles**

**1. Universal Compatibility** 🌐
- Any AI model works with any tool via human buttons
- Provider-agnostic design eliminates vendor lock-in
- Future AI advances integrate automatically

**2. Clean Separation of Concerns** 🧩
- Logic, UI, execution, and configuration are completely separate
- Each component testable and replaceable in isolation
- Multiple interfaces possible without code changes

**3. Variable-Input Philosophy** 🎨
- No hardcoded specifics anywhere in the system
- Tools are blank canvases - prompts define behavior
- Maximum flexibility for unlimited use cases

**4. Performance Optimization** ⚡
- Intelligent caching with fingerprinting
- Dynamic resource allocation
- Cost optimization through smart model selection

---

## 🎭 **Entry Point: `mao_v4.py`**

**Main CLI interface** providing multiple interaction modes and routing.

### **Command Line Interface**

```python
# Core functionality
def main():
    parser = argparse.ArgumentParser(description="MAO - AI Workflow Orchestrator")
    
    # Primary execution modes
    parser.add_argument("goal", nargs="?", help="Natural language goal")
    
    # System management
    parser.add_argument("--list-workflows", action="store_true")
    parser.add_argument("--stats", action="store_true") 
    parser.add_argument("--verbose", "-v", action="store_true")
    
    # Execution preferences
    parser.add_argument("--workspace", "-w", help="Custom workspace directory")
    parser.add_argument("--free-only", action="store_true", help="Use only free models")
    parser.add_argument("--privacy", action="store_true", help="Privacy-focused models")
```

### **Execution Flow**

**1. Argument Parsing & Validation**
- Command line argument processing
- Execution mode determination (direct, interactive)
- Preference extraction and validation

**2. Interface Initialization**
```python
mao = TerminalInterface(verbose=args.verbose)
```

**3. Request Routing**
- Stats requests → `mao.get_stats()`
- Workflow listing → `mao.list_workflows()`
- General goals → `mao.execute_goal()`
- Interactive mode → Input loop with continuous execution

**4. Result Processing**
- Success summary generation
- Error handling and user guidance
- Workspace management and file organization

### **MAO CLI Command Reference**

| **FUNCTION**                | **TERMINAL COMMAND**          | **IN-APP COMMAND**            |
| --------------------------- | ----------------------------- | ----------------------------- |
| **Start Application**       | `mao mao`                     | -                             |
| Restart application         | -                             | `/restart` or `! mao restart` |
| Exit application            | -                             | `/exit` or `! mao exit`       |
| Open config management UI   | `mao --config`                | `/config`                     |
| Resume most recent workflow | `mao --continue`              | `/continue`                   |
| **First message to AI**     | `mao --chat message`          | `/chat message`               |
| **Create entire workflow**  | `mao --goal project goal`     | `/goal project goal`          |
| **System Statistics**       | `mao --stats`                 | `/stats`                      |
| **List Workflows**          | `mao --workflows`             | `/workflows`                  |
| **Review Workflow**         | `mao --review custom command` | `/review custom command`      |
| **Setup from JSON**         | `mao --setup ./config.json`   | `/setup ./config.json`        |
| **Update Workflow**         | `mao --update ./phase.json`   | `/update ./phase.json`        |
| **Fix Deliverable**         | `mao --fix-it ./fix.json`     | `/fix-it ./fix.json`          |
| **Custom Output Directory** | `mao --output ~/downloads`    | `/output ~/downloads`         |
| **Use only free models**    | `mao --free`                  | `/free`                       |
| **Privacy models only**     | `mao --privacy`               | `/privacy`                    |
| **Verbose Debug Mode**      | `mao --verbose`               | `/verbose`                    |
| **View workflow logs**      | `mao --logs`                  | `/logs`                       |
| **Show workflow stats**     | `mao --stats`                 | `/stats`                      |
| **Check Health**            | `mao --doctor`                | `/doctor`                     |
| **View help messages**      | `mao --help`                  | `/help`                       |
| **Simulate Workflow**       | `mao --dry-run`               | `/dry-run`                    |
| **Terminal Commands**       | -                             | `!ls -la` (any bash/zsh)      |

---

## 🧠 **Memory MCP Integration Hub**

### **Architectural Evolution: Beyond `orchestrator/memory.py`**

MAO v4 shifts from local file-based memory to **Memory MCP integration** for persistent, entity-based project tracking.

**Legacy Approach (`orchestrator/memory.py`):**
- Local file-based state storage
- Session-scoped memory management  
- Limited cross-session persistence

**MAO v4 Memory MCP Approach:**
- Entity-based project tracking with persistent knowledge graphs
- Cross-session workflow continuity with complete context preservation
- Multi-agent state coordination via shared memory entities
- Distributed state management supporting interrupted session recovery

### **Core Integration Architecture**

```python
# orchestrator/memory_mcp_manager.py
class MemoryMCPManager:
    """Primary interface for workflow state management"""
    
    def __init__(self):
        self.memory_connector = MemoryMCPConnector()
        self.entity_cache = {}
        
    def create_workflow_context(self, workflow_id: str, user_goal: str):
        """Initialize persistent workflow entity"""
        entity = {
            "name": f"workflow-{workflow_id}",
            "entityType": "workflow",
            "observations": [
                f"User goal: {user_goal}",
                f"Created: {datetime.now().isoformat()}",
                f"Status: initialized"
            ]
        }
        return self.memory_connector.create_entities([entity])
    
    def update_workflow_state(self, workflow_id: str, state_update: str):
        """Add state observation to workflow entity"""
        entity_name = f"workflow-{workflow_id}"
        observation = {
            "entityName": entity_name,
            "contents": [f"{datetime.now().isoformat()}: {state_update}"]
        }
        return self.memory_connector.add_observations([observation])
    
    def get_workflow_context(self, workflow_id: str):
        """Retrieve complete workflow context for session recovery"""
        entity_name = f"workflow-{workflow_id}"
        return self.memory_connector.open_nodes([entity_name])
    
    def search_workflows(self, query: str):
        """Search across all workflow entities"""
        return self.memory_connector.search_nodes(f"{query} entityType:workflow")
```

### **Files API Integration Layer**

```python
# orchestrator/files_api_manager.py  
class FilesAPIManager:
    """Handles agent handoff packages and workflow file management"""
    
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic()
        self.memory_mcp = MemoryMCPManager()
        
    def create_agent_handoff_package(self, workflow_id: str, phase_data: dict):
        """Bundle context and files for agent handoff"""
        package = {
            "workflow_id": workflow_id,
            "phase_data": phase_data,
            "context": self.memory_mcp.get_workflow_context(workflow_id),
            "timestamp": datetime.now().isoformat()
        }
        
        # Upload to Files API for agent access
        file_response = self.anthropic_client.files.create(
            file=json.dumps(package, indent=2).encode(),
            purpose="workflow_handoff"
        )
        
        # Track file reference in Memory MCP
        self.memory_mcp.update_workflow_state(
            workflow_id, 
            f"Agent handoff package created: {file_response.id}"
        )
        
        return file_response.id
    
    def retrieve_handoff_package(self, file_id: str):
        """Retrieve and parse agent handoff package"""
        file_content = self.anthropic_client.files.content(file_id)
        return json.loads(file_content.content.decode())
    
    def save_workflow_deliverables(self, workflow_id: str, deliverables: dict):
        """Save final deliverables with workflow context"""
        package = {
            "workflow_id": workflow_id,
            "deliverables": deliverables,
            "completion_time": datetime.now().isoformat(),
            "workflow_log": self.memory_mcp.get_workflow_context(workflow_id)
        }
        
        file_response = self.anthropic_client.files.create(
            file=json.dumps(package, indent=2).encode(),
            purpose="workflow_completion"
        )
        
        return file_response.id
```

### **Session Recovery Implementation**

```python
def recover_session(self, last_workflow_id: str = None):
    """Recover interrupted session with complete context"""
    if not last_workflow_id:
        # Find most recent active workflow
        recent_workflows = self.memory_mcp.search_workflows("status:active")
        if not recent_workflows:
            return None
        last_workflow_id = self._extract_workflow_id(recent_workflows[0])
    
    # Retrieve complete workflow context
    workflow_context = self.memory_mcp.get_workflow_context(last_workflow_id)
    if not workflow_context:
        raise WorkflowNotFoundError(f"Workflow {last_workflow_id} not found")
    
    # Extract file references and workspace info
    observations = workflow_context.get("observations", [])
    file_refs = self._extract_file_references(observations)
    workspace_path = self._extract_workspace_path(observations)
    
    # Determine current phase and next actions
    current_phase = self._analyze_workflow_progress(observations)
    
    return {
        "workflow_id": last_workflow_id,
        "context": workflow_context,
        "file_references": file_refs,
        "workspace_path": workspace_path,
        "current_phase": current_phase,
        "recovery_actions": self._plan_recovery_actions(current_phase)
    }
```

### **Entity Relationship Patterns**

**Project Hierarchy:**
```
MAO-v4 (project)
├── workflow-abc123 (workflow)
│   ├── observations: [phase_completions, agent_handoffs, quality_metrics]
│   ├── relations: [uses → brave_search, hands-off-to → analysis_agent]
│   └── files: [workspace_path, deliverable_refs, handoff_packages]
├── workflow-def456 (workflow)
└── system-state (tracking)
```

**Cross-Workflow Relations:**
```python
# Example: Workflow template reuse
{
  "from": "workflow-abc123",
  "to": "workflow-template-content-strategy", 
  "relationType": "derived-from"
}

# Example: Tool usage patterns
{
  "from": "workflow-abc123",
  "to": "brave_search",
  "relationType": "uses-tool"
}
```

### **Performance Characteristics**

**State Persistence:**
- Memory MCP updates: <100ms per observation
- Context retrieval: <500ms for complete workflow history
- Session recovery: <2 seconds for full workflow reconstruction

**Scalability:**
- Supports unlimited concurrent workflows
- Entity relationships scale logarithmically  
- Cross-session state sharing between workflow instances

**Integration Benefits:**
- Zero-latency workflow context access
- Automatic state synchronization across agent handoffs
- Complete audit trail for workflow debugging and optimization

---

## 🔧 **Tool Integration Framework**

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