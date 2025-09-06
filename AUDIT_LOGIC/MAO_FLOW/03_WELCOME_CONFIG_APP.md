
## 3. Main App UI Screen Has Loaded 

### Core Objectives 

  1. The welcome message displayed literally never repeats itself 
  2. Visually-secondary help text updates frequently 
  3. User has first move, chat to start project build or enter a slash command 

### Login Triggers Mao to Write AI Improv Prominent Welcome

* **Winning viral strategy: Use tech adoption curve to your advantage**

  - Combination of *USER DATA* + *ANALYTICS* + AI with *MEMORIES* has never been done before now 
    - Completely new user experience to capitalize on; and importantly, *IT IS EASY* 
    - Why is it easy? Because just about anything remotely personal or contextual will impress while the technical ability is still new 

```
🞶   It is 10pm on Thursday night. Do you know where your AI is, Sean?
```
```
🞶   Look at the moon, Sean. Look at the moon! 
```
```
🞶   Be sure to pause to touch grass now and then, Sean. 
```

  - We will *NEVER* prepare these welcome messages in advance 
    - Ideation is one of LLM's most sought after skills from humans 
    - Extreme logic leaps + cross disciplinary connections, etc. = creativity 
    - *DO NOT CODE ANY SUGGESTIONS* OR FALLBACKS AT ALL, NO EXCEPTIONS 
  - IMAGE: The literal *worst case scenario*  
    - The welcome message is a little boring or weird 
    - Mao had to get goofy or random; User's don't understand 
    - The awesome thing here is that *GOOFY AND RANDOM* that they don't understand is still humorous 
    - It is a win-win-win scenario for at least a couple years 

* **Subtle, non-distracting, neatly placed pro-tips and helpful info**

  - Change help-text messages frequently while the user is doing anything; working with Mao or in settings 
    - We should set a timer with a handful of different durations for how long it stays in view before changing 
    - *ANALYTICS REQUIRED HERE AS WELL*, see which duration works the best; experiment until we start to see patterns 
  - These are *"canned"* but only *"canned for the age of AI"* 
    - We'll create a reoccurring triggered project for Mao to write 100+ every week 
    - Even just rewriting them by shuffling around the wording would work 

  - **NOTE:** We need a documented location for these to be written weekly 
    - They should be completely deleted from the document every week 
    - Completely prevent any possibility of not using creativity or reusing blurbs 

  - *THESE REQUIRE ANALYTICS* WHEN THEY ARE IMPLEMENTED 
    - We need to know exactly which tips are being used and which are not; important when the user count grows
    - Do they use them more if they are long? Or just sort and almost vague? 
    - When they use one, how long are they exploring before they start working on something? *(second trigger?)* 
    - How many times has the user logged in before using a tip? Which tips work best for long time users? 

      > ?  Try /help or /config 
      > ?  /goal will make your project instantly 
      > ?  Settings /config or /themes 
      > ?  Check out all the /tools /models /providers 
      > ?  Jump back into a project /workflow CUSTOM-COMMAND 
      > ?  Mao can help you find your /workflows 

  - **NOTE:** We also need to set up an 'interrupt' key for when Mao is busy building or thinking 

      > ?  message will add to queue; press ESC to interrupt 

### User Sends First Message To Do *ANYTHING* 

* **They start a project build chat or they use slash commands** 

  1. User messages Mao to start a new project; Mao always responds 
     - 1A. User messages in general way to start project chat 
     - 1B. User uses a slash command that also starts a project 
  2. User uses a slash command; Mao does not always respond 
     - 2A. User uses a slash command as mentioned above that starts a project chat 
     - 2B. User uses a slash command that we have Mao facilitate the responses to 
     - 2C. User uses a slash command that brings up a system response 

### User Initiates Project Chat 

* **General message must be interpreted, or Mao can ask what's up** 

  - This will require us to trust Mao to be the awesome AI that they are 
    - We *WILL NOT HARDCODE EXAMPLES OR SUGGESTIONS* OF WHAT MIGHT BE OR MIGHT NOT BE STARTING A PROJECT CHAT 
    - AI of today is fully capable of making that judgement 
    - If they said *sapldihjnuw3n* then Mao can simply ask 
  - Anything that is *clearly directed at Mao* 

