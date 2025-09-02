# Mao App UI/UX Design Guide
*Comprehensive design specifications extracted from MAO_FLOW.md for web application implementation*

---

## Overview

This document compiles all UI/UX specifications from MAO_FLOW.md into a comprehensive design guide for implementing the Mao web application. The design philosophy centers on luxury minimalism achieved through obsessive attention to micro-details rather than feature proliferation.

## Core Design Philosophy

### Single-Screen Chat-Centric Experience

Mao operates entirely within one container, one screen. Everything in the app happens through chat with minimal UI chrome. This approach leverages users' familiarity with AI chat interfaces while providing sophisticated workflow orchestration capabilities.

**Key Principles:**
- No menus, navigation, or complex UI chrome
- Chat serves as the natural interface for LLM operations
- Visual design keeps attention focused on chat contents
- Four-element design constraint: shadow movement, semantic highlighting, character choice, whitespace

### Luxury Through Micro-Detail Execution

The design philosophy follows the Hermès principle: perfection through flawless execution of subtle details rather than feature abundance. Users should feel "I don't know why, but this feels expensive" without consciously noticing the specific elements creating that sensation.

---

# Login System UI/UX

## Design Inspiration

Login flow inspired by Pork-bun's domain registration service, emphasizing user experience optimization and security best practices.

## Login Interface Structure

### Existing Account Login (Primary Flow)

**Visual Layout:**
- Clean, centered form on dedicated page
- Cloudflare auto-secure integration (no user action required)
- Minimal legal text placement

**Form Fields:**
```
┌─────────────────────────────────────┐
│ Enter your email or phone           │
├─────────────────────────────────────┤
│ Password                            │
│ Leave password blank if using       │
│ a passkey                          │
├─────────────────────────────────────┤
│ ☑ Remember Me (pre-checked)        │
└─────────────────────────────────────┘

[Login Button]
[Create New Account Button]
```

**UX Considerations:**
- Password field accepts any input when using passkey (flawless UX principle)
- System ignores password content if passkey is used
- Login button automatically triggers passkey prompt
- Clear indication that passkey option exists without being overwhelming

### New Account Creation

**Form Structure:**
```
┌─────────────────────────────────────┐
│ EMAIL                              │
├─────────────────────────────────────┤
│ PHONE                              │
│ One valid contact required as      │
│ Account ID                         │
├─────────────────────────────────────┤
│ PASSWORD                           │
│ Must be 12-72 characters, differ  │
│ from Account ID                    │
├─────────────────────────────────────┤
│ [USE PASSKEY] - Prominent button  │
├─────────────────────────────────────┤
│ ☑ Legal agreement checkbox        │
└─────────────────────────────────────┘
```

**Payment Integration:**
- Stripe integration for payment forms
- Free trial consideration with multiple UI configurations
- Clear subscription pricing display

### Multilingual Considerations

**Critical Note:** The word "passkey" doesn't translate cleanly in every language. Pair with explanatory subtitle: "Faster, one-tap sign-in with your device" for universal clarity.

## User Identity System

### UserID Generation

User identification uses the `meid` script for consistent, reproducible user IDs:

```bash
meid horvathaugust@gmail.com  → user-5253
meid 424-744-7687            → user-0697  
meid 4247447687              → user-0697 (same result)
```

**Implementation Requirements:**
- Account ID must be single string of characters
- Forms enforce strict formatting for compatibility
- UserID format: `user-####` (always 4 digits)
- Same Account ID always produces same UserID

### User Directory Structure

Automatic creation during user setup:
```
configs/user/user-5253/
├── analytics/
│   ├── cost_tracking.json
│   ├── session_metrics.json
│   ├── tool_usage.json
│   └── workflow_metrics.json
├── memories/
│   ├── personal_preferences.json
│   └── project_context.json
└── user_preferences.json (delta-only storage)
```

---

# Main Application Interface

## Container Design

### Visual Framework

**Single Container Architecture:**
- Everything exists within one minimalistic container
- Clean, simple, narrow lines with polished depth
- NO BUTTONS, NO MENU TEXT, NO ICONS visible
- Intentional absence creates "silence is loud" effect
- Frame appearance: narrow, centimeters-deep classic black picture frame

### Real-Time Shadow Animation System

