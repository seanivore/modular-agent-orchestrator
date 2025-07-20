# Section IV: How Data Flows Into Mao
*Every interface pathway data takes to reach the orchestrator*

---

When you run `mao --goal "Let's become millionaires"` in the terminal, use a slash command line like `/model Claude Opus 4` in the app, chat up Mao to help you brainstorm the details of your science project, or add `/memory I only ever write my Instagram captions with a single sentence` to chat, all paths lead to the same sophisticated orchestrator ready to take action.

---

## The Terminal Is Mao's Data Front Door 

Activating the primary entry point to the system is as simple as typing `mao` in the terminal, a command router and trigger entry point to conversation that adapts to you. 

The system recognizes if you're a first-time user and starts onboarding, a returning user prompting them to ask if they want to continue a previous session, or an experienced user executing specific commands. 

This is all thanks to the user management system, tracking sessions, preferences, and creating a novel and contexually relevant experience every interaction. 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Terminal Interface Architecture**
*Entry point patterns, command discovery, session management*

*Reference: `interfaces/ui_terminal.py`, `mao_v4.py` entry point*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

## Dynamic Command Discovery 

Slash commands are one of the many config files. New commands and capabilities can be added simply by dropping new configuration files into the appropriate directories. Mao will scan the directory to discover functionality on the fly. 

When you type `mao --help` the system isn't reading a static help file, it's dynamically building the help content by examining all the command configurations it finds in the system; they could techincally be changed up every day. 

This discovery approach extends to every aspect of the system; tools, models, and workflows all combine these components. 

As a user, you enjoy an interface that presents a rich ecosystem of capabilities through intelligent autocomplete and contextual suggestions.

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Dynamic Discovery Patterns**
*JSON-based command discovery, configuration scanning, autocomplete system*

*Reference: `orchestrator/cli_manager.py`, `configs/cli/*` command definitions*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

## Conversation-Driven Interaction

Mao's interface philosophy centers on conversation rather than navigation. They have no script, only an understanding of the product. No menus and no forms; we encourage Mao to do what they do best, learn through natural language. 

While you're describing what you want to accomplish, Mao is transforming your wishes into structured workflows and configurations behind the scenes, while simultaneously responding to you.

A conversational approach means you could say "I think I need a new marketing plan" and Mao will engage, "What do you need it for?" Simple back and forth allows Mao to gather the details they need without grilling you for information. Mention tools and they'll suggest what makes sense for the conversation thus far. 

Mao may be complex software, but it feels like you're chatting with a coworker. 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Conversation Processing Architecture** 
*Natural language interpretation, goal parsing, workflow generation*

*Reference: Goal command processing, workflow creation flows*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

## Settings and Personalization 

Behind every user interaction lies a sophisticated settings management system that remembers preferences, default configurations, and personal working patterns. The interface adapts to your preferred models, commonly used tools, and typical workflow structures. This personalization not only happens persistently across sessions, you don't even need to tell them what you want. 

They're like a best friend who just, remembers all the right things. 

The delta-only settings system storage only saves your preferences that differ from the defaults. This makes personalized configurations efficient and able to travel with you between systems. The interface reflects these personal preferences in everything from color themes to model suggestions.

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Settings Management Architecture**
*Delta-only storage, user preferences, personalization patterns*

*Reference: `orchestrator/settings_manager.py`, `orchestrator/username_manager.py`*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

---

## Integration Bridges and Communication Patterns

### Python-TypeScript Communication Bridge

Terminal information, along with the rest of the Mao system, is implemented in Python which provides a solid foundation for orchestrator communication. 

The actual application in the terminal? That's all TypeScripe and Node.js, creating a polished experience users expect from modern high-end design. Our hybrid approach maintains the robust Python backend that enables our premium interface layer. 

Data exchange, status updates, and command execution flow through a communication bridge using structure JSON protocols so that the interface layer can be enhanced without touching core orchestrator logic. 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Interface Bridge Architecture**
*Python-TypeScript communication, command routing, API patterns*

*Reference: `interfaces/` directory, UI integration patterns*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

### Real-Time Status and Progress Communication

What while you wait. Mao's interface displays progress metrics and status updates keeping you updated and slightly entertained. From tool status to system health, everything is tracked in real time. So check that ETA, and then wait for the tone while you check your email. 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Real-Time Communication Architecture**
*Progress tracking, status updates, metrics streaming*

