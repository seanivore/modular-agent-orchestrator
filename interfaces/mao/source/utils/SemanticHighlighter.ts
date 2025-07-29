// Semantic Highlighter - 6-Color System for Terminal-Native Design
// Based on PHASE_1_REVISED_ENHANCEMENTS.md specification

interface ColorTheme {
	mainHighlight: string;      // MAIN HIGHLIGHT COLOR (pink/bold)
	systemText: string;         // SYSTEM TEXT COLOR (yellow)  
	fadedSystemText: string;    // FADED SYSTEM TEXT COLOR (dimmed yellow)
	lightGray: string;          // LIGHT GRAY TEXT (neutral secondary)
	superLightBlue: string;     // SUPER LIGHT BLUE ALMOST WHITE (subtle accents)
	babyBlueDarker: string;     // BABY BLUE DARKER VERSION (stronger blue accents)
}

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
	private static currentTheme: ColorTheme = {
		// Dark Mode (current implementation) - fallback defaults
		mainHighlight: '#ff49ff',      // Pink - AI actions (BOLD only)
		systemText: '#f1d771',         // Yellow - AI explanations and conversation  
		fadedSystemText: '#d4c666',    // Dimmed yellow
		lightGray: '#bbbcbb',          // Gray - User input and secondary info
		superLightBlue: '#f0f8ff',     // Almost white blue - Subtle accents
		babyBlueDarker: '#82d0ff'      // Light blue - Highlighted items and recommendations
	};

	/**
	 * Get styling configuration for specific message type and user type
	 */
	static getMessageStyling(messageType: MessageType, userType: UserType): MessageStyling {
		const theme = this.currentTheme;
		
		if (userType === 'user') {
			return {
				borderColor: theme.lightGray,
				prefixColor: theme.lightGray,
				textColor: theme.lightGray,
				bulletColor: theme.lightGray,
				numberColor: theme.lightGray,
				actionColor: theme.lightGray,
				pastedIndicatorColor: theme.fadedSystemText,
				errorColor: '#ff6b6b', // Red for user errors
				expansionColor: theme.fadedSystemText
			};
		}

		// Mao (AI) message styling - varies by message type
		switch (messageType) {
			case 'conversational':
				return {
					borderColor: theme.systemText,
					prefixColor: theme.systemText,
					textColor: theme.systemText,
					bulletColor: theme.mainHighlight,
					numberColor: theme.systemText,
					actionColor: theme.systemText,
					pastedIndicatorColor: theme.fadedSystemText,
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			case 'bullet_list':
				return {
					borderColor: theme.systemText,
					prefixColor: theme.systemText,
					textColor: theme.systemText,
					bulletColor: theme.mainHighlight, // Pink bullets for emphasis
					numberColor: theme.systemText,
					actionColor: theme.systemText,
					pastedIndicatorColor: theme.fadedSystemText,
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			case 'numbered_list':
				return {
					borderColor: theme.systemText,
					prefixColor: theme.systemText,
					textColor: theme.systemText,
					bulletColor: theme.systemText,
					numberColor: theme.systemText, // Yellow throughout for numbered lists
					actionColor: theme.systemText,
					pastedIndicatorColor: theme.fadedSystemText,
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			case 'action_list':
				return {
					borderColor: theme.babyBlueDarker,
					prefixColor: theme.systemText,
					textColor: theme.babyBlueDarker,
					bulletColor: theme.mainHighlight,
					numberColor: theme.babyBlueDarker,
					actionColor: theme.babyBlueDarker, // Blue for action items
					pastedIndicatorColor: theme.fadedSystemText,
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			case 'pasted_text':
				return {
					borderColor: theme.fadedSystemText,
					prefixColor: theme.systemText,
					textColor: theme.fadedSystemText,
					bulletColor: theme.fadedSystemText,
					numberColor: theme.fadedSystemText,
					actionColor: theme.fadedSystemText,
					pastedIndicatorColor: theme.fadedSystemText, // Dimmed for paste indicators
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			case 'error':
				return {
					borderColor: '#ff6b6b',
					prefixColor: theme.systemText,
					textColor: '#ff6b6b', // Red for errors
					bulletColor: '#ff6b6b',
					numberColor: '#ff6b6b',
					actionColor: '#ff6b6b',
					pastedIndicatorColor: '#ff6b6b',
					errorColor: '#ff6b6b',
					expansionColor: theme.fadedSystemText
				};

			default:
				return this.getMessageStyling('conversational', userType);
		}
	}

	/**
	 * Apply semantic highlighting to content based on message type
	 */
	static highlightContent(content: string, messageType: MessageType): string {
		switch (messageType) {
			case 'conversational':
				return this.highlightConversationalContent(content);
			case 'bullet_list':
				return this.highlightBulletContent(content);
			case 'numbered_list':
				return this.highlightNumberedContent(content);
			case 'action_list':
				return this.highlightActionContent(content);
			case 'error':
				return this.highlightErrorContent(content);
			default:
				return content;
		}
	}

	private static highlightConversationalContent(content: string): string {
		// Highlight URLs in SUPER LIGHT BLUE
		let highlighted = content.replace(
			/(https?:\/\/[^\s]+)/g, 
			`\x1b[38;2;240;248;255m$1\x1b[0m` // Super light blue
		);

		// Highlight first few words in MAIN HIGHLIGHT COLOR (pink/bold)
		const words = highlighted.split(' ');
		if (words.length > 0) {
			const firstWords = words.slice(0, 3).join(' ');
			const restWords = words.slice(3).join(' ');
			highlighted = `\x1b[38;2;255;73;255m\x1b[1m${firstWords}\x1b[0m${restWords ? ' ' + restWords : ''}`;
		}

		return highlighted;
	}

	private static highlightBulletContent(content: string): string {
		// Remove bullet point and apply first-word highlighting
		const cleanContent = content.replace(/^[-•*]\s/, '');
		return this.highlightConversationalContent(cleanContent);
	}

	private static highlightNumberedContent(content: string): string {
		// Numbered lists use SYSTEM TEXT COLOR throughout - no special highlighting
		return content;
	}

	private static highlightActionContent(content: string): string {
		// Highlight task indicators and file paths
		let highlighted = content;

		// Highlight circles and triangles
		highlighted = highlighted.replace(
			/([○●▶︎▷])/g,
			`\x1b[38;2;255;73;255m$1\x1b[0m` // Pink for task indicators
		);

		// Highlight file paths
		highlighted = highlighted.replace(
			/(\/[^\s]+\.[a-zA-Z]+)/g,
			`\x1b[38;2;240;248;255m$1\x1b[0m` // Super light blue for file paths
		);

		return highlighted;
	}

	private static highlightErrorContent(content: string): string {
		// Error messages - keep simple red coloring
		return content;
	}

	/**
	 * Update theme (for dynamic theme switching)
	 */
	static updateTheme(newTheme: Partial<ColorTheme>): void {
		this.currentTheme = { ...this.currentTheme, ...newTheme };
	}

	/**
	 * Detect user's terminal theme (future implementation)
	 */
	static detectTerminalTheme(): 'dark' | 'light' | 'unknown' {
		// TODO: Implement terminal theme detection
		// For now, default to dark
		return 'dark';
	}

	/**
	 * Get theme presets for different modes
	 */
	static getThemePresets(): Record<string, ColorTheme> {
		return {
			'dark': {
				mainHighlight: '#ff49ff',
				systemText: '#f1d771', 
				fadedSystemText: '#d4c666',
				lightGray: '#bbbcbb',
				superLightBlue: '#f0f8ff',
				babyBlueDarker: '#82d0ff'
			},
			'light': {
				mainHighlight: '#d63384', // Darker pink for light backgrounds
				systemText: '#856404',    // Darker yellow
				fadedSystemText: '#6c757d',
				lightGray: '#6c757d',
				superLightBlue: '#0066cc',
				babyBlueDarker: '#0066cc'
			},
			'dark_colorblind': {
				mainHighlight: '#ff6b35', // Orange instead of pink
				systemText: '#4ecdc4',    // Teal instead of yellow
				fadedSystemText: '#95a5a6',
				lightGray: '#7f8c8d',
				superLightBlue: '#3498db',
				babyBlueDarker: '#2980b9'
			},
			'light_colorblind': {
				mainHighlight: '#e67e22', // Orange for light mode
				systemText: '#16a085',    // Dark teal
				fadedSystemText: '#7f8c8d',
				lightGray: '#95a5a6',
				superLightBlue: '#2980b9',
				babyBlueDarker: '#3498db'
			},
			'dark_ansi': {
				mainHighlight: '#ff0000', // ANSI red
				systemText: '#ffff00',    // ANSI yellow
				fadedSystemText: '#808080',
				lightGray: '#c0c0c0',
				superLightBlue: '#00ffff',
				babyBlueDarker: '#0000ff'
			},
			'light_ansi': {
				mainHighlight: '#800000', // Dark red
				systemText: '#808000',    // Dark yellow
				fadedSystemText: '#808080',
				lightGray: '#808080',
				superLightBlue: '#000080',
				babyBlueDarker: '#0000ff'
			}
		};
	}

	/**
	 * Apply theme preset
	 */
	static applyThemePreset(presetName: string): void {
		const presets = this.getThemePresets();
		if (presets[presetName]) {
			this.currentTheme = presets[presetName];
		}
	}
}