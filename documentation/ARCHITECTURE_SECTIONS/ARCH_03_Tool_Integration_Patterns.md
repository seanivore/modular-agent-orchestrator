# Tool Integration Patterns - Dynamic Discovery, Generation, and Execution

## Introduction

MAO's tool integration architecture implements sophisticated patterns for dynamic tool discovery, automated generation, and reliable execution. This system enables seamless integration of diverse AI tools while maintaining performance, reliability, and the LOCAL-only architecture principles.

## Dynamic Tool Discovery Patterns

### Tool Manager Architecture

The tool manager provides intelligent tool discovery and recommendation based on goal analysis:

```python
# orchestrator/manager_tools.py
class ToolManager:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.available_tools = {}
        self.tool_performance_cache = {}
        
    @handle_errors
    async def discover_tools(self, refresh_cache: bool = False):
        """Dynamically discover all available tools with caching"""
        cache_key = "discovered_tools"
        
        if not refresh_cache:
            cached_tools = await self.cache_manager.get(cache_key, "tools")
            if cached_tools:
                self.available_tools = cached_tools
                return cached_tools
                
        discovered_tools = {}
        tools_directory = Path(__file__).parent.parent / "tools"
        
        for tool_dir in tools_directory.iterdir():
            if tool_dir.is_dir() and not tool_dir.name.startswith('.'):
                tool_config = await self.load_tool_configuration(tool_dir)
                
                if tool_config and self.validate_tool_structure(tool_dir):
                    discovered_tools[tool_dir.name] = {
                        "config": tool_config,
                        "path": str(tool_dir),
                        "capabilities": tool_config.get("capabilities", []),
                        "performance_metrics": await self.get_tool_performance(tool_dir.name)
                    }
                    
        self.available_tools = discovered_tools
        await self.cache_manager.set(cache_key, discovered_tools, "tools", ttl=3600)
        
        return discovered_tools
        
    async def suggest_tools_for_goal(self, goal: str, context: dict = None):
        """Intelligent tool recommendation based on goal analysis"""
        tools = await self.discover_tools()
        
        # Goal analysis for capability matching
        goal_requirements = await self.analyze_goal_requirements(goal)
        
        suggestions = []
        for tool_name, tool_info in tools.items():
            compatibility_score = await self.calculate_compatibility_score(
                tool_info, goal_requirements, context
            )
            
            if compatibility_score > 0.3:  # Minimum threshold
                suggestions.append({
                    "tool_name": tool_name,
                    "compatibility_score": compatibility_score,
                    "capabilities": tool_info["capabilities"],
                    "estimated_cost": estimate_cost("tool_execution", 
                                                  tool=tool_name, 
                                                  goal_complexity=goal_requirements["complexity"]),
                    "performance_metrics": tool_info["performance_metrics"]
                })
                
        # Sort by compatibility score and performance
        suggestions.sort(key=lambda x: (x["compatibility_score"], 
                                      x["performance_metrics"].get("success_rate", 0)), 
                        reverse=True)
        
        return suggestions[:5]  # Top 5 recommendations
        
    async def analyze_goal_requirements(self, goal: str):
        """Analyze goal to extract capability requirements"""
        # Use cached analysis if available
        goal_hash = hashlib.sha256(goal.encode()).hexdigest()
        cache_key = f"goal_analysis:{goal_hash}"
        
        cached_analysis = await self.cache_manager.get(cache_key, "analysis")
        if cached_analysis:
            return cached_analysis
            
        # Goal complexity assessment
        word_count = len(goal.split())
        complexity = "simple" if word_count < 10 else "medium" if word_count < 25 else "complex"
        
        # Capability extraction patterns
        capability_patterns = {
            "search": ["search", "find", "lookup", "research", "investigate"],
            "generation": ["create", "generate", "build", "make", "produce"],
            "analysis": ["analyze", "examine", "review", "assess", "evaluate"],
            "manipulation": ["edit", "modify", "change", "update", "transform"],
            "communication": ["send", "notify", "alert", "message", "email"]
        }
        
        detected_capabilities = []
        goal_lower = goal.lower()
        
        for capability, keywords in capability_patterns.items():
            if any(keyword in goal_lower for keyword in keywords):
                detected_capabilities.append(capability)
                
        analysis = {
            "complexity": complexity,
            "word_count": word_count,
            "detected_capabilities": detected_capabilities,
            "requires_internet": any(term in goal_lower for term in ["search", "web", "online", "internet"]),
            "requires_files": any(term in goal_lower for term in ["file", "document", "save", "load"]),
            "estimated_duration": self.estimate_goal_duration(complexity, detected_capabilities)
        }
        
        await self.cache_manager.set(cache_key, analysis, "analysis", ttl=1800)
        return analysis
```

