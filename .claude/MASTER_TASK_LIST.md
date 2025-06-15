# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)


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