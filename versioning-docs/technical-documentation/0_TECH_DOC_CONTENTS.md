# Mao Technical Specifications 

## Critical Rules 

- **Rule #1** 
  * Variable-Input Philosophy is IMMUTABLE.
  * NEVER add hardcoded categories, templates, enums, or predetermined options
  * When in doubt, ask Sean; his brain is basically modular 
  * We've more than once decided to add a whole new set of JSON variable configurations 
- **Rule #2** 
  * 6-File Tool Architecture is IMMUTABLE. 
  * NEVER merge, combine, or reorganize the 6-file tool pattern 
  * You will need to audit any new files before implementation 
  * We've yet to see a new file that didn't need a heavy audit 
- **Rule #3** 
  * Human Button Interface is A MUST UNDERSTAND CONCEPT.
  * NEVER convert back to SDK-based approaches or provider-specific implementations
- **Rule #4** 
  * Print Statement Separation is MANDATORY
  * Print statements are ONLY allowed in UI layer files 
  * Core logic must remain print-free 
  * Only exception is 'demos' and 'button generator' files 
- **Rule #5** 
  * File Naming Standards are PROTECTED
  * Current standardized names cannot be changed for "clarity" or "consistency"
- **Rule #6** 
  * No Automatic Backward Compatibility
  * NEVER add legacy aliases, compatibility layers, or "keeping the old name" patterns
  * This is a completely new tool - there's no legacy to maintain
  * When backward compatibility becomes needed in the future, it must be:
    - Explicitly discussed with Sean first
    - Properly planned and architected
- **Rule #7** 
  * HUMAN-FIRST SETUP SCRIPT AND JSON CONFIG DESIGN
  * Setup scripts and JSON configs must be designed for human creation and execution first
  * Humans should be able to create, understand, and modify all configuration without AI assistance
  * Simple stays simple - no complexity just because Claude can handle it
  * Tool ensures human agency and understanding of their own workflows
  * Example: SFA pattern of `sfa workflow-name path/to/config.json` in terminal
- **Rule #8** 
  * NO TIMESTAMPS IN FILENAMES
  * Workspace directories use clean command-based naming: `marketing-strategy-startup/`
  * Never append timestamps like `marketing-strategy-startup_20250619_1430/`
  * If users need timestamps, Finder/filesystem provides them 
  * Keep filenames clean and focused on content, not creation time
  * Directory grouping by command name, not temporal organization
- **Rule #9** 
  * PHASES START AT 1, NEVER 0
  * All workflow phases numbered starting from 1
  * No "Phase 0" or "00_" prefixes in directory structure  
  * Improves UX and eliminates confusion from SFA legacy patterns
  * Clear, intuitive numbering that matches human expectations
- **Rule #10** 
  * NO HARDCODED SUCCESS CRITERIA
  * Never define specific quality metrics like "covers 5+ competitors" or "includes timeline"
  * Claude reviews deliverables using sequential thinking and context
  * Quality assurance through AI reasoning, not predetermined checklists
  * Maintains variable-input philosophy at quality validation level
  * Success criteria defined by user goals, not system assumptions
- **Rule #11** 
  * COMMAND REGISTRY SYSTEMS ARE UNNECESSARY
  * No command registry databases or tracking systems needed
  * Setup scripts create executable commands in `/usr/local/bin/` following Unix patterns
  * Unix filesystem handles command discovery and execution
  * Proven SFA pattern: setup script → executable command → direct execution
  * Avoid unnecessary complexity layers over working solutions
- **Rule #12** 
  * SINGLE RESPONSIBILITY FOR STATE MANAGEMENT
  * Memory MCP handles ALL workflow state persistence
  * No duplicate state saving mechanisms or parallel tracking systems  
  * One source of truth for workflow context and progression
  * Eliminates synchronization issues and redundant operations
  * Clean integration with single, authoritative state management system

## Documentation Organization 

### **📚 User-Facing Documentation**

**7. Application Usage Guide** 
How to use MAO as an interactive application platform --> [7_MAO_USER_GUIDE.md](./7_MAO_USER_GUIDE.md)

**What This Covers:**
- Command reference with terminal and in-app variants
- User experience flows and workflow creation patterns  
- Setup scripts and custom command usage
- Quality framework integration and troubleshooting
- Advanced configuration and Memory MCP integration

**Perfect For:**
- Users learning MAO application features
- Command reference and troubleshooting
- Understanding workflow creation and execution
- Setup script and custom command usage

### **🔧 Technical Documentation**

**1. MAO Overview**
Clean, focused overview --> [1_MAO_OVERVIEW.md](./1_MAO_OVERVIEW.md)

**What This Covers:**
- Clear value proposition and problem/solution
- How it actually works with real examples
- User journeys for different audiences
- Performance metrics and success stories
- Getting started guide

**What This Doesn't Try To Be:**
- Technical architecture reference
- Extension development guide
- Protection rules documentation

**2. MAO System File Roles**
How all these files fit together --> [2_MAO_SYSTEM_FILES.md](./2_MAO_SYSTEM_FILES.md)

**What This Covers:**
- Overview of system files and their roles
- How they interact with each other
- How they are used to create tools/models/providers
- How they are used to create the orchestrator
- Aka. how everything fits together 

**Perfect For:**
- Quick reference to understand the system 
- Understanding the system files and their roles 

**3. MAO Architecture**
Complete technical deep-dive --> [3_MAO_ARCHITECTURE.md](./3_MAO_ARCHITECTURE.md)

**What This Covers:**
- Complete system architecture and integration patterns
- Memory MCP integration and workflow state management
- Tool integration framework and human button system
- Implementation status and roadmap with clear gaps
- Performance characteristics and optimization strategies

**Perfect For:**
- Architects and senior developers
- Understanding complex integration patterns
- Implementation planning and dependency analysis
- Performance optimization and troubleshooting

**4. MAO Extension Guide**
How to add tools/models/providers --> [4_MAO_EXTENSION_GUIDE.md](./4_MAO_EXTENSION_GUIDE.md)

**What This Covers:**
- Adding new tools following 6-file pattern
- Model and provider integration
- Variable-input philosophy implementation
- Testing and validation requirements

**Perfect For:**
- Developers extending MAO capabilities
- Tool creators and integration partners
- Understanding modular architecture patterns

**5. MAO Protection Rules**
What never to change and why --> [5_MAO_PROTECTION_RULES.md](./5_MAO_PROTECTION_RULES.md)

**What This Covers:**
- Architectural integrity insurance
- Variable-input philosophy protection
- Human button interface requirements
- Performance regression prevention
- File naming and structure standards

**Perfect For:**
- All developers working on MAO
- Architectural decision validation
- Code review and quality assurance
- Preventing regression and maintaining innovation

### **🧪 Post-Implementation Documentation**

**8. Tests & Validations Guide**
Comprehensive testing, benchmarking & operational validation --> [8_MAO_TESTS_VALIDATIONS.md](./8_MAO_TESTS_VALIDATIONS.md)

**What This Will Cover** *(Post-Implementation)*:
- Real-world performance benchmarking with actual data
- End-to-end integration examples from completed workflows
- Operational error patterns discovered during testing
- Quality validation methodologies and success criteria
- User experience testing results and optimization strategies
- Continuous improvement framework with monitoring metrics

**Perfect For** *(After Implementation)*:
- QA teams validating system performance
- Operations teams troubleshooting and optimizing
- Developers understanding real integration patterns
- Users learning from actual operational experiences
- Stakeholders evaluating system effectiveness and ROI