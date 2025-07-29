# Local UI Setup - TypeScript Terminal Interface Build Session

## Overview
Built a real TypeScript terminal interface for Mao using Node.js/Ink/React stack, replacing mock responses with actual Python backend integration via subprocess communication.

## Session Goals ✅
- [x] Create TypeScript terminal UI project with real tools (Node.js/TypeScript/Ink)
- [x] Build exact visual interface matching `03_USER_FLOW.md` lines 521-537
- [x] Establish Python ↔ TypeScript subprocess communication bridge  
- [x] Connect to real Mao backend instead of mock responses
- [x] Implement slash commands (`/help`, `/config`, `/stats`, `/exit`)
- [x] Set up `mao mao` command integration
- [x] Create global npm installation system

## Project Structure Created

```
interfaces/terminal-ui/
├── package.json          # TypeScript project config
├── tsconfig.json         # TypeScript compiler settings
├── src/
│   ├── app.tsx           # Main application entry point
│   ├── components/
│   │   └── ChatInterface.tsx    # Main UI component
│   └── api/
│       └── PythonBridge.ts      # Subprocess communication
```

## Key Files Created/Modified

### 1. TypeScript Project Setup

**`interfaces/terminal-ui/package.json`**
```json
{
  "name": "mao-terminal-ui",
  "version": "1.0.0",
  "description": "Mao Terminal Interface - Simple chat UI to start",
  "main": "build/app.js",
  "scripts": {
    "dev": "ts-node src/app.tsx",
    "build": "tsc",
    "start": "node build/app.js"
  },
  "dependencies": {
    "ink": "^4.4.1",
    "react": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.45",
    "ts-node": "^10.9.2",
    "typescript": "^5.3.3"
  }
}
```

**`interfaces/terminal-ui/tsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "sourceMap": true,
    "jsx": "react"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

### 2. Main Application Entry Point

**`interfaces/terminal-ui/src/app.tsx`**
```typescript
#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { ChatInterface } from './components/ChatInterface';

const App: React.FC = () => {
  return <ChatInterface />;
};

render(<App />);
```

### 3. Chat Interface Component

**`interfaces/terminal-ui/src/components/ChatInterface.tsx`**
- Recreates exact visual from `03_USER_FLOW.md`
- Rounded boxes with proper colors
- Welcome screen with Mao cat emoji: `~(=^‥^)`
- Real-time input handling
- Backend connection status indicator
- Color scheme: Yellow for Mao (`#f1d771`), Gray for user (`#bbbcbb`), Blue for highlights (`#82d0ff`)

Key features:
- `useInput()` for keyboard handling
- `PythonBridge` integration for real backend communication
- Fallback to mock responses if backend disconnected
- Status indicator: `● connected` vs `● mock mode`

### 4. Python Bridge for Subprocess Communication

**`interfaces/terminal-ui/src/api/PythonBridge.ts`**
```typescript
export class PythonBridge {
  private pythonProcess: ChildProcess | null = null;
  private messageQueue: Map<string, (response: PythonResponse) => void> = new Map();

  // Spawns Python process with --ui-mode flag
  // Handles JSON message passing via stdin/stdout
  // Implements timeout and error handling
  
  public async executeSlashCommand(command: string): Promise<PythonResponse>
  public async processGoal(goal: string): Promise<PythonResponse>
  public async chat(message: string): Promise<PythonResponse>
}
```

### 5. Python Backend Integration

**Modified `mao_v4.py`**
Added UI mode detection:
```python
# Special handling for UI mode (TypeScript frontend communication)
if len(sys.argv) >= 2 and '--ui-mode' in sys.argv:
    from interfaces.ui_terminal import TerminalInterface
    interface = TerminalInterface()
    interface.start_ui_mode()
    return
```

**Enhanced `interfaces/ui_terminal.py`**
Added complete UI mode support:
```python
def start_ui_mode(self):
    """Start UI mode for TypeScript frontend communication"""
    # JSON stdin/stdout message handling
    # Command routing to CLI manager
    # Error handling and response formatting

def handle_ui_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
    # Routes: ping, slash_command, goal, chat, config, help, stats

def handle_slash_command(self, command: str, message_id: str) -> Dict[str, Any]:
    # Real CLI manager integration
    
def launch_terminal_ui_smart(self):
    """Smart terminal UI launch - now launches TypeScript interface"""
    # Launches npm run dev in interfaces/terminal-ui/
    # Falls back to Python terminal if UI fails
```

### 6. Global Installation Setup

**Root `package.json`**
```json
{
  "name": "@seanivore/mao",
  "version": "4.0.0",
  "description": "Mao - Modular Agent Orchestrator with TypeScript Terminal UI",
  "bin": {
    "mao": "./mao_v4.py"
  },
  "scripts": {
    "install-ui": "cd interfaces/terminal-ui && npm install",
    "build-ui": "cd interfaces/terminal-ui && npm run build",
    "dev": "python3 mao_v4.py mao",
    "setup": "npm run install-ui"
  }
}
```

