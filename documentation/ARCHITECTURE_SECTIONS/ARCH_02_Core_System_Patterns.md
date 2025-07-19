# Core System Patterns - Orchestration, State Management, and Caching

## Introduction

The MAO core system implements sophisticated orchestration patterns that coordinate multiple AI agents, manage complex workflow states, and optimize performance through intelligent caching. These patterns form the foundation for reliable, scalable AI orchestration while maintaining the LOCAL-only architecture principles.

## Orchestration Architecture Patterns

### Agent Orchestrator Core

The central orchestration system coordinates multiple AI agents and manages their interactions:

```python
# orchestrator/agent_orchestrator.py
class AgentOrchestrator:
    def __init__(self):
        self.active_workflows = {}
        self.agent_registry = {}
        self.performance_metrics = RealTimeMetrics()
        self.cache_manager = CacheManager()
        
    @handle_errors
    async def orchestrate_workflow(self, workflow_id: str, goal: str):
        """Core orchestration logic for multi-agent workflows"""
        workflow = await self.initialize_workflow(workflow_id, goal)
        
        try:
            # Agent capability analysis
            suitable_agents = await self.analyze_agent_capabilities(goal)
            
            # Workflow decomposition
            tasks = await self.decompose_workflow(goal, suitable_agents)
            
            # Sequential and parallel task execution
            results = await self.execute_task_sequence(tasks, workflow)
            
            # Result synthesis and validation
            final_result = await self.synthesize_results(results, workflow)
            
            return final_result
            
        except Exception as e:
            await self.handle_workflow_failure(workflow_id, e)
            raise
```

### Agent Callback Management

The callback system provides structured communication between agents and the orchestrator:

```python
# orchestrator/agent_callback.py
class AgentCallback:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.callback_registry = {}
        
    async def register_callback(self, agent_id: str, callback_type: str, handler):
        """Register agent callback handlers for orchestrator communication"""
        if agent_id not in self.callback_registry:
            self.callback_registry[agent_id] = {}
            
        self.callback_registry[agent_id][callback_type] = handler
        
    async def handle_agent_response(self, agent_id: str, response_data: dict):
        """Process agent responses with type-specific handling"""
        response_type = response_data.get("type", "general")
        
        handlers = {
            "progress_update": self.handle_progress_update,
            "tool_request": self.handle_tool_request,
            "handoff_request": self.handle_handoff_request,
            "completion": self.handle_completion,
            "error": self.handle_error
        }
        
        handler = handlers.get(response_type, self.handle_generic_response)
        return await handler(agent_id, response_data)
        
    async def handle_tool_request(self, agent_id: str, request_data: dict):
        """Handle agent tool execution requests"""
        tool_name = request_data["tool_name"]
        tool_params = request_data["parameters"]
        
        # Tool availability verification
        if not await self.verify_tool_availability(tool_name):
            return {"status": "error", "message": f"Tool {tool_name} not available"}
            
        # Tool execution with cost tracking
        cost_estimate = estimate_cost("tool_execution", tool=tool_name, params=tool_params)
        
        try:
            result = await self.orchestrator.execute_tool(tool_name, tool_params)
            await self.update_workflow_costs(agent_id, cost_estimate)
            return {"status": "success", "result": result}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

### Conversation Bridge Pattern

The conversation bridge maintains context and enables seamless agent-to-agent communication:

```python
# orchestrator/conversation_bridge.py
class ConversationBridge:
    def __init__(self):
        self.context_store = {}
        self.conversation_history = {}
        self.memory_mcp = None
        
    async def create_conversation_context(self, workflow_id: str, participants: list):
        """Create shared conversation context for multi-agent workflows"""
        context = {
            "workflow_id": workflow_id,
            "participants": participants,
            "shared_memory": {},
            "conversation_log": [],
            "context_metadata": {
                "created_at": datetime.utcnow(),
                "last_updated": datetime.utcnow(),
                "message_count": 0
            }
        }
        
        self.context_store[workflow_id] = context
        
        # Persist to Memory MCP if available
        if self.memory_mcp:
            await self.memory_mcp.store_conversation_context(workflow_id, context)
            
        return context
        
    async def bridge_agent_communication(self, from_agent: str, to_agent: str, 
                                       message: dict, workflow_id: str):
        """Bridge communication between agents with context preservation"""
        context = self.context_store.get(workflow_id)
        if not context:
            raise ValueError(f"No conversation context for workflow {workflow_id}")
            
        # Message enrichment with context
        enriched_message = {
            "from": from_agent,
            "to": to_agent,
            "content": message,
            "timestamp": datetime.utcnow(),
            "context_snapshot": self.extract_relevant_context(context, message)
        }
        
        # Update conversation log
        context["conversation_log"].append(enriched_message)
        context["context_metadata"]["last_updated"] = datetime.utcnow()
        context["context_metadata"]["message_count"] += 1
        
        # Persist updated context
        await self.persist_context_update(workflow_id, context)
        
        return enriched_message