**Core Animation Concept:**
- Container casts shadow that changes with real sun/moon movement
- Shadow direction and size shifts constantly but imperceptibly
- Motion so subtle it's "too slow to see happen"
- Only noticeable when pausing to observe: "wow, this is wider now on this side!"

**Technical Requirements:**
- JavaScript: `new Date()` for current time
- CSS: Dynamic `box-shadow` property updates
- Smooth transitions: `transition: box-shadow 0.5s ease`
- Optional: `navigator.geolocation` for real sun position
- Update frequency: Every minute via `setInterval(updateShadow, 60000)`

**Time-Based Shadow Characteristics:**

| TIME  | SHADOW PEAK CHARACTERISTIC |
|-------|----------------------------|
| 06:00 | Dawn awakening             |
| 09:00 | Morning warmth             |
| 12:00 | Harsh midday precision     |
| 15:00 | Afternoon softening        |
| 18:00 | Golden hour magic          |
| 21:00 | Twilight mystery           |
| 00:00 | Deep night crispness       |
| 03:00 | Pre-dawn stillness         |

**Shadow Design Specifications:**

*Daytime Shadows:*
- Warm light creates cool shadows; cool light creates warm shadows
- Light bounces around, subtly illuminating shadows with complexity
- Further objects have lighter shadows, bluer tone, less definition
- Morning: Warm, soft, long shadows; golden quality; cool color reflection
- Midday: High contrast, well-defined, short and sharp
- Afternoon: Lengthening shadows, cooler diffused light, warmer tones
- Golden Hour: Warm, soft, magical quality with long diffused shadows
- Twilight: Cooler, diffused light with soft, blurred shadow edges

*Nighttime Shadows:*
- Close range of values, AVOID PURE BLACK
- Darker shadows with color variations in cooler tones (blues, greens)
- Early night: Long dramatic shadows with softer edges
- Mid-night: Bright moon creates shorter, more defined, sharper shadows
- Late night: Redder/warmer glow with elongated shadows

**Dark Mode Adaptations:**
- Deeper blacks with subtle colored tints (dark purple, deep blue)
- Feel like "expensive black velvet" with rich depth
- Must NOT FEEL FLAT GRAY
- Maintain luxury depth without washing out

## Technology Stack

### Core Technologies
- **Pure HTML, CSS, and JavaScript** (no framework required)
- Maximum performance and simplicity focus
- Dynamic shadow system capabilities

### Performance Considerations
- **Critical:** Avoid lag from large-area animations
- Engineer smart shadow implementation
- Create shadows only in necessary areas along lines and shapes
- Limit animation scope to prevent performance issues

---

# Chat Interface Design

## Welcome Experience

### AI-Generated Welcome Messages

**Core Principle:** Welcome messages NEVER repeat themselves. Every login generates completely unique greeting using AI creativity.

**Example Welcome Variations:**
```
🞶 It is 10pm on Thursday night. Do you know where your AI is, Sean?
🞶 Look at the moon, Sean. Look at the moon!
🞶 Be sure to pause to touch grass now and then, Sean.
```

**Implementation Strategy:**
- NO hardcoded suggestions or fallbacks in code
- Utilize AI's ideation capabilities fully
- Combine user data + analytics + memories for personalization
- Extreme logic leaps and cross-disciplinary connections encouraged
- Accept goofy/random outcomes as feature, not bug

### Dynamic Help Text

**Rotating Help Messages:**
- Change frequently while user works with Mao or in settings
- Multiple timer durations for display time variation
- Analytics required to optimize duration and content effectiveness

**Example Help Messages:**
```
? Try /help or /config
? /goal will make your project instantly
? Settings /config or /themes
? Check out all the /tools /models /providers
? Jump back into a project /workflow CUSTOM-COMMAND
? Mao can help you find your /workflows
? message will add to queue; press ESC to interrupt
```

**Content Management:**
- Weekly AI-generated content creation (100+ messages)
- Complete replacement to prevent reuse
- Analytics tracking: usage patterns, length preferences, timing effectiveness
- Track user experience progression and tip utilization

## Message Type System

### Typography-Based Icons

**System Messages:**
```
● ○ ▶︎ ▷ = All system update messages
🞶 = Messages from Mao
> = Messages from User
```

**Status Indicators:**
```
● = completed action
○ = upcoming action not started
Flashing ○ to ● = active action

▶︎ = Completed list item
▷ = List item to be completed
Flashing ▷ to ▶︎ = active list item
```

### Example Message Threading

