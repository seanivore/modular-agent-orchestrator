1. In the documentation file there is an arg that uses specifics: 

```bash 
    parser.add_argument("--job-app", help="Job application workflow")
```

This document: `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/2_MAO_ARCHITECTURE.md`

I'm not again having them but we shouldn't have this kind of thing in the documentation unless we have a modular way of implementing them. 

2. Is this dated? What is "OC" 

**3. Request Routing**
- Stats requests → `oc.get_stats()`
- Workflow listing → `oc.list_workflows()`
- Job applications → `oc.job_application_workflow()`
- General goals → `oc.execute_goal()`
- Interactive mode → Input loop with continuous execution

I ask because we were calling the product "OC" before "Mao". 

3. The Model and the Provider should not be hard coded on each other 

```json 
  "id": "claude-sonnet-4",
  "display_name": "Claude Sonnet 4",
  "provider": "anthropic-direct",
```

We have these connector files for that reason. This keeps the individual files modular and when adding a new tool there is less to update. 

`./configs/connections/models_x_tools.json`
`./configs/connections/providers_x_models.json`

This happens again lower on the page under this section: 

"## 📁 Configuration System (`configs/`)" 

We should also just mention the connector pages there --- okay I just came across the connector mention at the bottom of the page but I'm confused and can't tell if it is mentioned for the right reason given the hardcoding on each other config above. 

4. These snippets don't exist on any files. 

**`coordinate_agents(agents: List[Agent]) -> Dict`**

**`get_model_cost_estimate(model: str, tokens: int) -> float`**

**`validate_model_capability(model: str, required_caps: List) -> bool`**

**`create_workflow_button(workflow_plan: WorkflowPlan, model: str) -> str`**

**`create_tool_button(tool_name: str, params: Dict, model: str) -> str`**

**`validate_button_execution(snippet: str) -> Dict`**


`def adapt_for_model(self, base_snippet: str, target_model: str) -> str:`

**`discover_available_tools() -> Dict[str, ToolConfig]`**

**`select_tools_for_task(task_description: str, available_models: List) -> List[str]`**

**`get_tool_metadata(tool_name: str) -> Dict`**

`def display_workflow_progress(self, phases: List[WorkflowPhase], current: int):`

`def display_cost_monitoring(self, budget: float, used: float, projected: float):`

`def display_success_summary(self, workspace: str, total_cost: float):`

5. This one only exists on the manager_buttons.py file itself. 

`class ButtonManager:`

Is that accurate? 

Found on this document: `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/2_MAO_ARCHITECTURE.md` 

6. These file names don't exist in the codebase. 

#### Current Provider Ecosystem
- **anthropic-direct.json** - Direct Anthropic API access
- **openai-direct.json** - Direct OpenAI API access
- **gemini-direct.json** - Direct Google Gemini access
- **litellm.json** - Universal LLM proxy service
- **lm-studio.json** - Local model deployment
- **requesty.json** - Universal OpenAI-compatible proxy

7. We need to stop calling it "Standardized 4-file architecture" 

It is a "Standardized 6-file architecture"

See new tree added at bottom of file, but there are two files that are shared. 

Found on this document: `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/technical-documentation/2_MAO_ARCHITECTURE.md` 
