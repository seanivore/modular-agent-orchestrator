/**
 * MessageBlock - THE Visual Experience of Mao's Intelligence
 * Shows sophisticated text adaptation, semantic highlighting, and courteous behavior
 * This is where users see Mao's intelligence through dynamic, adaptive text display
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {SemanticHighlighter} from '../utils/SemanticHighlighter.js';
import {TextBehavior} from '../utils/TextBehavior.js';
import {colorSystem} from '../utils/ColorSystem.js';
import {useVisualCommands} from '../utils/VisualCommands.js';

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

interface MessageState {
	displayContent: string;
	isExpanded: boolean;
	needsExpansion: boolean;
	expansionHint: string;
	messageType: MessageType;
	styling: any;
}

type MessageType = 
	| 'conversational' 
	| 'bullet_list' 
	| 'numbered_list' 
	| 'action_list' 
	| 'pasted_text' 
	| 'error';

export default function MessageBlock({message, isLatest = false}: MessageBlockProps) {
	// Hook into Mao's visual command system
	const visualState = useVisualCommands(message.id);
	
	const [state, setState] = useState<MessageState>(() => {
		const messageType = detectMessageType(message);
		const styling = SemanticHighlighter.getMessageStyling(messageType, message.type);
		const displayContent = TextBehavior.processContent(message.content, messageType, isLatest, false);
		
		return {
			displayContent,
			isExpanded: false,
			needsExpansion: TextBehavior.needsExpansion(message.content, false),
			expansionHint: TextBehavior.getExpansionHint(message.content, false),
			messageType,
			styling
		};
	});

	// Real-time content adaptation - "courteous behavior" in action
	useEffect(() => {
		const messageType = detectMessageType(message);
		const styling = SemanticHighlighter.getMessageStyling(messageType, message.type);
		const displayContent = TextBehavior.processContent(
			message.content, 
			messageType, 
			isLatest, 
			state.isExpanded
		);
		
		setState(prev => ({
			...prev,
			displayContent,
			messageType,
			styling,
			needsExpansion: TextBehavior.needsExpansion(message.content, state.isExpanded),
			expansionHint: TextBehavior.getExpansionHint(message.content, state.isExpanded)
		}));
	}, [message.content, isLatest, state.isExpanded]);

	// Handle expansion toggle with Ctrl+R
	const toggleExpansion = useCallback(() => {
		setState(prev => ({
			...prev,
			isExpanded: !prev.isExpanded
		}));
	}, []);

	useInput(useCallback((_, key) => {
		if (key.ctrl && key.return) {
			toggleExpansion();
		}
	}, [toggleExpansion]));

	// Get proper bullet symbol and color based on message type and source
	const getBulletDisplay = (): {symbol: string; color: string} => {
		if (message.type === 'user') {
			return {
				symbol: '>',
				color: colorSystem.getBulletColor('user')
			};
		}
		
		// AI messages get contextual bullets
		switch (state.messageType) {
			case 'action_list':
				return {
					symbol: '○',
					color: state.styling.bulletColor
				};
			case 'error':
				return {
					symbol: '!',
					color: state.styling.bulletColor
				};
			default:
				return {
					symbol: '●',
					color: state.styling.bulletColor
				};
		}
	};

	const bulletDisplay = getBulletDisplay();

	// Don't render if Mao decided to hide this message
	if (visualState.isHidden) {
		return null;
	}

	// Apply Mao's visual transformations
	const effectiveContent = visualState.rewrittenContent || state.displayContent;
	const isHighlighted = visualState.isHighlighted;
	const isCollapsedByMao = visualState.isCollapsed;
	
	// Mao can force expansion or collapse
	const effectiveExpansion = visualState.isExpanded !== undefined ? 
		visualState.isExpanded : state.isExpanded;

	return (
		<Box 
			flexDirection="column" 
			marginBottom={1}
			borderStyle={isHighlighted ? "round" : undefined}
			borderColor={isHighlighted ? colorSystem.getColor('bold') : undefined}
		>
			{/* Main Message Content */}
			<Box>
				<Text color={bulletDisplay.color}>{bulletDisplay.symbol}   </Text>
				<Box flexDirection="column" flexGrow={1}>
					{isCollapsedByMao ? 
						renderMaoCollapsedContent(message, state.messageType) :
						renderSemanticContent(effectiveContent, state.messageType, state.styling)
					}
				</Box>
			</Box>
			
			{/* Mao's intelligent expansion hints */}
			{(state.needsExpansion || isCollapsedByMao) && (
				<Box marginTop={1} marginLeft={4}>
					<Text color={state.styling.expansionColor}>
						{isCollapsedByMao ? 
							"Mao collapsed this for better focus • ctrl+r to expand" :
							state.expansionHint
						}
					</Text>
				</Box>
			)}
			
			{/* Visual intelligence indicator */}
			{(visualState.rewrittenContent || isHighlighted) && (
				<Box marginTop={1} marginLeft={4}>
					<Text color={colorSystem.getColor('processing')}>
						{visualState.rewrittenContent ? "↻ Mao optimized this content" : ""}
						{isHighlighted ? "★ Mao highlighted for attention" : ""}
					</Text>
				</Box>
			)}
		</Box>
	);
}

