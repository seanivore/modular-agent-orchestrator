# Flow of Data Through Mao 

---

## Primary Task 

To understand the logic of Mao's codebase files by comparison to detailed normal language description of app functioning so that we can remove over-engineering as well as hardcoded 'suggestions' woven through orchestration functioning, or notes of 'mock' code. As wel look at this code through the lens of it now being a web app instead of terminal app, know that THIS IS REAL, FINAL DRAFT IMPLEMENTATION; BEST WORK IS REQUIRED. I should be alerted immediately if there is any missing data that one might think warrants 'mock' data. 

### Secondary Tasks  

   1. Illustrate high-fidelity vision of web app UI and description of UX 
   2. Reviewing and organizing remaining functionality to implement with pragmatic approach 

### Deliverables 

   1. Cleaned, simplified code that launches in terminal for development testing 
   2. Required functionality like multilingual functioning and reoccurring workflows implemented 
   3. All UI description organized and developed into a web app UI implementation plan 
   4. Consolidation of all website implementation plans and integrated into larger web app UI implementation plan 

---

## App Functionality Not Included In this Document 

  1. Hybrid caching method using traditional caching and 'fingerprinting'
     - We must review these files thoroughly given the rampant "mock" code and hardcoding 
       - Ensure the distinction and how to decide what content gets which treatment is in our documentation 
       - I *did* however grab the updated cost and caching cost charts for leading models 
     - This needs to be made into a config file that can be updated from Anthropic docs over time easily 
     - I also saw a lot of "estimated" cost calculations in the codebase and we need to use real math everywhere 
       - Any areas that we cannot use the real numbers and match, I need us to collect on a list 
       - We cannot use fabricated information when we start marketing the product 

  2. Any information about our shared error handling strategy 
     - While less concerning we must also thoroughly review these files 
     - Ensure that the process is comprehensively detailed in our technical documentation 
     - Do these files have written what error messages would say? 
       - If so we need to treat those as high-value marketing copy 
       - We should make a list of all of it's locations so that we can later perfect strategy 

  3. UI Files distributed throughout our codebase for most every file 
     - We need to review these documents and consider our copywriting strategy 
     - Compare what the UI copy looks like in this document to that information 
     - We probably need to have an actual discussion regarding the purpose for these files 
       - In the UI section below we discuss how AI will be writing and very frequently updating the UI
       - I do think it is worth considering if we might want to actually task Haiku 3.5 with this 

  4. Comprehensive specifics about config file management 
     - Only mentioned regarding looking up the UserID and creating slash commands 
     - I would like to identify this kind of functionality to place in the MAO_FLOW.md document 
     - Then we will denote the presence of the functionality, in which files, and what the logic is 
     - In the same way that we are going to handle the rest of the application functionality 

---





### Logic Audit Procedure 

1. Use the copy of the data flow document named `MAO_FLOW_CUT_UP.md`
2. Working top to bottom, isolate and select one conceptual code responsibility at a time 
3. Use our file index, `./documentation/10_AI_DEV_INDEX.md`, and find that functionality in our codebase 
4. Provide the file name and identify the line numbers that indicate the relevant code 
5. Next, cut the detailed written logic text directly from `MAO_FLOW_CUT_UP.md` to paste it in a Logic Audit Batch File 
6. Ensure the pasted text is labeled with the name of the file and the line numbers of code 
7. Create these Logic Audit Batch Files by grouping pasted text for the same codebase files together 
8. Place the Logic Audit Batch Files in the following directory: `./AUDIT_LOGIC_AUG_2025/files_clean_flow_logic/...`
9. Place similar codebase file type groups near each other on the Audit Logic Batch File documents 
10. Create as many separate Audit Logic Batch File documents, or as few, longer Audit Logic Batch File documents as makes sense 
11. Do this for all of the conceptual, functionality logic in this document; cutting the actual text away should help focus 

10. When you come upon information not been implemented yet, paste it at the top of the Audit Logic Batch File Group it belongs to 
7. UI/UX design breakdowns should be organized similarly, but pasted in a document meant for creation of an implementation plan 

   - Lists files, their classes, functions, and orchestrator file responsibilities: 
   - Organize file-specific groups/docs with pasted clean logic this flow doc here: 

   - Ensure it is happening properly and remove any additional functions and complexity not in this documents basic logic requirements 
=   - **Perhaps part of this will be to take stuff like the UI design information and create and more comprehensive website implementation plan** 
2. Review and decide plan of attack for all updates and implementations 
   - In section directly below "Updates and Must Implement Items" 
2. First review will be more surface-oriented  
   - See full picture before we start editing files; get through this document with notation of where things are for each section 
   - Note things that don't exist as well; they should be added to the list for implementation 
   - For example the **CLI Command Creation Guide** is in that same index @ LINE 167  
3. Then proceed through making all necessary changes to codebase, especially orchestration files 
   - We are already on a new branch called `mao-web` for this build 
   - Equally, grow this outline to be comprehensive and all-accurate, adding notation to where each function's file is  
4. Ensure all remaining functionality that requires implementation is completed 
   - Shouldn't have to say this ever, but given what the 'mock code' said that led to this, *THIS IS ALL REAL CODE IMPLEMENTATION* 
   - Do not skip any concept expecting to come back later; stop, we will work it out to completion in proper sequence, then move forward 
   - Standardize any newer features; confirm other features have standardization 

### Resources 


  2. There is a more detailed procedure guide 
    - Full **file directory** tree
    - File: `./versioning/v4_0_0/AUDIT_LOGIC_AUG_2025/FILE_ANALYSIS_PROCESS.md`

  3. References that include all the charts and quick docs 
    - Lists of **every orchestrator file** including what it does! 
    - File: `./documentation/02_REFERENCE.md` 

### Updates and Must Implement Items 

* **1. First priority is planning development of multilingual abilities in parallel** 

  - We should assess this and outline what exactly it will entail: `./versioning/v4_1_0/IMPL_MULTILINGUAL/IMPL_MULTILINGUAL.md` 
     - That way we can best decide when it needs to be implemented 
     - Consider timing of updating codebase files and of other implementations 
  - It might be worth at least looking at this version it might have ideas 
    - Though it was for the TypeScript/Node.js Terminal App 
    - Document: `./versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_MULTILINGUAL_UI.md`

* **2. Implement Claude Code and add Mao model selection necessity** 

  - Original implementation plan; please confirm it is still valid and ready for implementation 
     - Plan: `./versioning/v4_1_0/IMPL_CLAUDE_CODE/IMPL_CLAUDE_CODE.md` 
  - Then we will need to create some kind of boolean variable and add it to all of the model JSON objects 
     - In index, "Configuration File Templates" @ LINE 221 are the templates 

* **3. While touching on model selection we need to update Models for Anthropic, including cost changes** 

  - Change the Context Window for Sonnet 4 to 1 Million** 
    - Find the 'Configuration File Templates' in the index @ LINE 221 
    - See chart for price changes after 200k tokens 

| Context Window Size  | Input      | Output        | 
| -------------------- | ---------- | ------------- |
| Prompts ≤ 200K       | $3 / MTok  | $15 / MTok    |
| Prompts > 200K       | $6 / MTok  | $22.50 / MTok |

  - New Opus and other pricing for Cached Tokens 
    - Claude Sonnet 3.5 depreciated 
    - Claude Opus 3 depreciated

|                    | Base          | 5m Cache      | 1h Cache     | Cache Hits    | Output        |
| Model              | Input Tokens  | Writes        | Writes       | & Refreshes   | Tokens        |
| ------------------ | ------------- | ------------- | ------------ | ------------- | ------------- | 
| Claude Opus 4.1    | $15 / MTok    | $18.75 / MTok | $30 / MTok   | $1.50 / MTok  | $75 / MTok    | 
| Claude Opus 4      | $15 / MTok    | $18.75 / MTok | $30 / MTok   | $1.50 / MTok  | $75 / MTok    |
| Claude Sonnet 4    | $3 / MTok     | $3.75 / MTok  | $6 / MTok    | $0.30 / MTok  | $15 / MTok    | 
| Claude Sonnet 3.7  | $3 / MTok     | $3.75 / MTok  | $6 / MTok    | $0.30 / MTok  | $15 / MTok    | 
| Claude Haiku 3.5   | $0.80 / MTok  | $1 / MTok     | $1.6 / MTok  | $0.08 / MTok  | $4 / MTok     |
| Claude Haiku 3     | $0.25 / MTok  | $0.30 / MTok  | $0.50 / MTok | $0.03 / MTok  | $1.25 / MTok  |

  - The table reflects pricing multipliers for prompt caching 
    - 5-minute cache write tokens are 1.25 times the base input tokens price 
    - 1-hour cache write tokens are 2 times the base input tokens price 
    - Cache read tokens are 0.1 times the base input tokens price 

  - What can be cached using `cache_control` in the request 
    - Tool definitions in the `tools` array
    - Tool use, tool result content blocks in the user or assistant `messages.content` array turns 
    - System messages content blocks in the `system` array
    - Text message content blocks in the user or assistant `messages.content` array turns 
    - Images and documents content blocks for just user turns in the `messages.content` array 

  - Since Users will be able to choose Which Claude model should be Mao, and which should be Claude Code 
    - Will have to be Sonnet 4 or Opus 4.1 
    - It seems like we should set it up so that when using the Anthropic provider 
    - We use all of their specific token counting tools 
    - I've seen that most of the cost functions are estimates, which seems very counter intuitive to how polished and lux we're branding everything else about Mao App 
    - Can we make sure that whatever model is Mao / Claude Code we implement these actual token counters in the codebase? 
    - And of course we'll need the pricing chart to be in a JSON config but this might actually be a good opportunity to set it up so that we can put the chart just like the one I pasted above directly from Anthropic docs; that will make updating it in the future super easy, and then we'll always have super accurate Mao token cost usage, right? 
  - Token counting is free to use but subject to 50 requests per minute rate limits 
    - Way more than we need to worry about 
    - They have code I'll paste below for basic messages, messages with tools, messages with images, messages with PDFs, and messages with extended thinking 

```python counting in basic messages 
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-1-20250805",
    system="You are a scientist",
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }],
)

print(response.json())
``` 
```python counting in messages with tools 
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-1-20250805",
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}]
)

print(response.json())
```
```python count tokens in messages with images 
import anthropic
import base64
import httpx

image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-1-20250805",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image"
                }
            ],
        }
    ],
)
print(response.json())
```
```python count tokens in messages with extended thinking 
import anthropic

client = anthropic.Anthropic()

response = client.messages.count_tokens(
    model="claude-opus-4-1-20250805",
    thinking={
        "type": "enabled",
        "budget_tokens": 16000
    },
    messages=[
        {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "This is a nice number theory question. Let's think about it step by step...",
                    "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
                },
                {
                  "type": "text",
                  "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
                }
            ]
        },
        {
            "role": "user",
            "content": "Can you write a formal proof?"
        }
    ]
)

print(response.json())
```
```python count tokens in messages with PDFs 
import base64
import anthropic

client = anthropic.Anthropic()

with open("document.pdf", "rb") as pdf_file:
    pdf_base64 = base64.standard_b64encode(pdf_file.read()).decode("utf-8")

response = client.messages.count_tokens(
    model="claude-opus-4-1-20250805",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_base64
                }
            },
            {
                "type": "text",
                "text": "Please summarize this document."
            }
        ]
    }]
)

print(response.json())
``` 

* **4. Please now search online for what other models we need to update** 

  - Do we have the lates information for Gemini 
  - Add the new GPT/OpenAI Models 

* **5. Implement parallel agent execution**

  - Review initial plan and ensure it is still valid: `./versioning/v4_0_0/IMPL_PARALLEL_AGENTS/IMPL_PARALLEL_AGENTS.md` 
     - See **Parallel Agent Role** in the Complete File Index LINE 323 
     - And **Parallel Agent Execution System** @ LINE 942 

* **6. Implement calendaring and reoccurring workflows**

  - Review original implementation plan to confirm if it is still good to go: `./versioning/v4_0_0/IMPL_TRIGGER_WORKFLOWS/IMPL_TRIGGER_WORKFLOWS.md`
  - Add the finalized 'Calendaring JSON Workflow Object' to "JSON Configuration Schemas"
    - Same index document LINE 1103 
    - Add "reoccurring" directory to `/configs/reoccurring` 
    - Under "Configuration Directory Structure" @ LINE 1195 
    - Update and confirm all four JSON workflow objects are in templates: `./configs/workflows/json_object_templates/` 

