# Development Tools Reference

## Centralized Scripts Location

Development tools that are useful across multiple projects have been moved to:
**`~/Development/scripts/`**

## Available Tools

### clearpy - Cache Cleaner
- **Location**: `~/Development/scripts/cache_cleaner/`
- **Installation**: `cd ~/Development/scripts/cache_cleaner && ./install_clearpy_command.sh`
- **Usage**: `clearpy [directory] [-v|-n|-h]`
- **Purpose**: Removes `__pycache__`, `.DS_Store`, and other temp files

### ptree - Enhanced Project Tree
- **Location**: `~/Development/scripts/project_tree/`
- **Installation**: `cd ~/Development/scripts/project_tree && ./install_ptree_command.sh`
- **Usage**: `ptree [-a|-s|-h]`
- **Purpose**: Enhanced project structure viewer with hidden file control

## Why Centralized?

- **Reusable**: Available across all projects
- **Maintainable**: Single source of truth for updates
- **Organized**: Categorized by function
- **Discoverable**: All tools documented in one place

## Adding New Tools

When creating new development tools, prefer adding them to `~/Development/scripts/` rather than project-specific locations, unless the tool is truly project-specific.

See `~/Development/scripts/README.md` for full documentation. 