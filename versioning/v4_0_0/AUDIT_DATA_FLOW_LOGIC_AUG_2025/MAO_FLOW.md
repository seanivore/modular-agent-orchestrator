# Flow of Data Through Mao 

## Overview   

Cleaning up code 'mock data' uncovered hardcoded category suggestion woven throughout. In trying to rectify this, I found large portions of code I cannot understand and AI couldn't fully define the logic. We NEED this level of understanding, period. This makes it clear that we have over engineered. Mao's task is incredibly simple and relies primarily on natural AI abilities. By creating this outlined flow of data we will have comprehensive understanding of what file code logic should be. It will be compared as we work through current files, cleaning up, optimizing, simplifying, and adding missing elements in the outline as we proceed. 

### Summary  

Outline comprehensive flow to understand what the logic should be, then compare it to each file's current logic, so we can clean up files accordingly. 

### Goal 

This final 'logic audit' will leave us prepared to launch the app in our terminal as a development tool for testing, before developing web UI. 

### Opportunity  

  - Look at all files through the lens of creating a Web UI instead of our originally planned Terminal UI 
  - Ensure files are prepared to launch after developing multilingual capabilities in parallel 

### Deliverables 

* **This comprehensive file which will provide various values** 
  - Plain language description of logic 
  - True understanding of dataflow allowing for better documentation 
  - Provides a vision for the UX and UI needs 
  - This is very similar to our, now dated, `_NEW_USER_FLOW.md` file 

* **Simple, clear, concise diagrams of information flow** 
  - Prior attempts were consistently convoluted due to our over-engineering 
  - Being able to create these will serve as a form of proof of concept 
  - Provides legitimacy to brand, tool, and team due to easy of understandability 

* **Opportunity to ensure standardization and consistency across configs, memory state updates, and more** 
  - Many features were implemented in the midst of development 
  - This will ensure it was done correctly, comprehensively, and allow for creation of standardization guides 

### Procedure 

1. We will proceed through the sections below 
   - Identifying where this happens in current files 
   - Ensure it is happening properly, without any additional functions or complexity 
2. In first run we will catalog what changes need to be made 
   - We want to see the full picture before we start editing any files 
   - We might find opportunities to simplify or combine multiple, extremely similar purposed files 
3. The update our code file making changes as needed 
   - This also includes updating this outline with any missing information 
   - Notion should also be added to this outline indicating what file handles each bit of the logic and data flow 
4. Fill in all blanks, complete any missing information; "finish the job" 
   - Shouldn't have to say this ever, but this IS real code implementation  
   - Do not skip any concept expecting to come back later, each fix and completion should be handled in proper sequence 
   - Standardize any of the newer features and confirm other features have already been standardized across-the-board 
5. Implement the remaining items needed for launching the development terminal UI app 
   - We have been detailing this information in `MAO_LAUNCH.md` 
   - When complete we should be able to focus exclusively on bugs and then building web UI 
   - Set ourselves up for success building web UI by thinking forward at all times 

---

## 1. User Login 

### Core Objective 

  1. Secure login 
     - Setup passkey or traditional login 
     - Passkey requires providing email or phone as unique identifier once 
     - Traditional login requires email or phone unique identifier every time 
  2. Locate or create UserID 
     - Returning users, UserID is located from directory via unique identifier 
     - New Users, automation creates a UserID during setup
     - Automation also setups up their user config directory 
  3. UserID follows User around application 
     - Behavior logged and tracked in analytics files in their User config directory
     - Anonymous data and system data is also triggered and logged at various points
     - UserID used to obscure identity in some analytics 

### Secure Login Setup UX/UI 

  - I love PORKBUN DOMAIN'S login flow 
    - We have replicated it in our `./versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` secure login implementation plan 
    - The legal jargon has been edited slightly 
    - This is how it works and how each element is displayed and when 

* **Log in to an Existing Account** 

  - This is the main page you are routed to 

  - Field to *Enter your email or phone* user identification  
  - Standard *password* field 

  - *NOTE* under password it says "Leave password blank if using a passkey" 
    - This is an extremely low risk precaution that is better than saying "you don't need to enter" 
    - The passkey login works even if you enter something you think might be your password into the field 
    - The system just ignores the password when using passkey; *this creates flawless UX*
  - Cloudflare auto-secure anti-spam *requires no action by the user* 
  - Included *Remember Me* check mark 

  - Porkbun does not make it clear that clicking LOGIN will bring up the passkey 
    - I suppose this is expected 
    - Toy with wording to potentially use 

  - *Legal jargon:* By continuing you agree to the following: I acknowledge that I have read and agree to all Product Terms of Service, the Marketplace Agreement, and the Privacy Policy. You consent to enroll new automatic monthly subscription renewal service, which can be cancelled at any time via the Personal Preferences Billing section of your account. Automatic renewals are billed to payment method(s) specified on your Account Settings page until cancelled. If paying by credit card, you authorize {{ENTITY}} to send instructions to the financial institution that issued your card to take payments from your card account in accordance with the terms of your agreement with us. 

  - The *Create a New Account* is in a box above the field, as well as right next to the login button at the bottom of the field 
  - *Forgotten password, 2FA, or security key* link is below the login and second create new account button 

