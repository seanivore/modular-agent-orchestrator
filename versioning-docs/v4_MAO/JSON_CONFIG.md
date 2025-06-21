# JSON Config File 

## New Needs, Old Needs 

1. User ID 
2. Workflow ID 
3. Model, fallback model, fail-safe model 
4. Provider, fallback provider, fail-safe provider 
5. Deliverable 

## Found Example 

### JSON Config Schema

```json
{
  "workflow_id": "uid-qmt-465",
  "custom_command": "marketing strategy startup",
  "goal": "Create comprehensive marketing strategy for fintech startup",
  "phases": [
    {
      "name": "market_research",
      "description": "Research target market and competitors",
      "tools": ["web_search", "text_editor"],
      "deliverable": "Market research report",
      "model": "claude-sonnet-4"
    },
    {
      "name": "strategy_development", 
      "description": "Develop marketing strategy and tactics",
      "tools": ["text_editor", "graphic_design"],
      "deliverable": "Marketing strategy document",
      "model": "claude-sonnet-4"
    }
  ],
  "variables": {
    "required": {
      "target_market": {               <-- Not modular appropriate 
        "description": "Primary target market segment",
        "example": "small business owners"
      }
    },
    "optional": {
      "budget": {
        "description": "Marketing budget constraint",
        "default": "not specified"
      }
    }
  }
}
```