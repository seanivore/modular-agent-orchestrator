# Mao Standardization Rules
*Critical standardization rules for context priming to review before each session* 

---

Find: Core principles, production and development guidelines, CRITICAL implementation rules, copywriting MUST FOLLOW guide, technical architecture and development guidelines. 

---

## Core Principles
**All JSON config files must be standalone, atomic units**
- Easy to add/remove/update individual components
- Directory scanning for live discovery
- No hardcoded lists, categories, enums, predetermined options
- Template-based consistency
- Mao is a single-screen, chat-based UI app; no menus, navigation, or complex UI chrome
- No emoji icons; use text-based visual hierarchy; conceptual semantic highlighting 
- We have only 4 colors, character choice, and whitespace to work with 
- NO BACKWARDS COMPATIBILITY, LEGACY ALIASES, OR COMPATIBILITY LAYERS
- Memory MCP is single source of truth AND ONLY STATE MANAGEMENT SYSTEM 
- Setup scripts create executable commands in `/Users/seanivore/bin`; proven pattern 
- Setup scripts do not put hyphens in command line, only spaces 

## Development Guidelines 
- Always use CacheManager, @handle_errors, and estimate_cost() in MAO files
- Follow FILE_STANDARDIZATION_RULES.md - no emoji icons, text-based visual hierarchy
- Use modular JSON discovery patterns, never hardcode file lists or mappings
- Follow 4-file tool structure: logic.py, button_*.py, ui_*.py, tool_*.json
- Use 'name' field in JSON configs, flat path structures, simplified operations
- CLI commands need 3 files: command.py, ui_command.py, command.json
- Memory MCP is single source of truth for all workflow state
- Use filesystem tools over artifacts for accuracy in Mao implementations
- Everything modular, everything discoverable via directory scanning
- Delta-only storage for settings - only store changes from defaults
- Conversation-driven interfaces only - no menus, navigation, or complex UI chrome

---

## Production Ready
- **NAMING** this is the product; don't put Mao or Mao-v4 in code or files
- **GENERIC HEADERS** do not mention version or brand  
- **REAL ONLY** no mock data ever in Mao ecosystem
- **IMPLEMENT IN FULL** not partial, no time limit, no rush a task is done when it is good

### Privacy and Analytics
- Maintain privacy architecture; user analytics deletable, system analytics anonymous
- User data in ./configs/user/[username]/ easily deletable for GDPR compliance
- All analytics require secondary anonymization; UserID is only tracker 

---

## Critical Implementation Rules 
- Abbreviate implementation in file name to **IMPL**
- Create directory in versioning folder; use naming structure: `IMPL_[UPDATE_NAME]`
- Directory may hold any prep. files, but final is named `IMPL_[UPDATE_NAME].md`
- Implementation document MUST BE MORE THOROUGH THAN TECHNICAL DOCUMENTATION 
- We will be keeping internal documentation more robust than public documentation 
- The update will NOT move forward until the implementation document is complete 
- Include ALL necessary logic, explained verbally; directory and files to create 
- Config files must have a JSON schema, template, and guide for creating, for example, a new tool 

### Development Workspace 
- Token conscious work: Use filesystem for persistent reference  
- Artifacts use fewer tokens than write_file 
- Full codebase in Project Knowledge; retrieval is not persistent reference 
- ALWAYS use sequential thinking before, during, and in review of tasks 
- Update Memory MCP with Project State before task, during, and after 

### Copywriting Styles Guide 
**PRACTICE AT ALL TIMES; FOR OURSELVES, IN APP, MARKETING** 
  1. Never use "MAO" in caps; it is a proper noun; their NAME is Mao
  2. Never use an m-dash or regular dash - in the middle of a sentence; use semicolon  
  3. Do not put markdown heading in bold or italics; use for variant emphasis 
  4. We only use military time; do not write AM or PM; eastern timezone 
  5. Write long date in EU format: 21 July 2025; short date: YYYY-MM-DD 

---