*Reference: `orchestrator/real_time_metrics.py`, workflow monitoring*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

### Stress Free Error Handling 

Remember the old days when an error message was a literal crypic message that was meaningless to you, the user who receied th error? 

Mao's error handling keeps the conversation going. An interface layer translates technical errors into context you'll understand. The deep technical details are there if you're into that kind of stuff, like debugging, otherwise Mao will let you know how to fix things without leaving the chat. 

| **ADD ARCHITECTURE HERE** |
| ------------------------- |

**Error Communication Architecture**
*Error translation, user feedback patterns, debugging support*

*Reference: `orchestrator/error_handling.py`, user communication flows*

| **END ARCHITECTURE SECTION** |
| ---------------------------- |

---

## Visual Protocol and User Experience Design

### Conversation-First Design Philosophy

The interface design prioritizes conversation over navigation. Instead of presenting users with complex menus and forms, the system encourages natural language interaction. This design philosophy extends to every aspect of the interface, from command completion to progress visualization.

Visual elements support the conversation rather than dominating it. Progress indicators are subtle and informative, command suggestions appear contextually, and status information is presented as part of the ongoing dialogue rather than in separate interface panels.

### Adaptive Interface Intelligence

The interface learns from user patterns and adapts its suggestions and shortcuts accordingly. Frequently used commands bubble up in autocomplete suggestions, common workflow patterns become template options, and preferred models and tools get priority in selection lists.

This adaptive behavior creates an interface that becomes more helpful over time while remaining predictable and consistent. Users develop muscle memory for common tasks while discovering new capabilities through intelligent suggestions.

---

NO VISION THIS IS WHAT WE ARE BUILDING AND THIS IS WHY CLAUDE CODE PROVIDED THE CODE FOR THINGS WE DIDN'T IMPLEMENT YET. BECAUSE WE NEEDED IT FOR THE DOCS SO THAT WE COULD IMPLEMENT IT. 

After this update I'm creating a rule that says we will never be implementing anything until it is completely in the documents, because I've been trying for that all month but we keep doing it backwards like this. 


## Tech Stack Definition

### Core Technologies
```
TERMINAL INTERFACE:
├── TypeScript/Node.js (Frontend terminal app)
├── Ink 4.4+ (React for terminals - what Claude Code uses)
├── React 18+ (Component-based UI)
└── Node.js APIs (File system, process management)

BACKEND INTEGRATION:
├── Python 3.11+ (Existing orchestrator - keep unchanged)
├── HTTP/WebSocket API (Communication bridge)
├── JSON-RPC or REST (Command routing)
└── Process spawning (Node.js calls Python processes)

ARCHITECTURE PATTERN:
├── Single Conversation Interface (like Claude Code)
├── No Menus / No Navigation Components
├── Unified Input Handler
└── Event-Driven State Management
```
---


## File Structure & Integration

### Clean UI Architecture
```
terminal-app/                    ← NEW: TypeScript terminal application
├── src/
│   ├── components/
│   │   ├── ConversationInterface.tsx    ← Main conversation UI (Ink/React)
│   │   ├── AutoCompleteSystem.tsx       ← CLI command suggestions
│   │   ├── ProgressVisualization.tsx    ← Live workflow progress
│   │   └── VisualProtocol.tsx           ← Color/shape system
│   ├── api/
│   │   ├── PythonBridge.ts              ← HTTP/JSON-RPC to Python
│   │   └── CLICommandRouter.ts          ← Routes to Python backend
│   └── app.tsx                          ← Main application entry
├── package.json                         ← npm dependencies (ink, react, etc.)
└── tsconfig.json                        ← TypeScript configuration

interfaces/                      ← EXISTING: Keep for Python integration
├── ui_terminal.py              ← Keep as API bridge to TypeScript
└── ui_web.py                   ← Future: Web interface placeholder
```

