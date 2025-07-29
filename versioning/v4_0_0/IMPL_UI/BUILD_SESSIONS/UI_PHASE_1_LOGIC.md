# Documenting Our Implementation of UI Phase 1 

## Context Primer Every Session

1. Start the `sequential_thinking` MCP tool and use it to think while you review the following between thoughts. 
2. Run the `memory` MCP tool and search the EXACT term `MAO_UI_Context_Priming_Strategy` in MCP memory and then read these docs in full:**
3. Read: 
    `./CLAUDE.md` --> Complete development rules including new UI Development Guidelines section
    `./documentation/10_AI_DEV_INDEX.md` --> Complete Python backend architecture understanding
    `./documentation/02_REFERENCE.md` --> Complete reference documentation for the project  
    `./versioning/v4_0_0/IMPL_UI/UI_CURRENT_STATE.md`--> Current working UI implementation state
4. Architecture Flow: User Input → ChatInterface.tsx → PythonBridge.ts → ui_terminal.py → orchestrator/ → Response
5. Current Working: `./interfaces/mao/` with Ink 6.1+, React 19.1+, subprocess communication 

## Pristine Logic  

As we were setting it up earlier, the context window was large and AI was making mistakes. My main concern is that we have two documents with VERY clearly defined logic and we need to make sure the implementation is exactly as described and pictured. 

- the first: `./versioning/v4_0_0/IMPL_UI/BUILD_SESSIONS/_VISUAL_BRAND_IDENTITY.md` --> though the icons are a bit complex
- the second: are those used in the example below --> icons here are simple and clear 

### Very Thorough Update of Implementation Document 

Address all of the items on the implementation document: `./versioning/v4_0_0/IMPL_UI/BUILD_SESSIONS/IMPL_UI_PHASE_1.md` 

Use the logic from the sections below. I've made sure to cover every topic. We may need to see if any of the early steps of phase 1 have had code changed made so that we can improve on them. Actually there definitely were code changes because we were testing the terminal. 

---

## Color Psychology  

There were files already written. Please, after reviewing the logic documents above, review the files below and make sure the implementation is exactly as described and pictured. 

- `./versioning/v4_0_0/IMPL_UI/BUILD_SESSIONS/IMPL_UI_PHASE_1.md` 

The document should also be rearranged so that we are first planning out the colors for the themes, which are less about the colors and more about the meaning of each color. The highlighting is a means of acknowledging that the only design element is color in the terminal and that the terminal is all text. The strategy is to help your brain get what they need faster, easier, more efficiently. 

### Color Category: MAIN 

  - This is the user's terminal setting for default "text" color (mind is yellow)
  - It is meant to mean the same things as you'd expect from the default terminal color 
  - You'd scan through it quickly to get the gist of something along with the BOLD highlights 
  - It is not a background color 

### Color Category: BOLD 

  - This is the user's terminal setting for default "bold" color (mind is pink)
  - It is the only one with bold styling 
  - It is a cognitive interrupt 
  - It says "STOP and look" 
  - It identifies for the user what of all the text that need to see 
  - Allows for the user to scan the text and see what is important 
  - It is used sparingly across the viewport 
  - It is not a background color 

Think of it conceptually like MLA title text rules. Here is a quick english class lesson! 

MLA style uses title case, but leaves most short prepositions, articles, and conjunctions in lowercase in titles.
This means:
 • Capitalize the first and last word of the title and subtitle.
 • Capitalize all principal words (nouns, pronouns, verbs, adjectives, adverbs, and subordinating conjunctions like “because,” “although,” “if”).
 • Do not capitalize articles (“a,” “an,” “the”), coordinating conjunctions (“and,” “but,” “or,” “nor,” “for,” “so,” “yet”), or prepositions (like “in,” “on,” “of,” “to,” “with,” “about”) unless they are the first or last word.

So, in MLA, a word like “about”—being a preposition—would be left lowercase in a title unless it appears at the beginning or end.

Example (MLA Title Case):
 • The Art of Thinking about Thinking

Consider this instead of "Chicago style often capitalizes prepositions of four or more letters in titles". MLA is telling your brain what words to read and what words to ignore. Not that we would stop the BOLD in the middle of the highlight for one word, but in a larger conceptual sense, the BOLD is telling your brain what words to ready and what words to ignore. 

