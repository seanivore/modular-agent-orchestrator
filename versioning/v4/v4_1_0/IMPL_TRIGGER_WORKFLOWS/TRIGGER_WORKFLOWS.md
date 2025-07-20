
### Types of triggered workflows include 
  1. Reoccuring user-planned schedule workflow (finance reports, social media posts, etc.)
     - **Type of workflow: "Scheduled"**
  2. Reoccuring goal-based self-assessment and workflow creation 
     - We need to identify what exactly they are able to assess 
     - This is related to the #2 update above for analytics 
     - **Type of workflow: "Self-Assessment"**
  3. Reoccuring user-planned unscheduled list of projects 
     - I'd love for them to power through creating implementation plans for updates like this list
     - Other tasks that are just a one-off task 
     - Only the trigger is reoccuring; then it pulls from a list 
     - Create logic for if list is empty 
     - **Type of workflow: "Project-List"**
  4. Reoccuring goal-based project-assessment and workflow creation 
     - This is similar to #2 but instead of improving Mao directly 
     - They would do things like market research, business plans, etc. 
     - For example "see what is best to do next to improve my business" 
     - **Type of workflow: "Goal-Assessment"**

### Each type of workflow needs its own logic and template 

- For example, for #4 improving business
- We need a way for them to explore what needs to be done
- Record that information 
- Keep project updates, etc. 

### Similarly, each type of workflow needs a setup script command and ... 

- Since they are all so similarly named, we needs a new command rather than just flags for /setup 
- Let's use /triggered --scheduled, --project-list, --self-assessment, --goal-assessment 
- The assessments need state management in memory; idk that we need a command for this or not 

### Calendaring / Scheduling Protocol / Availability Script 

- We need a calendar display in the UI that pulls from across all ./configs/reoccuring/... directory entries 
- Every JSON in the configs directory will have the following fields and be allowed the following TWO values 
- **FREQUENCY**
  - frequency code (for file name) options are intentionally limited to these options 
    - 1 = every week 
    - 2 = every other week 
    - 3 = every month 
    - 4 = every other month 
    - 5 = every year 
    - 6 = every other year 
    - 7 = every day 
    - 8 = every other day 
- **DAY**
  - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday 
  - For daily they would just select every day of the week 
  - **Can we logically completely avoid a month option?** 
    - For simplicity, they cannot select specific dates in the month
    - Instead they define the day as "first Monday of the month" 
    - For yearly, they indicate the week count number and day of the week 
    - "Monday of the 25th week of the year"
    - **Is this actually simpler?** 
      - It eliminates numbers and month names 
      - It is inherently reoccuring ... no need for actual dates for reoccuring 
      - Things like "every other week" or "every 4th week" or "every quarter" are intuitive and easy to understand 
      - No "the first DAY of MONTH" as that is what creates ambiguity 
      - We do need a "starting date" for recording things like every other week 
- Checking for Available Time Slots 
  - We need to create a script that reviews the calendar aka the ./configs/reoccuring/... directory 
  - Then provides time slots for the initial parameters provided 
  - How to handle amount of time to block out? 
    - We need natural gaps in the week and day in case someone is actually using the Mao app 
    - Unless, is it possible to design the app so that you can run multiple instances at one time? 
    - Or have "background" instances that are running even if you are using the app? 
  - `/avail --frequency every other week --day Monday`
  - I'm thinking 3 hour blocks, Eastern Time 
    - BLOCK 1: 0000-0300
    - BLOCK 2: 0300-0600
    - BLOCK 3: 0600-0900
    - BLOCK 4: 0900-1200
    - BLOCK 5: 1200-1500
    - BLOCK 6: 1500-1800
    - BLOCK 7: 1800-2100
    - BLOCK 8: 2100-0000

### We need to create a new .configs/reoccuring/ directories 

- Let's create a multi-subdirectory, primary directory 
- Base directory is .configs/reoccuring/.../ --> rest of directory just like .configs/workflows/ directory
  - .configs/reoccuring/scheduled/  --> workflows by user or Mao that occur every X time period 
  - .configs/reoccuring/project-list/ --> trigger every X time period; next project from list made by user or Mao
  - .configs/reoccuring/self-assessment/ --> trigger every X time period; self-assessment by Mao; state management 
  - .configs/reoccuring/goal-assessment/ --> trigger every X time period; goal-assessment made by user; state management 

