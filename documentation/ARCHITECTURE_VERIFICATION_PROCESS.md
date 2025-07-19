# Architecture Documentation Verification Process

## Purpose
Systematically verify every code example, class name, function signature, and import statement in the 6 architecture documents against the actual Mao v4 codebase to ensure 100% accuracy.

## Critical Issues Identified
- **Error Classes**: ARCH_01 documents non-existent error classes (MAOError, ToolExecutionError, ConfigurationError)
- **Real Error Hierarchy**: OrchestrationError, ValidationError, ProcessingError, ResourceError, APIError
- **Risk**: Inaccurate documentation creates "Google help center spinning in circles" experience

## Verification Methodology

### 1. MANDATORY: Read Before Writing Rule
**CRITICAL**: Before documenting ANY code element, the agent MUST:
- Read the actual file using the Read tool
- Copy the exact code snippet from the file
- Verify class names, function signatures, and variable names match exactly
- **NEVER write code from memory or training patterns**

### 2. Code Example Extraction & Immediate Verification
For each architecture document (ARCH_01 through ARCH_06):
- Extract every code snippet, class name, function signature
- **IMMEDIATELY read the claimed source file to verify accuracy**
- Note the actual file path and line numbers where code exists
- List all import statements and verify they exist in the actual files

### 3. Systematic File Reading Protocol
For each extracted code element:
- **File Verification**: Read actual file at documented path using Read tool
- **Exact Match Verification**: Code snippet must match file contents exactly
- **Context Verification**: Verify surrounding code context is accurate
- **Import Verification**: Read import statements from actual files
- **NO INVENTION RULE**: If code doesn't exist, mark as "TO BE IMPLEMENTED"

### 4. Code Snippet Verification Script Integration
Create verification process that:
- Greps codebase for exact code snippets
- Flags any code that doesn't exist in actual files
- Provides "ACTUAL CODE FOUND AT:" corrections
- Reports "CODE NOT FOUND - MARK AS PROPOSED" for non-existent patterns

### 3. Systematic File Review
Key files to verify against:
- `orchestrator/error_handling.py` - Error hierarchy
- `mao_v4.py` - Main application entry
- `orchestrator/orchestrator_core.py` - Core orchestration patterns
- `orchestrator/cache_system.py` - Caching implementation
- `managers/` directory - All manager implementations
- `tools/` directory - Tool integration patterns
- `interfaces/ui_terminal.py` - UI integration
- `cli_commands/` directory - CLI command patterns
- Configuration files in `configs/` directories

### 4. Node.js Integration Accuracy
- Verify subprocess communication patterns
- Ensure examples are modular and extensible
- Check against any existing TypeScript/Node.js code
- Validate command execution interfaces

### 5. Documentation Standards
- Maintain 60-80% written content, 20-40% code ratio
- Ensure entry-level accessibility
- Keep LOCAL-first architecture emphasis
- Professional technical writing standards

## Verification Checklist Template

### ARCH_01: Architecture Overview
- [ ] Error handling code examples (CRITICAL FIX NEEDED)
- [ ] Bootstrap sequence code snippets
- [ ] Subprocess communication examples
- [ ] File system organization claims

### ARCH_02: Core System Patterns  
- [ ] Orchestrator class implementations
- [ ] State management code examples
- [ ] Caching system snippets
- [ ] Manager integration patterns

### ARCH_03: Tool Integration Patterns
- [ ] Tool discovery mechanisms
- [ ] 4-file tool structure examples
- [ ] Button generation code
- [ ] Performance monitoring snippets

### ARCH_04: Configuration Data Patterns
- [ ] Delta-only storage implementation
- [ ] Settings manager examples
- [ ] Privacy compliance code
- [ ] Schema validation snippets

### ARCH_05: User Interface Patterns
- [ ] Terminal UI implementation
- [ ] Node.js ↔ Python communication
- [ ] CLI command patterns
- [ ] Rich terminal formatting

### ARCH_06: Extension Automation Patterns
- [ ] Template system implementation
- [ ] Script automation examples
- [ ] Workflow generation code
- [ ] Installation script patterns

## Quality Assurance Process

1. **Systematic Review**: Check each document section by section
2. **Cross-Reference Validation**: Verify against actual file contents
3. **Integration Testing**: Ensure examples work in context
4. **Update Documentation**: Fix all identified inaccuracies
5. **Final Audit**: Comprehensive review of corrected documentation

## Success Criteria
- **100% Accuracy**: Every code example exists and works as documented
- **Real Implementation**: No invented or theoretical code patterns
- **Practical Usage**: Examples reflect actual system implementation
- **Developer Ready**: Documentation enables real extension work

## Tools and Resources
- Direct file reading for verification
- Sequential Thinking MCP for systematic review
- Git history for understanding implementation evolution
- Actual codebase as single source of truth