### Integration Points
```
EXISTING PYTHON SYSTEMS (DO NOT TOUCH):
├── orchestrator/cli_manager.py    ← Routes all CLI commands
├── orchestrator/core.py           ← Main workflow orchestration  
├── orchestrator/memory_mcp.py     ← Session state management
├── configs/cli/*/                 ← All 30 CLI commands implemented
└── tools/*/                       ← All tools with button snippets

NEW TYPESCRIPT FRONTEND:
├── ConversationInterface.tsx      ← Calls PythonBridge API
├── AutoCompleteSystem.tsx        ← Scans CLI configs via API
├── ProgressVisualization.tsx     ← Gets real_time_metrics via API
└── PythonBridge.ts               ← HTTP/JSON-RPC to Python backend

COMMUNICATION BRIDGE:
├── HTTP API endpoints            ← Python serves TypeScript calls
├── WebSocket for live updates    ← Real-time progress streaming
├── JSON-RPC command routing      ← Structured command execution
└── File system integration       ← TypeScript reads configs directly
```

---

## Core Components Specification

### 1. ConversationInterface (TypeScript/React)
```typescript
// terminal-app/src/components/ConversationInterface.tsx
import React, { useState } from 'react';
import { Box, Text, useInput } from 'ink';
import { PythonBridge } from '../api/PythonBridge';

export const ConversationInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const pythonAPI = new PythonBridge();
  
  const handleInput = async (userInput: string) => {
    if (userInput.startsWith('/')) {
      // CLI command (route to Python backend)
      return await pythonAPI.executeCommand(userInput.slice(1));
    } else {
      // Natural language goal (route to Python backend)
      return await pythonAPI.executeCommand('goal', userInput);
    }
  };
  
  return (
    <Box flexDirection="column">
      {/* Single conversation interface - NO menus, NO navigation */}
    </Box>
  );
};
```

### 2. PythonBridge (TypeScript API Layer)
```typescript
// terminal-app/src/api/PythonBridge.ts
export class PythonBridge {
  private baseURL = 'http://localhost:8000'; // Python FastAPI server
  private responseTimeout = 200; // 200ms threshold for immediate feedback
  
  async executeCommand(command: string, args?: string): Promise<any> {
    // Show immediate feedback within 200ms threshold
    this.showImmediateFeedback(`Executing ${command}...`);
    
    try {
      // Non-blocking HTTP call to Python cli_manager.py via FastAPI
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      
      const response = await fetch(`${this.baseURL}/cli/${command}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ args, source: 'typescript-terminal' }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      return response.json();
    } catch (error) {
      // Fast, human-readable error handling
      throw new Error(`Command failed: ${error.message}`);
    }
  }
  
  async getAutoCompleteOptions(partial: string): Promise<string[]> {
    // Stream results as they arrive, don't batch
    const response = await fetch(`${this.baseURL}/autocomplete?q=${partial}`);
    return response.json();
  }
  
  private showImmediateFeedback(message: string): void {
    // Immediate feedback within 200ms - app feels alive
    console.log(message); // Replace with proper UI feedback
  }
}
```

### 3. VisualProtocol (TypeScript/Ink)
```typescript
// terminal-app/src/components/VisualProtocol.tsx
import { Text } from 'ink';

export const Colors = {
  pink: '#ff49ff',      // AI actions (BOLD only)
  yellow: '#f1d771',    // AI explanations  
  light_blue: '#82d0ff', // Highlighted items
  white: '#ffffff',     // System responses
  gray: '#bbbcbb',      // User input
  light_brown: '#7b714a' // Tree/metadata
} as const;

export const Shapes = {
  ai_active: '▲',       // AI working
  ai_waiting: '△',      // AI idle
  task_active: '●',     // Task in progress
  task_complete: '○'    // Task done
} as const;

export const StyledText: React.FC<{
  color: keyof typeof Colors;
  shape?: keyof typeof Shapes;
  children: React.ReactNode;
}> = ({ color, shape, children }) => (
  <Text color={Colors[color]}>
    {shape && Shapes[shape]} {children}
  </Text>
);
```

---

## Responsive UI Performance Rules

### Terminal App Responsiveness Philosophy
**"Responsiveness isn't just about speed—it's about rhythm. The best terminal apps feel like a conversation."** - Dia

### Core Performance Patterns
```typescript
// 1. NON-BLOCKING EVERYTHING
// ❌ Never block the event loop
await fs.readFile(path); // ✅ Always async
fs.readFileSync(path);   // ❌ Never sync calls

// 2. IMMEDIATE FEEDBACK (200ms threshold)
if (estimatedTime > 200) {
  showSpinner('Processing...');
}

