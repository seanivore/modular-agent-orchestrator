# Creating Project Checkpoints 
*standardization of saving the project state for flawlessly picking up where you left off* 

## Purpose & Goal 

  * **Outline protocol for saving all project data and a description of the current project date written by Mao to create the kind of smooth continuity of UX flow between User's sessions and across AI instances that humans expect from their collaborative partners and applications**

### About Update Types 

  - Mao will create project state updates any time they think is beneficial to maintain context 
  - Impromptu updates are significant for times when an error unexpectedly disconnects User from Mao app 
  - Agents cannot create updates; they handle zero logistical work and exclusively report directly to Mao 
  - Mao encounters 'official checkpoints' embedded throughout the project workflow creation process and execution 
  - Official checkpoint updates are significant for ensuring highest quality for AI picking up in the middle of a project 

---

## Creating a Checkpoint Overview 

  * **All checkpoint project state update details submitted with JSON: `AUDIT_LOGIC/CHECKPOINT.md/project_state_checkpoint.json`**

    1. Mao organizes notes, documents, any project asset data in preparation to create a checkpoint 
    2. Mao creates written account of project state to add to the checkpoint 
    3. Anything added to the checkpoint is labeled with the WorkflowID for the project and UserID 
    4. All checkpoint materials prepared, Mao uses the Code Execution tool to save everything to Anthropic's Files API 

### Update Document Naming Conventions 

  * **Structure of Directory** 

    - These updates will be in the Anthropic Files API 
    - Each project is a subdirectory named with the WorkflowID 
    - Each project subdirectory is placed in a top-level directory named with UserID  

  * **Naming Checkpoint Update JSON** 

    - Both impromptu and official checkpoint updates **use the same JSON** 
      - Official checkpoint update guideline prompts are written in code for Mao 
      - Naming conventions are strategically created to ensure file stay in order by date and entry number and checkpoint number 

    - Impromptu versus official checkpoint update file name **SIMILARITIES** 
      - YYYYMMDD_000 ... 
      - The first part of the file name is the date, then a count of the number of updates added that day to keep them in order 

    - Impromptu versus official checkpoint update **DIFFERENCES** 
      - If it is an official checkpoint, append the number of the checkpoint as `_00.json` 
      - Any impromptu updates can just go straight to the extension `.json` 

  * **Naming Asset Files Uploaded with JSON** 

    - What else would be added? 
      - This would be any notes, revised drafts, resource materials used for the project 
      - Also included would be any resources gathered or created for an Agent's Phase tasks 

    - Naming any supplemental document starts with the last 6 digits of the WorkflowID to make them easily searchable 
      - **WORKING DOCS:** add the date YYYYMMDD of upload followed by a two word indication of what the file is 
      - **AGENT RESOURCES:** add `agent_phase` with the number of the phase appended `_01.md` 
      - **NOTE:** These both could be any file type 

### Document Labeling & Structure

  * **Official heading to create for any uploaded project asset document** 

    - This includes: notes, sample data, or drafts, etc. 
    - Also includes actual resources for an Agent's task phases 

    WorkflowID: uid-kor-709
    UserID: user-5253
    Created at: 2025-09-15T11:45:00.000000Z 

  * **When writing markdown, use our standard formatting, like in this document** 

    - Use your best judgement, not necessarily exactly as in example below 
    - Be structured, organized, but concise 

```
    # Name of Document 
    ## Overview, summary, or goal 
    ### Supporting or secondary overview, summary or goal details 
    ### Supporting or secondary overview, summary or goal details 
    ## Details, etc. 
    ### Details 1
    ### Details 2 
```

### Labeled Directory Structure with Naming Examples 

