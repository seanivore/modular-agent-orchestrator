# Parallel Agents Implementation Plan
*Implementing parallel workflow execution for MAO v4.0.0*

---

## Overview

Implement the parallel agent execution feature that's already designed in the JSON config system but not yet implemented in the workflow execution logic. This enables multiple agents to work simultaneously on different aspects of complex projects.

## Current State Analysis

### ✅ What Already Exists
- **JSON Config Structure**: Phase numbering system supports parallel execution (`"01a"`, `"01b"`, `"01c"`)
- **AsyncAnthropic SDK**: Native async support with `await client.messages.create()`
- **Workflow Infrastructure**: Core orchestration files and state management
- **Documentation**: User flow documented in `NEW_USER_FLOW.md`

### ❌ What's Missing
- **Parallel Execution Logic**: Current `core.py` executes phases sequentially
- **Phase Grouping**: No logic to identify parallel phase groups
- **Async Coordination**: No use of `asyncio.gather()` for simultaneous execution
- **UI Display**: Terminal doesn't show parallel execution status

## Implementation Approach

### Phase Grouping Logic
```python
def _group_parallel_phases(self, phases: List[WorkflowPhase]) -> List[List[WorkflowPhase]]:
    """Group phases by their base phase number for parallel execution"""
    phase_groups = {}
    
    for phase in phases:
        # Extract base phase number (01a -> 01, 02b -> 02, 03 -> 03)
        phase_num = phase.phase_number if hasattr(phase, 'phase_number') else str(phases.index(phase) + 1)
        base_num = ''.join(filter(str.isdigit, phase_num))
        
        if base_num not in phase_groups:
            phase_groups[base_num] = []
        phase_groups[base_num].append(phase)
    
    # Return groups in order
    return [phase_groups[key] for key in sorted(phase_groups.keys())]
```

### Async Parallel Execution
```python
async def execute_workflow_async(self, workflow_id: str, anthropic_client=None) -> Dict[str, Any]:
    """Execute workflow with parallel phase support"""
    workflow = self.active_workflows[workflow_id]
    
    # Use AsyncAnthropic for parallel execution
    async_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Group phases for parallel execution
    phase_groups = self._group_parallel_phases(workflow.phases)
    
    results = []
    workflow_memory = {}
    
    for group in phase_groups:
        if len(group) > 1:
            # Execute multiple phases in parallel
            tasks = [
                self._execute_phase_async(phase, workflow, workflow_memory, async_client)
                for phase in group
            ]
            parallel_results = await asyncio.gather(*tasks)
            results.extend(parallel_results)
        else:
            # Single phase execution
            result = await self._execute_phase_async(group[0], workflow, workflow_memory, async_client)
            results.append(result)
    
    return {"results": results, "parallel_groups": len([g for g in phase_groups if len(g) > 1])}
```

## File Modifications Required

### Primary Implementation Files

#### `orchestrator/core.py` - Main Execution Logic
- **Function**: `execute_workflow()` → `execute_workflow_async()`
- **Changes**: 
  - Add `_group_parallel_phases()` method
  - Implement parallel execution with `asyncio.gather()`
  - Use `AsyncAnthropic` instead of `Anthropic`
  - Update phase loop to handle groups

#### `orchestrator/agent_orchestrator.py` - Agent Coordination
- **Function**: Agent handoff coordination
- **Changes**:
  - Handle multiple simultaneous agent completions
  - Coordinate parallel agent state updates
  - Manage concurrent Files API operations

#### `orchestrator/workflow_state.py` - State Management
- **Function**: Track parallel execution states
- **Changes**:
  - Track multiple phases executing simultaneously
  - Handle parallel state updates in Memory MCP
  - Coordinate completion detection across parallel agents

### Secondary Integration Files

#### `interfaces/ui_terminal.py` - User Interface
- **Function**: Display parallel execution progress
- **Changes**:
  - Show "Phase Group 1 (3 parallel agents)" instead of "Phase 1/5"
  - Real-time parallel execution status
  - Coordinated completion reporting

#### `orchestrator/agent_callback.py` - Result Processing
- **Function**: Handle parallel agent returns
- **Changes**:
  - Process multiple simultaneous results
  - Coordinate handoff package creation
  - Aggregate parallel deliverables

#### `orchestrator/memory_mcp.py` - State Persistence  
- **Function**: Store parallel workflow state
- **Changes**:
  - Track parallel execution in Memory MCP
  - Handle concurrent state updates
  - Coordinate session recovery for parallel workflows

## JSON Config Schema Updates

