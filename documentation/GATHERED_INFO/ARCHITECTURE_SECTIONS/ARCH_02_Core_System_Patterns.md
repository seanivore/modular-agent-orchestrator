# ARCH_02: Core System Patterns

The core system patterns in MAO represent a sophisticated orchestration architecture that transforms natural language goals into intelligent multi-phase workflows. These patterns demonstrate how modern AI systems can coordinate multiple models, tools, and data sources while maintaining performance, cost optimization, and robust error handling.

## Orchestration Architecture Patterns

MAO's orchestration system implements a goal-driven workflow architecture that analyzes user intent, designs optimal execution paths, and coordinates distributed AI resources to achieve complex objectives.

### Natural Language to Workflow Translation

The orchestrator's most sophisticated pattern transforms unstructured user goals into structured, executable workflows:

```python
# orchestrator/core.py - Goal analysis and workflow design
class WorkflowOrchestrator:
    async def create_workflow_from_goal(self, goal: str, user_id: str):
        """Transform natural language goal into executable workflow"""
        
        # Step 1: Analyze goal for task complexity and type
        goal_analysis = await self._analyze_goal(goal)
        
        # Step 2: Get tool suggestions based on goal analysis
        suggested_tools = await self.tool_manager.suggest_tools_for_goal(
            goal, goal_analysis.task_type
        )
        
        # Step 3: Design optimal workflow phases
        workflow_phases = await self._design_workflow_phases(
            goal, goal_analysis, suggested_tools
        )
        
        # Step 4: Select optimal models for each phase
        for phase in workflow_phases:
            phase.model = await self._select_optimal_model(
                phase.task_type, phase.complexity
            )
        
        # Step 5: Create and execute workflow plan
        workflow_plan = WorkflowPlan(
            goal=goal,
            phases=workflow_phases,
            user_id=user_id,
            estimated_cost=self._calculate_total_cost(workflow_phases)
        )
        
        return await self._execute_workflow(workflow_plan)
```

This pattern demonstrates several key orchestration principles:

**Intelligent Decomposition**: Complex goals are automatically broken down into manageable phases based on task analysis and tool availability. The system recognizes patterns like "research and summarize," "analyze and recommend," or "create and iterate."

**Context-Aware Tool Selection**: Tools are suggested based not just on keywords, but on deep understanding of the goal's requirements, user preferences, and available resources.

**Adaptive Model Selection**: Different AI models are selected for different phases based on their strengths. For example, Claude Sonnet might handle analysis while GPT-4 handles creative writing tasks.

### Dynamic Workflow Phase Creation

The workflow design system creates phases dynamically based on goal complexity and available tools:

```python
async def _design_workflow_phases(self, goal: str, analysis: GoalAnalysis, tools: List[Tool]):
    """Design optimal workflow phases based on goal analysis"""
    
    phases = []
    
    if analysis.requires_research:
        # Create research phase with appropriate search tools
        research_phase = WorkflowPhase(
            name="research",
            description=f"Research information for: {goal}",
            tools=[t for t in tools if 'search' in t.capabilities],
            input_sources=[],  # Initial phase
            expected_output="comprehensive research data"
        )
        phases.append(research_phase)
    
    if analysis.requires_analysis:
        # Create analysis phase using research results
        analysis_phase = WorkflowPhase(
            name="analysis", 
            description=f"Analyze research data for: {goal}",
            tools=[t for t in tools if 'analysis' in t.capabilities],
            input_sources=[phases[-1].name] if phases else [],
            expected_output="structured analysis and insights"
        )
        phases.append(analysis_phase)
    
    if analysis.requires_creation:
        # Create content generation phase
        creation_phase = WorkflowPhase(
            name="creation",
            description=f"Create deliverable for: {goal}",
            tools=[t for t in tools if 'content_creation' in t.capabilities],
            input_sources=[p.name for p in phases],
            expected_output="final deliverable"
        )
        phases.append(creation_phase)
    
    return phases
```