### Color Category: USER 

  - The 'USER' is always in medium-light gray 
  - This is because you sent it, you don't need to make it stand out 
  - Your brain can ignore it when looking at the screen 
  - We want you to forget it completely
  - It might not be formatted nicely or might be a block of text 
  - It is a background color 

### Color Category: TRUSTING UPDATE 

  - The 'TRUSTING UPDATE LEVEL 1' is an almost white blue shade  
  - The 'TRUSTING UPDATE LEVEL 2' is a almost-baby blue 
  - These are often used next to each other 
  - Example: In a to do list, the item you 
    - Just crossed off could be TRUSTING UPDATE LEVEL 2 as it is less important now that it is done 
    - Have next to it a TRUSTING UPDATE LEVEL 1 as it is the next item to do and deserves attention 
  - Notably, however, there is always likely something in the viewport that requires BOLD deserving more attention 
  - This is a close second, providing helpful information from AI that is not a priority but makes your life easier 
  - It is not a background color 

### Color Category: SUPPLEMENTAL INFO 

  - The 'SUPPLEMENTAL INFO LEVEL 1' is the same medium-light gray, same as the user color 
  - The 'SUPPLEMENTAL INFO LEVEL 2' is a faded green-gray-brown (to my yellow) 
  - In a block of text, the more important subtext is SUPPLEMENTAL INFO LEVEL 1 
  - In a block of text, the less important subtext is SUPPLEMENTAL INFO LEVEL 2, which is lighter than level 1 
  - They are background, back of mind, colors 
  - You want to find it when you're in need of 
  - You don't want to be distracted by it 

### Color Category: PROCESSING 

  - The 'THINKING' AI IMPROV word is light orange 
  - This has only one use case 
  - When you message Mao, they will be processing your message, thinking, and preparing the response 
  - This will be show using one word above the user text field 
  - The words are picked by AI based on context and will be fun 
  - Hat/tip to Claude Code 
  - Hooray for AI eliminating all canned text forever 
  - It is not a background color 

### Color Category: ACCENT & SUPPLEMENTAL OUTSIDE OF CHAT 

  - The 'ACCENT OUTSIDE OF CHAT' is a light purple 
  - The 'SUPPLEMENTAL OUTSIDE OF CHAT' is a dark faded gray 
  - This is a color probably only used once on the screen, often side by side 
  - The accent is not a background color 
  - The supplemental is a background color 
  - The supplemental is virtually transparent 
  - You'd see this under the user's text field with something like '?  try /help or /config` 
  - Next to that text it might say (use shift + tab twice to enter planning mode)


#### **Visual Hierarchy Goals**
1. **Instant attribution** (who said what)
2. **Priority assignment** (what needs attention)
3. **Information type** (explanation vs action vs context)
4. **Conversation flow** (natural reading patterns)

#### **Terminal Optimization**
- **High contrast** for legibility across terminals
- **Monospace-friendly** spacing and alignment
- **Color-blind accessible** through multiple visual cues
- **Works in various terminal themes**

## Color Pallets 

If possible, AI should help pick colors based on the colors relationships to each other for each of the following pallets. The user is presented this with "choose the best for your terminal". I have a frosted glass background, yellow text, and pink bold and I use "Dark Mode Colorblind-Friendly" which is where the colors above are identified from. The relationship between the colors is more important than the colors themselves. 

While it would be rad to create logic that picked colors based on the user's terminal settings, it isn't reliably known if we'd get the background, text, and bold colors to base things off of. So we can assume that they will be colored properly for their purposes. We can pick the other colors based on their relationships to each other, and fitting in each of the pallets. 

  1. Dark Mode 
  2. Light Mode 
  3. Dark Mode Colorblind-Friendly 
  4. Light Mode Colorblind-Friendly 
  5. Dark Mode ANSI Colors Only 
  6. Light Mode ANSI Colors Only 

---

## Message Block Behavior System Managing Chat History 

To keep the entire viewing space as clean as possible, only ever showing relevant information at that time, no matter how quickly the information is changing in real-time. 

The following logic is very specific and completely planned out. We need to create a plan that implements it exactly as described. The same goes for the visual of the chat terminal below. It is high-fidelity even though it is just wireframe. Spacing. Conceptual semantic syntax highlighting. Bullet point logic. No names. 

### Chat History Truncation Trigger  

Must be done purely for LLM limitations OR design decisions. 

   * Important to note that MESSAGES or "message blocks" of text are not only chat messages 
   * All chat messages and tool updates for actions are considered message blocks 
   * They all live in the same space, and are managed together, and behave like each other, befitting of our one-ui-user-experience 

