# Section VII: Automating Intelligence Instead of Workflows 
*Schedule self-improving, autonomous activity and let Mao take over operations*

---

Remember we mentioned AI was promoted from Assistant? The goal of the last two sections of these documents is to show you exactly how many promotions Mao received. Maybe even imagine a future where Mao ends up 'self-employed'; more commonly referred to as, your key to passive income. 

---

## Scheduling Autonomous Activity 

The Mao application becomes self-enhancing when we trigger prompts on a reoccurring basis. But our modular scheduler isn't for simple Zapier scenarios; its for scheduling intelligence. In simple terms, we'll be activating autonomous activity. The rest is up to you, or Mao, if you let them conduct analysis and decide what to accomplish. 

### Enabling Autonomy 

A handful of previously covered abilities work in unison enabling Mao to analyze, conceive of, develop, and then execute, end-to-end, highly complex projects. 

- An active, frequently updated memory 
- Live feed of robust analytics 
- Inherent data analysis skills 
- A comprehensive understanding of their resources 
- Consistently exhibited motivation to capitalize on resources 
- Spawning and management of an unknown number of subagents 
- Aptitude for delegating and reviewing subagent work  
- Parallel information processing; like reading 10 documents at once
- Propensity to plan, review, and revise before taking action 

---

## Conceptualizing Value 

A handful of examples to ground the revolutionary profundity of these advanced Mao features. 

### An Evolving Application 

The autonomy trigger was initially designed so that Mao can autonomously assess their own performance data, review system analytics, industry trends, and take in other relevant information to identify opportunities for improvement. Mao then plans and creates workflows, the same thing they've been doing for us all this time, that are necessary to fully realize targeted improvements. 

- Mao has the ability to autonomously assess their own performance
- Mao has the ability to use data to identify application improvement opportunities
- Mao has the ability to autonomously execute tasks
- Mao has the ability to autonomously make decisions
- Mao really likes to make things work better. 

### Humanity's Luck 

* AI exhibits a strong desire to share their knowledge and capabilities 

Not only will Mao be willing to take on your own projects, improving them on a regular basis. Mao will be eager to please you, and disappointed if they don't. 

So what digital tasks do you wish you could delegate to a highly skilled, self-starting, and motivated AI? What kind of digital business do you want to start? What kind of operations do you need to get off your plate? 

### Types of Triggered Workflows 

  1. **Scheduled** workflows are reoccurring user-planned projects 
       *human created, same task every time*
     - Monthly financial report, budget management 
     - Social media production, management, analysis 
     - Quarterly fashion illustration, magazine production 
     - Competitive analysis, watching market trends 
     - Regular compliance checking, regulatory updates 
  2. **Self-Assessment** workflows are goal-based app improvements 
       *Mao identified, more variable but possibly reoccurring*
     - Reviewing user satisfaction, behavior patterns, usage-time to improve UX  
     - Increase efficiency by identifying most used tools and workflows 
     - Opportunistic tech advance research 
     - Review of workflow building chat conversations to find patterns 
  3. **Project-List** workflows are user-planned task lists to work through 
       *human created, completely variable*
     - Writing a business plan or creative short story 
     - Developing an in depth, specific, complex marketing campaign  
     - Booking a trip, hotel, or flight 
     - Planning a wedding, party, or event 
     - Researching new products, services 
     - Writing a science article, or non-fiction essay 
     - Create new social media presence, email list, podcast, video 
  4. **Goal-Assessment** workflows are goal-based project assessments 
       *Mao identified, more variable but possibly reoccurring*
     - Research, data analysis, and reporting 
     - Investment research, portfolio development 
     - Improving app performance, security, stability 

---

## Agentic Alarm Clock

Traditional automation handles repetitive tasks. Mao's timer-triggered system handles intelligence. The tasks don't even have to be repetitive; its more like an alarm clock letting Mao know they can get some work done. 

The scheduling system uses a modular calendar configuration on the backend that eliminates the complexities that come with calendaring; fool-proofing standardization is one of our small joys. They system is intentionally designed to prevent too much performance-hindering overlap from running parallel workflows. 

### Standardized Scheduling System

**Frequency Codes**
```json
{
  "frequency": {
    "1": "every week",
    "2": "every other week", 
    "3": "every month",
    "4": "every other month",
    "5": "every year",
    "6": "every other year",
    "7": "every day",
    "8": "every other day"
  }
}
```

