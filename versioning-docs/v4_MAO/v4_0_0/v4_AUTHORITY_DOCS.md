# MAO v4 Authority Documentation
**Project Constitution & Blueprint**

*If all AI disappeared tomorrow, this document contains everything needed to understand, maintain, and complete MAO.*

---

## 🎯 WHAT IS MAO?

**MAO (Modular Agent Orchestrator)** is a revolutionary AI workflow system that eliminates the complexity of AI tool integration through:

- **95% Cost Reduction**: From $0.07+ to <$0.01 per workflow via token optimization
- **Universal Model Support**: Works with ANY AI model/provider via "human buttons"
- **Zero Configuration**: Natural language goals become executable workflows
- **Variable-Input Philosophy**: No hardcoded specifics - tools are blank canvases

**Core Innovation**: Human Button Interface - generates executable code snippets instead of managing SDKs, eliminating "it's complicated" responses and format conversion hell.

---

## 🏛️ ARCHITECTURAL DECISIONS (DO NOT CHANGE)

### 1. Variable-Input Philosophy 🎨
**Decision**: No hardcoded categories, templates, or domain-specific assumptions in ANY code.
**Reasoning**: Maximum flexibility - let prompts define specifics, not code.
**Protected Pattern**: Tools are blank canvases, workflows are dynamic.

```python
# ✅ CORRECT - Variable input
def analyze_content(content: str, analysis_approach: str) -> Dict:
    """Let the prompt define the approach"""

# ❌ FORBIDDEN - Hardcoded specifics  
analysis_types = ["financial", "marketing", "technical"]
```

### 2. Human Button Interface 🔘
**Decision**: Generate executable code snippets instead of managing multiple SDKs.
**Reasoning**: Universal compatibility without conversion complexity.
**Protected Pattern**: All tools have `create_button_snippet()` functions.

**DO NOT**: Convert back to SDK-based approach or provider-specific implementations.

### 3. 4-File Tool Architecture 📁
**Decision**: Every tool follows exact same pattern:
- `toolname.py` - Core logic (NO print statements)
- `ui_toolname.py` - Display formatting (print statements OK)  
- `button_toolname.py` - Human button generators (print statements OK for demo)
- `tool_toolname.json` - Metadata and discovery

**Reasoning**: Clean separation enables maintenance, testing, and UI flexibility.
**Protected Pattern**: Never merge these concerns back into monolithic files.

### 4. Manager Component Separation 🎭
**Decision**: Separate managers for models, buttons, tools, cache.
**Reasoning**: Single responsibility, easy testing, modular replacement.
**Protected Files**:
- `manager_models.py` - Model selection and cost optimization
- `manager_buttons.py` - Button generation coordination  
- `manager_tools.py` - Tool discovery and metadata
- `cache_system.py` - Fingerprinting and cost optimization

**DO NOT**: Merge these back into monolithic orchestrator file.

### 5. UI Separation 🖼️
**Decision**: NO print statements in core logic files.
**Reasoning**: Enables multiple interfaces (terminal, web, API) without code changes.
**Protected Rule**: Print statements ONLY in `ui_*.py` and `interfaces/` files.

**Exception**: Print statements in button generators are intentional for demo purposes.

---

## 🛠️ CURRENT ARCHITECTURE STATUS

### ✅ COMPLETED COMPONENTS

#### Core Orchestrator (`orchestrator/`)
- **`core.py`** - Main workflow orchestration logic
- **`manager_models.py`** - Dynamic model selection (renamed from `model_manager.py`)
- **`manager_buttons.py`** - Button generation coordination (renamed from `human_buttons.py`) 
- **`manager_tools.py`** - Tool discovery and metadata (renamed from `tool_discovery.py`)
- **`error_handling.py`** - Shared error handling with retry logic
- **`cache_system.py`** - Fingerprinting cache with 5,108x speed improvements

#### Standardized Tools (`tools/*/`)
All 8 tools follow identical 4-file pattern:

1. **brave_search** - Web search via Brave API
2. **dalle_generate** - AI image generation  
3. **file_operations** - File system operations
4. **graphic_design** - Image editing and text overlay
5. **perplexity_search** - Research via Perplexity API
6. **text_editor** - Text processing and formatting
7. **think** - Enhanced thinking and analysis
8. **web_search** - General web search operations

**Standardization Completed**: All tools have `create_button_snippet()` functions, correct import statements, clean UI separation.

