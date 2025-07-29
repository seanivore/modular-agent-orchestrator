/**
 * UI State Reader - Mao's Eyes Into Its Own Interface
 * Allows LLM to see current chat state and make intelligent visual decisions
 * This is the breakthrough: LLMs controlling their own visual output
 */

interface Message {
	id: string;
	type: 'user' | 'mao';
	content: string;
	timestamp: Date;
	metadata?: any;
}

interface UIState {
	messageCount: number;
	visibleLines: number;
	lastMessageType: string;
	conversationDensity: 'sparse' | 'moderate' | 'dense' | 'cluttered';
	cognitiveLoad: number; // 1-10 scale
	recentActivity: string[];
	layoutOpportunities: LayoutOpportunity[];
}

interface LayoutOpportunity {
	messageId: string;
	action: 'collapse' | 'hide' | 'expand' | 'highlight';
	reason: string;
	spaceSaved: number;
}

export class UIStateReader {
	/**
	 * Analyze current chat state for Mao's visual decision making
	 */
	static analyzeCurrentState(messages: Message[]): UIState {
		const messageCount = messages.length;
		const visibleLines = this.calculateVisibleLines(messages);
		const lastMessageType = messages[messages.length - 1]?.type || 'none';
		
		return {
			messageCount,
			visibleLines,
			lastMessageType,
			conversationDensity: this.calculateDensity(messages),
			cognitiveLoad: this.calculateCognitiveLoad(messages),
			recentActivity: this.extractRecentActivity(messages),
			layoutOpportunities: this.identifyLayoutOpportunities(messages)
		};
	}

	/**
	 * Generate natural language description for Mao to understand UI state
	 */
	static generateStateDescription(messages: Message[]): string {
		const state = this.analyzeCurrentState(messages);
		
		const description = `
Current UI Analysis:
- ${state.messageCount} messages in chat
- ${state.visibleLines} lines visible  
- Conversation density: ${state.conversationDensity}
- Cognitive load: ${state.cognitiveLoad}/10
- Last message from: ${state.lastMessageType}

Recent activity patterns:
${state.recentActivity.map(activity => `- ${activity}`).join('\n')}

Layout optimization opportunities:
${state.layoutOpportunities.map(opp => 
	`- ${opp.action} message ${opp.messageId}: ${opp.reason} (saves ${opp.spaceSaved} lines)`
).join('\n')}

Visual context: ${this.getVisualContext(messages)}
		`.trim();

		return description;
	}

	private static calculateVisibleLines(messages: Message[]): number {
		return messages.reduce((total, message) => {
			// Estimate lines per message based on content
			const contentLines = message.content.split('\n').length;
			const bulletPadding = message.type === 'user' ? 1 : 1;
			return total + contentLines + bulletPadding;
		}, 0);
	}

	private static calculateDensity(messages: Message[]): 'sparse' | 'moderate' | 'dense' | 'cluttered' {
		const visibleLines = this.calculateVisibleLines(messages);
		const messageCount = messages.length;
		
		if (messageCount <= 3) return 'sparse';
		if (visibleLines <= 20) return 'moderate';
		if (visibleLines <= 40) return 'dense';
		return 'cluttered';
	}

	private static calculateCognitiveLoad(messages: Message[]): number {
		let load = 0;
		
		// Base load from message count
		load += Math.min(messages.length * 0.5, 5);
		
		// Add load from complex message types
		messages.forEach(message => {
			if (message.content.includes('○') || message.content.includes('●')) load += 1;
			if (message.content.includes('error') || message.content.includes('failed')) load += 1.5;
			if (message.content.length > 500) load += 1;
			if (message.content.split('\n').length > 10) load += 1;
		});
		
		return Math.min(Math.round(load), 10);
	}

