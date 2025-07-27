# Documentation Preparation Guide

## Session Setup 

  1. Start a `sequential_thinking` session 
  2. Review what is written in or Project State use of the `memory` MCP, searching for the term `Mao Documentation Reorganization Project` 
  3. Look around for any other relevant information in the `memory` MCP and let me know if you find anything so that we can just include it specifically on this list and remove this open ended 'look around' note 
  4. Review the `CLAUDE.md` file, our guide for standardization and rules 
  5. Use this to understand the current state of the documentation pages we were working on: `./documentation/doc_prep_steps.md` you can see right at the top, under "We need to focus on TASK 1 first", I state "I'm not sure where CLI is... I think we should add it to..." which underscores the core issue with our previous process. No concrete plan on what goes where. The lack of clarity of an outline and the large size of the codebase has only made it continue to be difficult to write the documentation to completion. However, some of the files have been heavily edited and are in a good state. We will need to work through them one by one after identifying the online. I like the idea of our current doc state, the flow is good, writing was getting there, but we need to get the code architecture in place which requires a comprehensive outline with concrete plan on what goes where. g

## Overview

Developing a pragmatic approach to finishing up the documentation for Mao that maintains and builds on the current flow and narrative of the documents, and ensures the strategic content and writing style that was established to address the needs of standard documentation, as well as marketing and pitching audiences. 

### Strategic Content & Writing Style 

* Create documentation that is less dense and more accessible, modeling the style of Anthropic's documentation, for example. 
* Employ a pattern of writing using very brief paragraphs and long-form bullet points, that is proceeded by the code architecture related to the topics just discussed. This then continues with a patter of writing about the tool, then code about what was just written, etc. 
* Still ensure comprehensive coverage of the Mao system 

## Key Steps

### STEP 1: Initial Outline Building 
*enter with current state of documentation, exit with an outline of the current documentation along with the intention implied for the rest of the documentation features to be covered* 

- Review the current state of documentation 
- Consolidate and clean up multiple pages of documentation for a single section, a flaw of earlier processes 
- Create an outline based on the contents and flow 

#### Core Docs 

- `documentation/03_USER_FLOW_00.md`
- `documentation/03_USER_FLOW.md`

- `documentation/04_INTERFACE.md`

- `documentation/05_ORCHESTRATION.md`

- `documentation/06_ANALYTICS_MEMORY.md`

- `documentation/07_AUTOMATE_INTELLIGENCE.md`

- `documentation/08_FUTURE_THINKING_old-outline.md`
- `documentation/08_FUTURE_THINKING_original.md`
- `documentation/08_FUTURE_THINKING_semi-recent-never-reviewed.md`
- `documentation/08_FUTURE_THINKING.md`

#### Secondary Docs 

- `documentation/00_OVERVIEW_2.md`
- `documentation/00_OVERVIEW.md`

- `documentation/01_EVOLVING_AI_2.md`
- `documentation/01_EVOLVING_AI.md`

- `documentation/02_REFERENCE_2.md`
- `documentation/02_REFERENCE.md`

### STEP 2: Review & Feedback 
*enter with initial outline, exit with concrete understanding of the outline and the intention implied for the rest of the documentation features to be covered* 

- Review the initial outline 
- Opportunity to address items that are intentional 
- And remove items that are not intentional and merely a product of the process 
- Sean to gather any specific resources for the documentation 

### STEP 3: Building Out Comprehensive Outline 
*enter with initial outline, exit with comprehensive outline of the documentation features to be covered that includes notation of where each topic's code is located* 

- Take what is left after step 2 
- Review all of the files in the project directory tree, provided below 
- Build on the outline making it comprehensive as a tool to guide the writing process 
  - Decides where each item or feature will be addressed 
  - Ensures all features are addressed 
  - Ensures the flow of the documentation is maintained 
- Denote what file an architecture section is referencing 
  - This can be maintained in the actual documentation; each section chapter in the docs will highlight what files are relevant 
  - Helps while writing to know exactly where to go to find the code 
  - This solves the problem of context window limitations 

### STEP 4: Writing 
*enter with comprehensive outline, exit with completed documentation as well as implementation docs for trigger system and UI plans* 

- Write the documentation 
- Ensure the writing is consistent with the style of the documentation 

## Intention 

