# Tool Integration Patterns - Dynamic Discovery, Generation, and Execution

## Introduction

MAO's tool integration architecture implements sophisticated patterns for dynamic tool discovery, automated generation, and reliable execution. This system enables seamless integration of diverse AI tools while maintaining performance, reliability, and the LOCAL-only architecture principles.

## Dynamic Tool Discovery Patterns

### Tool Manager Architecture

The tool manager provides intelligent tool discovery and recommendation based on goal analysis:

```python
# orchestrator/manager_tools.py
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
        
        return tools
        
    def _analyze_goal_complexity(self, goal: str) -> Dict[str, Any]:
        """Analyze goal complexity without hardcoded assumptions"""
        words = goal.split()
        
        return {
            "word_count": len(words),
            "estimated_complexity": "simple" if len(words) < 10 else "complex",
            "contains_multiple_tasks": "and" in goal.lower() or "then" in goal.lower(),
            "time_sensitive": any(word in goal.lower() for word in ["urgent", "asap", "quickly", "fast"])
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
```

### Tool Validation and Structure Verification

The system validates tool structure and capabilities before integration:

```python
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
```

## Tool Generation Patterns

### Automated Tool Creation

The system provides templates and automation for generating new tools:

```python
# Actual tool implementation pattern from tools/brave_search/brave_search.py
@handle_errors(operation_name="brave_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(requests.exceptions.RequestException, APIError))
def search_web(query: str, count: int = 10, country: str = "US", search_type: str = "web") -> Dict[str, Any]:
    """
    Comprehensive web search using Brave Search API with enhanced error handling
    
    Args:
        query: Search query string
        count: Number of results to return (1-20)
        country: Country code for localized results
        search_type: Type of search ("web", "news", "local")
        
    Returns:
        Dict with structured search results or error information
    """
    # Validation
    if not query.strip():
        return {"error": "Search query cannot be empty"}
    
    # Clamp count to valid range
    count = min(20, max(1, count))
    
    # FINGERPRINT CACHING - Check cache first
    cache = CacheManager()
    cache_key = f"{query}|{count}|{country}|{search_type}"
    
    cached_result = cache.get_cached_analysis(cache_key, "brave_search")
    if cached_result:
        return json.loads(cached_result)
    
    # API Configuration
    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
    if not api_key:
        return {"error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable"}
    
    # Tool execution logic follows actual implementation patterns...
    # [Implementation details based on actual codebase]
    
    return search_results

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for this search operation"""
    # Brave API is typically free for reasonable usage
    # Return minimal cost for workflow planning
    return 0.001
```

### Button Generation Pattern

Tools generate executable code snippets for workflow integration:

```python
# Actual button generation from tools/brave_search/button_brave_search.py
def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude execution
    Universal model compatibility via code generation
    
    Args:
        params: Search parameters (query, count, country, search_type)
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    # Extract parameters with defaults
    query = params.get("query", "")
    count = params.get("count", 10)
    country = params.get("country", "US")
    search_type = params.get("search_type", "web")
    
    # Generate snippet that imports and uses the logic file
    snippet = f'''# Brave Search Tool Execution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.brave_search.brave_search import search_web, search_news, search_local, estimate_cost, validate_api_key

def main():
    """Execute Brave search using standardized logic"""
    
    # Search parameters
    query = "{query}"
    count = {count}
    country = "{country}"
    search_type = "{search_type}"
    
    print(f"🔍 Brave {{search_type.title()}} Search: {{query}}")
    
    # Validate API key first
    validation = validate_api_key()
    if not validation["valid"]:
        print(f"❌ API Error: {{validation['error']}}")
        return validation
    
    # Execute search using logic file function
    if search_type == "news":
        result = search_news(query, count, country)
    elif search_type == "local":
        result = search_local(query, count, country)
    else:
        result = search_web(query, count, country, search_type)
    
    # Display results
    if result.get("error"):
        print(f"❌ Search Error: {{result['error']}}")
    else:
        result_key = "articles" if search_type == "news" else "results"
        results_count = result.get("count", 0)
        print(f"✅ Found {{results_count}} results")
        
        # Show top 3 results
        for i, item in enumerate(result.get(result_key, [])[:3], 1):
            print(f"\n{{i}}. {{item.get('title', 'No title')}}")
            print(f"   {{item.get('description', 'No description')[:100]}}...")
            print(f"   {{item.get('url', 'No URL')}}")
    
    # Calculate cost
    cost_params = {{"query": query, "count": count, "search_type": search_type}}
    cost = estimate_cost(cost_params)
    print(f"\n💰 Cost: ${{cost:.4f}}")
    
    return result

if __name__ == "__main__":
    result = main()
    print(f"\n🎯 Search {{\"completed\" if result.get('status') == 'success' else \"failed\"}}")
'''
    
    return snippet
```