**Initial System Messages:**
```
● **UPDATE** New User Has Logged-in
  └── ▶︎ Acquired UserID
      ▶︎ User Directory Setup
      ▶︎ Create AI Improv Chat Greeting
   Done ($0.010 • 220 tokens • 8.3s)

● **PING** User Initiated Project Chat
  └── ▶︎ Created new Workflow ID
      ▶︎ First Project State Memory Update
      ▶︎ Greeted new user
   Done ($0.015 • 092 tokens • 1.9s)
```

**Conversation Flow:**
```
> Hi, Mao. My first time using this tool. How are you?

🞶 Happy to meet you, Sven. I'm well; eager to hear what you're interesting in
  working on today. Feel free to message, even double-text me, all you like if
  you're the type to spill your thoughts. Otherwise, if you like, I can walk you through
  the process. What are you thinking?
```

## Chat History Management

### Progressive Message Simplification

**Core Strategy:** Chat history cleans itself up to reduce cognitive load and manage context windows effectively.

**Simplification Rules:**
1. Truncate paragraphs over 50-75 words
   - Show start of paragraph
   - Add "+37 lines (press ctrl-r to expand and review)"
2. Remove completely irrelevant information
3. Transform verbose text into bullet-pointed lists
4. Maintain expandable/collapsible structure

**Example Progression:**

*Initial State:*
```
● New user login, greeting, project initiated
  └── Success ($0.025 • 312 tokens • 10.2s)

> Hi, Mao. My first time using this tool. How are you?

🞶 Happy to meet you, Sven. I'm well; eager to hear what you're interesting in
  working on today. Feel free to message, even double-text me, all you like if
  you're the type to spill your thoughts. Otherwise, if you like, I can walk you through
  the process. What are you thinking?

> Mao, I don't even know where to begin!

🞶 Tell me about yourself! What do you do? How is it relevant to what you need to get
  done today. Honestly, you can really spill as much as you like on me, I'm pretty good at handling human-speak.
```

*After Simplification:*
```
● New user login, greeting, project initiated
  └── Success ($0.025 • 312 tokens • 10.2s)

● > Hi, Mao. My first time using this tool. How are you?
  🞶 Happy to meet you, Sven.
  > 🞶 > 🞶
  └── +4 messages (ctrl-r to review)

> [Current conversation continues...]
```

### Double-Texting Support

**Message Display Rules:**
- Multiple consecutive messages from same sender lose hard return gaps
- Keep sender icon at start of each message
- Natural messaging service behavior
- Configurable in settings (user preference)

**Settings Options:**
1. `always` - Both can message multiple times
2. `user only` - Only user can double-text
3. `Mao only` - Only Mao can double-text
4. `never` - Must wait for response before sending again
5. `queue` - Messages held until Mao completes or pauses

**Interrupt Functionality:**
- ESC twice at any time interrupts Mao
- If user has queued message, ESC once pushes message through

---

# AI Status System ("AI Improv")

## Dynamic Status Generation

### Present Participle Creation

**Core Concept:** Instead of static "THINKING..." or "WORKING...", Mao generates contextual present participle words ending in -ING based on current activity and conversation context.

**Implementation Philosophy:**
- NO hardcoded suggestions or fallbacks
- AI generates contextually appropriate terms
- Accept non-dictionary words and creative expressions
- Embrace unexpected or humorous results

### Contextual Examples

**Based on Project Type:**
```
Corporate budget workflow → CALCULATING...
Talking dog screenplay → Digging...
Spider research → Crawling...
```

**Based on User Behavior/Tone:**
```
User typing quickly with errors → Combobulating...
User excited about project → DECORATING...
AI drawing blank → FLOUNDERING...
Workflow building → Architectivizing...
Time-sensitive thinking → TIME-TRAVELING...
```

### Visual Implementation

**Status Display Format:**
```
+ BUILDING CONFIDENCE + (12s • $0.003 • 140 tks)
+ Finding my groove + (22s • $0.009 • 222 tks)
+ Considering + (12s • $0.007 • 340 tks)
+ Chin Scratching + (12s • $0.007 • 340 tokens)
+ Delegating + (12s • $0.007 • 340 tokens)
+ Cleaning + (32s • $0.170 • 1345 tokens)
```

**Visual Characteristics:**
- Plus signs before and after the verb
- Cursor/icon blinks during activity (🞶)
- Real-time metrics: duration, cost, token count
- Positioned above user input field