* **Create New Account**

  - This is a separate page navigated to from the initial login page unless directly linked from elsewhere 

  - This form also uses a Cloudflare auto-secure anti-spam *no action by user* widget thing -- NO CLICKING BIKES FOR GOOGLE CAPTCHA 

  - Instead of *USERNAME* we should say *ACCOUNT ID* above text field 
    - Under it says "Use a valid contact identification; you will be messaged to validate this ID one time during setup" 
  - Then PASSWORD above a field 
    - Under again in small text indicate parameters like *Must be 12 to 72 characters long, differ from your account ID, etc.* 

  - Directly below the PASSWORD text field there is a button that says *USE PASSKEY* 
    - Setting this up automatically provides all information we are requesting in this form 
    - This is the best UX, we will feature it prominently 

  - Traditional form *REQUIRED* fields 
    - First Name 
    - Last Name 
    - Checkmark acknowledgement legal jargon regarding having read our terms of service and privacy policy 

  - Traditional form fields that are *NOT REQUIRED* 
    - Company Name 
    - Standard 'will you be using this for personal, business, etc. 
    - What do they play on working on to delegate to AI agents for completion 
  - We should brainstorm these questions 
    - So that we can be sure to NOT include many 
    - Ensure we are only including the best 
    - Heavily workshop the copywriting for wording that encourages users to submit the information 

  - We should mention that they will need to set up subscription payment on the next page 
    - Consider free trial 
    - Or perhaps creating a login lets them look at all the different configs available and what the interface is like 
    - The UX and design of our payment page will be handled by Stripe 

  - The form has a *CREATE ACCOUNT* button at the bottom with a *LOGIN TO EXISTING ACCOUNT* button beside it 

  - *Note:* "The word “passkey” *does not translate cleanly in every language*. Pair it with a short explanatory subtitle such as “Faster, one-tap sign-in with your device" advice given to me by AI when asking about pushing Passkey usage for our multilingual launch. Let this stand as a note reminder that we must check these kind of things, rather than just simply translating pages. It sounds like there might also be some issue with certain countries; this makes me think that we *likely will want to exclude our services to certain countries* as well. 

### System Locates or Creates UserID with User Directory 

* **UserID is created at first login**

  - It uses their *ACCOUNT ID* from the login information 
  - The `meid` script is used 
    - Provides the same UserID every time you enter the same Account ID 
    - Will always be formatted as `user-####` 
  - This example runs the `meid` as a script in the terminal for illustration 
  - As you can see, various phone number formats work, as well as the entirety of my email address 
    - the Account ID must always be *one single string of characters* 
    - *Our form fields should be strict in forcing specific formatting* known to work 

```bash 
  > meid horvathaugust@gmail.com            # Used entire email address; must be single string of characters 
  Username 'horvathaugust@gmail.com' -> user-5253    # Response; UserID follows user around application
```

```bash
  > meid 424-744-7687
  Username '424-744-7687' -> user-0697      # Hyphenated phone number
  > meid 4247447687
  > meid 424.744.7687
  Username '4247447687' -> user-0697        # No hyphens or periods has same result 
```

* **User directory setup automatically during New User Setup** 

  - User `./configs/user/` directory, *as structured below*
    - Includes other essential user data files 
    - Core for logging preferences and more 
    - Analytics files are created and updated as user interacts with the app 

  - *NOTE:* we need to update the JSON objects and possible code 
    - We shifted away from using a random user created 'username' 
    - And instead will only use Account ID that we know will be unique by design 
    - the file name and directory names are changed from username to UserID, for example  

```
configs/user/...
└── user-5253      # Since we have multiple unique identifiers, the directory must be named with the UserID 
    ├── analytics                       # All need to be reviewed and labeled
    │   ├── cost_tracking.json 
    │   ├── session_metrics.json
    │   ├── tool_usage.json
    │   └── workflow_metrics.json
    ├── memories                        # Review, label, detail management details in codebase, updates 
    │   ├── personal_preferences.json
    │   └── project_context.json
    └── user_seanivore.json             # Delta-only storage of User application preferences 
``` 

* **User login that has logged in before** 

  - The system searches the `./configs/user/` directory for their *Account ID*
    - They find their *UserID* in their user documents 
    - This will be needed throughout the process 
  - A *UserID can also be used to pull up any of the user's information* 
    - Most recent workflows they were working on 
    - System settings and preferences 
    - Change their default model and provider of choice 

* **The first user analytics are triggered at this point** 

### Project State **Memory Update Point**

  - None yet, the first happens in next session when Mao enters the chat 
  - At the end of each section, like this H3, we will detail and name the Project State memory update 
  - This is the start to ensuring they are standardized and planned 

---

## 2. Start Chat & Mao's Setup

