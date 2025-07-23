# User Flow 
## The Complete Mao Experience



---

## New User Experience

### First Time Setup

**Getting Started**: Download Mao, run the installer, and you're ready to begin. The system handles user configuration, model setup, and tool access automatically.

**Quick Onboarding**: Mao introduces itself and walks you through creating your first workflow. The conversation feels natural - just describe what you want to accomplish, and Mao handles the technical complexity.

### Your First Workflow

**Natural Conversation**: "I need to create a marketing strategy for my startup." That's it. Mao analyzes your goal, asks clarifying questions, and begins building a multi-phase workflow.

**Intelligent Planning**: Behind the scenes, Mao breaks your goal into phases, assigns appropriate AI agents, and sets up progress tracking. You see the plan and can approve or modify it before execution.

**Real-Time Execution**: Watch as different phases run in parallel. Get live updates, see progress indicators, and interact with the process when needed. The system manages complexity while keeping you informed.

**Quality Results**: Receive comprehensive deliverables organized exactly how you need them. Everything is tracked, saved, and available for future reference or iteration.

---

## Session Management & Memory

### Persistent Context

**Always On The Same Page**: Mao remembers everything about your projects, preferences, and working style. Start conversations mid-thought, and Mao picks up exactly where you left off.

**Smart Context Switching**: Work on multiple projects simultaneously. Mao maintains separate contexts and switches seamlessly based on your current focus.

**Learning Your Style**: Over time, Mao learns your communication patterns, quality standards, and business priorities. Each interaction becomes more personalized and efficient.

### Cross-Session Continuity 

**Project Memory**: Every workflow, decision, and outcome is remembered. Return to projects weeks later, and Mao provides complete context and suggests next steps.

**Pattern Recognition**: Mao identifies recurring workflows and suggests templates. Your marketing processes become reusable assets that improve over time.

What the experience will look like. What they will need to do, or how little they'll need to do. We touch on how Mao is able to always be on the same page using the Memory MCP tool as well as Workflow ID. 

| **ARCHITECTURE SECTION: Session Management & Memory System** |
| ------------------------------------------------------------ |

### Memory MCP Integration Architecture

The session management system relies on the **Memory MCP (Model Context Protocol)** server to maintain persistent workflow state and user context across sessions. This creates seamless continuity that feels magical to users but operates on solid technical foundations.

#### Core Memory Management Components

```python
# orchestrator/memory_mcp.py - Memory integration hub
class MemoryMCPManager:
    def __init__(self):
        self.memory_client = MemoryMCPClient()
        self.cache = CacheManager()
        
    async def save_workflow_context(self, workflow_id: str, context: Dict[str, Any]):
        """Save complete workflow state to knowledge graph"""
        workflow_entity = {
            "name": f"workflow_{workflow_id}",
            "type": "workflow_context",
            "observations": [
                f"Goal: {context['goal']}",
                f"Status: {context['status']}",
                f"Current Phase: {context['current_phase']}",
                f"Deliverables: {json.dumps(context['deliverables'])}"
            ]
        }
        await self.memory_client.create_entities([workflow_entity])
        
    async def restore_workflow_context(self, workflow_id: str) -> Dict[str, Any]:
        """Restore workflow state from knowledge graph"""
        nodes = await self.memory_client.search_nodes(f"workflow_{workflow_id}")
        return self._parse_workflow_context(nodes)
```

#### Session State Persistence

```python
# orchestrator/user_memory_manager.py - User session management
class UserMemoryManager:
    def __init__(self, username: str):
        self.username = username
        self.user_config_path = f"configs/user/{username}/user_{username}.json"
        self.memory_mcp = MemoryMCPManager()
        
    def save_session_state(self, session_data: Dict[str, Any]):
        """Persist current session context"""
        session_entity = {
            "name": f"session_{self.username}_{datetime.now().isoformat()}",
            "type": "user_session",
            "observations": [
                f"Active workflows: {session_data['active_workflows']}",
                f"Current focus: {session_data['current_focus']}",
                f"Preferences: {json.dumps(session_data['preferences'])}"
            ]
        }
        self.memory_mcp.create_entities([session_entity])
        
    def get_user_context(self) -> Dict[str, Any]:
        """Retrieve complete user context for session restoration"""
        user_nodes = self.memory_mcp.search_nodes(f"session_{self.username}")
        return self._compile_user_context(user_nodes)
```

