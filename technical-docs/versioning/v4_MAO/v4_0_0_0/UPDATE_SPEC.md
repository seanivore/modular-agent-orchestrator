---
NOTES: Sections we have and need, and the order. When they get large we can put into a separate document for things like philosophy, etc. 
1. Philosophy, Philosophical Journey 
2. Problems, Solutions; Orchestrator Role in Solutions, Agents Role in Solutions 
3. Human UI & UX; Workflow Setup, Terminal Display 
4. Start of protocol.md workflow planning 
5. Terminal UX 
(Right here we are currently breaking down a complex workflow to identify what goes in the terminal display, and more. When done we can convert it into a protocol that can go in the protocol.md document.)
6. Verbose mode 
7. Tool Creation with File-by-File Integration Breakdown and Code Snippets 
8. Shared Error Handling and Shared Cache 
9. Important Rules (for tools)
10. Then all the different code for the main system section 
----
Philosophy 
Problems and Solution 
Two Roles, Orchestrator and Agent 

---

# MAO v4.0.0 Update Specifications  
*JSON Config + Code Execution "Button" Architecture*

## The MAO Philosophy 

Our philosophical journey. 

**⚠️ WHAT NEEDS WORK (Your focus areas!):**
- User experience flow (setup conversation, custom commands)
- Print function audit (move to UI layer)
- Testing and validation

**🚨 CRITICAL ANTI-PATTERNS TO AVOID:**
- NO hardcoded use cases, categories, or domains
- NO predefined templates or frameworks
- NO "choose your method" menus
- NO domain-specific assumptions
- Tools must be blank canvases - let prompts define specifics

### Our Original Needs 

Our simple single-file agent grew rapidly and was a hassle to update. As it become more and more unwieldly, we were also stacking up hopeful ideas of what the future of the product looked like. 

1. Multiple Models Needed 
   - Needed cheaper options 
   - Potential to delegate tasks 
   - Expand capabilities but not complexity 
2. Serious Spring Cleaning 
   - Spotted specifics in agent system code 
   - Elements that could have started modular 
   - Became a very heavy and costly file 
3. Actual Agentic Workflows 
   - No over-planned branching 
   - Knowing creative decision choices isn't realistic 
   - AI needs to make more decisions 
4. Workflow Orchestrator Dream 
   - Delegation to other agents 
   - Access to more creative workflows 
   - Make simpler for human and agents  

### Puritanical Realism 

Thinking through the big picture challenges, they were too specific and loud not to adhere to them absolutely. It was seeing flaws in the old design, realizing things hardcoded actually were modular, that pointed to the solution. 

1. Accept: **AI Is Changing Every Constantly** 

- The product must not ever have a shelf life 
- Absolute protection from all that has been changing frequently 
- Must embrace changes fast enough to always be cutting edge 

2. Identify: **What Doesn't Change In AI?** 

- There are AI models 
- Models interact with tools 
- Python adopted early in docs 
- We want it to do something for us 
- Can't predict what we want it to do 
- Abilities will always be changing  

3. Solution: **Our Variable Input Use-Case** 

- Original product was free of hardcoded use-case information 
- Modularity solved many points 
- The part of the system it plugged into were all modular 

### Modularity Obsession 

Recognizing that the design system, the architecture, was essentially text-book 'good art' it became obvious we were on to something legitimate. The shift from chaos to calm was too profound, the end point was too clear. You couldn't look away. 

- **VARIABLES LIGHTBULB MOMENT**
  - Use-cases were input by variables in a config JSON 
  - Models have variables to config JSON
  - Tools have variables to config JSON 
  - Files can be organized as variables themselves 

- **MODULARITY IS DESIGN PERFECTION** 
  - Start with something chaotic 
  - End with a complete simplicity 
  - That is art; that is good design  

- **UNEXPECTED TRANSFORMATION DENOTES COMPLETION**
  - Figuring out modular logic is challenging
  - Our tasks are always more complicated than we think 
  - The tools stack up and constantly morph 
  - But the outcome is always unexpectedly simple 
 
## Defined Problem & Solution 

### Problems 
- **Token Cost Explosion** 
  - v3.3.0 grew to 23,400 tokens per read 
  - It was being read every loop 
  - Workflow writing targeted resume cost multiple dollars 
  - Dollars instead of pennies was no longer usable  
- **Manual JSON Bottleneck** 
  - Creating workflow configurations was time consuming 
  - We weren't even getting into unique workflow patterns 
  - Our branching decisions had multiple choices 
  - It wasn't agentic enough 
