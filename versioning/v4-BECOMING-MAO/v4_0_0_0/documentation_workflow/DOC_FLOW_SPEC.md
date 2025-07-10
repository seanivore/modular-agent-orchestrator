# DOCUMENTATION WORKFLOW SPECIFICATION
*The Definitive Mao Documentation Creation Blueprint*

---

## Project Vision

**Goal:** Create documentation so compelling that it could close a VC round while being technically excellent enough for enterprise developers, yet engaging and simple enough for our non-techincal target market users.

### Success Criteria

- **Non-technical users:** "I understand the value and want to try this immediately"
- **Developers:** "I can create a custom implementation in minutes with confidence" 
- **CTOs:** "I can smell the layers of value through the trusted architecture."
- **Investors:** "This solves problems that effect a massive market using solid execution."

---

## Storytelling Mao's Value

Illustrating the values and principles learned, leading into the success story.

### Storytelling Goal

- Show values by telling the brand story 
- Explain the technical architecture at multiple levels 
- Structure the documentation so that it is similar to the actual user journey 

### AI Industry's Non-Negotiables Obstacles (Problem)

* The industry will not stop changing
  - Who is the AI; models, their abilities, limitations, pricing, etc. 
  - Who gives you AI access; providers, cloud, self-hosted, etc. 
  - What AI can do; skills, tools, intelligence, reasoning ability, decision making, etc. 
  - How do you interact with AI; prompting, prompt strategy, phrasing, context, memory, etc. 
  - Medium to collaborate with AI; app, CLI, API, built-in commands, settings, etc.  
  - Data needed about AI; behavior, performance, accuracy, etc. 
* Don't build what AI will end up evolving into 
* Stop thinking about applications, programming, even code, in the old way 

### Accepting Those Absolutes & Moving On (Solution)

#### 1. Evergreen Value 

* Explain the solution 
  - Our philosophy of modularity 
  - The strict, variable-based, never hardcoding, rules 
  - Recognizing that you have to design UI for both the user and the AI 

#### 2. Story Arc of Where Mao Came From 

* Needed a code solution to replace the many Make (Integromat) scenario automations 
  - Published website with 200+ weekly blogs; API video shorts; two podcasts before Google's Notebook tool  
  - Learned from IndyDevDan's YouTube about building 'Single File Agents' using UV Astrum Python 
  - Sent Claude the transcript and was like, what is this? We had only made a couple MCPs and one HTML/CSS/JS website 

* Created SFAs that were specialized for specific tasks 
  - Required a lot of planning 
  - Took too much time; didn't make logical sense in the context of the industry changing 

* Implemented "Variable-Input" SFA 
  - Spread the task, or prompt, across values of variables in a JSON object
  - "Agent" SFA file was completely generic with no hardcoding; hard to get AI to do, needed lots of rules early 
  - A setup script executed with the SFA and the JSON object creates specific use case scripts on the fly 
  - Each use-case got a custom command to run in terminal 
  - Made over 50+ different use-cases 
  - Some I updated the JSON variables frequently and then kept running the command 
  - EXAMPLE: 
    1. Put MD document of Job Opening in directory 
    2. Another directory had resume, writing samples, summary of portfolio entries, impressive metrics, preferences 
    3. SFA had a phase that would write a targeted cover letter and targeted resume 
    4. Secondary phase critiqued and reviewed for accuracy 
    5. Final phase feedback was implemented 
    6. The result was applying to hundreds of jobs a week with great resumes 
  - EXAMPLE: `https://presenting.august.style/`
    1. Professional connection had a client needing Voice Agents for new-age telemarketing 
    2. SFA had first phase that did a bunch of research in various ways, asked Perplexity 
    3. Specifically researched how the app they use does voice modulation because all the research was hard data about it 
    4. Second phase focused on pulling out the core strategies  
    5. Next phase made it tangible by creating an archetypal persona that fit the strategy 
    6. Next phase created script and used the apps notation for voice modulation; created a "cheat sheet" 
    7. Review phases 
    8. Final feedback implementation phase 
  - EXAMPLE: `https://presenting.august.style/` 
    1. Quick Google found list of one paragraph "Brand Identity" for semi-known brands 
    2. Phase one created addmittedly surprisingly robust month long marketing plan 
    3. Phase wrote corporate emails, provided tips 
    4. Phase wrote captions and vividly described Instagram posts 
    5. Review phases, and implemented feedback 

* Variable-Everything Realization 
  - SFA got SUPER BLOATED and one day a resume cost a few dollars to create 
  - I wanted to use a free Google LLM instead 
  - It clicked "wait, technically the model is hardcoded" 
  - The same day Anthropic happened to release Claude Sonnet 4

* Introducing The Orchestrator 
  - Played around with SDK translating for one build
  - Forgot to have it parse the API responses 
  - I literally said "I fully do not understand why we can't just literally code a button that the agent just pushes to use a tool, the same as a human button" 
  - Claude paused, considered it, then realized the new "Code Execution" Sonnet 4 tool could do exactly that
  - Officially eliminating SDKs opened the door and we started adding Features
  - No feature would be added in a way that wasn't a config collection of JSON objects, one for each 'setting' 
  - Throughout the entire build, up to the day before the final codebase audit, we kept randomly making new JSON object collections 

* Mao was Born 3 June 2025 
  - We very quickly realized that, the more we made the "MAO" or Modular Agent Orchestrator able to do more complex tasks, THE EASIER IT GOT FROM A UI/UX POV 
  - That moment was like "okay, this is literally art, it is taking something and turning it into something completely different" and "there is something here; we have something here" 

* Accepting Those Absolutes 
  - Suddenly it was possible to not just accept the industry's non-negotiables, but to use them to our advantage 
  - We build so that you just drop in X, Y, Z file and the new model or tool or provider or command or setting JUST WORKS 
  - New codebase was audited many times, many rules were written 

* 4 Weeks Later, We Had 95%+ Compliance

#### 3. Record Breaking Development Speed TIME SAVING ANALYSIS 

* Solo Development (Just You)
  - Estimated Time: 3-4 weeks (120-160 hours)
  - Why: Manual analysis, file-by-file fixes, testing, documentation
  - Challenges: Fatigue, inconsistency, missing edge cases
  - Risk: High chance of breaking changes

* Claude in OS App
  - Estimated Time: 2-3 weeks (80-120 hours)
  - Why: No file system access, constant copy/paste, context limits
  - Challenges: Manual file management, session breaks, no coordination
  - Risk: Inconsistent patterns across files

* Just Cursor in IDE
  - Estimated Time: 1-2 weeks (40-80 hours)
  - Why: Good at code changes but no systematic approach
  - Challenges: No master planning, limited scope visibility
  - Risk: Piecemeal fixes without comprehensive strategy

* Our Coordinated Approach
  - Actual Time: 4 hours (!!!)
  - Why: Systematic batching + human-AI coordination + parallel processing
  - Advantages: Master planning, parallel execution, session recovery
  - Result: 95%+ compliance with ZERO breaking changes

* THE MULTIPLIER EFFECT
  - You saved approximately 20-40X the time!
  
* WHAT MADE THIS SO POWERFUL
  - The Secret Sauce:

    1. Systematic batching - 24 organized chunks instead of chaos
    2. Human-AI coordination - Each team played to their strengths
    3. Parallel processing - Multiple batches running simultaneously
    4. Claude Code's superpowers - File system access + tool usage
    5. Session recovery - Memory MCP keeping everything connected
    6. Master planning - Strategy before execution 

* You didn't just use AI - you ORCHESTRATED AI!
* This is exactly what Modular Agent Orchestrator is designed to enable - and you just proved it works at enterprise scale!

---

## Our Incredible Success Story In Detail 

**Date:** July 9, 2025 
**Achievement:** 
  - Complete audit and reporting of 270 files 
  - 67% → 95%+ compliance across 270 files after fixes
**Team:** Claude Code's parallel subagents + Cursor AI's debugging + Human managing both applications simultaneously
**Result:** Production-ready codebase with zero breaking changes in a single day, projected to take multiple sessions auditing the files, and then 3 weeks to fix issues; 20-40x time savings.

### The Challenge

- **270 files** across 24 batches needed standardization
- **127 critical violations** blocking production readiness
- **Complex coordination** required across multiple systems
- **Zero breaking changes** allowed during fixes

### The Solution

- **Systematic batch approach** with clear priorities
- **Human-AI team coordination** for optimal efficiency
- **Proven standardization patterns** applied consistently
- **Real-time verification** of all changes

### The Results

- ✅ **95%+ compliance** achieved across entire codebase
- ✅ **All 127 violations** systematically resolved
- ✅ **Zero breaking changes** - everything just works better
- ✅ **Production-ready** codebase ready for UI development