We are implementing this as a system that counts the tokens in the user's chat thread. It provides a icon-sized pie-chart-like indicator with the percentage of the context window that is being used. 

When the context window is almost gone, the system should automatically create a summary of the chat history, clear the chat except for the last two messages from each User and Mao, or last four messages, whichever is more recent (users can double-text in this app). It will place the summary at the top of the chat history, and then continue the chat as normal with the saved last few chat messages. 

Any active action lists must be kept in the chat history, directly following the chat history summary. 

There needs to be a clear UI notification -- the text under the User text field turning to 'ACCENT OUTSIDE OF CHAT' color and counting down the percentages until the truncation occurs, warning concisely what is about to happen. 

The "count down" must not be literal, otherwise the UX might be frustrating. The users message should be triggered at 10% with a brief message, then again at 5% with a persistent UI message described above. 

Then the chat history truncation should be triggered when there is an extended pause in between messages that is significantly longer than recent chats. Since this will always happen while User and Mao are in the act of chatting, the system should be able to detect this and trigger the truncation. 

### Long Term Functionality 

--> The best way to describe the behavior or message blocks are that they "behave courteously" and "take care of themselves" making sure to only use as much space as absolutely necessary. 

- Every message block of text is constantly being re-evaluated and re-written in real time, to make things as accurate and concise as possible 
- All 'no longer needed' text is hidden first; updates on progress that are presumed to already have been seen, for example
- Long form text is truncated, leaving only the first line of text, and then a second line
- To do lists collapse as they are completed, eventually to a single line. 
- Paragraphs are hidden with a faded, less legible color of the same standard text color in a line that says: ... +37 lines (press ctrl-w to expand)


## Message Block Logic  

The list covers the types of message blocks that are most common; any missing should have logic applied that is logical for the type of message block. 

'Message block' as a term includes messages that are actual chat from Mao or User, as well as updates from the app, and using text, keeps tabs on any active project workflow's progress. 

AI does love their bullet pointed lists, which is great, but we must be sure to use them in a way that is more helpful by making each bullet point longer instead of the normal "three words or less" that seems to be the LLM *truly, very pretty* standard. 

I thought I would have more types of block text than the below, but this is all I'm seeing right now. Obviously if we come across something novel we need to make a point that I look at it and layout the design logic for it. 

### Action Lists 

**TYPES OF LISTS**
  - List is for an ACTION (e.g. project todo lists), or
  - List is a LIST OF ACTIONS (e.g. master todo list)

**LIST BEHAVIOR**
  - They both take care of themselves, being "courteous" of the space they are using, to only use as much as absolutely necessary, as described for each list type below. 

**BEHAVIOR IN DETAIL**
1. Finalized and inactive lists 
  - The first two are completed tasks 
  - They originally had a todo list like the bottom task 
  - Completed, they have collapsed into two lines 
    - Line 1 = ACTION-CATEGORY (Name of the action)
    - Line 2 = "Done" (Tokens • Cost • Time)  
  - The "inactive" state, because of being completed, is indicated by the filled in circle 
2. Inactive, but not finalized lists 
  - The third item, the "Update Todos" action, is a master todo list 
  - It remains present, and after each task is completed, the circle is empty again, and the list is updated 
  - New action lists are created below the master list 
  - Completed action lists, after collapsed, are moved above the master list 
  - List items are indicated as complete or not by the filled in or empty triangle 
3. Active lists 
  - The fourth, fifth, and sixth items, three actions running in parallel, are active lists 
  - Their circles blink from filled to empty when active 
  - The first task is a project and it shows its own todo list that behaves as described above 
  - The second task is an administrative task, and the items below it will change rapidly as the AI completes actions
  - The third is a phase task of a workflow, and the items below *it will change rapidly as the AI completes actions*  
  - Task lists have indicators (triangles) while other types of lists do not; this is because of the ones changing state 
  - In both cases, they will eventually end up collapsing into inactive, completed lists "Done" 
  - Upon completion, admin lists may generate a new list, like perhaps the next projects workflow todo list 

