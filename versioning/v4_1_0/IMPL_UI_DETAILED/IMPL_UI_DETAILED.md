# Detailed UI Implementation Plans
*Component-by-component TypeScript/React/Ink implementation for all MAO tools and interfaces*

---

## 🎯 **IMPLEMENTATION OVERVIEW**

This document provides granular implementation details for every UI component in the MAO ecosystem. Each tool gets a complete UI implementation plan with TypeScript code, React/Ink components, and integration patterns.

**Core UI Stack:**
- **TypeScript 5.3+** with strict type checking
- **React 19.1+** with hooks and modern patterns  
- **Ink 6.1+** for terminal-native rendering
- **Node.js 20+** with ES modules

---

## 🏗️ **DISCOVERED TOOL ECOSYSTEM**

Based on filesystem analysis, MAO has 11 core tools requiring UI implementation:

```
tools/
├── brave_search/        # Brave API web search
├── code_execution/      # Code execution environment  
├── dalle_generate/      # DALL-E image generation
├── file_operations/     # File system operations
├── files_api/          # File API management
├── graphic_design/     # Design automation
├── mcp_connector/      # MCP protocol integration
├── perplexity_search/  # Perplexity API search
├── text_editor/        # Text editing operations
├── think/              # AI reasoning display
└── web_search/         # Native web search
```

Each tool follows the **4-file pattern**: `tool.py`, `button_tool.py`, `ui_tool.py`, `tool_config.json`

---

## 📱 **CORE UI COMPONENT ARCHITECTURE**

### **Base Component Structure**

```typescript
// interfaces/mao/source/components/base/BaseToolInterface.tsx
import React, {useState, useCallback, useEffect} from 'react';
import {Box, Text, useInput} from 'ink';
import {PythonBridge} from '../../api/PythonBridge.js';

export interface ToolInterfaceProps {
    toolName: string;
    operation: string;
    params: Record<string, any>;
    onResult: (result: any) => void;
    onError: (error: string) => void;
}

export interface ToolState {
    isLoading: boolean;
    progress: number;
    currentStep: string;
    result: any;
    error: string | null;
}

export abstract class BaseToolInterface extends React.Component<ToolInterfaceProps, ToolState> {
    protected pythonBridge: PythonBridge;
    
    constructor(props: ToolInterfaceProps) {
        super(props);
        this.pythonBridge = new PythonBridge();
        this.state = {
            isLoading: false,
            progress: 0,
            currentStep: '',
            result: null,
            error: null
        };
    }
    
    abstract renderContent(): React.ReactNode;
    abstract validateParams(): boolean;
    
    protected async executeOperation(): Promise<void> {
        if (!this.validateParams()) {
            this.setState({error: 'Invalid parameters'});
            return;
        }
        
        this.setState({isLoading: true, error: null});
        
        try {
            const result = await this.pythonBridge.executeTool(
                this.props.toolName,
                this.props.operation,
                this.props.params
            );
            
            this.setState({
                isLoading: false,
                result,
                currentStep: 'Complete'
            });
            
            this.props.onResult(result);
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.setState({
                isLoading: false,
                error: errorMessage
            });
            
            this.props.onError(errorMessage);
        }
    }
    
    render(): React.ReactNode {
        const {isLoading, progress, currentStep, error} = this.state;
        
        return (
            <Box flexDirection="column" width="100%">
                {/* Tool Header */}
                <Box borderStyle="round" borderColor="blue" paddingX={1}>
                    <Text color="cyan">{this.props.toolName.toUpperCase()}</Text>
                    <Text color="gray"> | </Text>
                    <Text color="white">{this.props.operation}</Text>
                </Box>
                
                {/* Loading State */}
                {isLoading && (
                    <Box flexDirection="column" marginY={1}>
                        <Text color="yellow">⏳ {currentStep || 'Processing...'}</Text>
                        <Box width={40}>
                            <Text color="blue">
                                {'█'.repeat(Math.floor(progress * 40 / 100))}
                                {'░'.repeat(40 - Math.floor(progress * 40 / 100))}
                            </Text>
                            <Text color="white"> {progress.toFixed(1)}%</Text>
                        </Box>
                    </Box>
                )}
                
                {/* Error State */}
                {error && (
                    <Box borderStyle="round" borderColor="red" paddingX={1} marginY={1}>
                        <Text color="red">❌ Error: {error}</Text>
                    </Box>
                )}
                
                {/* Tool-Specific Content */}
                <Box flexDirection="column">
                    {this.renderContent()}
                </Box>
            </Box>
        );
    }
}
```

---

## 🔍 **TOOL 1: WEB SEARCH UI IMPLEMENTATION**

### **Web Search Interface Component**

