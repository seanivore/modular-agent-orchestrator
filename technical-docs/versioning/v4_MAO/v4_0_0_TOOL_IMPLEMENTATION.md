# Agent Tool Implementation Plan

## Updated UI for New UX 

Tooling needs have been updated for our orchestrator-based system because of the new process, from setting up a new workflow, through to the workflows completion. Let's break it down to understand the changes you'll see. 

### Benefits

- UI swappable (terminal → web → API)
- Tools testable without UI dependencies  
- Human buttons portable across interfaces
- Cache shared between all tools
- Add new models: Edit JSON, instant support
- No SDK hell: Code snippets handle everything
- Cost optimization: Automatic best model selection
- User-editable: Change protocol.md to modify behavior 
- Tool discovery: Dynamic tool loading 
- Code execution: Execute code snippets directly 
- Parallel execution: Run tools in parallel 
- Extended thinking: Think while coordinating 
- Memory files: Save workflow state 


### Use-Case Development, Configuration Setup, & Workflow Activation  

#### Use-Case Development Setup  

Because we have an orchestrator, setup of workflows is done with the AI orchestrator to ensure the workflow is created correctly and understood. 

1. User runs a 'Workflow Development' agent that calls Claude 4, our workflow orchestrator 
2. Initially, the user comes prepared with the sections of the JSON config ready, in notes 
3. User provides the notes and describes the project's tasks they need to complete 
4. The orchestrator and User back-and-forth until there is an understanding and the most effective workflow has been created 
5. The orchestrator will then create the complete JSON config file 
6. The orchestrator will run the config file with the setup script for the use-case 
7. The orchestrator will then return the workflow to the user in the form of a README.me that contains the custom commands needed to run the workflow, as well as any other specifics like where to place input resource files or where to expect output completed file. 
8. After this first development session, User can run the workflow whenever they need 

#### Workflow Process 

1. User runs workflow command 
2. Orchestrator starts the workflow 
   - They gather information needed for the fist task 
   - OC calls the first agent 
   - OC records progress notes in their log 
   - OC commits all necessary conversation history, task information, etc. to their 'memory.py' file to maintain context when they are called back in after the first agent has completed their task 
3. Handoff of task to first agent which includes: 
   - Auto-save feature document
   - Live document token counter
   - Reminder of their token limit 
   - 'Human button' snippets to run for any tool use they may need 
   - 'Human button' snippet to run to call the orchestrator when complete (or to handle any other issues they may have)
4. Agent works on and completes their task 
5. Agent calls the OC when finished to hand in their work 
   - Communicates directly their task report 
   - Orchestrator records that report in the log for their workflow report  
   - Agent hands over any deliverables 
   - Orchestrator uses the Anthropic Files API to save draft deliverables  
   - If ever they needed more time or to fix something, the orchestrator can reset the loops to allow the agent to stay in the context and finish the task 
6. Orchestrator coordinates the next agent in the workflow 
...
This continues until the workflow is complete. 

#### Workflow Completion Observations 

- Note that only 'human button' snippets are handed off to agents. 
This allows us to work with LLMs from any provider and require nothing more than the API call to summon the LLM. 

- The orchestrator connects directory with the agent before and after they work on their task. 
This allows us to remove any need for tools that are purely logistical. It also means that there is no need for agents to "save_output" or any other function that would previously have triggered the end of a task phase. 

- The orchestrator is the only one that can save files. 
This is because the orchestrator is the only one that has access to the Anthropic Files API, which is being leveraged because it is free. When the final document is complete, then the OC will save the final version of the document to the user's directory. 

- The agents are provided the same functional convenience in their document tools as humans expect. 
They have auto-save, this prevents the need for them to save their output. And they have a token counter, this prevents the need for them to worry about their token when completing the task. When they received their task, a token limit for that specific LLM or limit as dictated by the Use-Case, is provided. No need to check tokens with a special tool to exit. 

