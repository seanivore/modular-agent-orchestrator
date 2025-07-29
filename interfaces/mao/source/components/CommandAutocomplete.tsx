/**
 * Command Autocomplete - Claude Code-style terminal autocomplete
 * Implements space management, CLI discovery, and terminal-native navigation
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';

interface Command {
	name: string;
	description: string;
	usage?: string;
	type: 'builtin' | 'cli' | 'recent';
}

interface AutocompleteProps {
	isActive: boolean;
	input: string;
	onSelect: (command: string) => void;
	onClose: () => void;
	availableCommands?: Command[];
}

interface AutocompleteState {
	filteredCommands: Command[];
	selectedIndex: number;
	isVisible: boolean;
}

// Built-in commands as specified
const BUILTIN_COMMANDS: Command[] = [
	{
		name: '/config',
		description: 'Configure Mao preferences and settings',
		usage: '/config [setting]',
		type: 'builtin'
	},
	{
		name: '/help',
		description: 'Show available commands and usage information',
		usage: '/help [command]',
		type: 'builtin'
	},
	{
		name: '/stats',
		description: 'Display system statistics and metrics',
		usage: '/stats [type]',
		type: 'builtin'
	},
	{
		name: '/goal',
		description: 'Create and manage workflow goals',
		usage: '/goal "description"',
		type: 'builtin'
	},
	{
		name: '/memory',
		description: 'Store and retrieve memories',
		usage: '/memory "content" or /memory --list',
		type: 'builtin'
	},
	{
		name: '/theme',
		description: 'Change visual theme',
		usage: '/theme [theme_name]',
		type: 'builtin'
	}
];

export default function CommandAutocomplete({
	isActive,
	input,
	onSelect,
	onClose,
	availableCommands = []
}: AutocompleteProps) {
	const [state, setState] = useState<AutocompleteState>({
		filteredCommands: [],
		selectedIndex: 0,
		isVisible: false
	});

	// Filter commands based on input
	useEffect(() => {
		if (!isActive || !input.startsWith('/')) {
			setState(prev => ({ ...prev, isVisible: false }));
			return;
		}

		const query = input.slice(1).toLowerCase(); // Remove '/' and lowercase
		
		// Combine all available commands
		const allCommands = [
			...BUILTIN_COMMANDS,
			...availableCommands
		];

		// Filter and sort by relevance
		const filtered = allCommands
			.filter(cmd => cmd.name.toLowerCase().includes(query))
			.sort((a, b) => {
				// Prioritize exact matches
				const aExact = a.name.toLowerCase().startsWith(`/${query}`);
				const bExact = b.name.toLowerCase().startsWith(`/${query}`);
				
				if (aExact && !bExact) return -1;
				if (!aExact && bExact) return 1;
				
				// Then by type (builtin first)
				if (a.type === 'builtin' && b.type !== 'builtin') return -1;
				if (a.type !== 'builtin' && b.type === 'builtin') return 1;
				
				// Finally alphabetically
				return a.name.localeCompare(b.name);
			})
			.slice(0, 8); // Limit to 8 suggestions

		setState(prev => ({
			...prev,
			filteredCommands: filtered,
			selectedIndex: Math.min(prev.selectedIndex, filtered.length - 1),
			isVisible: filtered.length > 0
		}));
	}, [isActive, input, availableCommands]);

	// Handle keyboard navigation
	useInput(useCallback((inputChar, key) => {
		if (!state.isVisible) return;

		if (key.upArrow) {
			setState(prev => ({
				...prev,
				selectedIndex: prev.selectedIndex > 0 ? prev.selectedIndex - 1 : prev.filteredCommands.length - 1
			}));
		} else if (key.downArrow) {
			setState(prev => ({
				...prev,
				selectedIndex: prev.selectedIndex < prev.filteredCommands.length - 1 ? prev.selectedIndex + 1 : 0
			}));
		} else if (key.return || key.tab) {
			const selectedCommand = state.filteredCommands[state.selectedIndex];
			if (selectedCommand) {
				onSelect(selectedCommand.name);
			}
		} else if (key.escape) {
			onClose();
		}
	}, [state.isVisible, state.selectedIndex, state.filteredCommands, onSelect, onClose]));

	// Don't render if not visible
	if (!state.isVisible) return null;

	return (
		<Box 
			flexDirection="column" 
			borderStyle="round"
			borderColor={colorSystem.getColor('trusting_update_1')}
			padding={1}
			marginBottom={1}
		>
			{/* Header */}
			<Box marginBottom={1}>
				<Text color={colorSystem.getColor('supplemental_2')}>
					Commands ({state.filteredCommands.length})
				</Text>
			</Box>

			{/* Command suggestions */}
			{state.filteredCommands.map((command, index) => (
				<CommandSuggestion
					key={command.name}
					command={command}
					isSelected={index === state.selectedIndex}
				/>
			))}

			{/* Navigation hint */}
			<Box marginTop={1} borderStyle="single" borderColor={colorSystem.getColor('dark_supplemental')}>
				<Text color={colorSystem.getColor('supplemental_2')}>
					↑↓ navigate • enter/tab select • esc close
				</Text>
			</Box>
		</Box>
	);
}

