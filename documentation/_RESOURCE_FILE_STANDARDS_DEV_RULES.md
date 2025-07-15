# Critical Mao Developmental Rules 

## **Rule #1** 
  - Variable-input philosophy is IMMUTABLE 
  - NEVER add hardcoded categories, templates, enums, or predetermined options
  - But we're not against adding new sets of variables!

## **Rule #2** 
  - 6-File Tool Architecture is IMMUTABLE. 
  - NEVER merge, combine, or reorganize the 6-file tool pattern 

## **Rule #3** 
  - Human Button Interface is A MUST UNDERSTAND CONCEPT 
  - NEVER convert back to SDK-based approaches or provider-specific implementations

## **Rule #4** 
  - Print statement separation is MANDATORY; only allowed in UI layer files 
  - Core logic must remain print-free; exceptions are 'demos' and 'button' generator files 

## **Rule #5** 
  - File naming standards are PROTECTED; keep them general, not more specific than needed 
  - E.g., why put 'mao' in a file name when all the files in the codebase are 'mao'
  - NO timestamps in file names; this is unnecessary UX

## **Rule #6** 
  - NO automatic backward compatibility; NO legacy aliases, compatibility layers, or "keeping the old name" patterns
  - Product is brand new, no legacy; in the future when it is needed it will be a discussion

## **Rule #7** 
  - HUMAN-FIRST DESIGN of SETUP SCRIPT and JSON CONFIG; they should be able to create and execute without AI assistance 
  - Less use by human users should not result in a more complex design, that is contrary to our mission 

## **Rule #8** 
  - Phases (tasks) start at 1, NEVER 0; NO "Phase 0" or "00_" prefixes in directory structure 
  - Improves UX, eliminates confusion, clear, intuitive; this is a rule of thumb 

## **Rule #9** 
  - NO HARDCODED SUCCESS CRITERIA; we don't pre-define metrics like "covers 5+ competitors" or "includes timeline"
  - Claude is QA, sequential thinking, reviewing deliverables 

## **Rule #10** 
  - Our SETUP SCRIPT means COMMAND REGISTRY is UNNECESSARY; unix filesystem handles command discovery and execution 
  - Setup scripts create executable commands in `/Users/seanivore/bin`; proven pattern 
  - SETUP SCRIPT DOES NOT PUT HYPHENS IN COMMAND LINE, only spaces 

## **Rule #11** 
  - SINGLE RESPONSIBILITY FOR STATE MANAGEMENT; Memory MCP handles ALL workflow state persistence 
  - No duplicate state saving mechanisms or parallel tracking systems; one source of truth for workflow context and progression 
  - Eliminates synchronization issues and redundant operations; clean integration with single, authoritative state management

## **Rule #12** 
  - It is 'Mao' not 'MAO'; this encourages proper pronunciation 
  - Don't use m-dashes, use semicolons; if it is a header, it doesn't need to be bold 
  - We don't use emojis in UI; not a huge fan of them in docs but eh 

---

# Mao File Standardization Rules
**Context Priming Must-Read for All Development**

## Core Design Principles

### Visual Design Rules
- **NO EMOJI ICONS** - Use text-based visual hierarchy only
- **ASCII Cat Only** - `~(=^‥^)` used sparingly, no other visual elements
- **Text Structure Logic** - Visual organization through spacing, typography, boxes
- **Claude Code Inspiration** - Clean, professional terminal interface patterns

### File Naming & Headers
- **No Version Numbers** in file headers (creates maintenance debt)
- **Simple Product Name** - It is a file in the product, so there is no need to use "Mao" or "MAO V4" or variants 
- **Generic Headers** - Avoid version-specific or brand-specific references

## Standardization Patterns

### All Python Files Must Include:

#### 1. Standard Imports (Top of File)
```python
# Standard Mao imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()
```

#### 2. Required Functions
```python
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    # Implementation specific to component
    pass
```

#### 3. Error Handling Decorators
```python
@handle_errors(operation_name="component_name", return_dict=True)
def main_function(self, params):
    # Function implementation
    pass
```

#### 4. Standard Caching Pattern
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

#### 5. Standalone Functions (For Button Imports)
```python
# At end of file - functions that button files can import
def standalone_function_name(params) -> return_type:
    """Standalone function for button file imports"""
    manager = ComponentManager()
    return manager.method_name(params)
```

### Tool-Specific Requirements

#### Tool Structure (4 Files Required)
1. `[tool_name].py` - Main logic file
2. `button_[tool_name].py` - Button snippet generation
3. `ui_[tool_name].py` - Display and UI components  
4. `tool_[tool_name].json` - Configuration and metadata

#### Button Files Pattern
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

#### JSON Configuration Schema
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

## Modular JSON Architecture

### Core Principle
**All JSON config files must be standalone, atomic units**
- Easy to add/remove/update individual components
- Directory scanning for live discovery
- No hardcoded lists anywhere in code
- Template-based consistency

### Implementation
- System scans directories for `*_component_type.json` files
- Each file is self-contained and complete
- Templates in `./configs/examples/` for new file creation
- Dynamic discovery prevents hardcoded references

## Violation Prevention

### Common Mistakes to Avoid:
1. **Code Duplication** - Button files copying logic instead of importing
2. **Missing Cost Functions** - Every component needs `estimate_cost()`
3. **Broken Imports** - Update all import paths after architectural changes
4. **Mixed Naming** - Use consistent function and field naming patterns
5. **Emoji Usage** - Text-based design only, no emoji icons
6. **Version Headers** - Generic product name only in file headers

### When in Doubt:
- Follow patterns from recently standardized tool files
- Check the Tool Standardization Plan for detailed examples
- Use existing templates from `./configs/examples/`
- Apply all checklist items before considering a file "complete"

---

**Remember: Prevention over correction. Follow these patterns from the start rather than fixing violations later.**