#### Workflow ID System Architecture

```python
# orchestrator/workflow_manager.py - Workflow identification and tracking
class WorkflowManager:
    def generate_workflow_id(self) -> str:
        """Generate unique workflow identifier"""
        import uuid
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"wf-{timestamp}-{unique_id}"
        
    def create_workflow_context(self, goal: str, user_id: str) -> Dict[str, Any]:
        """Create initial workflow context with memory integration"""
        workflow_id = self.generate_workflow_id()
        context = {
            "workflow_id": workflow_id,
            "user_id": user_id,
            "goal": goal,
            "created_at": datetime.now().isoformat(),
            "status": "planning",
            "phases": [],
            "memory_context": {}
        }
        
        # Save to Memory MCP immediately
        self.memory_mcp.save_workflow_context(workflow_id, context)
        return context
```

#### Cross-Session Data Flow

The memory system creates a continuous data flow that persists across sessions:

1. **Session Start**: System queries Memory MCP for user context and active workflows
2. **Ongoing Work**: All interactions, decisions, and progress automatically saved to knowledge graph
3. **Session End**: Current state persisted with timestamp and context markers
4. **Session Resume**: Previous context restored with full workflow state and user preferences

This architecture enables the "always on the same page" experience that makes Mao feel like a persistent team member rather than a stateless tool.

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

---

## The Workflow's JSON Config
 
When chatting with Mao, you will be helping them to fill out a JSON config file. This is basically a prompt that has been broken down into variables. Use the `/variables` command to remind yourself what you need to tell Mao. 

```bash
/variables # Shows the variables that are needed 
/variables-explain # Shows the variables that are needed with an explanation 
```

### JSON Config File Variables Described 

| **VARIABLE**         | **DESCRIPTION**                                               |
| -------------------- | ------------------------------------------------------------- |
| user_id              | User ID of Username creating the workflow                     |
| workflow_id          | Workflow ID created at start of planning                      |
| custom_command       | Custom command to execute workflow                            |
| workflow_goal        | Goal statement of entire workflow project                     |
| workflow_deliverable | Final deliverables of entire workflow project                 |
| workflow_description | Description of workflow to complete project                   |
| phase_number         | Count of phases as they're added to workflow                  |
| phase_goal           | Goal statement of the phase's assigned task                   |
| phase_deliverable    | Deliverable of the phase's assigned task                      |
| phase_description    | Description of the phase's assigned task                      |
| resources            | Resources the agent can use to complete the phase's tasks     |
| tools                | Tools the agent can use to complete the phase's tasks         |
| model_1              | Choice model to be the agent of this phase                    |
| model_2              | Backup model agent should choice agent be unavailable         |
| model_3              | Fail-safe model agent should choice and backup be unavailable |
| provider_1           | Provides for the choice model                                 |
| provider_2           | Provider for the backup model                                 |
| provider_3           | Provider for the fail-safe model                              |
| handoff_number       | Count of the handoffs as they're added to the workflow        |
| assessment_questions | Questions to assess if the deliverable is complete            |
| human_in_loop        | Whether the orchestrator should get human feedback            |


### Three JSON Config Schemas In A Workflow

We'll touch on the basics of the JSON config file and the three JSON objects that are created when a workflow is created before jumping into the technical details in an architecture section.

* **JSON Config Schema Templates** 

  - 1. WORKFLOW: `./templates/workflows/example-workflow_workflow_config.json`
  - 2. PHASE: `./templates/workflows/example-workflow_phase_config.json`
  - 3. HANDOFF: `./templates/workflows/example-workflow_handoff_config.json`

* **HELPER:** `./templates/workflows/README.md`

#### 1. The WORKFLOW JSON Object 

