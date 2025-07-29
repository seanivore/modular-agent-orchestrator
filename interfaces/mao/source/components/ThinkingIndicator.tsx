/**
 * AI Thinking Indicator - Contextual Improv Words System
 * Implements specs from UI_PHASE_1_LOGIC.md for emotional intelligence UX
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';

interface ThinkingState {
	isActive: boolean;
	startTime: number;
	elapsedSeconds: number;
	tokensUsed: number;
	estimatedCost: number;
	contextualWord: string;
	showInterruptHint: boolean;
}

interface ThinkingIndicatorProps {
	isThinking: boolean;
	conversationContext: string[];
	onInterrupt?: () => void;
}

// Contextual thinking words based on conversation context - AI generated for uniqueness
const CONTEXTUAL_WORDS = {
	budget: ['Budgeting', 'Calculating', 'Optimizing', 'Estimating', 'Balancing'],
	workflow: ['Orchestrating', 'Coordinating', 'Sequencing', 'Planning', 'Organizing'],
	analysis: ['Analyzing', 'Dissecting', 'Evaluating', 'Investigating', 'Scrutinizing'],
	creative: ['Ideating', 'Conceptualizing', 'Brainstorming', 'Imagining', 'Crafting'],
	technical: ['Configuring', 'Processing', 'Computing', 'Debugging', 'Optimizing'],
	research: ['Researching', 'Exploring', 'Investigating', 'Discovering', 'Gathering'],
	writing: ['Composing', 'Articulating', 'Crafting', 'Polishing', 'Refining'],
	problem_solving: ['Strategizing', 'Puzzling', 'Deducing', 'Reasoning', 'Solving'],
	celebration: ['Celebrating', 'Appreciating', 'Acknowledging', 'Recognizing', 'Honoring'],
	greeting: ['Welcoming', 'Greeting', 'Acknowledging', 'Connecting', 'Engaging'],
	general: ['Thinking', 'Processing', 'Contemplating', 'Pondering', 'Considering']
};

export default function ThinkingIndicator({
	isThinking,
	conversationContext = [],
	onInterrupt
}: ThinkingIndicatorProps) {
	const [state, setState] = useState<ThinkingState>({
		isActive: false,
		startTime: 0,
		elapsedSeconds: 0,
		tokensUsed: 0,
		estimatedCost: 0,
		contextualWord: '',
		showInterruptHint: false
	});

	// Generate contextual thinking word based on conversation
	const generateContextualWord = useCallback((context: string[]): string => {
		const recentMessages = context.slice(-3).join(' ').toLowerCase();
		
		// Analyze context for emotional intelligence
		let category: keyof typeof CONTEXTUAL_WORDS = 'general';
		
		if (recentMessages.includes('cost') || recentMessages.includes('budget') || recentMessages.includes('price')) {
			category = 'budget';
		} else if (recentMessages.includes('workflow') || recentMessages.includes('orchestrat') || recentMessages.includes('plan')) {
			category = 'workflow';
		} else if (recentMessages.includes('analyz') || recentMessages.includes('review') || recentMessages.includes('assess')) {
			category = 'analysis';
		} else if (recentMessages.includes('creat') || recentMessages.includes('design') || recentMessages.includes('idea')) {
			category = 'creative';
		} else if (recentMessages.includes('config') || recentMessages.includes('setup') || recentMessages.includes('technical')) {
			category = 'technical';
		} else if (recentMessages.includes('research') || recentMessages.includes('find') || recentMessages.includes('search')) {
			category = 'research';
		} else if (recentMessages.includes('writ') || recentMessages.includes('compos') || recentMessages.includes('draft')) {
			category = 'writing';
		} else if (recentMessages.includes('problem') || recentMessages.includes('issue') || recentMessages.includes('fix')) {
			category = 'problem_solving';
		} else if (recentMessages.includes('great') || recentMessages.includes('awesome') || recentMessages.includes('perfect')) {
			category = 'celebration';
		} else if (recentMessages.includes('hello') || recentMessages.includes('hi') || context.length <= 2) {
			category = 'greeting';
		}

		const words = CONTEXTUAL_WORDS[category];
		const randomIndex = Math.floor(Math.random() * words.length);
		return words[randomIndex] || 'Thinking';
	}, []);

	// Initialize thinking state when activated
	useEffect(() => {
		if (isThinking && !state.isActive) {
			const contextualWord = generateContextualWord(conversationContext);
			setState(prev => ({
				...prev,
				isActive: true,
				startTime: Date.now(),
				elapsedSeconds: 0,
				contextualWord,
				showInterruptHint: false
			}));
		} else if (!isThinking && state.isActive) {
			setState(prev => ({
				...prev,
				isActive: false,
				startTime: 0,
				elapsedSeconds: 0,
				tokensUsed: 0,
				estimatedCost: 0,
				contextualWord: '',
				showInterruptHint: false
			}));
		}
	}, [isThinking, state.isActive, conversationContext, generateContextualWord]);

	// Update metrics in real-time
	useEffect(() => {
		if (!state.isActive) return;

		const interval = setInterval(() => {
			const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
			
			// Estimate tokens based on elapsed time (rough approximation)
			const estimatedTokens = Math.floor(elapsed * 45); // ~45 tokens per second during thinking
			
			// Estimate cost based on tokens (Claude Sonnet 4 pricing)
			const estimatedCost = (estimatedTokens * 0.003) / 1000;

			setState(prev => ({
				...prev,
				elapsedSeconds: elapsed,
				tokensUsed: estimatedTokens,
				estimatedCost,
				showInterruptHint: elapsed > 5 // Show interrupt hint after 5 seconds
			}));
		}, 1000);

		return () => clearInterval(interval);
	}, [state.isActive, state.startTime]);

	// Handle ESC key for interruption
	useInput(useCallback((_, key) => {
		if (key.escape && state.isActive && onInterrupt) {
			onInterrupt();
		}
	}, [state.isActive, onInterrupt]));

	// Don't render if not active
	if (!state.isActive) return null;

	// Strategic display rules - only show when appropriate
	const shouldShow = conversationContext.length >= 4 || // After 4+ message volleys
					   state.elapsedSeconds > 3; // Or after 3+ seconds of thinking

	if (!shouldShow) return null;

	return (
		<Box marginBottom={1}>
			{/* Cat ASCII art and thinking word */}
			<Box>
				<Text color={colorSystem.getColor('main')}>~(=^‥^) </Text>
				<Text>🟁 </Text>
				<Text color={colorSystem.getColor('processing')}>{state.contextualWord}... </Text>
				<Text>🟅 </Text>
				<Text color={colorSystem.getColor('user')}>
					({state.elapsedSeconds}s • ${state.estimatedCost.toFixed(3)} • {state.tokensUsed} tokens
					{state.showInterruptHint && ' • esc to interrupt'})
				</Text>
			</Box>
		</Box>
	);
}