**In this way, most of the complexity of our prior workflows that were needed to automated job completion or track deliverables, or count tokens, all of it has been removed. The workflows will be able to get incredible complex with many possible branches, and could even span across multiple days of work, but the process is simpler. There is something magical about that.** 

## Implementation Overview 

1. We have new code for each tool and we pulled the code for each tool from the old SFA; these are both in the same file with new on top of old. 
2. We need to organize the code into the different files that are needed for our new modular system. 
3. Review the document plan as a whole and provide any feedback or suggestions if needed. 
4. Write any missing code, clean up any code that is not needed or that doesn't fit the new system, strive for simplicity and efficiency. 

### Variable-Input Agent Philosophy 

It is important to remember our very specific goals for the agent when building these tool files. The tool needs to be completely void of all specifics. Making Use-Case groups for an agent built without use-cases is flawed logic that would impose creative control on users. 

We'll be fixing two instances where this philosophy was not followed. The last time we tried to implement the tools, many hard-coded use-cases were added to the code and we had to revert to a previous state using git. These are tip they advises I add to help us and the AI avoid this happening again. 

We don't want to guess at or try to create pre-fab templates for different types of research, methods of thinking, or even for data analysis intentions. Only information here is what tools DO. We don't presume what they will be used for. This information will wholly be added via the prompts. 

It is possible down the line we might want categories and themes that help common use-cases, but when we do, we will implement that in a modular way. 

- Individual tools, not a rigid toolkit
- No theme groupings for a variable input agent
- No hardcoded options 
- Tools return structured data, not predetermined choices 
- No enum parameters for 'analysis_type' or 'framework_type' 
- No predetermined workflows 
- No 'choose your approach' menus 
- No template types  
- Tools should be blank canvases 

> If there are pre-fab helpers you think we need, please let me know. I would like to consider this in a later update using a more modular approach. 

## Tool Architecture Files 

**Tool Registry & Definitions** 
  - INDIVIDUAL TOOLS: `./sfa-v4/configs/tool_registry/tool_tool_name.json`
  - TOOLS X MODELS: `./sfa-v4/configs/model_tool.json`

**Clean, Light-Weight Logic Functions Tool Files** 
  - INDIVIDUAL TOOLS: `./sfa-v4/tools/tool_name.py`

**Tool UI Functions**
  - INDIVIDUAL TOOLS: `./sfa-v4/interfaces/ui_tool_name.py`
  - MASTER FILE: `./sfa-v4/interfaces/terminal.py`

**Human Button Tool Functions**
  - INDIVIDUAL TOOLS: `./sfa-v4/utilities/button_tool_name.py` 
  - MASTER FILE: `./sfa-v4/orchestrator/human_buttons.py`

**Shared Error Handling Utility** 
  - MAIN FILE: `./sfa-v4/utilities/error_handling.py`

**Tool Caching System**
  - MAIN FILE: `./sfa-v4/utilities/cache_tools_name.py`

**Tool Discovery Functions**
  - MAIN FILE: `./sfa-v4/orchestrator/tool_discovery.py`
  - Passes along the information to `/orchestrator/core.py` 

**Orchestrator (OC) Behavior Protocol**
  - MAIN FILE: `./sfa-v4/orchestrator/protocol.md`


### Tool Registry & Definition  
1. Define what the tool JSON config file includes 
2. Create the tool JSON config file for each tool 
3. Add them all to the `tool_registry` directory 
4. Create single `model_tool.json` file that matches all models to tools 
   - Metadata only
   - Tags should define what it does 
   - Do not presume use-case tags like 'finance' or 'marketing'
   - Do not hardcode models into the tool registry here 
   - This ensures it is up to date 
   - With every tool or model change 
   - Without having to change multiple files

### Clean, Light-Weight Logic Functions Tool Files 
1. All of these tool files should be in `./sfa-v4/tools/` directory 
2. Simply name each file by the name of the tool, `tool_name.py`
   - Pure tool logic files 
   - Return structured data 
