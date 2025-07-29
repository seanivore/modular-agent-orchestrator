/**
 * Semantic Highlighter - Implements exact _VISUAL_BRAND_IDENTITY.md specifications
 * Uses ColorSystem for consistent theming and semantic meaning
 */

import React from 'react';
import { colorSystem, ColorSystem } from './ColorSystem.js';

interface MessageStyling {
	borderColor: string;
	prefixColor: string;
	textColor: string;
	bulletColor: string;
	numberColor: string;
	actionColor: string;
	pastedIndicatorColor: string;
	errorColor: string;
	expansionColor: string;
}

type MessageType = 
	| 'conversational' 
	| 'bullet_list' 
	| 'numbered_list' 
	| 'action_list' 
	| 'pasted_text' 
	| 'error';

type UserType = 'user' | 'mao';

export class SemanticHighlighter {
	private static colorSystem: ColorSystem = colorSystem;

	/**
	 * Get styling configuration based on exact _VISUAL_BRAND_IDENTITY.md rules
	 */
	static getMessageStyling(messageType: MessageType, userType: UserType): MessageStyling {
		if (userType === 'user') {
			// User messages - always gray with gray bullet
			return {
				borderColor: this.colorSystem.getColor('user'),
				prefixColor: this.colorSystem.getColor('user'),
				textColor: this.colorSystem.getColor('user'),
				bulletColor: this.colorSystem.getColor('user'), // Gray bullet for user
				numberColor: this.colorSystem.getColor('user'),
				actionColor: this.colorSystem.getColor('user'),
				pastedIndicatorColor: this.colorSystem.getColor('supplemental_2'),
				errorColor: this.colorSystem.getColor('bold'),
				expansionColor: this.colorSystem.getColor('supplemental_2')
			};
		}

		// AI messages - exact bullet color rules from _VISUAL_BRAND_IDENTITY.md
		switch (messageType) {
			case 'conversational':
				return {
					borderColor: this.colorSystem.getColor('main'),
					prefixColor: this.colorSystem.getColor('main'),
					textColor: this.colorSystem.getColor('main'), // Yellow - AI explaining
					bulletColor: this.colorSystem.getBulletColor('ai'), // White bullet for AI
					numberColor: this.colorSystem.getColor('supplemental_2'), // Light brown for numbers
					actionColor: this.colorSystem.getColor('main'),
					pastedIndicatorColor: this.colorSystem.getColor('supplemental_2'),
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			case 'bullet_list':
				return {
					borderColor: this.colorSystem.getColor('main'),
					prefixColor: this.colorSystem.getColor('main'),
					textColor: this.colorSystem.getColor('main'), // Yellow for AI explaining
					bulletColor: this.colorSystem.getBulletColor('ai'), // White bullet for AI content
					numberColor: this.colorSystem.getColor('supplemental_2'),
					actionColor: this.colorSystem.getColor('main'),
					pastedIndicatorColor: this.colorSystem.getColor('supplemental_2'),
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			case 'numbered_list':
				return {
					borderColor: this.colorSystem.getColor('main'),
					prefixColor: this.colorSystem.getColor('main'),
					textColor: this.colorSystem.getColor('main'), // Yellow throughout
					bulletColor: this.colorSystem.getBulletColor('ai'),
					numberColor: this.colorSystem.getColor('supplemental_2'), // Light brown for numbers
					actionColor: this.colorSystem.getColor('main'),
					pastedIndicatorColor: this.colorSystem.getColor('supplemental_2'),
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			case 'action_list':
				// Action lists with special bullet rules
				return {
					borderColor: this.colorSystem.getColor('main'),
					prefixColor: this.colorSystem.getColor('main'),
					textColor: this.colorSystem.getColor('main'), // Yellow for descriptions
					bulletColor: this.colorSystem.getBulletColor('ai', 'bold'), // Light blue when text is pink/bold
					numberColor: this.colorSystem.getColor('supplemental_2'),
					actionColor: this.colorSystem.getColor('bold'), // Pink for actions
					pastedIndicatorColor: this.colorSystem.getColor('supplemental_2'),
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			case 'pasted_text':
				return {
					borderColor: this.colorSystem.getColor('supplemental_2'),
					prefixColor: this.colorSystem.getColor('supplemental_2'),
					textColor: this.colorSystem.getColor('supplemental_2'), // Light brown - less important
					bulletColor: this.colorSystem.getBulletColor('ai'),
					numberColor: this.colorSystem.getColor('supplemental_2'),
					actionColor: this.colorSystem.getColor('supplemental_2'),
					pastedIndicatorColor: this.colorSystem.getColor('trusting_update_2'), // Light blue for indicators
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			case 'error':
				return {
					borderColor: this.colorSystem.getColor('bold'),
					prefixColor: this.colorSystem.getColor('main'),
					textColor: this.colorSystem.getColor('bold'), // Pink for errors (attention)
					bulletColor: this.colorSystem.getColor('bold'),
					numberColor: this.colorSystem.getColor('bold'),
					actionColor: this.colorSystem.getColor('bold'),
					pastedIndicatorColor: this.colorSystem.getColor('bold'),
					errorColor: this.colorSystem.getColor('bold'),
					expansionColor: this.colorSystem.getColor('supplemental_2')
				};

			default:
				return this.getMessageStyling('conversational', userType);
		}
	}

	/**
	 * Apply semantic meaning through React-compatible color props
	 * Returns JSX-compatible color information
	 */
	static getContentHighlighting(content: string, messageType: MessageType): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		switch (messageType) {
			case 'conversational':
				return this.parseConversationalContent(content);
			case 'bullet_list':
				return this.parseBulletContent(content);
			case 'numbered_list':
				return this.parseNumberedContent(content);
			case 'action_list':
				return this.parseActionContent(content);
			case 'error':
				return this.parseErrorContent(content);
			default:
				return { parts: [{text: content, semantic: 'normal'}] };
		}
	}

	private static parseConversationalContent(content: string): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		const parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}> = [];
		
		// Parse for URLs (AI-highlighted when sent by AI)
		const urlRegex = /(https?:\/\/[^\s]+)/g;
		let lastIndex = 0;
		let match;
		
		while ((match = urlRegex.exec(content)) !== null) {
			// Add text before URL
			if (match.index > lastIndex) {
				const beforeText = content.substring(lastIndex, match.index);
				if (beforeText.trim()) {
					parts.push({text: beforeText, semantic: 'explanation'});
				}
			}
			
			// Add URL as AI highlight
			parts.push({text: match[0], semantic: 'ai_highlight'});
			lastIndex = match.index + match[0].length;
		}
		
		// Add remaining text
		if (lastIndex < content.length) {
			const remainingText = content.substring(lastIndex);
			if (remainingText.trim()) {
				parts.push({text: remainingText, semantic: 'explanation'});
			}
		}
		
		// If no URLs found, return as explanation
		if (parts.length === 0) {
			parts.push({text: content, semantic: 'explanation'});
		}
		
		return { parts };
	}

	private static parseBulletContent(content: string): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		// Parse bullet content - first few words get action highlighting per MLA-style rule
		const cleanContent = content.replace(/^[-•*]\s/, '');
		const words = cleanContent.split(' ');
		
		if (words.length <= 3) {
			return { parts: [{text: cleanContent, semantic: 'action'}] };
		}
		
		// First 2-3 words are action (like MLA title case logic)
		const actionWords = words.slice(0, 2).join(' ');
		const explanationWords = words.slice(2).join(' ');
		
		return {
			parts: [
				{text: actionWords, semantic: 'action'},
				{text: ' ' + explanationWords, semantic: 'explanation'}
			]
		};
	}

	private static parseNumberedContent(content: string): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		// Numbers get metadata styling, rest is explanation
		const numberMatch = content.match(/^(\d+\.\s*)(.*)/); 
		
		if (numberMatch) {
			const [, number, text] = numberMatch;
			const parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}> = [
				{text: number || '', semantic: 'metadata'}
			];
			
			// Parse URLs in the text part
			if (text) {
				const textParts = this.parseConversationalContent(text);
				parts.push(...textParts.parts);
			}
			
			return { parts };
		}
		