```

## State Management Architecture

### Workflow State Management

The workflow state manager handles complex multi-agent workflow states with persistence and recovery:

```python
# orchestrator/workflow_state.py
class WorkflowState:
    def __init__(self):
        self.state_store = {}
        self.state_history = {}
        self.recovery_handlers = {}
        
    async def initialize_workflow_state(self, workflow_id: str, initial_state: dict):
        """Initialize workflow state with recovery planning"""
        state = {
            "workflow_id": workflow_id,
            "status": "initialized",
            "current_phase": "planning",
            "agent_states": {},
            "shared_data": {},
            "execution_metadata": {
                "start_time": datetime.utcnow(),
                "estimated_duration": None,
                "cost_tracking": {"estimated": 0, "actual": 0},
                "progress_percentage": 0
            },
            "recovery_checkpoints": []
        }
        
        state.update(initial_state)
        
        self.state_store[workflow_id] = state
        await self.create_recovery_checkpoint(workflow_id, "initialization")
        
        return state
        
    async def update_workflow_state(self, workflow_id: str, updates: dict):
        """Update workflow state with automatic checkpointing"""
        current_state = self.state_store.get(workflow_id)
        if not current_state:
            raise ValueError(f"Workflow {workflow_id} not found")
            
        # Apply updates
        self.deep_update(current_state, updates)
        current_state["execution_metadata"]["last_updated"] = datetime.utcnow()
        
        # Automatic checkpoint creation for significant state changes
        if self.is_significant_update(updates):
            await self.create_recovery_checkpoint(workflow_id, updates.get("phase", "update"))
            
        # Persist to Memory MCP
        if hasattr(self, 'memory_mcp') and self.memory_mcp:
            await self.memory_mcp.update_workflow_state(workflow_id, current_state)
            
        return current_state
        
    async def recover_workflow_state(self, workflow_id: str, checkpoint_id: str = None):
        """Recover workflow state from checkpoint with intelligent resumption"""
        try:
            # Primary recovery from Memory MCP
            if hasattr(self, 'memory_mcp') and self.memory_mcp:
                state = await self.memory_mcp.get_workflow_state(workflow_id)
                if state:
                    self.state_store[workflow_id] = state
                    return state
        except Exception as e:
            logger.warning(f"MCP recovery failed: {e}")
            
        # Secondary recovery from local checkpoints
        checkpoint = await self.load_checkpoint(workflow_id, checkpoint_id)
        if checkpoint:
            self.state_store[workflow_id] = checkpoint["state"]
            return checkpoint["state"]
            
        # Tertiary recovery with state reconstruction
        return await self.reconstruct_workflow_state(workflow_id)