---

### About Trigger Scheduled Workflows  

- `/triggered --scheduled .configs/reoccuring/scheduled/2_3_7` 

Above is the setup command we need with the flag type, and then, just like our other workflow JSON setup, we only need to provide the name of the directory because there will be multiple JSON files for the script to gather. 

#### Calendaring "trigger" JSON file `configs/reoccuring/scheduled/2_3_7/...`

Naming convention for the date trigger file to be pulled by the calendar script. This is carefully created so that they line up in the file according to their actual flow. The name of the directory shares the same information as the Calendaring JSON file without the "trigger_" prefix. 

- scheduled 
- frequency code 
  - 1 = every week 
  - 2 = every other week 
  - 3 = every month 
  - 4 = every other month 
  - 5 = every year 
  - 6 = every other year 
  - 7 = every day 
  - 8 = every other day 
- day of the week number (1-7 where 1 is Monday)
- time block (1-8 where 1 is 0000-0300)

The example below would be saved as: `configs/reoccuring/scheduled/2_3/scheduled_2_3_7.json`

```json
{
  "name": "scheduled_2_3.json",
  "schema_version": "1.0",
  "scheduled_workflow": [
    {
    "trigger_type": "scheduled",
    "trigger_frequency": "every other week",
    "frequency_code": "2",
    "trigger_day": "Wednesday",
    "trigger_day_of_week_number": "3",
    "trigger_time": "1800-2100",
    "trigger_time_block": "7",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "workflow_id": "{{WORKFLOW_ID}}",
    "created_on": "2025-07-20",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919"
    }
  ]
}
```

#### Triggered Scheduled Workflow JSON Configuration Files 

All of the other JSON files for this type of workflow can be the exact same as how we do it for standard workflows. The only difference is that the workflow_id is the same as the trigger_workflow_id in the Calendaring JSON file. 

**The first essential workflow JSON file that groups the rest of the workflow JSON files together** 

```json 
{
  "name": "scheduled_2_3_7_workflow_config.json",
  "schema_version": "1.0",
  "workflow": [
    {
      "user_id": "{{USER_ID}}",
      "workflow_id": "{{WORKFLOW_ID}}",
      "custom_command": "command-use-case",
      "workflow_goal": "Create comprehensive use case",
      "workflow_deliverable": "Use-case report",
      "workflow_description": "Identify what is needed to complete the goal. Build a workflow that delegates the work to the appropriate agents, having them work in parallel if needed. Leave the last phase opened-ended. Detail that handoff before the last phase with a list of questions Orchestrator will use to assess if the deliverable is complete, and if not, what is needed to complete it.",
      "temp_directory": "{{TEMP_DIR}}/command-use-case/"
    }
  ]
}
```

**The phase JSON file for the workflow; as many as needed** 

