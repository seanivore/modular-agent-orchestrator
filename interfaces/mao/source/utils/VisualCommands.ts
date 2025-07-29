/**
 * Visual Commands - Mao's Direct UI Control System
 * Allows LLM to send layout commands alongside responses
 * Revolutionary: AI controlling its own visual presentation
 */

import React from 'react';

export interface VisualCommand {
	type: 'collapse' | 'hide' | 'expand' | 'highlight' | 'rewrite' | 'reorganize';
	messageId?: string;
	messageIds?: string[];
	duration?: number;
	newContent?: string;
	reason?: string;
}

export interface VisualResponse {
	content: string;
	commands: VisualCommand[];
	metadata: {
		cognitiveLoadTarget: number;
		visualPriority: 'low' | 'medium' | 'high';
		spacingStrategy: 'compact' | 'normal' | 'spacious';
	};
}

export class VisualCommandProcessor {
	private static messageStates = new Map<string, MessageVisualState>();
	private static listeners = new Set<(command: VisualCommand) => void>();

	/**
	 * Process visual commands from Mao's response
	 */
	static processCommands(commands: VisualCommand[]): void {
		commands.forEach(command => {
			this.executeCommand(command);
			this.notifyListeners(command);
		});
	}

	/**
	 * Parse visual commands from Mao's response text
	 * Mao can embed commands naturally in responses
	 */
	static parseEmbeddedCommands(content: string): {cleanContent: string; commands: VisualCommand[]} {
		const commands: VisualCommand[] = [];
		let cleanContent = content;

		// Parse embedded visual commands like: [VISUAL: collapse message-123]
		const visualCommandRegex = /\[VISUAL:\s*(\w+)(?:\s+([^\]]+))?\]/g;
		let match;

		while ((match = visualCommandRegex.exec(content)) !== null) {
			const [fullMatch, commandType, params] = match;
			
			const command: VisualCommand = {
				type: commandType as any,
				reason: 'Embedded in response'
			};

			// Parse parameters
			if (params) {
				const paramParts = params.split(' ');
				if (paramParts[0]?.startsWith('message-')) {
					command.messageId = paramParts[0];
				}
			}

			commands.push(command);
			cleanContent = cleanContent.replace(fullMatch, '');
		}