3. The bottom of the files have code from the old SFA, from that we want to pull: 
   - "Good error handling" 
   - "Token validation" 
   - "Tool result processing patterns" 
4. Review the rest of the tool file to ensure you know what other parts of the tool code is to be separated 
5. Use the following header to keep consistent 

  """
  Brave Web Search Tool
  Independent web search using Brave Search API with enhanced error handling
  """

### Tool UI Functions
1. All tools have their own UI file 
2. All print functions for interface layer
3. This includes all print() statements 
4. Terminal display formatting
   - Take structured data → pretty terminal output
   - Progress indicators, colors, tables
5. Name them `ui_tool_name.py`
6. Place them all in this directory: `./sfa-v4/interfaces/ui_tools/`
7. Use the following header to keep consistent 

  """
  BRAVE SEARCH TOOL
  UI Display Component
  """

### Human Button Tool Functions
1. All human button tool files are in the `./sfa-v4/utilities/human_button_tools` directory 
2. Name them `button_tool_name.py`
3. `create_human_button_snippet()` functions
4. Code generation for Claude 4 execution
5. Master file is `./sfa-v4/orchestrator/human_buttons.py`
6. Use the following header to keep consistent 

  """
  FILE OPERATIONS TOOL 
  Human Button Generators
  """

```python
def create_human_button_snippet(params: Dict, model: str) -> str:
    """Generate executable code snippet for this tool"""
    # Return self-contained Python code that:
    # 1. Imports necessary libraries
    # 2. Executes the tool functionality  
    # 3. Handles errors gracefully
    # 4. Returns results in standard format
```
The snippet on implementation plan is a bit different. 

```python
class HumanButtonInterface:
    def create_api_call_snippet(self, model_name: str, prompt: str) -> str:
        # Generate executable code for ANY model/provider combo
        # No SDK knowledge needed - just run the snippet!
    
    def create_tool_call_snippet(self, model_name: str, tool_name: str, params: dict) -> str:
        # Generate tool execution snippets
```

And then also this. "Code Execution Tool (THE GAME CHANGER)"

```python
# Instead of complex SDK management:
async def execute_model_call(snippet: str) -> dict:
    # Claude 4 executes the snippet directly!
    result = await anthropic_client.beta.messages.create(
        model="claude-sonnet-4",
        tools=[{"type": "code_execution_20241022", "name": "execute"}],
        messages=[{"role": "user", "content": f"Execute: {snippet}"}]
    )
    return parse_execution_result(result)
```

### Shared Error Handling Utility  
`./sfa-v4/utilities/`
1. Create a new file called `error_handling.py` 
2. Place it in the `utilities` directory 
3. Use the following header to keep consistent 
4. This is a space for all of the error handling that is repeated across many or all of the tools. 

  """
  ERROR HANDLING UTILITY
  Shared error handling for all tools
  """

### Tool Caching System
1. Create a new file called `cache_tools_name.py` 
2. Place it in the `./sfa-v4/utilities/cache_tools/` directory 
3. Master file is `./sfa-v4/orchestrator/hybrid_cache.py`
4. Use the following header to keep consistent 
   - Tools are cached forever
   - Using fingerprinting 
   - Avoids re-downloading 
   - This is a system that needs to be updated

  """
  CACHE TOOLS
  Tool caching system
  """

### Tool Discovery Functions
1. Create a new file called `tool_discovery.py` 
2. Place it in the `./sfa-v4/orchestrator/` directory 
3. Master file is `./sfa-v4/orchestrator/tool_discovery.py`
4. Use the following header to keep consistent 
5. Passes along the information to `/orchestrator/core.py` 

  """
  TOOL DISCOVERY
  Tool discovery system
  """

