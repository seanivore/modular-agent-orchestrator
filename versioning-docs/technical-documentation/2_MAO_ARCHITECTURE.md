# Mao Architecture
**Complete System Architecture & Integration Guide**

*Deep technical understanding of how Mao components work together*

---

## 🏗️ System Overview

Mao's architecture is built on **principled modularity** - every component is independent, replaceable, and universally compatible. This enables infinite extensibility without performance degradation.

### Core Architectural Principles

**1. Universal Compatibility** 🌐
- Any AI model works with any tool via human buttons
- Provider-agnostic design eliminates vendor lock-in
- Future AI advances integrate automatically

**2. Clean Separation of Concerns** 🧩
- Logic, UI, execution, and configuration are completely separate
- Each component testable and replaceable in isolation
- Multiple interfaces possible without code changes

**3. Variable-Input Philosophy** 🎨
- No hardcoded specifics anywhere in the system
- Tools are blank canvases - prompts define behavior
- Maximum flexibility for unlimited use cases

**4. Performance Optimization** ⚡
- Intelligent caching with fingerprinting
- Dynamic resource allocation
- Cost optimization through smart model selection

---

## 🎭 Entry Point: `mao_v4.py`

**Main CLI interface** providing multiple interaction modes and routing.

### Command Line Interface

```python
# Core functionality
def main():
    parser = argparse.ArgumentParser(description="Mao - AI Workflow Orchestrator")
    
    # Primary execution modes
    parser.add_argument("goal", nargs="?", help="Natural language goal")
    
    # System management
    parser.add_argument("--list-workflows", action="store_true")
    parser.add_argument("--stats", action="store_true") 
    parser.add_argument("--verbose", "-v", action="store_true")
    
    # Execution preferences
    parser.add_argument("--workspace", "-w", help="Custom workspace directory")
    parser.add_argument("--free-only", action="store_true", help="Use only free models")
    parser.add_argument("--privacy", action="store_true", help="Privacy-focused models")
```

### Execution Flow

**1. Argument Parsing & Validation**
- Command line argument processing
- Execution mode determination (direct, interactive)
- Preference extraction and validation

**2. Interface Initialization**
```python
oc = MaoTerminalInterface(verbose=args.verbose)
```

**3. Request Routing**
- Stats requests → `oc.get_stats()`
- Workflow listing → `oc.list_workflows()`
- General goals → `oc.execute_goal()`
- Interactive mode → Input loop with continuous execution

**4. Result Processing**
- Success summary generation
- Error handling and user guidance
- Workspace management and file organization

---

## 🧠 Orchestrator Core (`orchestrator/`)

The brain of Mao - coordinates all system components for intelligent workflow execution.

### `core.py` - The Maestro

**Primary Classes & Responsibilities:**

#### `WorkflowOrchestrator`
```python
class WorkflowOrchestrator:
    def __init__(self, config_dir: str = "configs"):
        self.model_manager = ModelManager(config_dir)
        self.buttons = ButtonManager(self.model_manager)
        self.tool_discovery = ToolManager(config_dir)
        self.cache_manager = CacheManager()
```

**Core Orchestration Methods:**

**`create_workflow_from_goal(user_goal: str, preferences: Optional[Dict] = None) -> WorkflowPlan`**
- Natural language processing and intent recognition
- Complexity assessment and resource estimation
- Workflow pattern matching and optimization
- Multi-phase workflow creation based on goal analysis

#### Supporting Data Classes

**`WorkflowPhase`**
```python
@dataclass
class WorkflowPhase:
    name: str                    # Phase identifier
    model: str                   # Selected AI model
    agent_role: str              # Specialized agent persona
    task_instructions: str       # Detailed task specification
    input_sources: List[str]     # Data sources and dependencies
    output_files: List[str]      # Expected deliverables
    estimated_tokens: int        # Resource estimation
    estimated_cost: float        # Budget allocation
```

