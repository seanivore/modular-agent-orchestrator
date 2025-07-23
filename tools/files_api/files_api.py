#!/usr/bin/env python3
"""
Files API Manager - Agent Handoff File Management
Provides workspace organization, draft storage, and agent communication via Files API
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import uuid4
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Set up logger
logger = logging.getLogger(__name__)

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="files_api", return_dict=True)
def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Estimate operation cost for budget planning
    Standard cost estimation interface for MAO tools
    
    Args:
        params: Operation parameters
        
    Returns:
        Estimated cost in USD (Files API operations are typically free)
    """
    # Files API operations are typically low" / "no cost
    operation = params.get("operation", "unknown")
    
    # Cost structure for different operations
    operation_costs = {
        "create_workspace": 0.0,
        "save_draft": 0.0,
        "prepare_handoff": 0.0,
        "save_deliverables": 0.0,
        "get_workflow_files": 0.0
    }
    
    return operation_costs.get(operation, 0.0)

@handle_errors(operation_name="create_workspace", return_dict=True)
def create_workflow_workspace(workflow_id: str) -> Dict[str, Any]:
    """
    Create file structure for workflow
    
    Args:
        workflow_id: Unique workflow identifier
        
    Returns:
        Dict with workspace creation results
    """
    if not workflow_id:
        return {"error": "Workflow ID is required"}
    
    # Check cache first
    cache_key = f"workspace_{workflow_id}"
    cached_result = cache.get_cached_analysis(cache_key, "files_api_workspace")
    if cached_result:
        return json.loads(cached_result)
    
    try:
        manager = FilesAPIManager()
        workspace_structure = manager.create_workflow_workspace(workflow_id)
        
        result = {
            "status": "success",
            "workspace_structure": workspace_structure,
            "workflow_id": workflow_id,
            "operation": "create_workspace",
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result
        cache.cache_content_analysis(cache_key, json.dumps(result), "files_api_workspace")
        
        return result
        
    except Exception as e:
        return {"error": f"Workspace creation failed: {str(e)}"}

@handle_errors(operation_name="save_draft", return_dict=True)
def save_workflow_draft(workflow_id: str, content: str, draft_type: str = "general", phase: str = None) -> Dict[str, Any]:
    """
    Save draft with automatic versioning
    
    Args:
        workflow_id: Workflow identifier
        content: Draft content
        draft_type: Type of draft
        phase: Optional workflow phase
        
    Returns:
        Dict with draft save results
    """
    if not workflow_id or not content:
        return {"error": "Workflow ID and content are required"}
    
    try:
        manager = FilesAPIManager()
        file_id = manager.save_draft(workflow_id, content, draft_type, phase)
        
        return {
            "status": "success",
            "file_id": file_id,
            "draft_type": draft_type,
            "phase": phase,
            "content_length": len(content),
            "operation": "save_draft",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Draft save failed: {str(e)}"}

@handle_errors(operation_name="prepare_handoff", return_dict=True)
def prepare_agent_handoff(workflow_id: str, agent_materials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Package materials for agent handoff
    
    Args:
        workflow_id: Workflow identifier
        agent_materials: Materials to package for agent
        
    Returns:
        Dict with handoff preparation results
    """
    if not workflow_id:
        return {"error": "Workflow ID is required"}
    
    try:
        manager = FilesAPIManager()
        file_id = manager.prepare_agent_handoff(workflow_id, agent_materials)
        
        return {
            "status": "success",
            "file_id": file_id,
            "materials_count": len(agent_materials),
            "operation": "prepare_handoff",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Handoff preparation failed: {str(e)}"}

@handle_errors(operation_name="save_deliverables", return_dict=True)
def save_agent_deliverables(workflow_id: str, phase: str, deliverables: Dict[str, str]) -> Dict[str, Any]:
    """
    Save agent deliverables with organized structure
    
    Args:
        workflow_id: Workflow identifier
        phase: Workflow phase
        deliverables: Dictionary of deliverable name to content mappings
        
    Returns:
        Dict with deliverables save results
    """
    if not workflow_id or not deliverables:
        return {"error": "Workflow ID and deliverables are required"}
    
    try:
        manager = FilesAPIManager()
        saved_files = manager.save_agent_deliverables(workflow_id, phase, deliverables)
        
        return {
            "status": "success",
            "saved_files": saved_files,
            "deliverables_count": len(saved_files),
            "phase": phase,
            "operation": "save_deliverables",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Deliverables save failed: {str(e)}"}

@handle_errors(operation_name="get_workflow_files", return_dict=True)
def get_workflow_files(workflow_id: str) -> Dict[str, Any]:
    """
    Get all files associated with a workflow
    
    Args:
        workflow_id: Workflow identifier
        
    Returns:
        Dict with workflow files listing
    """
    if not workflow_id:
        return {"error": "Workflow ID is required"}
    
    # Check cache first
    cache_key = f"workflow_files_{workflow_id}"
    cached_result = cache.get_cached_analysis(cache_key, "files_api_files")
    if cached_result:
        return json.loads(cached_result)
    
    try:
        manager = FilesAPIManager()
        workflow_files = manager.get_workflow_files(workflow_id)
        
        result = {
            "status": "success",
            "workflow_files": workflow_files,
            "total_files": sum(len(files) for files in workflow_files.values()),
            "operation": "get_workflow_files",
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result (short-term since files change)
        cache.cache_content_analysis(cache_key, json.dumps(result), "files_api_files")
        
        return result
        
    except Exception as e:
        return {"error": f"File listing failed: {str(e)}"}

class FilesAPIManager:
    """Manages workflow files and agent handoffs using Anthropic Files API"""
    
    def __init__(self):
        # Initialize Files API client when available
        self._client = None
        self.memory_mcp = None
        
    @property
    def client(self):
        """Lazy load Files API client"""
        if self._client is None:
            try:
                # This would connect to Anthropic Files API
                # For now, using a mock implementation
                self._client = MockFilesAPI()
            except Exception:
                # Fallback to local file system
                self._client = LocalFilesFallback()
        return self._client
    
    def set_memory_mcp(self, memory_manager):
        """Set Memory MCP manager for integration"""
        self.memory_mcp = memory_manager
    
    def create_workflow_workspace(self, workflow_id: str) -> Dict[str, str]:
        """Create file structure for workflow"""
        workspace_structure = {
            "config": f"workflow-{workflow_id}-config.json",
            "drafts_dir": f"workflow-{workflow_id}-drafts" / "",
            "handoffs_dir": f"workflow-{workflow_id}-handoffs" / "",
            "deliverables_dir": f"workflow-{workflow_id}-deliverables" / "",
            "metadata": f"workflow-{workflow_id}-metadata.json"
        }
        
        # Create metadata file
        metadata = {
            "workflow_id": workflow_id,
            "created": datetime.now().isoformat(),
            "workspace_structure": workspace_structure,
            "status": "initialized"
        }
        
        metadata_file_id = self.client.upload(
            json.dumps(metadata, indent=2),
            workspace_structure["metadata"]
        )
        
        # Store workspace info in Memory MCP if available
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id, 
                f"Files API workspace created: {metadata_file_id}"
            )
        
        return workspace_structure
    
    def save_draft(self, workflow_id: str, content: str, draft_type: str, phase: str = None) -> str:
        """Save draft with automatic versioning"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        phase_suffix = f"-{phase}" if phase else ""
        filename = f"workflow-{workflow_id}-{draft_type}{phase_suffix}-{timestamp}"
        
        file_id = self.client.upload(content, filename)
        
        # Update Memory MCP with draft info if available
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Draft saved: {draft_type} ({filename}) -> {file_id}"
            )
        
        return file_id
    
    def prepare_agent_handoff(self, workflow_id: str, agent_materials: Dict[str, Any]) -> str:
        """Package materials for agent handoff"""
        
        # Get workflow context from Memory MCP if available
        workflow_context = None
        if self.memory_mcp:
            workflow_context = self.memory_mcp.get_workflow_context(workflow_id)
        
        handoff_package = {
            "workflow_id": workflow_id,
            "handoff_id": uuid4().hex[:8],
            "context": workflow_context,
            "materials": agent_materials,
            "instructions": {
                "return_method": f"Files API handoff response",
                "workflow_callback": f"workflow-{workflow_id}",
                "expected_deliverables": agent_materials.get("expected_outputs", [])
            },
            "handoff_timestamp": datetime.now().isoformat(),
            "status": "prepared"
        }
        
        filename = f"handoff-{workflow_id}-{handoff_package['handoff_id']}"
        file_id = self.client.upload(
            json.dumps(handoff_package, indent=2), 
            filename
        )
        
        # Track handoff in Memory MCP
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Agent handoff prepared: {handoff_package['handoff_id']} -> {file_id}"
            )
        
        return file_id
    
    def restore_agent_context(self, workflow_id: str, handoff_file_id: str) -> Dict[str, Any]:
        """Restore context when agent returns"""
        handoff_data = self.client.download(handoff_file_id)
        package = json.loads(handoff_data)
        
        # Validate package
        if package.get("workflow_id") != workflow_id:
            raise ValueError(f"Handoff package workflow ID mismatch: expected {workflow_id}, got {package.get('workflow_id')}")
        
        # Update workflow state with return
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Agent returned from handoff: {package.get('handoff_id')} ({handoff_file_id})"
            )
        
        return package
    
    def save_agent_deliverables(self, workflow_id: str, phase: str, deliverables: Dict[str, str]) -> Dict[str, str]:
        """Save agent deliverables with organized structure"""
        saved_files = {}
        
        for deliverable_name, content in deliverables.items():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workflow-{workflow_id}-{phase}-{deliverable_name}-{timestamp}"
            
            file_id = self.client.upload(content, filename)
            saved_files[deliverable_name] = file_id
            
            # Track deliverable in Memory MCP
            if self.memory_mcp:
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Deliverable saved: {phase}" / "{deliverable_name} -> {file_id}"
                )
        
        return saved_files
    
    def get_workflow_files(self, workflow_id: str) -> Dict[str, List[str]]:
        """Get all files associated with a workflow"""
        try:
            all_files = self.client.list_files()
            workflow_files = {
                "config": [],
                "drafts": [],
                "handoffs": [],
                "deliverables": [],
                "metadata": []
            }
            
            workflow_prefix = f"workflow-{workflow_id}"
            
            for file_info in all_files:
                filename = file_info.get("filename", "")
                if filename.startswith(workflow_prefix):
                    if "config" in filename:
                        workflow_files["config"].append(file_info)
                    elif "draft" in filename:
                        workflow_files["drafts"].append(file_info)
                    elif "handoff" in filename:
                        workflow_files["handoffs"].append(file_info)
                    elif "deliverable" in filename:
                        workflow_files["deliverables"].append(file_info)
                    elif "metadata" in filename:
                        workflow_files["metadata"].append(file_info)
            
            return workflow_files
        except Exception as e:
            logger.warning(f"Failed to get workflow files: {e}")
            return {}
    
    def cleanup_workflow_files(self, workflow_id: str, keep_deliverables: bool = True):
        """Clean up temporary files for completed workflow"""
        workflow_files = self.get_workflow_files(workflow_id)
        
        cleanup_count = 0
        
        # Clean up drafts and handoffs
        for file_type in ["drafts", "handoffs"]:
            for file_info in workflow_files.get(file_type, []):
                try:
                    self.client.delete(file_info["file_id"])
                    cleanup_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete {file_info['filename']}: {e}")
        
        # Optionally clean up deliverables
        if not keep_deliverables:
            for file_info in workflow_files.get("deliverables", []):
                try:
                    self.client.delete(file_info["file_id"])
                    cleanup_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete {file_info['filename']}: {e}")
        
        # Update Memory MCP
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"File cleanup completed: {cleanup_count} files removed"
            )
        
        return cleanup_count