### Orchestrator (OC) Behavior Protocol 
1. File is created here: `./sfa-v4/orchestrator/protocol.md`
1. This is the protocol for the orchestrator 
2. In a markdown so that we can edit it easily 
3. Likely passed along to `/orchestrator/core.py`
4. Based on the tools and process and whatever else needs to go in here regarding flow and protocol 


## Current Tools 

### Brave Web Search Tool (`brave_search.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/brave_search.py`
- Independent, privacy-focused search
- News search, local search
- Alternative to mainstream search engines

### DALL-E Image Generation Tool (`dalle_generate.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/dalle_generate.py`
- AI-powered image generation 
- Using OpenAI's Latest DALL-E Model
- Professional workflow, error recovery

### File Operations Tool (`file_operations.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/file_operations.py`
- `read_file`, `read_multiple_files`, `list_directory`, `get_file_info`, `move_file`, `delete_file`
- The 'search_files' function has been removed
- All the standard needs, but OC handles saving  
- Auto-save when editing 

### Image Tools (`image_tools.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/image_tools.py`
- Vision AI image analysis plus designer created process 
- Regular resize, crop, add clean, classic text placement flow 
- Curated, pre-chosen fonts and blending methodology 

**There is a carefully constructed process written out in this tool, including what to do first, second, etc. This is intentional and is meant to be part of this tool's programming.**

### Perplexity Web Search Tool (`perplexity_search.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/perplexity_search.py`
- AI-powered research with reasoning
- Comprehensive analysis with citations
- Topic research, comparisons, trend analysis, etc.

### Text Editor Tool (`text_editor.py`) 
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/text_editor.py`
- Targeted editing by Anthropic   
- Create, edit, append, format documents
- Auto-save implementation

### Anthropic's Think Tool (`think.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/think.py`
- Structured reasoning: analysis, planning, problem-solving, decisions
- Best for reviewing tool gathered information 
- Studies show drastic performance improvement 

### Native Web Search Tool (`web_search.py`)
`/Users/seanivore/Development/single-file-agents/sfa-v4/tools/web_search.py`
- Anthropic's web search capabilities
- Transcript for YouTube video search results (to be added)
- Built-in for Claude 

## Tool Architecture Snippets 

### Universal Tool Structure
Every tool must implement the following. Please note that these were created before we had to create a reminder about the variable-input agent philosophy. Many of them probably have hardcoded information and information use-case specific information. 

```python
def get_tool_definition() -> Dict[str, Any]:
    """Standard tool definition for OC discovery"""
    return {
        "id": "unique_tool_id",
        "name": "Human Readable Name",
        "description": "What this tool accomplishes",
        "capabilities": ["research", "analysis", "generation"],
        "use_cases": ["market research", "competitor analysis"],
        "cost_estimate": 0.05,  # Per use in USD
        "model_compatibility": ["claude", "gpt", "gemini"],
        "tags": ["business", "research", "analysis"],
        "parameters": {...},  # Standard JSON schema
        "human_button_generator": create_snippet_function
    }

def create_human_button_snippet(params: Dict, model: str) -> str:
    """Generate executable code snippet for this tool"""
    # Return self-contained Python code that:
    # 1. Imports necessary libraries
    # 2. Executes the tool functionality  
    # 3. Handles errors gracefully
    # 4. Returns results in standard format
```

## Integration Points

### OC Discovery
```python
# OC can query tools by capability
tools = tool_discovery.find_tools_by_capability("research")
tools = tool_discovery.find_tools_by_tag("business")
tools = tool_discovery.find_tools_by_budget(max_cost=0.10)
```

### Human Button Generation
```python
# Each tool generates executable snippets
snippet = tool.create_human_button_snippet(
    params={"query": "renewable energy trends"},
    model="claude-sonnet-4"
)

