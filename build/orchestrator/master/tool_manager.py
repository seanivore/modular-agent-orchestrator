"""
Tool Discovery
Dynamic tool suggestion based on goals, not hardcoded categories
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class ToolDiscovery:
    """
    🔍 Dynamic tool discovery without hardcoded specifics
    Suggests tools based on goal analysis, not predefined categories
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.tool_registry = self._load_tool_registry()
        
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


# Simple interface for orchestrator integration
def discover_tools_for_goal(goal: str, model: str = "claude-sonnet-4", 
                           budget: str = "balanced") -> Dict[str, Any]:
    """
    🎯 Simple interface for tool discovery
    Used by orchestrator for dynamic tool selection
    """
    discovery = ToolDiscovery()
    return discovery.interactive_tool_selection(goal, model, budget) 