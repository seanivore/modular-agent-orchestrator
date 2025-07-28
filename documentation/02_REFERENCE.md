# Section II: Quick Reference Materials
*Everything you need to find quickly and start immediately*

---

This is your daily reference guide for productive work with Mao. Whether you're looking for a specific command, need to understand workflow variables, or want to troubleshoot an issue, this section provides immediate answers without the narrative context. Think of this as your technical cheat sheet.

---

## Essential Commands Quick Reference

### Application Launch and Core Workflow Commands
```bash
# Start Mao application
mao mao                                    # Launch main application

# Create workflows from natural language goals
mao --goal "create a marketing plan for my startup"

# Set up workflows from JSON configurations  
mao --setup ./config-files/workflow.json
mao --update ./config-files/phase-two.json  
mao --fix-it ./config-files/fix-requirements.json

# Monitor and manage workflows
mao --workflows                            # List all workflows
mao --stats                               # System performance metrics
mao --continue                            # Resume last workflow
```

### User and Session Management
```bash
# User management
mao --login [username]                    # Start user session
mao --logout                              # End user session
mao --config                              # Manage user settings
meid [username]                           # Generate user ID
uid                                       # Generate unique workflow ID

# System information and debugging
mao --help                               # Full command reference
mao --verbose                            # Detailed system output
mao --doctor                             # System health check
mao --logs                               # System logs and diagnostics
```

### Model, Provider, and Tool Management
```bash
# View available resources
mao --models                             # Available models
mao --providers                          # Available providers
mao --tools                              # Available tools
mao --variables                          # Workflow template variables
mao --variables-explain                  # Detailed variable explanations

# Set preferences
mao --model [model-name]                 # Set favorite model
mao --provider [provider-name]           # Set default provider
```

### In-App Command Equivalents
All terminal commands have in-app equivalents using `/` prefix:
```bash
# Inside Mao application
/goal "create a marketing plan"          # Same as --goal
/setup ./config.json                     # Same as --setup
/workflows                               # Same as --workflows
/config                                  # Same as --config
/help                                    # Same as --help
! ls -la                                 # Execute terminal commands
```

---

## Workflow Variables Reference

### Required Variables for All Workflows
| Variable               | Description                   | Format                | Example                                                 |
| ---------------------- | ----------------------------- | --------------------- | ------------------------------------------------------- |
| `user_id`              | Your unique user identifier   | `user-[number]`       | `user-1642`                                             |
| `workflow_id`          | Generated workflow identifier | `uid-[letters]-[num]` | `uid-abc-123`                                           |
| `custom_command`       | Your workflow command name    | `[space-separated]`   | `marketing analysis startup`                            |
| `workflow_goal`        | Primary objective             | Free text             | `Create comprehensive marketing strategy`               |
| `workflow_deliverable` | Expected output               | Free text             | `Marketing plan with budget and timeline`               |
| `workflow_description` | Detailed process description  | Free text             | `Multi-phase analysis including competitor research...` |

### Phase Configuration Variables
| Variable            | Description        | Format          | Example                         |
| ------------------- | ------------------ | --------------- | ------------------------------- |
| `phase_number`      | Phase sequence     | `01, 02, 03...` | `01`, `02a`, `02b`, `03`        |
| `phase_goal`        | Phase objective    | Free text       | `Research target market`        |
| `phase_deliverable` | Phase output       | Free text       | `Market research report`        |
| `phase_description` | Phase task details | Free text       | `Analyze competitor data`       |
| `resources`         | External resources | Array           | `["./data.md", "url.com"]`      |
| `tools`             | Required tools     | Array           | `["web_search", "text_editor"]` |

### Model and Provider Variables
| Variable     | Purpose              | Examples                           | Fallback Behavior     |
| ------------ | -------------------- | ---------------------------------- | --------------------- |
| `model_1`    | Primary model choice | `claude-sonnet-4`, `claude-opus-4` | Intelligent selection |
| `model_2`    | Backup model         | `claude-sonnet-3.7`                | Auto-fallback         |
| `model_3`    | Final fallback       | `claude-sonnet-3.5`                | Emergency option      |
| `provider_1` | Primary provider     | `anthropic-direct`, `litellm`      | Provider switching    |
| `provider_2` | Secondary provider   | Alternative provider               | Seamless handoff      |
| `provider_3` | Tertiary provider    | Fallback provider                  | Reliability guarantee |

