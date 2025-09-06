
## 6. Review of Workflow JSON Objects & Variables 

* **NOTE: I WOULD LIKE TO REMOVE THE 3RD FALLBACK MODEL AND PROVIDER FROM THE WORKFLOW JSON OBJECT**

### Core Objectives 

  - Ensure accurate understanding objects needed to create workflow 
  - Validating JSON object variable values 
  - Ensure there is *NO NEED OR DESIRE TO PROVIDE SUGGESTIONS OR EXAMPLES* in the code

### Defining **Workflow** JSON Object Variable Values

* **Workflows get 1 'Workflow Object' that describes the entire project** 

  - Examples and defined purposes of each variable in this object 

| Variable              | Purpose                                      | Value Example                                 |
|-----------------------|----------------------------------------------|-----------------------------------------------|
| *UserID*              | Connect all your stuff                       | user-5709                                     |
| *WorkflowID*          | Connect all of one project                   | uid-abd-123                                   |
| Custom command        | Executes your completed workflow             | report expense monthly                        |
| Workflow goal         | Overarching project objective                | Automate payments; expense report operations  |
| Workflow deliverables | What you get after all tasks                 | Receipt for payment of employee CC            |
| Workflow description  | How deliverables are created to achieve goal | *see below*                                   |

  - The *Workflow description* example from above: 

  1. Agents work in parallel to go and 
     - Gather the employee's submitted expenses 
     - Download their credit card statements 
     - Confirm accuracy and that all expenses have a receipt 
  2. Second batch of agents work in parallel to 
     - Review the work for accuracy 
     - Create specific detailing of any inaccuracies 
  3. During handoff, Mao reviews the results and proceeds according to their accuracy 
     - If all are accurate they execute next agent to make payment 
     - If they are not accurate they will execute an agent to double check the work 
     - If not accurate after second review agent they execute agent to email appropriate parties regarding expense report inconsistency 
  4. Agent works sequentially through each report to make payments 
     - They use the PayPal MCP tool to make payments one at a time for each of the employee's credit cards 
     - They then downloads the statement showing payment  
     - They return the paid statement back to Mao 

### Validating **Workflow** JSON Object Variable Values

* **Validation parameters go in code, not suggestions or examples** 

  - *Examples* do NOT go in code 
  - Validation guides can go in code 
    - The value's purpose so Mao understands it conceptually 
    - How to make sure the value is the appropriate amount and type of information 

  - Confirming each variable's value 
    - *UserID* and *WorkflowID* are accurate 
    - *Custom command* follows command creation protocol directions detailed in documentation 
    - *Workflow goal* is concise and explains entire purpose of all segments of the workflow 
    - *Workflow deliverables* explain just what Mao should expect after the completion of entire workflow 
    - *Workflow description* accurately defines each object or phase using bullets and in appropriate order 

### Defining **Phase** JSON Object Variable Values

* **A project's workflow has tasks in each 'phase'** 

  - Each phase, parallel or sequential, has one of these objects, with one exception 
  - EXCEPTION: Open-ended phases will not have an object 
    - This is when certain phases are not defined in advance 
    - Mao decides what the next phase should look like during the workflow running 
    - They get the deliverables from the previous agent's handoff 
    - They then create the next workflow on-the-fly based on what the agent provided them 
    - Details for adding them to the workflow can be found after this section 
  - Open-ended phases will be mentioned in the Workflow Object and the prior Handoff Object 


| Variable           | Purpose                                         | Value Example                                  | 
|--------------------|-------------------------------------------------|------------------------------------------------|
| Phase number       | Order to execute each phase                     | 1-A, 1-B, 2, 3                                 |
| Phase goal         | Objective purpose of phase                      | Compile expenses and CC statement into report  |
| Phase deliverable  | What Agent will provide to Mao in handoff       | Expense report for employee                    |
| Phase description  | How to create deliverable from resources, tools | Download receipts, get CC statement            |
| Resources          | Where to get deliverable info                   | Directory for receipts, CC website login       |
| Tools              | What gets resource info, makes deliverable      | Web browser, Google Sheets, Text edit, Vision  |
| Choice Model       | LLM to be Agent for this task                   | Sonnet-4                                       |
| Choice Provider    | Provider of Choice Model                        | Requesty                                       |
| Fallback Model     | LLM to be Agent if first provider API fails     | Sonnet-4                                       |
| Fallback Provider  | Provider of Fallback Model                      | Anthropic Direct                               |

