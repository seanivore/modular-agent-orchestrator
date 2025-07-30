# Section VI: Memory-Enhanced Contextual Analytics
*Processed workflows are learned, becoming intelligence and personal enhancement*

---

Welcome to analytics in the era of AI. This is SO FUTURE. Insights are pushed further thanks to the power of memory and an ability to understand context. Intelligence built into analytics really makes a wild difference. Mao's interconnected memory system establishes sophisticated and intuitive user experience and data insight capabilities. This is where autonomy and agentic system meet evolution. Check out what it will do for you. 

---

## Feels Like Emotional Intelligence

Contextualized analytics based on personal usage insights; because Mao notices. 

Imagine a user who works with Mao to write, journal their own memoir. Or perhaps Mao's tasks are far more tactile, working with the User to run operations for their cafe. You, the user, start your day and Mao already ordered your morning coffee made exactly to your high bar of specifications. 

Push things further by adding memories on the fly, like `/memory "Always book me a window seat in business class when I fly, and make sure that the east-bound flight is always a red-eye, but never the west-bound flight or I'll be back in LA at the crack of dawn!"`

WorkflowIDs can be used to pull in preferences they've been shown in previous projects, allowing Mao to suggest improvements to a workflow. "Didn't you want to make sure the summer rental has a saltwater pool for the kids? Or does Sam no longer react strongly to chlorine?" 

---

## Real-Time Analytics Architecture 
*orchestrator/user_analytics_manager.py, orchestrator/system_analytics_manager.py*

Mao's analytic system operates with privacy-first design, capturing valuable insights through strategic trigger points while maintaining complete user control over personal data.

### Core Principles 

1. **Privacy comes first** thanks to user analytics being incredibly easy to gather or delete, and system analytics being completely anonymous. 
2. All data collected is completely **non-intrusive** and never breaks main functionality or interrupts a user. 
3. **Modular discovery** is our key to dynamic detection of tools, workflows, patterns, and all kinds of brilliant insights. 
4. Everything triggers in **real-time** with immediate tracking and periodic batch aggregation. 

### Data Flow Architecture

```
User Actions → Trigger Points → Analytics Managers → JSON Storage → Aggregation → Insights
     ↓              ↓                    ↓               ↓             ↓           ↓
CLI Commands    Tool Manager     User Analytics    User Directory   System     Dashboard
Workflows      Workflow Mgr      System Analytics  System Directory Analytics    APIs
Tool Usage     Settings Mgr      Memory Analytics   Memory MCP      Privacy    Reports
```

### Metric Data Storage

```
./configs/user/[username]/analytics/  # User-specific analytics (deletable)
./configs/system/analytics/           # Anonymous aggregate analytics
./memory_mcp/                         # Analytics patterns and insights
```

### System-Level Analytics Implementation

The `SystemAnalyticsManager` handles anonymous aggregate analytics, tracking system-wide performance and health metrics with complete user anonymization.