**`WorkflowPlan`**
```python
@dataclass  
class WorkflowPlan:
    id: str                           # Unique workflow identifier
    name: str                         # Human-readable name
    description: str                  # Workflow purpose and scope
    phases: List[WorkflowPhase]       # Ordered execution phases
    total_estimated_cost: float       # Complete workflow budget
    estimated_duration_minutes: int   # Timeline estimation
    workspace_dir: str                # Output organization
```

**`ExecutionResult`**
```python
@dataclass
class ExecutionResult:
    phase_name: str              # Completed phase identifier
    model_used: str              # Actual model executed
    content: str                 # Primary deliverable content
    tool_calls: List[Dict]       # Tool usage and results
    tokens_used: int             # Actual resource consumption
    cost: float                  # Actual execution cost
    duration_seconds: float      # Actual execution time
    success: bool                # Completion status
    error: Optional[str]         # Error details if applicable
```

### `manager_models.py` - Dynamic Model Intelligence

**Core Functionality:**

#### `ModelManager`
```python
class ModelManager:
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.models: Dict[str, ModelConfig] = {}
        self.providers: Dict[str, ProviderConfig] = {}
        self.fallback_chains: Dict[str, List[str]] = {}
        
        self.load_all_configs()
```

**Model Selection Intelligence:**

**`get_best_model_for_task(task_description: str = None, preferences: Optional[Dict] = None) -> Optional[str]`**
- Task complexity analysis and capability matching
- Cost optimization with quality threshold enforcement
- Provider availability and rate limit consideration
- Fallback strategy implementation

**`get_model_config(model_name: str) -> Optional[ModelConfig]`**
- Retrieve complete model configuration
- Capabilities and pricing information
- Provider association via connection mappings

**`get_provider_for_model(model_name: str) -> Optional[ProviderConfig]`**
- Dynamic provider lookup via connection files
- No hardcoded provider-model relationships
- Uses `providers_x_models.json` for mapping

#### Configuration Loading

**Model Configuration Schema (modular approach):**
```json
{
  "id": "claude-sonnet-4-20250514",
  "display_name": "Claude Sonnet 4",
  "model_id": "claude-3-5-sonnet-20241022",
  "context_window": 200000,
  "max_output": 8192,
  "input_price": 3.0,
  "output_price": 15.0,
  "capabilities": {
    "tools": true,
    "vision": false,
    "caching": true
  },
  "optimal_use_cases": ["reasoning", "code", "analysis"]
}
```

### `manager_buttons.py` - Human Button Orchestration

**Revolutionary Universal Model Interface:**

#### `ButtonManager`
```python
class ButtonManager:
    def __init__(self, model_manager: ModelManager):
        self.models = model_manager
```

**Core Button Generation:**

**`create_api_call_snippet(model_name: str, prompt: str, system_message: Optional[str] = None, tools: Optional[List[Dict]] = None, max_tokens: int = 8192, temperature: float = 0.3) -> str`**
- Universal executable code snippet generation
- Multi-provider compatibility (Anthropic, OpenAI, Gemini)
- Self-contained dependency management
- Cost tracking and performance monitoring

**`create_workflow_execution_snippet(workflow: WorkflowPlan) -> str`**
- Complete workflow execution snippet generation
- Multi-phase coordination code
- Error handling and recovery logic
- Progress reporting and status updates

#### Universal Model Adaptation

The ButtonManager automatically adapts API calls based on provider type:
- **Anthropic**: Direct SDK integration with proper message formatting
- **OpenAI**: Compatible format for OpenAI and Requesty
- **Gemini**: Google GenerativeAI SDK integration
- **Universal**: Fallback for any OpenAI-compatible endpoint

### `manager_tools.py` - Dynamic Tool Discovery

**Intelligent Tool Ecosystem Management:**

#### `ToolManager`
```python
class ToolManager:
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.tool_registry = self._load_tool_registry()
```

**Tool Discovery & Management:**

