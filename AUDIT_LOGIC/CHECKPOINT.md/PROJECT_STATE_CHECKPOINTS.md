# Checkpoints & Project State Updates 

## Goal 

  * **Create the smooth continuity of UX flow between User's sessions and AI instances that humans expect in their collaborative partners and applications**

### About 

  - Mao can create a project state update any time they think is beneficial for the goal 
  - Agents cannot; they handle zero logistical work and only report directly to Mao  

### Overview 

  1. All project asset data is secured in the Anthropic Files API 
  2. Includes a written account that serves as "Memory" context for that section of the User session 
  3. Mao must use the Code Execution tool to save anything to the Files API 
  4. Assets and memory is organized and connected using the WorkflowID and the UserID 

---

## Official Checkpoints 

  - These are predetermined checkpoints flagging milestones throughout the entire process   
  - Project State entries are anchored in context throughout the process with relevant prompts 
  - They're placed at the start of a project chat, until the User's workflow deliverables are in hand 

### Standardizing the Checkpoints  

  1. Ensure nothing we would nudge Mao to record is forgotten  
  2. Implement these checkpoints and their prompts into the codebase 
  3. Create protocol for archiving entries to keep Files API clean as a working space 

### Checkpoint Numeric Coded Naming 

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

## Saving Project State to Checkpoint 

### Project Assets 

  1. Organize all current documents created when working on the project including drafts and notes 
  2. Rewrite notes if needed to ensure that someone else, another AI, will understand if they need to 
  3. Clearly label these documents to maintain their organization and purpose when returning to them 
  4. Keep the WorkflowID and UserID easily locatable on the document or header  
  5. The WorkflowID's last 6 characters should start **EVERY AND ANY** file in the Files API storage 

### Project State Memory Context  

  1. Project state memory entry is created on a prepared JSON template   
  2. Define the task, make sure any new AI reading will understand exactly what was being done 
  3. Include any interesting updates from during or after the task that may be important or insightful 
  4. If planned or discussed, please then detail what the next tasks are to follow this task 
  5. This is ESSENTIAL for help our AI instances create a flawless UX; ask, what would I need to know 



**CONFIRM** 
  - Do we want top level grouping by UserID? 
  - WorkflowID directory makes sense 
  - I think naming the subdirectories by checkpoint makes sense 
  - But then how does AI want to format filenames inside this and any other subdirectory of a workflow directory? 
  - FYC they could potentially REMOVE 'uid' because it will be on the front of all workflowIDs 
  - Date seems to make sense but does a three digit counter? 

```
├── user-5253/
│   ├── uid-kor-709/
│   └── uid-xje-103/
│       └── 01_initiated_chat_001/
│           └── mem-xje-103_20250910_001.json
└── user-1166/
    ├── uid-bei-664/
    └── uid-ktr-545/
```








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
