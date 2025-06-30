# Task #5 CLI Commands Integration, Standardization, & Implementation Plan

---

## Process for Standardization 

**DO ONE FILE AT A TIME, THEN AUDIT THAT FILE**

  1. Choose one CLI command at a time 
  2. Sequential think and determine plan 
     - What does this CLI need? 
     - What touch points are required? 
     - What files will need to be edited? E.g. `orchestrator/cli_manager.py`
     - What files will need to be created? E.g. `configs/cli/[command].py`
     - Standard cost estimate with proper naming
       - Add to JSON to avoid hardcoding 
       - Note that Sonnet 4 will be Mao reading these messages and replies, use their costs 
      - Search text in quotes in terminal with `token` to see token count when estimating
     - Caching of all CLI commands and responses
       - Basic caching implemented for the most part
       - Need to add proper fingerprinting for all CLI commands and their responses
  3. Detail to Sean what is needed 
  4. Conduct implementation  
  5. Report on the results of the implementation 
  6. Sequential thinking + full audit 
     - Using `./versioning-docs/technical-documentation/MAO_FILE_STANDARDIZATION_RULES.md`
     - Don't rush, find detail oriented perfection
     - This is for all files related to the CLI command that was just implemented 
  7. Layout what is needed for the fix 
  8. Implement fixes 
  9. Report on results of the fix 
  10. Repeat for next CLI command 

---

## Unified CLI Command Architecture

ALL CLI commands should be treated the same way (except `restart` and `exit` which are app-only by nature)

### Command Characteristics
**Dual Interface Support:** Every command works both ways
- **Terminal:** `mao --command` 
- **In-App:** `/command`
- **Exceptions:** `restart` and `exit` (app-only, can't restart/exit from outside app)

**Examples from Command Chart:**
- `mao --setup ./config.json` AND `/setup ./config.json`
- `mao --workflows` AND `/workflows`  
- `mao --login` AND `/login`
- `uid` (standalone) AND `/uid` (in-app)

### Unified File Structure
**Every CLI command follows the same 2-file pattern:**
```
configs/cli/[command]/
├── [command].py          ← Logic file with full Mao standardization
└── [command].json        ← Enhanced config
```

**No distinctions needed** - Whether it's:
- Workflow operations (`setup`, `update`, `fix-it`)
- System information (`stats`, `workflows`, `list-tools`)
- User management (`login`, `logout`, `user-id`)
- Utility functions (`uid`, `help`, `doctor`)

**All get identical treatment:**
- CacheManager + fingerprinting
- @handle_errors decorators
- estimate_cost() functions  
- Dynamic routing in CLI manager
- Work both terminal and in-app

---

## Standardization Requirements

**Logic File** 

```python
# configs/cli/[command].py
"""
[Command] CLI Command - Core Logic
[Description of what this command does]
"""
# Standard Mao imports 
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors, ValidationError

# Standard cache instance
cache = CacheManager()

# Required functions
def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate operation cost for budget planning"""
    pass

def [command]_operation(specific_params) -> Dict[str, Any]:
    """Specific operations as needed"""
    pass

# All main functions need @handle_errors decorator
@handle_errors(operation_name="[command]", return_dict=True)
def execute_[command](params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Main command execution with caching and error handling"""
    pass

# Intelligent caching with fingerprinting
def _generate_cache_key(input_params) -> str:
    """Generate cache key based on input fingerprints"""
    pass

# Standalone functions for app integration
def script_function_name(params) -> return_type:
    """Standalone function for app imports"""
    pass

# Standalone function for CLI manager import
def execute_command(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Standalone function for CLI manager"""
    return execute_[command](params)
```

**JSON Config:**

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