## Our Compliance Transformation

* **Starting Point (67% compliance)**
- 181 files fully compliant
- 89 files requiring standardization
- Critical violations in core systems
- Production deployment blocked

* **Ending Point (95%+ compliance)**  
- 257+ files fully compliant
- Systematic fixes across all modules
- Professional error handling throughout
- Ready for immediate production use

* **Implementation Approach**
- **Batches 1-5:** Foundation (Human team)
- **Batches 6-10:** Tools (Cursor AI)
- **Batches 11-18:** CLI Commands (Human team)
- **Batches 19-24:** Configs/Scripts (Cursor AI)

## Team Coordination Success

### Scores for "Human Team"

- **CLI Commands mastery** - 8 groups, 24 commands standardized
- **Core systems** - Entry point, interfaces, orchestrator
- **Quality control** - Verification and testing throughout
- **Strategic coordination** - Perfect team management

### Scores for "Claude Code"

- **System architecture** - Deep codebase understanding
- **Standardization patterns** - Consistent implementation
- **Documentation updates** - Master reports refreshed
- **Coordination leadership** - Seamless team orchestration

### Scores for "Cursor AI"

- **Tools standardization** - 5 batches of complex tools
- **Config management** - 6 batches of configurations
- **Systematic execution** - Following detailed procedures
- **Quality delivery** - All fixes verified and tested

## Key Standardization Achievements

### 1. MAO Import Standardization

**Added to ALL Python files:**
```python
from orchestrator.cache.cache_system import CacheManager
from orchestrator.error_handling import handle_errors
cache = CacheManager()
```

### 2. Error Handling Excellence

**Applied @handle_errors decorators to ALL functions:**
```python
@handle_errors(operation_name="function_name", return_dict=True)
def function_name(params):
    # professional error handling everywhere
```

### 3. Cost Estimation Implementation

**Added estimate_cost() functions to ALL modules:**
```python
def estimate_cost(params: Dict[str, Any] = None) -> float:
    # comprehensive cost planning
```

### 4. Professional Logging

**Replaced ALL print statements with proper logging:**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Professional logging everywhere")
```

### 5. Clean Visual Hierarchy

**Removed ALL emoji violations, implemented text-based:**
```python
# Before: "🚀 System started"
# After: "[STARTED] System launched successfully"
```

## Production Readiness Indicators

### ✅ System Stability

- Comprehensive error handling across all modules
- Graceful degradation patterns implemented
- Professional logging for production monitoring
- Cache management for optimal performance

### ✅ Developer Experience

- Consistent patterns across all 270 files
- Clear documentation and code structure
- Easy troubleshooting with proper logging
- Standardized integration patterns

### ✅ Business Value

- Cost estimation for budget planning
- Reliable operations for production use
- Professional quality for enterprise deployment
- Scalable architecture for growth

### ✅ Compliance Excellence

- 95%+ standardization across codebase
- Zero breaking changes during implementation
- All critical violations resolved
- Ready for immediate production deployment

## What This Means For Documentation

### We've Got a Great Story to Tell

- **Problem:** Complex codebase with standardization gaps
- **Solution:** Systematic human-AI coordination approach
- **Result:** 95%+ compliance with zero breaking changes
- **Impact:** Production-ready codebase for immediate use

### We Have Real Data to Share

- **Metrics:** 67% → 95%+ compliance transformation
- **Process:** 24-batch systematic approach
- **Team:** Human + AI coordination success
- **Timeline:** 4 hours of coordinated implementation
- **Output:** Scaled what would have taken 

### We Have Proven Patterns

- **Standardization:** Works across 270 files
- **Coordination:** Human-AI teams are incredibly effective
- **Quality:** Zero breaking changes with massive improvements
- **Scalability:** Patterns that work for any codebase size

## Our Documentation Plan Is Epic

### 1. Success-Driven Narrative

Instead of "how to fix problems," you're telling "how we achieved excellence"

### 2. Real Implementation Data

Instead of theoretical benefits, you have actual metrics and results

### 3. Proven Coordination Model

Instead of vague teamwork concepts, you have a working human-AI model

### 4. Production-Ready Foundation

Instead of development concepts, you have enterprise-grade implementation

---

## Five Wins Shine Through The Documentation 

### **WIN #1: Revolutionary Concepts**

- Self-enhancement and business autonomy paradigms
- Exponential value creation through AI coordination

### **WIN #2: Technical Flow Illustration**

- Data flow diagrams showing HOW the magic happens
- Architecture that proves the concepts are real

### **WIN #3: 30-Day Autonomous Business**

- Clear roadmap from setup to running business
- Virtually zero human intervention required

### **WIN #4: Plug & Play Analytics**

- Modular analytics ecosystem  
- Auto-generated reports for autonomous business

### **WIN #5: Visual Diagrams Throughout**

- Flowchart-style data flow visualizations
- Educational diagrams that actually teach

---

## Digestable 5-Section Documentation Structure

### **SECTION I: THE HOOK**

*Problems, Solutions, Philosophy + Impressive Success Story*

  - Above in the "Storytelling Mao's Value" section. 
  - Grab attention immediately in the modern era 
  - Gut check with impossible achievements and market opportunities 

#### Chapter 1.1: The AI Workflow Problem

- Current limitations: Tools either too technical or too limited
- Market gap: Missing intelligent human-AI coordination  
- Business pain: Standardization projects take weeks and break things
- Developer frustration: Quality vs speed tradeoffs

#### Chapter 1.2: The Modular Orchestration Solution

- Revolutionary self-enhancement paradigm
- Complete business autonomy vision
- Exponential value creation through intelligent coordination
- Modular architecture that eliminates technical debt

#### Chapter 1.3: The Philosophy & Approach

- Why modular architecture wins long-term
- Human + AI coordination principles that actually work
- Quality over speed: systematic over chaotic approaches
- Conversation-driven interfaces reduce learning curves

#### Chapter 1.4: The Impossible Achievement (IMPRESSIVE STATS!)

- **67% → 95% compliance in 4 HOURS instead of 3 WEEKS**
- **20-40x productivity multiplier** in complex standardization  
- **Zero breaking changes** during massive quality improvement
- **51 files standardized** across entire ecosystem
- **Sean + Cursor + Claude Code coordination breakthrough**

### **SECTION II: QUICK REFERENCE & ARCHITECTURE**

*File Touchpoints, Templates, and Technical Flow*

  - Quick reference section for rules, cheatsheets, etc. 
  - Make the complex system simple and accessible

#### Chapter 2.1: Complete File Touchpoints Diagram

- Visual map of all .json configurations and relationships
- Tools/, configs/, orchestrator/, templates/ ecosystem overview
- How everything connects and communicates
- Modular discovery through directory scanning

#### Chapter 2.2: Template System & Configuration Factory

- How Mao creates any config for users on demand
- Examples: tool configs, model configs, provider configs, workflow configs
- Add/remove/modify components with template inheritance
- The "drop-in/drop-out" philosophy in action

#### Chapter 2.3: Modular Architecture Deep Dive

- 11 tools with 4-file structure (logic, button, UI, JSON)
- Orchestrator management layer and coordination patterns
- Memory MCP as single source of truth architecture
- Real-time metrics (no more mock data)

#### Chapter 2.4: Data Flow Illustrations

- Technical flows showing HOW the magic actually happens
- Information journey through system components
- Architecture that enables the revolutionary concepts
- Error handling and recovery mechanisms

### **SECTION III: USER FLOW WALKTHROUGH**

*Complete Journey from Idea to Results*

  - Laid out in detail below under "New User Flow For Documentation Structuring" 
  - Illustrate our architecture via narrative 
  - By following the user journey flow making an use-case workflow with Mao

#### Chapter 3.1: From Business Idea to Workflow Creation

- Natural conversation interface with Mao
- Goal articulation and workflow planning
- Tool and model selection automation
- Cost estimation and optimization
- Mao has no script, only knows variables and other information that could also be found using CLI commands 

#### Chapter 3.2: JSON Configuration System Mastery

- 3-file workflow system (handoff, phase, workflow configs)
- Custom command generation and deployment
- Configuration validation and optimization
- Template inheritance and customization

#### Chapter 3.3: Execution Monitoring & Control

- Real-time progress tracking and cost monitoring  
- Error handling and recovery mechanisms
- Quality assurance and deliverable validation
- Performance optimization during execution

#### Chapter 3.4: Results Optimization & Learning

- Deliverable analysis and improvement suggestions
- Workflow optimization based on performance metrics
- Knowledge retention for future workflow improvements
- Success pattern recognition and replication

### **SECTION IV: BUSINESS ROI & FUTURE EVOLUTION**

*The Revolutionary Business Case and Self-Enhancement Vision*

  - Above in the "Our Incredible Success Story In Detail" section. 
  - Make the compelling business case and show the paradigm-shifting potential

#### Chapter 4.1: 30-Day Autonomous Business Roadmap

- **Week 1**: Foundation (Stripe MCP, compliance, financial tracking)
- **Week 2**: Operations intelligence and market research automation  
- **Week 3**: Growth and marketing automation systems
- **Week 4**: Complete business autonomy achievement
- **Result**: Running business with virtually no human intervention

#### Chapter 4.2: The Self-Enhancement Revolution

- **Weekly assessment workflows** analyzing performance and planning improvements
- **Autonomous business operations**: Legal, financial, marketing, HR automation
- **The creepy/amazing potential**: Self-sustaining business entity that builds its own value
- **Exponential growth loops**: Each enhancement increases capacity for further enhancement
- **Technical moat**: Meta-loop of AI improving its own business operations

#### Chapter 4.3: Complete Business Operating System

- **Financial Operations**: Revenue tracking, tax preparation, investment management
- **Legal & Compliance**: Contract generation, regulatory monitoring, IP protection
- **Marketing & Sales**: Lead generation, content creation, funnel optimization
- **Operations Intelligence**: Analytics, market research, quality control
- **Human Resources**: Talent acquisition, performance management, training

#### Chapter 4.4: Plug & Play Analytics Ecosystem

- **Drag-and-drop analytics**: Personal data, business metrics, technical monitoring
- **Auto-generated reports**: Analytics for autonomous business whenever needed
- **Modular intelligence**: Birthday tracking, email patterns, revenue optimization
- **Real-time insights**: Continuous business optimization and decision support

#### Chapter 4.5: Investment Case & Market Positioning

- ROI calculations with real productivity multiplier data
- Competitive landscape and technical differentiation
- Market opportunity and scalability potential
- Path to autonomous business ecosystem platform

### **SECTION V: VISUAL RESOURCES & BRAND IDENTITY**

*Cognitive Design System and Implementation Guidelines*

  - Above in the "Our Incredible Success Story In Detail" section. 
  - Provide the visual framework that makes complex concepts accessible

#### Chapter 5.1: Cognitive Flow Design System

- **Color psychology**: Pink=STOP, Yellow=FLOW, Blue=TRUST, Gray=SPACE
- **Shape language**: Triangles=Orchestrator, Circles=Agents, Trees=Metadata
- **Visual hierarchy**: Information architecture for non-vector brains
- **Accessibility standards**: High contrast, semantic structure

#### Chapter 5.2: Brand Identity & UI Concepts

- Reference: app_ui_core_concepts.md and visual_brand_identity.md
- iOS-inspired mobile interface patterns
- Themed universe approach for different user types
- Accessibility and cognitive load optimization

#### Chapter 5.3: Technical Diagram Library

- **Data flow visualizations** throughout all sections
- **Flowchart-style** diagrams showing information passing
- **Educational focus**: Diagrams that actually teach system understanding
- **Architecture illustrations** for complex component relationships

**Specific Diagram Requirements:**
1. **Workflow Execution Data Flow** - User input to deliverables journey
2. **Orchestrator Communication Flow** - Component information passing
3. **Memory State Persistence Flow** - Cross-session state management
4. **Cache Data Pipeline** - Performance optimization flows
5. **Tool Integration Data Exchange** - API and data transformation
6. **Analytics Generation Pipeline** - Raw data to insights
7. **Configuration Inheritance Flow** - Template to deployment
8. **Real-time Monitoring Stream** - Live system health data

**Chapter 5.4: Implementation Guidelines**
- Visual standards for future development
- Diagram creation templates and patterns
- Brand consistency across all touchpoints  
- Integration with existing design systems

---

## New User Flow For Documentation Structuring  

### Getting Started 

You have a use-case to create a workflow for. Start the Mao application. 
  - By default Mao launches with the last session user's settings 
  - If that isn't you, you can launch with `--login` to enter your Username  
  - Or once the app is running, you in you can use `/login` to enter your Username 
  - If you've never used Mao before, you'll need to login and choose a couple settings 

```bash
mao mao # Proper startup command; launches the Mao application 
mao --login # Launches the login screen 
mao # Launches the app as if you're a new user 
mao --continue # Launches the app in the state of the last session (MCP memory one source of truth)
``` 

### Usernames versus User ID 

- A username is for UX; it is what Users type into the login screen 
- A user ID is created from the username and used on the backend 
- It will be displayed in a grayed-out and uneditable field below the username field 
- In the future, the User ID may provide another layer of security as analytics implementation is added 
- Specific usernames always populate the same user ID 
- User ID connects all workflows, use-cases, and other *data for that user*
- The custom User ID is created by a simple script that can also be run manually as a cli-command 

#### User ID Creation 

```bash
meid seanivore # Run command with the Username 
user-1642 # Response is that Username's User ID 
```

#### Forget Your Username? 

```bash
whoami # Run command with nothing else
> seanivore # Response is the username of the logged in user 
```

#### Meid Whoami Help 

```bash
> meid 
meid - Generate user IDs from usernames