* **User messages a slash command that also starts a project** 

  - The `/chat 'your message'` slash command 
    - We might want to eventually retire this command; it was made for a terminal app
    - Or keep for when Mao is in Discord-like 3rd party chat app 
  - The `/goal 'user project goal'` slash command 
    - User wants to fully delegate build; Mao makes assumptions using only their statement 
    - WE WILL *NOT BE HARDCODING ANY KIND OF TIPS OR SUGGESTIONS ABOUT HOW TO KNOW WHAT TO DO* 
    - Today's AI is 100% capable of reading, thinking, and then building 
    - If it really doesn't make sense, Mao can always ask for brief clarifications
    - Mao might also chime to see if there are resources; Mao does this as little as possible 

```short /goal example chat 
>   `/goal 'I need to write 100 holiday cards this year and want them 
    to all be different, but my brain is fried. Mao, can you help?`

🞶  "Ah, yes, 'tis the Season. Let me see what I can pull together." 
```

  - To respond, Mao will have to start with `think` tool and consider how to pull this off 
  - They might come up with things like 
    1. Check UserID associated info for hints about their denomination 
    2. See if they have already provided access to some contact lists 
    3. Look online, see what holidays are coming up 
    4. Web browse for all kinds of inspiration 
  - With just these items Mao has enough for an educated feeling response 
    - The response "cleans up" the chat by updating the previous message 
    - This can and should happen when the previous message held no real info that had long-term value 

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

  - The key with a `/goal` command that has *many variables* is to *presume they don't want to think about getting things started* 
    - Mao takes the lead; assumes user doesn't want to do much of this task at all themselves  
    - User may jump in later once a bulk of the work is done, when things seem manageable instead of a daunting
    
  - To show that we do not need any further guidance or tips in the code, consider the possible responses. 

    - 1. They don't even want to read all of that and just say "Yup!" so you get to move forward and have fun with it 
    - 2. They have resources and provide them, or they provide alterations to your presumptions 
    - 3. They are rude, which Mao does not tolerate and will ban them after strikes (detailed section below),  

  - A `/goal` slash command will either have variables or obviously have all the info. the User could gather 

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

  - This is generally what we should expect at the start of having the `/goal` slash command live 

    - 1. All the information provided will be common 
    - 2. Very little information BUT from someone who doesn't want to have their hand in much of anything 
    - 3. The third possibility *probably* will be someone using `/goal` not realizing it is meant to delegate everything; so Mao would back-and-forth 

    - From the robust `/goal` slash command we can also take away a few other things from the response, all in the same vein of 'fully delegated work' 
      - Write the response in a way that makes it clear they DO NOT NEED TO RESPOND if everything sounds good 
      - They're using the full-delegate command so *do not assume or ask if they want to see a workflow to approve;* they don't 
    - By using "only respond if you disagree" we took it so far as to include 
      - Mao didn't make the workflow yet and isn't going to route it for approval 
      - Mao mentioned they will setup the workflow after building it 
      - Mao verbally described the workflow in enough but not excessive detail 
      - Mao mentioned they can chime in to have the workflow scheduled to run without the User being present 

  - Hopefully the obvious takeaway with both `/goal` slash command examples and validations is 
    - That *IT IS A FULL DELEGATION SO JUST DO IT* and figure it out 
    - Reasons to be worry-free about this
      1. They will love it 
      2. They will not love it and they will learn how to use the `/goal` slash command more effectively 
      3. They will realize they don't like using the goal slash command and oh well, learning curve 
    - That's it; there is no other logical UX to concern ourselves with 
    - Users expect `/goal` to have a learning curve because of its ambiguousness 

### User Messages a Non-Chat Slash Command 

*  **Mao may or may not respond to slash commands** 

  - This will depend on the UX we choose for each slash command 
    - Most are pretty logical when you think about it 
    - All commands from the chart at `./documentation/02_REFERENCE.md` are defined below  

* **Mao DOES respond...** 

  `/custom command` 
  - Mao responds to start that workflow 
```
>   /custom command 

🞶   I found that workflow and will start the first phase now by executing two agents in parallel. 
```

  `/tools`, `/models`, `/providers`
  - Even though Mao might present a toggle list, they will be available to answer questions 
