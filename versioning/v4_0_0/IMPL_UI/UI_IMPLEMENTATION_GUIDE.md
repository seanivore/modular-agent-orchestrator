# MAO TypeScript UI Implementation Guide
*Complete One-Stop-Shop Guide for Python→TypeScript Terminal Interface*

## Executive Summary

This guide provides complete implementation specifications for building the MAO TypeScript terminal interface that bridges with the existing Python backend. All core systems exist and work; this implementation creates the professional terminal UI layer using the same technology stack as Claude Code (TypeScript/Node.js with Ink).

**Implementation Scope:**
- Professional conversation-driven terminal interface using TypeScript/Node.js
- React-based terminal components using Ink 4.4+ (same as Claude Code)
- HTTP/WebSocket bridge to existing Python backend
- Git-style CLI integration with autocomplete and progress visualization
- Rich terminal formatting with graceful fallback patterns

**Current State:** All Python backend systems implemented and tested. UI documentation complete (41 components). Ready for frontend build.

---

## Technical Architecture

### Tech Stack Definition
```
TERMINAL INTERFACE:
├── TypeScript/Node.js (Frontend terminal app)
├── Ink 4.4+ (React for terminals - Claude Code's stack)
├── React 18+ (Component-based UI)
└── Node.js APIs (File system, process management)

BACKEND INTEGRATION:
├── Python 3.11+ (Existing orchestrator - unchanged)
├── Subprocess Communication (stdin/stdout/IPC)
├── JSON Message Passing (Structured communication)
└── Process spawning (Node.js spawns Python child process)

ARCHITECTURE PATTERN:
├── Single Conversation Interface (no menus)
├── Unified Input Handler (natural language + /commands)
├── Event-Driven State Management
└── Real-time Progress Visualization
```

### Communication Architecture
```
┌─────────────────────────────────────┐
│  TypeScript Terminal App            │
├─────────────────────────────────────┤
│  ConversationInterface.tsx          │ ←─┐
│  ├─ User Input Handler               │   │
│  ├─ Command Autocomplete             │   │
│  └─ Progress Visualization           │   │
├─────────────────────────────────────┤   │ JSON
│  PythonBridge.ts                    │   │ stdin/stdout
│  ├─ Subprocess Manager               │   │
│  ├─ Message Queue Handler           │   │
│  └─ Command Router                  │   │
└─────────────────────────────────────┘   │
              │                           │
              │ Child Process             │
              ▼                           │
┌─────────────────────────────────────┐   │
│  Python Backend (Existing)          │   │
├─────────────────────────────────────┤   │
│  interfaces/ui_terminal.py          │ ──┘
│  ├─ JSON Input Parser               │
│  ├─ Command Router                  │
│  └─ JSON Response Formatter         │
├─────────────────────────────────────┤
│  orchestrator/cli_manager.py        │
│  ├─ 30+ CLI Commands                │
│  ├─ Workflow Management             │
│  └─ Tool Integration                │
└─────────────────────────────────────┘
```

---

## Project Structure

### File Organization
```
modular-agent-orchestrator/          ← EXISTING: Main project (LOCAL app)
├── interfaces/
│   ├── ui_terminal.py               ← Enhanced for subprocess communication
│   ├── ui_web.py                    ← Future web interface
│   └── terminal-ui/                 ← NEW: TypeScript terminal interface
│       ├── package.json             ← Dependencies: ink, react, @types/*
│       ├── tsconfig.json            ← TypeScript configuration
│       ├── src/
│       │   ├── app.tsx              ← Main application entry point
│       │   ├── components/
│       │   │   ├── ConversationInterface.tsx ← Primary conversation UI
│       │   │   ├── AutoCompleteSystem.tsx    ← Command suggestions
│       │   │   ├── ProgressVisualization.tsx ← Live workflow progress
│       │   │   ├── VisualProtocol.tsx        ← Color/styling system
│       │   │   ├── LoginInterface.tsx        ← User authentication
│       │   │   └── ErrorDisplay.tsx          ← Error handling UI
│       │   ├── api/
│       │   │   ├── PythonBridge.ts           ← Subprocess communication
│       │   │   ├── CLICommandRouter.ts       ← Command routing logic
│       │   │   ├── MessageHandler.ts         ← stdin/stdout message handling
│       │   │   └── types.ts                  ← TypeScript interfaces
│       │   ├── utils/
│       │   │   ├── display-helpers.ts        ← UI formatting utilities
│       │   │   └── validation.ts             ← Input validation
│       │   └── styles/
│       │       └── protocol.ts               ← Visual design system
│       ├── build/                            ← Compiled JavaScript output
│       └── node_modules/                     ← npm dependencies
├── orchestrator/                    ← All backend logic (keep as-is)
├── configs/                         ← All configurations (keep as-is)
└── tools/                           ← All tools (keep as-is)
```

