# Change Log

All notable changes to the Single-File Agent will be documented in this file in reverse chronological order (most recent changes at the top).

## Version Notes Guidelines

Underscores are used instead of periods because of a conflict with running the python script and finding the files. 

Each version should include documentation in the versioning directory with naming conventions:

- `v[X_Y_Z]_ERRORS.md` - Error reports and bugs to be fixed (working notes)
- `v[X_Y_Z]_PATCH.md` - "We just did xyz" bullet lists after changes
- `v[X_Y_Z]_[FEATURE_NAME].md` - For feature updates (e.g., IMAGE_EDITOR)
- `v[X_Y_Z]_UPDATE.md` - For major updates with evolving content

Test files should be documented in the PATCH document, including paths and test results.

## v3_3_0 - 2025-05-21

### Added
- Requesty API integration for multiple LLM providers
- Support for model selection with `M` configuration variable
- Command-line model selection with `--model` flag
- Format conversion between Claude and OpenAI formats
- Agent file variable support in setup script

### Changed
- Updated setup script to detect and use appropriate agent file
- Enhanced error handling with fallback to Claude
- Improved token tracking across different model providers

### Documentation
- Added v3_3_0_REQUESTY_LLM_VARIABLE.md documenting the feature
- Updated README with model selection information
- Updated TECHNICAL_DOCS with agent file variable details

## v3_2_2 - 2025-05-10

### Added
- UX improvements for workflow adjustment notifications
- Enhanced token tracking with better feedback
- Improved error messaging for file operations

### Changed
- Streamlined workflow adjustment messages
- Updated progress tracking for multiple output files
- Refined tool descriptions for better AI understanding

### Fixed
- Issues with token counting in large files
- Fixed script cache invalidation edge cases
- Resolved workflow continuation logic bugs

### Documentation
- Documentation restructuring and organization
- Improved guidelines for agent updates

## v3_2_1 - 2025-04-12

### Fixed
- Token counting errors in large documents
- Script caching mechanism issues
- Error handling in file operations
- Path handling inconsistencies

### Documentation
- Added v3_2_1_ERRORS.md documenting issues
- Added v3_2_1_PATCH.md with detailed fixes
- Updated error handling recommendations

## v3_2_0 - 2025-03-25

### Added
- Token saving optimization strategies
- Script content caching for performance
- Enhanced token usage tracking
- Better token cost estimation

### Changed
- Improved context window management
- Refined workflow adjustment mechanism
- Enhanced progress reporting

### Documentation
- Added v3_2_0_TOKEN_SAVING_EFFORTS.md

## v3_1_0 - 2025-02-18

### Added
- Image editing capabilities
- Support for visual content manipulation
- Font management for text overlay
- Image resizing and cropping tools

### Fixed
- Various bug fixes in workflow execution
- Error handling improvements

### Documentation
- Added v3_1_0_IMAGE_EDITOR.md documenting the feature
- Added v3_1_1_ERRORS.md documenting issues

## v3_0_0 - 2025-01-15

### Added
- Workflow tooling system
- Phase management with continuation options
- Token awareness and management
- Rich console output with progress tracking
- Structured task reporting

### Changed
- Complete architecture refactoring
- Enhanced tool system with expanded capabilities
- Improved workflow branching logic

### Documentation
- Added BRANCH_FLOW_UPDATE_IMPLEMENTATION.md
- Added PHASE_ADJUSTMENT_UPDATE.md
- Added TEST_RESULTS.md
- Added original workflow diagram

## v2_0_0 - 2024-11-20

### Added
- Decision branching capabilities
- Variable input architecture
- Enhanced workflow management

### Changed
- Refactored agent architecture for modularity
- Improved configuration handling

### Documentation
- Added VARIABLE_INPUT_UPDATES.md
- Added WORKFLOW_ASSESSMENT.md

## v1_0_0 - 2024-09-05

### Added
- Initial version based on IndyDevDan's single-file agent concept
- Basic LLM interaction using Claude
- Simple file operations
- Decision-making capabilities
- Web search functionality

### Documentation
- Added original SFA files