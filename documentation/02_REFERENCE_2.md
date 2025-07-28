# Section II: Quick Reference Materials
*Everything you need to find quickly and start immediately*

---

Welcome to the practical heart of Mao documentation. Whether you're looking for a specific command, need to understand workflow variables, or want to troubleshoot an issue, this section provides immediate answers without the full narrative context. Think of this as your daily reference guide for productive work with Mao.

---

## Essential Commands Quick Reference

### Core Workflow Commands
```bash
# Get started with natural language goals
mao --goal "create a marketing plan for my startup"

# Set up workflows from JSON configurations  
mao --setup ./config-files/workflow.json
mao --update ./config-files/phase-two.json  
mao --fix-it ./config-files/fix-requirements.json

# Monitor and manage workflows
mao --workflows                    # List all workflows
mao --stats                       # System performance metrics
```

### User and Session Management
```bash
# User management
mao --login [username]            # Start user session
mao --user-id                     # Generate or show user ID
mao --config                      # Manage user settings

# System information  
mao --help                        # Full command reference
mao --verbose                     # Detailed system output
mao --logs                        # System logs and diagnostics
```

### Development and Debugging
```bash
# Debugging and development
mao --doctor                      # System health check
mao --models                      # Available models and providers
mao --tools                       # Available tools and capabilities
mao --variables                   # Workflow template variables
mao --variables --explain         # Detailed variable explanations
```

---

./modular-agent-orchestrator/orchestrator/
├── `__init__.py` --> orchestration package modular AI workflow system
├── `agent_callback.py` --> handles agent returns, execution results, and workflow progression
├── `agent_orchestrator.py` --> coordinates agent handoffs with context packages via Files API
├── `cache` --> our dual-layer hybrid caching system 
│   ├── `__init__.py` --> universal caching package for everything 
│   └── `cache_system.py` --> Files API for workflow handoffs; local cache for permanence; fingerprinting
├── `cli_manager.py` --> CLI command discovery, integration of slash commands to orchestrator functionality
├── `conversation_bridge.py` --> Converts natural language goals into executable custom commands
├── `core.py` --> main brain that turns natural language into intelligent workflows
├── `error_handling.py` --> Professional error handling patterns for universal files 
├── `manager_buttons.py` --> "Button" code snippet generator; avoids SDK usage 
├── `manager_models.py` --> Loads JSON configs and provides intelligent model selection
├── `manager_tools.py` --> Dynamic tool discovery; suggestion based on goals, not hardcoded categories
├── `mcp_hub.py` --> Integrates Memory MCP, Files API, and MCP Connector into unified system
├── `memory_mcp.py` --> Provides workflow state persistence for context tracking, state management, session recovery
├── `protocol.md` --> *empty file; guidelines for Mao chat interactions; behavior protocol* 
├── `real_time_metrics.py` --> Provides live data for UI components; no mock data allowed
├── `settings_manager.py` --> settings discovery, management; directory-based scanning of individual setting files
├── `system_analytics_manager.py` --> tracks system-wide performance metrics with full anonymization and privacy compliance
├── `user_analytics_manager.py` --> user-specific analytics with GDPR compliance; dynamic tool discovery
├── `user_memory_manager.py` --> user-specific memory storage, retrieval, management with Memory MCP integration
├── `username_manager.py` --> user creation, session persistence, settings integration
├── `workflow_manager.py` --> workflow ID generation, discovery, tracking
└── `workflow_state.py` --> simple state tracking with Memory MCP integration



---

## Workflow Variables Reference

### Required Variables for All Workflows
| Variable               | Description                   | Format               | Example                                                 |
| ---------------------- | ----------------------------- | -------------------- | ------------------------------------------------------- |
| `user_id`              | Your unique user identifier   | `user-[identifier]`  | `user-john_doe_2024`                                    |
| `workflow_id`          | Generated workflow identifier | `uid-[generated]`    | `uid-0000`                                              |
| `custom_command`       | Your workflow command name    | `[descriptive-name]` | `marketing analysis`                                    |
| `workflow_goal`        | Primary objective             | Free text            | `Create comprehensive marketing strategy`               |
| `workflow_deliverable` | Expected output               | Free text            | `Marketing plan with budget and timeline`               |
| `workflow_description` | Detailed process description  | Free text            | `Multi-phase analysis including competitor research...` |