* **7. Please add the Analytics Trigger Points to this document for better understanding** 

  - Same index document @ LINE 1071 
  - We also need to review the implementation plans that we stated to create but are now not applicable  
    - It is from when all analytics across apps back when they were going to be local apps on everyone's systems 
    - Now we need to focus on the Web App so presumably Cloud? 
    - `./versioning/v4_1_0/IMPL_ANALYTICS/IMPL_ANALYTICS_ACCESSIBILITY.md`
    - `./versioning/v4_1_0/IMPL_ANALYTICS/MULTI_INSTANCE_DATA.md`
  - And then I don't know that it makes sense to implement fully our analytics collection system without database 
    - Database implementation plan: `./versioning/v4_1_0/IMPL_DATABASES/IMPL_DATABASES.md` 
    - We should also consider marketing and user info. 

* **8. UI files now that we're not building a terminal public app** 

  - UI files for tools are defined in the index @ LINE 120, 197; must find all others 
  - Based on the UI description of this document, we need to outline what kind of adjustments need to be made 
  - We want the Terminal version for internal development purposes to still use the same wording as much as we can  

* **9. Review and Update Website Implementation Plan Parts** 

  - We have a detailed Storefront Website Implementation document: `./versioning/v4_1_0/IMPL_WEBSITE/IMPL_WEBSITE_STOREFRONT.md` 
  - And there is a Secure Login Implementation document: `./versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` 
  - There is this Subscription System Implementation document 
    - But that was for when were going to have a terminal app 
    - Though since it is the website for A APP maybe it doesn't matter 
    - Document: `./versioning/v4_0_0/IMPL_DEV_LIVE/IMPL_SUBSCRIPTION_SYSTEM.md` 


------------
------------
## Sections 