### Integration Points
- **Python Backend**: Keep all existing files unchanged
- **Communication Bridge**: Enhance `ui_terminal.py` for subprocess stdin/stdout communication
- **Configuration Sync**: TypeScript reads config files directly from local filesystem
- **State Management**: JSON message passing for real-time updates

---

## Core Components Implementation

### 1. Main Application Entry (app.tsx)
```typescript
// src/app.tsx
import React from 'react';
import { render } from 'ink';
import { ConversationInterface } from './components/ConversationInterface';

const App: React.FC = () => {
  return <ConversationInterface />;
};

render(<App />);
```

### 2. Primary Conversation Interface
```typescript
// src/components/ConversationInterface.tsx
import React, { useState, useEffect } from 'react';
import { Box, Text, useInput, useApp } from 'ink';
import { PythonBridge } from '../api/PythonBridge';
import { AutoCompleteSystem } from './AutoCompleteSystem';
import { ProgressVisualization } from './ProgressVisualization';
import { VisualProtocol } from './VisualProtocol';

interface ConversationMessage {
  type: 'user' | 'ai' | 'system';
  content: string;
  timestamp: Date;
  metadata?: any;
}

export const ConversationInterface: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentWorkflow, setCurrentWorkflow] = useState<string | null>(null);
  const { exit } = useApp();
  
  const pythonAPI = new PythonBridge();
  
  useEffect(() => {
    // Initialize connection to Python backend
    pythonAPI.initialize().then(() => {
      addMessage('system', '🎯 Mao ready! What would you like to create?');
    });
  }, []);
  
  const addMessage = (type: ConversationMessage['type'], content: string, metadata?: any) => {
    setMessages(prev => [...prev, { type, content, timestamp: new Date(), metadata }]);
  };
  
  const handleInput = async (userInput: string) => {
    if (userInput.trim() === '/exit') {
      exit();
      return;
    }
    
    addMessage('user', userInput);
    setIsProcessing(true);
    
    try {
      let result;
      
      if (userInput.startsWith('/')) {
        // CLI command execution
        const command = userInput.slice(1).split(' ')[0];
        const args = userInput.slice(command.length + 2);
        result = await pythonAPI.executeCommand(command, args);
      } else {
        // Natural language goal processing
        result = await pythonAPI.executeCommand('goal', userInput);
      }
      
      // Handle different response types
      await handleResponse(result);
      
    } catch (error) {
      addMessage('system', `❌ Error: ${error.message}`, { error: true });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleResponse = async (response: any) => {
    const { display_type, content, workflow_id } = response;
    
    switch (display_type) {
      case 'workflow_created':
        setCurrentWorkflow(workflow_id);
        addMessage('ai', `✅ Workflow created! ID: ${workflow_id}`);
        addMessage('ai', content.description);
        break;
        
      case 'help_categories':
        addMessage('ai', formatHelpCategories(content));
        break;
        
      case 'error':
        addMessage('system', `❌ ${content.error_message}`, { error: true });
        break;
        
      default:
        addMessage('ai', content.message || JSON.stringify(content, null, 2));
    }
  };
  
  const formatHelpCategories = (categories: any) => {
    return categories.map((cat: any) => 
      `${cat.icon} ${cat.name}: ${cat.description}`
    ).join('\n');
  };
  
  useInput((input) => {
    if (input === 'q') {
      exit();
    }
  });
  
  return (
    <Box flexDirection="column" padding={1}>
      <VisualProtocol.Header />
      
      {/* Message History */}
      <Box flexDirection="column" marginY={1}>
        {messages.map((msg, idx) => (
          <VisualProtocol.Message key={idx} message={msg} />
        ))}
      </Box>
      
      {/* Current Workflow Progress */}
      {currentWorkflow && (
        <ProgressVisualization workflowId={currentWorkflow} />
      )}
      
      {/* Input Area */}
      <Box marginTop={1}>
        <VisualProtocol.InputPrompt 
          value={input}
          onChange={setInput}
          onSubmit={handleInput}
          isProcessing={isProcessing}
        />
      </Box>
      
      {/* Autocomplete System */}
      <AutoCompleteSystem 
        currentInput={input}
        onSuggestionSelect={(suggestion) => setInput(suggestion)}
      />
    </Box>
  );
};
```

