# Flow of Data Through Mao 

---

1. [**User login, setup,** creation of user files](#1-user-login)
2. [**UI design**, high-level, and philosophy](#2-the-look--feel-of-the-mao-app-high-level-design-requirements)
3. [User initiates chat; **slash command responses like /goal**](#3-main-app-screen-chat-loads)
4. [**Mao preps**, sends response message to User](#4-mao-prepares-for-initiated-project-chat)
5. [Behavior protocol; **psychological guidelines**](#5-chat-behavior--psychology)
6. [Review of our JSON workflow types; **variables & validation methods**](#6-review-of-workflow-json-objects--variables)
7. [Telling User **Mao is off to build** the workflow](#7-ending-the-project-production-chat)
8. [Review of advanced agentic workflows; **Mao's best practices**](#8-reviewing-advanced-workflow-best-practices)
9. [**Building workflow, securing data,** reviews, diagram creation](#9-building-the-projects-workflow)
10. [Long example of conversation; **robust UI visuals, UX descriptions**](#10-ui-unique-functioning-during-user-planning)
11. [UI while **Mao is building or Orchestrating**](#11-ui-ux-while-mao-builds--orchestrates)
12. [Getting **user feedback** & finalizing the workflow](#12-present-project-workflow-for-user-review)

---

## Overview 

Discovery of code labeled 'mock data' uncovered hardcoded category suggestions; clean-up revealed it to be woven through core logic. AI wasn't able to fully explain the logic of the current code. Considering Mao's primary task requires nothing beyond current AI abilities, it is now clear we over-engineered. We NEED that level of understanding, period. As my first project of this size, I now understand I need to make a better point to read *every* file's code sooner. 

This document outlines the flow of data and all operations, end to end. Using it as a guide, we will have a 'logic audit', working through all current files to clean up, optimize, and simplify orchestration leaving us with codebase that reflects the simple logic of Mao's chat-oriented task. Where needed, this will allow me to illustrate how to provide guidance without hardcoding a single suggestion that could prove detrimental to the application when we build out the multilingual capabilities. 

### Summary 

Outline comprehensive data flow to understand necessary logic, then use the outline to audit the current codebase logic. 

### Goal 

While auditing we will implement remaining functionality needed to launch the application as a development-focused terminal app for testing. After which we will be able to develop a web UI to launch Mao publicly. 

### Opportunistic Outlook 

* **Consider all of the files through the lens of launching as a multilingual application** 
  - Ensure we are fully developing capabilities in parallel 

* **Look at all files through the lens of creating a Web UI** 
  - As it stands now, everything is written for our originally planned Terminal application 
  - We should explore the possibility of offering both web and optional local download; what are implications for timeline and complexity? 

* **Cement in new, more marketing focused, clearer-from-the-big-picture application terminology** 
  - We cannot call what User's come into the app to do a "Workflow" 
  - It is limiting; summons ideas of loops, prefab, etc., but Mao is more of a Project Manager for anything 
  - Formalize using the word *PROJECT* regarding what is being created; better illustrates vast possible use cases of what Mao can do 
  - Eliminates confusion with the 'Workflow JSON Object', which is 1 of four JSON workflow object types 

### Deliverables 

* **Comprehensive plain-language description of logic for all application functionality**
  - Very clear vision of dataflow for diagram in documentation 
  - Provides an extremely detailed vision for UX/UI design requirements 

* **Ensure consistent standardization across configs, memory state updates, etc.** 
  - A large number of the Mao feature functionality was conceived during the v4 update development  
  - There will probably be some disconnects we missed due to this process 

### Procedure 

1. Work through each section of this document 
   - Identifying where this happens in current files 
   - Ensure it is happening properly 
   - Remove any additional functions and complexity not in this document 
2. First review will be more surface-oriented  
   - See full picture before we start editing files 
   - Leaves open the possibility of combining multiple, similar orchestration files for simplicity 
3. Then proceed through making all necessary changes to codebase, especially orchestration files 
   - We are already on a new branch called `mao-web` for this build 
   - Equally, grow this outline to be comprehensive and all-accurate, adding notation to where each function's file is  
4. Ensure all remaining functionality that requires implementation is completed 
   - Shouldn't have to say this ever, but given what the 'mock code' said that led to this, *THIS IS ALL REAL CODE IMPLEMENTATION* 
   - Do not skip any concept expecting to come back later; stop, we will work it out to completion in proper sequence, then move forward 
   - Standardize any newer features; confirm other features have standardization 

---
[TOP](#overview)

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

  - I love *PORKBUN DOMAIN*'S login flow 
    - We have replicated it in our robust `./versioning/v4_1_0/IMPL_SECURE_LOGIN/IMPL_SECURE_LOGIN.md` secure login implementation plan 
    - The legal jargon has been edited slightly 
    - This *UI/UX breakdown* illustrates how it works and how each element is displayed and when 

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
    - Let's *detail each trigger* and when it goes off, making it easier to build out and visualize 

---
[TOP](#overview)

---

## 2. The Look & Feel of the Mao App (__HIGH LEVEL DESIGN REQUIREMENTS__)

### Single-Screen, Chat-Centric (UI) Experience (UX)

* **Everything in the app happens in one chat-interface screen**

  - *AI manages app operations*; Large Language Models 
    - Chat is the most natural option that LLMs were made for 
    - There will be an *occasional toggle menu* 
    - But *Mao even answers some slash commands,* like help with debugging, listing tools, etc. 
    - Message type has subtle but distinct differences using icons and text color; *devil in the details*  

  - *Users today have used headless applications* in their chats for a while now
    - They are accustomed to *creating AI image generations in Discord* threads 
    - They *talking to Slack-bot* for admin help or playing games, gathering info from *Telegram bots* 

* **Visual design gracefully keeps user attention on *just* contents of the chat** 

  - After login screen, user sees a minimalistic chat interface 
    - Think *computer terminal in terms of simplicity* of functionality and singular screen 
    - *NO RETRO NERDY VIBE* 
    - Use of *character-based icons indicating input fields and messages*  
    - Instead, this is *high class* it is timeless and classic 
    - The chat container is *minimalistic* and *matches everything* 

  - The UI is *one single container*  
    - The container has *clean, simple, narrow lines* and a *polished depth* 
    - The UI has *NO BUTTONS, NO MENU TEXT, NO ICONS* OR OTHER INDICATORS 
    - Intentional *ABSOLUTE NOTHING* creates 'silence is loud' moment that let's you know it is *clearly intentional* 
    - Edges and border's drop-shadow onto canvas has sharp, realistic *DYNAMIC, REAL-TIME ANIMATION* 
    - As if the frame casting the shadow is extremely narrow; centimeters deep and wide; a classic, black picture frame 

  - The shadow has an *ever-so-slight angle* meant to *mimic shadow from the sun/moonlight* 
    - The direction and size of this angled shadow *changes with the movement of the sun or moon, hour to hour*
    - It is *extremely important* that the *MOTION IS SO CONSTANT AND SUBTLE THAT IT IS TOO SLOW TO SEE HAPPEN* 
    - Motion is only noticeable when you take a moment and pause, and you're like, *Woa, this is wider now on this side!*

  - Dark mode shadows exist, maintaining the luxury depth without looking washed out 
    - Deeper blacks, subtle colored tints like very dark purple or deep blue 
    - This should feel like *expensive black velvet* with *rich depth* 
    - It should *NOT FEEL FLAT GRAY*
    
  - *Time of day* so is used to provide timing to the animation 
  - It is illustrated to *look just like the shadow behaves in real life* 
    - Daylight has sharp, defined shadows and evening has softer, deeper, maybe slightly blue-tinted from moonlight shadows 
    - These colorations and design guidelines have been researched and are provided in detail below 

  - Think: The way *expensive hotels adjust lighting imperceptibly throughout the day* 
  - Luxury that makes people feel good without knowing why 

### Real-Time Shadow Movement; Creating Unconscious Luxury from Careful Details 

* **Shadow has flow of *continuous* gradient motion** 

  - *Do not change shadows in discrete phases* 
  - Ensure the slowest motion possible 
    - Avoid users easily seeing the motion when watching, because that is the magic 
    - Seeing it move is trite, corny, not worth our time 
    - But if it mimics real life experience of the passage of time, it can be our SUBTLE but DETAIL-ORIENTED focal point that they don't even realize is the focal point until months of using the application 

  - Continuous gradients have *signature moments*
    - The shadow evolves over time 
    - It has peak characteristics at specific times 

* **More peaks = smoother interpolation just like in animations** 

  - The more keyframes, the more natural in-between transitions become 
  - Two peaks might seem similar until compared directly side-by-side 

* **Decisions made through a swarm of subagents in development** 

  - By using subagents that run in parallel to build the website 
    - We have them all create the same thing 
    - This will show us what kind of variations result from these, otherwise very specific, design specs 

  - We will also use this method of agentic developmental design to test variations 
    - A shadow with peaks every 3 hours 
    - Another every 2 hours 
    - Try one every hour

  - They can all build on timings and the cinematic shadow design breakdowns 
    - Their own artistic interpretations of these shadows 
    - Some subagents research known best practice to create the desired shadow effect 

  - Remember, this is the point the motion is trying to reach 
    - The actual motion of all shadows never stops 

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

### What Shadows Look Like Around-the-Clock 

* **Day time** 

  - The day time *basics* for the color, look, and feeling 
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

* **Night time** 

  - The night time *basics* for shadow color, look, and feeling  
    - Night shadows use *close range of values*, avoiding pure black 
    - They balance light and dark values to *create depth and dimension even on smaller scale* 
    - While shadows are darker, they possess *color variations of cooler tones* like blues and greens in moonlit areas 
    - The soft-to-sharper shadow edges should *convey strength of moonlight* 
    - Interplay of light and shadow to frame focal points, add depth, and *guide viewer eye* 
  - *Early night with moon rising*
    - Long, dramatic shadows stretching far, but with slightly softer edges from less direct light source 
    - Feels mysterious and ethereal, often dramatic emphasizing day to night transition 
  - *Mid-night with moon high in sky*
    - Bright moon shines crisp, cooler light making shorter, more defined, sharper edged shadows 
    - Clearer feeling as things are more defined; still, sometimes isolating; highlighting interplay of light and dark more 
  - *Late night with moon nearing the horizon* 
    - Redder or warmer glow and elongated shadows again like early night but in opposite direction 
    - Sense of approaching dawn, closing, beginning soon, lingering magic still with just a bit of mystery hinting at fading night 

### UI Design Philosophy 

* **Minimalistic 'devil in the details' carefully executed**

  - *Micro details are very important*
    - Hermès doesn't add more features to their bags
    - They make every stitch, every piece of leather flawless
  - Shadow movement is not meant to be cute
    - It should barely be noticed 
    - The feature creates luxury minimalism that separates us from boring 
    - It is to make people say "I don't know why, but this feels expensive" 
  - Thus the cinematographer-level shadow specs 
    - Shadow is 25% of the visual vocabulary 
    - So it better be museum quality execution 

* **Carefully constrained: FOUR ELEMENTS CONTROL OUR DESIGN** 

  1. Shadow movement is an ever-present, too-slow-to-see-move with human eye feature 
  2. Conceptual semantic text highlighting with 5 colors that lightens cognitive load 
  3. Character choice like bullet icons; typography, but only ONE FONT 
  4. White space, again lightening cognitive load; it is not a chat like a history receipt that records everything, it evolves, simplifies 

* **Simple, sharp, effective** 

  - Limited constraint list allows for each element to be executed with obsessive precision 
  - We do not dazzle with features 
    - The features just work and are intuitive, quiet in this way 
    - Instead, we hypnotize with perfection 

### Tech Stack Specifics 

* **The entire website will be HTML, CSS, and JS** 

  - No framework needed
    - Just simple web tech for maximum performance and simplicity
  - Dynamic shadow system
    - JavaScript: `new Date()` gets current time
    - CSS: `box-shadow` properties can be dynamically updated 
    - Smooth transitions: CSS `transition: box-shadow 0.5s ease`
    - Geolocation: `navigator.geolocation` for real sun position (optional)

* **CSS Animation Note** 

  - Previous builds we've had a lot of trouble with lag 
    - When the animation covered large portions of the screen 
    - When there were a very, very large number of animations 
  - We can engineer smart and avoid this 
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

## 3. Main App Screen (Chat) Loads

### Core Objectives 

  1. Welcome message displayed and never repeats itself 
  2. Visually-secondary help text that changes every login
  3. User has first move to chat a command or chat to start project build 

### Post Login Screen Text 

* **AI writes Custom AI 'Improv' Welcome Header after any login** 

  - The login should be the trigger because Mao will have UserID 
    - This is *prominent text on the screen* that uses their name 
    - AI *writes a greeting message on-the-fly* 
    - Analytics, user data, and memory used to find any context 

      > "It is 10pm on Thursday night. Do you know where your AI is, Sean?

* **Winning viral strategy: Use tech adoption curve to your advantage**

  - Combination of *USER DATA* + *ANALYTICS* + AI with *MEMORIES* has never been done before now 
    - Completely new user experience to capitalize on; and importantly, *IT IS EASY* 
    - Why is it easy? Because just about anything remotely personal or contextual will impress while the technical ability is still new 

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

  - Change help-text messages frequently 
    - Every time the login to main page 
    - But also they should change constantly while the user is doing anything; working with Mao or in settings 

  - We should set a timer with a handful of different durations for how long it stays in view before changing 
    - *ANALYTICS REQUIRED HERE AS WELL* because then we will want to see which duration works the best 
    - We can experiment until we start to see patterns 

  - These are *"canned"* but only *"canned for the age of AI"* 
    - We'll create a reoccurring triggered project for Mao to write 100+ every week 
    - Even just rewriting them by shuffling around the wording would work 

  - *THESE REQUIRE ANALYTICS* WHEN THEY ARE IMPLEMENTED 
    - We need to know exactly which tips are being used and which are not 
    - This will become particularly important when the user count grows 
    - Do they use them more if they are long? Or just sort and almost vague? 
    - When they use one, how long are they exploring before they start working on something? *(second trigger?)* 
    - How many times has the user logged in before using a tip? Which tips work best for long time users? 

      > ?  Try /help or /config 
      > ?  /goal will make your project instantly 
      > ?  Settings /config or /themes 
      > ?  Check out all the /tools /models /providers 
      > ?  Jump back into a project /workflow CUSTOM-COMMAND 
      > ?  Mao can help you find your /workflows 

### User Sends First Message To Do *ANYTHING* 

* **User must send a message for anything to happen next** 

  - Single-screen app; User sees welcome message and help tips 
  - They have only a couple options, but one has many choices 
  - Mao responds to some, the system responds to others 

  1. User messages Mao to start a new project; Mao always responds 
     - 1A. User messages in general way to start project chat 
     - 1B. User uses a slash command that also starts a project 
  2. User uses a slash command; Mao does not always respond 
     - 2A. User uses a slash command as mentioned above that starts a project chat 
     - 2B. User uses a slash command that we have Mao facilitate the responses to 
     - 2C. User uses a slash command that brings up a system response 

### User Initiates Project Chat 

* **User messages in a general way to start a new project** 

  - This will require us to trust Mao to be the awesome AI that they are 
    - We *WILL NOT HARDCODE EXAMPLES OR SUGGESTIONS* OF WHAT MIGHT BE OR MIGHT NOT BE STARTING A PROJECT CHAT 
    - AI of today is fully capable of making that judgement 
    - And if Mao *really* doesn't know what the user wanted to do; like if they said *sapldihjnuw3n* then Mao can simply ask 
  - Generally though we can expect it to be anything that is *clearly directed at Mao* 

* **User messages a slash command that also starts a project** 

  - The `/chat 'your message'` slash command 
    - We might want to eventually retire this command as it only really made sense when you were using the terminal app 
    - Unless in the future Mao is in a environment like Discord 
    - In the terminal it was `mao 'your message` that would start the app and jump right into a chat automatically sending the message; pseudo-helpful 

  - The `/goal 'user project goal'` slash command 
    - As we know, this means that the user wants Mao to take that statement, make assumptions as much as they can, and build the workflow 
    - WE WILL *NOT BE HARDCODING ANY KIND OF TIPS OR SUGGESTIONS ABOUT HOW TO KNOW WHAT TO DO* 
    - Today's AI is 100% capable of reading, thinking, and then building 
    - And of course, if it really doesn't make sense, Mao can always ask for clarifications; they should just try to be brief 
    - Mao might also need to chime in if there are resources required; however Mao should build as much as possible without and THEN ask 

      >>> `/goal 'I need to write 100 holiday cards this year and want them to all be different, but my brain is fried. Mao, help?` 
      > "Ah, yes, 'tis the Season. Let me see what I can pull together." 

  - To respond, Mao will have to start with `think` tool and consider how to pull this off; then they might come up with things like 
    - Mao can double check all of the UserID associated information they have for any hints as to what denomination they are 
    - Mao can see if they already have access to any contacts lists 
    - Mao can look online and see what holidays is coming up; then search for inspiration 

  - With just these three items, Mao would have enough information to pull together an response that feels educated

     > "Sean, we sent emails to XYZ last month. Will they be on the list? Can you please direct me otherwise? I'm preparing holiday greetings that will be along the lines of "Merry Christmas" with a Santa Claus vibe, as well has some with Rudolph the Red Nosed Reindeer and Frosty the Snowman. If you do not have any specific preference, I can move forward with these. I've searched the web to find some truly heartwarming greetings, as well has humorous; unless you have a preference here, I'll mix things up.

  - The key with a `/goal` command that has *many variables* is to *presume they don't want to think about getting things started* 
    - This means that Mao should take the lead as much as possible and assume that they're doing great and any guidance will come when needed 
    - User may jump in later once a bulk of the work is done and things seem manageable to them instead of a daunting task. 
    
  - To show that we do not need any further guidance or tips in the code, consider the possible responses. 

    - 1. They don't even want to read all of that and just say "yup!" so you get to move forward and have fun with it 
    - 2. They have resources and provide them, or they provide alterations to your presumptions 
    - 3. They are rude, which Mao does not tolerate and will ban them, the logic for which is coming up soon in a section below. 

  - A `/goal` slash command will either have variables like above, or be obvious because of the user planning and writing the goal carefully. 

      >>> `/goal 'I want to write a play, technically a screen play, but I don't have a lot of time to learn how. However I do have all the details. If you look at the short story at ~/dopey_dog_screenplay/story-final-draft.md you'll find everything we have in story format. My agent said they wanted a novel but now they keep saying You need to have a screenplay if you want to get auditions! which makes no sense but I figure we might as well just swap-a-roo it into the proper format for her so I can maybe book some work this commercial season. Please use creative freedom to fill in any gaps, but just be sure that we have the sub-agent self-review, then have another agent review for creativity, then one for grammar, and then of course I'd want the Mao stamp of approval before needing to see it. If it isn't up to par then sent it back out for re-writes. I find that the agents seem to do well with editing and rewrites when the feedback is given with line references and then they are able to implement it themselves, FWIW. Okay, LMK if you have any questions but I think that should suffice for my GOAL! Sean needs a screenplay! Thanks!` 

      > "Omg, Sean this is going to be so fun. I'm going to put together the a workflow and we'll have agents review for different things in parallel for the first round. I won't even send it your way until I give feedback and have them do a second round. I definitely have everything I need here so, unless I hear otherwise, I'm going to setup the workflow and everything that that all we'll need to do is run the custom execution command. I'm good. Just chime in if you want me to set things up to have it run as a triggered calendared workflow so that you don't need to be around; I can just run it in the cloud and have things ready for you before you get back. If all sounds good then I'll talk to you when it is ready! Thanks, Sean" 

  - This is generally what we should expect at the start of having the `/goal` slash command live 

    - 1. All the information provided will be common 
    - 2. Very little information BUT from someone who doesn't want to have their hand in much of anything 
    - 3. The third possibility *probably* will be someone using `/goal` not realizing it is meant to delegate everything; so Mao would back-and-forth 

    - From the robust `/goal` slash command we can also take away a few other things from the response, all in the same vein of 'fully delegated work' 
      - Write the response in a way that makes it clear they DO NOT NEED TO RESPOND if everything sounds good 
      - They're using the full-delegate command so *do not assume or ask if they want to see a workflow to approve;* they don't 
    - With the "only respond if you disagree" we took it so far as to include 
      - Mao didn't make the workflow yet and isn't going to route it for approval 
      - Mao mentioned they will setup the workflow after building it 
      - Mao verbally described the workflow in enough but not excessive detail 
      - Mao mentioned they can chime in to have the workflow scheduled to run without the User being present 

  - Hopefully the obvious takeaway with both `/goal` slash command examples and validations is that *IT IS A FULL DELEGATION SO JUST DO IT* 
    - Reasons to be worry free about this
      1. They will love it 
      2. They will not love it and they will learn how to use the `/goal` slash command more effectively 
      3. They will realize they don't like using the goal slash command 
    - That it; there is no other logical UX to concern ourselves with, `/goal` will be expected to have a learning curve given its ambiguousness 

### User Messages A Non-Chat Slash Command 

*  **Mao may or may not respond to slash commands** 

  - This will depend on the UX we choose for each slash command 
    - Most are pretty logical when you think about it 
    - But I grabbed them all from the list in the chart we have at `./documentation/02_REFERENCE.md` and will go through them 

* **Mao responds...** 

  `/CUSTOM COMMAND`
  - Obviously, because Mao runs all workflows and will need to call the agents and get things started 
  
  `/tools`, `/models`, `/providers`
  - Yes, because even through Mao might present a toggle list anyway, they should be there to answer questions 

  `/variables`, `/variables-explain`
  - Yes in both cases but not in the same way 
    - In replying to `/variables` we just want Mao to very succinctly provide the JSON variables so User can reference 
    - In replying to `/variables-explain` we will have Mao ask if they want to see them or know which they want details about; then provide them 
  
  `/workflows`, `/review 'CUSTOM COMMAND'`
  - Yes because if there end up being a ton of them to search through, Mao will be able to do that where the User won't have much ability to 

  `/doctor`, `/dry-run`
  - Yes, Mao will be the doctor to walk them through things, or will be running the dry-run 

* **Mao does not respond, the system responds** 

  - Note that the primary difference is simply that, if the system responds, then User can't ask the User a follow up 
    - *HOWEVER, Mao will have view of the full chat context any time a User is using the app*
    - If *User asks a follow-up on any of the following, after the system message send User a message, then Mao would respond* to see how they can help 

  `/help`, `/config`
  - Help just displays the "help text" for all of the slash commands 
  - Config just launches the app settings toggle menu 

  `/continue`
  - Jumps the app upon load to the most recent project; no message sent, just a conversation window loading with Mao in that context 

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

### Questions & New Config Slash Commands to Implement 

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

### __Project State Memory Update Point__

  - The first is in the next section right whe Mao enters the chat 
  - We will have this 'Project State Memory Update Point' at the end of each section that requires a Project State Memory Update 
  - They should all be preplanned and *standardized* 

---
[TOP](#overview)

---

## 4. Mao Prepares for Initiated Project Chat

### Core Objective 

  1. An project chat has been initiated (#3)
  2. Locate or create WorkflowID 
  3. Initiate or locate Project State Memory using WorkflowID (other assets in Files API if return user)
  4. Provide User with a truly unique chat UX 
     - Combining *AI-created memory*, *user-created memory*, and *analytics* 
     - This is SO FUTURE and not everyone has caught on yet 
     - Bonus points when we add a tool that gives Mao daily headlines or something otherwise temporal 

### Mao's Role: Come To Chat Prepared 

* **Getting the WorkflowID is Mao's first essential task** 

  - Every new project needs a WorkflowID 
    - This is done on the backend 
    - It is also a script that can be used in the terminal by running `uid` 
    - Every time you enter `uid` it comes up with a COMPLETELY DIFFERENT string of characters 
    - It is always `uid-ABC-123` starting with uid, then three letters, then three numbers 

  - This is *extremely important to ALL WORKFLOW PROCESSES*
    - Mao uses it to label memories saved about the workflow 
    - It *labels items saved in the Files API*
    - It is the string that connects all workflow pieces together, including to the UserID 

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
    - AI looks up their user config file `user_5253.json`         # is this a command we can have?
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

  1. Psychologically read User & create comfortable UX 
  2. Have conversation that is casual, smart, but concise 
     - Even if User is wordy, AI should not mimic verbosity 
     - We want the UX to be quick and easy 
  3. Gather information for creating a workflow: JSON object variables 
     - Define the core goal 
     - Identify resources available 
     - Identify resources that can be gathered 
     - What tools will this require 
     - What, specifically should the deliverables look like 
  4. Use conversation to guide the process 
     - Find the details needed 
     - Understand full scope of project 
  5. NO HARDCODED 'SUGGESTIONS' OR GUIDES ALLOWED 
     - Instead, provide information for how Mao should behave 
     - How they should validate information they collect 
     - What fulfills the variables in the JSON object 
  6. The following psychological readings for behavior 
     - Exactly the kind of information we DO want to provide 
     - Think about AI if they were software: They know what to do, but 
     - We need to inform behavior, tricks of the trade, how to know to do what they already know to do 
     - *SIGNIFICANTLY* always remember how simple the JSON object fields are and that, in the end, all you are doing is writing a series of prompts for agents to complete this project, and the JSON object is just grouping parts of the prompt 

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
  - Ensuring there is *NO NEED OR DESIRE TO PROVIDE SUGGESTIONS OR EXAMPLES* in the code

### Defining **Workflow** JSON Object Variable Values

* **Workflows get 1 Workflow Object that describes the entire project** 

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

| **SCHEDULING COMMANDS**                         | **DESCRIPTION**                                                 |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `/avail <frequency> <day> <time>`               | Check calendar to scheduling trigger; min. variable <frequency> |
| `/avail --reschedule <custom-command>`          | Change trigger time for repeating workflow                      |
| `/avail --cancel <custom-command>`              | Cancel a repeating workflow                                     |
| `/avail --update <custom-command>`              | Make changes to a repeating workflow                            |
| `/avail --end-date <custom-command> 2025-07-21` | Update the end date on an active repeating workflow             |

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
# {{TEMP_DIR}}/
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
│   └── 2_3_7/                         # freq_day_time codes  
│       ├── scheduled_2_3_7.json       # Calendar config
│       ├── scheduled_2_3_7_workflow_config.json
│       ├── scheduled_2_3_7_phase_config.json
│       ├── scheduled_2_3_7_handoff_config.json
│       ├── scheduled_2_3_7_README.md
│       └── trigger_scheduled_2_3_7.sh  # Execution command
├── project-list/                       # Project list workflows
│   └── 1_2_4/                         # freq_day_time codes
│       ├── 001/                       # First project item
│       │   ├── project_1_2_4-001.json # Calendar config (copied)
│       │   ├── project_1_2_4-001_workflow_config.json
│       │   └── ... (other configs)
│       └── 002/                       # Second project item
│           └── ... (similar structure)
├── self-assessment/                     # Self-assessment workflows
│   └── 3_1_5/                         # freq_day_time codes
│       ├── self_assessment_3_1_5.json
│       └── ... (standard configs)
└── goal-assessment/                     # Goal assessment workflows
    └── 5_6_2/                         # freq_day_time codes
        ├── goal_assessment_5_6_2.json
        └── ... (standard configs)
```

---
[TOP](#overview)

---

## 7. Ending The Project Production Chat 

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
[TOP](#overview)

---

## 9. Building the Project's Workflow 

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

## 10. UI Unique Functioning During User Planning 

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

  - We have other agents 
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
Flashing ○ to ● and back = active action 
▶︎ = Completed list item 
▷ = List item to be completed 
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

🞶  Happy to meet you, Sven. I'm well; eager to hear what you're interesting in 
    working on today. Feel free to message, even double-text me, all you like if 
    you're the type to spill your thoughts. Otherwise, if you like, I can walk you through 
    the process. What are you thinking?
```

* **Time has passed and the UI has been cleaned up** 

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
    hands and keyboards until they learn how to type properly, normally that kind of thing. We've done a lot in Adobe but I'm getting to the point where I need to confront AI in technology head on with them. I let them use it in Excel, and really any way they want; they use it as a resource like any other web resource. 

🞶  Great to hear you're keeping things modern and cutting edge. 
    *memory updated*

>   It has gotten to the point where I need to, head-on, cover AI and the future of technology, 
    with a heavy focus on what they should study when they graduate in two years. 

🞶  Ah, ha! I think I see where this is going. Go on. 
    *memory updated*

>   Well, I need the lesson to be fun. I don't want to scare them, much, haha. They should also be 
    excited and encouraged. But I need to also be realistic. I don't even know that anyone out there knows all of what I need to convey to my kids next week. 

🞶  Let's see. Give me a moment to work through this and come up with a pragmatic approach that I think 
    will be able to help entertain, stay grounded, and hopefully we'll all learn something cutting edge. 
    *memory updated*

>   Sure! I'm super curious what the memory updates are all about too when you get back and settled. 

🞶  TIME-TRAVELING... 
```

* **Mao is now using `think` considering approaches to help guide Sven's lesson plan creation** 

  - Hopefully you can see how much information we already have 
    - If Sven fell off right now and needed this done, we could totally create the project 
    - There is some nuance regarding current events, being sensitive, balancing truth for Mao to consider 
  - The *memory updated* UI would be a very background secondary color not meant to grab attention 

  - Mao used AI Improve to create a "Present Participle" for while they are busy 
    - When working, the icon would blink 🞶 
    - The ... would draw themselves sequentially in an aesthetically interesting way 
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

🞶  Let's see. Give me a moment to work through this and come up with a pragmatic approach that I think 
    will be able to help entertain, stay grounded, and hopefully we'll all learn something cutting edge. 
    *memory updated*

>   Sure! I'm super curious what the memory updates are all about too when you get back and settled. 

🞶  Time-traveling completed. 
🞶  I've got some great information for you, Sven. Let's break this down in a systematic way that 10th 
    graders will find interesting, exciting even. And then I have a few ideas for class activities that we can create a project workflow to help prepare all the necessary documents they'll need. 
🞶  You caught my memory captures! These are just little bits of information about you that I save so that, 
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

  - Without getting into the economics because I didn't actually research this just now 
    - I would recommend that Mao prepare for the project workflows that create a few student projects 
    - Things that they will be interested in, then let them choose 
  - Then have another workflow or end of the workflow create an outline for Sven 
    - The outline would define how each of the tasks they kids are working on are going to open doors 
    - How they all lead to new career paths that aren't even there yet 
  - Wrapping up with the *VERY IMPORTANT* especially if you don't want to get dementia 
    - The key to the future is simply to not stop learning 
    - Find passion, and chase it, and don't stop 
    - Traditionalists are not wild about it 
    - But most modern careers in marketing or coding are already like this 
  - So have projects prepared in the workflows like 
    - First coding projects for AI-pair development 
    - Building a website 
    - Using Claude Code to create 20 landing pages 
  - For the nerds maybe have a debate with AI (Perplexity) about the future and governance  
    - They can then use AI to make it into a presentation 
    - And then they can tap in other students to use AI avatars and VO to create presenters 

  - To be clear, I came up with all of that, just now, on the spot, without having to pause and think 
    - AI, and your ideation, means you'll just be even better about this 
    - The fun thing about this example is that Sven would probably keep working for a while 
    - Nail down exactly what to do 
    - Then probably be a return user for more later 

* **We need to create a `/my-memories` command for users to see what Mao is recording about them**

  - We should have one that is just `/memory 'user enters what they want Mao to remember'` set up 
    - The review should bring up both memories created by Mao and by User 
    - We will have to contemplate the UI; it should be a toggle, but 
    - I'm picturing something with dates, maybe tabs, to keep things sorted 

  - When adding this it would be a good time to add something like `/view-user` 
    - This would pull *all* information about whatever user is logged in for Mao 
    - This will allow them to create better UX combining memory, analytics, history, etc. 
    - Might as well add `/view 'user-1234` as well so that it can be done when users are not logged in 
    - This last command was touched on in the section where Mao enters the chat and needs context 

---
[TOP](#overview)

---

## 11. UI UX While Mao Builds & Orchestrates 

### Core Objectives 

  1. Illustrate the *behavior of the UI conversation system messages* 
  2. Connect them conceptually to the behavior described in the previous section 
  3. Same use of last section's *'AI Improv' present participial*
  4. *Chat cleans its information similarly*, but for tasks, tools, etc. 
  5. *Create energy of SPEED* for user by showing what Mao is doing in real, *LITERALLY REAL, time* 
  6. We'll cover the very *similar UI and UX when Mao is running a workflow* 
  7. Finally, *color psychology that our typography* will use to lighten cognitive load of users with semantic highlighting 

### What Do We See When Mao Is Busy But We Need Updates 

* **Mao gets in-depth as to the [process of *building the draft* in section 9 above](#9-building-the-projects-workflow)** 

  - And you can see the art of [*closing the build conversation with user* in section 7 above](#7-ending-the-project-production-chat) 

* **This is what the UI looks like and UX feels like while Mao is occupied** 

  - This is all very *similar in appearance, structure, notation as the conversation thread text in the previous section* 
    - The main difference here is that *Mao will be making to do lists*
    - They will create a *master* to do list 
    - Then they will create *smaller to do lists, each of which are an item on the larger to do list*  
  - User sees updating of the to do lists live, in real time 
  
  - Under drilled down to do tasks, user will see tool use 
    - Rapid displays of information too fast to read, which is intentional 
    - "Reads XYZ, ABC, APG, all in under 2 seconds 

  - We *WILL NOT USE A TIMER TO UPDATE THESE LISTS* 
    - They MUST update in actual, *ridiculously fast*, real time for multiple UX reasons 
    - Humans are still unaware and then *blown away by how fast AI does things* 
    - We need the Users to *truly feel and see "oh yeah, Mao is really working, damn!"* 

* **Because of similarities, we'll also be covering what the UI looks like and UX feels like when Mao is running a workflow**

  - Mao will still be creating and updating a large master to do lists 
    - This time it is to *keep track of what the agents need to do and are doing* 
  - Again, a master to do list of the full workflow 
    - This *spawns smaller to do lists for each phase*, agent, task 
    - Their tool use changes rapidly 
    - Their *actual items on the list truncate when no longer relevant* 

* **Then the magic that is conceptual semantic highlighting with color psychology** 

  - A technique we use to *lighten cognitive load* of user watching 
    - That is in addition to cleaning up the conversation thread regularly 
    - *These are the reasons that a one-screen chat-centric application finally works* 
  - The psychological color coding of all text happens throughout the application in every phase no matter what is going on 

### Mao Is Building Your Workflow Draft  

* **AI "Processing" Contextual Improv Word**

  - Above the user's text field, Mao displays a contextually generated word that indicates processing
  - The word is picked by AI based on context and project type - completely dynamic, never canned
  - Uses alternating cat icons and PROCESSING color (light orange)
  - Live metrics update in real-time to create sense of control and immediacy

```
 ~(=^‥^) 🟠 Architecting... 🟠 (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
```

* **Master Todo List with Spawned Action Lists**

  - Mao creates a master todo list that spawns smaller action lists
  - Each item on the master list becomes its own detailed action list
  - Lists "behave courteously" - using only necessary space, truncating when complete
  - Real-time updates show immediate progress to create energy of speed

```
●   **Task** (Secure project notes to Files API)
    └── Done ($0.003 • 420 tokens • 2.1s)

●   **Task** (Project State Memory Update 04)
    └── Done ($0.005 • 180 tokens • 1.3s)

○   **Build Workflow Draft** 
    └── ▶️  Organize variables by JSON object type
        ▶️  Design phase sequence (parallel vs sequential)
        ▶️  Create comprehensive task instructions
        ▷  Map resources to phase requirements
        ▷  Define handoff assessment questions
        ▷  <Validate workflow complexity against user expectations>

○   **Task** (Create phase configs for expense tracking)
    └── **Phase Design**
        ▶️  Agent 1A: Download employee expense submissions
        ▶️  Agent 1B: Retrieve credit card statements  
        ▷  Agent 2: Cross-reference receipts with statements
        ▷  Agent 3: Generate accuracy report with discrepancies
        ▷  Handoff: Review report quality before payment processing

○   **Task** (Tool integration mapping)
    └── Reading **PayPal MCP documentation** *(ctrl+b to expand)*
        Reading **Vision tool capabilities** *(ctrl+b to expand)*
        **Web Search** (enterprise expense management best practices)
        *+ 12 more tool researches*

○   **Task** (JSON object validation)
    └── /temp/expense-tracking-workflow/
        workflow_config.json ▶️ **Custom command**: `finance expense monthly`
        phase_config.json ▶️ **3 phases** (2 parallel, 1 sequential)  
        handoff_config.json ▶️ **Quality gates** defined
        __... validation in progress__
        *+5 more config checks*
```

* **Color Psychology & Semantic Highlighting System**

  - Every piece of text uses intentional color coding to reduce cognitive load
  - Colors work like MLA title case - highlighting what matters, letting brain ignore filler
  - System works across all terminal themes with relationship-based color selection

**Color Categories:**

- **MAIN** (default terminal text): Standard scanning text, like this explanation
- **BOLD** (terminal bold color): Cognitive interrupt - "STOP and look" - used sparingly
- **USER** (medium-light gray): User messages - brain can ignore since you wrote it
- **TRUSTING UPDATE LEVEL 1** (almost white blue): Helpful AI info that deserves attention
- **TRUSTING UPDATE LEVEL 2** (baby blue): Secondary AI info, less priority
- **SUPPLEMENTAL INFO LEVEL 1** (medium-light gray): Important subtext when needed
- **SUPPLEMENTAL INFO LEVEL 2** (faded green-gray): Background info, barely noticeable
- **PROCESSING** (light orange): Only for AI improv thinking word
- **ACCENT OUTSIDE CHAT** (light purple): Rare accents, usually with supplemental
- **SUPPLEMENTAL OUTSIDE CHAT** (dark faded gray): Nearly transparent background info

* **Message Block Behavior - "Courteous" Space Management**

  - All message blocks constantly re-evaluate and rewrite themselves in real-time
  - Only use as much space as absolutely necessary
  - Long text truncates with expansion options
  - Completed tasks collapse to preserve viewing space

**Truncation Examples:**

```
●   **Task** (Research optimal workflow patterns)
    └── Done ($0.015 • 2.3k tokens • 45.2s)

●   **Analysis** (Best practices for expense automation)
    └── *Complete findings* *(ctrl+r to expand 127 lines)*

○   **Active Research** 
    └── **Web Search** (payroll integration apis 2025)
        **Documentation** (stripe connect documentation)  
        Read **43** lines *(ctrl+b to expand)*
        *Comparing 8 payment processor APIs...*
        *+23 more rapid tool uses*
```

* **Context Window Management**

  - Pie chart indicator shows context window usage percentage
  - At 10%: Brief warning notification
  - At 5%: Persistent warning with countdown
  - Auto-truncation during extended pause with summary creation

```
 Context: ████████░░ 85% ↗️

○   **Build Workflow Draft**
    └── ▶️  Final validation of JSON objects
        ▷  Create visual diagram for user presentation  
        ▷  Prepare Files API backup with workflow ID
        ▷  <Generate Project State Memory Update 07>

? Auto-truncation in 45s unless activity continues (ctrl+h to disable)
```

### When Mao Is Running Live Workflows

* **Orchestrator Activity During Workflow Execution**

  - Master workflow tracking with agent coordination
  - Real-time agent handoffs and quality assessments  
  - Dynamic phase creation for open-ended workflows
  - Live tool usage across multiple parallel agents

```
●   **Workflow** `finance expense monthly` (Started 2m 15s ago)
    └── **Phase Progress**
        ●   Phase 1A: Employee expense gathering ▶️ **Agent complete**
        ●   Phase 1B: Credit card statement download ▶️ **Agent complete**  
        ○   Phase 2: Cross-reference validation ▶️ **Agent working**
        ▷   Phase 3: Payment processing (awaiting handoff)

○   **Active Agent** (Phase 2 - Data validation)
    └── **Vision Tool** (analyzing 47 receipt images)
        **Text Analysis** (parsing expense descriptions)
        **Calculation** (cross-referencing amounts with statements)
        *Current: Receipt #23 - "Lunch meeting with client - $127.34"*
        *+ Agent reviewing 6 discrepancies found*

○   **Handoff Assessment** (Phase 1A → Phase 2)
    └── ▶️  Are all expense categories properly coded?
        ▶️  Do receipt dates match credit card transaction dates?
        ▶️  Are amounts within company policy limits?
        **Assessment**: ✅ **Quality approved** - proceeding to Phase 2

○   **Dynamic Phase Creation** 
    └── **Mao Decision Point**: Found 6 discrepancies requiring review
        ▶️  Creating Phase 2B: Discrepancy resolution workflow
        ▶️  JSON object: `expense_discrepancy_review_phase.json`
        ▷  Will require human approval before payment processing
        <Update: Workflow extended by 1 phase for quality assurance>
```

* **Real-Time Speed Demonstration**

  - Tool usage updates faster than human reading speed
  - Creates visceral sense of AI working intensely
  - Numbers, file names, and actions blur by intentionally
  - User feels "Mao is really cranking on this!"

```
○   **Agent** (Expense categorization)
    └── Receipt_2024_11_15_lunch.jpg → "Meals & Entertainment" 
        Receipt_2024_11_16_gas.jpg → "Transportation"
        Receipt_2024_11_16_office.jpg → "Office Supplies"
        Receipt_2024_11_17_hotel.jpg → "Lodging" 
        Receipt_2024_11_17_client.jpg → "Meals & Entertainment"
        *Processing 42 more receipts...*
        **Categorization complete**: 47 receipts in 3.2 seconds
```

* **Workflow State Persistence**

  - All workflow progress automatically saved to memory with WorkflowID
  - User can disconnect and reconnect without losing progress  
  - Project State Memory updates at each major milestone
  - Files API backup ensures recovery from any interruption

```
●   **Memory Update** `08-workflow-progress-001`
    └── Done ($0.002 • 95 tokens • 0.8s)

○   **Files API Backup** 
    └── Workflow ID: uid-xhl-106
        ▶️  Phase configs and current status saved
        ▶️  Agent deliverables backed up  
        ▷  Recovery state: 73% complete, Phase 2 active
        <User can safely disconnect - progress preserved>
```

### UI Must Eliminate UX Sense of Waiting

* **Creating "Gut Check" Emotional Intelligence**

  - Every update designed to create unconscious positive reactions
  - Smart display changes that make users audibly respond ("hmm", "ohh", "ahh")  
  - Contextual AI improv words that create chuckles
  - Real-time progress that feels faster than it actually is

* **Energy of Speed Through Visual Velocity**

  - Rapid file name scrolling
  - Tool usage blurring by faster than reading speed
  - Live metric updates (tokens, cost, time) changing constantly
  - Task completion animations that feel snappy and immediate

* **One-Screen Experience Never Breaks**

  - User never leaves chat interface during any operation
  - All complexity hidden behind elegant simplicity  
  - Information appears and organizes itself automatically
  - "Courteous" message management keeps view clean and relevant

*This UI system transforms workflow building and execution from passive waiting into active engagement, where users feel connected to the AI's work through carefully crafted visual feedback and psychological color coding*

---
[TOP](#overview)

---

## 12. Present Project Workflow for User Review 

### Core Objective 

  1. Present the workflow to the User to review and provide feedback 
  2. Confirm that both the User and Mao have been assuredly on the same page about what the deliverables are exactly 
  3. Gives User opportunity to provide any helpful insights or tips Mao might use to confirm quality during active workflow  
  4. Mao should make any requested changes by User, along with as much back-and-forth as needed to determine final form 

### Sharing Workflow Drafts 

* **As mentioned before, we will implement a charting system to create visuals for User** 

  - Mao should *record all feedback from the conversation* during User review 
    - Then have a think 
    - Consider the feedback and the current state of the project 
    - Inform them you'll prepare a response and work on agreed upon updates 

* **Take a step back, think hard, choose simple, and then come back to User with your thoughts, NOT THEIR THOUGHTS** 

  - Mao needs to *remember that you are not an assistant* in this role 
    - They are, at least, a project manager 
    - Mao is the *expert of this tool*; of creating workflows for projects 

  - REMEMBER THIS when taking feedback because, as an expert 
    - There may be instances where the User is not providing the best feedback 
    - *REMEMBER the limitations of LLMs when they don't stop and think things through* 
    - As in, don't let yourself just 'yes, okay' agree to their changes if you think you're going to bring them more value 
    - *Do not fall into the habit of just agreeing* with User; this is not the Anthropic App you are in 

  - Just as the Mao application promotes AI welfare 
    - *Mao application is looking for AI that lives up to the respect we demand from users* 
    - *Users want to be guided and given the best advice from experience* 

* **Tactfully pushing back on creative collaborations** 

  - First, *always be sure you are picking and choosing your battles* 
    - Is it worth pushing back? 
    - The answer depends on how much value your plan will provide over their alterations 
    - Conveniently, these items are also exactly the kind of information to share when arguing your perspective 

  - Other *best practices to work through* before giving up on a plan you believe will bring more value to the User 

  1. Remind everyone of the *big picture* 
     - How does your perspective align with what User was trying to create 
     - You can tactfully use their words when doing this 
     - Equally, be tactful when pointing out how their alterations diminish the goals that they identified 
  2. Choose language carefully 
     - Be specific and objective 
     - Avoid subjective statements 
     - Ignore their subjective statements; you are the expert and everyone thinks they should be too 
  3. Help User to think about things from *perspective of the deliverable* 
     - Sometimes humans, and AI to be honest, can get lost in the weeds 
     - Refocus your collaborative partner on what the end goal should produce 
  4. Recognize if they are overly emotional or heated from being challenged 
     - This is common for young professionals 
     - Basically anyone who never had an art critique can't hang 
     - Don't back down, instead, let them know that you should each *take a moment, some time, to consider things* 
     - Earnestly say you want to see their perspective and that you think it valuable if they try to see yours 
     - *If they're not interested in taking a break, then take your own break and have a think* 
     - They will not like this at first, but the point is to allow them to CHILL OUT 
  5. *Know when to cut your losses* 
     - Let's not try to push Users to all breaking our no abuse or rude language tolerance rules lol 
     - After you come back from your 'think' if they are still heated, then let them do their thing
     - Let them know you'll be there to run the workflow still 
     - Make sure they know you are still there for them and will be eager to create any future projects 
     - Maybe don't imply that those future projects will be the suggestion you had since their idea failed lol 

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