```python
# Real SystemAnalyticsManager.track_performance method
@handle_errors
def track_performance(self, tool_name: str, response_time: float, success: bool, error_type: str = None) -> bool:
    """Track tool performance metrics anonymously"""
    try:
        data = self._read_system_analytics_file("tool_performance.json")
        current_time = datetime.now(timezone.utc).isoformat()
        
        # Initialize tool if not exists
        if tool_name not in data["tool_metrics"]:
            data["tool_metrics"][tool_name] = {
                "avg_response_time": 0.0,
                "success_rate": 0.0,
                "error_patterns": {},
                "performance_trend": "stable",
                "total_executions": 0
            }
        
        tool_data = data["tool_metrics"][tool_name]
        old_total = tool_data.get("total_executions", 0)
        tool_data["total_executions"] = old_total + 1
        
        # Update average response time
        if old_total == 0:
            tool_data["avg_response_time"] = response_time
        else:
            current_avg = tool_data["avg_response_time"]
            tool_data["avg_response_time"] = (current_avg * old_total + response_time) / tool_data["total_executions"]
        
        # Update success rate
        if old_total == 0:
            tool_data["success_rate"] = 1.0 if success else 0.0
        else:
            current_successes = tool_data["success_rate"] * old_total
            new_successes = current_successes + (1 if success else 0)
            tool_data["success_rate"] = new_successes / tool_data["total_executions"]
        
        # Track error patterns anonymously
        if error_type and not success:
            if error_type not in tool_data["error_patterns"]:
                tool_data["error_patterns"][error_type] = 0
            tool_data["error_patterns"][error_type] += 1
        
        # Update system health metrics (aggregated)
        all_tools = data["tool_metrics"].values()
        if all_tools:
            total_executions = sum(tool.get("total_executions", 0) for tool in all_tools)
            weighted_success_rate = sum(tool.get("success_rate", 0) * tool.get("total_executions", 0) for tool in all_tools)
            weighted_response_time = sum(tool.get("avg_response_time", 0) * tool.get("total_executions", 0) for tool in all_tools)
            
            if total_executions > 0:
                data["system_health"]["overall_success_rate"] = weighted_success_rate / total_executions
                data["system_health"]["avg_response_time"] = weighted_response_time / total_executions
                data["system_health"]["error_rate"] = 1.0 - (weighted_success_rate / total_executions)
        
        data["metadata"]["total_executions_analyzed"] = sum(tool.get("total_executions", 0) for tool in all_tools)
        data["metadata"]["last_updated"] = current_time
        
        return self._write_system_analytics_file("tool_performance.json", data)
        
    except Exception as e:
        # System analytics failures should not break main functionality
        return False
```

### Anonymous Time Pattern Analysis

```python
# Real SystemAnalyticsManager.calculate_time_patterns method
@handle_errors
def calculate_time_patterns(self, user_analytics_data: List[Dict]) -> Dict:
    """Calculate anonymous time usage patterns from user data"""
    try:
        peak_hours = {}
        peak_days = {}
        
        # Anonymize all user data before processing
        anonymized_data = [self._anonymize_user_data(user_data) for user_data in user_analytics_data]
        
        for user_data in anonymized_data:
            if "sessions" in user_data and "sessions" in user_data["sessions"]:
                for session in user_data["sessions"]["sessions"]:
                    if session.get("start_time"):
                        start_time = datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
                        
                        # Track hourly patterns (anonymous aggregates)
                        hour_range = f"{start_time.hour:02d}:00-{start_time.hour+1:02d}:00"
                        if hour_range not in peak_hours:
                            peak_hours[hour_range] = 0
                        peak_hours[hour_range] += 1
                        
                        # Track daily patterns (anonymous aggregates)
                        day_name = start_time.strftime("%A").lower()
                        if day_name not in peak_days:
                            peak_days[day_name] = 0
                        peak_days[day_name] += 1
        
        # Convert to percentages for privacy
        total_hours = sum(peak_hours.values())
        total_days = sum(peak_days.values())
        
        if total_hours > 0:
            peak_hours = {k: v / total_hours for k, v in peak_hours.items()}
        if total_days > 0:
            peak_days = {k: v / total_days for k, v in peak_days.items()}
        
        return {
            "peak_hours": peak_hours,
            "peak_days": peak_days
        }
    except Exception as e:
        return {"peak_hours": {}, "peak_days": {}}
```

---

## Session Analytics Architecture
*orchestrator/user_analytics_manager.py, interfaces/ui_terminal.py*

### Trigger Points

- App initialization (ui_terminal.py)
- App shutdown (ui_terminal.py) 
- Workflow count updates
- Tool activation tracking