```typescript
// interfaces/mao/source/components/tools/WebSearchInterface.tsx
import React, {useState, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {BaseToolInterface, ToolInterfaceProps} from '../base/BaseToolInterface.js';

interface WebSearchState extends ToolState {
    query: string;
    maxResults: number;
    searchMode: 'basic' | 'filtered' | 'content';
    filters: {
        domain?: string;
        dateRange?: string;
        contentType?: string;
    };
    results: SearchResult[];
}

interface SearchResult {
    title: string;
    url: string;
    snippet: string;
    source: string;
    timestamp: string;
}

export class WebSearchInterface extends BaseToolInterface<ToolInterfaceProps, WebSearchState> {
    constructor(props: ToolInterfaceProps) {
        super(props);
        this.state = {
            ...this.state,
            query: props.params.query || '',
            maxResults: props.params.max_results || 10,
            searchMode: props.params.search_mode || 'basic',
            filters: props.params.filters || {},
            results: []
        };
    }
    
    validateParams(): boolean {
        return this.state.query.trim().length > 0;
    }
    
    renderContent(): React.ReactNode {
        const {query, maxResults, searchMode, filters, results, isLoading} = this.state;
        
        return (
            <Box flexDirection="column">
                {/* Search Configuration */}
                <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                    <Text color="cyan">🔍 Search Configuration</Text>
                    <Text color="white">Query: </Text>
                    <Text color="green">{query}</Text>
                    <Text color="white">Mode: </Text>
                    <Text color="yellow">{searchMode}</Text>
                    <Text color="white">Max Results: </Text>
                    <Text color="magenta">{maxResults}</Text>
                    
                    {filters.domain && (
                        <>
                            <Text color="white">Domain Filter: </Text>
                            <Text color="blue">{filters.domain}</Text>
                        </>
                    )}
                    
                    {filters.dateRange && (
                        <>
                            <Text color="white">Date Range: </Text>
                            <Text color="blue">{filters.dateRange}</Text>
                        </>
                    )}
                </Box>
                
                {/* Search Results */}
                {results.length > 0 && (
                    <Box flexDirection="column">
                        <Text color="cyan">📋 Search Results ({results.length})</Text>
                        {results.map((result, index) => (
                            <Box key={index} flexDirection="column" borderStyle="single" paddingX={1} marginY={1}>
                                <Box>
                                    <Text color="white">{index + 1}. </Text>
                                    <Text color="green" bold>{result.title}</Text>
                                </Box>
                                <Text color="blue">{result.url}</Text>
                                <Text color="gray">{result.snippet}</Text>
                                <Box marginTop={1}>
                                    <Text color="yellow">Source: {result.source}</Text>
                                    <Text color="gray"> | {result.timestamp}</Text>
                                </Box>
                            </Box>
                        ))}
                    </Box>
                )}
                
                {/* Interactive Controls */}
                {!isLoading && (
                    <Box flexDirection="row" marginTop={1}>
                        <Text color="white">Press </Text>
                        <Text color="cyan">ENTER</Text>
                        <Text color="white"> to search, </Text>
                        <Text color="yellow">R</Text>
                        <Text color="white"> to refine, </Text>
                        <Text color="red">Q</Text>
                        <Text color="white"> to quit</Text>
                    </Box>
                )}
            </Box>
        );
    }
    
    componentDidMount() {
        // Auto-execute if query is provided
        if (this.state.query) {
            this.executeOperation();
        }
    }
    
    protected async executeOperation(): Promise<void> {
        this.setState({
            isLoading: true,
            currentStep: 'Initiating web search...',
            progress: 10
        });
        
        try {
            // Step 1: Validate query
            this.setState({
                currentStep: 'Validating search query...',
                progress: 25
            });
            
            const validationResult = await this.pythonBridge.executeTool(
                'web_search',
                'validate_search_query',
                {query: this.state.query}
            );
            
            if (!validationResult.success) {
                throw new Error(validationResult.error);
            }
            
            // Step 2: Execute search
            this.setState({
                currentStep: 'Performing web search...',
                progress: 50
            });
            
            const operation = this.getSearchOperation();
            const searchParams = this.buildSearchParams();
            
            const result = await this.pythonBridge.executeTool(
                'web_search',
                operation,
                searchParams
            );
            
            // Step 3: Process results
            this.setState({
                currentStep: 'Processing search results...',
                progress: 75
            });
            
            if (result.success) {
                this.setState({
                    results: result.results || [],
                    isLoading: false,
                    progress: 100,
                    currentStep: 'Search complete'
                });
                
                this.props.onResult(result);
            } else {
                throw new Error(result.error || 'Search failed');
            }
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown search error';
            this.setState({
                isLoading: false,
                error: errorMessage,
                progress: 0
            });
            
            this.props.onError(errorMessage);
        }
    }
    
    private getSearchOperation(): string {
        switch (this.state.searchMode) {
            case 'filtered':
                return 'perform_filtered_search';
            case 'content':
                return 'perform_content_search';
            default:
                return 'perform_web_search';
        }
    }
    
    private buildSearchParams(): Record<string, any> {
        const params: Record<string, any> = {
            query: this.state.query,
            max_results: this.state.maxResults
        };
        
        if (this.state.filters.domain) {
            params.domain = this.state.filters.domain;
        }
        
        if (this.state.filters.dateRange) {
            params.date_range = this.state.filters.dateRange;
        }
        
        if (this.state.filters.contentType) {
            params.content_type = this.state.filters.contentType;
        }
        
        return params;
    }
}

// Functional component wrapper for easier integration
export default function WebSearchUI(props: {
    query: string;
    maxResults?: number;
    searchMode?: 'basic' | 'filtered' | 'content';
    filters?: Record<string, any>;
    onResult: (result: any) => void;
    onError: (error: string) => void;
}) {
    return (
        <WebSearchInterface
            toolName="web_search"
            operation="perform_web_search"
            params={{
                query: props.query,
                max_results: props.maxResults,
                search_mode: props.searchMode,
                filters: props.filters || {}
            }}
            onResult={props.onResult}
            onError={props.onError}
        />
    );
}
```

---

## 💻 **TOOL 2: CODE EXECUTION UI IMPLEMENTATION**

### **Code Execution Interface Component**

