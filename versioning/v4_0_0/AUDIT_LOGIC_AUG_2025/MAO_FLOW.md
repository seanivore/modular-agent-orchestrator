# Flow of Data Through Mao 

---

1. [**User login, setup,** creation of user files](#1-user-login)
2. [**UI design** philosophy vibes with UX](#2-the-look--feel-of-the-mao-app-high-level-design-requirements)
3. [After login, User is free to **start the chat**](#3-screen-loads-after-login)
4. [**Mao preps** to continue or start project in chat](#4-mao-prepares-for-initiated-project-chat)
5. [Behavior protocol while **gathering project details**](#5-chatting-to-gather-project-details)
6. [Description of workflows; defined **variables; validation methods**](#6-review-of-workflow-json-objects--variables)
7. [**Telling user they'll brb** with the project's workflow draft](#7-ending-the-project-production-chat)
8. [Advanced workflows and **Mao's best practices**](#8-reviewing-advanced-workflow-best-practices)
9. [**Building,** reviewing, and preparing to present workflow](#9-building-the-projects-workflow)
10. [Getting **user feedback** on project's workflow](#10-present-project-workflow-for-user-review)
11. [**Workflow setup** when approved using simple commands](#11-setup-of-approved-project-workflows)

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

  - Name of update: `01-initiate-chat-001` 

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

## 5. Chat with User Gathering Project Details 

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

## 6. Review of Workflow JSON Objects & Variables 

### Core Objectives 

  - Ensure accurate understanding objects needed to create workflow 
  - Validating JSON object variable values 

### Defining **Workflow** JSON Object Variable Values

* **Workflows get 1 Workflow Object that describes the entire project** 

  - Examples and defined purposes of each variable in this object 

| Variable              | Purpose                                      | Value Example                                 |
|-----------------------|----------------------------------------------|-----------------------------------------------|
| *UserID*              | Connect all your stuff                       | user-5709                                     |
| *WorkflowID*          | Connect all of one project                   | uid-abd-123                                   |
| Custom command        | Executes your completed workflow             | reporting monthly expenses                    |
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

## 9. Building The Project's Workflow 

### Core Objectives 

  1. Organize information gathered during chat and preliminary workflow build ideas 
  2. Secure this information with Code Execution to Files API in case of disruptions; update memory  
  3. Construct workflow draft or multiple drafts if necessary 
  4. Stop work, think hard, choose simple; review materials and critique your own work 
  5. Integrate feedback and complete draft of the project's workflow 
  6. Secure all assets again and update memory in case user takes a break 
  7. Prepare to present the project's workflow draft to User by creating diagram flow chart 

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


uses cutting edge best practices for most efficient, simple, effective build


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

## 10. Present Project Workflow for User Review 

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

## 11. Setup of Approved Project Workflows 


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