**FEATURE UX NOTES** 
  - Regarding the *it will change rapidly as the AI completes actions* 
  - This action list is a good example of how the list will change rapidly as the AI completes actions, as it currently shows information that isn't really helpful if it was persistent, but it is happening *NOW* which makes it more relevant to show and helpful, for those few seconds it is active. 
  - This feature is a key part of the design, and is a key part of the user experience, as it provides that sense of "immediacy" and helps the user FEEL like things are getting done even faster than they actually are. 
  - Imagine the lack of this feature, and how much more frustrating it would be to stare at a static list of items just waiting, begging that they start to change, even just one more tool use, come on!

**DESIGN NOTES**
  - The use of **bold** indicates the BOLD color, or "MAIN HIGHLIGHT COLOR" that is actually bold 
  - The use of *italics* indicates use of SUPPLEMENTAL INFO LEVEL 1
  - The use of __bold italics__ indicates use of SUPPLEMENTAL INFO LEVEL 2
  - The use of `code` inline-indicators indicates TRUSTING UPDATE LEVEL 1 color 
  - The use of `< >` around text indicates TRUSTING UPDATE LEVEL 2
  - Indentation spacing is done deliberately and shows what the actual product should show, as in this is a very true-to-life example of what the terminal could display, only without color 
  - The icons and one branch down are accurate to high-fidelity designs as well 
  - All un-highlighted text is MAIN text color 
  - Please pull the logic and strategy implied by the placement of these specific highlights and write it out clearly and place it on the implementation document 
  - HIGH-FIDELITY EXAMPLE that is what the terminal could display, only without color, pretty much exactly as shown 

```
●   **Task** (Project memory updates)
    └── Done ($0.003 • 400 tokens • 8.3s)

●   **Task** (Finance report generation)
    └── Done ($0.012 • 60.6k tokens • 8m 32.3s)

●   **Update Todos** 
    └── ▶︎  Add new details to project memory 
        ▶︎  Complete finance report workflow 
        ▶︎  Design adaptive workflow for data collection 
        ▷  <Adapt workflow for full analytics report generation>
        ▷  Design adaptation to workflow for report distribution 
        ▷  <Update memory state for analytics report project>
        ▷  Pull next project and review workflow  

○   **Task** (Analytics report generation)
    └── **Update Todos**
        ▶︎  Download monthly user data from agent deliverable  
        ▶︎  Download monthly system metrics from agent deliverable 
        ▷  Compile comprehensive data sets 
        ▷  Read last month's reports 
        ▷  Analyze data; identify trends and anomalies 
        ▷  Generate written report 

○   **Task** (Preparing next project; Workflow ID: UID-1283)
    └── Read **54** lines *(ctrl+b to expand)*
        Read **88** lines *(ctrl+b to expand)*
        *+ 8 more tool uses*

○   **Task** (Audit Commands 7-9 Orchestrator Integration)
    └── /Users/seanivore/Development/modular-agent-orchestrator/tools/web_searc
        h/button_web_search.py
        /Users/seanivore/Development/modular-agent-orchestrator/tools/web_searc
        __... +37 lines (ctrl+r to expand)__
        **Bash** (find /Users/seanivore/Development/modular-agent-orchestrator/conf
        igs/cli -name "*.py" -exec grep -1 "execute_command" {} \; )

        *Waiting...*
        *+16 more tool uses*

__Key Achievements__:
- *Complete MAO compliance*: CacheManager, estimate_cost () in all files
- *Privacy-first architecture*: GDPR-ready with user data isolation
- *Modular discovery patterns*: Dynamic tool/workflow analytics integration

The system is now operational with `/memory` commands, comprehensive analytics tracking, and a solid foundation for future enhancements. The new `multistage_audited.md` workflow proved highly effective for complex implementations requiring quality assurance.

``` 

### Conversational Text Messages 

- Bullet points are the most common type of conversational text message *from the AI*. 
- They use MAIN HIGHLIGHT COLOR to indicate the most important information, typically the first few words of each bullet point or paragraph. 
- Paragraphs are concise and separated by a line break 
- The last section is USER text color; it always includes the > bullet point  
- As you can see, it is formatted however the user formats it. 
- Numbered list is all MAIN color, numbers and all. In each item though, since it is an ordered list, it is presumable that there is something of importance in each. Claude Code highlights the URLs in each ordered list text item in a list with the TRUSTING UPDATE LEVEL 2 color. 
- Most conversational text messages are maintained in the chat history, but we should truncate the longest (identify a length for the logic) and include the "use ctrl+b to expand" text -- also we could do a "ctrl+r" to read the rest of the message (woah just realized that is why CC uses R... I avoided R because of replicating their genius so much but maybe R makes the most sense)

