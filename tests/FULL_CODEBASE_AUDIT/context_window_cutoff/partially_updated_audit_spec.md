# Complete Codebase Audit & Standardization Specification

## Core Challenge

Systematically analyze all 292 Mao files to **document bugs, redundancies, and standardization violations** with detailed fix recommendations. Create comprehensive violation inventory and integration mapping to enable controlled, verified fixes before UI development.

**The Goal:** Create detailed violation reports with actionable fix specifications that can be reviewed, approved, and executed in controlled batches with full before/after verification.

---

## Output Requirements

### **File Naming**: `batch_[number]_[category]_analysis.md`

### **Directory Structure**:
```
tests/FULL_CODEBASE_AUDIT/
├── 00_EXECUTIVE_SUMMARY.md            ← Complete findings overview with critical issues
├── 01_CRITICAL_VIOLATIONS.md          ← Immediate fixes needed with detailed implementation specs
├── 02_UI_INTEGRATION_MAP.md           ← TypeScript→Python integration requirements
├── 03_DEPENDENCY_MATRIX.md            ← Complete file dependency mapping
├── 04_STANDARDIZATION_REPORT.md       ← Mao compliance violations with fix specifications
├── 05_DUPLICATE_CODE_REPORT.md        ← Function redundancy with merge/consolidation specs
├── 06_FIX_IMPLEMENTATION_SPECS.md     ← Actionable fix specifications for approved changes
└── batch_reports/
    ├── batch_01_orchestrator.md       ← Individual batch analyses
    ├── batch_02_interfaces.md
    └── [continues through batch_14...]
```

### **Master Report Format**:
```markdown
# Codebase Analysis - [CATEGORY]

## Critical Issues Found
- **VIOLATION:** [Type] in [file:line] - [specific issue]
- **CURRENT CODE:** ```[exact code that violates standard]```
- **PROPOSED FIX:** ```[exact replacement code]```
- **IMPACT:** [what this change affects]
- **DEPENDENCIES:** [other files that may be affected]

## Integration Touchpoints  
- **CALLS:** [files this depends on]
- **CALLED BY:** [files that depend on this]
- **UI INTEGRATION:** [TypeScript API needs]

## Fix Implementation Specifications
- **FILE:** [exact file path]
- **ACTION:** [REPLACE | INSERT | DELETE | RENAME]
- **LOCATION:** [line numbers or function names]
- **BEFORE:** ```[current code block]```
- **AFTER:** ```[proposed code block]```
- **VALIDATION:** [how to verify fix worked]
```

---

## Execution Strategy

### **Batch Processing Commands**

**SEQUENTIAL (Core Dependencies):**
```bash
# Batch 1: Orchestrator files (20 files) - Heavy interdependencies
claude > /project:sequential_volley ./complete_codebase_audit_spec.md batch=1

# Batch 2: Interfaces (2 files) - Depends on orchestrator analysis  
claude > /project:sequential_volley ./complete_codebase_audit_spec.md batch=2

# Batch 14: Root files including mao_v4.py - Depends on orchestrator understanding
claude > /project:sequential_volley ./complete_codebase_audit_spec.md batch=14
```

**PARALLEL (Independent Modules):**
```bash
# Batches 3-4: CLI commands (independent modules)
claude > /project:parallel_volley ./complete_codebase_audit_spec.md batch_range=3-4

# Batches 5-8: Config files (independent configurations)
claude > /project:parallel_volley ./complete_codebase_audit_spec.md batch_range=5-8

# Batches 9-11: Tools (independent implementations)  
claude > /project:parallel_volley ./complete_codebase_audit_spec.md batch_range=9-11

# Batches 12-13: Scripts/templates (independent support files)
claude > /project:parallel_volley ./complete_codebase_audit_spec.md batch_range=12-13
```

### **Batch Distribution**:
```
SEQUENTIAL BATCHES (3):
├── Batch 1: orchestrator/ (20 files)
├── Batch 2: interfaces/ (2 files)  
└── Batch 14: root files including mao_v4.py (2 files)

PARALLEL BATCHES (11):
├── Batches 3-4: configs/cli/ (37 commands)
├── Batches 5-8: configs/models, providers, settings, connections (26 files)
├── Batches 9-11: tools/ (74 tools)
└── Batches 12-13: scripts/, templates/ (34 files)
```

---

## Analysis Standards

### **Universal Requirements (Every File)**

**Apply this analysis to ALL 292 files:**

```markdown
### [FILE_NAME]
**Path:** [FULL_PATH]
**Type:** [Python/JSON/Script/Template]

**CRITICAL VIOLATIONS:**
- [ ] ❌ Hardcoded references (breaks modularity)
- [ ] ❌ Duplicate functions (breaks DRY principle)  
- [ ] ❌ Missing error handling (@handle_errors required)
- [ ] ❌ Print statements in system files (prohibited)
- [ ] ❌ State management outside Memory MCP (orchestrator only)

**STANDARDIZATION COMPLIANCE:**
- [ ] ✅ Standard imports (CacheManager, handle_errors)
- [ ] ✅ Cost estimation function (where required)
- [ ] ✅ Proper return types (Dict[str, Any])
- [ ] ✅ No version numbers in headers
- [ ] ✅ "Mao" not "MAO" (correct pronunciation)

**INTEGRATION MAPPING:**
- **Dependencies:** [what this file needs]
- **Dependents:** [what needs this file]  
- **TypeScript API:** [HTTP endpoints required]
- **Real-time Updates:** [WebSocket streaming needed]
```

### **Code Quality