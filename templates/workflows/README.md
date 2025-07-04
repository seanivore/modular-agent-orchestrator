# Workflow Creation Templates

This directory contains template files for creating new workflows using the 3-type JSON system.

## Quick Start

1. **Copy the template directory**:
   ```bash
   cp -r ./configs/examples/workflow_templates/example-workflow ./configs/workflows/.temp/your-workflow-name
   ```

2. **Edit the JSON files** in your temp directory:
   - `your-workflow-name_workflow_config.json` - High-level workflow definition
   - `your-workflow-name_phase_config.json` - Individual workflow phases  
   - `your-workflow-name_handoff_config.json` - Assessment and transition logic

3. **Run the setup script**:
   ```bash
   setup ./configs/workflows/.temp/your-workflow-name
   ```

## JSON Structure

### Workflow Config
- `custom_command`: What users type to run the workflow
- `workflow_id`: Generated automatically by `uid` script
- `user_id`: Generated automatically by `meid username` script
- `workflow_goal`: What this workflow accomplishes
- `workflow_deliverable`: What the user gets at the end

### Phase Config  
- `phase_number`: Sequential phase numbering (01, 02, 03...)
- `tools`: Array of MAO tools to use in this phase
- `models`: Primary, secondary, tertiary model choices
- `providers`: Primary, secondary, tertiary provider choices
- `resources`: Files, URLs, or data sources for this phase

### Handoff Config
- `assessment_questions`: How to evaluate if deliverable is complete
- `human_in_loop`: Whether human review is required

## Available Tools

Use any of these tools in your phase configs:
- `brave_search` - Privacy-focused web search
- `web_search` - Standard web search
- `perplexity_search` - AI-powered research
- `text_editor` - Content creation and editing
- `file_operations` - File management and organization
- `graphic_design` - Image editing and creation
- `dalle_generate` - AI image generation
- `code_execution` - Code running and development
- `files_api` - Workspace and draft management
- `mcp_connector` - External tool integration
- `think` - AI reasoning and planning

## Available Models

- `claude-sonnet-4` - Most capable Claude model
- `claude-opus-4` - Advanced reasoning
- `claude-sonnet-3.7` - Balanced performance  
- `gemini-2.5-pro` - Google's advanced model
- `gpt-4.1-mini` - OpenAI efficiency model
- `local-llama-3.1-8b` - Local model option

## Available Providers

- `anthropic-direct` - Direct Anthropic API
- `requesty` - Multi-provider routing
- `gemini-direct` - Direct Google API
- `openai-direct` - Direct OpenAI API
- `litellm` - Provider abstraction layer
- `lm-studio` - Local model serving

---

*Copy templates, customize for your use case, run setup - that's it!*