```python
# Real UserAnalyticsManager.track_session method
@handle_errors
def track_session(self, username: str, session_id: str, action: str, **kwargs) -> bool:
    """Track session metrics"""
    try:
        data = self._read_analytics_file(username, "session_metrics.json")
        current_time = datetime.now(timezone.utc).isoformat()
        
        if action == "start":
            session_metric = {
                "session_id": session_id,
                "start_time": current_time,
                "end_time": None,
                "duration_minutes": None,
                "workflow_count": 0,
                "tool_activations": 0
            }
            data["sessions"].append(session_metric)
            
        elif action == "end":
            # Find and update session
            for session in data["sessions"]:
                if session["session_id"] == session_id:
                    session["end_time"] = current_time
                    start_time = datetime.fromisoformat(session["start_time"].replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
                    session["duration_minutes"] = int((end_time - start_time).total_seconds() / 60)
                    break
```

### Session Data Schema

```json
{
  "sessions": [
    {
      "session_id": "sess_001",
      "start_time": "2025-01-15T09:00:00Z",
      "end_time": "2025-01-15T11:30:00Z", 
      "duration_minutes": 150,
      "workflow_count": 3,
      "tool_activations": 12
    }
  ],
  "aggregates": {
    "total_sessions": 1,
    "average_duration": 150,
    "total_time_minutes": 150
  },
  "metadata": {
    "last_updated": "2025-01-15T11:30:00Z"
  }
}
```

## Workflow Analytics Architecture
*orchestrator/user_analytics_manager.py, orchestrator/workflow_manager.py*

### Trigger Points

- Workflow start (workflow_manager.py)
- Workflow completion (workflow_manager.py)
- Tag extraction from README.md
- Success/failure tracking

```python
# Real UserAnalyticsManager.track_workflow method
@handle_errors
def track_workflow(self, username: str, workflow_id: str, workflow_command: str, action: str, **kwargs) -> bool:
    """Track workflow metrics"""
    try:
        data = self._read_analytics_file(username, "workflow_metrics.json")
        current_time = datetime.now(timezone.utc).isoformat()
        
        if action == "start":
            workflow_metric = {
                "workflow_id": workflow_id,
                "workflow_command": workflow_command,
                "start_time": current_time,
                "completion_time": None,
                "success": False,
                "workflow_tags": kwargs.get("tags", [])
            }
            data["workflows"].append(workflow_metric)
            
        elif action == "complete":
            # Find and update workflow
            for workflow in data["workflows"]:
                if workflow["workflow_id"] == workflow_id:
                    workflow["completion_time"] = current_time
                    workflow["success"] = kwargs.get("success", False)
                    break
            
            # Update tag analytics
            for workflow in data["workflows"]:
                if workflow["workflow_id"] == workflow_id and workflow["workflow_tags"]:
                    for tag in workflow["workflow_tags"]:
                        if tag not in data["tag_analytics"]:
                            data["tag_analytics"][tag] = {
                                "usage_count": 0,
                                "success_rate": 0.0,
                                "avg_duration": 0.0
                            }
                        
                        tag_data = data["tag_analytics"][tag]
                        tag_data["usage_count"] += 1
                        
                        # Update success rate and duration calculations...
        
        data["metadata"]["total_workflows_tracked"] = len(data["workflows"])
        data["metadata"]["last_updated"] = current_time
        return self._write_analytics_file(username, "workflow_metrics.json", data)
```

### Workflow Data Schema

```json
{
  "workflows": [
    {
      "workflow_id": "wf_001",
      "workflow_command": "competitor_analysis",
      "start_time": "2025-01-15T09:00:00Z",
      "completion_time": "2025-01-15T10:30:00Z",
      "success": true,
      "workflow_tags": ["parallel", "research", "analysis"]
    }
  ],
  "tag_analytics": {
    "parallel": {"usage_count": 5, "avg_duration": 45},
    "research": {"usage_count": 8, "success_rate": 0.92}
  },
  "metadata": {
    "total_workflows_tracked": 1,
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```

## Cost Tracking Architecture
*orchestrator/user_analytics_manager.py, orchestrator/manager_models.py*

### Trigger Points

- API costs from model managers
- Daily rollup aggregation
- Model-specific cost tracking
- Session cost accumulation

