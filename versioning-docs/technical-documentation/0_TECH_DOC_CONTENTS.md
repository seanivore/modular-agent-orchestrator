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

## Documentation Contents 

  1. What it is and why it matters; about the magic of Mao --> [1_MAO_OVERVIEW.md](./1_MAO_OVERVIEW.md)
  2. How do all these files fit together; understand it isn't chaos --> [2_MAO_SYSTEM_FILES.md](./2_MAO_SYSTEM_FILES.md)
  3. Complete technical deep-dive; when you need specifics --> [3_MAO_ARCHITECTURE.md](./3_MAO_ARCHITECTURE.md)
  4. How to add tools/models/providers; enjoy being modular --> [4_MAO_EXTENSION_GUIDE.md](./4_MAO_EXTENSION_GUIDE.md) 
  5. What never to change and why; specifications to follow --> [5_MAO_PROTECTION_RULES.md](./5_MAO_PROTECTION_RULES.md)

## 1. Mao Overview 

Clean, focused overview. 

### What This Covers 

  - Clear value proposition and problem/solution
  - How it actually works with real examples
  - User journeys for different audiences
  - Performance metrics and success stories
  - Getting started guide

### What This Doesn't Try To Be 

  - Technical architecture reference
  - Extension development guide
  - Protection rules documentation

## 2. Mao System File Roles 

### What This Covers 

  - Overview of system files and their roles
  - How they interact with each other
  - How they are used to create tools/models/providers
  - How they are used to create the orchestrator
  - Aka. how everything fits together 

### Perfect For 

  - Quick reference to understand the system 
  - Understanding the system files and their roles 

## 3. Mao Architecture 

Complete technical deep-dive to understand how everything connects under the hood. 

### What This Covers 

  - Complete system overview with architectural principles 
  - Every component explained in technical detail (orchestrator, managers, configs, tools)
  - Full integration flow from goal input to result delivery
  - Interface layer and future web capabilities
  - Performance metrics and architectural strengths

### Perfect For 

  - Developers who need to understand how everything connects
  - Technical users extending or integrating with Mao
  - System architects evaluating the design
  - Anyone who needs the deep technical reference

## 4. Mao Extension Guide  

Practical "how to add stuff" guide with complete step-by-step examples. 

### What This Covers 

  - Complete 4-file tool creation process with real code examples
  - Model configuration and integration steps
  - Provider setup and connection testing
  - Advanced patterns for multi-tool coordination
  - Comprehensive testing and validation strategies
  - Best practices and quality assurance guidelines
  - Advanced features like dynamic tool creation

**Zero hype, just clear instructions.** Exactly what developers need to extend Mao capabilities without breaking anything.

## 5. Mao Protection Rules  

The 'what to never change an why' guide, to protect all our architectural decisions. 

### What This Protects 

  - Variable-input philosophy (the core breakthrough)
  - 4-file tool architecture (clean separation)
  - Human button interface (universal compatibility)
  - Print statement rules (UI separation)
  - Naming standards (consistency)

### Plus Practical Enforcement 

  - Common AI mistake patterns with examples
  - Red flag phrases to watch for
  - Validation checklists
  - Step-by-step enforcement strategies