interface CommandSuggestionProps {
	command: Command;
	isSelected: boolean;
}

function CommandSuggestion({ command, isSelected }: CommandSuggestionProps) {
	const bgColor = isSelected ? colorSystem.getColor('dark_supplemental') : undefined;
	const textColor = isSelected ? colorSystem.getColor('bold') : colorSystem.getColor('main');
	const descColor = colorSystem.getColor('supplemental_2');

	return (
		<Box backgroundColor={bgColor} paddingX={1}>
			<Box width={16}>
				<Text color={textColor} bold={isSelected}>
					{command.name}
				</Text>
			</Box>
			<Box flexGrow={1}>
				<Text color={descColor}>
					{command.description}
				</Text>
			</Box>
			{command.type !== 'builtin' && (
				<Box>
					<Text color={colorSystem.getColor('accent_outside')}>
						{command.type}
					</Text>
				</Box>
			)}
		</Box>
	);
}

// Hook for managing autocomplete state
export function useCommandAutocomplete() {
	const [isActive, setIsActive] = useState(false);
	const [availableCommands, setAvailableCommands] = useState<Command[]>([]);

	const activate = useCallback(() => {
		setIsActive(true);
	}, []);

	const deactivate = useCallback(() => {
		setIsActive(false);
	}, []);

	const updateCommands = useCallback((commands: Command[]) => {
		setAvailableCommands(commands);
	}, []);

	// Discover CLI commands dynamically
	const discoverCliCommands = useCallback(async (): Promise<Command[]> => {
		try {
			// This would integrate with the Python backend's CLI discovery
			// For now, return mock commands
			return [
				{
					name: '/audit',
					description: 'Run system audit',
					type: 'cli'
				},
				{
					name: '/workflows', 
					description: 'Manage workflows',
					type: 'cli'
				},
				{
					name: '/tools',
					description: 'List available tools',
					type: 'cli'
				}
			];
		} catch (error) {
			console.error('Failed to discover CLI commands:', error);
			return [];
		}
	}, []);

	// Load commands on initialization
	useEffect(() => {
		discoverCliCommands().then(updateCommands);
	}, [discoverCliCommands, updateCommands]);

	return {
		isActive,
		availableCommands,
		activate,
		deactivate,
		updateCommands,
		discoverCliCommands
	};
}

// Command history management for up-arrow functionality
export class CommandHistory {
	private static commands: string[] = [];
	private static currentIndex = -1;

	static addCommand(command: string): void {
		// Don't add duplicates
		if (this.commands[this.commands.length - 1] !== command) {
			this.commands.push(command);
			
			// Limit history size
			if (this.commands.length > 50) {
				this.commands = this.commands.slice(-50);
			}
		}
		
		this.currentIndex = -1; // Reset index
	}

	static getPreviousCommand(): string | null {
		if (this.commands.length === 0) return null;
		
		if (this.currentIndex === -1) {
			this.currentIndex = this.commands.length - 1;
		} else if (this.currentIndex > 0) {
			this.currentIndex--;
		}
		
		return this.commands[this.currentIndex] || null;
	}

	static getNextCommand(): string | null {
		if (this.currentIndex === -1 || this.currentIndex >= this.commands.length - 1) {
			this.currentIndex = -1;
			return '';
		}
		
		this.currentIndex++;
		return this.commands[this.currentIndex] || null;
	}

	static getRecentCommands(limit = 5): Command[] {
		return this.commands
			.slice(-limit)
			.reverse()
			.map(cmd => ({
				name: cmd,
				description: 'Recent command',
				type: 'recent' as const
			}));
	}

	static reset(): void {
		this.currentIndex = -1;
	}
}

// Integration with space management for Claude Code-style behavior
export function useSpaceManagement(isAutocompleteActive: boolean) {
	const [spaceReserved, setSpaceReserved] = useState(false);

	useEffect(() => {
		setSpaceReserved(isAutocompleteActive);
	}, [isAutocompleteActive]);

	return {
		spaceReserved,
		reservedHeight: spaceReserved ? 10 : 0 // Reserve space for autocomplete panel
	};
}