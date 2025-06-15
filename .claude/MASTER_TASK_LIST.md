# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)

|----------------------|
| **SESSION 17 TASKS** |
| -------------------- |



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





## Technical Documentation Overhaul 

- Documentation is trying too hard and the result is a mess 
- Make it simple and easy understand 
- Comprehensive to clearly identify remaining work 
- Serve dual purpose of creating a roadmap for the final stretch of the build

1. Start fresh with simple, clear structure
2. Use docs process to identify final build tasks
3. Create clean roadmap for completion

## Final Build Tasks (identified during documentation overhaul)
- Whatever we discover during documentation review
- Integrate sections and notes from below 

```
/Development/modular-agent-orchestrator/
├── configs
│   ├── connections
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
│   └── providers
│       ├── anthropic-direct.json
│       ├── gemini-direct.json
│       ├── litellm.json
│       ├── lm-studio.json
│       ├── openai-direct.json
│       └── requesty.json
├── interfaces
│   ├── ui_terminal.py
│   └── ui_web.py
├── Mao_v4.py
├── orchestrator
│   ├── cache
│   │   ├── __init__.py
│   │   └── cache_system.py
│   ├── core.py
│   ├── error_handling.py
│   ├── manager_buttons.py
│   ├── manager_models.py
│   ├── manager_tools.py
│   ├── memory.py
│   └── protocol.md
├── tests
├── tools
│   ├── brave_search
│   │   ├── brave_search.py
│   │   ├── button_brave_search.py
│   │   ├── tool_brave_search.json
│   │   └── ui_brave_search.py
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
│   ├── graphic_design
│   │   ├── button_graphic_design.py
│   │   ├── fonts
│   │   ├── graphic_design.py
│   │   ├── tool_graphic_design.json
│   │   └── ui_graphic_design.py
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
└── versioning-docs
    ├── CHANGE_LOG.md
    ├── technical-documentation
    │   ├── OLD
    │   │   ├── 1.1_MEET_Mao.md
    │   │   ├── 1.2_SOLVING_PROBLEMS.md
    │   │   ├── 1.3_VARIABLE_INPUT.md
    │   │   ├── 2.1_ORCHESTRATOR.md
    │   │   ├── 2.2_AGENT_ROLE.md
    │   │   ├── 2.3_TOOL_IMPLEMENTATION_GUIDE.md
    │   │   ├── 3.1_BEHAVIOR.md
    │   │   ├── 3.1_USE_CASE_SETUP.md
    │   │   ├── 3.2_EXECUTE_USE_CASE.md
    │   │   ├── 3.2_SPAWN.md
    │   │   ├── 3.3_ORCHESTRATION.md
    │   │   ├── 3.4_WORKFLOW_MANAGEMENT.md
    │   │   ├── 4.1_FINGERPRINTING.md
    │   │   ├── 4.2_RESOURCE_EFFICIENCY.md
    │   │   ├── 5.1_RUNNING_ESTABLISHED_WORKFLOWS.md
    │   │   ├── 5.2_WORKFLOW_MONITOR.md
    │   │   ├── 5.3_WORKFLOW_REPORT.md
    │   │   └── 5.5_ERROR_HANDLING.md
    │   └── OTHER-DOCS-TO-REVIEW-INCLUDE
    │       ├── UPDATE_SPEC.md
    │       └── WORKFLOW_PROJECT.md
    └── v1-3_SFA
```

-----------------

|----------------------|
| **SESSION 18 TASKS** |
| -------------------- |

# Final Build Tasks (Unless they fit below)

## MCP API Connector 

Recent release by Anthropic that should be added before completion. 

**Model Context Protocol Server API Connector:** 
`/Users/seanivore/Development/modular-agent-orchestrator/.claude/TOOL_API_MCP_CONNECT.md` 

## Orchestrator Specific Tools Required 

  1. Code Execution: `/Users/seanivore/Development/modular-agent-orchestrator/.claude/TOOL_CODE_EXECUTION.md` 
  2. Files API: `/Users/seanivore/Development/modular-agent-orchestrator/.claude/TOOL_FILES_API.md` 