/**
 * Render content with full semantic highlighting intelligence
 * This is where the visual magic happens - colors show meaning
 */
function renderSemanticContent(
	content: string, 
	messageType: MessageType, 
	styling: any
): React.ReactNode {
	// Get semantic parsing from the highlighter
	const highlighting = SemanticHighlighter.getContentHighlighting(content, messageType);
	
	switch (messageType) {
		case 'conversational':
			return renderConversational(highlighting, styling);
		case 'bullet_list':
			return renderBulletList(content, highlighting, styling);
		case 'numbered_list':
			return renderNumberedList(content, highlighting, styling);
		case 'action_list':
			return renderActionList(content, highlighting, styling);
		case 'pasted_text':
			return renderPastedText(content, styling);
		case 'error':
			return renderError(highlighting, styling);
		default:
			return renderConversational(highlighting, styling);
	}
}

function renderConversational(highlighting: any, styling: any): React.ReactNode {
	return (
		<Box flexDirection="column">
			{highlighting.parts.map((part: any, idx: number) => (
				<Text 
					key={idx}
					color={colorSystem.getTextColor(part.semantic)}
					bold={part.semantic === 'action'}
				>
					{part.text}
				</Text>
			))}
		</Box>
	);
}

function renderBulletList(content: string, highlighting: any, styling: any): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => {
				const isBullet = line.trim().match(/^[-•*]\s/);
				const displayLine = isBullet ? line.replace(/^(\s*[-•*]\s)/, '') : line;
				
				// Parse each line for semantic meaning
				const lineHighlighting = SemanticHighlighter.getContentHighlighting(displayLine, 'bullet_list');
				
				return (
					<Box key={idx}>
						{isBullet && (
							<Text color={styling.bulletColor}>• </Text>
						)}
						<Box>
							{lineHighlighting.parts.map((part: any, partIdx: number) => (
								<Text 
									key={partIdx}
									color={colorSystem.getTextColor(part.semantic)}
									bold={part.semantic === 'action'}
								>
									{part.text}
								</Text>
							))}
						</Box>
					</Box>
				);
			})}
		</Box>
	);
}

function renderNumberedList(content: string, highlighting: any, styling: any): React.ReactNode {
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => {
				const numberMatch = line.match(/^(\d+\.\s*)(.*)/);
				
				if (numberMatch) {
					const [, number, text] = numberMatch;
					const textHighlighting = SemanticHighlighter.getContentHighlighting(text || '', 'numbered_list');
					
					return (
						<Box key={idx}>
							<Text color={colorSystem.getColor('supplemental_2')}>{number}</Text>
							<Box>
								{textHighlighting.parts.map((part: any, partIdx: number) => (
									<Text 
										key={partIdx}
										color={colorSystem.getTextColor(part.semantic)}
										bold={part.semantic === 'action'}
									>
										{part.text}
									</Text>
								))}
							</Box>
						</Box>
					);
				}
				
				return (
					<Box key={idx}>
						<Text color={styling.textColor}>{line}</Text>
					</Box>
				);
			})}
		</Box>
	);
}

function renderActionList(content: string, highlighting: any, styling: any): React.ReactNode {
	// Action lists get special visual treatment
	const lines = content.split('\n');
	
	return (
		<Box flexDirection="column">
			{lines.map((line, idx) => (
				<Box key={idx}>
					{line.includes('○') && (
						<Text color={colorSystem.getColor('user')}>○ </Text>
					)}
					{line.includes('●') && (
						<Text color={colorSystem.getColor('trusting_update_1')}>● </Text>
					)}
					{line.includes('▶︎') && (
						<Text color={colorSystem.getColor('bold')}>▶︎ </Text>
					)}
					{line.includes('▷') && (
						<Text color={colorSystem.getColor('supplemental_2')}>▷ </Text>
					)}
					<Text 
						color={line.includes('○') || line.includes('●') ? 
							colorSystem.getColor('main') : 
							colorSystem.getColor('supplemental_2')}
						bold={line.includes('●') || line.includes('▶︎')}
					>
						{line.replace(/[○●▶︎▷]\s*/, '')}
					</Text>
				</Box>
			))}
		</Box>
	);
}

function renderPastedText(content: string, styling: any): React.ReactNode {
	const tokenCount = Math.ceil(content.length / 4);
	
	if (tokenCount <= 100) {
		return (
			<Text color={styling.textColor}>
				{content}
			</Text>
		);
	}
	
	return (
		<Box>
			<Text color={styling.pastedIndicatorColor}>
				[{tokenCount} tokens of pasted text]
			</Text>
		</Box>
	);
}

function renderError(highlighting: any, styling: any): React.ReactNode {
	return (
		<Box flexDirection="column">
			{highlighting.parts.map((part: any, idx: number) => (
				<Text 
					key={idx}
					color={styling.errorColor}
					bold={true}
				>
					{part.text}
				</Text>
			))}
		</Box>
	);
}