```json 
{
  "name": "scheduled_2_3_7_phase_config.json",
  "schema_version": "1.0",
  "phase": [
    {
      "workflow_id": "{{WORKFLOW_ID}}",
      "phase_number": "01",
      "phase_goal": "Create use-case report",
      "phase_deliverable": "Use-case report",
      "phase_description": "Research target market. Explore demographics in all socioeconomic status ranges, all geo-locations, all education level, but only females, married, and with a birthday coming up in the next 5 months. Research competitors; detail their marketing strategy.",
      "resources":[
        "./directory/folder/file.md",
        "https://file.com/folder"
      ],
      "tools": ["web_search", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-sonnet-3.7",
      "model_3": "claude-sonnet-3.5",
      "provider_1": "requesty",
      "provider_2": "anthropic direct",
      "provider_3": "anthropic direct"
    }
  ]
}

**The handoff JSON file for the workflow; should only need one to cap off the workflow** 

```json 
{
  "name": "scheduled_2_3_7_handoff_config.json",
  "schema_version": "1.0",
  "handoff": [
    {
      "workflow_id": "{{WORKFLOW_ID}}",
      "handoff_number": "01",
      "assessment_questions": [
        "How can I assess if this deliverable is complete?",
        "What is needed to complete that assessment?",
        "Do I have what I need to complete the assessment?"
      ],
      "human_in_loop": "no"
    }
  ]
}
```
---

### About Triggered Project-List Workflows 

- `/triggered --project-list .configs/reoccuring/project-list/project_001_2/...` 

Above is the setup command we need with the flag type, and then, just like our other workflow JSON setup, we only need to provide the name of the directory because there will be multiple JSON files for the script to gather. In fact, at first, there might not be any workflows depending on the project. 

#### Calendaring "Project-List" JSON File 

**The Directory Name** 

This will always be the same except for the first part of the name which is based on the type of triggered workflow. 

- project 
- frequency code 
  - 1 = every week 
  - 2 = every other week 
  - 3 = every month 
  - 4 = every other month 
  - 5 = every year 
  - 6 = every other year 
  - 7 = every day 
  - 8 = every other day 
- day of the week number (1-7 where 1 is Monday)

**JSON File Name for Project List Calendaring Entry**

This is one of the only times so far that the directory name is not the same as the JSON file name. This was done to keep the directory name clean, simple, and better sorted. 

`configs/reoccuring/project-list/project_001_2/project_001_analytics_report_plan.json`

Naming convention for the project list file to be pulled by the calendar script. This is carefully created so that they line up in the file according to their actual flow and importance at the time of creation.

If something changes regarding the project urgency, add "URGENT" to the "notes" field. Make no other changes to the files. 

"Created on" is for when the JSON file was created. 

The example below would be saved as: `project_001_analytics_report_plan.json`



```json
{
  "name": "project_001_analytics_report_plan.json",
  "project_name": "Analytics Report Plan",
  "schema_version": "1.0",
  "project_list_workflow": [
    {
    "trigger_type": "project-list",
    "trigger_frequency": "weekly",
    "frequency_code": "1",
    "trigger_day": "Tuesday",
    "trigger_day_of_week_number": "2",
    "trigger_time": "0900-1200",
    "trigger_time_block": "4",
    "start_date": "2025-07-23",
    "end_date": "N/A",
    "list_placement": "001",
    "priority_level": "medium",
    "priority_level_number": "2",
    "workflow_id": "uid-aqb-907",
    "created_on": "2025-07-28",
    "created_by_username": "seanivore",
    "created_by_user_id": "user-1642",
    "notes": "none"
    }
  ]
}
```

#### Triggered Project-List Workflow JSON Configuration Files 

These are the same as any other workflow. Because of the nature of this project however, Mao might not make a workflow right away. They also might end up making multiple workflows. I'd imagine for this project they would create a plan first. 

---

### About Triggered Self-Assessment Workflows 

- `/triggered --self-assessment .configs/reoccuring/self-assessment/001/...` 

Above is the setup command we need with the flag type, and then, just like our other workflow JSON setup, we only need to provide the name of the directory because there will be multiple JSON files for the script to gather. 

In this case, we will only be using the assessment count as the directory name. This is because the assessment count will be the same for all workflows in the directory and it is part of the name of the JSON files. 

**The Directory Name**

- self_assess
- assessment_count = 001
  - Three digits always 
  - This should be the number based on how many times Mao has done an assessment
  - If this is an entry for a second part of an earlier assessment, it should get a number that is still consecutive  


 
```json
{
  "name": "self_assess_001.json",
  "self_assessment_count": "001",
  "schema_version": "1.0",
  "self_assessment_workflow": [
    {
    "trigger_type": "self-assessment",
    "workflow_id": "uid-xoy-572",
    "created_on": "2025-07-28",
    "created_by_username": "Mao",
    "created_by_user_id": "user-0919",
    }
  ]
}
```

**JSON File Name for Self-Assessment Calendaring Entry**

Directory: 
- `configs/reoccuring/self-assessment/001/self_assess_001.json`

File: 
- `self_assess_001.json` 

#### Triggered Project-List Workflow JSON Configuration Files 

These are the same as any other workflow. Because of the nature of this project however, Mao might not make a workflow right away. They also might end up making multiple workflows. I'd imagine for this project they would create a plan first. 