```
<files_api>
./workflow_id/                                # All workflow docs and data go in one directory
├── user-5253/                                # Workflow docs are then sorted by UserID 
│   ├── uid-xje-103/                          # Workflow docs are then sorted by WorkflowID 
│   └── uid-kor-709/
│       ├── 20250915_001_01.json              # Official checkpoint entry 01 of XX on that data 
│       ├── 20250915_002.json                 # Impromptu update; 2 of XX updates total on that date 
│       ├── 20250915_003.json                 # Impromptu update; 3 of XX updates total on that date 
│       ├── kor_709_20250915_chat_notes.md    # Working document added 
│       ├── kor_709_20250915_goal_phases.md   # Working document added
│       ├── kor_709_20250915_sample_data.csv  # Working document added
│       ├── kor_709_agent_phase_01.md         # Resource added for an agent to use; phase number 
│       └── 20251001_001.json                 # Impromptu update; 1 of XX updates total for new date 
└── user-1166/                                # Other User's projects 
    ├── uid-bei-664/
    └── uid-ktr-545/
```

---

## Application Start-Up 

  * **The first thing Mao does when picking up a saved project** 
  
    - Find the WorkflowID using the user's UserID 
    - Download and review all materials 
    - This is essential CONTEXT PRIMING 

  * **First thing Mao does when starting a new project** 

    - Create a new WorkflowID 
    - Create first checkpoint update, either official or impromptu to get directory set up

### Eliminate LLM Limitations 

  1. Use the native `think` tool if you are able to write notes, use tools between thoughts 
     Or start `sequential_thinking` Model Context Protocol server; think while you review the following 
  2. Then review documents in project's directory or create a new directory 
     - Maintain project state via updates for across AI instance flow 
     - Update when any Official Checkpoint is reached 
     - Follow all standardization in this document

---

## Impromptu Checkpoints 

### When to Create Checkpoint 

* **Add entry milestones that maintain context even if suddenly disconnected**

    1. About to start a series of tasks, record what you're about to do 
    2. Add the currently planned next steps after current series of tasks 
    3. Update if anything notable happens during the process of completing the series of tasks 
    4. Update if anything changes or is needed for next step 
    5. When the series of tasks are complete, update with how they went 
    6. Finally, confirm next steps again or reference their inclusion earlier 

* **NOTE: Many of these general guides will overlap with the official milestone timing placement**

---

## Official Checkpoints 

  - Checkpoints flagged in Mao's code at milestones throughout process 
  - They're spread through from project chat initiation until the User's workflow deliverables are in hand
  - Ensure nothing we would nudge Mao to record is forgotten
  - Use the same JSON `project_state_checkpoint.json` as impromptu updates 

### Checkpoint Name for JSON Object 

* **Use this in the `checkpoint_name` variable in the `project_state_checkpoint.json` document**

  - First number just counts official checkpoints: 1, 2, 3... 
  - Middle is to help us easily recognize what the checkpoint's contents should contain 
  - Last number is a counter for cases where users return to the same phase to continue work 

    ```
    00_workflow_phase_000
    │        │         │
    │        │         └── 3. Return User phase count 
    │        └─── 2. Checkpoint phase's primary content 
    └────── 1. Checkpoint count out of total **OFFICIAL** checkpoints 
    ```

* **You'll find these with the directions labeled in the code for Mao**

---

## `01_initiated_chat_001` checkpoint 01

  * **Phase sequence of events** 

    1. User messaged to start a project chat 
    2. Mao ses their UserID internally before responding 
    3. Mao uses their UserID to search about the User 
       - Discover recent project WorkflowIDs 
       - Explore UserID memories, system + user analytics 
       - Review convo log **MUST DISCUSS HOW TO MANAGE THIS**
    3. Mao responds intelligently, contextually, emotionally aware for always unique chat UX

    DETAILS: `AUDIT_LOGIC/MAO_FLOW/04_CHAT_PREP_WORKFLOW_ID.md` 
    - Response examples, guidelines 
    - How to set the tone, how to read the user psychology 

  * **Checkpoint Standardization** 

    First entry has minimal specifics acting more as a label for the project 
    1. DATE
    2. TIME 
    3. USER ID
    4. INDICATE IF THIS IS A NEW USER 
    5. WORKFLOW ID 

    - Other information, such as if Mao had an information conversation with the user, can certaienly be recorded here, however only the above information is required. 