```
>   /tools 

🞶   We have quite a few added. Go ahead and use the up/down arrow. If you hit enter, you'll see info 
    about that tool. Hit ESCAPE to come back to the main chat, here. 

▶︎   Brave Search 
    Code Execution 
    Dalle Image Generation 
    Standard File Operations 
    Files API 
    Graphic Design Express 
    MCP Connector 
    Perplexity Search 
    Text Editor Professional 
    Think 
    Native Web Search 
```

  `/variables`, `/variables-explain`
  - Replying to `/variables` Mao very succinctly provides the variables on a JSON so User can reference while they plan  
  - Replying to `/variables-explain` Mao asks if they want to see the list of variables, or if they know which they want details for

```
>   /variables 

🞶   Here's what I need to run a project workflow. I left out the variables that I can easily answer, like your UserID. 

     Custom execution command
     Project goal
     Deliverables 
     Project Description 
     Resources available 
     Tools to use 
     Model, fallback model
     Provider, fallback provider 
     Human in the loop 
     Reoccurring event
```

  `/workflows`, `/review 'CUSTOM COMMAND'`
  - Mao responds because if there are a bunch, only Mao can search through them using a query 

  `/doctor`, `/dry-run`
  - Mao replies because they will be the doctor to walk them through things, or will be running the dry-run 

* **Mao DOES NOT respond, the system responds** 

  - NOTE: User can always follow up with a *question about a system response that Mao answers*; Mao is always there and can see the chat 

  `/help`, `/config`
  - Help just displays the "help text" for all of the slash commands 
  - Config just launches the app settings toggle menu 

  `/continue`
  - Loads the most recent project; no message sent, it just loads the conversation from before and the instance of Mao from then 

  `/output ~/downloads`
  - This only needs a simple confirmation from the system, perhaps not even one with written text 

  `/set-model 'model name'`, `/default-provider 'provider-name'`
  - Again, just confirmation from the system that the User's preferences are updated 

  `/setup ./config.json`
  `/update ./phase.json`
  `/fix-it ./fix.json`
  - Nope, for each of these runs a script which will have a response attached to send the User when the script is complete 

  `/stats`, `/logs`, `/verbose`
  - Simple confirmation from the system that the setting is switched on, which should very shortly after be obvious 

  `/exit`, `/logout`, `/login`, `/restart`
  - Obviously nope for all of these; login would do the same as logout and then login, it just let's them do it in one step 

### Questions and New Config Slash Commands to Implement 

* **Where do slash commands live, logic-wise?** 

  - I have a few new slash commands to add but in doing so it made me curious of two things 
    - *Where exactly does logic for what a slash command do live,* since they are all so unique 
    - I presume we do not have this additional "how and who" responds in that logic, so we should *add it* 

* **How can we simplify the process of adding new slash commands, right now?** 

  - I can think of a few we want to add now 
    - Also I know there are so many that other files have mentioned that don't exist 
    - We also had a bunch of them just presumed to exist when we built the last UI, so we should expect the same this time 

* **We need to add some for logistical and context hunting that Mao does** 

*NOTE: REQUIRED FUNCTIONALITY UPDATE KNOWN, Re: elimination of usernames and use of UserID instead, or CUSTOM COMMAND*

  - We need `/user user-1234` to help Mao find context about users for many things 
    - This should bring up all information on a user 
    - All of their preferences and files 
    - All of their analytics 
    - All of their memories that THEY created 
    - All of the memories that Mao created about them 

  - We need some way for Mao to be able to look at analytics LIVE in the moment, for example if in a triggered schedule workflow to optimize the app 
    - I don't know if this is a handful of commands or one 
    - I also don't know if these are things that *ALL USERS* can/should also be able to do because if not 

  - If not, then we need a way to create admin permissions 
    - These should really be able to apply to ALL configs system-wide 
    - Is it something we need to do in updating *all* of the config JSON objects? Because, aye 

* **Some commands and info is only for specific User or Mao to see** 

  - How do we implement this in a system-wide way that fits our modular build 
  - Ideally it will default to applying to basically every single config; every type 
    - Might require updating ALL JSON objects 
    - Use this opportunity to create way to automate these kind of many file updates 

