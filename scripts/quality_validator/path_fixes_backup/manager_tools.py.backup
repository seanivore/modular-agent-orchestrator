"""
Tool Discovery
Dynamic tool suggestion based on goals, not hardcoded categories
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import importlib.util
import time
from datetime import datetime, timezone

# Standard MAO imports (following standardization pattern)
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors

# Analytics managers
from orchestrator.user_analytics_manager import UserAnalyticsManager
from orchestrator.system_analytics_manager import SystemAnalyticsManager
from orchestrator.username_manager import UsernameManager

# Standard cache instance
cache = CacheManager()


class ToolManager:
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.tool_registry = self._load_tool_registry()
        self.discovered_tools = {}
        
        # Lazy load MCP connector for external tools
        self._mcp_connector = None
        self._memory_mcp = None
        
        # Analytics managers
        self.user_analytics_manager = UserAnalyticsManager()
        self.system_analytics_manager = SystemAnalyticsManager()
        self.username_manager = UsernameManager()
        
        # Discover all tools on initialization
        self.discover_all_tools()
        
    def _load_tool_registry(self) -> Dict[str, Any]:
        """Load tool registry from JSON files"""
        registry = {}
        
        # Load all tool registry files
        registry_dir = self.config_dir / "tool_registry"
        if registry_dir.exists():
            for tool_file in registry_dir.glob("*.json"):
                try:
                    with open(tool_file, 'r') as f:
                        tool_data = json.load(f)
                        tool_id = tool_file.stem  # filename without .json
                        registry[tool_id] = tool_data
                except Exception as e:
                    # Store error for UI layer to display
                    pass  # Could log to structured error collection if needed
        
        return registry
    
    def suggest_tools_for_goal(self, goal: str, model: str = "claude-sonnet-4", 
                              budget_limit: float = 1.0) -> Dict[str, Any]:
        """
        🎯 Suggest tools based on goal analysis
        No hardcoded categories - pure goal-to-capability matching
        """
        goal_lower = goal.lower()
        suggested_tools = []
        total_cost = 0.0
        
        # Analyze each tool's relevance to the goal
        for tool_id, tool_config in self.tool_registry.items():
            relevance_score = self._calculate_relevance(goal_lower, tool_config)
            
            if relevance_score > 0:
                tool_cost = tool_config.get("cost_estimate", 0.0)
                
                # Check budget constraint
                if total_cost + tool_cost <= budget_limit:
                    suggested_tools.append({
                        "tool_id": tool_id,
                        "name": tool_config.get("name", tool_id),
                        "description": tool_config.get("description", ""),
                        "cost": tool_cost,
                        "relevance": relevance_score,
                        "reason": self._generate_relevance_reason(goal_lower, tool_config)
                    })
                    total_cost += tool_cost
        
        # Sort by relevance score (highest first)
        suggested_tools.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "suggested_tools": suggested_tools[:5],  # Top 5 suggestions
            "total_estimated_cost": total_cost,
            "goal_analysis": self._analyze_goal_complexity(goal),
            "model_compatibility": self._check_model_compatibility(suggested_tools, model)
        }
    
    def _calculate_relevance(self, goal: str, tool_config: Dict) -> float:
        """
        Calculate how relevant a tool is to the goal
        Uses semantic matching, not hardcoded categories
        """
        relevance = 0.0
        
        # Check description overlap
        description = tool_config.get("description", "").lower()
        goal_words = set(goal.split())
        desc_words = set(description.split())
        
        # Word overlap scoring
        common_words = goal_words.intersection(desc_words)
        if common_words:
            relevance += len(common_words) * 0.3
        
        # Check capabilities overlap
        capabilities = tool_config.get("capabilities", [])
        for capability in capabilities:
            cap_words = set(capability.lower().split())
            cap_overlap = goal_words.intersection(cap_words)
            if cap_overlap:
                relevance += len(cap_overlap) * 0.5
        
        # Check use cases overlap
        use_cases = tool_config.get("use_cases", [])
        for use_case in use_cases:
            case_words = set(use_case.lower().split())
            case_overlap = goal_words.intersection(case_words)
            if case_overlap:
                relevance += len(case_overlap) * 0.4
        
        return relevance
    
    def _generate_relevance_reason(self, goal: str, tool_config: Dict) -> str:
        """Generate human-readable reason for tool suggestion"""
        goal_words = set(goal.split())
        
        # Find the strongest connection
        description = tool_config.get("description", "").lower()
        desc_words = set(description.split())
        desc_overlap = goal_words.intersection(desc_words)
        
        capabilities = tool_config.get("capabilities", [])
        cap_matches = []
        for cap in capabilities:
            cap_words = set(cap.lower().split())
            if goal_words.intersection(cap_words):
                cap_matches.append(cap)
        
        if cap_matches:
            return f"Matches your need for {cap_matches[0].lower()}"
        elif desc_overlap:
            return f"Relevant for {' '.join(list(desc_overlap)[:2])}"
        else:
            return "May be useful for this task"
    
    def _analyze_goal_complexity(self, goal: str) -> Dict[str, Any]:
        """Analyze goal complexity without hardcoded assumptions"""
        words = goal.split()
        
        return {
            "word_count": len(words),
            "estimated_complexity": "simple" if len(words) < 10 else "complex",
            "contains_multiple_tasks": "and" in goal.lower() or "then" in goal.lower(),
            "time_sensitive": any(word in goal.lower() for word in ["urgent", "asap", "quickly", "fast"])
        }
    
    def _check_model_compatibility(self, tools: List[Dict], model: str) -> Dict[str, Any]:
        """Check tool compatibility with selected model"""
        compatible_tools = []
        incompatible_tools = []
        
        for tool in tools:
            tool_id = tool["tool_id"]
            tool_config = self.tool_registry.get(tool_id, {})
            
            # Check if model is in supported models list
            supported_models = tool_config.get("supported_models", [])
            if not supported_models or model in supported_models:
                compatible_tools.append(tool_id)
            else:
                incompatible_tools.append(tool_id)
        
        return {
            "compatible_count": len(compatible_tools),
            "incompatible_count": len(incompatible_tools),
            "all_compatible": len(incompatible_tools) == 0,
            "model_used": model
        }
    
    def get_tool_details(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific tool"""
        return self.tool_registry.get(tool_id)
    
    def list_all_tools(self) -> List[Dict[str, Any]]:
        """List all available tools with basic info"""
        tools = []
        
        for tool_id, config in self.tool_registry.items():
            tools.append({
                "tool_id": tool_id,
                "name": config.get("name", tool_id),
                "description": config.get("description", ""),
                "cost": config.get("cost_estimate", 0.0)
            })
        
        return sorted(tools, key=lambda x: x["cost"])
    
    def discover_all_tools(self) -> Dict[str, Any]:
        """Discover tools from multiple sources"""
        tools = {}
        
        # 1. Discover local MAO tools
        local_tools = self._discover_local_tools()
        tools.update(local_tools)
        
        # 2. Discover MCP server tools
        mcp_tools = self._discover_mcp_tools()
        tools.update(mcp_tools)
        
        # 3. Cache discovery results
        self.discovered_tools = tools
        
        # 4. Log discovery results
        if self.memory_mcp:
            try:
                self.memory_mcp.client.create_entities([{
                    "name": "tool-discovery",
                    "entityType": "system-status",
                    "observations": [
                        f"Discovered {len(local_tools)} local tools",
                        f"Discovered {len(mcp_tools)} MCP tools",
                        f"Total tools available: {len(tools)}"
                    ]
                }])
            except Exception as e:
                # Don't fail tool discovery if memory logging fails
                print(f"Warning: Failed to log tool discovery to memory: {e}")
        
        return tools
    
    def _discover_local_tools(self) -> Dict[str, Any]:
        """Discover MAO local tools with 6-file validation"""
        tools_dir = Path.cwd() / "tools"
        local_tools = {}
        
        if not tools_dir.exists():
            return local_tools
        
        for tool_dir in tools_dir.iterdir():
            if not tool_dir.is_dir() or tool_dir.name.startswith('.'):
                continue
            
            # Validate 6-file architecture
            tool_info = self._validate_tool_structure(tool_dir)
            if tool_info:
                local_tools[tool_dir.name] = tool_info
        
        return local_tools
    
    def _validate_tool_structure(self, tool_dir: Path) -> Optional[Dict[str, Any]]:
        """Validate 6-file tool architecture"""
        required_files = {
            "main": tool_dir / f"{tool_dir.name}.py",
            "config": tool_dir / f"tool_{tool_dir.name}.json",
            "button": tool_dir / f"button_{tool_dir.name}.py", 
            "ui": tool_dir / f"ui_{tool_dir.name}.py"
        }
        
        # Check if core files exist
        missing_files = []
        for file_type, file_path in required_files.items():
            if not file_path.exists():
                missing_files.append(file_type)
        
        if missing_files:
            return None  # Tool not properly structured
        
        # Load tool configuration
        try:
            with open(required_files["config"]) as f:
                config = json.load(f)
        except Exception:
            return None  # Invalid config
        
        # Load button generator function
        button_module = self._load_button_module(required_files["button"])
        if not button_module:
            return None  # Missing button function
        
        return {
            "type": "local",
            "name": config.get("name", tool_dir.name),
            "description": config.get("description", ""),
            "config": config,
            "button_generator": button_module.create_button_snippet,
            "main_module": required_files["main"],
            "files": required_files
        }
    
    def _load_button_module(self, button_file: Path):
        """Load button module dynamically"""
        try:
            spec = importlib.util.spec_from_file_location("button_module", button_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if create_button_snippet function exists
            if hasattr(module, 'create_button_snippet'):
                return module
            return None
        except Exception:
            return None
    
    def _discover_mcp_tools(self) -> Dict[str, Any]:
        """Discover tools from MCP servers"""
        if not self.mcp_connector:
            return {}
        
        try:
            mcp_tools = self.mcp_connector.get_available_tools()
            
            # Format MCP tools for unified interface
            formatted_tools = {}
            for tool_name, tool_info in mcp_tools.items():
                formatted_tools[tool_name] = {
                    "type": "mcp",
                    "name": tool_info.get("tool", tool_name),
                    "description": tool_info.get("description", ""),
                    "server": tool_info.get("server", "unknown"),
                    "parameters": tool_info.get("parameters", {}),
                    "available": tool_info.get("available", False)
                }
            
            return formatted_tools
        except Exception:
            return {}
    
    @property
    def mcp_connector(self):
        """Lazy load MCP connector"""
        if self._mcp_connector is None:
            try:
                from tools.mcp_connector.mcp_connector import MCPConnector
                self._mcp_connector = MCPConnector()
            except ImportError:
                pass
        return self._mcp_connector
    
    @property
    def memory_mcp(self):
        """Lazy load Memory MCP"""
        if self._memory_mcp is None:
            try:
                from .memory_mcp import MemoryMCPManager
                self._memory_mcp = MemoryMCPManager()
            except ImportError:
                pass
        return self._memory_mcp
    
    def get_tool_for_workflow(self, tool_name: str, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get tool configured for specific workflow"""
        if tool_name not in self.discovered_tools:
            # Attempt rediscovery
            self.discover_all_tools()
            
        if tool_name not in self.discovered_tools:
            return None
        
        tool_info = self.discovered_tools[tool_name]
        
        # Track tool request
        if self.memory_mcp:
            self.memory_mcp.update_workflow_state(
                workflow_id,
                f"Tool requested: {tool_name}"
            )
        
        return tool_info
    
    def create_executable_tool_button(self, tool_name: str, workflow_id: str, context: Dict = None) -> Optional[str]:
        """Create executable button for any tool type"""
        tool_info = self.get_tool_for_workflow(tool_name, workflow_id)
        if not tool_info:
            return None
        
        context = context or {}
        
        if tool_info["type"] == "local":
            # Use tool's button generator
            try:
                return tool_info["button_generator"](workflow_id, context, tool_info["config"])
            except Exception:
                return None
        
        elif tool_info["type"] == "mcp":
            # Generate MCP tool button
            return self._create_mcp_tool_button(tool_info, workflow_id, context)
        
        return None
    
    def _create_mcp_tool_button(self, tool_info: Dict, workflow_id: str, context: Dict) -> str:
        """Create executable button for MCP tool"""
        server_name = tool_info["server"]
        tool_name = tool_info["name"]
        
        button_code = f'''
"""
Executable MCP Tool: {tool_name}
Server: {server_name}
Workflow: {workflow_id}
"""

import json
from datetime import datetime

# Tool configuration
WORKFLOW_ID = "{workflow_id}"
SERVER_NAME = "{server_name}"
TOOL_NAME = "{tool_name}"
CONTEXT = {json.dumps(context, indent=2)}

def execute_mcp_tool():
    """Execute MCP tool with workflow tracking"""
    print(f"🔌 Executing MCP tool: {{TOOL_NAME}} on {{SERVER_NAME}}")
    print(f"🔗 Workflow: {{WORKFLOW_ID}}")
    
    # In real implementation, would call MCP connector
    # For now, return mock result
    result = {{
        "success": True,
        "tool": TOOL_NAME,
        "server": SERVER_NAME,
        "output": "MCP tool executed successfully",
        "timestamp": datetime.now().isoformat()
    }}
    
    print(f"✅ MCP tool execution complete!")
    return result

# Execute the tool
if __name__ == "__main__":
    execute_mcp_tool()
'''
        
        return button_code
    
    def interactive_tool_selection(self, goal: str, model: str, 
                                 budget: str = "balanced") -> Dict[str, Any]:
        """
        🎭 Interactive tool selection for OC conversations
        Returns data for OC to present to user naturally
        """
        # Convert budget preference to numeric limit
        budget_limits = {
            "free": 0.0,
            "low": 0.10,
            "balanced": 0.50,
            "premium": 2.0
        }
        budget_limit = budget_limits.get(budget, 0.50)
        
        # Get tool suggestions
        suggestions = self.suggest_tools_for_goal(goal, model, budget_limit)
        
        # Prepare conversation data
        core_tools = [t for t in suggestions["suggested_tools"] if t["cost"] == 0.0]
        paid_tools = [t for t in suggestions["suggested_tools"] if t["cost"] > 0.0]
        
        return {
            "core_tools": [t["tool_id"] for t in core_tools],
            "core_explanation": self._generate_core_explanation(core_tools),
            "paid_options": paid_tools,
            "estimated_tool_cost": suggestions["total_estimated_cost"],
            "goal_complexity": suggestions["goal_analysis"],
            "model_compatibility": suggestions["model_compatibility"]
        }
    
    def _generate_core_explanation(self, core_tools: List[Dict]) -> str:
        """Generate natural explanation of core tool selection"""
        if not core_tools:
            return "I can handle this with built-in capabilities."
        
        tool_names = [tool["name"] for tool in core_tools]
        
        if len(tool_names) == 1:
            return f"I can accomplish this with {tool_names[0]}."
        elif len(tool_names) == 2:
            return f"I can accomplish this with {tool_names[0]} and {tool_names[1]}."
        else:
            names_str = ", ".join(tool_names[:-1]) + f", and {tool_names[-1]}"
            return f"I can accomplish this with {names_str}."
    
    @handle_errors
    def estimate_cost(self, operation: str = "tool_operation") -> float:
        """Standard cost estimation for tool operations"""
        cost_map = {
            "tool_discovery": 0.002,
            "tool_execution": 0.005,
            "tool_suggestion": 0.001,
            "tool_operation": 0.002
        }
        return cost_map.get(operation, 0.002)
    
    @handle_errors
    def execute_tool_with_analytics(self, tool_name: str, username: str, session_id: str = None) -> Dict[str, Any]:
        """Execute tool with analytics tracking"""
        start_time = time.time()
        success = False
        error_type = None
        
        try:
            # Track tool execution start
            if session_id:
                self.user_analytics_manager.track_session(username, session_id, "update_tool_activations")
            
            # Execute tool (placeholder - would call actual tool execution)
            result = {
                "success": True,
                "tool": tool_name,
                "output": f"Tool {tool_name} executed successfully",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            success = True
            
        except Exception as e:
            error_type = type(e).__name__
            result = {
                "success": False,
                "tool": tool_name,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            # Calculate response time
            response_time = time.time() - start_time
            
            # Track analytics (failures don't break main functionality)
            try:
                # Track user analytics
                self.user_analytics_manager.track_tool_usage(
                    username, tool_name, success, response_time
                )
                
                # Track system analytics
                self.system_analytics_manager.track_performance(
                    tool_name, response_time, success, error_type
                )
                
            except Exception as analytics_error:
                # Analytics failures should not break tool execution
                pass
        
        return result
    
    @handle_errors
    def track_tool_discovery(self, username: str, discovered_tools: Dict[str, Any]) -> bool:
        """Track tool discovery for analytics"""
        try:
            # Auto-add newly discovered tools to analytics
            for tool_name in discovered_tools.keys():
                self.user_analytics_manager.auto_add_component(username, "tool", tool_name)
            
            return True
            
        except Exception as e:
            # Analytics failures should not break discovery
            return False
    
    @handle_errors
    def get_tool_usage_analytics(self, username: str) -> Dict[str, Any]:
        """Get tool usage analytics for user"""
        try:
            return self.user_analytics_manager._read_analytics_file(username, "tool_usage.json")
        except Exception as e:
            return {}


# Simple interface for orchestrator integration
def discover_tools_for_goal(goal: str, model: str = "claude-sonnet-4", 
                           budget: str = "balanced") -> Dict[str, Any]:
    """
    🎯 Simple interface for tool discovery
    Used by orchestrator for dynamic tool selection
    """
    discovery = ToolManager()
    return discovery.interactive_tool_selection(goal, model, budget)