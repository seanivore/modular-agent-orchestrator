# CLI Auto-Complete Implementation Guide

## Overview

This guide provides a comprehensive implementation plan for creating an auto-complete system for the MAO CLI commands, similar to Claude Code's interface where all commands show as you type and are scrollable.

## System Architecture

### 1. Command Discovery System

**Core Component:** Dynamic CLI Command Scanner
```javascript
class CLICommandScanner {
    constructor(configPath = './configs/cli/') {
        this.configPath = configPath;
        this.commands = new Map();
        this.lastScan = null;
        this.watchMode = false;
    }

    async scanCommands() {
        // Scan configs/cli/ directory for all command directories
        // Parse JSON configs for command metadata
        // Build command index with search optimization
    }

    getCommands(filter = '') {
        // Return filtered commands based on input
        // Support fuzzy matching and command categories
    }
}
```

### 2. Auto-Complete UI Component

**Frontend Component Structure:**
```typescript
interface CLICommand {
    name: string;
    command: string;
    terminal_flag: string;
    app_command: string;
    help: string;
    type: 'standalone' | 'needs_input' | 'needs_file_or_directory';
    category: string;
    examples?: string[];
}

interface AutoCompleteProps {
    value: string;
    onChange: (value: string) => void;
    onSelect: (command: CLICommand) => void;
    placeholder?: string;
}
```

## Implementation Strategy

### Phase 1: Backend Command Discovery

**1.1 Command Index Builder**
```python
# orchestrator/cli_autocomplete.py
class CLIAutoCompleteManager:
    def __init__(self):
        self.command_index = {}
        self.last_update = None
        
    def build_command_index(self):
        """Build searchable index from configs/cli/ directory"""
        commands = []
        cli_path = Path(__file__).parent.parent / "configs" / "cli"
        
        for command_dir in cli_path.iterdir():
            if command_dir.is_dir():
                json_file = command_dir / f"{command_dir.name}.json"
                if json_file.exists():
                    command_data = self._parse_command_config(json_file)
                    commands.append(command_data)
        
        return self._create_search_index(commands)
    
    def get_suggestions(self, input_text: str, limit: int = 10):
        """Get auto-complete suggestions for input text"""
        # Implement fuzzy matching and ranking
        pass
```

**1.2 Real-time Command Updates**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CommandConfigWatcher(FileSystemEventHandler):
    def __init__(self, autocomplete_manager):
        self.autocomplete_manager = autocomplete_manager
        
    def on_modified(self, event):
        if event.src_path.endswith('.json'):
            # Rebuild command index when configs change
            self.autocomplete_manager.build_command_index()
```

### Phase 2: Frontend Auto-Complete Interface

**2.1 Input Component with Dropdown**
```typescript
// components/CLIAutoComplete.tsx
import React, { useState, useEffect, useRef } from 'react';