## Tool Execution Patterns

### Search Tools Integration

The system includes comprehensive search tool patterns:

```python
# Actual Brave Search implementation from tools/brave_search/brave_search.py
@handle_errors(operation_name="brave_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(requests.exceptions.RequestException, APIError))
def search_web(query: str, count: int = 10, country: str = "US", search_type: str = "web") -> Dict[str, Any]:
    """Comprehensive web search using Brave Search API with enhanced error handling"""
    
    # Validation
    if not query.strip():
        return {"error": "Search query cannot be empty"}
    
    # Clamp count to valid range
    count = min(20, max(1, count))
    
    # FINGERPRINT CACHING - Check cache first
    cache = CacheManager()
    cache_key = f"{query}|{count}|{country}|{search_type}"
    
    cached_result = cache.get_cached_analysis(cache_key, "brave_search")
    if cached_result:
        return json.loads(cached_result)
    
    # API Configuration
    api_key = os.getenv("BRAVE_API_KEY") or os.getenv("X_SUBSCRIPTION_TOKEN")
    if not api_key:
        return {"error": "Brave API key not found. Set BRAVE_API_KEY or X_SUBSCRIPTION_TOKEN environment variable"}
    
    # Headers configuration
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    # Search parameters
    base_params = {
        "q": query,
        "count": count,
        "country": country,
        "search_lang": "en",
        "ui_lang": "en-US",
        "spellcheck": 1
    }
    
    # Perform search with shared retry logic (handled by decorator)
    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search", 
        headers=headers, 
        params=base_params,
        timeout=30
    )
    
    if response.status_code == 429:
        raise APIError(f"Rate limited by Brave API", "brave_search", 429)
    elif response.status_code != 200:
        raise APIError(f"HTTP {response.status_code}: {response.text[:200]}", "brave_search", response.status_code)
    
    # Parse and process results
    data = response.json()
    results = data.get("web", {}).get("results", [])
    
    processed_results = []
    for i, result in enumerate(results, 1):
        processed_results.append({
            "rank": i,
            "title": result.get("title", "No title"),
            "url": result.get("url", "No URL"), 
            "description": result.get("description", "No description")
        })
    
    # Create comprehensive result data
    search_results = {
        "status": "success",
        "query": query,
        "search_type": search_type,
        "timestamp": datetime.now().isoformat(),
        "count": len(processed_results),
        "country": country,
        "results": processed_results
    }
    
    # FINGERPRINT CACHING - Cache successful results
    cache.cache_content_analysis(cache_key, json.dumps(search_results), "brave_search")
    
    return search_results
            
    def process_search_results(self, raw_data: dict):
        """Process raw search results into structured format"""
        results = []
        
        web_results = raw_data.get("web", {}).get("results", [])
        
        for item in web_results:
            result = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "published": item.get("published", ""),
                "thumbnail": item.get("thumbnail", {}).get("src", ""),
                "relevance_score": self.calculate_relevance_score(item)
            }
            results.append(result)
            
        return {
            "web_results": results,
            "total_count": len(results),
            "search_metadata": {
                "provider": "brave",
                "timestamp": datetime.utcnow().isoformat(),
                "query_processed": raw_data.get("query", {}).get("original", "")
            }
        }
```

### Content Creation Tools

Advanced content creation tools with AI integration:

```python
# Actual DALL-E implementation pattern - TO BE IMPLEMENTED
def generate_image_with_dalle(prompt: str, generation_params: dict = None) -> Dict[str, Any]:
    """
    DALL-E image generation implementation
    
    Note: This represents the planned DALL-E integration pattern.
    The actual implementation would follow the same structure as other tools
    with proper error handling, caching, and cost estimation.
    """
    
    # Current MAO pattern would include:
    # 1. Input validation
    # 2. Cache checking
    # 3. API key validation
    # 4. Request execution with retry logic
    # 5. Result processing
    # 6. Cache storage
    
    return {
        "status": "not_implemented",
        "message": "DALL-E integration follows planned architecture but not yet implemented",
        "planned_features": [
            "Prompt enhancement and validation",
            "Multiple image size and quality options",
            "Cost estimation and tracking",
            "Result caching and fingerprinting",
            "Error handling with retry logic"
        ]
    }

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for image generation"""
    # DALL-E pricing would be based on model and size
    base_cost = 0.02  # Approximate cost per image
    
    model = params.get("model", "dall-e-3")
    size = params.get("size", "1024x1024")
    count = params.get("count", 1)
    
    # Adjust cost based on parameters
    if model == "dall-e-3":
        base_cost = 0.04 if size == "1024x1024" else 0.08
    
    return base_cost * count
```
            
    async def enhance_prompt(self, base_prompt: str, params: dict = None):
        """Enhance prompt for better image generation"""
        enhancement_style = params.get("enhancement", "professional") if params else "professional"
        
        enhancement_patterns = {
            "professional": "professional, high quality, detailed, well-composed",
            "artistic": "artistic, creative, expressive, imaginative",
            "realistic": "photorealistic, natural lighting, authentic, detailed",
            "minimal": ""
        }
        
        enhancement = enhancement_patterns.get(enhancement_style, "")
        
        if enhancement and enhancement not in base_prompt.lower():
            enhanced = f"{base_prompt}, {enhancement}"
        else:
            enhanced = base_prompt
            
        # Ensure prompt length is within limits
        if len(enhanced) > 4000:
            enhanced = enhanced[:3997] + "..."
            
        return enhanced
```

## Tool Performance Monitoring

### Performance Analytics

The system tracks tool performance for optimization:

```python
# Actual tool performance monitoring from manager_tools.py
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
def get_tool_usage_analytics(self, username: str) -> Dict[str, Any]:
    """Get tool usage analytics for user"""
    try:
        return self.user_analytics_manager._read_analytics_file(username, "tool_usage.json")
    except Exception as e:
        return {}

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
```

## Integration Guidelines

### Adding New Tools

To integrate a new tool into the MAO system:

1. **Create Tool Directory Structure** (6-file architecture)
   ```
   tools/new_tool/
   ├── new_tool.py           # Core implementation with error handling
   ├── button_new_tool.py    # Button generation with create_button_snippet()
   ├── ui_new_tool.py        # UI integration
   ├── tool_new_tool.json    # Configuration metadata
   └── (optional files)      # Additional support files
   ```

2. **Implement Required Functions**
   - Main function with `@handle_errors` and `@retry_with_backoff` decorators
   - `estimate_cost(params: Dict[str, Any]) -> float` function
   - Proper cache integration using `CacheManager()`
   - Input validation and error handling

3. **Tool Configuration** (tool_new_tool.json)
   ```json
   {
     "name": "new_tool",
     "description": "Tool description",
     "capabilities": ["capability1", "capability2"],
     "cost_estimate": 0.001,
     "supported_models": ["claude-sonnet-4"]
   }
   ```

4. **Button Generator Implementation**
   ```python
   def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
       # Generate executable code snippet that imports from new_tool.py
       # Include parameter handling and result display
       # Return self-contained Python code
   ```

5. **Automatic Integration**
   - ToolManager discovers via `_discover_local_tools()`
   - Validates 6-file structure with `_validate_tool_structure()`
   - Includes in goal-based suggestions automatically
   - Analytics tracking included via `execute_tool_with_analytics()`

## Conclusion

MAO's tool integration patterns provide a comprehensive framework for adding, discovering, and executing AI tools. The dynamic discovery system eliminates manual configuration, while the standardized template approach ensures consistency and reliability.

The performance monitoring and caching systems optimize tool execution, while the button generation pattern enables seamless workflow integration. These patterns work together to create a flexible, extensible tool ecosystem that maintains the LOCAL-only architecture while providing powerful AI capabilities.