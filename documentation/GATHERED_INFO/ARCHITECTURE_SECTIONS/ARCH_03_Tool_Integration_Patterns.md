# ARCH_03: Tool Integration Patterns

MAO's tool integration architecture represents a sophisticated approach to building extensible AI systems through dynamic discovery, standardized interfaces, and intelligent execution patterns. The system enables seamless integration of diverse tools while maintaining type safety, performance optimization, and comprehensive error handling.

## Dynamic Tool Discovery Architecture

The foundation of MAO's tool system is its pure dynamic discovery pattern that eliminates hardcoded tool mappings and enables infinite extensibility through JSON-driven configuration.

### JSON-Driven Tool Registration

Every tool in MAO declares its capabilities, requirements, and integration points through standardized JSON metadata:

```json
{
  "name": "brave_search",
  "display_name": "Brave Search", 
  "version": "1.0.0",
  "description": "Privacy-focused web search with real-time results",
  "capabilities": [
    "web_search",
    "news_search", 
    "local_search",
    "real_time_data",
    "privacy_focused_search"
  ],
  "models": "all",
  "cost_estimate": 0.001,
  "tags": ["search", "web", "research", "privacy", "independent", "real_time"],
  "file_paths": {
    "logic": "./brave_search.py",
    "button": "./button_brave_search.py",
    "ui": "./ui_brave_search.py", 
    "config": "./brave_search.json"
  },
  "operations": {
    "search_web": {
      "description": "Search the web using Brave Search API",
      "parameters": {
        "query": {"type": "string", "required": true},
        "count": {"type": "integer", "required": false, "default": 10},
        "freshness": {"type": "string", "required": false}
      }
    }
  },
  "integrations": {
    "memory_mcp": true,
    "cache_system": true, 
    "error_handling": true
  }
}
```

This comprehensive metadata enables the orchestrator to understand tool capabilities without loading tool code, supporting intelligent tool selection and workflow planning.

### Directory-Based Tool Discovery

The tool manager implements automatic discovery through filesystem scanning:

```python
# orchestrator/manager_tools.py - Dynamic tool discovery
class ToolManager:
    def __init__(self):
        self.tools = {}
        self.tool_configs = {}
        
    async def discover_all_tools(self):
        """Discover all available tools through directory scanning"""
        
        tool_directories = [
            Path("tools/search"),
            Path("tools/content_creation"), 
            Path("tools/development"),
            Path("tools/system")
        ]
        
        for tool_dir in tool_directories:
            if not tool_dir.exists():
                continue
                
            # Scan for tool configuration files
            for config_file in tool_dir.glob("**/tool.json"):
                try:
                    tool_config = await self._load_tool_config(config_file)
                    await self._register_tool(tool_config)
                except Exception as e:
                    logger.warning(f"Failed to load tool {config_file}: {e}")
                    continue
    
    async def _register_tool(self, config: dict):
        """Register tool with capability indexing"""
        
        tool_name = config['name']
        self.tool_configs[tool_name] = config
        
        # Index by capabilities for fast lookup
        for capability in config.get('capabilities', []):
            if capability not in self.capability_index:
                self.capability_index[capability] = []
            self.capability_index[capability].append(tool_name)
        
        # Index by tags for workflow planning
        for tag in config.get('tags', []):
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(tool_name)
```

This discovery pattern ensures that new tools are automatically available without modifying core system code. Tools are registered by simply placing properly configured tool directories in the appropriate locations.

### Intelligent Tool Suggestion Engine

MAO implements a sophisticated tool suggestion system that analyzes user goals and recommends optimal tool combinations:

```python
async def suggest_tools_for_goal(self, goal: str, task_type: str = None):
    """Suggest optimal tools based on goal analysis"""
    
    # Analyze goal for capability requirements
    goal_analysis = await self._analyze_goal_requirements(goal)
    required_capabilities = goal_analysis.required_capabilities
    preferred_tags = goal_analysis.preferred_tags
    
    # Find tools by capability matching
    capability_matches = []
    for capability in required_capabilities:
        if capability in self.capability_index:
            capability_matches.extend(self.capability_index[capability])
    
    # Score tools by relevance
    tool_scores = {}
    for tool_name in set(capability_matches):
        tool_config = self.tool_configs[tool_name]
        score = self._calculate_tool_relevance_score(
            tool_config, required_capabilities, preferred_tags
        )
        tool_scores[tool_name] = score
    
    # Select top tools with diversity
    suggested_tools = []
    covered_capabilities = set()
    
    for tool_name, score in sorted(tool_scores.items(), key=lambda x: x[1], reverse=True):
        tool_config = self.tool_configs[tool_name]
        tool_capabilities = set(tool_config.get('capabilities', []))
        
        # Add tool if it provides new capabilities
        if not tool_capabilities.issubset(covered_capabilities):
            suggested_tools.append(tool_config)
            covered_capabilities.update(tool_capabilities)
            
        # Stop when we have sufficient coverage
        if len(suggested_tools) >= MAX_SUGGESTED_TOOLS:
            break
    
    return suggested_tools
```

