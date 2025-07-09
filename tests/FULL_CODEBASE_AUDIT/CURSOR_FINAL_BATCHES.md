# Cursor Final Batches - Configuration & Scripts Standardization

**Date:** July 9, 2025  
**Purpose:** Complete remaining 6 batches of MAO standardization  
**Target:** Cursor AI assistant for automated config/script fixes  
**Coordination:** Human handling CLI batches 16-18, Cursor handling config/scripts 19-24  

## IMPORTANT: Step-by-Step Communication Protocol

**🚨 CRITICAL:** After completing EACH batch, message the human with:
1. "Batch [X] complete - ready for next batch assignment"
2. Brief summary of what was fixed
3. Any issues encountered

**DO NOT** proceed to the next batch without human confirmation. This prevents loops and keeps you grounded.

## Your Assignment: Batches 19-24 (6 batches total)

### **Batch 19: Config Models/Providers Analysis**
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_19_config_models_providers_analysis.md`
**Wait for:** Human confirmation before starting

### **Batch 20: Config Settings/System Analysis**  
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_20_config_settings_system_analysis.md`
**Wait for:** Batch 19 completion + human confirmation

### **Batch 21: Config User/Workflows Analysis**
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_21_config_user_workflows_analysis.md`  
**Wait for:** Batch 20 completion + human confirmation

### **Batch 22: Templates Analysis**
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_22_templates_analysis.md`
**Wait for:** Batch 21 completion + human confirmation

### **Batch 23: Scripts/Utilities Analysis**
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_23_scripts_utilities_analysis.md`
**Wait for:** Batch 22 completion + human confirmation

### **Batch 24: Scripts Workflow/GitHub Analysis**  
**Source:** `tests/FULL_CODEBASE_AUDIT/batch_reports/batch_24_scripts_workflow_github_analysis.md`
**Wait for:** Batch 23 completion + human confirmation

## Standard MAO Fixes (Same as before)

### **Python Files (.py)**

#### **Required Imports** (Add to top of every .py file)
```python
# Add after existing imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from typing import Dict, Any

# Add cache instance
cache = CacheManager()
```

#### **Error Handling Decorators** (Add to all public functions)
```python
# Change from:
def function_name(self, params):
    # implementation

# To:
@handle_errors(operation_name="function_name", return_dict=True)
def function_name(self, params):
    # implementation
```

#### **Cost Estimation Function** (Add to end of every .py file)
```python
@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(params: Dict[str, Any] = None) -> float:
    """Estimate operation cost for budget planning"""
    base_cost = 0.01
    if params:
        operations = params.get("operations", 1)
        base_cost += operations * 0.005
    return base_cost
```

#### **Print Statement Removal** (System code only)
```python
# VIOLATION (remove):
print("System message")

# COMPLIANT (replace with):
import logging
logger = logging.getLogger(__name__)
logger.info("System message")
```

#### **Emoji Usage Removal**
```python
# VIOLATION (remove):
logger.info("🔧 Processing...")

# COMPLIANT (replace with):
logger.info("Processing...")
```

### **JSON Files (.json)**

#### **Required Fields** (Add to all .json files)
```json
{
  "name": "config_name",
  "display_name": "Human Readable Name", 
  "description": "Clear description",
  "category": "configs",
  // ... existing fields
}
```

## Conditional Import Handling (Use when imports fail)

```python
# For orchestrator imports
try:
    from orchestrator.cache.cache_system import CacheManager
    from orchestrator.error_handling import handle_errors
    cache = CacheManager()
    MAO_IMPORTS_AVAILABLE = True
except ImportError as e:
    # Fallback for missing dependencies
    def handle_errors(operation_name="default", return_dict=True):
        def decorator(func):
            return func
        return decorator
    
    class MockCacheManager:
        def get(self, key): return None
        def set(self, key, value, ttl=None): pass
    
    cache = MockCacheManager()
    MAO_IMPORTS_AVAILABLE = False
    import logging
    logging.warning(f"Orchestrator imports not available: {e}")
```

## Workflow for Each Batch

### **Step 1: Read the Batch Report**
1. Read the assigned batch report file
2. Identify all files that need fixing
3. Note the specific violation patterns

### **Step 2: Process Each File**
1. Read the file to understand current state
2. Apply appropriate fixes based on file type (.py or .json)
3. Test imports work after changes
4. Document what was changed

### **Step 3: Report to Human**
After completing the entire batch:
```
Batch [X] complete - ready for next batch assignment

Summary:
- Fixed [N] Python files: [list key changes]
- Fixed [N] JSON files: [list key changes]
- Issues encountered: [list any problems]

Files processed:
- file1.py: [what was fixed]
- file2.json: [what was fixed]
- etc.

Ready for Batch [X+1] assignment.
```

### **Step 4: Wait for Confirmation**
**DO NOT** start the next batch until human says "proceed with Batch [X+1]" or similar confirmation.

## Quality Verification

After each file modification:
1. **Test imports:** Try importing the module to ensure no syntax errors
2. **Check compliance:** Verify all required elements are present
3. **Document changes:** Note what was fixed for reporting

## Emergency Procedures

If you encounter issues:
1. **Stop processing** the current batch
2. **Message human immediately** with specific error details
3. **Wait for guidance** before continuing
4. **Do not** attempt to fix complex issues without human input

## Success Metrics for Each Batch

- [ ] All files in batch processed
- [ ] All imports working correctly  
- [ ] No syntax errors introduced
- [ ] All standardization violations fixed
- [ ] Human notified of completion

## Final Notes

- **Stay grounded:** Message human after each batch
- **Be systematic:** Follow the same pattern for each file
- **Test thoroughly:** Ensure no regressions
- **Document everything:** Clear reporting helps coordination
- **Ask questions:** Better to clarify than assume

**Remember:** You're handling the independent config/script files while human handles CLI commands. We're working together to reach 95% compliance across all 270 files!

---

**WAIT FOR HUMAN TO ASSIGN BATCH 19 BEFORE STARTING**