This dynamic phase creation enables the system to adapt to any goal complexity. Simple goals might generate a single phase, while complex goals can create sophisticated multi-phase workflows with proper dependency management.

### Intelligent Model Selection

MAO implements context-aware model selection that considers task requirements, cost optimization, and performance characteristics:

```python
async def _select_optimal_model(self, task_type: str, complexity: str):
    """Select optimal model based on task requirements"""
    
    # Get available models and their capabilities
    available_models = await self.model_manager.get_available_models()
    
    # Filter models by task compatibility
    compatible_models = [
        model for model in available_models
        if task_type in model.optimal_tasks
    ]
    
    # Apply selection criteria
    if complexity == "high":
        # Use most capable model for complex tasks
        return max(compatible_models, key=lambda m: m.capability_score)
    elif self.cost_optimization_enabled:
        # Prefer free models when cost optimization is enabled
        free_models = [m for m in compatible_models if m.cost == 0]
        if free_models:
            return max(free_models, key=lambda m: m.capability_score)
    
    # Default to best cost/performance ratio
    return min(compatible_models, key=lambda m: m.cost_per_token / m.capability_score)
```

This selection pattern balances performance requirements with cost optimization, ensuring that expensive models are only used when necessary while maintaining high-quality results.

## State Management Architecture

MAO implements a sophisticated multi-layer state management system that provides both performance and reliability through hybrid storage strategies.

### Memory MCP Integration Pattern

The Memory MCP serves as the authoritative source for workflow state, providing persistence and recovery capabilities:

```python
# orchestrator/memory_mcp.py - Workflow state persistence
class MemoryMCP:
    async def store_workflow_state(self, workflow_id: str, state_data: dict):
        """Store workflow state with metadata and versioning"""
        
        state_record = {
            'workflow_id': workflow_id,
            'timestamp': datetime.utcnow().isoformat(),
            'state_version': self._increment_version(workflow_id),
            'data': state_data,
            'checksum': self._calculate_checksum(state_data)
        }
        
        # Store in Memory MCP with error handling
        try:
            await self.mcp_client.store(
                key=f"workflow_state_{workflow_id}",
                value=json.dumps(state_record),
                metadata={'type': 'workflow_state', 'user_id': state_data.get('user_id')}
            )
        except MCPConnectionError:
            # Fallback to local storage
            await self._store_local_fallback(workflow_id, state_record)
```

### Multi-Layer State Persistence

The state management system implements multiple storage layers with automatic failover:

```python
# orchestrator/workflow_state.py - Intelligent state management
class WorkflowState:
    def __init__(self):
        self.active_workflows = {}  # In-memory active state
        self.execution_history = {}  # Session-level history
        self.workflow_memory = {}  # Context between phases
        
    async def persist_workflow_progress(self, workflow_id: str, phase_result: dict):
        """Persist workflow progress with multi-layer storage"""
        
        # Update in-memory state
        if workflow_id not in self.active_workflows:
            self.active_workflows[workflow_id] = {'phases': [], 'status': 'active'}
        
        self.active_workflows[workflow_id]['phases'].append(phase_result)
        
        # Store in Memory MCP for persistence
        try:
            await self.memory_mcp.store_workflow_state(workflow_id, self.active_workflows[workflow_id])
        except Exception as e:
            logger.warning(f"MCP storage failed, using local backup: {e}")
            self._store_local_backup(workflow_id, phase_result)
        
        # Update workflow memory for context passing
        await self._update_workflow_context(workflow_id, phase_result)
```

### Context-Aware Phase Execution

The system maintains rich context between workflow phases using file-based memory management:

```python
async def _build_context_for_phase(self, phase: WorkflowPhase, workflow_id: str):
    """Build comprehensive context from previous phases"""
    
    context_parts = []
    
    # Include results from input source phases
    for source_phase in phase.input_sources:
        phase_results = await self._get_phase_results(workflow_id, source_phase)
        if phase_results:
            context_parts.append({
                'phase': source_phase,
                'results': phase_results['output'],
                'metadata': phase_results['metadata']
            })
    
    # Include relevant workflow memory
    workflow_context = await self.workflow_memory.get(workflow_id, {})
    if workflow_context.get('persistent_context'):
        context_parts.append(workflow_context['persistent_context'])
    
    # Build comprehensive context document
    context_document = self._compile_context_document(context_parts)
    
    # Store context in Files API for model access
    context_file_id = await self.files_api.upload_content(
        content=context_document,
        filename=f"workflow_{workflow_id}_phase_{phase.name}_context.md"
    )
    
    return context_file_id
```