```python
# Real UserAnalyticsManager.track_costs method
@handle_errors
def track_costs(self, username: str, date: str, model_name: str, cost: float, session_id: str = None) -> bool:
    """Track cost metrics"""
    try:
        data = self._read_analytics_file(username, "cost_tracking.json")
        current_time = datetime.now(timezone.utc).isoformat()
        
        # Find or create daily cost entry
        daily_cost = None
        for cost_entry in data["daily_costs"]:
            if cost_entry["date"] == date:
                daily_cost = cost_entry
                break
        
        if daily_cost is None:
            daily_cost = {
                "date": date,
                "total_spend": 0.0,
                "model_breakdown": {},
                "session_count": 0
            }
            data["daily_costs"].append(daily_cost)
        
        # Update costs
        daily_cost["total_spend"] += cost
        
        if model_name not in daily_cost["model_breakdown"]:
            daily_cost["model_breakdown"][model_name] = 0.0
        daily_cost["model_breakdown"][model_name] += cost
        
        # Update totals
        total_spend = sum(entry["total_spend"] for entry in data["daily_costs"])
        avg_daily = total_spend / len(data["daily_costs"]) if data["daily_costs"] else 0.0
        
        data["totals"] = {
            "monthly_spend": total_spend,
            "avg_daily": avg_daily
        }
        
        return self._write_analytics_file(username, "cost_tracking.json", data)
```

### Cost Tracking Data Schema

```json
{
  "daily_costs": [
    {
      "date": "2025-01-15",
      "total_spend": 2.45,
      "model_breakdown": {
        "claude-sonnet-4": 1.80,
        "gpt-4": 0.65
      },
      "session_count": 3
    }
  ],
  "totals": {
    "monthly_spend": 45.67,
    "avg_daily": 1.52
  },
  "metadata": {
    "last_updated": "2025-01-15T23:59:59Z"
  }
}
```

---

## Memory System Architecture
*orchestrator/user_memory_manager.py, orchestrator/memory_mcp.py, orchestrator/mcp_hub.py*

Mao's memory system provides intelligent storage and retrieval of user preferences, contextual insights, and personalized suggestions through Memory MCP integration.

### Core Memory Components

1. **UserMemoryManager** - Main memory operations and user interface
2. **MemoryMCPManager** - MCP integration for persistent storage
3. **MCPIntegrationHub** - Unified system coordination

### Memory Storage Architecture

```python
# Real UserMemoryManager.store_memory method
@handle_errors(operation_name="store_memory", return_dict=True)
def store_memory(self, user_id: str, content: str, category: str = None, 
                tags: List[str] = None, priority: str = "medium") -> Dict[str, Any]:
    """Store a new memory for the user with automatic categorization."""
    if not user_id or not content:
        raise ValueError("User ID and content are required")
    
    # Get username from user_id
    username = self._get_username_from_user_id(user_id)
    if not username:
        raise APIError(f"Could not find username for user_id: {user_id}")
    
    # Generate memory ID
    memory_id = f"mem_{uuid4().hex[:8]}"
    
    # Auto-categorize if not provided
    if not category:
        category = self._auto_categorize_content(content)
    
    # Create memory object
    memory = {
        "memory_id": memory_id,
        "content": content,
        "category": category,
        "tags": tags or [],
        "priority": priority,
        "created_at": datetime.now().isoformat(),
        "last_accessed": datetime.now().isoformat(),
        "access_count": 0,
        "relevance_score": 1.0,
        "context_triggers": self._extract_context_triggers(content),
        "source": "user_input",
        "metadata": {
            "auto_categorized": category != category,
            "confidence_score": 0.85,
            "related_memories": [],
            "embedding_vector": None
        }
    }
    
    # Store in file system
    self._store_memory_to_file(username, memory, category)
    
    # Store in Memory MCP for persistence
    self._store_memory_to_mcp(user_id, memory)
    
    # Clear related caches
    self._clear_user_memory_cache(user_id)
    
    return {
        "success": True,
        "memory_id": memory_id,
        "category": category,
        "tags": tags,
        "message": "Memory stored successfully"
    }
```

