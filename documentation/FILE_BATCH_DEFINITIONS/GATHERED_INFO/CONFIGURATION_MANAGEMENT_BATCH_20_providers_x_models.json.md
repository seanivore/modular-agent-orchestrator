# Configuration Management - providers_x_models.json

**File Location:** `/Users/seanivore/Development/modular-agent-orchestrator/configs/connections/providers_x_models.json`

## Simple Sentence Form

**Overview:** Provider-model relationship mappings define which providers support specific models, enabling dynamic provider selection, failover strategies, and optimal routing decisions for model access and availability management.

## Code & Explanation

**Architecture Overview:**
- **Provider-Model Compatibility Matrix:** Implements comprehensive mapping showing which providers support each model for dynamic provider selection and routing optimization
- **Multi-Provider Model Support:** Several models support multiple providers (openai/gpt-4.1-nano, local-llama-3.1-8b) enabling provider failover and optimization
- **Provider Specialization Recognition:** Maps provider strengths (Anthropic Direct for Claude models, Gemini Direct for Gemini models, Requesty for multi-model routing)
- **Dynamic Routing Foundation:** Enables intelligent provider selection based on model requirements, provider availability, and performance characteristics
- **Failover Strategy Support:** Multiple provider options for critical models ensuring reliable model access under various conditions

**Provider-Model Distribution:**
- **Anthropic Direct:** Exclusive provider for official Claude models (Sonnet 4, Opus 4, 3.7 Sonnet)
- **Requesty Router:** Multi-model support across providers enabling cost optimization and intelligent routing
- **Gemini Direct:** Dedicated provider for direct Google model access with free usage benefits
- **Local Providers:** LM Studio and LiteLLM supporting local model operation for privacy and cost efficiency

**Recommended Documentation Location:** `./docs/orchestration/provider-model-routing-architecture.md` for provider selection strategies and model availability optimization

## Written & Illustrated Data Info

**Data In-Flow:**
- Model access requests requiring provider compatibility validation and selection
- Provider availability assessment requiring model support capability verification
- Failover scenario handling requiring multi-provider model support validation
- Cost optimization requests needing provider comparison for specific model access

**Data Out-Flow:**
- Provider compatibility confirmation with model support validation
- Optimal provider recommendation based on model requirements and availability
- Failover provider options for reliable model access under various conditions
- Cost optimization guidance comparing provider options for specific models

**Key Configuration Elements:**
```json
{
  "models": {
    "claude-sonnet-4-20250514": {
      "providers": ["anthropic-direct"]
    },
    "openai/gpt-4.1-nano": {
      "providers": ["openai-direct", "requesty"]
    },
    "local-llama-3.1-8b": {
      "providers": ["lm-studio", "litellm"]
    }
  }
}
```

**Integration Points:**
- Provider selection systems use mappings for model availability and compatibility validation
- Routing optimization frameworks reference multi-provider options for intelligent selection
- Failover management systems implement backup provider strategies for reliable access
- Cost optimization systems compare provider options for budget-conscious model access

**Privacy and Local Storage Compliance:**
- Provider-model mappings stored locally ensuring user control over provider selection strategies
- Local provider options (LM Studio, LiteLLM) supporting privacy-focused model access
- User-controlled provider routing without external dependencies for mapping configuration
- Privacy-compliant provider selection supporting complete autonomy over model access patterns