- **Hardcoded Assumptions** 
  - Claude model assumptions throughout codebase 
  - Costs, print functions and more in the scripts 
  - Expanding became too complicated as it stood 
- **Tool Bloat** 
  - Every agent sees all tools, even irrelevant ones
  - We were stacking up the tools quickly 
  - Their error handling, definitions, etc. was a lot 

### Solutions 
- **Claude Orchestrator** 
  - Can create workflows dynamically in chat 
  - Works rapidly meaning access to more interesting workflows 
  - They can be called between agents and alter the workflow live 
  - Provides 'just in time' tools along with the task  
  - Collects deliverables directly 
- **Modular Architecture** 
  - Everything cached on its own, one time 
  - Only what is needed by the agent is passed to the agent 
  - More files didn't mean more code overall 
  - Easier to add new updates 
  - Cost estimates got into low fractions 
- **Provider Agnostic** 
  - SDK translation is side-stepped completely  
  - Works with any LLM provider or model, just like use-case variables 
  - The buttons are human-like and code execution 
  - Its really many-things-agnostic 

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


### Orchestrator Agent
- **Setup Role** 
  - Available in chat as workflow architect 
  - Can rapidly build workflow 
  - Provides ideas, cost, etc. 
- **Workflow Role** 
  - They are the on-call project manager
  - Agents call to end task, eliminating logistical tools 
  - Monitors progress and handles error recovery
  - Can change the next planned task or workflow on the fly 
**Human-Friendly** 
  - Improves with essential simplicity 
  - Same JSON config and be hand written 
  - Same setup script can create workflow 
  - Same custom command selection to run workflow 


### Agent Role, Re: Generated Button Interface
**Role**: Task + Buttons 
- Claude 4 uses code execution 
- Agent gets assignment 
  - Mention User chosen or model *TOKEN MAX* output count 
  - Pairs with edit document's *live, persistent token count UI*
  - Includes *AUTOSAVE* reminder; same conveniences as humans, like a Google Doc 
  - *No option to save output,* all is handed off directly to MAO 
  - Includes an *MAO callback snippet*
  - *Snippets are generated to be executed for function calls* 
- Agent uses clean functional tools to do work, no SDK code specifics 
- Agent runs provided snippet to call MAO with deliverables as only exit point 

**Features**: Stress-free
- Automatic format conversion (Claude ↔ OpenAI ↔ Gemini)
- Unified tool calling interface
- Provider-specific optimizations (caching, token efficiency)
- Fallback mechanisms and error handling

## Managing Variables Via Snippets 

1. JSON Configuration System 
**Goal: Dynamic model/provider discovery, eliminate ALL hardcoding; if it is hardcoded, show Sean to consider**

2. Universal Model Manager 
**Instead of hardcoded provider classes, use JSON configs + Code Execution Tool to generate executable snippets for any model/provider combo.**

3. Button-Simple Function Calls 
**No more 'Provider > Response' instead 'Snippet > Result'**

### Test Should Include 
- Load all configs successfully 
- Create `./components/ai/connections/models_x_providers.json`
- Generate snippets for every model/provider combo 
- Execute snippets via Code Execution Tool 
- Verify cost calculations from JSON pricing
- Test result of agent button function calls 


## 🎯 REVOLUTIONARY ACHIEVEMENTS SUMMARY

### **Token Efficiency Revolution** 📉
- **Before**: 23,400 tokens per agent ($0.07+ per phase)
- **After**: <1,000 tokens per agent (95% reduction achieved!)
- **Method**: Modular tool loading vs. monolithic file reads

#### **95% Token Reduction** 📉
- **Before**: 23,400 tokens per agent ($0.07+ per phase)
- **After**: <1,000 tokens per agent (95% reduction!)
- **Method**: Modular tool loading vs. monolithic file reads


### **Variable-Input Philosophy Success** 🎨
- **Eliminated**: Hardcoded templates, frameworks, use cases
- **Achieved**: True blank canvas tools adaptable to any domain
- **Proven**: AI naturally applies methodologies without rigid coding

### **Modular Architecture Victory** 🏗️
- **Transformed**: 7 monolithic tools → 35 modular files
- **Achieved**: Clean separation of concerns across all tools
- **Proven**: 5-file pattern works across diverse tool types

### **Universal Compatibility** 🌐
- **Human Buttons**: Work with ANY model/provider via code generation
- **SDK Independence**: No more provider-specific implementations
- **Future-Proof**: Easy to extend and maintain


Use-Case Development, Configuration Setup, & Workflow Activation  

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