### 3. Python Backend Bridge
```typescript
// src/api/PythonBridge.ts
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

interface PendingCommand {
  id: string;
  resolve: (value: any) => void;
  reject: (error: Error) => void;
  timeout: NodeJS.Timeout;
}

export class PythonBridge {
  private pythonProcess: ChildProcess | null = null;
  private pendingCommands: Map<string, PendingCommand> = new Map();
  private messageBuffer: string = '';
  private progressCallbacks: Map<string, (data: any) => void> = new Map();
  private commandIdCounter: number = 0;
  
  async initialize(): Promise<void> {
    try {
      // Spawn Python subprocess
      const pythonPath = path.join(process.cwd(), '..', '..', 'interfaces', 'ui_terminal.py');
      
      this.pythonProcess = spawn('python3', [pythonPath, '--subprocess-mode'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: path.join(process.cwd(), '..', '..')
      });
      
      this.setupProcessHandlers();
      
      // Test connection with ping command
      await this.executeCommand('ping', '');
      
    } catch (error) {
      throw new Error(`Failed to initialize Python backend: ${error.message}`);
    }
  }
  
  private setupProcessHandlers(): void {
    if (!this.pythonProcess) return;
    
    // Handle stdout messages from Python
    this.pythonProcess.stdout?.on('data', (data: Buffer) => {
      this.messageBuffer += data.toString();
      this.processMessages();
    });
    
    // Handle stderr for errors
    this.pythonProcess.stderr?.on('data', (data: Buffer) => {
      console.error('Python stderr:', data.toString());
    });
    
    // Handle process exit
    this.pythonProcess.on('exit', (code, signal) => {
      console.error(`Python process exited with code ${code}, signal ${signal}`);
      this.rejectAllPendingCommands(new Error('Python process exited unexpectedly'));
    });
    
    // Handle process errors
    this.pythonProcess.on('error', (error) => {
      console.error('Python process error:', error);
      this.rejectAllPendingCommands(error);
    });
  }
  
  private processMessages(): void {
    // Split buffer by newlines to get complete JSON messages
    const lines = this.messageBuffer.split('\n');
    this.messageBuffer = lines.pop() || ''; // Keep incomplete line in buffer
    
    for (const line of lines) {
      if (line.trim()) {
        try {
          const message = JSON.parse(line);
          this.handleMessage(message);
        } catch (error) {
          console.error('Failed to parse message from Python:', line, error);
        }
      }
    }
  }
  
  private handleMessage(message: any): void {
    if (message.type === 'command_response' && message.command_id) {
      // Handle command response
      const pending = this.pendingCommands.get(message.command_id);
      if (pending) {
        clearTimeout(pending.timeout);
        this.pendingCommands.delete(message.command_id);
        
        if (message.error) {
          pending.reject(new Error(message.error));
        } else {
          pending.resolve(message.result);
        }
      }
    } else if (message.type === 'progress_update' && message.workflow_id) {
      // Handle progress update
      const callback = this.progressCallbacks.get(message.workflow_id);
      if (callback) {
        callback(message.data);
      }
    }
  }
  
  async executeCommand(command: string, args?: string): Promise<any> {
    if (!this.pythonProcess || !this.pythonProcess.stdin) {
      throw new Error('Python process not initialized');
    }
    
    return new Promise((resolve, reject) => {
      const commandId = `cmd_${++this.commandIdCounter}`;
      
      // Set up timeout
      const timeout = setTimeout(() => {
        this.pendingCommands.delete(commandId);
        reject(new Error(`Command timeout: ${command}`));
      }, 30000);
      
      // Store pending command
      this.pendingCommands.set(commandId, { id: commandId, resolve, reject, timeout });
      
      // Send command to Python
      const message = {
        type: 'command',
        command_id: commandId,
        command,
        args: args || '',
        timestamp: new Date().toISOString()
      };
      
      this.pythonProcess!.stdin!.write(JSON.stringify(message) + '\n');
    });
  }
  
  async getAutoCompleteOptions(partial: string): Promise<string[]> {
    try {
      const result = await this.executeCommand('autocomplete', partial);
      return result.suggestions || [];
    } catch (error) {
      console.error('Autocomplete error:', error);
      return [];
    }
  }
  
  subscribeToWorkflowProgress(workflowId: string, callback: (data: any) => void): void {
    this.progressCallbacks.set(workflowId, callback);
  }
  
  unsubscribeFromWorkflowProgress(workflowId: string): void {
    this.progressCallbacks.delete(workflowId);
  }
  
  private rejectAllPendingCommands(error: Error): void {
    for (const pending of this.pendingCommands.values()) {
      clearTimeout(pending.timeout);
      pending.reject(error);
    }
    this.pendingCommands.clear();
  }
  
  destroy(): void {
    if (this.pythonProcess) {
      this.pythonProcess.kill();
      this.pythonProcess = null;
    }
    this.rejectAllPendingCommands(new Error('PythonBridge destroyed'));
  }
}
```