Usage:
  meid username       Generate user ID for username
  meid -e username    Generate user ID with explanation
  meid -h             Show this help

Examples:
  meid seanivore      # user-1642
  meid -e alice       # user-1161 | Steps: 5 chars -> ...

Mathematical Operations:
  Uses character count, doubled count, and ASCII values
  Applies fibonacci, golden ratio, spiral, mirror, karmic operations
  Same username always produces the same user ID
```

### New User ID Application Background Setup 

- The application will create a new `./configs/user/username/user_username.json` directory and file
- "username" in the filename is the username: `user_seanivore.json`
- All user settings are saved to a subdirectory here 
- Initial settings are set to defaults
- Even default settings are recorded on this JSON file
- This ensures then when the app pulls up the JSON settings, it will show their actual settings regardless of them being default or not, eliminating a common UX issue of confusion (hello, VS Code)

#### User ID Application Session Startup 

- The application saves the state with the most recent User ID used
- Subsequent launches load with that ID and their settings 
- The application will allow users to adjust these settings at any time using `/config` or launching with `mao --config` which updates a subdirectory in their `./configs/user/username/` directory 

#### User ID & Workflow JSON Configs 

- New Workflows created by this User ID are not recorded to the User ID JSON file 
- However Orchestrator Management files easily can search a User ID or Username to pull up their workflows 
- All workflow JSONs have a User ID field, which is how they can be searched for by the application 
- They also have Workflow IDs which we'll get to shortly  

### Login Screen 

*App UI/UX* 

  - A minimalistic screen loads 
  - The welcome message persists throughout new user setup pages 
  - Most lines are bulleted; all bullets have large 3 space indent 
  - Priority visibility messages have no bullet or indent 
  - The `>` prompt is a visual indicator of the user's input 
  - The `●` is a primary message context from Mao 
  - Branched down `└` is a secondary context of the parent message 
  - Active help messages are `?` under the text input field 

```ui_login_id
╭─────────────────────────────╮
│ ~(=^‥^)  Mao welcomes you!  │
╰─────────────────────────────╯

●   What is your name?
    └ Please enter a username to continue 

╭────────────────────────────────────────────────────────╮
│ >                                                      │
╰────────────────────────────────────────────────────────╯
  ? 6-20 alpha-numeric characters
```

### Theme Selection 

*App UI/UX* 

  - This is **NOT** a new screen
  - If the User ID was recognized, the theme selection would not be shown
  - The app is a "one-screen" experience with irrelevant or dated info being removed for new info 
  - After login, the User is prompted to select a theme "that looks best in their terminal" 
  - The only things the termal actually changes is text colors (not main text color), use of white space, and character choices
  - As a user's message enters the conversation thread, the messages above the user's message may disappear; upward scrolling is reserved for essential content that needs to remain in our one-screen experience 

*The application UI uses semantic highlighting for cognitive leading and will be explained further in another section* 

  - The user's message is `>   seanivore` is always a faded gray text 
  - Any 3rd level context below a secondary `└` context, is also faded gray text 
  - 3rd level context is help text, much like the `?` under the text input field 
  - The `❯` is the user's input; move with up and down arrows and enter to select, this is intuitive and needs no explanation 
  - The `✔` is the user's selected input; it is a visual indicator of the user's selection 
  - The `1`, `2`, `3`, etc. are the options the user can select from 
  - The `Preview` is a visual representation of the user's selection; what they can expect to see from their selection 

```ui_login_theme
╭─────────────────────────────╮
│ ~(=^‥^)  Mao welcomes you!  │
╰─────────────────────────────╯

