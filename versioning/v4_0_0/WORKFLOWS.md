# Modern AI Workflow Patterns

Advanced AI systems use five core workflow patterns for complex task coordination. Mao implements all of these patterns dynamically, choosing the optimal approach based on your specific goals.

## The Five Workflow Patterns

### **Prompt Chaining**
Sequential workflow steps where each phase builds on the previous output.

*Examples:*
- Generate marketing copy, then translate it into different languages
- Write document outline, validate against criteria, then write full document
- Research phase → Analysis phase → Final report creation

### **Routing**  
Intelligent direction of different request types to specialized processes.

*Examples:*
- Customer service queries routed to appropriate response workflows
- Simple questions sent to faster models, complex ones to more capable models
- Content type detection routing to specialized processing agents

### **Parallelization**
Multiple agents working simultaneously on different aspects of the same goal.

*Sectioning approach:*
- Content creation while guardrails screening runs in parallel
- Multiple evaluation agents assessing different performance aspects
- Research agents gathering information from different sources simultaneously

*Voting approach:*
- Multiple agents reviewing code for vulnerabilities with consensus requirement
- Content appropriateness evaluation with different vote thresholds
- Quality assessment requiring majority agreement

### **Orchestrator-Workers**
Central coordination agent managing specialized worker agents.

*Examples:*
- Complex coding projects modifying multiple files with specialized agents per file type
- Research projects gathering and analyzing information from multiple sources
- Creative projects coordinating writers, editors, and reviewers

### **Evaluator-Optimizer**
Iterative improvement cycles with evaluation and refinement phases.

*Examples:*
- Literary translation with critique and revision cycles
- Complex search tasks requiring multiple rounds of analysis
- Creative work with feedback loops and iterative enhancement

## Mao's Dynamic Implementation

**Mao is fundamentally an Orchestrator-Workers system** that dynamically implements the other four patterns as needed:

- **Always uses Routing** - Determines optimal models, tools, and approaches for each phase
- **Integrates Prompt Chaining** - Builds sequential phases where outputs feed forward
- **Leverages Parallelization** - Runs multiple agents simultaneously when beneficial
- **Implements Evaluator-Optimizer** - Often leaves final phases open-ended for assessment and iteration

**The key innovation:** Mao doesn't force you to choose a workflow type. Instead, Mao analyzes your goal and dynamically constructs the optimal combination of these patterns to achieve your specific objectives.

## Open-Ended Workflow Philosophy

Unlike static automation tools, Mao frequently creates **intentionally incomplete workflows**. When working on creative or complex projects, Mao will:

1. Plan the initial phases with clear objectives
2. Execute those phases using appropriate agents
3. **Stop and assess the actual results** before planning next steps
4. Dynamically create additional phases based on what was actually produced

This approach mirrors how humans naturally work - you don't plan every detail in advance, you adapt based on what you discover along the way.

**Example:** A short story writing project might initially plan for "research → outline → first draft." But after seeing the first draft, Mao might dynamically add "character development enhancement → dialogue polish → illustration planning" based on the story's actual strengths and needs.

This evaluator-optimizer approach ensures your final deliverables exceed what any pre-planned workflow could achieve.