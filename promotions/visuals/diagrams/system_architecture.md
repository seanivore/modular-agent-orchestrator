# System Architecture Overview
*For use in: 06_ORCHESTRATION.md - Showcasing Mao's plug-and-play modularity*

## Plug & Play Architecture

```mermaid
flowchart TD
    subgraph USER_SPACE["User Space"]
        USER["User Input<br/>'Create marketing campaign'"]
    end
    
    subgraph CORE["Mao Core Orchestrator"]
        GOAL["Goal Analysis<br/>Determine requirements"]
        PLAN["Workflow Planning<br/>Select optimal tools/models"]
        EXECUTE["Execution Engine<br/>Coordinate parallel agents"]
    end
    
    subgraph PLUG_PLAY["Plug & Play Ecosystem"]
        TOOLS["🔧 Tool Registry<br/>Auto-discovered"]
        MODELS["🤖 Model Registry<br/>JSON configured"]
        PROVIDERS["🌐 Provider Registry<br/>API integrated"]
    end
    
    subgraph NEW_ADDITIONS["Easy Integration"]
        NEW_TOOL["New Tool<br/>Drop in tools/ directory<br/>+ JSON config = Ready!"]
        NEW_MODEL["New Model<br/>Add JSON config<br/>Instantly available"]
        MCP_TOOL["MCP Server<br/>Register once<br/>Use everywhere"]
    end
    
    subgraph EXECUTION["Smart Execution"]
        PARALLEL["Parallel Agents<br/>5 simultaneous<br/>tasks running"]
        CACHE["Smart Caching<br/>Hybrid local+cloud<br/>performance boost"]
        MEMORY["Memory MCP<br/>Cross-session<br/>continuity"]
    end
    
    USER --> GOAL
    GOAL --> PLAN
    PLAN --> EXECUTE
    
    PLAN -.-> TOOLS
    PLAN -.-> MODELS  
    PLAN -.-> PROVIDERS
    
    NEW_TOOL --> TOOLS
    NEW_MODEL --> MODELS
    MCP_TOOL --> TOOLS
    
    EXECUTE --> PARALLEL
    EXECUTE --> CACHE
    EXECUTE --> MEMORY
    
    %% JSON Examples
    TOOLS --> JSON1["brave_search.json<br/>perplexity_search.json<br/>dalle_generate.json<br/>+50 more tools"]
    MODELS --> JSON2["claude-sonnet-4.json<br/>claude-opus-4.json<br/>gpt-4.json<br/>+any model"]
    PROVIDERS --> JSON3["anthropic-direct.json<br/>openai-direct.json<br/>litellm.json<br/>+any provider"]
    
    %% Styling for visual impact
    style USER_SPACE fill:#e8f4fd
    style CORE fill:#fff3e0
    style PLUG_PLAY fill:#f3e5f5
    style NEW_ADDITIONS fill:#e8f5e8
    style EXECUTION fill:#fef7ff
    
    style NEW_TOOL fill:#4caf50,color:#ffffff
    style NEW_MODEL fill:#2196f3,color:#ffffff
    style MCP_TOOL fill:#9c27b0,color:#ffffff
    
    classDef jsonConfig fill:#ffeb3b,stroke:#f57f17,stroke-width:2px,color:#333333
    class JSON1,JSON2,JSON3 jsonConfig
```

## Claude Code Integration Vision

```mermaid
flowchart LR
    subgraph USER_REQUEST["User Conversation"]
        ASK["'I need a tool that<br/>analyzes competitor pricing'"]
    end
    
    subgraph CLAUDE_CODE["Claude Code Magic"]
        ANALYZE["Analyze Request<br/>Determine tool specs"]
        GENERATE["Generate Tool<br/>Complete 4-file structure"]
        DEPLOY["Auto-Deploy<br/>Instantly available"]
    end
    
    subgraph AUTO_CREATION["Automatic Creation"]
        MAIN["competitor_analysis.py<br/>Core logic + classes"]
        BUTTON["button_competitor_analysis.py<br/>Snippet generation"]
        UI["ui_competitor_analysis.py<br/>Display formatting"]
        CONFIG["tool_competitor_analysis.json<br/>Configuration"]
    end
    
    subgraph INSTANT_USE["Immediate Usage"]
        AVAILABLE["Tool now in registry<br/>Ready for workflows"]
        WORKFLOW["Next workflow can<br/>use new tool immediately"]
    end
    
    ASK --> ANALYZE
    ANALYZE --> GENERATE
    GENERATE --> DEPLOY
    
    DEPLOY --> MAIN
    DEPLOY --> BUTTON
    DEPLOY --> UI
    DEPLOY --> CONFIG
    
    MAIN --> AVAILABLE
    BUTTON --> AVAILABLE
    UI --> AVAILABLE
    CONFIG --> AVAILABLE
    
    AVAILABLE --> WORKFLOW
    
    %% Emphasis on the magic
    style CLAUDE_CODE fill:#6c5ce7,color:#ffffff
    style AUTO_CREATION fill:#00cec9,color:#ffffff
    style INSTANT_USE fill:#00b894,color:#ffffff
    
    style ASK fill:#fdcb6e
    style WORKFLOW fill:#e17055,color:#ffffff
```

## Usage Notes
- **First diagram:** Shows how easy it is to add new tools/models via JSON
- **Second diagram:** Illustrates Claude Code's tool generation capability
- Perfect for demonstrating "drag & drop" modularity to investors/users
- Emphasizes the JSON-based configuration simplicity