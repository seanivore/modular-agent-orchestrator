# Getting Mao Ready for Dev Launch  
*Implementing our way to global subscription finish line* 

---

- **FOR FILE UPDATE:** If you read using the retrieval method first, then you can either tell me what sections to delete outright, or if it is complicated (like if we're updating actual code after these docs), then you might want to either read_file and tell me the exact lines to delete, or read_file and then edit_file yourself; just be careful if you do that because we want to try to avoid you needed to write entire long files at all costs. The more we can avoid that, the longer we'll be able to keep this context window going.

---

## Launch Intentions  

  1. Files have been validated and tested 
  2. The application has not actually been launched for real testing yet 
  3. The application will be setup to work in the terminal just for development purposes 
  4. Then we will implement it into a web app 

### Progress 

1. We've updated the documentation 
   - To reflect that there is no "terminal" or "TypeScript" UI 
   - We left gaps for the web UI info 
2. Fixing MCP servers 
   - Some "MOCK" code was added 
   - MCP servers we do not use were added as "fallback" 
   - There already is an actual fallback, so we're setting that up 
   - All but the `memory` MCP server will be removed 
   - All hardcoding is removed; MCP servers are a config collection item 
   - The details for setting up STDIO MCP Servers was added to `./documentation/10_AI_DEV_INDEX.md` documentation 
   - We've added a note to turn the MCP file into a directory on our `./versioning/v4_2_0/v4_2_0_MUST_UPDATE.md` document 

### Current State Assessment 

* **Audit Results:**

- Python Backend: "PRODUCTION READY with 95%+ compliance"
- Entry Point: mao_v4.py with CLI routing 'working' (according to testing)
- Basic Orchestration: Core workflow execution 'functional' 
- Tool System: Basic tool integration 'operational'
- Error Handling: Professional error handling 'implemented'
- Caching: CacheManager instances 'working' (according to testing)

* **What's Missing:**

- Parallel agent execution (the 01a, 01b async stuff)
- Timer-triggered workflows (the recurring automation)

---

## MCP Server & "Mock" Code 

* **GOAL:** 
- *Remove ALL Mock classes* - they block real functionality  
- *Replace with proper fallbacks* - LocalFilesFallback, LocalMemoryFallback, empty configs
- *Fix print statements* - use logging instead
- *Remove hardcoded servers* - use config system only

* **STATUS:**
- *memory_mcp.py* - FIXED (MockMemoryMCP deleted, STDIO MCP approach ready)
- *mcp_servers.json* - UPDATED (memory MCP server added)
- *agent_callback.py* - FIXED (Mock content generation removed, real file operations via Files API)

### To Be Fixed 

#### 1. `agent_callback.py` (3,283 tokens)
* **Violation:** Line 159 - `file_content = f"Mock content for {file_ref}"` **FIXED**

--> NEED TO SEARCH AND REMOVE HARDCODED RECOMMENDATIONS; DEFINED: `./versioning/MEM_STATE.md`

#### 2. `files_api.py` (4,563 tokens) 
**Violations:** 
- `MockFilesAPI` class (lines ~430-500)
- Print statements (lines 399, 415, 424)

* **Fix:** Delete MockFilesAPI class, keep LocalFilesFallback (documented fallback)
* **Approach:** Delete entire Mock class, replace print statements with logging

#### 3. `mcp_connector.py` (4,115 tokens)
**Violations:**
- Hardcoded server creation in `load_server_configs()` 
- `MockServerConnection` class  
- Print statements (lines 111, 113, 124, 272, 437, 441)

**Fix:** Remove hardcoded "aider" and "filesystem" servers, delete Mock class
**Approach:** Clean up server config loading, remove all Mock implementations

#### 4. `manager_tools.py` (4,935 tokens)
* **Violation:** Need to check for mock implementations in tool discovery

* **Fix:** Ensure all tool discovery uses real file scanning, no mock data
**Approach:** Read file first to identify specific mock violations

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
  2. Core dog-fooding functionality (goal → workflow → results)
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
