# CLI Command Standardization & Implementation Plan
**Context Jump Document for Task #5 Implementation**

---

## Project Status & Context

**Current State:** Task #5 "Leftover From Integration Plan Notes" - CLI Commands Integration
- ✅ **CLI Commands Manager created** (`orchestrator/cli_manager.py`) 
- ✅ **Basic caching implemented** for frequently-called commands
- ✅ **Dynamic cost reading** from JSON files (no hardcoded costs)
- 🚧 **Full standardization needed** for all CLI commands and utility scripts

**Problem Identified:** CLI commands need "proper fingerprinting for ALL CLI commands and their responses" like tools have

**Architecture Discovery:** Two distinct types of CLI commands require different standardization approaches

---

## Two Types of CLI Commands Identified

### Type A: Utility Scripts (Standalone + App Integration)
**Examples:** `workflow_setup.sh`, `unique_id_generator.py`, `user_id_generator.py`

**Current Structure:**
- `.py` files with business logic
- `.sh` install scripts for terminal commands  
- Work both as standalone terminal commands AND called from within app
- **Currently: NO MAO standardization, NO caching** ❌

**Current Issues:**
- `workflow_setup.sh` - Expensive JSON parsing, file operations, no caching
- `unique_id_generator.py` - Complex math operations, no MAO imports
- `user_id_generator.py` - Similar issues to unique_id_generator

### Type B: App Interface Commands (App-Only)
**Examples:** `stats`, `workflows`, `help`, `login`, `logout`, `list_tools`

**Current Structure:**
- JSON config files only (`configs/cli/[command].json`)
- Hardcoded methods in CLI manager
- **Currently: Basic caching added, but no logic files** ⚠️

**Current Issues:**
- No dedicated logic files with proper standardization
- Limited caching capabilities  
- Mixed responsibilities in CLI manager

---

## Standardization Requirements

### Type A: Utility Scripts Standardization
**File Structure:** Keep existing `.py` + `.sh` pattern
**Required Additions:**

```python
# Standard MAO imports (top of .py file)
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError
import hashlib
import json
from datetime import datetime

# Standard cache instance
cache = CacheManager()

# Required functions
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    pass

# All main functions need @handle_errors decorator
@handle_errors(operation_name="script_name", return_dict=True)
def main_function(params):
    pass

# Intelligent caching with fingerprinting
def _generate_cache_key(input_params) -> str:
    """Generate cache key based on input fingerprints"""
    pass

# Standalone functions for app integration
def script_function_name(params) -> return_type:
    """Standalone function for app imports"""
    pass
```

### Type B: App Interface Commands Standardization  
**File Structure:** Create new 2-file pattern
1. `configs/cli/[command].py` - Logic file with full MAO standardization
2. `configs/cli/[command].json` - Enhanced config with operations, integration flags

**Required Pattern:**

```python
# configs/cli/[command].py
"""
[Command] CLI Command - Core Logic
[Description of what this command does]
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

cache = CacheManager()

@handle_errors(operation_name="[command]", return_dict=True)
def execute_[command](params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main command execution with caching and error handling"""
    pass

def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    pass

def [command]_operation(specific_params) -> Dict[str, Any]:
    """Specific operations as needed"""
    pass

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager"""
    return execute_[command](params)
```

**Enhanced JSON Config:**

```json
{
  "command": "[command]",
  "type": "standalone",
  "terminal_flag": "--[command]",
  "app_command": "/[command]",
  "interface_method": "[command]",
  "help": "Description of command",
  "cost_estimate": 0.001,
  "logic_file": "configs/cli/[command].py",
  "operations": {
    "execute": {
      "description": "Main command operation",
      "required_params": [],
      "optional_params": ["param1"]
    }
  },
  "integration": {
    "memory_mcp": true,
    "cache_system": true,
    "error_handling": true
  },
  "cache_settings": {
    "enabled": true,
    "duration_seconds": 300,
    "cache_key_includes": ["system_state", "user_context"]
  }
}
```

---

## Implementation Plan

### Phase 1: Create Standardization Templates (CURRENT PRIORITY)
1. **Create Type A template** using existing utility script
2. **Create Type B template** using medium-complexity command (`workflows`)
3. **Test templates to perfection** - ensure full MAO compliance
4. **Document template patterns** for systematic replication

### Phase 2: Implement Type B Commands (New Logic Files)
**Simple Commands (5-7 commands):**
- `help`, `user_id`, `workflow_id`, `login`, `logout`  
- Quick wins with minimal logic

**Medium Commands (8-10 commands):**
- `workflows`, `list_tools`, `stats`, `model_list`, `provider_list`
- Directory scanning, config reading, system data

