/**
 * MAO Semantic Color System
 * Implements the 6-color psychology-based terminal interface
 * Based on _VISUAL_BRAND_IDENTITY.md specifications
 */

export interface ColorTheme {
	main: string; // Default terminal text color (MAIN) 
	bold: string; // Bold terminal color - cognitive interrupt (BOLD)
	user: string; // User messages - background neutral (USER)
	trusting_update_1: string; // AI highlights, trusted info (TRUSTING UPDATE LEVEL 1)
	trusting_update_2: string; // Secondary trusted info (TRUSTING UPDATE LEVEL 2)
	supplemental_1: string; // Important subtext (SUPPLEMENTAL INFO LEVEL 1)
	supplemental_2: string; // Less important subtext (SUPPLEMENTAL INFO LEVEL 2)
	processing: string; // AI thinking word color (PROCESSING)
	accent_outside: string; // Outside chat accents (ACCENT OUTSIDE OF CHAT)
	dark_supplemental: string; // Very faded background (SUPPLEMENTAL OUTSIDE OF CHAT)
}

// 6 adaptive color modes as specified
const COLOR_THEMES: Record<string, ColorTheme> = {
	'dark_mode': {
		main: '#f1d771', // Yellow - user's default terminal text
		bold: '#ff49ff', // Pink - the ONLY bold color, cognitive interrupt
		user: '#bbbcbb', // Gray - user messages, background neutral
		trusting_update_1: '#82d0ff', // Light blue - AI-highlighted URLs/commands
		trusting_update_2: '#b3e0ff', // Almost baby blue - secondary trusted info
		supplemental_1: '#bbbcbb', // Same as user color - important subtext
		supplemental_2: '#7b714a', // Light brown - metadata, less important
		processing: '#ffb366', // Light orange - AI thinking words
		accent_outside: '#c49fff', // Light purple - outside chat accents
		dark_supplemental: '#4d4d4d' // Dark faded gray - virtually transparent
	},
	'light_mode': {
		main: '#8b7a00', // Darker yellow for light backgrounds
		bold: '#cc00cc', // Darker pink for visibility
		user: '#666666', // Darker gray
		trusting_update_1: '#0066cc', // Darker blue
		trusting_update_2: '#3385dd', // Medium blue
		supplemental_1: '#666666', // Same as user
		supplemental_2: '#5a5230', // Darker brown
		processing: '#cc7a00', // Darker orange
		accent_outside: '#8833cc', // Darker purple
		dark_supplemental: '#cccccc' // Light gray for light mode
	},
	'dark_colorblind': {
		main: '#f1d771', // Yellow maintained
		bold: '#ff3366', // Red-pink for colorblind visibility
		user: '#bbbcbb', // Gray maintained
		trusting_update_1: '#33ccff', // Bright cyan
		trusting_update_2: '#66ddff', // Lighter cyan
		supplemental_1: '#bbbcbb', // Same as user
		supplemental_2: '#996633', // Warm brown
		processing: '#ff9933', // Warm orange
		accent_outside: '#cc66ff', // Bright purple
		dark_supplemental: '#4d4d4d' // Dark gray
	},
	'light_colorblind': {
		main: '#8b7a00', // Dark yellow
		bold: '#cc0033', // Dark red-pink
		user: '#666666', // Dark gray
		trusting_update_1: '#0099cc', // Dark cyan
		trusting_update_2: '#2dadda', // Medium cyan
		supplemental_1: '#666666', // Same as user
		supplemental_2: '#663300', // Dark brown
		processing: '#cc6600', // Dark orange
		accent_outside: '#6633cc', // Dark purple
		dark_supplemental: '#cccccc' // Light gray
	},
	'dark_ansi': {
		main: 'yellow', // ANSI yellow
		bold: 'magenta', // ANSI magenta
		user: 'gray', // ANSI gray
		trusting_update_1: 'cyan', // ANSI cyan
		trusting_update_2: 'blue', // ANSI blue
		supplemental_1: 'gray', // ANSI gray
		supplemental_2: 'white', // ANSI white for brown substitute
		processing: 'red', // ANSI red for orange substitute
		accent_outside: 'blue', // ANSI blue
		dark_supplemental: 'black' // ANSI black
	},
	'light_ansi': {
		main: 'black', // ANSI black on light
		bold: 'red', // ANSI red
		user: 'gray', // ANSI gray
		trusting_update_1: 'blue', // ANSI blue
		trusting_update_2: 'cyan', // ANSI cyan
		supplemental_1: 'gray', // ANSI gray
		supplemental_2: 'black', // ANSI black
		processing: 'red', // ANSI red
		accent_outside: 'magenta', // ANSI magenta
		dark_supplemental: 'white' // ANSI white
	}
};

