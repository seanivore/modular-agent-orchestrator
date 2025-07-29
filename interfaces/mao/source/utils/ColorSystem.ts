/**
 * MAO Semantic Color System
 * Uses terminal's actual MAIN and BOLD colors, with semantic relationships for others
 * Based on UI_PHASE_1_LOGIC.md color psychology specifications
 */

export interface ColorTheme {
	main: string; // Terminal's default text color - let terminal decide
	bold: string; // Terminal's bold color - let terminal decide  
	user: string; // User messages - background neutral gray
	trusting_update_1: string; // AI highlights, trusted info (almost white blue)
	trusting_update_2: string; // Secondary trusted info (baby blue)
	supplemental_1: string; // Important subtext (same as user)
	supplemental_2: string; // Less important subtext (faded)
	processing: string; // AI thinking word color (light orange)
	accent_outside: string; // Outside chat accents (light purple)
	dark_supplemental: string; // Very faded background (dark gray)
}

// 6 adaptive color modes - relationships matter more than exact colors
const COLOR_THEMES: Record<string, ColorTheme> = {
	'dark_mode': {
		main: 'inherit', // Use terminal's default text color
		bold: 'inherit', // Use terminal's bold color
		user: '#bbbcbb', // Medium-light gray - background, forgettable
		trusting_update_1: '#f0f8ff', // Almost white blue - subtle accents
		trusting_update_2: '#82d0ff', // Baby blue darker version - stronger accents
		supplemental_1: '#bbbcbb', // Same as user - important subtext  
		supplemental_2: '#7b714a', // Faded green-gray-brown - less important
		processing: '#ffb366', // Light orange - thinking words only
		accent_outside: '#c8a2c8', // Light purple - accent outside chat
		dark_supplemental: '#4a4a4a' // Dark faded gray - transparent background
	},
	
	'light_mode': {
		main: 'inherit', // Use terminal's default text color
		bold: 'inherit', // Use terminal's bold color  
		user: '#666666', // Medium gray for light backgrounds
		trusting_update_1: '#e6f3ff', // Very light blue
		trusting_update_2: '#4a90e2', // Medium blue
		supplemental_1: '#666666', // Same as user
		supplemental_2: '#8b7355', // Light brown variant for light mode
		processing: '#ff8c42', // Orange adjusted for light backgrounds
		accent_outside: '#9966cc', // Purple adjusted for light mode
		dark_supplemental: '#cccccc' // Light gray for light mode backgrounds
	},
	
	'dark_colorblind': {
		main: 'inherit', // Use terminal's default text color
		bold: 'inherit', // Use terminal's bold color
		user: '#cccccc', // Higher contrast gray
		trusting_update_1: '#ffffff', // Pure white for high contrast
		trusting_update_2: '#88ccff', // Brighter blue for visibility
		supplemental_1: '#cccccc', // Higher contrast than user
		supplemental_2: '#999966', // More distinct from other colors
		processing: '#ffaa44', // Higher contrast orange
		accent_outside: '#cc88cc', // More distinct purple
		dark_supplemental: '#555555' // Slightly lighter for contrast
	},
	
	'light_colorblind': {
		main: 'inherit', // Use terminal's default text color
		bold: 'inherit', // Use terminal's bold color
		user: '#444444', // Darker gray for light backgrounds, high contrast
		trusting_update_1: '#001122', // Very dark blue for contrast
		trusting_update_2: '#2266aa', // Strong blue
		supplemental_1: '#444444', // Same as user
		supplemental_2: '#664422', // Strong brown contrast
		processing: '#cc4400', // Strong orange
		accent_outside: '#663399', // Strong purple
		dark_supplemental: '#aaaaaa' // Medium gray
	},
	
	'dark_ansi': {
		main: 'inherit', // Use terminal's default text color
		bold: 'inherit', // Use terminal's bold color
		user: 'gray', // ANSI gray
		trusting_update_1: 'white', // ANSI white
		trusting_update_2: 'cyan', // ANSI cyan as blue substitute
		supplemental_1: 'gray', // ANSI gray
		supplemental_2: 'yellow', // ANSI yellow as brown substitute
		processing: 'yellow', // ANSI yellow as orange substitute
		accent_outside: 'magenta', // ANSI magenta as purple
		dark_supplemental: 'black' // ANSI black
	},
	
	'light_ansi': {
		main: 'inherit', // Use terminal's default text color  
		bold: 'inherit', // Use terminal's bold color
		user: 'black', // ANSI black for light backgrounds
		trusting_update_1: 'white', // ANSI white
		trusting_update_2: 'blue', // ANSI blue
		supplemental_1: 'black', // ANSI black 
		supplemental_2: 'yellow', // ANSI yellow
		processing: 'red', // ANSI red as orange substitute
		accent_outside: 'magenta', // ANSI magenta
		dark_supplemental: 'white' // ANSI white for backgrounds
	}
};

