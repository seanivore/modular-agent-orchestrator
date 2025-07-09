# Multistage Codebase Audit Command

## Purpose
Execute comprehensive codebase audit with decision points, documentation consolidation, and visual diagram generation.

## Command Structure
```bash
claude > /project:multistage_audit ./complete_codebase_audit_spec.md
```

## Stage Overview

### **Stage 1: File Inventory & Sequential Analysis**
- Execute batches 1-5 sequentially (foundation files)
- Complete file inventory verification
- **Decision Point:** Review foundation analysis quality before proceeding

### **Stage 2: Parallel Batch Analysis** 
- Execute batches 6-24 in parallel (independent modules)
- Generate individual batch reports
- **Decision Point:** Review batch completeness and quality

### **Stage 3: Master Reports Generation**
- Consolidate findings into master reports
- Generate critical violations and fix specifications
- **Decision Point:** Approve violation inventory before documentation

### **Stage 4: Documentation Consolidation**
- Execute documentation consolidation spec
- Build fresh documentation from discoveries
- Compare against old documentation files
- **Decision Point:** Review documentation quality and completeness

### **Stage 5: Visual Documentation Assessment**
- **PAUSE:** Step back and assess documentation
- **Decision:** Identify areas that would benefit from diagrams
- **Options:** Architecture flow, API mappings, state management, error handling
- **Decision Point:** Approve diagram generation plan

### **Stage 6: Diagram Generation** (if approved)
- Generate Mermaid diagrams for approved areas
- Integrate visual documentation with written docs
- **Decision Point:** Review diagram quality and integration

### **Stage 7: Fresh Agent Review**
- Handoff to different agent for final review
- Use Sequential Thinking MCP for thorough analysis
- **Decision Point:** Approve final documentation package

## Decision Points

### **After Stage 1:**
- Are foundation files properly analyzed?
- Is file inventory 100% complete?
- Are critical violations properly flagged?

### **After Stage 2:**
- Are all 24 batches complete?
- Is documentation being written consistently?
- Are integration touchpoints being mapped?

### **After Stage 3:**
- Are master reports comprehensive?
- Are fix specifications actionable?
- Is violation inventory complete?

### **After Stage 4:**
- Is documentation accurate and complete?
- Are integration guides clear for UI development?
- Are extension procedures actionable?

### **After Stage 5:**
- **KEY DECISION:** Which areas need visual diagrams?
- Are there complex flows that need illustration?
- Would diagrams significantly help UI developers?

### **After Stage 6:**
- Do diagrams accurately represent the system?
- Are visuals properly integrated with documentation?
- Is the complete package ready for review?

### **After Stage 7:**
- Does fresh agent approve documentation quality?
- Are all requirements met for UI development?
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