### Validating **Phase** JSON Object Variable Values

* **Validation parameters go in code, not suggestions or examples** 

  - *Examples* do NOT go in code 
  - Can go in code 
    - The value's purpose so Mao understands it conceptually 
    - How to make sure the value is the appropriate amount and type of information 

  - Confirming each variable's value 
    - *Phase number* will be in proper order, and have the same number but include a letter if parallel 
    - *Phase goal* provides context as to what the deliverable should provide the project 
    - *Phase deliverable* explains what Mao will get in the handoff from the agent  
    - *Phase description* should effectively define how the agent can create the deliverables; this might be long and that is okay, as long as it is clear and comprehensive ensuring all necessary info is provided to the Agent 
    - *Resources* these could be paths to documents, directories, or they could be websites; they should adequately provide a way for the Agent to gather what is needed to fulfill the description and create the deliverable 
    - *Tools* should be clear as to which tool they should use for what to eliminate any potential confusion 
    - *Choice model* is which model the User prefers or Mao suggests is best to run the phase; best fit to complete the task 
    - *Choice provider* is the API that should be called to execute the desired model as Agent 
    - *Fallback model* is the model to use if the first provider API call fails after X number of tries 
    - *Fallback provider* is the API to use if that first provider API didn't work   

### Defining **Handoff** JSON Object Variable Values

* **There is a Handoff Object that follows every phase in the workflow** 

  - After an agent completes their phase tasks they call Mao so they can hand in their deliverables 
  - The Handoff Object defines exactly what that process should look like 
  - This object will provide any information Mao needs to decide if the deliverables are of adequate quality 
  - If there is an open-ended phase, this will help Mao make a decision about what that phase will be 

| Variable              | Purpose                      | Value Example                          | 
|-----------------------|------------------------------|----------------------------------------| 
| Handoff Number        | Keeps objects in order       | Number matches Phase Object it follows | 
| Handoff assessment Qs | Helps Mao decide next steps  | *See below*                            | 
| Human in-the-loop     | Wait for human approval      | Default: No                            |

  - The *Handoff assessment questions* value example from above 
    - Is every item on the employees CC statement addressed in the report? 
    - Did the employee include a receipt for every single expense on the credit card report? 
    - Does the math add up accurately? What did the review say, if anything, and were those issues fixed? 

### Validating **Handoff** JSON Object Variable Values

* **Validation parameters go in code, not suggestions or examples** 

  - *Examples* do NOT go in code 
  - Can go in code 
    - The value's purpose so Mao understands it conceptually 
    - How to make sure the value is the appropriate amount and type of information 

  - Confirming each of the variable's values is adequate 
    - *Handoff number* should make sense and match the appropriate Phase Object's number 
    - *Handoff assessment questions* should be created when creating the workflow and should help make decisions 
    - *Human-in-the-loop* is "No" unless otherwise indicated 

### Defining **Calendaring** JSON Object Variable Values 

* **Reoccurring workflow or triggered activity requires this 1 additional 'Calendaring' JSON object** 

  - *All other standard JSON objects are still created as usual* 
  - There are only a few other differences 
    - File naming structure; this will be explained in full after this section so that the standard naming structure is easily compared to the reoccurring workflow file naming structures 
    - What command is used to setup the workflow; all setup commands will be explained when this walkthrough gets to the point of setting up the approved project's workflow 
    - They trigger on a reoccurring basis, obviously 
    - Users or Mao may have been the creator of the workflow; how freaky AI-agentic is that 

| Variable   | Purpose                                       | Value Example    | 
|------------|-----------------------------------------------|------------------|
| Type       | Type of reoccurring workflow                  | *Defined below*  | 
| Frequency  | How often the workflow is triggered           | Every week       |
| Day        | Day of week workflow triggers on              | Tuesday          | 
| Time       | 3 hour time block dedicated for the workflow  | 1800-2100        |

* **Calendared reoccurring work scheduling**

