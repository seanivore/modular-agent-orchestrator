/**
 * MessageBlock - Core message block component with courteous behavior
 * Every message block constantly re-evaluated and re-written in real-time
 * Uses only as much space as absolutely necessary
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';

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

type MessageType = 
	| 'conversational' 
	| 'bullet_list' 
	| 'numbered_list' 
	| 'action_list' 
	| 'pasted_text';

export default function MessageBlock({message, isLatest = false}: MessageBlockProps) {
	const [isExpanded, setIsExpanded] = useState(false);
	const messageType = detectMessageType(message);
	
	// Courteous behavior - constantly re-evaluate content
	const displayContent = getDisplayContent(message.content, messageType, isLatest, isExpanded);
	const needsExpansion = shouldShowExpansion(message.content, messageType, isExpanded);
	
	// Handle ctrl+r for expansion/collapse
	useInput(useCallback((_, key) => {
		if (key.ctrl && (key.return || key.name === 'r')) {
			setIsExpanded(!isExpanded);
		}
	}, [isExpanded]));

	// Get bullet symbol and color based on message type and source
	const bulletDisplay = getBulletDisplay(message.type, messageType);

	return (
		<Box flexDirection="column" marginBottom={1}>
			{/* Main Message Content */}
			<Box>
				<Text color={bulletDisplay.color}>{bulletDisplay.symbol}   </Text>
				<Box flexDirection="column" flexGrow={1}>
					{renderMessageContent(displayContent, messageType, message.type)}
				</Box>
			</Box>
			
			{/* Expansion hint when needed */}
			{needsExpansion && (
				<Box marginLeft={4}>
					<Text color={colorSystem.getColor('supplemental_2')}>
						{getExpansionHint(message.content, isExpanded)}
					</Text>
				</Box>
			)}
		</Box>
	);
}

/**
 * Detect message type for proper rendering
 */
function detectMessageType(message: Message): MessageType {
	const content = message.content;
	
	// Detect pasted text by token count (>100 tokens threshold)
	if (estimateTokens(content) > 100) {
		return 'pasted_text';
	}
	
	// Detect action lists by symbols
	if (content.includes('○') || content.includes('●') || content.includes('▶︎') || content.includes('▷')) {
		return 'action_list';
	}
	
	// Detect numbered lists
	if (/^\d+\.\s/m.test(content)) {
		return 'numbered_list';
	}
	
	// Detect bullet lists
	if (/^[-•*]\s/m.test(content)) {
		return 'bullet_list';
	}
	
	// Default to conversational
	return 'conversational';
}

/**
 * Get bullet symbol and color based on exact specs from implementation docs
 */
function getBulletDisplay(userType: 'user' | 'mao', messageType: MessageType): {symbol: string; color: string} {
	if (userType === 'user') {
		// User messages always get gray > bullet
		return {
			symbol: '>',
			color: colorSystem.getColor('user')
		};
	}
	
	// AI messages get white ● bullet (except action lists which have their own symbols)
	if (messageType === 'action_list') {
		return {
			symbol: '', // Action lists handle their own symbols
			color: colorSystem.getColor('main')
		};
	}
	
	return {
		symbol: '●',
		color: colorSystem.getBulletColor('ai')
	};
}

/**
 * Courteous behavior - get display content using minimal necessary space
 */
function getDisplayContent(content: string, messageType: MessageType, isLatest: boolean, isExpanded: boolean): string {
	if (isExpanded) {
		return content;
	}
	
	// Apply courteous truncation based on message type
	switch (messageType) {
		case 'conversational':
			return truncateConversational(content, isLatest);
		case 'bullet_list':
			return truncateBulletList(content, isLatest);
		case 'action_list':
			return content; // Action lists manage their own space
		case 'pasted_text':
			return `[${estimateTokens(content)} tokens of pasted text]`;
		default:
			return truncateConversational(content, isLatest);
	}
}

/**
 * Truncate conversational text courteously
 */
function truncateConversational(content: string, isLatest: boolean): string {
	const lines = content.split('\n').filter(line => line.trim());
	const maxLines = isLatest ? 5 : 2; // Latest messages get more space
	
	if (lines.length <= maxLines) {
		return content;
	}
	
	// Show first lines only
	return lines.slice(0, maxLines).join('\n');
}

/**
 * Truncate bullet lists courteously
 */
function truncateBulletList(content: string, isLatest: boolean): string {
	const lines = content.split('\n');
	const bulletLines = lines.filter(line => line.trim().match(/^[-•*]\s/));
	const maxBullets = isLatest ? 4 : 2;
	
	if (bulletLines.length <= maxBullets) {
		return content;
	}
	
	// Keep first bullets and their sub-content
	const result: string[] = [];
	let bulletCount = 0;
	
	for (const line of lines) {
		if (line.trim().match(/^[-•*]\s/)) {
			if (bulletCount >= maxBullets) break;
			bulletCount++;
		}
		result.push(line);
	}
	
	return result.join('\n');
}

/**
 * Determine if expansion controls should be shown
 */
function shouldShowExpansion(content: string, messageType: MessageType, isExpanded: boolean): boolean {
	if (messageType === 'pasted_text') return false;
	if (messageType === 'action_list') return false;
	
	const lines = content.split('\n').filter(line => line.trim());
	return lines.length > 3 || content.length > 300;
}