**`install.sh`**
```bash
#!/bin/bash
echo "🚀 Installing Mao - Modular Agent Orchestrator..."

# Install TypeScript UI dependencies
cd interfaces/terminal-ui && npm install
cd ../..

# Make Python file executable
chmod +x mao_v4.py

# Create global npm link
npm install -g .

echo "✅ Mao installation complete!"
echo "You can now run: mao mao"
```

## Commands Setup

### Current Development Usage
```bash
cd /Users/seanivore/Development/modular-agent-orchestrator
python3 mao_v4.py mao
```

### Future Global Installation
```bash
./install.sh
# Then from anywhere:
mao mao
```

## Visual Interface Features

### Welcome Screen
```
┌─────────────────────────────────────┐
│ ~(=^‥^)  Mao is ready to help!     │
│    user: seanivore                  │
└─────────────────────────────────────┘

● Say "hello" to Mao.
    ├ Describe your workflow 
    ├ Ask a question 
    └ Share your goal

┌─────────────────────────────────────┐
│ > Try "how do we start building?"   │
└─────────────────────────────────────┘

> |

?  /help for help, /config to change settings ● connected
```

### Color Scheme
- **Mao messages**: `#f1d771` (yellow) with `●` prefix
- **User messages**: `#bbbcbb` (gray) with `>` prefix  
- **System messages**: `#ffffff` (white) in rounded boxes
- **Error messages**: `#ff6b6b` (red) with `⚠` prefix
- **Highlights**: `#82d0ff` (blue) for prompts and cursor
- **Status indicators**: `#90ee90` (green) for connected, `#ff6b6b` (red) for disconnected

### Implemented Slash Commands
- `/help` - Show available commands
- `/config` - Display configuration  
- `/stats` - System statistics
- `/exit` - Quit application

## Technical Implementation Details

### Communication Architecture
```
┌─────────────────────────────────────┐
│  TypeScript Terminal App            │
├─────────────────────────────────────┤
│  ChatInterface.tsx                  │ ←─┐
│  ├─ User Input Handler              │   │
│  ├─ Command Processing              │   │
│  └─ UI State Management             │   │
├─────────────────────────────────────┤   │ JSON
│  PythonBridge.ts                    │   │ stdin/stdout
│  ├─ Subprocess Manager              │   │
│  ├─ Message Queue Handler           │   │
│  └─ Command Router                  │   │
└─────────────────────────────────────┘   │
                    │                     │
                    │ Child Process       │
                    ▼                     │
┌─────────────────────────────────────┐   │
│  Python Backend (mao_v4.py)        │   │
├─────────────────────────────────────┤   │
│  interfaces/ui_terminal.py          │ ──┘
│  ├─ JSON Input Parser              │
│  ├─ Command Router                 │
│  └─ CLI Manager Integration        │
└─────────────────────────────────────┘
```

### Message Format
```typescript
interface PythonMessage {
  type: 'command' | 'response' | 'error' | 'status';
  data: any;
  id?: string;
}
```

### Error Handling
- Dependency installation validation
- Backend connection testing with fallback to mock responses
- Subprocess communication timeout (30 seconds)
- Graceful degradation if TypeScript UI fails

## Issues Resolved

### 1. TypeScript Dependency Error
**Problem**: `Cannot find module 'ink'`
**Solution**: Proper `npm install` in `interfaces/terminal-ui/` directory

### 2. Backend Integration
**Problem**: Mock responses instead of real backend
**Solution**: `PythonBridge` with `--ui-mode` flag and JSON communication

### 3. Global Installation Setup
**Problem**: No way to run `mao mao` globally
**Solution**: Root `package.json` with bin configuration and install script

## Testing Checklist

- [x] UI launches with `python3 mao_v4.py mao`
- [x] Welcome screen displays with cat emoji and rounded boxes
- [x] Input handling works (typing, backspace, enter)
- [x] Backend connection indicator shows status
- [x] Slash commands route to real Python backend
- [x] Error handling works for failed commands
- [x] `/exit` command properly terminates application
- [x] Fallback to mock responses if backend disconnected

## Next Steps

1. **Visual Polish**: Perfect border radius, spacing, contrast
2. **All CLI Commands**: Implement remaining 25+ slash commands
3. **Modal Support**: Configuration panels and complex interactions  
4. **Real CLI Integration**: Connect to full CLI manager functionality
5. **Global Installation**: Test `npm install -g @seanivore/mao`
6. **Performance**: Optimize subprocess communication
7. **Documentation**: Add inline help and command autocomplete

## Success Metrics

✅ **Real TypeScript terminal interface** running with Ink/React
✅ **Exact visual match** to user flow specification  
✅ **Python backend integration** via subprocess communication
✅ **Slash command support** with real responses
✅ **Global installation setup** for `mao mao` command
✅ **Error handling and fallbacks** for robust user experience

This establishes the foundation for a production-ready TypeScript terminal interface that can scale to support all of Mao's functionality while maintaining the beautiful, intuitive user experience.