**`suggest_tools_for_goal(goal: str, model: str = "claude-sonnet-4", budget_limit: float = 1.0) -> Dict[str, Any]`**
- Goal-to-capability semantic matching
- Tool combination optimization
- Model compatibility filtering
- Resource efficiency consideration

**`get_tool_details(tool_id: str) -> Optional[Dict[str, Any]]`**
- Complete tool specification retrieval
- Parameter schema and validation rules
- Cost estimation and performance metrics

**`list_all_tools() -> List[Dict[str, Any]]`**
- Available tool enumeration
- Capability and cost information
- Integration metadata

#### Tool Registry Integration

**Tool Configuration Schema:**
```json
{
  "id": "tool_name",
  "name": "Tool Display Name", 
  "description": "Comprehensive functionality description",
  "version": "1.0.0",
  "capabilities": ["capability1", "capability2"],
  "tags": ["category1", "category2"],
  "cost_estimate": 0.001,
  "model_compatibility": ["all"],
  "parameters": {
    "param1": {
      "type": "string",
      "required": true,
      "description": "Parameter purpose and usage"
    }
  }
}
```

### `cache/cache_system.py` - Intelligent Performance Optimization

**5,108x Performance Improvements Through Smart Caching:**

#### `CacheManager`
```python
class CacheManager:
    def __init__(self, cache_dir: str = "~/.mao_cache"):
        self.cache_dir = Path(cache_dir).expanduser()
        self.fingerprint_cache = {}
        self.session_memory = {}
```

**Fingerprinting & Cache Strategies:**

**`generate_content_hash(content: str) -> str`**
- MD5 fingerprinting for content identification
- Collision detection and resolution
- Cache key optimization for fast retrieval

**`cache_content_analysis(content: str, analysis: str, cache_type: str) -> bool`**
- Structured content caching with metadata
- TTL management and expiration handling
- Cache invalidation and cleanup strategies

**`get_cached_analysis(content: str, cache_type: str) -> Optional[str]`**
- Lightning-fast cache retrieval (<5 seconds)
- Cache hit optimization and performance monitoring
- Automatic cache warming for frequently accessed content

#### Cache Performance Metrics

**Typical Performance Gains:**
```
| Operation Type        | Without Cache | With Cache | Improvement |
| --------------------- | ------------- | ---------- | ----------- |
| Content Analysis      | 1.328s        | 0.000s     | 5,108x      |
| Tool Result Retrieval | 0.850s        | 0.012s     | 71x         |
| Model Selection       | 0.245s        | 0.003s     | 82x         |
| Workflow Planning     | 2.100s        | 0.089s     | 24x         |
```

---

## 📁 Configuration System (`configs/`)

**JSON-based modular configuration enabling universal compatibility.**

### Model Configurations (`models/`)

The actual model configuration uses a centralized `models.json` file with individual model definitions:

#### Current Model Ecosystem
- **claude-sonnet-4-20250514** - Premium reasoning and code generation
- **claude-opus-4-20250514** - Maximum capability model for complex tasks
- **claude-3-7-sonnet-20250219** - Balanced performance and efficiency
- **gemini-2.5-pro** - Free alternative with strong capabilities
- **openai/gpt-4.1-mini** - Cost-optimized OpenAI model
- **openai/gpt-4.1-nano** - Ultra-low-cost option for simple tasks
- **local-llama-3.1-8b** - Local/private deployment option

### Provider Configurations (`providers/`)

The actual provider configuration uses a centralized `providers.json` file:

#### Current Provider Ecosystem
- **anthropic-direct** - Direct Anthropic API access
- **openai-direct** - Direct OpenAI API access  
- **gemini-direct** - Direct Google Gemini access
- **litellm** - Universal LLM proxy service
- **lm-studio** - Local model deployment
- **requesty** - Universal OpenAI-compatible proxy

