# Section VIII: Conceptual Semantic Visual Identity  

---

# UI Foundation Technical Architecture Specification

## Executive Summary

This specification defines the **exact** technical architecture for the UI Foundation Build to prevent any confusion like the previous implementation where the wrong tech stack and architecture were used. The goal is a **conversation-driven terminal interface** that rivals Claude Code's quality while maintaining the unique visual identity.

---

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

### Why This Stack
- **TypeScript/Node.js**: Exact same stack as Claude Code for professional terminal UI
- **Ink**: React for terminals - proven by Claude Code to deliver professional experience
- **Python backend**: Keep existing orchestrator unchanged, communicate via API
- **Hybrid approach**: Best of both worlds - professional TypeScript UI + robust Python logic

---

## Architecture Principles 

### ✅ CORRECT: Conversation-Driven Architecture
```
┌─────────────────────────────────────┐
│  TERMINAL INTERFACE                 │
├─────────────────────────────────────┤
│  [Single Input Field]               │
│  > Tell me what you want to do...   │
│                                     │
│  [Conversation History]             │
│  AI: I'll help you create that...   │
│  User: Make it use TypeScript       │
│  AI: Updated! Here's your workflow  │
│                                     │
│  [Live Progress Display]            │
│  ▲ Creating components...           │
│  ○ Testing integration...           │
└─────────────────────────────────────┘
```

### ❌ WRONG: Menu/Navigation Architecture (What We Avoided)
```
┌─────────────────────────────────────┐
│  TERMINAL INTERFACE                 │
├─────────────────────────────────────┤
│  [Main Menu]                        │
│  1. Create Workflow                 │
│  2. Manage Settings                 │
│  3. View Statistics                 │
│                                     │
│  [Navigation Bar]                   │
│  < Back | Next > | Help            │
└─────────────────────────────────────┘
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

---

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
- **▼** = Collapsed (click/key to expand)
- **▲** = Expanded (click/key to collapse)  
- **●** = Cannot collapse (actively cycling)
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

---

The following are final draft by Claude Code. 

---

# SECTION V: VISUAL RESOURCES & BRAND IDENTITY
*The Cognitive Design System with Implementation Code*

---

## Chapter 5.1: The Cognitive Flow Design System

### Visual Psychology for AI Orchestration

**The Challenge**: Traditional AI interfaces overwhelm users with technical complexity. **The Solution**: A cognitive design system that guides users through natural workflow creation.

#### **The Four-Color Cognitive Framework**

```css
/* The Mao Cognitive Color System */
:root {
  /* Primary Cognitive Colors */
  --cognitive-stop: #ff49ff;      /* Pink - "STOP and Focus Here" */
  --cognitive-flow: #f1d771;      /* Yellow - "Flow With This" */
  --cognitive-trust: #82d0ff;     /* Blue - "This is Trustworthy Action" */
  --cognitive-space: #bbbcbb;     /* Gray - "This is Your Space" */
  
  /* Supporting Colors */
  --success: #4CAF50;             /* Green - Completion */
  --warning: #FF9800;             /* Orange - Caution */
  --error: #F44336;               /* Red - Problems */
  --info: #2196F3;                /* Blue - Information */
  
  /* Cognitive Color Variations */
  --cognitive-stop-light: #ff79ff;
  --cognitive-stop-dark: #cc39cc;
  --cognitive-flow-light: #f5e191;
  --cognitive-flow-dark: #d4b851;
  --cognitive-trust-light: #a2e0ff;
  --cognitive-trust-dark: #5fa9cc;
  --cognitive-space-light: #d1d2d1;
  --cognitive-space-dark: #95969;
}

/* Cognitive Color Usage Classes */
.cognitive-stop {
  background-color: var(--cognitive-stop);
  color: white;
  border: 2px solid var(--cognitive-stop-dark);
  box-shadow: 0 4px 12px rgba(255, 73, 255, 0.3);
  /* Psychological impact: Demands attention, creates focus */
}

.cognitive-flow {
  background-color: var(--cognitive-flow);
  color: #333;
  border: 1px solid var(--cognitive-flow-dark);
  /* Psychological impact: Natural conversation, learning state */
}

.cognitive-trust {
  background-color: var(--cognitive-trust);
  color: white;
  border: 1px solid var(--cognitive-trust-dark);
  transition: all 0.2s ease;
  /* Psychological impact: Safe interaction, reliable action */
}