#### Configuration System (`configs/`)
- **JSON Model Configs** - Individual files per model with capabilities, costs, limits
- **JSON Provider Configs** - Provider connection patterns and authentication  
- **Tool Registry** - Metadata for dynamic tool discovery
- **Connection Mappings** - Model-to-tool compatibility matrices

#### Interface Layer (`interfaces/`)
- **`terminal.py`** - Clean terminal interface with verbose mode
- **`web.py`** - Web interface foundation (future)

### 🔗 INTEGRATION STATUS

#### ✅ Working Integrations
- **Cache System** - Fingerprinting working across all tools
- **Tool Standardization** - All 8 tools follow same patterns
- **Model Management** - Dynamic selection and cost optimization
- **Error Handling** - Shared patterns across all components
- **UI Separation** - Clean vs verbose output modes

#### ⚠️ Partial Integrations  
- **Tool Discovery** - `manager_tools.py` exists but not connected to `core.py`
- **Protocol Documentation** - `protocol.md` file exists but empty
- **Memory System** - `memory.py` file exists but empty

---

## 🚨 CRITICAL "DO NOT CHANGE" RULES

### 1. File Naming Convention 📛
**DO NOT** rename these standardized files:
- `manager_models.py` (NOT `model_manager.py`)
- `manager_buttons.py` (NOT `human_buttons.py`)  
- `manager_tools.py` (NOT `tool_discovery.py`)
- `cache_system.py` (NOT `hybrid_cache.py`)

**Class Names**: 
- `ModelManager` (NOT `UniversalModelManager`)
- `ButtonManager` (NOT `HumanButtonInterface`)
- `ToolManager` (NOT `ToolDiscovery`)
- `CacheManager` (NOT `HybridCacheManager`)

### 2. Import Patterns 📥
**Correct Import Pattern** (DO NOT CHANGE):
```python
from orchestrator.cache.cache_system import CacheManager
from orchestrator.manager_models import ModelManager
from orchestrator.manager_buttons import ButtonManager
from orchestrator.manager_tools import ToolManager
```

### 3. Function Naming 🔧
**All button files MUST have**: `create_button_snippet(params, model) -> str`
**DO NOT** use custom names like `create_dalle_generation_button` or `create_analysis_snippet`

### 4. Print Statement Rules 📢
- **FORBIDDEN**: Print statements in `orchestrator/*.py` and `tools/*/toolname.py`
- **ALLOWED**: Print statements in `tools/*/ui_*.py` and `interfaces/*.py`
- **INTENTIONAL**: Print statements in `tools/*/button_*.py` for demo purposes

### 5. Variable-Input Enforcement 🎨
**NEVER add back**:
- Hardcoded categories or templates
- "Choose your method" dropdown menus
- Domain-specific assumptions
- Predefined frameworks or use cases

---

## 🔄 WHAT STILL NEEDS TO BE BUILT

### Phase 1: Core Integrations (Session 18)

#### A. MCP API Connector ⭐ **HIGH PRIORITY**
- **What**: Model Context Protocol Server API integration
- **Why**: Latest Anthropic standard for AI tool communication
- **File**: Based on `.claude/TOOL_API_MCP_CONNECT.md`
- **Status**: Not started

#### B. Code Execution Tool 🎯 **CORE FEATURE**
- **What**: Direct Claude 4 Code Execution integration for human buttons
- **Why**: Makes buttons actually executable vs just code snippets
- **File**: Based on `.claude/TOOL_CODE_EXECUTION.md` 
- **Status**: Not started
- **Critical**: Must integrate with existing button system

#### C. Files API Integration 💾 **WORKFLOW ESSENTIAL**
- **What**: Anthropic Files API for agent handoffs and temp storage
- **Why**: Enables workflow continuity and agent communication
- **File**: Based on `.claude/TOOL_FILES_API.md`
- **Status**: Not started

#### D. Tool Discovery Connection 🔗 **MISSING LINK**
- **What**: Connect `manager_tools.py` to `core.py` for automatic tool discovery
- **Why**: Orchestrator currently can't discover available tools
- **Status**: Components exist, need integration
- **Effort**: Low - just wiring existing pieces

#### E. Protocol Documentation 📋 **BEHAVIOR SPECIFICATION**
- **What**: Complete `orchestrator/protocol.md` with MAO behavior patterns
- **Why**: Consistent AI behavior across all workflows
- **Status**: Empty file exists
- **Content Needed**: Decision trees, interaction patterns, escalation rules

