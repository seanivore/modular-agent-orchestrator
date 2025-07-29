# Mermaid Diagrams for Documentation

This file contains all the Mermaid diagrams used throughout the Mao documentation. Copy and paste these directly into the relevant documentation files.

## Dual-Perspective User Journey Flow (Vertical with Emojis)
*For use in: 03_USER_FLOW.md - Shows both user experience and Mao's orchestration*

```mermaid
flowchart TD
    subgraph USER["👤 USER EXPERIENCE"]
        A1["Launch Mao<br/>mao mao"]
        A1 --> B1["Login Screen<br/>Enter username"]
        B1 --> C1["Theme Selection<br/>Choose terminal theme"]
        C1 --> D1["Primary Workspace<br/>'Say hello to Mao'"]
        D1 --> E1["Share Goal<br/>'I need a detailed research report<br/>for hiring creative talent'"]
        E1 --> F1["Casual Chat<br/>Provide details or say 'lead me'"]
        F1 --> G1["Review Variables<br/>/variables or /variables-explain"]
        G1 --> H1["Approve Workflow<br/>Mao shows workflow plan"]
        H1 --> I1["Watch Progress<br/>See agents working"]
        I1 --> J1["Review Results<br/>Comprehensive deliverables"]
        J1 --> K1["Request Changes<br/>Or approve completion"]
    end
    
    subgraph MAO["🧠 MAO'S ORCHESTRATION"]
        A2["System Initialization<br/>Load user settings & memory"]
        A2 --> B2["User Authentication<br/>Create/load user_username.json"]
        B2 --> C2["Theme Configuration<br/>Save UI preferences"]
        C2 --> D2["AI Welcome Generation<br/>Create unique greeting"]
        D2 --> E2["Goal Analysis<br/>Assess complexity & scope<br/>Create Workflow ID: uid-scw-965"]
        E2 --> F2["Workflow Planning<br/>Generate JSON configs<br/>Store in .temp directory"]
        F2 --> G2["Variable Collection<br/>Determine required fields<br/>Set defaults from user config"]
        G2 --> H2["Setup Script Execution<br/>Create final directory structure<br/>Generate executable script"]
        H2 --> I2["Parallel Agent Deployment<br/>5 agents working simultaneously<br/>Real-time progress tracking"]
        I2 --> J2["Result Integration<br/>Combine agent outputs<br/>Store in deliverables/"]
        J2 --> K2["Workflow Management<br/>Update workflow state<br/>Log to memory MCP"]
    end
    
    A1 -.-> A2
    B1 -.-> B2
    C1 -.-> C2
    D1 -.-> D2
    E1 -.-> E2
    F1 -.-> F2
    G1 -.-> G2
    H1 -.-> H2
    I1 -.-> I2
    J1 -.-> J2
    K1 -.-> K2
    
    subgraph TECH["🔧 TECHNICAL DETAILS"]
        L["Directory Structure<br/>configs/workflows/hiring-research/<br/>├── config-files/<br/>├── deliverables/<br/>└── metadata/"]
        M["ID Generation<br/>User ID: user-1642<br/>Workflow ID: uid-scw-965"]
        N["JSON Objects<br/>workflow_config.json<br/>phase_config.json<br/>handoff_config.json"]
        O["User Settings<br/>Theme: Dark CVD<br/>Model: claude-sonnet-4<br/>Provider: anthropic-direct"]
    end
    
    E2 -.-> M
    F2 -.-> N
    B2 -.-> O
    H2 -.-> L
    
    style A1 fill:#e1f5fe
    style E1 fill:#fff3e0
    style I1 fill:#f3e5f5
    style J1 fill:#e8f5e8
    
    style A2 fill:#e3f2fd
    style E2 fill:#fff8e1
    style I2 fill:#f3e5f5
    style J2 fill:#e8f5e8
    
    classDef userSide fill:#e8f4fd,stroke:#1976d2,stroke-width:2px
    classDef maoSide fill:#f8e8fd,stroke:#9c27b0,stroke-width:2px
    classDef technical fill:#f0f0f0,stroke:#666,stroke-width:1px
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2 maoSide
    class L,M,N,O technical
```

## Dual-Perspective User Journey Flow (Integrated Technical Details)
*Technical details integrated into the main flow for better readability*