### 4. Visual Protocol System
```typescript
// src/components/VisualProtocol.tsx
import React from 'react';
import { Box, Text } from 'ink';

// MAO Color System (from documentation)
const Colors = {
  pink: '#ff49ff',      // AI actions (BOLD only)
  yellow: '#f1d771',    // AI explanations and conversation
  light_blue: '#82d0ff', // Highlighted items and recommendations
  white: '#ffffff',     // System responses
  gray: '#bbbcbb',      // User input and secondary info
  light_brown: '#7b714a' // Tree/metadata and organizational context
} as const;

export const VisualProtocol = {
  Header: () => (
    <Box marginBottom={1}>
      <Text color={Colors.pink} bold>🎯 MAO</Text>
      <Text color={Colors.yellow}> - Modular Agent Orchestrator</Text>
    </Box>
  ),
  
  Message: ({ message }: { message: any }) => {
    const getMessageColor = () => {
      switch (message.type) {
        case 'user': return Colors.gray;
        case 'ai': return Colors.yellow;
        case 'system': return message.metadata?.error ? 'red' : Colors.white;
        default: return Colors.white;
      }
    };
    
    const getPrefix = () => {
      switch (message.type) {
        case 'user': return '> ';
        case 'ai': return '● ';
        case 'system': return '⚡ ';
        default: return '';
      }
    };
    
    return (
      <Box marginY={0}>
        <Text color={getMessageColor()}>
          {getPrefix()}{message.content}
        </Text>
      </Box>
    );
  },
  
  InputPrompt: ({ value, onChange, onSubmit, isProcessing }: {
    value: string;
    onChange: (value: string) => void;
    onSubmit: (value: string) => void;
    isProcessing: boolean;
  }) => (
    <Box>
      <Text color={Colors.light_blue}>
        {isProcessing ? '⟳ Processing... ' : '> '}
      </Text>
      {/* Note: Actual input implementation requires ink's useInput hook */}
    </Box>
  ),
};
```