class MockFilesAPI:
    """Mock implementation for development" / "testing"""
    
    def __init__(self):
        self.files = {}
        self.file_counter = 0
    
    def upload(self, content: str, filename: str) -> str:
        """Mock file upload"""
        self.file_counter += 1
        file_id = f"mock_file_{self.file_counter:04d}"
        
        self.files[file_id] = {
            "file_id": file_id,
            "filename": filename,
            "content": content,
            "uploaded": datetime.now().isoformat(),
            "size": len(content)
        }
        
        return file_id
    
    def download(self, file_id: str) -> str:
        """Mock file download"""
        if file_id not in self.files:
            raise FileNotFoundError(f"File {file_id} not found")
        
        return self.files[file_id]["content"]
    
    def list_files(self) -> List[Dict[str, Any]]:
        """Mock file listing"""
        return [
            {
                "file_id": file_id,
                "filename": file_info["filename"],
                "uploaded": file_info["uploaded"],
                "size": file_info["size"]
            }
            for file_id, file_info in self.files.items()
        ]
    
    def delete(self, file_id: str) -> bool:
        """Mock file deletion"""
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False


class LocalFilesFallback:
    """Local file system fallback when Files API unavailable"""
    
    def __init__(self):
        self.storage_dir = Path.cwd() " / " "configs" " / " "files_fallback"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Metadata tracking
        self.metadata_file = self.storage_dir " / " "files_metadata.json"
        self.files_metadata = self._load_metadata()
        self.file_counter = len(self.files_metadata)
    
    def _load_metadata(self):
        """Load file metadata"""
        try:
            with open(self.metadata_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_metadata(self):
        """Save file metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.files_metadata, f, indent=2)
    
    def upload(self, content: str, filename: str) -> str:
        """Local file save"""
        self.file_counter += 1
        file_id = f"local_file_{self.file_counter:04d}"
        
        # Save content to file
        file_path = self.storage_dir " / " f"{file_id}_{filename}"
        with open(file_path, 'w') as f:
            f.write(content)
        
        # Update metadata
        self.files_metadata[file_id] = {
            "file_id": file_id,
            "filename": filename,
            "path": str(file_path),
            "uploaded": datetime.now().isoformat(),
            "size": len(content)
        }
        
        self._save_metadata()
        return file_id
    
    def download(self, file_id: str) -> str:
        """Local file read"""
        if file_id not in self.files_metadata:
            raise FileNotFoundError(f"File {file_id} not found")
        
        file_path = self.files_metadata[file_id]["path"]
        with open(file_path) as f:
            return f.read()
    
    def list_files(self) -> List[Dict[str, Any]]:
        """Local file listing"""
        return [
            {
                "file_id": file_id,
                "filename": file_info["filename"],
                "uploaded": file_info["uploaded"],
                "size": file_info["size"]
            }
            for file_id, file_info in self.files_metadata.items()
        ]
    
    def delete(self, file_id: str) -> bool:
        """Local file deletion"""
        if file_id in self.files_metadata:
            try:
                file_path = Path(self.files_metadata[file_id]["path"])
                if file_path.exists():
                    file_path.unlink()
                del self.files_metadata[file_id]
                self._save_metadata()
                return True
            except Exception:
                pass
        return False