.cognitive-trust:hover {
  background-color: var(--cognitive-trust-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(130, 208, 255, 0.4);
}

.cognitive-space {
  background-color: var(--cognitive-space);
  color: #333;
  border: 1px solid var(--cognitive-space-dark);
  /* Psychological impact: Familiar workspace, user control area */
}
```

#### **React Component Implementation**

```jsx
// components/CognitiveButton.jsx
import React from 'react';
import './CognitiveButton.css';

const CognitiveButton = ({ 
  type = 'trust',           // stop, flow, trust, space
  size = 'medium',          // small, medium, large
  icon,                     // Optional icon component
  children,
  onClick,
  disabled = false,
  loading = false,
  ...props 
}) => {
  const getButtonClass = () => {
    const baseClass = 'mao-button';
    const typeClass = `cognitive-${type}`;
    const sizeClass = `mao-button-${size}`;
    const stateClass = disabled ? 'disabled' : loading ? 'loading' : '';
    
    return `${baseClass} ${typeClass} ${sizeClass} ${stateClass}`.trim();
  };

  const getAriaLabel = () => {
    const typeDescriptions = {
      stop: 'Important action requiring attention',
      flow: 'Continue with natural workflow',
      trust: 'Safe and reliable action',
      space: 'User workspace interaction'
    };
    
    return props['aria-label'] || typeDescriptions[type];
  };

  return (
    <button
      className={getButtonClass()}
      onClick={onClick}
      disabled={disabled || loading}
      aria-label={getAriaLabel()}
      {...props}
    >
      {loading && <span className="mao-spinner" aria-hidden="true" />}
      {icon && <span className="mao-button-icon">{icon}</span>}
      <span className="mao-button-text">{children}</span>
    </button>
  );
};

// Usage examples with cognitive psychology
const CognitiveButtonExamples = () => {
  return (
    <div className="cognitive-examples">
      {/* Pink - STOP and Focus Here */}
      <CognitiveButton 
        type="stop" 
        onClick={() => console.log('Critical decision point')}
      >
        Start Workflow
      </CognitiveButton>
      
      {/* Yellow - Flow With This */}
      <CognitiveButton 
        type="flow"
        onClick={() => console.log('Natural conversation flow')}
      >
        Continue Learning
      </CognitiveButton>
      
      {/* Blue - Trustworthy Action */}
      <CognitiveButton 
        type="trust"
        onClick={() => console.log('Safe to proceed')}
      >
        Save Progress
      </CognitiveButton>
      
      {/* Gray - Your Space */}
      <CognitiveButton 
        type="space"
        onClick={() => console.log('User workspace')}
      >
        Edit Settings
      </CognitiveButton>
    </div>
  );
};

export default CognitiveButton;
```

### The Shape Language System

#### **Orchestrator & Agent Symbol Components**

```jsx
// components/StatusIndicators.jsx
import React from 'react';

const OrchestratorIndicator = ({ status = 'waiting', size = 24 }) => {
  const getTriangleClass = () => {
    return status === 'active' ? 'orchestrator-active' : 'orchestrator-waiting';
  };
  
  return (
    <div className={`orchestrator-indicator ${getTriangleClass()}`}>
      <svg width={size} height={size} viewBox="0 0 24 24">
        <triangle
          points="12,2 22,20 2,20"
          className={`orchestrator-triangle ${getTriangleClass()}`}
        />
      </svg>
      <span className="status-label">
        {status === 'active' ? '▲ Orchestrating' : '△ Ready'}
      </span>
    </div>
  );
};

const AgentIndicator = ({ status = 'waiting', agentName, size = 20 }) => {
  const getCircleClass = () => {
    return status === 'active' ? 'agent-active' : 'agent-waiting';
  };
  
  return (
    <div className={`agent-indicator ${getCircleClass()}`}>
      <svg width={size} height={size} viewBox="0 0 20 20">
        <circle
          cx="10"
          cy="10"
          r="8"
          className={`agent-circle ${getCircleClass()}`}
        />
      </svg>
      <span className="agent-label">
        {status === 'active' ? '●' : '○'} {agentName}
      </span>
    </div>
  );
};

// Workflow status display component
const WorkflowStatusDisplay = ({ 
  orchestratorStatus, 
  agents = [],
  currentPhase 
}) => {
  return (
    <div className="workflow-status-display">
      <div className="status-header">
        <OrchestratorIndicator status={orchestratorStatus} />
        <span className="phase-indicator">Phase: {currentPhase}</span>
      </div>
      
      <div className="agents-status">
        {agents.map(agent => (
          <AgentIndicator
            key={agent.id}
            status={agent.status}
            agentName={agent.name}
          />
        ))}
      </div>
    </div>
  );
};
```

```css
/* StatusIndicators.css */
.orchestrator-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
}

.orchestrator-triangle.orchestrator-waiting {
  fill: none;
  stroke: var(--cognitive-trust);
  stroke-width: 2px;
  /* △ Waiting State - outline shows potential energy */
}

.orchestrator-triangle.orchestrator-active {
  fill: var(--cognitive-stop);
  stroke: var(--cognitive-stop-dark);
  stroke-width: 1px;
  /* ▲ Active State - filled shows kinetic energy */
  animation: pulse-orchestrator 2s infinite;
}

@keyframes pulse-orchestrator {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.agent-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 2px 0;
  padding: 4px 8px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.agent-circle.agent-waiting {
  fill: none;
  stroke: var(--cognitive-space);
  stroke-width: 2px;
  /* ○ Agent waiting - harmonious with orchestrator */
}

.agent-circle.agent-active {
  fill: var(--cognitive-flow);
  stroke: var(--cognitive-flow-dark);
  stroke-width: 1px;
  /* ● Agent active - synchronized with orchestrator */
  animation: pulse-agent 1.5s infinite;
}

@keyframes pulse-agent {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.workflow-status-display {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 1px solid var(--cognitive-space);
  border-radius: 12px;
  padding: 16px;
  margin: 16px 0;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--cognitive-space-light);
}

.agents-status {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
```

---

## Chapter 5.2: Mobile-First Interface Design

### iOS-Inspired Workflow Creation

#### **Card-Based Interaction Components**

```jsx
// components/WorkflowCards.jsx
import React, { useState } from 'react';
import { CognitiveButton } from './CognitiveButton';
import './WorkflowCards.css';

const GoalDefinitionCard = ({ onGoalSubmit }) => {
  const [goal, setGoal] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = async () => {
    setIsAnalyzing(true);
    await onGoalSubmit(goal);
    setIsAnalyzing(false);
  };

  return (
    <div className="workflow-card goal-definition-card">
      <div className="card-header">
        <span className="card-icon">🎯</span>
        <h3 className="card-title">Goal Definition</h3>
      </div>
      
      <div className="card-content">
        <p className="card-description">
          What do you want to accomplish today?
        </p>
        
        <div className="goal-input-container">
          <textarea
            className="goal-input cognitive-space"
            placeholder="Describe your goal in natural language..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            rows={3}
          />
        </div>
        
        {isAnalyzing && (
          <div className="analysis-indicator cognitive-flow">
            <span className="analysis-symbol">△</span>
            <span>Mao analyzing your request...</span>
          </div>
        )}
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="trust"
          onClick={handleSubmit}
          disabled={!goal.trim() || isAnalyzing}
          loading={isAnalyzing}
        >
          Analyze Goal
        </CognitiveButton>
      </div>
    </div>
  );
};

const WorkflowSuggestionCard = ({ 
  suggestion, 
  onAccept, 
  onModify 
}) => {
  return (
    <div className="workflow-card suggestion-card">
      <div className="card-header">
        <span className="card-icon">✨</span>
        <h3 className="card-title">Workflow Suggestion</h3>
      </div>
      
      <div className="card-content">
        <div className="suggestion-summary">
          <div className="workflow-name">
            <span className="orchestrator-symbol">▲</span>
            <span>Recommended: {suggestion.name}</span>
          </div>
          
          <div className="workflow-details">
            <div className="detail-item">
              <span className="agent-symbols">
                {suggestion.agents.map((_, i) => (
                  <span key={i} className="agent-symbol">○</span>
                ))}
              </span>
              <span>{suggestion.agents.length} agents will coordinate</span>
            </div>
            
            <div className="detail-item">
              <span className="time-icon">⏱️</span>
              <span>Estimated: {suggestion.estimatedTime}</span>
            </div>
            
            <div className="detail-item">
              <span className="cost-icon">💰</span>
              <span>Cost: {suggestion.estimatedCost}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="stop"
          onClick={onAccept}
          size="large"
        >
          Start Workflow
        </CognitiveButton>
        
        <CognitiveButton
          type="space"
          onClick={onModify}
          size="medium"
        >
          Modify Settings
        </CognitiveButton>
      </div>
    </div>
  );
};

const ExecutionMonitoringCard = ({ 
  workflowStatus, 
  currentPhase, 
  progress, 
  onPause,
  onStop 
}) => {
  return (
    <div className="workflow-card execution-card">
      <div className="card-header">
        <span className="card-icon">🔄</span>
        <h3 className="card-title">Workflow Execution</h3>
      </div>
      
      <div className="card-content">
        <div className="execution-status">
          <div className="status-line">
            <span className="orchestrator-active">▲</span>
            <span className="status-text">{workflowStatus.name} Running</span>
          </div>
          
          <div className="agents-status">
            {workflowStatus.agents.map((agent, index) => (
              <div key={agent.id} className="agent-status-line">
                <span className={`agent-symbol ${agent.status === 'active' ? 'agent-active' : 'agent-waiting'}`}>
                  {agent.status === 'active' ? '●' : '○'}
                </span>
                <span className="agent-task">
                  Agent {index + 1}: {agent.currentTask}
                </span>
              </div>
            ))}
          </div>
          
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="progress-text">{progress}%</span>
          </div>
        </div>
      </div>
      
      <div className="card-actions">
        <CognitiveButton
          type="space"
          onClick={onPause}
          size="medium"
        >
          Pause
        </CognitiveButton>
        
        <CognitiveButton
          type="stop"
          onClick={onStop}
          size="medium"
        >
          Stop Workflow
        </CognitiveButton>
      </div>
    </div>
  );
};

export { GoalDefinitionCard, WorkflowSuggestionCard, ExecutionMonitoringCard };
```

#### **Card Styling with Mobile-First Approach**

```css
/* WorkflowCards.css */
.workflow-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin: 16px 0;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid var(--cognitive-space-light);
}

.workflow-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 20px 16px 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid var(--cognitive-space-light);
}