**Complex Commands (8-10 commands):**
- `goal`, `setup`, `update`, `fix_it`, `continue`, `review`
- Business logic, workflow operations, state management

### Phase 3: Standardize Type A Utility Scripts (Add to Todo)
**Priority Scripts:**
1. `workflow_setup.sh` - Add intelligent caching for JSON operations
2. `unique_id_generator.py` - Add full MAO standardization
3. `user_id_generator.py` - Add full MAO standardization  
4. Other utility scripts as discovered

### Phase 4: Update CLI Manager Integration
1. **Route Type A → Utility scripts** with proper imports
2. **Route Type B → Logic files** with dynamic loading
3. **Unified caching strategy** for both types
4. **Error handling consistency** across all command types

---

## Success Criteria

### Template Quality Standards
- ✅ Full MAO standardization compliance (CacheManager, @handle_errors, estimate_cost)
- ✅ Intelligent caching with content fingerprinting
- ✅ Proper error handling and validation
- ✅ Modular architecture (add/remove commands by files)
- ✅ Cost optimization for repeated usage
- ✅ Integration with Memory MCP, cache system, error handling

### Implementation Standards
- **One command at a time** - Perfect each before moving to next
- **Test after each** - Verify template compliance before scaling
- **No doubling back** - Get standardization right the first time
- **Document decisions** - Clear reasoning for architecture choices

---

## Context Jump Information for Future Claude Sessions

**Current Working Directory:** `/Users/seanivore/Development/modular-agent-orchestrator`

**Key Files to Reference:**
- `orchestrator/cli_manager.py` - Current CLI commands manager (basic caching implemented)
- `versioning-docs/technical-documentation/MAO_FILE_STANDARDIZATION_RULES.md` - Standardization requirements  
- `tools/web_search/web_search.py` - Example of perfect MAO standardization (tool example)
- `configs/cli/[command].json` - Existing CLI command JSON configs

**Sean's Preferences:**
- Systematic approach, one at a time
- Test to perfection before scaling
- Filesystem tools preferred over artifacts for accuracy
- Frequent Memory MCP updates during implementation
- Quality over speed, no rushing
- Sequential thinking MCP for complex analysis

**Next Session Start Point:**
1. Create Type B template using `workflows` command
2. Test template for perfect MAO compliance
3. Apply template to simple commands first
4. Scale systematically through medium then complex commands

**Critical Architecture Decision:**
- Type A (Utility Scripts): Keep .py + .sh, add MAO standardization
- Type B (App Commands): Create new .py + enhanced .json pattern  
- Both types get proper fingerprinting and caching

---

## DETAILED IMPLEMENTATION ANALYSIS
**Discovered during architecture planning session**

### File Requirements Analysis

**30 CLI Commands Identified:**
```
chat.json, config.json, continue.json, doctor.json, dry_run.json, exit.json, 
fix_it.json, free_only.json, goal.json, help.json, list_tools.json, login.json, 
logout.json, logs.json, model.json, model_list.json, output_directory.json, 
privacy.json, provider.json, provider_list.json, restart.json, review.json, 
setup.json, stats.json, update.json, user_id.json, variables.json, 
variables_explain.json, verbose.json, workflow_id.json, workflows.json
```

### Files That DON'T Exist Yet (Need to Create)
**30 Logic Files + Subdirectories:** `configs/cli/[command]/[command].py`
- `configs/cli/workflows/workflows.py`
- `configs/cli/stats/stats.py` 
- `configs/cli/help/help.py`
- etc. (30 total subdirectories + logic files)
- Each needs full MAO standardization pattern from tools:
  - CacheManager import and usage
  - @handle_errors decorators  
  - estimate_cost() function
  - Intelligent caching with fingerprinting
  - Standalone functions for CLI manager import

### Files That EXIST (Need to Move + Enhancement)
**30 JSON Files:** Move from `configs/cli/[command].json` to `configs/cli/[command]/[command].json`
- Current: `configs/cli/workflows.json`
- Move to: `configs/cli/workflows/workflows.json`
- Then enhance with operations, integration, cache_settings

**Current structure:**
```json
{
  "command": "workflows",
  "type": "standalone",
  "terminal_flag": "--workflows", 
  "app_command": "/workflows",
  "interface_method": "workflows",
  "help": "List all configured workflows and their status",
  "cost_estimate": 0.002
}
```

**Need to add:**
```json
{
  "logic_file": "configs/cli/workflows/workflows.py",
  "operations": {
    "list_workflows": {
      "description": "List all configured workflows",
      "required_params": [],
      "optional_params": ["filter", "status"]
    }
  },
  "integration": {
    "memory_mcp": true,
    "cache_system": true,
    "error_handling": true
  },
  "cache_settings": {
    "enabled": true,
    "duration_seconds": 300,
    "cache_key_includes": ["workflow_directory_state"]
  }
}
```