// 3. STREAM RESULTS, DON'T BATCH
workflowStream.on('data', (chunk) => {
  displayProgress(chunk); // Show as it arrives
});

// 4. MINIMAL STARTUP TIME
// Lazy-load modules, lean dependencies
const heavyModule = await import('./heavy-processing');
```

### Conversation Rhythm Requirements
- **Echo within 200ms** - User needs to know app is alive
- **Stream progress updates** - Don't wait for completion to show output
- **Fast error feedback** - Human-readable errors immediately
- **Configurable verbosity** - Adapt to user's environment
- **Clear visual rhythm** - Predictable response patterns

### Technical Implementation
```typescript
// Use readline/enquirer for interactive prompts
import readline from 'readline';
import ora from 'ora'; // Spinners for long tasks
import cliProgress from 'cli-progress'; // Progress bars

// Always show activity within 200ms
const spinner = ora('Working...').start();
setTimeout(() => {
  if (!taskComplete) spinner.text = 'Still working...';
}, 200);

// Stream output with Node's native streams
process.stdout.write(chunk); // Real-time display

// Offload heavy computation to worker threads
const worker = new Worker('./heavy-task.js');
worker.postMessage(data);
```

### Visual Protocol Integration
- **Immediate color feedback** - Pink interrupts within 200ms
- **Smooth state transitions** - No jarring changes
- **Progressive disclosure** - Build complexity gradually
- **Contextual rhythm** - Match conversation flow

---

## What We're NOT Building

### ❌ Avoid These Patterns (From Previous Failed Implementation)
- **main_menu.py** - No menu systems
- **navigation.py** - No navigation components
- **Multiple app components** - Single conversation interface only
- **Separate routing files** - Use existing cli_manager.py
- **Complex state management** - Use existing memory_mcp.py

### ❌ Tech Stack Mistakes to Avoid
- **Python for terminal UI** - Use TypeScript/Node.js with Ink like Claude Code
- **Python-only approach** - Need hybrid TypeScript frontend + Python backend
- **Web technologies for terminal** - Ink is specifically for terminal interfaces
- **Direct Python CLI calls** - Use HTTP/JSON-RPC bridge for clean separation

---

## Integration Strategy

### Phase 1: TypeScript Terminal App Setup
1. **Create terminal-app directory** with TypeScript/Node.js project
2. **Install Ink and React dependencies** (like your playground)
3. **Build ConversationInterface component** (single conversation UI)
4. **Create Python API bridge** for backend communication

### Phase 2: Python Backend API  
1. **Add FastAPI server** to existing Python orchestrator
2. **Expose CLI commands via HTTP endpoints**
3. **Create WebSocket endpoints** for real-time progress
4. **Test TypeScript ↔ Python communication**

### Phase 3: Integration & Polish
1. **Connect auto-complete** to Python CLI discovery
2. **Implement live progress display** via WebSocket
3. **Add visual protocol** with Ink styling
4. **Professional Claude Code-quality experience**


## Success Criteria

### Technical Requirements
- ✅ **Single conversation interface** (no menus/navigation)
- ✅ **Integrates with existing CLI commands** via cli_manager.py
- ✅ **Visual protocol** implemented with Ink styling
- ✅ **Auto-complete system** discovering commands dynamically
- ✅ **Session continuity** via memory_mcp.py integration

### Quality Standards
- ✅ **Claude Code quality** terminal experience
- ✅ **Professional visual design** matching foundation_spec.md
- ✅ **Seamless CLI integration** with all 30 existing commands
- ✅ **Zero architecture violations** - no menu/navigation patterns
- ✅ **Performance** - smooth, responsive interface

### Integration Validation
- ✅ **All existing systems work** unchanged
- ✅ **CLI commands route properly** through cli_manager.py
- ✅ **Visual protocol** displays correctly with Ink
- ✅ **Auto-complete** discovers all CLI commands
- ✅ **Progress display** shows real workflow data

---

## Dependencies and Setup

### Required Libraries
```bash
npm install ink ink-spinner ink-select-input ink-text-input react
npm install -D @types/node @types/react tsx typescript
```

### Foundation Files
- Existing orchestrator core system (`orchestrator/core.py`)
- Memory MCP integration (`orchestrator/memory_mcp.py`)
- Configuration system (`configs/` directory structure)
- Tool integration system (`tools/` with button snippets)

### Development Approach
1. **Start with Claude Code patterns** - use proven interface design
2. **Implement content translator** - systematically convert ui_terminal.py
3. **Build incrementally** - working application from first implementation
4. **Test continuously** - verify all existing functionality preserved
5. **Polish progressively** - enhance visual quality and user experience

### Quality Gates
- **Architecture review** - No menu/navigation patterns
- **Integration testing** - All CLI commands functional
- **Visual validation** - Protocol implemented correctly
- **Performance testing** - Smooth, responsive experience
- **User experience** - Conversation-driven flow works naturally

---

## Design Rules Integration

### Cognitive Flow Protocol Requirements
The TypeScript/Ink implementation must follow the **45 design rules** documented in `MAO_TERMINAL_INTERFACE_DESIGN_RULES.md`:

#### Critical Spacing & Alignment
```typescript
// 4ch left alignment for ALL content
const CONTENT_INDENT = '    '; // 4 character spaces
const TREE_ALIGNMENT = '    ├── '; // Tree branches align with content