### 5. Progress Visualization
```typescript
// src/components/ProgressVisualization.tsx
import React, { useState, useEffect } from 'react';
import { Box, Text } from 'ink';
import { PythonBridge } from '../api/PythonBridge';

interface ProgressData {
  workflow_id: string;
  current_phase: string;
  progress_percentage: number;
  estimated_remaining: string;
  active_tools: string[];
}

export const ProgressVisualization: React.FC<{ workflowId: string }> = ({ workflowId }) => {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const pythonAPI = new PythonBridge();
  
  useEffect(() => {
    // Subscribe to progress updates
    pythonAPI.subscribeToWorkflowProgress(workflowId, (data) => {
      setProgress(data);
    });
    
    return () => {
      pythonAPI.unsubscribeFromWorkflowProgress(workflowId);
    };
  }, [workflowId]);
  
  if (!progress) return null;
  
  const progressBar = '█'.repeat(Math.floor(progress.progress_percentage / 10)) + 
                     '░'.repeat(10 - Math.floor(progress.progress_percentage / 10));
  
  return (
    <Box flexDirection="column" marginY={1} paddingX={2} borderStyle="round">
      <Text color="#82d0ff">📈 Workflow Progress</Text>
      <Box marginTop={1}>
        <Text color="#f1d771">Phase: </Text>
        <Text color="white">{progress.current_phase}</Text>
      </Box>
      <Box>
        <Text color="#f1d771">Progress: </Text>
        <Text color="green">[{progressBar}] {progress.progress_percentage}%</Text>
      </Box>
      {progress.active_tools.length > 0 && (
        <Box>
          <Text color="#f1d771">Active: </Text>
          <Text color="#82d0ff">{progress.active_tools.join(', ')}</Text>
        </Box>
      )}
      <Box>
        <Text color="#bbbcbb">ETA: {progress.estimated_remaining}</Text>
      </Box>
    </Box>
  );
};
```

---

## Python Backend Enhancements

### Subprocess Communication Integration
```python
# interfaces/ui_terminal.py (enhance existing file)
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any

class TerminalInterface:
    def __init__(self):
        self.mcp_hub = None
        self.subprocess_mode = False
        
    def run_subprocess_mode(self):
        """Run in subprocess mode for TypeScript communication"""
        self.subprocess_mode = True
        
        # Send ready signal
        self.send_message({
            "type": "ready",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Process incoming commands from stdin
        try:
            for line in sys.stdin:
                if line.strip():
                    try:
                        message = json.loads(line.strip())
                        self.handle_subprocess_message(message)
                    except json.JSONDecodeError as e:
                        self.send_error_message(f"Invalid JSON: {e}")
                        
        except KeyboardInterrupt:
            self.send_message({"type": "shutdown"})
            
    def handle_subprocess_message(self, message: Dict[str, Any]):
        """Handle incoming message from TypeScript frontend"""
        message_type = message.get('type')
        command_id = message.get('command_id')
        
        try:
            if message_type == 'command':
                command = message.get('command')
                args = message.get('args', '')
                
                # Route to existing command handler
                result = self.route_command(command, args)
                
                # Send response back to TypeScript
                self.send_command_response(command_id, result)
                
            elif message_type == 'ping':
                self.send_command_response(command_id, {"status": "pong"})
                
            else:
                self.send_command_response(command_id, None, f"Unknown message type: {message_type}")
                
        except Exception as e:
            self.send_command_response(command_id, None, str(e))
            
    def route_command(self, command: str, args: str = '') -> dict:
        """Route command to appropriate handler with structured response"""
        # Import existing CLI manager (when available)
        try:
            from orchestrator.cli_manager import CLIManager
            cli_manager = CLIManager()
            result = cli_manager.execute_command(command, args)
        except ImportError:
            # Fallback for development/testing
            result = {"message": f"Executed {command} with args: {args}"}
        
        # Ensure response is structured for TypeScript consumption
        if not isinstance(result, dict):
            result = {"content": result, "display_type": "text"}
            
        result.update({
            "command": command,
            "timestamp": datetime.utcnow().isoformat(),
            "subprocess_safe": True
        })
        
        return result
        
    def send_command_response(self, command_id: str, result: Dict[str, Any] = None, error: str = None):
        """Send command response back to TypeScript"""
        response = {
            "type": "command_response",
            "command_id": command_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
            
        self.send_message(response)
        
    def send_progress_update(self, workflow_id: str, progress_data: dict):
        """Send progress update to TypeScript client"""
        self.send_message({
            "type": "progress_update",
            "workflow_id": workflow_id,
            "data": progress_data,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    def send_message(self, message: Dict[str, Any]):
        """Send JSON message to TypeScript via stdout"""
        if self.subprocess_mode:
            print(json.dumps(message), flush=True)
            
    def send_error_message(self, error: str):
        """Send error message to TypeScript"""
        self.send_message({
            "type": "error",
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        })

# Add subprocess mode argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--subprocess-mode', action='store_true', 
                       help='Run in subprocess mode for TypeScript communication')
    args = parser.parse_args()
    
    interface = TerminalInterface()
    
    if args.subprocess_mode:
        interface.run_subprocess_mode()
    else:
        # Normal terminal mode (existing functionality)
        interface.launch_terminal_ui_smart()
```

