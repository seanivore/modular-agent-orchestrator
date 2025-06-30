# Mao v4 Context Jump - User Configuration & Setup Script Implementation

## PROJECT STATE SUMMARY

**Tool Standardization Phase: COMPLETE ✅**
- 51 files standardized across entire MAO v4 ecosystem
- Real orchestrator integration fixes applied (no more mock data)
- Real-time metrics infrastructure created (orchestrator/real_time_metrics.py)

## IMMEDIATE TASKS READY FOR IMPLEMENTATION

### TASK 1: User Configuration System 
**Status**: Well-defined specs, ready for Claude Code implementation
**Priority**: Foundation requirement
**Files Needed**: Create configs/user/ directory and user config management

#### Setting Options & Descriptions

| **SETTING**       | **DEFAULT**        | **DESCRIPTION**                                      |
| ----------------- | ------------------ | ---------------------------------------------------- |
| Quick launch      | `always`           | Launch app with last user logged in                  |
| Favorite model    | `claude-sonnet-4`  | Use for workflows unless discussed                   |
| Default provider  | `anthropic direct` | I prefer this provider; discuss to change            |
| Theme             | `dark mode CVD`    | Dark computer theme; use high legibility colors      |
| Cat vibes         | `I love it`        | We'll meow it up for you                             |
| Double-texting    | `always`           | Interrupt Mao like any messenger experience          |
| Tone notification | `once, no push`    | When a workflow is complete, a simple tone is played |

**Quick Launch Options:**
1. `always` - Launch app with user from last session, unless logged out
2. `off` - Load Username login on every startup 
3. `continue only` - Launch `mao --continue` to skip login, otherwise load Username login

**Tone Notification Options:**
1. `once, no push` - When a workflow is complete, a simple tone is played, no push notification
2. `silent, push` - When a workflow is complete, no tone is played, but a push notification announces completion
3. `no notifications` - No tone is played, no push notification

#### Implementation Requirements
1. Create `configs/user/user_username.json` files for each user
2. Load settings on app startup (default to last session user)
3. `/config` command opens settings interface
4. `mao --config` launches directly to config screen
5. Settings persist across sessions
6. UI follows NEW_USER_FLOW.md visual patterns

### TASK 2: Setup Script Implementation
**Status**: Architecture designed, examples available from SFA
**Priority**: Enables multi-JSON workflow system
**Reference**: Use SFA v3 examples for custom command patterns

#### Multi-Object JSON Workflow System
Three separate JSON objects per workflow:
1. `command_use_case_workflow_config.json` - Main workflow configuration
2. `command_use_case_phase_config.json` - Individual phase definitions  
3. `command_use_case_handoff_config.json` - Human-in-loop and review points

#### Setup Script Requirements
1. Process temp JSON objects from `./configs/workflows/.temp/use_case_name/`
2. Create final workflow directory: `./configs/workflows/command_use_case/`
3. Generate custom command script and install to `~/bin/`
4. Create directory structure:
   ```
   configs/workflows/command_use_case/
   ├── config-files/
   │   ├── command_use_case_workflow_config.json
   │   ├── command_use_case_phase_config.json
   │   └── command_use_case_handoff_config.json
   ├── README_command_use_case.md
   ├── command_use_case.sh
   ├── metadata/
   │   ├── command_use_case_memory.json
   │   └── command_use_case_log.md
   └── deliverables/
       └── command_use_case_report.md
   ```

#### Command Naming Protocol
- 2-3 words maximum
- Reverse drill-down order (marketing strategy, not strategy marketing)
- Follow git-style patterns
- No hyphens, plurals, or complex grammar
- Present tense, simple forms

#### SFA Examples Reference
Located in: `./versioning-docs/v1-3_SFA/use-case/`
Examples of working custom commands:
- `doc-research-simple`
- `doc-brand-email`
- `marketing-strategy`
- `job-me-up`

## KEY ARCHITECTURE DECISIONS

### Real Data Integration (NO MORE MOCK DATA)
- Fixed ui_terminal.py to call real orchestrator methods
- Created real-time metrics providers (SystemMetricsProvider, WorkflowMonitor, CostTracker)
- All stats, workflows, and progress data now comes from real sources

### Multi-JSON Workflow Architecture
- Modular JSON objects instead of monolithic files
- `"type": "needs_file_or_directory"` supports both individual files and directories
- Setup script processes multiple objects and creates unified workflow

### Custom Command Strategy
- Install to `~/bin/` following established pattern (like meid, uid, ptree, token)
- Each workflow becomes a memorable command (marketing strategy)
- Avoids complex flag management

## CLAUDE CODE IMPLEMENTATION CONTEXT

### For User Configuration Task
**Include**: Complete NEW_USER_FLOW.md file for UI/UX context
**Focus**: Settings schema, persistence, and interface integration
**Dependencies**: Existing orchestrator and config system

### For Setup Script Task  
**Include**: SFA use-case examples and NEW_USER_FLOW.md workflow sections
**Focus**: Multi-JSON processing and custom command generation
**Dependencies**: User configuration system, orchestrator integration

## INTEGRATION POINTS

### Real-Time Features Ready
- `orchestrator/real_time_metrics.py` provides live data for UI
- No mock data - all metrics come from real system state
- Foundation build can use SystemMetricsProvider, WorkflowMonitor, CostTracker

### Orchestrator Integration Complete
- `WorkflowOrchestrator.create_workflow_from_goal()` works
- `list_workflows()`, `get_workflow_status()` provide real data
- UI terminal methods now call real orchestrator functions

### Memory MCP Integration
- Ready for workflow state persistence
- Connects to existing Memory MCP system
- Supports session recovery and continuation

## CURRENT FILE STATE

### Recently Fixed/Created
- `interfaces/ui_terminal.py` - Fixed mock data, now uses real orchestrator
- `orchestrator/real_time_metrics.py` - New real-time data providers
- `scripts/user_id_generator/install_meid_command.sh` - Fixed logic error
- `scripts/quality_validator/mao-validate` - Fixed path issues
- All CLI configs created for missing commands

### Ready for Enhancement
- User configuration system (well-specified, ready to build)
- Setup script implementation (architecture designed)
- Claude Code spec integration (NEW_USER_FLOW.md provides UI context)

## SUCCESS CRITERIA

### User Configuration System
- ✅ Settings persist across sessions
- ✅ `/config` interface works smoothly  
- ✅ Default to last session user
- ✅ All 7 settings functional with proper options

### Setup Script System
- ✅ Multi-JSON workflow processing
- ✅ Custom command generation and installation
- ✅ Proper directory structure creation
- ✅ Integration with orchestrator workflow creation

### Foundation Readiness
- ✅ Real data providers available for UI
- ✅ No mock data in system
- ✅ Clear architecture for Claude Code development
- ✅ NEW_USER_FLOW.md provides comprehensive UI/UX guidance

---

**NEXT ACTIONS**: Implement user configuration system first (foundational), then setup script system (enables workflows), then enhance Claude Code specs with working implementations.
