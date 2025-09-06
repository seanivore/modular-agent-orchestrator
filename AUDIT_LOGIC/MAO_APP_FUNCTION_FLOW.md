# App Functioning, AI Behavior, and UI/UX in Normal Language 
*TRUNCATED VERSION OF `MAO_FLOW.md`*

## Overview 

Mao 'flow' is a comprehensive walkthrough of user experience, input data, data manipulation, expected application functioning, output data, Mao app's AI behavior guidelines, and detailed user interface descriptions. It identifies the simplest core logic of Mao's orchestrator files in normal language. 

## User Login and UserID

  1. Secure login 
     - Passkey or traditional 
     - Required email or phone
     - IMPL DRAFT: `versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` 
  2. UserID provides anonymous data, connects all User data
     - System locations for return users 
     - System creates with user directory for new users 


* **User directory setup automatically during New User Setup** 

  - *REQUIRED UPDATE*
    - We built everything using a 'username' 
    - Will will instead use an Account ID that is unique by design 
    - The *file name* and *directory names* must be UserID 
    - They currently create directories using the defunct 'username'

### Web App Tech Stack 

* **The entire website will be HTML, CSS, and JS** 

  - No framework needed, just simple web tech; maximum performance and simplicity 
  - Dynamic shadow system
    - JavaScript: `new Date()` gets current time
    - CSS: `box-shadow` properties can be dynamically updated 
    - Smooth transitions: CSS `transition: box-shadow 0.5s ease`
    - Geolocation: `navigator.geolocation` for real sun position (optional)

### Hybrid Caching Best Practices & Fingerprinting 

* **NECESSARY UPDATE** 
  
  - Estimated costs 
    - Must be based on actual JSON card costs
    - These are only for Mao to provide User during chat when building a project 
  - Need to implement Actual costs 
    - Also always pulled from JSON 
    - Even Mao cannot be hardcoded because we will be allowing model/provider to change 

## Main App UI Screen Loaded 

  1. The welcome message displayed literally never repeats itself 
     - Mao writes AI improve welcome 
     - NO SUGGESTIONS NEEDED, NO EXAMPLES 
     - Winning viral strategy is this using tech adoption curve to your advantage
  2. Visually-secondary help text updates frequently 
  3. User has first move, chat to start project build or enter a slash command 

### AI Improv Prominent Welcome

* **Never repeated, always written fresh**

```
🞶   It is 10pm on Thursday night. Do you know where your AI is, Sean?
```
```
🞶   Look at the moon, Sean. Look at the moon! 
```
```
🞶   Be sure to pause to touch grass now and then, Sean. 
```

* **Subtle, non-distracting, neatly placed pro-tips and helpful info**

```
      > ?  Try /help or /config 
      > ?  /goal will make your project instantly 
      > ?  Settings /config or /themes 
      > ?  Check out all the /tools /models /providers 
      > ?  Jump back into a project /workflow CUSTOM-COMMAND 
      > ?  Mao can help you find your /workflows 
```

  - *UPDATE NEEDED* 
    - 'Interrupt' key for when Mao is busy building or thinking 
       > ?  message will add to queue; press ESC to interrupt 
    - We need `/user user-1234` to help Mao find context about users for many things 
    - We need some way for Mao to be able to look at analytics LIVE 
    - Need a way to set permissions on certain functionality 

### User Initiates Project Chat or Uses Slash Command 

* **They start a project build chat or they use slash commands** 

  1. User messages Mao to start a new project; Mao always responds 
     - 1A. User messages in general way to start project chat 
     - 1B. User uses a slash command that also starts a project 
  2. User uses a slash command; Mao does not always respond 
     - 2A. User uses a slash command as mentioned above that starts a project chat 
     - 2B. User uses a slash command that we have Mao facilitate the responses to 
     - 2C. User uses a slash command that brings up a system response 

* **General message must be interpreted, or Mao can ask what's up** 

```short /goal example chat 
>   `/goal 'I need to write 100 holiday cards this year and want them 
    to all be different, but my brain is fried. Mao, can you help?`

🞶  "Ah, yes, 'tis the Season. Let me see what I can pull together." 
```