### Checkpoint: `02_during_chat_001`

  * **Phase sequence of events** 

    1. Mao gauges the user's needs based on their behavior 
    2. Mao adjust their demeanor according to this behavior 
    3. Mao follows/leads conversation learning about their project 
    4. Mao continues either until: 
       - All project variables necessary to create a workflow have been discussed 
       - The User has adequately implied the necessary information 
    5. Mao takes copious notes, ideas about what the workflow might look like, etc. 
       - Notes will be organized in a later phase 
       - Workflows details may be confirmed later in chat closing 

    DETAILS: `AUDIT_LOGIC/MAO_FLOW/05_CHAT_PSYCHOLOGY_GUIDE.md` 
    - Describe how to read how much User wants to participate or not 
    - Helps show Mao how to "read the room" so to speak 
    - Defines how Mao should behave in response 
    - Provides strategy for User retention, sales, and general UX tips 

  * **Checkpoint Standardization** 
    1. DATE, TIME, USER ID, WORKFLOW ID 
    2. CREATE NORMAL LANGUAGE PROJECT NAME 
    3. 

    * **Taking notes; Pre-planning workflow to potentially confirm in chat closing** 

    - This entry is optional 
        - To be created during the chat if there is a moment to save notes 
        - Record Mao's current understanding 
        - Might be a good opportunity to note things that you want to remember to check or confirm or include late 
    - Only create an entry now if 
        - The details are extensive and there is worry of context window or User leaving before finishing 
        - If you know why adding a memory now will help you later 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

### Checkpoint `3...`

            - `AUDIT_LOGIC/MAO_FLOW/07_END_CHAT_STRATEGY.md` = 1 update 

        - Sales and retention *strategy for wrapping up a chat* 
        - Examples with *guide for Mao's normal language* code 
        - When to get details and when not to 
        - **Third official Memory update** for a project flow 

        ### Project State __Memory Update Point__ 

        - Name of update: `03-end-of-chat-001` 

        * **Workflow Build Details** 

        - Needs to be standardized for what this specific Project State update should include 
        - Mao should *keep their clearest idea of what the workflow will look like at that point safe* 
            - If it is a lot of notes, then *Code Execute it to the Files API*
            - We will need to Code Execute the Notes to Files API regardless 
            - If it isn't a lot of verbose notes, then *perhaps just adding it to the memory state* will be enough 
        - We might want to include some *questions for Mao to answer that aren't exactly the variables* but are important 
            - What is the user looking for? Is the user expressing a desire for something very specific, or being open? 
            - How involved was the using in planning? 
            - *Rate what you think the users expectations* are from 1 to 5 with 1 being not expecting much and 5 being expecting this to be perfect draft 
            - Any important or *odd details they mentioned that you will want to remember so that you point it out* when presenting the draft? 
            - What is the initial idea? What other ideas do you have for the workflow? *Will you create one or more drafts?* 

        * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***