The codebase is rather large and complex which is making it difficult to construct documentation because of AI context window limitations. As a result, I've been struggling, have dealt with multiple issues where Claude Code completely made up code and consistently complained about needing to read files and do things "manually". This led to broken pages of each section of documentation, and an inability to see how to close the gap when there is so much code to keep track of. Initially the idea was to write the text of the documentation first and then add code snippets. By creating the outline first, we can do just that, but without the need to read the codebase at the time of writing to know what code to add and from where to find it. 

## Flow of Documentation VS Our Outline/Writing Process 

- **Core documentation** is intended to use the implied narrative, much of which has been written and edited down, to create a flow of the documentation that covers the entirety of the system. All concepts and features are intended to be addressed here. 

- **Secondary documentation** is has the following intentions to address after the completion of the core documentation. 
  1. Overview = a more narrative version of a simple table of contents 
  2. Evolving AI = an actual introduction to the product, brand story, and vision 
  3. Reference = comprehensive user-guide references of the system, including commands and other need to reference information 

### Core Documentation  

- `03_USER_FLOW.md`
- `04_INTERFACE.md`
- `05_ORCHESTRATION.md`
- `06_ANALYTICS_MEMORY.md`
- `07_AUTOMATE_INTELLIGENCE.md`
- `08_FUTURE_THINKING.md`

### Secondary Documentation  

- `00_OVERVIEW.md`
- `01_EVOLVING_AI.md`
- `02_REFERENCE.md`

### Conceptual Flow of Core Documentation 

We start with the end-to-end flow of a first time user's experience. 
- What they will encounter and how they will interact with the system. 
- This is broken up into digestible sections that are to be followed by code architecture of that section. 

We then "follow the flow of data" through the system. 
- This is meant to follow nicely what the user was doing in the 'user flow' section with the data that is being passed through the system, in the 'interface' section. 
- The data then is processed by the system and results returned to the user; as explained by the 'orchestration' section which is meant to cover the core system files. 
- This is a section where we are meant to write about the UI plans as if they are already implemented, as a means to create the actual implementation documentation. 

We then cover the analytics and memory of the system. 
- Now we're getting into how data and technology are used to create a novel user experience. 
- It is where we start to introduce the value of the system and the potential of the product. 

This value's climax would then be the 'automate intelligence' section. 
- In writing it we came up with the actual logic for implementing the actual automation of intelligence. 
- This trigger system is being included as a means to create the implementation documentation which will be implemented after creating documentation. 

We then wrap up things by looking forward. 
- This is meant to cover the ideas we have planned already. 
- And also sprinkle in ideas that are not yet planned but are in the works, or are just brilliant possibilities. 

## Project Directory Tree 