	private static extractRecentActivity(messages: Message[]): string[] {
		const recent = messages.slice(-5); // Last 5 messages
		const activities: string[] = [];
		
		recent.forEach(message => {
			if (message.type === 'user') {
				if (message.content.startsWith('/')) {
					activities.push(`User executed: ${message.content.split(' ')[0]}`);
				} else {
					activities.push('User asked question');
				}
			} else {
				if (message.content.includes('○') || message.content.includes('●')) {
					activities.push('Mao provided action list');
				} else if (message.content.includes('1.') || message.content.includes('2.')) {
					activities.push('Mao provided numbered list');
				} else {
					activities.push('Mao provided explanation');
				}
			}
		});
		
		return activities;
	}

	private static identifyLayoutOpportunities(messages: Message[]): LayoutOpportunity[] {
		const opportunities: LayoutOpportunity[] = [];
		
		messages.forEach((message, index) => {
			// Identify old action lists that can collapse
			if (message.content.includes('○') && index < messages.length - 3) {
				opportunities.push({
					messageId: message.id,
					action: 'collapse',
					reason: 'Old action list - can summarize',
					spaceSaved: this.estimateCollapseSavings(message.content)
				});
			}
			
			// Identify resolved errors that can hide
			if (message.content.toLowerCase().includes('error') && index < messages.length - 2) {
				const resolved = messages.slice(index + 1).some(m => 
					m.content.toLowerCase().includes('resolved') || 
					m.content.toLowerCase().includes('fixed')
				);
				if (resolved) {
					opportunities.push({
						messageId: message.id,
						action: 'hide',
						reason: 'Error resolved in later messages',
						spaceSaved: message.content.split('\n').length
					});
				}
			}
			
			// Identify long content that should collapse
			if (message.content.split('\n').length > 8 && index < messages.length - 1) {
				opportunities.push({
					messageId: message.id,
					action: 'collapse',
					reason: 'Long content - truncate for space',
					spaceSaved: Math.max(0, message.content.split('\n').length - 3)
				});
			}
		});
		
		return opportunities.slice(0, 5); // Limit to top 5 opportunities
	}

	private static estimateCollapseSavings(content: string): number {
		const lines = content.split('\n').length;
		return Math.max(0, lines - 2); // Collapse to ~2 lines
	}

	private static getVisualContext(messages: Message[]): string {
		const contexts: string[] = [];
		
		if (messages.length === 0) contexts.push('empty chat');
		if (messages.length >= 10) contexts.push('long conversation');
		
		const hasActionLists = messages.some(m => m.content.includes('○') || m.content.includes('●'));
		if (hasActionLists) contexts.push('contains action lists');
		
		const hasErrors = messages.some(m => m.content.toLowerCase().includes('error'));
		if (hasErrors) contexts.push('contains errors');
		
		const recentUser = messages.slice(-3).some(m => m.type === 'user');
		if (recentUser) contexts.push('recent user input');
		
		return contexts.join(', ') || 'normal conversation';
	}

	/**
	 * Export UI state as JSON for Python backend
	 */
	static exportForBackend(messages: Message[]): string {
		const state = this.analyzeCurrentState(messages);
		const description = this.generateStateDescription(messages);
		
		return JSON.stringify({
			state,
			description,
			timestamp: Date.now()
		}, null, 2);
	}

	/**
	 * Calculate if new content will cause visual overload
	 */
	static willCauseOverload(messages: Message[], newContentLines: number): boolean {
		const currentLines = this.calculateVisibleLines(messages);
		const projectedLines = currentLines + newContentLines;
		
		// Consider overload if we'll exceed reasonable terminal height
		return projectedLines > 50 || messages.length > 12;
	}

	/**
	 * Suggest immediate pre-emptive actions before adding content
	 */
	static suggestPreemptiveActions(messages: Message[], newContentLines: number): LayoutOpportunity[] {
		if (!this.willCauseOverload(messages, newContentLines)) {
			return [];
		}
		
		const opportunities = this.identifyLayoutOpportunities(messages);
		
		// Sort by space savings and prioritize for immediate action
		return opportunities
			.sort((a, b) => b.spaceSaved - a.spaceSaved)
			.slice(0, 3); // Top 3 most impactful actions
	}
}