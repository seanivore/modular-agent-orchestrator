#!/usr/bin/env python3
"""
Memory MCP Manager for Workflow State Persistence
Provides workflow context tracking, state management, and session recovery
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4

from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError

class MemoryMCPManager:
    """Manages workflow state persistence using Memory MCP"""
    
    def __init__(self):
        # Standard cache instance
        self.cache = CacheManager()
        
        # Initialize MCP client when available
        self._client = None
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Memory MCP operations are generally very low cost
        base_cost = 0.0
        
        # Add cost for workflow creation
        num_workflows = params.get("num_workflows", 1)
        base_cost += num_workflows * 0.001  # $0.001 per workflow
        
        # Add cost for state updates
        state_updates = params.get("state_updates", 5)
        base_cost += state_updates * 0.0001  # $0.0001 per update
        
        # Add cost for search operations
        search_operations = params.get("search_operations", 1)
        base_cost += search_operations * 0.0005  # $0.0005 per search
        
        # Add cost for recovery operations
        recovery_operations = params.get("recovery_operations", 0)
        base_cost += recovery_operations * 0.001  # $0.001 per recovery
        
        return base_cost
        
    @property
    def client(self):
        """Lazy load MCP client to avoid import issues"""
        if self._client is None:
            try:
                # Try to connect to Memory MCP server via STDIO subprocess
                # Uses: npx -y @modelcontextprotocol/server-memory
                import subprocess
                import json
                from pathlib import Path
                
                # Check if memory server is configured
                config_file = Path.cwd() / "configs" / "connections" / "mcp_servers.json"
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                    
                    if "memory" in config.get("servers", {}):
                        memory_config = config["servers"]["memory"]
                        
                        # Start the memory MCP server subprocess
                        cmd = [memory_config.get("command", "npx")]
                        cmd.extend(memory_config.get("args", ["-y", "@modelcontextprotocol/server-memory"]))
                        
                        # For now, we'll still use fallback until subprocess communication is implemented
                        # TODO: Implement proper STDIO MCP client communication
                        raise Exception("STDIO MCP client not yet implemented - using fallback")
                
                raise Exception("Memory MCP server not configured - using fallback")
                
            except Exception:
                # Fallback to local storage if MCP unavailable
                self._client = LocalMemoryFallback()
        return self._client
    
    @handle_errors(operation_name="create_workflow_context", return_dict=False)
    def create_workflow_context(self, workflow_id: str, user_goal: str) -> str:
        """Create workflow entity with unique ID"""
        entity_data = {
            "name": f"workflow-{workflow_id}",
            "entityType": "active-workflow", 
            "observations": [
                f"User goal: {user_goal}",
                f"Created: {datetime.now().isoformat()}",
                f"Workflow ID: {workflow_id}",
                "Status: initialized"
            ]
        }
        
        result = self.client.create_entities([entity_data])
        return f"workflow-{workflow_id}"
    
    def update_workflow_state(self, workflow_id: str, state_update: str) -> bool:
        """Add observations to workflow entity"""
        observation_data = {
            "entityName": f"workflow-{workflow_id}",
            "contents": [f"{datetime.now().strftime('%H:%M:%S')} - {state_update}"]
        }
        
        try:
            self.client.add_observations([observation_data])
            return True
        except Exception as e:
            # Use logging instead of print
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to update workflow state: {e}")
            return False
    
    @handle_errors(operation_name="get_workflow_context", return_dict=False)
    def get_workflow_context(self, workflow_id: str) -> Optional[Dict]:
        """Retrieve full workflow context"""
        # Check cache first for recent workflow contexts
        cache_key = f"workflow_context|{workflow_id}"
        cached_result = self.cache.get_cached_analysis(cache_key, "workflow_context")
        if cached_result:
            return json.loads(cached_result)
        
        try:
            context = self.client.open_nodes([f"workflow-{workflow_id}"])
            if context and len(context) > 0:
                result = context[0]
                # Cache the result for future use
                self.cache.cache_content_analysis(cache_key, json.dumps(result), "workflow_context")
                return result
            return None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to retrieve workflow context: {e}")
            return None
    
    @handle_errors(operation_name="search_workflow_patterns", return_dict=False)
    def search_workflow_patterns(self, query: str) -> List[Dict]:
        """Find similar workflows for pattern matching"""
        try:
            results = self.client.search_nodes(query)
            # Filter for workflow entities only
            workflows = [r for r in results if r.get('entityType') == 'active-workflow']
            return workflows
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to search workflow patterns: {e}")
            return []
        
    @handle_errors(operation_name="handle_session_recovery", return_dict=False)
    def handle_session_recovery(self, workflow_id: str) -> Optional[Dict]:
        """Restore workflow state after interruption"""
        context = self.get_workflow_context(workflow_id)
        if context:
            recovery_info = self._parse_workflow_state(context)
            
            # Log recovery attempt
            self.update_workflow_state(
                workflow_id,
                f"Session recovery attempted - Status: {recovery_info.get('status', 'unknown')}"
            )
            
            return recovery_info
        return None
    
    def _parse_workflow_state(self, context: Dict) -> Dict:
        """Parse workflow context into recovery information"""
        observations = context.get('observations', [])
        
        # Extract key information from observations using structured approach
        status = "unknown"
        progress = 0
        phase_info = []
        
        for obs in observations:
            # Use structured parsing instead of English keyword detection
            # Look for patterns that work in any language
            
            # Try to extract status from timestamp format: "timestamp - Status: value"
            if " - " in obs and ":" in obs:
                parts = obs.split(" - ", 1)
                if len(parts) > 1:
                    content = parts[1]
                    # Look for key-value patterns
                    if ":" in content:
                        key, value = content.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if "status" in key:
                            status = value
                        elif "progress" in key:
                            try:
                                # Extract numeric progress
                                import re
                                nums = re.findall(r'\d+', value)
                                if nums:
                                    progress = int(nums[0])
                            except ValueError:
                                pass
                        elif "phase" in key.lower() and ("completed" in value.lower() or "finished" in value.lower()):
                            phase_info.append(obs)
        
        # Determine resumability based on status patterns (language-neutral)
        resumable_indicators = ["progress", "active", "running", "executing", "waiting", "pause"]
        can_resume = any(indicator in status.lower() for indicator in resumable_indicators)
        
        return {
            "workflow_id": context.get('name', '').replace('workflow-', ''),
            "status": status,
            "progress_percentage": progress,
            "completed_phases": phase_info,
            "can_resume": can_resume,
            "last_activity": observations[-1] if observations else "No activity recorded"
        }
    
    def list_active_workflows(self) -> List[Dict]:
        """Get all active workflows"""
        try:
            all_workflows = self.client.search_nodes("active-workflow")
            active = [w for w in all_workflows if 'completed' not in w.get('observations', [])[-1].lower()]
            return active
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to list active workflows: {e}")
            return []
    
    def mark_workflow_complete(self, workflow_id: str, final_results: Dict):
        """Mark workflow as completed with final results"""
        completion_data = {
            "final_cost": final_results.get('total_cost', 0),
            "duration_minutes": final_results.get('duration', 0),
            "deliverables_count": len(final_results.get('files', [])),
            "success": final_results.get('success', False)
        }
        
        self.update_workflow_state(
            workflow_id,
            f"COMPLETED - {json.dumps(completion_data)}"
        )
        
        return True


class LocalMemoryFallback:
    """Local file-based fallback when MCP unavailable"""
    
    def __init__(self):
        from pathlib import Path
        self.storage_dir = Path.cwd() / "configs" / "memory_fallback"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self.entities_file = self.storage_dir / "entities.json"
        self.observations_file = self.storage_dir / "observations.json"
        
        self.entities = self._load_json(self.entities_file, {})
        self.observations = self._load_json(self.observations_file, {})
    
    def _load_json(self, file_path, default):
        """Load JSON file with fallback"""
        try:
            with open(file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return default
    
    def _save_data(self):
        """Save data to files"""
        with open(self.entities_file, 'w') as f:
            json.dump(self.entities, f, indent=2)
        with open(self.observations_file, 'w') as f:
            json.dump(self.observations, f, indent=2)
    
    def create_entities(self, entities: List[Dict]) -> List[str]:
        """Local entity creation"""
        created = []
        for entity in entities:
            entity_id = entity['name']
            self.entities[entity_id] = entity
            self.observations[entity_id] = entity.get('observations', [])
            created.append(entity_id)
        
        self._save_data()
        return created
    
    def add_observations(self, observations: List[Dict]) -> bool:
        """Local observation addition"""
        for obs_data in observations:
            entity_name = obs_data['entityName']
            if entity_name in self.observations:
                self.observations[entity_name].extend(obs_data['contents'])
            else:
                self.observations[entity_name] = obs_data['contents']
        
        self._save_data()
        return True
    
    def open_nodes(self, names: List[str]) -> List[Dict]:
        """Local node retrieval"""
        results = []
        for name in names:
            if name in self.entities:
                entity = self.entities[name].copy()
                entity['observations'] = self.observations.get(name, [])
                results.append(entity)
        return results
    
    def search_nodes(self, query: str) -> List[Dict]:
        """Local node search"""
        results = []
        for entity_id, entity in self.entities.items():
            # Simple text search
            entity_text = json.dumps(entity).lower()
            obs_text = ' '.join(self.observations.get(entity_id, [])).lower()
            
            if query.lower() in entity_text or query.lower() in obs_text:
                result = entity.copy()
                result['observations'] = self.observations.get(entity_id, [])
                results.append(result)
        return results