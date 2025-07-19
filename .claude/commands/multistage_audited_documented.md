**MULTI-STAGE DOCUMENTATION PROJECT WITH INTEGRATED AUDIT & PROGRESS TRACKING**

Intelligently orchestrate large-scale documentation projects through adaptive multi-stage execution with comprehensive QA, architectural compliance auditing, and robust progress tracking.

**Variables:**

spec_file: $ARGUMENTS

**ARGUMENTS PARSING:**
Parse the following arguments from "$ARGUMENTS":
1. `spec_file` - Path to the markdown specification file defining the documentation project requirements

**PHASE 1: SPECIFICATION ANALYSIS & PROGRESS SYSTEM SETUP**

Read and deeply analyze the specification file at `spec_file` to understand:
- **Documentation Scope**: Files to document, questionnaire patterns, output requirements
- **Batch Structure**: Sequential vs parallel phases, dependencies between batches
- **Context Management**: How knowledge builds progressively across documentation phases
- **Quality Requirements**: Architectural compliance, professional standards, completeness validation
- **Progress Tracking**: Number of batches, files, and deliverables for status management

**Progress Tracking System Setup:**
```
Create progress tracking directory: ./.claude/multi-audit-doc-status/
├── session_state.json          # Current session progress and context
├── batch_completion.json       # Batch-by-batch completion tracking  
├── context_summaries.json      # Progressive knowledge accumulation
├── quality_checkpoints.json    # Audit compliance tracking
└── agent_handoffs.json         # Context transfer protocols
```

**Initial Progress State Creation:**
```json
{
  "project_name": "Extracted from spec_file",
  "session_id": "timestamp_based_unique_id", 
  "total_phases": "extracted_from_spec",
  "total_batches": "extracted_from_spec",
  "total_files": "extracted_from_spec",
  "current_phase": 1,
  "current_batch": null,
  "completed_batches": [],
  "failed_batches": [],
  "session_start": "ISO_timestamp",
  "last_update": "ISO_timestamp",
  "architecture_compliance_verified": false
}
```

**PHASE 2: INTELLIGENT WORKFLOW DESIGN WITH CONTEXT STRATEGY**

Based on specification analysis, design optimal execution strategy with sophisticated context management:

**Context Management Protocol:**
- **Batch-Level Assignment**: Complete batches assigned to single agents (not individual files)
- **Progressive Summarization**: After each batch, create intermediate context documents
- **Shared Knowledge Repository**: Build cumulative understanding documents in `.claude/multi-audit-doc-status/context_summaries.json`
- **Strategic Handoffs**: Explicit context transfer protocols between sequential phases
- **Scope Boundaries**: Clear architectural understanding prevents agent overlap

**Documentation-Specific Workflow Design:**
```
IF (Foundation phase identified):
    → Sequential execution with architecture principle establishment
    → Create "core_architecture_summary.md" for subsequent phases
    
IF (Module phases identified):
    → Parallel execution by logical module groupings
    → Each agent references foundation summary + creates module summary
    
IF (Integration phase identified):
    → Sequential execution consuming all previous summaries
    → Final integration and cross-module consistency validation
```

**Agent Coordination Strategy for Documentation:**
- **Knowledge Building**: Each agent contributes to cumulative understanding
- **Context Inheritance**: Later agents reference summaries from earlier work
- **Overlap Prevention**: Clear batch boundaries with architectural context
- **Quality Consistency**: Shared questionnaire patterns and compliance checking

**PHASE 3: ADAPTIVE EXECUTION WITH DOCUMENTATION INTELLIGENCE**

**Stage 1: Foundation Documentation** (If Sequential Phase Identified)
```
Launch FOUNDATION AGENT with:
- Complete specification context
- Architecture principles document analysis
- Foundation batch questionnaires
- Responsibility for creating "core_architecture_summary.md"
- Progress tracking updates to session_state.json

Update Progress: Mark foundation batches as in_progress → completed
```

**Stage 2: Parallel Module Documentation** (If Parallel Phases Identified)
```
Determine optimal agent distribution for module documentation:
- Group related module batches logically (tools, CLI, config, templates)
- Launch 2-4 parallel agents based on module complexity
- Each agent receives: foundation summary + specific module batches
- Assign distinct module focus areas to prevent overlap
- Each agent creates module-specific summary for integration

Agent Assignment Strategy:
- Tools Ecosystem Agent: All tool-related batches
- CLI System Agent: All command-related batches  
- Configuration Agent: All config-related batches
- Templates/Scripts Agent: All template-related batches

Update Progress: Track each module batch completion in batch_completion.json
```

**Stage 3: Integration Documentation** (Sequential Final Phase)
```
Launch INTEGRATION AGENT with complete context:
- All foundation and module summaries
- Integration batch questionnaires
- Cross-module consistency validation
- Final architecture compliance verification
- Complete deliverable validation

Update Progress: Mark integration batches and final completion
```

