"""
Chat CLI Command - Core Logic
Jump to main application with message passthrough via conversation bridge
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="chat", return_dict=True)
@retry_with_backoff(max_retries=2, base_delay=1.0)
def execute_chat(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main chat command execution with caching and error handling.
    
    Args:
        params: Command parameters including message content
        
    Returns:
        Standardized result dictionary with conversation bridge results
    """
    # Validate message parameter
    if not params or not params.get("message"):
        return {
            "success": False,
            "error": "Chat command requires a message parameter",
            "timestamp": datetime.now().isoformat()
        }
    
    # Check cache first for similar message patterns
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "chat")
    if cached_result:
        cached_data = json.loads(cached_result)
        # Update timestamp but keep cached workflow analysis
        cached_data["timestamp"] = datetime.now().isoformat()
        cached_data["from_cache"] = True
        return cached_data
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result for 5 minutes (active conversation patterns)
    if result.get("success"):
        cache.cache_content_analysis(cache_key, json.dumps(result), "chat")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure via conversation bridge.
    """
    if not params:
        return 0.002  # Base cost for simple message
    
    # Use conversation bridge cost estimation
    try:
        from orchestrator.conversation_bridge import ConversationToWorkflowBridge
        bridge = ConversationToWorkflowBridge()
        
        # Estimate complexity based on message length and content
        message = params.get("message", "")
        message_length = len(message.split())
        
        # Determine goal complexity
        goal_complexity = "low"
        if message_length > 50:
            goal_complexity = "high"
        elif message_length > 20:
            goal_complexity = "medium"
        
        bridge_params = {
            "goal_complexity": goal_complexity,
            "num_phases": 2,  # Typical workflow phases
        }
        
        return bridge.estimate_cost(bridge_params)
        
    except Exception:
        # Fallback cost estimation
        message_length = len(params.get("message", "").split())
        if message_length > 50:
            return 0.005  # Complex message
        elif message_length > 20:
            return 0.003  # Medium message
        else:
            return 0.002  # Simple message

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including message pattern analysis"""
    message = params.get("message", "") if params else ""
    
    # Create pattern-based key rather than exact message for privacy
    message_words = message.lower().split()
    message_length = len(message_words)
    
    # Extract key patterns for similar message detection
    key_patterns = []
    common_goal_words = ["create", "build", "analyze", "research", "design", "write", "plan", "develop"]
    for word in common_goal_words:
        if word in message_words:
            key_patterns.append(word)
    
    # Build cache key from patterns rather than content
    pattern_key = f"chat|len:{message_length}|patterns:{sorted(key_patterns)}"
    
    return hashlib.md5(pattern_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core chat command logic implementation"""
    try:
        message = params.get("message", "")
        
        # Initialize conversation bridge
        from orchestrator.conversation_bridge import ConversationToWorkflowBridge
        bridge = ConversationToWorkflowBridge()
        
        # Create workflow from conversation
        workflow_result = bridge.create_workflow_from_conversation(message)
        
        if workflow_result.get("success"):
            return {
                "success": True,
                "message": "Successfully created workflow from message",
                "workflow_id": workflow_result.get("workflow_id"),
                "custom_command": workflow_result.get("custom_command"),
                "use_case_directory": workflow_result.get("use_case_directory"),
                "config_path": workflow_result.get("config_path"),
                "ready_to_execute": workflow_result.get("ready_to_execute", False),
                "original_message": message,
                "bridge_output": workflow_result.get("setup_output", ""),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"Conversation bridge failed: {workflow_result.get('error', 'Unknown error')}",
                "workflow_id": workflow_result.get("workflow_id"),
                "original_message": message,
                "bridge_stderr": workflow_result.get("setup_stderr", ""),
                "timestamp": datetime.now().isoformat()
            }
            
    except ImportError as e:
        return {
            "success": False,
            "error": f"Conversation bridge not available: {str(e)}",
            "original_message": params.get("message", ""),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Chat command execution failed: {str(e)}",
            "original_message": params.get("message", ""),
            "timestamp": datetime.now().isoformat()
        }

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_chat(params)