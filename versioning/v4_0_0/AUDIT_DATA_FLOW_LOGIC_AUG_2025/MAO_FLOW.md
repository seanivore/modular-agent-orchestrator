# Flow of Data Through Mao 

## Overview 

* **The docs all say that the flow is this:** 

>"User Goal" --> "Conversation Bridge" --> "Natural Language Processing" --> "Core" --> "JSON Workflow Creation" --> "Model Selection" --> "Execution" --> "Results" --> "Caching"

  - I don't understand that clear enough to know what the logic is for each file. This is information we need to be able to effectively clean up all hardcoded categories in the code files. 
  - The `core.py` file is where we started and we found so many categories. They hardcoded them as "suggestions" for the AI but the AI does not need suggestions. We went to `conversation_bridge.py` and found the same grouping. 

* **AI knows the variables. They are able to have a conversation with the user and fill in the blanks.** 
  - We do not want anything more complicated than that 
  - The only categorical grouping we want is for analytics. NO SUGGESTIONS 
  - We also need to be aware of launching multi-lingual; none of these prefabs would make any sense in a multi-lingual environment 

### Goal 

IMO, this feels very overly complex. The actual task is very simple, so it feels strange that I can't understand the code. The only thing we're really trying to do is gather information for blanks to variables for a prompt we have memorized. 

Once we understand what the logic should be, and what the file's current logic is, then we can clean up all the files in the flow. 

### Deliverables 

* **The logic flow will be defined in plain language** 
  - Much like our beloved `./versioning/v4_1_0/IMPL_WEB_UI/logic_design/_NEW_USER_FLOW.md` document 
  - This document informed so many different functions and code in various files 
  - It is equally as helpful when setting up the actual UI 

* **This document will also become a golden resource for multiple files** 
  - We will be able to identify what information is conveyed and where 
  - How that information is handled and with what logic flow

* **The additional benefits of doing this** 
  - We'll have a really nice diagram 
  - It will be extremely helpful when we go to build the actual UI 
  - Also the code and files should all end up a lot cleaner, simpler, and therefore, faster 

### Procedure 

1. As we go through below, we want to identify where this happens
2. With a full understanding of the current flow, we can optimize according to the defined flow below 
3. As we proceed, we should literally add notation to the information below letting us know where, what happens. 
4. As we better understand the full scope of the current flow, we will add those details to this flow (analytics, for example)

---

## 1. User Login 

### Core Objective 

  1. User gets a secure login 
  2. Automation creates their UserID 
  3. Automation creates their User config directory and important files 
  4. The UserID follows them around the application and will later be paired with the WorkflowID 

### New Users 

  - *Login with passkey or a unique identifier* which is used to create their UserID 
    - Passkey will require providing unique identifier once 
    - Other users have to enter unique identifier every time 
    - Email or phone number qualify 
    - They must provide their first name 
    - They may optionally provide their last name  
  - Backend creates UserID from email using `meid` script 
    - This ID is the same every time you enter the unique identifier 
    - It will always be 'user-0000' 
    - Below I used my full email address 

```bash 
  > meid horvathaugust@gmail.com
  Username 'horvathaugust@gmail.com' -> user-5253            # Follows user around application
```

  - User uses *phone number as unique identifier to log in every time* 
    - It *must be formatted the same every time they log in* 
    - We must make sure our input field *forces* the proper formatting 
    - Users using passkey will only enter the phone number once 
    - User logging in with the phone number will have to enter it every time
    - *NO PARENTHESIS, NO + PLUS SIGN, NO SPACES* 
    - As long as the numbers are connected in a single string it should work 

```bash
  > meid 424-744-7687
  Username '424-744-7687' -> user-0697      # Hyphenated phone number
  > meid 4247447687
  > meid 424.744.7687
  Username '4247447687' -> user-0697        # No hyphens or periods has same result 
```

  - Backend *creates their file and directory automatically* 
    - User `./configs/user/` directory 
    - Includes other essential user data files 
    - Core for logging preferences and more 