export class ColorSystem {
	private currentTheme: string = 'dark_mode';
	private theme: ColorTheme;

	constructor(themeName: string = 'dark_mode') {
		this.currentTheme = themeName;
		this.theme = COLOR_THEMES[themeName] || COLOR_THEMES.dark_mode;
	}

	/**
	 * Get color for specific semantic meaning
	 */
	getColor(semanticType: keyof ColorTheme): string {
		return this.theme[semanticType];
	}

	/**
	 * Switch theme and get updated colors
	 */
	setTheme(themeName: string): void {
		if (COLOR_THEMES[themeName]) {
			this.currentTheme = themeName;
			this.theme = COLOR_THEMES[themeName];
		}
	}

	/**
	 * Get all available themes
	 */
	getAvailableThemes(): string[] {
		return Object.keys(COLOR_THEMES);
	}

	/**
	 * Get current theme name
	 */
	getCurrentTheme(): string {
		return this.currentTheme;
	}

	/**
	 * Determine bullet color based on content type and text color
	 * Implements exact decision tree from _VISUAL_BRAND_IDENTITY.md
	 */
	getBulletColor(contentType: 'user' | 'ai' | 'system', textColor?: keyof ColorTheme): string {
		// Is text PINK and bold? -> LIGHT BLUE bullet
		if (textColor === 'bold') {
			return this.theme.trusting_update_1;
		}
		// Is this from user? -> GRAY bullet
		if (contentType === 'user') {
			return this.theme.user;
		}
		// Is this AI or system response? -> WHITE bullet (main color)
		return this.theme.main;
	}

	/**
	 * Get text color based on semantic meaning
	 * Implements exact decision tree from _VISUAL_BRAND_IDENTITY.md
	 */
	getTextColor(semanticMeaning: 'action' | 'explanation' | 'user_input' | 'ai_highlight' | 'system_auto' | 'metadata'): string {
		switch (semanticMeaning) {
			case 'action': // AI taking specific action - PINK and BOLD
				return this.theme.bold;
			case 'explanation': // AI explaining - YELLOW (main)
				return this.theme.main;
			case 'user_input': // User messages - GRAY
				return this.theme.user;
			case 'ai_highlight': // AI-sent URLs/commands - LIGHT BLUE
				return this.theme.trusting_update_1;
			case 'system_auto': // System automated - WHITE (main for terminal)
				return this.theme.main;
			case 'metadata': // Numbers, organizational info - LIGHT BROWN
				return this.theme.supplemental_2;
			default:
				return this.theme.main;
		}
	}

	/**
	 * Apply "courteous behavior" styling - determines prominence
	 */
	getCourtesyLevel(importance: 'primary' | 'secondary' | 'background'): {
		color: string;
		dimColor?: boolean;
		bold?: boolean;
	} {
		switch (importance) {
			case 'primary': // Requires immediate attention
				return { color: this.theme.bold, bold: true };
			case 'secondary': // Helpful but not urgent
				return { color: this.theme.trusting_update_1 };
			case 'background': // Minimal prominence
				return { color: this.theme.supplemental_2, dimColor: true };
		}
	}
}

// Global color system instance
export const colorSystem = new ColorSystem();

// Theme names for UI selection
export const THEME_DISPLAY_NAMES: Record<string, string> = {
	'dark_mode': 'Dark Mode',
	'light_mode': 'Light Mode', 
	'dark_colorblind': 'Dark Mode Colorblind-Friendly',
	'light_colorblind': 'Light Mode Colorblind-Friendly',
	'dark_ansi': 'Dark Mode ANSI Colors Only',
	'light_ansi': 'Light Mode ANSI Colors Only'
};