### Tool Validation and Structure Verification

The system validates tool structure and capabilities before integration:

```python
def validate_tool_structure(self, tool_directory: Path):
    """Validate tool follows the 4-file architecture pattern"""
    required_files = {
        "logic.py": "Core tool implementation",
        "tool.json": "Tool configuration and metadata"
    }
    
    optional_patterns = {
        "button_*.py": "Button generation component",
        "ui_*.py": "UI integration component"
    }
    
    validation_results = {
        "valid": True,
        "missing_required": [],
        "missing_optional": [],
        "validation_errors": []
    }
    
    # Check required files
    for required_file, description in required_files.items():
        file_path = tool_directory / required_file
        if not file_path.exists():
            validation_results["missing_required"].append(required_file)
            validation_results["valid"] = False
            
    # Check optional pattern files
    for pattern, description in optional_patterns.items():
        matching_files = list(tool_directory.glob(pattern))
        if not matching_files:
            validation_results["missing_optional"].append(pattern)
            
    # Validate logic.py structure
    logic_file = tool_directory / "logic.py"
    if logic_file.exists():
        try:
            validation_results.update(self.validate_logic_file(logic_file))
        except Exception as e:
            validation_results["validation_errors"].append(f"Logic file validation failed: {e}")
            validation_results["valid"] = False
            
    return validation_results
    
def validate_logic_file(self, logic_file_path: Path):
    """Validate logic.py contains required methods and patterns"""
    import ast
    
    validation = {
        "has_main_class": False,
        "has_execute_method": False,
        "has_cost_estimation": False,
        "has_error_handling": False,
        "imports_cache_manager": False
    }
    
    try:
        with open(logic_file_path, 'r') as f:
            tree = ast.parse(f.read())
            
        for node in ast.walk(tree):
            # Check for main tool class
            if isinstance(node, ast.ClassDef):
                validation["has_main_class"] = True
                
                # Check for required methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == "execute":
                            validation["has_execute_method"] = True
                        elif item.name == "estimate_cost":
                            validation["has_cost_estimation"] = True
                            
            # Check for required imports
            if isinstance(node, ast.ImportFrom):
                if node.module and "cache_system" in node.module:
                    validation["imports_cache_manager"] = True
                elif node.module and "error_handling" in node.module:
                    validation["has_error_handling"] = True
                    
    except Exception as e:
        validation["parse_error"] = str(e)
        
    return validation
```

## Tool Generation Patterns

### Automated Tool Creation

The system provides templates and automation for generating new tools:

```python
# From tool.py template analysis
class ToolTemplate:
    """Standardized template for creating new MAO tools"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.cache_manager = CacheManager()
        self.logger = setup_logger(__name__)
        
    @handle_errors
    async def initialize(self):
        """Initialize tool with configuration and dependencies"""
        try:
            await self.cache_manager.initialize()
            await self.validate_configuration()
            await self.setup_tool_dependencies()
            
            self.logger.info(f"Tool {self.__class__.__name__} initialized successfully")
            return {"status": "initialized", "config": self.config}
            
        except Exception as e:
            self.logger.error(f"Tool initialization failed: {e}")
            raise
            
    @handle_errors
    async def execute(self, input_data: str, parameters: dict = None):
        """Execute tool with input data and optional parameters"""
        # Input validation
        validation_result = await self.validate_input(input_data, parameters)
        if not validation_result["valid"]:
            return {"status": "error", "errors": validation_result["errors"]}
            
        # Cost estimation before execution
        estimated_cost = self.estimate_cost(input_data, parameters)
        
        try:
            # Core tool execution logic (to be implemented by specific tools)
            result = await self.perform_tool_operation(input_data, parameters)
            
            # Cache successful results
            if result.get("status") == "success":
                cache_key = self.generate_cache_key(input_data, parameters)
                await self.cache_manager.set(cache_key, result, "tool_results")
                
            return {
                "status": "success",
                "result": result,
                "cost": estimated_cost,
                "cached": False
            }
            
        except Exception as e:
            self.logger.error(f"Tool execution failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "cost": estimated_cost
            }
            
    def estimate_cost(self, input_data: str, parameters: dict = None):
        """Estimate resource cost for tool execution"""
        base_cost = {
            "tokens": len(input_data.split()) * 1.2,
            "time_ms": 1000,
            "memory_mb": 10,
            "complexity": "medium"
        }
        
        # Adjust based on parameters
        if parameters:
            if parameters.get("detailed_analysis"):
                base_cost["tokens"] *= 2
                base_cost["time_ms"] *= 1.5
                base_cost["complexity"] = "high"
                
        return base_cost
        
    async def validate_input(self, input_data: str, parameters: dict = None):
        """Validate input data and parameters"""
        validation = {"valid": True, "errors": [], "warnings": []}
        
        # Basic input validation
        if not input_data or not input_data.strip():
            validation["valid"] = False
            validation["errors"].append("Input data cannot be empty")
            
        if len(input_data) > 10000:  # 10KB limit
            validation["valid"] = False
            validation["errors"].append("Input data exceeds size limit")
            
        # Parameter validation
        if parameters:
            if not isinstance(parameters, dict):
                validation["valid"] = False
                validation["errors"].append("Parameters must be a dictionary")
                
        return validation
```

