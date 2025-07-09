# MAO Standardization Rules for Claude Memory
> Key rules to add using Claude Code's # memory feature

## Core Standardization Rules

```
# Always use CacheManager, @handle_errors, and estimate_cost() in MAO files
```

```
# Follow MAO_FILE_STANDARDIZATION_RULES.md - no emoji icons, text-based visual hierarchy
```

```
# Use modular JSON discovery patterns, never hardcode file lists or mappings
```

```  
# Maintain privacy-first architecture - user analytics deletable, system analytics anonymous
```

```
# Follow 4-file tool structure: logic.py, button_*.py, ui_*.py, tool_*.json
```

```
# Use 'name' field in JSON configs, flat path structures, simplified operations
```

```
# CLI commands need 3 files: command.py, ui_command.py, command.json
```

```
# Memory MCP is single source of truth for all workflow state
```

```
# Real-time metrics only - no mock data anywhere in MAO ecosystem
```

```
# Use filesystem tools over artifacts for accuracy in MAO implementations
```

## Privacy & Compliance Rules

```
# User data in ./configs/user/[username]/ - easily deletable for GDPR compliance
```

```
# System analytics never contain user identifiers - secondary anonymization required
```

```
# All analytics use UserID for tracking, not usernames or personal info
```

## Architecture Philosophy Rules

```
# Everything modular, everything discoverable via directory scanning
```

```
# Delta-only storage for settings - only store changes from defaults
```

```
# Conversation-driven interfaces only - no menus, navigation, or complex UI chrome
```