```typescript
// interfaces/mao/source/components/tools/CodeExecutionInterface.tsx
import React, {useState, useCallback, useRef, useEffect} from 'react';
import {Box, Text, useInput} from 'ink';
import {BaseToolInterface, ToolInterfaceProps} from '../base/BaseToolInterface.js';

interface CodeExecutionState extends ToolState {
    code: string;
    language: string;
    executionMode: 'script' | 'interactive' | 'file';
    output: ExecutionOutput[];
    inputBuffer: string;
    isInteractive: boolean;
    environment: {
        variables: Record<string, any>;
        packages: string[];
        workingDirectory: string;
    };
}

interface ExecutionOutput {
    type: 'stdout' | 'stderr' | 'return' | 'error';
    content: string;
    timestamp: number;
    lineNumber?: number;
}

export class CodeExecutionInterface extends BaseToolInterface<ToolInterfaceProps, CodeExecutionState> {
    private outputRef = useRef<ExecutionOutput[]>([]);
    
    constructor(props: ToolInterfaceProps) {
        super(props);
        this.state = {
            ...this.state,
            code: props.params.code || '',
            language: props.params.language || 'python',
            executionMode: props.params.execution_mode || 'script',
            output: [],
            inputBuffer: '',
            isInteractive: props.params.execution_mode === 'interactive',
            environment: props.params.environment || {
                variables: {},
                packages: [],
                workingDirectory: process.cwd()
            }
        };
    }
    
    validateParams(): boolean {
        return this.state.code.trim().length > 0 && this.state.language.length > 0;
    }
    
    renderContent(): React.ReactNode {
        const {code, language, executionMode, output, isInteractive, environment} = this.state;
        
        return (
            <Box flexDirection="column">
                {/* Code Configuration */}
                <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                    <Text color="cyan">⚡ Code Execution</Text>
                    <Box>
                        <Text color="white">Language: </Text>
                        <Text color="green">{language}</Text>
                        <Text color="white"> | Mode: </Text>
                        <Text color="yellow">{executionMode}</Text>
                        {isInteractive && <Text color="magenta"> [INTERACTIVE]</Text>}
                    </Box>
                    <Box>
                        <Text color="white">Working Directory: </Text>
                        <Text color="blue">{environment.workingDirectory}</Text>
                    </Box>
                </Box>
                
                {/* Code Display */}
                <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                    <Text color="cyan">📝 Code</Text>
                    <Box flexDirection="column">
                        {code.split('\n').map((line, index) => (
                            <Box key={index}>
                                <Text color="gray">{String(index + 1).padStart(3, ' ')}: </Text>
                                <Text color="white">{line}</Text>
                            </Box>
                        ))}
                    </Box>
                </Box>
                
                {/* Environment Variables */}
                {Object.keys(environment.variables).length > 0 && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">🔧 Environment Variables</Text>
                        {Object.entries(environment.variables).map(([key, value]) => (
                            <Box key={key}>
                                <Text color="yellow">{key}</Text>
                                <Text color="white">: </Text>
                                <Text color="green">{String(value)}</Text>
                            </Box>
                        ))}
                    </Box>
                )}
                
                {/* Execution Output */}
                {output.length > 0 && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">📤 Output</Text>
                        <Box flexDirection="column" maxHeight={20} overflowY="scroll">
                            {output.map((outputLine, index) => (
                                <Box key={index}>
                                    <Text color={this.getOutputColor(outputLine.type)}>
                                        {this.getOutputPrefix(outputLine.type)}
                                    </Text>
                                    <Text color="white">{outputLine.content}</Text>
                                </Box>
                            ))}
                        </Box>
                    </Box>
                )}
                
                {/* Interactive Input */}
                {isInteractive && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1}>
                        <Text color="cyan">⌨️  Interactive Input</Text>
                        <Box>
                            <Text color="yellow">&gt;&gt;&gt; </Text>
                            <Text color="white">{this.state.inputBuffer}</Text>
                        </Box>
                        <Text color="gray">Press ENTER to execute, CTRL+C to exit interactive mode</Text>
                    </Box>
                )}
                
                {/* Controls */}
                {!this.state.isLoading && (
                    <Box flexDirection="row" marginTop={1}>
                        <Text color="white">Press </Text>
                        <Text color="cyan">ENTER</Text>
                        <Text color="white"> to execute, </Text>
                        <Text color="yellow">I</Text>
                        <Text color="white"> for interactive, </Text>
                        <Text color="red">Q</Text>
                        <Text color="white"> to quit</Text>
                    </Box>
                )}
            </Box>
        );
    }
    
    private getOutputColor(type: ExecutionOutput['type']): string {
        switch (type) {
            case 'stdout': return 'green';
            case 'return': return 'cyan';
            case 'stderr': return 'yellow';
            case 'error': return 'red';
            default: return 'white';
        }
    }
    
    private getOutputPrefix(type: ExecutionOutput['type']): string {
        switch (type) {
            case 'stdout': return '[OUT] ';
            case 'return': return '[RET] ';
            case 'stderr': return '[ERR] ';
            case 'error': return '[ERR] ';
            default: return '[LOG] ';
        }
    }
    
    protected async executeOperation(): Promise<void> {
        this.setState({
            isLoading: true,
            currentStep: 'Preparing execution environment...',
            progress: 10
        });
        
        try {
            // Step 1: Setup environment
            this.setState({
                currentStep: 'Setting up execution environment...',
                progress: 25
            });
            
            const envResult = await this.pythonBridge.executeTool(
                'code_execution',
                'setup_environment',
                {
                    language: this.state.language,
                    environment: this.state.environment
                }
            );
            
            if (!envResult.success) {
                throw new Error(envResult.error);
            }
            
            // Step 2: Execute code
            this.setState({
                currentStep: 'Executing code...',
                progress: 50
            });
            
            const executionResult = await this.pythonBridge.executeTool(
                'code_execution',
                'execute_code',
                {
                    code: this.state.code,
                    language: this.state.language,
                    execution_mode: this.state.executionMode,
                    environment: this.state.environment
                }
            );
            
            // Step 3: Process output
            this.setState({
                currentStep: 'Processing execution results...',
                progress: 75
            });
            
            if (executionResult.success) {
                const newOutput: ExecutionOutput[] = [];
                
                // Add stdout
                if (executionResult.stdout) {
                    executionResult.stdout.split('\n').forEach((line: string) => {
                        if (line.trim()) {
                            newOutput.push({
                                type: 'stdout',
                                content: line,
                                timestamp: Date.now()
                            });
                        }
                    });
                }
                
                // Add stderr
                if (executionResult.stderr) {
                    executionResult.stderr.split('\n').forEach((line: string) => {
                        if (line.trim()) {
                            newOutput.push({
                                type: 'stderr',
                                content: line,
                                timestamp: Date.now()
                            });
                        }
                    });
                }
                
                // Add return value
                if (executionResult.return_value !== undefined) {
                    newOutput.push({
                        type: 'return',
                        content: String(executionResult.return_value),
                        timestamp: Date.now()
                    });
                }
                
                this.setState({
                    output: [...this.state.output, ...newOutput],
                    isLoading: false,
                    progress: 100,
                    currentStep: 'Execution complete'
                });
                
                this.props.onResult(executionResult);
                
                // Switch to interactive mode if needed
                if (this.state.executionMode === 'interactive') {
                    this.setState({isInteractive: true});
                }
                
            } else {
                throw new Error(executionResult.error || 'Code execution failed');
            }
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown execution error';
            
            // Add error to output
            const errorOutput: ExecutionOutput = {
                type: 'error',
                content: errorMessage,
                timestamp: Date.now()
            };
            
            this.setState({
                output: [...this.state.output, errorOutput],
                isLoading: false,
                error: errorMessage,
                progress: 0
            });
            
            this.props.onError(errorMessage);
        }
    }
    
    // Handle interactive input
    useInput(useCallback((inputChar, key) => {
        if (!this.state.isInteractive) return;
        
        if (key.return && this.state.inputBuffer.trim()) {
            this.executeInteractiveCommand(this.state.inputBuffer.trim());
            this.setState({inputBuffer: ''});
        } else if (key.backspace || key.delete) {
            this.setState(prev => ({
                inputBuffer: prev.inputBuffer.slice(0, -1)
            }));
        } else if (key.ctrl && inputChar === 'c') {
            this.setState({isInteractive: false});
        } else if (inputChar && !key.ctrl && !key.meta && !key.return) {
            this.setState(prev => ({
                inputBuffer: prev.inputBuffer + inputChar
            }));
        }
    }, [this.state.isInteractive, this.state.inputBuffer]));
    
    private async executeInteractiveCommand(command: string): Promise<void> {
        const inputOutput: ExecutionOutput = {
            type: 'stdout',
            content: `>>> ${command}`,
            timestamp: Date.now()
        };
        
        this.setState(prev => ({
            output: [...prev.output, inputOutput]
        }));
        
        try {
            const result = await this.pythonBridge.executeTool(
                'code_execution',
                'execute_interactive',
                {
                    command,
                    language: this.state.language,
                    environment: this.state.environment
                }
            );
            
            if (result.success && result.output) {
                const responseOutput: ExecutionOutput = {
                    type: 'return',
                    content: result.output,
                    timestamp: Date.now()
                };
                
                this.setState(prev => ({
                    output: [...prev.output, responseOutput]
                }));
            }
            
        } catch (error) {
            const errorOutput: ExecutionOutput = {
                type: 'error',
                content: error instanceof Error ? error.message : 'Interactive execution error',
                timestamp: Date.now()
            };
            
            this.setState(prev => ({
                output: [...prev.output, errorOutput]
            }));
        }
    }
}

// Functional component wrapper
export default function CodeExecutionUI(props: {
    code: string;
    language?: string;
    executionMode?: 'script' | 'interactive' | 'file';
    environment?: Record<string, any>;
    onResult: (result: any) => void;
    onError: (error: string) => void;
}) {
    return (
        <CodeExecutionInterface
            toolName="code_execution"
            operation="execute_code"
            params={{
                code: props.code,
                language: props.language || 'python',
                execution_mode: props.executionMode || 'script',
                environment: props.environment || {}
            }}
            onResult={props.onResult}
            onError={props.onError}
        />
    );
}
```

