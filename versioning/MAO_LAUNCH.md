# Getting Mao Ready for Dev Launch  
*Implementing our way to global subscription finish line* 

---

**The note in "Update Documentation" section is helpful for all of the necessary tasks as we process through this document.**

---

## Current State Assessment 

* **✅ What Actually Works (Per Comprehensive Audit):**

- Python Backend: "PRODUCTION READY with 95%+ compliance"
- Core System: 7 MCP tools discovered, 4 MCP servers connected
- Entry Point: mao_v4.py with CLI routing working
- Basic Orchestration: Core workflow execution functional
- Tool System: Basic tool integration operational
- Error Handling: Professional error handling implemented
- Caching: CacheManager instances working

* **❌ What's Still Missing:**

- Parallel agent execution (the 01a, 01b async stuff)
- Timer-triggered workflows (the recurring automation)
- Advanced UI features (but we're pivoting away from that anyway!)

### Update Documentation 

We need to remove the information about the old UI. Instead of adding information about the new UI here, we will include it as a step in the IMPL documents. 

For the upcoming questions, the number 10 document is probably helpful. I think we'll want to update it to make the way to use MCP servers more clear, as I think we did something similar on that document for how to add each type of config collection items. 

Also on that document you'll see that we keep a list of all the dependencies, all the class names for each file, and all the methods/functions for each class. This is *IMPORTANT* to keep up to date because it prevent AI from grep'ing around everywhere and then guessing at the rest of the code when they find part of what they wanted. 

*NOTE: If you read using the retrieval method first, then you can either tell me what sections to delete outright, or if it is complicated (like if we're updating actual code after these docs), then you might want to either read_file and tell me the exact lines to delete, or read_file and then edit_file yourself; just be careful if you do that because we want to try to avoid you needed to write entire long files at all costs. The more we can avoid that, the longer we'll be able to keep this context window going.*

```
./documentation/
├── 00_OVERVIEW.md
├── 01_EVOLVING_AI.md
├── 02_REFERENCE.md
├── 03_USER_FLOW.md
├── 04_MAOS_FLOW.md
├── 05_INTERFACE.md
├── 06_ORCHESTRATION.md
├── 07_ANALYTICS_MEMORY.md
├── 08_AUTOMATE_INTELLIGENCE.md
├── 09_FUTURE_THINKING.md
└── 10_AI_DEV_INDEX.md
```

### Confirm All Tools Are Discoverable 

Re: "7 MCP tools discovered" from above. 
- There are 11 tools, though 'code_execution' and 'files_api' and only going to be used by Mao. 
- Agents might use 'mcp_connector', however, as of now it is only planned to be used by Mao to access the `memory` MCP server, Mao's 'one source of truth' for everything memory-related. 

```
./tools/
├── brave_search
│   ├── brave_search.py
│   ├── button_brave_search.py
│   ├── tool_brave_search.json
│   └── ui_brave_search.py
├── code_execution
│   ├── button_code_execution.py
│   ├── code_execution.py
│   ├── tool_code_execution.json
│   └── ui_code_execution.py
├── dalle_generate
│   ├── button_dalle_generate.py
│   ├── dalle_generate.py
│   ├── tool_dalle_generate.json
│   └── ui_dalle_generate.py
├── file_operations
│   ├── button_file_operations.py
│   ├── file_operations.py
│   ├── tool_file_operations.json
│   └── ui_file_operations.py
├── files_api
│   ├── button_files_api.py
│   ├── files_api.json
│   ├── files_api.py
│   ├── tool_files_api.json
│   └── ui_files_api.py
├── graphic_design
│   ├── button_graphic_design.py
│   ├── fonts
│   ├── graphic_design.py
│   ├── tool_graphic_design.json
│   └── ui_graphic_design.py
├── mcp_connector
│   ├── button_mcp_connector.py
│   ├── mcp_connector.py
│   ├── tool_mcp_connector.json
│   └── ui_mcp_connector.py
├── perplexity_search
│   ├── button_perplexity_search.py
│   ├── perplexity_search.py
│   ├── tool_perplexity_search.json
│   └── ui_perplexity_search.py
├── text_editor
│   ├── button_text_editor.py
│   ├── text_editor.py
│   ├── tool_text_editor.json
│   └── ui_text_editor.py
├── think
│   ├── button_think.py
│   ├── think.py
│   ├── tool_think.json
│   └── ui_think.py
└── web_search
    ├── button_web_search.py
    ├── tool_web_search.json
    ├── ui_web_search.py
    └── web_search.py
```

### Eliminate Unnecessary MCP Tools 

Re: "4 MCP servers connected" from above.
- I'm feeling very weird about this, because I have no idea what they are. 
- Meaning, I'm worried that they're probably hard-coded because we didn't set up a config system for MCP servers. 
- *Note: We should set up a config system for MCP servers* 
- Only the `memory` MCP server is essential, planned as Mao's 'one source of truth' for everything memory-related. 
- That one *might* be hard-coded; we should confirm, and then make sure we change things so that it is not because who knows if that MCP will or will not always be available. 

### Investigate and Eliminate "MOCK" Content In Code 

- `./orchestrator/agent_callback.py`
Line 159: "            file_content = f"Mock content for {file_ref}"

- `./orchestrator/manager_tools.py`
- `./orchestrator/memory_mcp.py`
Starting at Line 427 in the first, then Line 50 in the second. 
We have the `memory` MCP server, so there is no reason to have any mock code, not that "MOCK CODE" is ever acceptable. Seriously makes me so angry. 

---

## Two Main New IMPL Plans 

```
./versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_DEV_LIVE.md       ← Basic terminal functionality
./versioning/v4_1_0/IMPL_WEB_UI/IMPL_WEB_UI.md           ← Web app with terminal aesthetic
```

### IMPL_DEV_LIVE 

The directory is created. All of the remaining "IMPL-TO-LAUNCH" documents are in here to be pulled from and then deleted. These are noted below in the "Other Important IMPL Documents" section. 

```
./versioning/v4_0_0/IMPL_DEV_LIVE/
├── COMPREHENSIVE_IMPLEMENTATION_ROADMAP.md
├── IMPL_MULTILINGUAL_UI.md
├── IMPL_SUBSCRIPTION_SYSTEM.md
├── IMPL_UI_COMPLETE.md
└── IMPL_UI_DETAILED.md
```

#### Focus On 

  1. What actually works NOW (basic CLI commands, workflow execution)
  2. Core dogfooding functionality (goal → workflow → results)
  3. Basic tool integration (the 7 MCP tools that are discovered)
  4. Simple terminal interface (no fancy TypeScript, just Python CLI)

#### Must Complete 

- `./versioning/v4_0_0/IMPL_PARALLEL_AGENTS/IMPL_PARALLEL_AGENTS.md`

❌ IMPL_PARALLEL_AGENTS.md - NOT IMPLEMENTED
Status: Comprehensive spec but no code exists yet
Evidence: Documents states "What's Missing: Parallel Execution Logic, Phase Grouping, Async Coordination, UI Display"
File Checklist: Shows JSON config supports parallel (01a, 01b, 01c) but core.py executes sequentially

- `./versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md`

❌ IMPL_TRIGGER_WORKFLOWS.md - NOT IMPLEMENTED
Status: Comprehensive spec but no code exists yet
Evidence: Documents states "What's Missing: Trigger Logic, Workflow Execution, Async Coordination, UI Display"
File Checklist: Shows JSON config supports triggers (01a, 01b, 01c) but core.py executes sequentially

### IMPL_WEB_UI 

The directory is created, but only contains wire frames and some design and logic description documents. Here is what we need to add, and what each of those need to be added. 

```
./versioning/v4_1_0/IMPL_WEB_UI/
├── IMPL_ANALYTICS_ACCESSIBILITY.md       ← Review from location below, then move here
├── IMPL_ANTHROPIC_TOOLS/       ← Review from location below, then move here
├── IMPL_CLAUDE_CODE.md       ← Review from location below, then move here
├── IMPL_DATABASES.md       ← Review from location below, then move here
└── IMPL_WEB_UI.md       ← To be created 
```

#### We Can Leverage 

  1. Gradient terminal designs from your parallel volley funnel
  2. Existing Python backend API (just change the interface layer)
  3. Terminal aesthetic but web accessible
  4. Foundation for Discord/WhatsApp bots

#### Review And Then Move 

* **CLAUDE CODE `./versioning/v4_1_0/IMPL_CLAUDE_CODE/IMPL_CLAUDE_CODE.md`**
  - Should be pretty much done 
  - Need to add a method for the user to choose what model they want to use as Mao; Sonnet-4, Opus-4.1, or Claude Code as the default. 
  - Need a setting to change what the Claude Code model is and who the default is. 

* **ANALYTICS ACCESSIBILITY `./versioning/v4_1_0/IMPL_ANALYTICS/IMPL_ANALYTICS_ACCESSIBILITY.md`**
  - `./versioning/v4_1_0/IMPL_ANALYTICS/IMPL_ANALYTICS_ACCESSIBILITY.md`
  - `./versioning/v4_1_0/IMPL_ANALYTICS/MULTI_INSTANCE_DATA.md`
  - Should be pretty much done 
  - BUT, that plan was for collecting data from local apps on user's devices 
  - We probably need a new one for web app data collection

* **ANTHROPIC TOOLS `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/IMPL_ANTHROPIC_TOOLS.md`**
  - `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_BASH.md`
  - `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_FINE_GRAINED_STREAMING.md`
  - `./versioning/v4_1_0/IMPL_ANTHROPIC_TOOLS/TOOL_PARALLEL_USE.md`
  - These are just the documentation from Anthropic's website 
  - Probably needs further details after review

* **DATABASES `./versioning/v4_1_0/IMPL_DATABASES/IMPL_DATABASES.md`**
  - Might be pretty much done 
  - Needs review to confirm 

---

## Other Important IMPL Documents 

- Whatever remains from "IMPL_DEV_LIVE" header above. 
```
./versioning/v4_0_0/IMPL_DEV_LIVE/
├── COMPREHENSIVE_IMPLEMENTATION_ROADMAP.md
├── IMPL_MULTILINGUAL_UI.md
├── IMPL_SUBSCRIPTION_SYSTEM.md
├── IMPL_UI_COMPLETE.md
└── IMPL_UI_DETAILED.md
```

- Pull directory from these instead/as well as above, if needed. 

  - `./versioning/v4_1_0/IMPL_MULTILINGUAL/IMPL_MULTILINGUAL.md`
  - `./versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` 
  - `./versioning/v4_1_0/IMPL_WEBSITE/IMPL_WEBSITE_STOREFRONT.md` 

---