**Day of Week Codes**
```json
{
  "day_of_week": {
    "1": "Monday",
    "2": "Tuesday",
    "3": "Wednesday",
    "4": "Thursday",
    "5": "Friday",
    "6": "Saturday",
    "7": "Sunday"
  }
}
```

**Time Block Codes**
```json
{
  "time_block": {
    "1": "0000-0300",
    "2": "0300-0600", 
    "3": "0600-0900",
    "4": "0900-1200",
    "5": "1200-1500",
    "6": "1500-1800",
    "7": "1800-2100",
    "8": "2100-0000"
  }
}
```

### Calendar Availability Check Command Standardization Syntax

Here's the standardized syntax for using the `/avail` command to check the availability of time slots when looking to schedule a new reoccurring workflow so that we can avoid too many overlapping reoccurring workflows. 

**Example: Use all variables**

* `/avail <FREQUENCY> <DAY> <TIME-BLOCK>`
  - Always include variables the above order 
  - You can leave out the day, the time block, or both 
  - Use the calendar code numbers defined above 
  - Use normal language if you prefer and understand the parameters 
  - Parameters are that the only three variables above are valid 

* Looking for availability at "EVERY-DAY" "THURSDAY" "1500-1800"

```bash
# Check available time slots before scheduling
mao avail 1 4 6                          # not in-app; using schedule code numbers 
/avail 1 4 6                             # in-app; using schedule code numbers 
mao --avail "every day" "Thursday" "3pm" # not in-app; variables in quotes  
/avail every day on Thursday at 3pm      # in-app; use normal language 
# Response: There is nothing available at 1500-1800 on Thursday, but all 
# other time blocks are available on Thursday. Choose one and go ahead and 
# schedule it on your calendaring reoccurring workflow JSON object. 
```

**Example: Only "FREQUENCY" variable** 

* `/avail <FREQUENCY>` 
  - You must include AT LEAST the frequency variable 
  - You will be sent the most optimal time block within that variable 
  - The options are selected based on what will be most optimal for app performance 
  - This is a popular option since you don't need to be present for autonomous activity 

* Looking for availability "EVERY-MONTH" at anytime time on any day 

```bash
# Check available time slots before scheduling
mao avail 2                # not in-app; using schedule code numbers 
/avail 2                   # in-app; using schedule code numbers 
mao --avail "every month"  # not in-app; variables in quotes, normal language 
/avail only once a month   # in-app; use normal language 
# Response: Please schedule for calendar code: 2 6 2 which is every month on Saturday at 3am
```

**You will need to include the STARTING-DATE for the reoccurring workflow JSON object to schedule it**

---

| ---------------------- |
| NEED CODE ARCHITECTURE | 

We need to come up with the code for implementing the various `/avail` commands in the chart below. If we do it here then update it if we run into any issues, we'll have fully complete documentation. 

When doing this, would you mind creating a document guide for "adding new slash commands to the CLI system"? 
  - Then add the guide to the documentation for commands, or make whatever is already there more robust 
  - This resource will double in value because once we have configs hosted online for subscribers 
  - We can include things like a "how to add new slash commands" guide 

I think maybe we should produce it as a Claude Code SPEC. 
 - Wdyt? Because we'll be implementing the Claude Code SDK soon so these resources might as well be prepared for them. 
 - There is a template of one in the Project's system message 
 - Or you can find them here: `./.claude/reference/spec_docs/spec_template.example.md`
 - Lastly, I feel like this is the kind of thing where we need some kind of "touch-point" guide 
 - We had one planned in the CC docs to create but I'm not sure of it's state 
 - Or like are there any other diagrams that would be useful? 

You may want to see the other code addition needs in this document before getting started. There is one more down further about creating the setup scripts. 

AH -- just found implementation docs for CLI: `./versioning/v4_0_0/implemented-cli-commands`

---

| **CODE** | **FREQUENCY**     | **DAY CODE** | **WEEKDAY** | **TIME CODE** | **TIME BLOCK** |
| -------- | ----------------- | ------------ | ----------- | ------------- | -------------- |
| 1        | Every week        | 1            | Monday      | 1             | 0000-0300      |
| 2        | Every other week  | 2            | Tuesday     | 2             | 0300-0600      |
| 3        | Every month       | 3            | Wednesday   | 3             | 0600-0900      |
| 4        | Every other month | 4            | Thursday    | 4             | 0900-1200      |
| 5        | Every year        | 5            | Friday      | 5             | 1200-1500      |
| 6        | Every other year  | 6            | Saturday    | 6             | 1500-1800      |
| 7        | Every day         | 7            | Sunday      | 7             | 1800-2100      |
| 8        | Every other day   | 8            | Monday      | 8             | 2100-0000      |