This is the first JSON object that is created when a workflow is created. It contains the workflow's goal, deliverable, description, and other details. Each project's workflow has only one workflow JSON object. It is the JSON object that holds together all the other JSON objects. 

#### 2. The PHASE JSON Object 

This is the second JSON object that is created when a workflow is created. It contains a task needed to be completed to achieve the workflow's goal. Just like the workflow, each phase has a goal, deliverable, description, and specific details for the agent. The objects are tied together by the workflow_id. Phases are numbered sequentially, starting with 01, 02, 03, etc. If there are agents running in parallel, they will share the same phase_number, appended with an underscore and a letter, a, b, c, etc. 

#### 3. The HANDOFF JSON Object 

This is the third type of JSON object. Since Mao is orchestrating the entire workflow, even though they have delegated the tasks to various agents, they will be present for every handoff of deliverables. When an Agent is complete, they call Mao to hand off the deliverable. The deliverable object provides a list of questions that the Orchestrator will use to assess if the deliverable is complete. 

**NOTE:** It is VERY common and highly encouraged that Mao leave the final phase of workflows that deal with creative subject matter completely open. When the Agent completes their deliverable, Mao is able to assess it on the spot and make a decision as to what the next step in the flow should be. This is pushed heavily because it is so very natural to how a human would do it on their own. 

Similarly, Mao may decide the Agent's deliverables are not acceptable; not up to par. In this case they may use a command to change the workflow instead up updating it, though the result is similar, a new agent is tasked and called and the flow continues until completion. 

We'll touch on the specifics of how to setup, edit, or fix a workflow via JSON objects after this architecture section. 

---

| **ARCHITECTURE SECTION: JSON Configuration System** |
| --------------------------------------------------- |

### 3-Type JSON Workflow Architecture

The Mao workflow configuration system uses a modular approach with three distinct JSON object types that work together to define, execute, and manage complex workflows. This architecture provides maximum flexibility while maintaining clear separation of concerns.

#### Core Configuration Components

```python
# orchestrator/conversation_bridge.py - JSON config generation
class WorkflowConfigGenerator:
    def __init__(self):
        self.template_path = "templates/workflows/"
        self.temp_path = "configs/workflows/.temp/"
        
    def create_workflow_config(self, user_goal: str, user_id: str) -> Dict[str, Any]:
        """Generate workflow configuration from natural language goal"""
        workflow_id = self.generate_workflow_id()
        
        # Parse goal into structured components
        parsed_goal = self.analyze_goal(user_goal)
        
        workflow_config = {
            "workflow": [{
                "user_id": user_id,
                "workflow_id": workflow_id,
                "custom_command": self.generate_command_name(parsed_goal),
                "workflow_goal": parsed_goal['goal'],
                "workflow_deliverable": parsed_goal['deliverable'],
                "workflow_description": parsed_goal['description'],
                "temp_directory": f"{self.temp_path}{workflow_id}/"
            }]
        }
        
        return workflow_config
```

#### Phase Configuration Generation

```python
# orchestrator/phase_manager.py - Dynamic phase creation
class PhaseConfigManager:
    def generate_phase_configs(self, workflow_goal: str, complexity_analysis: Dict) -> List[Dict]:
        """Create phase configurations based on goal complexity"""
        phases = []
        
        # Analyze goal to determine required phases
        phase_requirements = self.decompose_goal(workflow_goal, complexity_analysis)
        
        for idx, phase_req in enumerate(phase_requirements, 1):
            phase_config = {
                "phase": [{
                    "workflow_id": workflow_goal['workflow_id'],
                    "phase_number": f"{idx:02d}",
                    "phase_goal": phase_req['goal'],
                    "phase_deliverable": phase_req['deliverable'],
                    "phase_description": phase_req['description'],
                    "resources": phase_req['resources'],
                    "tools": self.select_optimal_tools(phase_req),
                    "model_1": self.select_primary_model(phase_req),
                    "model_2": self.select_backup_model(phase_req),
                    "model_3": self.select_fallback_model(phase_req),
                    "provider_1": self.get_model_provider("model_1"),
                    "provider_2": self.get_model_provider("model_2"),
                    "provider_3": self.get_model_provider("model_3")
                }]
            }
            phases.append(phase_config)
            
        return phases
```

