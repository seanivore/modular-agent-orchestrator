# Critial Mao Tool QA Standardization 

## Context & Discovery

Sean discovered systematic quality issues in Mao tool files despite previous audit approvals. This represents a critical quality control failure that must be addressed methodically before proceeding with final implementation phases.

### Core Issues Identified
1. **Tool Logic Inconsistencies**: Mixed cost function naming, inconsistent caching patterns, missing error handling
2. **Button File Problems**: Mixed dispatch patterns, broken import paths, structural confusion  
3. **Three New Tools Incomplete**: Code Execution, Files API, MCP Connector missing components and proper placement
4. **Architectural Questions**: Tool placement confusion between `./tools/` and `./orchestrator/`

## Architectural Decisions

### Tool Placement Rules
- **`./tools/` directory**: Tools that agents directly use for execution
- **`./orchestrator/` directory**: Internal system components used by orchestrator

### Tool Placement Resolution
- **Code Execution**: Staying in `./tools/` because agents use this for executing code snippets
- **Files API**: Move to `./tools/` because agents use this for file operations during workflows
- **MCP Connector**: Move to `./tools/` because agents use this to access any MCP servers

## Standardization Requirements

### Tool Logic Files (`[tool_name].py`)
**Required Components:**
```python
# Standard imports
from orchestrator.cache.cache_system import CacheManager  
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

# Standard error handling decorator
@handle_errors(operation_name="[tool_name]", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(...))

# REQUIRED: Standard cost estimation function  
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    # Implementation specific to tool
    pass

# REQUIRED: Standard caching pattern
cache_key = f"{param1}|{param2}|{param3}"
cached_result = cache.get_cached_analysis(cache_key, "[tool_name]")
if cached_result:
    return json.loads(cached_result)

# After successful operation
cache.cache_content_analysis(cache_key, json.dumps(result), "[tool_name]")
```

### Button Files (`button_[tool_name].py`)
**Required Structure:**
```python
def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Single entry point for button snippet generation
    Universal model compatibility via code generation
    """
    operation = params.get("operation", "default_operation")
    
    if operation == "operation1":
        return _create_operation1_snippet(params, model)
    elif operation == "operation2":  
        return _create_operation2_snippet(params, model)
    else:
        return _create_default_snippet(params, model)

# Private helper functions
def _create_operation1_snippet(params: Dict[str, Any], model: str) -> str:
    # Implementation
    pass
```

### UI Files (`ui_[tool_name].py`)
**Required Components:**
- Rich console formatting
- Error display functions
- Verbose/concise display modes
- Consistent color schemes and icons

### JSON Files (`tool_[tool_name].json`)
**Required Structure:**
```json
{
    "name": "tool_name",
    "version": "1.0.0",
    "description": "Tool description",
    "capabilities": ["capability1", "capability2"],
    "cost_estimate": 0.001,
    "models_supported": ["all"],
    "file_path": "tools/tool_name/tool_name.py",
    "button_path": "tools/tool_name/button_tool_name.py",
    "ui_path": "tools/tool_name/ui_tool_name.py"
}
```

## Execution Phases

### Phase 1: Architecture Fixes (Session 1) ✅
**Priority**: Critical architectural issues first