### Status Transition Examples

**During Workflow Creation:**
1. `+ BUILDING CONFIDENCE +` (initial planning)
2. `+ Finding my groove +` (getting organized)
3. `+ Considering +` (critical analysis)
4. `+ Chin Scratching +` (deep thinking)
5. `+ Architectivizing +` (designing structure)
6. `+ Delegating +` (assigning agent tasks)
7. `+ Cleaning +` (finalizing details)

---

# Color Psychology & Semantic Highlighting

## Four-Element Design Constraint

The entire visual design operates within strict limitations:
1. **Shadow movement** (ever-present, imperceptible)
2. **Conceptual semantic text highlighting** (few colors, cognitive load reduction)
3. **Character choice** (typography, ONE FONT only)
4. **White space** (generous, strategic spacing)

## Color Tier System

### Tier 1: Primary AI Communication
**Purpose:** How AI talks to you normally or conveys important information

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| Main standard | yellow | rgb(240, 215, 112) | Normal writing, scan the message |
| Bold standard | pink | rgb(255, 73, 255) | Cognitive interrupt; LOOK HERE! |

### Tier 2: Throw-Away Content
**Purpose:** Not meant for lingering attention, just there for normalcy

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| User messages | warm gray | rgb(187, 187, 187) | Encouraged to disregard |
| AI `THINK` Text | warm gray | rgb(187, 187, 187) | Ignore, no UX value |
| User block cursor | pale mustard | rgb(183, 171, 103) | Distinct to draw eye |

### Tier 3: Helpful Information
**Purpose:** Good news updates, chill assistance

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| Trusted low-key update | blue ice | rgb(192, 231, 255) | Secondary info, be at ease |
| Trusted elevated update | blue sky | rgb(132, 207, 255) | Helpful info, should be seen |

### Tier 4: Error Handling
**Purpose:** Unusual but calm error indication

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| Unexpected errors | pale pink | rgb(255, 166, 164) | Error but chill, made calm |

### Tier 5: Background Support
**Purpose:** Helpful when lost, generally ignorable

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| Supplemental subtext | green-gray | rgb(187, 188, 187) | Notice eventually, subdued |
| Supplemental info | green-brown | rgb(124, 115, 75) | Read if bored |

### Tier 6: Rare Accents
**Purpose:** Specific intentions, used sparingly

| Element | Color | RGB Code | Intention |
|---------|-------|----------|-----------|
| Accent on down-low | barely tangerine | rgb(255, 198, 116) | Marketing/gimmick attention |
| Accent rare novel | pale purple | rgb(202, 202, 255) | Novel, intriguing content |

## Theme System Implementation

### Theme Categories
1. Dark mode
2. Light mode  
3. Dark mode (CVD - Color Vision Deficiency)
4. Light mode (CVD)
5. Dark mode (ANSI colors only)
6. Light mode (ANSI colors only)

### Configuration Requirements
- Themes stored as modular config files
- User-downloadable/deletable themes
- Apple-style controlled customization
- Users modify brightness/hue/saturation within parameters
- System protects semantic highlighting integrity
- Palette generation based on single color selection

---

# Live Workflow UI

## Master Task List System

### Real-Time Progress Display

**Core Structure:** Master task list spawns smaller task lists as workflow executes. All lists update in real-time at actual processing speed.

**Visual Hierarchy:**
```
● **Data** Secure project notes to Files API • 3 sec ago
  └── Done (1 tool use • $0.000 • 420 tokens)

● **Data** Project State Memory Update • 3 sec ago
  └── Done (1 tool use • $0.005 • 180 tokens)

○ **Build Workflow** First Draft of Expense Project
  └── ▶︎ Organize variables by JSON object type
      ▶︎ Design phase sequence (parallel vs sequential)
      ▶︎ Create comprehensive task instructions
      ▷ Map resources to phase requirements
      ▷ Define handoff assessment questions
      ▷ Validate workflow complexity against user expectations
```

### Speed Demonstration Strategy

**Performance Display Goals:**
- Tool usage updates faster than human reading speed
- Create visceral sense of AI working intensely
- Numbers, file names, URLs update rapidly
- Show only handful at any time due to speed
- User feels "Mao is really cranking on this!"