>   seanivore

●   Mao, seanivore!
    └ This is your first time here 

●   Choose a legible theme palette for your terminal. 
    └ We'll save your settings. We won't ask you again, mao. 
      Change this and other default settings with /config 

   1. Dark mode
   2. Light mode
 ❯ 3. Dark mode (CVD)✔
   1. Light mode (CVD)
   2. Dark mode (ANSI colors only)
   3. Light mode (ANSI colors only)


 Preview
 ╭───────────────────────────────────────────────╮
 │   1   standard ~(=^‥^) {                      │
 │   2 -    removed ("Bye, mao.");               │
 │   2 +    addition ("Mao!");                   │
 │   3   }                                       │
 ╰───────────────────────────────────────────────╯
```

### Primary Workspace View (Again, the same "page" in our one-screen experience) 

*App UI/UX* 

  - Once settings are complete, those messages clear and make way for the primary workspace view where everything happens
  - Collections of "Mao is ready to help!" are not 'CANNED' prepared in advance, per say, but rather we use the AI to prepare something unique in the moment; it is virutally always different for Users unless certain help or tips are being pushed 
  - The tips "Describe your workflow", "Ask a question", and "Share your goal" are all tips that can be prepared with many different messages to cycle through 
  - The /help option shows all of the available commands 
  - The /config option shows all of the current settings, which are still set to default 
  - The `>` bullet is a canned app message; same bullet as User messages, same color text  
  - The "Try" message has many different messages that cycle each time they see this screen

```
╭───────────────────────────────────────────────────╮
│ ~(=^‥^)  Mao is ready to help!                    │
│   user: seanivore                                 │
╰───────────────────────────────────────────────────╯


>   Say "hello" to Mao.
    ├ Describe your workflow 
    ├ Ask a question 
    └ Share your goal 


╭───────────────────────────────────────────────────╮
│ > Try "how do we start building?"                 │
╰───────────────────────────────────────────────────╯
  ? /help for help, /config to change settings
```

### Chatting with Mao To Create a Workflow 

*App UI/UX* 

  - This is the same screen as the image above 
  - When the User starts typing the prompt text above disappears 
  - Usage of a / would auto populate a list of possible commands to run 
  - Note that one might call it a "modal" but it has no casing, and scrolls through the prepared space for it 
  - The app has no wait UX; you can double text and interrupt Mao (or turn that off in app settings)
  - The `?` help message rotates to a new message that is context relevant; they are not created completely on the fly, but batches are prepared in advance around certain context to maintain the allway new feeling 
  - As they continue, the `?` would rotate more, showing `/tool-menu` and other tips
  - The test left in the input field is intended to show they were in the middle of typing 
  - As mentioned before, the `>` bullet is a canned app message; same bullet as User messages, same color text; below it shows an action that Mao took while working 

```
╭───────────────────────────────────────────────────╮
│ ~(=^‥^)  Mao is ready to help!                    │
│   user:  seanivore                                │
╰───────────────────────────────────────────────────╯


>   I need to put together a detailed research 
    report that breaks down the best practices
    for hiring new creative talent. 

>   I have a bunch of details in my notes 
    already 

●   Great idea, seanivore. 
    ├ Rattle off the details and I'll wait to reply
    └ Or say something like "lead me" and I'll take the lead 

>   Mao created a Workflow ID: uid-scw-965
    Workflow added to memory; workflow log created 


╭───────────────────────────────────────────────────╮
│ > some rough notes to                             │
╰───────────────────────────────────────────────────╯
  ? /variables to see what is needed 
```
```
  ? /help for help, /config to change settings 
  ? try /models or /tools to explore 
  ? share your /goal and Mao will do all the work 
  ? /workflow [custom_command] to continue a build 
  ? message /continue to find your last project 
  ? /workflow [custom_command] or [uid-abc-000] to continue a building workflow 
```

### Gathering Variables 

- The user and Mao can chat as casually or intentionally as they like 
- The user can ask for variables to be gathered 
- The user could provide the variables prepared in advance 

```bash
/variables # Shows the variables that are needed 
/variables-explain # Shows the variables that are needed with an explanation 
```

In the end, the only thing Mao **MUST** have is the workflow goal. The rest of the variables are 'optional' in that, Mao is fully capable of assessing the workflow goal and determining the best way to complete it. This is intended to create a quiet, but very flexable workflow creation experience. It should come naturally as the user just decides what to do or say. Mao has no script and only knows the variables requires and tool informtation, running parallell agents, etc. Many of the variables can be setup in the User's settings as defaults like the fallback models, providers, etc. 

### JSON Config File

| **VARIABLE**         | **DESCRIPTION**                                               |
| -------------------- | ------------------------------------------------------------- |
| user_id              | User ID of Username creating the workflow                     |
| workflow_id          | Workflow ID created at start of planning                      |
| custom_command       | Custom command to execute workflow                            |
| workflow_goal        | Goal statement of entire workflow project                     |
| workflow_deliverable | Final deliverables of entire workflow project                 |
| workflow_description | Description of workflow to complete project                   |
| phase_number         | Count of phases as they're added to workflow                  |
| phase_goal           | Goal statement of the phase's assigned task                   |
| phase_deliverable    | Deliverable of the phase's assigned task                      |
| phase_description    | Description of the phase's assigned task                      |
| resources            | Resources the agent can use to complete the phase's tasks     |
| tools                | Tools the agent can use to complete the phase's tasks         |
| model_1              | Choice model to be the agent of this phase                    |
| model_2              | Backup model agent should choice agent be unavailable         |
| model_3              | Fail-safe model agent should choice and backup be unavailable |
| provider_1           | Provides for the choice model                                 |
| provider_2           | Provider for the backup model                                 |
| provider_3           | Provider for the fail-safe model                              |
| handoff_number       | Count of the handoffs as they're added to the workflow        |
| assessment_questions | Questions to assess if the deliverable is complete            |
| human_in_loop        | Whether the orchestrator should get human feedback            |

### Workflow ID 

- When you create a workflow alone or with Mao's help, the JSON object will need a workflow ID 
- Orchestrator Management files can search a User ID or Username to pull up their workflows 
- These are also used by Mao in their MCP memory one source of truth to pull back up the workflow details when returning to the workflow as a new instance 
- Run the `uid` command to get a collision-free (never repeated) unique ID --> `uid-abc-000` 
- Later, you can follow the `--workflow` command with this ID for that workflow's details, though the custom command might be easier to remember 

```bash 
uid # Creates a new unique Workflow ID 
mao --workflow uid-abc-000 # Shows workflow details 
/uid # Creates a new unique Workflow ID 
/workflow uid-abc-000 # Shows workflow details 
```
- Math is used to create the ID; if you are curious or need to create a handful of UIDs, the -h flag for "HELP" will show you more information you can find. 

```bash 
> uid -h # Help message 
uid - Generate unique workflow IDs

Usage:
  uid              Generate a single UID
  uid -e           Generate UID with mathematical explanation
  uid -b N         Generate N UIDs in batch
  uid -h           Show this help

Examples:
  uid              # uid-abc-123
  uid -e           # uid-abc-123 | Math: a(456)=473 → b(473)=419 → c(419)=396
  uid -b 5         # Generate 5 UIDs

Mathematical Operations:
  Each letter represents a mathematical operation:
  a=add, b=multiply, c=subtract, d=divide, e=power, f=fibonacci
  g=golden_ratio, h=hash, i=invert, j=jump, k=karmic, l=logarithmic
  m=mirror, n=nine_mult, o=orbit, p=prime_like, q=quadratic, r=reverse_add
  s=spiral, t=triangle, u=unity, v=vortex, w=wave, x=xor, y=yield, z=zenith