---

## 🎨 **TOOL 3: DALLE GENERATE UI IMPLEMENTATION**

### **DALL-E Image Generation Interface**

```typescript
// interfaces/mao/source/components/tools/DalleGenerateInterface.tsx
import React, {useState, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {BaseToolInterface, ToolInterfaceProps} from '../base/BaseToolInterface.js';

interface DalleGenerateState extends ToolState {
    prompt: string;
    size: '1024x1024' | '1792x1024' | '1024x1792';
    quality: 'standard' | 'hd';
    style: 'vivid' | 'natural';
    numberOfImages: number;
    generatedImages: GeneratedImage[];
    promptRevisions: string[];
}

interface GeneratedImage {
    url: string;
    revisedPrompt: string;
    timestamp: number;
    size: string;
    quality: string;
    style: string;
}

export class DalleGenerateInterface extends BaseToolInterface<ToolInterfaceProps, DalleGenerateState> {
    constructor(props: ToolInterfaceProps) {
        super(props);
        this.state = {
            ...this.state,
            prompt: props.params.prompt || '',
            size: props.params.size || '1024x1024',
            quality: props.params.quality || 'standard',
            style: props.params.style || 'vivid',
            numberOfImages: props.params.n || 1,
            generatedImages: [],
            promptRevisions: []
        };
    }
    
    validateParams(): boolean {
        return this.state.prompt.trim().length > 0 && this.state.numberOfImages >= 1 && this.state.numberOfImages <= 4;
    }
    
    renderContent(): React.ReactNode {
        const {prompt, size, quality, style, numberOfImages, generatedImages, promptRevisions} = this.state;
        
        return (
            <Box flexDirection="column">
                {/* Generation Configuration */}
                <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                    <Text color="cyan">🎨 DALL-E Image Generation</Text>
                    <Box flexDirection="column">
                        <Box>
                            <Text color="white">Prompt: </Text>
                            <Text color="green">{prompt}</Text>
                        </Box>
                        <Box marginTop={1}>
                            <Text color="white">Size: </Text>
                            <Text color="yellow">{size}</Text>
                            <Text color="white"> | Quality: </Text>
                            <Text color="magenta">{quality}</Text>
                            <Text color="white"> | Style: </Text>
                            <Text color="blue">{style}</Text>
                        </Box>
                        <Box>
                            <Text color="white">Number of Images: </Text>
                            <Text color="cyan">{numberOfImages}</Text>
                        </Box>
                    </Box>
                </Box>
                
                {/* Prompt Revisions */}
                {promptRevisions.length > 0 && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">📝 Prompt Revisions by DALL-E</Text>
                        {promptRevisions.map((revision, index) => (
                            <Box key={index} marginY={1}>
                                <Text color="yellow">{index + 1}. </Text>
                                <Text color="white">{revision}</Text>
                            </Box>
                        ))}
                    </Box>
                )}
                
                {/* Generated Images */}
                {generatedImages.length > 0 && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">🖼️  Generated Images ({generatedImages.length})</Text>
                        {generatedImages.map((image, index) => (
                            <Box key={index} flexDirection="column" marginY={1}>
                                <Box>
                                    <Text color="white">{index + 1}. </Text>
                                    <Text color="green" bold>Image Generated</Text>
                                </Box>
                                <Box marginLeft={3}>
                                    <Text color="blue">URL: {image.url}</Text>
                                </Box>
                                <Box marginLeft={3}>
                                    <Text color="yellow">Size: {image.size}</Text>
                                    <Text color="white"> | Quality: </Text>
                                    <Text color="magenta">{image.quality}</Text>
                                    <Text color="white"> | Style: </Text>
                                    <Text color="blue">{image.style}</Text>
                                </Box>
                                {image.revisedPrompt !== prompt && (
                                    <Box marginLeft={3}>
                                        <Text color="gray">Revised Prompt: {image.revisedPrompt}</Text>
                                    </Box>
                                )}
                                <Box marginLeft={3}>
                                    <Text color="gray">Generated: {new Date(image.timestamp).toLocaleString()}</Text>
                                </Box>
                            </Box>
                        ))}
                    </Box>
                )}
                
                {/* Image Preview Placeholder */}
                {generatedImages.length > 0 && (
                    <Box flexDirection="column" borderStyle="double" paddingX={1} marginBottom={1}>
                        <Text color="cyan">🖥️  Image Preview</Text>
                        <Text color="gray">Terminal image preview would appear here</Text>
                        <Text color="white">Use image viewer to open: </Text>
                        <Text color="green">`open {generatedImages[0]?.url}`</Text>
                    </Box>
                )}
                
                {/* Controls */}
                {!this.state.isLoading && (
                    <Box flexDirection="row" marginTop={1}>
                        <Text color="white">Press </Text>
                        <Text color="cyan">ENTER</Text>
                        <Text color="white"> to generate, </Text>
                        <Text color="yellow">R</Text>
                        <Text color="white"> to regenerate, </Text>
                        <Text color="red">Q</Text>
                        <Text color="white"> to quit</Text>
                    </Box>
                )}
            </Box>
        );
    }
    
    protected async executeOperation(): Promise<void> {
        this.setState({
            isLoading: true,
            currentStep: 'Preparing image generation...',
            progress: 10
        });
        
        try {
            // Step 1: Validate prompt
            this.setState({
                currentStep: 'Validating prompt...',
                progress: 20
            });
            
            const validationResult = await this.pythonBridge.executeTool(
                'dalle_generate',
                'validate_prompt',
                {prompt: this.state.prompt}
            );
            
            if (!validationResult.success) {
                throw new Error(validationResult.error);
            }
            
            // Step 2: Generate images
            this.setState({
                currentStep: 'Generating images with DALL-E...',
                progress: 40
            });
            
            const generationParams = {
                prompt: this.state.prompt,
                size: this.state.size,
                quality: this.state.quality,
                style: this.state.style,
                n: this.state.numberOfImages
            };
            
            const result = await this.pythonBridge.executeTool(
                'dalle_generate',
                'generate_image',
                generationParams
            );
            
            // Step 3: Process results
            this.setState({
                currentStep: 'Processing generated images...',
                progress: 80
            });
            
            if (result.success) {
                const newImages: GeneratedImage[] = result.images.map((imageData: any) => ({
                    url: imageData.url,
                    revisedPrompt: imageData.revised_prompt || this.state.prompt,
                    timestamp: Date.now(),
                    size: this.state.size,
                    quality: this.state.quality,
                    style: this.state.style
                }));
                
                // Extract unique prompt revisions
                const revisions = newImages
                    .map(img => img.revisedPrompt)
                    .filter((revision, index, arr) => 
                        revision !== this.state.prompt && arr.indexOf(revision) === index
                    );
                
                this.setState({
                    generatedImages: [...this.state.generatedImages, ...newImages],
                    promptRevisions: [...this.state.promptRevisions, ...revisions],
                    isLoading: false,
                    progress: 100,
                    currentStep: 'Image generation complete'
                });
                
                this.props.onResult(result);
                
            } else {
                throw new Error(result.error || 'Image generation failed');
            }
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown generation error';
            this.setState({
                isLoading: false,
                error: errorMessage,
                progress: 0
            });
            
            this.props.onError(errorMessage);
        }
    }
    
    // Handle regeneration
    private async regenerateImages(): Promise<void> {
        this.setState({
            generatedImages: [],
            promptRevisions: []
        });
        
        await this.executeOperation();
    }
    
    useInput(useCallback((inputChar, key) => {
        if (this.state.isLoading) return;
        
        if (key.return) {
            this.executeOperation();
        } else if (inputChar === 'r' || inputChar === 'R') {
            this.regenerateImages();
        } else if (inputChar === 'q' || inputChar === 'Q') {
            // Handle quit
        }
    }, [this.state.isLoading]));
}

// Functional component wrapper
export default function DalleGenerateUI(props: {
    prompt: string;
    size?: '1024x1024' | '1792x1024' | '1024x1792';
    quality?: 'standard' | 'hd';
    style?: 'vivid' | 'natural';
    numberOfImages?: number;
    onResult: (result: any) => void;
    onError: (error: string) => void;
}) {
    return (
        <DalleGenerateInterface
            toolName="dalle_generate"
            operation="generate_image"
            params={{
                prompt: props.prompt,
                size: props.size || '1024x1024',
                quality: props.quality || 'standard',
                style: props.style || 'vivid',
                n: props.numberOfImages || 1
            }}
            onResult={props.onResult}
            onError={props.onError}
        />
    );
}
```