		return { parts: [{text: content, semantic: 'explanation'}] };
	}

	private static parseActionContent(content: string): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		const parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}> = [];
		
		// Parse action list content with task indicators and file paths
		// (Variables removed to avoid unused variable warnings)
		
		// For now, return simplified parsing - will enhance with ActionList component
		if (content.includes('○') || content.includes('●')) {
			// Task line
			parts.push({text: content, semantic: 'action'});
		} else if (content.includes('/') && content.includes('.')) {
			// File path line
			parts.push({text: content, semantic: 'ai_highlight'});
		} else {
			// Regular action content
			parts.push({text: content, semantic: 'explanation'});
		}
		
		return { parts };
	}

	private static parseErrorContent(content: string): {
		parts: Array<{text: string; semantic: 'action' | 'explanation' | 'ai_highlight' | 'metadata' | 'normal'}>;
	} {
		// Errors are all high-priority action content
		return { parts: [{text: content, semantic: 'action'}] };
	}

	/**
	 * Update color system theme
	 */
	static updateTheme(themeName: string): void {
		this.colorSystem.setTheme(themeName);
	}

	/**
	 * Get available themes from color system
	 */
	static getAvailableThemes(): string[] {
		return this.colorSystem.getAvailableThemes();
	}

	/**
	 * Get color by semantic meaning
	 */
	static getColor(semanticMeaning: 'action' | 'explanation' | 'user_input' | 'ai_highlight' | 'system_auto' | 'metadata'): string {
		return this.colorSystem.getTextColor(semanticMeaning);
	}

	/**
	 * Highlight content with React components (compatibility method for MessageBlock)
	 */
	static highlightContent(content: string, _messageType: MessageType): React.ReactNode {
		// This method provides React-compatible highlighting
		// Returns the content as string for now - will be enhanced with React components
		// Future enhancement: use this.getContentHighlighting(content, messageType) for semantic parsing
		
		// Return content as string for now - will be enhanced with React components
		// when MessageBlock is fully integrated with the semantic system
		return content;
	}
}