/**
 * Intelligent message type detection
 * Determines how content should be visually presented
 */
function detectMessageType(message: Message): MessageType {
	const content = message.content.toLowerCase();
	
	// High-priority detection first
	if (content.includes('error:') || content.includes('failed') || message.metadata?.error) {
		return 'error';
	}
	
	// Detect pasted text by token count
	if (content.includes('tokens of pasted text') || estimateTokens(message.content) > 100) {
		return 'pasted_text';
	}
	
	// Detect action lists by symbols
	if (content.includes('○') || content.includes('●') || content.includes('▶︎') || content.includes('▷')) {
		return 'action_list';
	}
	
	// Detect numbered lists
	if (/^\d+\.\s/m.test(content) || content.includes('\n1.') || content.includes('\n2.')) {
		return 'numbered_list';
	}
	
	// Detect bullet points
	if (content.match(/^[-•*]\s/m) || content.includes('\n- ') || content.includes('\n• ')) {
		return 'bullet_list';
	}
	
	// Default to conversational
	return 'conversational';
}

function estimateTokens(text: string): number {
	return Math.ceil(text.length / 4);
}

/**
 * Hook for managing message block state
 * Provides external control over expansion, auto-hide, etc.
 */
export function useMessageBlock(message: Message) {
	const [isExpanded, setIsExpanded] = useState(false);
	const [autoHideTimeout, setAutoHideTimeout] = useState<NodeJS.Timeout | null>(null);
	
	const expand = useCallback(() => {
		setIsExpanded(true);
		// Clear auto-hide when user explicitly expands
		if (autoHideTimeout) {
			clearTimeout(autoHideTimeout);
			setAutoHideTimeout(null);
		}
	}, [autoHideTimeout]);
	
	const collapse = useCallback(() => {
		setIsExpanded(false);
	}, []);
	
	const scheduleAutoHide = useCallback((delay: number = 30000) => {
		if (autoHideTimeout) {
			clearTimeout(autoHideTimeout);
		}
		
		const timeout = setTimeout(() => {
			setIsExpanded(false);
		}, delay);
		
		setAutoHideTimeout(timeout);
	}, [autoHideTimeout]);
	
	return {
		isExpanded,
		expand,
		collapse,
		scheduleAutoHide
	};
}

/**
 * Render Mao's intelligently collapsed content
 * Shows just enough to maintain context without clutter
 */
function renderMaoCollapsedContent(message: Message, messageType: MessageType): React.ReactNode {
	const content = message.content;
	
	switch (messageType) {
		case 'action_list':
			// Show task count and first task
			const taskCount = (content.match(/[○●]/g) || []).length;
			const firstTask = content.split('\n').find(line => 
				line.includes('○') || line.includes('●')
			);
			return (
				<Text color={colorSystem.getColor('supplemental_2')}>
					{taskCount} tasks • {firstTask?.replace(/[○●]\s*/, '') || 'processing...'}
				</Text>
			);
			
		case 'bullet_list':
			// Show bullet count and first item
			const bulletCount = (content.match(/^[-•*]\s/gm) || []).length;
			const firstBullet = content.split('\n').find(line => 
				line.trim().match(/^[-•*]\s/)
			);
			return (
				<Text color={colorSystem.getColor('supplemental_2')}>
					{bulletCount} items • {firstBullet?.replace(/^[-•*]\s/, '') || 'list items...'}
				</Text>
			);
			
		case 'numbered_list':
			// Show item count and first item
			const itemCount = (content.match(/^\d+\.\s/gm) || []).length;
			const firstItem = content.split('\n').find(line => 
				line.trim().match(/^\d+\.\s/)
			);
			return (
				<Text color={colorSystem.getColor('supplemental_2')}>
					{itemCount} steps • {firstItem?.replace(/^\d+\.\s/, '') || 'numbered items...'}
				</Text>
			);
			
		case 'error':
			// Show error type and brief description
			const errorMatch = content.match(/(error|failed|exception)[:\s](.{0,50})/i);
			if (errorMatch) {
				return (
					<Text color={colorSystem.getColor('bold')}>
						{errorMatch[1]}: {errorMatch[2]}...
					</Text>
				);
			}
			return (
				<Text color={colorSystem.getColor('bold')}>
					Error occurred • details collapsed
				</Text>
			);
			
		case 'pasted_text':
			// Already handled by token count display
			const tokenCount = Math.ceil(content.length / 4);
			return (
				<Text color={colorSystem.getColor('supplemental_2')}>
					[{tokenCount} tokens of pasted content]
				</Text>
			);
			
		default:
			// Show first sentence or line
			const firstSentence = content.split(/[.!?]/)[0];
			const preview = firstSentence.length > 60 ? 
				firstSentence.substring(0, 60) + '...' : 
				firstSentence + '...';
			return (
				<Text color={colorSystem.getColor('supplemental_2')}>
					{preview}
				</Text>
			);
	}
}