#!/usr/bin/env python3
"""
Universal Model Manager
Loads JSON configs and provides intelligent model selection
"""

# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError, ValidationError

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

# Standard cache instance
cache = CacheManager()


@dataclass
class ModelCapabilities:
    """Model capabilities loaded from JSON"""
    tools: bool = False
    vision: bool = False
    caching: bool = False
    parallel_tools: bool = False
    extended_thinking: bool = False
    code_execution: bool = False
    files_api: bool = False
    image_generation: bool = False


@dataclass
class ModelConfig:
    """Complete model configuration"""
    name: str
    provider: str
    display_name: str
    model_id: str
    context_window: int
    max_output: int
    input_price: float
    output_price: float
    capabilities: ModelCapabilities
    safe_token_limit: int
    optimal_use_cases: List[str]
    image_input_price: Optional[float] = None  # 🆕 For vision models
    image_output_price: Optional[float] = None  # 🆕 For vision models
    privacy_note: Optional[str] = None


@dataclass
class ProviderConfig:
    """Provider configuration"""
    name: str
    display_name: str
    api_type: str
    base_url: str
    auth_header: Optional[str]
    env_var: Optional[str]
    supports_streaming: bool
    supports_caching: bool
    rate_limits: Dict[str, int]
    description: str


class ModelManager:
    """
    The brain of v4! 🧠
    Loads JSON configs and provides intelligent model selection
    """
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.models: Dict[str, ModelConfig] = {}
        self.providers: Dict[str, ProviderConfig] = {}
        self.fallback_chains: Dict[str, List[str]] = {}
        
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all JSON configurations"""
        try:
            self._load_models_config()
            self._load_providers_config()
            # Return success info for UI layer to display
            return {
                "status": "success",
                "models_loaded": len(self.models),
                "providers_loaded": len(self.providers)
            }
        except Exception as e:
            # Return error info for UI layer to display
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def _load_models_config(self):
        """Load models from JSON config"""
        models_path = self.config_dir / "models.json"
        
        with open(models_path, 'r') as f:
            data = json.load(f)
        
        for name, config in data["models"].items():
            capabilities = ModelCapabilities(**config.get("capabilities", {}))
            
            self.models[name] = ModelConfig(
                name=name,
                provider=config["provider"],
                display_name=config["display_name"],
                model_id=config["model_id"],
                context_window=config["context_window"],
                max_output=config["max_output"],
                input_price=config["input_price_per_million"],
                output_price=config["output_price_per_million"],
                capabilities=capabilities,
                safe_token_limit=config["safe_token_limit"],
                optimal_use_cases=config["optimal_use_cases"],
                image_input_price=config.get("image_input_price_per_million"),  # 🆕 NEW!
                image_output_price=config.get("image_output_price_per_million"),  # 🆕 NEW!
                privacy_note=config.get("privacy_note")
            )
    
    def _load_providers_config(self):
        """Load providers from JSON config"""
        providers_path = self.config_dir / "providers.json"
        
        with open(providers_path, 'r') as f:
            data = json.load(f)
        
        # Load providers
        for name, config in data["providers"].items():
            self.providers[name] = ProviderConfig(
                name=name,
                display_name=config["display_name"],
                api_type=config["api_type"],
                base_url=config["base_url"],
                auth_header=config.get("auth_header"),
                env_var=config.get("env_var"),
                supports_streaming=config["supports_streaming"],
                supports_caching=config["supports_caching"],
                rate_limits=config["rate_limits"],
                description=config["description"]
            )
        
        # Load fallback chains
        self.fallback_chains = data.get("fallback_chains", {})
    
    def get_best_model_for_task(self, task_description: str = None, preferences: Optional[Dict] = None) -> Optional[str]:
        """
        🎯 TRULY DYNAMIC MODEL SELECTION!
        Selects optimal model based on preferences and requirements - NO hardcoded categories!
        """
        preferences = preferences or {}
        
        # Start with all available models
        candidate_models = list(self.models.values())
        
        # Apply hard requirements first (these eliminate models)
        if preferences.get("requires_tools", False):
            candidate_models = [m for m in candidate_models if m.capabilities.tools]
        
        if preferences.get("requires_vision", False):
            candidate_models = [m for m in candidate_models if m.capabilities.vision]
        
        if preferences.get("requires_caching", False):
            candidate_models = [m for m in candidate_models if m.capabilities.caching]
        
        if preferences.get("requires_code_execution", False):
            candidate_models = [m for m in candidate_models if m.capabilities.code_execution]
        
        if preferences.get("free_only", False):
            candidate_models = [m for m in candidate_models if m.input_price == 0.0]
        
        if preferences.get("privacy_focused", False):
            candidate_models = [m for m in candidate_models if m.privacy_note]
        
        # Check if task description matches any optimal use cases
        if task_description:
            matching_models = [
                model for model in candidate_models
                if any(use_case.lower() in task_description.lower() for use_case in model.optimal_use_cases)
            ]
            if matching_models:
                candidate_models = matching_models
        
        if not candidate_models:
            return None
        
        # Dynamic selection based on preferences (no hardcoded task types!)
        selection_strategy = preferences.get("selection_strategy", "balanced")
        
        if selection_strategy == "cheapest":
            return min(candidate_models, key=lambda m: m.input_price).name
        
        elif selection_strategy == "fastest":
            # Prefer models with smaller context windows (typically faster)
            return min(candidate_models, key=lambda m: m.context_window).name
        
        elif selection_strategy == "highest_quality":
            # Prefer models with highest output limits and advanced capabilities
            return max(candidate_models, key=lambda m: (
                m.max_output,
                m.capabilities.extended_thinking,
                m.capabilities.parallel_tools
            )).name
        
        elif selection_strategy == "largest_context":
            return max(candidate_models, key=lambda m: m.context_window).name
        
        else:  # "balanced" - default strategy
            # Smart balanced selection: prefer models with tools, good context, reasonable price
            scored_models = []
            for model in candidate_models:
                score = 0
                
                # Capability bonuses
                if model.capabilities.tools: score += 10
                if model.capabilities.vision: score += 5
                if model.capabilities.caching: score += 3
                if model.capabilities.extended_thinking: score += 5
                
                # Context window bonus (normalized)
                score += min(model.context_window / 10000, 10)
                
                # Price penalty (lower is better)
                if model.input_price > 0:
                    score -= min(model.input_price * 10, 15)
                else:
                    score += 5  # Free model bonus
                
                scored_models.append((score, model))
            
            # Return highest scoring model
            return max(scored_models, key=lambda x: x[0])[1].name
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """Get complete configuration for a model"""
        return self.models.get(model_name)
    
    def get_provider_config(self, provider_name: str) -> Optional[ProviderConfig]:
        """Get provider configuration"""
        return self.providers.get(provider_name)
    
    def get_provider_for_model(self, model_name: str) -> Optional[ProviderConfig]:
        """Get the provider configuration for a specific model"""
        model = self.get_model_config(model_name)
        if not model:
            return None
        return self.get_provider_config(model.provider)
    
    def estimate_cost(self, model_name: str, input_tokens: int, output_tokens: int, image_tokens: int = 0) -> float:
        """Calculate estimated cost for a model and token usage"""
        model = self.get_model_config(model_name)
        if not model:
            return 0.0
        
        # Regular text tokens
        input_cost = (input_tokens / 1_000_000) * model.input_price
        output_cost = (output_tokens / 1_000_000) * model.output_price
        
        # Image tokens (if applicable)
        image_cost = 0.0
        if image_tokens > 0 and model.image_input_price:
            image_cost = (image_tokens / 1_000_000) * model.image_input_price
        
        return input_cost + output_cost + image_cost
    
    def get_fallback_chain(self, strategy_key: str) -> List[str]:
        """Get fallback provider chain for strategy or requirement key"""
        return self.fallback_chains.get(strategy_key, ["anthropic-direct", "requesty"])
    
    def list_models_by_capability(self, capability: str) -> List[str]:
        """List all models that support a specific capability"""
        return [
            name for name, model in self.models.items()
            if getattr(model.capabilities, capability, False)
        ]
    
    def list_free_models(self) -> List[str]:
        """List all free models"""
        return [
            name for name, model in self.models.items()
            if model.input_price == 0.0
        ]
    
    def get_dynamic_model_recommendation(self, goal: str, preferences: Optional[Dict] = None) -> Dict[str, Any]:
        """
        🚀 DYNAMIC MODEL RECOMMENDATION!
        Analyzes goal and recommends model based on detected requirements - NO hardcoded categories!
        """
        preferences = preferences or {}
        
        # Analyze goal to detect requirements dynamically
        detected_requirements = {}
        goal_lower = goal.lower()
        
        # Detect capability requirements from goal text
        if any(word in goal_lower for word in ["image", "photo", "visual", "picture", "analyze image", "see"]):
            detected_requirements["requires_vision"] = True
        
        if any(word in goal_lower for word in ["search", "web", "browse", "find", "lookup"]):
            detected_requirements["requires_tools"] = True
        
        if any(word in goal_lower for word in ["code", "program", "script", "function", "debug"]):
            detected_requirements["requires_code_execution"] = True
        
        # Detect preference hints from goal text
        if any(word in goal_lower for word in ["quick", "fast", "rapid", "immediate"]):
            detected_requirements["selection_strategy"] = "fastest"
        elif any(word in goal_lower for word in ["best", "high quality", "excellent", "premium"]):
            detected_requirements["selection_strategy"] = "highest_quality"
        elif any(word in goal_lower for word in ["cheap", "free", "budget", "cost-effective"]):
            detected_requirements["selection_strategy"] = "cheapest"
        elif any(word in goal_lower for word in ["long", "detailed", "comprehensive", "extensive"]):
            detected_requirements["selection_strategy"] = "largest_context"
        
        # Merge detected requirements with user preferences (user preferences take priority)
        final_preferences = {**detected_requirements, **preferences}
        
        # Get recommendation
        recommended_model = self.get_best_model_for_task(goal, final_preferences)
        
        return {
            "recommended_model": recommended_model,
            "detected_requirements": detected_requirements,
            "final_preferences": final_preferences,
            "goal_analysis": {
                "requires_vision": detected_requirements.get("requires_vision", False),
                "requires_tools": detected_requirements.get("requires_tools", False),
                "requires_code": detected_requirements.get("requires_code_execution", False),
                "strategy": detected_requirements.get("selection_strategy", "balanced")
            }
        }
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """Get all available models in a format suitable for CLI display"""
        models_data = {}
        for name, model_config in self.models.items():
            models_data[name] = {
                "name": model_config.name,
                "display_name": model_config.display_name,
                "provider": model_config.provider,
                "description": f"{model_config.display_name} - {model_config.provider} model",
                "capabilities": [
                    cap for cap, enabled in model_config.capabilities.__dict__.items() 
                    if enabled
                ],
                "cost_estimate": model_config.input_price,
                "context_window": model_config.context_window,
                "max_tokens": model_config.max_output
            }
        return models_data
    
    def health_check(self) -> Dict[str, bool]:
        """Check if all configured providers are accessible"""
        # TODO: Implement actual API health checks
        return {name: True for name in self.providers.keys()}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about available models and providers"""
        return {
            "total_models": len(self.models),
            "total_providers": len(self.providers),
            "free_models": len(self.list_free_models()),
            "models_with_tools": len(self.list_models_by_capability("tools")),
            "models_with_vision": len(self.list_models_by_capability("vision")),
            "models_with_caching": len(self.list_models_by_capability("caching")),
            "claude_4_models": len([m for m in self.models if "sonnet-4" in m or "opus-4" in m]),
        }


