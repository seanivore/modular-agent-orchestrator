# Mao Dynamic Visual Protocol Rules

## **THE COMPLETE SYSTEM** 🎯

### **BULLET POINT ASSIGNMENT RULES**

#### **Gray Bullet (●)** `#bbbcbb`
- **User commands** typed by human
- **User messages** sent to AI
- **User questions** or requests

#### **White Bullet (●)** `#ffffff` 
- **AI responses** (informational)
- **AI explanations** and status updates
- **System responses** (non-AI automated)

#### **Light Blue Bullet (●)** `#82d0ff`
- **Only when paired with PINK text**
- **AI priority actions** requiring attention
- **Important AI-initiated tasks**

### **TEXT COLOR HIERARCHY**

#### **Pink Text** `#ff49ff` ⭐ **HIGHEST PRIORITY**
- **AI taking specific action** ("Read Todos", "Creating file")
- **Call-to-action** text requiring user attention
- **THE ONLY COLOR THAT IS EVER BOLD**
- **Used extremely sparingly** for maximum impact
- **Always paired with light blue bullet when AI-generated**

#### **Yellow Text** `#f1d771` 📝 **PRIMARY CONTENT**
- **AI explanations** and informational responses
- **Main conversational content**
- **Default "speaking" color for AI**
- **User's default terminal text color** (carries over)

#### **White Text** `#ffffff` 🤖 **SYSTEM/AUTOMATED**
- **System messages** not from AI
- **Automated responses** 
- **URLs and commands** when from system (not highlighted)
- **Non-AI generated content**

#### **Gray Text** `#bbbcbb` 👤 **USER/SECONDARY**
- **User input** and commands
- **Supporting information**
- **Lists contents** and secondary details
- **URLs and commands** when sent by user (not highlighted)
- **The bullet itself** when user-generated

#### **Light Blue Text** `#82d0ff` 🔗 **AI-HIGHLIGHTED**
- **URLs and commands** ONLY when AI sends them
- **Checkmarks** on completed items
- **AI-emphasized** important information
- **Never used for user-generated content**

#### **Light Brown Text** `#7b714a` 📊 **METADATA/CONTEXT**
- **Numbers** in ordered lists (1. 2. 3.)
- **Background information** with tree characters
- **Indented context** `└ (Todo list is empty)`
- **Secondary organizational** information

---

## **FORMATTING RULES**

### **Indentation Hierarchy**
```
●   Primary message  ← Bullets have large 3 space indent
    └ Secondary context       ← 4 spaces + tree character
      3rd level context       ← 6 spaces, no tree, faded, gray text 
```

### **Tree Characters** `#7b714a`
- **`└`** for final/single nested item
- **`├`** for middle items in list
- **`│`** for continuation lines
- **Always light brown color**

### **Bold Text Rule** ⚠️ **CRITICAL**
- **ONLY pink text is ever bold**
- **No other color** uses bold formatting
- **Bold = urgent attention required**

### **Spacing Strategy**
- **Big gap** between bullet and content (minimum 3 spaces)
- **Generous line spacing** for readability
- **Bullets always far left** for scan-ability

---

## **SEMANTIC MEANING SYSTEM**

### **Information Attribution**
```
Gray bullet + Gray text = "User said this"
White bullet + Yellow text = "AI is explaining"  
White bullet + Pink text + Bold = "AI is acting - PAY ATTENTION"
Light blue bullet + Pink text = "AI priority action"
```

### **URL/Command Treatment**
- **User sends URL/command** → Gray (no highlighting)
- **AI sends URL/command** → Light blue (highlighted)
- **System generates URL/command** → White (no highlighting)

### **List Hierarchy**
```
1. Main item                        ← Light brown number
   ● Sub-bullet                     ← Bullet follows hierarchy rules
     └ Context info                 ← Light brown tree + context
```

---

## **PSYCHOLOGICAL DESIGN PRINCIPLES**