### Button Generation Pattern

Tools generate executable code snippets for workflow integration:

```python
# Button generation pattern from tool documentation
def create_button_snippet(tool_name: str, goal: str, parameters: dict = None):
    """Generate executable button snippet for workflow integration"""
    
    # Sanitize inputs for code generation
    safe_tool_name = tool_name.replace('-', '_').replace(' ', '_')
    safe_goal = goal.replace('"', '\\"').replace('\n', '\\n')
    
    # Parameter handling
    params_str = ""
    if parameters:
        params_list = []
        for key, value in parameters.items():
            if isinstance(value, str):
                params_list.append(f'"{key}": "{value}"')
            else:
                params_list.append(f'"{key}": {value}')
        params_str = f", {{{', '.join(params_list)}}}" if params_list else ""
        
    # Generate executable code snippet
    snippet = f'''
# {tool_name} - Generated Tool Button
import asyncio
from tools.{safe_tool_name}.logic import {safe_tool_name.title()}Tool

async def execute_{safe_tool_name}_for_goal():
    """Execute {tool_name} for goal: {goal}"""
    tool = {safe_tool_name.title()}Tool()
    
    try:
        await tool.initialize()
        
        result = await tool.execute(
            input_data="{safe_goal}"{params_str}
        )
        
        if result["status"] == "success":
            print(f"✓ {tool_name} completed successfully")
            print(f"Result: {{result['result']}}")
            return result["result"]
        else:
            print(f"✗ {tool_name} failed: {{result.get('message', 'Unknown error')}}")
            return None
            
    except Exception as e:
        print(f"✗ {tool_name} execution error: {{e}}")
        return None
    finally:
        await tool.cleanup()

# Execute the tool
if __name__ == "__main__":
    result = asyncio.run(execute_{safe_tool_name}_for_goal())
'''
    
    return {
        "snippet": snippet,
        "tool_name": tool_name,
        "goal": goal,
        "parameters": parameters,
        "estimated_cost": estimate_cost("button_generation", tool=tool_name, goal_length=len(goal))
    }
```

## Tool Execution Patterns

### Search Tools Integration

The system includes comprehensive search tool patterns:

```python
# Search tool pattern from Brave Search documentation
class BraveSearchTool:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.api_key = os.getenv("BRAVE_API_KEY")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        
    @handle_errors
    async def execute_search(self, query: str, search_params: dict = None):
        """Execute Brave search with caching and error handling"""
        # Check cache first
        cache_key = f"brave_search:{hashlib.sha256(query.encode()).hexdigest()}"
        
        cached_result = await self.cache_manager.get(cache_key, "search")
        if cached_result:
            return {
                "status": "success",
                "results": cached_result,
                "cached": True,
                "cost": {"tokens": 0, "api_calls": 0}
            }
            
        # Prepare search parameters
        params = {
            "q": query,
            "count": search_params.get("count", 10),
            "safesearch": search_params.get("safesearch", "moderate"),
            "freshness": search_params.get("freshness", "")
        }
        
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Process and structure results
                        structured_results = self.process_search_results(data)
                        
                        # Cache successful results
                        await self.cache_manager.set(cache_key, structured_results, "search", ttl=3600)
                        
                        return {
                            "status": "success",
                            "results": structured_results,
                            "cached": False,
                            "cost": self.estimate_search_cost(query, len(structured_results))
                        }
                    else:
                        error_data = await response.text()
                        raise Exception(f"Search API error: {response.status} - {error_data}")
                        
        except Exception as e:
            logger.error(f"Brave search failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "cost": {"tokens": 0, "api_calls": 1}
            }
            
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
# Content creation pattern from DALL-E documentation
class DalleImageGenerator:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    @handle_errors
    async def generate_image(self, prompt: str, generation_params: dict = None):
        """Generate images with DALL-E integration"""
        # Parameter processing
        params = {
            "model": generation_params.get("model", "dall-e-3"),
            "size": generation_params.get("size", "1024x1024"),
            "quality": generation_params.get("quality", "standard"),
            "style": generation_params.get("style", "vivid"),
            "n": generation_params.get("count", 1)
        }
        
        # Prompt enhancement
        enhanced_prompt = await self.enhance_prompt(prompt, generation_params)
        
        try:
            # Cost estimation before generation
            estimated_cost = self.estimate_generation_cost(enhanced_prompt, params)
            
            # Generate image
            response = await self.openai_client.images.generate(
                prompt=enhanced_prompt,
                **params
            )
            
            # Process and save results
            generated_images = []
            for idx, image_data in enumerate(response.data):
                image_info = await self.process_generated_image(
                    image_data, prompt, idx, params
                )
                generated_images.append(image_info)
                
            return {
                "status": "success",
                "images": generated_images,
                "original_prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "generation_params": params,
                "cost": estimated_cost
            }
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "cost": estimated_cost
            }
            
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
# Tool performance monitoring
class ToolPerformanceMonitor:
    def __init__(self):
        self.performance_data = {}
        self.cache_manager = CacheManager()
        
    async def record_tool_execution(self, tool_name: str, execution_data: dict):
        """Record tool execution metrics for performance analysis"""
        timestamp = time.time()
        
        execution_record = {
            "tool_name": tool_name,
            "timestamp": timestamp,
            "duration_ms": execution_data.get("duration_ms", 0),
            "status": execution_data.get("status", "unknown"),
            "cost": execution_data.get("cost", {}),
            "cache_hit": execution_data.get("cached", False),
            "input_size": execution_data.get("input_size", 0),
            "output_size": execution_data.get("output_size", 0)
        }
        
        # Store in performance data
        if tool_name not in self.performance_data:
            self.performance_data[tool_name] = []
            
        self.performance_data[tool_name].append(execution_record)
        
        # Maintain rolling window (last 1000 executions)
        if len(self.performance_data[tool_name]) > 1000:
            self.performance_data[tool_name] = self.performance_data[tool_name][-1000:]
            
        # Cache performance summary
        await self.update_performance_summary(tool_name)
        
    async def get_tool_performance_summary(self, tool_name: str, days: int = 7):
        """Generate comprehensive performance summary for tool"""
        cutoff_time = time.time() - (days * 24 * 3600)
        
        tool_data = self.performance_data.get(tool_name, [])
        recent_data = [record for record in tool_data if record["timestamp"] > cutoff_time]
        
        if not recent_data:
            return {"tool_name": tool_name, "message": "No recent performance data"}
            
        # Calculate metrics
        total_executions = len(recent_data)
        successful_executions = len([r for r in recent_data if r["status"] == "success"])
        failed_executions = total_executions - successful_executions
        
        durations = [r["duration_ms"] for r in recent_data if r["duration_ms"] > 0]
        cache_hits = len([r for r in recent_data if r["cache_hit"]])
        
        summary = {
            "tool_name": tool_name,
            "time_period_days": days,
            "execution_metrics": {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
                "cache_hit_rate": cache_hits / total_executions if total_executions > 0 else 0
            },
            "performance_metrics": {
                "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
                "min_duration_ms": min(durations) if durations else 0,
                "max_duration_ms": max(durations) if durations else 0,
                "p95_duration_ms": self.calculate_percentile(durations, 95) if durations else 0
            },
            "cost_metrics": self.calculate_cost_metrics(recent_data),
            "recommendations": await self.generate_performance_recommendations(tool_name, recent_data)
        }
        
        return summary
```

## Integration Guidelines

### Adding New Tools

To integrate a new tool into the MAO system:

1. **Create Tool Directory Structure**
   ```
   tools/new_tool/
   ├── logic.py              # Core implementation with ToolTemplate
   ├── button_new_tool.py    # Button generation
   ├── ui_new_tool.py        # UI integration
   └── new_tool.json         # Configuration
   ```

2. **Implement Required Interfaces**
   - Extend ToolTemplate base class
   - Implement `execute()` method with error handling
   - Add `estimate_cost()` function
   - Include cache manager integration

3. **Tool Configuration**
   ```json
   {
     "name": "new_tool",
     "version": "1.0.0",
     "description": "Tool description",
     "capabilities": ["capability1", "capability2"],
     "requirements": ["dependency1"],
     "cost_model": "standard"
   }
   ```

4. **Automatic Integration**
   - The tool manager will automatically discover the new tool
   - Dynamic discovery will include it in suggestions
   - Performance monitoring will track its usage

## Conclusion

MAO's tool integration patterns provide a comprehensive framework for adding, discovering, and executing AI tools. The dynamic discovery system eliminates manual configuration, while the standardized template approach ensures consistency and reliability.

The performance monitoring and caching systems optimize tool execution, while the button generation pattern enables seamless workflow integration. These patterns work together to create a flexible, extensible tool ecosystem that maintains the LOCAL-only architecture while providing powerful AI capabilities.