```
- **Customization ideas** (make it uniquely yours)
- **Big feature possibilities** (when you're ready to dream bigger)
- **Simple edits to try** (because sometimes you just want to tinker)
```

```
**The real truth?** You've already won. You conceptualized, specified, and guided the implementation of a professional-grade terminal UI that rivals Claude Code while adding your own innovations. The MAO orchestration trees, contextual auto-complete, and semantic visual protocol are genuinely cool innovations.

**My recommendation:** Start with the "IMMEDIATE EXPLORATION STEPS" section, run those tests, see your creation in action, and then just... play! Pick whatever sounds fun from the guide. There's no wrong next step when you're already at the summit!
```

```
>   my hands are shaking i had zero idea that we'd get to this point today --CLAUDE CODE IS THE GOAT FOR SERIOUS, IDE'S ARE thank you for all the
help!! I can't believe this thing like from the workflows that started it all with variable input JSON configurations, then one day we were like, wait why is the model hard coded? that SAME DAY, unexpectedly, sonnet 4 was launched. when looking at the detailes with claude was like "ugh why do we have SDKs with everyone, can't we just have like, code a human button for them to push to do something with a tool? and claude is like
"oh... wait.... uhhh... Sonnet 4..... Code Execution.... Is the orchestrator. Yes, yes we can ditch SDK "hell" (always claude's word not mine hahaha) forever. Then the tools, then the freaking models and providers and then the commands and settings -- literally every single thing is PLUG AND PLAY just drop it in and boom, nothing else. I just need to make documents for what each variable JSON config requires like the tools needing 4 files -- THEN we'll have Sonnet 4 learn how to set them up for everyone. Then in v5, we'll use the Claude Code SDK so that people can just aks for custom things and not need to know anything. Our target market is people who dont really use tech. AHH even the UI is basically modular -- like it all is so simple and should translate to an iOS and web app so easily. That is what sold me on this thing -- the fact that the more complex we made it, as long as we also made it modular and i WAS STRICT (becuase claude likes to hardcode heh) it ended up making things simpler in the end-- i was like... that is literally how art works. you put in something and get something else completely unexpectedly ;alsdjf; lasld;l; thank you <3 <3
```

### Pasted Text 

When you paste text into the terminal to send to Mao, it is pasted as a simple indicator of a block of pasted text. This is to avoid chaotic chat history if a User pastes pages of text, while allowing Users to send batches of pasted text to Mao when needed. Note the `< >` around the pasted text for the TRUSTING UPDATE LEVEL 2 color. 

```
>   <[289 tokens of pasted text]>
>   Or if I wanted, I could put it <[653 tokens of pasted text]> in the middle of my message text. 
```

However, let's create logic for it. If the pasted text is more than 75 to 100 tokens. About two long sentences. LMK if you think it should be longer. 

---

## AI "Processing" Contextual Improv'ed Word 

Above the user's text field, at the left, the AI will show a word that is picked by AI based on context and will be fun. 

This is a word that is used to indicate that the AI is processing the user's message.

- The icons should alternate between 🟁 and 🟅 
- Use the exact same cat ASCII art as shown below 
- The word should be the PROCESSING color 
- Users should virtually never end up with the same word ever 

```
 ~(=^‥^) 🟁 Budgeting... 🟅 (8s • $0.003 • 120 tokens)
╭────────────────────────────────────────────────────────╮
│ >                                                      │
╰────────────────────────────────────────────────────────╯
```

- The live updating metrics in parenthesis is to be USER color 
- These must change in real time, it is an important UX feature because it makes the user feel like they are in control of the process and lets them forget how long it is actually taking. It is meant to be quick. 

Hat/tip to Claude Code for this idea in using AI to eliminate canned text forever. 

There is related implementation logic of this for the Welcome screen's message that needs to be found so that they can be implemented together. 

## Live Status Indicators 

These were also used in the lists for an ACTION that was inactive and completed. 

```
●   **Task** (Project memory updates)
    └── Done ($0.003 • 400 tokens • 8.3s)

●   **Task** (Finance report generation)
    └── Done ($0.012 • 60.6k tokens • 8m 32.3s)
```

We'll want COST (to three decimal places), TOKENS, and ELAPSED-TIME -- I know there are many others and we should set it up but plan later about how to present that information. 

---