---

## 🧠 **TOOL 4: THINK UI IMPLEMENTATION**

### **AI Thinking Process Visualizer**

```typescript
// interfaces/mao/source/components/tools/ThinkInterface.tsx
import React, {useState, useCallback, useEffect} from 'react';
import {Box, Text, useInput} from 'ink';
import {BaseToolInterface, ToolInterfaceProps} from '../base/BaseToolInterface.js';

interface ThinkState extends ToolState {
    problem: string;
    thinkingMode: 'sequential' | 'creative' | 'analytical' | 'problem_solving';
    thoughts: ThoughtStep[];
    currentThought: number;
    isThinkingComplete: boolean;
    conclusion: string;
    confidence: number;
}

interface ThoughtStep {
    id: number;
    type: 'analysis' | 'hypothesis' | 'evaluation' | 'synthesis' | 'conclusion';
    content: string;
    timestamp: number;
    confidence: number;
    connections: number[];  // IDs of related thoughts
}

export class ThinkInterface extends BaseToolInterface<ToolInterfaceProps, ThinkState> {
    private thinkingInterval: NodeJS.Timeout | null = null;
    
    constructor(props: ToolInterfaceProps) {
        super(props);
        this.state = {
            ...this.state,
            problem: props.params.problem || props.params.query || '',
            thinkingMode: props.params.thinking_mode || 'sequential',
            thoughts: [],
            currentThought: 0,
            isThinkingComplete: false,
            conclusion: '',
            confidence: 0
        };
    }
    
    validateParams(): boolean {
        return this.state.problem.trim().length > 0;
    }
    
    renderContent(): React.ReactNode {
        const {problem, thinkingMode, thoughts, currentThought, isThinkingComplete, conclusion, confidence} = this.state;
        
        return (
            <Box flexDirection="column">
                {/* Problem Statement */}
                <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                    <Text color="cyan">🧠 AI Thinking Process</Text>
                    <Box>
                        <Text color="white">Problem: </Text>
                        <Text color="green">{problem}</Text>
                    </Box>
                    <Box>
                        <Text color="white">Mode: </Text>
                        <Text color="yellow">{thinkingMode}</Text>
                        {isThinkingComplete && (
                            <>
                                <Text color="white"> | Confidence: </Text>
                                <Text color={confidence > 0.8 ? 'green' : confidence > 0.6 ? 'yellow' : 'red'}>
                                    {(confidence * 100).toFixed(1)}%
                                </Text>
                            </>
                        )}
                    </Box>
                </Box>
                
                {/* Thinking Progress */}
                {thoughts.length > 0 && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">💭 Thought Process</Text>
                        <Box flexDirection="column">
                            {thoughts.map((thought, index) => (
                                <Box key={thought.id} flexDirection="column" marginY={1}>
                                    <Box>
                                        <Text color={index === currentThought ? 'yellow' : 'white'}>
                                            {index + 1}. 
                                        </Text>
                                        <Text color={this.getThoughtTypeColor(thought.type)} bold>
                                            [{thought.type.toUpperCase()}]
                                        </Text>
                                        {index === currentThought && !isThinkingComplete && (
                                            <Text color="yellow"> ← Current</Text>
                                        )}
                                    </Box>
                                    <Box marginLeft={3}>
                                        <Text color="white">{thought.content}</Text>
                                    </Box>
                                    <Box marginLeft={3}>
                                        <Text color="gray">
                                            Confidence: {(thought.confidence * 100).toFixed(1)}%
                                        </Text>
                                        {thought.connections.length > 0 && (
                                            <>
                                                <Text color="gray"> | Connected to: </Text>
                                                <Text color="blue">
                                                    {thought.connections.map(id => `#${id}`).join(', ')}
                                                </Text>
                                            </>
                                        )}
                                    </Box>
                                </Box>
                            ))}
                        </Box>
                    </Box>
                )}
                
                {/* Live Thinking Indicator */}
                {this.state.isLoading && !isThinkingComplete && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="yellow">⚡ Active Thinking...</Text>
                        <Box>
                            <Text color="white">Current Step: </Text>
                            <Text color="cyan">{this.state.currentStep}</Text>
                        </Box>
                        <Box marginTop={1}>
                            {this.renderThinkingAnimation()}
                        </Box>
                    </Box>
                )}
                
                {/* Conclusion */}
                {isThinkingComplete && conclusion && (
                    <Box flexDirection="column" borderStyle="double" paddingX={1} marginBottom={1}>
                        <Text color="green" bold>✅ Conclusion</Text>
                        <Text color="white">{conclusion}</Text>
                        <Box marginTop={1}>
                            <Text color="white">Overall Confidence: </Text>
                            <Text color={confidence > 0.8 ? 'green' : confidence > 0.6 ? 'yellow' : 'red'}>
                                {(confidence * 100).toFixed(1)}%
                            </Text>
                        </Box>
                    </Box>
                )}
                
                {/* Thought Connections Visualization */}
                {thoughts.length > 0 && isThinkingComplete && (
                    <Box flexDirection="column" borderStyle="single" paddingX={1} marginBottom={1}>
                        <Text color="cyan">🔗 Thought Connections</Text>
                        {this.renderThoughtConnections()}
                    </Box>
                )}
                
                {/* Controls */}
                {!this.state.isLoading && (
                    <Box flexDirection="row" marginTop={1}>
                        <Text color="white">Press </Text>
                        <Text color="cyan">ENTER</Text>
                        <Text color="white"> to think, </Text>
                        <Text color="yellow">R</Text>
                        <Text color="white"> to rethink, </Text>
                        <Text color="red">Q</Text>
                        <Text color="white"> to quit</Text>
                    </Box>
                )}
            </Box>
        );
    }
    
    private getThoughtTypeColor(type: ThoughtStep['type']): string {
        switch (type) {
            case 'analysis': return 'blue';
            case 'hypothesis': return 'magenta';
            case 'evaluation': return 'yellow';
            case 'synthesis': return 'cyan';
            case 'conclusion': return 'green';
            default: return 'white';
        }
    }
    
    private renderThinkingAnimation(): React.ReactNode {
        const [dots, setDots] = useState('');
        
        useEffect(() => {
            const interval = setInterval(() => {
                setDots(prev => prev.length >= 3 ? '' : prev + '.');
            }, 500);
            
            return () => clearInterval(interval);
        }, []);
        
        return (
            <Box>
                <Text color="yellow">Thinking{dots}</Text>
                <Text color="blue"> ████████████████████</Text>
            </Box>
        );
    }
    
    private renderThoughtConnections(): React.ReactNode {
        const connections = this.state.thoughts.reduce((acc, thought) => {
            thought.connections.forEach(connectedId => {
                const connection = `${thought.id} → ${connectedId}`;
                if (!acc.includes(connection)) {
                    acc.push(connection);
                }
            });
            return acc;
        }, [] as string[]);
        
        return (
            <Box flexDirection="column">
                {connections.map((connection, index) => (
                    <Text key={index} color="blue">
                        {connection}
                    </Text>
                ))}
                {connections.length === 0 && (
                    <Text color="gray">No connections found</Text>
                )}
            </Box>
        );
    }
    
    protected async executeOperation(): Promise<void> {
        this.setState({
            isLoading: true,
            currentStep: 'Initializing thinking process...',
            progress: 10,
            thoughts: [],
            currentThought: 0,
            isThinkingComplete: false
        });
        
        try {
            // Step 1: Initialize thinking
            this.setState({
                currentStep: 'Analyzing problem structure...',
                progress: 20
            });
            
            const initResult = await this.pythonBridge.executeTool(
                'think',
                'initialize_thinking',
                {
                    problem: this.state.problem,
                    thinking_mode: this.state.thinkingMode
                }
            );
            
            if (!initResult.success) {
                throw new Error(initResult.error);
            }
            
            // Step 2: Stream thinking process
            this.setState({
                currentStep: 'Processing thoughts...',
                progress: 40
            });
            
            const thinkingResult = await this.pythonBridge.executeTool(
                'think',
                'stream_thinking',
                {
                    problem: this.state.problem,
                    thinking_mode: this.state.thinkingMode,
                    max_thoughts: 10
                }
            );
            
            if (thinkingResult.success) {
                // Process streamed thoughts
                const thoughts: ThoughtStep[] = thinkingResult.thoughts.map((thoughtData: any, index: number) => ({
                    id: index + 1,
                    type: thoughtData.type,
                    content: thoughtData.content,
                    timestamp: Date.now() + index * 1000,
                    confidence: thoughtData.confidence || 0.7,
                    connections: thoughtData.connections || []
                }));
                
                // Simulate streaming by adding thoughts one by one
                for (let i = 0; i < thoughts.length; i++) {
                    await new Promise(resolve => setTimeout(resolve, 1500));
                    
                    this.setState(prev => ({
                        thoughts: [...prev.thoughts, thoughts[i]],
                        currentThought: i,
                        progress: 40 + (i / thoughts.length) * 40
                    }));
                }
                
                // Step 3: Generate conclusion
                this.setState({
                    currentStep: 'Generating conclusion...',
                    progress: 90
                });
                
                const conclusionResult = await this.pythonBridge.executeTool(
                    'think',
                    'generate_conclusion',
                    {
                        problem: this.state.problem,
                        thoughts: thoughts,
                        thinking_mode: this.state.thinkingMode
                    }
                );
                
                if (conclusionResult.success) {
                    this.setState({
                        conclusion: conclusionResult.conclusion,
                        confidence: conclusionResult.confidence || 0.8,
                        isThinkingComplete: true,
                        isLoading: false,
                        progress: 100,
                        currentStep: 'Thinking complete'
                    });
                    
                    this.props.onResult({
                        ...thinkingResult,
                        conclusion: conclusionResult.conclusion,
                        confidence: conclusionResult.confidence
                    });
                } else {
                    throw new Error(conclusionResult.error || 'Failed to generate conclusion');
                }
                
            } else {
                throw new Error(thinkingResult.error || 'Thinking process failed');
            }
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown thinking error';
            this.setState({
                isLoading: false,
                error: errorMessage,
                progress: 0
            });
            
            this.props.onError(errorMessage);
        }
    }
    
    // Handle rethinking
    private async rethink(): Promise<void> {
        this.setState({
            thoughts: [],
            currentThought: 0,
            isThinkingComplete: false,
            conclusion: '',
            confidence: 0
        });
        
        await this.executeOperation();
    }
    
    useInput(useCallback((inputChar, key) => {
        if (this.state.isLoading) return;
        
        if (key.return) {
            if (!this.state.isThinkingComplete) {
                this.executeOperation();
            }
        } else if (inputChar === 'r' || inputChar === 'R') {
            this.rethink();
        } else if (inputChar === 'q' || inputChar === 'Q') {
            // Handle quit
        }
    }, [this.state.isLoading, this.state.isThinkingComplete]));
}