### Optional Variables for Enhanced Workflows
| Variable         | Description             | Default                           | Usage                     |
| ---------------- | ----------------------- | --------------------------------- | ------------------------- |
| `temp_directory` | Processing workspace    | `configs/workflows/.temp/[name]/` | During workflow creation  |
| `created_at`     | Creation timestamp      | Current time                      | Automatic tracking        |
| `phase_number`   | Phase sequence          | `01, 02, 03...`                   | Multi-phase workflows     |
| `resources`      | External resources      | `[]`                              | URLs, files, data sources |
| `tools`          | Specific tools required | Auto-detected                     | Tool preferences          |

### Model and Provider Variables
| Variable     | Purpose              | Examples                            | Fallback Behavior     |
| ------------ | -------------------- | ----------------------------------- | --------------------- |
| `model_1`    | Primary model choice | `claude-sonnet-4`, `gpt-4.1`        | Intelligent selection |
| `model_2`    | Backup model         | Alternative model                   | Auto-fallback         |
| `model_3`    | Final fallback       | Reliable model                      | Emergency option      |
| `provider_1` | Primary provider     | `anthropic-direct`, `openai-direct` | Provider switching    |
| `provider_2` | Secondary provider   | Alternative provider                | Seamless handoff      |
| `provider_3` | Tertiary provider    | Fallback provider                   | Reliability guarantee |

---

## Application Settings Reference

### Core Settings Categories
```bash
# View all available settings
mao --config --list

# Modify specific settings  
mao --config theme dark             # Visual appearance
mao --config default-provider anthropic-direct
mao --config favorite-model claude-sonnet-4
mao --config double-texting true    # Interrupt capability
mao --config cat-vibes true         # Friendly mode
mao --config quick-launch false     # Startup behavior
mao --config tone-notification subtle
```

### Settings Descriptions
| Setting             | Options                  | Purpose                 | Default             |
| ------------------- | ------------------------ | ----------------------- | ------------------- |
| `theme`             | `light`, `dark`, `auto`  | Interface appearance    | `auto`              |
| `default-provider`  | Provider names           | Primary AI service      | Based on setup      |
| `favorite-model`    | Model names              | Preferred AI model      | Intelligent default |
| `double-texting`    | `true`, `false`          | Interrupt workflows     | `false`             |
| `cat-vibes`         | `true`, `false`          | Friendly communication  | `true`              |
| `quick-launch`      | `true`, `false`          | Fast startup mode       | `false`             |
| `tone-notification` | `subtle`, `clear`, `off` | Status indicators       | `subtle`            |
| `data-collection`   | Privacy levels           | Analytics participation | `privacy-first`     |

---

## System Architecture Quick Map

### File Organization Overview
```
mao-v4/
├── orchestrator/              # Core intelligence system
│   ├── core.py               # Main workflow orchestration
│   ├── cli_manager.py        # Command routing and discovery
│   ├── memory_mcp.py         # Persistent memory system
│   ├── workflow_manager.py   # Workflow lifecycle management
│   └── managers/             # Specialized managers
├── configs/                  # All configuration files
│   ├── cli/                  # Command definitions
│   ├── models/               # AI model configurations
│   ├── providers/            # Service provider settings
│   ├── tools/                # Tool configurations
│   └── workflows/            # Workflow templates and active workflows
├── tools/                    # Available tool implementations
├── interfaces/               # User interface layers
└── scripts/                  # Utility and setup scripts
```