## MAO Protocol 
Editable markdown file defining orchestrator decision-making at `./build/orchestrator/protocol.md`

**IMPORTANT**: 
- To avoid hardcoding information, only indicate what models or tools are capable of. Do not assume or provide use-case examples. 
- When connecting this reference information for the MAO, remain free of hardcoding. 
- If this requires the information to be in a script instead of a markdown document, then only place it there via `./build/orchestrator/master/model_manager.py` or via `./build/orchestrator/master/tool_manager.py`

### Identify Workflow Patterns 
- **Parallel Tool Calling**: Sonnet 4 feature 
- **Parallel Agent Tasking**: Efficient
- **Pre-fab. Tasks**: 
  - Save needs like "consolidate document" 
  - That are common 
  - Always go to the same model 
  - Consider making them a simple, prepared tool snippet 
- **Token Heavy**: Prioritize efficiency models 
- **Research Heavy**: Free or cheap model with robust for analysis 

### Fallback Models
**Preselect Fallback Models** 
  - Free models are not always reliable 
  - Add secondary option to the workflow config JSON 
  - Consider third or permanent default depending on costs 

## Terminal User Interface 

- All tools have a `ui_tool_name.py` file 
- Master build has a `./build/interfaces/ui_terminal.py` 


## Human UI & UX 

### Workflow Project Planning 

WE NEED TO COME UP WITH A REALLY FORMULAIC WAY TO THINK ABOUT BREAKING DOWN PROJECTS THAT IS CREATIVE ENOUGH TO FIT ALL KINDS OF USE CASES, BIG OR SMALL. Let's take a great example and break it down. 

1. Think PROJECTS as the workflow now 
   - We need to plan big picture as smaller will come more easily then. 
   - I want to *really* think this stuff through before creating actual UI, attempting to get it right as possible the first time. 
   - Perhaps it will help to think of the project itself as modular. 
2. We need a hierarchy to break down the most complex projects that has enough chunks to handle very large tasks. 
   - I want to use an example that I had Perplexity Pro do once which was a "where to move" analysis for two cities that took into account many variables, it gave scoring to qualitative variables, and created a matrix, then analyzed that. 
   - I exported a markdown of the chat; could you please go through it and pull out the variables and phases? The phases can be simplified, in that, towards the end of the conversation is the best matrix when we really had nailed down what variables to look at, how to weight them, etc. Think of the chat itself as the evolution of Perplexity and I figuring out the best way to do that as we went, so no need to have multiple phases that are the same: `./technical-docs/versioning/v4_MAO/WORKFLOW_PROJECT.md`
3. Need to have a "Workflow evolves as it progresses" setting that I'd like to be the primary type of workflow. 
   - I'm not a fan of having "branching" that uses multiple choice options because it doesn't leave room for creativity 
   - For example in the sample project from Perplexity, maybe when OC gets it back to review they think of another variable 
   - OMG also we need to have a 'human input' sort of 'pause' for similar reasons 
4. I'm actually really excited about the workflow example from Perplexity because so much of what they did we can do running agents in parallel 

- Project  
- Tasks are par

### Terminal Updates Printed Text Without Reprinting 

- Enough with the constantly printing feed 
- Prints so much that you end up reading and reading 
- Then you realize you didn't need to read much of anything 
- Instead we'll create a static, real-time monitoring display 

```
┌─—————— Workflow Monitor ─────────────────────────┐
│ Marketing Strategy • Running 3m 24s               │
├───────────────────────────────────────────────────┤
│ ✅ Research Agent    • Analyzed market trends     │
│ 🔄 Strategy Agent    • Creating frameworks...     │
│ ⏸️  Writing Agent     • Waiting for strategy      │
├───────────────────────────────────────────────────┤
│ Models: Gemini (FREE) → Claude Sonnet 4           │
│ Tokens: 2,847 used • $0.02 spent • Est: $0.08     │
│ ETA: 2 minutes remaining                          │
└───────────────────────────────────────────────────┘
```

┌——— WORKFLOW MONITOR ————┐
| Use Case Name           |
├—————————————————————————┤
| STATUS: 
Phase 1 of 3 — Research 
Elapsed Time: 00:00:00 
Spent: $0.021 
├—————————————— Vegas & San Jose Standard of Life Analysis ——————————————┤
| Research, Calculation, Analysis 
| Phase 1: Matrix Creation 
| 
| 10 Year Climate Change Cost Impact 
├———————————————————————————————— ACTIVE ————————————————————————————————┤
| Parallel Agents  | Phase 3 (00:00:23) of 4 (00:06:45)  |
| Agent Gemini 2.5 Pro | Task: Cost Analysis 
| TASK NAME: Overall Cost Analysis 

 

