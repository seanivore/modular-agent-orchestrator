# Cursor Parallel Fixes - Automated Standardization Instructions

**Date:** July 9, 2025  
**Purpose:** Parallel processing of independent file standardization fixes  
**Target:** Cursor AI assistant for automated standardization  
**Coordination:** Human handling critical files, Cursor handling independent modules  

## Overview

This document provides **specific instructions** for Cursor to handle automated standardization fixes on independent files while the human handles critical architectural components.

**Division of Labor:**
- **Human:** Core orchestrator, cache system, critical managers
- **Cursor:** Independent tools, CLI commands, configuration files

## Files Assigned to Cursor

### **Batch 6: Tools/Search Analysis**
**Source:** `batch_reports/batch_06_tools_search_analysis.md`  
**Files to Fix:**
- `tools/search/search.py`
- `tools/search/button_search.py` (SKIP - button files allow print statements)
- `tools/search/ui_search.py`
- `tools/search/tool_search.json`

### **Batch 7: Tools/Content Creation Analysis**
**Source:** `batch_reports/batch_07_tools_content_creation_analysis.md`  
**Files to Fix:**
- `tools/content_creation/content_creation.py`
- `tools/content_creation/button_content_creation.py` (SKIP - button files allow print statements)
- `tools/content_creation/ui_content_creation.py`
- `tools/content_creation/tool_content_creation.json`

### **Batch 8: Tools/Development Analysis**
**Source:** `batch_reports/batch_08_tools_development_analysis.md`  
**Files to Fix:**
- `tools/development/development.py`
- `tools/development/button_development.py` (SKIP - button files allow print statements)
- `tools/development/ui_development.py`
- `tools/development/tool_development.json`

### **Batch 9: Tools/System Analysis**
**Source:** `batch_reports/batch_09_tools_system_analysis.md`  
**Files to Fix:**
- `tools/files_api/files_api.py`
- `tools/files_api/button_files_api.py` (SKIP - button files allow print statements)
- `tools/files_api/ui_files_api.py`
- `tools/files_api/tool_files_api.json`
- `tools/mcp_connector/mcp_connector.py`
- `tools/mcp_connector/button_mcp_connector.py` (SKIP - button files allow print statements)
- `tools/mcp_connector/ui_mcp_connector.py`
- `tools/mcp_connector/tool_mcp_connector.json`
- `tools/think/think.py`
- `tools/think/button_think.py` (SKIP - button files allow print statements)
- `tools/think/ui_think.py`
- `tools/think/tool_think.json`

## Required Standardization Fixes

### **1. Python File Standardization (.py files)**

#### **Required Imports (Add to top of every .py file)**
```python
# Add after existing imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
from typing import Dict, Any

# Add cache instance
cache = CacheManager()
```

#### **Error Handling Decorators (Add to all public functions)**
```python
# Change from:
def function_name(self, params):
    # implementation

# To:
@handle_errors(operation_name="function_name", return_dict=True)
def function_name(self, params):
    # implementation
```

#### **Cost Estimation Function (Add to end of every .py file)**
```python
@handle_errors(operation_name="estimate_cost", return_dict=True)
def estimate_cost(self, params: Dict[str, Any] = None) -> float:
    """Estimate tool operation cost for budget planning"""
    base_cost = 0.01  # Base tool cost
    
    if params:
        operations = params.get("operations", 1)
        base_cost += operations * 0.005
        
        files = params.get("files", 0)
        base_cost += files * 0.001
        
        # Add tool-specific cost factors as appropriate
        
    return base_cost
```

#### **Print Statement Removal (System code only)**
```python
# VIOLATION (remove):
print("System message")
print(f"Status: {status}")

# COMPLIANT (replace with):
import logging
logger = logging.getLogger(__name__)

logger.info("System message")
logger.info(f"Status: {status}")
```

**IMPORTANT:** Do NOT remove print statements from `button_*.py` files - they are allowed!

#### **Emoji Usage Removal**
```python
# VIOLATION (remove):
logger.info("🔧 Processing...")
logger.info("✅ Complete!")

# COMPLIANT (replace with):
logger.info("Processing...")
logger.info("Complete!")
```

### **2. JSON File Standardization (.json files)**

#### **Required Fields (Add to all .json files)**
```json
{
  "name": "tool_name",
  "display_name": "Human Readable Name",
  "description": "Clear description of tool functionality",
  "category": "tools",
  "requires_auth": false,
  // ... existing fields
}
```

#### **Field Ordering (Reorder fields)**
1. `name` (required)
2. `display_name` (required)
3. `description` (required)
4. `category` (recommended)
5. `requires_auth` (recommended)
6. All other fields (alphabetical)

## Implementation Process

### **Step 1: Batch Processing**
1. **Read the batch report** for each assigned batch
2. **Identify violation patterns** from the analysis
3. **Apply fixes systematically** to each file
4. **Test imports** after each file modification

### **Step 2: File Processing Workflow**
For each file:
1. **Create backup** (`cp file.py file.py.backup`)
2. **Apply standardization fixes** using patterns above
3. **Test imports** (`python3 -c "from module import *; print('✅ Success')"`)
4. **Document changes** in the reporting section below