### Handoff Configuration Variables
| Variable               | Description               | Format   | Example                        |
| ---------------------- | ------------------------- | -------- | ------------------------------ |
| `handoff_number`       | Handoff sequence          | `01, 02` | `01`                           |
| `assessment_questions` | Quality control questions | Array    | `["Is deliverable complete?"]` |
| `human_in_loop`        | Requires human approval   | `yes/no` | `no`                           |

---

## File System Architecture Quick Map

### Core System Files
```
./orchestrator/
├── core.py                    # Main workflow orchestration brain
├── conversation_bridge.py     # Natural language to workflows
├── agent_orchestrator.py      # Agent coordination and handoffs
├── cli_manager.py            # Command discovery and routing
├── workflow_manager.py       # Workflow lifecycle management
├── memory_mcp.py             # Persistent memory system
├── workflow_state.py         # State tracking and recovery
├── mcp_hub.py               # MCP integration coordination
├── cache/
│   └── cache_system.py       # Dual-layer caching system
├── manager_models.py         # AI model management
├── manager_tools.py          # Dynamic tool discovery
├── manager_buttons.py        # Universal code generation
├── settings_manager.py       # Dynamic settings management
├── username_manager.py       # User session management
├── user_analytics_manager.py # User analytics tracking
├── system_analytics_manager.py # System performance metrics
├── user_memory_manager.py    # Personal memory storage
├── real_time_metrics.py      # Live system monitoring
└── error_handling.py         # Professional error handling
```

### Configuration Directories
```
./configs/
├── cli/                      # Command definitions (3-file pattern)
├── models/                   # AI model specifications
├── providers/                # Service provider configurations
├── connections/              # Model-provider-tool mappings
├── settings/                 # Application settings
├── user/[username]/          # User-specific data
│   ├── analytics/           # User analytics (deletable)
│   └── memories/            # Personal memories
├── workflows/                # Active workflow storage
└── system/analytics/         # Anonymous system metrics
```

### Tool Architecture (6-File Pattern)
```
./tools/[tool_name]/
├── [tool_name].py           # Core tool functionality
├── ui_[tool_name].py        # Terminal interface
├── button_[tool_name].py    # Universal code generation
├── tool_[tool_name].json    # Tool configuration
├── [tool_name]_helpers.py   # Helper functions
└── [tool_name]_tests.py     # Testing functions
```

### Interface and Script Locations
```
./interfaces/
├── ui_terminal.py           # Main terminal application
└── ui_web.py               # Web interface (future)

./scripts/
├── mao_launch_setup/        # Installation scripts
├── workflow_setup/          # Workflow creation scripts
├── user_id_generator/       # User ID generation
├── unique_id_generator/     # Workflow ID generation
└── quality_validator/       # Configuration validation
```

---

## Application Settings Reference

### Core Settings Configuration
```bash
# View and modify settings
mao --config                             # Open settings interface
/config                                  # In-app settings

# Direct setting modification (planned)
mao --config theme dark                  # Visual appearance
mao --config default-provider anthropic-direct
mao --config favorite-model claude-sonnet-4
```

### Available Settings
| Setting             | Options                          | Purpose                  | Default             |
| ------------------- | -------------------------------- | ------------------------ | ------------------- |
| `quick_launch`      | `always`, `off`, `continue_only` | Startup behavior         | `always`            |
| `favorite_model`    | Model names                      | Preferred AI model       | `claude-sonnet-4`   |
| `default_provider`  | Provider names                   | Primary AI service       | `anthropic direct`  |
| `theme`             | `dark mode`, `light mode`, etc   | Interface appearance     | `dark mode CVD`     |
| `tone_notification` | `once no push`, `silent push`    | Completion notifications | `one time, no push` |
| `cat_vibes`         | `I love it`, `mao and then`      | Friendly communication   | `I love it`         |
| `double_texting`    | `always`, `never`                | Interrupt capability     | `always`            |

---

## Calendar and Trigger Workflow Codes

### Frequency Codes
| Code | Frequency         | Code | Frequency        |
| ---- | ----------------- | ---- | ---------------- |
| 1    | Every week        | 5    | Every year       |
| 2    | Every other week  | 6    | Every other year |
| 3    | Every month       | 7    | Every day        |
| 4    | Every other month | 8    | Every other day  |

### Day of Week Codes
| Code | Day       | Code | Day      |
| ---- | --------- | ---- | -------- |
| 1    | Monday    | 5    | Friday   |
| 2    | Tuesday   | 6    | Saturday |
| 3    | Wednesday | 7    | Sunday   |
| 4    | Thursday  |      |          |