### **Color Psychology Applied**
- **Pink** = Cognitive interrupt ("STOP and look")
- **Blue** = Trust and action (AI recommendations)  
- **Yellow** = Warmth and communication (conversation)
- **Gray** = Background/neutral (user space)
- **Brown** = Earth/foundation (organizational info)

### **Visual Hierarchy Goals**
1. **Instant attribution** (who said what)
2. **Priority assignment** (what needs attention)
3. **Information type** (explanation vs action vs context)
4. **Conversation flow** (natural reading patterns)

### **Terminal Optimization**
- **High contrast** for legibility across terminals
- **Monospace-friendly** spacing and alignment
- **Color-blind accessible** through multiple visual cues
- **Works in various terminal themes**

---

## **IMPLEMENTATION RULES**

### **Decision Tree for Text Color**
```
Is this bold? → PINK (AI action requiring attention)
Is this from user? → GRAY
Is this AI explaining? → YELLOW  
Is this AI highlighting link/command? → LIGHT BLUE
Is this system automated? → WHITE
Is this organizational/metadata? → LIGHT BROWN
```

### **Decision Tree for Bullet Color**
```
Is text PINK and bold? → LIGHT BLUE bullet
Is this from user? → GRAY bullet
Is this AI or system response? → WHITE bullet
```

### **Consistency Rules**
- **Never mix** user and AI visual patterns
- **Always maintain** bullet-to-left positioning
- **Always use** generous spacing
- **Never use bold** except for pink text
- **Always use tree characters** for nested context

---

## **WHY THIS SYSTEM IS GENIUS** 💡

### **Conversation Protocol**
This isn't just styling - it's a **visual conversation protocol** that creates:
- **Clear turn-taking** in human-AI dialogue
- **Attention management** through color hierarchy  
- **Context preservation** through consistent attribution
- **Cognitive load reduction** through predictable patterns

### **Terminal UI Evolution**
They've solved the fundamental challenge of **rich communication in constrained medium** by creating:
- **Semantic color system** (meaning through color)
- **Hierarchical information architecture** (importance through position)
- **Consistent visual language** (learnable patterns)
- **Cross-terminal compatibility** (works everywhere)

This is **conversation design as much as interface design** - they've created a visual language for human-AI collaboration! 🤖✨

---

# **MAO VISUAL PROTOCOL INNOVATION** 🎭

## **EXTENDING CLAUDE CODE'S GENIUS** ⚡

Building on Claude Code's proven foundation, MAO adds **workflow relationship visualization** through directory tree integration.

### **MAO'S UNIQUE INNOVATION: ORCHESTRATION TREES** 📂

#### **Shape Language**
- **Triangle (△/▲)** = Orchestrator (Mao) 
- **Circle (○/●)** = Agent
- **Maintain shape identity** throughout all states (waiting → active → complete)

#### **Tree Structure Integration**
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

#### **Tree Character Meanings**
- **├──** = "This flows from the parent task"
- **│** = "Continuation of the same branch" 
- **└──** = "This completes the current branch"
- **No tree** = "New top-level thread/major transition"

### **ANIMATION STATES WITH SHAPES** 🔄

#### **Waiting State**
```
△   Next orchestration step              ← Outlined triangle
○   Upcoming agent task                  ← Outlined circle  
```

#### **Active State (Pulsing)**
```
▲   Mao thinking and planning            ← Filled triangle, pulsing
●   Agent working on research            ← Filled circle, pulsing
```

#### **Complete State**
```
△̃   Mao completed planning               ← Triangle with checkmark overlay
○̃   Agent completed research             ← Circle with checkmark overlay
```

### **PROGRESS RELAY VISUALIZATION** 🏃‍♂️

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

### **COLOR ADAPTATION FOR MAO** 🎨

Following Claude Code's semantic color principles:

#### **For Progress Indicators**
- **Gray** `#bbbcbb` → Waiting states (outlined shapes)
- **Pink** `#ff49ff` → Active states (filled, pulsing) - ATTENTION HERE
- **Light Blue** `#82d0ff` → Completed checkmarks
- **Yellow** `#f1d771` → Phase labels and descriptions
- **Light Brown** `#7b714a` → Tree characters and metadata