#### Handoff Assessment Architecture

```python
# orchestrator/handoff_manager.py - Quality control and progression
class HandoffConfigManager:
    def create_handoff_configs(self, phases: List[Dict]) -> List[Dict]:
        """Generate handoff configurations for quality assessment"""
        handoffs = []
        
        for phase in phases:
            handoff_config = {
                "handoff": [{
                    "workflow_id": phase['workflow_id'],
                    "handoff_number": phase['phase_number'],
                    "assessment_questions": self.generate_assessment_questions(
                        phase['phase_deliverable']
                    ),
                    "human_in_loop": self.determine_human_review_need(phase),
                    "quality_criteria": self.define_quality_standards(phase),
                    "continuation_logic": self.setup_flow_control(phase)
                }]
            }
            handoffs.append(handoff_config)
            
        return handoffs
```

#### Template System Integration

```json
// templates/workflows/example-workflow_workflow_config.json
{
  "workflow": [
    {
      "user_id": "user-REPLACE_WITH_YOUR_USER_ID",
      "workflow_id": "uid-REPLACE_WITH_GENERATED_ID", 
      "custom_command": "example workflow",
      "workflow_goal": "Create a comprehensive example workflow that demonstrates the 3-type JSON system",
      "workflow_deliverable": "Example workflow report with findings and recommendations",
      "workflow_description": "This example workflow shows how to structure a multi-phase workflow using the new JSON system. Replace this description with your specific workflow details.",
      "temp_directory": "configs/workflows/.temp/example-workflow/",
      "created_at": "REPLACE_WITH_CURRENT_TIMESTAMP"
    }
  ]
}
```

#### Configuration Data Flow

The 3-type JSON system creates a structured workflow creation pipeline:

1. **Goal Analysis**: Natural language processed into structured workflow requirements
2. **Template Processing**: Base templates populated with goal-specific data
3. **Configuration Generation**: Three JSON objects created with proper ID linking
4. **Validation**: Comprehensive JSON schema validation and dependency checking
5. **Storage**: Configurations saved to temp directory for user review
6. **Deployment**: Final configurations moved to active workflow directory upon approval

This modular approach allows for easy modification, testing, and reuse of workflow components while maintaining consistency and reliability across all workflow types.

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

### **WORKFLOW** JSON Object 

- This is the first JSON object that is created when a workflow is created 
- It contains the workflow's goal, deliverable, description, and other details 
- Each project's workflow has only one workflow JSON object 
- The 'goal', 'deliverable', and 'description' are all items that will be broken down into the phases 
- The objects are tied together by the workflow_id 
- While building the workflow, the temp_directory is used to store the JSON objects, the management of this file is explained later

```json
{
  "workflow": [
    {
      "user_id": "user-0663",
      "workflow_id": "uid-qmt-465",
      "custom_command": "marketing strategy startup",
      "workflow_goal": "Create comprehensive marketing strategy for my fintech startup",
      "workflow_deliverable": "Marketing strategy report",
      "workflow_description": "Identify what is needed to complete the goal. Build a workflow that delegates the work to the appropriate agents, having them work in parallel if needed. Leave the last phase opened-ended. Detail that handoff before the last phase with a list of questions Orchestrator will use to assess if the deliverable is complete, and if not, what is needed to complete it.",
      "temp_directory": "configs/workflows/.temp/marketing-strategy-startup/"
    }
  ]
}
```

### **PHASE** JSON Object 

- This is the second JSON object that is created when a workflow is created 
- It contains a task needed to be completed to achieve the workflow's goal 
- Just like the workflow, each phase has a goal, deliverable, description, and specific details for the agent 
- The objects are tied together by the workflow_id 
- Phases are numbered sequentially, starting with 01, 02, 03, etc. 
- If there are agents running in parallel, they will share the same phase_number, appended with an underscore and a letter, a, b, c, etc. 