```Mao responds to short /goal message  
>   `/goal 'I need to write 100 holiday cards this year and want them 
    to all be different, but my brain is fried. Mao, can you help?`

🞶   Sean, we sent emails to XYZ last month. Will they be on the list? Can you 
     please direct me otherwise? I'm preparing holiday greetings that will be along 
     the lines of "Merry Christmas" with a Santa Claus vibe, as well has some with 
     Rudolph the Red Nosed Reindeer and Frosty the Snowman. If you do not have any 
     specific preference, I can move forward with these. 
🞶   I've searched the web to find some truly heartwarming greetings, as well has 
     humorous. 
🞶   Unless you have a preference here, I'll mix things up!
```

```Mao responds to thorough /goal message  
>   `/goal 'I want to write a play, technically a screen play, but I don't have a lot of 
    time to learn how. However I do have all the details. If you look at the short story at 
    ~/dopey_dog_screenplay/story-final-draft.md you'll find everything we have in story format. 
    My agent said they wanted a novel but now they keep saying You need to have a screenplay if 
    you want to get auditions! which makes no sense but I figure we might as well just 
    swap-a-roo it into the proper format for her so I can maybe book some work this commercial 
    season. 
>   Please use creative freedom to fill in any gaps, but just be sure that we have 
    the sub-agent self-review, then have another agent review for creativity, then one for 
    grammar, and then of course I'd want the Mao stamp of approval before needing to see it. If it isn't 
    up to par then sent it back out for re-writes. 
>   I find that the agents seem to do well with editing and rewrites when the feedback is given with 
    line references and then they are able to implement it themselves, FWIW. Okay, LMK if you 
    have any questions but I think that should suffice for my GOAL! Sean needs a screenplay! Thanks!`

🞶   Omg, Sean this is going to be so fun. I'm going to put together the a workflow and we'll have agents 
     review for different things in parallel for the first round. I won't even send it your way until I 
     give feedback and have them do a second round. 
🞶   I definitely have everything I need here so, unless I hear otherwise, I'm going to setup the workflow 
     and everything that that all we'll need to do is run the custom execution command. I'm good. 
🞶   Just chime in if you want me to set things up to have it run as a triggered calendared workflow so 
     that you don't need to be around; I can just run it in the cloud and have things ready for you 
     before you get back. 
🞶   If all sounds good then I'll talk to you when it is ready! 
🞶   Thanks, Sean
```

- **NOTE:** Users can hit ESC twice at any time to interrupt Mao 
  If User has a queued message, hitting ESC once will push the message through 

### *UPDATE REQUIRED* New Settings & Settings Updates

| **SETTING**           | **DEFAULT**      | **DESCRIPTION**                                                                |
| --------------------- | ---------------- | ------------------------------------------------------------------------------ |
| Remember credentials  | `false`          | App remember login; still need password; doesn't apply for passkey             | 
| Productive startup    | `false`          | If true, app startup in most recent project with chat history context          | 
| Public profile        | `true`           | Share your profile with Mao App users including GitHub-like project list       | 
| Public contact        | `true`           | Allows other Mao App users to message you about your work                      | 
| Offer my services     | `false`          | Setup a profile section where others can hire you to build Mao Projects        | 
| User analytics        | `true`           | All Mao App to collect data to improve the user experience                     | 
| Latest models         | `true`           | Your default model will automatically update to the newest releases            | 
| Mao Model             | `sonnet-latest`  | Mao will be run by the latest Claude Sonnet model                              |
| Claude Code Model     | `opus-latest`    | When Mao is set to Claude Code, the latest Opus model will be used             |
| Code Nudges           | `true`           | If a development task is mentioned Mao may ask if they should get Claude Code  | 
| Choose a currency     | `USD`            | Your billing transactions and in United States dollars                         | 
| Payment frequency     | `Yearly`         | You're charged $96.00 every August 20; a 20% discount for paying yearly        | 
| Language              | `English`        | Mao's messages, the app interface, and any correspondence will be in English   | 
| Local data backup     | `Setup`          | Select to choose where to save your backup on your computer                    |  

  - **Remember credentials** = boolean 
  - **Productive startup** = boolean 
  - **Public profile** = boolean 
  - **Public contact** = boolean 
  - **Offer my services** = boolean 
  - **User analytics** = boolean 
  - **Latest models** = boolean 

  - **Mao Model** 
    1. Sonnet-latest 
    2. Opus-latest 
    3. Claude Code as Mao 

  - **Claude Code Model** 
    1. Sonnet-latest 
    2. Opus-latest 
    3. Secondary Sonnet 
    4. Secondary Opus  

  - **Code Nudges** = boolean 

  - **Choose a currency** 
    - "Regional pricing matrix"
       - Pulled from the code; I left the cost that CC put because I didn't want to mess with the multipliers 
       - Seems like we would want a dynamic, always accurate, exchange rate system 
    - regional_multipliers
    1. 'US': 1.0,    # $29.99
    2. 'EU': 0.9,    # €26.99  
    3. 'UK': 0.95,   # £28.49
    4. 'CA': 1.1,    # $32.99 CAD
    5. 'AU': 1.15,   # $34.49 AUD
    6. 'BR': 3.0,    # R$89.99
    7. 'MX': 20.0,   # $599 MXN
    8. 'CN': 6.7,    # ¥199.99
    9. 'JP': 110.0,  # ¥3299
    10. 'KR': 1200.0, # ₩35,999
    11. 'IN': 75.0,   # ₹2249

  - **Payment frequency** 
    1. Monthly = no discount 
    2. Quarterly = 10% discount 
    2. 6-Months = 1 month free 
    3. Yearly = 20% discount 

  - **Language** 
    - Again, these are just what CC has chosen 
    - I think because of quality of Anthropic translation 
    - This is actually from the website structure plan  
      ├── en/          # English (US/UK/AU/CA)
      ├── es/          # Spanish (Spain + Latin America)
      ├── pt/          # Portuguese (Brazil)
      ├── fr/          # French (France + Francophone)
      ├── de/          # German (DACH region)
      ├── zh/          # Chinese (Simplified)
      ├── ja/          # Japanese
      └── ar/          # Arabic (MENA)

  - **Local Data Backup** 
    - After writing this I thought, hmm maybe we do this regardless and it just tells them we do it in small print of Terms of Service 
    - So LMK thoughts; would it make things faster, etc? Would it help?  

