# SFA Main Update: Phase Adjustment Workflow
`sfa-main.py` for testing without affecting the original agent 

## Key Components of the Implementation

1. Workflow Adjustment Tool
- Simple tool with two actions: END_PHASE and ADD_PHASE
- Clean, straightforward interface for Claude

2. Phase Reset Function
- Resets iteration counter without ending the phase
- Maintains the same Claude instance
- Adds a clear message to conversation history

3. Token Checking Integration
- Always checks tokens before saving
- Resets phase for revision if over limit
- Includes token count in output messages

4. Task Report Tool Update
- Standardized phase summary format
- Includes accomplishments, token counts, decisions, and next steps
- Triggers phase completion when saved

5. Main Loop Modifications
- Warns Claude before reaching max iterations
- Provides option to request more iterations

## Implementation Process 

> I've created an implementation plan for our streamlined end-of-task workflow. This implementation focuses on the simplified flow you designed while ensuring it works with the existing SFA architecture. To test this implementation without affecting the original agent:

1. Create a Copy of the SFA Agent

```bash
cp /Users/seanivore/Development/single-file-agents/sfa_agent.py /Users/seanivore/Development/single-file-agents/sfa-main.py
```

2. Make the Necessary Modifications to `sfa-main.py`

- Add all the components from the artifact
- Update the handler functions and main loop

3. Create Task Reporting Tool

- Add the updated task_reporting.py to tools directory

4. Test with Branching Workflow 
- These are both the same command workflow 

```bash
./branching_workflow.sh /path/to/your/config.json sfa-main.py 
sfa -s /path/to/your/config.json
```

## Benefits of This Approach

- **Simplicity**: Clean, straightforward flow with minimal branching
- **Efficiency**: No unnecessary tracking of trigger sources
- **Consistency**: Standardized phase summary format
- **Flexibility**: Seamless handling of both ending and extending phases
- **Reliability**: Token checking integrated into the workflow

You're absolutely right that the `task_report` tool seems to already have some of what we need, but we're enhancing it to fit our streamlined workflow better.

Does this implementation plan look good to you? Would you like me to help with any particular part of the integration?

## End Task Workflow Logic 

```
PHASE RUNNING (CLAUDE INSTANCE ACTIVE)
           |
           ↓
+------------------------- +
| End phase tool triggered |     <-- "save_output" or "complete_task" or "workflow_adjustment" or "task_report" or "add_phase"
+------------------------- +          It honestly doesn't really matter how they get here if we have all exits covered 
           |
           ↓
+-------------------------+
| End phase or add phase? |     <-- Then this is our only necessary router
+-------------------------+
        /              \
       /                \
     [END]             [ADD]
       |                 |
       ↓                 ↓
       |                 |
       ↓                 |
+---------------+        |
| < 7k tokens?  |        |     <-- NEW RULE: count every document to record in your phase summary about your phase 
+---------------+        |
   /       \             |
  /         \            |
[YES]       [NO]---------+
  |           |
  |           ↓
  |    +-------------------------+
  |    | RESET LOOP COUNTER      |
  |    | MAINTAIN CLAUDE INSTANCE|
  |    | CONTINUE SAME PHASE     |    <-- Let's build new phase type, doesn't call Claude, allows already called LLM to enter  
  |    +-------------------------+
  |                     \ 
  |                      \
  |                       \
  |                        \
  |                         \
+--------------------+     [EXIT]--- -->------ --> [START NEW PHASE TYPE]
| Write Phase Summary|
+--------------------+
         \
          \
           |
           ↓
 +---------------------+
 | SAVE PHASE SUMMARY  |
 | SAVE OTHER OUTPUTS  |
 +---------------------+
            |
            ↓
            |
            ↓
        [PHASE AUTO ENDS
       SFA TRIGGERED EXIT]--- -->------ --> [WORKFLOW OR COMPLETION]
```

### Comments for Each Section

#### 1. End Phase Tool Triggered
- Currently: `save_output` or `complete_task` 
- Current, but needs update for this workflow: `task_report` 
- New tools: `adjust_workflow` `add_task` `add_phase` 

#### 2. End Phase or Add Phase?
- Weed out all the Claudes who just want to work more 

#### 3. Check Tokens (for Save Output)
- Let's simplify things and say everyone with a document gets a count 
- They should add their count to their phase summary 
- Under 7k and SFA confirmation approves them to move forward
- Under 7k and they'll get a phase to complete revisions 
- Let's post a guide that shows word and paragraph count average compared to tokens   

#### 4. Reset Loop Counter (for token limit or add phase)
- They get special entry into an exclusive phase that retains context window 
- There is no file-save trigger; transfer is automatic 

#### 5. Write Phase Summary, Decision Outputs from Phase If Needed 
- If your task was a decision, detail your decision 
- If you're task was anything else, detail your accomplishments 
- If you need to provide information to the next phase, add it to the phase summary 
- If you exited with documents, include your token count in the phase summary 

#### 6. Save Outputs and Summary 
- This is the final step of the phase 
- Creates all output files and summary 
- Triggers the true phase completion 

## Implementation Steps 

End-of-Task Workflow Implementation for SFA

This file contains the implementation code for adding the streamlined end-of-task workflow
to the Single-File Agent. This focuses on implementing the simplified flow with END_PHASE and ADD_PHASE paths.

Main Components:
1. Workflow Adjustment Tool Definition
2. Phase Reset Function
3. Token Checking Integration
4. Task Report Tool Update
5. Main Loop Modifications