		return {cleanContent: cleanContent.trim(), commands};
	}

	/**
	 * Generate visual commands based on UI analysis
	 */
	static generateSmartCommands(
		uiState: any, 
		newContentLength: number,
		newContentType: string
	): VisualCommand[] {
		const commands: VisualCommand[] = [];

		// Auto-collapse if adding large content to cluttered chat
		if (uiState.conversationDensity === 'cluttered' && newContentLength > 200) {
			// Find old messages to collapse
			uiState.layoutOpportunities
				.filter((opp: any) => opp.action === 'collapse')
				.slice(0, 2)
				.forEach((opp: any) => {
					commands.push({
						type: 'collapse',
						messageId: opp.messageId,
						reason: `Auto-collapse for space: ${opp.reason}`
					});
				});
		}

		// Auto-hide resolved errors when adding new content
		if (newContentType !== 'error') {
			uiState.layoutOpportunities
				.filter((opp: any) => opp.action === 'hide' && opp.reason.includes('resolved'))
				.forEach((opp: any) => {
					commands.push({
						type: 'hide',
						messageId: opp.messageId,
						reason: opp.reason
					});
				});
		}

		// Highlight important new content
		if (newContentType === 'action_list' || newContentType === 'error') {
			commands.push({
				type: 'highlight',
				duration: 5000,
				reason: 'Important content needs attention'
			});
		}

		return commands;
	}

	private static executeCommand(command: VisualCommand): void {
		switch (command.type) {
			case 'collapse':
				this.collapseMessage(command.messageId!);
				break;
			case 'hide':
				this.hideMessage(command.messageId!);
				break;
			case 'expand':
				this.expandMessage(command.messageId!);
				break;
			case 'highlight':
				this.highlightMessage(command.messageId);
				break;
			case 'rewrite':
				this.rewriteMessage(command.messageId!, command.newContent!);
				break;
			case 'reorganize':
				this.reorganizeMessages(command.messageIds!);
				break;
		}
	}

	private static collapseMessage(messageId: string): void {
		const state = this.messageStates.get(messageId) || {};
		this.messageStates.set(messageId, {
			...state,
			isCollapsed: true,
			lastCollapsed: Date.now()
		});
	}

	private static hideMessage(messageId: string): void {
		const state = this.messageStates.get(messageId) || {};
		this.messageStates.set(messageId, {
			...state,
			isHidden: true,
			lastHidden: Date.now()
		});
	}

	private static expandMessage(messageId: string): void {
		const state = this.messageStates.get(messageId) || {};
		this.messageStates.set(messageId, {
			...state,
			isCollapsed: false,
			isExpanded: true
		});
	}

	private static highlightMessage(messageId?: string): void {
		if (messageId) {
			const state = this.messageStates.get(messageId) || {};
			this.messageStates.set(messageId, {
				...state,
				isHighlighted: true,
				highlightExpiry: Date.now() + 5000
			});
		}
	}

	private static rewriteMessage(messageId: string, newContent: string): void {
		const state = this.messageStates.get(messageId) || {};
		this.messageStates.set(messageId, {
			...state,
			rewrittenContent: newContent,
			lastRewritten: Date.now()
		});
	}

	private static reorganizeMessages(messageIds: string[]): void {
		// Complex reorganization logic would go here
		// For now, just mark as reorganized
		messageIds.forEach(id => {
			const state = this.messageStates.get(id) || {};
			this.messageStates.set(id, {
				...state,
				wasReorganized: true
			});
		});
	}

	/**
	 * Get current visual state for a message
	 */
	static getMessageState(messageId: string): MessageVisualState {
		return this.messageStates.get(messageId) || {};
	}

	/**
	 * Subscribe to visual command events
	 */
	static subscribe(listener: (command: VisualCommand) => void): () => void {
		this.listeners.add(listener);
		return () => this.listeners.delete(listener);
	}

	private static notifyListeners(command: VisualCommand): void {
		this.listeners.forEach(listener => listener(command));
	}

	/**
	 * Clear expired highlights and temporary states
	 */
	static cleanupExpiredStates(): void {
		const now = Date.now();
		
		this.messageStates.forEach((state, _messageId) => {
			if (state.highlightExpiry && now > state.highlightExpiry) {
				state.isHighlighted = false;
				delete state.highlightExpiry;
			}
		});
	}

	/**
	 * Get system-wide visual stats for Mao's awareness
	 */
	static getVisualStats(): {
		collapsedCount: number;
		hiddenCount: number;
		highlightedCount: number;
		rewrittenCount: number;
	} {
		let collapsedCount = 0;
		let hiddenCount = 0;
		let highlightedCount = 0;
		let rewrittenCount = 0;

		this.messageStates.forEach(state => {
			if (state.isCollapsed) collapsedCount++;
			if (state.isHidden) hiddenCount++;
			if (state.isHighlighted) highlightedCount++;
			if (state.rewrittenContent) rewrittenCount++;
		});

		return {collapsedCount, hiddenCount, highlightedCount, rewrittenCount};
	}
}

interface MessageVisualState {
	isCollapsed?: boolean;
	isHidden?: boolean;
	isExpanded?: boolean;
	isHighlighted?: boolean;
	highlightExpiry?: number;
	rewrittenContent?: string;
	lastCollapsed?: number;
	lastHidden?: number;
	lastRewritten?: number;
	wasReorganized?: boolean;
}

/**
 * Hook for React components to respond to visual commands
 */

export function useVisualCommands(messageId: string) {
	const [state, setState] = React.useState<MessageVisualState>(() => 
		VisualCommandProcessor.getMessageState(messageId)
	);

	React.useEffect(() => {
		const unsubscribe = VisualCommandProcessor.subscribe((command) => {
			if (command.messageId === messageId || !command.messageId) {
				setState(VisualCommandProcessor.getMessageState(messageId));
			}
		});

		return unsubscribe;
	}, [messageId]);

	return state;
}

/**
 * Cleanup interval for expired states
 */
setInterval(() => {
	VisualCommandProcessor.cleanupExpiredStates();
}, 5000);