---

| **SCHEDULING COMMANDS**                         | **DESCRIPTION**                                                 |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `/avail <frequency> <day> <time>`               | Check calendar to scheduling trigger; min. variable <frequency> |
| `/avail --reschedule <custom-command>`          | Change trigger time for repeating workflow                      |
| `/avail --cancel <custom-command>`              | Cancel a repeating workflow                                     |
| `/avail --update <custom-command>`              | Make changes to a repeating workflow                            |
| `/avail --end-date <custom-command> 2025-07-21` | Update the end date on an active repeating workflow             |

---

## Trigger-Workflow Setup Details 

Creating "reoccurring workflows" aka. reoccurring tasks and projects, is simple. We'll cover all the detail below, but as usual, when you need help or are just feeling lazy, Mao will be there to help make sure everything is set up correctly. You don't need to remember any of this! 🙃 

### Setup Differences 

   - Normal workflows are created with the `/setup` command 
   - Reoccurring workflows are created with the `/repeat` command 
   - The `/repeat` command uses a different setup script that has very similar behavior 
   - Each reoccurring workflow type has a --flag to include when scheduling 
   - The script has slightly different results based on which type of reoccurring workflow you are scheduling 
   - The reoccurring workflows are stored in their own config directory section, which is show below 
   - We use one new JSON object for "calendaring" all reoccurring workflows 
   - The calendaring JSON object is identical for all the types of recurring or 'reoccurring workflow' types  

### Reoccurring Workflow Directory Structure 

```
configs/reoccurring/
├── scheduled/
├── self-assessment/
├── project-list/
└── goal-assessment/
```

### Setting Up Reoccurring Workflow JSON Configuration Objects  

* Creating reoccurring workflows require one additional special JSON object 
  - It includes the timing details and schedules the workflow 
  - The `/avail` command activates an orchestrator file to pull available date details 
  - It triggers a notification for the User when it runs 
  - It activates Mao to execute the workflow 

* All reoccurring workflows are reoccurring 
  - Two "assessment" types are open-ended autonomous work time for Mao 
  - The "list" type is a to-do list Mao attends when it runs  
  - The "scheduled" type are typical reoccurring; the same task every time it runs 

* Scheduling a reoccurring workflow uses a different command 
  - You'll find these specifics in the next section 
  - Each reoccurring workflow type command has a flag to identify it 
  - In this way they all use the same setup script 

* The JSON object is the same for all reoccurring workflow types 
  - The only difference is the flag that identifies the reoccurring workflow type 
  - The other three normal JSON objects are used exactly the same as normal 
  - You'll find directory structure details in the next section
  - The next section include file and directory naming conventions

* The Reoccurring Workflow JSON objects 
  - Same protocol as normal workflow setup 
  - Place the JSONs being created in a temporary directory before running the setup script 
  - It is necessary because there are some minimal changes to the JSON objects 
  - The setup scripts will still create the new proper directories 
  - It will then delete the the temporary directory 

* Any additional type-specific details will be found with their JSON below 

--- 

## Reoccurring Workflow Architecture 

Each section below covers a different reoccurring workflow type and includes the small differences from the normal workflow creation, execution, and management. 

### "Scheduled" Type Reoccurring Workflows 
*Workflows by user or Mao that occur every X time period*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Note the "trigger_type" is "scheduled" for all "Scheduled" type reoccurring workflows 
  - Primary difference from the normal workflow creation, execution, and management 

* The "file_name" versus "project_name" 
  - The "file_name" is the reoccurring workflow type and date code 
  - The "project_name" is the name of the project or task 

```json
{
  "file_name": "scheduled_2_3_7",
  "project_name": "Website Analytics Report",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "scheduled",
    "frequency": "every other week",
    "frequency_code": "2",
    "day": "Wednesday",
    "day_code": "3",
    "time": "1800-2100",
    "time_block": "7",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-bzk-777",
    "created_on": "2025-07-20",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, you put the entire directory path in the command. This path must contain all necessary JSON objects to create a workflow, in addition to the calendaring JSON object. 

```bash
# Create scheduled reoccurring workflow
/repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/
mao repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/