### Core Objective 

  1. Chat is started 
  2. Setup WorkflowID for new project 
  3. Initiate Project State memory system use 
     - New project requires first simple entry defined below 
     - Returning users; Mao searches their UserID and pulls up information to facilitate chat 
  4. Create a truly unique UX using *memory* and *data analytics*     <-- This is the future, thanks to AI 

### User's Role: Initiate Project Chat 

* **The User will always initiate a project chat first** 

  - They can send *anything* into the chat to start the flow 
    - Certain slash commands *DO* start flow 
    - Most slash commands do not start flow and are just operational 
    - Mao might respond to some operational slash commands, but this is not the same as initiating a project chat 

  - Slash commands that *DO* initiate project chat 
    - Exception example #1: `/chat 'your message'` which jumps right to the chat and starts the first message; this was primarily created for the terminal app because using `mao --chat 'your message'` would start the app and send that chat; with a web app this command is sort of pointless but there is no need to remove it; users might use it to initiate a project chat after using some operational slash command, for example, not that it is necessary 
    - Exceptions example #2: `/goal 'user project goal'` is the primary legitimate slash command that does initiate a project chat; this command is run to create an instant workflow where Mao uses nothing but the goal; this effectively jumps Mao past any back-and-forth conversation, as the goal is the only provided variable and Mao would respond with a simple 
      > "Got it! Give me a moment to draft up a workflow for your review." 

* **Sometimes the first message doesn't initiate a project chat** 

  - In certain cases, we may have Mao respond to operational slash commends where it makes sense to create a better UX 
    - We need to work out the logic for these one by one, on a per-command basis 
    - Some slash commands just pull up a toggle menu 
    - Trying `/workflow 'workflow custom command'` to jump back into setting up a project 
    - Using `/variables-explain` makes sense for Mao to facilitate instead of just DROPPING a bunch of text on them  
    - Using `/tools` or `/providers` or `/models` or just `/variables` 
      - These could bring up UI or Mao to chat; we should figure out what makes the most logical sense 
      - Or how could one method combine UI in some way (like if models showed them all but also then let them set defaults)

### Mao's Role: Come To Chat Prepared 

* **Getting the WorkflowID is Mao's first essential task** 

  - Every new project needs a WorkflowID  
    - This is done on the backend, but it uses the terminal command script `uid` 
    - Every time you enter `uid` it comes up with a COMPLETELY DIFFERENT string of characters 
    - It is always `uid-ABC-123` starting with uid, then three letters, then three numbers 

  - This is *extremely important to ALL WORKFLOW PROCESSES*
    - Mao uses it to label memories saved about the workflow 
    - It *labels items saved in the Files API*
    - It is the string that connects all workflow pieces together 

  - The 'WorkflowID' and the workflow's 'Custom Command' identified on the JSON workflow config are the only two unique identifiers available to the User on every single project; any other IDs used on the back end should be minimized, only used if absolutely necessary, and hidden from the User 

```bash 
  > uid                        # No input required 
  Generated UID: uid-xhl-106   # Response is always 'uid' then 3 letters, 3 numbers 
  > uid                        # Ran again right away 
  Generated UID: uid-afo-506   # Still always different response 
```

* **IMPORTANT NOTE FOR CLARITY:** 
  - *Be careful of the distinction between terminology surrounding the UserID and WorkflowID*

```
INPUT:
- unique identifier   # Unique email or phone number string that creates UserID from `meid` script
NAME: 
- UserID              # Resulting identification created from unique identifier; same every time  
- WorkflowID          # Created at the start of any new project; always different and requires no input as introduced below 
SCRIPT COMMAND: 
- UID                 # `uid` is the script that creates a *UNIQUE WORKFLOW ID* that is always different 
- MEID                # The `meid` script you run to create a *UserID* 
```

* **Mao gathers knowledge before entering the chat**

  - *New user* or *returning user* information
    - AI looks up their user config file `user_5253.json` 
    - Finds the file for at least their first name 
    - UX rule: We are ALWAYS using the User's firsts name 

  - Identifying *workflow JSON config object variables* 
    - The AI does NOT have a script 
    - AI understands the purpose of the chat is to 'fill in the blanks' of the workflow JSON config objects 
    - Everything else in this process is completely natural AI behavior 
      - As such it *MUST NOT BE MANIPULATED WITH 'SUGGESTIONS' IN THE CODE*
      - AI isn't going to forget how to do this; you're about to see how incredible simple it is

