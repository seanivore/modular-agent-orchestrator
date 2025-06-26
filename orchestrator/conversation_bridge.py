"""
Conversation to Workflow Bridge -
Converts natural language goals into executable custom commands 
"""

import os
import json
import subprocess
import re
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from .cache.cache_system import CacheManager
from .error_handling import handle_errors, retry_with_backoff, APIError


class ConversationToWorkflowBridge:
    """Convert conversations to executable workflows using proven SFA patterns"""
    
    def __init__(self):
        from .memory_mcp import MemoryMCPManager
        
        # Standard cache instance
        self.cache = CacheManager()
        
        self.memory_mcp = MemoryMCPManager()
        self.setup_script_path = "scripts/setup_workflow.sh"  # ONE setup script
        self.use_case_base = "configs/use_case"
        
        # Ensure use-case directory exists
        os.makedirs(self.use_case_base, exist_ok=True)
    
    def estimate_cost(self, params: Dict[str, Any]) -> float:
        """Estimate operation cost for budget planning"""
        # Conversation bridge operations include analysis and setup
        base_cost = 0.0
        
        # Add cost for goal analysis
        goal_complexity = params.get("goal_complexity", "medium")
        if goal_complexity == "low":
            base_cost += 0.001
        elif goal_complexity == "medium":
            base_cost += 0.002
        else:  # high
            base_cost += 0.005
        
        # Add cost for config generation and setup
        num_phases = params.get("num_phases", 2)
        base_cost += num_phases * 0.001  # $0.001 per phase configuration
        
        # Add cost for script execution
        base_cost += 0.001  # Setup script execution
        
        return base_cost
    
    @handle_errors(operation_name="create_workflow_from_conversation", return_dict=True)
    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError, subprocess.CalledProcessError))
    def create_workflow_from_conversation(self, user_goal: str) -> Dict[str, Any]:
        """Convert conversation to executable workflow following SFA pattern"""
        workflow_id = f"workflow-{uuid4().hex[:8]}"
        
        # Check cache for similar goal analysis
        cache_key = f"goal_analysis|{user_goal[:50]}"  # First 50 chars for caching
        cached_result = self.cache.get_cached_analysis(cache_key, "goal_analysis")
        if cached_result:
            cached_data = json.loads(cached_result)
            # Use cached analysis but generate new workflow ID
            workflow_spec = cached_data["workflow_spec"]
        else:
            # Analyze goal and extract requirements (no hardcoded categories)
            workflow_spec = self._analyze_goal(user_goal)
            # Cache the analysis
            self.cache.cache_content_analysis(cache_key, json.dumps({"workflow_spec": workflow_spec}), "goal_analysis")
        
        try:
            # Create workflow entity in Memory MCP
            self.memory_mcp.create_workflow_context(workflow_id, user_goal)
            
            # Generate JSON config (same format humans create)
            config = {
                "workflow_id": workflow_id,
                "custom_command": self._generate_command_name(workflow_spec, user_goal),
                "goal": user_goal,
                "phases": self._design_phases(workflow_spec),
                "variables": self._extract_variables(workflow_spec, user_goal)
            }
            
            # Save config to use-case directory
            command_name = config["custom_command"].replace(" ", "-")
            use_case_dir = f"{self.use_case_base}/{command_name}"
            os.makedirs(use_case_dir, exist_ok=True)
            
            config_path = f"{use_case_dir}/config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Run the SAME setup script humans use
            result = subprocess.run([
                self.setup_script_path, 
                config_path
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                # Track success in Memory MCP
                self.memory_mcp.update_workflow_state(
                    workflow_id,
                    f"Custom command created: {config['custom_command']}"
                )
                
                return {
                    "success": True,
                    "workflow_id": workflow_id,
                    "custom_command": config["custom_command"],
                    "use_case_directory": use_case_dir,
                    "config_path": config_path,
                    "setup_output": result.stdout,
                    "ready_to_execute": True
                }
            else:
                # Track failure in Memory MCP
                error_msg = f"Setup script failed: {result.stderr}"
                self.memory_mcp.update_workflow_state(workflow_id, error_msg)
                
                return {
                    "success": False,
                    "error": error_msg,
                    "workflow_id": workflow_id,
                    "config_path": config_path,
                    "setup_stderr": result.stderr
                }
                
        except Exception as e:
            # Track exception in Memory MCP
            error_msg = f"Conversation bridge error: {str(e)}"
            self.memory_mcp.update_workflow_state(workflow_id, error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "workflow_id": workflow_id
            }
    
    @handle_errors(operation_name="analyze_goal", return_dict=True)
    def _analyze_goal(self, user_goal: str) -> Dict[str, Any]:
        """Extract workflow requirements from goal (no hardcoded categories)"""
        goal_lower = user_goal.lower()
        
        # Simple goal analysis based on keywords and patterns
        analysis = {
            "complexity": "medium",  # Default
            "domain": "general",     # Default
            "required_tools": [],
            "suggested_phases": [],
            "task_types": []
        }
        
        # Detect complexity based on goal language
        if any(word in goal_lower for word in ["simple", "quick", "basic", "just"]):
            analysis["complexity"] = "low"
        elif any(word in goal_lower for word in ["comprehensive", "detailed", "thorough", "complete", "full"]):
            analysis["complexity"] = "high"
        
        # Detect likely required tools based on goal content
        tool_indicators = {
            "web_search": ["research", "find", "search", "investigate", "analyze", "competitors", "market"],
            "text_editor": ["write", "create", "document", "report", "content", "strategy", "plan"],
            "think": ["analyze", "plan", "strategy", "recommend", "evaluate", "assess"],
            "graphic_design": ["design", "visual", "logo", "brand", "graphics", "images"],
            "dalle_generate": ["generate", "create images", "illustrations", "visual content"]
        }
        
        for tool, keywords in tool_indicators.items():
            if any(keyword in goal_lower for keyword in keywords):
                analysis["required_tools"].append(tool)
        
        # Default tools if none detected
        if not analysis["required_tools"]:
            analysis["required_tools"] = ["think", "text_editor"]
        
        # Detect domain based on keywords
        domain_keywords = {
            "business": ["business", "strategy", "marketing", "sales", "company", "startup"],
            "technology": ["tech", "software", "ai", "programming", "development", "app"],
            "creative": ["creative", "design", "content", "brand", "art", "visual"],
            "research": ["research", "analysis", "study", "investigate", "data"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in goal_lower for keyword in keywords):
                analysis["domain"] = domain
                break
        
        return analysis
    
    def _generate_command_name(self, workflow_spec: Dict[str, Any], user_goal: str) -> str:
        """Generate natural language command name (spaces, not hyphens)"""
        goal_lower = user_goal.lower()
        
        # Extract key concepts from goal
        key_words = []
        
        # Look for action words
        action_words = ["create", "build", "develop", "analyze", "research", "design", "write", "plan"]
        for action in action_words:
            if action in goal_lower:
                key_words.append(action)
                break
        
        # Look for subject matter
        subject_patterns = [
            r"(marketing|content|business|competitive?)\s+(strategy|plan|analysis)",
            r"(website|app|software|tool|platform)",
            r"(logo|brand|design|visual)",
            r"(research|analysis|study)",
            r"(startup|company|business)"
        ]
        
        for pattern in subject_patterns:
            matches = re.findall(pattern, goal_lower)
            if matches:
                for match in matches[0] if isinstance(matches[0], tuple) else [matches[0]]:
                    if match and match not in key_words:
                        key_words.append(match)
        
        # Clean up and limit to 3-4 words
        key_words = [word for word in key_words if len(word) > 2][:4]
        
        # If we didn't extract enough, use fallback
        if len(key_words) < 2:
            domain = workflow_spec.get("domain", "general")
            if domain != "general":
                key_words = ["create", domain, "workflow"]
            else:
                key_words = ["custom", "workflow"]
        
        return " ".join(key_words)
    
    def _design_phases(self, workflow_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design workflow phases based on goal analysis (no hardcoded assumptions)"""
        complexity = workflow_spec.get("complexity", "medium")
        required_tools = workflow_spec.get("required_tools", ["think", "text_editor"])
        domain = workflow_spec.get("domain", "general")
        
        phases = []
        
        # Simple workflows: 1-2 phases
        if complexity == "low":
            phases.append({
                "name": "execution",
                "description": "Execute the requested task",
                "tools": required_tools,
                "deliverable": "Completed task output",
                "model": "claude-sonnet-4"
            })
        
        # Medium complexity: 2-3 phases
        elif complexity == "medium":
            # Research phase if web tools needed
            if any(tool in required_tools for tool in ["web_search", "perplexity_search"]):
                phases.append({
                    "name": "research",
                    "description": "Research and gather information",
                    "tools": [tool for tool in required_tools if "search" in tool] + ["text_editor"],
                    "deliverable": "Research findings",
                    "model": "claude-sonnet-4"
                })
            
            # Analysis/Strategy phase
            phases.append({
                "name": "analysis",
                "description": "Analyze information and develop approach",
                "tools": ["think", "text_editor"],
                "deliverable": "Analysis and strategy",
                "model": "claude-sonnet-4"
            })
            
            # Creation phase if creative tools needed
            if any(tool in required_tools for tool in ["graphic_design", "dalle_generate"]):
                phases.append({
                    "name": "creation",
                    "description": "Create final deliverables",
                    "tools": [tool for tool in required_tools if tool in ["graphic_design", "dalle_generate", "text_editor"]],
                    "deliverable": "Final creative outputs",
                    "model": "claude-sonnet-4"
                })
        
        # High complexity: 3-4 phases
        else:  # complexity == "high"
            phases.extend([
                {
                    "name": "research",
                    "description": "Comprehensive research and information gathering",
                    "tools": [tool for tool in required_tools if "search" in tool] + ["text_editor"],
                    "deliverable": "Detailed research report",
                    "model": "claude-sonnet-4"
                },
                {
                    "name": "analysis",
                    "description": "Deep analysis and strategic planning",
                    "tools": ["think", "text_editor"],
                    "deliverable": "Strategic analysis",
                    "model": "claude-sonnet-4"
                },
                {
                    "name": "development",
                    "description": "Develop comprehensive solution",
                    "tools": required_tools,
                    "deliverable": "Solution framework",
                    "model": "claude-sonnet-4"
                },
                {
                    "name": "finalization",
                    "description": "Finalize and polish deliverables",
                    "tools": ["text_editor"] + [tool for tool in required_tools if tool in ["graphic_design", "dalle_generate"]],
                    "deliverable": "Final polished outputs",
                    "model": "claude-sonnet-4"
                }
            ])
        
        return phases
    
    def _extract_variables(self, workflow_spec: Dict[str, Any], user_goal: str) -> Dict[str, Any]:
        """Extract required and optional variables from goal (flexible, not hardcoded)"""
        variables = {
            "required": {},
            "optional": {}
        }
        
        domain = workflow_spec.get("domain", "general")
        goal_lower = user_goal.lower()
        
        # Domain-specific variable suggestions (not hardcoded requirements)
        if domain == "business":
            if "startup" in goal_lower or "company" in goal_lower:
                variables["optional"]["company_stage"] = {
                    "description": "Company stage or size",
                    "default": "startup"
                }
            if "target" in goal_lower or "audience" in goal_lower:
                variables["optional"]["target_audience"] = {
                    "description": "Target audience or market",
                    "default": "not specified"
                }
        
        elif domain == "creative":
            if "brand" in goal_lower or "logo" in goal_lower:
                variables["optional"]["brand_style"] = {
                    "description": "Brand style or aesthetic preferences",
                    "default": "modern and professional"
                }
        
        # Always include budget as optional
        variables["optional"]["budget"] = {
            "description": "Budget constraints or preferences",
            "default": "not specified"
        }
        
        # Timeline is often useful
        variables["optional"]["timeline"] = {
            "description": "Timeline or deadline requirements",
            "default": "standard timeline"
        }
        
        return variables


# Example usage and testing functions
def test_conversation_bridge():
    """Test the conversation bridge with sample goals"""
    bridge = ConversationToWorkflowBridge()
    
    test_goals = [
        "Create a marketing strategy for my B2B startup",
        "Research competitors in the project management space",
        "Design a logo and brand identity for my company",
        "Write a comprehensive business plan"
    ]
    
    for goal in test_goals:
        print(f"\n🎯 Testing goal: {goal}")
        result = bridge.create_workflow_from_conversation(goal)
        
        if result["success"]:
            print(f"✅ Created command: {result['custom_command']}")
            print(f"📁 Directory: {result['use_case_directory']}")
        else:
            print(f"❌ Failed: {result['error']}")


if __name__ == "__main__":
    # Run tests if executed directly
    test_conversation_bridge()