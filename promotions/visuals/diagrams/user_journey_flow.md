# User Journey Flow Diagram
*For use in: 03_USER_FLOW.md - Dual perspective showing user experience and Mao's orchestration*

## Enhanced Version (Better Legibility)

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
    
    %% Enhanced color scheme for better contrast
    style A1 fill:#003366,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style E1 fill:#004d00,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style I1 fill:#660066,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style J1 fill:#b30000,stroke:#ffffff,stroke-width:2px,color:#ffffff
    
    style A2 fill:#000080,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style E2 fill:#006600,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style I2 fill:#800080,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style J2 fill:#cc0000,stroke:#ffffff,stroke-width:2px,color:#ffffff
    
    classDef userSide fill:#f0f8ff,stroke:#003366,stroke-width:3px,color:#003366
    classDef maoSide fill:#fff0ff,stroke:#660066,stroke-width:3px,color:#660066
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2 maoSide
```

## Alternate High-Contrast Version

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
    
    %% High contrast version for maximum legibility
    style USER fill:#000000,stroke:#ffffff,stroke-width:4px,color:#ffffff
    style MAO fill:#333333,stroke:#ffffff,stroke-width:4px,color:#ffffff
    
    classDef userSide fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000
    classDef maoSide fill:#f0f0f0,stroke:#333333,stroke-width:2px,color:#000000
    
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 userSide
    class A2,B2,C2,D2,E2,F2,G2,H2,I2,J2,K2 maoSide
```

## Usage Notes
- **Enhanced Version:** Better for web display with improved contrast
- **High-Contrast Version:** Maximum legibility for presentations
- Both versions maintain the dual-perspective concept
- Colors can be further customized by modifying the style lines