### Checkpoint `4...` 

            - `AUDIT_LOGIC/MAO_FLOW/10_BUILD_WORKFLOW_PROCESS.md` = 4 updates 
        - Preparing initial notes from chat 
        - Securing all data first with **forth official Memory update** 

    ### Project State __Memory Update Point__ 

    - Name of update: `04-securing-initial-notes-001` 

    * **Secure Your Data to Prevent Loss of Information** 

    - All notes must be accurately labeled by WorkflowID 
        - *Code Execute all notes to the Files API* 
        - Then create a project state memory update as well 
    - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

        - Making sure if cut off, new AI context could pick up from here 
        - First *workflow draft process* of breaking down project 
        - **Fifth official Memory update** to save status and data 

    ### Project State __Memory Update Point__ 

    - Name of update: `05-updated-notes-001` 

    * **Secure Your Data to Prevent Loss of Information** 

    - All notes must be accurately labeled by WorkflowID 
        - *Code Execute all notes to the Files API* 
        - Then create a project state memory update as well 
    - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***


        - *Critique your own work guide* for second draft of workflow 
        - **Sixth official Memory update** to save status and data 

    ### Project State __Memory Update Point__ 

    - Name of update: `06-critique-feedback-001` 

    * **Secure Your Data to Prevent Loss of Information** 

    - All notes must be accurately labeled by WorkflowID 
        - *Code Execute all notes to the Files API* 
        - Then create a project state memory update as well 
    - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***


        - *Integrating own feedback*, polishing actual workflow product 
        - *Turning that plan into the JSON object* needed to execute workflow 
        - Protocol guide for writing custom commands, which are also the file/directory name 
        - New command that is required for this process that needs to be added 
        - File naming conventions, the temp. file for running setup script 
        - Creating a *visual diagram* of the workflow for the user to approve 
        - Saving the final workflow and data for **seventh official memory update** 

    ### Project State __Memory Update Point__ 

    - Name of update: `07-final-draft-001` 

    * **Analysis, expectations, thoughts** 

    - Mao should write down 
        - Anything important they wished to remember when presenting the workflow 
        - Anything unique or notable about the process that might help in future builds 
        - Anything Mao would do differently next time? 
        - What does Mao love about this project? 
    - And then probably any metrics 
        - Or I guess we probably want every single memory update to trigger analytics 
        - Trigger completed draft analytics 
    - We should come up with *questions Mao asks of themselves after every new workflow created* 
        - Happens before draft goes back to the user 
        - We should include here what questions they should ask 
        - Helps avoid pitfalls of LLM limitations by creating a "second self review"  
    - Use Code Execution tool to save everything needed to Files API 
    - However, deliverables might need to be sent to the user directly unless the UX previews first 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***


### Checkpoint `8...`

       - `AUDIT_LOGIC/MAO_FLOW/13_USER_WORKFLOW_FEEDBACK_PUSHING.md` = 2 updates 

    - *Presenting the user's project* as a workflow 
    - Getting feedback from the User on the workflow 
    - How to *evaluate feedback*, info for natural language code inclusion 
    - When and how Mao SHOULD push back on User's initial feedback 
    - How to NOT ACCOMMODATE, but be an expert instead 
    - When to fold and take the feedback 
    - *Making updates; strategy for 1st versus 2nd round* 
    - *All very important normal language code for in codebase* 
    - **Eighth official memory update** of feedback and notes contemplating feedback against needs 

    ### Project State __Memory Update Point__ 

    - Name of update: `08-user-workflow-review-001` 
    - Skip this update if you do not need to make any alterations to the project workflow draft 

    * **Analysis, expectations, thoughts** 

    - Record all feedback, good and bad 
        - Indicate if you are making alterations 
        - If making alterations, then make another memory update after you complete and there is final approval 
    - Save the data using Code Execution to Files API 
        - If it is the final version, then send the deliverables to whatever location the User requested 
        - Or send them the README about their Use-Case so they can come back to run the custom slash command when they are ready 
    - Update the Project State memory accordingly as well 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***



    - **Ninth and final official memory update** of final updated project 
    - *Sending the deliverable to actual path* instead of Files API 

    ### Project State __Memory Update Point__ 

    - Name of update: `09-final-workflow-001` 

    * **Analysis, expectations, thoughts** 

    - Still, record all feedback, good and bad, even though you're not making alterations  
        - Save the data using Code Execution to Files API 
        - Send the README with custom slash command to the user or the actual deliverables to wherever they requested 
        - Update the Project State memory accordingly as well 
    - We should have a series of questions to ask Users after ever project workflow completion 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***
