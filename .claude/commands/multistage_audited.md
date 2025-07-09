**MULTI-STAGE PROJECT EXECUTION WITH INTEGRATED AUDIT COMMAND**

Intelligently orchestrate complex projects through adaptive multi-stage parallel execution with comprehensive QA review and built-in architectural compliance auditing.

**Variables:**

spec_file: $ARGUMENTS

**ARGUMENTS PARSING:**
Parse the following arguments from "$ARGUMENTS":
1. `spec_file` - Path to the markdown specification file defining the project requirements

**PHASE 1: SPECIFICATION ANALYSIS & STRATEGY PLANNING**

Read and deeply analyze the specification file at `spec_file` to understand:
- **Project Scope**: What needs to be created, modified, or fixed
- **File Structure**: Existing files, directories, and relationships
- **Complexity Indicators**: Number of files, types of tasks, dependencies
- **Quality Requirements**: Professional standards, testing needs, deployment targets
- **Success Criteria**: What constitutes completion and quality

**Strategic Analysis Questions:**
- What are the main deliverables and sub-tasks?
- Which tasks can be parallelized for efficiency?
- What dependencies exist between different work streams?
- What quality assurance steps would ensure success?
- How many stages would optimize this workflow?

**PHASE 2: ADAPTIVE WORKFLOW DESIGN**

Based on specification analysis, intelligently determine optimal execution strategy:

**Workflow Complexity Assessment:**
- **Simple Projects**: Single agent execution with basic review
- **Moderate Projects**: 2-3 stage workflow with limited parallelization  
- **Complex Projects**: Multi-stage with extensive parallel execution and comprehensive QA

**Stage Architecture Decision Matrix:**
```
IF (multiple file categories OR distinct task types):
    → Design parallel execution by logical groupings
    
IF (main deliverable + supporting tasks):
    → Primary agent + parallel support agents
    
IF (high quality standards OR deployment critical):
    → Always include comprehensive final QA stage
    
IF (file modifications across categories):
    → Group by category/type for parallel execution
```

**Agent Coordination Strategy:**
- **Task Grouping**: Logical clustering of related work
- **Parallel Optimization**: Maximum efficiency without coordination overhead
- **Dependency Management**: Proper sequencing of dependent tasks
- **Quality Gates**: Strategic review points throughout workflow

**PHASE 3: INTELLIGENT EXECUTION ORCHESTRATION**

Deploy the determined workflow strategy with adaptive agent management:

**Stage 1: Primary Deliverable Creation**
```
IF primary deliverable identified:
    Launch PRIMARY AGENT with:
    - Complete specification context
    - Focus on main deliverable creation
    - Integration requirements with supporting work
    - Quality standards for primary output
```

**Stage 2: Parallel Supporting Work** (If Applicable)
```
IF supporting tasks identified:
    Determine optimal agent distribution:
    - Group related tasks logically
    - Launch 2-6 parallel agents based on scope
    - Assign distinct focus areas to prevent overlap
    - Provide complete context to each agent
    
    Agent Assignment Strategy:
    - Categorize tasks by type/domain/file structure
    - Assign 1 agent per logical category
    - Ensure clear boundaries and deliverables
    - Coordinate timing to prevent conflicts
```

**Stage 3: Comprehensive QA Review with Architectural Audit** (Always Include)
```
Launch REVIEW AGENT with complete context:
- Test all deliverables against specification
- Verify integration between all work streams
- Check professional quality standards
- Validate deployment readiness
- Execute comprehensive architectural compliance audit
- Identify and fix any remaining issues
- Ensure success criteria are met
```

**PHASE 4: ADAPTIVE EXECUTION MANAGEMENT**

**Dynamic Workflow Adaptation:**
- Monitor agent progress and coordination
- Adjust parallel execution if conflicts arise
- Reallocate tasks if agents encounter blockers
- Scale up/down agent count based on complexity discovered
- Ensure clean handoffs between stages

**Quality Assurance Integration:**
- Each stage includes mini-reviews for quality gates
- Final QA stage includes comprehensive testing
- Professional standards maintained throughout
- Deployment readiness verified
- Success criteria validation

**Context Optimization:**
- Efficient context sharing between agents
- Progressive summarization to manage limits
- Strategic coordination to prevent overlap
- Clean state management across stages