class ColorSystem {
	private currentTheme: string = 'dark_colorblind';
	
	/**
	 * Get color by semantic meaning
	 */
	getColor(semanticMeaning: keyof ColorTheme): string {
		const theme = COLOR_THEMES[this.currentTheme];
		if (!theme) return 'inherit';
		return theme[semanticMeaning] || theme.main;
	}
	
	/**
	 * Get bullet color based on context and rules from _VISUAL_BRAND_IDENTITY.md
	 */
	getBulletColor(context: 'user' | 'ai', textStyle?: 'bold'): string {
		if (context === 'user') {
			// User bullets always gray
			return this.getColor('user');
		}
		
		// AI bullets - white normally, light blue when text is pink/bold
		if (textStyle === 'bold') {
			return this.getColor('trusting_update_1'); // Light blue when text is bold/pink
		}
		
		return 'white'; // White bullet for normal AI content
	}
	
	/**
	 * Get text color by semantic meaning with proper fallbacks
	 */
	getTextColor(semanticMeaning: 'action' | 'explanation' | 'user_input' | 'ai_highlight' | 'system_auto' | 'metadata'): string {
		switch (semanticMeaning) {
			case 'action':
				return this.getColor('bold'); // Pink - cognitive interrupt
			case 'explanation':
				return this.getColor('main'); // Terminal default - main content
			case 'user_input':
				return this.getColor('user'); // Gray - background, forgettable
			case 'ai_highlight':
				return this.getColor('trusting_update_1'); // Light blue - trusted info
			case 'system_auto':
				return this.getColor('supplemental_2'); // Faded - less important
			case 'metadata':
				return this.getColor('supplemental_2'); // Faded - background info
			default:
				return this.getColor('main');
		}
	}
	
	/**
	 * Set current theme
	 */
	setTheme(themeName: string): void {
		if (COLOR_THEMES[themeName]) {
			this.currentTheme = themeName;
		}
	}
	
	/**
	 * Get current theme name
	 */
	getCurrentTheme(): string {
		return this.currentTheme;
	}
	
	/**
	 * Get all available theme names
	 */
	getAvailableThemes(): string[] {
		return Object.keys(COLOR_THEMES);
	}
	
	/**
	 * Get theme display names for UI
	 */
	getThemeDisplayNames(): Record<string, string> {
		return {
			'dark_mode': 'Dark Mode',
			'light_mode': 'Light Mode', 
			'dark_colorblind': 'Dark Mode Colorblind-Friendly',
			'light_colorblind': 'Light Mode Colorblind-Friendly',
			'dark_ansi': 'Dark Mode ANSI Colors Only',
			'light_ansi': 'Light Mode ANSI Colors Only'
		};
	}
	
	/**
	 * Auto-detect best theme for user's terminal
	 */
	detectBestTheme(): string {
		// Could add logic to detect terminal capabilities and user preferences
		// For now, default to colorblind-friendly dark mode
		return 'dark_colorblind';
	}
}

// Export singleton instance and class
export const colorSystem = new ColorSystem();
export { ColorSystem };

// Set initial theme based on detection
colorSystem.setTheme(colorSystem.detectBestTheme());