```

### Memory MCP Integration

The Memory MCP provides persistent state storage with intelligent fallback mechanisms:

```python
# orchestrator/memory_mcp.py
class MemoryMCP:
    def __init__(self):
        self.connection = None
        self.local_fallback = {}
        self.sync_queue = []
        
    async def store_workflow_memory(self, workflow_id: str, memory_data: dict):
        """Store workflow memory with automatic fallback"""
        try:
            # Primary storage to Memory MCP
            if self.connection:
                result = await self.connection.store_memory({
                    "workflow_id": workflow_id,
                    "memory_type": "workflow_state",
                    "data": memory_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
                
                if result.get("status") == "success":
                    return result
                    
        except Exception as e:
            logger.warning(f"Memory MCP storage failed: {e}")
            
        # Fallback to local storage
        self.local_fallback[workflow_id] = {
            "data": memory_data,
            "timestamp": datetime.utcnow(),
            "sync_pending": True
        }
        
        # Queue for later synchronization
        self.sync_queue.append({
            "operation": "store",
            "workflow_id": workflow_id,
            "data": memory_data
        })
        
        return {"status": "stored_locally", "sync_pending": True}
        
    async def retrieve_workflow_memory(self, workflow_id: str):
        """Retrieve workflow memory with intelligent fallback"""
        try:
            # Primary retrieval from Memory MCP
            if self.connection:
                result = await self.connection.get_memory({
                    "workflow_id": workflow_id,
                    "memory_type": "workflow_state"
                })
                
                if result.get("status") == "success":
                    return result["data"]
                    
        except Exception as e:
            logger.warning(f"Memory MCP retrieval failed: {e}")
            
        # Fallback to local storage
        local_data = self.local_fallback.get(workflow_id)
        if local_data:
            return local_data["data"]
            
        return None
        
    async def sync_pending_operations(self):
        """Synchronize pending operations when MCP becomes available"""
        if not self.connection or not self.sync_queue:
            return
            
        successful_syncs = []
        
        for operation in self.sync_queue:
            try:
                if operation["operation"] == "store":
                    await self.store_workflow_memory(
                        operation["workflow_id"],
                        operation["data"]
                    )
                    successful_syncs.append(operation)
                    
            except Exception as e:
                logger.warning(f"Sync failed for {operation['workflow_id']}: {e}")
                
        # Remove successfully synced operations
        for sync_op in successful_syncs:
            self.sync_queue.remove(sync_op)
```

## Caching Architecture Patterns

### Dual-Layer Cache System

MAO implements sophisticated caching with memory and persistent layers:

```python
# orchestrator/cache/cache_system.py
class CacheManager:
    def __init__(self):
        self.memory_cache = {}
        self.cache_stats = {"hits": 0, "misses": 0, "writes": 0}
        self.files_api = None
        self.cache_policies = {
            "default_ttl": 3600,  # 1 hour
            "max_memory_size": 100 * 1024 * 1024,  # 100MB
            "compression_threshold": 1024  # 1KB
        }
        
    async def get(self, key: str, category: str = "general"):
        """Intelligent cache retrieval with fingerprinting and validation"""
        cache_key = f"{category}:{key}"
        
        # Layer 1: Memory cache with TTL validation
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if self.is_cache_entry_valid(entry):
                self.cache_stats["hits"] += 1
                return entry["data"]
            else:
                # Remove expired entry
                del self.memory_cache[cache_key]
                
        # Layer 2: Files API cache
        if self.files_api:
            try:
                file_path = f"cache/{category}/{key}"
                content = await self.files_api.read_file(file_path)
                
                # Validate content integrity
                if await self.validate_cached_content(file_path, content):
                    # Promote to memory cache
                    await self.promote_to_memory_cache(cache_key, content)
                    self.cache_stats["hits"] += 1
                    return content
                    
            except FileNotFoundError:
                pass
            except Exception as e:
                logger.warning(f"Cache read error for {key}: {e}")
                
        self.cache_stats["misses"] += 1
        return None
        
    async def set(self, key: str, value: any, category: str = "general", ttl: int = None):
        """Intelligent cache storage with deduplication and compression"""
        cache_key = f"{category}:{key}"
        ttl = ttl or self.cache_policies["default_ttl"]
        
        # Content fingerprinting for deduplication
        content_hash = hashlib.sha256(str(value).encode()).hexdigest()
        
        # Check for existing content with same hash
        if await self.content_exists(content_hash):
            await self.create_content_link(cache_key, content_hash)
            return content_hash
            
        # Compression for large content
        stored_value = value
        compressed = False
        
        if len(str(value)) > self.cache_policies["compression_threshold"]:
            stored_value = await self.compress_content(value)
            compressed = True
            
        # Memory cache entry
        cache_entry = {
            "data": value,  # Store uncompressed in memory
            "stored_data": stored_value,
            "hash": content_hash,
            "compressed": compressed,
            "timestamp": time.time(),
            "ttl": ttl,
            "access_count": 0
        }
        
        # Memory cache with size management
        await self.ensure_memory_cache_space(cache_key, cache_entry)
        self.memory_cache[cache_key] = cache_entry
        
        # Files API storage
        if self.files_api:
            try:
                file_path = f"cache/{category}/{key}"
                await self.files_api.write_file(file_path, stored_value)
                await self.files_api.write_file(f"{file_path}.meta", {
                    "hash": content_hash,
                    "compressed": compressed,
                    "timestamp": cache_entry["timestamp"],
                    "ttl": ttl
                })
                
            except Exception as e:
                logger.warning(f"Cache write error for {key}: {e}")
                
        self.cache_stats["writes"] += 1
        return content_hash
        
    async def invalidate_pattern(self, pattern: str, category: str = "general"):
        """Invalidate cache entries matching pattern"""
        import fnmatch
        
        invalidated_keys = []
        cache_prefix = f"{category}:"
        
        # Memory cache invalidation
        keys_to_remove = []
        for cache_key in self.memory_cache:
            if cache_key.startswith(cache_prefix):
                key_part = cache_key[len(cache_prefix):]
                if fnmatch.fnmatch(key_part, pattern):
                    keys_to_remove.append(cache_key)
                    invalidated_keys.append(key_part)
                    
        for key in keys_to_remove:
            del self.memory_cache[key]
            
        # Files API cache invalidation
        if self.files_api:
            try:
                cache_dir = f"cache/{category}"
                files = await self.files_api.list_files(cache_dir)
                
                for file_path in files:
                    file_name = Path(file_path).name
                    if fnmatch.fnmatch(file_name, pattern):
                        await self.files_api.delete_file(file_path)
                        await self.files_api.delete_file(f"{file_path}.meta")
                        
            except Exception as e:
                logger.warning(f"Cache invalidation error: {e}")
                
        return invalidated_keys
```

### Content Fingerprinting

Advanced content fingerprinting enables intelligent deduplication:

```python
async def generate_content_fingerprint(self, content: any, metadata: dict = None):
    """Generate comprehensive content fingerprint for deduplication"""
    # Primary content hash
    content_str = json.dumps(content, sort_keys=True) if isinstance(content, dict) else str(content)
    primary_hash = hashlib.sha256(content_str.encode()).hexdigest()
    
    # Semantic hash for similar content detection
    semantic_features = self.extract_semantic_features(content)
    semantic_hash = hashlib.sha256(str(semantic_features).encode()).hexdigest()
    
    # Metadata hash for context-aware caching
    metadata_hash = None
    if metadata:
        metadata_str = json.dumps(metadata, sort_keys=True)
        metadata_hash = hashlib.sha256(metadata_str.encode()).hexdigest()
        
    fingerprint = {
        "primary": primary_hash,
        "semantic": semantic_hash,
        "metadata": metadata_hash,
        "size": len(content_str),
        "type": type(content).__name__,
        "timestamp": time.time()
    }
    
    return fingerprint
    
def extract_semantic_features(self, content):
    """Extract semantic features for similar content detection"""
    if isinstance(content, str):
        # Text content features
        words = content.lower().split()
        return {
            "word_count": len(words),
            "unique_words": len(set(words)),
            "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "key_terms": sorted(set(w for w in words if len(w) > 4))[:10]
        }
    elif isinstance(content, dict):
        # Structured data features
        return {
            "key_count": len(content.keys()),
            "depth": self.calculate_dict_depth(content),
            "keys": sorted(content.keys()),
            "value_types": [type(v).__name__ for v in content.values()]
        }
    else:
        # Generic features
        return {
            "type": type(content).__name__,
            "size": len(str(content)),
            "hash": hashlib.md5(str(content).encode()).hexdigest()
        }
```

## Performance Monitoring Patterns

### Real-Time Metrics Collection

The system provides comprehensive real-time performance monitoring:

```python
# orchestrator/real_time_metrics.py
class RealTimeMetrics:
    def __init__(self):
        self.metrics_store = {}
        self.metric_history = {}
        self.performance_thresholds = {
            "response_time_ms": 5000,
            "memory_usage_mb": 500,
            "cache_hit_rate": 0.8,
            "error_rate": 0.05
        }
        
    async def record_operation_metrics(self, operation: str, duration_ms: float, 
                                     metadata: dict = None):
        """Record operation performance metrics"""
        timestamp = time.time()
        
        metric_entry = {
            "operation": operation,
            "duration_ms": duration_ms,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "performance_score": self.calculate_performance_score(duration_ms, operation)
        }
        
        # Store current metrics
        if operation not in self.metrics_store:
            self.metrics_store[operation] = []
            
        self.metrics_store[operation].append(metric_entry)
        
        # Maintain rolling history (last 1000 entries)
        if len(self.metrics_store[operation]) > 1000:
            self.metrics_store[operation] = self.metrics_store[operation][-1000:]
            
        # Update aggregated metrics
        await self.update_aggregated_metrics(operation, metric_entry)
        
        # Performance threshold monitoring
        await self.check_performance_thresholds(operation, metric_entry)
        
    async def get_performance_summary(self, time_window_minutes: int = 60):
        """Generate comprehensive performance summary"""
        cutoff_time = time.time() - (time_window_minutes * 60)
        
        summary = {
            "time_window_minutes": time_window_minutes,
            "operations": {},
            "system_health": {},
            "recommendations": []
        }
        
        for operation, metrics in self.metrics_store.items():
            recent_metrics = [m for m in metrics if m["timestamp"] > cutoff_time]
            
            if recent_metrics:
                durations = [m["duration_ms"] for m in recent_metrics]
                
                operation_summary = {
                    "call_count": len(recent_metrics),
                    "avg_duration_ms": sum(durations) / len(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "p95_duration_ms": self.calculate_percentile(durations, 95),
                    "error_count": len([m for m in recent_metrics if m.get("error")]),
                    "performance_trend": self.calculate_performance_trend(recent_metrics)
                }
                
                summary["operations"][operation] = operation_summary
                
        # System health assessment
        summary["system_health"] = await self.assess_system_health(summary["operations"])
        
        # Performance recommendations
        summary["recommendations"] = await self.generate_performance_recommendations(summary)
        
        return summary
```

## Integration Patterns

### Cost Estimation Integration

Every core system operation includes comprehensive cost estimation:

```python
def estimate_orchestration_cost(workflow_complexity: str, agent_count: int, 
                              estimated_duration_minutes: int):
    """Estimate cost for orchestration operations"""
    base_costs = {
        "simple": {"base_tokens": 500, "complexity_multiplier": 1.0},
        "medium": {"base_tokens": 1500, "complexity_multiplier": 1.5},
        "complex": {"base_tokens": 3000, "complexity_multiplier": 2.0}
    }
    
    complexity_config = base_costs.get(workflow_complexity, base_costs["medium"])
    
    estimated_cost = {
        "tokens": int(complexity_config["base_tokens"] * agent_count * complexity_config["complexity_multiplier"]),
        "time_minutes": estimated_duration_minutes,
        "memory_mb": agent_count * 50,  # Estimated memory per agent
        "cache_operations": agent_count * 10,  # Estimated cache operations
        "complexity": workflow_complexity,
        "confidence": 0.8 if workflow_complexity != "complex" else 0.6
    }
    
    return estimated_cost
```

## Conclusion

The core system patterns in MAO provide a robust foundation for AI orchestration through sophisticated state management, intelligent caching, and comprehensive performance monitoring. These patterns ensure reliable operation while maintaining the LOCAL-only architecture and privacy-first principles.

The orchestration patterns enable complex multi-agent workflows with proper error handling and recovery mechanisms. The state management architecture provides persistence and recovery capabilities essential for long-running AI workflows. The caching system optimizes performance while maintaining data integrity and intelligent deduplication.

These core patterns work together to create a professional-grade AI orchestration platform that scales efficiently while maintaining reliability and performance standards.