Agent Analysis of data 
Parallel agent: Analysis of research   
Elapsed Time: 00:00:00 
Spent: $0.021 
├—————————————————————————┤
| UP NEXT 
Phase(s): 3 
Total Phases: 5
Agents running in parallel 
Elapsed Time: 00:00:00 
Spent: $0.021 
├—————————————————————————┤
DETAILS 

### Web UX 

Planning this display will make translating it to other UI solutions all the easier.  

### Verbose Mode With Forensic Debugging (ADDED ✅)

- Enhanced terminal interface 
- Forensic debugging  
- Browser development tools-style 
- X-Ray view into what every model is doing 

#### Included 

- 📡 Network requests & responses
- 🚦 Rate limits & quotas  
- ⚡ Processing speeds
- 💸 Cost breakdowns
- 🔧 Tool usage
- 🧠 Model internals

### Forensic Debugging Feature Details 

#### Network Traces
```
🌐 NETWORK TRACE STARTING:
📡 Target: https://api.anthropic.com
📤 Payload: 1,247 bytes
🔑 Headers: {'Authorization': 'Bearer anth_***', 'Content-Type': 'application/json'}
✅ Response: 200 OK (3,891 bytes)
🚦 Rate limits: {'x-ratelimit-remaining': '499'}
```

#### Model Forensics
```
📊 EXECUTION FORENSICS:
🎯 Tokens: 6,000
💸 Cost: $0.039600
⚡ Rate: 2,609 tokens/sec
📡 API latency: 340ms
🧠 Model time: 2.1s
💾 Cache: MISS
🏁 Reason: stop
```

#### Error Forensics
```
🚨 FAILURE FORENSICS:
📡 HTTP: 429 Too Many Requests
🏷️  Type: RateLimitError
🚦 Rate limited: true
⏰ Retry in: 60s
🔢 Error code: rate_limit_exceeded
```

#### Performance Analytics
```
📊 PERFORMANCE ANALYTICS:
Total tokens: 24,000
Processing rate: 3,000 tokens/sec
Cost efficiency: 294,118 tokens/$
```


## Tool Creation 6-File Architecture Pattern


For each tool, create exactly 4 files, update 2 files: 

```
./components/tools/tool_name/...
├── tool_name.py              # 1. Core Logic
├── ui_tool_name.py           # 2. UI Display
├── button_tool_name.py       # 3. Human Buttons
└── tool_name.json            # 4. Tool Registry
./build/orchestrator/...
├── /master/error_handling.py  # 5. Shared Error Handling
└── /cache/cache_system.py     # 6. Shared Cache System
```

### 🔧 File-by-File Implementation

#### 1. Core Logic File (`tool_name_modular.py`)

**Purpose**: Pure functionality with enhanced error handling
**Rules**: NO UI, NO hardcoded specifics, structured data return

```python
"""
Tool Name
Independent tool logic with enhanced error handling
"""

import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import time


def main_function(param1: str, param2: int = 10, param3: str = "default") -> Dict[str, Any]:
    """
    Execute tool functionality with comprehensive error handling
    
    Args:
        param1: Primary input parameter
        param2: Optional numeric parameter
        param3: Optional string parameter
        
    Returns:
        Dict with structured results or error information
    """
    try:
        # Validation
        if not param1.strip():
            return {"error": "Primary parameter cannot be empty"}
        
        # Clamp numeric values to valid ranges
        param2 = min(20, max(1, param2))
        
        # API Configuration (if needed)
        api_key = os.getenv("API_KEY_NAME")
        if not api_key:
            return {"error": "API key not found. Set API_KEY_NAME environment variable"}
        
        # Main logic with retry pattern
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Your main logic here
                result = perform_operation(param1, param2, param3)
                
                if result:
                    break
                    
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {str(e)}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Process and return structured results
        return {
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": processed_results,
            "metadata": {
                "processing_time": processing_time,
                "parameters_used": {"param1": param1, "param2": param2, "param3": param3}
            }
        }
        
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1
        }


def estimate_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for this operation"""
    # Return realistic cost estimate for workflow planning
    return 0.001
```

#### 2. UI Display File (`ui_tool_name.py`)

**Purpose**: Beautiful terminal output formatting
**Rules**: NO business logic, clean vs verbose modes, Rich console formatting