```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01",
      "phase_goal": "Market research",
      "phase_deliverable": "Market research report",
      "phase_description": "Research target market. Explore demographics in all socioeconomic status ranges, all geo-locations, all education level, but only females, married, and with a birthday coming up in the next 5 months. Research competitors; detail their marketing strategy. Research trends in the industry that could affect the marketing strategy. Generate a report with findings and recommendations.",
      "resources": ["Files in /resources/marketing/", "https://example.com/market-data"],
      "tools": ["web_search", "perplexity_search", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-opus-4", 
      "model_3": "gpt-4.1-mini",
      "provider_1": "anthropic-direct",
      "provider_2": "anthropic-direct",
      "provider_3": "openai-direct"
    }
  ]
}
```

### **HANDOFF** JSON Object 

- This is the third type of JSON object
- Since Mao is orchestrating the entire workflow, even though they have delegated the tasks to various agents, they will be present for every handoff of deliverables
- When an Agent is complete, they call Mao to hand off the deliverable
- The deliverable object provides a list of questions that the Orchestrator will use to assess if the deliverable is complete
- The human_in_loop field determines whether the user should review and approve before continuation

```json
{
  "handoff": [
    {
      "workflow_id": "uid-qmt-465",
      "handoff_number": "01",
      "assessment_questions": [
        "Does the report include comprehensive demographic analysis?",
        "Are competitor strategies clearly documented?",
        "Are industry trends identified and analyzed?",
        "Does the report include actionable recommendations?"
      ],
      "human_in_loop": false
    }
  ]
}
```

---

## Creating Workflows

### The Setup Process

**Conversation-Driven Planning**: Simply tell Mao what you want to accomplish. "Create a social media content calendar for my consulting business." Mao asks clarifying questions and builds the workflow structure.

**Review and Approval**: See the complete workflow plan before execution. Modify phases, adjust tools, or change approaches. Everything is transparent and customizable.

**One-Command Execution**: Once approved, your workflow becomes a custom command. Run `social-media-calendar` anytime to execute the complete workflow with your current context.

### Workflow Management

**Live Monitoring**: Watch phases execute in real-time. See which agents are working, what tools they're using, and how progress is advancing.

**Dynamic Adjustment**: Workflows adapt as they run. If an agent discovers new requirements, Mao can modify the workflow mid-execution with your approval.

**Quality Control**: Built-in assessment points ensure deliverables meet your standards before proceeding to the next phase.

| **ARCHITECTURE SECTION: Workflow Creation & Execution** |
| ------------------------------------------------------- |

### Workflow Setup Script Architecture

The workflow setup process transforms JSON configurations into executable custom commands through an automated script system that handles directory creation, command installation, and workflow deployment.

#### Core Setup Script Components

