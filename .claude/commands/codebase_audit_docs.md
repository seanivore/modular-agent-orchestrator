# Full Codebase Audit: A Multistage Command with Dual Specs for Technical Documentation Completion 

## Purpose
Execute comprehensive codebase audit with decision points, documentation consolidation, and visual diagram generation.

## Command Structure
```bash
claude > /project:codebase_audit_docs ./codebase_audit_spec.md ./documentation_spec.md batch_01_root_files.md
```

**Variables:**
audit_spec: $ARGUMENTS
docs_spec: $ARGUMENTS
batch_file: $ARGUMENTS

**ARGUMENTS PARSING:**
1. `audit_spec` - Complete codebase audit specification
2. `docs_spec` - Documentation consolidation specification
3. `batch_file` - Specific batch to execute (eliminates confusion)

## Stage Overview

### **Stage 0: Pre-Execution Validation**
- Verify file inventory completeness (100% coverage)
- Validate batch definitions accuracy
- Confirm execution environment readiness
- **Decision Point:** Approve execution readiness before proceeding

### **Stage 1: File Inventory & Sequential Analysis**
- Execute batches 1-5 sequentially (foundation files)
- Complete file inventory verification
- **Mid-Stage Decision Point:** Review foundation analysis after batches 1-3
- **Decision Point:** Review foundation analysis quality before proceeding

### **Stage 2: Parallel Batch Analysis** 
- Execute batches 6-24 in parallel (independent modules)
- Generate individual batch reports
- **Mid-Stage Decision Point:** Review parallel batch progress at 50% completion
- **Decision Point:** Review batch completeness and quality

### **Stage 3: Master Reports Generation**
- Consolidate findings into master reports
- Generate critical violations and fix specifications
- **Quality Gate:** Comprehensive violation inventory review
- **Decision Point:** Approve violation inventory before documentation

### **Stage 4: Documentation Consolidation**
- Execute documentation consolidation using `docs_spec`
- Input: All batch reports and analysis from Stages 1-3
- Use Sequential Thinking MCP for consolidation strategy
- Build fresh documentation from audit discoveries
- Compare against existing documentation files
- **Decision Point:** Review documentation quality and completeness

### **Stage 5: Visual Documentation Assessment**
- **PAUSE:** Review consolidated documentation from Stage 4
- **Assessment:** Identify complex areas that would benefit from visual diagrams
- **Human Understanding Focus:** What diagrams would make documentation easier for humans to understand?
- **Priority Options:** Integration touchpoint diagrams (TypeScript↔Python), API mappings, architecture flow
- **Additional Options:** State management, error handling, workflow diagrams
- **Decision Point:** Approve diagram generation plan for enhanced human comprehension

### **Stage 6: Diagram Generation** (if approved)
- Generate Mermaid diagrams for approved areas
- Integrate visual documentation with written docs
- **Decision Point:** Review diagram quality and integration

### **Stage 7: Independent Agent Review**
- **Fresh Agent Handoff:** Different agent reviews complete documentation package
- **Independent Assessment:** Fresh perspective on documentation quality and completeness
- **Use Sequential Thinking MCP for thorough analysis**
- **Final Quality Gate:** Comprehensive system validation by independent reviewer
- **Decision Point:** Independent agent approval of final documentation package

## Decision Points

### **After Stage 0:**
- Is file inventory 100% complete and accurate?
- Are batch definitions properly structured?
- Is execution environment ready for large-scale analysis?

### **Stage 1 Mid-Point:**
- Are foundation batches 1-3 producing quality analysis?
- Is violation detection working properly?
- Are integration touchpoints being mapped correctly?

### **After Stage 1:**
- Are foundation files properly analyzed?
- Is file inventory 100% complete?
- Are critical violations properly flagged?

### **Stage 2 Mid-Point:**
- Is parallel batch execution proceeding smoothly?
- Are batch reports maintaining consistent quality?
- Are any coordination issues emerging?

### **After Stage 2:**
- Are all 24 batches complete?
- Is documentation being written consistently?
- Are integration touchpoints being mapped?

### **Stage 3 Quality Gate:**
- Are violation inventories comprehensive?
- Are fix specifications actionable?
- Is cross-file analysis complete?

### **After Stage 3:**
- Are master reports comprehensive?
- Are fix specifications actionable?
- Is violation inventory complete?

### **After Stage 4:**
- Is documentation accurate and complete?
- Are integration guides clear for UI development?
- Are extension procedures actionable?

### **After Stage 5:**
- **KEY DECISION:** Which areas of consolidated documentation need visual diagrams?
- **Priority Focus:** Integration touchpoint diagrams for TypeScript↔Python communication
- Are there complex flows that need illustration for human understanding?
- Would diagrams significantly help UI developers and future maintainers?
- What visual formats would be most effective?

### **After Stage 6:**
- Do diagrams accurately represent the system?
- Are visuals properly integrated with documentation?
- Is the complete package ready for review?

### **Final Quality Gate (Independent Agent):**
- Does independent agent approve documentation quality?
- Are all requirements met for UI development?
- Is documentation clear and comprehensive for human understanding?
- Is the audit complete and ready for implementation?

## Quality Gates

### **Stage Completion Criteria:**
- All deliverables produced per stage requirements
- Quality standards met at each decision point
- Decision maker approval before proceeding

### **Final Success Criteria:**
- 24 batches analyzed (~270 files)
- 7 master reports generated
- Complete documentation package ready
- Visual diagrams (if approved) integrated
- Fresh agent quality review passed

## Usage Notes

- **Pause at each decision point** - Don't rush through
- **Use Sequential Thinking** for complex decisions
- **Quality over speed** - Each stage builds on previous
- **Collaborative approach** - Decision maker input required

---

*This command provides structured, decision-driven execution of the complete codebase audit with built-in quality gates and flexibility for visual documentation.*