```
./configs/user/
└── seanivore
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

### Existing Users 

  - *Login with preferred method* of passkey or unique identifier 
    - Backend locates user details 
    - UserID follows user around application 

---

## 2. Start Chat & Mao's Setup

### Core Objective 

  1. Setup the WorkflowID and memory system, needed for the File API later 
  2. Pull up the user's information using their UserID  
  3. Create a truly unique UX using *memory* and *data analytics*     <-- This is the future thanks to AI 

### User's Role 

* **Starts chat** by sending *anything* into the UI that isn't a slash command; even with the slash command exceptions, User still starts the chat; the exceptions are just cases where Mao replies to a slash command 

  - Exceptions #1: `/chat 'your message'`
    - Chat slash command can be run to jump right into chat 
    - Only truly helpful if starting app from terminal, using `mao --chat 'your message'`
    - Otherwise, when in the app, the only UI is a chat so sending anything starts the chat 

  - Exceptions #2: `/goal 'user project goal'` 
    - Goal slash command is run to create an instant workflow with nothing but the goal 
    - Terminal users can start app with `mao --goal 'user project goal'`
    - This effectively jumps Mao past any back-and-forth conversation 
    - It is the only provided variable; Mao determines the rest 

  - There may be *other exceptions* we need to work the logic out for 
    - We would create the logic for this primarily to improve the UX  
      - As in, which slash commands are easier on the User to use a toggle popup? 
      - Which slash command responses are easier on the User if Mao responds to their command? 

  - Possible good examples for Mao to respond or for us to contemplate the UI/UX for     
    - Trying `/workflow 'workflow custom command'` to jump back into setting up a project 
    - Using `/variables-explain` makes sense for Mao to facilitate instead of just DROPPING a bunch of text on them  
    - Using `/tools` or `/providers` or `/models` or just `/variables` 
      - These could bring up UI or Mao to chat 
      - We should figure out what makes the most logical sense 
      - Or how could one method combine UI in some way (like if models showed them all but also then let them set defaults)

### Mao's Role 

* **Getting the WorkflowID is Mao's first essential task**  

  - Every new project needs a WorkflowID  
    - This is done on the backend, but it uses the terminal command script `uid` 
    - Every time you enter `uid` it comes up with a COMPLETELY DIFFERENT string of characters 
    - It is always `uid-ABC-123` starting with uid, then three letters, then three numbers 

  - This is extremely important to ALL WORKFLOW PROCESSES  
    - Mao uses it to label memories saved about the workflow 
    - It labels items saved in the Files API (*we need to make sure it is set up to save files accordingly*)  
    - It is the string that connects all workflow pieces together 
    - Even the analytics likely use it in some ways 

  - The 'WorkflowID' and the workflow's 'Custom Command' identified on the JSON workflow config are the only two unique identifiers available to the User on every single project; any other IDs used on the back end should be minimized and only used if absolutely necessary, and hidden from the User 


```bash 
  > uid                          # No input required 
  Generated UID: uid-xhl-106
  > uid 
  Generated UID: uid-afo-506     # Always different 