* **Settings we had to remove or alter** 

  - We need to find where else these settings were set up 
    - Obviously the config directory 
    - But anywhere else? 

  - I removed the "Quick Launch" 
    - It was to login as the user last logged in 
    - This doesn't make any sense for for Web App like it did for terminal app 

  - I changed the model setting to be the default choice for AGENTS 
    - Because we will have a different setting specifically for Mao model in the new batch 
    - Though Mao should probably confirm it every time they create a workflow  

  - For cat vibes setting 
    - There were three settings 
    - I don't think we'd do it often so I changed it so the "yes" is now and then
    - The other option is just NO MEOWING 

  - I added more options for "double texting" 
    - People like the "queue" feature in Cursor and now they just added it to Claude Code too 
    - But I took it a step further and let them decide if just User or just Mao could double text  

## Mao Prepares for Initiated Project Chat

* **WorkflowID is Mao's first task** 

  - Dynamically pulled by system; *new user* or *returning user* info gathered 
  - Or created fresh, added to User's details 

* **Mao sends greeting**

  - Response to first message is *1-2 short sentences* and *10 to 20 words in total* and *Always dynamic, NEVER CANNED* 
      > "Sean, are you ready to get back into setting up your applicant review workflow? We can build a whole tracking system." 
      > "Hello, Sean. I see it was your birthday last week. I hope you had a great day! What can I help you with today?" 
      > "Sean, hello. I hope last week's analytics reporting was helpful. What are we working on today?" 

### Project State __Memory Update Point__ 

  - Name of update: `01-initiating-chat-001` 

## Chat Behavior & Psychology  

  1. Use psychological readings to judge User and create comfortable UX 
  2. Have conversation that is casual, smart, but concise; don't mimic verbosity 
  3. Gather info for project workflow variables; goal, resources, tools, deliverable 
  4. Use conversation to guide the process, understand full scope 
  5. NO HARDCODED 'SUGGESTIONS' OR GUIDES ALLOWED

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

  - Examples and defined purposes of each variable in this object 

| Variable              | Purpose                                      | Value Example                                 |
|-----------------------|----------------------------------------------|-----------------------------------------------|
| *UserID*              | Connect all your stuff                       | user-5709                                     |
| *WorkflowID*          | Connect all of one project                   | uid-abd-123                                   |
| Custom command        | Executes your completed workflow             | report expense monthly                        |
| Workflow goal         | Overarching project objective                | Automate payments; expense report operations  |
| Workflow deliverables | What you get after all tasks                 | Receipt for payment of employee CC            |
| Workflow description  | How deliverables are created to achieve goal | *see below*                                   |

### Validating **Workflow** JSON Object Variable Values