## MAO IS NOT
- ❌ **API provider or cloud service** (no web server, REST endpoints)
- ❌ **NOT A WEB OR MOBILE APP** (no HTML, CSS, web browsers)
- ❌ **NOT a SaaS** (no remote hosting of the app)

## MAO IS
- ✅ **Local terminal app** (on user's device)
- ✅ **Self-contained Python backend** (mao_v4.py + modules)
- ✅ **Local TypeScript/Node.js terminal UI** (beautiful terminal interface)
- ✅ **Subprocess communication** (Node.js ↔ Python via stdin/stdout/IPC)
- ✅ **Local file system** (all configs, data, logs stored locally)
- ✅ **API consumer** (calls OpenAI, Anthropic, search APIs, etc.)
- ✅ **Personal productivity tool** (like Claude Code, not like web apps)
- ✅ **Future subscription model** (download configs/tools/workflows)

### THINK 
 - Desktop app, not web app 
 - Subprocess calls, not API calls 
 - Local files, not HTTP requests 
 - Terminal interface, not browser interface 
 - Personal tool, not multi-user service 

## FUTURE VISION IS STILL LOCAL FIRST 
1. **Phase 1:** Local terminal application (current focus)
2. **Phase 2:** Local desktop application (Electron/Tauri wrapper)
3. **Phase 3:** Mobile application (running locally on phone/tablet)
4. **Phase 4:** Optional analytics aggregation (collect from multiple local instances)

## TECHNICAL ARCHITECTURE
```
User's Local Machine
├── TypeScript/Node.js Terminal UI (frontend)
│   ├── Rich terminal interface
│   ├── User input handling
│   └── Subprocess management
├── Python Backend (mao_v4.py)
│   ├── Core orchestration logic
│   ├── Tool ecosystem
│   ├── CLI commands
│   └── Local file operations
└── External API Calls
    ├── OpenAI/Anthropic APIs
    ├── Search APIs (Brave, Perplexity)
    ├── Other service APIs
    └── Future: Config/workflow downloads
```
---

## Development Guidelines 

### 1. Standard Imports (Top of File)
```python
# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()
```

### 2. Required Functions
```python
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    # Implementation specific to component
    pass
```

### 3. Error Handling Decorators
```python
@handle_errors(operation_name="component_name", return_dict=True)
def main_function(self, params):
    # Function implementation
    pass
```

### 4. Standard Caching Pattern
```python
# Get from cache first
cache_key = f"{param1}|{param2}|{param3}"
cached_result = cache.get_cached_analysis(cache_key, "component_name")
if cached_result:
    return json.loads(cached_result)

# Process and cache result
result = process_data()
cache.cache_content_analysis(cache_key, json.dumps(result), "component_name")
```

### 5. Standalone Functions (For Button Imports)
```python
# At end of file - functions that button files can import
def standalone_function_name(params) -> return_type:
    """Standalone function for button file imports"""
    manager = ComponentManager()
    return manager.method_name(params)
```

---

## Documentation Writing Principles

### Writing Style (Following Anthropic Docs Approach)
- **Narrative prose over bullet points** as primary structure
- **Brief paragraphs** for accessibility and readability
- **Natural weaving** of technical architecture within narrative story
- **NO separate technical sections** - integrate code explanations throughout
- **Pattern:** Brief text → code architecture → more text → code architecture
- **Audience:** Accessible to both technical and marketing/pitch audiences

### Documentation Rules
- **Never delete existing writing** - suggest edits only
- **Use semicolons instead of m-dashes** in narrative flow
- **No emoji icons** - text-based visual hierarchy only
- **No bullet points as primary narrative device** - prose first
- **Brief paragraphs** with comprehensive coverage

---

## CLI Command Requirements

### CLI Structure (3 Files Required)
1. `[command_name].py` - Main command logic
2. `ui_[command_name].py` - Display components
3. `[command_name].json` - Command configuration

### CLI JSON Configuration
```json
{
    "name": "command_name",
    "help": "Command description",
    "terminal_flag": "--flag",
    "type": "command_type",
    "file_path": "configs/cli/command_name/command_name.py",
    "ui_path": "configs/cli/command_name/ui_command_name.py"
}
```

---

## Context Priming Strategy

### Two-Document System for AI Development
**Efficient context priming without reading all comprehensive documentation**

#### **CLAUDE.md (This Document) - "Rules & Principles"**
**Contains:**
- Core development principles and constraints
- Standardization requirements and quality control
- Code patterns and architectural guidelines
- Writing style rules and copywriting standards
- Error handling, caching, and import requirements
- "HOW TO WORK" with Mao codebase

**Use for:** Understanding project standards, development approach, and coding requirements

#### **documentation/09_DEV_PRIMER.md - "Templates & Creation Guides"**
**Contains:**
- Step-by-step config creation guides
- JSON templates with examples
- Directory structure examples
- File naming conventions with samples
- Implementation patterns with code examples
- "HOW TO CREATE" each type of Mao component

**Use for:** Actually building new tools, CLI commands, configs, and components

#### **Memory MCP - "Project State Updates"**
**Contains:**
- Current task progress and status
- Session-specific decisions and changes
- Dynamic project state information
- Context for ongoing work

**Use for:** Picking up where previous sessions left off

### **Context Priming Workflow**
1. **Start every session:** Read CLAUDE.md (rules and standards)
2. **When creating components:** Reference 09_DEV_PRIMER.md (templates and guides)
3. **For project continuity:** Search Memory MCP for current state
4. **Skip comprehensive docs:** Unless specific technical details needed

---

## Tool-Specific Requirements

### Tool Structure (4 Files Required)
1. `[tool_name].py` - Main logic file
2. `button_[tool_name].py` - Button snippet generation
3. `ui_[tool_name].py` - Display and UI components  
4. `tool_[tool_name].json` - Configuration and metadata

### Button Files Pattern
```python
def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """Single entry point for button snippet generation"""
    operation = params.get("operation", "default_operation")
    
    if operation == "operation1":
        return _create_operation1_snippet(params, model)
    elif operation == "operation2":
        return _create_operation2_snippet(params, model)
    else:
        return _create_default_snippet(params, model)

# Private helper functions only
def _create_operation1_snippet(params: Dict[str, Any], model: str) -> str:
    # Use imports from main logic file, not duplicated code
    pass
```

### JSON Configuration Schema
```json
{
    "name": "component_name",
    "version": "1.0.0", 
    "description": "Component description",
    "file_path": "path/to/main.py",
    "button_path": "path/to/button_main.py",
    "ui_path": "path/to/ui_main.py",
    "operations": {
        "operation_name": {
            "description": "What this operation does",
            "required_params": ["param1", "param2"],
            "optional_params": ["param3"]
        }
    },
    "models_supported": ["all"],
    "cost_estimate": 0.001
}
```

---

## Quality Control Checklist

### Before Creating Any File:
- [ ] Does this follow the 4-file pattern (if applicable)?
- [ ] Are all standard imports included?
- [ ] Is `estimate_cost()` function present?
- [ ] Are error handling decorators applied?
- [ ] Is caching pattern implemented correctly?
- [ ] Are standalone functions provided for imports?
- [ ] No emoji icons or version numbers in headers?

### Button File Specific:
- [ ] Single `create_button_snippet()` entry point?
- [ ] Operation-based dispatch pattern?
- [ ] Imports from logic file (no code duplication)?
- [ ] Private helper functions only?
- [ ] No hardcoded paths or metadata?

### JSON File Specific:
- [ ] Uses `"name"` field (not `"id"` or `"tool_id"`)?
- [ ] Flat path structure (`file_path`, `button_path`, `ui_path`)?
- [ ] Simplified `operations` object structure?
- [ ] No nested or overly complex parameter definitions?

---

**Remember: Prevention over correction. Follow these patterns from the start rather than fixing violations later.**

---