### Time Block Codes
| Code | Time Block | Code | Time Block |
| ---- | ---------- | ---- | ---------- |
| 1    | 0000-0300  | 5    | 1200-1500  |
| 2    | 0300-0600  | 6    | 1500-1800  |
| 3    | 0600-0900  | 7    | 1800-2100  |
| 4    | 0900-1200  | 8    | 2100-0000  |

### Trigger Workflow Commands
```bash
# Check calendar availability
/avail [frequency] [day] [time]          # Check specific slot
/avail 3                                 # Suggest optimal monthly slot

# Create trigger workflows
/repeat --scheduled [temp_dir]           # Scheduled workflows
/repeat --list-new [temp_dir]           # New project list
/repeat --list-add [temp_dir]           # Add to existing list
/repeat --self-assessment [temp_dir]     # Self-improvement workflows
/repeat --goal-assessment [temp_dir]     # Goal-based projects
/repeat --sub-task [temp_dir]           # Subtasks for assessments
```

---

## Troubleshooting Quick Fixes

### Common Issues and Solutions
| Problem              | Symptom                   | Quick Solution        | Command                     |
| -------------------- | ------------------------- | --------------------- | --------------------------- |
| Command not found    | `command not found` error | Check system health   | `mao --doctor`              |
| Workflow won't start | Workflow fails to launch  | Verify user session   | `mao --login [username]`    |
| Model unavailable    | Model selection errors    | List available models | `mao --models`              |
| Configuration issues | Settings not saving       | Reset configuration   | Check user file permissions |
| Memory system errors | Context not persisting    | Check MCP connection  | `mao --doctor`              |

### Diagnostic Commands
```bash
# System health and status
mao --doctor                             # Comprehensive system check
mao --stats                              # Performance metrics
mao --logs                               # Recent system activity
mao --verbose [command]                  # Detailed command output

# Workflow debugging
mao --review [custom-command]            # Check workflow details
mao --workflows                          # List all workflows
mao --variables                          # Check variable definitions
```

### File Location Diagnostics
```bash
# Check if files exist in expected locations
ls -la configs/user/[username]/          # User configuration
ls -la configs/workflows/                # Workflow storage
ls -la tools/                           # Available tools
which mao                                # Mao command location
which [custom-command]                   # Custom workflow commands
```

---

## JSON Configuration Templates

### Minimal Workflow Configuration
```json
{
  "workflow": [{
    "user_id": "user-1642",
    "workflow_id": "uid-abc-123",
    "custom_command": "marketing analysis startup",
    "workflow_goal": "Create marketing analysis",
    "workflow_deliverable": "Marketing analysis report",
    "workflow_description": "Analyze market and create report"
  }]
}
```

### Phase Configuration
```json
{
  "phase": [{
    "workflow_id": "uid-abc-123",
    "phase_number": "01",
    "phase_goal": "Research market",
    "phase_deliverable": "Market research report",
    "phase_description": "Research target market and competitors",
    "resources": ["./data/market_info.md"],
    "tools": ["web_search", "text_editor"],
    "model_1": "claude-sonnet-4",
    "provider_1": "anthropic-direct"
  }]
}
```

### Handoff Configuration
```json
{
  "handoff": [{
    "workflow_id": "uid-abc-123",
    "handoff_number": "01",
    "assessment_questions": [
      "Is the market research comprehensive?",
      "Are all data sources included?",
      "Is the analysis actionable?"
    ],
    "human_in_loop": "no"
  }]
}
```

---

## Performance Optimization Tips

### Speed Enhancement Strategies
- **Use caching**: Mao automatically caches analysis and content fingerprints
- **Set favorite model**: Consistent model selection improves response patterns
- **Enable parallel phases**: Use phase numbering like `01a`, `01b` for parallel execution
- **Leverage Memory MCP**: Context persistence reduces redundant processing

### Resource Management
- **Budget awareness**: Mao tracks costs in real-time with daily budget management
- **Model selection**: Intelligent selection balances cost, speed, and capability
- **Tool optimization**: Dynamic tool discovery prevents unnecessary tool loading
- **Cache optimization**: Dual-layer caching system (Files API + local fingerprinting)

---

*This reference provides immediate answers to common questions and tasks. For deeper understanding of concepts and architecture, explore the narrative documentation sections. For implementation details, refer to the specific architecture sections in the main documentation.*