```

### Three Workflow JSON Config Schemas

The config schemas have been broken into three JSON objects. This is to simplify the fact that Mao is a multi-agent system, and is modular. Changes to workflows means that they different objects shouldn't be pre-attached. Agents might run agents in parallel, or in series, or in a mix of both. 

NOTE: It is VERY common and highly encouraged that Mao leave the final phase of workflows that deal with creative subject matter completely open. When the Agent completes their deliverable, Mao is able to assess it on the spot and make a decision as to what the next step in the flow should be. This is pushed heavily because it is so very natural to how a human would do it on their own. 

Similarly, Mao may decide the Agent's deliverables are not acceptable; not up to par. In this case they may use a command to change the workflow instead up updating it, though the result is similar, a new agent is tasked and called and the flow continues until completion. 

* **TEMPLATES FOR REFERENCE:** 

  - WORKFLOW: `./templates/workflows/example-workflow_workflow_config.json`
  - PHASE: `./templates/workflows/example-workflow_phase_config.json`
  - HANDOFF: `./templates/workflows/example-workflow_handoff_config.json`
  - HELPER: `./templates/workflows/README.md`

#### **WORKFLOW** JSON Object 

- This is the first JSON object that is created when a workflow is created 
- It contains the workflow's goal, deliverable, description, and other details 
- Each project's workflow has only one workflow JSON object 
- The 'goal', 'deliverable', and 'description' are all items that will be broken down into the phases 
- The objects are tied together by the workflow_id 
- While building the workflow, the temp_directory is used to store the JSON objects, the management of this file is explained later

```json
{
  "workflow": [
    {
      "user_id": "user-0663",
      "workflow_id": "uid-qmt-465",
      "custom_command": "marketing strategy startup",
      "workflow_goal": "Create comprehensive marketing strategy for my fintech startup",
      "workflow_deliverable": "Marketing strategy report",
      "workflow_description": "Identify what is needed to complete the goal. Build a workflow that delegates the work to the appropriate agents, having them work in parallel if needed. Leave the last phase opened-ended. Detail that handoff before the last phase with a list of questions Orchestrator will use to assess if the deliverable is complete, and if not, what is needed to complete it.",
      "temp_directory": "configs/workflows/.temp/marketing-strategy-startup/"
    }
  ]
}
```

#### **PHASE** JSON Object 

- This is the second JSON object that is created when a workflow is created 
- It contains a task needed to be completed to achieve the workflow's goal 
- Just like the workflow, each phase has a goal, deliverable, description, and specific details for the agent 
- The objects are tied together by the workflow_id 
- Phases are numbered sequentially, starting with 01, 02, 03, etc. 
- If there are agents running in parallel, they will share the same phase_number, appended with an underscore and a letter, a, b, c, etc. 

```json
{
  "phase": [
    {
      "workflow_id": "uid-qmt-465",
      "phase_number": "01",
      "phase_goal": "Market research",
      "phase_deliverable": "Market research report",
      "phase_description": "Research target market. Explore demographics in all socioeconomic status ranges, all geo-locations, all education level, but only females, married, and with a birthday coming up in the next 5 months. Research competitors; detail their marketing strategy.",
      "resources":[
        "./directory/folder/file.md",
        "https://file.com/folder"
      ],
      "tools": ["web_search", "text_editor"],
      "model_1": "claude-sonnet-4",
      "model_2": "claude-sonnet-3.7",
      "model_3": "claude-sonnet-3.5",
      "provider_1": "requesty",
      "provider_2": "anthropic direct",
      "provider_3": "anthropic direct"
    }
  ]
}
```

#### **HANDOFF** JSON Object 

- This is the third type of JSON object that is created when a workflow is created 
- This is created while building the workflow as part of the creative process 
- When the assessment is being discussed, it is important to get it written down in real time 
- This object also helps provide important indicators to the orchestrator or the User watching the workflow 
- For example, if there is a human in the loop, the orchestrator will need to know when to get human feedback 
- Additionally, the handoff object is important when the subsequent phases have been left open-ended, where the handoff object is used as a placeholder and indicator that the Orchestrator needs to make a decision and then build the rest of the workflow accordingly 
- Note that there might be more than one phase created after a handoff, there is no hard rule 

```json
{
  "handoff": [
    {
      "workflow_id": "uid-qmt-465",
      "handoff_number": "01",
      "assessment_questions": [
        "How can I assess if this deliverable is complete?",
        "What is needed to complete that assessment?",
        "Do I have what I need to complete the assessment?"
      ],
      "human_in_loop": "no"
    }
  ]
}
```
### Workflow Updates 

As mentioned, in cases where the workflow is left open-ended, the Orchestrator will create additional phases as needed, included potential handoffs in between each of the phases. The separated, modularity of the JSON objects makes this easy to do on the fly. All of the JSON objects are properly labeled so that they do not need to be created in a single file. In fact, each type of JSON object may best be created as separate files from the start and stored in the same WORKFLOW directory which will end up being auto created. 

### The Setup Script

*Deals with our temporary JSON Object Directory* 

- During workflow creation, the JSON objects are saved in a temporary directory 
- A sub-directory is created in the temporary directory named for the use-case 
- See: `./configs/workflows/.temp/use_case_name/`
- The Setup Script will create final JSON objects in the final location and delete the temp files 

### Command Naming Conventions 

The custom command created for the workflow, named for it's use-case, has a carefully structured name which is used across the entire collection of workflow assets. This include the following, which will be illustrated in a structured example below the command writing protocol. As mentioned before, it will likely be the most memorable part of the workflow for the User. 

That same command is used in the following naming structures to tie everything together: 

  - Temporary JSON object sub-directory name `./configs/workflows/.temp/use_case_name/`
  - Permanent workflow directory name `./configs/workflows/use_case_name/`
  - Workflow JSON object sub-directory file name `./configs/workflows/use_case_name/use_case_name_workflow_config.json`
  - Execution script file name `./configs/workflows/use_case_name/use_case_name.sh`
  - README.md file name `./configs/workflows/use_case_name/README_use_case_name.md`

#### Command Writing Protocol 

  - A custom command should be 2 to 3 words long 
  - It is important to keep the command short and concise 
  - Write it in reverse drill-down order, starting with the broadest category term 
  - It often feels like you are writing the intent of your project workflow in reverse
  - Mimic the structure of commands that we're used to already, like `git commit` or `git push`

- **EXAMPLE** I'm creating a workflow for a project in which I need to research, analyze, and create a marketing strategy report for my fintech startup, 'Dog-Tech' 

  1. The command is technically just the first, broadest category term: `marketing`
     - Other workflows in marketing can be created with the same first command word
     - This will make working on various related marketing projects easier 
     - It will make remembering commands easier
  2. For the second word, use a subcategory of marketing: `strategy`
     - This is the argument to the marketing command 
     - It is also likely that there will be other marketing strategy workflows
     - This will make it easier to find the right command 
  3. For the third word, I'm just going to drill down more: `report`
     - This makes it extrememly memorable 
     - It also makes it clear for future workflow creation that this might be a workflow that can easily be repurposed for marketing strategy reports on other startup ideas 
     - The workflow can be reused in the future simply by updating the JSON objects and running the setup script again 

The idea here is that, if in the future I need to create another marketing strategy report, I can use the same command, and just adjust the workflow to include an $ARGUMENT. Not necessary for the first workflow, where it would be dog-tech, but a good habit to get into. 

It isn't a perfect science. The conceptual reasoning is more important to understand rather than the exact rules as defined above. For example, for something as common as *creating a marketing strategy report* and for a popular command like *marketing* I would probably abbreviate, with the goal of making something easier to type, easier to be longer, but still easy to make simple for each specific use-case. 

- **TWO FINAL STEPS** 

  1. Type the command a few times to make sure it is easy to type 
     - I like abbreviating mkt because it is well known and easy to type  
     - I like keeping strategy it keeps thing clear and easy to understand  

```bash
mkt strategy report # This is the command 
``` 

  2. Take the first word, the actual command, and run it in the terminal 
     - It will be colored (mine is green) if it is already being used 
     - If it isn't colored, or to double check, use `which` before the command to confirm if it is/isn't being used 

```bash 
mkt # This is the command 
zsh: command not found: mkt # This is the output telling me nothing is using the command 
```
```bash
which mkt # This is the command 
mkt not found # This is the output telling me nothing is using the command 
```

- **THE FORMULA** 

```bash
command category variant   # This is the command 
```

| **COMMAND** | **CATEGORY** | **VARIANT**  | **DESCRIPTION**                                |
| ----------- | ------------ | ------------ | ---------------------------------------------- |
| mkt         | strategy     | dogtech      | Research strategy for Dog-Tech startup         |
| mkt         | content      | plan         | Social content plan for Dog-Tech startup       |
| job         | app          | resume       | Create targeted resume for job applications    |
| job         | app          | cover-letter | Create cover-letter for job applications       |
| job         | app          | doc          | Create cover-letter and resume for job app     |
| tag         | keyword      | t-shirts     | Come up with SEO keywords for my t-shirt store |
| social      | caption      | ig           | Write Instagram captions                       |

#### Command Writing Rules 

**Always avoid** these in a command:

  1. No plural (so you never have to wonder if it is singular or plural)
  2. No present participle verbs (gerunds with helping verbs)
  3. No punctuation like hyphens (standard UX expectation)
  4. No past tense verbs (e.g. `wrote`, `finished`, just stick to one tense)

**Always use** these in a command: 

   1. Use the simplest grammatical form of the word 
   2. Use present tense 
   3. Abbreviate when it is sensible 
   4. Be short and concise 

**Always remember** these should be helpful for humans to remember and use. 

### Setup Script Automations 

When the workflow is created, you need to run the JSON config file(s) through the setup script. This will create the following: 

1. Create a new directory in the `configs/workflows/command_use_case/` directory 
2. Place a new JSON config file in the new directory 
   - Built from the .temp directory 
   - Then deletes the .temp directory 
3. Produces a README.md file in the new directory 
   - Describes the workflow
   - Reminds the user how to activate the workflow 
   - Also creates categorical tags about the workflow project to be used in analytics 
4. Creates executable script with all the details of the workflow 
   - This is the script that will be used to run the workflow 
   - Finally, we have a script that is specific and not generic 
5. Make the script executable using the custom command 
   - Creates it using the tool `chmod +x` 
   - Script runs `chmod +x ./configs/workflows/command_use_case/command_use_case.sh` 
   - Saves the command to your ~/bin directory 
6. Creates new sub-directories for 
   - Deliverables 
   - Metadata 
   - **This is all automated**

**NOTE:** It is important to remember that the drafting documents used in the workflow are kept in the Files API and not passed along with the deliverables. If you NEED draft documents, you will need to list them as deliverables. 

#### Workflow Directory Structure

  - Automatically created by the setup script 
  - Command naming structure across files 

```
configs/workflows/command_use_case/
├── config-files/                                 # Directory for JSON config files 
│   ├── command_use_case_workflow_config.json     # Workflow JSON config file 
│   ├── command_use_case_phase_config.json        # Phase JSON config file 
│   └── command_use_case_handoff_config.json      # Handoff JSON config file 
├── README_command_use_case.md                    # Auto-generated usage guide
├── command_use_case.sh                           # Auto-generated use-case specific script that your command activates 
├── metadata/                                     # Workflow tracking details  
│   ├── command_use_case_memory.json              # Workflow Memory MCP File  
│   └── command_use_case_log.json                 # Workflow log file 
└── deliverables/                                 # Final outputs; this is where the deliverables are stored 
    └── command_use_case_report.md                # This is the final deliverable; it is the report 