**PHASE 5: INTEGRATED ARCHITECTURAL COMPLIANCE AUDIT**

**Built-in Quality Control Framework:**
Execute comprehensive audit as integral part of Stage 3:

**File Standardization Compliance:**
- [ ] All new `.py` files have CacheManager import and usage
- [ ] All new `.py` files have @handle_errors decorators  
- [ ] All new `.py` files have estimate_cost() functions
- [ ] All new `.json` files use 'name' field (not 'id' or 'tool_id')
- [ ] All new `.json` files use flat path structures
- [ ] No emoji icons in any files (text-based visual hierarchy only)

**Architecture Pattern Compliance:**  
- [ ] No hardcoded file lists or mappings (use directory scanning)
- [ ] Modular discovery patterns implemented correctly
- [ ] Memory MCP used for state persistence (not duplicate systems)
- [ ] Real-time data only (no mock data introduced)
- [ ] Privacy-first architecture maintained

**Integration Point Validation:**
- [ ] CLI manager properly routes new commands
- [ ] Settings manager handles new configurations
- [ ] Workflow manager integrates with new features
- [ ] Error handling follows established patterns
- [ ] Cost estimation integrates with real-time metrics

**Privacy Compliance Check:**
- [ ] User data stored in ./configs/user/[username]/ directories
- [ ] System analytics contain no user identifiers
- [ ] Data deletion workflows work correctly
- [ ] Anonymous aggregation properly implemented

**Testing Validation:**
- [ ] New CLI commands execute without errors
- [ ] Configuration files load and save correctly  
- [ ] Integration points don't break existing functionality
- [ ] Error scenarios handled gracefully
- [ ] Performance impact within acceptable limits

**Audit Resolution Process:**
1. **Execute Audit**: Run complete checklist after implementation
2. **Fix Non-Compliance**: Address any architectural violations immediately
3. **Re-Validate**: Test fixes and re-run audit checklist
4. **Document Changes**: Update implementation notes with corrections
5. **Confirm Compliance**: Mark implementation as fully audit-passed

**EXECUTION PRINCIPLES:**

**Intelligent Adaptation:**
- Let specification complexity determine workflow design
- Scale agent deployment based on actual project needs
- Adapt stages dynamically based on discovered requirements
- Balance efficiency with quality throughout

**Quality-First Approach:**
- Always include comprehensive final review with integrated audit
- Build quality gates into multi-stage workflows
- Ensure professional standards across all deliverables
- Validate success criteria achievement

**Architectural Compliance:**
- Enforce MAO development guidelines throughout implementation
- Maintain privacy-first architecture principles
- Ensure modular, discoverable patterns in all code
- Validate real-time data requirements and performance standards

**Coordination Excellence:**
- Prevent agent overlap through clear task boundaries
- Manage dependencies between parallel work streams
- Ensure clean integration of all work products
- Coordinate timing to optimize overall efficiency

**Professional Delivery:**
- Target deployment-ready quality from start
- Include comprehensive testing and validation
- Ensure all deliverables meet professional standards
- Validate complete specification compliance

**ULTRA-THINKING DIRECTIVE:**

Before execution, deeply analyze:

**Project Scope & Strategy:**
- What does this specification truly require?
- What's the optimal balance of stages vs. parallel execution?
- Where are the key quality risks that need extra attention?
- How can we ensure single-shot success with minimal iteration?

**Workflow Design:**
- What logical groupings make sense for parallel work?
- Which tasks have dependencies that require sequencing?
- How many agents would optimize efficiency without chaos?
- What quality gates would catch issues early?

**Architectural Compliance:**
- How do we ensure MAO development guidelines are followed?
- What architectural patterns need special attention?
- How do we maintain privacy-first principles throughout?
- What modular discovery patterns are required?

**Success Optimization:**
- What could go wrong and how do we prevent it?
- How do we ensure all work products integrate cleanly?
- What testing and validation steps ensure deployment readiness?
- How do we balance speed with quality and compliance throughout?

Deploy an intelligent, adaptive workflow that maximizes efficiency, quality, and architectural compliance, ensuring professional deliverables that meet all specification requirements and MAO development standards in a coordinated, well-orchestrated execution.

Begin with deep specification analysis and proceed through adaptive workflow design, intelligent execution, comprehensive quality assurance, and integrated architectural compliance validation.