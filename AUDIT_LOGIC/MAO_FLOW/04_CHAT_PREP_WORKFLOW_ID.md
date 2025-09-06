
## 4. Mao Prepares for Initiated Project Chat

### Core Objective 

  1. Mao must enter the chat and respond 
  2. Locate or create WorkflowID 
  3. Initiate or locate Project State Memory using WorkflowID (other assets in Files API if return user)
  4. Provide User with a truly unique chat UX 

### Mao Has Entered The Chat Prepared 

* **WorkflowID is Mao's first task** 

  - The system dynamically pulls up workflows using their UserID if they are not a new user 
    - If they are a return user, Mao may want to first ask if they are starting a new project 
    - Or if they're working on a previous project 
  - New projects get WorkflowID 
    - This is done on the backend but it is based on a terminal script `uid` 
    - Every time you enter `uid` it comes up with a COMPLETELY DIFFERENT string of characters 
    - The format characters are always as follows `uid-ABC-123` 
  - The WorkflowID is extremely important to ALL WORKFLOW PROCESSES 
    - Labels memories 
    - Indicates what in Files API goes to the project 

  - The only two unique identifiers available to the User on every single project
    - 1. WorkflowID 
    - 2. The Project's 'CUSTOM COMMAND' to execute a workflow 
  - Both of these unique IDs can serve as a search query if needed by User 
    - Any other IDs used on the back end should be 
      - Minimized 
      - Only used if absolutely necessary 
      - Hidden from the User 
  - Note that the important *UserID* is not something we want to ask Users to memorize 
  - The mention of CUSTOM COMMAND here is because, of anything, that is what the user would remember of a project's workflow 

```bash 
  > uid                        # No input required 
  Generated UID: uid-xhl-106   # Response is always 'uid' then 3 letters, 3 numbers 
  > uid                        # Ran again right away 
  Generated UID: uid-afo-506   # Still always different response 
```

* **IMPORTANT NOTE FOR CLARITY:** 
  - *Be careful of the distinction between terminology surrounding the UserID and WorkflowID* 
  - Also, the CUSTOM COMMAND is unique to every Project 

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
    - AI looks up their user config file `user_5253.json`         # we needs a /user user-1234 command?
    - Finds the file for at least their first name 
    - UX rule: We are ALWAYS using the User's firsts name 

  - Identifying *workflow JSON config object variables* 
    - The AI does NOT have a script 
    - AI understands the purpose of the chat is to 'fill in the blanks' of the workflow JSON config objects 
    - Everything else in this process is completely natural AI behavior 
      - As such it *MUST NOT BE MANIPULATED WITH 'SUGGESTIONS' IN THE CODE*
      - AI isn't going to forget how to do this; you're about to see how incredible simple it is

* **Mao sends greeting**

  - Respond to User's first message 
    - *1-2 short sentences* 
    - *10 to 20 words in total* 
    - *Always dynamic, NEVER CANNED* 
      - NO suggestions in codebase 
      - AI doesn't need the help 
      - Funny, random, goofy 
      - Be fun, be weird 
      - Experimentation is ENCOURAGED (in a future update we will dig into identifying statement sentiment and whatever other linguistic properties we can attribute to messages sent by the AI to get as technical as we can, *and then* we will be able to connect analytics to these messages)

  - Returning user's *recent projects or interactions* 
      > "Sean, are you ready to get back into setting up your applicant review workflow? We can build a whole tracking system." 

  - AI can *scan the user's personally saved memories* 
      > "Hello, Sean. I see it was your birthday last week. I hope you had a great day! What can I help you with today?" 

  - The *AI also saves notable interactions with the user*; this is where UX really shines 
      > "Sean, hello. I hope last week's analytics reporting was helpful. What are we working on today?" 

### Project State __Memory Update Point__ 

  - Name of update: `01-initiating-chat-001` 

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
