**CLI IMPLEMENTATION VOLLEY SPECIFICATION**

This specification defines the systematic implementation of MAO CLI commands using either sequential or parallel volley workflows. Designed specifically for the remaining CLI commands (#4-24) with proven patterns, architectural clarity, and quality standards.

**SOURCE DOCUMENTS:**
- **Command Reference:** `./versioning-docs/v4_MAO/CLI_COMMAND_STANDARDIZATION_PLAN.md`
- **Quality Standards:** `./versioning-docs/technical-documentation/MAO_FILE_STANDARDIZATION_RULES.md`
- **Proven Pattern:** Implementation success from commands #1-4 (help, tools, models, providers)

---

## **CRITICAL ARCHITECTURE UNDERSTANDING**

### **Two-Layer System Architecture**
```
CLI-CONFIGS (Command Implementation):
./configs/cli/COMMAND/
├── COMMAND.json        ← Command configuration
├── COMMAND.py          ← Core logic with MAO standardization
└── ui_COMMAND.py       ← UI display patterns

DATA-CONFIGS (Information Sources):
./configs/providers/    ← Individual provider JSON files  
./configs/models/       ← Individual model JSON files
./configs/workflows/    ← Individual workflow JSON files
```

### **Path Resolution Rules**
- **CLI Commands READ FROM** data directories (`./configs/providers/`, `./configs/models/`)
- **CLI Commands WRITE TO** their own directory (`./configs/cli/COMMAND/`)
- **Managers Handle Loading** from individual JSON files (drop-in/drop-out modularity)
- **No Unified Files** - Everything is modular individual JSON files

---

## **COMMAND TYPE CATEGORIES**

### **Category A: Data Display Commands (Simple)**
**Commands:** `providers`, `workflows`, `stats`, `tools`, `models`, `help`
**Characteristics:** Read data, format display, minimal logic
**Implementation Pattern:** File scanning + UI formatting
**Complexity:** Low
**Parallelizable:** ✅ High (no conflicts)

### **Category B: Manager Integration Commands (Medium)**  
**Commands:** `config`, `login`, `logout`, `user_id`, `workflow_id`, `variables`
**Characteristics:** Integrate with existing managers, state changes
**Implementation Pattern:** Manager method calls + state handling
**Complexity:** Medium
**Parallelizable:** ⚠️ Moderate (potential manager conflicts)

### **Category C: Workflow Operations (Complex)**
**Commands:** `goal`, `setup`, `update`, `continue`, `review`, `fix_it`, `doctor`, `dry_run`
**Characteristics:** Complex workflow logic, file operations, orchestrator integration
**Implementation Pattern:** Workflow manager + orchestrator integration
**Complexity:** High  
**Parallelizable:** ❌ Low (high integration dependencies)

---

## **3-PHASE VOLLEY PATTERN FOR CLI COMMANDS**

### **PHASE 1: REQUIREMENTS ANALYSIS**

**For Each CLI Command, Analyze:**

**A. Command Functionality Assessment**
```
REQUIRED ANALYSIS:
- What does this CLI command provide to users?
- Which data sources does it read from? (./configs/X/ directories)
- What processing logic is needed?
- How does it fit into the overall CLI structure?
- What are the terminal and in-app command variants?
```

**B. Architecture Integration Points**
```
INTEGRATION TOUCHPOINTS:
- Universal: cli_manager.py (routing), ui_terminal.py (slash commands)
- Manager-Specific: Which orchestrator managers are involved?
  * username_manager.py (login, logout, user_id)
  * workflow_manager.py (workflows, workflow_id, setup, review)
  * settings_manager.py (config, output, model settings)
  * real_time_metrics.py (stats, performance data)
  * manager_models.py (models, providers discovery)
  * manager_tools.py (tools discovery)

DATA DEPENDENCIES:
- Which ./configs/ directories need to be scanned?
- Are there connection files needed? (providers_x_models.json)
- What file modification tracking is needed for caching?
```

**C. Implementation Strategy**
```
COST ESTIMATION (Claude Sonnet 4):
- Data Display: 0.001 (file reading only)
- Manager Integration: 0.002-0.005 (logic processing)
- Workflow Operations: 0.01-0.05 (complex orchestrator calls)

CACHING STRATEGY:
- Duration: 5min (dynamic), 15min (semi-static), 1hr (static)
- Fingerprinting: Directory mod times, file counts, content hashes
- Cache Keys: Include system state that affects command output

UI DISPLAY APPROACH:
- Essential data structure only
- No detailed formatting specifications  
- Preserve creative freedom for UI designers
- Text-based visual hierarchy (no emoji)
```

### **PHASE 2: IMPLEMENTATION**

**A. Create 3-File Structure**

**1. Command JSON Configuration**
```json
{
  "name": "COMMAND_NAME",
  "command": "COMMAND_NAME", 
  "type": "standalone",
  "terminal_flag": "--COMMAND_NAME",
  "app_command": "/COMMAND_NAME",
  "interface_method": "COMMAND_METHOD",
  "help": "Brief description for help display",
  "cost_estimate": 0.001,
  "file_path": "configs/cli/COMMAND_NAME/COMMAND_NAME.py",
  "ui_path": "configs/cli/COMMAND_NAME/ui_COMMAND_NAME.py",
  "operations": {
    "execute": {
      "description": "Main command operation",
      "required_params": [],
      "optional_params": []
    }
  },
  "integration": {
    "memory_mcp": false,
    "cache_system": true, 
    "error_handling": true,
    "manager_touchpoints": ["RELEVANT_MANAGERS"]
  },
  "cache_settings": {
    "enabled": true,
    "duration_seconds": 900,
    "cache_key_includes": ["RELEVANT_STATE"]
  }
}
```

**2. Core Logic File Template**
```python
"""
COMMAND_NAME CLI Command - Core Logic
[Brief description of command functionality]
"""

import json
import hashlib
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Standard MAO imports
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, retry_with_backoff, APIError

# Standard cache instance
cache = CacheManager()

@handle_errors(operation_name="COMMAND_NAME", return_dict=True)
def execute_COMMAND_NAME(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main command execution with caching and error handling.
    
    Args:
        params: Command parameters from CLI/app input
        
    Returns:
        Standardized result dictionary
    """
    # Check cache first
    cache_key = _generate_cache_key(params)
    cached_result = cache.get_cached_analysis(cache_key, "COMMAND_NAME")
    if cached_result:
        return json.loads(cached_result)
    
    # Execute command logic
    result = _execute_command_logic(params)
    
    # Cache result with appropriate duration
    cache.cache_content_analysis(cache_key, json.dumps(result), "COMMAND_NAME")
    
    return result

def estimate_cost(params: Dict[str, Any] = None) -> float:
    """
    Estimate operation cost for budget planning.
    Uses Claude Sonnet 4 cost structure.
    """
    # Adjust based on command complexity
    return 0.001  # Default for data display commands

def _generate_cache_key(params: Dict[str, Any] = None) -> str:
    """Generate fingerprinted cache key including relevant system state"""
    base_key = f"COMMAND_NAME|{str(params) if params else 'none'}"
    
    # Add system state fingerprints relevant to this command
    # Examples:
    # - Directory modification times
    # - File counts in relevant directories
    # - Connection file states
    
    return hashlib.md5(base_key.encode()).hexdigest()[:16]

def _execute_command_logic(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Core command logic implementation"""
    # Command-specific implementation here
    pass

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager routing"""
    return execute_COMMAND_NAME(params)
```

**3. UI Display File Template**
```python
"""
COMMAND_NAME CLI Command - UI Display Patterns
Essential data structure for COMMAND_NAME display
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any, List

# Module-level console for consistency
console = Console()

def display_COMMAND_NAME_result(result: Dict[str, Any]) -> None:
    """
    Display COMMAND_NAME results with consistent CLI UI patterns.
    
    Args:
        result: Command execution result from COMMAND_NAME.py
    """
    if not result.get("success", True):
        display_error(result.get("error", "Unknown error occurred"))
        return
    
    # Essential data structure for UI designers
    # Focus on data organization, not detailed formatting
    # Preserve creative freedom for actual interface design
    
    pass

def display_error(error_message: str) -> None:
    """Display error with consistent Panel formatting"""
    console.print(Panel(
        f"[red]Error:[/red] {error_message}",
        style="red",
        title="COMMAND_NAME Error"
    ))
```

**B. Manager Integration Patterns**

**Data Display Commands:**
```python
# Scan directory for individual JSON files
data_dir = Path(__file__).parent.parent.parent / "DATA_TYPE"
for file in data_dir.glob("*.json"):
    with open(file, 'r') as f:
        config = json.load(f)
```

**Manager Integration Commands:**
```python
# Import and use existing managers
from orchestrator.RELEVANT_manager import ManagerClass
manager = ManagerClass()
result = manager.relevant_method(params)
```

**Workflow Operations:**
```python
# Complex orchestrator integration
from orchestrator.workflow_manager import WorkflowManager
from orchestrator.memory_mcp import MemoryMCP
workflow_manager = WorkflowManager()
memory = MemoryMCP()
```

### **PHASE 3: QUALITY AUDIT**

**A. MAO Standardization Compliance Checklist**

**Logic File Requirements:**
- ✅ Standard MAO imports (CacheManager, handle_errors, retry_with_backoff, APIError)
- ✅ estimate_cost() function implemented
- ✅ @handle_errors decorators applied to main functions
- ✅ Standard caching pattern with fingerprinting
- ✅ Standalone execute_command() function for CLI manager
- ✅ No emoji icons or version numbers in headers
- ✅ Professional error handling throughout

**UI File Requirements:**
- ✅ Data-focused display patterns only
- ✅ Essential information structure preserved
- ✅ No detailed formatting specifications
- ✅ Text-based visual hierarchy maintained
- ✅ Creative freedom preserved for UI designers

**JSON Config Requirements:**
- ✅ Uses "name" field (MAO standard)
- ✅ Proper file_path and ui_path fields
- ✅ Cost estimate included
- ✅ Integration touchpoints specified
- ✅ Cache settings configured appropriately

**B. Integration Testing**
```
VALIDATION REQUIREMENTS:
- Command JSON loads without errors
- Core logic executes without import issues
- Cache system integration works properly
- Manager touchpoints connect correctly
- UI display handles both success and error cases
- File paths resolve correctly in two-layer architecture
```

**C. System Integration**
```
CLI MANAGER ROUTING TEST:
- Command discoverable via directory scan
- Interface method maps correctly
- Terminal and in-app variants work
- Help text displays properly

ORCHESTRATOR INTEGRATION TEST:
- Manager connections function correctly
- No import conflicts with existing system
- Error handling integrates with system patterns
- Memory/state management works as expected
```

---

## **PARALLEL PROCESSING GUIDELINES**

### **Batch Grouping Strategy**

**Safe Parallel Batches (No Conflicts):**
- **Batch A:** `providers`, `workflows`, `stats` (pure data display)
- **Batch B:** `tools`, `models`, `help` (directory scanning)
- **Batch C:** `variables`, `user_id`, `workflow_id` (simple manager calls)

**Sequential Dependencies:**
- `login` → `logout` (user session management)
- `setup` → `update` → `fix_it` (workflow operations)
- `config` affects multiple other commands

**Coordination Points:**
- Manager import conflicts (same manager used by multiple commands)
- Shared cache namespaces
- CLI manager routing updates

---

## **SUCCESS CRITERIA**

**Per Command Implementation:**
- ✅ 3-file structure created with correct naming and full MAO compliance
- ✅ 100% compliance with MAO_FILE_STANDARDIZATION_RULES.md requirements
- ✅ Proper integration with identified orchestrator touchpoints
- ✅ Professional code quality suitable for production deployment
- ✅ Intelligent caching with appropriate fingerprinting
- ✅ Cost estimation accurate for Claude Sonnet 4 operations

**System Integration:**
- ✅ CLI Manager routing updated and functional for all new commands
- ✅ Terminal and in-app command variants work correctly
- ✅ Git-style help grouping displays commands appropriately
- ✅ No hardcoded references anywhere in the system
- ✅ Quality consistency with established pattern from commands #1-4

**Architecture Validation:**
- ✅ Two-layer architecture properly maintained
- ✅ Drop-in/drop-out modularity preserved
- ✅ Manager integration follows existing patterns
- ✅ Error handling and caching integrate with MAO systems

---

## **IMPLEMENTATION WORKFLOW**

### **Sequential Approach:**
```bash
# Process single command with proven pattern
/project:sequential_volley ./cli_implementation_volley_spec.md COMMAND_NUMBER
```

### **Parallel Approach:**
```bash
# Process command batches with coordinated agents
/project:parallel_volley ./cli_implementation_volley_spec.md 5-10 3
/project:parallel_volley ./cli_implementation_volley_spec.md 11-18 4  
/project:parallel_volley ./cli_implementation_volley_spec.md 19-24 3
```

---

This specification provides complete guidance for systematic CLI command implementation while maintaining MAO quality standards, architectural integrity, and proven implementation patterns from our successful commands #1-4.