.card-icon {
  font-size: 24px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--cognitive-trust);
  border-radius: 8px;
  color: white;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #2c3e50;
}

.card-content {
  padding: 20px;
}

.card-actions {
  padding: 16px 20px 20px 20px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Goal Definition Card Specific */
.goal-input-container {
  margin: 16px 0;
}

.goal-input {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid var(--cognitive-space);
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
  min-height: 80px;
  transition: border-color 0.3s ease;
}

.goal-input:focus {
  outline: none;
  border-color: var(--cognitive-trust);
  box-shadow: 0 0 0 3px rgba(130, 208, 255, 0.2);
}

.analysis-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  animation: pulse-flow 2s infinite;
}

@keyframes pulse-flow {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Suggestion Card Specific */
.suggestion-summary {
  space-y: 16px;
}

.workflow-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--cognitive-stop);
  margin-bottom: 16px;
}

.orchestrator-symbol {
  color: var(--cognitive-stop);
  font-size: 20px;
}

.workflow-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4a5568;
}

.agent-symbols {
  display: flex;
  gap: 2px;
}

.agent-symbol {
  color: var(--cognitive-flow);
  font-size: 16px;
}

/* Execution Card Specific */
.execution-status {
  space-y: 16px;
}

.status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.orchestrator-active {
  color: var(--cognitive-stop);
  font-size: 18px;
  animation: pulse-orchestrator 2s infinite;
}

.agents-status {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.agent-status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.agent-symbol.agent-active {
  color: var(--cognitive-flow);
  animation: pulse-agent 1.5s infinite;
}

.agent-symbol.agent-waiting {
  color: var(--cognitive-space);
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: var(--cognitive-space-light);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--cognitive-trust) 0%, var(--cognitive-flow) 100%);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-text {
  font-weight: 600;
  color: var(--cognitive-trust);
  min-width: 40px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .workflow-card {
    margin: 12px 0;
    border-radius: 12px;
  }
  
  .card-header {
    padding: 16px;
  }
  
  .card-content {
    padding: 16px;
  }
  
  .card-actions {
    padding: 12px 16px 16px 16px;
    flex-direction: column;
  }
  
  .card-actions button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .workflow-card {
    margin: 8px;
    border-radius: 8px;
  }
  
  .goal-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}
```

### Gesture-Inspired Desktop Interactions

#### **Swipe-Like Navigation Component**

```jsx
// components/SwipeNavigation.jsx
import React, { useState, useRef, useEffect } from 'react';
import './SwipeNavigation.css';