```mermaid
flowchart TD
    subgraph USER["USER EXPERIENCE"]
        A1["Launch Mao<br/>mao mao"]
        A1 --> B1["Login Screen<br/>Enter username"]
        B1 --> C1["Theme Selection<br/>Choose terminal theme"]
        C1 --> D1["Primary Workspace<br/>'Say hello to Mao'"]
        D1 --> E1["Share Goal<br/>'I need a detailed research report<br/>for hiring creative talent'"]
        E1 --> F1["Casual Chat<br/>Provide details or say 'lead me'"]
        F1 --> G1["Review Variables<br/>/variables or /variables-explain"]
        G1 --> H1["Approve Workflow<br/>Mao shows workflow plan"]
        H1 --> I1["Watch Progress<br/>See agents working"]
        I1 --> J1["Review Results<br/>Comprehensive deliverables"]
        J1 --> K1["Request Changes<br/>Or approve completion"]
    end
    
    subgraph MAO["MAO'S ORCHESTRATION"]
        A2["System Initialization<br/>Load user settings & memory"]
        A2 --> B2["User Authentication<br/>Create/load user_username.json<br/>User ID: user-1642"]
        B2 --> C2["Theme Configuration<br/>Save UI preferences<br/>Theme: Dark CVD, Model: claude-sonnet-4"]
        C2 --> D2["AI Welcome Generation<br/>Create unique greeting"]
        D2 --> E2["Goal Analysis<br/>Assess complexity & scope<br/>Generate Workflow ID: uid-scw-965"]
        E2 --> F2["Workflow Planning<br/>Generate JSON configs in .temp/<br/>workflow_config.json, phase_config.json"]
        F2 --> G2["Variable Collection<br/>Determine required fields<br/>Set defaults from user config"]
        G2 --> H2["Setup Script Execution<br/>Create directory: configs/workflows/hiring-research/<br/>├── config-files/ ├── deliverables/ └── metadata/"]
        H2 --> I2["Parallel Agent Deployment<br/>5 agents working simultaneously<br/>Real-time progress tracking"]
        I2 --> J2["Result Integration<br/>Combine agent outputs<br/>Store in deliverables/ directory"]
        J2 --> K2["Workflow Management<br/>Update workflow state<br/>Log to memory MCP"]
    end
    
    A1 -.-> A2
    B1 -.-> B2
    C1 -.-> C2
    D1 -.-> D2
    E1 -.-> E2
    F1 -.-> F2
    G1 -.-> G2
    H1 -.-> H2
    I1 -.-> I2
    J1 -.-> J2
    K1 -.-> K2
    
    style A1 fill:#e1f5fe
    style E1 fill:#fff3e0
    style I1 fill:#f3e5f5
    style J1 fill:#e8f5e8
    
    style A2 fill:#e3f2fd
    style E2 fill:#fff8e1
    style I2 fill:#f3e5f5
    style J2 fill:#e8f5e8
    
    classDef userSide fill:#e8f4fd,stroke:#1976d2,stroke-width:2px
    classDef maoSide fill:#f8e8fd,stroke:#9c27b0,stroke-width:2px
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2 maoSide
```

## Streamlined Dual-Flow (Ultra Clean)
*Simplified version with technical details inline*

```mermaid
flowchart TD
    A1["Launch Mao<br/>mao mao"] -.-> A2["System Initialization<br/>Load settings & memory"]
    
    B1["Login Screen<br/>Enter username"] -.-> B2["User Authentication<br/>Create user_username.json<br/>Generate User ID: user-1642"]
    
    C1["Theme Selection<br/>Choose terminal theme"] -.-> C2["Save Configuration<br/>Theme: Dark CVD<br/>Model: claude-sonnet-4"]
    
    D1["Primary Workspace<br/>'Say hello to Mao'"] -.-> D2["AI Welcome Generation<br/>Create unique greeting"]
    
    E1["Share Goal<br/>'I need a detailed research report'"] -.-> E2["Goal Analysis & Planning<br/>Generate Workflow ID: uid-scw-965<br/>Create JSON configs in .temp/"]
    
    F1["Casual Chat<br/>Provide details or 'lead me'"] -.-> F2["Variable Collection<br/>workflow_config.json<br/>phase_config.json<br/>handoff_config.json"]
    
    G1["Review Variables<br/>/variables or /variables-explain"] -.-> G2["Setup Script Execution<br/>Create configs/workflows/hiring-research/<br/>Generate executable command"]
    
    H1["Approve Workflow<br/>Mao shows plan"] -.-> H2["Deploy 5 Parallel Agents<br/>Research | Creative | Strategy<br/>Budget | Implementation"]
    
    I1["Watch Progress<br/>See agents working"] -.-> I2["Real-time Integration<br/>Combine outputs<br/>Store in deliverables/"]
    
    J1["Review Results<br/>Comprehensive deliverables"] -.-> J2["Memory MCP Update<br/>Log workflow state<br/>Ready for continuation"]
    
    A1 --> B1 --> C1 --> D1 --> E1 --> F1 --> G1 --> H1 --> I1 --> J1
    A2 --> B2 --> C2 --> D2 --> E2 --> F2 --> G2 --> H2 --> I2 --> J2
    
    style A1 fill:#e1f5fe
    style E1 fill:#fff3e0
    style H1 fill:#f3e5f5
    style J1 fill:#e8f5e8
    
    style A2 fill:#e3f2fd
    style E2 fill:#fff8e1
    style H2 fill:#f3e5f5
    style J2 fill:#e8f5e8
    
    classDef userSide fill:#e8f4fd,stroke:#1976d2,stroke-width:2px
    classDef maoSide fill:#f8e8fd,stroke:#9c27b0,stroke-width:2px
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2 maoSide
```

