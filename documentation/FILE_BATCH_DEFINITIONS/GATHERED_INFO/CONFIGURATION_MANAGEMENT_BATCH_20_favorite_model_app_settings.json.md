# Configuration Management - favorite_model_app_settings.json

**File Location:** `/Users/seanivore/Development/modular-agent-orchestrator/configs/settings/favorite_model_app_settings.json`

## Simple Sentence Form

**Overview:** Favorite model application settings manage default AI model preferences with dynamic discovery integration, comprehensive fallback options, and workflow-level override capabilities for intelligent model selection.

## Code & Explanation

**Architecture Overview:**
- **Dynamic Model Discovery:** Implements "dynamic_model_list" source enabling automatic detection of available models without hardcoded dependencies
- **Intelligent Default Selection:** Sets "claude-sonnet-4" as default providing optimal cost-performance balance for most workflows
- **Comprehensive Fallback Strategy:** Provides four-tier fallback hierarchy (Claude Sonnet 4 → Claude Opus 4 → Gemini 2.5 Pro → GPT-4.1 Mini) ensuring model availability
- **Workflow Override Capability:** Declares "can be changed per workflow" enabling dynamic model selection while maintaining user preference baseline
- **UI Navigation Integration:** Places in "Startup & Navigation" section with preview and help text emphasizing workflow flexibility

**Model Selection Strategy:**
- **Primary Choice:** Claude Sonnet 4 as default balancing advanced capabilities with cost efficiency
- **Premium Fallback:** Claude Opus 4 for complex reasoning tasks requiring advanced capabilities
- **Free Alternative:** Gemini 2.5 Pro for cost-sensitive workflows with large context requirements
- **OpenAI Option:** GPT-4.1 Mini for workflows requiring OpenAI-specific capabilities

**Recommended Documentation Location:** `./docs/models/model-selection-architecture.md` for favorite model management and dynamic selection optimization strategies

## Written & Illustrated Data Info

**Data In-Flow:**
- Model preference selection requiring dynamic model list integration
- Workflow initialization requests needing default model determination
- Fallback configuration validation ensuring reliable model availability
- Dynamic discovery updates requiring model availability refresh and validation

**Data Out-Flow:**
- Model preference confirmation with workflow override capability validation
- Dynamic model list integration status with current availability assessment
- Fallback chain validation ensuring reliable model access under all conditions
- Workflow flexibility confirmation supporting per-workflow model customization

**Key Configuration Elements:**
```json
{
  "favorite_model": {
    "default": "claude-sonnet-4",
    "source": "dynamic_model_list",
    "fallback_options": [
      "claude-sonnet-4",
      "claude-opus-4",
      "gemini-2.5-pro", 
      "gpt-4.1-mini"
    ],
    "help_text": "Default AI model for new workflows - can be changed per workflow"
  }
}
```

**Integration Points:**
- Model selection systems use dynamic discovery for current model availability
- Workflow initialization systems reference favorite model for default selection
- Fallback management implements hierarchical model selection for reliability
- Cost optimization frameworks consider favorite model preference for budget planning

**Privacy and Local Storage Compliance:**
- Model preferences stored locally ensuring user control over AI model selection
- Dynamic model discovery without external configuration dependencies
- User-autonomous model selection supporting workflow customization and cost optimization
- Local model preference management ensuring privacy-compliant AI model access configuration