### Files That Need Touchpoints/Updates
**1 Management File (STAYS in orchestrator):** `orchestrator/cli_manager.py`
- **Current:** Hardcoded methods in `_execute_interface_method()`
- **Need:** Route to logic files using dynamic imports
- **Change:** Load and call `configs/cli/[command]/[command].py` files instead of hardcoded method mappings
- **Architecture:** Management file stays in orchestrator (like `orchestrator/manager_tools.py`)

### Architecture Simplification Discovery
**CLI Commands are SIMPLER than tools:**
- ❌ **No button files needed** (not used by AI agents)
- ❌ **No separate UI files needed** (CLI manager handles display)
- ✅ **Just 2 files per command:** Logic + Enhanced JSON

**vs Tools (4 files each):**
- tool_name.py (logic)
- button_tool_name.py (AI agent snippets) 
- ui_tool_name.py (display)
- tool_tool_name.json (config)

### Implementation Complexity Breakdown

**Simple Commands (7 commands) - Minimal logic:**
- `help`, `user_id`, `workflow_id`, `login`, `logout`, `privacy`, `verbose`
- Mostly return static data or simple state management

**Medium Commands (12 commands) - System scanning:**
- `workflows`, `list_tools`, `stats`, `model_list`, `provider_list`
- `variables`, `variables_explain`, `config`, `logs`, `free_only`, `output_directory`, `dry_run`
- Directory scanning, config file reading, system data collection

**Complex Commands (11 commands) - Business logic:**
- `goal`, `setup`, `update`, `fix_it`, `continue`, `review` 
- `doctor`, `chat`, `restart`, `exit`, `model`, `provider`
- Workflow operations, state management, system integration

### Success Criteria for Templates
- ✅ Full MAO standardization compliance (matches tool quality)
- ✅ Intelligent caching with content fingerprinting  
- ✅ Proper error handling and validation
- ✅ Modular architecture (add/remove commands by files)
- ✅ Cost optimization for repeated usage
- ✅ Integration with Memory MCP, cache system, error handling
- ✅ No hardcoded methods in CLI manager

### Next Session Priorities
1. **Create `workflows.py` template** - Medium complexity example
2. **Enhance `workflows.json`** - Add operations, integration, cache_settings
3. **Test template perfection** - Ensure full MAO compliance
4. **Update CLI manager routing** - Dynamic logic file loading
5. **Document template pattern** - For systematic replication

*This detailed analysis ensures we understand the full scope before implementation and can create perfect templates for systematic scaling.*

---

## WORKFLOWS IMPLEMENTATION EXAMPLE
**Concrete example to verify understanding before proceeding**

### Step 1: Create Subdirectory Structure
```bash
# Create subdirectory
mkdir -p configs/cli/workflows/
```

### Step 2: Move Existing JSON File
```bash
# Move existing flat JSON into subdirectory
mv configs/cli/workflows.json configs/cli/workflows/workflows.json
```

