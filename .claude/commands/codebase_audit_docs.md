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
- **Memory MCP Checkpoint:** Query current audit state for session recovery
- Verify file inventory completeness (100% coverage)
- Validate batch definitions accuracy
- Confirm execution environment readiness
- **Memory MCP Save:** "Stage 0 Pre-Execution - Environment validated, ready to begin"
- **Decision Point:** Approve execution readiness before proceeding

### **Stage 1: File Inventory & Sequential Analysis**
- **Memory MCP Query:** Check batch completion status (batches 1-5)
- Execute batches 1-5 sequentially (foundation files)
- **Memory MCP Save:** After each batch - "Batch [X] completed - [key violations found]"
- Complete file inventory verification
- **Mid-Stage Decision Point:** Review foundation analysis after batches 1-3
- **Memory MCP Save:** "Stage 1 Mid-Point - Foundation analysis quality approved"
- **Decision Point:** Review foundation analysis quality before proceeding

### **Stage 2: Parallel Batch Analysis** 
- **Memory MCP Query:** Check parallel batch completion status (batches 6-24)
- Execute batches 6-24 in parallel (independent modules)
- **Memory MCP Save:** Track batch completion - "Batch [X] completed - [violations and discoveries]"
- Generate individual batch reports
- **Mid-Stage Decision Point:** Review parallel batch progress at 50% completion
- **Memory MCP Save:** "Stage 2 Mid-Point - 50% parallel batches complete, quality approved"
- **Decision Point:** Review batch completeness and quality

### **Stage 3: Master Reports Generation**
- **Memory MCP Query:** Retrieve all batch findings for consolidation
- Consolidate findings into master reports
- Generate critical violations and fix specifications
- **Memory MCP Save:** "Stage 3 - Master reports generated, [X] critical violations documented"
- **Quality Gate:** Comprehensive violation inventory review
- **Decision Point:** Approve violation inventory before documentation

### **Stage 4: Documentation Consolidation**
- **Memory MCP Query:** Retrieve all documentation updates from batches
- Execute documentation consolidation using `docs_spec`
- Input: All batch reports and analysis from Stages 1-3
- Use Sequential Thinking MCP for consolidation strategy
- Build fresh documentation from audit discoveries
- Compare against existing documentation files
- **Memory MCP Save:** "Stage 4 - Documentation consolidated, [X] sections updated"
- **Decision Point:** Review documentation quality and completeness

### **Stage 5: Visual Documentation Assessment**
- **PAUSE:** Review consolidated documentation from Stage 4
- **Assessment:** Identify complex areas that would benefit from visual diagrams
- **Human Understanding Focus:** What diagrams would make documentation easier for humans to understand?
- **Priority Options:** Integration touchpoint diagrams (TypeScript↔Python), API mappings, architecture flow
- **Additional Options:** State management, error handling, workflow diagrams
- **Memory MCP Save:** "Stage 5 - Visual assessment complete, [X] diagrams approved for generation"
- **Decision Point:** Approve diagram generation plan for enhanced human comprehension

### **Stage 6: Diagram Generation** (if approved)
- Generate Mermaid diagrams for approved areas
- Integrate visual documentation with written docs
- **Memory MCP Save:** "Stage 6 - [X] diagrams generated and integrated"
- **Decision Point:** Review diagram quality and integration

### **Stage 7: Independent Agent Review**
- **Memory MCP Query:** Retrieve complete audit package for independent review
- **Fresh Agent Handoff:** Different agent reviews complete documentation package
- **Independent Assessment:** Fresh perspective on documentation quality and completeness
- **Use Sequential Thinking MCP for thorough analysis**
- **Final Quality Gate:** Comprehensive system validation by independent reviewer
- **Memory MCP Save:** "Stage 7 - Independent review complete, audit approved for implementation"
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

- **Memory MCP Integration** - Query state before starting, save at each checkpoint
- **Session Recovery** - Use Memory MCP to resume from any stage
- **Pause at each decision point** - Don't rush through
- **Use Sequential Thinking** for complex decisions
- **Quality over speed** - Each stage builds on previous
- **Collaborative approach** - Decision maker input required

## Session Recovery Protocol

**To Resume Mid-Audit:**
1. Query Memory MCP: "What is the current state of Full_Codebase_Audit for Mao_v4_Build?"
2. Review stage completion status and last checkpoint
3. Identify next required action based on saved state
4. Continue from appropriate stage with full context

**Common Recovery Points:**
- After Stage 1: Continue with parallel batch analysis
- After Stage 3: Continue with documentation consolidation
- After Stage 5: Continue with diagram generation (if approved)
- After Stage 6: Continue with independent agent review

---

*This command provides structured, decision-driven execution of the complete codebase audit with built-in quality gates and flexibility for visual documentation.*