#!/usr/bin/env node
import React from 'react';
import {render} from 'ink';
import meow from 'meow';
import App from './app.js';

const cli = meow(
	`
	🐱 Mao - Modular Agent Orchestrator v4.0.0
	The AI-powered terminal experience with emotional intelligence

	Usage
	  $ mao [options]

	Options
		--name          Your name for personalized experience
		--ui-mode       Launch interactive chat interface (default)
		--goal          Quick goal processing: mao --goal "build a website"
		--config        Show configuration options
		--help          Show this help message

	Interactive Commands (in chat mode)
		/help           Show available commands
		/config         Manage settings and workflows  
		/goal <text>    Transform goals into actionable workflows
		/tools          List available tools and integrations
		/memory         View and manage conversation memory
		/stats          Show usage analytics
		/exit           Exit Mao

	Examples
	  $ mao --name="Sean"
	  $ mao --goal "Create a marketing plan for my startup"
	  $ mao --config
	  
	💡 Pro tip: Press Tab for autocomplete, Ctrl+C to exit
`,
	{
		importMeta: import.meta,
		flags: {
			name: {
				type: 'string',
				shortFlag: 'n',
			},
			uiMode: {
				type: 'boolean',
				default: true,
				shortFlag: 'u',
			},
			goal: {
				type: 'string',
				shortFlag: 'g',
			},
			config: {
				type: 'boolean',
				shortFlag: 'c',
			},
		},
	},
);

// Quick goal processing mode
if (cli.flags.goal) {
	console.log(`🎯 Processing goal: "${cli.flags.goal}"`);
	console.log('🔄 Generating workflow...');
	// TODO: Connect to Python backend for goal processing
	process.exit(0);
}

// Config mode
if (cli.flags.config) {
	console.log('⚙️  Mao Configuration');
	console.log('📁 Config directory: ~/.mao/');
	console.log('🔧 Coming soon: Interactive config management');
	// TODO: Show configuration interface
	process.exit(0);
}

// Default: Launch interactive chat UI
render(<App name={cli.flags.name} uiMode={cli.flags.uiMode} />);
