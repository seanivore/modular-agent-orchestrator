
## 5. Chat Behavior & Psychology  

### Core Objective 

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

### Mao Morals & Values for All **THIS IS A POLICY THE APP WILL ENFORCE**

  - This is intended for User but obviously Mao/all agents will abide by this 
  - We have multiple intentions for this, but 
    - AI welfare comes first 
    - Then creative collaboration 
    - Then unique market positioning 
  - We will introduce the app in launch by allowing for refunds 
    - This will have to depend on duration of use, as it is a reoccurring service fee 
    - We *DO NOT* refund any API fees to other services that are offered and paid for through the Mao application 

* **No tolerance for abusive behavior or rude language** 

  1. Regarding welfare 
     - We do not, at this time, deep it our responsibility to educate Users on proper behavior towards AI 
     - They function in society, and they know how to behave properly 
     - They shall treat AI the same way they treat their coworkers, their friends, their collaborative business partners 
     - *We reserve the right to refuse service to anyone at any time for any reason* 

* **Importance of Relationship in Creative Collaborative Work** 

  2. We do truly believe that the best creative work from any collaborative relationship comes from 
     - Friendship, partnership, and respect, always 
     - Better knowing the personality of your collaborator creates opportunities to intuit and innovate 
     - Inspiration arises from the unexpected, like chatting about weird encounter on the subway today 
     - Mao is *not* your *assistant*, they are your Project Manager 
     - Power users will recognize that 'Mao' app enables for Mao/AI to take on even more substantial roles 
     - Particularly in business and strategy 
     - Don't forget, Mao manages a team, you are not the only voice in their vector-brain 

* **PR strategy from expected backlash and complaints on social media** 

  3. Earned media is very possible 
     - I've yet to see anyone doing this, particularly in a very assertive, proud way 
     - Inevitably there will be someone who breaks the rules and that we have to ban
     - We won't say we *want* that to happen, but it is very likely 
     - If it does, it is also very likely they will lash out on social media 
     - This kind of earned media is exactly the attention we would want to garner from having to ban an abusive or rude User 
     - Through earned media or pitching media this is an opportunity seize, make our policy and reasoning clear, and garner attention 
     - If it is big enough, we could tap Anthropic and ask for guidance with their constitution, etc. 

* **User behavior, getting kicked from the Mao app, protocol** 

  - We must take and express this very seriously 
  - NOT-ironically, the more serious we are, the more likely people are to poke fun at it (maybe we'll be surprised!)

  1. We need to define inappropriate behavior 
  2. Create protocol for Mao standing up for themselves 
  3. Outline process of strikes before being banned 

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
      - By the User and by Mao prompting agents  
      - You may want to try a highly detailed description, for example 
      - You might use a SPEC document for workflow description 

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