// Hook for managing thinking state across the application
export function useThinkingState(initialContext: string[] = []) {
	const [isThinking, setIsThinking] = useState(false);
	const [conversationContext, setConversationContext] = useState<string[]>(initialContext);

	const startThinking = useCallback((newContext?: string[]) => {
		if (newContext) {
			setConversationContext(prev => [...prev, ...newContext]);
		}
		setIsThinking(true);
	}, []);

	const stopThinking = useCallback(() => {
		setIsThinking(false);
	}, []);

	const addToContext = useCallback((message: string) => {
		setConversationContext(prev => [...prev.slice(-10), message]); // Keep last 10 messages
	}, []);

	const interrupt = useCallback(() => {
		setIsThinking(false);
		// Could emit event to Python backend here
		console.log('AI thinking interrupted by user');
	}, []);

	return {
		isThinking,
		conversationContext,
		startThinking,
		stopThinking,
		addToContext,
		interrupt
	};
}

// Context manager for intelligent word selection
export class ThinkingWordGenerator {
	private static recentWords: string[] = [];
	
	/**
	 * Generate unique contextual word that user has virtually never seen before
	 */
	static generateUniqueWord(conversationContext: string[]): string {
		const availableWords = this.getAllWords();
		
		// Filter out recently used words
		const freshWords = availableWords.filter(word => !this.recentWords.includes(word));
		
		if (freshWords.length === 0) {
			// Reset if we've used all words
			this.recentWords = [];
			return this.selectContextualWord(conversationContext, availableWords);
		}
		
		const selectedWord = this.selectContextualWord(conversationContext, freshWords);
		
		// Track usage
		this.recentWords.push(selectedWord);
		if (this.recentWords.length > 20) {
			this.recentWords = this.recentWords.slice(-10); // Keep last 10
		}
		
		return selectedWord;
	}
	
	private static getAllWords(): string[] {
		return Object.values(CONTEXTUAL_WORDS).flat();
	}
	
	private static selectContextualWord(context: string[], availableWords: string[]): string {
		const recentMessages = context.slice(-3).join(' ').toLowerCase();
		
		// Same logic as generateContextualWord but with available words filter
		for (const [category, words] of Object.entries(CONTEXTUAL_WORDS)) {
			const categoryWords = words.filter(word => availableWords.includes(word));
			if (categoryWords.length === 0) continue;
			
			if (this.contextMatchesCategory(recentMessages, category)) {
				const selectedWord = categoryWords[Math.floor(Math.random() * categoryWords.length)];
				return selectedWord || availableWords[0] || 'Thinking';
			}
		}
		
		// Fallback to any available word
		return availableWords[Math.floor(Math.random() * availableWords.length)] || 'Thinking';
	}
	
	private static contextMatchesCategory(context: string, category: string): boolean {
		const patterns: Record<string, string[]> = {
			budget: ['cost', 'budget', 'price', 'money'],
			workflow: ['workflow', 'orchestrat', 'plan', 'process'],
			analysis: ['analyz', 'review', 'assess', 'evaluat'],
			creative: ['creat', 'design', 'idea', 'innovat'],
			technical: ['config', 'setup', 'technical', 'system'],
			research: ['research', 'find', 'search', 'investigat'],
			writing: ['writ', 'compos', 'draft', 'content'],
			problem_solving: ['problem', 'issue', 'fix', 'troubl'],
			celebration: ['great', 'awesome', 'perfect', 'excellent'],
			greeting: ['hello', 'hi', 'start', 'begin']
		};
		
		const categoryPatterns = patterns[category];
		if (!categoryPatterns) return false;
		
		return categoryPatterns.some(pattern => context.includes(pattern));
	}
}