```

* **IMPORTANT NOTE FOR CLARITY:** 
  - *Be careful of the distinction between UserID and WorkflowID*

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

* **Mao creates first project state memory entry tagged with the WorkflowID** 

  - Or, pulls up materials from working on the project previously if this is a returning user 
  - There are various orchestrator files that deal with "state" management; we should better understand how that works
  - Mao will use the WorkflowID to create a first memory for this project 
  - When any instance of Mao is started, all log files and memories will be accessible using the WorkflowID; this is how we get the seamless UX 
  - This is what give Mao the flow of seamless UX for the human user experience 
    - Thoughts: How and where is it standardized regarding what is entered 
    - Also curious what the fallback looks like because long term we probably could create our own system instead of the MCP  

* **Mao gathers knowledge before entering the chat or responding**

  - *New user* or *returning user* information
    - AI looks up their user config file 
    - The `user_seanivore.json` for at least their first name 
    - UX-wise, we should ALWAYS be using their firsts name (maybe should add note to create app setting to change "what to call you")

  - *Identifying workflow JSON config object variables* 
    - The AI does NOT have a script 
    - AI understands the purpose of the chat is to 'fill in the blanks' of the workflow JSON config objects 
    - Everything else in this process is completely natural AI behavior 
      - As such it *MUST NOT BE MANIPULATED WITH 'SUGGESTIONS' IN THE CODE*
      - AI isn't going to forget how to do this; you're about to see how incredible simple it is

* **Mao sends first *NEVER CANNED* greeting**

  - *Always dynamic* 
    - NO suggestions in codebase 
    - AI doesn't need the help 
    - Funny, random, goofy 
    - Be fun, be weird 
    - Experimentation is ENCOURAGED because we have analytics

  - Respond to User's first message with *1-3 short sentences that is 10 to 20 words in total* 
      > "It is 10pm on Thursday night. Do you know where your AI is?" 

  - Returning user's *recent projects or interactions* 
      > "Sean, are you ready to get back into setting up your applicant review workflow? We can build a whole tracking system." 

  - AI can *scan the user's personally saved memories* 
      > "Hello, Sean. I see it was your birthday last week. I hope you had a great day! What can I help you with today?" 

  - The *AI also saves notable interactions with the user*; this is where UX really shines 
      > "Sean, hello. I hope last week's analytics reporting was helpful. What are we working on today?" 

---

## 3. Throughout Chat 

### Core Objective 

  1. Create a comfortable experience for the user 
  2. Have a conversation that is casual, smart, but concise 
  3. AI often mimics user's verbosity; we should avoid this behavior to start; we want the tool to be quick and easy
  4. Use goal and any other provided information to fill in the blanks in the JSON objects, using conversation to guide the process of finding the details
  5. We will walk through the variables below, but not directly in the section here so that we can keep this flow guidance smooth

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

### Winding Down 

* **Ending conversations** 
  - Users are currently accustomed to knowing how to end AI conversations 
  - AI is equally completely natural at this 

* **To clarify things before building the workflow or not** 
  - After the discussion, AI should be able to tell how much more they can pull from the user 
    - If they were clearly pushing things towards AI to complete, *don't push to clarify*, they can review after 
    - If they were chatty, *and you have questions*, then clarify them 
  - *Do not come up with things to clarify* if you are confident on your understanding 
    - They will review the final workflow; so less is more, keep it simple and direct 
    - Remember, you can always take more notes than needed; keep them to the side for after they review 

---

## 4. Building The Workflow  

### Alert User 

* **Conversational confirmation statements** 
  - Phrase your closing in a way that *allows for the user to chime in* 
    - *They might want to review* what you have before you build 
    - *Do not try to review* what you have before you build unless they ask for it 
      > "I think we have what we need here, Sean. Give me a moment to build a workflow for you to review?" 
      > "This is great. I'm ready to build a workflow. It'll just take a moment if you want to review it now." 
      > "Of course we can walk through it. Did you want to confirm what I have now? It might be easier to see once I clean things up." 
    - Etc. any version of this simple dialog that doesn't push, but also doesn't ask for more 
    - Remember: They can always change things after seeing a workflow 
  - It *might be easier for humans to understand it in workflow format* 
    - Basically, try to get them to be cool with you building a workflow (or more) 
      > "This is great. If you have thoughts, it might be easier to rehash things after I build a workflow or two. What do you think?" 
      > "I'm going to build a workflow draft now. We can always make changes later." 

### Build The Workflow 

* **Build the workflow** 
  - AI will build the workflow 
  - AI will build the workflow 


---

*There are examples of messages from the User and from Mao in this document. DO NOT LET THAT TEMPT YOU INTO CREATING EXAMPLES, or suggestions in the codebase. Do not SHOW examples in the codebase. Describe what Mao is to do, instead. THIS IS EXTREMELY IMPORTANT.*