### Phase Configuration
```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01a",
      "phase_goal": "Market research - Demographics",
      "phase_deliverable": "Demographics report"
    },
    {
      "workflow_id": "uid-qmt-465", 
      "phase_number": "01b",
      "phase_goal": "Market research - Competitors",
      "phase_deliverable": "Competitor analysis"
    },
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01c", 
      "phase_goal": "Market research - Trends",
      "phase_deliverable": "Market trends report"
    }
  ]
}
```

**Key Pattern**: All phases with base number "01" execute in parallel, then phase "02" waits for all "01" phases to complete.

## Implementation Steps

### Step 1: Core Async Infrastructure
1. Install/verify `AsyncAnthropic` support
2. Create `_group_parallel_phases()` method
3. Add `_execute_phase_async()` helper method
4. Test phase grouping logic with mock phases

### Step 2: Parallel Execution Engine
1. Implement `execute_workflow_async()` method
2. Add `asyncio.gather()` coordination
3. Handle parallel error management
4. Test with simple 2-phase parallel workflow

### Step 3: State Management Integration
1. Update `workflow_state.py` for parallel tracking
2. Coordinate Memory MCP updates
3. Handle concurrent Files API operations
4. Test session recovery with parallel workflows

### Step 4: UI/UX Enhancements
1. Update terminal display for parallel execution
2. Show real-time parallel progress
3. Coordinate completion reporting
4. Test user experience flow

### Step 5: Error Handling & Edge Cases
1. Handle partial parallel failures
2. Implement parallel timeout handling
3. Coordinate error recovery
4. Test complex parallel scenarios

## Success Criteria

### Functional Requirements
- [ ] Phases with same base number execute simultaneously
- [ ] Sequential phases wait for parallel groups to complete
- [ ] All parallel results properly aggregated
- [ ] Memory MCP correctly tracks parallel state
- [ ] Files API handles concurrent operations
- [ ] UI displays parallel execution status

### Performance Benefits
- [ ] 50%+ time reduction for parallelizable workflows
- [ ] Efficient resource utilization across API calls
- [ ] No increase in token costs (same total work)
- [ ] Maintains workflow quality and coordination

### Integration Requirements
- [ ] Backwards compatible with existing sequential workflows
- [ ] Works with all existing tools and models
- [ ] Maintains caching efficiency
- [ ] Preserves error handling and recovery

## Testing Strategy

### Unit Tests
- Phase grouping logic (`"01a"`, `"01b"` → group "01")
- Async execution coordination
- Error handling in parallel scenarios
- State management during parallel execution

### Integration Tests  
- Complete parallel workflow execution
- Memory MCP coordination across parallel agents
- Files API concurrent operations
- UI display during parallel execution

### Performance Tests
- Execution time comparison (parallel vs sequential)
- Resource utilization during parallel execution
- API rate limit handling with multiple concurrent calls
- Memory usage with parallel workflow state

## Risk Assessment & Mitigation

### High Risk: API Rate Limits
- **Mitigation**: Implement intelligent rate limiting and queuing
- **Fallback**: Sequential execution mode for rate-limited scenarios

### Medium Risk: Memory MCP Concurrency
- **Mitigation**: Implement atomic state updates and coordination locks
- **Fallback**: Local fallback storage for coordination failures

### Low Risk: UI Complexity
- **Mitigation**: Progressive enhancement - basic parallel display first
- **Fallback**: Existing sequential UI continues to work

## Documentation Updates Required

### User Documentation
- `03_USER_FLOW.md`: Document parallel phase creation
- `04_MAOS_ROLE.md`: Add parallel workflow examples
- `07_USER_GUIDE.md`: Include parallel execution tutorials

### Technical Documentation  
- `05_ORCHESTRATION.md`: Document parallel execution architecture
- `10_DEV_PRIMER.md`: Add orchestrator file responsibility guide
- Update JSON schema documentation with parallel examples

## Future Enhancements

### Phase 2 Features
- **Smart Dependency Detection**: Automatically identify parallelizable phases
- **Resource-Based Scheduling**: Optimize parallel execution based on available API quotas
- **Dynamic Load Balancing**: Adjust parallel execution based on phase complexity

### Advanced Coordination
- **Partial Result Streaming**: Show results as parallel phases complete
- **Intelligent Merging**: Automatically combine parallel deliverables
- **Cross-Phase Communication**: Allow parallel agents to coordinate during execution

---

This implementation transforms MAO from a sequential workflow orchestrator into a true parallel agent coordination system, dramatically improving efficiency for complex multi-faceted projects while maintaining the simplicity and reliability of the existing architecture.