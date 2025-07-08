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
  
  async executeCommand(command: string, args?: string): Promise<any> {
    // HTTP call to Python cli_manager.py via FastAPI
    const response = await fetch(`${this.baseURL}/cli/${command}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ args, source: 'typescript-terminal' })
    });
    return response.json();
  }
  
  async getAutoCompleteOptions(partial: string): Promise<string[]> {
    // Get CLI commands from Python backend
    const response = await fetch(`${this.baseURL}/autocomplete?q=${partial}`);
    return response.json();
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

*This specification ensures we build exactly what the foundation_spec.md calls for: a professional, conversation-driven terminal interface that integrates seamlessly with existing systems while maintaining the unique visual identity and avoiding all previous architectural mistakes.*