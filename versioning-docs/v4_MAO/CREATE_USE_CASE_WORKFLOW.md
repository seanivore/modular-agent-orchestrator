# Setting Up A New Workflow Use-Case 

Creating this as one flow document because it feels like this is all missing from the technical documentation in any clear way. 

## Updates And Where To Put Them 
1. User ID 
   - Created a new cli JSON 
   - Created a template JSON in the examples directory here `./configs/examples/cli_command.json` 


## User ID and Workflow ID 

**User ID**
  - Using Mao app, use a 6-20 alpha-numeric username; it will always generate the same User ID 
  - Every JSON object you create will need this same generated number 
  - Run the `meid` command with your Username to get your User ID
  - Keeps all of the use-cases you've created and each workflow you've ran together and easy to look up 
  - Always results in the same 'user-0000' --> the examples below is `user-0663` 
  - Run the --workflow command followed by your User ID to see all of your workflows 

```bash 
meid whoami 
mao --workflow whoami 
```
```zsh
> /meid whoami
> /workflow whoami 
```

**Workflow ID**
  - When you create a workflow alone or with Mao's help, the JSON object will need a workflow ID 
  - Run the `uid` command to get a collision-free (never repeated) unique ID --> `uid-abc-000` 
  - Follow --workflow command with this ID for that workflow's details; custom command might be easier to remember 

```bash 
uid 
mao --workflow uid-abc-000
```
```zsh
> /uid 
> /workflow uid-abc-000 
```


## New Needs, Old Needs 

1. User ID 
2. Workflow ID 
3. Model, fallback model, fail-safe model 
4. Provider, fallback provider, fail-safe provider 
5. Deliverable 
6. Resources (paths, URLs, etc.)
7. custom command 
8. goal 
9. phase_name
10. description 
11. tools 
12. model 
13. provider 

## Found Example 

### JSON Config Schema

```json
{
  "workflow_id": "uid-qmt-465",
  "custom_command": "marketing strategy startup",
  "goal": "Create comprehensive marketing strategy for fintech startup",
  "phases": [
    {
      "phase_name": "market_research",
      "description": "Research target market and competitors",
      "tools": ["web_search", "text_editor"],
      "deliverable": "Market research report",
      "model_1": "claude-sonnet-4",
      "model_1": "claude-sonnet-3.7",
      "model_1": "claude-sonnet-3.5",
      "provider": "anthropic direct"
    }
  ]
  }
}
```