### **Step 3: Verification**
After each batch:
1. **Test all file imports** work correctly
2. **Verify no functional regressions**
3. **Check compliance** with standardization rules
4. **Update progress** in reporting section

## Conditional Import Handling

Use **conditional imports** to handle missing dependencies:

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

## Progress Reporting

### **Batch 6: Tools/Search (Status: PENDING)**
- [ ] `tools/search/search.py` - 
- [ ] `tools/search/ui_search.py` - 
- [ ] `tools/search/tool_search.json` - 

**Changes Made:**
- 

**Issues Encountered:**
- 

**Testing Results:**
- 

---

### **Batch 7: Tools/Content Creation (Status: PENDING)**
- [ ] `tools/content_creation/content_creation.py` - 
- [ ] `tools/content_creation/ui_content_creation.py` - 
- [ ] `tools/content_creation/tool_content_creation.json` - 

**Changes Made:**
- 

**Issues Encountered:**
- 

**Testing Results:**
- 

---

### **Batch 8: Tools/Development (Status: PENDING)**
- [ ] `tools/development/development.py` - 
- [ ] `tools/development/ui_development.py` - 
- [ ] `tools/development/tool_development.json` - 

**Changes Made:**
- 

**Issues Encountered:**
- 

**Testing Results:**
- 

---

### **Batch 9: Tools/System (Status: PENDING)**
- [ ] `tools/files_api/files_api.py` - 
- [ ] `tools/files_api/ui_files_api.py` - 
- [ ] `tools/files_api/tool_files_api.json` - 
- [ ] `tools/mcp_connector/mcp_connector.py` - 
- [ ] `tools/mcp_connector/ui_mcp_connector.py` - 
- [ ] `tools/mcp_connector/tool_mcp_connector.json` - 
- [ ] `tools/think/think.py` - 
- [ ] `tools/think/ui_think.py` - 
- [ ] `tools/think/tool_think.json` - 

**Changes Made:**
- 

**Issues Encountered:**
- 

**Testing Results:**
- 

---

## Quality Assurance

### **Automated Verification Script**
Run this after each batch to verify compliance:

```bash
#!/bin/bash
# Verify standardization compliance

echo "🔍 Verifying standardization compliance..."

# Check for required imports
echo "Checking required imports..."
find tools/ -name "*.py" -not -path "*/button_*" | while read file; do
    if ! grep -q "from orchestrator.cache.cache_system import CacheManager" "$file"; then
        echo "❌ Missing CacheManager import: $file"
    fi
    if ! grep -q "from orchestrator.error_handling import handle_errors" "$file"; then
        echo "❌ Missing handle_errors import: $file"
    fi
done

# Check for estimate_cost function
echo "Checking estimate_cost functions..."
find tools/ -name "*.py" -not -path "*/button_*" | while read file; do
    if ! grep -q "def estimate_cost" "$file"; then
        echo "❌ Missing estimate_cost function: $file"
    fi
done

# Check for print statements (excluding button files)
echo "Checking for print statements..."
find tools/ -name "*.py" -not -path "*/button_*" | while read file; do
    if grep -q "print(" "$file"; then
        echo "❌ Print statement found: $file"
        grep -n "print(" "$file"
    fi
done

# Check JSON schema compliance
echo "Checking JSON schema compliance..."
find tools/ -name "*.json" | while read file; do
    if ! python3 -c "import json; data=json.load(open('$file')); assert 'name' in data and 'display_name' in data" 2>/dev/null; then
        echo "❌ JSON schema violation: $file"
    fi
done

echo "✅ Verification complete!"
```

### **Rollback Procedures**
If issues arise:

```bash
#!/bin/bash
# Emergency rollback
echo "🔄 Rolling back changes..."

find tools/ -name "*.backup" | while read backup; do
    original="${backup%.backup}"
    echo "Restoring $original..."
    cp "$backup" "$original"
done

echo "✅ Rollback complete!"
```

## Success Criteria

### **Completion Metrics**
- [ ] All assigned files processed
- [ ] All imports working correctly
- [ ] No functional regressions
- [ ] 100% compliance with standardization rules
- [ ] All tests passing

### **Quality Metrics**
- [ ] Zero print statement violations
- [ ] Complete error handling coverage
- [ ] All cost estimation functions implemented
- [ ] JSON schema compliance achieved
- [ ] Documentation updated

## Coordination Notes

### **Communication Protocol**
- **Update progress** in this document as you complete each batch
- **Document any issues** encountered during processing
- **Test thoroughly** before marking batches complete
- **Note any dependencies** that require human attention

### **Handoff Points**
- **Critical dependencies** should be flagged for human review
- **Complex integration issues** should be escalated
- **Architecture questions** should be discussed
- **Breaking changes** should be avoided

## Final Verification

After completing all batches:

1. **Run comprehensive tests**
2. **Verify all imports work**
3. **Check for regressions**
4. **Update final status**
5. **Prepare handoff summary**

---

**This document will be updated in real-time as Cursor processes each batch. Check back for progress updates and coordination notes.**