```python
"""
TOOL NAME
UI Display Component
"""

from typing import Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def display_tool_results(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Take structured data → beautiful terminal output
    
    Args:
        result: Tool result data
        verbose: Show detailed technical information
    """
    console = Console()
    
    # Handle error cases
    if "error" in result:
        console.print(f"❌ Tool Error: {result['error']}", style="red")
        if verbose and "timestamp" in result:
            console.print(f"   Timestamp: {result['timestamp']}", style="dim")
        return
    
    # Handle empty results
    if not result.get("results"):
        console.print(f"⚠️ No results found", style="yellow")
        return
    
    # Main results display
    input_param = result.get("input_param", "Unknown input")
    results = result.get("results", [])
    
    # Header
    if verbose:
        header_text = f"🔧 Tool Results: {input_param} ({len(results)} items)"
        console.print(Panel(header_text, style="blue"))
    else:
        console.print(f"🔧 Found {len(results)} results for: {input_param}", style="blue bold")
    
    # Results table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item", style="bold")
    table.add_column("Description", style="dim")
    
    if verbose:
        table.add_column("Details", style="link")
    
    for i, item in enumerate(results, 1):
        title = item.get("title", "No title")[:60] + "..." if len(item.get("title", "")) > 60 else item.get("title", "No title")
        description = item.get("description", "No description")[:100] + "..." if len(item.get("description", "")) > 100 else item.get("description", "No description")
        
        if verbose:
            details = item.get("details", "No details")
            table.add_row(str(i), title, description, details)
        else:
            table.add_row(str(i), title, description)
    
    console.print(table)
    
    # Verbose metadata
    if verbose:
        metadata = result.get("metadata", {})
        if metadata:
            console.print("\n📊 Processing Metadata:", style="bold")
            
            if "processing_time" in metadata:
                console.print(f"   Processing Time: {metadata['processing_time']:.2f}s")
            
            console.print(f"   Timestamp: {result.get('timestamp', 'Unknown')}")


def display_cost_estimate(cost: float, verbose: bool = False) -> None:
    """Display cost estimation for tool operation"""
    console = Console()
    
    if cost == 0:
        console.print("💰 Cost: FREE", style="green bold")
    else:
        console.print(f"💰 Estimated cost: ${cost:.4f}", style="yellow")


def format_for_agent_handoff(results: Dict[str, Any]) -> str:
    """Format results for agent-to-agent handoff"""
    if "error" in results:
        return f"Tool execution failed: {results['error']}"
    
    input_param = results.get("input_param", "Unknown input")
    results_list = results.get("results", [])
    
    if not results_list:
        return f"No results found for: {input_param}"
    
    # Format top results for handoff
    formatted_results = [f"Tool results for '{input_param}' ({len(results_list)} items):\n"]
    
    for i, item in enumerate(results_list[:5], 1):  # Top 5 for handoff
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        
        formatted_results.append(f"{i}. {title}")
        formatted_results.append(f"   {description}\n")
    
    return "\n".join(formatted_results)
```

### 3. Human Button File (`button_tool_name.py`)

**Purpose**: Generate executable code snippets for Claude 4
**Rules**: Self-contained, universal model compatibility, built-in cost tracking

