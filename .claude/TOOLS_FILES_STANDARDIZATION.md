# MAO v4 Tool Files Standardization Checklist

## For Cursor: Systematic Review of All 8 Tools

### Tools to Review:
- `tools/brave_search/`
- `tools/dalle_generate/`  
- `tools/file_operations/`
- `tools/graphic_design/`
- `tools/perplexity_search/`
- `tools/text_editor/`
- `tools/think/`
- `tools/web_search/`

---

## 1. BUTTON FILES (`button_*.py`) Standardization

### Function Name Consistency
**Current inconsistencies found:**
- `create_dalle_generation_button` → should be `create_button_snippet`
- `create_analysis_snippet` → should be `create_button_snippet` 
- Various other function names → should be `create_button_snippet`

**Standard signature for ALL button files:**
```python
def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude 4 execution
    Universal model compatibility via code generation
    """
```

### Import Statements in Button Files
**Check for these patterns and update:**
- `from orchestrator.cache.cache_system import CacheManager` ✅
- `from orchestrator.manager_models import ModelManager` ✅  
- `from orchestrator.manager_buttons import ButtonManager` ✅

---

## 2. PRINT STATEMENT AUDIT (ALL FILES)

### Files to Clean:
**Search entire codebase for `print(` and move to UI layer**

**Pattern to find:** `print(`
**Pattern to replace:** Remove from core logic files, move to `ui_*.py` files

**Files that should have NO print statements:**
- All `tools/*/toolname.py` (core logic)
- All `tools/*/button_*.py` (button generators)
- `orchestrator/core.py`
- `orchestrator/manager_*.py`
- `orchestrator/cache/cache_system.py`

**Files that CAN have print statements:**
- All `tools/*/ui_*.py` (UI display layer)
- `interfaces/terminal.py`

---

## 3. CLASS NAME CONSISTENCY

### Import Statement Updates
**Verify these are correct in ALL files:**
```python
from orchestrator.cache.cache_system import CacheManager
from orchestrator.manager_models import ModelManager  
from orchestrator.manager_buttons import ButtonManager
from orchestrator.manager_tools import ToolManager
```

### Variable Name Updates
**Search and replace patterns:**
- `self.human_buttons` → `self.buttons`
- `HybridCacheManager` → `CacheManager`
- `UniversalModelManager` → `ModelManager`
- `HumanButtonInterface` → `ButtonManager`
- `ToolDiscovery` → `ToolManager`

---

## 4. JSON TOOL DEFINITIONS (`tool_*.json`)

### File Path Corrections
**Current wrong pattern:**
```json
"files": {
  "core_logic": "tools/brave_search_modular.py",
  "ui_display": "interfaces/ui_tools/ui_brave_search.py", 
  "buttons": "utilities/button_tools/button_brave_search.py"
}
```

**Correct pattern for ALL tools:**
```json
"files": {
  "core_logic": "tools/TOOLNAME/TOOLNAME.py",
  "ui_display": "tools/TOOLNAME/ui_TOOLNAME.py", 
  "buttons": "tools/TOOLNAME/button_TOOLNAME.py"
}
```

**Example for brave_search:**
```json
"files": {
  "core_logic": "tools/brave_search/brave_search.py",
  "ui_display": "tools/brave_search/ui_brave_search.py", 
  "buttons": "tools/brave_search/button_brave_search.py"
}
```

---

## 5. VARIABLE-INPUT PHILOSOPHY CHECK

### Anti-Patterns to Remove:
- Hardcoded categories or templates
- Predefined frameworks or "choose your method" menus  
- Domain-specific assumptions
- Enum-style predetermined choices

### What to Look For:
```python
# ❌ BAD - Hardcoded specifics
analysis_types = ["financial", "marketing", "technical"]
templates = {"business_plan": "...", "research_report": "..."}

# ✅ GOOD - Variable input
def analyze_content(content: str, analysis_approach: str) -> Dict:
    """Let the prompt define the approach, not the code"""
```

---

## 6. ERROR HANDLING CONSOLIDATION

### Check Import Pattern:
**All tool files should import:**
```python
from orchestrator.error_handling import handle_error, retry_with_backoff
```

### Verify Error Handling Usage:
- No duplicate error handling code
- Professional retry logic using shared utilities
- Graceful degradation patterns

---

## 7. FINAL VERIFICATION TESTS

### Test Each Tool Has:
1. ✅ `create_button_snippet()` function with correct signature
2. ✅ No print statements in core logic files
3. ✅ Correct import statements using new class names
4. ✅ Correct file paths in JSON definitions
5. ✅ No hardcoded specifics or categories
6. ✅ Shared error handling patterns

### Quick Test Commands:
```bash
# Find remaining print statements
grep -r "print(" tools/ orchestrator/

# Find old import patterns  
grep -r "hybrid_cache\|human_buttons\|model_manager\|tool_discovery" tools/ orchestrator/

# Find inconsistent function names
grep -r "def create_" tools/*/button_*.py
```

---

## Notes for Cursor:

- **Priority**: Function name standardization and print statement removal
- **Philosophy**: Tools are blank canvases - no hardcoded specifics!
- **Architecture**: Clean separation - logic, UI, buttons, registry, error handling
- **Testing**: Each tool should work in isolation after changes

This cleanup will eliminate technical debt and ensure all tools follow the same professional patterns! 🎯