#### **Information Hierarchy**
```
△   Mao analyzing research results        ← Yellow text (AI explaining)
├── ●   Quality check: 8.7/10            ← Light brown metadata  
├── ●   3 critical gaps identified        ← Yellow content
└── ▲   Spawning analysis agent           ← Pink text (AI taking action)
```

### **WHY THIS IS REVOLUTIONARY** 💡

#### **Unique MAO Identity**
- **Beyond bullet points** - shows actual workflow relationships
- **Familiar paradigm** - developers know directory trees
- **Information density** - more context without clutter
- **Visual storytelling** - see the orchestration narrative

#### **Cognitive Benefits**
- **Relationship clarity** - understand how tasks connect
- **Workflow comprehension** - see the orchestration decisions  
- **Progress tracking** - follow the agent handoff chain
- **Context preservation** - maintain the bigger picture

#### **Technical Advantages**
- **Scalable complexity** - handles parallel workflows
- **Familiar symbols** - leverages existing terminal conventions
- **Terminal-native** - works in any terminal environment
- **Accessible** - multiple visual cues beyond just color

### **IMPLEMENTATION RULES** 📋

#### **Tree Structure Guidelines**
1. **Top-level items** (no tree chars) = Major workflow transitions
2. **├── branches** = Direct spawns or consequences  
3. **│ continuations** = Same agent/context continuing
4. **└── completions** = Final item in a branch
5. **Nested trees** = Sub-tasks or deliverables

#### **Shape + Tree Combination**
```
△   Root orchestration                   ← No tree (top level)
├── ●   Spawned agent                   ← Tree shows relationship
│   ├── Sub-deliverable                 ← Agent's work breakdown
│   └── Final deliverable              ← Completion marker
└── △   Next orchestration              ← Back to orchestrator
```

#### **Progress Animation Rules**
1. **Maintain shape identity** - triangle stays triangle even when complete
2. **Pulsing for active** - filled shapes pulse to show motion
3. **Checkmark overlay** - preserve shape but add completion indicator
4. **Tree persistence** - relationships remain visible throughout

---

## **MAO'S COMPLETE VISUAL LANGUAGE** 🚀

**Combining Claude Code's proven foundation with MAO's orchestration innovation:**

✅ **Semantic color system** (who/what/priority)
✅ **Bullet spacing strategy** (prominence through pattern breaks)  
✅ **Shape-based role identity** (triangle/circle persistence)
✅ **Tree relationship mapping** (workflow dependency visualization)
✅ **Animation state system** (outline → filled → checkmark)

**Result**: The most sophisticated terminal UI for AI workflow orchestration ever created! 🎭✨

This visual protocol turns complex multi-agent workflows into **intuitive, scannable, beautiful terminal experiences** that users can understand at a glance.

---

## **DYNAMIC STATUS CYCLING SYSTEM** 📺

### **LIVE ACTIVITY MONITORING** ⚡

Instead of static status text, MAO displays **cycling status updates** that show real-time progress and current activities.

#### **Cycling Text Pattern**
```
●   Research Agent                     ← 3 seconds (base state)
●   Research Agent: Analyzing market   ← 3 seconds (activity 1)  
●   Research Agent: Finding competitors ← 3 seconds (activity 2)
●   Research Agent: Gathering insights ← 3 seconds (activity 3)
●   Research Agent                     ← Cycle restart
```

#### **Context-Aware Activity Messages**

**Research Phase Activities:**
- "Searching competitor websites"
- "Analyzing pricing strategies" 
- "Gathering market data"
- "Processing industry reports"
- "Synthesizing key findings"

**Analysis Phase Activities:**
- "Processing research data"
- "Identifying key patterns"
- "Cross-referencing sources"
- "Building recommendations"
- "Formatting deliverables"

**Orchestrator Activities:**
- "Reviewing agent outputs"
- "Assessing quality metrics"
- "Planning workflow adjustments"
- "Preparing next assignments"
- "Coordinating parallel work"

**Content Creation Activities:**
- "Drafting initial outline"
- "Writing key sections"
- "Refining messaging"
- "Adding supporting details"
- "Finalizing deliverables"

