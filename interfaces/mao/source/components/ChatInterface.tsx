import React, {useState, useCallback, useEffect} from 'react';
import {Box, Text, useInput, Spacer} from 'ink';
import {PythonBridge} from '../api/PythonBridge.js';
import MessageBlock from './MessageBlock.js';

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
	const [pythonBridge] = useState(() => new PythonBridge());

	useEffect(() => {
		// Check backend connection status
		pythonBridge.ping().then(() => {
			setIsConnected(true);
		}).catch(() => {
			setIsConnected(false);
		});
	}, [pythonBridge]);

	const getMockResponse = useCallback((content: string): string => {
		if (content.startsWith('/help')) return 'Available commands: /config, /stats, /exit, /goal';
		if (content.startsWith('/exit')) process.exit(0);
		if (content.startsWith('/config')) return 'Configuration panel would open here';
		if (content.startsWith('/stats')) return 'System stats: 3 tools loaded, 2 models available';
		return `I understand you said: "${content}". Backend connection needed for full functionality!`;
	}, []);

	const handleUserMessage = useCallback(async (content: string) => {
		const userMessage: Message = {
			id: `user-${Date.now()}`,
			type: 'user',
			content,
			timestamp: new Date(),
		};

		setMessages(prev => [...prev, userMessage]);

		try {
			let response: string;
			
			if (content.startsWith('/')) {
				response = await pythonBridge.executeSlashCommand(content);
			} else {
				response = await pythonBridge.chat(content);
			}

			const maoMessage: Message = {
				id: `mao-${Date.now()}`,
				type: 'mao',
				content: response,
				timestamp: new Date(),
			};

			setMessages(prev => [...prev, maoMessage]);
		} catch (error) {
			// Fallback to mock responses if backend fails
			const mockResponse = getMockResponse(content);
			const maoMessage: Message = {
				id: `mao-${Date.now()}`,
				type: 'mao',
				content: mockResponse,
				timestamp: new Date(),
			};

			setMessages(prev => [...prev, maoMessage]);
		}
	}, [pythonBridge, getMockResponse]);

	useInput(useCallback((inputChar, key) => {
		if (key.return && input.trim()) {
			handleUserMessage(input.trim());
			setInput('');
		} else if (key.backspace || key.delete) {
			setInput(prev => prev.slice(0, -1));
		} else if (inputChar && !key.ctrl && !key.meta && !key.return) {
			setInput(prev => prev + inputChar);
		}
	}, [handleUserMessage, input]));

	return (
		<Box flexDirection="column" height="100%" width="100%">
			{/* Welcome Header */}
			<Box
				borderStyle="round"
				borderColor="#f1d771"
				padding={1}
				marginBottom={1}
			>
				<Box>
					<Text color="#f1d771" bold>~(=^‥^)</Text>
					<Text>  Mao is ready to help!</Text>
				</Box>
				<Spacer />
				<Box flexDirection="column">
					<Text dimColor>user: {username}</Text>
				</Box>
			</Box>

			{/* Instructions */}
			<Box marginBottom={1}>
				<Text color="#82d0ff">●</Text>
				<Text> Say "hello" to Mao.</Text>
			</Box>
			<Box marginLeft={4} marginBottom={1} flexDirection="column">
				<Text dimColor>├ Describe your workflow</Text>
				<Text dimColor>├ Ask a question</Text>
				<Text dimColor>└ Share your goal</Text>
			</Box>

			{/* Messages */}
			<Box flexDirection="column" flexGrow={1}>
				{messages.length === 0 ? (
					<Box borderStyle="round" borderColor="#bbbcbb" padding={1} marginBottom={1}>
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
				borderColor="#82d0ff"
				padding={1}
			>
				<Text> {'>'} {input}</Text>
				<Text color="#82d0ff">|</Text>
			</Box>

			{/* Status Bar */}
			<Box marginTop={1} justifyContent="space-between">
				<Text dimColor>  ?  /help for help, /config to change settings</Text>
				<Text color={isConnected ? 'green' : 'yellow'}>
					● {isConnected ? 'connected' : 'mock mode'}
				</Text>
			</Box>

			{/* Connection Warning */}
			{!isConnected && (
				<Box marginTop={1}>
					<Text color="yellow">⚠ ⚠ Backend connection failed - using mock responses</Text>
				</Box>
			)}
		</Box>
	);
}