This suggestion engine enables intelligent workflow planning by automatically identifying the most relevant tools for any given goal, while ensuring diversity and avoiding redundant capabilities.

## Standardized Tool Architecture

MAO enforces a consistent 4-file architecture for all tools, ensuring predictable integration patterns and maintainable code organization.

### Core Logic Implementation

The primary tool logic follows standardized patterns for API integration, error handling, and result formatting:

```python
# tools/search/brave_search/brave_search.py - Core tool logic
from orchestrator.cache import CacheManager
from orchestrator.error_handling import handle_errors
from orchestrator.cost_estimation import estimate_cost

class BraveSearchTool:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.cache_manager = CacheManager()
        
    @handle_errors
    @estimate_cost(operation="web_search")
    async def search_web(self, query: str, count: int = 10, freshness: str = None):
        """Search the web using Brave Search API"""
        
        # Check cache first
        cache_key = f"brave_search_{query}_{count}_{freshness}"
        cached_result = await self.cache_manager.get(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare API request
        params = {
            'q': query,
            'count': count
        }
        if freshness:
            params['freshness'] = freshness
        
        # Execute search with error handling
        try:
            response = await self._make_api_request(params)
            result = self._format_search_results(response)
            
            # Cache successful results
            await self.cache_manager.set(cache_key, result, ttl=3600)
            
            return result
            
        except APIRateLimitError as e:
            # Implement exponential backoff
            await self._handle_rate_limit(e)
            return await self.search_web(query, count, freshness)
```

This pattern ensures that all tools implement consistent error handling, caching, and cost estimation while maintaining their unique functionality.

### Button Interface Generation

MAO generates executable code snippets for each tool, enabling users to understand and replicate tool functionality:

```python
# tools/search/brave_search/button_brave_search.py - Button interface
class BraveSearchButton:
    def __init__(self, tool_manager):
        self.tool_manager = tool_manager
        
    async def generate_search_button(self, query: str, provider: str = "anthropic"):
        """Generate executable code snippet for web search"""
        
        # Determine optimal model for the task
        optimal_model = await self.tool_manager.get_optimal_model(
            task_type="web_search",
            provider=provider
        )
        
        # Generate provider-specific code
        if provider == "anthropic":
            return self._generate_anthropic_code(query, optimal_model)
        elif provider == "openai":
            return self._generate_openai_code(query, optimal_model)
        elif provider == "gemini":
            return self._generate_gemini_code(query, optimal_model)
    
    def _generate_anthropic_code(self, query: str, model: str):
        """Generate Anthropic-specific search code"""
        return f'''
import anthropic
from brave_search import BraveSearchTool

# Initialize client and tool
client = anthropic.Client(api_key="your-api-key")
search_tool = BraveSearchTool()

# Execute search
search_results = await search_tool.search_web(
    query="{query}",
    count=10
)

# Process with Claude
response = client.messages.create(
    model="{model}",
    messages=[{{
        "role": "user",
        "content": f"Analyze these search results: {{search_results}}"
    }}]
)

print(response.content)
'''
```

These button interfaces demonstrate practical integration patterns and help users understand how to incorporate MAO tools into their own projects.

### Terminal UI Integration

Tool UI components provide rich terminal interfaces that integrate seamlessly with MAO's overall user experience:

```python
# tools/search/brave_search/ui_brave_search.py - Terminal UI component
class BraveSearchUI:
    def __init__(self, tool):
        self.tool = tool
        
    async def interactive_search(self):
        """Interactive search interface with real-time results"""
        
        print("🔍 Brave Search - Privacy-focused web search")
        print("Enter search queries (type 'exit' to quit)")
        
        while True:
            query = input("\nSearch query: ").strip()
            
            if query.lower() == 'exit':
                break
            
            if not query:
                continue
            
            # Show search progress
            print(f"🔄 Searching for: {query}")
            
            try:
                # Execute search with progress indication
                results = await self.tool.search_web(query)
                
                # Display results in formatted table
                self._display_search_results(results)
                
                # Offer follow-up options
                await self._handle_search_followup(query, results)
                
            except Exception as e:
                print(f"❌ Search failed: {e}")
                print("💡 Try a different query or check your connection")
    
    def _display_search_results(self, results: dict):
        """Display search results in a formatted terminal table"""
        
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        table = Table(title="🔍 Search Results", show_header=True)
        
        table.add_column("Title", style="cyan", no_wrap=False)
        table.add_column("URL", style="blue", no_wrap=True)
        table.add_column("Snippet", style="white", no_wrap=False)
        
        for result in results.get('web', {}).get('results', []):
            table.add_row(
                result.get('title', 'No title'),
                result.get('url', 'No URL'),
                result.get('description', 'No description')[:100] + "..."
            )
        
        console.print(table)
```

The UI components provide rich, interactive experiences that demonstrate tool capabilities while maintaining consistency with MAO's terminal-first design philosophy.

## Tool Execution and Orchestration Patterns

MAO implements sophisticated execution patterns that coordinate multiple tools while maintaining performance, reliability, and user feedback.

### Parallel Tool Execution

For workflows requiring multiple data sources, MAO can execute tools in parallel:

```python
# orchestrator/core.py - Parallel tool execution
async def execute_parallel_tools(self, tools: List[Tool], context: dict):
    """Execute multiple tools in parallel for efficiency"""
    
    # Prepare tool execution tasks
    tasks = []
    for tool in tools:
        task = asyncio.create_task(
            self._execute_tool_with_context(tool, context)
        )
        tasks.append((tool.name, task))
    
    # Execute all tools concurrently
    results = {}
    completed_tasks = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
    
    # Process results and handle exceptions
    for (tool_name, _), result in zip(tasks, completed_tasks):
        if isinstance(result, Exception):
            logger.warning(f"Tool {tool_name} failed: {result}")
            results[tool_name] = {'error': str(result), 'success': False}
        else:
            results[tool_name] = {'data': result, 'success': True}
    
    return results
```

This parallel execution pattern significantly improves workflow performance when multiple independent data sources are required.

### Tool Chain Orchestration

MAO supports sophisticated tool chaining where the output of one tool becomes the input for subsequent tools:

```python
async def execute_tool_chain(self, tool_chain: List[ToolChainStep], initial_input: dict):
    """Execute a chain of tools with data flow"""
    
    current_data = initial_input
    chain_results = []
    
    for step in tool_chain:
        try:
            # Transform input data based on step requirements
            tool_input = await self._transform_data_for_tool(
                current_data, step.input_mapping
            )
            
            # Execute tool with transformed input
            tool_result = await self._execute_tool(step.tool, tool_input)
            
            # Record step result
            step_result = {
                'step_name': step.name,
                'tool_name': step.tool.name,
                'input': tool_input,
                'output': tool_result,
                'success': True,
                'timestamp': datetime.utcnow()
            }
            chain_results.append(step_result)
            
            # Transform output for next step
            current_data = await self._transform_tool_output(
                tool_result, step.output_mapping
            )
            
        except Exception as e:
            # Handle chain interruption
            step_result = {
                'step_name': step.name,
                'tool_name': step.tool.name,
                'error': str(e),
                'success': False,
                'timestamp': datetime.utcnow()
            }
            chain_results.append(step_result)
            
            # Determine if chain can continue
            if step.required:
                raise ToolChainInterruptedError(f"Required step {step.name} failed: {e}")
            
            # Continue with partial data if step is optional
            logger.warning(f"Optional step {step.name} failed, continuing chain")
    
    return {
        'final_result': current_data,
        'chain_results': chain_results,
        'success': True
    }
```

### Smart Tool Selection and Fallbacks

MAO implements intelligent fallback mechanisms when preferred tools are unavailable:

```python
async def execute_with_fallbacks(self, capability: str, context: dict, fallback_strategy: str = "quality"):
    """Execute tool with intelligent fallback selection"""
    
    # Get all tools that provide the required capability
    candidate_tools = self._get_tools_by_capability(capability)
    
    # Sort by strategy (quality, cost, speed)
    if fallback_strategy == "quality":
        candidate_tools.sort(key=lambda t: t.quality_score, reverse=True)
    elif fallback_strategy == "cost":
        candidate_tools.sort(key=lambda t: t.cost_estimate)
    elif fallback_strategy == "speed":
        candidate_tools.sort(key=lambda t: t.average_response_time)
    
    # Try tools in order until one succeeds
    last_error = None
    for tool in candidate_tools:
        try:
            # Check if tool is available
            if not await self._check_tool_availability(tool):
                continue
            
            # Execute tool
            result = await self._execute_tool(tool, context)
            
            # Log successful fallback if not first choice
            if tool != candidate_tools[0]:
                logger.info(f"Successfully used fallback tool {tool.name} for {capability}")
            
            return result
            
        except ToolNotAvailableError as e:
            last_error = e
            logger.warning(f"Tool {tool.name} not available: {e}")
            continue
        except Exception as e:
            last_error = e
            logger.error(f"Tool {tool.name} execution failed: {e}")
            continue
    
    # All tools failed
    raise AllToolsFailedError(f"No tools available for capability {capability}. Last error: {last_error}")
```

## Tool Performance and Analytics

MAO implements comprehensive performance monitoring and analytics for tool usage optimization.

### Real-Time Performance Tracking

```python
# orchestrator/real_time_metrics.py - Tool performance tracking
class ToolPerformanceTracker:
    def __init__(self):
        self.performance_data = {}
        
    async def track_tool_execution(self, tool_name: str, execution_context: dict):
        """Track comprehensive tool performance metrics"""
        
        start_time = time.time()
        
        try:
            # Execute tool with monitoring
            result = await self._execute_with_monitoring(tool_name, execution_context)
            
            execution_time = time.time() - start_time
            success = True
            error_type = None
            
        except Exception as e:
            execution_time = time.time() - start_time
            success = False
            error_type = type(e).__name__
            result = None
        
        # Record performance metrics
        metrics = {
            'tool_name': tool_name,
            'execution_time': execution_time,
            'success': success,
            'error_type': error_type,
            'input_size': len(str(execution_context)),
            'output_size': len(str(result)) if result else 0,
            'timestamp': datetime.utcnow(),
            'context_type': execution_context.get('task_type', 'unknown')
        }
        
        await self._store_performance_metrics(metrics)
        
        return result
```

### Tool Usage Analytics and Optimization

MAO provides insights into tool usage patterns and optimization opportunities:

```python
async def generate_tool_analytics_report(self, user_id: str = None, time_period: str = "7d"):
    """Generate comprehensive tool usage analytics"""
    
    # Gather usage data
    usage_data = await self._get_tool_usage_data(user_id, time_period)
    
    analytics_report = {
        'summary': {
            'total_tool_executions': len(usage_data),
            'unique_tools_used': len(set(d['tool_name'] for d in usage_data)),
            'average_execution_time': sum(d['execution_time'] for d in usage_data) / len(usage_data),
            'success_rate': sum(1 for d in usage_data if d['success']) / len(usage_data)
        },
        'tool_performance': {},
        'optimization_recommendations': []
    }
    
    # Analyze per-tool performance
    for tool_name in set(d['tool_name'] for d in usage_data):
        tool_data = [d for d in usage_data if d['tool_name'] == tool_name]
        
        analytics_report['tool_performance'][tool_name] = {
            'usage_count': len(tool_data),
            'average_execution_time': sum(d['execution_time'] for d in tool_data) / len(tool_data),
            'success_rate': sum(1 for d in tool_data if d['success']) / len(tool_data),
            'error_types': list(set(d['error_type'] for d in tool_data if d['error_type'])),
            'cost_per_execution': await self._calculate_average_tool_cost(tool_name, tool_data)
        }
    
    # Generate optimization recommendations
    analytics_report['optimization_recommendations'] = await self._generate_optimization_recommendations(
        analytics_report['tool_performance']
    )
    
    return analytics_report
```

The tool integration patterns in MAO demonstrate a sophisticated approach to building extensible AI systems that can incorporate diverse capabilities while maintaining performance, reliability, and user experience. The combination of dynamic discovery, standardized architecture, intelligent execution, and comprehensive analytics provides developers with a powerful framework for building complex AI workflows that adapt to changing requirements and optimize performance over time.