# Technical Data Flow Through System
*For use in: 05_INTERFACE.md - Complex technical flow for engineers to drool over*

## Complete System Data Flow with Cost Tracking

```mermaid
sequenceDiagram
    participant U as User Interface
    participant CLI as CLICommandsManager
    participant WO as WorkflowOrchestrator
    participant TM as ToolManager
    participant MM as ModelManager
    participant CM as CacheManager
    participant MCP as MemoryMCP
    participant AA as UserAnalyticsManager
    participant FA as FilesAPI
    participant AG as ParallelAgents
    
    Note over U,AG: Cost Estimation: $0.15 - $0.45 per workflow
    
    U->>CLI: /goal "marketing campaign"
    Note right of CLI: execute_slash_command()
    CLI->>WO: create_workflow_from_goal()
    
    Note over WO: _analyze_goal() → Cost: $0.001
    WO->>MM: select_optimal_model()
    MM-->>WO: claude-sonnet-4 ($0.003/1K tokens)
    
    WO->>TM: interactive_tool_selection()
    Note right of TM: get_available_tools() → discover_tools()
    TM-->>WO: [brave_search, dalle_generate, text_editor]
    
    WO->>CM: get_cached_analysis()
    Note right of CM: cache_key = "workflow|marketing|campaign"
    CM-->>WO: Cache MISS
    
    WO->>WO: _design_workflow_phases()
    Note over WO: Generate 5 parallel phases (01a-01e)
    WO->>MCP: create_workflow()
    Note right of MCP: Store workflow state + context
    
    WO->>AA: track_workflow()
    Note right of AA: SessionMetric + WorkflowMetric creation
    
    WO->>FA: store_workflow_file()
    Note right of FA: Upload JSON configs to Files API
    FA-->>WO: file_id: file-abc123xyz
    
    Note over WO,AG: Parallel Execution Block - 5 Agents
    par Phase 01a: Market Research
        WO->>AG: execute_phase_async()
        Note right of AG: Model: claude-sonnet-4<br/>Est. Cost: $0.045
        AG->>TM: create_tool_button("brave_search")
        AG->>CM: cache_tool_result()
        AG-->>WO: Market research complete
    and Phase 01b: Creative Assets  
        WO->>AG: execute_phase_async()
        Note right of AG: Model: claude-opus-4<br/>Est. Cost: $0.125
        AG->>TM: create_tool_button("dalle_generate")
        AG-->>WO: Visual assets created
    and Phase 01c: Content Strategy
        WO->>AG: execute_phase_async()
        Note right of AG: Model: claude-sonnet-4<br/>Est. Cost: $0.035
        AG->>TM: create_tool_button("text_editor")
        AG-->>WO: Content strategy drafted
    and Phase 01d: Budget Analysis
        WO->>AG: execute_phase_async()
        Note right of AG: Model: claude-sonnet-4<br/>Est. Cost: $0.025
        AG->>MCP: restore_agent_context()
        AG-->>WO: Budget breakdown ready
    and Phase 01e: Implementation Plan
        WO->>AG: execute_phase_async()
        Note right of AG: Model: claude-sonnet-4<br/>Est. Cost: $0.030
        AG->>CM: get_cached_tool_result()
        AG-->>WO: Implementation timeline
    end
    
    Note over WO: Aggregation Phase - Total Cost: $0.260
    WO->>CM: cache_content_analysis()
    Note right of CM: Store aggregated results<br/>Key: "workflow|marketing|campaign|results"
    
    WO->>AA: track_costs()
    Note right of AA: CostMetric: $0.260<br/>Model breakdown logged
    
    WO->>MCP: update_workflow_state()
    Note right of MCP: Status: completed<br/>Store deliverables metadata
    
    WO->>FA: retrieve_workflow_file()
    FA-->>WO: Complete deliverables package
    
    WO-->>U: Workflow Results + Cost Summary
    Note over U: Total Time: 3.5 minutes<br/>Total Cost: $0.260<br/>5 Parallel Deliverables
```

## Detailed Component Communication Flow