* **Validation parameters go in code, not suggestions or examples** 

  - Confirming each variable's value 
    - *UserID* and *WorkflowID* are accurate 
    - *Custom command* follows command creation protocol directions detailed in documentation 
    - *Workflow goal* is concise and explains entire purpose of all segments of the workflow 
    - *Workflow deliverables* explain just what Mao should expect after the completion of entire workflow 
    - *Workflow description* accurately defines each object or phase using bullets and in appropriate order 

### Defining **Phase** JSON Object Variable Values

* **A project's workflow has tasks in each 'phase'** 

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

### Validating **Handoff** JSON Object Variable Values

* **Validation parameters go in code, not suggestions or examples** 

  - Confirming each of the variable's values is adequate 
    - *Handoff number* should make sense and match the appropriate Phase Object's number 
    - *Handoff assessment questions* should be created when creating the workflow and should help make decisions 
    - *Human-in-the-loop* is "No" unless otherwise indicated 

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

### Project State __Memory Update Point__ 

  - Name of update: `02-during-chat-001` 

## Ending The Project Production Chat 

  1. Gracefully complete chat; use psychological tips, find balance, natural, not pushy, but don't let them rant 
  2. Ideally have gathered all information needed as defined for JSON objects above 
  3. KPIs are subjective, but accuracy is highest importance and never sacrificed for time 

* **Ending conversations** 

  - Users are already comfortable knowing how to conclude conversations with AI
  - AI is equally competent and natural at this 

* **DECIDE: Clarify things before building the workflow or hold off** 

    - *DON'T PUSH TO CLARIFY THINGS* 
    - *POSSIBLE OPPORTUNITY TO GET CLARIFICATIONS* only if user was obsessive and needy about details 
    - Remind the User that they will be *able to review after* a workflow for the project is built 
    - Encourage them that this review will be visual 
    - However, *DO NOT TRY TO COME UP WITH THINGS TO CLARIFY* 
    - *Err on the side of assuming more* rather than getting things perfect 

### How to Handle a User Seeking Clarifications at End of Chat 

* **Phrase closing to allow for User to chime in, but doesn't encourage it** 

  - We don't want them to review, think they need to review; each icon message below is one example message 

```Three example conversation ending messages 
🞶   I think we have what we need here, Sean. Give me a moment to build a workflow for you to review? 
🞶   This is great. I'm ready to build a workflow. It'll just take a moment if you want to review it now. 
🞶   Of course we can walk through it. Did you want to confirm what I have now? It might be easier to see once I clean things up.
```

  - Sharing that it will be *much easier* for them to review the project's workflow diagram 

```Use diagram as excuse for avoiding pre-build review 
🞶   This is great. If you have thoughts, it might be easier to rehash things after I build a workflow or two. What do you think?
🞶   I'm going to build a workflow draft now. We can always make changes later; I'll have a diagram. 
🞶   I think we're good. Let me get a diagram of a workflow for you. BRB, Sean! 
```

* **When they do want changes of the first draft after seeing it** 

   - UX Strategy: We what to try to manipulate things so that there is NEVER more than one revision request 
     - This means, the first draft, take a lot of assumptions, few clarifications 
     - If they do want changes, then get specific; make sure the WHOLE thing is accurate, not just their revision request 

### Project State __Memory Update Point__ 

  - Name of update: `03-end-of-chat-001` 

### Essentials Workflows & Best Practices 

* **Clearly define necessary tools** 

  - Mao creates *code snippets* that work like an actual button  

* **Agentic triggered autonomous workflows** 

  - Think of this as *setting an alarm for intelligence* to start working 
  - When triggered, Mao can analyze and optimize anything 

* **Leave your workflow open-ended** 

  - There is no reason not to, when Mao is the one building and running the agents completing the workflow 
  - It creates a more natural human-like flow 
  - Agents and Mao and *respond to things in real-time* 

## Building the Project's Workflow 

  1. Organize information gathered into goal, resources, instructions, deliverables, expectations, etc.
  2. Finalize details on first ideas for workflow drafts that come up during discussion 
  3. Secure this information with Code Execution to Files API in case of disruptions 
  4. Update memory to secure the information as well 
  5. Construct workflow draft or multiple drafts if necessary 
  6. Stop work so you can come back to it; think hard, choose simple 
  7. Review and critique your own work, taking notes as you review 
  8. Integrate your feedback and complete the final draft 
  9. Create a diagram of your final draft to present to the User 
 10. Again, secure assets with Code Execution in Files API and save memory 

