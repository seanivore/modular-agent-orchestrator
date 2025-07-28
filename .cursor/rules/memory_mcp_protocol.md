# Memory MCP Usage Protocol

## Core Principles
- **Always announce new entities** - Notify Sean whenever creating new Memory MCP entities
- **Entity specificity required** - Create focused entities for distinct issues/sessions rather than generic ones
- **Track all entities** - Maintain a record of created entities for easy discovery

## Entity Creation Protocol
1. **Always announce**: "🔔 New Entity Created: `entity-name` (entity-type)"
2. **Be specific**: Create targeted entities for distinct problems/sessions
3. **Avoid generic**: Don't use broad entity names like "project" or "task"
4. **Record location**: Always add new entities to the entity tracking list

## Entity Naming Convention
- Use kebab-case: `python-syntax-validation-fixes`
- Include context: `troubleshooting-session`, `implementation-plan`, `bug-report`
- Be descriptive: Entity name should indicate the specific scope

## Entity Tracking Location
**All new entities should be recorded in:** `memory-entity-registry` entity
- Purpose: Central registry of all created entities for easy discovery
- Update whenever creating new entities
- Include: entity name, type, creation context, and brief description

## Memory Visibility
- Sean cannot see Memory MCP contents directly
- I am the exclusive maintainer of the memory system
- Memory serves as cross-session continuity for long-term projects 