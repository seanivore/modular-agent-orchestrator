# Mao Technical Specifications 

## Critical Rules 

- **Rule #1** 
  * Variable-input philosophy is IMMUTABLE 
  * NEVER add hardcoded categories, templates, enums, or predetermined options
  * But we're not against adding new sets of variables! 
- **Rule #2** 
  * 6-File Tool Architecture is IMMUTABLE. 
  * NEVER merge, combine, or reorganize the 6-file tool pattern 
- **Rule #3** 
  * Human Button Interface is A MUST UNDERSTAND CONCEPT 
  * NEVER convert back to SDK-based approaches or provider-specific implementations
- **Rule #4** 
  * Print statement separation is MANDATORY; only allowed in UI layer files 
  * Core logic must remain print-free; exceptions are 'demos' and 'button' generator files 
- **Rule #5** 
  * File naming standards are PROTECTED; keep them general, not more specific than needed 
  * E.g., why put 'mao' in a file name when all the files in the codebase are 'mao'
  * NO timestamps in file names; this is unnecessary UX
- **Rule #6** 
  * NO automatic backward compatibility; NO legacy aliases, compatibility layers, or "keeping the old name" patterns
  * Product is brand new, no legacy; in the future when it is needed it will be a discussion
- **Rule #7** 
  * HUMAN-FIRST DESIGN of SETUP SCRIPT and JSON CONFIG; they should be able to create and execute without AI assistance 
  * Less use by human users should not result in a more complex design, that is contrary to our mission 
- **Rule #8** 
  * Phases (tasks) start at 1, NEVER 0; NO "Phase 0" or "00_" prefixes in directory structure 
  * Improves UX, eliminates confusion, clear, intuitive; this is a rule of thumb 
- **Rule #9** 
  * NO HARDCODED SUCCESS CRITERIA; we don't pre-define metrics like "covers 5+ competitors" or "includes timeline"
  * Claude is QA, sequential thinking, reviewing deliverables 
- **Rule #10** 
  * Our SETUP SCRIPT means COMMAND REGISTRY is UNNECESSARY; unix filesystem handles command discovery and execution 
  * Setup scripts create executable commands in `/Users/seanivore/bin`; proven pattern 
  * SETUP SCRIPT DOES NOT PUT HYPHENS IN COMMAND LINE, only spaces 
- **Rule #11** 
  * SINGLE RESPONSIBILITY FOR STATE MANAGEMENT; Memory MCP handles ALL workflow state persistence 
  * No duplicate state saving mechanisms or parallel tracking systems; one source of truth for workflow context and progression 
  * Eliminates synchronization issues and redundant operations; clean integration with single, authoritative state management system 
- **Rule #12** 
  * It is 'Mao' not 'MAO'; this encourages proper pronunciation 
  * Don't use m-dashes, use semicolons; if it is a header, it doesn't need to be bold 
  * We don't use emojis in UI; not a huge fan of them in docs but eh 

## Documentation Organization 

### Orchestrator File Roles 

- `__init__.py` = "Modular AI workflow orchestration system"
- `agent_callback.py` = "Handles agent returns, execution results, and workflow progression"
- `agent_orchestrator.py` = "Coordinates agent handoffs with context packages via Files API"
- `cli_manager.py` = "Dynamic CLI command discovery and interface integration connecting CLI/slash commands to orchestrator functionality"
- `conversation_bridge.py` = "Converts natural language goals into executable custom commands"
- `core.py` = "The main brain that turns natural language into intelligent workflows"
- `error_handling.py` = "Professional error handling patterns for all tools"
- `manager_buttons.py` = "Creates executable code snippets for any model/provider combo to avoid SDK hell"
- `manager_models.py` = "Loads JSON configs and provides intelligent model selection"
- `manager_tools.py` = "Dynamic tool suggestion based on goals, not hardcoded categories"
- `mcp_hub.py` = "Integrates Memory MCP, Files API, and MCP Connector into unified system"
- `memory_mcp.py` = "Provides workflow context tracking, state management, and session recovery"
- `real_time_metrics.py` = "Provides live data for UI components; no mock data allowed"
- `settings_manager.py` = "Dynamic settings discovery and management using directory-based scanning of individual setting files"
- `username_manager.py` = "Handles user creation, session persistence, and settings integration"
- `workflow_manager.py` = "Handles workflow ID generation, discovery, and tracking"
- `workflow_state.py` = "Simple state tracking with Memory MCP integration"

### User-Facing Documentation

**Application Usage Guide** 
How to use Mao as an interactive application platform --> [7_MAO_USER_GUIDE.md](./7_MAO_USER_GUIDE.md)

**What This Covers**

- Command reference with terminal and in-app variants
- User experience flows and workflow creation patterns  
- Setup scripts and custom command usage
- Quality framework integration and troubleshooting
- Advanced configuration and Memory MCP integration

**Perfect For**

- Users learning MAO application features
- Command reference and troubleshooting
- Understanding workflow creation and execution
- Setup script and custom command usage

### Technical Documentation

**MAO Overview**
Clean, focused overview --> [1_MAO_OVERVIEW.md](./1_MAO_OVERVIEW.md)

**What This Covers**

- Clear value proposition and problem/solution
- How it actually works with real examples
- User journeys for different audiences
- Performance metrics and success stories
- Getting started guide

**What This Doesn't Try To Be**

- Technical architecture reference
- Extension development guide
- Protection rules documentation

**MAO System File Roles**
How all these files fit together --> [2_MAO_SYSTEM_FILES.md](./2_MAO_SYSTEM_FILES.md)

**What This Covers**

- Overview of system files and their roles
- How they interact with each other
- How they are used to create tools/models/providers
- How they are used to create the orchestrator
- Aka. how everything fits together 

**Perfect For**

- Quick reference to understand the system 
- Understanding the system files and their roles 

**MAO Architecture**
Complete technical deep-dive --> [3_MAO_ARCHITECTURE.md](./3_MAO_ARCHITECTURE.md)

**What This Covers**

- Complete system architecture and integration patterns
- Memory MCP integration and workflow state management
- Tool integration framework and human button system
- Implementation status and roadmap with clear gaps
- Performance characteristics and optimization strategies

**Perfect For**

- Architects and senior developers
- Understanding complex integration patterns
- Implementation planning and dependency analysis
- Performance optimization and troubleshooting

**MAO Extension Guide**
How to add tools/models/providers --> [4_MAO_EXTENSION_GUIDE.md](./4_MAO_EXTENSION_GUIDE.md)

**What This Covers**

- Adding new tools following 6-file pattern
- Model and provider integration
- Variable-input philosophy implementation
- Testing and validation requirements

**Perfect For**

- Developers extending MAO capabilities
- Tool creators and integration partners
- Understanding modular architecture patterns

**MAO Protection Rules**
What never to change and why --> [5_MAO_PROTECTION_RULES.md](./5_MAO_PROTECTION_RULES.md)

**What This Covers**

- Architectural integrity insurance
- Variable-input philosophy protection
- Human button interface requirements
- Performance regression prevention
- File naming and structure standards

**Perfect For**

- All developers working on MAO
- Architectural decision validation
- Code review and quality assurance
- Preventing regression and maintaining innovation 