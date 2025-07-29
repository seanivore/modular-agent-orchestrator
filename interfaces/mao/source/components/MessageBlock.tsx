import React, {useState, useEffect} from 'react';
import {Box, Text} from 'ink';
import {SemanticHighlighter} from '../utils/SemanticHighlighter.js';
import {TextBehavior} from '../utils/TextBehavior.js';

interface Message {
	id: string;
	type: 'user' | 'mao';
	content: string;
	timestamp: Date;
	metadata?: any;
}

interface MessageBlockProps {
	message: Message;
	isLatest?: boolean;
}

export default function MessageBlock({message, isLatest = false}: MessageBlockProps) {
	const [isExpanded] = useState(false);
	const [displayContent, setDisplayContent] = useState(message.content);
	
	// Message type detection
	const messageType = detectMessageType(message);
	
	// Apply courteous behavior - constantly re-evaluate content
	useEffect(() => {
		const courteousContent = TextBehavior.processContent(
			message.content, 
			messageType, 
			isLatest,
			isExpanded
		);
		setDisplayContent(courteousContent);
	}, [message.content, messageType, isLatest, isExpanded]);
	
	// Get semantic highlighting for this message type
	const styling = SemanticHighlighter.getMessageStyling(messageType, message.type);
	
	return (
		<Box
			padding={1}
			marginBottom={1}
		>
			{/* Message Header */}
			<Box>
				<Text color={styling.prefixColor}>
					{message.type === 'mao' ? '🐱 mao' : '👤 you'}:
				</Text>
			</Box>
			
			{/* Message Content with Semantic Highlighting */}
			<Box marginTop={1} flexDirection="column">
				{renderMessageContent(displayContent, messageType, styling)}
			</Box>
			
			{/* Expansion Controls */}
			{TextBehavior.needsExpansion(message.content, isExpanded) && (
				<Box marginTop={1}>
					<Text color={styling.expansionColor}>
						{TextBehavior.getExpansionHint(message.content, isExpanded)}
					</Text>
				</Box>
			)}
		</Box>
	);
}

function detectMessageType(message: Message): MessageType {
	const content = message.content.toLowerCase();
	
	// Detect pasted text (high token count indicators)
	if (content.includes('tokens of pasted text') || estimateTokens(message.content) > 100) {
		return 'pasted_text';
	}
	
	// Detect action lists
	if (content.includes('○ Task') || content.includes('● Task') || content.includes('▶︎') || content.includes('▷')) {
		return 'action_list';
	}
	
	// Detect error messages
	if (content.includes('error:') || content.includes('failed') || message.metadata?.error) {
		return 'error';
	}
	
	// Detect numbered lists
	if (/^\d+\.\s/.test(content) || content.includes('\n1.') || content.includes('\n2.')) {
		return 'numbered_list';
	}
	
	// Detect bullet points
	if (content.includes('- ') || content.includes('• ') || content.includes('* ')) {
		return 'bullet_list';
	}
	
	// Default to conversational
	return 'conversational';
}

function renderMessageContent(
	content: string, 
	messageType: MessageType, 
	styling: any
): React.ReactNode {
	switch (messageType) {
		case 'pasted_text':
			return renderPastedText(content, styling);
		case 'action_list':
			return renderActionList(content, styling);
		case 'numbered_list':
			return renderNumberedList(content, styling);
		case 'bullet_list':
			return renderBulletList(content, styling);
		case 'error':
			return renderErrorMessage(content, styling);
		default:
			return renderConversationalText(content, styling);
	}
}

function renderConversationalText(content: string, styling: any): React.ReactNode {
	// Split into paragraphs and apply semantic highlighting
	const paragraphs = content.split('\n\n');
	
	return (
		<Box flexDirection="column">
			{paragraphs.map((paragraph, idx) => (
				<Box key={idx} marginBottom={idx < paragraphs.length - 1 ? 1 : 0}>
					<Text color={styling.textColor}>
						{SemanticHighlighter.highlightContent(paragraph, 'conversational')}
					</Text>
				</Box>
			))}
		</Box>
	);
}

function renderBulletList(content: string, styling: any): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => {
				const isBullet = line.trim().match(/^[-•*]\s/);
				const displayLine = isBullet ? line.replace(/^(\s*[-•*]\s)/, '') : line;
				
				return (
					<Box key={idx}>
						{isBullet && (
							<Text color={styling.bulletColor}>• </Text>
						)}
						<Text color={styling.textColor}>
							{SemanticHighlighter.highlightContent(displayLine, 'bullet_list')}
						</Text>
					</Box>
				);
			})}
		</Box>
	);
}

function renderNumberedList(content: string, styling: any): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => (
				<Box key={idx}>
					<Text color={styling.numberColor}>
						{SemanticHighlighter.highlightContent(line, 'numbered_list')}
					</Text>
				</Box>
			))}
		</Box>
	);
}

function renderActionList(content: string, styling: any): React.ReactNode {
	// Action lists get special rendering - will integrate with ActionList.tsx later
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => (
				<Box key={idx}>
					<Text color={styling.actionColor}>
						{SemanticHighlighter.highlightContent(line, 'action_list')}
					</Text>
				</Box>
			))}
		</Box>
	);
}

function renderPastedText(content: string, styling: any): React.ReactNode {
	const tokenCount = estimateTokens(content);
	
	if (tokenCount <= 100) {
		// Show full text for small pastes
		return (
			<Text color={styling.textColor}>
				{content}
			</Text>
		);
	}
	
	// Show token indicator for large pastes
	return (
		<Box>
			<Text color={styling.pastedIndicatorColor}>
				[{tokenCount} tokens of pasted text]
			</Text>
		</Box>
	);
}

function renderErrorMessage(content: string, styling: any): React.ReactNode {
	return (
		<Box flexDirection="column">
			<Text color={styling.errorColor}>
				{SemanticHighlighter.highlightContent(content, 'error')}
			</Text>
		</Box>
	);
}

function estimateTokens(text: string): number {
	// Rough token estimation: ~4 characters per token
	return Math.ceil(text.length / 4);
}

type MessageType = 
	| 'conversational' 
	| 'bullet_list' 
	| 'numbered_list' 
	| 'action_list' 
	| 'pasted_text' 
	| 'error';