const SwipeNavigation = ({ 
  children, 
  currentIndex = 0, 
  onIndexChange,
  showDots = true 
}) => {
  const containerRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [currentX, setCurrentX] = useState(0);
  const [translateX, setTranslateX] = useState(0);

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setStartX(e.clientX);
    setCurrentX(e.clientX);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    
    setCurrentX(e.clientX);
    const deltaX = e.clientX - startX;
    setTranslateX(deltaX);
  };

  const handleMouseUp = () => {
    if (!isDragging) return;
    
    setIsDragging(false);
    const deltaX = currentX - startX;
    const threshold = 100; // Minimum swipe distance
    
    if (Math.abs(deltaX) > threshold) {
      if (deltaX > 0 && currentIndex > 0) {
        // Swiped right - go to previous
        onIndexChange(currentIndex - 1);
      } else if (deltaX < 0 && currentIndex < children.length - 1) {
        // Swiped left - go to next
        onIndexChange(currentIndex + 1);
      }
    }
    
    setTranslateX(0);
  };

  const getTransform = () => {
    const baseTransform = -(currentIndex * 100);
    const dragOffset = isDragging ? (translateX / containerRef.current?.offsetWidth) * 100 : 0;
    return `translateX(${baseTransform + dragOffset}%)`;
  };

  return (
    <div className="swipe-navigation">
      <div 
        className="swipe-container"
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{
          transform: getTransform(),
          transition: isDragging ? 'none' : 'transform 0.3s ease'
        }}
      >
        {children.map((child, index) => (
          <div key={index} className="swipe-item">
            {child}
          </div>
        ))}
      </div>
      
      {showDots && (
        <div className="swipe-dots">
          {children.map((_, index) => (
            <button
              key={index}
              className={`swipe-dot ${index === currentIndex ? 'active' : ''}`}
              onClick={() => onIndexChange(index)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Usage example for workflow stages
const WorkflowStageNavigation = () => {
  const [currentStage, setCurrentStage] = useState(0);
  
  const stages = [
    <GoalDefinitionCard onGoalSubmit={handleGoalSubmit} />,
    <WorkflowSuggestionCard suggestion={suggestion} onAccept={handleAccept} />,
    <ExecutionMonitoringCard workflowStatus={status} progress={progress} />
  ];

  return (
    <SwipeNavigation
      currentIndex={currentStage}
      onIndexChange={setCurrentStage}
    >
      {stages}
    </SwipeNavigation>
  );
};
```

---

## Chapter 5.3: Technical Data Flow Visualizations

### Mermaid Diagram Components with Cognitive Colors

#### **Dynamic Workflow Visualization**

```jsx
// components/WorkflowVisualization.jsx
import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

const WorkflowVisualization = ({ workflowData, type = 'execution' }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    mermaid.initialize({
      theme: 'base',
      themeVariables: {
        primaryColor: '#82d0ff',      // cognitive-trust
        primaryTextColor: '#2c3e50',
        primaryBorderColor: '#5fa9cc', // cognitive-trust-dark
        lineColor: '#bbbcbb',         // cognitive-space
        secondaryColor: '#f1d771',    // cognitive-flow
        tertiaryColor: '#ff49ff',     // cognitive-stop
        background: '#ffffff',
        mainBkg: '#f8f9fa',
        secondBkg: '#e9ecef',
        tertiaryBkg: '#dee2e6'
      }
    });
  }, []);

  const generateMermaidDiagram = () => {
    switch (type) {
      case 'execution':
        return `
          graph LR
            A[User Goal: "${workflowData.goal}"] --> B[Intent Parser]
            B --> C[Tool Selection Engine]
            C --> D[Agent Coordination Layer]
            D --> E[${workflowData.agents[0]}]
            D --> F[${workflowData.agents[1]}]
            D --> G[${workflowData.agents[2]}]
            E --> H[Data Collection]
            F --> I[Analysis]
            G --> J[Report Generation]
            H --> K[Results Aggregation]
            I --> K
            J --> K
            K --> L[Deliverable: ${workflowData.deliverable}]
            
            classDef userInput fill:#f1d771,stroke:#d4b851,stroke-width:2px
            classDef processing fill:#82d0ff,stroke:#5fa9cc,stroke-width:2px
            classDef coordination fill:#ff49ff,stroke:#cc39cc,stroke-width:2px
            classDef agents fill:#bbbcbb,stroke:#959695,stroke-width:2px
            classDef output fill:#82d0ff,stroke:#5fa9cc,stroke-width:3px
            
            class A userInput
            class B,C processing
            class D coordination
            class E,F,G agents
            class L output
        `;
        
      case 'architecture':
        return `
          graph TB
            subgraph "User Interface Layer"
              A[Terminal UI]
              B[Conversation Bridge]
            end
            
            subgraph "Orchestration Layer"
              C[Core Orchestrator]
              D[Agent Callback System]
              E[Memory MCP]
            end
            
            subgraph "Tool Ecosystem"
              F[Research Tool]
              G[Analysis Tool]
              H[Generation Tool]
            end
            
            A --> B
            B --> C
            C --> D
            D --> E
            D --> F
            D --> G
            D --> H
            
            classDef interface fill:#f1d771,stroke:#d4b851,stroke-width:2px
            classDef orchestration fill:#ff49ff,stroke:#cc39cc,stroke-width:2px
            classDef tools fill:#82d0ff,stroke:#5fa9cc,stroke-width:2px
            
            class A,B interface
            class C,D,E orchestration
            class F,G,H tools
        `;
        
      default:
        return `graph TD; A[Default] --> B[Diagram]`;
    }
  };

  useEffect(() => {
    if (chartRef.current) {
      const diagramDefinition = generateMermaidDiagram();
      mermaid.render('mermaid-chart', diagramDefinition).then(({ svg }) => {
        chartRef.current.innerHTML = svg;
      });
    }
  }, [workflowData, type]);

  return (
    <div className="workflow-visualization">
      <div ref={chartRef} className="mermaid-container" />
    </div>
  );
};

// Real-time workflow progress visualization
const LiveWorkflowProgress = ({ workflowStatus }) => {
  const generateProgressDiagram = () => {
    const { currentPhase, completedPhases, agents } = workflowStatus;
    
    let diagram = `graph LR\n`;
    
    // Add phases
    workflowStatus.phases.forEach((phase, index) => {
      const isCompleted = completedPhases.includes(phase.name);
      const isCurrent = currentPhase === phase.name;
      
      diagram += `  ${phase.id}[${phase.name}]\n`;
      
      if (index > 0) {
        diagram += `  ${workflowStatus.phases[index-1].id} --> ${phase.id}\n`;
      }
    });
    
    // Add styling based on status
    diagram += `\n`;
    workflowStatus.phases.forEach((phase) => {
      const isCompleted = completedPhases.includes(phase.name);
      const isCurrent = currentPhase === phase.name;
      
      if (isCompleted) {
        diagram += `  class ${phase.id} completed\n`;
      } else if (isCurrent) {
        diagram += `  class ${phase.id} current\n`;
      } else {
        diagram += `  class ${phase.id} pending\n`;
      }
    });
    
    diagram += `
      classDef completed fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
      classDef current fill:#ff49ff,stroke:#cc39cc,stroke-width:3px,color:#fff
      classDef pending fill:#bbbcbb,stroke:#959695,stroke-width:1px
    `;
    
    return diagram;
  };

  return (
    <div className="live-progress-visualization">
      <h4>Workflow Progress</h4>
      <WorkflowVisualization 
        workflowData={{ 
          customDiagram: generateProgressDiagram() 
        }} 
        type="custom" 
      />
      
      <div className="progress-legend">
        <div className="legend-item">
          <span className="legend-dot completed"></span>
          <span>Completed</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot current"></span>
          <span>Current</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot pending"></span>
          <span>Pending</span>
        </div>
      </div>
    </div>
  );
};
```

---

## Chapter 5.4: Brand Identity & Implementation Guidelines

### Complete CSS Design System

#### **Typography System**

```css
/* Typography.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Typography Scale */
  --font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
  
  /* Font Sizes */
  --font-size-xs: 0.75rem;     /* 12px */
  --font-size-sm: 0.875rem;    /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;    /* 18px */
  --font-size-xl: 1.25rem;     /* 20px */
  --font-size-2xl: 1.5rem;     /* 24px */
  --font-size-3xl: 1.875rem;   /* 30px */
  --font-size-4xl: 2.25rem;    /* 36px */
  --font-size-5xl: 3rem;       /* 48px */
  
  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;
  
  /* Font Weights */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}

/* Typography Classes */
.mao-heading-1 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  color: #1a202c;
  margin-bottom: 1rem;
}

.mao-heading-2 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  color: #2d3748;
  margin-bottom: 0.75rem;
}

.mao-heading-3 {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.mao-body-large {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-relaxed);
  color: #4a5568;
}

.mao-body-normal {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
  color: #4a5568;
}

.mao-body-small {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
  color: #718096;
}

.mao-caption {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.mao-code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-sm);
  background: #f7fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #e2e8f0;
}

