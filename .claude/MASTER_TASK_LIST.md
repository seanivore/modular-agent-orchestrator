# Master Task List
Mao v4.0.0.0 (Modular Agent Orchestrator)

|----------------------|
| **SESSION 18 TASKS** |
| -------------------- |

# **Need To Audit `mao_v4.py` File**

## Updated Code "OC" to "MAO"

oc.get_stats --> mao.get_stats
oc.list_workflows --> mao.list_workflows
oc.job_application_workflow --> mao.job_application_workflow
oc.display.success_summary --> mao.display.success_summary

### Also On This File 

- Print functions 
- Specifics about job applications 
- Mentions of args that are specific 


-----------------

# **Walk Through of UX Flow**

Needs to be completed. 

## Branding Updates 

- It is no longer 'Mao' it is 'Mao' to encourage proper pronunciation of the product (a find and replace across codebase has already been run)
- I'm not using the word 'human buttons' anymore, I'm calling them 'button snippets' just FYI

## Setup Script & Terminal UX Application Considerations 

**Important difference from before:** Very often a work flow will need to be changed. Ideally we're going to have Claude Orchestrator creating workflows without and endpoint, meaning we'll need a way for them to easily add a next phase, etc. in a similar way to how setup of a full workflow works. 

### Terminal Application 

1. Activation of Mao should be more like Claude Code, more like an application 
2. Activate the application and the UI can ask you right at the start what you need to do 
   - New Use-Case, Lazy Setup 
   - New Use-Case, Invested Setup 
   - Active Use-Case that you need to update or make changes to 
3. We need to consider how something like this is built modular 
   - It would be valuable to have in the future 
   - But only if we know how to build something like this while making sure we have room for future updates 
   - What might those updates be? 
     - UI choices like a pretty text entry field when Claude asks for a variable 
     - Ability to easily review a use-case JSON variable configs in digital form 
     - Easy way to select what LLM you want if you have a preference because they're listed 
     - We could even set it up to handle creation of new models or providers, maybe even tools 
     - Eventually, in using it to add new tools, it could help create them, using Claude Code SDK to build the tool on the fly 

### Setup Script 

1. Let's go all out with the args 
   - What is helpful 
   - What did we have before 
   - What should we leave room for in the future 
2. As arg ideally, or other script 
   - We need simple way for workflows to be updated 
   - Most will be created without final phases 
   - Orchestrator Claude will create final phases after reviewing previous tasks 
   - The setup should be very similar to the normal setup script 

# Mao UX Flow 

## Use-Case Workflow Setup or Activate 

### New Use-Case, Lazy Setup 

1. User runs command `mao chat` 
2. Claude Sonnet 4, orchestrator, arrives in terminal 
3. Claude and User back-and-forth conversation 
4. Claude asks all needed information to setup a workflow for the use-case 
5. Claude create the JSON config for that Use-Case 
6. Claude runs the setup script `mao setup` with the JSON config for that use case 

### New Use-Case, Invested Setup 

1. User has all necessary JSON config information prepared 
2. User fills out the JSON config themselves or sends Claude the complete information 
3. User runs the setup script `mao setup` with the JSON config for the at new use case 

### Active Use-Case  

1. User has a use-case with a workflow already created 
2. They can look at the use-case directory to remind themselves of the custom command 
3. User runs the use-case workflow's custom command 

#### **New JSON Config Variable Needs**

1. Custom unique ID for every workflow to manage `memory.py` files across workflow sessions 
2. Token max limit, either user-chosen or pulled from the max of the LLM who will run that agent task 

## Start of Use-Case Workflow 

1. User runs the custom command for their use-case's workflow 
2. Claude Sonnet is called to orchestrate the workflow 
3. Claude gathers what is needed to hand off the the first agent(s)
4. Claude calls the agent(s) that start the workflow 
5. Claude passes off the details for the agent to complete their task of the workflow 
   - Description of the task, their motivation, the deliverable 
   - Important FYIs including that their doc tool has auto-save 
   - Their FYIs include what their personal token limit is (LLM max or use-case specific max)
   - They're reminded that they will be able to see a live token counter as they work on the document 
   - The last reminder is that they hand the deliverable directly back to Orchestrator Claude, there is no 'save output' 
   - Button snippets for their tools, for each tool command 
   - Button snippet for calling Orchestrator Claude when they are complete their task 
6. Claude records update to `memory.py` for context history just like a chat thread 
   - This is so that when the agent is done and calls Claude back, they can get up to speed 
   - We might want to consider if this might be better if their workflow log is part of the actual memory document 
   - Every `memory.py` document and has a unique ID that matches the unique ID of the workflow and are kept together 
   - See "`memory.py` Per-Workflow Usage Flow" section below for specifics on this newly planned feature 
7. Agent goes off and works to complete their task 
8. Agent calls Orchestrator Claude when they are finished their task and meets Claude directly 
9.  The deliverables, within token limit, are handed off to Claude 
10. Agent provides Claude a task report 
   - Depending on the workflow this might also include information needed for the next task 
   - No matter what it is, Claude records it in their Workflow Log 
11. Claude saves all working drafts in the Files API 
   - Totally free service from Anthropic avoids use of tokens 
   - Only documents that Claude adds to Files API using Code Execution can later be downloaded 
   - The final version of deliverables will be handed to User in standard paths/directory method 
   - The Files API will be purged regularly 
12. Claude reviews the documents and makes a decision 
   - If there's a pre-planned next task, are the materials needed ready or not? 
   - If there's no next task, Claude plans the next phase on the fly 
   - If the documents aren't ready yet, Claude changes the remaining task sequence 
13. Claude then either: 
   - Updates workflow 
   - Hands off to next agent 
   - Wraps up and submits final deliverable 

### `memory.py` Per-Workflow Usage Flow 

1. Workflow Start
  - OC pulls memory.py from use-case directory (along with config, README, etc.)
  - Executes code to add memory.py to Files API
  - Now it's accessible for the workflow session
2. During Workflow
  - Agents complete tasks → call OC
  - OC accesses memory.py from Files API (no token cost)
  - Updates memory with task results, context
  - Memory stays in Files API for efficient access
3. Workflow End
  - OC pulls final deliverables to actual directory paths
  - Also pulls updated memory.py back to use-case directory
  - Memory persists for future workflow runs
  - Files API gets purged (as designed)

### Items To Be Integrated To Flow 

- Timing for creating button snippets 
- Gathering specifics like the token max limit 

### Items To Be Sorted In Other Code Planning 

- Because the Orchestrator is the only one who can "save output" we need to remember AUTO-SAVE docs for agents 
- They need a live token counter just like we have in the IDE when I'm typing up a document 


-----------------

# **Combine Final Stretch Task Lists** 

  1. There are tasks listed on the walk-through UX 
  2. We have this implementation plan: `/Users/seanivore/Development/modular-agent-orchestrator/versioning-docs/v4_MAO/v4_0_0/v4_PHASE_2_IMPLEMENTATION_PLANNING.md` 
  3. All of the points below 

Comb through and combine the task lists. Then organize them to be completed in the most efficient way. 

|----------------------|
| **SESSION 19 TASKS** |
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