1. **Move Files API to tools/** 
   - Create `tools/files_api/` directory ✅
   - Move `orchestrator/files_api.py` to `tools/files_api/files_api.py` ✅
   - Add missing components: button, UI, JSON files ✅
   - Update all imports throughout codebase ✅

2. **Move MCP Connector to tools/**
   - Create `tools/mcp_connector/` directory ✅
   - Move `orchestrator/mcp_connector.py` to `tools/mcp_connector/mcp_connector.py` ✅
   - Add missing components: button, UI, JSON files ✅
   - Update all imports throughout codebase ✅

3. **Complete Code Execution Tool**
   - Fix TODO comments and placeholder code ✅
   - Implement proper Code Execution tool integration ✅
   - Add missing components: button, UI, JSON files ✅

4. **Delete orchestrator/memory.py** 
   - Confirmed old file that violates Memory MCP strategy ✅
   - Update any remaining references ✅

### Phase 2: Tool Standardization (Session 2)
**Focus**: One tool at a time, each file, complete audit and fix

**Standardization Checklist per Tool, per File:**
- [ ] CacheManager properly imported and used
- [ ] Single cache instance (no duplicates)
- [ ] Standard `estimate_cost()` function (remove non-standard names)
- [ ] Proper error handling decorators
- [ ] Consistent caching pattern (get → process → cache)
- [ ] No TODO comments or placeholder code
- [ ] Remove hardcoded metadata/capabilities from logic files

**Tools to Standardize:**
1: brave_search.py 
```
brave_search.py (Logic file): ✅ GOOD
ui_brave_search.py (UI file): ✅ GOOD
tool_brave_search.json (Config file): ✅ GOOD
button_brave_search.py (Button file): ❌ NEEDS FIXES
  - Has estimate_execution_cost() instead of estimate_cost()
  - Has get_tool_capabilities() with hardcoded metadata (belongs in JSON)
  - Duplicates ALL logic instead of importing from logic file
  - Button snippets don't use the logic file functions
--> The button file should import and use the logic file functions instead of duplicating everything. 
```
2: dalle_generate.py 
```
dalle_generate.py: ⚠️ NEEDS MINOR FIXES
  - Has _calculate_dalle_cost() instead of standard estimate_cost()
  - Has get_dalle_capabilities() with hardcoded metadata (belongs in JSON)
ui_dalle_generate.py: ✅ GOOD
tool_dalle_generate.json: ✅ EXCELLENT
button_dalle_generate.py: 🚨 MAJOR ISSUES
  - MASSIVE file that duplicates ALL logic instead of importing
  - Inconsistent function naming (create_button_snippet vs others)
  - Has get_dalle_button_metadata() with hardcoded metadata
  - Cost calculation duplicated multiple times throughout
  - No standardized estimate_cost() function
  - Uses estimated_cost variable inconsistently
```
3: file_operations.py 
```
file_operations.py: ⚠️ MISSING COST FUNCTION
  - NO estimate_cost() function at all! This is completely missing
ui_file_operations.py: ✅ GOOD
tool_file_operations.json: ✅ EXCELLENT
button_file_operations.py: 🚨 MAJOR DUPLICATION
  - MASSIVE duplication - ALL logic copy/pasted instead of importing
  - Has create_read_file_snippet() instead of just create_button_snippet() entry
  - Multiple standalone snippet functions instead of single entry point
  - No cost estimation functions anywhere
```
4: graphic_design.py 
```
graphic_design.py: ✅ EXCELLENT
ui_graphic_design.py: ✅ EXCELLENT
tool_graphic_design.json: ✅ EXCELLENT
button_graphic_design.py: 🚨 MAJOR ISSUES
  - Multiple functions instead of single create_button_snippet() entry point
  - Has create_button_snippet(), create_editing_snippet(), create_optimization_snippet(), create_font_info_snippet()
  - Has get_model_compatibility() with hardcoded metadata (belongs in JSON)
  - Has its own estimate_cost() function with different logic than logic file
  - No imports from logic file - generates all code instead of using logic functions
  - Inconsistent operation pattern
```
5: perplexity_search.py 
```
perplexity_search.py: ✅ FIXED
ui_perplexity_search.py: ✅ EXCELLENT
tool_perplexity_search.json: ✅ EXCELLENT
button_perplexity_search.py: 🚨 MAJOR ISSUES
  - Has correct single create_button_snippet() entry point with operation dispatch
  - Hardcoded import paths like /Users/seanivore/Development/single-file-agents/Mao
  - Has get_model_compatibility_info() with hardcoded metadata (belongs in JSON)
  - No imports from logic file - generates all code instead of using logic functions
  - References to old module names perplexity_search_modular instead of current structure
  - Complex snippets that duplicate API logic instead of using MAO functions
```
6: text_editor.py 
```
text_editor.py: ⚠️ NEEDS FIXES
  - Cache imported but NOT used anywhere in the file
  - NO estimate_cost() function at all! This is completely missing
ui_text_editor.py: ✅ EXCELLENT
tool_text_editor.json: ✅ EXCELLENT
button_text_editor.py: 🚨 MAJOR ISSUES
  - Hardcoded paths like /Users/seanivore/Development/single-file-agents/Mao
  - References to old module names like text_editor_modular instead of current structure
  - Has get_model_compatibility_info() with hardcoded metadata (belongs in JSON)
  - No imports from logic file - generates all code instead of using MAO functions
```
7: think.py 
```
think.py: ⚠️ NEEDS FIXES
  - Cache imported but NOT used anywhere in the file
  - Has get_thinking_capabilities() with hardcoded metadata (belongs in JSON)
  - Has TOOL_METADATA with hardcoded model capabilities (belongs in JSON)
  - Cost calculations are incomplete - basic estimation but no proper estimate_cost() function
ui_think.py: ✅ EXCELLENT
tool_think.json: ✅ EXCELLENT
button_think.py: 🚨 MAJOR ISSUES
  - Multiple functions instead of single create_button_snippet() entry point
  - Functions: create_button_snippet(), create_prompt_enhancement_button(), create_thinking_validation_button(), etc.
  - No imports from logic file - generates all code instead of using MAO functions
  - Hardcoded API implementations instead of using logic functions
  - Multiple entry points violate our standardization pattern
```
8: web_search.py 
```
web_search.py: ⚠️ MISSING COST FUNCTION
  - NO public estimate_cost() function! Has private _calculate_search_cost() but missing required public interface
ui_web_search.py: ✅ EXCELLENT
tool_web_search.json: ✅ EXCELLENT
button_web_search.py: 🚨 BROKEN 
  - BROKEN IMPORT PATHS - imports from non-existent modules
  - tools.web_search_modular (doesn't exist)
  - interfaces.ui_tools.ui_web_search (doesn't exist)
  - HARDCODED API CALLS - generates Anthropic client code instead of using MAO logic functions
  - NO cost estimation - button doesn't use logic file's cost functions
```
9: files_api.py 
```
files_api.py: 🚨 MAJOR STANDARDIZATION GAPS
  - NO CacheManager import or usage - completely missing
  - NO cache instance - no caching at all
  - NO estimate_cost() function - completely missing public cost interface
  - NO error handling decorators - missing @handle_errors decorators
  - NO caching pattern - no get → process → cache pattern
ui_files_api.py: ✅ EXCELLENT
tool_files_api.json: ✅ EXCELLENT
button_files_api.py: 🚨 DISCONNECTED FROM LOGIC
  - NO imports from logic file - doesn't use MAO logic functions at all
  - Standalone cost function - has estimate_execution_cost() but not using logic file
  - No integration - generates code that creates workspace locally instead of using MAO FilesAPIManager
```
10: mcp_connector.py 
```
mcp_connector.py: ⚠️ MISSING STANDALONE FUNCTIONS
  - MISSING standalone function wrappers - has MCPConnector class but no standalone functions for button imports
ui_mcp_connector.py: ✅ EXCELLENT
tool_mcp_connector.json: ✅ EXCELLENT
button_mcp_connector.py: 🚨 HARDCODED PATHS & NO LOGIC INTEGRATION
  - NO imports from logic file - doesn't import any MAO logic functions
  - Hardcoded sys.path manipulation - uses complex path manipulation instead of proper imports
  - No cost integration - doesn't use estimate_cost() from logic file
  - Creates MCPConnector directly - instantiates class instead of using standardized functions
```
11: code_execution.py 
```
code_execution.py: ⚠️ MISSING STANDALONE FUNCTIONS
  - MISSING standalone function wrappers - has CodeExecutionTool class but no standalone functions for button imports
ui_code_execution.py: ✅ EXCELLENT
tool_code_execution.json: ✅ EXCELLENT
button_code_execution.py: 🚨 HARDCODED PATHS & NO LOGIC INTEGRATION
  - NO imports from logic file - doesn't import any MAO logic functions
  - Hardcoded sys.path manipulation - uses complex path manipulation instead of proper imports
  - Direct class instantiation - creates CodeExecutionTool() instead of using standardized functions
  - No cost integration - doesn't use estimate_cost() from logic file
```

### Phase 3: Button File Standardization (Session 3)
**Focus**: Single entry point pattern for all button files

**Standardization Checklist:**
- [ ] Single `create_button_snippet()` function as entry point
- [ ] Operation-based dispatch pattern
- [ ] Fix broken import paths (no _modular references)
- [ ] Remove standalone snippet functions from public interface
- [ ] Consistent parameter handling
- [ ] Updated paths to actual MAO directory structure

**Files to Standardize:**
1. button_brave_search.py ✅ (Already good)
2. button_dalle_generate.py
3. button_file_operations.py (Complex - needs restructure)
4. button_graphic_design.py  
5. button_perplexity_search.py ✅ (Already good)
6. button_text_editor.py (Fix import paths)
7. button_think.py
8. button_web_search.py

### Phase 4: UI and JSON File Audit (Session 4)
**Focus**: Complete missing files and audit existing

**Create Missing Files:**
- tools/code_execution/ui_code_execution.py
- tools/code_execution/tool_code_execution.json
- tools/files_api/ui_files_api.py  
- tools/files_api/tool_files_api.json
- tools/mcp_connector/ui_mcp_connector.py
- tools/mcp_connector/tool_mcp_connector.json

**Audit Existing UI Files:**
- Consistent Rich console formatting
- Error handling display
- Verbose/concise modes
- Color scheme consistency

**Audit Existing JSON Files:**
- Correct file paths after architectural moves
- Consistent schema structure
- Complete capability descriptions

### Phase 5: Orchestrator Integration Audit (Session 5)
**Focus**: Ensure all orchestrator touchpoints are updated

**Files to Update:**
- Update imports after architectural moves
- Verify error handling integration
- Confirm cache system integration  
- Update tool discovery for new locations
- Test complete workflow integration

## Quality Control Framework

### Validation Scripts
Create automated checks to prevent future regressions:

1. **Tool Structure Validator**
   - Verify 4-file pattern for each tool
   - Check required function signatures
   - Validate import paths

2. **Cost Function Validator**  
   - Ensure all tools have `estimate_cost()` function
   - Verify consistent function signatures
   - Check for non-standard naming

3. **Cache Pattern Validator**
   - Verify CacheManager usage
   - Check for duplicate cache instances
   - Validate caching patterns

4. **Import Path Validator**
   - Check all import statements resolve correctly
   - Verify no broken references
   - Validate file paths in JSON configs

### Testing Strategy
- Test each tool individually after standardization
- Integration tests after architectural moves
- End-to-end workflow tests after completion
- Cost calculation verification across all tools

## Cross-Session Coordination

### Session Handoff Protocol
1. Update this document with completed tasks
2. Update Memory MCP with progress status
3. Note any discovered issues for next session
4. Test completed work before handoff

### Progress Tracking
- [ ] Phase 1: Architecture Fixes
- [ ] Phase 2: Tool Logic Standardization  
- [ ] Phase 3: Button File Standardization
- [ ] Phase 4: UI and JSON File Audit
- [ ] Phase 5: Orchestrator Integration Audit

## Success Criteria

### Phase Completion Requirements
- All tools follow identical patterns
- No TODO comments or placeholder code
- All import paths resolve correctly
- Cost calculations work consistently
- Cache patterns optimized
- Error handling comprehensive
- 4-file structure complete for all tools

### Final Validation
- Automated validation scripts pass
- Manual spot-checks confirm quality
- Integration tests successful
- Documentation updated to reflect changes

---

**This plan prioritizes systematic quality over speed. Each phase must be completed thoroughly before proceeding to the next phase.**