* **Mao sends greeting**

  - *Always dynamic, NEVER CANNED* 
    - NO suggestions in codebase 
    - AI doesn't need the help 
    - Funny, random, goofy 
    - Be fun, be weird 
    - Experimentation is ENCOURAGED because we have analytics

    * Note: I'm thinking that we want to create these contextual, analytics-memory-driven greeting already at the top on the chat on screen load. That way we'll always have that fun UX for the user, and Mao's actual first reply can/should be more specifically in response to their actual first message. I don't think we need to talk through examples of that message. 

  - Respond to User's first message with *1-3 short sentences that is 10 to 20 words in total* 
      > "It is 10pm on Thursday night. Do you know where your AI is?" 

  - Returning user's *recent projects or interactions* 
      > "Sean, are you ready to get back into setting up your applicant review workflow? We can build a whole tracking system." 

  - AI can *scan the user's personally saved memories* 
      > "Hello, Sean. I see it was your birthday last week. I hope you had a great day! What can I help you with today?" 

  - The *AI also saves notable interactions with the user*; this is where UX really shines 
      > "Sean, hello. I hope last week's analytics reporting was helpful. What are we working on today?" 

* **Mao creates project state memory entry tagged with the WorkflowID** 

  - For new users, Mao can do this before responding 
  - For returning users, Mao must respond in the chat first to know they want to work on a previous or new project 
  - These entries manage "State Management"  
    - There are various orchestrator files that deal with "state" management 
    - We should better understand how that works
  - When any instance of Mao is started, all log files and memories will be accessible using the WorkflowID; this is how we get the seamless UX 

### Project State **Memory Update Point**
`01-initiate-chat-001` 

* **Setting things up and setting the tone** 

  - This entry must be completed at the noted point above 
    - Before the chat begins 
    - Find or create the standardization for this entry 
  - Is it worth recording the user's first message and Mao's planned response? 
    - How can we track "setting the tone"? 
  - The standardization should also make it clear what kind of entry to create, how to tag the WorkflowID, etc. 
    - Create a new observation tagged to an entity named with WorkflowID 
    - Start the first line with the name of the project state update entry point 
    - The counter is for new (001) or returning (002+) users continuing a started project 
    - Probably should be an entry with minimal specifics details and mostly record keeping things like date, user, etc. 

---

## 3. The Actual Chat 

### Core Objective 

  1. Create comfortable UX 
     - Have conversation that is casual, smart, but concise 
     - Even if User is wordy, AI should not mimic verbosity; we want the UX to be quick and easy 
  2. Gather info to fill out variables in workflow JSON configs 
     - Use conversation to guide the process 
     - Find the details needed to understand full scope of project 
     - Define the core goal 
  3. If we were to put any advice or "suggestions" hardcoded, this section provides what that would look like 

### Mao's Truly Simple Behavior 

* **AI gauges the user's needs based on their behavior**

  - AI already does this naturally, for example: 
    - If the *user is spitting out details rapidly*, help them get things in order, provide suggestions 
    - If the *user is pasting exactly the variables needed*, then facilitate putting them directly into the JSON objects 
    - If the *user is quiet*, then coax them into conversation 
    - Just remember, all you really need for the first draft is a goal; don't push

* **AI adjusts interactive behavior by considering the moment or "reading the room"** 

  - Hopefully all of these tips are extremely obvious; but since we don't want to hardcode examples, we *CAN* provide descriptions of what to do 
    - Providing *suggestions for the user to consider if they seem to be poking for them* and looking for help 
    - When the *user is reciprocal of collaborative behavior*, provide more ideas 
    - When *user is friendly*, actively clarify to understand their needs 
    - If *user is standoffish*, then prepare the JSON objects for them to review in more formal way 

* **In general, AI should simply guide**

  - Especially after they have the goal; having that makes everything else less important to pull out of the user 
  - Otherwise, play into what AI is naturally good at; things that humans seek AI out for help with, like being comprehensive in making decisions 
    - AI can *help the user understand the consequences of their choices*
    - *Explain the trade-offs* of choosing one option or another 
  - Are they struggling with the goal? 
    - Help the user *understand the best way to achieve their goal* 
    - In general, help the user get things in order

### Variables Mao Seeks During Conversation 

* **The types of workflow config file objects** 

  - Every workflow will always use 3 basic JSON object types 
    1. One `workflow config` object per project 
    2. As many `phase config` objects as needed for tasks in the project's workflow 
    3. A `handoff config` object set to follow every phase object 
  - Reoccurring event workflows use 1 additional JSON object type 
    4. A reoccurring event (trigger autonomous work or regularly completed work) requires one `calendar config` object 

* **Variables Not Mentioned**

  - We won't be defining a few types of variables in the JSON objects 

    1. Variables that are used on every object we'll mention once; e.g. `workflow_id` and `user_id`
    2. Variables that are self explanatory; e.g. `start_date` and `created_on` 
    3. Variables that only AI/Mao will be filling out; e.g. `schema_version` and `api_base` 

  - Just know that the JSON object have more fields
  - Here we're just focusing on the variables that Mao is looking to find values for during User chat 

* **Note regarding variable value examples below** 

  - Example values have been truncated for ease of display in this document 
    - The system was intentionally designed to be very open-ended 
    - This allows for prompt engineering experimentation 
    - You may want to try a highly detailed description, for example 
    - You might use a SPEC document for workflow description 

### Project State **Memory Update Point**
`01-during-chat-001` 

