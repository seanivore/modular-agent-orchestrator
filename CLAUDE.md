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

## Privacy and Analytics

- Maintain privacy-first architecture; user analytics deletable, system analytics anonymous
- User data in ./configs/user/[username]/ - easily deletable for GDPR compliance
- System analytics never contain user identifiers - secondary anonymization required
- All analytics use UserID for tracking, not usernames or personal info

## Performance Guidelines

- Real-time metrics only - no mock data anywhere in Mao ecosystem