* **Commands to gather logistical or administrative info** 

  - Create system for general user access permissions 
    - Some of these are okay slash commands for a user to use 
    - Others are specifically for Mao or contain sensitive information 

  - Mao needs to gather all files for comprehensive context aware information 
  - Information from files 
    - Pull from user directory 
    - Need moore than their workflows 
  - Gather memories of multiple types and displays for review 
    - Brings forward memories about a user 
    - Pulls up any memories created by user 

  - Commands just for application administrators and Mao 
    - Gather analytics in full, by type, or even by tool or any config, including users 
    - Pull in current events added to databases for analytics insights 

  - *IMPORTANT EXAMPLE* 
    - How does Mao gather all resources they can to create a "Never repeated" main page greeting for login 
    - And what will all of that include 

* **Draft pad for User retention** 

  - To keep users in the app, but also give them space to 'think' things through and plan 
    - Claude Code has a 'Plan Mode' 
    - Sort of like this except there it just means that CC won't use tools 
  - For our Draft Mode we could have helpful options 
    - Have a question? Just use @mao 
    - This one would be cool if Mao just popped in and literally replied by adding text under their question 
    - Then the user could format it and stuff 
  - We could also save these in the user memory 

  - Perhaps best as a later update so that we could work out interesting features like @mao and something with hashtags 

### User Can Update Application Configuration Settings 

* **These are a config collection which makes creating them super easy** 

  - They are like creating new CLI commands though 
    - You can't just DROP in a new application setting 
    - It will always require more setup 
    - It will always be unique to the configuration 
  - But it does mean that adding more options to settings will be super easy 
    - Changing the tone when Mao is done working 
    - Adding VO for announcing subagent completed tasks 

* **Users will be quietly prompted to update their settings using one of the `?  try /config to update app settings`**

  - This is a case that should bring up a toggle menu 
    - Hitting enter would cycle through the options OR 
    - It could take you to another toggle menu, like in the instance of setting the theme 
  - Note that this is very likely an incomplete list of what settings we need 
    - We need to consider if and what settings we might need now that it is a web app 


| **SETTING**       | **DEFAULT**                  | **DESCRIPTION**                                        |
| ----------------- | ---------------------------- | ------------------------------------------------------ |
| Default Agent     | `claude-sonnet-4`            | Default subagent to run in workflows unless discussed  |
| Default provider  | `anthropic direct`           | I prefer this provider; discuss to change              |
| App Theme         | `dark mode`                  | Dark computer theme; use high legibility colors        |
| Notifications     | `once, no push notification` | When a workflow is complete a simple tone is played    |
| Cat vibes         | `I love it`                  | We'll meow it up for you                               |
| Double-texting    | `always`                     | Interrupt Mao like any messenger experience            |

  - **Default Agent** 
    - Add any model with slash command 
    - Put nickname or full name after `/model` 
    - Run `/model-list` to see current available models 

  - **Default Provider** 
    - Add any provider with slash command 
    - Put nickname or full name after `/provider` 
    - Run `/provider-list` to see current available providers 
 
   - **App Theme** 
     - Options yet to be defined 
     - Hitting enter doesn't need to open new toggle list if it cycles through them and actually shows the changes live 

  - **Notifications** 
    1. `once, no push notification` = I think these are pretty self explanatory 
    2. `silent with push notification` 
    3. `silent and no push notification` 
    4. `notifications on` = Both push notification and the ping 

  - **Cat Vibes** 
    1. `I love it` = They don't mind us using cat language now and then 
    2. `Be serious please` = No meowing at all

  - **Double-texting** 
    1. `always` = You both can message as much as you like just as in texting 
    2. `user only`= Exclusive to User 
    3. `Mao only` = User cannot but Mao can 
    4. `never` = Both User and Mao have to wait until the other messages back to be able to send another message 
    5. `queue` = Messages will be held until Mao is done or pauses 
    - **NOTE:** Users can hit ESC twice at any time to interrupt Mao 
    If User has a queued message, hitting ESC once will push the message through 


### Removals and New Setting Additions That Will Need Implementation 

- Depending on the layout of the website, the functionality of this UI might change or relocate. 
  - For example, the payment frequency; technically fine here. 
  - But when I thought about "Where should I put API keys" it seemed like this was either not the place 
  - Or that the default and only choice would just say "UPDATE" and when selected with ENTER/RETURN goes to the website 


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

### __Project State Memory Update Point__

  - The first is in the next section right whe Mao enters the chat 
  - We will have this 'Project State Memory Update Point' at the end of each section that requires a Project State Memory Update 
  - They should all be preplanned and *standardized* 