// Functional component wrapper
export default function ThinkUI(props: {
    problem: string;
    thinkingMode?: 'sequential' | 'creative' | 'analytical' | 'problem_solving';
    onResult: (result: any) => void;
    onError: (error: string) => void;
}) {
    return (
        <ThinkInterface
            toolName="think"
            operation="stream_thinking"
            params={{
                problem: props.problem,
                thinking_mode: props.thinkingMode || 'sequential'
            }}
            onResult={props.onResult}
            onError={props.onError}
        />
    );
}
```

---

## 🗂️ **REMAINING TOOLS QUICK REFERENCE**

### **Tool 5-11: Implementation Templates**

Each remaining tool follows the same pattern. Here's the quick implementation guide:

```typescript
// Template for remaining tools
export class [ToolName]Interface extends BaseToolInterface {
    // Tool-specific state interface
    // Tool-specific validation logic
    // Tool-specific rendering with:
    //   - Configuration display
    //   - Progress indicators  
    //   - Results visualization
    //   - Interactive controls
    // Tool-specific execution with streaming updates
    // Tool-specific input handling
}
```

**Remaining Tools to Implement:**
1. **FileOperationsInterface** - File system operations with tree view
2. **FilesApiInterface** - API file management with upload/download progress
3. **GraphicDesignInterface** - Design automation with preview capabilities
4. **McpConnectorInterface** - MCP protocol with connection status
5. **PerplexitySearchInterface** - Perplexity search with source citations
6. **TextEditorInterface** - Rich text editing with syntax highlighting
7. **BraveSearchInterface** - Brave search with result filtering

---

## 🔗 **UI INTEGRATION PATTERNS**

### **Tool Orchestration Manager**

```typescript
// interfaces/mao/source/components/ToolOrchestrator.tsx
import React, {useState, useCallback} from 'react';
import {Box, Text} from 'ink';