```python
"""
TOOL NAME
Human Button Generators
"""

from typing import Dict, Any


def create_human_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """
    Generate executable code snippet for Claude 4 execution
    Universal model compatibility via code generation
    
    Args:
        params: Tool parameters
        model: Target model for execution
        
    Returns:
        Self-contained executable Python code snippet
    """
    
    # Extract parameters with defaults
    param1 = params.get("param1", "")
    param2 = params.get("param2", 10)
    param3 = params.get("param3", "default")
    
    # Generate self-contained executable snippet
    snippet = f'''# Tool Name Execution
# Model: {model}
# Input: {param1}

import json
import requests
import os
import time
from datetime import datetime

def execute_tool():
    """Execute tool with comprehensive error handling"""
    
    # Tool parameters
    param1 = "{param1}"
    param2 = {param2}
    param3 = "{param3}"
    
    try:
        # Validation
        if not param1.strip():
            return {{"error": "Primary parameter cannot be empty", "cost": 0.0}}
        
        # Clamp values to valid ranges
        param2 = min(20, max(1, param2))
        
        # API Configuration (if needed)
        api_key = os.getenv("API_KEY_NAME")
        if not api_key:
            return {{
                "error": "API key not found. Set API_KEY_NAME environment variable",
                "cost": 0.0
            }}
        
        # Main logic with retry pattern
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Your main logic here
                result = perform_operation(param1, param2, param3)
                
                if result:
                    break
                    
            except requests.exceptions.Timeout:
                last_error = f"Request timeout (attempt {{attempt + 1}}/{{max_retries}})"
                if attempt < max_retries - 1:
                    continue
            except requests.exceptions.RequestException as e:
                last_error = f"Network error: {{str(e)}}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        
        # Check final result
        if not result:
            return {{
                "error": f"Tool execution failed after {{max_retries}} attempts. Last error: {{last_error}}",
                "cost": 0.001
            }}
        
        # Process and return structured results
        tool_results = {{
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": result,
            "metadata": {{
                "processing_time": processing_time,
                "parameters_used": {{"param1": param1, "param2": param2, "param3": param3}}
            }},
            "cost": 0.001  # Adjust based on actual API costs
        }}
        
        return tool_results
        
    except Exception as e:
        return {{
            "error": f"Tool execution failed: {{str(e)}}",
            "timestamp": datetime.now().isoformat(),
            "input_param": param1,
            "cost": 0.001
        }}

# Execute the tool
result = execute_tool()

# Display results
print("🔧 Tool Execution Results:")
print(f"Input: {param1}")
print(f"Status: {{result.get('status', 'error')}}")
print(f"Cost: ${{result.get('cost', 0.001):.4f}}")

if result.get('error'):
    print(f"❌ Error: {{result['error']}}")
else:
    print("✅ Tool executed successfully")
    print(f"Results: {{len(result.get('results', []))}}")

# Return structured result for orchestrator
result'''
    
    return snippet


def estimate_execution_cost(params: Dict[str, Any]) -> float:
    """Estimate cost for executing this tool"""
    # Return realistic cost estimate
    return 0.001


def get_tool_capabilities() -> Dict[str, Any]:
    """Return tool capabilities for orchestrator discovery"""
    return {
        "name": "tool_name",
        "capabilities": ["capability1", "capability2", "capability3"],
        "cost_estimate": 0.001,
        "models_supported": ["all"],
        "tags": ["tag1", "tag2", "tag3"],
        "parameters": {
            "param1": {"type": "string", "required": True, "description": "Primary input parameter"},
            "param2": {"type": "integer", "default": 10, "description": "Optional numeric parameter"},
            "param3": {"type": "string", "default": "default", "description": "Optional string parameter"}
        }
    }
```

### 4. Tool Registry File (`tool_name.json`)

**Purpose**: Tool metadata and discovery configuration
**Rules**: Clean metadata, NO hardcoded use cases, capability-based discovery

```json
{
  "id": "tool_name",
  "name": "Tool Display Name",
  "description": "Brief description of tool functionality with enhanced error handling",
  "version": "1.0.0",
  "capabilities": [
    "capability1",
    "capability2", 
    "capability3"
  ],
  "tags": [
    "tag1",
    "tag2", 
    "tag3"
  ],
  "cost_estimate": 0.001,
  "models_supported": ["all"],
  "dependencies": ["requests", "API_KEY_NAME"],
  "parameters": {
    "param1": {
      "type": "string",
      "required": true,
      "description": "Primary input parameter"
    },
    "param2": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 20,
      "description": "Optional numeric parameter"
    },
    "param3": {
      "type": "string",
      "default": "default",
      "description": "Optional string parameter"
    }
  },
  "functions": [
    {
      "name": "main_function",
      "description": "Execute primary tool functionality",
      "parameters": ["param1", "param2", "param3"]
    },
    {
      "name": "estimate_cost",
      "description": "Estimate operation cost",
      "parameters": ["params"]
    }
  ],
  "files": {
    "core_logic": "tools/tool_name_modular.py",
    "ui_display": "interfaces/ui_tools/ui_tool_name.py", 
    "human_buttons": "utilities/human_button_tools/button_tool_name.py"
  },
  "error_handling": {
    "retry_logic": true,
    "timeout_handling": true,
    "rate_limit_handling": true,
    "graceful_degradation": true
  },
  "output_format": {
    "success": {
      "status": "success",
      "input_param": "string",
      "timestamp": "string", 
      "results": "array",
      "metadata": "object",
      "cost": "float"
    },
    "error": {
      "error": "string",
      "timestamp": "string",
      "input_param": "string",
      "cost": "float"
    }
  }
}
```

### 5. Shared Error Handling (`build/orchestrator/master/error_handling.py`)

**Purpose**: Common error patterns for all tools
**Rules**: Reusable functions, professional retry logic, graceful degradation

