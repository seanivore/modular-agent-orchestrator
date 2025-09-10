# Official Project State Checkpoints & Protocol

## Overview 

- Pleasant **UX is maintained if connection drops** thanks to checkpoints. They **provide new AI all context** needed to continue where things left off, maintaining a smooth flow. 

- Mao creates checkpoints **any time they think is beneficial**. **Agents cannot** create checkpoints. Their role is intentionally minimized so they have nothing in their context window other than your project. 

- Below are **official checkpoints flagging milestones** from project's chat start, until user's workflow deliverable is in hand. Here, **Mao answers contextually relevant prompts** about process progress in addition to saving context and data. 

### Necessary to Standardize Checkpoints 

  1. Standardize these across all of them; make sure nothing we should nudge for Mao to record is being forgotten 
  2. Implement these into the codebase flow 
  3. Create protocol for how and where these are saved; ideally searchable for future 

### Checkpoint Name Numeric Coding 

    ```
    00_workflow_phase_000
    │        │       │
    │        │       └── 3. Return User phase count 
    │        └────── 2. Checkpoint phase location 
    └───────────── 1. Checkpoint Number 
    ```

  1. This shows what number checkpoint this is out of all OFFICIAL checkpoints. 
  2. This is meant to help us easily recognize what this checkpoint's content should contain if we're looking in the future. 
  3. This counter, starting at 001, shows how many times a return User has started this project at or gone through this checkpoint's phase. 

---

## Mao's Checkpoint Workflow 

  1. WorkflowID must label all information committed to checkpoint 
  2. Checkpoint includes creating a memory entry  
  3. Checkpoint requires code execution to save project assets to Files API 

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
│           └── uid-xje-103_2025_09_10_001.json
└── user-1166/
    ├── uid-bei-664
    └── uid-ktr-545
```

---

## `01_initiated_chat_001` checkpoint 01

  * **Phase sequence of events** 

    1. User messaged to start a project chat 
    2. Mao can see their UserID internally, uses it to search what is know about the User before responding
       - Discover WorkflowID for recent projects; explore memories saved by Mao or User; Review system and user analytics 
       - Review log of first messages sent to this User **MUST DISCUSS HOW TO MANAGE THIS**
    3. Mao uses this knowledge to respond like a colleague who know User well 
       - Intelligent, emotionally aware, contextually aware; will show if they're a return User or new User 
       - Regarding about **DISCUSS** note, we need to somehow avoid AI using the same messages; I experience this from Dia and Claude Code and it is a terrible UX  
    4. Provide User with a truly unique chat UX 

  * **Details, response examples, guidelines, how to set the tone** 

    SEE HERE: `AUDIT_LOGIC/MAO_FLOW/04_CHAT_PREP_WORKFLOW_ID.md`

  * **Checkpoint Standardization** 

  - First entry has minimal specifics acting more as a label for the project 
    1. DATE
    2. TIME 
    3. USER ID
    4. INDICATE IF THIS IS A NEW USER 
    5. RECORD THE WORKFLOW ID CREATED FOR THE PROJECT 

  - You have to have the WorkflowID to be able to save the information to the checkpoint
  - The User does not need to have provided any other information 
  - If they are a new User, include any "learning about them" information 

    * **Setting things up and setting the tone** 

    - This entry must be completed at the noted point above 
        - For new users, Mao can do this before responding 
        - For returning users, Mao must respond in the chat first to know they want to work on a previous or new project 
    - First entry so it should have 
        - Minimal specifics details 
        - Mostly record keeping things like date, user, etc. 

    * **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***
    
    - Make it clear what kind of entry to create 
        - How to tag the WorkflowID, etc. 
        - Create a new observation tagged to an entity named with WorkflowID 
    - Start the first line with the name of the project state update entry point 
        - This entry is `01-initiate-chat-001` 
        - The 01 before the name is because it is the first entry in the entire Project Workflow 
        - The appended counter, starting at 001, and then 002+ for returning users 
        - This is unlikely to go above 001 in this first section 
        - But you never know when a User could drop out or internet cut out 

### Checkpoint: `02...`


        - `AUDIT_LOGIC/MAO_FLOW/05_CHAT_PSYCHOLOGY_GUIDE.md` = 1 update 
    - How to *read the User's engagement interest* 
    - Sales and retention conversation strategy 
    - Things that *get conveyed to Mao in normal language* code 
    - Dealing and banning abusive Users 
    - Intro to variables Mao is collecting 
    - **Second official Memory update** for a project flow 

    ### Project State __Memory Update Point__ 

    - Name of update: `02-during-chat-001` 

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