**PHASE 4: COMPREHENSIVE QA WITH ARCHITECTURAL COMPLIANCE AUDIT**

**Documentation Quality Assurance:**
```
Launch REVIEW AGENT with complete context:
- Test all deliverables against specification requirements
- Verify questionnaire completion across all batches
- Check professional documentation standards
- Validate file naming conventions and output locations
- Execute comprehensive architectural compliance audit
- Ensure documentation completeness and consistency
- Cross-reference all batch outputs for integration
```

**Integrated Architectural Compliance Audit:**
Execute comprehensive audit as integral part of final QA:

**Documentation-Specific Compliance:**
- [ ] All questionnaires fully answered with codebase information
- [ ] Documentation emphasizes LOCAL application architecture
- [ ] No web service or API provider patterns documented
- [ ] File naming follows batch_number_file_name.md convention
- [ ] All deliverables saved to correct /documentation/GATHERED_INFO/ paths
- [ ] Architecture principles correctly understood and documented

**Architecture Pattern Compliance:**
- [ ] Documentation reflects modular discovery patterns
- [ ] LOCAL terminal application concepts correctly documented
- [ ] Memory MCP integration documented as single source of truth
- [ ] Privacy-first architecture principles reflected in documentation
- [ ] Real-time data patterns documented (no mock data references)

**Documentation Integration Validation:**
- [ ] Progressive knowledge building evident across phases
- [ ] Context summaries properly reference earlier work
- [ ] Cross-module relationships properly documented
- [ ] No contradictions between different batch documentations
- [ ] Complete coverage of all specified files and questionnaires

**Progress Tracking Audit:**
- [ ] All batch completion properly tracked in JSON files
- [ ] Context summaries accurately reflect cumulative knowledge
- [ ] Quality checkpoints document architectural compliance
- [ ] Session recovery information complete for future sessions

**PHASE 5: PROGRESS TRACKING & SESSION RECOVERY**

**Continuous Progress Updates:**
Throughout execution, maintain real-time updates to tracking files:

```json
// batch_completion.json updates
{
  "batch_01_root_files": {
    "status": "completed",
    "agent_id": "foundation_agent_001", 
    "files_documented": 1,
    "deliverables_created": 1,
    "completion_time": "ISO_timestamp",
    "context_summary_created": true
  }
}
```

**Session Recovery Capability:**
```
IF session interrupted:
    → Read current state from ./.claude/multi-audit-doc-status/
    → Determine last completed batch
    → Resume from next pending batch
    → Inherit all context summaries from completed work
    → Continue with appropriate phase and agent assignment
```

**Context Accumulation Management:**
```
After each batch completion:
    → Update context_summaries.json with key architectural insights
    → Reference previous summaries in subsequent agent instructions
    → Build progressive understanding across all documentation phases
    → Maintain clear knowledge inheritance patterns
```

**EXECUTION PRINCIPLES:**

**Documentation-First Intelligence:**
- Prioritize systematic questionnaire completion over speed
- Ensure architectural understanding drives all documentation
- Build cumulative knowledge that improves documentation quality
- Maintain professional standards throughout all deliverables

**Context Excellence:**
- Sophisticated context management prevents information loss
- Progressive summarization builds better architectural understanding
- Strategic handoffs ensure knowledge continuity across agents
- Clean integration of all documentation phases

**Robust Progress Tracking:**
- JSON-based fallback system works regardless of MCP availability
- Session recovery enables multi-session documentation projects
- Real-time progress updates provide transparency
- Quality checkpoints ensure compliance throughout

**Architectural Compliance:**
- Built-in audit ensures LOCAL application principles understood
- Privacy-first architecture reflected in all documentation
- Modular patterns properly documented throughout
- Professional deployment-ready documentation quality

**ULTRA-THINKING DIRECTIVE:**

Before execution, deeply analyze:

**Documentation Strategy:**
- How does this specification's questionnaire structure build knowledge?
- What's the optimal balance of sequential foundation vs parallel modules?
- Where are the key architectural insights that need extra attention?
- How can context management ensure documentation quality and consistency?

**Workflow Optimization:**
- What logical module groupings make sense for parallel documentation?
- Which batches have dependencies requiring sequential processing?
- How many agents optimize efficiency while maintaining context quality?
- What progress tracking prevents work loss during multi-session projects?

**Quality Assurance:**
- How do we ensure all questionnaires are fully answered?
- What architectural compliance checks catch misunderstandings early?
- How do we validate documentation completeness and professional quality?
- What context inheritance patterns ensure cumulative knowledge building?

Deploy an intelligent, adaptive documentation workflow that maximizes both systematic coverage and architectural understanding, ensuring professional deliverables with robust progress tracking and sophisticated context management for large-scale documentation projects.

Begin with deep specification analysis, proceed through adaptive workflow design, intelligent execution with context building, comprehensive quality assurance, and integrated architectural compliance validation.