### Memory Data Schema

```json
{
  "memories": [
    {
      "memory_id": "mem_a1b2c3d4",
      "content": "Always use descriptive variable names", 
      "category": "coding_preference",
      "tags": ["coding", "variables", "best_practices"],
      "priority": "medium",
      "created_at": "2025-01-15T10:30:00Z",
      "last_accessed": "2025-01-15T10:30:00Z",
      "access_count": 0,
      "relevance_score": 1.0,
      "context_triggers": ["variable", "naming", "code"],
      "source": "user_input"
    }
  ],
  "metadata": {
    "user_id": "user-1642",
    "total_memories": 1,
    "last_updated": "2025-01-15T10:30:00Z"
  }
}
```

### MCP Integration Architecture

```python
# Real MCP integration from user_memory_manager.py
def _store_memory_to_mcp(self, user_id: str, memory: Dict[str, Any]):
    """Store memory to Memory MCP for persistence"""
    try:
        # Create MCP entity for the memory
        entity_data = {
            "name": f"user_memory_{user_id}_{memory['memory_id']}",
            "entityType": "user-memory",
            "observations": [
                f"User ID: {user_id}",
                f"Memory ID: {memory['memory_id']}",
                f"Content: {memory['content']}",
                f"Category: {memory['category']}",
                f"Tags: {', '.join(memory['tags'])}",
                f"Created: {memory['created_at']}"
            ]
        }
        
        self.memory_mcp.client.create_entities([entity_data])
        
    except Exception as e:
        # Log error but don't fail the operation
        print(f"Warning: Failed to store memory to MCP: {e}")
```

---

## Analytics Trigger Points Reference
*This section documents where analytics triggers are implemented across the codebase*

### Session Triggers
- **File**: `interfaces/ui_terminal.py`
- **Trigger Points**: 
  - App initialization → `track_session(username, session_id, "start")`
  - App shutdown → `track_session(username, session_id, "end")`
  - Workflow count updates → `track_session(username, session_id, "update_workflow_count")`
  - Tool activations → `track_session(username, session_id, "update_tool_activations")`

### Tool Usage Triggers  
- **File**: `orchestrator/manager_tools.py`
- **Trigger Points**:
  - Tool invocation → `track_tool_usage(username, tool_name, success, response_time)`
  - Tool completion → Success/failure tracking
  - Tool discovery → Dynamic tool addition to analytics

### Workflow Triggers
- **File**: `orchestrator/workflow_manager.py` 
- **Trigger Points**:
  - Workflow start → `track_workflow(username, workflow_id, command, "start", tags=tags)`
  - Workflow completion → `track_workflow(username, workflow_id, command, "complete", success=True/False)`
  - Tag extraction → README.md scanning during setup

### Cost Triggers
- **Files**: `orchestrator/manager_models.py`, `orchestrator/real_time_metrics.py`
- **Trigger Points**:
  - API calls → `track_costs(username, date, model_name, cost, session_id)`
  - Model selection → Cost estimation and tracking
  - Daily rollup → End-of-day aggregation

### Memory Triggers
- **File**: `configs/cli/memory/memory.py`
- **Trigger Points**:
  - Memory storage → `/memory "content"` command
  - Memory retrieval → `/memory --list` command
  - Memory deletion → `/memory --delete [ID]` command
  - Contextual suggestions → Workflow-based memory retrieval

---

## Privacy & Data Control Architecture
*orchestrator/user_analytics_manager.py, orchestrator/username_manager.py*

Privacy isn't an afterthought in Mao's analytics and memory systems; it's foundational to the architecture. Every piece of user data is designed to be easily discoverable, exportable, and deletable.

### User Data Directory Structure 

**All easily deletable information**