| Code | Frequency         || Code | Day       || Code | Time Block |
| ---- | ----------------- || ---- | --------- || ---- | ---------- |
| 1    | Every week        || 1    | Monday    || 1    | 0000-0300  |
| 2    | Every other week  || 2    | Tuesday   || 2    | 0300-0600  |
| 3    | Every month       || 3    | Wednesday || 3    | 0600-0900  |
| 4    | Every other month || 4    | Thursday  || 4    | 0900-1200  |
| 5    | Every year        || 5    | Friday    || 5    | 1200-1500  |
| 6    | Every other year  || 6    | Saturday  || 6    | 1500-1800  |
| 7    | Every day         || 7    | Sunday    || 7    | 1800-2100  |
| 8    | Every other day   |                    | 8    | 2100-0000  |

* **Use `/avail <FREQUENCY> <DAY> <TIME-BLOCK>` to see if there is a calendar opening** 

  - At most you need to check the frequency using `/avail`
    - Do this if you don't have a huge preference on when the automation runs 
    - The system will respond with the best fit based on the rest of the schedule 
    - Frequency is first so just one number code works 

```bash
# Looking for any availability as long as it is once 'EVERY-MONTH' 
# Check available time slots before scheduling
 > /avail 2                   # using schedule code numbers 
 > /avail only once a month   # using normal language 
Response: Please schedule for calendar code: 2 6 2 which is every month on Saturday at 3am
```

  - If using all of them, use in that order 
    - You can use normal language 
    - But again, in the FREQUENCY, DAY, TIME, order 
    - The system will respond with if the time is available 
    - If not available, it will suggest the next best option 
  - The calendar is dynamic 
    - In the example you see "go ahead and pick one and create your workflow" 
    - This is because once the workflow is ran with the setup script, it will be visible when the system does an `/avail` check 

```bash
# Looking for availability at 'EVERY-DAY' 
# And on 'THURSDAY' at '1500-1800'
# Check available time slots before scheduling
 > /avail 1 4 6                             # using schedule code numbers 
 > /avail every day on Thursday at 3pm      # use normal language 
Response: There is nothing available at 1500-1800 on Thursday, but all other time blocks are available on Thursday. Choose one and go ahead and schedule it on your calendaring reoccurring workflow JSON object. 
```

| **SCHEDULING COMMANDS**                         | **DESCRIPTION**                                       |
| ----------------------------------------------- | ----------------------------------------------------- |
| `/avail <frequency> <day> <time>`               | Check calendar to schedule; min. variable <frequency> |
| `/avail --reschedule <custom-command>`          | Change trigger time for repeating workflow            |
| `/avail --cancel <custom-command>`              | Cancel a repeating workflow                           |
| `/avail --update <custom-command>`              | Make changes to a repeating workflow                  |
| `/avail --end-date <custom-command> 2025-07-21` | Update the end date on an active repeating workflow   |

**You will need to include the STARTING-DATE for the reoccurring workflow JSON object to schedule it**

### Validating **Calendaring** JSON Object Variable Values 

* **This has been said in every section but here is the last time we'll say it: Validation parameters go in code, not suggestions or examples** 

  - *Examples* do NOT go in code 
  - Can go in code 
    - The value's purpose so Mao understands it conceptually 
    - How to make sure the value is the appropriate amount and type of information 

* **Confirming each of the variable's values** 

  - *Type* can be one of four different reoccurring workflows types 
    - Types defined in brief below; [extensively in "Automating Intelligence"](/documentation/08_AUTOMATE_INTELLIGENCE.md) 
    - Acceptable responses for this variable's value are `Scheduled`, `Self-Assessment`, `Project-List`, or `Goal-Assessment` 
  - *Frequency* type is chosen from a chart and each of the 8 type sof frequencies are coded with number 1 to 8 
  - *Day* can only be 1 of the 7 days of the week; they are also coded starting the week with Monday as 1 through to Sunday as 7 
  - *Time* is one of 8 blocks of four-hour chunks each day has been broken into; they are defined specifically below and each also use a numerical code  

* **Types of Triggered Reoccurring Projects, Work, Planning, Etc.** 

  1. **Scheduled** 
     - Reoccurring, user-planned projects 
     - Same project's workflow every time it runs 
  2. **Self-Assessment** 
     - Goal-based app improvements 
     - Mao identifies via data and plans optimization workflows 
  3. **Project-List**
     - User-planned task list to work through 
     - Completely variable, new task each time; a to-do list 
  4. **Goal-Assessment**
     - Goal-based project assessment and improvements 
     - Mao or user identified; more open ended; AI has autonomy 

### Saving The Collection Of JSON Objects 