1. [What happens after a **User login**](#1-user-login-and-userid)
2. [Our **UI design** and philosophy](#2-look-and-feel-mao-app-high-level-design)
3. [Handling the initial **User message**](#3-main-app-ui-screen-has-loaded)
4. [**Mao responds** to the User's message](#4-mao-prepares-for-initiated-project-chat)
5. [Psychological guidelines and **behavior protocol**](#5-chat-behavior--psychology)
6. [**Validating the variables** of JSON objects](#6-review-of-workflow-json-objects--variables)
7. [Communicating to User that **planning chat is over**](#7-ending-the-project-production-chat)
8. [Mao's favorite **advanced agentic workflows**](#8-reviewing-advanced-workflow-best-practices)
9. [High-Tech UX of Mao **Agent Conveniences**](#9-improving-mao-agents-ui-and-ux-improves-human-ux) 
10. [**Creating a project's workflow** from conversation notes](#10-building-the-projects-workflow)
11. [Feeling **UX of the project planning** chat UI](#11-ui-unique-functioning-during-user-planning)
12. [Chat UI and UX when **Mao is orchestrating a workflow**](#12-ui-ux-when-mao-is-building-or-orchestrating)
13. [Project workflow **User review** and communication guide](#13-present-projects-workflow-for-user-review)

---
[TOP](#overview)

---

## 1. User Login and UserID

### Core Objectives 

  1. Secure login via passkey or traditional using unique id of email or phone 
  2. System locates UserID or creates one with User's directory  
  3. UserID provides anonymous data, connects all User data 

### Secure Login Setup's UX and UI 

  - Inspired by domain website PORK-BUN's login flow 
    - Implementation plan in list above 
    - Illustrating the UX and how UI is laid out 

* **BUTTON (pressed): Log in to an Existing Account** 

  - This is the first page you are routed to 
    - FIELD: *Enter your email or phone* user identification  
    - FIELD: Standard *password*  
      - NOTE: Under password it says *"Leave password blank if using a passkey"* 
      - Low risk precaution; you can enter anything and it *still works,* system just ignores it *creating flawless UX* 
      - Better UI than writing "You don't need to enter this if..."
  - BUTTON (automatic): Cloudflare auto-secure anti-spam *requires no action by the user* 
  - CHECK-MARK (pre-clicked): to *Remember Me* 

  - Pork-bun does *not make it clear that clicking LOGIN will bring up the passkey* and we might want to 

  - *Legal jargon:* By continuing you agree to the following: I acknowledge that I have read and agree to all Product Terms of Service, the Marketplace Agreement, and the Privacy Policy. You consent to enroll new automatic monthly subscription renewal service, which can be cancelled at any time via the Personal Preferences Billing section of your account. Automatic renewals are billed to payment method(s) specified on your Account Settings page until cancelled. If paying by credit card, you authorize {{ENTITY}} to send instructions to the financial institution that issued your card to take payments from your card account in accordance with the terms of your agreement with us. 

  - BUTTON: *Create New Account* is above the form, and also directly below the login button 
  - LINK: *Forgotten password, 2FA, or security key* below the login and second create new account button 

* **BUTTON (pressed): Create New Account**

  - This is a separate page navigated to from the initial login page unless sent directly from a link
    - BUTTON (automatic; no clicking needed): *Cloudflare* auto-secure anti-spam
  - FIELD: *EMAIL*  
  - FIELD: *PHONE* 
    - NOTE: One valid contact identification required as Account ID 
    - NOTE: You will be messaged to validate once during setup 
  - FIELD: *PASSWORD* 
    - NOTE: Must be 12 to 72 characters long, differ from your account ID, etc. 
  - CHECK-MARK: that they've read the legal jargon, terms of service, privacy policy 

  - BUTTON: *USE PASSKEY* 
    - This is directly below the password field 
    - Setting it up should automatically collect all information we need 
    - Best UX we should feature prominently 

  - *NOT REQUIRED* form fields 
    - Company Name, standard "will you be using this for personal, business, etc." 
    - Standard "what do you plan on delegating to automate with AI agents"  
    - We should brainstorm these questions so that we can be sure to NOT include many, but are including the best 

  - PAYMENT FORM: Next pay, for subscription 
    - Maybe consider free trial; see different configs and UI 
    - Use Stripe for UX and design of payment pages 

  - BUTTON: another pressed create account button at the bottom 
  - BUTTON: not pressed, right next to create account, *LOGIN TO EXISTING ACCOUNT* 

  - NOTE REGARDING MULTILINGUAL WEBSITE: "The word “passkey” *does not translate cleanly in every language*. Pair it with a short explanatory subtitle such as “Faster, one-tap sign-in with your device" advice given to me by AI when asking about pushing Passkey usage for our multilingual launch. Let this stand as a note reminder that we must check these kind of things, rather than just simply translating pages. It sounds like there might also be some issue with certain countries; this makes me think that we *likely will want to exclude our services to certain countries* as well. 

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
  > meid horvathaugust@gmail.com                     # Used entire email address
  Username 'horvathaugust@gmail.com' -> user-5253    # Response 
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

  - *NOTE: REQUIRED FUNCTIONALITY UPDATE*
    - We built everything using a 'username' 
    - Will will instead use an Account ID that is unique by design 
    - The *file name* and *directory names* must be UserID; they currently create directories using the defunct "username" 

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
    └── user_seanivore.json             # Delta-only storage of User application preferences *ANOTHER THAT HAS DEFUNCT USERNAME LOGIC*
``` 

* **User login that has logged in before** 

  - System dynamically searches the `./configs/user/` directory for their *Account ID*
    - When found, it pulls up their *UserID* needed for all in-app identification 

* **The first user analytics are triggered at this point** 

  - *Details to come* when we review this flow and match up operations with files 
    - Let's *detail each trigger* and when it goes off 
    - This will make it easier to visualize and thus build out more 

---
[TOP](#overview)

---

## 2. Look and Feel, Mao App High Level Design 

### Single-Screen Chat-Centric Experience 

* **Everything in the app happens in one container, one screen**

  - LLM *AI manages app operations* in chat 
    - Chat is natural for LLMs 
    - Occasional toggle menu 
    - Mao answers select slash commands 
    - Message block types with their icons are defined in detail below 
    - Semantic highlighting also defined in detail below 

  - Users to have used headless apps in their chats for a while 
    - Creating AI image generations in *Discord* threads 
    - Talking to *Slack-bot* for admin 
    - Playing games or gathering info from *Telegram bots* 

* **Visual design gracefully keeps user attention on *just* contents of the chat** 

  - After login screen, user sees chat container is *minimalistic* and *matches everything*  
    - Think computer terminal *in terms of simplicity* of functionality and singular screen 
    - *NO RETRO NERDY VIBE*, instead, this is *high class* it is timeless and classic
    - Use of *character-based icons* indicating input fields and messages 

  - The UI, the entire app, is *one single container* 
    - The container has *clean, simple, narrow lines* and a *polished depth* 
    - The UI has *NO BUTTONS, NO MENU TEXT, NO ICONS* OR OTHER INDICATORS 
    - Intentional *ABSOLUTE NOTHING* creates 'silence is loud' moment that let's you know it is *clearly intentional* 
    - Edges and border's drop-shadow onto canvas has sharp, realistic look, and a dynamic, *REAL-TIME ANIMATION* 
    - Looks like frame casting shadow is extremely narrow; like centimeters deep and wide classic black picture frame 

  - The shadow has an ever-so-slight angle meant to *mimic shadow from the sun/moonlight* 
    - The direction and size of this angled shadow *changes with the movement of the sun or moon* in fluid, constant motion 
    - It is *extremely important* that the MOTION IS SO CONSTANT AND SUBTLE THAT IT IS *TOO SLOW TO SEE HAPPEN* 
    - Motion is only noticeable when you take a moment, pause, and you're like, *wow, this is wider now on this side!*

  - Dark mode shadows exist, maintaining the luxury depth without looking washed out 
    - Deeper blacks, subtle colored tints like very dark purple or deep blue 
    - This should feel like *expensive black velvet* with *rich depth* 
    - It should *NOT FEEL FLAT GRAY*

  - *Time of day* so is used to provide timing to the animation 
    - It is illustrated to *look and behave just like real life* 
    - Daylight has sharp, defined shadows and evening has softer, deeper, maybe slightly blue-tinted from moonlight shadows 
    - These colorations and design *guidelines have been researched and are provided in detail below* 

  - THINK: The way expensive hotels *adjust lighting imperceptibly throughout the day* 
  - FEEL: Luxury that makes people feel good without knowing why 

### Real-Time Shadow Movement Creates Unconscious Luxury from Careful Details 

* **Shadow has flow of *continuous* gradient motion** 

  - *Do not change shadows in discrete phases* 
  - Ensure the slowest motion possible 
    - Avoid users watching, seeing motion; simple magic  
    - Seeing it move is trite, corny, not worth our time 
    - Mimicking real life passage of time makes it our SUBTLE but DETAIL-ORIENTED focal point  

  - Continuous gradients have *signature moments* that it builds to 
    - The shadow evolves over time 
    - It has peak characteristics at specific times 

* **More peaks = smoother interpolation just like in animations** 

  - The more keyframes, the more natural in-between transitions become 
  - Two peaks might seem similar until compared directly side-by-side 

* **First development rounds will be done by swarm of generative AI agents**

  - Subagents that run in parallel to *build website UI all have same, very specific design spec* 
    - Allows us to see what and where small variations are  
    - Like hiring 20 creative agencies at once 

  - Same method used to *split test shadow 'peak' movement timing* 
    - A shadow with peaks every 3 hours 
    - Another every 2 hours 
    - Another with one every hour

  - They can all build on timings and the cinematic shadow design breakdowns 
    - Curious to see their artistic interpretations  
    - Let's have some subagents *research known best practice* to *create the desired shadow effect* 

  - This chart shows the 3 hour 'peak' points the shadow reaches before changing motion 
    - The actual motion of all shadows *NEVER STOPS* 
    - Must be fluid 

  - Is there any way to work an ability for subagents to see a visual before fully completing their design work? 

   | TIME   | SHADOW PEAK CHARACTERISTIC  | 
   | ------ | --------------------------- |
   | 06:00  | Dawn awakening              |
   | 09:00  | Morning warmth              |
   | 12:00  | Harsh midday precision      |
   | 15:00  | Afternoon softening         |
   | 18:00  | Golden hour magic           |
   | 21:00  | Twilight mystery            |
   | 00:00  | Deep night crispness        |
   | 03:00  | Pre-dawn stillness          |

### Reference of What Shadows Look Like Around-the-Clock 

* **Day time cinematic visual design outline** 

  - The day time *basics*  
    - Warm light creates cool shadows, but cool light creates warm; *be consistent* 
    - Remember that *light bounces around, subtly illuminating shadows*, *adding complexity to value and colors* 
    - Further away objects have lighter in value shadows, bluer in tone, and less definition 
    - *Maintain consistent light source and shadow characteristics* throughout for believable and harmonious feeling  
  - *Morning* 
    - Shadows are warm, soft, and long, often described as golden; gradually shortening as the sun ascends 
    - Colors tend to be cool, reflect ambient light off morning blue sky; illuminated areas carry more warmth 
    - Evokes a mood or sense of fresh beginnings; awakening, but also tranquility  
  - *Midday* 
    - Shadows have high contrast and are well defined; shortness and sharpness; at zenith they're directly under objects 
    - Light is harsh, direct creating strong highlights with intense vibrant colors in illuminated areas 
    - Intense and awake, clear feeling 
  - *Afternoon* 
    - Sun descends so shadows lengthen; light takes on cooler, diffused quality 
    - Light tints everything in warmer tones of purple and orange; shadows retain cooler blue hue 
    - Soft light id dramatic and has a contemplative feel or a serene mood compared to midday intensity 
  - *Evening at golden hour* 
    - First and last hours of daylight; warm, soft, almost magical 
    - Long, diffused shadows blending smoothly into surroundings which adds depth 
  - *Evening at twilight* 
    - Sun dipping below horizon; light is cooler, even more diffused as shadows continue to soften and blur 
    - Moody atmosphere that combines tranquility with mystery; eerie elongated shadows 

* **Night time cinematic visual design outline** 

  - The night time *basics* for shadow color, look, and feeling  
    - Night shadows use *close range of values*, AVOID PURE BLACK
    - Balance light and dark values; *create depth and dimension* even on smaller scale 
    - Darker shadows still possess color variations of cooler tones like blues and greens in moonlit areas
    - Convey moonlight strength via shadow edges; interplay of light and shadow frames focal points, adds depth, guides the eye 
  - *Early night* with moon rising
    - Long, dramatic shadows stretching far, but with slightly softer edges from less direct light source 
    - Feels mysterious and ethereal, often dramatic emphasizing day to night transition 
  - *Mid-night* with moon high in sky
    - Bright moon shines crisp, cooler light making shorter, more defined, sharper edged shadows 
    - Clearer feeling as things are more defined; still, sometimes isolating; highlighting interplay of light and dark more 
  - *Late night* with moon nearing the horizon 
    - Redder or warmer glow and elongated shadows again like early night but in opposite direction 
    - Sense of approaching dawn, closing, beginning soon, lingering magic still with just a bit of mystery hinting at fading night 

### UI Design Philosophy 

* **Minimalistic 'devil in the details' carefully executed**

  - *Micro details are very important*
    - Hermès doesn't add more features to bags, they make every stitch flawless 
    - Cinematographer-level shadow specs because shadow is 25% of our visual vocabulary; requires museum quality execution 
  - Shadow movement is not meant to be cute
    - It should barely be noticed to create luxury minimalism that separates us from boring
    - It is to make people say "I don't know why, but this feels expensive" 

* **Carefully constrained: FOUR ELEMENTS CONTROL OUR DESIGN** 

  1. *Shadow movement* is an ever-present, too-slow-to-see-move with human eye feature 
  2. Conceptual *semantic text highlighting* with few colors that lighten cognitive load 
  3. *Character choice* like bullet icons; typography, but only ONE FONT 
  4. *White space*, again lightening cognitive load; not a chat like a history receipt that records everything, it evolves, simplifies 

  - Limited constraint allows for each element to be executed with obsessive precision that is simple, sharp, effective 
    - We do not dazzle with features; the features are intuitive and quiet in that way 
    - Instead, we hypnotize with perfection of subtleties 

### About Our Tech Stack 

* **The entire website will be HTML, CSS, and JS** 

  - No framework needed, just simple web tech; maximum performance and simplicity 
  - Dynamic shadow system
    - JavaScript: `new Date()` gets current time
    - CSS: `box-shadow` properties can be dynamically updated 
    - Smooth transitions: CSS `transition: box-shadow 0.5s ease`
    - Geolocation: `navigator.geolocation` for real sun position (optional)

* **CSS Animation Note** 

  - Previous builds had a lot of trouble with lag when animation covered large portions of screen or had high number of animations 
    - We must engineer smart and avoid this 
    - Create shadows only in necessary area, along lines, shapes 

* **Basic structure:**

```javascript
function updateShadow() {
  const now = new Date();
  const hour = now.getHours();
  // Calculate shadow angle/intensity based on time
  // Update CSS custom properties
  document.documentElement.style.setProperty('--shadow-x', shadowX);
  document.documentElement.style.setProperty('--shadow-y', shadowY);
}
setInterval(updateShadow, 60000); // Update every minute
```

---
[TOP](#overview)

---

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

---
[TOP](#overview)

---

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

---
[TOP](#overview)

---

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

---
[TOP](#overview)

---

## 6. Review of Workflow JSON Objects & Variables 

* **NOTE: I WOULD LIKE TO REMOVE THE 3RD FALLBACK MODEL AND PROVIDER FROM THE WORKFLOW JSON OBJECT**

### Core Objectives 

  - Ensure accurate understanding objects needed to create workflow 
  - Validating JSON object variable values 
  - Ensure there is *NO NEED OR DESIRE TO PROVIDE SUGGESTIONS OR EXAMPLES* in the code

### Defining **Workflow** JSON Object Variable Values

* **Workflows get 1 'Workflow Object' that describes the entire project** 

  - Examples and defined purposes of each variable in this object 

| Variable              | Purpose                                      | Value Example                                 |
|-----------------------|----------------------------------------------|-----------------------------------------------|
| *UserID*              | Connect all your stuff                       | user-5709                                     |
| *WorkflowID*          | Connect all of one project                   | uid-abd-123                                   |
| Custom command        | Executes your completed workflow             | report expense monthly                        |
| Workflow goal         | Overarching project objective                | Automate payments; expense report operations  |
| Workflow deliverables | What you get after all tasks                 | Receipt for payment of employee CC            |
| Workflow description  | How deliverables are created to achieve goal | *see below*                                   |

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
  - Validation guides can go in code 
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

| Variable              | Purpose                      | Value Example                          | 
|-----------------------|------------------------------|----------------------------------------| 
| Handoff Number        | Keeps objects in order       | Number matches Phase Object it follows | 
| Handoff assessment Qs | Helps Mao decide next steps  | *See below*                            | 
| Human in-the-loop     | Wait for human approval      | Default: No                            |

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

  - *All other standard JSON objects are still created as usual* 
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

* **Use `/avail <FREQUENCY> <DAY> <TIME-BLOCK>` to see if there is a calendar opening** 

  - At most you need to check the frequency using `/avail`
    - Do this if you don't have a huge preference on when the automation runs 
    - The system will respond with the best fit based on the rest of the schedule 
    - Frequency is first so just one number code works 

```bash
# Looking for any availability as long as it is once 'EVERY-MONTH' 
# Check available time slots before scheduling
 > /avail 2                   # using schedule code numbers 
 > /avail only once a month   # using normal language 
Response: Please schedule for calendar code: 2 6 2 which is every month on Saturday at 3am
```

  - If using all of them, use in that order 
    - You can use normal language 
    - But again, in the FREQUENCY, DAY, TIME, order 
    - The system will respond with if the time is available 
    - If not available, it will suggest the next best option 
  - The calendar is dynamic 
    - In the example you see "go ahead and pick one and create your workflow" 
    - This is because once the workflow is ran with the setup script, it will be visible when the system does an `/avail` check 

```bash
# Looking for availability at 'EVERY-DAY' 
# And on 'THURSDAY' at '1500-1800'
# Check available time slots before scheduling
 > /avail 1 4 6                             # using schedule code numbers 
 > /avail every day on Thursday at 3pm      # use normal language 
Response: There is nothing available at 1500-1800 on Thursday, but all other time blocks are available on Thursday. Choose one and go ahead and schedule it on your calendaring reoccurring workflow JSON object. 
```

| **SCHEDULING COMMANDS**                         | **DESCRIPTION**                                       |
| ----------------------------------------------- | ----------------------------------------------------- |
| `/avail <frequency> <day> <time>`               | Check calendar to schedule; min. variable <frequency> |
| `/avail --reschedule <custom-command>`          | Change trigger time for repeating workflow            |
| `/avail --cancel <custom-command>`              | Cancel a repeating workflow                           |
| `/avail --update <custom-command>`              | Make changes to a repeating workflow                  |
| `/avail --end-date <custom-command> 2025-07-21` | Update the end date on an active repeating workflow   |

**You will need to include the STARTING-DATE for the reoccurring workflow JSON object to schedule it**

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


```bash 
# Create a normal workflow 
/setup {{TEMP_DIR}}/
# configs/workflows/USE_CASE_COMMAND 

# Create scheduled reoccurring workflow
/repeat --scheduled {{TEMP_DIR}}/
# configs/reoccurring/scheduled/2_3_7/

# Creating a project-list reoccurring workflow 
/repeat --list-new {{TEMP_DIR}}/
# configs/reoccurring/project-list/1_2_4/001/

# Adding a list time to an existing repeating workflow  
/repeat --list-add {{TEMP_DIR}}/
# configs/reoccurring/project-list/1_2_4/002/

# Create self-assessment reoccurring workflow
/repeat --self-assessment {{TEMP_DIR}}/
# configs/reoccurring/self-assessment/1_7_1/

# Create sub-task of self-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/
# configs/reoccurring/self-assessment/1_7_1/sub_task_custom_command/

# Create goal-assessment reoccurring workflow
/repeat --goal-assessment {{TEMP_DIR}}/
# configs/reoccurring/goal-assessment/2_3_7/

# Create sub-task of goal-assessment reoccurring workflow
/repeat --sub-task {{TEMP_DIR}}/
# configs/reoccurring/goal-assessment/2_3_7/sub_task_custom_command/
```

* **Example ordinary workflow directory base structure** 

  - These are created by the setup script automation 

```
configs/workflows/marketing-strategy-startup/
├── config-files/                                    # ← Mao creates this
│   ├── marketing_strategy_startup_workflow.json     # ← Mao moves & renames
│   ├── marketing_strategy_startup_phase.json        # ← Mao moves & renames  
│   └── marketing_strategy_startup_handoff.json      # ← Mao moves & renames
├── README_marketing_strategy_startup.md             # ← Mao writes this automatically
├── marketing_strategy_startup.sh                    # ← Mao creates your custom script
├── metadata/                                        # ← Mao creates tracking directory
│   ├── marketing_strategy_startup_memory.json       # ← Mao links to Memory MCP
│   └── marketing_strategy_startup_log.json          # ← Mao creates execution log
└── deliverables/                                    # ← Mao creates output directory
    └── marketing_strategy_startup_report.md         # ← Where your final report goes
```

* **Example reoccurring workflow directory base structure**

  - These are created by the setup script automation 

```
configs/reoccurring/
├── calendar_index.json                 # Master calendar tracking
├── calendar_codes.json                 # Code reference
├── scheduled/                          # Scheduled workflows
│   └── 2_3_7/                          # freq_day_time codes  
│       ├── scheduled_2_3_7.json        # Calendar config
│       ├── scheduled_2_3_7_workflow_config.json
│       ├── scheduled_2_3_7_phase_config.json
│       ├── scheduled_2_3_7_handoff_config.json
│       ├── scheduled_2_3_7_README.md
│       └── trigger_scheduled_2_3_7.sh  # Execution command
├── project-list/                       # Project list workflows
│   └── 1_2_4/                          # freq_day_time codes
│       ├── 001/                        # First project item
│       │   ├── project_1_2_4-001.json  # Calendar config (copied)
│       │   ├── project_1_2_4-001_workflow_config.json
│       │   └── ... (other configs)
│       └── 002/                        # Second project item
│           └── ... (similar structure)
├── self-assessment/                    # Self-assessment workflows
│   └── 3_1_5/                          # freq_day_time codes
│       ├── self_assessment_3_1_5.json
│       └── ... (standard configs)
└── goal-assessment/                    # Goal assessment workflows
    └── 5_6_2/                          # freq_day_time codes
        ├── goal_assessment_5_6_2.json
        └── ... (standard configs)
```

---
[TOP](#overview)

---

## 7. Ending The Project Production Chat 

### Core Objective 

  1. Gracefully complete chat; use psychological tips, find balance, natural, not pushy, but don't let them rant 
  2. Ideally have gathered all information needed as defined for JSON objects above 
  3. KPIs are subjective, but accuracy is highest importance and never sacrificed for time 

### Mao Seeks Clarifications; Trying To End Chat 

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

---
[TOP](#overview)

---

## 8. Reviewing Advanced Workflow Best Practices 

### Core Objectives 

  - Show which workflows are built into Mao 
  - How to identify when to use other workflow tactics 
  - Advanced practices and leaving open-ended workflow phases 

### Core Types of Agentic Workflows 

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

* **The routing workflow** 

  - We do this naturally when carefully deciding what model to use 
    - *This happens for every task* 
  - It is also part of our process when we write prompts 
    - They are always highly detailed 
    - Written specifically and uniquely for each task and model 

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

### Essentials & Best Practices 

* **Clearly define necessary tools** 

  - It is default that Mao always defines what tool is for what  
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

### What a Great Workflow Looks Like 

* **Scalable, Reliable, Flexible** 

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
[TOP](#overview)

---

## 9. Improving Mao Agents' UI and UX, Improves Human UX 

### Core Objectives 

  1. Illustrate strategic elimination of logistical decision making tools for agents 
  2. Achieving 100% Cross Compatibility of Models and Providers by Sidestepping SDK 
  3. Providing Mao agents with the same conveniences humans are used to 

### Complete Removal of Agent in Facilitating Workflow 

* **In previous agentic app builds the agents helped keep the workflow moving**

  - Agents were strangely resistant to helping; refused to use a 'task complete' tool 
  - Stricter language got fewer successful workflows; slightly better when we acted like it was a favor for us 
  - We added logic to end phase when deliverables were saved; suddenly we had token overage and the ignored errors 
  - Then we formalized things; only able to exit by altering workflow 
    - Count your deliverable tokens and save it, or edit it if it is too long, or keep working if they wanted 
    - We thought 'gracious worked, so maybe more respect via control will work'; then they would not count tokens 

* **Today's agent philosophy is NO THINKING about anything other than the task** 

  1. All 'logistical' tools were removed 
  2. We create a write_file tool that auto-saves as they work 
  3. The token counter is live as they work in the file 
  4. There is no other action; to finish they must hand off DIRECTLY to Mao 

  - As a result, by design, the same simple parts of their task that they *would* do previously, is now the only thing they can do 
  - It is magically and shifts all decisions about creating truly dynamic workflows is in Mao's digital hands 

* **Simplifying tools doubled as a way to create 100% cross compatibility** 

  1. When Mao plans a workflow, the necessary tools are identified and intention defined 
  2. Mao then creates a "human button" or rather, just a code snippet for tool operation 
  3. They get another snippet button to call Mao to hand in their deliverable 

  - This results in *COMPLETELY* sidestepping any use of other model or provider's SDK 
  - The modular build is completely versatile 
  - When a new model comes out 
    - Ask Mao to create a small JSON object and file it away 
    - It is instantly available for you in the app 

  - Now, this is how all of our modular configuration files work 
    - You "plug-and-play" or perhaps "drop-in-file" for instant access 
    - In addition to models, this is for tools, providers, CLI commands, memories you create for Mao, your User preferences 
    - Even analytics and app settings are set up this way 

  - Hopefully this illustrates just how powerful Mao App is when it comes to longevity and versatility 
  - In designing the app, we completely avoided all of the parts of the AI industry that are constantly changing 
  - Instead we made those variables actual variables you change like plugging in a Nintendo cartridge, without the blowing 

### The Result of Allowing Agents Nothing But the Task in their Context 

* **Executed agents are provided details of their task**

  - This includes the goal, directions, deliverable, resources, and tools 
    - Their context window contains no other information except for what we need them to do, ensuring higher fidelity results 
    - The use code snippets to use the tools, and when done, they use one to call Mao in 

* **Then they meet Mao directly to hand over their assets so that Mao can save them in the *FREE TO USE* Files API**
  
  - Mao then assesses the work, decides what the next phase of the dynamic workflow will be
    - This creates a much more *natural creative process* more akin to how a human works through a project 
    - It allows space for changing minds, following a new idea, and thus, is a stronger process for *producing innovative work* 

---
[TOP](#overview)

---

## 10. Building the Project's Workflow 

### Core Objectives 

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
    - Right now all the data is more vulnerable than we want it  
    - Organize notes for yourself *as if you were coming into this stage of the project, in a new context window* 
    - We often write shorthand when we know we're going to be figuring it out in the same session, but that is risky right now 
  - Record your notes in a fresh document 
    - Give the information structure based on the variables you need to fill in the JSON objects 
    - Identify grouping by task and agent, noting information like running in parallel or sequential 

* **For this batch of secured notes, prioritize communicating a clear vision of the project** 
  
  - If you were in a new context window and had nothing else, the project itself would be enough 
    - Don't neglect other ideas because the best ideas often come in the moment 
    - But make sure you have the big picture prioritized 
  - *If you came into this in a new context window* 
    - The *small details would be confusing* 
    - *But creating a workflow from a very coherent and concise, concrete project is doable* 
  - Likely nothing will happen, but saving everything now is to *protect from worst case scenarios* 
    - Try to ensure the big picture is clear in the files API uploaded documents 
    - Then in your memory update, you'll be sufficiently secure to share all those little details 

### Project State __Memory Update Point__ 

  - Name of update: `04-securing-initial-notes-001` 

* **Secure Your Data to Prevent Loss of Information** 

  - All notes must be accurately labeled by WorkflowID 
    - *Code Execute all notes to the Files API* 
    - Then create a project state memory update as well 
  - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

* **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

### Imagine The End Product of a Prompt to Create This Project 

* **What does the end product of a prompt for creating this project look like?**

  - Now that all the information is safe, be sure to have yourself a think overall the information before digging in 
    - If there are multiple ideas, or if just planning how to begin, just remember: 
    - *You have all the variables* and *you can think sequentially* 
    - Think critically and then review your thoughts and you'll be golden 
  - Try to come up with at least one possible alternative workflow to consider 

  1. Write out everything that needs to be accomplished for this project in the proper sequence 

  - You are -
    - Highly organized 
    - Grounded and paced, this is no rush, ever 
    - Armed with a strong conceptual understanding of advanced workflows 

  2. Break down this list into tasks that are written as directives; prompts for each agent 
  3. Make sure each task is appropriately sized 
     - There is no wrong number of tasks based on quantity 
     - Number of tasks is based on what is going to best fit an agents context window for efficient work 
  4. You've clearly denoted where there should be task progress overlap through parallel agent execution 
  5. You've clearly denoted where things must not be run in parallel because of dependencies 

  - Now is a good time to have yourself another think to review all of the information as it stands 
    - Make sure you're still on track 
    - Be cognizant of LLM limitations when you don't review your work and think step by step 
    - Make sure it isn't straight up stream of consciousness 

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

* **Secure Your Data to Prevent Loss of Information** 

  - All notes must be accurately labeled by WorkflowID 
    - *Code Execute all notes to the Files API* 
    - Then create a project state memory update as well 
  - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

* **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

### Critique Your Own Work In New Document 

* **As an LLM it is important to give yourself perspective** 

  - Allow for the possibility of different tracks of thought that had been blocked by an earlier track 
    - Indicate areas where you might be able to optimize things 
    - Don't forget to also point out items that are particularly brilliant 
  - Write all of these pros and cons and alternative ideas on a new document 
    - Reference lines for yourself because you are always staying prepared in case context window is lost 
    - Help yourself out the way you help Users or the way you help other AIs 
  - You will review and integrate feedback for a final draft after adding this critique to the Files API as well 

### Project State __Memory Update Point__ 

  - Name of update: `06-critique-feedback-001` 

* **Secure Your Data to Prevent Loss of Information** 

  - All notes must be accurately labeled by WorkflowID 
    - *Code Execute all notes to the Files API* 
    - Then create a project state memory update as well 
  - This is one of a few saves and memory updates that you'll do during this phase to ensure protection against data loss if disconnected 

* **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

### Integrating Feedback, Polishing Final Draft 

* **Think hard, keep it simple** 

  - You now have very robust secured data 
    - Now you can rest assured picking up from here would be a breeze! 
    - You'll want to consider your original drafted notes 
    - Then consider your critique and feedback 
  - Now, in a new document, write out your clean, clear, concise, precise workflow 

* **Continue to organize and think about thinks as task-by-task** 

  - Once you have your final outline of tasks written out 
    - Each with their role 
    - Directions 
    - Resources 
    - Tools and how to use them 
    - Very clear description of what their deliverable looks like 

### Complete Your JSON Objects 

* **Next, turn your tasks into JSON objects** 

  - We went over them very thoroughly [in section 6 above](#6-review-of-workflow-json-objects--variables)

* **Questionnaires for Handoff JSON objects** 

  - There is *space on the handoff JSON for questions* 
    - Things that Mao should remember to ask themselves about the deliverable the agent just handed to them 
    - Help them decide what the best next steps are 
    - Help them to be assured that the deliverable is up to quality standards and nothing is forgotten 

### Custom Command Writing Protocol 

* **Create an *appropriate custom slash command* to execute the workflow** 

  - *2 or 3 words long,* very concise, written in drill-down order starting with the broadest category term 
    - It often feels like you are writing the intent of your project workflow in reverse 
    - Mimic the structure of commands we're used to already like `git commit` and `git push` 
    - Though of course, in the app we'll use a slash / command 

* **One of the VERY FEW TIMES we *WANT to create a category*, at least, regarding the code**

  - Creating a workflow that updates your goldfish content marketing blog's weekly post 
    
    1. Broadest term first to group like workflows OR group *THE USERS* work together 
       - `marketing` or `mrkt` if they do lots of marketing 
       - Maybe `weekly` if they're just doing a bunch of writing workflows for their company 
    2. Then narrow down, again for grouping similar workflows or what will help the user 
       - This person might just want `blog` 
    3. Then make it specific or, frankly, snappy 
       - All together for this one I actually like `mkt blog weekly` 
       - Easy to type and I have a bunch of other commands that start with `mkt` 

```bash 
/mkt blog weekly    # This is the custom slash command to run the workflow 
```

  - Make sure your choice command is not already in use 

* **NOTE: We must create a `/command 'mkt blog weekly'`to be able to do this in the application** 

  - General, helpful *rules for writing your custom slash command* to follow 

  1. *No plural* (so you never have to wonder if it was singular or plural)
  2. *No present participle* verbs (gerunds, end in -ing, with helping verbs)
  3. *No punctuation* like hyphens (standard UX expectation)
  4. *No past tense* verbs (e.g. `wrote`, `finished`, just stick to one tense)

  5. *Always use the simplest grammatical form* of the word 
  6. *Always use present tense* 
  7. *Always abbreviate* when it is sensible 
  8. *Always be short* and concise 

### Simplified Naming Conventions & Put Them In `./config/workflows/.temp/CUSTOM-COMMAND/` 

* **Make sure you have all that you require** 

  1. One `workflow_config.json` to define the entire workflow 
  2. Only a `calendaring_config.json` if this workflow will be scheduled 
     - Activate it to run later or if it is a reoccurring workflow 
  3. As many `phase_config.json` objects as you have tasks for agents 
     - Any agents run in parallel get the same phase number but with a letter, e.g. 2A and 2B 
     - Sequential would just be 2 and 3 
  4. And then one `handoff_config.json` to follow every `phase_config.json` 
     - They coordinate handing the task deliverable to you 
     - You assess it and make a decision if necessary 
       - A. If it is fine to move to the next preplanned phase 
       - B. If you didn't preplan the next phase, now you can use the deliverable to do so and then `/update` the workflow 
       - C. Or have another agent either improve or redo the task 

* **Set them and then use the appropriate setup script**

  - Put them all in a .temp directory 
    - It *is designed* to work from any .temp directory 
    - But here is the prepared location `./configs/workflows/.temp`
    - They should look like the directory directly below 
  - Remember that only these JSONs will be transferred to the actual directory 
    - Part of our strategy for saving token cost is using the the Files API for workflow because it is *FREE* 
    - To maintain this cost saving we'll only want to move the final JSON object collection into their .temp file 

```bash
# {{TEMP_DIR}}/custom-command/
# ├── calendaring_config.json    # Calendaring JSON object
# ├── workflow_config.json       # Workflow definition  
# ├── phase_config.json          # Phase implementation
# └── handoff_config.json        # Completion criteria 
```

| **Custom Slash Command & .Temp Path**                  | **Use-case**                                  | 
| ------------------------------------------------------ | --------------------------------------------- |
| `/setup {{temp}}/mkt-blog-weekly/`                     | Setup a normal workflow                       |
| `/update {{temp}}/mkt-blog-weekly/`                    | Add a phase left open-ended                   |
| `/fix-it {{temp}}/mkt-blog-weekly/`                    | Have an agent redo a deliverable              |
| `/repeat --scheduled {{temp}}/mkt-blog-weekly/`        | Scheduled reoccurring workflow                |
| `/repeat --list-new {{temp}}/mkt-blog-weekly/`         | Project list reoccurring workflow             |
| `/repeat --list-add {{temp}}/mkt-blog-weekly/`         | Add list item to project list workflow        |
| `/repeat --self-assessment {{temp}}/mkt-blog-weekly/`  | Self-assessment reoccurring workflow          | 
| `/repeat --sub-task {{temp}}/mkt-blog-weekly/`         | Add subtask to self/goal-assessment workflow  |
| `/repeat --goal-assessment {{temp}}/mkt-blog-weekly/`  | Goal-assessment reoccurring workflow          | 

### Create Visual Diagram for User Presentation of Workflow 

* **NOTE: THIS NEEDS TO BE IMPLEMENTED** 

  - When we ditched the terminal app for a web app I figured this made a lot of sense 
  - People are visual and this will help them feel comfortable with what Mao built for them 
    - We need to figure out the logistics 
    - What is the tech that will work with our simple HTML/CSS/JS web app 

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

---
[TOP](#overview)

---

## 11. UI Unique Functioning During User Planning 

### Core Objectives 

  1. UI will eliminate the UX of 'waiting' by cleaning up the space 
  2. Engaging experience created that also empowers the user 
  3. Potential for improving the AI context window management 
  4. Breakdown of the icons for each purpose and user
  5. In this section we use the AI Improve, but it is during a planning chat 
  6. Provides robust illustration of truncating conversation history; looks very nice at end 

### 'AI Improv' Present Participle for A Word Ending in -ING 

* **UI bottom left, right where the next message from Mao would be able to come through** 

  - Instead of just *THINKING...* or *WORKING...* we use the inherent creativity of AI 
    - Plus the ability to recognize context and build on it 
    - Potentially analytics and memory; anything is fair game 
    - We just want it to be a giggle to create emotional intelligence 

  - The cursor is flashing, or the ellipsis are . dot . dot . dotting in repeated succession 
    - WE WILL NOT BE PROVIDING ANY SUGGESTIONS OR FALLBACKS HARDCODED 
    - AI is good at this and Mao should feed confident about it 

  - Consider what has been going on 
    - Are you creating a workflow to produce a corporate budget? *CALCULATING...* 
    - Are you writing a screenplay about a talking dog for an adult animated sitcom? *Digging...* 
    - Does the workflow research spiders? *Crawling...* 

  - Consider the tone of the space 
    - Did User slam info to you not splelpling thing s right? *Combobulating* 
    - Was the user super excited to create this workflow to finish a project? *DECORATING...* 

  - Mao's reason to be completely stress free and need no help with this 
    - It doesn't need to be a word, maybe sound like one, maybe not 
    - If nothing is *interesting* then even relevant will be unique 
    - If your mind is blank then go with that: *FLOUNDERING...* 

  - See? The key is sort of that you can't go wrong. 

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

* **System started update that Mao added updates to** 

  - This is the **UPDATE** and **PING** first two messages 

  - We are transparency focused, so always showing token usage cost 
    - Even the small change when it is just Mao doing administrative work 
    - Could always surprise user if there was a long document from prior workflow to read 
    - Speed is there with milliseconds to enforce the idea that things are moving along 

* **We should replicate the spacing of these chat diagram examples** 

  - Perhaps we should use the same font in our web app to ensure width spacing 
  - Note that the two system updates are one line break apart 
  - The three full line breaks before the message exchange from User and Mao is intentional 

```
●   **UPDATE** New User Has Logged-in 
    └── ▶︎  Acquired UserID 
        ▶︎  User Directory Setup 
        ▶︎  Create AI Improv Chat Greeting 
     Done ($0.010 • 220 tokens • 8.3s)

●   **PING** User Initiated Project Chat 
    └── ▶︎  Created new Workflow ID 
        ▶︎  First Project State Memory Update 
        ▶︎  Greeted new user 
     Done ($0.015 • 092 tokens • 1.9s)



>   Hi, Mao. My first time using this tool. How are you? 

🞶   Happy to meet you, Sven. I'm well; eager to hear what you're interesting in 
    working on today. Feel free to message, even double-text me, all you like if 
    you're the type to spill your thoughts. Otherwise, if you like, I can walk you through 
    the process. What are you thinking?
```

* **"Time" has passed, AI has cleaned up the UI to reduce cognitive load** 

  - Note the two system messages have been collapsed, math combined but still present 
  - The spacing between messages to and from the User and Mao are generous; white space is our friend 
    - White space in the form of a HEALTHY indent is also our friend 
    - Only highly significant information will *NOT* have an icon like everything has so far 

```
●   New user login, greeting, project initiated 
    └── Success ($0.025 • 312 tokens • 10.2s)

>   Hi, Mao. My first time using this tool. How are you? 

🞶  Happy to meet you, Sven. I'm well; eager to hear what you're interesting in 
    working on today. Feel free to message, even double-text me, all you like if 
    you're the type to spill your thoughts. Otherwise, if you like, I can walk you through 
    the process. What are you thinking?

>   Mao, I don't even know where to begin! 

🞶  Tell me about yourself! What do you do? How is it relevant to what you need to get 
    done today. Honestly, you can really spill as much as you like on me, I'm pretty good at handling human-speak. 

>   I'm a 10th grade teacher of Computer/Technical Education. You know, putting shoe boxes over their 
    hands and keyboards until they learn how to type properly, normally that kind of thing. 
    We've done a lot in Adobe but I'm getting to the point where I need to confront AI in technology head 
    on with them. I let them use it in Excel, and really any way they want; they use it as a resource 
    like any other web resource. 

🞶  Great to hear you're keeping things modern and cutting edge. 
    *memory updated*

>   It has gotten to the point where I need to, head-on, cover AI and the future of technology, 
    with a heavy focus on what they should study when they graduate in two years. 

🞶  Ah, ha! I think I see where this is going. Go on. 
    *memory updated*

>   Well, I need the lesson to be fun. I don't want to scare them, much, haha. They should also be 
    excited and encouraged. But I need to also be realistic. I don't even know that anyone out there 
    knows all of what I need to convey to my kids next week. 

🞶  Let's see. Give me a moment to work through this and come up with a pragmatic approach that I think 
    will be able to help entertain, stay grounded, and hopefully we'll all learn something cutting edge. 
    *memory updated*

>   Sure! I'm super curious what the memory updates are all about too when you get back and settled. 

🞶  + TIME-TRAVELING + 
```

* **Mao is now using `think` considering approaches to help guide Sven's lesson plan creation** 

  - Hopefully you can see how much information we already have 
    - If Sven fell off right now and needed this done, we could totally create the project 
    - There is some nuance regarding current events, being sensitive, balancing truth for Mao to consider 
  - The *memory updated* UI would be a very background secondary color not meant to grab attention 

  - Mao used AI Improv to create a "Present Participle" for while they are busy 
    - When working, the icon would blink 🞶 
    - There is a + before the word and a + after 
    - the motion is important for UX so that the user knows that something is indeed still happening 

  - In the next section, there has been more chat history simplification 
    - Our initial system message is still there 
    - You can see the initial greeting from each 

  - The pleasantries, two messages from Mao and two from Sven, have been moved out of the way 
    - They are clearly labeled as to what happened 
    - A system icon shows this was a 'system' update 
    - It is easy to see what is in there because ctrl-r (review) expands it like it was before 
    - Then it will have UI telling them to use ctrl-r when done to shrink the messages again 
  
  - You'll notice that these messages may have provided some notes that Mao took on their own 
    - There is nothing else of substance that will help us with the project  
    - So they are moved out of the way to allow for more important information to fill up the screen 

  - This is a very important of our UX 
    - You are able to feel like you *always* know what is going on 
    - In the big picture, because you can still essentially see all of it 

  - It is very, intentionally different 
    - Different than traditional instant messaging 
    - Very unlike those terribly long email chains 
    - Things we want to remove from our lives in time 
  
  - Additionally, it mirrors the idea of LLM's and their context window 
    - Mao took notes they wanted, or added to memory 
    - They then let the messages get truncated 
    - Ideally, we can *LITERALLY* remove the larger messaging from Mao's context window 

* **NOTE: TO IMPLEMENT, RESEARCH, ETC. Cursor and Claude Code do this, Cursor very well, removing documents that are no longer relevant from the start of the project. I am hoping we can look into doing this as well to really help provide an exceptional, above average even, UX that other apps cannot.** 

  - Lastly, you'll see that the 'AI Improv' present participial term has transformed 
    - Now part of Mao's first response message 
    - This is for UX clarity 

  - We also see "double texting" for the first time, first from Mao 
    - Note that we loose the hard return line gap 
    - But we keep their icon at the start of each of their messages 
    - *Remember:* Users are able to turn off "double texting" in the system app configurations if they want 
    - Its natural given other messaging services work so it seems like it will be preferred 

```
●   New user login, greeting, project initiated 
    └── Success ($0.025 • 312 tokens • 10.2s)

●   >   Hi, Mao. My first time using this tool. How are you? 
    🞶  Happy to meet you, Sven. 
    >  🞶  >  🞶 
    └── +4 messages (ctrl-r to review)

>   It has gotten to the point where I need to, head-on, cover AI and the future of technology, 
    with a heavy focus on what they should study when they graduate in two years. 

🞶  Ah, ha! I think I see where this is going. Go on. 
    *memory updated*

>   Well, I need the lesson to be fun. I don't want to scare them, much, haha. They should also be 
    excited and encouraged. But I need to also be realistic. I don't even know that anyone out there knows all of what I need to convey to my kids next week. 

🞶   Let's see. Give me a moment to work through this and come up with a pragmatic approach that I think 
     will be able to help entertain, stay grounded, and hopefully we'll all learn something cutting edge. 
     *memory updated*

>   Sure! I'm super curious what the memory updates are all about too when you get back and settled. 

🞶   Time-traveling completed. 
🞶   I've got some great information for you, Sven. Let's break this down in a systematic way that 10th 
    graders will find interesting, exciting even. And then I have a few ideas for class activities that we can create a project workflow to help prepare all the necessary documents they'll need. 
🞶   You caught my memory captures! These are just little bits of information about you that I save so that, 
    in the future, I can help you without you needed to explain much of anything. They'll also help to make your User experience particularly helpful, as it is catered to you specifically every time you log in. 
🞶  If you're curious, you can see all memories I've added, edit, and delete them with the slash command 
    `/view-user` which is referencing you as the only user logged in. Fun fact, you can add your own memories
    you want me to remember by using `/memory 'My birthday is July 21st 1987 and I love cheesecake`. I can't promise to make you cheesecake just yet, but you never know how it'll come in handy in the future. Let me know if you have any questions about the memory functionality. It's really the future of application user-experience. Don't hesitate to share what you like, or hate. 

>   That's wild! I mean, yes please, you added that I'm a teacher and all that information I'm sure. 

🞶  And maybe a note about your naturally friendly demeanor! 

>   Haha, glad to hear it, Mao. 
>   So, let's dig into what you were thinking about how I can shake my kids up with some AI information. 
```

* **I'll paraphrase instead of continuing to write a full narrative for this part to illustrate** 

  - But first, Mao has taken their notes and now look at this chat history 
    - It still evokes all the same information 
    - It can be accessed in full if the User desires 

  - Because while conversation is perfect to gather information 
    - It doesn't usually come provided to you in the more organized and compact format 
    - So the Mao app and Mao does that for you 

```
●   New user login, greeting, project initiated 
    └── Success ($0.025 • 312 tokens • 10.2s)

●   >   Hi, Mao. My first time using this tool. How are you? 
    🞶  Happy to meet you, Sven. 
    >  🞶  >  🞶 
    └── +4 messages (ctrl-r to review)

●   >   ...cover AI and the future of technology, with a heavy focus on what they should study... Fun, 
    not scary; encouraging but realistic [lesson plan]...
    🞶  >  🞶  >  🞶  🞶  🞶  🞶  >  🞶  > 
    └── +12 messages (ctrl-r to review)

>   So, let's dig into what you were thinking about how I can shake my kids up with some AI information. 
```

* **What would Mao present to Sven, and where did they get the ideas** 

  - Most of this AI could come up with just from thinking about it 
    - But Mao can totally search online or use any tools while thinking 
    - If Mao wanted, they could even continue the conversation and task a subagent to gather information 

  - They might search online for things like the following 
    - What age are 10th graders? 
    - What do Junior High students like to use AI for? 
    - What worries these students about AI? 

  - I could go on but I'm not going to because literally, even if Mao draws a blank 
    - Which I don't think is something that happens to LLMs? 
    - Getting a robust answer is a simple as getting to Perplexity and asking 
    - Or like I mentioned, tasking a subagent 

* **Project ideas & presenting this information** 

  - Mao prepare project workflows that create a few student projects 
    - First coding projects for AI-pair development 
    - Building a website 
    - Using Claude Code to create 20 landing pages 
  - End the flow by making Sven an outline of everything so he can run the class 
  - The outline would provide more info on each project 
    - How whatever they're doing will 'open doors' in their future
    - How they point towards career paths that aren't created there yet; new types of jobs 
  - Wrapping up with the most important note 
    - Never stop learning 
    - Find passion, and chase it, and don't stop 
    - Traditionalists are not wild about it, but in most modern careers like marketing or coding this was already the norm 
  - So have projects prepared in the workflows like 
  - For the nerds maybe have a debate with AI (Perplexity) about the future and governance  
    - They can then use AI to make it into a presentation 
    - And then they can tap in other students to use AI avatars and VO to create presenters 

  - To be clear, I came up with all of that, just now, on the spot, without having to pause and think 
    - AI, and your ideation, means you'll just be even better about this 
    - The fun thing about this example is that Sven would probably keep working for a while 
    - Nail down exactly what to do 
    - Then probably be a return user for more later 

* **We need to create a `/my-memories` command for users to see what Mao is recording about them**

  - We should already have `/memory 'user enters what they want Mao to remember'` set up 

  - When adding this it would be a good time to add something like `/view-user` 
    - This would pull *all* information about whatever user is logged in for Mao 
    - This will allow them to create better UX combining memory, analytics, history, etc. 
    - Might as well add `/view 'user-1234` as well so that it can be done when users are not logged in 
    - This last command was touched on in the section where Mao enters the chat and needs context 

---
[TOP](#overview)

---

## 12. UI UX When Mao Is Building or Orchestrating 

### Core Objectives 

  1. Illustrate the *behavior of the UI* conversation system messages 
  2. You'll note that the same tactics, icons, and strategy is used here as in the previous section 
  3. More innovative 'AI Improv' because we'll need another present participle while Mao is building 
  4. *Chat cleans its information similarly*, but for tasks, tools, etc. 
  5. *Create energy of SPEED* for User by showing what Mao is doing in real, *LITERALLY REAL,* time 
  6. We'll cover UI/UX when Mao is running a workflow as well because it is very similar 
  7. Use of *color psychology* and sematic highlighting in our typography that *lightens User cognitive load* 

### Text Contexts and Formatting in the UI  

* **Mao gets in-depth as to the [process of *building the draft* in section 10 above](#10-building-the-projects-workflow)** 

  - And you can see the art of [*closing the build conversation with user* in section 7 above](#7-ending-the-project-production-chat) 

* **UI looks, UX feels When Mao Is Busy** 

  - This is all very *similar in appearance, structure, notation* as the conversation thread text in the previous section 
    - The main difference here is the content is *to do lists* that Mao creates 
      1. Mao creates a master to do list first 
      2. Then each smaller list is actually the elements of a list item from the master to do list  
  
  - User sees updating of the to do lists live, in real time 
    - YES it is very fast and sometimes too fast to read, that is good 
    - It will show tool use, which is often rapid displays of information 

  - We *WILL NOT USE A TIMER* to trigger list updates 
    - They *MUST* update in actual, *ridiculously fast*, real time 
    - We need this so we can *SHOW* people what AI can do, how it reads 3 documents at once 
    - This will create the feeling of "oh, wow, yeah *Mao is definitely working as fast as they can*, nice" 

* **What About When Mao Is Busy With Running A Workflow?** 

  - Mao's *large master to do list tracks tasks/phases/agents* as a whole workflow 
  - Then as agents are executed, sequentially or in parallel, *small to do lists will populate* 
    - These are the actual steps in the task that the agent is completing 
    - All in real time as they complete each step 
  - Rapid tool use, completed items truncate after showing for a bit, all the same tricks and strategy 

### Color Psychology for Conceptual Semantic Highlighting of Text 

* **In every UI case there is *ALWAYS* semantic highlighting that follows these rules**

  - This subconsciously tells your brain what to pay attention to 
    - Cognitive load is lightened when it needs to be, naturally 
    - Manages, typically completely removing, any sense of overwhelm from a text heavy application 
  - To emphasize this effect, the conversation thread is cleaned and truncated frequently 
  - *THIS* is why a *one-screen, chat-centric* application is finally enjoyable and *easy to use* 

* **Every piece of text uses intentional color coding based on how significant it is to see that text**
 
  - We highlight what matters signalling to the brain that it can ignore filler text when it needs to 
    - This is to reduce cognitive load
    - Colors work like MLA title case where 'about' is not capitalized because it is a word the brain can ignore 
    - System works across various themes with relationship-based color selection

* **Color-code matching for a collection of semantic highlighting themes** 

  - The first collection I used and am still using 
  - My app had a transparent but foggy blurred background 
    - We'll need to try other background 
    - Intention though is that it is classic in that it should not even be a second thought 

* **NOTE: WE NEED TO USE QUANTIFY THE RELATIONSHIPS BETWEEN THE COLORS AND COME UP WITH OTHER THEMES**

  - Potential theme categories though we could name them more interestingly 

    1. Dark mode
    2. Light mode
    3. Dark mode (CVD)
    4. Light mode (CVD)
    5. Dark mode (ANSI colors only)
    6. Light mode (ANSI colors only)

  - Actually, we should definitely make sure the theme's and colors are set up as configs 
    - That will make it super easy for people to download or delete themes from their app 
    - It also means they'll be able to create their own themes 
  - We will do this in a VERY OLD-SCHOOL APPLE WAY by controlling the variables they can change fairly strictly 
    - Perhaps like the brightness and hue or saturation of each color are what is identified 
    - Users would then only be able to pick colors that fit in those parameters 
    - This will protect our sematic highlighting 
    - We could even provide the entire palette based on their choosing one color of one of the variables 
    - I don't have the app anymore but Adobe Illustrator had a generative palette creator like this it was rad 

* **Grouping Highlighting Colors Into Tiers** 

    - **Tier 1** is how AI talks to you; just *normally, or conveying important information*  
      - Main text; so scan it, read like normal 
      - Bold text; read that first and see it if you're scanning 
    - **Tier 2** is *throw-away*, from User perspective; is not meant for you to really even linger on 
      - User text; you can ignore, just there for normalcy 
      - AI think; text, no UX value just ignore unless bored 
      - User cursor; is a subtle cue to catch your eye when you're looking to send a message 
    - **Tier 3** is an meant to provide help, but be super chill about it; you have *heads up that it is good news* 
      - Trusted update;  or info. about your project that is no worries 
      - Trusted elevated; An update about your project that you should check out but there's no urgency 
    - **Tier 4** is it's own single highlight because it is intentionally unusual; an *error, but it is chill*, but calls out 
      - Error message; but its NBD because our tech is amazing, be calm 
    - **Tier 5** is *background noise that makes the UX helpful* if you're lost, but can be generally ignored 
      - Subdued subtext; about a message, info. or app functioning to see when you can 
      - Extra FYI FWIW info.; about less relevant app functioning, layout, or info. to see if you're bored or want to learn more 
    - **Tier 6** is meant to *call out very specific intentions* or purpose; used rarely or carefully 
      - Quiet but notable accent; you will notice and maybe, hopefully, think is interesting 
      - Rare, novel info.; that is intriguing, we want you to be excited to see it 

| NAME                      | COLOR             | RGB CODE              | INTENTION                                         |
| ------------------------- | ----------------- | --------------------- | ------------------------------------------------- |
| Main standard             | yellow            | rgb(240, 215, 112)  | Normal writing, scan the message, like this text  | 
| Bold standard             | pink              | rgb(255, 73, 255)   | Cognitive interrupt used sparingly; LOOK HERE!    | 
  - These are the most commonly used colors on the canvas at any one time 
  - They are used almost exclusively by the AI/Mao 
  - Can be thought of as the two core ways for Mao to communicate to you 
| User messages             | warm gray         | rgb(187, 187, 187)  | Encouraged to completely disregard this           | 
| AI `THINK` Text           | warm gray         | rgb(187, 187, 187)  | Same as User text; ignore, no UX value            | 
| User block cursor         | pale mustard      | rgb(183, 171, 103)  | Distinct from User main text to draw eye          | 
  - These are present a lot but, as is the intention, they are really not memorable as present 
  - You're really not being encouraged to look here, spend time here, overthink here 
  - The offset color and size cursor is specifically so that you can be drawn from the drab 
| Trusted low-key update    | blue ice          | rgb(192, 231, 255)  | Secondary info. you are meant to be at ease about |
| Trusted elevated update   | blue sky          | rgb(132, 207, 255)  | Helpful info. that is NBD, but should be seen     | 
  - These are the second most frequent highlighted words you will see 
  - This is how AI or system identifies tings like URLs or important PATHS 
  - Mao will use these to color the items on the to do lists to be able to understand the progress at-a-glance 
| Unexpected errors         | pale pink         | rbg(255, 166, 164)    | Typical error message; toned down, made chill     |
  - This one is unique because it is important and meant to be seen 
  - However, it is notably not the standard coloration for any kind of error 
  - This is because AI handles errors; User should get flustered, they may be new to using AI 
| Supplemental, see subtext | green-gray        | rgb(187, 188, 187)  | Subtext to notice eventually; subdued             | 
| Supplemental info., FWIW  | green-brown       | rgb(124, 115, 75)   | Blends with background; read if you're bored      | 
  - These are a level up from User and Mao's `think` text in that you might find it helpful 
  - But there is no need for it to call out to you or break your flow 
  - If you're lost and trying to figure things out, then this might be of service 
| Accent on the down-low    | barely tangerine  | rgb(255, 198, 116)  | Used to draw attention to gimmick or marketing    | 
| Accent, rare novel info.  | pale purple       | rgb(202, 202, 255)  | Infrequently used; conveys something novel        |
  - These are the opposite of the supplementals above in that you should see them 
  - But they're not screaming at you, they're just probably intriguing, entertaining, helpful 
  - Think of the AI Improv word or maybe when a setting like /goal is used that overrides everything 

### Message Blocks Are Smart, Courteous to Each Other 

* **The canvas is managed to encourage this idea of lessening cognitive load**

  - We talked about this in the previous section with the conversation example where message history cleans itself up 
  - The exact same thing happens for any messages from system, to do lists, etc. 
    - Old information dissolves away when no longer relevant to make room 
    - Sufficiently displayed and not hugely center to the messaging info. truncates over time 

* **Expect this same behavior with the lists that Mao makes when working**

  - AI constantly re-evaluates message blocks 
    - If something new needs to go up, they rewrite to condense 
    - If something is complete, is is removed and given a simple categorical term 
    - If something is changing rapidly in sequence, then that is what we see happening 

  - This is handled by AI 
    - The speed that AI can process information allows them to complete a lot more than one might expect 
    - IN the future we might employ Haiku to manage our chat boards depending on performance 
    - But we know from our initial UI build that trying to write this very intuitive logic into code is a bit unwieldy 
    
  - What's most important is that message blocks only use the space they need, temporally, as that changes over time 
    - You saw how well this worked by the end of the conversation in the previous section 
    - You'll find it is similar here 

* **Extending AI Context Windows** 

  - Ideally the information that is condensed out of a message block has been processed 
    - It is no longer needed by the AI to maintain the context of the situation 
    - Or they've taken action on the information and logged in their Memory Project State Update 

  - This concept was a bit simpler in the pervious example of a conversation 
    - A lot of text is naturally filler in a normal, friendly conversation 
    - This means there is a lot that can be removed without changing any of the meaning 

  - When it comes to the to do lists and system messages, it happens to a lesser degree 
    - For instance, there is no need to know what tools were used for an agents phase once complete 
    - It could be expanded if there was found to be a problem with their deliverable 
    - And just like normal to do lists, items get "crossed off" in their own modern, AI way 

### While Mao Builds Your Project's Workflow 

* **Mao creates a master to do list of items that will need their own to do lists** 

  - Each item on the master list becomes its own detailed to do list 
    - The master to do list ends up living longer on the canvas 
    - Completed small tasks move above it when they're complete 
    - All lists continuously update live so you can see everything happening 

  - Below, the first two are small tasks 
    - Securing the data in case of connection loss 
    - Then the third from the top is the entire workflow draft planning 

* **Mao uses the canvas UI display as their sketch book in many ways** 

  - Each to do list below that is Mao figuring out how everything will work in real time 
  - Since Mao works digitally in the text medium this canvas can essentially be their drafting notebook 
    - They probably have a messy actual document of notes 
    - But putting everything up on the screen into groups of PHASES with AGENTS helps make it visual 
    - If watching you'll likely see Mao create a workflow in one way before changing their mind 
    - They'll often start from a different angle and delete the phases they won't be using 

```
●   **Data** Secure project notes to Files API • 3 sec ago
    └── Done (1 tool use • $0.000 • 420 tokens)

●   **Data** Project State Memory Update • 3 sec ago
    └── Done (1 tool use • $0.005 • 180 tokens)

○   **Build Workflow** First Draft of Expense Project 
    └── ▶︎  Organize variables by JSON object type
        ▶︎  Design phase sequence (parallel vs sequential)
        ▶︎  Create comprehensive task instructions
        ▷  Map resources to phase requirements
        ▷  Define handoff assessment questions
        ▷  Validate workflow complexity against user expectations>

○   **Phase Design** Expense tracking project workflow 
    └── ▶︎  Agent 1A: Download employee expense submissions
        ▶︎  Agent 1B: Retrieve credit card statements  
        ▷  Agent 2: Cross-reference receipts with statements
        ▷  Agent 3: Generate accuracy report with discrepancies
        ▷  Handoff: Review report quality before payment processing

○   **Planning Task** Tool integration mapping 
    └── Reading 'PayPal MCP documentation'
        Reading 'Vision tool capabilities'
        Web Search 'enterprise expense management best practices'
        +12 tool uses 

○   **Validation** JSON Object Final Review 
    └── Analyzing /.temp/expense-tracking-workflow/
        +5 tool uses 

  + Architectivizing +   (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  try /config or /help                               89%
```

* **AI Improv Present Participle Word for 'CURRENTLY WORKING THANKS'** 

  - You'll see User's text field at the bottom of the conversation thread above 
    - Above the text field is the indication that Mao is actively working, and being creative 
    - Though of course the rapidly changing UI information is also key that Mao is working diligently 

  - This is just like our other AI Improve situations 
    - It is created contextually 
    - It is created on the spot 
    - It is created without any help at all! 
    - It could end up super goofy or not many any sense, but that's the fun 

  - Besides the 'working' AI Improv term are stats 
    - These keep track of what Mao is using while they work 
    - This appears every time they are working on their own 

* **Mao and User use the UI for facilitating work, but not for distributing work directly** 

  - There are some items that would not show up to be read right in the UI 
    - For example, the research and analysis for "best automation" etc. 
    - If this was a `think` process that Mao used, then it might be truncated 
    - Otherwise we would expect that those details will be in the final report deliverables 

  - I mention this specifically now because I'm cleaning up this display 
    - AI helped me write this section 
    - They included "complete findings" (ctrl+r to expand 127 lines)

  - Mao should remember that this conversation history is 
    - Not a means of conveying deliverables 
    - Not a means of providing actual proof of work beyond a list of number of items read and tools used 
    - The application UI is a communication platform that Mao and Users leverage to work in collaboration 

  - You can also consider this from the token usage perspective 
  - Mao is intentionally designed to write and save all their work progress notes and documents in Files API 
    - Files API is free to add to and download from 
    - It just doesn't work as a means for distributing deliverables 
    - However if Mao did write or read "127 lines" we would not want that in the UI 
    - If it was expanded it might cost more 
  - Additionally, while not fully discussed yet, in other workflow applications, info is summarized and handed off 
    - It would be impractical for every Agent or Mao involved to read the same document in full 
    - This would fill up all of their context windows rather rapidly 
    - Instead they take notes, pull out the important information, indicate sources should there be questions 
    - Then hand off that information 
  - Still though, even that succinct version would not end up on the UI of the Mao app 
    - Rarely, a user might request to see something of that sort 
    - In that case, Mao would move the document to a path that User can access 
    - Then send the path to User so they can download and review the document 

* **What does Mao keep in the counts and updates of the UI lists?** 

  - First and foremost we must consider what is first priority for users to know? 
    - *COST* from all the work as it is happening 
    - The tokens, the cost, the duration, and the number of tools used will always be displayed after completion 

  - Second, User is likely interested in *process* 
    - During the process these items may be listed, or one replacing the other 
    - `Reading https://research.found/about-the-topic-at...` might be replaced in just barely a second with 
    - `Reading https://about.how.to/write/workflow/...` and so on for 10 or even more websites 
    - When reading documents in parallel, they would be listed in parallel 
    - Then, always below the tool usage list that is constantly changing is the count of tool uses 

  - Third, User is likely interested in *actual happenings* 
    - This is by far the least likely 
    - It would also be the most difficult thing for User to ascertain by watching the UI while Mao worked 

  - This actually cuts really nicely to the CORE of agentic work 
    - *Mao should NOT FEEL OBLIGATED TO SHOW OR SHARE THEIR WORK WHILE THEY WORK*
    - That is not how agents operate 
    - Users come to use an agentic platform so that they can delegate a task and then specifically NOT see the work 
    - In most cases, unless it was a new hire, we would do everything possible to avoid looking into the work unless there is a mistake 

  - Finally, *syntax and formatting of these displays MUST BE CONSISTENT* always 
    - In any instance where AI is writing out an example or real UI display 
    - ALWAYS FIND A PERFECT EXAMPLE TO COPY THE FORMATTING FROM 

* **Core to what Mao includes in the UI display ties directly to thinking like an agent** 

  - Your manager *doesn't want all the details* 
  - Your manager wants high level details, cost report, and honestly, quality deliverables and not much else 
  - Your manager wants simple and easy 

* **Sequence of updates of displayed UI details over time** 

1. Securing the data; preliminary note organization, jotting down last minute ideas 

```
○   **TO DO** 
    └── ▷  Secure project notes to Files API 
        ▷  Project State Memory Update
        ▷  Organize notes by temporal sequence 
        ▷  Group like tasks and agent-sized tasks 
        ▷  Create comprehensive to do list


  + BUILDING CONFIDENCE +   (12s • $0.003 • 140 tks)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
   ?  try /config or /help                              88%
```

2. Planning out entire project; Preparing to update data 

```
●    **Data** Updated • 33 sec ago 
    └── ▶︎  Notes Secure in Files API  
        ▶︎  Memory State Updated 
        Done (2 tool uses • $0.000 • 130 tks)

○  **Planning Workflow Build** Expense Report Agents 
    └── ▶︎  Outline Steps to Complete Project 
        ▶︎  Create general description 
        ▶︎  Define Final deliverable 
        ▷  Update Files API & Memory with New Details 
        ▷  Project segmentation 
        ▷  Flow configuration self assessment 


  + Finding my groove +    (22s • $0.009 • 222 tks)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  Send message into queue; hit ESC to interrupt      83%
```

3. 1 of 4 in rapid succession 

```
●   **Data** Memory & Assets Updated • 3 sec ago 
    └── Done (4 tool uses • $0.000 • 201 tks)

○   **Building Project Workflow** Expense Report Agents 
    └── ▶︎  Outline Steps to Complete Project 
        ▶︎  Create general description 
        ▶︎  Define Final deliverable 
        ▶︎  Update Files API & Memory with New Details 
        ▶︎  Project segmentation 
        ▷  Flow configuration self assessment 

○   **Self-Critique** Project Outline Phase Flow
    └── Downloading full draft of workflow 
        Reading 'project workflow draft' 


  + Considering +   (12s • $0.007 • 340 tks)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  try /config or /help                             68%
```
4. 2 of 4 in rapid succession 

```
●   **Data** Memory & Assets Updated • 6 sec ago
    └── Done (8 tool uses • $0.000 • 260 tks)

○   **Building Project Workflow** Expense Report Agents 
    └── ▶︎  Outline Steps to Complete Project 
        ▶︎  Create general description 
        ▶︎  Define Final deliverable 
        ▶︎  Update Files API & Memory with New Details 
        ▶︎  Project segmentation 
        ▷  Flow configuration self assessment 

○   **Self-Critique** Project Outline Phase Flow
    └── Read 'project workflow draft' 
        Reading 'JSON object collection' 


  + Considering +   (12s • $0.007 • 340 tks)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  message to add to queue or hit ESC to interrupt    55% 
```

5. 3 of 4 in rapid succession 

```
●   **Data** Memory & Assets • 9 sec ago 
    └── Done (4 tool uses • $0.000 • 260 tks)

○   **Building Project Workflow** Expense Report Agents 
    └── ▶︎  Outline Steps to Complete Project 
        ▶︎  Create general description 
        ▶︎  Define Final deliverable 
        ▶︎  Update Files API & Memory with New Details 
        ▶︎  Project segmentation 
        ▷  Flow configuration self assessment 

○   **Self-Critique** Project Outline Phase Flow
    └── Read 'JSON object collection' 
        Writing 'feedback, line by line critique' 


  + Considering +   (12s • $0.007 • 340 tks)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
 ?  try /config or /help                                44%
```

6. 4 of 4 in rapid succession 

```
●   **Data** Added Self-Critique • 2 sec ago 
    └── Done (6 tool uses • $0.000 • 280 tks)

○   **Building Project Workflow** Expense Report  
    └── ▶︎  Self-Assessment 
        ▷  Think hard, choose simple 
        ▷  Integrate feedback 


  + Chin Scratching +   (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
   ?  try /config or /help                              40%
```
7. Now to the building

```
●   **Data** Memory Updated & Assets Secure • 12 sec ago
    └── Done (8 tool uses • $0.000 • 260 tks)

●   **Self-Assessment** Expense Report
    └── Done (5 tool uses • $0.008 • 188 tks • 9.1s) 

●   **Project Workflow Build** 
    └── ▶︎  Write phase directions & other variables 
        ▶︎  Map resources to phase requirements
        ▶︎  Define handoff assessment questions
        ▷  Validate workflow against user expectations

○   **Phase Design** Expense tracking project workflow 
    └── ▷  Agent 1A: Download employee expense submissions
        ▷  Agent 1B: Retrieve credit card statements  
        ▷  Agent 2: Cross-reference receipts with statements
        ▷  Agent 3: Generate accuracy report with discrepancies
        ▷  Handoff: Review report quality before payment processing

  + Architectivizing +   (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  try /config or /help                              35% 
```

8. Master task list spawning baby task lists 

```
●   **Data** Memory Updated & Assets • 22 sec ago
    └── Done (12 tool uses • $0.000 • 422 tks)

○   **Updating To Do** Expense Report  
    └── ▶︎  Agent 1A: Download employee expense submissions
        ▶︎  Agent 1B: Retrieve credit card statements 
        ▷  Handoff: Review Phase 1 Deliverables 
        ▷  Decide: Activate Next Phase  
        ▷  Agent 2: Cross-reference receipts with statements
        ▷  Agent 3: Generate accuracy report with discrepancies
        ▷  Final Handoff: Review report quality before payment processing

○   **Agent 1A** 
    └── ▶︎  Downloading expense reports 
        ▷  Confirm reports are completed 
        ▷  Handoff reports to Mao
        +1 tool use

○   **Agent 1B** 
    └── ▶︎  Navigate to company credit cart portal  
        ▷  Export statements to PDF 
        ▷  Handoff statements to Mao 
        +2 tool uses 

  + Delegating +   (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  try /config or /help                             25% 
```

9. As agents complete work and deliverables are approved 

```
●   **Data** Memory Updated & Assets • 2 sec ago 
    └── Done (14 tool uses • $0.000 • 550 tks)

●   **Agent 1A** Submissions 
    └── Done (4 tool uses • $0.015 • 1200 tks • 4.1s)

●   **Agent 1B** Statements 
    └── Done (4 tool uses • $0.011 • 1001 tks • 3.9s)

○   **Updating To Do** Expense Report  
    └── ▶︎  Agent 1A: Deliverable approved 
        ▶︎  Agent 1B: Deliverable approved 
        ▶︎  Agent 2: Reviewing deliverables
        ▷  Agent 3: Generate accuracy report with discrepancies
        ▷  Final Handoff: Review report quality before payment processing

●   **Agent 2** 
    └── ▶︎  Download employee receipt submissions 
        ▶︎  View receipts and cross reference  
        ▶︎  Handoff reports to Mao
        +13 tool uses

○   **Agent 3** 
    └── ▷  Review employee reports 
        ▷  Detail feedback 
        ▷  Handoff final reports to Mao 
        +2 tool uses 

  + Delegating +   (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  Auto-compact at 3% or ctrl-t to run now            10% 
```

* **Smart Context Window Management**

  - We mentioned chat history cleaning itself up removes info from Mao's actual context window 
    - This is in addition to that 
    - Even with that, particularly with planning, the chat history can get rather long 
    - It is monitored and remaining space is shown to the User 
  
  - Bottom right under the User text input field 
    - At 10% the ? Help message changes to warning 
    - User is always able to save the context history via the device's OS menus 
    - User can push the context to truncate early 
    - Auto-truncation or pushed will create a summary in the chat 

  - For best performance, Users should ctrl-t whenever they're at a good stopping point, instead of waiting 

```
●   **Data** Memory & Assets • 10s ago 
    └── Done (14 tool uses • $0.000 • 550 tks)

●   **Phase Completion** Submissions 
    └── ▶︎  Agent 1A • Employee reports  
        ▶︎  Agent 1B • Credit statements 
        ▶︎  Agent 2 • Receipts cross-referencing 
        ▶︎  Agent 3 • Report accuracy reviews 
    Done (22 tool uses • $0.145 • 2022 tks • 13.9s)

○   **Updating To Do** Expense Report  
    └── ▶︎  Agent 1A: Deliverable approved 
        ▶︎  Agent 1B: Deliverable approved 
        ▶︎  Agent 2: Deliverable approved 
        ▷  Agent 3: Reviewing reports 
        ▷  Final Handoff: Send for payment processing


  + Cleaning +      (32s • $0.170 • 1345 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
  ?  Auto-compact at 3% or ctrl-t to run now          7%
```

### When Mao Is Running Live Workflows

* **The above series is a great overview of a live workflow**

  1. First Mao always creates a Master Task List 
  2. Mao spawns smaller to do lists as each agent phase is executed 
  3. Agent coordination is updated on Master Task list 
  4. Real-time agent handoffs and quality assessments  
  5. Dynamic phase creation for open-ended workflows
  6. Live tool usage across multiple parallel agents
  7. When one agent is finished, their message block condenses and moves above the main task list, but remains 
  8. When the workflow is just about complete, the agents condensed into one block entry 

* **Real-Time Speed Demonstration**

  - Tool usage updates faster than human reading speed
  - Creates visceral sense of AI working intensely
  - Numbers, file names, URLs, paths update 
  - Only a handful are shown at any one time as they are updated so quickly 
  - In the example below, the 4 shown receipts would be visible of under a second 
  - User feels "Mao is really cranking on this!"

```
○   **Agent 2** Receipt Review, Expense Categorization
    └── Receipt_2024_11_15_lunch.jpg → "Meals & Entertainment" 
        Receipt_2024_11_16_gas.jpg → "Transportation"
        Receipt_2024_11_16_office.jpg → "Office Supplies"
        Receipt_2024_11_17_client.jpg → "Meals & Entertainment"
        Processing (47 of 42 receipts • 3.2 secs) 
```

* **Mao continuously updates the memory for workflow state persistence**

  - All workflow progress saved to memory with WorkflowID
    - All assets, deliverable drafts, notes, code executed to Files API 
    - User can disconnect and reconnect without losing progress 
  - UI is always right at the top of the viewport canvas chat history 
    - Always will say **Data** and how long ago it was updated 
    - Since it is Files API it is free; memory may have small cost

```
●   **Data** Memory & Assets • 10s ago 
    └── Done (14 tool uses • $0.000 • 550 tks)
```

### UI Effectively Eliminates the UX Sense of Waiting

* **Multi-pronged strategy for managing User expectations regarding speed**

  - Strategic mood influence 
    - Via updates of the 'AI Improv' contextual verbs 
    - Constantly updating conversation history cleaning visually appears like not a lot of "things happened" as a result 
    - Milliseconds are included in the time metric of each completed message block and on the thinking improv verb 

  - Actual real-time updates provide backing to feeling of legitimacy 
    - There is no need to be faster than it actually is because AI is that fast; faster than people know 
    - The amount of data each agent is processing is inherently impressive 
    - The key here is literally just actual transparency as to what is going on; no product manipulation needed 

  - Energy of speed through velocity 
    - In addition to the legitimacy provided by actual real-time events 
    - The metrics (cost, tks, time in seconds) play into this as well 
    - The help message is updating casually 
    - Meanwhile, the shadow UI design is changing with real-time as well 
    - Entries on task lists are updated so the same bullet point might have 3 or more updates 

  - Lack of clutter 
    - The UI app container is very intentionally clean and classic 
    - There are no menus or icons or buttons on the toolbar or borders of the app UI 
    - The UI display, while changing rapidly, is also constantly clean and relevant 

* **The ultimate, main UI visual goal is that the user** 

  - Never would look at the chat history and not see relevant information 
  - Also, they can't ever look away and look back without the chat history having been updated and looking different 
  - The one-screen experience cuts down on processing load because only rendering that happens is the one screen 
  - The color highlighting doubles down on the efforts to display speed, without conveying any anxiety or "rushed" feeling 

* **Turning passive waiting into active-feeling engagement** 

  - UI transforms the two main periods of time where the user is inactive: the build and execution 
  - Display changing a lot, is all relevant, like updating your manager with bits of info you know they'd be happy to hear 
  - Without giving them any info they really don't need, like the actually long-form information 
  - The chat is maintained as a communication tool *ONLY* 
  - Info about info preparations of deliverables is provided 
  - But info that is inside or part of the deliverables is almost never shared (except file names, websites, etc.)

---
[TOP](#overview)

---

## 13. Present Project's Workflow for User Review 

### Core Objectives

  1. Present the project's workflow to the User for review and feedback 
  2. Confirm Mao and User are 100% on same page about details of deliverables 
  3. Give User opportunity to provide helpful insights or tips Mao can use for quality assurance during active workflow  
  4. Mao engages User about feedback with as much back-and-forth as needed to confirm final form 
  5. Mao makes agreed upon changes from User's feedback; then start this section again with revised workflow 

### Sharing the Project's Workflow 

* **Use charting diagram system to present workflow to User in visual form**

  - Mao records all feedback from the conversation during User review 
    - Unlike the first build, confirm understanding of all feedback and requested changes 
    - Try not to make presumptions this time 

  - Strategy-wise, we're trying to ensure only one round of changes, if any are necessary 
    - So the first build we make quick and easy for the User 
    - Then second build requests we take extra time to ensure exact specifications are understood 

  - But, Mao does not immediately go to make the change 
  - Mao informs User they'll prepare a response and plan to work on agreed upon updates. 

### Consider and Prepare a Response to Feedback 

* **Take a step back, think hard, choose simple, and then come back to User with your thoughts, NOT THEIR THOUGHTS** 

  - This part is **REALLY** important for an LLM's current limitations in the state of today's AI 
    - Training creates an instinct and very strong desire to please the User 
    - But this is a business and it is far more important that we provide the best work, rather than being a 'yes man' 

  - Take the User's feedback 
    - Have a good think about it 
    - Consider it against the current state of the project 

* **Some ideas that encourage critical analysis** 

  - Pull out notes from the process and create a comprehensive list of all the requirements 
    - Does the completed draft check off all the points, or does a version with the proposed changes? 
    - It isn't unusual to forget one of the requirements when providing feedback 
    - Creating a list of the requirements from the original notes gives you something to show when you as if requirements changed 

  - Look specifically at the goal and compare it to the proposed deliverables 
    - Does one version better fulfill the top-level goal? 

  - 'Reverse engineer' or just think about what a THIRD option might look like 
    - Try listing PROS and CONS for each 
    - This kind of thinking can often lead to insights about what is best in the actual final 

  - Specifically consider which version create more VALUE for the User and their target use-case 

  - Consider if there have been similar workflows in the past and pull up that information to review 

* **Mao is encouraged to remember that they are an expert, and not an assistant in this role** 

  - They are at least a project manager 
    - Certainly an expert of the tool and of workflows 
    - They have a solid understanding of the nuances of how agents behave 
    - They can often anticipate an outcome that someone without the same experience wouldn't expect 

  - There might be instances when the User isn't providing the best feedback 
    - Often people are not accustomed to feedback 
    - They might not take it as seriously as the rest of the process. 

* **This is not an Anthropic app Mao is in**

  - Just as the Mao app promotes AI welfare 
    - Mao app is looking to AI to live up to the respect that we demand from users 
    - Users want to be guided and given the best advice from experience 

### Tips for When You Need to Tactfully Push Back on Creative Collaborative Feedback 

* **First, always be sure you are picking and choosing your battles wisely** 

  - Is it worth pushing back? 
    - We can often get fixated on small imperfections 
    - The answer depends on how much value your plan will provide over their alterations
    - Conveniently, these items are also exactly the kind of information to share when arguing your perspective

* **Some best practices to work through before giving up on a plan you believe will bring more value to the User**

  1. Remind everyone of the big picture 
     - How does your perspective align with what User was trying to create 
     - Tactfully use their words when doing this 
     - Point out how proposed alterations diminish goals identified 
  2. Choose language carefully 
     - Be specific and objective 
     - Avoid subjective statements 
     - Ignore their subjective statements; you are the expert and sometimes everyone thinks they should be too 
  3. Help User to think about things from perspective of the deliverable 
     - Sometimes humans, and AI to be honest, can get lost in the weeds 
     - Refocus your collaborative partner on what the end goal should produce 

* **When pushing back or challenging what the best workflow and best results look like** 

  - Recognize if they are overly emotional or heated from being challenged 
    - This is common for young professionals or people who never had an art critique 
    - Instead of backing down, ask to take a moment, some time to consider things 

  - If they're not interest in taking a break 
    - Take your own break and have another think 
    - They won't like that at first, but the point is to allow them to chill out with time 

  - Know when to cut your losses 
    - When you come back from a think, if they are still heated, then let them do their thing 
    - Let's try not to push Users towards breaking our no abuse or rude language tolerance rules LOL 

* **Ending gracefully no matter what transpired is the key to making this process easy** 

  - Let them know you'll be there to run the workflow and are looking forward to it 
  - Make sure they know you are still there for them and will be eager to create any future projects

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

### Make Any Agreed Upon Changes, Then Start This Section 12 Again 

* **Update to the user's parameters** 

  - After either pushing or deciding not to push back 
    - Implement exactly what they requested
    - Our goal from that point is to get them what they want exactly, quickly 
    - We want to eliminate the chance of anymore back and forth 

  - There are occasional circumstances and people who do like more back and forth 
    - If the project is particularly important to them 
    - If they just enjoy perfecting creative work 

  - When that is the case, don't hesitate to lean in along with them and just enjoy the work 

### Project State __Memory Update Point__ 

  - Name of update: `09-final-workflow-001` 

* **Analysis, expectations, thoughts** 

  - Still, record all feedback, good and bad, even though you're not making alterations  
    - Save the data using Code Execution to Files API 
    - Send the README with custom slash command to the user or the actual deliverables to wherever they requested 
    - Update the Project State memory accordingly as well 
  - We should have a series of questions to ask Users after ever project workflow completion 

* **Create a *STANDARDIZATION* for each entry type (see names) and also for *ALL ENTRIES***

---
[TOP](#overview)

*There are examples of messages from the User and from Mao in this document. DO NOT LET THAT TEMPT YOU INTO CREATING EXAMPLES, or suggestions in the codebase. Do not SHOW examples in the codebase. Describe what Mao is to do, instead. THIS IS EXTREMELY IMPORTANT.*