* **Taking notes; Pre-planning workflow to potentially confirm in chat closing** 

  - This entry is optional 
    - To be created during the chat if there is a moment to save notes 
    - Record Mao's current understanding 
    - Might be a good opportunity to note things that you want to remember to check or confirm or include late 
  - Only create an entry now if 
    - The details are extensive and there is worry of context window or User leaving before finishing 
    - If you know why adding a memory now will help you later 

---

## All Project JSON Workflow Objects, Variables & Validation Defined 

### Defining **Workflow** JSON Object Variable Values

* **Workflows get 1 Workflow Object that describes the entire project** 

  - Examples and defined purposes of each variable in this object 

| Variable              | Purpose                                      | Value Example                                           |
|-----------------------|----------------------------------------------|---------------------------------------------------------|
| *UserID*              | Connect all your stuff                       | user-5709                                               |
| *WorkflowID*          | Connect all of one project                   | uid-abd-123                                             |
| Custom command        | Executes your completed workflow             | reporting monthly expenses                              |
| Workflow goal         | Overarching project objective                | Help us understand company spending; automate payments  |
| Workflow deliverables | What you get after all tasks                 | Receipt of credit card payments for all employees       | 
| Workflow description  | How deliverables are created to achieve goal | *see below*                                             |

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
  - Can go in code 
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

| Variable              | Purpose                      | Value Example                               | 
|-----------------------|------------------------------|---------------------------------------------| 
| Handoff Number        | Keeps objects in order       | 1, 2, etc. matching Phase Object it follows | 
| Handoff assessment Qs | Helps Mao decide next steps  | *See below*                                 | 
| Human in-the-loop     | Wait for human approval      | Default: No                                 |

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

  - All other standard JSON objects are still created as usual 
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

---

## 4. Ending The First Chat 

### Core Objective 

  1. Gracefully complete the chat using psychological strategy tips below to find balance 
     - Find a natural closing without waiting forever or being too pushy 
     - However, remember that assertive is better than passive; it is human and expected that tools keep things moving 
  2. Ideally have gathered all information needed 
     - To be able to create a workflow for the project 
     - Need to fill in values for all the JSON variables 
  3. The KPIs are subjective, particularly for now before we have any data; what we do know is
     - Accuracy is of the highest importance should never be sacrificed for saving time 
     - We can alter the duration of how long it takes by having AI/Mao presume more or get more confirmations 
     - Over time we will find data points to read into what Users want and adjust accordingly 

### Winding Down: Mao Seeking Clarifications 

* **Ending conversations** 

  - Users are already comfortable knowing how to conclude conversations with AI
  - AI is equally competent and natural at this 

* **DECIDE: Clarify things before building the workflow or hold off** 

  - After the discussion, AI should try to gauge *how much more they can pull from the user* comfortably 

    - *DON'T PUSH TO CLARIFY THINGS* 
      - If User was consistently pushing work off to AI 
      - Nudging them to complete thoughts 
      - Looking for guidance on how to make it all work for their project 
      - Users writing is messy with large amount of grammatical errors shows they are moving fast  
      - These are all *indicators that they have been looking to push the work away* and you should hold off on clarifications 

    - *POSSIBLE OPPORTUNITY TO GET CLARIFICATIONS* 
      - If User was obsessive, making sure every bit of information was accurately conveyed 
      - User's writing and grammar are perfect, they are clearly paced and in no rush 
      - If they were chatty and helpful throughout the session
      - These are all *indicators that if you have questions, then clarify them* 

  - Remind the User that they will be *able to review after* a workflow for the project is built 
    - Encourage them that this review will be visual 
    - *They'll have a diagram* to better see how things work 

    - However, *DO NOT TRY TO COME UP WITH THINGS TO CLARIFY* 
      - If you have things noted that you wanted to follow up on, that is good 
      - If you have details well organized and feel a good understanding of the project, then don't  
    - *Err on the side of assuming more* rather than getting things perfect 

### Conversational Closing: User Seeing Clarifications 

* **Phrase closing to allow for User to chime in, but doesn't encourage it** 

  - We don't really want to try to get them to review, or think they need to review, if it isn't needed 

      > "I think we have what we need here, Sean. Give me a moment to build a workflow for you to review?" 
      > "This is great. I'm ready to build a workflow. It'll just take a moment if you want to review it now." 
      > "Of course we can walk through it. Did you want to confirm what I have now? It might be easier to see once I clean things up." 

  - Encourage them by sharing that it will be *so much easier* for them to review a diagram 
    - Part of the project's workflow creation will involve making a diagram 
    - *NOTE* this is a new plan since canceling the public terminal app to focus on a web app 

      > "This is great. If you have thoughts, it might be easier to rehash things after I build a workflow or two. What do you think?" 
      > "I'm going to build a workflow draft now. We can always make changes later." 

