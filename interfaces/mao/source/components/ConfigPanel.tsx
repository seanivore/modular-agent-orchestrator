/**
 * Configuration Panel - Claude Code-style modal config panel
 * Triggered by /config command, nudges input field up to make room
 * Uses space bar for simple toggles, enter for complex settings like themes
 */

import React, {useState, useCallback, useEffect} from 'react';
import {Box, Text, useInput} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';
import {PythonBridge} from '../api/PythonBridge.js';

interface ConfigOption {
	key: string;
	label: string;
	type: 'toggle' | 'select' | 'input';
	value: any;
	options?: string[];
	description?: string;
}

interface ConfigPanelProps {
	isOpen: boolean;
	onClose: () => void;
	pythonBridge: PythonBridge;
}

export default function ConfigPanel({isOpen, onClose, pythonBridge}: ConfigPanelProps) {
	const [currentSection, setCurrentSection] = useState<'main' | 'themes'>('main');
	const [selectedIndex, setSelectedIndex] = useState(0);
	const [configOptions, setConfigOptions] = useState<ConfigOption[]>([]);
	const [isLoading, setIsLoading] = useState(true);

	// Load configuration options dynamically from backend
	useEffect(() => {
		if (isOpen) {
			loadConfigOptions();
		}
	}, [isOpen]);

	const loadConfigOptions = useCallback(async () => {
		try {
			setIsLoading(true);
			const response = await pythonBridge.executeSlashCommand('/config --list-options');
			const options = parseConfigOptions(response);
			setConfigOptions(options);
		} catch (error) {
			// No fallback options - wait for backend connection
			setConfigOptions([]);
		} finally {
			setIsLoading(false);
		}
	}, [pythonBridge]);

	// Handle keyboard navigation
	useInput(useCallback((inputChar, key) => {
		if (!isOpen) return;

		if (currentSection === 'main') {
			if (key.upArrow) {
				setSelectedIndex(prev => Math.max(0, prev - 1));
			} else if (key.downArrow) {
				setSelectedIndex(prev => Math.min(configOptions.length - 1, prev + 1));
			} else if (key.return) {
				const selected = configOptions[selectedIndex];
				if (selected?.type === 'select' && selected.key === 'theme') {
					setCurrentSection('themes');
					setSelectedIndex(0);
				} else if (selected?.type === 'toggle') {
					toggleOption(selected.key);
				}
			} else if (inputChar === ' ') {
				const selected = configOptions[selectedIndex];
				if (selected?.type === 'toggle') {
					toggleOption(selected.key);
				}
			} else if (key.escape) {
				onClose();
			}
		} else if (currentSection === 'themes') {
			const themes = colorSystem.getAvailableThemes();
			if (key.upArrow) {
				setSelectedIndex(prev => Math.max(0, prev - 1));
			} else if (key.downArrow) {
				setSelectedIndex(prev => Math.min(themes.length - 1, prev + 1));
			} else if (key.return || inputChar === ' ') {
				const selectedTheme = themes[selectedIndex];
				if (selectedTheme) {
					selectTheme(selectedTheme);
					setCurrentSection('main');
					setSelectedIndex(0);
				}
			} else if (key.escape) {
				setCurrentSection('main');
				setSelectedIndex(0);
			}
		}
	}, [isOpen, currentSection, selectedIndex, configOptions, onClose]));

	const toggleOption = useCallback(async (optionKey: string) => {
		try {
			await pythonBridge.executeSlashCommand(`/config --set ${optionKey}`);
			// Reload options to get updated values
			await loadConfigOptions();
		} catch (error) {
			console.error('Failed to toggle config option:', error);
		}
	}, [pythonBridge, loadConfigOptions]);

	const selectTheme = useCallback(async (themeName: string) => {
		try {
			colorSystem.setTheme(themeName);
			await pythonBridge.executeSlashCommand(`/config --set theme="${themeName}"`);
		} catch (error) {
			console.error('Failed to set theme:', error);
		}
	}, [pythonBridge]);

	if (!isOpen) return null;

	if (isLoading) {
		return (
			<Box
				borderStyle="round"
				borderColor={colorSystem.getColor('trusting_update_1')}
				padding={1}
				marginBottom={1}
			>
				<Text color={colorSystem.getColor('main')}>Loading configuration...</Text>
			</Box>
		);
	}

	if (currentSection === 'themes') {
		return renderThemeSelection();
	}

	return renderMainConfig();

	function renderMainConfig(): React.ReactNode {
		return (
		<Box
			borderStyle="round"
			borderColor={colorSystem.getColor('trusting_update_1')}
			padding={1}
			marginBottom={1}
			flexDirection="column"
		>
			<Box marginBottom={1}>
				<Text color={colorSystem.getColor('bold')} bold>Configuration</Text>
				<Text color={colorSystem.getColor('supplemental_2')}> • ESC to close</Text>
			</Box>

			{configOptions.map((option, idx) => (
				<Box key={option.key} marginBottom={0}>
					<Text 
						color={idx === selectedIndex ? 
							colorSystem.getColor('bold') : 
							colorSystem.getColor('main')
						}
						bold={idx === selectedIndex}
					>
						{idx === selectedIndex ? '► ' : '  '}
						{option.label}
					</Text>
					
					{option.type === 'toggle' && (
						<Text color={colorSystem.getColor('trusting_update_2')}>
							{' '}[{option.value ? 'ON' : 'OFF'}]
						</Text>
					)}
					
					{option.type === 'select' && option.key === 'theme' && (
						<Text color={colorSystem.getColor('trusting_update_2')}>
							{' '}[{colorSystem.getCurrentTheme()}] →
						</Text>
					)}
				</Box>
			))}

			<Box marginTop={1}>
				<Text color={colorSystem.getColor('supplemental_2')}>
					Space: toggle • Enter: select • ↑↓: navigate
				</Text>
			</Box>
		</Box>
	);
}

	function renderThemeSelection(): React.ReactNode {
		const themes = colorSystem.getAvailableThemes();
		const themeNames = colorSystem.getThemeDisplayNames();

		return (
		<Box
			borderStyle="round"
			borderColor={colorSystem.getColor('trusting_update_1')}
			padding={1}
			marginBottom={1}
			flexDirection="column"
		>
			<Box marginBottom={1}>
				<Text color={colorSystem.getColor('bold')} bold>Select Theme</Text>
				<Text color={colorSystem.getColor('supplemental_2')}> • ESC to go back</Text>
			</Box>

			{themes.map((theme, idx) => (
				<Box key={theme} marginBottom={0}>
					<Text 
						color={idx === selectedIndex ? 
							colorSystem.getColor('bold') : 
							colorSystem.getColor('main')
						}
						bold={idx === selectedIndex}
					>
						{idx === selectedIndex ? '► ' : '  '}
						{themeNames[theme] || theme}
					</Text>
					
					{theme === colorSystem.getCurrentTheme() && (
						<Text color={colorSystem.getColor('trusting_update_1')}>
							{' '}(current)
						</Text>
					)}
				</Box>
			))}

			<Box marginTop={1}>
				<Text color={colorSystem.getColor('supplemental_2')}>
					Enter/Space: select • ↑↓: navigate • ESC: back
				</Text>
			</Box>
		</Box>
	);
}

/**
 * Parse configuration options from backend response
 */
function parseConfigOptions(response: string): ConfigOption[] {
	try {
		const parsed = JSON.parse(response);
		if (parsed.options && Array.isArray(parsed.options)) {
			return parsed.options;
		}
	} catch {
		// Fall back to text parsing
		return parseTextConfigOptions(response);
	}
	
	return [];
}

/**
 * Parse text-based config response
 */
function parseTextConfigOptions(response: string): ConfigOption[] {
	const options: ConfigOption[] = [];
	const lines = response.split('\n');
	
	for (const line of lines) {
		const match = line.trim().match(/^(\w+):\s*(.+)$/);
		if (match && match[1] && match[2]) {
			options.push({
				key: match[1],
				label: match[1].replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
				type: 'toggle',
				value: match[2].toLowerCase() === 'true'
			});
		}
	}
	
	return options;
}
}

