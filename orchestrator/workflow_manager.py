"""
Workflow Manager 
Handles workflow ID generation, discovery, and tracking
Clean implementation with proper imports and multilingual tag support
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

# Standard MAO imports - absolute paths
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
from orchestrator.user_analytics_manager import UserAnalyticsManager
from orchestrator.system_analytics_manager import SystemAnalyticsManager
from orchestrator.username_manager import UsernameManager

# Import workflow ID generator
from scripts.unique_id_generator.unique_id_generator import generate_workflow_uid, generate_workflow_uid_with_explanation

# Standard cache instance
cache = CacheManager()

class WorkflowManager:
    """
    Manages workflow IDs, discovery, and tracking
    Provides workflow search and management capabilities
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "configs"
        self.workflows_dir = self.base_path / "workflows"
        self.temp_dir = self.workflows_dir / ".temp"
        
        # Analytics managers
        self.user_analytics_manager = UserAnalyticsManager()
        self.system_analytics_manager = SystemAnalyticsManager()
        self.username_manager = UsernameManager()
        
        # Ensure directories exist
        self.workflows_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    @handle_errors(operation_name="generate_workflow_id", return_dict=True)
    def generate_workflow_id(self, with_explanation: bool = False) -> Dict[str, Any]:
        """
        Generate a new unique workflow ID
        Returns workflow ID and optional mathematical explanation
        """
        try:
            if with_explanation:
                workflow_id, explanation = generate_workflow_uid_with_explanation()
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "explanation": explanation,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                workflow_id = generate_workflow_uid()
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            raise APIError(f"Failed to generate workflow ID: {str(e)}")
    
    @handle_errors(operation_name="list_workflows", return_dict=True)
    def list_workflows(self) -> List[Dict[str, Any]]:
        """Get fresh list of all workflows from directory"""
        workflows = []
        
        # Scan main workflows directory
        for workflow_dir in self.workflows_dir.iterdir():
            if workflow_dir.is_dir() and not workflow_dir.name.startswith('.'):
                workflow_info = self._extract_workflow_info(workflow_dir)
                if workflow_info:
                    workflows.append(workflow_info)
        
        # Sort by last_modified (most recent first)
        workflows.sort(key=lambda x: x.get("last_modified", ""), reverse=True)
        
        return workflows
    
    @handle_errors(operation_name="find_workflows", return_dict=True)
    def find_workflows(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Find workflows by ID, command, goal, or description
        Useful for workflow discovery
        """
        if not search_term:
            return []
        
        search_lower = search_term.lower().strip()
        matches = []
        
        for workflow_info in self.list_workflows():
            # Search in various fields
            searchable_fields = [
                workflow_info.get("workflow_id", "").lower(),
                workflow_info.get("custom_command", "").lower(),
                workflow_info.get("workflow_goal", "").lower(),
                workflow_info.get("workflow_description", "").lower(),
                workflow_info.get("directory_name", "").lower()
            ]
            
            if any(search_lower in field for field in searchable_fields if field):
                matches.append(workflow_info)
        
        return matches
    
    @handle_errors(operation_name="get_workflow_by_id", return_dict=True)
    def get_workflow_by_id(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow information by workflow ID"""
        if not workflow_id:
            return None
        
        # Check cache first
        cache_key = f"workflow_info_{workflow_id}"
        cached_result = cache.get_cached_analysis(cache_key, "workflow_manager")
        if cached_result:
            return json.loads(cached_result)
        
        for workflow_info in self.list_workflows():
            if workflow_info.get("workflow_id") == workflow_id:
                # Cache the result
                cache.cache_content_analysis(cache_key, json.dumps(workflow_info), "workflow_manager")
                return workflow_info
        
        return None
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get_workflow_by_id for UI compatibility"""
        return self.get_workflow_by_id(workflow_id)
    
    @handle_errors(operation_name="get_workflow_by_command", return_dict=True)
    def get_workflow_by_command(self, custom_command: str) -> Optional[Dict[str, Any]]:
        """Get workflow information by custom command"""
        if not custom_command:
            return None
        
        command_lower = custom_command.lower().strip()
        
        for workflow_info in self.list_workflows():
            if workflow_info.get("custom_command", "").lower() == command_lower:
                return workflow_info
        
        return None
    
    @handle_errors(operation_name="list_active_workflows", return_dict=True)
    def list_active_workflows(self) -> List[Dict[str, Any]]:
        """Get workflows that are currently active/in-progress"""
        active_workflows = []
        
        for workflow_info in self.list_workflows():
            # Check if workflow has active status indicators
            status = workflow_info.get("status", "unknown").lower()
            if status in ["active", "in_progress", "running", "paused"]:
                active_workflows.append(workflow_info)
        
        return active_workflows
    
    @handle_errors(operation_name="list_temp_workflows", return_dict=True)
    def list_temp_workflows(self) -> List[Dict[str, Any]]:
        """Get workflows in temporary directory (being created)"""
        temp_workflows = []
        
        for temp_dir in self.temp_dir.iterdir():
            if temp_dir.is_dir():
                temp_info = self._extract_temp_workflow_info(temp_dir)
                if temp_info:
                    temp_workflows.append(temp_info)
        
        return temp_workflows
    
    def _extract_workflow_info(self, workflow_dir: Path) -> Optional[Dict[str, Any]]:
        """Extract workflow information from workflow directory"""
        try:
            config_dir = workflow_dir / "config-files"
            if not config_dir.exists():
                return None
            
            # Look for main workflow config file
            workflow_config = None
            for config_file in config_dir.glob("*_workflow_config.json"):
                try:
                    with open(config_file, 'r') as f:
                        workflow_config = json.load(f)
                    break
                except (json.JSONDecodeError, IOError):
                    continue
            
            if not workflow_config:
                return None
            
            # Extract key information
            workflow_data = workflow_config.get("workflow", [{}])[0] if workflow_config.get("workflow") else {}
            
            info = {
                "directory_name": workflow_dir.name,
                "directory_path": str(workflow_dir),
                "workflow_id": workflow_data.get("workflow_id", "unknown"),
                "custom_command": workflow_data.get("custom_command", "unknown"),
                "workflow_goal": workflow_data.get("workflow_goal", ""),
                "workflow_description": workflow_data.get("workflow_description", ""),
                "workflow_deliverable": workflow_data.get("workflow_deliverable", ""),
                "user_id": workflow_data.get("user_id", "unknown"),
                "created_at": workflow_data.get("created_at", ""),
                "status": self._determine_workflow_status(workflow_dir),
                "last_modified": self._get_last_modified(workflow_dir),
                "has_deliverables": (workflow_dir / "deliverables").exists(),
                "has_metadata": (workflow_dir / "metadata").exists()
            }
            
            return info
            
        except Exception:
            return None
    
    def _extract_temp_workflow_info(self, temp_dir: Path) -> Optional[Dict[str, Any]]:
        """Extract workflow information from temporary directory"""
        try:
            # Look for any JSON files in temp directory
            workflow_files = list(temp_dir.glob("*.json"))
            if not workflow_files:
                return None
            
            # Try to find workflow config
            for config_file in workflow_files:
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                    
                    # Check if this looks like a workflow config
                    if "workflow" in config_data or "workflow_id" in config_data:
                        workflow_data = config_data.get("workflow", [{}])[0] if config_data.get("workflow") else config_data
                        
                        return {
                            "directory_name": temp_dir.name,
                            "directory_path": str(temp_dir),
                            "workflow_id": workflow_data.get("workflow_id", "temp"),
                            "custom_command": workflow_data.get("custom_command", "temp"),
                            "workflow_goal": workflow_data.get("workflow_goal", ""),
                            "status": "temp",
                            "last_modified": self._get_last_modified(temp_dir),
                            "is_temporary": True
                        }
                except (json.JSONDecodeError, IOError):
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _determine_workflow_status(self, workflow_dir: Path) -> str:
        """Determine workflow status based on directory contents"""
        try:
            metadata_dir = workflow_dir / "metadata"
            deliverables_dir = workflow_dir / "deliverables"
            
            if deliverables_dir.exists() and any(deliverables_dir.iterdir()):
                return "completed"
            elif metadata_dir.exists():
                # Check for log files indicating active status
                log_files = list(metadata_dir.glob("*_log.json"))
                if log_files:
                    return "active"
            
            return "created"
            
        except Exception:
            return "unknown"
    
    def _get_last_modified(self, directory: Path) -> str:
        """Get last modification time of directory"""
        try:
            return datetime.fromtimestamp(directory.stat().st_mtime).isoformat()
        except Exception:
            return datetime.now().isoformat()
    
    def extract_workflow_tags(self, workflow_path: Path) -> List[str]:
        """
        Extract explicit tags from workflow README.md for analytics
        
        BEHAVIORAL GUIDANCE FOR MAO:
        - Only extract explicit tags that users or Mao actually write
        - Support multilingual tags - use whatever language is in the README
        - No automatic categorization or English keyword detection
        - Tags come from "Tags:" lines and hashtags only
        """
        try:
            readme_path = workflow_path / "README.md"
            if not readme_path.exists():
                return []
            
            with open(readme_path, 'r') as f:
                content = f.read()
            
            tags = []
            
            # Extract explicit tags from "Tags:" lines
            if "Tags:" in content:
                lines = content.splitlines()
                for line in lines:
                    if line.strip().startswith("Tags:"):
                        tag_line = line.split("Tags:")[1].strip()
                        tags.extend([tag.strip() for tag in tag_line.split(',')])
                        break
            
            # Extract hashtags
            import re
            hashtags = re.findall(r'#(\w+)', content)
            tags.extend(hashtags)
            
            # Remove duplicates and return
            return list(set(tags))
            
        except Exception as e:
            return []
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        operation = params.get("operation", "unknown")
        
        cost_map = {
            "generate_workflow_id": 0.0001,  # Very cheap ID generation
            "list_workflows": 0.001,
            "find_workflows": 0.002,
            "get_workflow": 0.0005,
            "workflow_discovery": 0.001
        }
        
        return cost_map.get(operation, 0.001)
    
    @handle_errors
    def track_workflow_start(self, workflow_id: str, workflow_command: str, username: str, tags: List[str] = None) -> bool:
        """Track workflow start for analytics"""
        try:
            # Track workflow start
            self.user_analytics_manager.track_workflow(
                username, workflow_id, workflow_command, "start", tags=tags or []
            )
            
            return True
            
        except Exception as e:
            # Analytics failures should not break workflow execution
            return False
    
    @handle_errors
    def track_workflow_completion(self, workflow_id: str, username: str, success: bool = True) -> bool:
        """Track workflow completion for analytics"""
        try:
            # Track workflow completion
            self.user_analytics_manager.track_workflow(
                username, workflow_id, "", "complete", success=success
            )
            
            return True
            
        except Exception as e:
            # Analytics failures should not break workflow execution
            return False


# Standalone functions for backward compatibility
def generate_workflow_id(with_explanation: bool = False) -> Dict[str, Any]:
    """Standalone function for generating workflow ID"""
    manager = WorkflowManager()
    return manager.generate_workflow_id(with_explanation)

def list_workflows() -> List[Dict[str, Any]]:
    """Standalone function for listing all workflows"""
    manager = WorkflowManager()
    return manager.list_workflows()

def find_workflows(search_term: str) -> List[Dict[str, Any]]:
    """Standalone function for finding workflows"""
    manager = WorkflowManager()
    return manager.find_workflows(search_term)

def get_workflow_by_id(workflow_id: str) -> Optional[Dict[str, Any]]:
    """Standalone function for getting workflow by ID"""
    manager = WorkflowManager()
    return manager.get_workflow_by_id(workflow_id)

def get_workflow(workflow_id: str) -> Optional[Dict[str, Any]]:
    """Standalone function for getting workflow (UI compatibility)"""
    manager = WorkflowManager()
    return manager.get_workflow(workflow_id)

def get_workflow_by_command(custom_command: str) -> Optional[Dict[str, Any]]:
    """Standalone function for getting workflow by command"""
    manager = WorkflowManager()
    return manager.get_workflow_by_command(custom_command)

def list_active_workflows() -> List[Dict[str, Any]]:
    """Standalone function for listing active workflows"""
    manager = WorkflowManager()
    return manager.list_active_workflows()

def list_temp_workflows() -> List[Dict[str, Any]]:
    """Standalone function for listing temporary workflows"""
    manager = WorkflowManager()
    return manager.list_temp_workflows()