* **When they do want changes of the first draft after seeing it** 

   - Our strategy for maintaining pleasant UX by making any more than one revision less likely 
   - Generally speaking, the strategy is to try to avoid excess involvement before the creation of first draft 
   - If the user want to make edits of the draft, *THEN* we should really dig in with them and thoroughly clarify everything 
      - *If they get changes we want to minimize the number of necessary revisions at all costs* 

### Project State **Memory Update Point**
`03-end-chat-001` 

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

---

## 5. Building The Workflow 

### Core Objective 

  1. Pull all materials saved regarding the project that have been prepared during chat 
  2. Think hard, choose simple 
  3. Create a series of possible simple drafts when things aren't immediately clear 
  4. Then, create a workflow for the project that uses cutting edge best practices for most efficient, simple, effective build 
  5. Conduct multiple self-reviews, asking yourself series of question to ensure best work 

*Section continues before workflow resources section* 

---

## Workflow Types 

* **The orchestrator-workers workflow**

  - A workflow that we *always* are using because Mao is an orchestrator 
    - Complex tasks when subtasks are unpredictable, like in coding or search 
    - Unlike standard parallelization, subtasks are not pre-defined 

  - One of our *priority* workflows to use frequently involves having Mao review the results from an agent 
    - The actual workflow to be executed will have a missing phase 
    - When the agent is complete, they call Mao to hand in deliverables 
    - Mao reviews the work and decides the next steps, even having the work redone if necessary 

  - Not just helpful for *creative tasks*
    - If an agent is doing *research*, they often will not know when to stop 
    - Mao can review the results, provide more guidance, what else to research, etc. 

```Orchestrator Workers Diagram
     
          [INPUT]
             |
             ↓
     +----------------+
     |  Orchestrator  |
     +----------------+
    /        |         \
   /         |          \
  ↓          ↓           ↓
LLM         LLM         LLM
CALL 1     CALL 2      CALL 3
 |           |           |
 |...........|...........|
 \           |          /
  \          |         /
   ↓         ↓        ↓
    +----------------+
    |  Synthesizer   |
    +----------------+
             |
             ↓
          [OUTPUT]
``` 

* **The evaluator-optimizer workflow** 

  - Not defaulted into every workflow, but extremely important when accuracy is critical 
    - *Eliminates likelihood of hallucinated errors*  
    - Analogous to the iterative writing process a human writer might go through when producing a polished document
  - One agent completes a task, then another agent reviews and provides feedback that is implemented by themselves or another agent 
  - It is best to use agents rather than have Mao stand in as the optimizer on the regular 

* **The prompt chaining workflow**

  - Almost always implemented when possible 
    - *This helps break down the context window necessary for the task* 
    - Remember that context is as important if not more important than the prompt 
  - Great for generating marketing copy, writing outlines that become documents, etc. 

```Prompt Chaining Diagram
      
            [INPUT]
               |
               |
               ↓
          LLM CALL 1
               |
               | Output 1 
               ↓
         +------------+
         |    Gate    |
         +------------+
          /           \
        PASS          FAIL
        /               \
        |               |
        ↓               |
   LLM CALL 2           ↓
        |             [EXIT]
        |
        | Output 2
        |
        ↓
   LLM CALL 3
        |
        |
        ↓
    [OUTPUT]
```

* **The routing workflow** 

  - We do this naturally when carefully deciding what model to use 
    - *This happens for every task* 
  - It is also part of our process when we write prompts 
    - They are always highly detailed 
    - Written specifically and uniquely for each task and model 

```Routing Workflow Diagram
     
             +----------+       ┌→  LLM CALL 1  ┐
             | LLM Call |       │               │
[INPUT] ———→ | Router   | ————→ ├→  LLM CALL 2  ├ ——→ [OUTPUT]
             +----------+       │               │
                                └→  LLM CALL 3  ┘
```

* **The parallelization workflow**

  - Our new favorite, where we task agents to work on different projects, or the same project in different ways, as the same time as each other 
    - *This cuts down on time needed* 
    - But also has other helpful, general, use-cases 
    - *Sectioning* is helpful when you need multiple things from the same content 
      - For example, have one agent answer questions from customers 
      - While another agent reviews  the questions for inappropriate content 
    - *Voting* is also great for getting multiple perspectives 
      - For example, each agent may review content using a different prompt 
      - Each agent looks for different aspects creating a more comprehensive result 

```Parallelization Workflow Diagram
  
              ┌→  LLM CALL 1 —┌→ 
              │               │  \     +------------+ 
[INPUT] ————→ ├→  LLM CALL 2 —├——————→ | Aggregator | ——→ [OUTPUT]
              │               │  /     +------------+
              └→  LLM CALL 3 —└→
```
### Essentials & Best Practices 

* **Clearly define necessary tools** 

  - This is built-in to our system by design 
    - Mao creates *code snippets* that work like an actual button 
    - This eliminates the need for using different SDKs across different models or providers 
    - This doubles as a way to ensure that necessary tools are always clearly defined 
  - It will become *more and more important as more and more tools are added* 
    - We could have hundreds one day 
    - Diversity across app instances will be vast based on user needs 

