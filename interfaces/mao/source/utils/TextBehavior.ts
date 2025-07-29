// Text Behavior - "Courteous" Message Block Logic
// Implements real-time re-evaluation and space optimization
// Based on PHASE_1_REVISED_ENHANCEMENTS.md specification

type MessageType = 
	| 'conversational' 
	| 'bullet_list' 
	| 'numbered_list' 
	| 'action_list' 
	| 'pasted_text' 
	| 'error';

export class TextBehavior {
	private static readonly MAX_DISPLAY_LINES = 3; // Default truncation threshold
	private static readonly TOKEN_THRESHOLD = 100; // For pasted text handling

	/**
	 * Process content with courteous behavior
	 * Constantly re-evaluates and rewrites content to use minimal space
	 */
	static processContent(
		content: string, 
		messageType: MessageType, 
		isLatest: boolean,
		isExpanded: boolean
	): string {
		if (isExpanded) {
			return content; // Show full content when expanded
		}

		switch (messageType) {
			case 'conversational':
				return this.processConversationalContent(content, isLatest);
			case 'bullet_list':
				return this.processBulletListContent(content, isLatest);
			case 'numbered_list':
				return this.processNumberedListContent(content, isLatest);
			case 'action_list':
				return this.processActionListContent(content, isLatest);
			case 'pasted_text':
				return this.processPastedTextContent(content);
			case 'error':
				return this.processErrorContent(content);
			default:
				return content;
		}
	}

	/**
	 * Determine if content needs expansion controls
	 */
	static needsExpansion(content: string, isExpanded: boolean): boolean {
		if (isExpanded) return true; // Always show "collapse" option when expanded
		
		const lines = content.split('\n');
		return lines.length > this.MAX_DISPLAY_LINES || 
			   content.length > 300 || // Arbitrary character threshold
			   this.containsLongFormContent(content);
	}

	/**
	 * Get expansion hint text
	 */
	static getExpansionHint(content: string, isExpanded: boolean): string {
		if (isExpanded) {
			return 'ctrl+r to collapse';
		}

		const lines = content.split('\n');
		const hiddenLines = Math.max(0, lines.length - this.MAX_DISPLAY_LINES);
		
		if (hiddenLines > 0) {
			return `... +${hiddenLines} lines (ctrl+r to expand)`;
		}

		const estimatedTokens = Math.ceil(content.length / 4);
		if (estimatedTokens > this.TOKEN_THRESHOLD) {
			return `... +${estimatedTokens - this.TOKEN_THRESHOLD} tokens (ctrl+r to expand)`;
		}

		return 'ctrl+r to expand';
	}

	private static processConversationalContent(
		content: string, 
		isLatest: boolean
	): string {
		// For latest messages, be less aggressive with truncation
		const maxLines = isLatest ? this.MAX_DISPLAY_LINES + 2 : this.MAX_DISPLAY_LINES;
		
		// Split into lines and apply truncation
		const lines = content.split('\n');
		if (lines.length <= maxLines) {
			return content;
		}

		// Keep first lines and add truncation hint
		const visibleLines = lines.slice(0, maxLines);
		return visibleLines.join('\n');
	}

	private static processBulletListContent(
		content: string, 
		isLatest: boolean
	): string {
		const lines = content.split('\n');
		const bulletLines = lines.filter(line => line.trim().match(/^[-•*]\s/));
		
		// For bullet lists, show at least 3 bullets even if it exceeds line limit
		const maxBullets = isLatest ? 5 : 3;
		
		if (bulletLines.length <= maxBullets) {
			return content;
		}

		// Keep first bullets and their sub-items
		const visibleContent = this.keepFirstItems(lines, maxBullets, /^[-•*]\s/);
		return visibleContent;
	}

	private static processNumberedListContent(
		content: string, 
		isLatest: boolean
	): string {
		const lines = content.split('\n');
		const numberedLines = lines.filter(line => line.trim().match(/^\d+\.\s/));
		
		// Numbered lists get special treatment - show more items
		const maxItems = isLatest ? 7 : 5;
		
		if (numberedLines.length <= maxItems) {
			return content;
		}

		const visibleContent = this.keepFirstItems(lines, maxItems, /^\d+\.\s/);
		return visibleContent;
	}