**Example Rapid Updates:**
```
○ **Agent 2** Receipt Review, Expense Categorization
  └── Receipt_2024_11_15_lunch.jpg → "Meals & Entertainment"
      Receipt_2024_11_16_gas.jpg → "Transportation"
      Receipt_2024_11_16_office.jpg → "Office Supplies"
      Receipt_2024_11_17_client.jpg → "Meals & Entertainment"
      Processing (47 of 42 receipts • 3.2 secs)
```

## Multi-Agent Coordination Display

### Parallel Agent Execution

**Visual Structure for Simultaneous Agents:**
```
○ **Updating To Do** Expense Report
  └── ▶︎ Agent 1A: Download employee expense submissions
      ▶︎ Agent 1B: Retrieve credit card statements
      ▷ Handoff: Review Phase 1 Deliverables
      ▷ Decide: Activate Next Phase

○ **Agent 1A**
  └── ▶︎ Downloading expense reports
      ▷ Confirm reports are completed
      ▷ Handoff reports to Mao
      +1 tool use

○ **Agent 1B**
  └── ▶︎ Navigate to company credit card portal
      ▷ Export statements to PDF
      ▷ Handoff statements to Mao
      +2 tool uses
```

### Completion and Consolidation

**Progressive Condensation:**
- Individual agents complete and condense above main list
- When workflow nears completion, all agents consolidate into single block
- Maintain cost/time/token transparency throughout
- Memory and assets always show update status at top

**Final Consolidation Example:**
```
● **Data** Memory & Assets • 10s ago
  └── Done (14 tool uses • $0.000 • 550 tks)

● **Phase Completion** Submissions
  └── ▶︎ Agent 1A • Employee reports
      ▶︎ Agent 1B • Credit statements
      ▶︎ Agent 2 • Receipts cross-referencing
      ▶︎ Agent 3 • Report accuracy reviews
  Done (22 tool uses • $0.145 • 2022 tks • 13.9s)
```

## Context Window Management

### Smart Compaction System

**Automatic Management:**
- Context window percentage displayed bottom right
- Warning appears at 10% remaining
- Auto-compaction available or user-triggered (ctrl-t)
- Always preserve user ability to save context via OS menus

**Display Progression:**
```
? try /config or /help                               89%
? Send message into queue; hit ESC to interrupt      83%
? message to add to queue or hit ESC to interrupt    55%
? Auto-compact at 3% or ctrl-t to run now            10%
? Auto-compact at 3% or ctrl-t to run now             7%
```

**Best Practice:** Users should ctrl-t at good stopping points rather than waiting for automatic truncation.

---

# Settings System UI

## Toggle Menu Interface

### Core Settings Categories

**Primary Settings Table:**

| Setting | Default | Options | Description |
|---------|---------|---------|-------------|
| Default Agent | `claude-sonnet-4` | Model selection | Default subagent unless discussed |
| Default Provider | `anthropic direct` | Provider selection | Preferred API provider |
| App Theme | `dark mode` | Theme cycling | High legibility colors |
| Notifications | `once, no push` | 4 notification levels | Workflow completion alerts |
| Cat Vibes | `I love it` | Yes/No | Occasional cat language |
| Double-texting | `always` | 5 messaging modes | Messenger-style experience |

### Extended Settings Table

**Additional Configuration Options:**

| Setting | Default | Type | Description |
|---------|---------|------|-------------|
| Remember credentials | `false` | boolean | App login persistence |
| Productive startup | `false` | boolean | Start with recent project context |
| Public profile | `true` | boolean | GitHub-like project sharing |
| Public contact | `true` | boolean | Allow user messaging |
| Offer services | `false` | boolean | Hire-me profile section |
| User analytics | `true` | boolean | Data collection consent |
| Latest models | `true` | boolean | Auto-update to newest releases |
| Mao Model | `sonnet-latest` | model selection | Mao's operating model |
| Claude Code Model | `opus-latest` | model selection | Development task model |
| Code Nudges | `true` | boolean | Suggest Claude Code for dev tasks |
| Currency | `USD` | currency selection | Billing currency |
| Payment frequency | `Yearly` | billing cycle | Discount tier selection |
| Language | `English` | language selection | UI and communication language |
| Local data backup | `Setup` | configuration | Backup location selection |

### Notification Settings Detail

**Notification Options:**
1. `once, no push notification` - Simple tone only
2. `silent with push notification` - Push only
3. `silent and no push notification` - No alerts
4. `notifications on` - Both push and tone

