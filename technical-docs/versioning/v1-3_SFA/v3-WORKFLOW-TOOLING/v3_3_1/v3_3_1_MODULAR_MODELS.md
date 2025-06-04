# Model & Provider Configuration System 
v3.3.1 (Patch Update - Model Configuration)

Now that we have different models, we need to adjust some of the calculations and warning systems to accommodate things like 1M token context windows, free models, and output limit warnings. In retrospect, this is how things should have been done from the start. 

Since all of the models we come across either use Anthropic or OpenAI API keys, we can even make the "PROVIDER" a variable in the config file. That means for now we can just list any Requesty models we're going to use and the display and limits will be handled properly, and in the future, as long as the provider uses OpenAI API endpoints, like most of them do, LM Studio and LiteLLM, will all work automatically. We'll have a PROVIDER CONFIGURATION SYSTEM along with the MODEL CONFIGURATION SYSTEM. 

## Modular Configuration System  
Set up variables just like we do with the JSON configuration files. 

### `/models/model-config.json`
```json
{
  "models": {
    "claude-3-7-sonnet-20250219": {
      "provider": "anthropic",
      "context_window": 200000,
      "max_output": 64000,
      "max_output_beta": 128000,
      "vision": false,
      "caching": true,
      "tools": true,
      "input_price_per_million": 3.00,
      "output_price_per_million": 15.00,
      "safe_token_limit": 7000
    },
    "google/gemini-2.5-pro-exp-03-25": {
      "provider": "requesty",
      "context_window": 1048576,
      "max_output": 65536,
      "vision": false,
      "caching": false,
      "tools": false,
      "input_price_per_million": 0.00,
      "output_price_per_million": 0.00,
      "safe_token_limit": 30000
    },
    "anthropic/claude-3-7-sonnet-latest": {
      "provider": "requesty",
      "context_window": 200000,
      "max_output": 64000,
      "max_output_beta": 128000,
      "vision": false,
      "caching": true,
      "tools": true,
      "input_price_per_million": 3.00,
      "output_price_per_million": 15.00,
      "safe_token_limit": 7000
    }
  }
}
```

### Benefits of This Approach:
1. **Easy Updates**: Add new models without code changes
2. **Dynamic Token Limits**: Each model can have its own safe limits
3. **Accurate Cost Tracking**: Model-specific pricing
4. **Feature Detection**: Know which models support caching, tools, vision
5. **Future-Proof**: Ready for new models and capability changes

### Implementation in v3.3.1:
```python
def load_model_config():
    """Load model configuration from JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), "models", "model-config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {"models": {}}

def get_model_info(model_name):
    """Get model configuration info."""
    model_config = load_model_config()
    return model_config["models"].get(model_name, {
        "context_window": 200000,
        "max_output": 64000,
        "safe_token_limit": 7000,
        "input_price_per_million": 3.00,
        "output_price_per_million": 15.00
    })
```

----

## API for Provider Configuration

- **OpenAI**: `https://api.openai.com/v1` + OpenAI API key
- **Requesty**: `https://router.requesty.ai/v1` + Requesty API key  
- **LM Studio**: `http://localhost:1234/v1` + any/no API key
- **LiteLLM**: `http://localhost:4000/v1` + LiteLLM API key

## Expanded Model Configuration

We could definitely expand the model config to include full provider details:

```json
{
  "providers": {
    "anthropic-direct": {
      "api_type": "anthropic",
      "base_url": "https://api.anthropic.com",
      "auth_header": "x-api-key",
      "env_var": "ANTHROPIC_API_KEY"
    },
    "requesty": {
      "api_type": "openai",
      "base_url": "https://router.requesty.ai/v1",
      "auth_header": "authorization",
      "env_var": "ROUTER_API_KEY"
    },
    "lm-studio": {
      "api_type": "openai",
      "base_url": "http://localhost:1234/v1",
      "auth_header": null,
      "env_var": null
    },
    "litellm": {
      "api_type": "openai", 
      "base_url": "http://localhost:4000/v1",
      "auth_header": "authorization",
      "env_var": "LITELLM_API_KEY"
    }
  },
  "models": {
    "claude-3-7-sonnet-20250219": {
      "provider": "anthropic-direct",
      "model_id": "claude-3-7-sonnet-20250219",
      "context_window": 200000,
      // ... other specs
    },
    "google/gemini-2.5-pro-exp-03-25": {
      "provider": "requesty",
      "model_id": "google/gemini-2.5-pro-exp-03-25",
      "context_window": 1048576,
      // ... other specs
    },
    "local-llama": {
      "provider": "lm-studio",
      "model_id": "llama-3.1-8b-instruct",
      "context_window": 128000,
      "input_price_per_million": 0.00,
      "output_price_per_million": 0.00
    }
  }
}
```

## Implementation Strategy

This would let us create a completely generic LLM client:

```python
def create_client(provider_config):
    """Create appropriate client based on provider config."""
    if provider_config["api_type"] == "anthropic":
        return Anthropic(api_key=os.getenv(provider_config["env_var"]))
    elif provider_config["api_type"] == "openai":
        import openai
        client_args = {
            "base_url": provider_config["base_url"]
        }
        if provider_config["env_var"]:
            client_args["api_key"] = os.getenv(provider_config["env_var"])
        return openai.OpenAI(**client_args)

def get_client_for_model(model_name):
    """Get the appropriate client for a model."""
    model_config = get_model_info(model_name)
    provider_config = get_provider_info(model_config["provider"])
    return create_client(provider_config)
```

## The Beauty of This Approach

With this system, you could:
- Add any OpenAI-compatible provider instantly
- Support local LLMs through LM Studio
- Route through LiteLLM to access dozens of providers
- Even support multiple API keys for the same provider
- Easily switch between local and cloud models

You're absolutely right that this makes the system incredibly modular and future-proof!

## Roadmap Suggestion

- **v3.3.0**: Basic Requesty integration (current plan)
- **v3.3.1**: Model configuration JSON
- **v3.3.2**: Full provider configuration system

This third update would make SFA into a truly universal LLM agent system that could work with virtually any provider. Pretty exciting possibility!