## Dual-Perspective User Journey Flow (Clean - No Emojis)
*Alternative version matching Mao's minimal app aesthetic*

```mermaid
flowchart TD
    subgraph USER["USER EXPERIENCE"]
        A1["Launch Mao<br/>mao mao"]
        A1 --> B1["Login Screen<br/>Enter username"]
        B1 --> C1["Theme Selection<br/>Choose terminal theme"]
        C1 --> D1["Primary Workspace<br/>'Say hello to Mao'"]
        D1 --> E1["Share Goal<br/>'I need a detailed research report<br/>for hiring creative talent'"]
        E1 --> F1["Casual Chat<br/>Provide details or say 'lead me'"]
        F1 --> G1["Review Variables<br/>/variables or /variables-explain"]
        G1 --> H1["Approve Workflow<br/>Mao shows workflow plan"]
        H1 --> I1["Watch Progress<br/>See agents working"]
        I1 --> J1["Review Results<br/>Comprehensive deliverables"]
        J1 --> K1["Request Changes<br/>Or approve completion"]
    end
    
    subgraph MAO["MAO'S ORCHESTRATION"]
        A2["System Initialization<br/>Load user settings & memory"]
        A2 --> B2["User Authentication<br/>Create/load user_username.json"]
        B2 --> C2["Theme Configuration<br/>Save UI preferences"]
        C2 --> D2["AI Welcome Generation<br/>Create unique greeting"]
        D2 --> E2["Goal Analysis<br/>Assess complexity & scope<br/>Create Workflow ID: uid-scw-965"]
        E2 --> F2["Workflow Planning<br/>Generate JSON configs<br/>Store in .temp directory"]
        F2 --> G2["Variable Collection<br/>Determine required fields<br/>Set defaults from user config"]
        G2 --> H2["Setup Script Execution<br/>Create final directory structure<br/>Generate executable script"]
        H2 --> I2["Parallel Agent Deployment<br/>5 agents working simultaneously<br/>Real-time progress tracking"]
        I2 --> J2["Result Integration<br/>Combine agent outputs<br/>Store in deliverables/"]
        J2 --> K2["Workflow Management<br/>Update workflow state<br/>Log to memory MCP"]
    end
    
    A1 -.-> A2
    B1 -.-> B2
    C1 -.-> C2
    D1 -.-> D2
    E1 -.-> E2
    F1 -.-> F2
    G1 -.-> G2
    H1 -.-> H2
    I1 -.-> I2
    J1 -.-> J2
    K1 -.-> K2
    
    subgraph TECH["TECHNICAL DETAILS"]
        L["Directory Structure<br/>configs/workflows/hiring-research/<br/>├── config-files/<br/>├── deliverables/<br/>└── metadata/"]
        M["ID Generation<br/>User ID: user-1642<br/>Workflow ID: uid-scw-965"]
        N["JSON Objects<br/>workflow_config.json<br/>phase_config.json<br/>handoff_config.json"]
        O["User Settings<br/>Theme: Dark CVD<br/>Model: claude-sonnet-4<br/>Provider: anthropic-direct"]
    end
    
    E2 -.-> M
    F2 -.-> N
    B2 -.-> O
    H2 -.-> L
    
    style A1 fill:#e1f5fe
    style E1 fill:#fff3e0
    style I1 fill:#f3e5f5
    style J1 fill:#e8f5e8
    
    style A2 fill:#e3f2fd
    style E2 fill:#fff8e1
    style I2 fill:#f3e5f5
    style J2 fill:#e8f5e8
    
    classDef userSide fill:#e8f4fd,stroke:#1976d2,stroke-width:2px
    classDef maoSide fill:#f8e8fd,stroke:#9c27b0,stroke-width:2px
    classDef technical fill:#f0f0f0,stroke:#666,stroke-width:1px
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2 maoSide
    class L,M,N,O technical
```