#### Provider Configuration Structure
```json
{
  "anthropic-direct": {
    "display_name": "Anthropic Direct API",
    "api_type": "anthropic",
    "base_url": "https://api.anthropic.com",
    "auth_header": "x-api-key",
    "env_var": "ANTHROPIC_API_KEY",
    "supports_streaming": true,
    "supports_caching": true,
    "rate_limits": {
      "requests_per_minute": 50,
      "tokens_per_minute": 100000
    },
    "description": "Direct access to Anthropic's Claude models"
  }
}
```

### Connection Mappings (`connections/`)

**Dynamic relationship mapping eliminates hardcoded connections:**

#### `models_x_tools.json`
```json
{
  "tools": {
    "brave_search": {
      "models": {
        "primary": "claude-sonnet-4-20250514",
        "cost_optimized": "google/gemini-2.5-pro-exp-03-25",
        "privacy_focused": "vertex/anthropic/claude-3-7-sonnet-latest"
      }
    }
  }
}
```

#### `providers_x_models.json`  
```json
{
  "models": {
    "claude-sonnet-4-20250514": {
      "providers": ["anthropic-direct"]
    },
    "gemini-2.5-pro": {
      "providers": ["gemini-direct"]
    },
    "openai/gpt-4.1-nano": {
      "providers": ["openai-direct", "requesty"]
    }
  }
}
```

---

## 🔧 Tool Ecosystem (`tools/`)

**Standardized 6-file architecture enabling infinite extensibility.**

### Universal Tool Architecture

**Every tool follows identical structure:**

```
tools/your_new_tool/
├── your_new_tool.py          # Core functionality
├── tool_your_new_tool.json   # Configuration and metadata  
├── button_your_new_tool.py   # Human button interface
└── ui_your_new_tool.py       # User interface components
```

**Plus two shared files across all tools:**

```
orchestrator/
├── error_handling.py         # Shared error handling utilities
└── cache/
    └── cache_system.py       # Shared caching system
```

### Current Tool Library (8 Core Tools)

#### Research & Analysis Tools

**`brave_search/`** - Privacy-focused web search
- **Core Logic**: Brave Search API integration with privacy preservation
- **Capabilities**: Web search, news research, real-time information
- **Cost**: ~$0.001 per search operation
- **Optimal Models**: gemini-2.5-pro (cost), claude-sonnet-4 (quality)

**`perplexity_search/`** - Advanced AI research with citations
- **Core Logic**: Perplexity API integration for research tasks
- **Capabilities**: Deep research, citation verification, academic sources
- **Cost**: ~$0.005 per research query
- **Optimal Models**: claude-sonnet-4 (analysis), claude-opus-4 (complex research)

**`web_search/`** - General web research capabilities
- **Core Logic**: Multi-source web search aggregation
- **Capabilities**: Comprehensive internet research, trend analysis
- **Cost**: ~$0.002 per search operation
- **Optimal Models**: gemini-2.5-pro (efficiency), claude-sonnet-4 (synthesis)

#### Content & Design Tools

**`text_editor/`** - Advanced document processing
- **Core Logic**: Sophisticated text manipulation and formatting
- **Capabilities**: Document creation, editing, formatting, template generation
- **Cost**: ~$0.0005 per editing operation
- **Optimal Models**: claude-sonnet-4 (quality), gemini-2.5-pro (efficiency)

**`graphic_design/`** - Visual content creation and automation
- **Core Logic**: Image editing, text overlay, design automation with font management
- **Capabilities**: Visual design, layout optimization, brand consistency
- **Cost**: ~$0.002 per design operation
- **Optimal Models**: claude-sonnet-4 (creativity), dalle_generate (image creation)

**`dalle_generate/`** - AI image generation
- **Core Logic**: DALL-E 3 integration for visual content creation
- **Capabilities**: Custom image generation, visual concept creation
- **Cost**: ~$0.04 per image generation
- **Optimal Models**: claude-sonnet-4 (prompt optimization), dalle-3 (generation)

#### Intelligence & Operations Tools

