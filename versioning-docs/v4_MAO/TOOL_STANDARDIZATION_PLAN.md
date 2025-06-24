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
- **Code Execution**: Stay in `./tools/` - agents use this for executing code snippets
- **Files API**: Move to `./tools/` - agents use this for file operations during workflows
- **MCP Connector**: Move to `./tools/` - agents use this to access MCP servers

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

### Phase 1: Architecture Fixes (Session 1)
**Priority**: Critical architectural issues first

1. **Move Files API to tools/**
   - Create `tools/files_api/` directory
   - Move `orchestrator/files_api.py` to `tools/files_api/files_api.py`
   - Add missing components: button, UI, JSON files
   - Update all imports throughout codebase

2. **Move MCP Connector to tools/**
   - Create `tools/mcp_connector/` directory  
   - Move `orchestrator/mcp_connector.py` to `tools/mcp_connector/mcp_connector.py`
   - Add missing components: button, UI, JSON files
   - Update all imports throughout codebase

3. **Complete Code Execution Tool**
   - Fix TODO comments and placeholder code
   - Implement proper Code Execution tool integration
   - Add missing components: button, UI, JSON files

4. **Delete orchestrator/memory.py**
   - Confirmed old file that violates Memory MCP strategy
   - Update any remaining references

### Phase 2: Tool Logic Standardization (Session 2)
**Focus**: One tool at a time, complete audit and fix

**Standardization Checklist per Tool:**
- [ ] CacheManager properly imported and used
- [ ] Single cache instance (no duplicates)
- [ ] Standard `estimate_cost()` function (remove non-standard names)
- [ ] Proper error handling decorators
- [ ] Consistent caching pattern (get → process → cache)
- [ ] No TODO comments or placeholder code
- [ ] Remove hardcoded metadata/capabilities from logic files

**Tools to Standardize:**
1. brave_search.py ✅ (Already good)
2. dalle_generate.py (Fix cost function naming)
3. file_operations.py (Add missing cost estimation)
4. graphic_design.py ✅ (Already good)
5. perplexity_search.py (Fix duplicate cache calls, cost function naming)
6. text_editor.py (Implement missing cache usage and cost estimation)
7. think.py (Clean up metadata, implement proper cost estimation)
8. web_search.py (Fix duplicate cache calls, standardize cost function)

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