```bash
# scripts/workflow_setup/workflow_setup.sh - Main setup orchestration
#!/bin/bash

setup_workflow() {
    local WORKFLOW_NAME="$1"
    local USER_ID="$2"
    local WORKFLOW_ID="$3"
    
    # Define directory structure
    WORKFLOW_DIR="configs/workflows/$WORKFLOW_NAME"
    TEMP_DIR="configs/workflows/.temp/$WORKFLOW_NAME"
    COMMAND_PATH="$HOME/bin/$WORKFLOW_NAME"
    
    echo "Setting up workflow: $WORKFLOW_NAME"
    
    # Create workflow directory structure
    mkdir -p "$WORKFLOW_DIR"/{config-files,deliverables,metadata}
    
    # Process JSON configurations
    process_json_configs "$TEMP_DIR" "$WORKFLOW_DIR/config-files"
    
    # Generate custom command
    create_custom_command "$WORKFLOW_NAME" "$WORKFLOW_ID" "$COMMAND_PATH"
    
    # Generate README
    create_workflow_readme "$WORKFLOW_DIR" "$WORKFLOW_NAME" "$WORKFLOW_ID"
    
    # Clean up temp directory
    rm -rf "$TEMP_DIR"
    
    echo "✅ Workflow setup complete: $WORKFLOW_NAME"
}

process_json_configs() {
    local TEMP_DIR="$1"
    local CONFIG_DIR="$2"
    
    # Copy and rename JSON configurations
    cp "$TEMP_DIR/workflow_config.json" "$CONFIG_DIR/${WORKFLOW_NAME}_workflow_config.json"
    cp "$TEMP_DIR/phase_config.json" "$CONFIG_DIR/${WORKFLOW_NAME}_phase_config.json" 
    cp "$TEMP_DIR/handoff_config.json" "$CONFIG_DIR/${WORKFLOW_NAME}_handoff_config.json"
    
    echo "📄 JSON configurations processed"
}

create_custom_command() {
    local WORKFLOW_NAME="$1"
    local WORKFLOW_ID="$2" 
    local COMMAND_PATH="$3"
    
    # Generate executable command script
    cat > "$COMMAND_PATH" << EOF
#!/bin/bash
# Auto-generated workflow command: $WORKFLOW_NAME
# Workflow ID: $WORKFLOW_ID

echo "🚀 Executing workflow: $WORKFLOW_NAME"
echo "📋 Workflow ID: $WORKFLOW_ID"

# Call MAO orchestrator with workflow configuration
python3 -c "
import sys
sys.path.append('$(pwd)')
from orchestrator.core import WorkflowOrchestrator

try:
    orchestrator = WorkflowOrchestrator()
    workflow_result = orchestrator.execute_workflow('$WORKFLOW_ID')
    print('✅ Workflow completed successfully')
    print(f'📊 Results: {workflow_result}')
except Exception as e:
    print(f'❌ Workflow execution failed: {e}')
    sys.exit(1)
"
EOF

    chmod +x "$COMMAND_PATH"
    echo "🔧 Custom command created: $WORKFLOW_NAME"
}
```

#### Python Orchestrator Integration

```python
# orchestrator/workflow_state.py - Workflow execution coordination
class WorkflowExecutor:
    def __init__(self):
        self.memory_mcp = MemoryMCPManager()
        self.cache = CacheManager()
        self.phase_manager = PhaseManager()
        
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute complete workflow from configurations"""
        
        # Load workflow configurations
        workflow_config = self.load_workflow_config(workflow_id)
        phase_configs = self.load_phase_configs(workflow_id)
        handoff_configs = self.load_handoff_configs(workflow_id)
        
        # Initialize execution context
        execution_context = {
            "workflow_id": workflow_id,
            "status": "executing",
            "current_phase": 1,
            "results": {},
            "start_time": datetime.now().isoformat()
        }
        
        # Execute phases sequentially
        for phase_config in phase_configs:
            phase_result = await self.execute_phase(phase_config, execution_context)
            
            # Quality assessment at handoff
            handoff_config = self.get_handoff_config(phase_config['phase_number'])
            assessment_result = await self.assess_deliverable(phase_result, handoff_config)
            
            if assessment_result['approved']:
                execution_context['results'][phase_config['phase_number']] = phase_result
                execution_context['current_phase'] += 1
            else:
                # Handle quality issues - retry or human intervention
                await self.handle_quality_issues(phase_config, assessment_result)
                
        # Finalize workflow
        execution_context['status'] = "completed"
        execution_context['end_time'] = datetime.now().isoformat()
        
        # Save final results to Memory MCP
        await self.memory_mcp.save_workflow_results(workflow_id, execution_context)
        
        return execution_context
        
    async def execute_phase(self, phase_config: Dict, context: Dict) -> Dict[str, Any]:
        """Execute individual phase with model fallback"""
        
        # Try models in priority order
        models = [
            (phase_config['model_1'], phase_config['provider_1']),
            (phase_config['model_2'], phase_config['provider_2']), 
            (phase_config['model_3'], phase_config['provider_3'])
        ]
        
        for model, provider in models:
            try:
                agent = self.create_agent(model, provider, phase_config['tools'])
                result = await agent.execute_task(
                    goal=phase_config['phase_goal'],
                    description=phase_config['phase_description'],
                    resources=phase_config['resources']
                )
                
                # Success - return result
                return {
                    "phase_number": phase_config['phase_number'],
                    "status": "completed",
                    "model_used": model,
                    "deliverable": result,
                    "execution_time": result.get('execution_time'),
                    "cost": result.get('cost')
                }
                
            except Exception as e:
                # Log error and try next model
                self.log_model_failure(model, provider, str(e))
                continue
                
        # All models failed
        raise Exception(f"Phase {phase_config['phase_number']} failed on all models")
```