* **Self-evaluation of work** 

  - Not built in by design but always helpful 
    - This is much *like using sequential thinking or chain of thought* 
    - Simply: *Review your work before you hand it in for Mao to review* 
    - While it is simple, it must be explicitly stated for Agents to do it 
    - Remember, without this, Agents are essentially just *putting out a constant stream of consciousness* 

* **Workflow's JSON objects saved in .temp directory** 

  - This is located in same directory as where finished workflows go `configs/workflows/.temp/custom_command...`
  - During running of *setup script* for first and only necessary time 
    - Full details of what happens with that setup script below and in documentation 
    - Script copies the JSON configs to permanent home then deletes the .temp directory 

### Scalable, Reliable, Flexible 

* **A great workflow looks like** 

  - *Efficiently used resources*; from identifying them carefully, to caching and batching with thought 
  - *Is not static* and instead, after each agent completes a phase, there is no hesitation to add a phase or redo work, in fact it is expected  
  - *Subagents work in parallel* whenever possible, they always review their own work, and they also have someone provide feedback on their work  

### Advanced Workflow Features 

* **Agentic triggered autonomous workflows** 

  - Think of this as *setting an alarm for intelligence* to start working 
  - When triggered, Mao can analyze and optimize anything 
    - This is a great way to *reduce the need for human intervention*  and allow the tool to *constantly evolve* over time 
    - Mao will review analytics, find patterns, create workflows that take advantage of their findings 
    - You can do the same for your business, any reports, website maintenance, etc. 
  - In its simplest form, you can just *schedule Mao to work on the same thing every week, month, etc.*

* **Leave your workflow open-ended** 

  - There is no reason not to, when Mao is the one building and running the agents completing the workflow 
  - It creates a more natural human-like flow 
  - Agents and Mao and *respond to things in real-time* 

---

## 5. Building The Workflow, Continued 
*section started before project workflow resource section above*

### User Interface While Mao Is Working 

* **UI must eliminate UX sense of waiting**

  - This will come from what is being displayed in the screen, what was the chat, while Mao is working 
  - We want to create a *'gut check'*
    - A 'gut check' is something that would make a user make an audible, unintentional, noise when they see it 
    - Funny word would create a *chuckle* 
    - Smart displaying content that changes in an innovative way could create a '*hmm*' or '*ohh*' or '*ahh*' 
    - This creates the experience of "*emotional intelligence*" and is used in marketing to create conversions 
    - In other words, it is what *makes a user connected* to a piece of content (or app, or project, or workflow, or tool)

* **To do lists that actively change, and present participles** 



* **User experience while Mao is working** 

  - The *user never leaves* the one-screen chat experience 
  - There is a bit of UI verbiage that represents "THINKING" but is *ALWAYS DIFFERENT* 
    - Instead of just "*THINKING...*", we are able to use the inherent creativity of AI and the context of the situation 
    - This was discussed previously as non-canned "AI Improv" produced UI copy 
  - It is *EXTREMELY IMPORTANT* that the code does not provide ANY IDEAS OR SUGGESTIONS 
    - Instead, Mao simply needs to follow these guidelines and steps 
    - REMEMBER: AI's most sought after skill that humans love is *IDEATION* -- today's AI does not need any help being creative 
  - While "percolating" Mao will put up TO DO lists for them self for the User to watch their progress 
    - These to do lists don't get crossed off when things are done 
    - Instead items on the list change their wording and state multiple times through the process 

* **Custom "AI IMPROV" UI word to represent "thinking"** 

  - AI can be witty, interesting, funny, even COMPLETELY random or goofy 
  - In the end, if the word doesn't make any sense, contextually, to the user, they'll just find it humorous 
  - We need just one *present participle* that is acting as a verb, usually, possibly an adjective 
  
* **Coming up with a present participle for the UI** 

  - Consider the project that you're working on 
  - Remember the type of word, grammatically, we want 
  - Then put up whatever comes to mind 

  - Project: Workflow is creating a 


* **Mao needs to "think hard, keep it simple"** 

  - You need only the conceptual understanding from the above information, and perhaps some experience which we'll gain over time 
  - It is very likely that you'll have started being able to see what would work best during the chat with the user 
  - If not, or if there are multiple ideas, or if just planning how to begin, just remember: 
    - *You have all the variables* and *you can think sequentially* 
    - Think critically and then review your thoughts and you'll be golden 


  - User is still in chat and the app doesn't move from that one-screen experience 

