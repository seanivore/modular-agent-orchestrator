# CLI Manager Logic Audit Analysis

## What MAO_FLOW.md Says This Functionality Should Do

According to MAO_FLOW.md, CLI command management should:

1. **Dynamic Discovery**: Scan directories for CLI command JSON configurations without hardcoded lists
2. **True Modularity**: Support plug-and-play CLI commands that are self-contained
3. **No Hardcoded Categories**: Avoid predetermined English-language command categories or workflow assumptions
4. **Trust AI Intelligence**: Let Claude handle command execution without hardcoded suggestions or examples
5. **Multilingual Ready**: Support different cultural approaches to command naming and workflow patterns
6. **3-File Structure**: Each CLI command consists of command.py, ui_command.py, and command.json files
7. **Simple Logic**: Clean interface that discovers and executes without over-engineering

## What the Current Code Actually Does

The current cli_manager.py file contains **major violations** of MAO principles:

### Critical Violations Identified

1. **Massive Hardcoded Method Mapping (Lines 182-242)**
   - 200+ lines of hardcoded English command categories
   - Predetermined workflow assumptions like "login", "logout", "workflows"
   - Violates core MAO principle: "No hardcoded lists, categories, enums, predetermined options"
   - This is exactly the "toxic hardcoded workflow categories" warned against in CLAUDE.md

2. **Path Syntax Errors (Lines 32, 84, 905, 919, 926, 939)**
   - Incorrect path syntax: "configs / cli" instead of "configs/cli"
   - Will cause file system errors during execution
   - Shows lack of testing and quality control

3. **Over-Engineering and Complexity**
   - File is 966 lines long but could be <300 lines with proper design
   - Contains numerous placeholder methods returning "Implementation pending"
   - Duplicate method definitions (e.g., `_execute_verbose_command` appears twice)
   - Violates MAO principle: "Think hard, choose simple"

4. **Cultural Imperialism in Code**
   - Hardcoded English command assumptions destroy multilingual capability
   - Forces Western linear thinking patterns on all users
   - Creates predetermined workflow categories that limit user creativity
   - Violates MAO's core value proposition as a truly adaptive, multilingual orchestrator

5. **Missing MAO Standardization**
   - Doesn't follow standard MAO import patterns from CLAUDE.md
   - Missing proper error handling decorators
   - Improper caching implementation with hardcoded command categories
   - No standalone functions for button imports

### Specific Code Issues

- **Lines 182-242**: Toxic hardcoded method mappings that destroy modularity
- **Lines 32, 84, etc.**: Path syntax errors will cause runtime failures  
- **Lines 644-676**: Duplicate `_execute_verbose_command` method definition
- **Lines 363-461**: Multiple placeholder methods that add no value
- **Lines 831-875**: Hardcoded cacheable command categories

## AI Behavioral Guidance and Validation Methods Needed

### AI Protocol for CLI Command Handling
- **Trust AI Intelligence**: Claude Sonnet 4 can dynamically determine optimal command execution patterns
- **No Predetermined Categories**: Allow command structures to emerge from actual user needs
- **Cultural Adaptation**: Support different cultural approaches to command organization
- **Dynamic Discovery**: Scan JSON configurations and execute corresponding Python logic files

### Validation Methods (Without Examples or Suggestions)
- **JSON Schema Validation**: Ensure command configurations follow proper structure
- **File Path Validation**: Verify command Python files exist before attempting execution
- **Error Handling**: Gracefully handle missing or malformed command configurations
- **Security Validation**: Prevent execution of commands outside allowed directories

### Behavioral Guidelines for AI
- **Read Command Intent**: Understand what user wants to accomplish, not just command syntax
- **Adaptive Execution**: Adjust command behavior based on user context and preferences
- **Error Communication**: Provide helpful error messages without predetermined suggestions
- **Continuous Learning**: Use command usage patterns to improve discovery and execution

## The Correct Simple Logic That Should Be Implemented

### Clean Architecture Design
1. **Discovery Phase**: Scan `configs/cli/` directory for JSON command configurations
2. **Validation Phase**: Verify command structure and required file paths exist
3. **Execution Phase**: Dynamically import and execute command logic from Python files
4. **Response Phase**: Return execution results with proper error handling

### Implementation Principles
- **Single Responsibility**: CLI manager only discovers and routes commands
- **Dynamic Loading**: Use importlib to load command logic from JSON-specified paths
- **No Hardcoded Mappings**: Each command is self-contained and defines its own behavior
- **Proper Error Handling**: Use MAO standard error handling patterns
- **Efficient Caching**: Cache discovery results, not predetermined command categories

### File Structure Integration
- **Command Discovery**: Read JSON configs to find command.py and ui_command.py paths
- **Dynamic Import**: Load and execute command logic without hardcoded references
- **UI Integration**: Support both terminal flags and in-app slash commands
- **Cost Estimation**: Dynamically read cost estimates from command JSON configurations

## Missing or To-Be-Implemented Functionality

### Required Updates for Full Implementation
1. **Path Syntax Fixes**: Correct all file path strings to use proper syntax
2. **Method Mapping Removal**: Delete entire hardcoded mapping dictionary
3. **Dynamic Command Loading**: Implement importlib-based command execution
4. **Standard MAO Patterns**: Add proper imports, error handling, caching
5. **Standalone Functions**: Add button import functions per MAO standards
6. **JSON Schema Validation**: Ensure command configurations are properly structured

### Additional CLI Functionality Needed
- **Command Autocomplete**: Dynamic suggestion based on discovered commands
- **Help System**: Generate help from JSON configurations, not hardcoded text
- **Permission Handling**: Support user-specific command access controls
- **Session Context**: Pass user session context to command execution
- **Performance Metrics**: Track command usage for analytics without predetermined categories

## Recommendation

**Complete Refactor Required**: The current implementation violates fundamental MAO principles and should be rewritten from scratch following the clean architecture design outlined above. The hardcoded method mappings represent exactly the kind of "cultural imperialism disguised as features" that CLAUDE.md explicitly warns against.