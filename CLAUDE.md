# Mao Standardization Rules
*Critical standardization rules for context priming to review before each session* 

---

Find: Core principles, production and development guidelines, CRITICAL implementation rules, copywriting MUST FOLLOW guide, technical architecture and development guidelines. 

---

## Core Principles
**All JSON config files must be standalone, atomic units**
- Easy to add/remove/update individual components
- Directory scanning for live discovery
- No hardcoded lists, categories, enums, predetermined options
- Template-based consistency
- Mao is a single-screen, chat-based UI app; no menus, navigation, or complex UI chrome
- No emoji icons; use text-based visual hierarchy; conceptual semantic highlighting 
- We have only 4 colors, character choice, and whitespace to work with 
- NO BACKWARDS COMPATIBILITY, LEGACY ALIASES, OR COMPATIBILITY LAYERS
- Memory MCP is single source of truth AND ONLY STATE MANAGEMENT SYSTEM 
- Setup scripts create executable commands in `/Users/seanivore/bin`; proven pattern 
- Setup scripts do not put hyphens in command line, only spaces 

## Development Guidelines 
- Always use CacheManager, @handle_errors, and estimate_cost() in MAO files
- Follow FILE_STANDARDIZATION_RULES.md - no emoji icons, text-based visual hierarchy
- Use modular JSON discovery patterns, never hardcode file lists or mappings
- Follow 4-file tool structure: logic.py, button_*.py, ui_*.py, tool_*.json
- Use 'name' field in JSON configs, flat path structures, simplified operations
- CLI commands need 3 files: command.py, ui_command.py, command.json
- Memory MCP is single source of truth for all workflow state
- Use filesystem tools over artifacts for accuracy in Mao implementations
- Everything modular, everything discoverable via directory scanning
- Delta-only storage for settings - only store changes from defaults
- Conversation-driven interfaces only - no menus, navigation, or complex UI chrome

## UI Development Guidelines
**Previously contained planning for a public terminal app; needs new bullet points**

---

## Critical Implementation Rules 
- Abbreviate implementation in file name to **IMPL**
- Create directory in versioning folder; use naming structure: `IMPL_[UPDATE_NAME]`
- Directory may hold any prep. files, but final is named `IMPL_[UPDATE_NAME].md`
- Implementation document MUST BE MORE THOROUGH THAN TECHNICAL DOCUMENTATION 
- We will be keeping internal documentation more robust than public documentation 
- The update will NOT move forward until the implementation document is complete 
- Include ALL necessary logic, explained verbally; directory and files to create 
- Config files must have a JSON schema, template, and guide for creating, for example, a new tool 

### Development Workspace 
- Token conscious work: Use filesystem for persistent reference  
- Artifacts use fewer tokens than write_file 
- Full codebase in Project Knowledge; retrieval is not persistent reference 
- ALWAYS use sequential thinking before, during, and in review of tasks 
- Update Memory MCP with Project State before task, during, and after 

### Copywriting Styles Guide 
**PRACTICE AT ALL TIMES; FOR OURSELVES, IN APP, MARKETING** 
  1. Never use "MAO" in caps; it is a proper noun; their NAME is Mao
  2. Never use an m-dash or regular dash - in the middle of a sentence; use semicolon  
  3. Do not put markdown heading in bold or italics; use for variant emphasis 
  4. We only use military time; do not write AM or PM; eastern timezone 
  5. Write long date in EU format: 21 July 2025; short date: YYYY-MM-DD  

---

## Documentation Writing Principles

### Writing Style (Following Anthropic Docs Approach)
- **Narrative prose over bullet points** as primary structure
- **Brief paragraphs** for accessibility and readability
- **Natural weaving** of technical architecture within narrative story
- **NO separate technical sections** - integrate code explanations throughout
- **Pattern:** Brief text → code architecture → more text → code architecture
- **Audience:** Accessible to both technical and marketing/pitch audiences

### Documentation Rules
- **Never delete existing writing** - suggest edits only
- **Use semicolons instead of m-dashes** in narrative flow
- **No emoji icons** - text-based visual hierarchy only
- **No bullet points as primary narrative device** - prose first
- **Brief paragraphs** with comprehensive coverage

---

**Remember: Prevention over correction. Follow these patterns from the start rather than fixing violations later.**

---


# 🚨 WHY HARDCODED WORKFLOW CATEGORIES ARE TOXIC

## The Fundamental Problem

**Hardcoded English workflow assumptions destroy the core value proposition of Mao as a truly modular, multilingual AI orchestrator.**

The *ONLY* reason to add categories like this is tagging for *ANALYTICS* where translation will not break the logic of the code. 

## Examples of Toxic Code Found:

### 1. Agent Callback Hardcoded Recommendations (Lines 252-259)
```python
# Tool-specific recommendations
tool_name = execution_results.get('tool_name', '')
if 'research' in tool_name.lower():
    recommendations.append("Proceed to analysis phase")
elif 'analysis' in tool_name.lower():
    recommendations.append("Proceed to creative / implementation phase")
elif 'creative' in tool_name.lower():
    recommendations.append("Review and finalize deliverables")
```