#### CLI Integration Architecture

```python
# configs/cli/setup/setup.py - CLI workflow setup integration
class SetupCommand:
    def __init__(self):
        self.workflow_manager = WorkflowManager()
        self.setup_script_path = "scripts/workflow_setup/workflow_setup.sh"
        
    def execute_setup(self, args: List[str]) -> Dict[str, Any]:
        """Execute workflow setup from CLI"""
        
        if not args:
            return self.interactive_setup()
            
        # Parse setup arguments
        setup_type = args[0]
        
        if setup_type == "workflow":
            return self.setup_workflow_from_temp()
        elif setup_type == "validate":
            return self.validate_temp_configs()
        else:
            return {"error": "Unknown setup type"}
            
    def setup_workflow_from_temp(self) -> Dict[str, Any]:
        """Process temp JSON configs into executable workflow"""
        
        temp_dir = "configs/workflows/.temp/"
        temp_workflows = self.scan_temp_directory(temp_dir)
        
        if not temp_workflows:
            return {"error": "No temp workflows found"}
            
        # Process each temp workflow
        results = []
        for workflow_name in temp_workflows:
            try:
                # Validate JSON configurations
                validation_result = self.validate_workflow_configs(workflow_name)
                if not validation_result['valid']:
                    results.append({
                        "workflow": workflow_name,
                        "status": "validation_failed",
                        "errors": validation_result['errors']
                    })
                    continue
                    
                # Execute setup script
                setup_result = self.execute_setup_script(workflow_name)
                results.append({
                    "workflow": workflow_name,
                    "status": "success",
                    "command": setup_result['custom_command'],
                    "directory": setup_result['workflow_directory']
                })
                
            except Exception as e:
                results.append({
                    "workflow": workflow_name,
                    "status": "error",
                    "error": str(e)
                })
                
        return {"setup_results": results}
```

This architecture seamlessly bridges natural language goals to executable workflows through the 3-type JSON system, automated setup scripts, and integrated CLI commands. The result is a system that feels conversational but operates on robust technical foundations.

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

---

## Advanced Workflow Features

### Parallel Execution

**Multi-Agent Coordination**: Complex workflows run multiple phases simultaneously. Research agents work in parallel with content creation agents, coordinating through Mao's orchestration.

**Resource Management**: Intelligent scheduling prevents conflicts and optimizes performance. Expensive API calls are batched and cached for efficiency.

### Dynamic Adaptation

**Intelligent Pivoting**: Workflows adjust based on intermediate results. If market research reveals unexpected insights, Mao can modify the strategy phases automatically.

**Quality-Driven Flow**: Built-in quality checkpoints ensure each phase meets standards before continuation. Failed phases trigger automatic retry with different approaches.

### Business Integration

**Cost Consciousness**: Every workflow tracks costs and optimizes for efficiency. Set budgets and receive alerts when approaching limits.

**Brand Consistency**: Mao learns your brand voice, visual style, and quality standards. All outputs maintain consistency across projects and time.

**Scalability**: Start with simple workflows and gradually increase complexity. The system grows with your business needs and sophistication.

---

## The Complete Experience

From initial idea to final deliverable, Mao transforms workflow orchestration from a technical challenge into a natural conversation. The sophisticated architecture remains invisible to users, who experience only the intelligence, reliability, and results they need to accelerate their business goals.

**This is the future of work**: AI agents that understand context, maintain memory, and deliver consistent quality while you focus on strategy and growth.