---

## Package Configuration

### package.json
```json
{
  "name": "mao-terminal-ui",
  "version": "1.0.0",
  "description": "MAO Professional Terminal Interface",
  "main": "build/app.js",
  "scripts": {
    "dev": "ts-node src/app.tsx",
    "build": "tsc",
    "start": "node build/app.js",
    "test": "jest",
    "lint": "eslint src/**/*.{ts,tsx}"
  },
  "dependencies": {
    "ink": "^4.4.0",
    "react": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "ts-node": "^10.9.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.50.0",
    "@typescript-eslint/eslint-plugin": "^6.7.0",
    "jest": "^29.7.0"
  },
  "bin": {
    "mao": "./build/app.js"
  }
}
```

### tsconfig.json
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
    "declarationMap": true,
    "sourceMap": true,
    "jsx": "react"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

---

## Implementation Steps

### Phase 1: Foundation Setup
1. **Initialize TypeScript Project**
   ```bash
   mkdir interfaces/terminal-ui
   cd interfaces/terminal-ui
   npm init -y
   npm install ink react
   npm install -D typescript @types/react ts-node @types/node
   ```

2. **Create Basic Project Structure**
   ```bash
   mkdir -p src/{components,api,utils,styles}
   touch src/app.tsx src/components/ConversationInterface.tsx
   touch src/api/PythonBridge.ts tsconfig.json
   ```

3. **Implement Core Components**
   - Start with `app.tsx` and basic `ConversationInterface`
   - Add `PythonBridge.ts` with HTTP client
   - Implement `VisualProtocol.tsx` for styling

### Phase 2: Python Integration
1. **Enhance ui_terminal.py**
   - Add subprocess mode argument parsing
   - Add stdin/stdout JSON message handling
   - Implement command routing to existing CLI manager

2. **Test Communication Bridge**
   - Test Python subprocess spawning from TypeScript
   - Test TypeScript subprocess communication
   - Verify command execution flow via stdin/stdout

### Phase 3: Advanced Features
1. **Implement AutoComplete System**
   - Connect to Python command discovery
   - Add fuzzy matching for command suggestions
   - Integrate with conversation interface

2. **Add Progress Visualization**
   - JSON message progress updates from Python subprocess
   - Real-time progress bars and status
   - Workflow state visualization

### Phase 4: Polish & Integration
1. **Error Handling & Recovery**
   - Comprehensive error display
   - Connection retry logic
   - Graceful degradation patterns

2. **Performance Optimization**
   - Command response caching
   - Efficient re-rendering
   - Memory usage optimization

---

## Display Pattern Integration