## Simple User Journey Flow (Alternative)
*For use when you want a simpler version focusing just on the core workflow*

```mermaid
flowchart TD
    A["👤 User has Goal<br/>'I need a marketing plan'"] --> B["💬 Communicates with Mao<br/>via Terminal or Web UI"]
    
    B --> C["🧠 Mao Analyzes Goal<br/>Determines complexity & scope"]
    
    C --> D{"🤔 Multi-step project?"}
    
    D -->|Simple Task| E["🔧 Direct Tool Usage<br/>Single agent execution"]
    D -->|Complex Project| F["🚀 Workflow Creation<br/>Multi-agent orchestration"]
    
    E --> G["📋 Single Deliverable<br/>Quick completion"]
    
    F --> H["⚡ Parallel Agent Deployment<br/>5 agents working simultaneously"]
    
    H --> I["📊 Agent 1: Research<br/>Market analysis & data"]
    H --> J["🎨 Agent 2: Creative<br/>Content & visual planning"]
    H --> K["📈 Agent 3: Strategy<br/>Campaign & timeline"]
    H --> L["💰 Agent 4: Budget<br/>Cost analysis & ROI"]
    H --> M["📱 Agent 5: Implementation<br/>Tools & execution plan"]
    
    I --> N["🎯 Integrated Results<br/>Comprehensive deliverable"]
    J --> N
    K --> N
    L --> N
    M --> N
    
    G --> O["✅ User Reviews Results<br/>Immediate feedback & iteration"]
    N --> O
    
    O --> P{"😊 Satisfied?"}
    P -->|No| Q["🔄 Refinement Request<br/>Specific improvements"]
    P -->|Yes| R["🏆 Project Complete<br/>Ready for implementation"]
    
    Q --> H
    
    style A fill:#e1f5fe
    style R fill:#e8f5e8
    style H fill:#fff3e0
    
    classDef agent fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef result fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    
    class I,J,K,L,M agent
    class G,N,R result
```

## System Architecture Overview
*For use in: 06_ORCHESTRATION.md*

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI1["🖥️ Web Interface<br/>ui_web.py"]
        UI2["💻 Terminal Interface<br/>ui_terminal.py"]
        UI3["📱 CLI Commands<br/>mao_v4.py"]
    end
    
    subgraph "Orchestrator Core"
        ORCH["🧠 Agent Orchestrator<br/>agent_orchestrator.py"]
        CB["📞 Agent Callback<br/>agent_callback.py"]
        CACHE["💾 Cache System<br/>cache_system.py"]
    end
    
    subgraph "Configuration Management"
        CONFIG["⚙️ Config Manager<br/>config/"]
        MODELS["🤖 Model Configs<br/>models/"]
        PROVIDERS["🔌 Provider Configs<br/>providers/"]
        WORKFLOWS["📋 Workflow Configs<br/>workflows/"]
    end
    
    subgraph "Tool Ecosystem"
        TOOLS["🔧 Tool Registry<br/>tools/"]
        MCP["🔗 MCP Connector<br/>mcp_connector.py"]
        SEARCH["🔍 Search Tools<br/>web_search/, brave_search/"]
        FILES["📁 File Operations<br/>file_operations.py"]
        CODE["💻 Code Execution<br/>code_execution.py"]
    end
    
    subgraph "Analytics & Memory"
        ANALYTICS["📊 Analytics System<br/>analytics/"]
        MEMORY["🧠 Memory Persistence<br/>user_memory.py"]
        LOGS["📜 Activity Logs<br/>activity_logger.py"]
    end
    
    subgraph "External Integrations"
        ANTHROPIC["🤖 Anthropic API<br/>Claude Models"]
        APIS["🌐 External APIs<br/>Various Providers"]
        GITHUB["📚 GitHub Integration<br/>webhook_handler.py"]
    end
    
    UI1 --> ORCH
    UI2 --> ORCH
    UI3 --> ORCH
    
    ORCH --> CB
    ORCH --> CACHE
    ORCH --> CONFIG
    ORCH --> TOOLS
    ORCH --> ANALYTICS
    
    CB --> MEMORY
    CB --> LOGS
    
    TOOLS --> MCP
    TOOLS --> SEARCH
    TOOLS --> FILES
    TOOLS --> CODE
    
    CONFIG --> MODELS
    CONFIG --> PROVIDERS
    CONFIG --> WORKFLOWS
    
    ORCH --> ANTHROPIC
    TOOLS --> APIS
    ANALYTICS --> GITHUB
    
    style ORCH fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    style CACHE fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    style ANALYTICS fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