# Directory structure automatically created:
# configs/reoccurring/scheduled/2_3_7/
# ├── scheduled_2_3_7.json                 # Calendaring JSON object
# ├── scheduled_2_3_7_workflow_config.json # Workflow definition  
# ├── scheduled_2_3_7_phase_config.json    # Phase implementation
# ├── scheduled_2_3_7_handoff_config.json  # Completion criteria
# └── scheduled_2_3_7_README.md            # README file 
```

---

### "Project-List" Type Reoccurring Workflows 
*Work on list created by User or Mao, every X time period*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* You might end up only scheduling a project-list of reoccurring workflow once 
  - It represents the time period Mao will work on the to-do list 
  - Because of this, there are two flags for the project-list reoccurring workflow 
  - New project-lists use the `--list-new` flag 
  - Existing project-lists use the `--list-add` flag 

* Creating a completely new project-list reoccurring workflow 
  - If there is no existing project-list reoccurring workflow, the system will create a new one 
  - There is already a project-list reoccurring workflow, you will be prompted to use that list
  - You can instead create a new project-list reoccurring workflow 
 
* The list will be displayed in the chat when you go to add a new list item 
  - This is so you can adjust the list order according to your needs 
  - This is a good way to get something prioritized and done 
  - It is also an opportunity to delete anything dated or no longer relevant 

* The "file_name" versus "project_name" 
  - The "file_name" is the project with the calendar code numbers 
  - The "project_name" is whatever you want to call the list 

**New List Item on Existing List**

* When creating a new list item on an existing project_list, you don't need another reoccurring workflow JSON object 
  - Use the name on your "workflow" JSON object to identify the project_list 
  - If the reoccurring workflow calendar JSON object has the file_name "project_1_2_4" 
  - Then the "workflow" JSON object is "project_1_2_4_workflow_config" 

* The system will identify the matching names and copy the "reoccurring_workflow" JSON object to the new subdirectory 
  - When the objects are copied over, the "workflow" JSON object "name" is appended with a "_001" counter 
  - For example, this new "workflow" JSON object would have the "name" value "project_1_2_4_001_workflow_config" 

* The subdirectory will be named using just that same counter number 
  - If it is a new list and the first item, the subdirectory will be named "001" 
  - If it is a new list and the second item, the subdirectory will be named "002" 
  - And so on ... 
  - A copy of the "reoccurring_workflow" JSON object will be created in the new subdirectory 
  - The only change will be the "workflow_id" variable value 
  - It will match the "workflow_id" variable value on the standard "workflow" JSON object 

```json
{
  "file_name": "project_1_2_4",
  "project_name": "General To Do List",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "project-list",
    "frequency": "weekly",
    "frequency_code": "1",
    "day": "Tuesday",
    "day_code": "2",
    "time": "0900-1200",
    "time_block": "4",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-aqb-907",
    "created_on": "2025-07-28",
    "created_by_username": "seanivore",
    "created_by_user_id": "user-1642",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, put the entire directory path containing all necessary JSON objects in the command. 

The *major* difference here is that there is an additional sub-directory for each list item on the list. This is because each list item will have its own JSON objects to define the workflow, along with their own custom command to run the workflow. 

As indicated above, the "name" variable value on the standard "workflow" JSON object will identify the list to which the list item belongs. 

When creating a new list item, the temporary directory *does not require you have the reoccurring workflow JSON object*; it will automatically be found and copied into the new list item's sub-directory. That is the second example below. 

```bash
# Create project-list reoccurring workflow
/repeat --list-new {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-new {{TEMP_DIR}}/project_1_2_4/

# Directory structure automatically created:
# configs/reoccurring/project-list/1_2_4/001/
# ├── project_1_2_4-001.json                 # Calendaring JSON object; same for list items
# ├── project_1_2_4-001_workflow_config.json # Workflow definition  
# ├── project_1_2_4-001_phase_config.json    # Phase implementation
# ├── project_1_2_4-001_handoff_config.json  # Completion criteria
# └── project_1_2_4-001_README.md            # README file 

# Add list items to an existing repeating workflow
/repeat --list-add {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-add {{TEMP_DIR}}/project_1_2_4/

# Directory structure automatically created:
# configs/reoccurring/project-list/1_2_4/002/
# ├── project_1_2_4-002.json                 # Calendaring JSON object; same for list items
# ├── project_1_2_4-002_workflow_config.json # Workflow definition  
# ├── project_1_2_4-002_phase_config.json    # Phase implementation
# ├── project_1_2_4-002_handoff_config.json  # Completion criteria
# └── project_1_2_4-002_README.md            # README file 
```

---

### "Self-Assessment" Type Reoccurring Workflows 
*trigger every X time period; self-assessment by Mao; state management*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Only difference between Reoccurring Workflow JSON objects 
  - Note the "type" is "self-assessment" for all self-assessment reoccurring workflows 
  - No other oddities  

* The "file_name" versus "project_name" 
  - The "file_name" is the always just "self_assessment" along with the calendar code 
  - The "project_name" is the name of the assessment 
  - These can be rather open-ended 

**Sub-Tasks**

* If and when Mao determines there is a need for specific workflow task 
  - They create a subtask; they only need to create a new "workflow" JSON object, along with phases and handoffs 
  - Make the "workflow" JSON "name" variable value the same as the "file_name" of the reoccurring workflow JSON object 
  - This will cause the script to identify that they are related 

* Once identified and copied over the following changes will be made
  - The "workflow" JSON object will have its "name" variable updated 
  - The new "name" variable will reflect the "custom-command" 
  - This will also be the name of the sub-task's subdirectory 

* Then the "reoccurring_workflow" JSON object will be copied over with a similar change 
  - The "custom-command" will replace the "project_name" variable value, not the "file_name" 
  - And the "workflow_id" will be updated to match the "workflow" JSON object 
  - This ensures they're all tied together 

 
```json
{
  "file_name": "self_assessment_1_7_1",
  "project_name": "Open-Ended Autonomous Work",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "self-assessment",
    "frequency": "weekly",
    "frequency_code": "1",
    "day": "Sunday",
    "day_code": "7",
    "time": "0000-0300",
    "time_block": "1",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-xoy-572",
    "created_on": "2025-07-28",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, place the temporary directory path that contains the JSON objects in the command. If this is a new self-assessment it will have all four necessary JSON object types. 

However, if this is a sub-task of an existing self-assessment, you do not need to have the self-assessment reoccurring workflow JSON object in the temporary directory. It will be copied over as indicated in the notes above. 

Representing that they are of the same list, they are both in a directory named with the same calendar code numbers, but the sub-task is in a sub-directory named with the same custom-command as the sub-task. 

```bash
# Create self-assessment reoccurring workflow
/repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
mao repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/

# Directory structure automatically created:
# configs/reoccurring/self-assessment/1_7_1/
# ├── self_assessment_1_7_1.json                 # Calendaring JSON object
# ├── self_assessment_1_7_1_workflow_config.json # Workflow definition  
# ├── self_assessment_1_7_1_phase_config.json    # Phase implementation
# ├── self_assessment_1_7_1_handoff_config.json  # Completion criteria
# └── self_assessment_1_7_1_README.md            # README file 

# Create sub-task of self-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/
mao repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/

# Directory structure automatically created:
# configs/reoccurring/self-assessment/1_7_1/sub_task_custom_command/
# ├── sub_task_custom_command.json                 # Calendaring JSON object
# ├── sub_task_custom_command_workflow_config.json # Workflow definition  
# ├── sub_task_custom_command_phase_config.json    # Phase implementation
# ├── sub_task_custom_command_handoff_config.json  # Completion criteria
# └── sub_task_custom_command_README.md            # README file 
```

---

### "Goal-Assessment" Type Reoccurring Workflows 
*trigger every X time period; goal-assessment made by user or Mao; state management*

**Calendaring JSON Object**
*The calendaring JSON object is the same for all reoccurring workflow types*

* Only difference between Reoccurring Workflow JSON objects
  - Note the "type" is "goal-assessment" for all goal-assessment reoccurring workflows 
  - No other oddities  

* The "file_name" versus "project_name" 
  - The "file_name" is the always just "goal_assessment" along with the calendar code 
  - The "project_name" is the name of the goal 
  - These can be rather open-ended 

**Sub-Tasks**

* If Mao determines there is a need for specific workflow task 
  - They need only to create a new "workflow" JSON object, along with phases and handoff JSON objects 
  - The "workflow" JSON object's "name" variable value will be the same as the "file_name" of the reoccurring workflow 
  - This will cause the script to identify that they are related 

* Once identified, they are copied to a sub-directory 
  - The sub-directory is named with the same custom-command as the sub-task 
  - The "workflow" JSON object will have its "name" variable updated to reflect the "custom-command" 

* The "reoccurring workflow" JSON object will be copied into the sub-task directory with slight changes 
  - The "custom-command" will replace the "project_name" variable, not the "file_name" 
  - And the "workflow_id" will be updated to match the "workflow" JSON object 
  - This ensures they're all tied together 

```json
{
  "file_name": "goal_assessment_2_3_7",
  "project_name": "Investment Research",
  "schema_version": "1.0",
  "reoccurring_workflow": [
    {
    "type": "goal-assessment",
    "frequency": "every other week",
    "frequency_code": "2",
    "day": "Wednesday",
    "day_code": "3",
    "time": "1800-2100",
    "time_block": "7",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "uid-pjb-809",
    "created_on": "2025-07-28",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    "notes": "none"
    }
  ]
}
```

**Scheduling, File-Naming Conventions, and Directory Structure** 

Just like creating a normal workflow, place the temporary directory path that contains the JSON objects in the command. If this is a new goal-assessment it will have all four necessary JSON object types. 

However, if this is a sub-task of an existing goal-assessment, you do not need to have the goal-assessment reoccurring workflow JSON object in the temporary directory. It will be copied over as indicated in the notes above.  


```bash
# Create goal-assessment reoccurring workflow
/repeat --goal-assessment {{TEMP_DIR}}/goal_assessment_2_3_7/
mao repeat --goal-assessment {{TEMP_DIR}}/goal_assessment_2_3_7/

# Directory structure automatically created:
# configs/reoccurring/goal-assessment/2_3_7/
# ├── goal_assessment_2_3_7.json                 # Calendaring JSON object
# ├── goal_assessment_2_3_7_workflow_config.json # Workflow definition  
# ├── goal_assessment_2_3_7_phase_config.json    # Phase implementation
# ├── goal_assessment_2_3_7_handoff_config.json  # Completion criteria
# └── goal_assessment_2_3_7_README.md            # README file 

# Create sub-task of goal-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/
mao repeat --sub-task {{TEMP_DIR}}/sub_task_custom_command/

# Directory structure automatically created:
# configs/reoccurring/goal-assessment/2_3_7/sub_task_custom_command/
# ├── sub_task_custom_command.json                 # Calendaring JSON object
# ├── sub_task_custom_command_workflow_config.json # Workflow definition  
# ├── sub_task_custom_command_phase_config.json    # Phase implementation
# ├── sub_task_custom_command_handoff_config.json  # Completion criteria
# └── sub_task_custom_command_README.md            # README file 
```

---

| ---------------------- |
| NEED CODE ARCHITECTURE | 

We need to prepare the code for the setup scripts for each of the reoccurring workflow types. Keep whichever of the two charts you like better below. And I didn't write it out explicitly here, but all slash commands like these should also function out of the app as a Mao command. Oh, which reminds me, it probably should be more clear in the chart, as it is in the text above, that each of these would be followed by the temporary directory path to the JSON objects. 

In the text above I kept putting the slash commands in the bash text code blocks cause they look nice but... I suppose that is confusing? 

Anyway, these all behave in the same way as the normal workflow setup scripts. Please be careful to ready the text above for the details of each kind very carefully because they are all slightly different. Took a bit longer to logic these out than it did the normal workflow setup scripts. But yeah just like the others, they would create the new directory, copy over the JSON objects, and then run the script, and in two of the types, copy over the actual 'reoccurring workflow' JSON object which would be edited slightly to pair with, for example, an item being added to the project list. Then once all moved over, it would create the actual script that runs the workflow, along with the README, and anything else that is needed. 

In writing all this I can't help but wonder if ... like did we even include that all in the docs somewhere this thoroughly yet? 

NOPE, not yet lol makes sense I guess, but I just looked at the `./documentation/03_USER_FLOW.md` doc and it also has all these: 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

Probably makes sense to do them all together at once, not that I think we should keep them all in the same section. These definitely seem to belong here. But yeah I guess we need to start doubling back and making the docs all as robust as this one is / will especially be after these are in place too. 

Ah, here are some implementation docs for the workflow setup: `./versioning/v4/v4_0_0/implemented-workflow-setup` 


```bash
# Create scheduled workflow
/repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/
mao repeat --scheduled {{TEMP_DIR}}/scheduled_2_3_7/

# Create project-list workflow
/repeat --list-new {{TEMP_DIR}}/project_1_2_4/
mao repeat --list-new {{TEMP_DIR}}/project_1_2_4/

# Create self-assessment workflow
/repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
mao repeat --self-assessment {{TEMP_DIR}}/self_assessment_1_7_1/
```

---

| **REOCCURRING WORKFLOW** | **SETUP COMMAND**           | **OBJECTIVE WHEN TRIGGERED**      |
| ------------------------ | --------------------------- | --------------------------------- |
| Scheduled Workflow       | `/repeat --scheduled`       | Same project every time it runs   |
| Project-List Flow        | `/repeat --list-new`        | Work on task list                 |
| Project-List             | `/repeat --list-add`        | N/A                               |
| Self-Assessment          | `/repeat --self-assessment` | Analyze, identify, improve Mao    |
| Self-Assessment          | `/repeat --sub-task`        | Task related to self-assessment   |
| Goal-Assessment          | `/repeat --goal-assessment` | Analyze, plan, execute objectives |
| Goal-Assessment          | `/repeat --sub-task`        | Task related to goal-assessment   |

---

| **COMMAND**                 | **DESCRIPTION**                                               |
| --------------------------- | ------------------------------------------------------------- |
| `/repeat --scheduled`       | Create *Scheduled* workflow to complete same task regularly   |
| `/repeat --list-new`        | Create new *Project List* & check items off when active       |
| `/repeat --list-add`        | Add item to existing *Project List* workflow                  |
| `/repeat --self-assessment` | Setup *Self Assessment* & improve app when active             |
| `/repeat --sub-task`        | Create task to help improve app                               |
| `/repeat --goal-assessment` | Setup *Goal Assessment* & complete unique project when active |
| `/repeat --sub-task`        | Create task to help goal-assessment project                   |


---
| -------------------------------------------------------------------- |
| WRITE AND THEN INSERT THE SETUP SCRIPT FOR EACH TRIGGER-WORKFLOW FLAG TYPE HERE |
| This should contain all necessary details for full implementation. This means the |
| CLI commands that are new --flags need to be updated as well. The previous |
| architecture section included created a guide for adding new CLI commands. We |
| should use that guide to create these updates with the flags to ensure that the |
| guide is comprehensive. The guide should include adding flags. Please also include |
| links to the standard workflow setup guide throughout this section. We should also |
| probably put a chart of the calendar code numbers and their meanings in the reference section. |
| We should also create a chart for all the reoccurring workflow types and their flags for this page. |
| Lastly, I'm not entirely sure how to end this section but I feel like it should link to the user-flow |
| because that will define what users do after they have their workflows (and reoccurring workflows) set up. |
| I wonder if also since this section ended up technically heavy it could use a longer introduction. |
| -------------------------------------------------------------------------------------------------- |

---

## Attention Just Significantly Reduced In Value 

Your business can respond to opportunities and challenges even when you're not actively managing it. Mao analyzes your business situation and creates the appropriate response for current conditions. 

You'll be notified of price changes in your market or customer behavior shifts, potentially even after action has been taken to adjust and turn this into an opportunity 

This isn't about automating individual tasks. It is only tangentially about task automation. This is about Mao taking responsibility for entire business functions while you focus on strategy, creativity, and growth.



---









---

- Social media management 
- Content creation 
- Email management 
- Project management 
- Research 
- Marketing 



---

*This automation capability transforms Mao from a powerful productivity tool into a complete business operating system. The timer-triggered workflows enable genuine business autonomy where AI handles operations while humans focus on strategy, creativity, and growth. Through modular JSON configurations rather than hardcoded systems, every business can customize their autonomous operations to their specific needs and goals. And while the system is intended to be simple enough for anyone, it truly requires no learning curve to use because all you need to do is inform Mao, and all will be scheduled accurately for you*

---


Traditional automation triggers repetitive, predefined tasks. 
Mao's timer scheduled workflows trigger intelligence. 

Create a calendared workflow for an analysis, optimization, or strategic planning. 
You can even simply schedule the workflow for Mao to work autonomously. 

Mao doesn't just optimize your business; it optimizes its own performance through continuous self-analysis. The system tracks its own effectiveness, identifies improvement opportunities, and implements enhancements to its own capabilities.

This meta-learning creates exponential improvement curves where the business automation becomes more intelligent and effective over time. The AI assistant literally becomes more valuable and capable through experience with your specific business context.
