/**
 * Command Autocomplete - Claude Code-style terminal autocomplete
 * Dynamically discovers commands from Python backend CLI system
 * No hardcoded command lists - everything discovered at runtime
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';
import {PythonBridge} from '../api/PythonBridge.js';

interface Command {
	name: string;
	description: string;
	usage?: string;
	type: 'cli' | 'recent';
}

interface AutocompleteProps {
	isActive: boolean;
	input: string;
	onSelect: (command: string) => void;
	onClose: () => void;
	pythonBridge: PythonBridge;
}

interface AutocompleteState {
	availableCommands: Command[];
	filteredCommands: Command[];
	selectedIndex: number;
	isLoading: boolean;
}

export default function CommandAutocomplete({
	isActive,
	input,
	onSelect,
	onClose,
	pythonBridge
}: AutocompleteProps) {
	const [state, setState] = useState<AutocompleteState>({
		availableCommands: [],
		filteredCommands: [],
		selectedIndex: 0,
		isLoading: true
	});

	// Discover available commands from Python backend
	const discoverCommands = useCallback(async () => {
		try {
			setState(prev => ({...prev, isLoading: true}));
			
			// Request command discovery from Python backend
			const response = await pythonBridge.executeSlashCommand('/help --list-commands');
			const commands = parseCommandsFromResponse(response);
			
			setState(prev => ({
				...prev,
				availableCommands: commands,
				isLoading: false
			}));
		} catch (error) {
			console.error('Failed to discover commands:', error);
			
			// No fallback commands - wait for backend connection
			setState(prev => ({
				...prev,
				availableCommands: [],
				isLoading: false
			}));
		}
	}, [pythonBridge]);

	// Initialize command discovery
	useEffect(() => {
		if (isActive && state.availableCommands.length === 0) {
			discoverCommands();
		}
	}, [isActive, discoverCommands, state.availableCommands.length]);

	// Filter commands based on input
	useEffect(() => {
		if (!input.startsWith('/')) {
			setState(prev => ({...prev, filteredCommands: [], selectedIndex: 0}));
			return;
		}

		const searchTerm = input.slice(1).toLowerCase(); // Remove '/' prefix
		const filtered = state.availableCommands.filter(cmd =>
			cmd.name.slice(1).toLowerCase().includes(searchTerm) ||
			cmd.description.toLowerCase().includes(searchTerm)
		);

		// Sort by relevance - exact matches first, then starts-with, then contains
		filtered.sort((a, b) => {
			const aName = a.name.slice(1).toLowerCase();
			const bName = b.name.slice(1).toLowerCase();
			
			if (aName === searchTerm) return -1;
			if (bName === searchTerm) return 1;
			if (aName.startsWith(searchTerm)) return -1;
			if (bName.startsWith(searchTerm)) return 1;
			return 0;
		});

		setState(prev => ({
			...prev,
			filteredCommands: filtered,
			selectedIndex: 0
		}));
	}, [input, state.availableCommands]);

	// Handle keyboard navigation
	useInput(useCallback((inputChar, key) => {
		if (!isActive || state.isLoading) return;

		if (key.upArrow) {
			setState(prev => ({
				...prev,
				selectedIndex: Math.max(0, prev.selectedIndex - 1)
			}));
		} else if (key.downArrow) {
			setState(prev => ({
				...prev,
				selectedIndex: Math.min(prev.filteredCommands.length - 1, prev.selectedIndex + 1)
			}));
		} else if (key.return || key.tab) {
			if (state.filteredCommands[state.selectedIndex]) {
				onSelect(state.filteredCommands[state.selectedIndex].name);
			}
		} else if (key.escape) {
			onClose();
		}
	}, [isActive, state, onSelect, onClose]));

	// Don't render if not active or no commands to show
	if (!isActive || state.isLoading) {
		return null;
	}

	if (state.filteredCommands.length === 0) {
		return null;
	}

	return (
		<Box 
			flexDirection="column" 
			marginTop={1}
			borderStyle="round"
			borderColor={colorSystem.getColor('trusting_update_1')}
			paddingX={1}
		>
			{state.filteredCommands.slice(0, 8).map((command, idx) => (
				<Box key={command.name}>
					<Text 
						color={idx === state.selectedIndex ? 
							colorSystem.getColor('bold') : 
							colorSystem.getColor('main')
						}
						bold={idx === state.selectedIndex}
					>
						{command.name}
					</Text>
					<Text color={colorSystem.getColor('supplemental_2')}>
						{' - ' + command.description}
					</Text>
				</Box>
			))}
			
			{state.filteredCommands.length > 8 && (
				<Box marginTop={1}>
					<Text color={colorSystem.getColor('supplemental_2')}>
						... +{state.filteredCommands.length - 8} more commands
					</Text>
				</Box>
			)}
		</Box>
	);
}

/**
 * Parse commands from Python backend response
 * Expects JSON format with command list
 */
function parseCommandsFromResponse(response: string): Command[] {
	try {
		// Try to parse as JSON first
		const parsed = JSON.parse(response);
		if (parsed.commands && Array.isArray(parsed.commands)) {
			return parsed.commands.map((cmd: any) => ({
				name: cmd.name,
				description: cmd.description || cmd.help || 'No description available',
				usage: cmd.usage,
				type: 'cli' as const
			}));
		}
	} catch {
		// Fall back to parsing text response
		return parseTextCommandList(response);
	}
	
	return [];
}

/**
 * Parse commands from text response (fallback)
 */
function parseTextCommandList(response: string): Command[] {
	const commands: Command[] = [];
	const lines = response.split('\n');
	
	for (const line of lines) {
		// Look for patterns like "/command - description"
		const match = line.trim().match(/^(\/\w+)\s*-\s*(.+)$/);
		if (match) {
			commands.push({
				name: match[1],
				description: match[2],
				type: 'cli'
			});
		}
	}
	
	return commands;
}

