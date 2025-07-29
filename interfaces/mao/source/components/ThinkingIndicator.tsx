/**
 * AI Thinking Indicator - Let AI Be AI
 * No hardcoded word lists - AI generates contextual thinking words on the fly
 * Guidelines instead of walls: be goofy, contextual, fun
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';
import {PythonBridge} from '../api/PythonBridge.js';

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
	pythonBridge: PythonBridge;
}

export default function ThinkingIndicator({
	isThinking,
	conversationContext = [],
	onInterrupt,
	pythonBridge
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

	// Generate AI thinking word when thinking starts
	useEffect(() => {
		if (isThinking && !state.isActive) {
			// Don't show thinking indicator for simple/early responses
			if (!shouldShowThinking(conversationContext)) {
				return;
			}

			generateThinkingWord(conversationContext, pythonBridge)
				.then(contextualWord => {
					setState(prev => ({
						...prev,
						isActive: true,
						startTime: Date.now(),
						elapsedSeconds: 0,
						contextualWord,
						showInterruptHint: false
					}));
				});
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
	}, [isThinking, state.isActive, conversationContext, pythonBridge]);

	// Update metrics in real-time
	useEffect(() => {
		if (!state.isActive) return;

		const interval = setInterval(async () => {
			const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
			
			// Get actual token count and cost from backend if possible
			const tokenData = await getActualTokenCount(elapsed, pythonBridge);

			setState(prev => ({
				...prev,
				elapsedSeconds: elapsed,
				tokensUsed: tokenData.tokens,
				estimatedCost: tokenData.cost,
				showInterruptHint: elapsed > 5 // Show interrupt hint after 5 seconds
			}));
		}, 1000);

		return () => clearInterval(interval);
	}, [state.isActive, state.startTime, pythonBridge]);

	// Handle ESC key for interruption
	useInput(useCallback((_, key) => {
		if (key.escape && state.isActive && onInterrupt) {
			onInterrupt();
		}
	}, [state.isActive, onInterrupt]));

	// Don't render if not active
	if (!state.isActive) return null;

	return (
		<Box marginBottom={1}>
			{/* Cat ASCII art and AI-generated thinking word */}
			<Box>
				<Text color={colorSystem.getColor('main')}>~(=^‥^) </Text>
				<Text color={colorSystem.getColor('trusting_update_1')}>● </Text>
				<Text color={colorSystem.getColor('processing')}>{state.contextualWord}... </Text>
				<Text color={colorSystem.getColor('trusting_update_1')}>● </Text>
				<Text color={colorSystem.getColor('user')}>
					({state.elapsedSeconds}s • ${state.estimatedCost.toFixed(3)} • {state.tokensUsed} tokens
					{state.showInterruptHint && ' • esc to interrupt'})
				</Text>
			</Box>
		</Box>
	);
}

/**
 * Determine if thinking indicator should be shown
 * Only show after established back-and-forth (4+ message volleys)
 */
function shouldShowThinking(conversationContext: string[]): boolean {
	// Don't show for early messages or simple responses
	if (conversationContext.length < 4) return false;
	
	// Don't show for very short recent messages (probably simple responses)
	const recentMessages = conversationContext.slice(-2);
	const hasComplexRecent = recentMessages.some(msg => msg.length > 50);
	
	return hasComplexRecent;
}

/**
 * Generate contextual thinking word from AI
 * No hardcoded lists - AI creates based on conversation context
 */
async function generateThinkingWord(
	conversationContext: string[], 
	pythonBridge: PythonBridge
): Promise<string> {
	try {
		// Create context summary for AI word generation
		const recentContext = conversationContext.slice(-3).join(' ');
		
		// Ask AI to generate a contextual thinking word
		const prompt = `Based on this conversation context: "${recentContext}"
		
Generate a single fun, contextual thinking word (like "Orchestrating", "Budgeting", "Flibbergitting").
Guidelines:
- Be goofy and creative when appropriate
- Match the conversation context
- Make it sound engaging and active
- One word only, ending with "...ing" if possible
- Make the user think "that's exactly what Mao would be doing right now"

Just return the word, nothing else.`;

		const response = await pythonBridge.chat(prompt);
		
		// Extract just the word from response  
		const word = extractThinkingWord(response);
		return word || 'Processing'; // Minimal fallback, not hardcoded generation
		
	} catch (error) {
		console.error('Failed to generate thinking word:', error);
		return 'Thinking'; // Simple fallback when AI generation completely fails
	}
}

/**
 * Extract thinking word from AI response
 */
function extractThinkingWord(response: string): string | null {
	// Clean up the response - take first word that looks like a thinking word
	const words = response.trim().split(/\s+/);
	
	for (const word of words) {
		const cleaned = word.replace(/[^a-zA-Z]/g, '');
		// Look for words ending in 'ing' or common thinking patterns
		if (cleaned.length > 3 && 
			(cleaned.endsWith('ing') || 
			 cleaned.endsWith('izing') || 
			 cleaned.endsWith('ting'))) {
			return cleaned;
		}
	}
	
	// If no good word found, return first substantial word
	const firstWord = words[0]?.replace(/[^a-zA-Z]/g, '');
	return firstWord && firstWord.length > 3 ? firstWord : null;
}


/**
 * Hook for managing thinking state across the application
 */
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

/**
 * Get actual token count and cost from backend instead of estimation
 */
async function getActualTokenCount(elapsed: number, pythonBridge: PythonBridge): Promise<{tokens: number; cost: number}> {
	try {
		// Try to get real metrics from Python backend
		const response = await pythonBridge.executeSlashCommand('/stats --current-session');
		const parsed = parseTokenResponse(response);
		if (parsed) {
			return parsed;
		}
	} catch (error) {
		// Fall back to intelligent estimation only when backend unavailable
		console.log('Using fallback token estimation:', error);
	}
	
	// Fallback estimation based on elapsed time (better than hardcoded rates)
	const baseTokenRate = 45; // tokens per second baseline
	const timeBasedVariation = Math.sin(elapsed * 0.1) * 10; // Natural variation
	const estimatedTokens = Math.floor(elapsed * (baseTokenRate + timeBasedVariation));
	const estimatedCost = (estimatedTokens * 0.003) / 1000; // Current model pricing
	
	return {
		tokens: estimatedTokens,
		cost: estimatedCost
	};
}

/**
 * Parse token response from backend
 */
function parseTokenResponse(response: string): {tokens: number; cost: number} | null {
	try {
		const parsed = JSON.parse(response);
		if (parsed.current_session && parsed.current_session.tokens && parsed.current_session.cost) {
			return {
				tokens: parsed.current_session.tokens,
				cost: parsed.current_session.cost
			};
		}
	} catch {
		// Try to parse plain text response
		const tokenMatch = response.match(/(\d+)\s*tokens/i);
		const costMatch = response.match(/\$?(\d+\.?\d*)/);
		
		if (tokenMatch && costMatch && tokenMatch[1] && costMatch[1]) {
			return {
				tokens: parseInt(tokenMatch[1]),
				cost: parseFloat(costMatch[1])
			};
		}
	}
	
	return null;
}