/* Responsive Typography */
@media (max-width: 768px) {
  .mao-heading-1 {
    font-size: var(--font-size-3xl);
  }
  
  .mao-heading-2 {
    font-size: var(--font-size-2xl);
  }
  
  .mao-heading-3 {
    font-size: var(--font-size-xl);
  }
}
```

#### **Complete Button System**

```css
/* Buttons.css */
.mao-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font-family-primary);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  
  /* Focus styles for accessibility */
  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(130, 208, 255, 0.3);
  }
  
  /* Disabled state */
  &.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }
  
  /* Loading state */
  &.loading {
    cursor: wait;
  }
}

/* Size Variations */
.mao-button-small {
  padding: 8px 16px;
  font-size: var(--font-size-sm);
  min-height: 36px;
}

.mao-button-medium {
  padding: 12px 24px;
  font-size: var(--font-size-base);
  min-height: 44px;
}

.mao-button-large {
  padding: 16px 32px;
  font-size: var(--font-size-lg);
  min-height: 52px;
}

/* Cognitive Type Variations */
.mao-button.cognitive-trust {
  background: linear-gradient(135deg, var(--cognitive-trust) 0%, var(--cognitive-trust-dark) 100%);
  color: white;
  border: 1px solid var(--cognitive-trust-dark);
}

.mao-button.cognitive-trust:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-trust-dark) 0%, var(--cognitive-trust) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(130, 208, 255, 0.4);
}

.mao-button.cognitive-stop {
  background: linear-gradient(135deg, var(--cognitive-stop) 0%, var(--cognitive-stop-dark) 100%);
  color: white;
  border: 2px solid var(--cognitive-stop-dark);
  box-shadow: 0 4px 12px rgba(255, 73, 255, 0.3);
}

.mao-button.cognitive-stop:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-stop-dark) 0%, var(--cognitive-stop) 100%);
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(255, 73, 255, 0.5);
}

.mao-button.cognitive-flow {
  background: linear-gradient(135deg, var(--cognitive-flow) 0%, var(--cognitive-flow-dark) 100%);
  color: #2d3748;
  border: 1px solid var(--cognitive-flow-dark);
}