const CLIAutoComplete: React.FC<AutoCompleteProps> = ({
    value,
    onChange,
    onSelect,
    placeholder = "Type / to see available commands..."
}) => {
    const [suggestions, setSuggestions] = useState<CLICommand[]>([]);
    const [isOpen, setIsOpen] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (value.startsWith('/')) {
            fetchSuggestions(value.slice(1));
            setIsOpen(true);
        } else {
            setIsOpen(false);
        }
    }, [value]);

    const fetchSuggestions = async (query: string) => {
        // API call to backend for command suggestions
        const response = await fetch(`/api/cli/suggestions?q=${query}`);
        const commands = await response.json();
        setSuggestions(commands);
    };

    const handleKeyDown = (e: KeyboardEvent) => {
        if (!isOpen) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                setSelectedIndex(prev => 
                    prev < suggestions.length - 1 ? prev + 1 : prev
                );
                break;
            case 'ArrowUp':
                e.preventDefault();
                setSelectedIndex(prev => prev > 0 ? prev - 1 : prev);
                break;
            case 'Enter':
                e.preventDefault();
                if (suggestions[selectedIndex]) {
                    selectCommand(suggestions[selectedIndex]);
                }
                break;
            case 'Escape':
                setIsOpen(false);
                break;
        }
    };

    return (
        <div className="relative">
            <input
                ref={inputRef}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2"
            />
            
            {isOpen && suggestions.length > 0 && (
                <CommandDropdown
                    commands={suggestions}
                    selectedIndex={selectedIndex}
                    onSelect={selectCommand}
                />
            )}
        </div>
    );
};
```

**2.2 Command Dropdown with Categories**
```typescript
// components/CommandDropdown.tsx
const CommandDropdown: React.FC<{
    commands: CLICommand[];
    selectedIndex: number;
    onSelect: (command: CLICommand) => void;
}> = ({ commands, selectedIndex, onSelect }) => {
    const groupedCommands = useMemo(() => {
        return commands.reduce((groups, command) => {
            const category = command.category || 'Other';
            if (!groups[category]) groups[category] = [];
            groups[category].push(command);
            return groups;
        }, {} as Record<string, CLICommand[]>);
    }, [commands]);

    return (
        <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto z-50">
            {Object.entries(groupedCommands).map(([category, categoryCommands]) => (
                <div key={category} className="border-b border-gray-100 last:border-b-0">
                    <div className="px-3 py-2 text-xs font-semibold text-gray-500 bg-gray-50 sticky top-0">
                        {category.toUpperCase()}
                    </div>
                    {categoryCommands.map((command, index) => {
                        const globalIndex = commands.indexOf(command);
                        return (
                            <CommandItem
                                key={command.name}
                                command={command}
                                isSelected={globalIndex === selectedIndex}
                                onClick={() => onSelect(command)}
                            />
                        );
                    })}
                </div>
            ))}
        </div>
    );
};
```

**2.3 Individual Command Item**
```typescript
// components/CommandItem.tsx
const CommandItem: React.FC<{
    command: CLICommand;
    isSelected: boolean;
    onClick: () => void;
}> = ({ command, isSelected, onClick }) => {
    return (
        <div
            className={`px-3 py-2 cursor-pointer transition-colors ${
                isSelected ? 'bg-blue-50 border-l-2 border-blue-500' : 'hover:bg-gray-50'
            }`}
            onClick={onClick}
        >
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <div className="flex items-center space-x-2">
                        <span className="font-mono text-sm font-medium text-blue-600">
                            {command.app_command}
                        </span>
                        <span className="text-xs text-gray-400">
                            {command.terminal_flag}
                        </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{command.help}</p>
                </div>
                <div className="ml-2 flex-shrink-0">
                    <TypeBadge type={command.type} />
                </div>
            </div>
        </div>
    );
};

const TypeBadge: React.FC<{ type: string }> = ({ type }) => {
    const styles = {
        'standalone': 'bg-green-100 text-green-800',
        'needs_input': 'bg-yellow-100 text-yellow-800',
        'needs_file_or_directory': 'bg-blue-100 text-blue-800'
    };

    return (
        <span className={`px-2 py-1 text-xs rounded-full ${styles[type as keyof typeof styles] || 'bg-gray-100 text-gray-800'}`}>
            {type.replace(/_/g, ' ')}
        </span>
    );
};
```

### Phase 3: Advanced Features

**3.1 Fuzzy Search Implementation**
```typescript
// utils/fuzzySearch.ts
export class FuzzySearchEngine {
    private commands: CLICommand[];

    constructor(commands: CLICommand[]) {
        this.commands = commands;
    }

    search(query: string, limit: number = 10): CLICommand[] {
        if (!query) return this.commands.slice(0, limit);

        const scored = this.commands
            .map(command => ({
                command,
                score: this.calculateScore(query, command)
            }))
            .filter(item => item.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, limit);

        return scored.map(item => item.command);
    }

    private calculateScore(query: string, command: CLICommand): number {
        const searchText = `${command.name} ${command.app_command} ${command.help}`.toLowerCase();
        const queryLower = query.toLowerCase();
        
        // Exact match gets highest score
        if (searchText.includes(queryLower)) {
            return 100;
        }

        // Fuzzy matching based on character presence and order
        let score = 0;
        let queryIndex = 0;
        
        for (let i = 0; i < searchText.length && queryIndex < queryLower.length; i++) {
            if (searchText[i] === queryLower[queryIndex]) {
                score += queryLower.length - queryIndex;
                queryIndex++;
            }
        }

        return queryIndex === queryLower.length ? score : 0;
    }
}
```

**3.2 Command Categories and Organization**
```typescript
// utils/commandCategories.ts
export const COMMAND_CATEGORIES = {
    'BASICS': ['help', 'tools', 'models', 'providers'],
    'WORKFLOW_CREATION': ['goal', 'setup', 'update', 'fix_it'],
    'WORKFLOW_MANAGEMENT': ['continue', 'review', 'workflows', 'stats'],
    'USER_SETTINGS': ['config', 'login', 'logout', 'user_id', 'workflow_id', 'variables'],
    'QUICK_SETTINGS': ['set_model', 'default_provider', 'output'],
    'SYSTEM_OPERATIONS': ['chat', 'doctor', 'dry_run', 'verbose', 'logs']
};