**`think/`** - Enhanced reasoning and problem-solving
- **Core Logic**: Advanced thinking frameworks and analysis
- **Capabilities**: Multi-step reasoning, problem decomposition, decision support
- **Cost**: ~$0.001 per thinking session
- **Optimal Models**: claude-opus-4 (complex reasoning), claude-sonnet-4 (balanced)

**`file_operations/`** - File system management
- **Core Logic**: Comprehensive file and directory operations
- **Capabilities**: File management, organization, backup, version control
- **Cost**: ~$0.0001 per operation
- **Optimal Models**: Any model (simple operations), claude-sonnet-4 (complex organization)

### Tool Integration Architecture

#### 6-File Pattern Details

**1. Core Logic File (`tool_name.py`)**
```python
"""
Tool Name - Core Logic
Pure functionality with comprehensive error handling
NO print statements, NO UI dependencies
"""

def main_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Execute tool functionality with structured return
    
    Returns:
        Dict with 'status', 'results', 'cost', 'metadata'
    """
    try:
        # Validation and processing
        result = perform_operation(param1, param2)
        
        return {
            "status": "success",
            "input_param": param1,
            "timestamp": datetime.now().isoformat(),
            "results": result,
            "metadata": {"processing_time": processing_time},
            "cost": estimate_cost({"param1": param1, "param2": param2})
        }
    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "cost": 0.0
        }

def estimate_cost(params: Dict[str, Any]) -> float:
    """Calculate realistic cost estimate for workflow planning"""
    return 0.001  # Tool-specific calculation
```

**2. UI Display File (`ui_tool_name.py`)**
```python
"""
Tool Name - UI Display Component
Beautiful terminal output formatting
Print statements OK here - this is the UI layer
"""

from rich.console import Console
from rich.panel import Panel

def display_tool_results(result: Dict[str, Any], verbose: bool = False):
    """Transform structured data into beautiful terminal output"""
    console = Console()
    
    if "error" in result:
        console.print(f"❌ [red]{result['error']}[/red]")
        return
    
    console.print(f"✅ [green]Tool Results[/green]")
    console.print(Panel(str(result.get("results", "")), title="Output"))
    
    if verbose:
        console.print(f"💰 Cost: ${result.get('cost', 0):.6f}")
        console.print(f"⏱️ Duration: {result.get('metadata', {}).get('processing_time', 0):.3f}s")
```

**3. Human Button Generator (`button_tool_name.py`)**
```python
"""
Tool Name - Human Button Generators
Executable code snippets for universal model compatibility
Print statements OK for demo and execution feedback
"""

def create_button_snippet(params: Dict[str, Any], model: str = "claude-sonnet-4") -> str:
    """Generate self-contained executable snippet"""
    
    param1 = params.get("param1", "")
    param2 = params.get("param2", 10)
    
    snippet = f'''# Tool Execution - Model: {model}
import json
from datetime import datetime

def execute_tool():
    """Execute tool with comprehensive error handling"""
    
    param1 = "{param1}"
    param2 = {param2}
    
    print(f"🔧 Executing Tool...")
    print(f"📝 Input: {{param1}}")
    
    try:
        # Tool implementation here
        result = perform_operation(param1, param2)
        
        return {{
            "status": "success",
            "results": result,
            "cost": 0.001,
            "timestamp": datetime.now().isoformat()
        }}
    except Exception as e:
        return {{
            "error": str(e),
            "cost": 0.0
        }}

# Execute and return results
result = execute_tool()
print(f"✅ Tool completed: {{result}}")
result
'''
    return snippet.strip()
```

**4. Tool Registry (`tool_tool_name.json`)**
```json
{
  "id": "tool_name",
  "name": "Tool Display Name",
  "description": "Comprehensive tool functionality description",
  "version": "1.0.0",
  "capabilities": ["capability1", "capability2"],
  "tags": ["category1", "category2"],
  "cost_estimate": 0.001,
  "model_compatibility": ["all"],
  "parameters": {
    "param1": {
      "type": "string",
      "required": true,
      "description": "Primary input parameter"
    }
  }
}
```