* **All of the JSON objects go in the same *.temp* directory** 

  - In the configs directory there is `./workflows` and `./reoccurring` 
    - We only find the .temp folder in the `./workflows/.temp/` 
    - This is for simplicity 
    - Since they all use different setup scripts, it doesn't matter if they all start out in the .temp directory within workflows 

* **JSON workflow file-naming conventions** 

  1. If you have a normal workflow you set it up like below, but without the ` calendaring_config.json` object 

```bash
# {{TEMP_DIR}}/custom-command/
# ├── calendaring_config.json    # Calendaring JSON object
# ├── workflow_config.json       # Workflow definition  
# ├── phase_config.json          # Phase implementation
# └── handoff_config.json        # Completion criteria 
```

  2. Run the appropriate script for the type of workflow you are setting up 
  3. All files will be renamed and moved to their appropriate location in the directory 


```bash 
# Create a normal workflow 
/setup {{TEMP_DIR}}/
# configs/workflows/USE_CASE_COMMAND 

# Create scheduled reoccurring workflow
/repeat --scheduled {{TEMP_DIR}}/
# configs/reoccurring/scheduled/2_3_7/

# Creating a project-list reoccurring workflow 
/repeat --list-new {{TEMP_DIR}}/
# configs/reoccurring/project-list/1_2_4/001/

# Adding a list time to an existing repeating workflow  
/repeat --list-add {{TEMP_DIR}}/
# configs/reoccurring/project-list/1_2_4/002/

# Create self-assessment reoccurring workflow
/repeat --self-assessment {{TEMP_DIR}}/
# configs/reoccurring/self-assessment/1_7_1/

# Create sub-task of self-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/
# configs/reoccurring/self-assessment/1_7_1/sub_task_custom_command/

# Create goal-assessment reoccurring workflow
/repeat --goal-assessment {{TEMP_DIR}}/
# configs/reoccurring/goal-assessment/2_3_7/

# Create sub-task of goal-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/
# configs/reoccurring/goal-assessment/2_3_7/sub_task_custom_command/
```

* **Example ordinary workflow directory base structure** 

  - These are created by the setup script automation 

```
configs/workflows/marketing-strategy-startup/
├── config-files/                                    # ← Mao creates this
│   ├── marketing_strategy_startup_workflow.json     # ← Mao moves & renames
│   ├── marketing_strategy_startup_phase.json        # ← Mao moves & renames  
│   └── marketing_strategy_startup_handoff.json      # ← Mao moves & renames
├── README_marketing_strategy_startup.md             # ← Mao writes this automatically
├── marketing_strategy_startup.sh                    # ← Mao creates your custom script
├── metadata/                                        # ← Mao creates tracking directory
│   ├── marketing_strategy_startup_memory.json       # ← Mao links to Memory MCP
│   └── marketing_strategy_startup_log.json          # ← Mao creates execution log
└── deliverables/                                    # ← Mao creates output directory
    └── marketing_strategy_startup_report.md         # ← Where your final report goes
```

* **Example reoccurring workflow directory base structure**

  - These are created by the setup script automation 

```
configs/reoccurring/
├── calendar_index.json                 # Master calendar tracking
├── calendar_codes.json                 # Code reference
├── scheduled/                          # Scheduled workflows
│   └── 2_3_7/                          # freq_day_time codes  
│       ├── scheduled_2_3_7.json        # Calendar config
│       ├── scheduled_2_3_7_workflow_config.json
│       ├── scheduled_2_3_7_phase_config.json
│       ├── scheduled_2_3_7_handoff_config.json
│       ├── scheduled_2_3_7_README.md
│       └── trigger_scheduled_2_3_7.sh  # Execution command
├── project-list/                       # Project list workflows
│   └── 1_2_4/                          # freq_day_time codes
│       ├── 001/                        # First project item
│       │   ├── project_1_2_4-001.json  # Calendar config (copied)
│       │   ├── project_1_2_4-001_workflow_config.json
│       │   └── ... (other configs)
│       └── 002/                        # Second project item
│           └── ... (similar structure)
├── self-assessment/                    # Self-assessment workflows
│   └── 3_1_5/                          # freq_day_time codes
│       ├── self_assessment_3_1_5.json
│       └── ... (standard configs)
└── goal-assessment/                    # Goal assessment workflows
    └── 5_6_2/                          # freq_day_time codes
        ├── goal_assessment_5_6_2.json
        └── ... (standard configs)
```
