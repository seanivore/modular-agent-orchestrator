# Single-File Agent Technical Documentation

This document serves as both a table of contents for technical documentation and contains the agent update protocol. The technical documentation provides implementation details and explains how the Single-File Agent system works.

## Agent Update Protocol

The following protocol should be followed when updating the agent to ensure proper versioning and documentation.

### 1. Identify Update Type

First, determine the type of update:

- **Major update**: Notable functional changes, refactoring, or behavior changes
- **Minor update**: Performance improvements, small tooling additions that don't change core behavior
- **Patch update**: Bug fixes without changing the agent's core behavior

Version numbers follow semantic versioning: v[MAJOR].[MINOR].[PATCH]

### 2. Create Version Directory

1. Create the appropriate new versioning sub-directory for the new version
   - For patch/minor: Create folder in current major version (e.g., `./versioning/v3-WORKFLOW-TOOLING/v3_2_3/`)
   - For major: Create new major directory (e.g., `./versioning/v4-[FEATURE_NAME]/v4_0_0/`)

### 3. Copy and Rename Agent File

1. Copy the existing agent file (leave in the project root)
2. Rename it with the new version number (e.g., `sfa_v3_2_3_main.py`)
3. If making major changes, consider creating a backup of the original file

### 4. Document Changes

Create appropriate documentation files in the version directory following these naming conventions:

- `v[X_Y_Z]_ERRORS.md` - For error reports and bugs to be fixed
- `v[X_Y_Z]_PATCH.md` - "We just did xyz" bullet lists after changes
- `v[X_Y_Z]_[FEATURE_NAME].md` - For feature updates (e.g., IMAGE_EDITOR)
- `v[X_Y_Z]_UPDATE.md` - For major updates with evolving content

Include:
- Start date
- Subsequent session dates
- Completion date
- Details of changes made
- Testing results

### 5. Make Code Changes

1. Make necessary modifications to the agent file
2. Update version number and comments within the code
3. Document changes as you go in the version documentation file

### 6. Testing

1. Perform thorough testing appropriate to the update
2. For major changes, test all core functionality
3. For minor changes, test affected components
4. For patches, verify the bug is fixed
5. Store test files in the `tests` directory (organize in version folders after completion)
6. Document test paths and results in the patch document

### 7. Update CHANGE_LOG.md

Add a new entry at the top of CHANGE_LOG.md:

```markdown
## v[X_Y_Z] - YYYY-MM-DD

### Added
- New feature or capability
- Another addition

### Changed
- Modified behavior or implementation
- Another change

### Fixed
- Bug that was addressed
- Another fix

### Documentation
- Documentation updates
```

### 8. Update Documentation

Update the following documentation as needed:

1. README.md - For user-facing changes
2. SPECIFICATIONS.md - For changes to what the system should do
3. Technical documentation files for implementation details:
   - CORE_ARCHITECTURE.md - For changes to architecture
   - TOOLS_AND_CAPABILITIES.md - For tool changes
   - PERFORMANCE_OPTIMIZATION.md - For performance changes
   - DEPLOYMENT_AND_SETUP.md - For setup changes
   - TROUBLESHOOTING_AND_BEST_PRACTICES.md - For new best practices

### 9. Finalization

1. Move the old agent file to its appropriate versioning directory
2. Ensure all documentation is updated
3. Perform a final verification test
4. Document the final test results

### 10. Clean Up

1. Organize test files into appropriate version subdirectories
2. Remove any temporary files or debug code
3. Ensure versioning directories follow the consistent pattern

### 11. Create GitHub Release

Once the update is complete and tested, create a GitHub release to tag the version:

```zsh
cd ~/Development/single-file-agents && gh release create v[X.Y.Z] --title "v[X.Y.Z]: [Brief Title]" --notes "[Detailed release notes with features, changes, and fixes]"
```

Example: 

```zsh
cd ~/Development/single-file-agents && gh release create v3.2.2 --title "v3.2.2: Improve UX and fix token caching" --notes "This release includes UX improvements and fixes for Claude 3.7 token caching:\n\n- Remove debug statements that cluttered terminal output\n- Fix phase numbering to be 1-based instead of 0-based\n- Truncate task descriptions in terminal display\n- Increase Claude thinking display to 1000 characters\n- Add phase info to the loop separator bar\n- Fix Claude 3.7 model name for token caching"
```

## Technical Documentation Files

Detailed implementation documentation is organized in the following files within the `technical-docs` directory:

### 1. [CORE_ARCHITECTURE.md](./technical-docs/CORE_ARCHITECTURE.md)

- Configuration format and structure
- Workflow execution engine
- Phase management system
- Context window management
- Standardized workflows

### 2. [TOOLS_AND_CAPABILITIES.md](./technical-docs/TOOLS_CAPABILITIES.md)

- Complete tool reference
- Tool implementation details
- Tool parameters and return values
- Adding custom tools
- Tool execution flow

### 3. [PERFORMANCE_OPTIMIZATION.md](./technical-docs/PERFORMANCE_OPTIMIZATION.md)

- Token management strategies
- Token counting implementation
- Prompt caching system
- Performance benchmarking
- Context optimization techniques

### 4. [DEPLOYMENT_AND_SETUP.md](./technical-docs/DEPLOYMENT_SETUP.md)

- Setup scripts documentation
- Installation process
- Environment configuration
- Command creation process
- Workflow setup details

### 5. [TROUBLESHOOTING_AND_BEST_PRACTICES.md](./technical-docs/TROUBLESHOOTING_BEST_PRACTICES.md)

- Error handling patterns
- Common issues and solutions
- Best practices for workflows
- Configuration validation
- Test strategies

## Version Tagging in Documentation

Throughout the documentation, features are tagged with the version in which they were introduced. For example:

```markdown
## Token Caching System [v3_2_0]

The token caching system was introduced in v3_2_0 to improve performance...
```

This helps track when features were added and which version is required for specific functionality.