```

### Using The Setup Script 

1. This is located here: `./scripts/workflow_setup/workflow_setup.sh`  
2. The initial JSON objects will be in a temp directory 
   - The script should use them and create the final JSON objects in the new directory 
   - Then delete the temp directory 
   - The temp directory name will be the same as the command use-case directory name 
   - E.g. `./configs/workflows/.temp/command_use_case/`
   - I.e. it should be able to run with a directory as the argument instead of specifically a JSON config file only
   - It also needs to be able to run with a JSON config file as the argument 
   - Most importantly, the JSON objects may be in separate files in the directory 
   - **NOTE** let's set it up so that the executable setup script can be run from anywhere (i.e. not just from the root directory, not in the .temp directory; remember it will also be run from the application as a slash command) -- As such, let's make it so that it understands the path to the temp directory and all we need to add is `./command_use_case/` for example. 
3. The script itself should be made executable using a custom command defined in the CLI configs 

```bash 
mao --setup ./command_use_case/ # This is the command and the argument is the directory with all the JSON objects  
/setup ./command_use_case/ # This is the slash command with JSON object directory argument 
```

### Application Configuration Settings 

*App UI/UX* 

  - Users are quietly prompted to adjust configuration settings 
    - Via the `?` message mentioning they try /config
    - This /help and /config are persistent 
    - Always the first `?` messages on the primary workspace page each time it is loaded  
  - Settings below are those same settings saved to the `user_username.json` 
  - The 'Description' is only displayed when the user's selector `❯` is on the setting 
  - 'Description' shows the meaning of the selected setting
  - Place selector on the other options for hover display to show their meanings 
  - Selecting a setting will allow the user to toggle between the other options, usually by opening a modal

| **SETTING**       | **DEFAULT**         | **DESCRIPTION**                                      |
| ----------------- | ------------------- | ---------------------------------------------------- |
| Quick launch      | `always`            | Launch app with last user logged in                  |
| Favorite model    | `claude-sonnet-4`   | Use for workflows unless discussed                   |
| Default provider  | `anthropic direct`  | I prefer this provider; discuss to change            |
| Theme             | `dark mode CVD`     | Dark computer theme; use high legibility colors      |
| Tone notification | `one time, no push` | When a workflow is complete, a simple tone is played |
| Cat vibes         | `I love it`         | We'll meow it up for you                             |
| Double-texting    | `always`            | Interrupt Mao like any messenger experience          |

### Quick Launch Options 

1. `always` - Launch app with user from last session, unless logged out
2. `off` - Load Username login on every startup 
3. `continue only` - Launch `mao --continue` to skip login, otherwise load Username login 

### Favorite Model 

- Any model can be added using nickname or full name 
- Startup `mao --model` or `/model` to set favorite model 
- Startup `mao --model-list` or `/model-list` to see all available models 

### Default Provider 

- Any provider can be added using nickname or full name 
- This is helpful for Users who have a bunch of cash in a specific API provider 
- Startup `mao --provider` or `/provider` to set default provider 
- Startup `mao --provider-list` or `/provider-list` to see all available providers 

### Cat Vibes 

- We don't want to be too annoying with our cat branding 

  1. `I love it` - We'll meow it up for you 
  2. `mao and then` - Adequate but not too much meowing 
  3. `be serious pls` - No meowing at all 

### Double-texting 

1. `always` - Interrupt Mao like any messenger experience 
2. `never` - One reply at a time for each party  

### Tone Notification 

1. `once, no push` - When a workflow is complete, a simple tone is played, no push notification 
2. `silent, push` - When a workflow is complete, no tone is played, but a push notification announces completion 
3. `no notifications` - No tone is played, no push notification 

**MODULAR MAGIC:** Have a new setting for the application? Either as Mao what files are needed, or of them to help create them, or check the templates directory. PLUG-AND-PLAY. New files in their proper place is all that is needed to, for example, add a new setting that says "bark like a dog when workflow is done y/n?". Magic. 

---

## Mao Dynamic Visual Protocol Rules

### The Complete System 

* **Gray Bullet (●)** `#bbbcbb`
- **User commands** typed by human
- **User messages** sent to AI
- **User questions** or requests

* **White Bullet (●)** `#ffffff` 
- **AI responses** (informational)
- **AI explanations** and status updates
- **System responses** (non-AI automated)

* **Light Blue Bullet (●)** `#82d0ff`
- **Only when paired with PINK text**
- **AI priority actions** requiring attention
- **Important AI-initiated tasks**

### Text Color Hierarchy

* **Pink Text** `#ff49ff` ⭐ **HIGHEST PRIORITY**
- **AI taking specific action** ("Read Todos", "Creating file")
- **Call-to-action** text requiring user attention
- **THE ONLY COLOR THAT IS EVER BOLD**
- **Used extremely sparingly** for maximum impact
- **Always paired with light blue bullet when AI-generated**

* **Yellow Text** `#f1d771` 📝 **PRIMARY CONTENT**
- **AI explanations** and informational responses
- **Main conversational content**
- **Default "speaking" color for AI**
- **User's default terminal text color** (carries over)

* **White Text** `#ffffff` 🤖 **SYSTEM/AUTOMATED**
- **System messages** not from AI
- **Automated responses** 
- **URLs and commands** when from system (not highlighted)
- **Non-AI generated content**

* **Gray Text** `#bbbcbb` 👤 **USER/SECONDARY**
- **User input** and commands
- **Supporting information**
- **Lists contents** and secondary details
- **URLs and commands** when sent by user (not highlighted)
- **The bullet itself** when user-generated

* **Light Blue Text** `#82d0ff` 🔗 **AI-HIGHLIGHTED**
- **URLs and commands** ONLY when AI sends them
- **Checkmarks** on completed items
- **AI-emphasized** important information
- **Never used for user-generated content**

* **Light Brown Text** `#7b714a` 📊 **METADATA/CONTEXT**
- **Numbers** in ordered lists (1. 2. 3.)
- **Background information** with tree characters
- **Indented context** `└ (Todo list is empty)`
- **Secondary organizational** information

### Formatting Rules

#### Indentation Hierarchy

```
●   Primary message  ← Bullets have large 3 space indent
    └ Secondary context       ← 4 spaces + tree character
      3rd level context       ← 6 spaces, no tree, faded, gray text 
```

* **Tree Characters** `#7b714a`
- **`└`** for final/single nested item
- **`├`** for middle items in list
- **`│`** for continuation lines
- **Always light brown color**