### Double-Texting Configuration

**Messaging Behavior Options:**
1. `always` - Both can message multiple times like texting
2. `user only` - User can double-text, Mao cannot
3. `Mao only` - Mao can double-text, user cannot
4. `never` - Must wait for response before next message
5. `queue` - Messages held until Mao pauses

### Theme Selection Implementation

**Theme Switching:**
- Hitting enter cycles through theme options
- Live preview of changes as user cycles
- No secondary toggle menu needed if cycling works well
- Visual feedback immediate

### Currency and Pricing

**Regional Pricing Matrix:**
```javascript
regional_multipliers = {
  'US': 1.0,     // $29.99
  'EU': 0.9,     // €26.99
  'UK': 0.95,    // £28.49
  'CA': 1.1,     // $32.99 CAD
  'AU': 1.15,    // $34.49 AUD
  'BR': 3.0,     // R$89.99
  'MX': 20.0,    // $599 MXN
  'CN': 6.7,     // ¥199.99
  'JP': 110.0,   // ¥3299
  'KR': 1200.0,  // ₩35,999
  'IN': 75.0     // ₹2249
}
```

**Payment Frequency Discounts:**
1. Monthly - no discount
2. Quarterly - 10% discount
3. 6-Months - 1 month free
4. Yearly - 20% discount

---

# User Input and Interaction

## Input Field Design

### Text Input Container

**Visual Structure:**
```
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
```

**Positioning:** Bottom of chat container, consistent visual integration with message history above.

### Status Integration

**Below Input Field Integration:**
- AI Improv status appears directly above input field
- Context percentage indicator on bottom right
- Help/tip rotation on bottom left
- Real-time cost/token/timing metrics

**Example Layout:**
```
+ Architectivizing + (12s • $0.007 • 340 tokens)
╭──────────────────────────────────────────────────────────╮
│ >                                                        │
╰──────────────────────────────────────────────────────────╯
? try /config or /help                             35%
```

## Slash Command System

### Command Categories by Response Type

**Mao Responds:**
- `/custom command` - Start existing workflow
- `/tools`, `/models`, `/providers` - Toggle lists with Q&A
- `/variables`, `/variables-explain` - Show/explain workflow variables
- `/workflows`, `/review 'CUSTOM COMMAND'` - Search workflows
- `/doctor`, `/dry-run` - AI-guided troubleshooting

**System Responds:**
- `/help`, `/config` - Display help text or settings menu
- `/continue` - Load recent project without message
- `/output ~/downloads` - Simple system confirmation
- `/set-model`, `/default-provider` - Settings confirmation
- `/setup ./config.json`, `/update ./phase.json`, `/fix-it ./fix.json` - Script execution
- `/stats`, `/logs`, `/verbose` - Toggle confirmations
- `/exit`, `/logout`, `/login`, `/restart` - System actions

### Toggle List Interface