```
./configs/user/[username]/
├── user_[username].json           # Main user configuration
├── memories/                      # User preferences and memories
│   ├── personal_preferences.json
│   └── project_context.json
└── analytics/                     # User-specific analytics (deletable)
    ├── session_metrics.json
    ├── tool_usage.json
    ├── workflow_metrics.json
    └── cost_tracking.json
```

### System Data Directory Structure

**All anonymous information**

```
./configs/system/analytics/
├── aggregate_usage.json    # Anonymous usage patterns
├── tool_performance.json   # Tool efficiency metrics  
└── system_health.json      # Resource and error tracking
```

### Data Separation Strategy

User analytics remain completely private and tied to user identifiers for easy GDPR compliance. System analytics are anonymous aggregates with all user identifiers stripped before storage.

```python
# Real implementation from UserAnalyticsManager
def _get_user_analytics_dir(self, username: str) -> Path:
    """Get user analytics directory path"""
    return self.user_dir / username / "analytics"

def _ensure_analytics_dir(self, username: str) -> Path:
    """Ensure user analytics directory exists"""
    analytics_dir = self._get_user_analytics_dir(username)
    analytics_dir.mkdir(parents=True, exist_ok=True)
    return analytics_dir
```

### GDPR Compliance Matrix

```json
{
  "user_analytics": {
    "storage": "./configs/user/[username]/analytics/",
    "identifier": "username",
    "deletion_method": "delete_user_directory",
    "retention": "user_controlled"
  },
  "user_memories": {
    "storage": "./configs/user/[username]/memories/",
    "identifier": "user_id",
    "deletion_method": "delete_user_directory", 
    "retention": "user_controlled"
  },
  "system_analytics": {
    "storage": "./configs/system/analytics/",
    "anonymization": "remove_all_user_identifiers",
    "retention": "1_year_rolling",
    "purpose": "performance_optimization"
  }
}
```

### Data Transparency

Users maintain complete control over their analytics and memory data through transparent management tools. The system provides clear visibility into what data is stored and enables one-command deletion of all personal data.

**Real User Directory Management:**
- Complete user data stored in single directory tree
- Easy discovery of all user-related files
- Simple deletion process removes everything
- No hidden or distributed user data
- Full GDPR compliance by design

---

## Dynamic Discovery Architecture
*orchestrator/user_analytics_manager.py, orchestrator/manager_tools.py*

Following Mao's core philosophy of "Everything modular, everything discoverable," the analytics system automatically adapts to new tools, workflows, and components without requiring manual configuration.

### Tool Discovery Implementation

```python
# Real implementation from UserAnalyticsManager
@handle_errors
def scan_available_tools(self, username: str) -> List[str]:
    """Scan and discover available tools for analytics"""
    try:
        # This integrates with manager_tools.py discover_all_tools()
        data = self._read_analytics_file(username, "tool_usage.json")
        tracked_tools = list(data["tool_usage"].keys())
        
        # Update discovery scan timestamp
        data["metadata"]["last_discovery_scan"] = datetime.now(timezone.utc).isoformat()
        self._write_analytics_file(username, "tool_usage.json", data)
        
        return tracked_tools
        
    except Exception as e:
        return []
```

### Auto-Addition Pattern

When new tools are used, they're automatically added to analytics tracking:

```python
# Auto-add tool if not tracked (from track_tool_usage)
if tool_name not in data["tool_usage"]:
    data["tool_usage"][tool_name] = {
        "total_uses": 0,
        "success_rate": 0.0,
        "avg_response_time": 0.0,
        "last_used": None
    }
```

---

## Error Handling Philosophy

**Analytics failures never break main functionality.** Every analytics operation is wrapped in error handling that ensures system resilience:

```python
# Real pattern from UserAnalyticsManager
except Exception as e:
    # Analytics failures should not break main functionality
    return False
```

This design principle ensures that analytics enhance the user experience without ever compromising core system reliability.

---

*Mao's memory and analytics systems create an AI assistant that truly learns and adapts while maintaining absolute respect for user privacy and control over personal data.*