// Import all tool interfaces
import WebSearchUI from './tools/WebSearchInterface.js';
import CodeExecutionUI from './tools/CodeExecutionInterface.js';
import DalleGenerateUI from './tools/DalleGenerateInterface.js';
// ... other tool imports

interface ToolOrchestratorProps {
    activeTools: string[];
    toolParams: Record<string, any>;
    onToolResult: (toolName: string, result: any) => void;
    onToolError: (toolName: string, error: string) => void;
}

export default function ToolOrchestrator({
    activeTools,
    toolParams,
    onToolResult,
    onToolError
}: ToolOrchestratorProps) {
    
    const renderTool = useCallback((toolName: string) => {
        const params = toolParams[toolName] || {};
        
        switch (toolName) {
            case 'web_search':
                return (
                    <WebSearchUI
                        key={toolName}
                        query={params.query}
                        maxResults={params.max_results}
                        searchMode={params.search_mode}
                        filters={params.filters}
                        onResult={(result) => onToolResult(toolName, result)}
                        onError={(error) => onToolError(toolName, error)}
                    />
                );
                
            case 'code_execution':
                return (
                    <CodeExecutionUI
                        key={toolName}
                        code={params.code}
                        language={params.language}
                        executionMode={params.execution_mode}
                        environment={params.environment}
                        onResult={(result) => onToolResult(toolName, result)}
                        onError={(error) => onToolError(toolName, error)}
                    />
                );
                
            case 'dalle_generate':
                return (
                    <DalleGenerateUI
                        key={toolName}
                        prompt={params.prompt}
                        size={params.size}
                        quality={params.quality}
                        style={params.style}
                        numberOfImages={params.n}
                        onResult={(result) => onToolResult(toolName, result)}
                        onError={(error) => onToolError(toolName, error)}
                    />
                );
                
            // Add other tools...
            
            default:
                return (
                    <Box borderStyle="single" paddingX={1}>
                        <Text color="red">Unknown tool: {toolName}</Text>
                    </Box>
                );
        }
    }, [toolParams, onToolResult, onToolError]);
    
    return (
        <Box flexDirection="column">
            {activeTools.map(toolName => (
                <Box key={toolName} marginBottom={1}>
                    {renderTool(toolName)}
                </Box>
            ))}
        </Box>
    );
}
```

---

## 🎯 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Core Infrastructure (Day 1)**
- [ ] BaseToolInterface abstract class
- [ ] PythonBridge integration patterns  
- [ ] Error handling and loading states
- [ ] Progress visualization components

### **Phase 2: Primary Tools (Day 1-2)**
- [ ] WebSearchInterface (complete implementation)
- [ ] CodeExecutionInterface with interactive mode
- [ ] DalleGenerateInterface with image preview
- [ ] ThinkInterface with streaming thoughts

### **Phase 3: Secondary Tools (Day 2)**
- [ ] FileOperationsInterface with tree view
- [ ] TextEditorInterface with syntax highlighting
- [ ] McpConnectorInterface with connection status
- [ ] PerplexitySearchInterface with citations

### **Phase 4: Integration & Polish (Day 3)**
- [ ] ToolOrchestrator for multi-tool workflows
- [ ] ChatInterface integration with all tools
- [ ] Performance optimization and caching
- [ ] Comprehensive testing and error handling

---

**This detailed UI implementation plan gives you granular, production-ready TypeScript/React/Ink code for every tool in your MAO ecosystem. Each component is fully interactive, handles real-time updates, and integrates seamlessly with your Python backend through the PythonBridge!** 🚀⚡