#### **Progress Integration Options**
```
●   Research Agent: 23% complete      ← Percentage updates
●   Research Agent: Finding gap #3    ← Item-specific progress
●   Research Agent: 67% complete      ← Updated percentage  
●   Research Agent: Finalizing report ← Completion phase
```

### **MULTI-AGENT COORDINATION DISPLAY** 🎛️

#### **Independent Cycling**
```
▲   Mao: Coordinating parallel work    ← Orchestrator cycle (3s)
├── ●   Research: Analyzing trend #4   ← Agent 1 cycle (3s)
├── ●   Design: Testing layout v2      ← Agent 2 cycle (3s)
└── ●   Content: Writing intro para    ← Agent 3 cycle (3s)
```

**Each line cycles independently** creating a **live mission control feel**!

#### **Timing Strategy**
- **3-second default cycle** for optimal readability
- **Pause on user interaction** (typing, scrolling, navigation)
- **Faster 2s cycles** for short/simple tasks
- **Slower 4s cycles** for complex/long processes
- **Dynamic timing** based on task complexity

#### **Activity Synchronization**
```
STATE: All agents reporting progress
▲   Mao: Processing status updates     ← Coordinated timing
├── ●   Research: Submitting findings  ← All update together
├── ●   Analysis: Submitting insights  ← Synchronized handoff
└── ●   Content: Submitting drafts     ← Clean transition
```

### **ACCORDION COLLAPSE + CYCLING** 📁

#### **Progressive Disclosure with Live Updates**

**Expanded State (Active Work):**
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

**Auto-Collapsed State (Focus Mode):**
```
△̃   [▼] Initial Planning (2m ago)     ← Static collapsed
├── ○̃   [▼] Research Complete (1m ago) ← Static collapsed  
├── ○̃   [▼] Design Complete (30s ago)  ← Recently collapsed
└── ▲   Creative Review: Quality check ← Current work cycling
    ├── ●   Analyzing submissions      ← Active subtask cycling
    ├── ○   Assessment pending         ← Static queued  
    └── ○   Recommendations queued     ← Static planned
```

#### **Collapse Interaction Rules**
- **[▼]** = Collapsed (click/key to expand)
- **[▲]** = Expanded (click/key to collapse)  
- **[●]** = Cannot collapse (actively cycling)
- **Auto-collapse** after 30s of completion + no user focus

#### **Smart Collapse Logic**
```
If agent.status == "complete" AND 
   time_since_completion > 30_seconds AND
   user_not_actively_viewing AND
   new_active_work_present:
     auto_collapse_branch()
     preserve_expand_toggle()
```

### **TERMINAL "MISSION CONTROL" EXPERIENCE** 🚀

#### **Live Dashboard Feel**
```
WORKFLOW: Content Strategy Development
┌─────────────────────────────────────┐
│ ▲   Mao: Orchestrating phase handoff │ ← 3s cycle
│ ├── ●   Research: Final validation   │ ← 3s cycle  
│ ├── ●   Analysis: Gap prioritization │ ← 3s cycle
│ └── ●   Strategy: Framework design   │ ← 3s cycle
└─────────────────────────────────────┘
```

#### **Information Density Optimization**
- **Maximum context** in minimal space
- **Live activity awareness** without overwhelming detail
- **Hierarchical focus** (current work prominent)
- **Historical context** available but collapsed

#### **Psychological Benefits**
- **Confidence building** - see continuous progress
- **Engagement maintenance** - dynamic visual interest
- **Process transparency** - understand what's happening
- **Control feeling** - can expand/collapse as needed

### **IMPLEMENTATION SPECIFICATIONS** 🔧

#### **Cycling Engine Requirements**
```javascript
class StatusCycler {
  constructor(messages, timing = 3000) {
    this.messages = messages;
    this.currentIndex = 0;
    this.timing = timing;
    this.paused = false;
  }
  
  cycle() {
    if (!this.paused) {
      this.currentIndex = (this.currentIndex + 1) % this.messages.length;
    }
  }
  
  pauseOnInteraction() {
    this.paused = true;
    setTimeout(() => this.paused = false, 2000);
  }
}
```