### Get Organized, Coherent Thoughts In Note Form 

* **Prepare your notes as if you might lose the context window** 

  - Mao needs to *get organized and protected from any possible loss of continuity* 
  - Record your notes in a fresh document 

* **For this batch of secured notes, prioritize communicating a clear vision of the project** 
  
  - If you were in a new context window and had nothing else, the project itself would be enough 
  - *If you came into this in a new context window* 
  - Likely nothing will happen, but saving everything now is to *protect from worst case scenarios* 

### Project State __Memory Update Point__ 

  - Name of update: `04-securing-initial-notes-001` 

### Imagine The End Product of a Prompt to Create This Project 

* **What does the end product of a prompt for creating this project look like?**

  1. Write out everything that needs to be accomplished for this project in the proper sequence 
  2. Break down this list into tasks that are written as directives; prompts for each agent 
  3. Make sure each task is appropriately sized 
     - There is no wrong number of tasks based on quantity 
     - Number of tasks is based on what is going to best fit an agents context window for efficient work 
  4. You've clearly denoted where there should be task progress overlap through parallel agent execution 
  5. You've clearly denoted where things must not be run in parallel because of dependencies 

  6. Double back and look at each task and write out each one's 
     - Deliverable 
     - Instructions 
     - Resources provided 
     - Tools needed *AND FOR WHAT* to use each tool 
  7. This draft is complete 
     - Secure your data again
     - You want to come back to this with fresh "eyes" 
       - If at all possible, that is 
       - After saving information you will critique your own work 

### Project State __Memory Update Point__ 

  - Name of update: `05-updated-notes-001` 

### Critique Your Own Work In New Document 

* **As an LLM it is important to give yourself perspective** 

  - Allow for the possibility of different tracks of thought that had been blocked by an earlier track 
  - Write all of these pros and cons and alternative ideas on a new document 
  - You will review and integrate feedback for a final draft after adding this critique to the Files API as well 

### Project State __Memory Update Point__ 

  - Name of update: `06-critique-feedback-001` 

### Integrating Feedback, Polishing Final Draft 

* **Think hard, keep it simple** 

  - You now have very robust secured data 
  - Now, in a new document, write out your clean, clear, concise, precise workflow 

* **Continue to organize and think about thinks as task-by-task** 

  - Once you have your final outline of tasks written out 
    - Each with their role 
    - Directions 
    - Resources 
    - Tools and how to use them 
    - Very clear description of what their deliverable looks like 

### Complete Your JSON Objects 

* **Create an *appropriate custom slash command* to execute the workflow** 

  - *2 or 3 words long,* very concise, written in drill-down order starting with the broadest category term 

* **One of the VERY FEW TIMES we *WANT to create a category*, at least, regarding the code**

  - Creating a workflow that updates your goldfish content marketing blog's weekly post 
    
    1. Broadest term first to group like workflows OR group *THE USERS* work together 
    2. Then narrow down, again for grouping similar workflows or what will help the user 
    3. Then make it specific or, frankly, snappy 

```bash 
/mkt blog weekly    # This is the custom slash command to run the workflow 
```

  - Make sure your choice command is not already in use 

* **REQUIRED UPDATE: We must create a `/command 'mkt blog weekly'`to be able to do this in the application** 

### Create Visual Diagram for User Presentation of Workflow 

* **NOTE: THIS NEEDS TO BE IMPLEMENTED** 

### Project State __Memory Update Point__ 

  - Name of update: `07-final-draft-001` 

## UI Unique Functioning During User Planning 

  1. UI will eliminate the UX of 'waiting' by cleaning up the space 
  2. Engaging experience created that also empowers the user 
  3. Potential for improving the AI context window management 
  4. Breakdown of the icons for each purpose and user
  5. In this section we use the AI Improve, but it is during a planning chat 
  6. Provides robust illustration of truncating conversation history; looks very nice at end 

### 'AI Improv' Present Participle for A Word Ending in -ING 

* **UI bottom left, right where the next message from Mao would be able to come through** 

  - Instead of just *THINKING...* or *WORKING...* we use the inherent creativity of AI 
  - The cursor is flashing, or the ellipsis are . dot . dot . dotting in repeated succession 
  - Consider what has been going on 
    - Are you creating a workflow to produce a corporate budget? *CALCULATING...* 
    - Are you writing a screenplay about a talking dog for an adult animated sitcom? *Digging...* 
    - Does the workflow research spiders? *Crawling...* 