.mao-button.cognitive-flow:hover:not(.disabled) {
  background: linear-gradient(135deg, var(--cognitive-flow-dark) 0%, var(--cognitive-flow) 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(241, 215, 113, 0.4);
}

.mao-button.cognitive-space {
  background: var(--cognitive-space);
  color: #2d3748;
  border: 1px solid var(--cognitive-space-dark);
}

.mao-button.cognitive-space:hover:not(.disabled) {
  background: var(--cognitive-space-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(187, 188, 187, 0.3);
}

/* Button Icons */
.mao-button-icon {
  display: flex;
  align-items: center;
  font-size: 1.2em;
}

.mao-button-text {
  display: flex;
  align-items: center;
}

/* Loading Spinner */
.mao-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Button Groups */
.mao-button-group {
  display: flex;
  gap: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mao-button-group .mao-button {
  border-radius: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.2);
}

.mao-button-group .mao-button:first-child {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.mao-button-group .mao-button:last-child {
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-right: none;
}
```

### Layout & Component System

#### **Grid System**

```css
/* Grid.css */
.mao-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.mao-container-fluid {
  width: 100%;
  padding: 0 16px;
}

.mao-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -8px;
}

.mao-col {
  flex: 1;
  padding: 0 8px;
}

/* Responsive columns */
.mao-col-1 { flex: 0 0 8.333333%; max-width: 8.333333%; }
.mao-col-2 { flex: 0 0 16.666667%; max-width: 16.666667%; }
.mao-col-3 { flex: 0 0 25%; max-width: 25%; }
.mao-col-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
.mao-col-5 { flex: 0 0 41.666667%; max-width: 41.666667%; }
.mao-col-6 { flex: 0 0 50%; max-width: 50%; }
.mao-col-7 { flex: 0 0 58.333333%; max-width: 58.333333%; }
.mao-col-8 { flex: 0 0 66.666667%; max-width: 66.666667%; }
.mao-col-9 { flex: 0 0 75%; max-width: 75%; }
.mao-col-10 { flex: 0 0 83.333333%; max-width: 83.333333%; }
.mao-col-11 { flex: 0 0 91.666667%; max-width: 91.666667%; }
.mao-col-12 { flex: 0 0 100%; max-width: 100%; }

@media (max-width: 768px) {
  .mao-col-sm-12 { flex: 0 0 100%; max-width: 100%; }
  .mao-col-sm-6 { flex: 0 0 50%; max-width: 50%; }
  .mao-col-sm-4 { flex: 0 0 33.333333%; max-width: 33.333333%; }
  .mao-col-sm-3 { flex: 0 0 25%; max-width: 25%; }
}

@media (max-width: 480px) {
  .mao-row {
    margin: 0 -4px;
  }
  
  .mao-col {
    padding: 0 4px;
  }
  
  .mao-col-xs-12 { flex: 0 0 100%; max-width: 100%; }
}
```

#### **Terminal UI Implementation**

```jsx
// components/TerminalUI.jsx
import React, { useState, useRef, useEffect } from 'react';
import './TerminalUI.css';

const TerminalUI = ({ onCommand, history = [] }) => {
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const inputRef = useRef(null);
  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    setIsProcessing(true);
    await onCommand(input);
    setInput('');
    setIsProcessing(false);
    inputRef.current?.focus();
  };

  return (
    <div className="mao-terminal">
      <div className="terminal-header">
        <div className="terminal-controls">
          <span className="terminal-dot terminal-dot-red"></span>
          <span className="terminal-dot terminal-dot-yellow"></span>
          <span className="terminal-dot terminal-dot-green"></span>
        </div>
        <div className="terminal-title">
          Mao - Modular Agent Orchestrator
        </div>
      </div>
      
      <div className="terminal-body" ref={terminalRef}>
        <div className="terminal-welcome">
          <div className="welcome-logo">
            <span className="orchestrator-symbol">△</span>
            <span className="welcome-text">Mao v4.0</span>
          </div>
          <div className="welcome-message">
            Ready to orchestrate AI workflows. Type your goal in natural language.
          </div>
        </div>
        
        {history.map((entry, index) => (
          <div key={index} className={`terminal-entry ${entry.type}`}>
            {entry.type === 'user' && (
              <div className="terminal-user-input">
                <span className="terminal-prompt">$</span>
                <span className="terminal-command">{entry.content}</span>
              </div>
            )}
            
            {entry.type === 'system' && (
              <div className="terminal-system-output">
                <div className="system-header">
                  <span className="orchestrator-active">▲</span>
                  <span className="system-message">{entry.title}</span>
                </div>
                <div className="system-content">
                  {entry.content}
                </div>
              </div>
            )}
            
            {entry.type === 'result' && (
              <div className="terminal-result">
                <div className="result-header">
                  <span className="success-symbol">✅</span>
                  <span className="result-title">{entry.title}</span>
                </div>
                <div className="result-content">
                  {entry.content}
                </div>
              </div>
            )}
          </div>
        ))}
        
        <form onSubmit={handleSubmit} className="terminal-input-form">
          <div className="terminal-input-line">
            <span className="terminal-prompt">$</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What would you like to accomplish?"
              className="terminal-input"
              disabled={isProcessing}
              autoFocus
            />
            {isProcessing && (
              <div className="terminal-processing">
                <span className="processing-spinner">△</span>
                <span>Processing...</span>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default TerminalUI;
```

```css
/* TerminalUI.css */
.mao-terminal {
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  font-family: var(--font-family-mono);
  max-width: 900px;
  margin: 0 auto;
  border: 1px solid #333;
}

.terminal-header {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #333;
}

.terminal-controls {
  display: flex;
  gap: 6px;
}

.terminal-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.terminal-dot-red { background: #ff5f56; }
.terminal-dot-yellow { background: #ffbd2e; }
.terminal-dot-green { background: #27ca3f; }

.terminal-title {
  color: #a0aec0;
  font-size: 14px;
  font-weight: 500;
}

.terminal-body {
  background: #1a1a1a;
  color: #e2e8f0;
  padding: 20px;
  height: 500px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.5;
}

.terminal-welcome {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #333;
}

.welcome-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.orchestrator-symbol {
  color: var(--cognitive-stop);
  font-size: 20px;
}

.welcome-text {
  color: var(--cognitive-trust);
  font-weight: 600;
  font-size: 16px;
}

.welcome-message {
  color: #a0aec0;
  font-size: 13px;
}

.terminal-entry {
  margin-bottom: 16px;
}

.terminal-user-input {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.terminal-prompt {
  color: var(--cognitive-trust);
  font-weight: bold;
}

.terminal-command {
  color: #e2e8f0;
}

.terminal-system-output {
  background: rgba(130, 208, 255, 0.1);
  border: 1px solid var(--cognitive-trust);
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
}

.system-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: var(--cognitive-trust);
  font-weight: 600;
}

.orchestrator-active {
  color: var(--cognitive-stop);
  animation: pulse-orchestrator 2s infinite;
}

.system-content {
  color: #cbd5e0;
  padding-left: 24px;
}

.terminal-result {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid #4CAF50;
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #4CAF50;
  font-weight: 600;
}

.result-content {
  color: #cbd5e0;
  padding-left: 24px;
}

.terminal-input-form {
  position: sticky;
  bottom: 0;
  background: #1a1a1a;
  padding-top: 16px;
  border-top: 1px solid #333;
}

.terminal-input-line {
  display: flex;
  align-items: center;
  gap: 8px;
}

.terminal-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #e2e8f0;
  font-family: inherit;
  font-size: 14px;
  outline: none;
}

.terminal-input::placeholder {
  color: #718096;
}

.terminal-processing {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--cognitive-flow);
  font-size: 12px;
}

.processing-spinner {
  animation: pulse-orchestrator 1.5s infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .mao-terminal {
    border-radius: 0;
    height: 100vh;
  }
  
  .terminal-body {
    height: calc(100vh - 60px);
  }
  
  .terminal-header {
    padding: 16px;
  }
  
  .terminal-body {
    padding: 16px;
  }
}
```

**🎯 EPIC VISUAL DESIGN SYSTEM COMPLETE!**

**What You Now Have:**
- **Complete CSS framework** with cognitive color psychology
- **React component library** for all UI patterns  
- **Mobile-first responsive design** with iOS inspiration
- **Terminal interface** with real-time workflow visualization
- **Mermaid diagram integration** with brand colors
- **Accessible design patterns** with proper ARIA labels
- **Performance-optimized animations** with smooth transitions

**Ready to build the most intuitive AI workflow interface ever created!** 💎✨

The full 5-document suite is now complete - each one packed with implementable code that developers can actually use to build the Mao interface exactly as designed!

---



---


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

### Mao Terminal Interface Design Rules

* **Core Philosophy**
- **Visual graphic design with constraints**: mono text + semantic colors + white space ONLY. 
- Design is what makes people actually USE our functional application.

* **Layout & Spacing Rules**

* **Character Grid Foundation**
1. **Design to the grid** - Terminal columns = character cells (typically 8-10px wide, 16-20px tall)
2. **Grid-based thinking** - Use character cell units (20px grid = character cell dimensions)
3. **Column alignment** - All layouts respect terminal grid constraints (80x24, 60x80, etc.)
4. **Monospace constraints** - Every character occupies exactly one grid cell

* **Paragraph Grouping**
5. **Group related content together** - first 4 lines stay at top, large gap, then input field
6. **Before/after paragraph spacing** - think document spacing, not cramped terminal
7. **Much taller height overall** - let content breathe, we're not fighting for real estate
8. **Double spacing between message blocks** - generous vertical rhythm

* **Horizontal Alignment System**
9. **4ch left alignment** - ALL text content aligns at 4 character spaces from left edge
10. **Tree branches align with content** - `├──` and text content share same left edge
11. **No-indicator lines = RARE emphasis** - even rarer than pink text, used for POWER
12. **Consistent indicator spacing** - `●` + 4ch gap before all text content

* **Typography Constraints**

* **Font & Size Limitations**
13. **One font, one size ONLY** - never change font size due to terminal uncertainty
14. **Monospace grid system** - each character = one grid cell (8-10px wide, 16-20px tall)
15. **Character cell atomic units** - design in character counts, not arbitrary pixels
16. **Grid-first design** - layouts that fit 80x24 or 60x80 work everywhere
17. **No visual chrome** - only semantic colors, character choice, and white space

* **Color System & Hierarchy**

* **Opacity & Subtlety**
18. **Light blue 50% opacity** - trustworthy actions should be subtle, not competing
19. **White 50% opacity** - less prominent for system/automated content
20. **Secondary yellow** - brown mustard with light opacity (like Claude Code)

* **Pink Bold Usage Rules (MOST CRITICAL)**
21. **Pink emphasizes WHAT something happens TO** - not the verb/action
    - ❌ "**Creating** project structure"  
    - ✅ "Creating **project structure**"
22. **One pink statement per viewport** - for 60-row terminals, only one visible pink
23. **Never consecutive pink lines** - increases cognitive load too much
24. **Pink = cognitive interrupt for objects/targets** - draws attention to WHAT needs focus

* **Interaction & State Patterns**

* **Completion Behavior**
25. **Checkmark icon replacement**: `▲ ✓ Portfolio complete!` → `✓ Portfolio complete!`
26. **Collapse completed workflows** - when all sub-items complete, show single confirmation
27. **Two-frame completion states** - show process reaching completion, then collapsed

* **Contextual Options Display**
28. **No command lists unless /slash-command used** - don't show `/preview /data /focus` lists
29. **Main screen options = toggles/choices** - "Deploy now? (y/n)" style
30. **"Popup modules"** have pre-accommodated space - no screen shifting when content appears

* **Workflow Tree Visualization**
31. **Tree characters align with content** - maintain 4ch alignment rule
32. **Shape persistence through states** - triangle stays triangle even when complete
33. **Progressive disclosure** - show hierarchy and relationships through tree structure

* **Content Strategy**

* **Help & Guidance**
34. **Single contextual help message** - not lists of options
35. **Modular help system** - different states pull different contextual messages
36. **Contextual affordances** - not menus/buttons, but situation-aware guidance

* **Message Attribution & Flow**
37. **Clear turn-taking** - visual conversation protocol for human-AI dialogue
38. **Attention management** - color hierarchy guides cognitive flow
39. **Context preservation** - consistent attribution and visual patterns

* **Technical Constraints**

* **Terminal Compatibility**
40. **Work with any terminal theme** - don't override user's background/default colors
41. **ANSI color fallbacks** - graceful degradation for limited color terminals
42. **Cross-platform consistency** - same experience across terminal environments
43. **Grid-based portability** - designs that work in 80x24 work everywhere

* **Performance & Responsiveness**
44. **Real-time updates** - content updates without screen jumping or shifting
45. **Smooth state transitions** - visual continuity during workflow changes
46. **Minimal cognitive load** - predictable patterns reduce mental overhead

* **Quality Standards**

* **Visual Excellence**
47. **Every space is intentional** - precise typography like Sean's original examples
48. **Cognitive architecture** - colors serve brain function, not aesthetics
49. **Professional polish** - terminal UI that rivals graphical applications
50. **Grid-perfect alignment** - respect character cell boundaries

* **User Experience**
51. **Intuitive attribution** - instantly clear who said what
52. **Priority clarity** - what needs attention vs what's informational
53. **Conversation flow** - natural reading and interaction patterns
54. **Wireframe methodology** - design in 20px character grid units for accuracy

---

## Business ROI & Future Evolution Resources for Documentation

### **v4.1.0 - Multi-Instance Foundation** 
*Building the infrastructure for scale*

🔗 **Cross-Instance Analytics Aggregation**
- Unified dashboards across all MAO instances
- Real-time metrics from distributed sources
- Privacy-compliant data aggregation
- **Impact:** Enterprise teams can see organization-wide AI productivity

🤝 **Shared Memory System** 
- Team memory sharing and collaboration
- Collective knowledge building across users
- **Impact:** Teams build on each other's AI workflows and learnings

📊 **Predictive Analytics Engine**
- Machine learning insights for workflow optimization
- Productivity suggestions based on usage patterns
- **Impact:** AI that learns how to make AI more efficient

⚡ **Distributed Cache System**
- Shared cache across multiple instances
- Reduced redundant computations
- **Impact:** Faster performance at enterprise scale

### **v4.2.0 - The Democratization Breakthrough** 
*No technical experience required*

🎨 **Claude Code SDK Integration**
- Users ask MAO for new tools in plain English
- Zero technical knowledge required
- Automated tool creation and deployment
- **Impact:** Designers, marketers, managers can build AI workflows

🏪 **Modular Catalogs**
- Curated tool libraries
- Model and provider marketplaces
- Workflow template collections
- **Impact:** Instant access to community-built AI solutions

📈 **Advanced Analytics Dashboard**
- Personal productivity metrics (like your 40X efficiency story!)
- Team performance insights
- Cost optimization recommendations
- **Impact:** Data-driven AI adoption across organizations

### **v5.0.0 - The Platform Economy**
*Subscription marketplace for AI workflows*

💰 **Subscription Marketplace**
- Premium workflow libraries
- Enterprise-grade tool collections
- Professional template packages
- **Impact:** Sustainable business model + community monetization

🌐 **Enterprise Integration Suite**
- API gateway for external systems
- Single sign-on and security compliance
- Custom deployment options
- **Impact:** Seamless integration into existing enterprise workflows

🔮 **AI-Powered Optimization**
- Automatic workflow improvements
- Predictive cost management
- Smart resource allocation
- **Impact:** AI that continuously improves AI productivity

### **THE ENGAGEMENT REVOLUTION**
*Making AI productivity addictive through data*

#### **Personal Achievement System**
- **"You've orchestrated 47.3 hours of AI productivity"**
- **"Your workflows are 23% more cost-efficient than average"**
- **"You're in the top 15% for tool diversity"**
- **Impact:** Users become emotionally invested in their AI journey

#### **Community Bragging Rights**
- Shareable productivity achievements
- Team leaderboards and challenges
- Industry benchmarking
- **Impact:** Viral organic growth through social proof

#### **Intelligent Insights**
- Personal productivity trends
- Workflow optimization suggestions
- Cost efficiency recommendations
- **Impact:** Users see continuous value and improvement

### **THE MARKET OPPORTUNITY**

**14 million new developers entering by 2030** need accessible AI tools

**Current Problem:**
- AI development is fragmented, slow, risky
- Requires deep technical expertise
- No systematic approach to AI orchestration

**Our Solution:**
- **Proven 40X efficiency gains** (3 weeks → 3 hours)
- **Democratized through Claude Code SDK** (no coding required)
- **Scalable through marketplace model** (sustainable growth)

**The Vision:**
Transform AI from a technical tool into an accessible productivity platform that anyone can master, with built-in community, analytics, and continuous improvement.

---

## Mao's Self-Enhancement Business Growth Planning 

Application becomes self-enhancing by triggering prompts on regular scheduled basis. Maintaining of business opperations, planning and growth, marketing, and more completely automated and self-directed based on live analytical data. 

```bash
# Mao's internal scheduler triggers every Sunday at 2 AM
mao self-enhance --schedule weekly --focus "performance optimization"
```

### Weekly Self-Enhancement Workflow

1. Weekly assessment of appliation version update goals 
2. Plan workflow to implement proposed features 
3. Assess current features, propose improvements 

#### 1. Actual Future Update Plans 
- Translation agent; application language support 
- Integrate Claude Code SDK for tool builds 
- Build subscription-based workflow and tool catalog 

#### 2. Spawn Feature Implementation Subagents 
- Build out system infrastructure 
- Create new tools and workflows
- Create digital properties and ads 
- Maintain web subscription service offerings 

#### 3. RAG Enhanced Legal Agent 
- Legal guidance for business decisions
- Regulatory compliance checking across industries
- Policy adherence monitoring for enterprise clients
- Risk assessment for new initiatives
- Documentation audit ensuring legal standards

#### 4. RAG-Implemented Compliance Agent
- Accesses federal regulations database
- Industry-specific compliance requirements
- Legal precedent knowledge
- Real-time regulatory updates

#### 5. Self-Marketing Coordinator 
- Regular workflow producing direct marketing
- Monthly analytic report preparations 
- Business plan proposals based on user patterns 

#### 6. Ongoing Business Accounting
- Research and prepare tax and business obligations 
- Maintain subscription backend payments 
- Monthly, quarterly, and yearly revenue reporting 
- Regular budget analysis; decision making for savings 
- Investment research and analysis 
- Investment portfolio management 

#### 7. User Contact and Support
- What features are users requesting?
- Which workflows are most popular?
- Where do users get stuck?

#### 8. Full-Time Developer (Claude Code SDK)
- Setup user-requested tools 
- Add any modular variable to collections 
- QA and validation testing after every update 
- Maintain new file touch-points; tech documentation updates 

With the **v4.2.0 Claude Code SDK integration**, users will literally be able to say:
- *"Create me a compliance agent that checks our marketing copy against FTC guidelines"*
- *"Build a research agent that monitors patent filings in our industry"*
- *"Make a business intelligence agent that tracks competitor pricing"*

#### 9. Baby Subagents Roaming the Internet 

- Web scraping agents gathering market intelligence
- Social media monitoring agents tracking brand mentions
- Competitive analysis agents watching industry trends
- Research agents compiling technical documentation
- Data mining agents extracting business insights

### The Beautiful Meta-Loop

Give Mao a built-in evolutionary mechanism that uses data for decision making and subsequent workflow planning. 

- **Self-analyzing** its performance and user satisfaction
- **Self-optimizing** its code and workflows  
- **Self-expanding** its capabilities through new tool creation
- **Self-documenting** its improvements and learnings
- **Self-marketing** by demonstrating continuous value growth

*This is the future of work! The modular-agent-orchestrator becomes the spawning ground for an entire ecosystem of intelligent subagents*

---

**Key points to highlight in this structured pitch document**
1. **Technical roadmap** that builds logically from foundation to marketplace
2. **Democratization story** that shows how we make AI accessible
3. **Engagement strategy** that keeps users invested and growing
4. **Market opportunity** that validates the 14M developer thesis