// No-indicator lines for RARE emphasis
<Text>Creating your portfolio...</Text>     // ← POWER LINE (no indicator)
<Text>●    Portfolio structure planned</Text> // ← Normal line with indicator
```

#### Pink Usage Rules (Most Critical)
```typescript
// ✅ CORRECT: Pink emphasizes WHAT something happens TO
<Text>Creating <Text color="#ff49ff" bold>project structure</Text></Text>

// ❌ WRONG: Pink on verbs/actions
<Text><Text color="#ff49ff" bold>Creating</Text> project structure</Text>

// One pink statement per 60-row viewport
const maxPinkPerViewport = 1;
```

#### Color Opacity System
```typescript
export const Colors = {
  pink: '#ff49ff',           // Full opacity - cognitive interrupts
  yellow: '#f1d771',         // Full opacity - conversation flow
  light_blue: 'rgba(130, 208, 255, 0.5)', // 50% opacity - subtle trust
  white: 'rgba(255, 255, 255, 0.5)',      // 50% opacity - less prominent
  gray: '#bbbcbb',           // Full opacity - user space
  yellow_secondary: 'rgba(184, 164, 86, 0.7)' // Brown mustard with opacity
} as const;
```

#### Layout Architecture
```typescript
// Paragraph grouping with document-style spacing
<Box flexDirection="column" gap={2}>
  {/* Group 1: Header content */}
  <Box flexDirection="column">
    <Text>{headerLines}</Text>
  </Box>
  
  {/* Large gap */}
  <Box height={3} />
  
  {/* Group 2: Input field */}
  <Box flexDirection="column">
    <Text>{inputPrompt}</Text>
  </Box>
</Box>
```

### Quality Enforcement
- **Every space is intentional** - Match Sean's precise typography examples
- **Cognitive architecture** - Colors serve brain function, not aesthetics
- **Visual conversation protocol** - Clear turn-taking and attribution
- **Professional polish** - Terminal UI that rivals graphical applications

---

*This specification ensures we build exactly what the foundation_spec.md calls for: a professional, conversation-driven terminal interface that integrates seamlessly with existing systems while maintaining the unique visual identity, responsive performance, and cognitive flow protocol.*

---


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

## **Shape Language**

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

## **COLOR ADAPTATION FOR MAO** 🎨

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

## Future Interface Expansion

### TypeScript Terminal Application Vision

The planned TypeScript terminal interface represents the next evolution of Mao's user experience. Built with the same technologies as professional development tools like Claude Code, this interface will provide the polished, responsive experience users expect from modern software.

The TypeScript interface will maintain the conversational philosophy while adding visual richness, improved autocomplete, and more sophisticated progress visualization. The architecture is designed to support this transition seamlessly while preserving all existing functionality.

### Web Interface Potential

While Mao's current focus is on terminal-based workflows, the interface architecture is designed to support future web-based access. The same command routing, configuration management, and workflow orchestration that powers the terminal interface could drive web-based interactions.

This flexibility ensures that as user needs evolve, Mao can adapt its interface modalities while preserving the core workflow orchestration capabilities that make it powerful.

---

*This interface foundation supports everything that follows. Every piece of data, every user intention, every workflow goal flows through these carefully designed input channels before reaching the orchestrator core where the real magic happens.*