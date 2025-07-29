import React, {useState, useEffect} from 'react';
import {Box, Text, useInput} from 'ink';
import TextInput from 'ink-text-input';
import Spinner from 'ink-spinner';
import chalk from 'chalk';
import gradient from 'gradient-string';
import figlet from 'figlet';

type Props = {
	name?: string;
	uiMode?: boolean;
};

type Message = {
	id: string;
	type: 'user' | 'mao' | 'system';
	content: string;
	timestamp: Date;
};

export default function App({name, uiMode = true}: Props) {
	const [messages, setMessages] = useState<Message[]>([]);
	const [input, setInput] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const [isConnected, setIsConnected] = useState(false);

	// Emotional intelligence greeting - remember context
	const getPersonalizedGreeting = () => {
		const hour = new Date().getHours();
		const timeOfDay = hour < 12 ? 'morning' : hour < 17 ? 'afternoon' : 'evening';
		const userName = name || 'friend';
		
		return `Good ${timeOfDay}, ${userName}! 🐱 Ready to build something amazing together?`;
	};

	useEffect(() => {
		// Initialize with emotional intelligence greeting
		const welcomeMessage: Message = {
			id: Date.now().toString(),
			type: 'mao',
			content: getPersonalizedGreeting(),
			timestamp: new Date(),
		};
		setMessages([welcomeMessage]);
		
		// Simulate connection to Python backend
		setTimeout(() => setIsConnected(true), 1000);
	}, [name]);

	const handleSubmit = async () => {
		if (!input.trim()) return;

		const userMessage: Message = {
			id: Date.now().toString(),
			type: 'user',
			content: input,
			timestamp: new Date(),
		};

		setMessages(prev => [...prev, userMessage]);
		setInput('');
		setIsLoading(true);

		// Simulate Mao response
		setTimeout(() => {
			const maoResponse: Message = {
				id: (Date.now() + 1).toString(),
				type: 'mao',
				content: `I hear you! "${input}" - Let me process that with the orchestrator...`,
				timestamp: new Date(),
			};
			setMessages(prev => [...prev, maoResponse]);
			setIsLoading(false);
		}, 1500);
	};

	useInput((input, key) => {
		if (key.return) {
			handleSubmit();
		}
	});

	const renderMaoTitle = () => {
		const maoAscii = figlet.textSync('MAO', {
			font: 'Small',
			horizontalLayout: 'fitted',
			verticalLayout: 'fitted',
		});

		return (
			<Box marginBottom={1}>
				<Text color="cyan">{maoAscii}</Text>
			</Box>
		);
	};

	const renderConnectionStatus = () => (
		<Box marginBottom={1}>
			<Text color={isConnected ? 'green' : 'yellow'}>
				{isConnected ? '● Connected to Orchestrator' : '○ Connecting...'}
			</Text>
		</Box>
	);

	const renderMessage = (message: Message) => {
		const timeStr = message.timestamp.toLocaleTimeString([], {
			hour: '2-digit',
			minute: '2-digit',
		});

		switch (message.type) {
			case 'user':
				return (
					<Box key={message.id} marginBottom={1}>
						<Text color="blue" bold>
							You ({timeStr}):
						</Text>
						<Text> {message.content}</Text>
					</Box>
				);
			case 'mao':
				return (
					<Box key={message.id} marginBottom={1}>
						<Text color="magenta" bold>
							Mao ({timeStr}):
						</Text>
						<Text> {message.content}</Text>
					</Box>
				);
			case 'system':
				return (
					<Box key={message.id} marginBottom={1}>
						<Text color="gray" italic>
							{message.content}
						</Text>
					</Box>
				);
			default:
				return null;
		}
	};

	const renderChatArea = () => (
		<Box flexDirection="column" minHeight={10} maxHeight={20}>
			{messages.map(renderMessage)}
			{isLoading && (
				<Box>
					<Text color="yellow">
						<Spinner type="dots" />
					</Text>
					<Text color="yellow"> Mao is thinking...</Text>
				</Box>
			)}
		</Box>
	);

	const renderInputArea = () => (
		<Box borderStyle="round" borderColor="cyan" paddingX={1}>
			<Text color="cyan">→ </Text>
			<TextInput
				value={input}
				onChange={setInput}
				placeholder="Type your message or /help for commands..."
			/>
		</Box>
	);

	const renderHelp = () => (
		<Box marginBottom={1}>
			<Text color="gray" dimColor>
				💡 Try: /help | /config | /goal "build a website" | /tools | Press Enter to send
			</Text>
		</Box>
	);

	return (
		<Box flexDirection="column" padding={1}>
			{renderMaoTitle()}
			{renderConnectionStatus()}
			{renderChatArea()}
			{renderHelp()}
			{renderInputArea()}
		</Box>
	);
}