	private static processActionListContent(
		content: string, 
		isLatest: boolean
	): string {
		// Action lists are special - they manage their own space
		// This will integrate with ActionList.tsx component later
		const lines = content.split('\n');
		
		// Keep task headers and first few action items
		const taskLines = lines.filter(line => line.includes('○ Task') || line.includes('● Task'));
		const maxTasks = isLatest ? 2 : 1;
		
		if (taskLines.length <= maxTasks) {
			return content;
		}

		// Complex action list truncation logic
		return this.truncateActionList(lines, maxTasks);
	}

	private static processPastedTextContent(
		content: string
	): string {
		// Pasted text gets token count treatment
		const estimatedTokens = Math.ceil(content.length / 4);
		
		if (estimatedTokens <= this.TOKEN_THRESHOLD) {
			return content;
		}

		// Convert to token indicator
		return `[${estimatedTokens} tokens of pasted text]`;
	}

	private static processErrorContent(
		content: string
	): string {
		// Error messages should be concise but complete
		const lines = content.split('\n');
		
		if (lines.length <= 4) {
			return content;
		}

		// Keep error message and first few lines of context
		return lines.slice(0, 4).join('\n');
	}

	private static keepFirstItems(
		lines: string[], 
		maxItems: number, 
		itemPattern: RegExp
	): string {
		const result: string[] = [];
		let itemCount = 0;
		let inItem = false;

		for (const line of lines) {
			if (line.trim().match(itemPattern)) {
				if (itemCount >= maxItems) {
					break;
				}
				itemCount++;
				inItem = true;
				result.push(line);
			} else if (inItem) {
				// Include sub-items/continuation lines
				result.push(line);
			} else {
				// Include non-item lines (headers, etc.)
				result.push(line);
			}
		}

		return result.join('\n');
	}

	private static truncateActionList(lines: string[], maxTasks: number): string {
		const result: string[] = [];
		let taskCount = 0;
		let currentTask: string[] = [];

		for (const line of lines) {
			if (line.includes('○ Task') || line.includes('● Task')) {
				// New task found
				if (currentTask.length > 0 && taskCount < maxTasks) {
					result.push(...currentTask);
				}
				
				if (taskCount >= maxTasks) {
					break;
				}
				
				currentTask = [line];
				taskCount++;
			} else {
				// Add to current task
				currentTask.push(line);
			}
		}

		// Add the last task if within limit
		if (currentTask.length > 0 && taskCount <= maxTasks) {
			result.push(...currentTask);
		}

		return result.join('\n');
	}

	private static containsLongFormContent(content: string): boolean {
		// Detect content that typically needs expansion
		return content.includes('```') || // Code blocks
			   content.includes('http') || // URLs (might be long)
			   content.length > 500 ||     // Long content
			   content.split(' ').some(word => word.length > 30); // Long words/paths
	}

	/**
	 * Auto-hide logic for "no longer needed" content
	 * Called when messages are no longer the focus
	 */
	static applyAutoHide(content: string, messageType: MessageType): string {
		// Auto-hide assumes user has already seen this content
		// Be more aggressive with truncation
		
		const lines = content.split('\n');
		const maxLines = messageType === 'action_list' ? 2 : 1;
		
		if (lines.length <= maxLines) {
			return content;
		}

		// Show just the summary/first line
		return lines.slice(0, maxLines).join('\n');
	}

	/**
	 * Calculate visual impact score for intelligent truncation
	 */
	static calculateVisualImpact(content: string, messageType: MessageType): number {
		let score = 0;
		
		// Base score from length
		score += Math.min(content.length / 100, 10);
		
		// Adjust by message type
		switch (messageType) {
			case 'action_list':
				score += 5; // Action lists are visually important
				break;
			case 'error':
				score += 7; // Errors need attention
				break;
			case 'pasted_text':
				score -= 3; // Pasted text is less visually important
				break;
		}
		
		// Adjust by content characteristics
		if (content.includes('○') || content.includes('●')) {
			score += 2; // Lists are structured content
		}
		
		if (content.includes('\n\n')) {
			score += 1; // Paragraphs add structure
		}
		
		return Math.max(0, Math.min(score, 20));
	}
}