```

## Data Flow Sequence Diagram
*For use in: 05_INTERFACE.md*

```mermaid
sequenceDiagram
    participant User
    participant Interface
    participant Orchestrator
    participant Cache
    participant Tools
    participant Provider
    participant Analytics
    
    User->>Interface: "/goal 'create marketing plan'"
    Interface->>Orchestrator: Parse and validate request
    
    Orchestrator->>Cache: Check for existing workflow
    Cache-->>Orchestrator: Cache miss/hit result
    
    alt New Workflow
        Orchestrator->>Orchestrator: Analyze goal complexity
        Orchestrator->>Tools: Load required tools
        Tools-->>Orchestrator: Tool configurations
        
        Orchestrator->>Provider: Initialize AI model
        Provider-->>Orchestrator: Model ready
        
        loop For each parallel agent
            Orchestrator->>Provider: Send agent task
            Provider-->>Orchestrator: Agent response
            Orchestrator->>Analytics: Log agent activity
        end
        
        Orchestrator->>Cache: Store workflow state
        Orchestrator->>Analytics: Record completion metrics
    end
    
    Orchestrator->>Interface: Formatted results
    Interface->>User: Display comprehensive output
    
    User->>Interface: "/continue with revisions"
    Interface->>Orchestrator: Continue workflow request
    
    Orchestrator->>Cache: Load workflow state
    Cache-->>Orchestrator: Previous context
    
    Orchestrator->>Provider: Process revisions
    Provider-->>Orchestrator: Updated results
    
    Orchestrator->>Analytics: Update performance data
    Orchestrator->>Interface: Revised output
    Interface->>User: Updated deliverables
```

## Memory & Analytics Integration
*For use in: 07_ANALYTICS_MEMORY.md*

```mermaid
graph LR
    subgraph "Data Collection Points"
        A["👤 User Interactions<br/>Commands, goals, feedback"]
        B["🤖 Agent Activities<br/>Tool usage, decisions, outputs"]
        C["⚡ System Performance<br/>Response times, cache hits, errors"]
        D["📊 Workflow Metrics<br/>Completion rates, complexity scores"]
    end
    
    subgraph "Analytics Engine"
        E["📈 Activity Logger<br/>Real-time event capture"]
        F["🔄 Data Aggregator<br/>Pattern recognition"]
        G["💾 Memory Persistence<br/>Cross-session storage"]
        H["📊 Performance Tracker<br/>Efficiency calculations"]
    end
    
    subgraph "Intelligence Enhancement"
        I["🧠 Learning Patterns<br/>User preferences"]
        J["⚡ Optimization Engine<br/>Workflow improvements"]
        K["🎯 Predictive Analysis<br/>Success probability"]
        L["📋 Recommendation System<br/>Next actions"]
    end
    
    subgraph "Output & Feedback"
        M["📊 Analytics Dashboard<br/>Visual metrics"]
        N["🔍 Insight Reports<br/>Performance summaries"]
        O["⚙️ System Optimization<br/>Automatic tuning"]
        P["💡 User Guidance<br/>Proactive suggestions"]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    E --> G
    E --> H
    
    F --> I
    G --> I
    H --> J
    
    I --> K
    J --> K
    K --> L
    
    L --> M
    L --> N
    J --> O
    I --> P
    
    G -.->|"Cross-session<br/>memory"| I
    O -.->|"Feedback loop"| F
    
    style E fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style I fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    style J fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
```

---

## Usage Instructions

1. **Copy the entire mermaid code block** (including ```mermaid and ```)
2. **Paste directly into markdown files** where you want the diagram to appear
3. **GitHub Pages with Jekyll** will automatically render these as interactive diagrams
4. **Customize colors and styling** by modifying the `style` and `classDef` lines

## Additional Diagrams Needed

- **Tool Integration Flow** - How button snippets are created and used
- **Cross-Session State Management** - Memory persistence between sessions  
- **Multi-Instance Communication** - How multiple Mao instances could coordinate
- **Security & Privacy Flow** - Local vs cloud processing visualization