```python
"""
Shared Error Handling Patterns
Common retry logic, validation, and graceful degradation for all SFA v4 tools
"""

import time
import requests
from typing import Callable, Any, Dict, Optional
from functools import wraps


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retry logic with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries (seconds)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.Timeout as e:
                    last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                        continue
                    raise e
                except requests.exceptions.RequestException as e:
                    last_error = f"Network error: {str(e)}"
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                        continue
                    raise e
                except Exception as e:
                    # Don't retry on non-network errors
                    raise e
            
            raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")
        
        return wrapper
    return decorator


def validate_api_response(response: requests.Response) -> Dict[str, Any]:
    """
    Common API response validation
    
    Args:
        response: HTTP response object
        
    Returns:
        Validation result with status and error info
    """
    if response.status_code == 200:
        return {"valid": True, "data": response.json()}
    elif response.status_code == 429:
        return {"valid": False, "error": "Rate limited", "retry_after": response.headers.get("Retry-After")}
    elif response.status_code == 401:
        return {"valid": False, "error": "Authentication failed - check API key"}
    elif response.status_code == 403:
        return {"valid": False, "error": "Access forbidden - insufficient permissions"}
    elif response.status_code >= 500:
        return {"valid": False, "error": f"Server error ({response.status_code}) - try again later"}
    else:
        return {"valid": False, "error": f"HTTP {response.status_code}: {response.text[:200]}"}


def handle_rate_limits(response: requests.Response) -> Optional[float]:
    """
    Universal rate limit handling
    
    Args:
        response: HTTP response object
        
    Returns:
        Recommended wait time in seconds, or None if no rate limiting
    """
    if response.status_code == 429:
        # Check for Retry-After header
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
        
        # Default rate limit wait
        return 60.0
    
    return None


def safe_api_call(url: str, headers: Dict[str, str], params: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    """
    Safe API call with comprehensive error handling
    
    Args:
        url: API endpoint URL
        headers: Request headers
        params: Request parameters
        timeout: Request timeout in seconds
        
    Returns:
        Standardized response with error handling
    """
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        
        # Handle rate limiting
        wait_time = handle_rate_limits(response)
        if wait_time:
            time.sleep(wait_time)
            # Retry once after rate limit
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
        
        # Validate response
        validation = validate_api_response(response)
        if validation["valid"]:
            return {"success": True, "data": validation["data"]}
        else:
            return {"success": False, "error": validation["error"]}
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error - check network"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def validate_required_params(params: Dict[str, Any], required: list) -> Dict[str, Any]:
    """
    Validate required parameters are present and non-empty
    
    Args:
        params: Parameter dictionary
        required: List of required parameter names
        
    Returns:
        Validation result
    """
    missing = []
    empty = []
    
    for param in required:
        if param not in params:
            missing.append(param)
        elif not str(params[param]).strip():
            empty.append(param)
    
    if missing or empty:
        error_parts = []
        if missing:
            error_parts.append(f"Missing parameters: {', '.join(missing)}")
        if empty:
            error_parts.append(f"Empty parameters: {', '.join(empty)}")
        
        return {"valid": False, "error": "; ".join(error_parts)}
    
    return {"valid": True}
```

### 6. Shared Cache Integration (`build/orchestrator/cache/cache_system.py`) 