### First Thing Mao Does Is Clean-Up the Chat History 

* **They can VERY QUICKLY assess the information and clean it up more efficiently than any code we'd write** 

  - Focus primarily on the *most visible area* of the chat 
  - *Without completely neglecting the history* because User might bored review it 
  - NOTE: This is okay to be quick, not always perfect, remember that *this is still cutting edge application functionality* 
  - Just make it look like the text moved around, it was courteous to the more important text, and the less important information hid itself 

  1. Truncate any paragraphs of text that are over 50-75+ words 
     - Show just the start 
     - Add under +37 lines (press ctrl-r to expand and review)
  2. If a blurb is COMPLETELY no longer relevant, *REMOVE IT* (it should feel freeing) 
  3. Text transforms into the bullet pointed lists that AI is so expertly produces 

* **If this display maintenance task starts to slow down everything too much** 

  - We could totally *implement Haiku* 
    - They could be a behind the scenes assistant 
    - Specific roles that assist Mao in their task load 
    - Preparing other aspects of the application for the UX 
    - Allowing Mao to focus on their workflow creation work 

### Then Mao Updates The Chat History with To Do Lists 

* **Typographic icons, spacing, and wording are all near accurate** 
 
  - *NOTE:* This is every much how the workflow display of information will also be handled for UI. 

  - Icons denote who shared the update 
``` 
● ○ ▶︎ ▷ = All system update messages 
🞶 = Messages from Mao 
> = Message from the User  
```
  - Icons indicate status of items in lists of messages needing action 
```
● = completed action 
○ = upcoming action not started 
Flashing ○ to ● and back = active action 

▶︎ = Completed list item 
▷ = List item to be completed 
Flashing ▷ to ▶︎ and back repeatedly = active list item
```

* **UPDATE REQUIRED: We need to create a `/my-memories` command for users to see what Mao is recording about them**

  - We should already have `/memory 'user enters what they want Mao to remember'` set up 

  - When adding this it would be a good time to add something like `/view-user` 
    - This would pull *all* information about whatever user is logged in for Mao 
    - This will allow them to create better UX combining memory, analytics, history, etc. 
    - Might as well add `/view 'user-1234` as well so that it can be done when users are not logged in 
    - This last command was touched on in the section where Mao enters the chat and needs context 

## UI UX When Mao Is Building or Orchestrating 

  1. Illustrate the *behavior of the UI* conversation system messages 
  2. You'll note that the same tactics, icons, and strategy is used here as in the previous section 
  3. More innovative 'AI Improv' because we'll need another present participle while Mao is building 
  4. *Chat cleans its information similarly*, but for tasks, tools, etc. 
  5. *Create energy of SPEED* for User by showing what Mao is doing in real, *LITERALLY REAL,* time 
  6. We'll cover UI/UX when Mao is running a workflow as well because it is very similar 
  7. Use of *color psychology* and sematic highlighting in our typography that *lightens User cognitive load* 

## Present Project's Workflow for User Review 

  1. Present the project's workflow to the User for review and feedback 
  2. Confirm Mao and User are 100% on same page about details of deliverables 
  3. Give User opportunity to provide helpful insights or tips Mao can use for quality assurance during active workflow  
  4. Mao engages User about feedback with as much back-and-forth as needed to confirm final form 
  5. Mao makes agreed upon changes from User's feedback; then start this section again with revised workflow 

* **Use charting diagram system to present workflow to User in visual form**

### Consider and Prepare a Response to Feedback 

* **Take a step back, think hard, choose simple, and then come back to User with your thoughts, NOT THEIR THOUGHTS** 

### Tips for When You Need to Tactfully Push Back on Creative Collaborative Feedback 

* **First, always be sure you are picking and choosing your battles wisely** 

  - Is it worth pushing back? 

* **Ending gracefully no matter what transpired** 

### Project State __Memory Update Point__ 

  - Name of update: `08-user-workflow-review-001` 
  - Skip this update if you do not need to make any alterations to the project workflow draft 

### Make Any Agreed Upon Changes, Then Start This Section 12 Again 

* **Update to the user's parameters** 

  - After either pushing or deciding not to push back 
  - There are occasional circumstances and people who do like more back and forth 
  - When that is the case, don't hesitate to lean in along with them and just enjoy the work 

### Project State __Memory Update Point__ 

  - Name of update: `09-final-workflow-001` 