### Step 3: Create Logic File
**File:** `configs/cli/workflows/workflows.py`
```python
"""
Workflows CLI Command - Core Logic
List and manage configured workflows with intelligent caching
"""

import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports (following tool standardization)
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="list_workflows", return_dict=True)
def list_workflows(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    List all configured workflows with intelligent caching
    
    Args:
        params: Optional filter parameters
        
    Returns:
        Dict with workflow list and metadata
    """
    # Generate cache key based on workflow directory state
    workflows_dir = Path(__file__).parent.parent.parent / "workflows"
    cache_key = _generate_workflows_cache_key(workflows_dir, params)
    
    # Check cache first (fingerprinting like tools)
    cached_result = cache.get_cached_analysis(cache_key, "workflows_list")
    if cached_result:
        return json.loads(cached_result)
    
    # Scan workflow directories
    workflow_list = []
    if workflows_dir.exists():
        for workflow_dir in workflows_dir.iterdir():
            if workflow_dir.is_dir() and not workflow_dir.name.startswith('.'):
                workflow_info = _get_workflow_info(workflow_dir)
                if workflow_info:
                    workflow_list.append(workflow_info)
    
    # Prepare result
    result = {
        "status": "success",
        "operation": "list_workflows",
        "workflows": workflow_list,
        "total_workflows": len(workflow_list),
        "timestamp": datetime.now().isoformat()
    }
    
    # Cache the result (fingerprinting)
    cache.cache_content_analysis(cache_key, json.dumps(result), "workflows_list")
    
    return result

def _generate_workflows_cache_key(workflows_dir: Path, params: Dict[str, Any]) -> str:
    """
    Generate cache key that includes workflow directory state fingerprint.
    This ensures cache invalidation when workflows change.
    """
    # Base key with params
    base_key = f"workflows_list|{str(params) if params else 'none'}"
    
    # Add directory state fingerprint
    if workflows_dir.exists():
        workflow_dirs = sorted([d.name for d in workflows_dir.iterdir() if d.is_dir()])
        dir_fingerprint = hashlib.md5(str(workflow_dirs).encode()).hexdigest()[:8]
        base_key += f"|state:{dir_fingerprint}"
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _get_workflow_info(workflow_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Extract workflow information from directory
    """
    try:
        # Look for workflow config JSON
        config_files_dir = workflow_dir / "config-files"
        if config_files_dir.exists():
            workflow_configs = list(config_files_dir.glob("*_workflow_config.json"))
            if workflow_configs:
                with open(workflow_configs[0], 'r') as f:
                    config = json.load(f)
                    workflow_data = config.get('workflow', [{}])[0]
                    return {
                        "name": workflow_dir.name,
                        "workflow_id": workflow_data.get('workflow_id'),
                        "custom_command": workflow_data.get('custom_command'),
                        "goal": workflow_data.get('workflow_goal'),
                        "status": "configured"
                    }
        
        # Fallback - just directory info
        return {
            "name": workflow_dir.name,
            "workflow_id": None,
            "custom_command": workflow_dir.name.replace('-', ' '),
            "goal": "Unknown",
            "status": "directory_only"
        }
        
    except Exception:
        return None

def estimate_cost(params: Dict[str, Any]) -> float:
    """
    Estimate operation cost for budget planning
    Standard cost estimation interface for MAO CLI commands
    """
    # Workflow listing is relatively inexpensive
    # Cost mainly from directory scanning and JSON parsing
    return 0.002

# Standalone function for CLI manager import (following tool pattern)
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Standalone function for CLI manager to import and call
    """
    return list_workflows(params)
```

### Step 4: Enhance JSON Config
**File:** `configs/cli/workflows/workflows.json`
```json
{
  "command": "workflows",
  "type": "standalone",
  "terminal_flag": "--workflows",
  "app_command": "/workflows",
  "interface_method": "workflows",
  "help": "List all configured workflows and their status",
  "cost_estimate": 0.002,
  "logic_file": "configs/cli/workflows/workflows.py",
  "operations": {
    "list_workflows": {
      "description": "List all configured workflows with status",
      "required_params": [],
      "optional_params": ["filter", "status"]
    }
  },
  "integration": {
    "memory_mcp": true,
    "cache_system": true,
    "error_handling": true
  },
  "cache_settings": {
    "enabled": true,
    "duration_seconds": 300,
    "cache_key_includes": ["workflow_directory_state"]
  }
}
```

### Step 5: Update CLI Manager Routing
**File:** `orchestrator/cli_manager.py` (add to `_execute_interface_method`)
```python
def _execute_interface_method(self, method_name: str, input_data: Any, 
                             config: Dict, source: str) -> Dict[str, Any]:
    """
    Dynamically execute interface methods by loading logic files.
    """
    
    # Check if we have a logic file for this command
    logic_file = config.get("logic_file")
    if logic_file:
        try:
            # Dynamic import of logic file
            import importlib.util
            spec = importlib.util.spec_from_file_location("command_logic", logic_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Call the execute_command function
            if hasattr(module, 'execute_command'):
                return module.execute_command(input_data)
            else:
                return {"error": f"No execute_command function in {logic_file}"}
                
        except Exception as e:
            return {"error": f"Failed to load logic file {logic_file}: {str(e)}"}
    
    # Fallback to existing hardcoded methods...
    # (existing method mappings)
```

### Step 6: Test the Implementation
```python
# Test the workflows command
from orchestrator.cli_manager import CLICommandsManager

manager = CLICommandsManager()
result = manager.execute_command("workflows")
print(result)

# Should return cached result on second call
result2 = manager.execute_command("workflows")
print(f"Cached: {result2.get('cached', False)}")
```

### What This Achieves
- ✅ **Full MAO standardization** (CacheManager, @handle_errors, estimate_cost)
- ✅ **Intelligent caching** with workflow directory fingerprinting
- ✅ **Modular architecture** (logic file + enhanced JSON)
- ✅ **Dynamic routing** in CLI manager
- ✅ **Cost optimization** for repeated calls
- ✅ **Template for replication** across all 30 commands

### Replication Process
1. **Copy workflows template** → Rename for new command
2. **Adapt logic** for command-specific functionality  
3. **Update JSON config** with command-specific operations
4. **Test functionality** to ensure MAO compliance
5. **Repeat systematically** for all commands

*This concrete example shows exactly how the standardization works and can be replicated across all CLI commands.*