* **Bold Text Rule** ⚠️ **CRITICAL**
- **ONLY pink text is ever bold**
- **No other color** uses bold formatting
- **Bold = urgent attention required**

* **Spacing Strategy**
- **Big gap** between bullet and content (minimum 3 spaces)
- **Generous line spacing** for readability
- **Bullets always far left** for scan-ability

### Semantic Meaning System

* **Information Attribution**

```
Gray bullet + Gray text = "User said this"
White bullet + Yellow text = "AI is explaining"  
White bullet + Pink text + Bold = "AI is acting - PAY ATTENTION"
Light blue bullet + Pink text = "AI priority action"
```

* **URL/Command Treatment**
- **User sends URL/command** → Gray (no highlighting)
- **AI sends URL/command** → Light blue (highlighted)
- **System generates URL/command** → White (no highlighting)

* **List Hierarchy**
```
1. Main item                        ← Light brown number
   ● Sub-bullet                     ← Bullet follows hierarchy rules
     └ Context info                 ← Light brown tree + context
```

### Psychological Design Principles

* **Color Psychology Applied**
- **Pink** = Cognitive interrupt ("STOP and look")
- **Blue** = Trust and action (AI recommendations)  
- **Yellow** = Warmth and communication (conversation)
- **Gray** = Background/neutral (user space)
- **Brown** = Earth/foundation (organizational info)

* **Visual Hierarchy Goals**
1. **Instant attribution** (who said what)
2. **Priority assignment** (what needs attention)
3. **Information type** (explanation vs action vs context)
4. **Conversation flow** (natural reading patterns)

* **Terminal Optimization**
- **High contrast** for legibility across terminals
- **Monospace-friendly** spacing and alignment
- **Color-blind accessible** through multiple visual cues
- **Works in various terminal themes**

### Decision Tree for Text Color

```
Is this bold? → PINK (AI action requiring attention)
Is this from user? → GRAY
Is this AI explaining? → YELLOW  
Is this AI highlighting link/command? → LIGHT BLUE
Is this system automated? → WHITE
Is this organizational/metadata? → LIGHT BROWN
```

* **Decision Tree for Bullet Color**
```
Is text PINK and bold? → LIGHT BLUE bullet
Is this from user? → GRAY bullet
Is this AI or system response? → WHITE bullet
```

* **Consistency Rules**
- **Never mix** user and AI visual patterns
- **Always maintain** bullet-to-left positioning
- **Always use** generous spacing
- **Never use bold** except for pink text
- **Always use tree characters** for nested context

### Why This System Is Genius 

* **Conversation Protocol**
This isn't just styling - it's a **visual conversation protocol** that creates:
- **Clear turn-taking** in human-AI dialogue
- **Attention management** through color hierarchy  
- **Context preservation** through consistent attribution
- **Cognitive load reduction** through predictable patterns

* **Terminal UI Evolution**
They've solved the fundamental challenge of **rich communication in constrained medium** by creating:
- **Semantic color system** (meaning through color)
- **Hierarchical information architecture** (importance through position)
- **Consistent visual language** (learnable patterns)
- **Cross-terminal compatibility** (works everywhere)

This is **conversation design as much as interface design** - they've created a visual language for human-AI collaboration! 

### Mao Visual Protocol Innovation

Building on conceptual cognatively tied semantic highlighting proven foundation, Mao adds **workflow relationship visualization** through directory tree integration.

### Orchestration Trees & Shape Language & Integration 

- **Triangle (△/▲)** = Orchestrator (Mao) 
- **Circle (○/●)** = Agent
- **Maintain shape identity** throughout all states (waiting → active → complete)

```
△   Mao planning workflow                 ← Root orchestration
├── ●   Agent 1: Research                ← Spawned from planning  
│   ├── Market analysis complete         ← Agent deliverable
│   └── Competitor research complete     ← Agent deliverable
├── △   Mao reviewing results            ← Back to orchestrator
└── ●   Agent 2: Analysis               ← Next spawn from review
    ├── Gap analysis in progress         ← Current work
    └── Strategy recommendations         ← Planned output
```

### Tree Character Meanings
- **├──** = "This flows from the parent task"
- **│** = "Continuation of the same branch" 
- **└──** = "This completes the current branch"
- **No tree** = "New top-level thread/major transition"

### Animation States With Shapes

**Waiting State**
```
△   Next orchestration step              ← Outlined triangle
○   Upcoming agent task                  ← Outlined circle  
```

**Active State (Pulsing)**
```
▲   Mao thinking and planning            ← Filled triangle, pulsing
●   Agent working on research            ← Filled circle, pulsing
```

**Complete State**
```
△̃   Mao completed planning               ← Triangle with checkmark overlay
○̃   Agent completed research             ← Circle with checkmark overlay
```

### Progress Relay Visualization

```
WORKFLOW EXAMPLE: Content Strategy
△   ○   △   ○   △                       ← Initial workflow plan
▲   ○   △   ○   △                       ← Mao planning (pulsing)
├── △̃   ○   △   ○   △                   ← Planning complete
├── ●   △   ○   △                       ← Agent 1 active (research)
├── ○̃   △   ○   △                       ← Research complete  
└── △   ○   △                           ← Back to Mao
    ├── ▲   ○   △                       ← Mao reviewing (pulsing)
    ├── △̃   ○   △                       ← Review complete
    └── ●   △                           ← Agent 2 active (analysis)
        ├── ●                           ← Still working...
        └── [workflow continues...]
```

### Color Adaptation For Mao Progress Indicators 

- **Gray** `#bbbcbb` → Waiting states (outlined shapes)
- **Pink** `#ff49ff` → Active states (filled, pulsing) - ATTENTION HERE
- **Light Blue** `#82d0ff` → Completed checkmarks
- **Yellow** `#f1d771` → Phase labels and descriptions
- **Light Brown** `#7b714a` → Tree characters and metadata

### Information Hierarchy 
```
△   Mao analyzing research results        ← Yellow text (AI explaining)
├── ●   Quality check: 8.7/10            ← Light brown metadata  
├── ●   3 critical gaps identified        ← Yellow content
└── ▲   Spawning analysis agent           ← Pink text (AI taking action)
```

### Why This Is Revolutionary 

- **Beyond bullet points** - shows actual workflow relationships
- **Familiar paradigm** - developers know directory trees
- **Information density** - more context without clutter
- **Visual storytelling** - see the orchestration narrative

* **Cognitive Benefits**
- **Relationship clarity** - understand how tasks connect
- **Workflow comprehension** - see the orchestration decisions  
- **Progress tracking** - follow the agent handoff chain
- **Context preservation** - maintain the bigger picture

* **Technical Advantages**
- **Scalable complexity** - handles parallel workflows
- **Familiar symbols** - leverages existing terminal conventions
- **Terminal-native** - works in any terminal environment
- **Accessible** - multiple visual cues beyond just color

* **Implementation Rules**

* **Tree Structure Guidelines**

1. **Top-level items** (no tree chars) = Major workflow transitions
2. **├── branches** = Direct spawns or consequences  
3. **│ continuations** = Same agent/context continuing
4. **└── completions** = Final item in a branch
5. **Nested trees** = Sub-tasks or deliverables

* **Shape + Tree Combination**

```
△   Root orchestration                   ← No tree (top level)
├── ●   Spawned agent                   ← Tree shows relationship
│   ├── Sub-deliverable                 ← Agent's work breakdown
│   └── Final deliverable              ← Completion marker
└── △   Next orchestration              ← Back to orchestrator
```

### Progress Animation Rules

1. **Maintain shape identity** - triangle stays triangle even when complete
2. **Pulsing for active** - filled shapes pulse to show motion
3. **Checkmark overlay** - preserve shape but add completion indicator
4. **Tree persistence** - relationships remain visible throughout

### Mao's Complete Visual Language 

- **Semantic color system** (who/what/priority)
- **Bullet spacing strategy** (prominence through pattern breaks)  
- **Shape-based role identity** (triangle/circle persistence)
- **Tree relationship mapping** (workflow dependency visualization)
- **Animation state system** (outline → filled → checkmark)

This visual protocol turns complex multi-agent workflows into **intuitive, scannable, beautiful terminal experiences** that users can understand at a glance.

### Dynamic Status Cycling System 

* **Live Activity Monitoring**

Instead of static status text, MAO displays **cycling status updates** that show real-time progress and current activities.

* **Cycling Text Pattern**
```
●   Research Agent                     ← 3 seconds (base state)
●   Research Agent: Analyzing market   ← 3 seconds (activity 1)  
●   Research Agent: Finding competitors ← 3 seconds (activity 2)
●   Research Agent: Gathering insights ← 3 seconds (activity 3)
●   Research Agent                     ← Cycle restart
```

