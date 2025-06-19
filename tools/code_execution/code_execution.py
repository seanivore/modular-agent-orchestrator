#!/usr/bin/env python3
"""
Code Execution Tool - Workflow-Integrated Execution System
Transforms human buttons from static snippets into executable code with tracking
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class CodeExecutionTool:
    """Enhanced code execution with workflow tracking and MCP integration"""
    
    def __init__(self):
        # Lazy load to avoid circular imports
        self._memory_mcp = None
        self._files_api = None
        
    @property
    def memory_mcp(self):
        """Lazy load Memory MCP manager"""
        if self._memory_mcp is None:
            from orchestrator.memory_mcp import MemoryMCPManager
            self._memory_mcp = MemoryMCPManager()
        return self._memory_mcp
    
    @property
    def files_api(self):
        """Lazy load Files API manager"""
        if self._files_api is None:
            from orchestrator.files_api import FilesAPIManager
            self._files_api = FilesAPIManager()
        return self._files_api
    
    def execute_human_button(self, button_code: str, workflow_id: str, context: Dict = None) -> Dict[str, Any]:
        """Execute human button code with comprehensive workflow tracking"""
        
        execution_id = f"exec-{uuid.uuid4().hex[:8]}"
        context = context or {}
        
        # Log execution start in Memory MCP
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Code execution started: {execution_id} - {context.get('tool_name', 'unknown_tool')}"
        )
        
        try:
            # Prepare execution environment with workflow context
            exec_env = self._prepare_environment(workflow_id, context, execution_id)
            
            # Execute code with Claude Code Execution tool
            # In real implementation, this would use the actual Claude Code execution
            result = self._execute_code(button_code, exec_env)
            
            # Save any generated files via Files API
            file_ids = []
            if result.get('files'):
                for filename, content in result['files'].items():
                    file_id = self.files_api.save_draft(
                        workflow_id, 
                        content, 
                        f"execution-{execution_id}",
                        filename
                    )
                    file_ids.append(file_id)
            
            # Update workflow state with success
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Code execution completed: {execution_id} - {len(file_ids)} files generated"
            )
            
            return {
                "success": True,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "files_created": file_ids,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Log execution failure
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Code execution failed: {execution_id} - {str(e)}"
            )
            
            return {
                "success": False,
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _prepare_environment(self, workflow_id: str, context: Dict, execution_id: str) -> Dict[str, Any]:
        """Prepare execution environment with workflow context"""
        
        # Get workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Prepare environment variables
        env = {
            "WORKFLOW_ID": workflow_id,
            "EXECUTION_ID": execution_id,
            "WORKFLOW_CONTEXT": workflow_context,
            "EXECUTION_CONTEXT": context,
            "FILES_API_AVAILABLE": True,
            "MEMORY_MCP_AVAILABLE": True
        }
        
        return env
    
    def _execute_code(self, code: str, env: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code with environment (mock implementation)"""
        
        # In real implementation, this would:
        # 1. Use Claude Code Execution tool
        # 2. Inject environment variables
        # 3. Capture output and files
        # 4. Return structured results
        
        # Mock execution for development
        mock_result = {
            "output": f"Mock execution of code with workflow {env['WORKFLOW_ID']}",
            "files": {
                "result.txt": f"Execution result for {env['EXECUTION_ID']}",
                "log.json": json.dumps({
                    "execution_id": env['EXECUTION_ID'],
                    "workflow_id": env['WORKFLOW_ID'],
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                }, indent=2)
            },
            "execution_time": 1.2,
            "success": True
        }
        
        return mock_result
    
    def create_executable_button_snippet(self, tool_name: str, workflow_id: str, 
                                       agent_context: Dict = None, tool_config: Dict = None) -> str:
        """Generate executable button snippet for specific tool"""
        
        agent_context = agent_context or {}
        tool_config = tool_config or {}
        
        # Track button creation
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Executable button created: {tool_name}"
        )
        
        # Generate self-contained executable snippet
        executable_snippet = f'''
"""
Executable MAO Tool: {tool_name}
Workflow ID: {workflow_id}
Auto-generated executable snippet with workflow tracking
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

# === WORKFLOW CONTEXT ===
WORKFLOW_ID = "{workflow_id}"
TOOL_NAME = "{tool_name}"
EXECUTION_ID = str(uuid.uuid4())[:8]

AGENT_CONTEXT = {json.dumps(agent_context, indent=2)}
TOOL_CONFIG = {json.dumps(tool_config, indent=2)}

print(f"🛠️  Starting {{TOOL_NAME}} execution: {{EXECUTION_ID}}")
print(f"🔗 Workflow: {{WORKFLOW_ID}}")

try:
    # === TOOL IMPLEMENTATION ===
    {self._get_tool_implementation(tool_name, tool_config)}
    
    # === EXECUTION WRAPPER ===
    def execute_with_tracking():
        """Execute tool with comprehensive tracking"""
        
        print(f"▶️  Executing {{TOOL_NAME}}...")
        
        # Run tool-specific logic
        result = main_tool_function(AGENT_CONTEXT, TOOL_CONFIG)
        
        # Save results (files automatically uploaded via Code Execution)
        created_files = []
        if result.get('files'):
            for file_name, content in result['files'].items():
                output_file = f"workflow-{{WORKFLOW_ID}}-{{EXECUTION_ID}}-{{file_name}}"
                
                # Write file (Code Execution tool handles upload)
                with open(output_file, 'w') as f:
                    f.write(content)
                created_files.append(output_file)
                
                print(f"💾 Created: {{output_file}}")
        
        # Display results
        print(f"✅ {{TOOL_NAME}} execution complete!")
        print(f"📁 Files created: {{len(created_files)}}")
        print(f"📊 Result summary: {{result.get('summary', 'No summary available')}}")
        
        # Return structured data for agent callback
        return {{
            "workflow_id": WORKFLOW_ID,
            "execution_id": EXECUTION_ID,
            "tool_name": TOOL_NAME,
            "success": True,
            "files": created_files,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }}
    
    # Execute the tool
    final_result = execute_with_tracking()
    
    print("\\n" + "="*50)
    print(f"🎯 AGENT CALLBACK INSTRUCTIONS:")
    print(f"1. Execution complete for workflow: {{WORKFLOW_ID}}")
    print(f"2. Files saved and accessible via Code Execution")
    print(f"3. Return with execution results to continue workflow")
    print("="*50)
    
except Exception as e:
    print(f"❌ {{TOOL_NAME}} execution failed: {{str(e)}}")
    print(f"🔗 Workflow: {{WORKFLOW_ID}} - Execution: {{EXECUTION_ID}}")
    raise
'''
        
        return executable_snippet
    
    def _get_tool_implementation(self, tool_name: str, tool_config: Dict) -> str:
        """Get tool-specific implementation code"""
        
        # This would be dynamically loaded from each tool's button file
        # For now, providing a generic implementation template
        
        generic_implementation = '''
    def main_tool_function(context, config):
        """Tool-specific implementation - dynamically loaded"""
        
        # Generic tool execution template
        result = {
            "summary": f"Executed {TOOL_NAME} with context",
            "files": {
                "output.md": f"# {TOOL_NAME} Results\\n\\nExecution completed successfully.",
                "metadata.json": json.dumps({
                    "tool": TOOL_NAME,
                    "execution_id": EXECUTION_ID,
                    "workflow_id": WORKFLOW_ID,
                    "context": context,
                    "config": config
                }, indent=2)
            },
            "metrics": {
                "execution_time": 1.0,
                "success": True
            }
        }
        
        return result
'''
        
        # TODO: Load actual tool implementation
        # tool_module = importlib.import_module(f"tools.{tool_name}.button_{tool_name}")
        # return tool_module.get_implementation_code()
        
        return generic_implementation
    
    def handle_agent_return(self, workflow_id: str, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process agent return with execution results"""
        
        execution_id = execution_results.get('execution_id', 'unknown')
        
        # Retrieve workflow context from Memory MCP
        workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        # Process any files created during execution
        processed_files = []
        if execution_results.get('files'):
            for file_path in execution_results['files']:
                # Files are accessible because they were uploaded via Code Execution
                try:
                    # In real implementation, would read from Files API
                    file_content = f"Mock content for {file_path}"
                    processed_files.append({
                        "path": file_path,
                        "content": file_content,
                        "accessible": True
                    })
                except Exception as e:
                    processed_files.append({
                        "path": file_path,
                        "error": str(e),
                        "accessible": False
                    })
        
        # Update workflow state with agent return
        self.memory_mcp.update_workflow_state(
            workflow_id,
            f"Agent returned with execution results: {execution_id} - {len(processed_files)} files"
        )
        
        return {
            "workflow_context": workflow_context,
            "execution_results": execution_results,
            "processed_files": processed_files,
            "next_phase_ready": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_execution_status(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get all executions for a workflow"""
        
        # In real implementation, would query Memory MCP for execution history
        # For now, return mock data
        return [
            {
                "execution_id": "exec-abc123",
                "tool_name": "web_search",
                "status": "completed",
                "files_created": 2,
                "timestamp": "2025-06-20T14:30:00"
            },
            {
                "execution_id": "exec-def456", 
                "tool_name": "text_editor",
                "status": "in_progress",
                "files_created": 0,
                "timestamp": "2025-06-20T14:35:00"
            }
        ]


# === CONVENIENCE FUNCTIONS ===

def create_code_execution_tool() -> CodeExecutionTool:
    """Factory function for Code Execution Tool"""
    return CodeExecutionTool()

def execute_tool_button(tool_name: str, workflow_id: str, context: Dict = None) -> str:
    """Quick function to generate executable button"""
    tool = create_code_execution_tool()
    return tool.create_executable_button_snippet(tool_name, workflow_id, context)
