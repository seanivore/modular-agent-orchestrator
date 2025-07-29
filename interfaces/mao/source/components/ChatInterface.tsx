import React, {useState, useCallback, useEffect} from 'react';
import {Box, Text, useInput, Spacer} from 'ink';
import {PythonBridge} from '../api/PythonBridge.js';
import MessageBlock from './MessageBlock.js';
import ActionList from './ActionList.js';
import ThinkingIndicator from './ThinkingIndicator.js';
import CommandAutocomplete from './CommandAutocomplete.js';
import {colorSystem} from '../utils/ColorSystem.js';
import {UIStateReader} from '../utils/UIStateReader.js';
import {VisualCommandProcessor} from '../utils/VisualCommands.js';

type Props = {
	username: string;
};

type Message = {
	id: string;
	type: 'user' | 'mao';
	content: string;
	timestamp: Date;
};

export default function ChatInterface({username}: Props) {
	const [messages, setMessages] = useState<Message[]>([]);
	const [input, setInput] = useState('');
	const [isConnected, setIsConnected] = useState(false);
	const [isThinking, setIsThinking] = useState(false);
	const [showAutocomplete, setShowAutocomplete] = useState(false);
	const [activeWorkflows, setActiveWorkflows] = useState<any[]>([]);
	const [pythonBridge] = useState(() => new PythonBridge());

	useEffect(() => {
		// Check backend connection status
		pythonBridge.ping().then(() => {
			setIsConnected(true);
		}).catch(() => {
			setIsConnected(false);
		});
	}, [pythonBridge]);

	const getGracefulFallback = useCallback((content: string): string => {
		if (content.startsWith('/help')) return 'Available commands: /config, /stats, /exit, /goal';
		if (content.startsWith('/exit')) process.exit(0);
		if (content.startsWith('/config')) return 'Configuration panel - connecting to backend...';
		if (content.startsWith('/stats')) return 'System stats - connecting to backend...';
		return `Processing: "${content}" - establishing backend connection...`;
	}, []);

	const handleUserMessage = useCallback(async (content: string) => {
		const userMessage: Message = {
			id: `user-${Date.now()}`,
			type: 'user',
			content,
			timestamp: new Date(),
		};

		// Add user message first
		setMessages(prev => {
			const newMessages = [...prev, userMessage];
			
			// Send UI state to backend for Mao's visual analysis
			const uiStateDescription = UIStateReader.generateStateDescription(newMessages);
			console.log('UI State for Mao:', uiStateDescription);
			
			return newMessages;
		});
		
		setIsThinking(true);

		try {
			let response: string;
			
			// Include UI context in requests so Mao can make visual decisions
			const currentUIState = UIStateReader.exportForBackend(messages);
			
			if (content.startsWith('/')) {
				response = await pythonBridge.executeSlashCommand(content);
			} else {
				// Send UI state with chat message for intelligent layout decisions
				response = await pythonBridge.chat(content + `\n\n[UI_CONTEXT: ${currentUIState}]`);
			}

			// Parse any embedded visual commands from Mao's response
			const {cleanContent, commands} = VisualCommandProcessor.parseEmbeddedCommands(response);
			
			// Execute Mao's visual commands immediately
			if (commands.length > 0) {
				VisualCommandProcessor.processCommands(commands);
			}

			const maoMessage: Message = {
				id: `mao-${Date.now()}`,
				type: 'mao',
				content: cleanContent, // Use cleaned content without visual commands
				timestamp: new Date(),
			};

			setMessages(prev => [...prev, maoMessage]);
		} catch (error) {
			// Graceful fallback with connection status
			const fallbackResponse = getGracefulFallback(content);
			const maoMessage: Message = {
				id: `mao-${Date.now()}`,
				type: 'mao',
				content: fallbackResponse,
				timestamp: new Date(),
			};

			setMessages(prev => [...prev, maoMessage]);
			console.error('Backend communication error:', error);
		} finally {
			setIsThinking(false);
		}
	}, [pythonBridge, getGracefulFallback, messages]);

	useInput(useCallback((inputChar, key) => {
		// Handle autocomplete
		if (showAutocomplete) {
			if (key.escape) {
				setShowAutocomplete(false);
			}
			return; // Let CommandAutocomplete handle input
		}

		// Show autocomplete when typing /
		if (inputChar === '/' && !input.length) {
			setShowAutocomplete(true);
			setInput('/');
			return;
		}

		// Handle normal input
		if (key.return && input.trim()) {
			handleUserMessage(input.trim());
			setInput('');
			setShowAutocomplete(false);
		} else if (key.backspace || key.delete) {
			const newInput = input.slice(0, -1);
			setInput(newInput);
			if (!newInput.length) {
				setShowAutocomplete(false);
			}
		} else if (key.escape) {
			setInput('');
			setShowAutocomplete(false);
		} else if (inputChar && !key.ctrl && !key.meta && !key.return) {
			setInput(prev => prev + inputChar);
		}
	}, [handleUserMessage, input, showAutocomplete]));

	return (
		<Box flexDirection="column" height="100%" width="100%">
			{/* Welcome Header */}
			<Box
				borderStyle="round"
				borderColor={colorSystem.getColor('main')}
				padding={1}
				marginBottom={1}
			>
				<Box>
					<Text color={colorSystem.getColor('main')} bold>~(=^‥^)</Text>
					<Text>  Mao is ready to help!</Text>
				</Box>
				<Spacer />
				<Box flexDirection="column">
					<Text dimColor>user: {username}</Text>
				</Box>
			</Box>

			{/* Instructions */}
			<Box marginBottom={1}>
				<Text color={colorSystem.getColor('trusting_update_1')}>●</Text>
				<Text> Say "hello" to Mao.</Text>
			</Box>
			<Box marginLeft={4} marginBottom={1} flexDirection="column">
				<Text dimColor>├ Describe your workflow</Text>
				<Text dimColor>├ Ask a question</Text>
				<Text dimColor>└ Share your goal</Text>
			</Box>

			{/* Active Action Lists */}
			{activeWorkflows.length > 0 && (
				<Box flexDirection="column" marginBottom={1}>
					{activeWorkflows.map((workflow, index) => (
						<ActionList
							key={workflow.id}
							id={workflow.id}
							title={workflow.title}
							type={workflow.type}
							items={workflow.items}
							metadata={workflow.metadata}
						/>
					))}
				</Box>
			)}

			{/* Thinking Indicator */}
			{isThinking && (
				<ThinkingIndicator
					isThinking={isThinking}
					conversationContext={messages.map(m => m.content)}
					onInterrupt={() => setIsThinking(false)}
				/>
			)}

			{/* Command Autocomplete */}
			{showAutocomplete && (
				<CommandAutocomplete
					isActive={showAutocomplete}
					input={input}
					onSelect={(command) => {
						setInput(command);
						setShowAutocomplete(false);
						handleUserMessage(command);
					}}
					onClose={() => setShowAutocomplete(false)}
				/>
			)}

			{/* Messages */}
			<Box flexDirection="column" flexGrow={1}>
				{messages.length === 0 ? (
					<Box borderStyle="round" borderColor={colorSystem.getColor('user')} padding={1} marginBottom={1}>
						<Text dimColor> {'>'} Try "how do we start building?" or "/help"</Text>
					</Box>
				) : (
					messages.map((message, index) => (
						<MessageBlock 
							key={message.id} 
							message={message}
							isLatest={index === messages.length - 1}
						/>
					))
				)}
			</Box>

			{/* Input */}
			<Box
				borderStyle="round"
				borderColor={colorSystem.getColor('trusting_update_1')}
				padding={1}
			>
				<Text> {'>'} {input}</Text>
				<Text color={colorSystem.getColor('trusting_update_1')}>|</Text>
			</Box>

			{/* Bottom Status Line - Original Design */}
			<Box marginTop={1} justifyContent="space-between">
				<Text dimColor>  ?  /help for help, /config to change settings</Text>
				<Text color={isConnected ? 'green' : 'yellow'}>
					● {isConnected ? 'connected' : 'mock mode'}
				</Text>
			</Box>
		</Box>
	);
}