#### **Message Context System**
```python
ACTIVITY_MESSAGES = {
    "research": [
        "Analyzing market trends",
        "Gathering competitor data", 
        "Processing industry reports",
        "Synthesizing key insights"
    ],
    "analysis": [
        "Identifying patterns",
        "Cross-referencing sources",
        "Building frameworks",
        "Generating recommendations"  
    ],
    "orchestrator": [
        "Reviewing deliverables",
        "Planning next phase",
        "Coordinating agents",
        "Optimizing workflow"
    ]
}
```

#### **Visual State Management**
- **Cycling text** updates every 3 seconds
- **Shape animations** (pulsing) independent of text
- **Tree structure** remains static during cycles
- **Collapse state** preserved through cycling
- **User interactions** pause cycling temporarily

---

## **COMPLETE MAO VISUAL SYSTEM SUMMARY** 🏆

**MAO's terminal UI combines:**

✅ **Claude Code's proven foundation** (semantic colors, bullet spacing, attention management)
✅ **Orchestration tree visualization** (workflow relationship mapping)  
✅ **Progressive shape identity** (triangle/circle persistence through states)
✅ **Live status cycling** (mission control activity monitoring)
✅ **Smart accordion collapse** (progressive disclosure for complex workflows)

**Result**: **The most sophisticated, intuitive, and engaging terminal UI for AI workflow orchestration ever created** - turning complex multi-agent coordination into a beautiful, scannable, live experience that users will love to watch and use! 🎭✨💃🤖

## Claude Code UI Inspiration 

### Settings 

--> Configure Mao preferences 
- Auto-compact: true 
- Use todo list: true 
- Verbose output: false 
- Theme: Dark mode (colorblind-friendly) 
- Notifications: bell 
- Editor mode: normal 
- Model: Default (recommended) 

### Theme

--> Choose the text style that looks best with your terminal. 
1. Dark Mode 
   - White text --> #ffffff
   - Diff removal --> #6b5251
   - Diff addition --> #506d51
2. Light Mode 
   - Black text --> #131313
   - Diff removal --> #bf88a4
   - Diff addition --> #6ca36c
3. Dark Mode Colorblind-Friendly 
   - White text --> #ffffff
   - Diff removal --> #6d1813
   - Diff addition --> #18516d
4. Light Mode Colorblind-Friendly 
   - Black text --> #11100f
   - Diff removal --> #bea4a3
   - Diff addition --> #87a4c0
5. Dark Mode ANSI Colors Only 
   - White text --> #ffffff
   - Diff removal --> #a41e1a
   - Diff addition --> #29a423
6. Light Mode ANSI Colors Only 
   - Black text --> #010101
   - Diff removal --> #a41e19
   - Diff addition --> #29a424

### Text Colors 

- Yellow --> #f1d771
  - Main text  
  - My terminal's default text color, but this is the only one that carried over  
- Pink --> #ff49ff
  - Prominent, CTA, attention, accent text  
  - Bright and used very sparingly 
  - The only color or text that is ever bold  
- Gray --> #bbbcbb
  - Contents of a list  
  - Logistical, not important but sometimes useful text 
  - The color of messages I send (SMART) 
  - URLs and commands are NOT highlighted, they stay gray if sent from me 
  - The bullet point is a gray > if it is a message I sent or if it was an automated response 
- Light blue --> #82d0ff
  - Very carefully used accent color 
  - Highlighted URLs and commands only when the AI messaged them 
  - Check marks on completed items 
  - The large bullet point if the text in the bullet point is PINK 
- White --> #ffffff
  - Used when it is an automated response and not the AI
  - "No JSON args configured. Run 'mao help' for more information." 
  - URLs and commands are NOT highlighted, they stay white if not an AI response 
  - The large bullet point if the text is from the AI 
- Light brown --> #7b714a
  - Numbers in an ordered list 
  - Background information text ( └ to do list is empty)