### Key System Components
| Component             | Purpose                  | Location                           | Integration Points    |
| --------------------- | ------------------------ | ---------------------------------- | --------------------- |
| **Core Orchestrator** | Main intelligence engine | `orchestrator/core.py`             | All system components |
| **CLI Manager**       | Command routing          | `orchestrator/cli_manager.py`      | Interface layer       |
| **Memory System**     | Persistent learning      | `orchestrator/memory_mcp.py`       | User data, workflows  |
| **Workflow Manager**  | Project lifecycle        | `orchestrator/workflow_manager.py` | User goals, execution |
| **Tool Discovery**    | Capability detection     | `orchestrator/manager_tools.py`    | Dynamic tool loading  |
| **Model Selection**   | AI service routing       | `orchestrator/manager_models.py`   | Provider management   |

---

## Troubleshooting Quick Fixes

### Common Issues and Solutions
| Problem                | Quick Solution           | Command                      |
| ---------------------- | ------------------------ | ---------------------------- |
| Command not found      | Update command discovery | `mao --doctor`               |
| Workflow won't start   | Check user session       | `mao --login [username]`     |
| Model unavailable      | List available models    | `mao --models`               |
| Slow performance       | Clear cache              | `mao --doctor --clear-cache` |
| Memory issues          | Restart with fresh state | `mao --restart`              |
| Configuration problems | Reset to defaults        | `mao --config --reset`       |

### Diagnostic Commands
```bash
# System health and status
mao --doctor                      # Comprehensive system check
mao --stats                       # Performance metrics
mao --logs                        # Recent system activity
mao --verbose [command]           # Detailed command output

# Cache and performance
mao --doctor --clear-cache        # Clear system cache
mao --stats --real-time          # Live performance monitoring

# Configuration diagnosis
mao --config --validate          # Check configuration integrity
mao --config --export            # Backup current settings
mao --config --import [file]     # Restore settings
```

### Error Code Reference
| Code      | Meaning                | Common Causes        | Solution                 |
| --------- | ---------------------- | -------------------- | ------------------------ |
| `ERR_001` | Authentication failure | Invalid user session | `mao --login`            |
| `ERR_002` | Workflow configuration | JSON syntax error    | Validate JSON syntax     |
| `ERR_003` | Model unavailable      | Provider issues      | `mao --models --refresh` |
| `ERR_004` | Tool not found         | Missing dependencies | `mao --tools --update`   |
| `ERR_005` | Memory system          | MCP connection       | `mao --doctor --memory`  |

---

## Performance Optimization Tips

### Speed Enhancement Strategies
```bash
# Enable intelligent caching
mao --config cache-optimization true

# Use preferred models for consistency
mao --config favorite-model [your-preferred-model]

# Optimize tool selection
mao --tools --optimize-for speed

# Batch similar operations
mao --setup [multiple-configs] --batch-mode
```

### Resource Management
```bash
# Monitor resource usage
mao --stats --resources

# Set budget constraints
mao --config max-cost-per-workflow 5.00

# Enable cost optimization
mao --config cost-optimization aggressive

# Track spending
mao --stats --costs --period month
```

---

## Integration Patterns

### External System Integration
```bash
# Export workflow results
mao --export-workflow [workflow-id] --format json

# Import external data
mao --import-data [file] --type [csv|json|text]

# API access patterns
mao --api-key generate              # Create API access
mao --api-key list                  # View active keys
mao --api-key revoke [key-id]       # Remove access
```

### Development Integration
```bash
# Development mode
mao --dev-mode enable               # Enhanced logging
mao --dev-mode test [workflow]      # Dry run workflows
mao --dev-mode validate [config]    # Configuration testing

# Custom tool development
mao --create-tool [name]            # Generate tool template
mao --install-tool [path]           # Add custom tool
mao --test-tool [name]              # Validate tool integration
```

---

*This reference section provides immediate answers to common questions and tasks. For deeper understanding of concepts and architecture, explore the full documentation sections. For urgent issues, start with the troubleshooting section and diagnostic commands.*