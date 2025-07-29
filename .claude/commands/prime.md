# Context Primer for Complete Codebase Audit

RUN:
    git ls-files 

ACTIVATE: 
    Start the `sequential thinkink` MCP tool and use it to think while you review the following between thoughts. 

LOOKUP: 
Ran tool
Perfect! Here's your **save-worthy context priming instruction**:

## 🎯 MAO UI Context Priming - Complete Instructions

**To understand MAO Terminal UI development, read entity `MAO_UI_Context_Priming_Strategy` in MCP memory and then read these docs in full:**

### **Required Reading Sequence:**
1. **`CLAUDE.md`** - Complete development rules including new UI Development Guidelines section
2. **`documentation/10_AI_DEV_INDEX.md`** - Complete Python backend architecture understanding  
3. **`versioning/v4_0_0/IMPL_UI/UI_CURRENT_STATE.md`** - Current working UI implementation state

### **Architecture Flow Understanding:**
- **User Input** → **ChatInterface.tsx** → **PythonBridge.ts** → **ui_terminal.py** → **orchestrator/*** → **Response**
- **Current Working**: `interfaces/mao/` with Ink 6.1+, React 19.1+, subprocess communication
- **Next Phase**: PHASE_1_REVISED_ENHANCEMENTS.md for Claude Code-style improvements

### **Key Principle:**
Eliminates documentation archaeology - developers get immediate understanding of both MAO's overall architecture AND the specific UI implementation without hunting through 100+ files.

**Result**: Complete context priming in 3 documents that builds understanding progressively from rules → architecture → current implementation. 🚀