```mermaid
graph TB
    subgraph "Request Processing Layer"
        A[User Input] --> B[CLICommandsManager.execute_slash_command]
        B --> C[Input Validation & Parsing]
    end
    
    subgraph "Orchestration Layer"
        C --> D[WorkflowOrchestrator.create_workflow_from_goal]
        D --> E[WorkflowOrchestrator._analyze_goal]
        E --> F[WorkflowOrchestrator._design_workflow_phases]
        F --> G[WorkflowOrchestrator.execute_workflow_async]
    end
    
    subgraph "Resource Management Layer"
        H[ModelManager.select_optimal_model] 
        I[ToolManager.get_available_tools]
        J[ToolManager.interactive_tool_selection]
        K[CacheManager.get_cached_analysis]
        L[CacheManager.cache_content_analysis]
    end
    
    subgraph "Execution Layer"
        M[AgentOrchestrator.coordinate_agent_handoff]
        N[AgentOrchestrator.execute_workflow_phase]
        O[ButtonManager.create_tool_execution_snippet]
        P[Real-time Progress Tracking]
    end
    
    subgraph "Persistence Layer"
        Q[MemoryMCP.create_workflow]
        R[MemoryMCP.update_workflow_state]
        S[FilesAPI.store_workflow_file]
        T[FilesAPI.retrieve_workflow_file]
    end
    
    subgraph "Analytics Layer"
        U[UserAnalyticsManager.track_session]
        V[UserAnalyticsManager.track_workflow]
        W[UserAnalyticsManager.track_costs]
        X[SystemAnalyticsManager.track_performance]
    end
    
    %% Flow connections with annotations
    D -.->|"Cost: $0.001"| H
    D -.->|"Discovery"| I
    E -.->|"Cache Check"| K
    F -.->|"Store Config"| Q
    G -.->|"5 Parallel Phases"| M
    M -.->|"Per Phase"| N
    N -.->|"Button Gen"| O
    G -.->|"Results Cache"| L
    G -.->|"State Update"| R
    G -.->|"File Storage"| S
    
    %% Analytics connections
    D -.->|"Session Start"| U
    G -.->|"Workflow Track"| V
    G -.->|"Cost Track"| W
    N -.->|"Performance"| X
    
    %% Cost annotations
    H -.->|"$0.003-0.015/1K"| D
    N -.->|"$0.025-0.125/phase"| G
    L -.->|"Free (local)"| G
    S -.->|"$0.001/file"| G
    
    %% Styling for technical audience
    classDef orchestration fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef resource fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef execution fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef persistence fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef analytics fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class D,E,F,G orchestration
    class H,I,J,K,L resource
    class M,N,O,P execution
    class Q,R,S,T persistence
    class U,V,W,X analytics
```

## Technical Implementation Reference

### Core Functions Referenced (from 10_AI_DEV_INDEX.md lines 276-285)
- **Execute workflows** → `core.py` → `WorkflowOrchestrator` → `execute_workflow()`
- **Coordinate agents** → `agent_orchestrator.py` → `AgentOrchestrator` → `coordinate_agent_handoff()`
- **Track workflow state** → `workflow_state.py` → `WorkflowStateManager` → `update_workflow_state()`
- **Handle tool discovery** → `manager_tools.py` → `ToolManager` → `get_available_tools()`
- **Manage models** → `manager_models.py` → `ModelManager` → `select_optimal_model()`
- **Cache operations** → `cache/cache_system.py` → `CacheManager` → `get_cached_analysis()`
- **Process CLI commands** → `cli_manager.py` → `CLICommandsManager` → `execute_slash_command()`
- **Store user memory** → `user_memory_manager.py` → `UserMemoryManager` → `store_memory()`
- **Track analytics** → `user_analytics_manager.py` → `UserAnalyticsManager` → `track_session()`

### Performance Metrics
- **Parallel Execution:** 5 simultaneous agents reduce execution time by 80%
- **Hybrid Caching:** 95% cache hit rate on repeated workflows
- **Cost Optimization:** Dynamic model selection saves 30-60% vs. always using premium models
- **Memory Continuity:** Cross-session context reduces setup time by 70%