### Command Display Types
Based on the GATHERED_INFO documentation, implement these display patterns:

```typescript
// src/utils/display-helpers.ts
export const DisplayHandlers = {
  workflow_created: (data: any) => ({
    title: `✅ Workflow Created: ${data.workflow_id}`,
    content: data.description,
    actions: data.next_steps || []
  }),
  
  help_categories: (data: any) => ({
    title: '📚 Available Commands',
    content: data.categories.map((cat: any) => 
      `${cat.icon} ${cat.name}\n   ${cat.description}`
    ).join('\n\n')
  }),
  
  real_time_stats: (data: any) => ({
    title: '📊 System Statistics',
    content: `Active Workflows: ${data.active_workflows}\nCompleted: ${data.completed_workflows}`
  }),
  
  tool_results: (data: any) => ({
    title: `🔧 ${data.tool_name} Results`,
    content: data.formatted_output,
    metadata: data.execution_info
  }),
  
  error: (data: any) => ({
    title: '❌ Error',
    content: data.error_message,
    suggestions: data.suggested_actions || []
  })
};
```

### CLI Command Integration
All 30+ CLI commands from the Python backend are documented with display patterns:

- `/goal` - Natural language workflow creation
- `/help` - Git-style command categories  
- `/continue` - Resume previous workflows
- `/logs` - System activity display
- `/stats` - Performance metrics
- `/tools` - Available tool management
- `/models` - AI model configuration
- And 20+ additional commands

Each command returns structured data that the TypeScript interface can render appropriately.

---

## Testing & Validation

### Integration Testing
```typescript
// tests/integration.test.ts
import { PythonBridge } from '../src/api/PythonBridge';

describe('Python Integration', () => {
  let bridge: PythonBridge;
  
  beforeAll(async () => {
    bridge = new PythonBridge();
    await bridge.initialize();
  });
  
  test('should execute goal command', async () => {
    const result = await bridge.executeCommand('goal', 'Create a simple website');
    expect(result.display_type).toBe('workflow_created');
    expect(result.workflow_id).toBeDefined();
  });
  
  test('should get autocomplete suggestions', async () => {
    const suggestions = await bridge.getAutoCompleteOptions('goa');
    expect(suggestions).toContain('goal');
  });
});
```

### Manual Testing Checklist
- [ ] TypeScript compilation without errors
- [ ] Python subprocess spawns correctly
- [ ] stdin/stdout communication works
- [ ] All CLI commands route correctly
- [ ] Visual protocol displays properly
- [ ] Progress updates work in real-time
- [ ] Error handling works gracefully
- [ ] Autocomplete suggests commands
- [ ] User sessions persist correctly

---

## Deployment & Distribution

### Build Process
```bash
# Development mode
npm run dev

# Production build  
npm run build
npm start

# Install globally
npm install -g .
mao  # Run from anywhere
```

### Integration with Existing MAO
The TypeScript terminal UI can be integrated into the existing MAO project:

1. **Standalone Mode**: Independent terminal app calling Python API
2. **Embedded Mode**: Include in MAO repo as `terminal-ui/` directory
3. **Package Mode**: Distribute as separate npm package

---

## Summary

This implementation guide consolidates insights from 100+ documentation files into a complete specification for building MAO's TypeScript terminal interface. The architecture leverages proven patterns from Claude Code while integrating seamlessly with the existing Python backend.

**Key Benefits:**
- Professional terminal interface using industry-standard tools
- Conversation-driven UX without complex menus
- Real-time progress visualization via subprocess communication
- Complete CLI command integration (30+ commands)
- Rich formatting with graceful fallback patterns
- Type-safe TypeScript implementation
- LOCAL-first architecture with no external web services

**Implementation Time Estimate:** 2-3 weeks for core functionality, 1-2 weeks for polish and testing.

The Python backend is complete and tested. This TypeScript layer provides the final piece for a professional, Claude Code-quality terminal interface while maintaining MAO's unique conversation-driven approach to AI workflow orchestration. 