**Example Tool List Display:**
```
> /tools

🞶 We have quite a few added. Go ahead and use the up/down arrow. If you hit enter, you'll see info
  about that tool. Hit ESCAPE to come back to the main chat, here.

▶︎ Brave Search
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

**Navigation:**
- Up/down arrows for selection
- Enter for detailed information
- Escape returns to main chat
- Mao available for questions during browsing

---

# Cost and Analytics Transparency

## Real-Time Cost Display

### Always-Visible Metrics

**Standard Cost Display Format:**
```
Done ($0.010 • 220 tokens • 8.3s)
Done (1 tool use • $0.005 • 180 tokens)
Done (22 tool uses • $0.145 • 2022 tks • 13.9s)
```

**Display Requirements:**
- Show cost for every operation, even small administrative work
- Include token count for transparency
- Duration in seconds with decimal precision
- Tool usage count when applicable
- Real-time updates, not batched reporting

### Dynamic Cost Tracking

**Live Status Updates:**
```
(12s • $0.007 • 340 tokens)
(22s • $0.009 • 222 tks)
(32s • $0.170 • 1345 tokens)
```

**Implementation Notes:**
- Milliseconds included to emphasize speed
- Cost accuracy using real math (not estimates)
- Files API operations marked as $0.000 (free)
- Memory operations may have small cost

## Model Pricing Integration

### Provider-Specific Configuration

**Anthropic Pricing Matrix (Example):**

| Model | Base Input | 5m Cache Write | 1h Cache Write | Cache Hits | Output |
|-------|------------|----------------|----------------|------------|--------|
| Claude Opus 4.1 | $15/MTok | $18.75/MTok | $30/MTok | $1.50/MTok | $75/MTok |
| Claude Sonnet 4 | $3/MTok | $3.75/MTok | $6/MTok | $0.30/MTok | $15/MTok |
| Claude Haiku 3.5 | $0.80/MTok | $1/MTok | $1.6/MTok | $0.08/MTok | $4/MTok |

**Context Window Pricing:**

| Context Size | Input | Output |
|--------------|-------|--------|
| ≤ 200K | $3/MTok | $15/MTok |
| > 200K | $6/MTok | $22.50/MTok |

**Implementation Requirements:**
- Dynamic pricing configuration via JSON
- Regular updates for new models/pricing
- Accurate token counting per provider
- Cache optimization cost calculations

---

# Advanced UI Features

## Message Block Intelligence

### Courteous Space Management

**Self-Managing Canvas:**
- Message blocks use only space needed temporally
- AI constantly re-evaluates message blocks
- Old information dissolves when no longer relevant
- New information condenses existing content to make room
- Completed items get simple categorical terms

**Behavior Rules:**
- If something new needs display → rewrite to condense
- If something complete → remove, give categorical term
- If something changing rapidly → show sequence happening
- Context-aware temporal relevance assessment

### Expandable/Collapsible Structure

**Expansion Controls:**
- `ctrl-r` to expand collapsed sections
- `ctrl-r` again to collapse when done reviewing
- Clear indication of collapsed content count
- Preserved structure maintains context

**Example Collapsed State:**
```
● > Hi, Mao. My first time using this tool. How are you?
  🞶 Happy to meet you, Sven.
  > 🞶 > 🞶
  └── +4 messages (ctrl-r to review)
```

## Visual Workflow Diagrams

### Implementation Requirement

**Status:** NEEDS TO BE IMPLEMENTED
- Users expect visual workflow review before execution
- Must integrate with simple HTML/CSS/JS tech stack
- Should present workflow phases, dependencies, and flow
- Visual comfort for user approval process

**Technical Considerations:**
- Research integration options for web app
- Maintain consistency with minimalist design
- Support workflow complexity visualization
- Enable user-friendly modification interface

---

# Technical Implementation Notes

## Performance Requirements

### Animation Constraints

**Critical Performance Rules:**
- Avoid lag from large-area animations
- Engineer smart shadow implementation
- Create shadows only in necessary areas
- Limit simultaneous animations

### Real-Time Updates

**Update Philosophy:**
- NEVER use timers for fake updates
- Updates MUST reflect actual processing speed
- Transparency shows AI capability authentically
- Energy of speed through velocity, not deception

## Browser Compatibility

### Technology Decisions

**Core Stack:**
- Pure HTML, CSS, JavaScript (no frameworks)
- Maximum performance and simplicity
- Dynamic shadow system using CSS properties
- Smooth transitions for professional feel

### Geolocation Integration

**Optional Enhancement:**
- `navigator.geolocation` for real sun position
- Fallback to time-based shadow calculation
- Enhanced realism for luxury experience

---

# Implementation Checklist

## Phase 1: Core Interface

- [ ] Single container design with shadow animation system
- [ ] Message type icons and semantic color highlighting
- [ ] Chat history progressive simplification
- [ ] AI Improv dynamic status system
- [ ] Real-time cost/token/timing display

## Phase 2: User Experience

- [ ] Login flow with passkey integration
- [ ] Settings toggle menu system
- [ ] Slash command recognition and routing
- [ ] Double-texting and message queue system
- [ ] Context window management with compaction

## Phase 3: Advanced Features

- [ ] Live workflow task list displays
- [ ] Multi-agent coordination visualization
- [ ] Theme system with color psychology
- [ ] Visual workflow diagrams
- [ ] Performance optimization and testing

## Phase 4: Polish and Launch

- [ ] Multilingual considerations implementation
- [ ] Analytics integration for UI optimization
- [ ] Accessibility compliance
- [ ] Cross-browser compatibility testing
- [ ] User experience validation

---

This design guide provides the complete specification for implementing Mao's web application interface. The emphasis on luxury through micro-detail execution, combined with functional minimalism, creates a distinctive user experience that leverages AI capabilities while maintaining human-centered design principles.