export function categorizeCommand(command: CLICommand): string {
    for (const [category, commands] of Object.entries(COMMAND_CATEGORIES)) {
        if (commands.includes(command.command)) {
            return category;
        }
    }
    return 'OTHER';
}
```

### Phase 4: Backend API Integration

**4.1 FastAPI Endpoint for Auto-Complete**
```python
# api/endpoints/cli.py
from fastapi import APIRouter, Query
from typing import List, Optional
from orchestrator.cli_autocomplete import CLIAutoCompleteManager

router = APIRouter(prefix="/api/cli", tags=["cli"])
autocomplete_manager = CLIAutoCompleteManager()

@router.get("/suggestions")
async def get_command_suggestions(
    q: str = Query("", description="Search query"),
    limit: int = Query(10, description="Maximum number of suggestions"),
    category: Optional[str] = Query(None, description="Filter by category")
) -> List[dict]:
    """Get auto-complete suggestions for CLI commands"""
    suggestions = autocomplete_manager.get_suggestions(q, limit, category)
    return [command.dict() for command in suggestions]

@router.get("/commands")
async def get_all_commands() -> List[dict]:
    """Get all available CLI commands"""
    commands = autocomplete_manager.get_all_commands()
    return [command.dict() for command in commands]

@router.post("/refresh")
async def refresh_command_index():
    """Refresh the command index from configs"""
    autocomplete_manager.build_command_index()
    return {"status": "refreshed"}
```

**4.2 WebSocket for Real-time Updates**
```python
# api/websockets/cli.py
from fastapi import WebSocket
import json

class CLIWebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_command_update(self, command_data: dict):
        """Broadcast command updates to all connected clients"""
        message = json.dumps({
            "type": "command_update",
            "data": command_data
        })
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                await self.disconnect(connection)
```

## UX/UI Considerations

### 1. Claude Code-style Interface
- **Dropdown Positioning**: Ensure dropdown doesn't overflow viewport
- **Keyboard Navigation**: Full arrow key navigation with Enter/Escape support
- **Visual Hierarchy**: Clear command names, help text, and type indicators
- **Scrollable Results**: Handle large command lists gracefully

### 2. Performance Optimization
- **Debounced Search**: Prevent excessive API calls during typing
- **Virtual Scrolling**: For large command lists
- **Caching**: Cache command data with intelligent invalidation
- **Lazy Loading**: Load command details on demand

### 3. Accessibility Features
- **Screen Reader Support**: Proper ARIA labels and announcements
- **High Contrast Mode**: Support for accessibility themes
- **Keyboard Only Navigation**: Full functionality without mouse
- **Focus Management**: Clear focus indicators

## Implementation Timeline

### Week 1: Backend Foundation
- [ ] Implement CLIAutoCompleteManager
- [ ] Create command indexing system
- [ ] Build fuzzy search engine
- [ ] Set up file system watching

### Week 2: Basic Frontend
- [ ] Create auto-complete input component
- [ ] Implement dropdown with keyboard navigation
- [ ] Add command categorization
- [ ] Basic styling and UX

### Week 3: Advanced Features
- [ ] Add fuzzy search integration
- [ ] Implement command type badges
- [ ] Add help text and examples
- [ ] Real-time command updates

### Week 4: Integration & Polish
- [ ] API integration and testing
- [ ] Performance optimization
- [ ] Accessibility improvements
- [ ] Documentation and deployment

## File Structure

```
src/
├── components/
│   ├── CLIAutoComplete.tsx
│   ├── CommandDropdown.tsx
│   └── CommandItem.tsx
├── utils/
│   ├── fuzzySearch.ts
│   └── commandCategories.ts
├── api/
│   ├── endpoints/
│   │   └── cli.py
│   └── websockets/
│       └── cli.py
└── orchestrator/
    └── cli_autocomplete.py
```

This implementation provides a comprehensive auto-complete system that matches the quality and usability of Claude Code's interface while being specifically tailored to the MAO CLI command structure.