This context management enables phases to build upon previous work intelligently, maintaining coherence across complex multi-step workflows.

## Caching Architecture and Performance Optimization

MAO implements a sophisticated dual-layer caching system that balances performance, cost, and storage efficiency.

### Content Fingerprinting and Deduplication

The caching system uses content fingerprinting to detect and deduplicate expensive API operations:

```python
# orchestrator/cache/cache_system.py - Hybrid caching with fingerprinting
class CacheSystem:
    async def cache_expensive_operation(self, operation_key: str, content: str, result: dict):
        """Cache expensive operations with content fingerprinting"""
        
        # Generate content fingerprint for deduplication
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        cache_key = f"{operation_key}_{content_hash}"
        
        # Create cache record with metadata
        cache_record = {
            'result': result,
            'content_hash': content_hash,
            'timestamp': datetime.utcnow().isoformat(),
            'access_count': 1,
            'operation_type': operation_key
        }
        
        # Store in memory cache for fast access
        self.memory_cache[cache_key] = cache_record
        
        # Store in Files API for persistence
        if self.files_api_available:
            await self.files_api.upload_content(
                content=json.dumps(cache_record),
                filename=f"cache_{cache_key}.json"
            )
```

### Intelligent Cache Decisions

The caching system makes intelligent decisions about what to cache based on operation cost and reuse likelihood:

```python
async def should_cache_operation(self, operation_type: str, content_size: int, estimated_cost: float):
    """Intelligent cache decision based on cost and reuse probability"""
    
    # Always cache expensive operations
    if estimated_cost > EXPENSIVE_OPERATION_THRESHOLD:
        return True
    
    # Cache based on content characteristics
    if operation_type in ['goal_analysis', 'tool_suggestion']:
        # These operations are frequently reused
        return True
    
    # Consider content size for storage efficiency
    if content_size > LARGE_CONTENT_THRESHOLD:
        # Only cache large content if it's expensive
        return estimated_cost > LARGE_CONTENT_CACHE_THRESHOLD
    
    # Default caching for medium-cost operations
    return estimated_cost > MEDIUM_COST_THRESHOLD
```

### Cache Warming and Preemptive Loading

MAO implements cache warming strategies to improve perceived performance:

```python
async def warm_cache_for_user(self, user_id: str):
    """Preemptively warm cache based on user patterns"""
    
    # Analyze user's common goals and patterns
    user_patterns = await self.user_analytics.get_usage_patterns(user_id)
    
    # Pre-load frequently used tool configurations
    for tool_name in user_patterns.frequent_tools:
        tool_config = await self.tool_manager.get_tool_config(tool_name)
        cache_key = f"tool_config_{tool_name}"
        self.memory_cache[cache_key] = tool_config
    
    # Pre-analyze common goal patterns
    for goal_pattern in user_patterns.common_goals:
        if goal_pattern not in self.memory_cache:
            analysis = await self._analyze_goal(goal_pattern)
            self.memory_cache[f"goal_analysis_{goal_pattern}"] = analysis
```

## Error Handling and Recovery Patterns

MAO implements comprehensive error handling that ensures system resilience while providing meaningful user feedback.

### Graceful Degradation Architecture

The system implements multiple levels of graceful degradation:

```python
# orchestrator/error_handling.py - Comprehensive error recovery
class ErrorHandler:
    async def handle_workflow_phase_error(self, phase: WorkflowPhase, error: Exception, context: dict):
        """Handle phase errors with intelligent recovery strategies"""
        
        if isinstance(error, APITimeoutError):
            # Retry with exponential backoff
            return await self._retry_with_backoff(phase, context, max_retries=3)
        
        elif isinstance(error, ModelNotAvailableError):
            # Fallback to alternative model
            alternative_model = await self._find_alternative_model(phase.requirements)
            if alternative_model:
                phase.model = alternative_model
                return await self._retry_phase(phase, context)
        
        elif isinstance(error, ToolNotAvailableError):
            # Remove failed tool and continue with available tools
            available_tools = [t for t in phase.tools if t.name != error.tool_name]
            if available_tools:
                phase.tools = available_tools
                return await self._retry_phase(phase, context)
        
        elif isinstance(error, InsufficientCreditsError):
            # Switch to free model if available
            free_model = await self._find_free_alternative(phase.model)
            if free_model:
                phase.model = free_model
                return await self._retry_phase(phase, context)
        
        # If recovery fails, gracefully degrade
        return await self._graceful_phase_degradation(phase, error, context)
```

### Recovery Planning and Continuation

When workflows encounter errors, MAO implements intelligent recovery planning:

```python
async def create_recovery_plan(self, failed_workflow: Workflow, error_context: dict):
    """Create intelligent recovery plan for failed workflows"""
    
    recovery_options = []
    
    # Analyze failure point and remaining phases
    failed_phase_index = error_context.get('failed_phase_index', 0)
    remaining_phases = failed_workflow.phases[failed_phase_index:]
    
    # Option 1: Resume from last successful phase
    if failed_phase_index > 0:
        recovery_options.append({
            'type': 'resume_from_checkpoint',
            'description': f'Resume from phase {failed_phase_index}',
            'phases': remaining_phases,
            'estimated_cost': self._calculate_recovery_cost(remaining_phases)
        })
    
    # Option 2: Simplified workflow with alternative approach
    simplified_phases = await self._create_simplified_workflow(
        failed_workflow.goal, remaining_phases
    )
    recovery_options.append({
        'type': 'simplified_approach',
        'description': 'Use simplified workflow with basic tools',
        'phases': simplified_phases,
        'estimated_cost': self._calculate_recovery_cost(simplified_phases)
    })
    
    # Option 3: Manual intervention points
    recovery_options.append({
        'type': 'manual_intervention',
        'description': 'Provide manual input and continue',
        'intervention_points': self._identify_manual_intervention_points(remaining_phases)
    })
    
    return recovery_options
```

### Professional Error Communication

MAO provides clear, actionable error messages that help users understand issues and next steps:

```python
def format_user_friendly_error(self, error: Exception, context: dict) -> dict:
    """Format errors for clear user communication"""
    
    error_messages = {
        APITimeoutError: {
            'title': 'API Response Timeout',
            'message': 'The AI service is taking longer than expected to respond.',
            'actions': ['Try again in a moment', 'Switch to a faster model', 'Simplify your request'],
            'technical_details': str(error)
        },
        InsufficientCreditsError: {
            'title': 'Insufficient API Credits',
            'message': 'Your API credits are insufficient for this operation.',
            'actions': ['Switch to a free model', 'Add more credits', 'Simplify the workflow'],
            'cost_breakdown': context.get('cost_breakdown', {})
        },
        ModelNotAvailableError: {
            'title': 'AI Model Unavailable',
            'message': f'The requested model {error.model_name} is currently unavailable.',
            'actions': ['Try an alternative model', 'Wait and retry', 'Check service status'],
            'alternatives': context.get('alternative_models', [])
        }
    }
    
    return error_messages.get(type(error), {
        'title': 'Unexpected Error',
        'message': 'An unexpected error occurred during processing.',
        'actions': ['Try again', 'Report this issue', 'Check system status'],
        'technical_details': str(error)
    })
```

The core system patterns demonstrate MAO's sophisticated approach to AI orchestration, combining intelligent workflow design, robust state management, performance optimization, and comprehensive error handling. These patterns provide a foundation for building reliable, scalable, and user-friendly AI automation systems that can handle complex real-world scenarios while maintaining excellent performance and user experience.