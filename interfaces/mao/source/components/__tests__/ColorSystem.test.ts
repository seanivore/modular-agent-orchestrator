/**
 * ColorSystem Tests - Validates exact _VISUAL_BRAND_IDENTITY.md compliance
 */

import test from 'ava';
import {ColorSystem, colorSystem, THEME_DISPLAY_NAMES} from '../../utils/ColorSystem.js';

test('ColorSystem - Theme switching', t => {
	const cs = new ColorSystem();
	
	// Test theme switching
	cs.setTheme('light_mode');
	t.is(cs.getCurrentTheme(), 'light_mode');
	
	// Test invalid theme handling
	cs.setTheme('invalid_theme');
	t.is(cs.getCurrentTheme(), 'light_mode'); // Should remain unchanged
});

test('ColorSystem - Available themes', t => {
	const themes = colorSystem.getAvailableThemes();
	
	// Should have all 6 specified themes
	t.is(themes.length, 6);
	t.true(themes.includes('dark_mode'));
	t.true(themes.includes('light_mode'));
	t.true(themes.includes('dark_colorblind'));
	t.true(themes.includes('light_colorblind'));
	t.true(themes.includes('dark_ansi'));
	t.true(themes.includes('light_ansi'));
});

test('ColorSystem - Color retrieval', t => {
	const cs = new ColorSystem('dark_mode');
	
	// Test main colors exist and are correct format
	const mainColor = cs.getColor('main');
	t.is(mainColor, '#f1d771'); // Yellow as specified
	
	const boldColor = cs.getColor('bold');
	t.is(boldColor, '#ff49ff'); // Pink as specified
	
	const userColor = cs.getColor('user');
	t.is(userColor, '#bbbcbb'); // Gray as specified
});

test('ColorSystem - Bullet color logic', t => {
	const cs = new ColorSystem('dark_mode');
	
	// User content gets gray bullet
	const userBullet = cs.getBulletColor('user');
	t.is(userBullet, '#bbbcbb');
	
	// AI content gets main color bullet
	const aiBullet = cs.getBulletColor('ai');
	t.is(aiBullet, '#f1d771');
	
	// Bold text gets light blue bullet
	const boldBullet = cs.getBulletColor('ai', 'bold');
	t.is(boldBullet, '#82d0ff');
});

test('ColorSystem - Text color semantics', t => {
	const cs = new ColorSystem('dark_mode');
	
	// Action text should be pink (bold)
	const actionColor = cs.getTextColor('action');
	t.is(actionColor, '#ff49ff');
	
	// Explanation text should be yellow (main)
	const explanationColor = cs.getTextColor('explanation');
	t.is(explanationColor, '#f1d771');
	
	// User input should be gray
	const userColor = cs.getTextColor('user_input');
	t.is(userColor, '#bbbcbb');
	
	// AI highlights should be light blue
	const highlightColor = cs.getTextColor('ai_highlight');
	t.is(highlightColor, '#82d0ff');
	
	// Metadata should be light brown
	const metadataColor = cs.getTextColor('metadata');
	t.is(metadataColor, '#7b714a');
});

test('ColorSystem - Courtesy levels', t => {
	const cs = new ColorSystem('dark_mode');
	
	// Primary should be bold pink
	const primary = cs.getCourtesyLevel('primary');
	t.is(primary.color, '#ff49ff');
	t.is(primary.bold, true);
	
	// Secondary should be light blue
	const secondary = cs.getCourtesyLevel('secondary');
	t.is(secondary.color, '#82d0ff');
	t.is(secondary.bold, undefined);
	
	// Background should be dimmed brown
	const background = cs.getCourtesyLevel('background');
	t.is(background.color, '#7b714a');
	t.is(background.dimColor, true);
});

test('Theme display names mapping', t => {
	const themes = Object.keys(THEME_DISPLAY_NAMES);
	
	// Should have display names for all themes
	t.is(themes.length, 6);
	t.is(THEME_DISPLAY_NAMES['dark_mode'], 'Dark Mode');
	t.is(THEME_DISPLAY_NAMES['light_colorblind'], 'Light Mode Colorblind-Friendly');
});

test('ColorSystem - ANSI theme compatibility', t => {
	const cs = new ColorSystem('dark_ansi');
	
	// ANSI themes should use string color names
	const mainColor = cs.getColor('main');
	t.is(mainColor, 'yellow');
	
	const boldColor = cs.getColor('bold');
	t.is(boldColor, 'magenta');
});