### Phase 2: User Experience Flow (Session 19)

#### A. First-Time Setup Experience 🎬
**Missing Flow**: `Goal → MAO Setup → JSON Config → Custom Command → Ready!`

**Components Needed**:
- Setup conversation interface
- JSON config generation from natural language
- Custom command creation and installation
- Use case directory structure (`configs/use_case/*/`)

#### B. Workflow Execution Experience 🚀  
**Missing Flow**: `Custom Command → Workflow Execution → Results`

**Components Needed**:
- Seamless execution from generated commands
- Real-time progress monitoring
- Results presentation and storage
- Error handling and recovery

#### C. Configuration Management 📁
**Missing System**: JSON variable-input configs for repeatable workflows

**Components Needed**:
- Variable definition system (required vs optional)
- Use case templates (without hardcoded specifics)
- README generation for each workflow
- Command line argument processing

### Phase 3: Testing & Validation (Session 20)

#### A. End-to-End Testing 🧪
- Complete user journey testing (new user → working workflow)
- Multi-tool workflow testing  
- Cross-model compatibility testing
- Error handling and edge case coverage

#### B. Performance Validation 📊
- Verify 95% token reduction claims vs v3.3.0
- Confirm <$0.01 per workflow execution target
- Cache hit rate optimization
- Model selection efficiency analysis

#### C. Human Button Integration Testing 🔘
- Button generation across all supported models
- Claude 4 Code Execution integration testing
- Error handling and retry logic validation
- Cross-platform compatibility verification

---

## 📊 QUALITY METRICS & SUCCESS CRITERIA

### Performance Targets 🎯
- **Cost**: <$0.01 per workflow execution (vs $0.07+ in v3)
- **Speed**: <5 second cache hits, <30 second new workflows
- **Reliability**: 99%+ success rate for standard workflows
- **Efficiency**: 95% token reduction vs monolithic approaches

### User Experience Goals 👤
- **Setup Time**: New user to working workflow in <10 minutes
- **Learning Curve**: Zero technical knowledge required for basic usage
- **Flexibility**: Support any goal without code changes
- **Transparency**: Clear progress and cost visibility

### Technical Standards 🔧
- **Modularity**: Any component replaceable without affecting others
- **Testability**: Every component testable in isolation
- **Extensibility**: New tools addable via 4-file pattern
- **Maintainability**: Clear separation of concerns throughout

---

## 🚨 DANGER ZONES (Common AI Mistakes)

### 1. "Improving" the Variable-Input Philosophy
**AI Often Tries**: Adding categories, templates, or "helpful" presets
**Why It's Wrong**: Breaks the core philosophy of maximum flexibility
**Correct Response**: "This is intentionally variable - prompts define specifics"

### 2. "Simplifying" the 4-File Architecture  
**AI Often Tries**: Merging files for "simplicity" or "efficiency"
**Why It's Wrong**: Destroys separation of concerns and testing ability
**Correct Response**: "4-file pattern is intentional and protected"

### 3. "Modernizing" the Human Button Approach
**AI Often Tries**: Converting back to SDK-based approaches
**Why It's Wrong**: Reintroduces complexity and format conversion issues
**Correct Response**: "Human buttons solve SDK hell - don't go backward"

### 4. "Optimizing" Print Statement Locations
**AI Often Tries**: Adding print statements to core logic for "debugging"
**Why It's Wrong**: Breaks UI separation and multi-interface support
**Correct Response**: "Print statements only in UI layer - use return data"

### 5. "Enhancing" with Hardcoded Intelligence
**AI Often Tries**: Adding smart defaults, common patterns, or helpful shortcuts
**Why It's Wrong**: Violates blank canvas principle and limits flexibility
**Correct Response**: "Keep tools generic - let prompts provide specifics"

---

## 🎨 THE ART OF MAO

MAO is built on **principled simplicity**:
- **Fewer assumptions** = more flexibility
- **Cleaner separation** = easier maintenance  
- **Universal patterns** = broader compatibility
- **Variable inputs** = unlimited possibilities

**This documentation protects those principles while enabling continued evolution.**

---

*This is your blueprint. If all AI disappeared tomorrow, a human could pick up this document and continue building MAO exactly as intended.* 🎯