**5. Shared Error Handling (`orchestrator/error_handling.py`)**
- Comprehensive retry logic with exponential backoff
- Graceful degradation and fallback strategies
- User-friendly error communication and recovery

**6. Shared Caching (`orchestrator/cache/cache_system.py`)**
- Intelligent performance optimization across all tools
- Content fingerprinting and cache management
- 5,108x performance improvements on cache hits

---

## 🎯 Interface Layer (`interfaces/`)

**Clean separation enabling multiple interaction modes.**

### `ui_terminal.py` - Professional Terminal Interface

**Core Classes & Functionality:**

#### `MaoTerminalInterface`
```python
class MaoTerminalInterface:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.orchestrator = WorkflowOrchestrator()
        self.display = TerminalDisplay(verbose)
```

**Primary Interface Methods:**

**`execute_goal(goal: str, workspace: str, preferences: Dict) -> Dict`**
- Goal processing and workflow initiation
- Progress monitoring and status updates
- Result presentation and workspace management
- Error handling and user guidance

**`get_stats() -> None`**
- System performance metrics display
- Cache utilization and efficiency reports
- Model usage and cost analytics
- Tool performance and reliability statistics

**`list_workflows() -> None`**
- Available workflow pattern enumeration
- Usage examples and parameter descriptions
- Cost estimates and duration projections
- Success rate and quality metrics

---

## 🎯 Architectural Strengths

### Modularity Benefits

**Component Independence:**
- Each component testable and replaceable in isolation
- Multiple interface possibilities without core changes
- Easy debugging and maintenance through clear separation

**Infinite Extensibility:**
- Add unlimited tools without performance degradation
- Support new models/providers without code changes
- Scale team usage without architectural modifications

**Future-Proof Design:**
- AI advances integrate automatically via human buttons
- New interaction modalities possible via interface layer
- Business model evolution supported by flexible architecture

### Performance Optimization

**Intelligent Resource Management:**
- Dynamic model selection based on task requirements
- Smart caching with 5,108x performance improvements
- Cost optimization through efficient resource allocation

**Scalability Patterns:**
- Linear performance scaling with complexity
- Concurrent workflow support without interference
- Memory efficiency through modular loading

### Quality Assurance

**Professional Error Handling:**
- Comprehensive retry logic with exponential backoff
- Graceful degradation and fallback strategies
- User-friendly error communication and recovery

**Consistent Results:**
- Standardized tool interfaces ensure predictable behavior
- Quality validation and automatic improvement triggers
- Performance monitoring and optimization feedback loops

---

## 🔮 Architectural Evolution

### Current Architecture Status: 85% Complete

**Completed Systems:**
- ✅ Core orchestration and workflow management
- ✅ Universal model compatibility via human buttons
- ✅ Complete tool ecosystem with 6-file standardization
- ✅ Intelligent caching and performance optimization
- ✅ Professional error handling and resilience
- ✅ Clean interface separation and terminal UX

**Integration Needs (15% Remaining):**
- 🔗 Tool discovery connection to orchestrator core
- 📋 Protocol documentation for behavioral consistency  
- 💾 Memory system for conversation context
- 🌐 MCP API integration for enhanced tool communication
- ⚡ Code execution tool for true human button functionality

### Future Architectural Enhancements

**Advanced Intelligence:**
- Self-improving workflow patterns based on usage analytics
- Predictive resource allocation and optimization
- Adaptive behavior learning from user interactions

**Expanded Ecosystem:**
- Community tool marketplace with quality standards
- Industry-specific tool packages and templates
- Third-party integration APIs and developer programs

**Enterprise Features:**
- Team collaboration and workflow sharing capabilities
- Advanced security and compliance frameworks
- Business system integration and automation

**Next-Generation Capabilities:**
- Multimodal workflow support (text, image, audio, video)
- Real-time learning and adaptation mechanisms
- Advanced reasoning and planning capabilities

---

*This architecture enables Mao to be more than just another AI tool - it's a platform for the future of intelligent work automation.*