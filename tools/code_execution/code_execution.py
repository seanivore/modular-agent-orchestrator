#!/usr/bin/env python3
"""
Code Execution Tool - Claude API Integration
Execute Python code using Claude's secure sandboxed environment
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import anthropic

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

class CodeExecutionTool:
    """Claude Code Execution API integration with workflow tracking"""
    
    def __init__(self):
        self.anthropic_client = None
        self._memory_mcp = None
        self._files_api = None
        
    def _get_anthropic_client(self):
        """Get Anthropic client with code execution beta header"""
        if self.anthropic_client is None:
            self.anthropic_client = anthropic.Anthropic(
                default_headers={
                    "anthropic-beta": "code-execution-2025-05-22"
                }
            )
        return self.anthropic_client
        
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
            from tools.files_api.files_api import FilesAPIManager
            self._files_api = FilesAPIManager()
        return self._files_api
    
    @handle_errors(operation_name="code_execution", return_dict=True)
    @retry_with_backoff(max_retries=2, base_delay=1.0, exceptions=(APIError,))
    def execute_code(self, code: str, workflow_id: str = None, container_id: str = None, 
                    model: str = "claude-sonnet-4") -> Dict[str, Any]:
        """Execute Python code using Claude's Code Execution API"""
        
        execution_id = f"exec-{uuid.uuid4().hex[:8]}"
        
        # Check cache first
        cache_key = f"code_execution|{hash(code)}|{container_id or 'new'}"
        cached_result = cache.get_cached_analysis(cache_key, "code_execution")
        if cached_result:
            return json.loads(cached_result)
        
        try:
            client = self._get_anthropic_client()
            
            # Prepare request parameters
            request_params = {
                "model": f"claude-{model.replace('claude-', '')}" if not model.startswith('claude-') else model,
                "max_tokens": 4096,
                "messages": [{
                    "role": "user", 
                    "content": f"Execute this Python code:\n\n```python\n{code}\n```"
                }],
                "tools": [{
                    "type": "code_execution_20250522",
                    "name": "code_execution"
                }]
            }
            
            # Reuse container if provided
            if container_id:
                request_params["container"] = container_id
            
            # Log execution start
            if workflow_id and self.memory_mcp:
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Code execution started: {execution_id}"
                )
            
            # Execute via Claude API
            response = client.messages.create(**request_params)
            
            # Parse execution results
            result = self._parse_execution_response(response, execution_id)
            
            # Log execution completion
            if workflow_id and self.memory_mcp:
                status = "success" if result["success"] else "failed"
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Code execution {status}: {execution_id}"
                )
            
            # Cache successful results
            if result["success"]:
                cache.cache_content_analysis(cache_key, json.dumps(result), "code_execution")
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "execution_id": execution_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            if workflow_id and self.memory_mcp:
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Code execution error: {execution_id} - {str(e)}"
                )
            
            return error_result
    
    def _parse_execution_response(self, response, execution_id: str) -> Dict[str, Any]:
        """Parse Claude API response for code execution results"""
        
        result = {
            "success": False,
            "execution_id": execution_id,
            "container_id": getattr(response, 'container', {}).get('id'),
            "stdout": "",
            "stderr": "",
            "return_code": None,
            "files": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Extract execution results from response content
        for content_block in response.content:
            if content_block.type == "code_execution_tool_result":
                tool_result = content_block.content
                
                if hasattr(tool_result, 'type') and tool_result.type == "code_execution_result":
                    result["stdout"] = getattr(tool_result, 'stdout', '')
                    result["stderr"] = getattr(tool_result, 'stderr', '')
                    result["return_code"] = getattr(tool_result, 'return_code', 0)
                    result["success"] = result["return_code"] == 0
                    
                    # Extract any generated files
                    if hasattr(tool_result, 'content'):
                        for file_item in tool_result.content:
                            if hasattr(file_item, 'file_id'):
                                result["files"].append({
                                    "file_id": file_item.file_id,
                                    "filename": getattr(file_item, 'filename', 'output'),
                                    "type": getattr(file_item, 'type', 'unknown')
                                })
                
                elif hasattr(tool_result, 'type') and tool_result.type == "code_execution_tool_result_error":
                    result["error"] = getattr(tool_result, 'error_code', 'unknown_error')
                    result["success"] = False
        
        return result
    
    @handle_errors(operation_name="code_execution_with_files", return_dict=True)
    def execute_code_with_files(self, code: str, file_ids: List[str], workflow_id: str = None,
                               model: str = "claude-sonnet-4") -> Dict[str, Any]:
        """Execute code with Files API uploads"""
        
        try:
            client = anthropic.Anthropic(
                default_headers={
                    "anthropic-beta": "code-execution-2025-05-22,files-api-2025-04-14"
                }
            )
            
            # Prepare message content with file references
            content = [{"type": "text", "text": f"Execute this Python code:\n\n```python\n{code}\n```"}]
            
            # Add file uploads to content
            for file_id in file_ids:
                content.append({
                    "type": "container_upload",
                    "file_id": file_id
                })
            
            response = client.messages.create(
                model=f"claude-{model.replace('claude-', '')}" if not model.startswith('claude-') else model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": content
                }],
                tools=[{
                    "type": "code_execution_20250522",
                    "name": "code_execution"
                }]
            )
            
            execution_id = f"exec-{uuid.uuid4().hex[:8]}"
            result = self._parse_execution_response(response, execution_id)
            
            # Log file-based execution
            if workflow_id and self.memory_mcp:
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Code execution with {len(file_ids)} files: {execution_id}"
                )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    @handle_errors(operation_name="download_execution_files", return_list=True)
    def download_execution_files(self, file_ids: List[str], workflow_id: str = None) -> List[Dict[str, Any]]:
        """Download files created during code execution"""
        
        client = anthropic.Anthropic(
            default_headers={
                "anthropic-beta": "files-api-2025-04-14"
            }
        )
        
        downloaded_files = []
        
        for file_id in file_ids:
            try:
                # Get file metadata
                file_metadata = client.beta.files.retrieve_metadata(file_id)
                
                # Download file content
                file_content = client.beta.files.download(file_id)
                
                downloaded_files.append({
                    "file_id": file_id,
                    "filename": file_metadata.filename,
                    "size": file_metadata.size_bytes,
                    "content": file_content.content,
                    "success": True
                })
                
                # Save to Files API if workflow provided
                if workflow_id and self.files_api:
                    self.files_api.save_draft(
                        workflow_id,
                        file_content.content.decode('utf-8') if isinstance(file_content.content, bytes) else file_content.content,
                        f"execution-output",
                        file_metadata.filename
                    )
                
            except Exception as e:
                downloaded_files.append({
                    "file_id": file_id,
                    "error": str(e),
                    "success": False
                })
        
        return downloaded_files
    
    def create_persistent_container(self, workflow_id: str = None) -> Dict[str, Any]:
        """Create a persistent container for multi-step execution"""
        
        try:
            client = self._get_anthropic_client()
            
            # Create container with initial code
            response = client.messages.create(
                model="claude-sonnet-4",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": "Initialize workspace for code execution. Print 'Container ready.'"
                }],
                tools=[{
                    "type": "code_execution_20250522",
                    "name": "code_execution"
                }]
            )
            
            container_id = getattr(response, 'container', {}).get('id')
            expires_at = getattr(response, 'container', {}).get('expires_at')
            
            if workflow_id and self.memory_mcp:
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Created persistent container: {container_id}"
                )
            
            return {
                "success": True,
                "container_id": container_id,
                "expires_at": expires_at,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# REQUIRED: Standard cost estimation function
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    
    # Code execution pricing: $0.05 per session-hour (minimum 5 minutes)
    execution_time_minutes = params.get("execution_time_minutes", 5)  # Minimum 5 minutes
    session_hours = max(execution_time_minutes / 60, 5/60)  # At least 5 minutes
    
    execution_cost = session_hours * 0.05
    
    # Additional costs for file processing
    file_count = len(params.get("file_ids", []))
    file_processing_cost = file_count * 0.001  # Small cost per file
    
    return execution_cost + file_processing_cost

# REQUIRED: Standalone function wrappers for button file imports
@handle_errors(operation_name="execute_python_code", return_dict=True)
def execute_python_code(code: str, workflow_id: str = None, container_id: str = None, model: str = "claude-sonnet-4") -> Dict[str, Any]:
    """Execute Python code using Claude's Code Execution API"""
    tool = CodeExecutionTool()
    result = tool.execute_code(code, workflow_id, container_id, model)
    result["operation"] = "execute_code"
    return result

@handle_errors(operation_name="execute_code_with_files", return_dict=True)
def execute_code_with_files(code: str, file_ids: List[str], workflow_id: str = None, model: str = "claude-sonnet-4") -> Dict[str, Any]:
    """Execute code with Files API uploads"""
    tool = CodeExecutionTool()
    result = tool.execute_code_with_files(code, file_ids, workflow_id, model)
    result["operation"] = "execute_with_files"
    return result

@handle_errors(operation_name="create_persistent_container", return_dict=True)
def create_persistent_container(workflow_id: str = None) -> Dict[str, Any]:
    """Create a persistent container for multi-step execution"""
    tool = CodeExecutionTool()
    result = tool.create_persistent_container(workflow_id)
    result["operation"] = "create_container"
    return result

@handle_errors(operation_name="download_execution_files", return_list=True)
def download_execution_files(file_ids: List[str], workflow_id: str = None) -> List[Dict[str, Any]]:
    """Download files created during code execution"""
    tool = CodeExecutionTool()
    results = tool.download_execution_files(file_ids, workflow_id)
    return results


# Factory function
def create_code_execution_tool() -> CodeExecutionTool:
    """Create Code Execution Tool instance"""
    return CodeExecutionTool()
