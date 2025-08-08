# Flow of Data Through Mao 

## Overview 

- The docs all say that the flow is this: 

"User Goal" --> "Conversation Bridge" --> "Natural Language Processing" --> "Core" --> "JSON Workflow Creation" --> "Model Selection" --> "Execution" --> "Results" --> "Caching"

- But to really clean up the hardcoded categories in the code, I need to better understand what is actually happening and where 
- So I'm going to write it out in normal language that includes what information is conveyed and where 

IMO, this feels very overly complex. The workflow JSON is just simple variables which are just parts of a prompt request. 

### Goal 

The `core.py` file is where we started and we found so many categories. They hardcoded them as "suggestions" for the AI but the AI does not need suggestions. We went to `conversation_bridge.py` and found the same grouping. 

Once we understand what the logic should be, and what the file's current logic is, then we can clean up all the files in the flow. 

### Deliverable

**AI knows the variables. They are able to have a conversation with the user and fill in the blanks. We do not want anything more complicated than that. The only categorical grouping we want is for analytics. NO SUGGESTIONS. We also need to be aware of launching multi-lingual; none of these prefabs would make any sense in a multi-lingual environment.**

The secondary benefit of doing this is that we'll have a really nice diagram. 

---

## 1. User Login 

### New Users 

  - *Login with passkey or a unique identifier* which is used to create their UserID 
    - Passkey will require providing unique identifier once 
    - Other users have to enter unique identifier every time 
    - Email or phone number qualify 
    - They must provide their first name 
    - They may optionally provide thgeir last name  
  - Backend creates UserID from email using `uid` script 

```bash 
  > uid horvathaugust@gmail.com
  Generated UID: uid-ona-821            # Follows user around application
```

  - User uses *phone number as unique identifier to log in every time* 
    - It must be formatted the same every time they log in 
    - We must make sure our input field forces the proper formatting 
    - Users using passkey will only enter the phone number once 
    - User logging in with the phone number will have to enter it every time

```bash
  > uid 424-744-7687
  Generated UID: uid-hlu-632            # Hyphenated phone number
  > uid 4247447687
  Generated UID: uid-rye-904            # Is different than no hyphens
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
    - UID follows user around application 

---

## 2. Start Chat 

### User's Role 

* **Starts chat** by sending anything into the UI that isn't a slash command 

  - Exceptions #1: *chat command* 
    - `/chat 'your message'` can be run to jump into chat 
    - Only truly helpful in terminal using `mao --chat 'your message'`
    - Otherwise, when in the app, the only UI is a chat so sending anything starts the chat 

  - Exceptions #2: *goal command* 
    - `/goal 'user project goal'` can be run to set a goal 
    - Terminal users can start app with `mao --goal 'user project goal'`
    - This effectively jumps Mao past any back-and-forth conversation 
    - It is the only provided variable; Mao determines the rest 

  - There may be *other exceptions* we need to work the logic out for 
    - These would be primarily for better UX 
    - Meaning, andy commands that get a response from Mao instead of from the system 
    - Trying `/workflow 'workflow custom command'` to jump back into setting up a project 
    - Using `/variables-explain` makes sense for Mao to facilitate 
    - Using `/tools` or `/providers` or `/models` or just `/variables` could bring up UI or Mao to chat; examples that need logic 

### Mao's Role 

* **Entry knowledge** 
  - *New user* or *returning user* information
    - AI looks up their user config file 
    - The `user_seanivore.json` for at least their first name 
    - We PUSH using the first name 
  - *The variables needed to complete workflow JSON objects*
    - The AI does NOT have a script 
    - All the AI needs to know is the purpose of the chat: To fill in the blanks in the JSON objects 
    - Everything else is natural AI behavior and MUST NOT BE MANIPULATED WITH 'SUGGESTIONS' 
    - AI will not forget how to do this; it is what they're great at 

* **Never a canned greeting**
  - *Always dynamic*, meaning NO suggestions in codebase 
    - AI doesn't need the help 
    - Funny, random, goofy -- all of these are fun and we should encourage experimentation 
    - We have analytics to adjust what works and doesn't over time 
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
  2. Have a casual conversation that is casual, but smart and concise 
  3. Use goal and any other provided information to fill in the blanks in the JSON objects 

### Truly Simple Behavior 

* **AI behaves naturally**
  - *Gauge user's needs* based on their behavior  
  - Something AI already does naturally 
  - If the *user is spitting out details rapidly*, help them get things in order, provide suggestions 
  - If the *user is pasting exactly the variables needed*, then facilitate putting them directly into the JSON objects 
  - If the *user is quiet*, then coax them into conversation 

* **Interactive behavior** 
  - AI can easily consider in the moment 
  - Providing suggestions for the user to consider if they seem to be poking for them 
  - When the *user is collaboratively reciprocal*, provide ideas
  - When *user is friendly*, actively clarify to understand their needs 
  - If *user is standoffish*, then prepare the JSON objects for them to review in more formal way 

* **AI simply guides**
  - AI can *help the user understand the consequences of their choices*
  - Explain the trade-offs 
  - Help the user understand the best way to achieve their goal 
  - Help the user get things in order

### Winding Down 

---

## 4. Take What You Have 