/**
 * Get expansion hint text
 */
function getExpansionHint(content: string, isExpanded: boolean): string {
	if (isExpanded) {
		return 'ctrl+r to collapse';
	}
	
	const lines = content.split('\n').filter(line => line.trim());
	const hiddenLines = Math.max(0, lines.length - 2);
	
	if (hiddenLines > 0) {
		return `... +${hiddenLines} lines (ctrl+r to expand)`;
	}
	
	return 'ctrl+r to expand';
}

/**
 * Render message content with proper semantic highlighting
 */
function renderMessageContent(content: string, messageType: MessageType, userType: 'user' | 'mao'): React.ReactNode {
	switch (messageType) {
		case 'conversational':
			return renderConversational(content, userType);
		case 'bullet_list':
			return renderBulletList(content);
		case 'numbered_list':
			return renderNumberedList(content);
		case 'action_list':
			return renderActionList(content);
		case 'pasted_text':
			return renderPastedText(content);
		default:
			return renderConversational(content, userType);
	}
}

/**
 * Render conversational text with semantic highlighting
 */
function renderConversational(content: string, userType: 'user' | 'mao'): React.ReactNode {
	if (userType === 'user') {
		// User text is always gray, no special highlighting
		return <Text color={colorSystem.getColor('user')}>{content}</Text>;
	}
	
	// AI conversational text uses MAIN color with BOLD highlights for key words
	const paragraphs = content.split('\n\n');
	
	return (
		<Box flexDirection="column">
			{paragraphs.map((paragraph, idx) => (
				<Box key={idx} marginBottom={idx < paragraphs.length - 1 ? 1 : 0}>
					{renderParagraphWithHighlights(paragraph)}
				</Box>
			))}
		</Box>
	);
}

/**
 * Render paragraph with MLA-style highlighting (first few important words bold)
 */
function renderParagraphWithHighlights(paragraph: string): React.ReactNode {
	// Simple implementation: first 2-3 words get BOLD highlighting
	const words = paragraph.split(' ');
	if (words.length <= 3) {
		return <Text color={colorSystem.getColor('bold')} bold>{paragraph}</Text>;
	}
	
	const keyWords = words.slice(0, 2).join(' ');
	const restOfParagraph = words.slice(2).join(' ');
	
	return (
		<Text>
			<Text color={colorSystem.getColor('bold')} bold>{keyWords}</Text>
			<Text color={colorSystem.getColor('main')}> {restOfParagraph}</Text>
		</Text>
	);
}

/**
 * Render bullet list with proper formatting
 */
function renderBulletList(content: string): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => {
				const isBullet = line.trim().match(/^[-•*]\s/);
				if (isBullet) {
					const bulletContent = line.replace(/^(\s*[-•*]\s)/, '');
					return (
						<Box key={idx}>
							<Text color={colorSystem.getBulletColor('ai')}>• </Text>
							{renderParagraphWithHighlights(bulletContent)}
						</Box>
					);
				}
				return (
					<Box key={idx}>
						<Text color={colorSystem.getColor('main')}>{line}</Text>
					</Box>
				);
			})}
		</Box>
	);
}

/**
 * Render numbered list
 */
function renderNumberedList(content: string): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => {
				const numberMatch = line.match(/^(\d+\.\s*)(.*)/);
				if (numberMatch) {
					const [, number, text] = numberMatch;
					return (
						<Box key={idx}>
							<Text color={colorSystem.getColor('main')}>{number}</Text>
							<Text color={colorSystem.getColor('main')}>{text}</Text>
						</Box>
					);
				}
				return (
					<Box key={idx}>
						<Text color={colorSystem.getColor('main')}>{line}</Text>
					</Box>
				);
			})}
		</Box>
	);
}

/**
 * Render action list with proper symbols and colors
 */
function renderActionList(content: string): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => (
				<Box key={idx}>
					<Text color={colorSystem.getColor('main')}>{line}</Text>
				</Box>
			))}
		</Box>
	);
}

/**
 * Render pasted text indicator
 */
function renderPastedText(content: string): React.ReactNode {
	return (
		<Text color={colorSystem.getColor('trusting_update_2')}>
			{content}
		</Text>
	);
}

/**
 * Get actual token count using more sophisticated calculation
 * Falls back to improved estimation when exact counting unavailable
 */
function estimateTokens(text: string): number {
	// More accurate token estimation algorithm
	// Considers word boundaries, punctuation, and typical token patterns
	const words = text.trim().split(/\s+/);
	let tokenCount = 0;
	
	for (const word of words) {
		// Handle punctuation and special characters more accurately
		if (word.length <= 3) {
			tokenCount += 1;
		} else if (word.length <= 6) {
			tokenCount += 1.5;
		} else {
			// Longer words typically split into multiple tokens
			tokenCount += Math.ceil(word.length / 4);
		}
		
		// Account for punctuation as separate tokens
		const punctuationCount = (word.match(/[.!?,:;]/g) || []).length;
		tokenCount += punctuationCount * 0.5;
	}
	
	return Math.ceil(tokenCount);
}