### 2. Core Orchestrator Workflow Patterns (Lines 180-220)
```python
# Research-driven workflows
if "research" in task_types:
    phases.append(WorkflowPhase(name="research_phase", ...))

# Analysis/reasoning phase  
if "reasoning" in task_types:
    phases.append(WorkflowPhase(name="analysis_phase", ...))

# Creative/implementation phase
if "creative" in task_types:
    phases.append(WorkflowPhase(name="creative_phase", ...))
```

### 3. Hardcoded Agent Roles by Domain
```python
roles = {
    "research": {
        "business": "Business intelligence analyst...",
        "creative": "Creative industry research expert...",
    },
    "creative": {
        "business": "Marketing strategist...",
        "technology": "Technical writer...",
    }
}
```

## Why This Is Catastrophically Harmful

### 1. **Multilingual Destruction**
- **English Workflow Bias:** Assumes all users think in "research → analysis → creative" patterns
- **Cultural Imperialism:** Forces Western linear thinking patterns on all cultures
- **Translation Failure:** Categories like "creative/implementation phase" are meaningless in many languages
- **Lost Nuance:** Different cultures have different problem-solving approaches that get forced into English boxes

### 2. **Modularity Violation** 
- **Defeats Core Value:** Mao's strength is being truly modular and adaptive
- **Tool Limitation:** Tools get artificially categorized instead of being discovered dynamically
- **Innovation Blocking:** New workflow patterns can't emerge because they're locked into predefined categories
- **User Limitation:** Users can't create workflows that don't fit English business paradigms

### 3. **AI Intelligence Reduction**
- **Claude Doesn't Need This:** Claude Sonnet 4 is perfectly capable of ideation and workflow design
- **Constrains Creativity:** Hardcoded recommendations limit what the AI can suggest
- **Reduces Adaptability:** System becomes rigid instead of intelligent and responsive
- **Wastes AI Capability:** We're paying for advanced AI but then constraining it with hardcoded logic

### 4. **Scale and Maintenance Issues**
- **Translation Nightmare:** Every hardcoded string needs translation and cultural adaptation
- **Business Logic Debt:** Changes require touching multiple files instead of being data-driven
- **Testing Complexity:** Every hardcoded path needs separate test coverage
- **Bug Multiplication:** Hardcoded assumptions create edge cases and failures

## Real-World Impact Examples

### Spanish User Scenario:
- User says: "Necesito investigar el mercado para mi startup"
- System detects "research" and forces English "research → analysis → creative" workflow
- User actually wanted: "investigación → validación → implementación" (different cultural approach)
- Result: Workflow doesn't match user's mental model, delivers suboptimal results

### Japanese User Scenario:
- User describes iterative improvement process (Kaizen approach)
- System forces linear Western workflow pattern
- Japanese iterative refinement approach gets lost
- Cultural work methodology is not supported

### Technical User Scenario:
- Developer wants: "prototype → test → iterate → deploy"
- System forces: "research → analysis → creative" 
- Doesn't match technical workflow patterns
- User has to fight the system instead of being helped by it

## The Correct Approach

### 1. **Pure Tool Discovery**
- Let tools be discovered based on actual goal analysis
- Use tool capabilities and descriptions, not hardcoded categories
- Allow Claude to determine optimal workflow patterns

### 2. **Dynamic Workflow Generation**  
- Analyze user goal in their language and cultural context
- Generate workflow phases based on actual requirements
- Use Claude's intelligence to determine phase progression

### 3. **Cultural Adaptation**
- Support different cultural problem-solving approaches
- Allow workflow patterns to emerge from user behavior
- Don't force Western business paradigms on all users

### 4. **True Modularity**
- Tools describe their capabilities, not their workflow position
- Phases determined by goal requirements, not predefined categories
- System adapts to user needs instead of forcing user into system constraints

## Immediate Actions Required

### 1. **Delete Hardcoded Categories**
- Remove all "research", "analysis", "creative" hardcoded logic
- Delete predefined workflow patterns
- Remove English-assumption recommendations

### 2. **Implement Dynamic Discovery**
- Use tool descriptions and capabilities
- Let Claude determine optimal workflows
- Support emergent workflow patterns

### 3. **Cultural Testing**
- Test with non-English goals
- Validate with users from different cultural backgrounds  
- Ensure workflows adapt to different thinking patterns

### 4. **Documentation Update**
- Remove hardcoded workflow examples from docs
- Emphasize true modularity and adaptability
- Show examples of diverse workflow patterns

## Conclusion

**Hardcoded workflow categories are not just bad code - they're cultural imperialism disguised as features.** They destroy the fundamental value proposition of Mao as a truly intelligent, adaptive, multilingual AI orchestrator.

The solution is to trust Claude's intelligence, embrace true modularity, and let workflows emerge from actual user needs rather than predetermined English business categories.

**This is exactly the kind of poison that makes AI tools fail globally while succeeding only for English-speaking Western business users.**