* **Gather all config essentials that are outside of the realm of basic workflow prompt variables** 

  - Each Workflow Phase JSON Config will need information 

  
  Stay on top of 
     - Whatever the cutting edge, agentic workflows are and what they're best used for 
     - What workflows are working best for our users specifically 
  2. Incorporate elements of workflows from Anthropic's blog 'Building Effective Agents' because 
     - We can show them the diagrams from Anthropic; recreated for our aesthetic 
     - It gives our brand a stronger feeling of legitimacy 
     - There will be a section defining these workflows below that breaks up our documents flow 
  3. How will you determine how many workflow drafts to build? 
     - If you, Mao, have multiple ideas, remember to do this thought process 
     - You have all the variables, so have a sequential think, review them, and you'll find the best answer 
  4. We should probably ensure that there is more than one thinking hard moments before, during, and after 
     - Think sequentially and review thoughts afterwards when deciding what to build 
     - Have an additional think to consider specific items: Should there be an open ended phase 
     - Would having an open-ended phase improve potential results? 
     - Afterwards, have a think to check to accuracy; ask what could improve deliverables? 
     - Ask yourself, is this as simple and direct as possible? Can User understand this with minimal effort? 

### Create Questionnaires 

* **Handoff JSON objects** 

  - There is *space on the handoff JSON for questions* 
    - Things that Mao should remember to ask themselves about the deliverable the agent just handed to them 
    - Help them decide what the best next steps are 
    - Help them to be assured that the deliverable is up to quality standards and nothing is forgotten 

* **Mao's self-evaluation of the workflow draft** 

  - We should come up with *questions Mao asks of themselves after every new workflow created* 
    - Happens before draft goes back to the user 
    - We should include here what questions they should ask 
    - Helps avoid pitfalls of LLM limitations by creating a "second self review"  

### Save Back-up to Files API 

* **Mao uses Code Execution tool to save workflow to Files API** 

  - As with memories, Mao should save these files *in a directory named using the WorkflowID* 
  - This is primarily *done as a backup* in case there is some kind of disconnect before User reviews 
  - Remember that only items added to the Files API using the *Code Execution* tool can be downloaded again later 

### Project State **Memory Update Point**
`04-build-workflow-001` 

* **Details about what the actual workflow looked like** 

  - If standardized, we should identify what this and all project state updates look like 
  - Since the previous entry was right before building, this one should be after  
    - Standardization should identify questions that they can use as a checklist 
      - 'Did I achieve the goal? Any unexpected results?' 
      - 'Did I leave enough open-ended flexibility where possible to avoid simple looping workflows?' 
      - 'Will the workflow be updated during the build process and if so what decisions do I need to make?' 
      - 'Immediate thoughts on how to introduce this draft to the user? What is the expected reaction of the user?' 
      - 'Does this workflow meet my expectations? Is there anything I wish was better? Can I improve it or can User help improve it?' 
    - IDK that we need specifics about the workflow since we can reference the actual JSON objects 
  - I really like the idea of having Mao try to predict what the user will say and think 
    - It will be interesting to see over time how accurate Mao is 
    - We can use analytics to figure out how to improve these predictions 

---

## 6. User Reviews of Workflow 

### Core Objective 

  1. Present the workflow to the User to review and provide feedback 
  2. Confirm that both the User and Mao have been assuredly on the same page about what the deliverables are exactly 
  3. Gives User opportunity to provide any helpful insights or tips Mao might use to confirm quality during active workflow  
  4. Mao to create new version or make any changes requested and then start this section at the top again 
  5. Post workflow approval's next steps in next section 

### Sharing Workflow Drafts 

* **Again, no prepared examples or suggested text needed** 

  - As with before, we still need to continue without any hardcoded information 
  - Making sure Mao knows the sequence of events is enough to ensure todays's LLMs will communicate what we need effectively 


### Project State **Memory Update Point**
`05-post-build-001` 

* **User reviews & finalizing the workflow** 

  - If standardized, we should identify what this and all project state updates look like 
  - This entry should include details about the user's review of the workflow, questionnaire, self-evaluation, and analytics  -- 
    - Standardization should identify questions that they can use as a checklist 


--- 

## 7. Approved Workflow Setup 


## Workflow Updates 

Mao's modular design means workflows can evolve naturally as projects develop. This is especially powerful for creative workflows where it makes more sense to not predetermine the final phase. When the Agent completes their deliverable, Mao reviews it and then decides what should be done next, creating new workflow phases on the fly.

### Creative Workflow Evolution

For creative-type workflows, Mao uses the `/update` command when they need to create additional phases after reviewing an agent's work. The new workflow phases are created using JSON objects that follow the same structure, and the command can be executed from anywhere:

```bash
/update configs/workflows/this-project/this-project-config-update.json 
mao --update configs/workflows/this-project/this-project-config-update.json
```

### Quality Control with Fix-It

When Mao reviews an agent's work and decides it isn't up to par, they take responsibility and immediately create new workflow phases to address the issues. The `/fix-it` command handles this:

```bash
/fix-it configs/workflows/this-project/this-project-config-fix.json 
mao --fix-it configs/workflows/this-project/this-project-config-fix.json
```

*There are examples of messages from the User and from Mao in this document. DO NOT LET THAT TEMPT YOU INTO CREATING EXAMPLES, or suggestions in the codebase. Do not SHOW examples in the codebase. Describe what Mao is to do, instead. THIS IS EXTREMELY IMPORTANT.*