# Claude 4 Code Execution Tool runs the snippet
result = execute_code_snippet(snippet)
```

### Cost Integration
```python
# Tools report their costs for workflow planning
estimated_cost = tool.estimate_cost(params)
actual_cost = tool.get_last_execution_cost()
```

### Dynamic Workflow Generation
```python
def generate_workflow(goal: str) -> dict:
    return {
        "command_name": auto_generated_name,
        "workspace": f"projects/{sanitized_goal}/",
        "workflow": {
            "research_phase": {
                "model": model_manager.get_best_model_for_task("research"),
                "execution_snippet": buttons.create_api_call_snippet(...),
                "deliverables": ["research-summary.md"]
            },
            "analysis_phase": {
                "model": model_manager.get_best_model_for_task("reasoning"), 
                "execution_snippet": buttons.create_api_call_snippet(...),
                "deliverables": ["strategy-plan.md"]
            }
        }
    }
```

### Workflow Orchestrator

```python
class WorkflowOrchestrator:
    def __init__(self, model_manager: UniversalModelManager):
        self.models = model_manager
        self.protocol = self.load_protocol()
    
    async def create_workflow_from_goal(self, user_goal: str) -> dict:
        # "Research renewable energy and create marketing strategy"
        # ↓
        # Auto-generated optimal workflow with model selection
    
    async def execute_workflow(self, workflow: dict) -> dict:
        # Coordinate specialist agents via human button snippets
```

## Tool Metadata System

### Dynamic Tool Registry (`configs/tool_registry.json`)
```json
{
  "tools": {
    "web_search": {
      "id": "web_search",
      "name": "Native Web Search",
      "description": "Real-time web search with citations",
      "capabilities": ["research", "current_information"],
      "use_cases": ["market research", "news analysis", "fact checking"],
      "cost_per_use": 0.01,
      "tags": ["research", "web", "realtime"],
      "dependencies": ["anthropic_api"],
      "version": "1.0.0"
    }
  }
}
```

### OC Integration Pattern
```python
class ToolDiscovery:
    def interactive_tool_selection(self, goal: str, model: str, budget: str) -> Dict:
        # 1. Analyze goal for required capabilities
        capabilities = self.extract_capabilities_from_goal(goal)
        
        # 2. Find compatible tools
        compatible_tools = self.find_tools_by_capabilities(capabilities)
        compatible_tools = self.filter_by_model_compatibility(compatible_tools, model)
        compatible_tools = self.filter_by_budget(compatible_tools, budget)
        
        # 3. Generate suggestion with explanation
        return {
            "core_tools": ["web_search", "financial_analysis"],
            "optional_tools": ["competitor_analysis", "image_generation"],
            "core_explanation": "I recommend web search for research and financial analysis for ROI calculations",
            "estimated_tool_cost": 0.16,
            "user_choice_prompt": "Would you like to add any optional tools?"
        }
```

## Testing Strategy 

### Tool Validation Tests
```python
# Each tool must pass:
def test_tool_definition():
    """Validate tool definition structure"""
    definition = tool.get_tool_definition()
    assert "id" in definition
    assert "human_button_generator" in definition
    
def test_human_button_generation():
    """Test snippet generation"""
    snippet = tool.create_human_button_snippet(test_params, "claude-sonnet-4")
    assert snippet.startswith("# Tool:")
    assert "import" in snippet
    assert "return" in snippet

def test_cost_estimation():
    """Validate cost calculations"""
    cost = tool.estimate_cost(test_params)
    assert isinstance(cost, float)
    assert cost > 0
```

### Integration Tests
```python
def test_oc_tool_discovery():
    """Test OC can find and suggest tools"""
    tools = tool_discovery.find_tools_for_goal("Create marketing strategy")
    assert "web_search" in [t["id"] for t in tools]
    
def test_workflow_integration():
    """Test tools work in complete workflows"""
    workflow = orchestrator.create_workflow_from_goal("Research competitors")
    assert any("competitor_analysis" in phase.tools for phase in workflow.phases)