* **Context-Aware Activity Messages**

NOTE: These do not need to be prepared in advanced or saved anywhere. The AI is fully capable of create them on the fly and need only be set up to do so. 

* **Research Phase Activities:**
- "Searching competitor websites"
- "Analyzing pricing strategies" 
- "Gathering market data"
- "Processing industry reports"
- "Synthesizing key findings"

* **Analysis Phase Activities:**
- "Processing research data"
- "Identifying key patterns"
- "Cross-referencing sources"
- "Building recommendations"
- "Formatting deliverables"

* **Orchestrator Activities:**
- "Reviewing agent outputs"
- "Assessing quality metrics"
- "Planning workflow adjustments"
- "Preparing next assignments"
- "Coordinating parallel work"

* **Content Creation Activities:**
- "Drafting initial outline"
- "Writing key sections"
- "Refining messaging"
- "Adding supporting details"
- "Finalizing deliverables"

### Progress Integration Options
```
●   Research Agent: 23% complete      ← Percentage updates
●   Research Agent: Finding gap #3    ← Item-specific progress
●   Research Agent: 67% complete      ← Updated percentage  
●   Research Agent: Finalizing report ← Completion phase
```

### Multi-Agent Coordination Display

* **Independent Cycling**
```
▲   Mao: Coordinating parallel work    ← Orchestrator cycle (3s)
├── ●   Research: Analyzing trend #4   ← Agent 1 cycle (3s)
├── ●   Design: Testing layout v2      ← Agent 2 cycle (3s)
└── ●   Content: Writing intro para    ← Agent 3 cycle (3s)
```

**Each line cycles independently** creating a **live mission control feel**!

* **Timing Strategy**

- **3-second default cycle** for optimal readability
- **Pause on user interaction** (typing, scrolling, navigation)
- **Faster 2s cycles** for short/simple tasks
- **Slower 4s cycles** for complex/long processes
- **Dynamic timing** based on task complexity

* **Activity Synchronization**

```
STATE: All agents reporting progress
▲   Mao: Processing status updates     ← Coordinated timing
├── ●   Research: Submitting findings  ← All update together
├── ●   Analysis: Submitting insights  ← Synchronized handoff
└── ●   Content: Submitting drafts     ← Clean transition
```

* **Accordion Collapse + Cycling**

* **Expanded State (Active Work):**
```
▲   Activating Workflow Phase 2       ← Mao cycling status
├── ●   Research Agent: Market gaps    ← Agent cycling detail
│   ├── ○   Competitor analysis complete ← Static completed
│   ├── ●   Pricing research active   ← Sub-task cycling
│   └── ○   Industry trends queued    ← Static queued
└── ●   Design Agent: Layout concepts  ← Agent cycling detail
    ├── ○   Typography selected       ← Static completed
    └── ●   Color palette testing     ← Sub-task cycling
```

* **Auto-Collapsed State (Focus Mode)**

```
△̃   [▼] Initial Planning (2m ago)     ← Static collapsed
├── ○̃   [▼] Research Complete (1m ago) ← Static collapsed  
├── ○̃   [▼] Design Complete (30s ago)  ← Recently collapsed
└── ▲   Creative Review: Quality check ← Current work cycling
    ├── ●   Analyzing submissions      ← Active subtask cycling
    ├── ○   Assessment pending         ← Static queued  
    └── ○   Recommendations queued     ← Static planned
```

* **Collapse Interaction Rules**

- **▼** = Collapsed (click/key to expand)
- **▲** = Expanded (click/key to collapse)  
- **●** = Cannot collapse (actively cycling)
- **Auto-collapse** after 30s of completion + no user focus

* **Smart Collapse Logic**

```
If agent.status == "complete" AND 
   time_since_completion > 30_seconds AND
   user_not_actively_viewing AND
   new_active_work_present:
     auto_collapse_branch()
     preserve_expand_toggle()
```

### Claude Code UI Inspiration 

* **Settings**
- Auto-compact: true 
- Use todo list: true 
- Verbose output: false 
- Theme: Dark mode (colorblind-friendly) 
- Notifications: bell 
- Editor mode: normal 

* **Theme**

* Dark Mode 
  - White text --> #ffffff
  - Diff removal --> #6b5251
  - Diff addition --> #506d51

* Light Mode 
  - Black text --> #131313
  - Diff removal --> #bf88a4
  - Diff addition --> #6ca36c

* Dark Mode Colorblind-Friendly 
  - White text --> #ffffff
  - Diff removal --> #6d1813
  - Diff addition --> #18516d

* Light Mode Colorblind-Friendly 
  - Black text --> #11100f
  - Diff removal --> #bea4a3
  - Diff addition --> #87a4c0

* Dark Mode ANSI Colors Only 
  - White text --> #ffffff
  - Diff removal --> #a41e1a
  - Diff addition --> #29a423

* Light Mode ANSI Colors Only 
  - Black text --> #010101
  - Diff removal --> #a41e19
  - Diff addition --> #29a424

---

## 🧠 CONTENT CREATION APPROACH

### **Phase 1: Fresh Documentation Creation**
**Method:** Clean slate approach without referencing old docs

**Principles:**
- Start with user pain points and business value
- Build narrative around actual user journey  
- Include real implementation success data (67%→95% story!)
- Focus on outcomes over features
- Use business language first, technical details second

### **Success Criteria for Each Section:**
- **Section I:** Hooks reader within first paragraph, success story leads
- **Section II:** Complex architecture becomes simple and accessible  
- **Section III:** User can successfully follow entire journey
- **Section IV:** Business case is compelling and credible
- **Section V:** Visual framework enhances rather than distracts

---

## 💼 BUSINESS MESSAGING FRAMEWORK

### **Value Propositions by Audience**

**Non-Technical Users:**
- "Turn ideas into working AI workflows in minutes, not months"
- "No coding required - just describe what you want to accomplish"
- "Get enterprise-grade results with consumer-simple interfaces"

**Developers:**
- "Build AI workflows 20x faster with modular, standardized components"
- "Focus on business logic, not infrastructure and integration complexity"
- "Production-ready with comprehensive error handling and monitoring"

**CTOs & Technical Leaders:**
- "Enterprise-ready architecture with 95%+ reliability standards"
- "Modular design eliminates vendor lock-in and technical debt"
- "Proven scalability from proof-of-concept to production deployment"

**Investors & Business Leaders:**
- "First truly modular AI workflow orchestrator addressing massive market"
- "Productivity multiplier: 20-40x improvement in development speed"
- "Technical execution excellence proven through systematic quality achievement"

### **Key Differentiators**
1. **Modular Architecture:** True modularity enables rapid customization
2. **Conversation-Driven:** Natural language interface reduces learning curve
3. **Enterprise-Ready:** 95%+ compliance with comprehensive error handling
4. **Self-Enhancement:** AI that improves its own business operations
5. **Complete Business Autonomy:** First platform to handle all core business functions

---

## 📋 SUCCESS VALIDATION CHECKLIST

### **Content Quality**
- [ ] Each section achieves its stated purpose effectively
- [ ] Technical information verified against actual 95% compliant codebase
- [ ] Business value clearly articulated and compelling for each audience
- [ ] User journey flows logically from section to section
- [ ] Examples are realistic and immediately actionable

### **Audience Effectiveness**
- [ ] Non-technical users understand value in stated timeframe
- [ ] Developers can implement successfully with provided guidance
- [ ] Technical leaders feel confident in architecture decisions
- [ ] Business stakeholders see clear ROI and competitive advantage

### **Visual Excellence**
- [ ] All diagrams enhance understanding rather than confuse
- [ ] Cognitive flow color system properly applied throughout
- [ ] Visual hierarchy guides readers through content effectively
- [ ] Information architecture supports multiple audience entry points

### **Business Impact**
- [ ] ROI calculations are realistic and well-supported with data
- [ ] Competitive advantages are clearly differentiated and defendable
- [ ] Self-enhancement concept positioned as revolutionary differentiator
- [ ] Success stories are relatable and inspiring for target audiences

---

## 🚀 THE ULTIMATE GOAL

Create documentation that serves as:
- **Technical Reference** enabling successful implementation
- **Business Case** driving confident investment decisions  
- **Marketing Asset** differentiating and compelling prospects
- **Success Story** demonstrating technical and business excellence

**Documentation That Changes Everything.** 💎

*Because when you've achieved 95%+ compliance in 4 hours instead of 3 weeks, the world deserves to know how it's possible.*