~/Development/modular-agent-orchestrator
├── _config.yml
├── .archive
├── .example.env
├── .gitignore
├── CLAUDE.md
├── configs
│   ├── cli
│   │   ├── chat
│   │   │   ├── chat.json
│   │   │   ├── chat.py
│   │   │   └── ui_chat.py
│   │   ├── config
│   │   │   ├── config.json
│   │   │   ├── config.py
│   │   │   └── ui_config.py
│   │   ├── continue
│   │   │   ├── continue.json
│   │   │   ├── continue.py
│   │   │   └── ui_continue.py
│   │   ├── default_provider
│   │   │   ├── default_provider.json
│   │   │   ├── default_provider.py
│   │   │   └── ui_default_provider.py
│   │   ├── doctor
│   │   │   ├── doctor.json
│   │   │   ├── doctor.py
│   │   │   └── ui_doctor.py
│   │   ├── dry_run
│   │   │   ├── dry_run.json
│   │   │   ├── dry_run.py
│   │   │   └── ui_dry_run.py
│   │   ├── exit
│   │   │   └── exit.json
│   │   ├── fix_it
│   │   │   ├── fix_it.json
│   │   │   ├── fix_it.py
│   │   │   └── ui_fix_it.py
│   │   ├── goal
│   │   │   ├── goal.json
│   │   │   ├── goal.py
│   │   │   └── ui_goal.py
│   │   ├── help
│   │   │   ├── help.json
│   │   │   ├── help.py
│   │   │   └── ui_help.py
│   │   ├── login
│   │   │   ├── login.json
│   │   │   ├── login.py
│   │   │   └── ui_login.py
│   │   ├── logout
│   │   │   ├── logout.json
│   │   │   ├── logout.py
│   │   │   └── ui_logout.py
│   │   ├── logs
│   │   │   ├── logs.json
│   │   │   ├── logs.py
│   │   │   └── ui_logs.py
│   │   ├── mao
│   │   │   ├── mao.json
│   │   │   ├── mao.py
│   │   │   └── ui_mao.py
│   │   ├── memory
│   │   │   ├── memory.json
│   │   │   ├── memory.py
│   │   │   └── ui_memory.py
│   │   ├── model
│   │   │   └── model.json
│   │   ├── models
│   │   │   ├── models.json
│   │   │   ├── models.py
│   │   │   └── ui_models.py
│   │   ├── onboard
│   │   │   ├── onboard.json
│   │   │   ├── onboard.py
│   │   │   └── ui_onboard.py
│   │   ├── output_directory
│   │   │   ├── output_directory.json
│   │   │   ├── output_directory.py
│   │   │   └── ui_output_directory.py
│   │   ├── privacy
│   │   │   └── privacy.json
│   │   ├── provider
│   │   │   └── provider.json
│   │   ├── provider_list
│   │   │   └── provider_list.json
│   │   ├── providers
│   │   │   ├── providers.json
│   │   │   ├── providers.py
│   │   │   └── ui_providers.py
│   │   ├── restart
│   │   │   └── restart.json
│   │   ├── review
│   │   │   ├── review.json
│   │   │   ├── review.py
│   │   │   └── ui_review.py
│   │   ├── set_model
│   │   │   ├── set_model.json
│   │   │   ├── set_model.py
│   │   │   └── ui_set_model.py
│   │   ├── setup
│   │   │   ├── setup.json
│   │   │   ├── setup.py
│   │   │   └── ui_setup.py
│   │   ├── stats
│   │   │   ├── stats.json
│   │   │   ├── stats.py
│   │   │   └── ui_stats.py
│   │   ├── tools
│   │   │   ├── tools.json
│   │   │   ├── tools.py
│   │   │   └── ui_tools.py
│   │   ├── update
│   │   │   ├── ui_update.py
│   │   │   ├── update.json
│   │   │   └── update.py
│   │   ├── user_id
│   │   │   ├── ui_user_id.py
│   │   │   ├── user_id.json
│   │   │   └── user_id.py
│   │   ├── variables
│   │   │   ├── ui_variables.py
│   │   │   ├── variables.json
│   │   │   └── variables.py
│   │   ├── variables_explain
│   │   │   └── variables_explain.json
│   │   ├── verbose
│   │   │   ├── ui_verbose.py
│   │   │   ├── verbose.json
│   │   │   └── verbose.py
│   │   ├── workflow_id
│   │   │   ├── ui_workflow_id.py
│   │   │   ├── workflow_id.json
│   │   │   └── workflow_id.py
│   │   └── workflows
│   │       ├── ui_workflows.py
│   │       ├── workflows.json
│   │       └── workflows.py
│   ├── connections
│   │   ├── mcp_servers.json
│   │   ├── models_x_tools.json
│   │   └── providers_x_models.json
│   ├── models
│   │   ├── claude-3-7-sonnet.json
│   │   ├── claude-opus-4.json
│   │   ├── claude-sonnet-4.json
│   │   ├── gemini-2.5-pro.json
│   │   ├── gpt-4.1-mini.json
│   │   ├── gpt-4.1-nano.json
│   │   └── local-llama-3.1-8b.json
│   ├── providers
│   │   ├── anthropic-direct.json
│   │   ├── gemini-direct.json
│   │   ├── litellm.json
│   │   ├── lm-studio.json
│   │   ├── openai-direct.json
│   │   └── requesty.json
│   ├── settings
│   │   ├── application_settings_schema.json
│   │   ├── cat_vibes_app_settings.json
│   │   ├── data_collection_app_settings.json
│   │   ├── default_provider_app_settings.json
│   │   ├── double_texting_app_settings.json
│   │   ├── favorite_model_app_settings.json
│   │   ├── quick_launch_app_settings.json
│   │   ├── theme_app_settings.json
│   │   └── tone_notification_app_settings.json
│   ├── system
│   │   └── analytics
│   │       ├── aggregate_usage.json
│   │       └── tool_performance.json
│   ├── user
│   │   └── seanivore
│   │       ├── analytics
│   │       │   ├── cost_tracking.json
│   │       │   ├── session_metrics.json
│   │       │   ├── tool_usage.json
│   │       │   └── workflow_metrics.json
│   │       ├── memories
│   │       │   ├── personal_preferences.json
│   │       │   └── project_context.json
│   │       └── user_seanivore.json
│   └── workflows
│       └── json_object_templates
│           ├── command_use_case_handoff_config.json
│           ├── command_use_case_phase_config.json
│           └── command_use_case_workflow_config.json
├── documentation
│   ├── 00_OVERVIEW_2.md
│   ├── 00_OVERVIEW.md
│   ├── 01_EVOLVING_AI_2.md
│   ├── 01_EVOLVING_AI.md
│   ├── 02_REFERENCE_2.md
│   ├── 02_REFERENCE.md
│   ├── 03_USER_FLOW_00.md
│   ├── 03_USER_FLOW.md
│   ├── 04_INTERFACE.md
│   ├── 05_ORCHESTRATION.md
│   ├── 06_ANALYTICS_MEMORY.md
│   ├── 07_AUTOMATE_INTELLIGENCE.md
│   ├── 08_FUTURE_THINKING_old-outline.md
│   ├── 08_FUTURE_THINKING_original.md
│   ├── 08_FUTURE_THINKING_semi-recent-never-reviewed.md
│   ├── 08_FUTURE_THINKING.md
│   ├── doc_prep_guide.md
│   ├── doc_prep_steps.md
│   └── FILE_BATCH_DEFINITIONS
│       ├── ARCHITECTURE_SECTIONS
│       │   ├── ARCH_01_Architecture_Overview.md
│       │   ├── ARCH_02_Core_System_Patterns.md
│       │   ├── ARCH_03_Tool_Integration_Patterns.md
│       │   ├── ARCH_04_Configuration_Data_Patterns.md
│       │   ├── ARCH_05_User_Interface_Patterns.md
│       │   └── ARCH_06_Extension_Automation_Patterns.md
│       ├── FILE_BATCH_DEFINITION_PROMPTS
│       │   ├── CLI_COMMAND_SYSTEM.md
│       │   ├── CONFIGURATION_MANAGEMENT.md
│       │   ├── CORE_SYSTEM_ARCHITECTURE.md
│       │   ├── TEMPLATES_AND_SCRIPTS.md
│       │   ├── TOOLS_ECOSYSTEM.md
│       │   └── UI_TYPESCRIPT_INTEGRATION.md
│       └── GATHERED_INFO
│           ├── CLI_COMMAND_SYSTEM_BATCH_11_HELP.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_11_LOGIN.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_11_LOGOUT.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_11_LOGS.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_12_GOAL.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_12_MEMORY.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_12_STATS.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_12_WORKFLOWS.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_13_CONFIG.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_13_SETUP.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_13_USER_ID.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_13_WORKFLOW_ID.md
│           ├── CLI_COMMAND_SYSTEM_BATCH_14_TOOLS.md
│           ├── CLI_COMMAND_SYSTEM_PROGRESS_SUMMARY.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_anthropic-direct.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_claude-3-7-sonnet.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_claude-opus-4.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_claude-sonnet-4.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_gemini-2.5-pro.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_gemini-direct.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_gpt-4.1-mini.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_gpt-4.1-nano.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_litellm.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_lm-studio.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_local-llama-3.1-8b.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_openai-direct.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_19_requesty.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_aggregate_usage.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_application_settings_schema.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_cat_vibes_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_data_collection_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_default_provider_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_double_texting_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_favorite_model_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_mcp_servers.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_models_x_tools.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_providers_x_models.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_quick_launch_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_theme_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_tone_notification_app_settings.json.md
│           ├── CONFIGURATION_MANAGEMENT_BATCH_20_tool_performance.json.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_01_mao_v4.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_02_ui_terminal.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_agent_callback.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_agent_orchestrator.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_cli_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_conversation_bridge.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_error_handling.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_mcp_hub.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_memory_mcp.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_orchestrator_core.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_orchestrator_init.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_protocol.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_workflow_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_03_workflow_state.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_manager_buttons.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_manager_models.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_manager_tools.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_real_time_metrics.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_settings_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_system_analytics_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_user_analytics_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_user_memory_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_04_username_manager.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_05_cache_init.md
│           ├── CORE_SYSTEM_ARCHITECTURE_BATCH_05_cache_system.md
│           ├── CORE_SYSTEM_ARCHITECTURE_FOUNDATION_SUMMARY.md
│           ├── QA_AUDIT_RESULTS.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_cli_command.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_example-workflow_handoff_config.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_example-workflow_phase_config.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_example-workflow_workflow_config.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_model.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_provider.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_README.md.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_setting_name_app_settings.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_tool_config_template.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_tool.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_tool.py.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_ui_tool.py.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_22_user_username.json.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_config_documenter.py.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_install_mao_command.sh.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_install_ptree_command.sh.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_install_validator.sh.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_mao_validator.py.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_mao-validate.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_mao.sh.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_ptree.sh.md
│           ├── TEMPLATES_AND_SCRIPTS_BATCH_23_webhook_handler.py.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_BRAVE_BUTTON.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_BRAVE_CONFIG.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_BRAVE_SEARCH.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_BRAVE_UI.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_PERPLEXITY_BUTTON.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_PERPLEXITY_CONFIG.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_PERPLEXITY_SEARCH.md
│           ├── TOOLS_ECOSYSTEM_BATCH_06_PERPLEXITY_UI.md
│           ├── TOOLS_ECOSYSTEM_BATCH_07_WEB_BUTTON.md
│           ├── TOOLS_ECOSYSTEM_BATCH_07_WEB_CONFIG.md
│           ├── TOOLS_ECOSYSTEM_BATCH_07_WEB_SEARCH.md
│           ├── TOOLS_ECOSYSTEM_BATCH_07_WEB_UI.md
│           ├── TOOLS_ECOSYSTEM_BATCH_08_CONTENT_CREATION_COMPREHENSIVE.md
│           ├── TOOLS_ECOSYSTEM_BATCH_09_DEVELOPMENT_TOOLS_COMPREHENSIVE.md
│           ├── TOOLS_ECOSYSTEM_BATCH_10_SYSTEM_TOOLS_COMPREHENSIVE.md
│           ├── UI_TYPESCRIPT_INTEGRATION_CLI_BATCH_1.md
│           ├── UI_TYPESCRIPT_INTEGRATION_CLI_BATCH_2.md
│           ├── UI_TYPESCRIPT_INTEGRATION_SUMMARY.md
│           ├── UI_TYPESCRIPT_INTEGRATION_TOOLS_COMPREHENSIVE.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_chat.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_continue.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_dry_run.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_goal.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_help.md
│           ├── UI_TYPESCRIPT_INTEGRATION_ui_logs.md
│           └── UI_TYPESCRIPT_INTEGRATION_ui_terminal.md
├── index.md
├── interfaces
│   ├── ui_terminal.py
│   └── ui_web.py
├── mao_v4.py
├── orchestrator
│   ├── __init__.py
│   ├── agent_callback.py
│   ├── agent_orchestrator.py
│   ├── cache
│   │   ├── __init__.py
│   │   └── cache_system.py
│   ├── cli_manager.py
│   ├── conversation_bridge.py
│   ├── core.py
│   ├── error_handling.py
│   ├── manager_buttons.py
│   ├── manager_models.py
│   ├── manager_tools.py
│   ├── mcp_hub.py
│   ├── memory_mcp.py
│   ├── protocol.md
│   ├── real_time_metrics.py
│   ├── settings_manager.py
│   ├── system_analytics_manager.py
│   ├── user_analytics_manager.py
│   ├── user_memory_manager.py
│   ├── username_manager.py
│   ├── workflow_manager.py
│   └── workflow_state.py
├── README.md
├── scripts
│   ├── auto_docs
│   │   └── config_documenter.py
│   ├── github_integration
│   │   └── webhook_handler.py
│   ├── mao_launch_setup
│   │   ├── install_mao_command.sh
│   │   └── mao.sh
│   ├── project_tree
│   │   ├── install_ptree_command.sh
│   │   └── ptree.sh
│   ├── quality_validator
│   │   ├── aggressive_json_fixes_report.json
│   │   ├── cache_usage_audit_report.json
│   │   ├── cache_usage_audit.py
│   │   ├── designer_precision_fixes_report.json
│   │   ├── designer_precision_path_audit.json
│   │   ├── error_handling_audit_report.json
│   │   ├── error_handling_audit.py
│   │   ├── file_path_audit_precision.py
│   │   ├── file_path_audit_report.json
│   │   ├── file_path_audit_v2_designer_precision.py
│   │   ├── file_path_audit.py
│   │   ├── file_path_fixer_precision.py
│   │   ├── file_path_fixer_v3_designer_precision.py
│   │   ├── file_path_fixer.py
│   │   ├── file_path_fixes_report.json
│   │   ├── function_naming_audit_report.json
│   │   ├── function_naming_audit.py
│   │   ├── function_naming_perfection_report.json
│   │   ├── function_naming_perfector.py
│   │   ├── import_audit_precision.py
│   │   ├── import_audit_report.json
│   │   ├── import_audit.py
│   │   ├── import_fixer.py
│   │   ├── import_fixes_applied.json
│   │   ├── import_precision_audit_report.json
│   │   ├── install_import_tools.sh
│   │   ├── install_validator.sh
│   │   ├── json_config_audit_precision.py
│   │   ├── json_config_audit_report.json
│   │   ├── json_config_audit.py
│   │   ├── json_config_fixer_v2.py
│   │   ├── json_config_lexus_fixer.py
│   │   ├── json_config_normalization_report.json
│   │   ├── json_config_normalizer.py
│   │   ├── lexus_json_fixes_report.json
│   │   ├── mao_validator.py
│   │   ├── mao-validate
│   │   ├── quality_audit_dashboard.json
│   │   ├── quality_audit_results.json
│   │   ├── quality_audit_suite.py
│   │   ├── quality_validator_README.md
│   │   └── test_validator.sh
│   ├── token_counter
│   │   ├── install_standalone_token.sh
│   │   └── token_standalone.py
│   ├── unique_id_generator
│   │   ├── install_uid_command.sh
│   │   └── unique_id_generator.py
│   ├── user_id_generator
│   │   ├── install_meid_command.sh
│   │   └── user_id_generator.py
│   └── workflow_setup
│       ├── install-workflow-commands.sh
│       └── workflow_setup.sh
├── templates
│   ├── cli_commands
│   │   └── cli_command.json
│   ├── models
│   │   └── model.json
│   ├── providers
│   │   └── provider.json
│   ├── settings
│   │   └── setting_name_app_settings.json
│   ├── tools
│   │   ├── tool_config_template.json
│   │   ├── tool.json
│   │   ├── tool.py
│   │   └── ui_tool.py
│   ├── users
│   │   └── user_username.json
│   └── workflows
│       ├── example-workflow_handoff_config.json
│       ├── example-workflow_phase_config.json
│       ├── example-workflow_workflow_config.json
│       └── README.md
├── tools
│   ├── brave_search
│   │   ├── brave_search.py
│   │   ├── button_brave_search.py
│   │   ├── tool_brave_search.json
│   │   └── ui_brave_search.py
│   ├── code_execution
│   │   ├── button_code_execution.py
│   │   ├── code_execution.py
│   │   ├── tool_code_execution.json
│   │   └── ui_code_execution.py
│   ├── dalle_generate
│   │   ├── button_dalle_generate.py
│   │   ├── dalle_generate.py
│   │   ├── tool_dalle_generate.json
│   │   └── ui_dalle_generate.py
│   ├── file_operations
│   │   ├── button_file_operations.py
│   │   ├── file_operations.py
│   │   ├── tool_file_operations.json
│   │   └── ui_file_operations.py
│   ├── files_api
│   │   ├── button_files_api.py
│   │   ├── files_api.json
│   │   ├── files_api.py
│   │   ├── tool_files_api.json
│   │   └── ui_files_api.py
│   ├── graphic_design
│   │   ├── button_graphic_design.py
│   │   ├── fonts
│   │   │   ├── BebasNeue-Regular.ttf
│   │   │   ├── Georgia-Bold.ttf
│   │   │   ├── Georgia-Italic.ttf
│   │   │   ├── Georgia-Regular.ttf
│   │   │   ├── Montserrat-ExtraBold.ttf
│   │   │   ├── Montserrat-ExtraBoldItalic.ttf
│   │   │   ├── Montserrat-ExtraLight.ttf
│   │   │   ├── Montserrat-ExtraLightItalic.ttf
│   │   │   ├── Montserrat-Regular.ttf
│   │   │   ├── OpenSans-MediumItalic.ttf
│   │   │   ├── OpenSans-Regular.ttf
│   │   │   ├── PlayfairDisplay-Black.ttf
│   │   │   ├── PlayfairDisplay-BlackItalic.ttf
│   │   │   ├── PlayfairDisplay-Bold.ttf
│   │   │   ├── PlayfairDisplay-BoldItalic.ttf
│   │   │   ├── PlayfairDisplay-Italic.ttf
│   │   │   └── PlayfairDisplay-Regular.ttf
│   │   ├── graphic_design.py
│   │   ├── tool_graphic_design.json
│   │   └── ui_graphic_design.py
│   ├── mcp_connector
│   │   ├── button_mcp_connector.py
│   │   ├── mcp_connector.py
│   │   ├── tool_mcp_connector.json
│   │   └── ui_mcp_connector.py
│   ├── perplexity_search
│   │   ├── button_perplexity_search.py
│   │   ├── perplexity_search.py
│   │   ├── tool_perplexity_search.json
│   │   └── ui_perplexity_search.py
│   ├── text_editor
│   │   ├── button_text_editor.py
│   │   ├── text_editor.py
│   │   ├── tool_text_editor.json
│   │   └── ui_text_editor.py
│   ├── think
│   │   ├── button_think.py
│   │   ├── think.py
│   │   ├── tool_think.json
│   │   └── ui_think.py
│   └── web_search
│       ├── button_web_search.py
│       ├── tool_web_search.json
│       ├── ui_web_search.py
│       └── web_search.py
└── versioning
    ├── CHANGE_LOG.md
    ├── v1_8_3
    │   ├── sfa_decision_research_agent.py
    │   └── sfa_write_review_agent.py
    ├── v2_1_1
    │   ├── VARIABLE_INPUT_UPDATES.md
    │   └── WORKFLOW_ASSESSMENT.md
    ├── v3_0_0
    │   ├── 2025-05-02-UPDATES.md
    │   ├── BRANCH_FLOW_UPDATE_IMPLEMENTATION.md
    │   ├── branching_workflow.sh
    │   ├── FIRST_NEW_AGENT_TEST.md
    │   ├── original-workflow-diagram-v1.md
    │   ├── PHASE_ADJUSTMENT_UPDATE.md
    │   ├── setup-sfa-workflow.sh
    │   ├── sfa_v3_0_0_agent.py
    │   ├── sfa.orig
    │   └── TEST_RESULTS.md
    ├── v3_1_0
    │   ├── v3_1_0_IMAGE_EDITOR.md
    │   └── v3_1_1_ERRORS.md
    ├── v3_2_0
    │   ├── sfa_v3_2_0_agent.py
    │   └── v3_2_0_TOKEN_SAVING_EFFORTS.md
    ├── v3_2_1
    │   ├── v3_2_1_ERRORS.md
    │   └── v3_2_1_PATCH.md
    ├── v3_2_2
    │   ├── sfa_v3_2_2_main.py
    │   └── v3_2_2_UX_UPDATES.md
    ├── v3_3_0
    │   ├── fix_requesty.py
    │   ├── sfa_v3_3_0_main_updated.py
    │   ├── test_requesty_new.py
    │   ├── test_requesty.py
    │   ├── v3_3_0_REQUESTY_LLM_VARIABLE.md
    │   ├── v3_3_0_SETUP_SCRIPT_FIX.md
    │   └── v3_3_0_TESTING_SUMMARY.md
    ├── v3_3_1
    │   ├── sfa_v3_main.py
    │   ├── v3_3_1_CONVERT_TOOL_BACK.md
    │   └── v3_3_1_MODULAR_MODELS.md
    ├── v4_0_0
    │   ├── _LOOKING_AHEAD.md
    │   ├── _SELF_ENHANCEMENT.md
    │   ├── DEV_IMPL_UI
    │   │   ├── _DESIGN_RULES.md
    │   │   ├── _NEW_USER_FLOW.md
    │   │   ├── _VISUAL_BRAND_IDENTITY.md
    │   │   ├── about_claude_code_ui_dev
    │   │   │   ├── original_plexy_research_ts_node.md
    │   │   │   └── responsive_ts_nodejs_tips.md
    │   │   ├── og_ui_dev_flow
    │   │   │   ├── advanced_spec.md
    │   │   │   ├── CLI_AUTOCOMPLETE_IMPLEMENTATION.md
    │   │   │   ├── foundation_spec.md
    │   │   │   └── MAO_APP_UI_IMPLEMENTATION.md
    │   │   ├── TERMINAL_UI_RULES.md
    │   │   ├── UI_TECH_ARCHITECTURE.md
    │   │   └── wireframe_img
    │   │       ├── 01-mao-terminal-wireframes.html
    │   │       └── 02-mao-terminal-wireframes.html
    │   ├── IMPL_ANALYTICS_MEMORY
    │   │   ├── ANALYTICS_IMPL_SPEC_README.md
    │   │   └── MAO_MEMORY_ANALYTICS_IMPL_SPEC.md
    │   ├── IMPL_CLI_COMMANDS
    │   │   ├── AGENTIC_CLI_SETUP_README.md
    │   │   ├── CLI_COMMAND_STANDARDIZATION.md
    │   │   ├── cli_impl_volley_spec.md
    │   │   └── cli_volley_spec.md
    │   ├── IMPL_GITHUB_INTEGRATION
    │   │   └── GITHUB_INTEGRATION_SETUP.md
    │   ├── IMPL_WORKFLOW_SETUP
    │   │   ├── EXAMPLE_COMPLEX_WORKFLOW.md
    │   │   ├── IMPL_USER_CONFIG_SETUP_SCRIPT.md
    │   │   ├── IMPL_WORKFLOW_CREATION.md
    │   │   ├── INTEGRATION_POINTS_BY_FILE.md
    │   │   ├── USER_ID_CONFIG_SETUP.md
    │   │   └── WORKFLOW_ID_SETUP.md
    │   ├── NEXT_STEPS.md
    │   └── QUALITY_VALIDATOR_RESULTS
    │       ├── cache_usage_path_errors.md
    │       ├── continued_improvements.md
    │       ├── error_handling.md
    │       ├── quality_audit_suite.md
    │       └── using_quality_validator.md
    ├── v4_1_0
    │   ├── IMPL_ANALYTICS
    │   │   └── IMPL_ANALYTICS_ACCESSIBILITY.md
    │   ├── IMPL_CLAUDE_CODE
    │   │   ├── CLAUDE_CODE_SDK.md
    │   │   └── IMPL_CLAUDE_CODE.md
    │   ├── IMPL_MULTILINGUAL
    │   │   ├── IMPL_MULTILINGUAL.md
    │   │   └── TOOL_MULTILINGUAL.md
    │   ├── IMPL_MUST_UPDATES
    │   │   ├── MUST_UPDATES.md
    │   │   ├── TOOL_BASH.md
    │   │   └── TOOL_PARALLEL_USE.md
    │   ├── IMPL_REVIEW_DISCUSS
    │   │   ├── COUNT_MESSAGE_TOKENS.md
    │   │   ├── GOOGLE_SHEETS_ADD_ON.md
    │   │   ├── TOOL_COMPUTER_USE.md
    │   │   └── TOOL_FINE_GRAINED_STREAMING.md
    │   ├── IMPL_ROBUST_ANALYTICS
    │   │   └── DATA_COLLECTION_ARCHITECTURE.md
    │   ├── IMPL_SECURE_LOGIN
    │   │   ├── IMPL_SECURE_LOGIN.md
    │   │   └── secure_login_details.md
    │   ├── IMPL_TRIGGER_WORKFLOWS
    │   │   ├── IMPL_TRIGGER_WORKFLOWS.md
    │   │   └── timer_architecture.md
    │   └── IMPL_WEBSITE
    │       ├── IMPL_WEBSITE_STOREFRONT.md
    │       └── website-requirement.md
    └── vX_Future
        ├── TOOL_AIDER_MCP_SERVER.md
        ├── TOOL_BATCH_PROCESSING.md
        ├── TOOL_HOOKS.md
        ├── TOOL_OPENAI_AGENT_AS_TOOL.md
        ├── TOOL_PROGRAMMATIC_AIDER.md
        ├── TOOL_PROMPT_CHAIN.md
        ├── TOOL_XML_TAGGING.md
        ├── v4_EARTH_SYMPHONY.md
        └── v4_SFA_COLLAB.md