# Example usage and testing (DEVELOPMENT ONLY - UI layer handles display in production)
if __name__ == "__main__":
    # Test the model manager
    manager = ModelManager()
    
    print(r"\n🎯 Dynamic Model Selection Examples:")
    print(f"Balanced selection: {manager.get_best_model_for_task()}")
    print(f"Cheapest option: {manager.get_best_model_for_task(preferences={'selection_strategy': 'cheapest'})}")
    print(f"Highest quality: {manager.get_best_model_for_task(preferences={'selection_strategy': 'highest_quality'})}")
    print(f"Vision required: {manager.get_best_model_for_task(preferences={'requires_vision': True})}")
    
    print(r"\n💰 Cost Examples:")
    balanced_model = manager.get_best_model_for_task()
    print(f"Cost for 1000 input, 500 output tokens with {balanced_model}: ${manager.estimate_cost(balanced_model, 1000, 500):.6f}")
    
    print(r"\n📊 Stats:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print(r"\n🚀 Dynamic Goal Analysis:")
    goal = "Research renewable energy trends and create a marketing strategy with images"
    recommendation = manager.get_dynamic_model_recommendation(goal)
    print(f"Goal: {goal}")
    print(f"Recommended model: {recommendation['recommended_model']}")
    print(f"Detected requirements: {recommendation['detected_requirements']}")
    print(f"Goal analysis: {recommendation['goal_analysis']}")


# ========================================================================
# STANDALONE FUNCTIONS FOR BUTTON IMPORTS
# ========================================================================

def standalone_model_selection(params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for button file imports - model selection"""
    manager = ModelManager()
    task_description = params.get("task_description")
    preferences = params.get("preferences", {})
    
    selected_model = manager.get_best_model_for_task(task_description, preferences)
    
    return {
        "selected_model": selected_model,
        "task_description": task_description,
        "preferences": preferences
    }


def standalone_model_recommendation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for button file imports - goal-based recommendation"""
    manager = ModelManager()
    goal = params.get("goal", "")
    preferences = params.get("preferences", {})
    
    return manager.get_dynamic_model_recommendation(goal, preferences)


def standalone_cost_estimation(params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function for button file imports - cost estimation"""
    manager = ModelManager()
    model_name = params.get("model_name")
    input_tokens = params.get("input_tokens", 0)
    output_tokens = params.get("output_tokens", 0)
    image_tokens = params.get("image_tokens", 0)
    
    if not model_name:
        return {"error": "model_name is required", "cost": 0.0}
    
    cost = manager.estimate_cost(model_name, input_tokens, output_tokens, image_tokens)
    
    return {
        "model_name": model_name,
        "estimated_cost": cost,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "image_tokens": image_tokens
    }


def estimate_cost(params: Dict[str, Any] = None) -> float:
    """REQUIRED: Standard MAO estimate_cost function signature"""
    if not params:
        return 0.001  # Base operation cost
    
    # Use internal cost estimation if parameters provided
    model_name = params.get("model_name")
    if model_name:
        manager = ModelManager()
        return manager.estimate_cost(
            model_name,
            params.get("input_tokens", 1000),
            params.get("output_tokens", 500),
            params.get("image_tokens", 0)
        )
    
    # Default cost for model management operations
    complexity = params.get("complexity", 1.0)
    return 0.001 * complexity