### Tool Discovery 

The file that was called 'tool_discovery' now called `manager_tools.py` needs to be connected to `core.py` 

### Protocol Document 

Create `protocol.md` for Mao behavior. 

-----------------

|----------------------|
| **SESSION 19 TASKS** |
| -------------------- |

# Create User Experience Flow 

**This is what we're missing still:**

```
First Time: Goal → Mao Setup → JSON Config → Custom Command → Ready!
Later: Custom Command → Workflow Execution → Results
```

- First time setup UX
- Workflow execution UX
- Clear path: 
  1. "I have a goal" 
  2. "I have a working workflow" 
  3. "I can run this anytime."

## Tools for Workflow Setup 

### JSON Variable-Input Config File 

Decide what JSON Config looks like: 

  1. New variables needed 
     - Must answer variables 
     - Optional variables (because Mao will decide)
  2. Old variables carried over 
  3. Set up the use-case directory `./configs/use_case/*/...`

### Setup Script 

  1. Delete the old `sfa` command 
  2. What args can we think of being handy this time 
  3. Creates USE_CASE_README.md in the use-case's directory 
     - Summarizes the project
     - Explains each task 
     - Estimated cost, etc. 
     - Command to execute 
  4. File: `./config/setup_scripts/setup_workflow.py`
     - Processes JSON config 
     - Creates custom command
  5. Unlike example directly below, make sure no hyphens in command 
     - First word of command is actual command 
     - Rest are args 
     - So that the UX is just like other terminal commands, e.g. git, etc. 

```bash
# What this creates
sfa my-research-workflow
sfa my-content-creation
sfa my-data-analysis
```

### Test 

Generated command should execute the workflow. 

## Create Setup Entry Point

- File: `/Mao_v4_setup.py`
- What: Main script that determines setup vs run mode
- Simple Explanation: Smart entry point that knows if you're setting up or running

```python
# What we're building
def main():
    if is_first_time_or_setup_requested():
        launch_Mao_setup_conversation()
    else:
        run_existing_workflow()
```

### Test 

`python Mao_v4_setup.py` should start Mao conversation for new users

## Build Mao Setup Conversation

- File: `./build/interfaces/setup_conversation.py`
- What: Mao interviews user and creates JSON workflow config
- Simple Explanation: Friendly chat with OC that turns your goal into a workflow

- Flow:
  1. Mao asks about your goal
  2. Mao suggests tools and models
  3. Mao creates JSON config
  4. Mao explains what will happen

### Test

- Conversation should produce valid JSON workflow config

-----------------

|----------------------|
| **SESSION 20 TASKS** |
| -------------------- |

# Testing & Validation 

Comprehensive testing of the complete system from setup through execution.

## Test complete first-time user experience

Pretend to be a new user and go through the whole process. 

**Test Scenarios**
  - New user with research goal
  - New user with content creation goal
  - New user with data analysis goal

**Success Criteria**: Each should result in working custom command

## Workflow Execution Testing 

Test that generated workflows actually work, running custom commands. 

**Test Scenarios**:
  - Simple single-tool workflows
  - Complex multi-tool workflows
  - Workflows with different models

**Success Criteria**: All workflows execute and return expected results

## Snippet Button Integration Testing

Test that "human" buttons work with Claude 4 Code Execution. 

**Test Scenarios**:
  - Different models (Anthropic, OpenAI, Gemini)
  - Different tools (search, text, image)
  - Error handling and retries

**Success Criteria**: Buttons generate valid code that executes successfully

## Performance & Cost Validation

Verify 95% token reduction and cost optimization to make sure efficiency claims are real; update claims if needed. 

**Metrics**:
  - Token usage vs v3.3.0
  - Cost per workflow execution
  - Cache hit rates
  - Model selection optimization

**Success Criteria**: Maintain <$0.01 per workflow execution

### Verbose Output UI

Noted down that we never tested this earlier. Will need to test all UI anyway. 