```

## Top Level Integrations

### Code Execution Tool (THE GAME CHANGER)
```python
# Instead of complex SDK management:
async def execute_model_call(snippet: str) -> dict:
    # Claude 4 executes the snippet directly!
    result = await anthropic_client.beta.messages.create(
        model="claude-sonnet-4",
        tools=[{"type": "code_execution_20241022", "name": "execute"}],
        messages=[{"role": "user", "content": f"Execute: {snippet}"}]
    )
    return parse_execution_result(result)
```

### Files API for Cost Optimization
```python
class DraftManager:
    async def save_draft(self, content: str, name: str):
        # FREE Files API storage!
        await anthropic_client.files.create(content=content, name=name)
    
    async def promote_to_final(self, draft_id: str, final_path: str):
        # Only final results hit expensive filesystem
        content = await anthropic_client.files.retrieve(draft_id)
        save_to_real_filesystem(content, final_path)
```

### Parallel Tool Execution
```python
async def parallel_specialists(tasks: List[Task]) -> List[Result]:
    # Multiple agents working simultaneously!
    snippets = [
        buttons.create_api_call_snippet(task.optimal_model, task.prompt)
        for task in tasks
    ]
    
    # Claude 4 can execute tools in parallel
    results = await asyncio.gather(*[
        execute_code_snippet(snippet) for snippet in snippets
    ])
    
    return orchestrator.synthesize_results(results)
```

### Extended Thinking + Tools
```python
# Orchestrator can think while coordinating
orchestrator_response = await anthropic_client.beta.messages.create(
    model="claude-sonnet-4",
    tools=orchestrator_tools,
    thinking=True,  # Extended thinking while using tools!
    messages=[{"role": "user", "content": "Plan and execute this complex workflow..."}]
)
```

### Memory Files for Workflow State
```python
class WorkflowMemory:
    async def save_workflow_state(self, workflow_id: str, state: dict):
        # Claude 4's memory capabilities
        memory_content = json.dumps(state)
        await anthropic_client.files.create(
            content=memory_content,
            name=f"workflow_{workflow_id}_state.json"
        )
```

## Wider Architecture 

### Toolkit Configuration (`configs/toolkits.json`)
**NEEDS TO BE UPDATED, RE: SFA PHILOSOPHY NOTE**

```json
{
  "toolkits": {
    "core": {
      "tools": ["workflow_control", "file_operations", "decision_making"],
      "always_loaded": true,
      "token_cost": 500
    },
    "research": {
      "tools": ["web_search", "perplexity_search", "document_analysis"],
      "load_for_tasks": ["research", "analysis"],
      "token_cost": 1200
    },
    "creative": {
      "tools": ["content_generation", "brand_voice", "image_editing"],
      "load_for_tasks": ["creative", "marketing"],
      "token_cost": 800
    }
  }
}
```

### Dynamic Tool Loading
```python
class ToolManager:
    def get_tools_for_task(self, task_type: str) -> List[ToolDefinition]:
        # Only load relevant tools, not everything!
        toolkits = self.config.get_toolkits_for_task(task_type)
        return self.load_minimal_tool_set(toolkits)
    
    def generate_tool_snippet(self, tool_name: str, params: dict) -> str:
        # Generate executable snippet for tool use
        return f"result = {tool_name}({json.dumps(params)})"
```

### Code Execution Tool Integration
```python
# Instead of complex tool implementations:
def web_search_snippet(query: str) -> str:
    return f'''
import requests
response = requests.get("https://api.brave.com/search", 
                       params={{"q": "{query}"}})
result = response.json()
print(result)
'''

def image_optimization_snippet(image_path: str) -> str:
    return f'''
from PIL import Image
img = Image.open("{image_path}")
optimized = img.resize((1200, 800), Image.Resampling.LANCZOS)
optimized.save("optimized_" + "{image_path}")
print("Image optimized successfully")
'''
```