```python
"""
Cache Integration Example
Shows how modular tools integrate with universal cache and error handling
"""

from typing import Dict, Any
from ..error_handling import handle_errors, retry_with_backoff, ValidationError
from .universal_cache import get_global_cache, cache_operation, CacheFingerprint, ModelToolMapper

# Example: How a modular tool integrates with infrastructure

@handle_errors(operation_name="web_search", return_dict=True)
@retry_with_backoff(max_retries=3, base_delay=1.0)
@cache_operation(operation="web_search", ttl_hours=6, estimated_cost=0.003)
def perform_web_search(query: str, search_type: str = "comprehensive", 
                      model: str = "claude-3-5-sonnet", context: str = "") -> Dict[str, Any]:
    """
    Example of modular tool function with full infrastructure integration
    
    This shows how a tool function can use:
    - Error handling with professional patterns
    - Retry logic with exponential backoff  
    - Universal caching with fingerprinting
    - Cost tracking and optimization
    """
    
    # Validate parameters (error handling will catch ValidationError)
    if not query.strip():
        raise ValidationError("Query cannot be empty", "query", query)
    
    # Simulate web search operation
    # In real implementation, this would call actual web search API
    search_results = {
        "query": query,
        "search_type": search_type,
        "model_used": model,
        "results": [
            {"title": f"Result for {query}", "url": "https://example.com", "snippet": "Example snippet"},
            {"title": f"Another result for {query}", "url": "https://example2.com", "snippet": "Another snippet"}
        ],
        "metadata": {
            "total_results": 2,
            "search_time": 0.5,
            "cached": False  # Will be updated by cache system
        }
    }
    
    return {
        "status": "success",
        "search_data": search_results,
        "message": "Web search completed successfully"
    }

def demonstrate_cache_integration():
    """Demonstrate how cache integration works"""
    
    # Get global cache instance
    cache = get_global_cache()
    
    # Get model-tool mapper
    mapper = ModelToolMapper(cache)
    
    print("🗄️ SFA v4 Cache Integration Demo")
    print("=" * 50)
    
    # Example 1: Basic operation with caching
    print("\n1. First search (will be cached):")
    result1 = perform_web_search(
        query="AI orchestration tools",
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result1['status']}")
    print(f"   Results: {len(result1['search_data']['results'])}")
    
    # Example 2: Same search (should hit cache)
    print("\n2. Same search (should hit cache):")
    result2 = perform_web_search(
        query="AI orchestration tools", 
        search_type="comprehensive",
        model="claude-3-5-sonnet"
    )
    print(f"   Status: {result2['status']}")
    print(f"   Results: {len(result2['search_data']['results'])}")
    
    # Example 3: Show cache statistics
    print("\n3. Cache Statistics:")
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Example 4: Model optimization
    print("\n4. Model Optimization:")
    optimal_model = mapper.get_optimal_model("web_search", budget_limit=0.01)
    print(f"   Optimal model for budget $0.01: {optimal_model}")
    
    cost_estimate = mapper.get_cost_estimate("web_search", "claude-3-5-sonnet", "medium")
    print(f"   Estimated cost for claude-3-5-sonnet: ${cost_estimate:.4f}")
    
    # Example 5: Manual cache fingerprinting
    print("\n5. Manual Cache Fingerprinting:")
    fingerprint = CacheFingerprint.generate_fingerprint(
        operation="web_search",
        params={"query": "test", "search_type": "quick"},
        model="claude-3-haiku"
    )
    print(f"   Generated fingerprint: {fingerprint}")
    
    print("\n✅ Cache integration demo completed!")

def demonstrate_error_handling():
    """Demonstrate error handling integration"""
    
    print("\n⚠️ Error Handling Demo")
    print("=" * 30)
    
    # Example 1: Validation error
    print("\n1. Testing validation error:")
    result = perform_web_search(query="", search_type="comprehensive")
    if "error" in result:
        print(f"   Caught validation error: {result['error']}")
        print(f"   Error code: {result['error_code']}")
    
    # Example 2: Show how retry logic would work
    print("\n2. Retry logic is built-in for network failures")
    print("   (Would automatically retry with exponential backoff)")
    
    print("\n✅ Error handling demo completed!")

if __name__ == "__main__":
    # Run demonstrations
    demonstrate_cache_integration()
    demonstrate_error_handling() 
```

## 🚨 Critical Rules

### Variable-Input Philosophy
- **NEVER** hardcode use cases, categories, or specific domains
- **ALWAYS** return structured data, not predetermined choices
- **ALWAYS** let prompts define specifics, not the code

### Anti-Patterns to Avoid
```python
# ❌ WRONG - Hardcoded categories
analysis_types = ["financial", "marketing", "technical"]

# ❌ WRONG - Predefined templates  
templates = {"business_plan": "...", "research_report": "..."}

# ❌ WRONG - Domain-specific enums
class AnalysisFramework(Enum):
    SWOT = "swot"
    PESTLE = "pestle"
```

### Correct Patterns
```python
# ✅ RIGHT - Blank canvas approach
def analyze_content(content: str, analysis_approach: str) -> Dict:
    """Let the prompt define the approach, not the code"""
    
# ✅ RIGHT - Structured data return
return {
    "analysis": analysis_result,
    "key_points": extracted_points,
    "metadata": {"approach": analysis_approach}
}
```

----

## Conclusion 💎

SFA v4 represents a fundamental shift from hardcoded tool to universal AI orchestrator. The JSON config + Code Execution Tool approach eliminates technical debt while enabling unprecedented flexibility.

**The Vision**: Anyone types what they want in natural language, and the orchestrator figures out the optimal way to accomplish it using any available AI models.

**The Reality**: We're building the infrastructure that makes this possible.

**The Business**: This becomes the "headless AI orchestrator" that powers intelligent workflows everywhere.

Let's build the future of AI workflow automation! 🚀


----

## Orchestrator System Files 


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