/**
 * ActionList Component - The Core UX Innovation
 * Implements 3 types with rapid-changing content for "immediacy" feeling
 * Based on UI_PHASE_1_LOGIC.md specifications
 */

import React, {useState, useEffect, useCallback} from 'react';
import {Box, Text} from 'ink';
import {colorSystem} from '../utils/ColorSystem.js';

interface ActionItem {
	id: string;
	text: string;
	status: 'pending' | 'active' | 'completed';
	subItems?: ActionItem[];
}

interface ActionListProps {
	id: string;
	title: string;
	type: 'finalized' | 'inactive_not_finalized' | 'active';
	items: ActionItem[];
	metadata?: {
		cost?: string;
		tokens?: string;
		time?: string;
	};
	isExpanded?: boolean;
	onToggleExpand?: () => void;
}

interface ActionListState {
	isBlinking: boolean;
	currentActivity: string;
	activityIndex: number;
}

// Activity messages for rapid updates (cycling every 3 seconds)
const ACTIVITY_MESSAGES = {
	research: [
		'Analyzing market data',
		'Finding competitors', 
		'Gathering insights',
		'Processing research',
		'Synthesizing findings'
	],
	analysis: [
		'Processing data',
		'Identifying patterns',
		'Cross-referencing sources',
		'Building recommendations',
		'Formatting deliverables'
	],
	orchestrator: [
		'Reviewing outputs',
		'Assessing quality',
		'Planning adjustments',
		'Preparing assignments',
		'Coordinating work'
	],
	content: [
		'Drafting outline',
		'Writing sections',
		'Refining messaging',
		'Adding details',
		'Finalizing deliverables'
	]
};

export default function ActionList({
	id,
	title,
	type,
	items,
	metadata,
	isExpanded = true,
	onToggleExpand
}: ActionListProps) {
	const [state, setState] = useState<ActionListState>({
		isBlinking: type === 'active',
		currentActivity: '',
		activityIndex: 0
	});

	// Core UX Feature: Rapid-changing activity updates for "immediacy" feeling
	useEffect(() => {
		if (type !== 'active') return;

		const activityType = inferActivityType(title);
		const activities = ACTIVITY_MESSAGES[activityType] || ACTIVITY_MESSAGES.orchestrator;

		const interval = setInterval(() => {
			setState(prev => ({
				...prev,
				currentActivity: activities[prev.activityIndex % activities.length],
				activityIndex: prev.activityIndex + 1
			}));
		}, 3000); // 3-second cycles as specified

		// Initial activity
		setState(prev => ({
			...prev,
			currentActivity: activities[0]
		}));

		return () => clearInterval(interval);
	}, [type, title]);

	// Blinking animation for active lists
	useEffect(() => {
		if (type !== 'active') return;

		const blinkInterval = setInterval(() => {
			setState(prev => ({
				...prev,
				isBlinking: !prev.isBlinking
			}));
		}, 1000); // 1-second blink cycle

		return () => clearInterval(blinkInterval);
	}, [type]);

	const getBulletSymbol = (): string => {
		switch (type) {
			case 'finalized':
				return '●'; // Filled circle for completed
			case 'inactive_not_finalized':
				return '○'; // Empty circle for inactive
			case 'active':
				return state.isBlinking ? '●' : '○'; // Blinking for active
			default:
				return '○';
		}
	};

	const getBulletColor = (): string => {
		switch (type) {
			case 'finalized':
				return colorSystem.getColor('trusting_update_1'); // Light blue for completed
			case 'inactive_not_finalized':
				return colorSystem.getColor('user'); // Gray for inactive
			case 'active':
				return colorSystem.getColor('bold'); // Pink for active (attention)
			default:
				return colorSystem.getColor('user');
		}
	};

	const getTitleColor = (): string => {
		return type === 'active' && state.currentActivity ? 
			colorSystem.getColor('bold') : // Pink for active with activity
			colorSystem.getColor('main'); // Yellow for others
	};

	const renderCollapsedState = (): React.ReactNode => {
		if (type === 'finalized') {
			return (
				<Box marginLeft={4}>
					<Text color={colorSystem.getColor('supplemental_2')}>
						└── Done ({metadata?.cost} • {metadata?.tokens} • {metadata?.time})
					</Text>
				</Box>
			);
		}

		return (
			<Box marginLeft={4}>
				<Text color={colorSystem.getColor('supplemental_2')}>
					└── [▼] {items.length} items (click to expand)
				</Text>
			</Box>
		);
	};

	const renderExpandedItems = (): React.ReactNode => {
		return (
			<Box flexDirection="column" marginLeft={4}>
				{items.map((item, index) => (
					<Box key={item.id}>
						<Text color={colorSystem.getColor('supplemental_2')}>
							{index === items.length - 1 ? '└──' : '├──'} 
						</Text>
						<Text color={colorSystem.getColor('supplemental_2')}>
							{getItemSymbol(item.status)} 
						</Text>
						<Text 
							color={getItemTextColor(item.status)}
							bold={item.status === 'active'}
						>
							{item.text}
						</Text>
					</Box>
				))}
			</Box>
		);
	};

	const getItemSymbol = (status: 'pending' | 'active' | 'completed'): string => {
		switch (status) {
			case 'completed':
				return '▶︎'; // Filled triangle
			case 'active':
				return '▶︎'; // Filled triangle for active
			case 'pending':
				return '▷'; // Empty triangle
			default:
				return '▷';
		}
	};

	const getItemTextColor = (status: 'pending' | 'active' | 'completed'): string => {
		switch (status) {
			case 'active':
				return colorSystem.getColor('bold'); // Pink for active items
			case 'completed':
				return colorSystem.getColor('trusting_update_1'); // Light blue for completed
			case 'pending':
				return colorSystem.getColor('supplemental_2'); // Light brown for pending
			default:
				return colorSystem.getColor('main');
		}
	};

	return (
		<Box flexDirection="column" marginBottom={1}>
			{/* Main Task Header */}
			<Box>
				<Text color={getBulletColor()}>{getBulletSymbol()}   </Text>
				<Text color={getTitleColor()} bold={type === 'active'}>
					{title}
				</Text>
				{type === 'active' && state.currentActivity && (
					<Text color={colorSystem.getColor('processing')}>
						: {state.currentActivity}
					</Text>
				)}
			</Box>

			{/* Task Content */}
			{!isExpanded ? (
				renderCollapsedState()
			) : (
				renderExpandedItems()
			)}

			{/* Activity indicator for active tasks */}
			{type === 'active' && state.currentActivity && (
				<Box marginLeft={4} marginTop={1}>
					<Text color={colorSystem.getColor('supplemental_2')}>
						*Updating every 3 seconds...*
					</Text>
				</Box>
			)}
		</Box>
	);
}

// Helper function to infer activity type from task title
function inferActivityType(title: string): keyof typeof ACTIVITY_MESSAGES {
	const titleLower = title.toLowerCase();
	
	if (titleLower.includes('research') || titleLower.includes('analysis')) {
		return 'research';
	}
	if (titleLower.includes('content') || titleLower.includes('writing')) {
		return 'content';
	}
	if (titleLower.includes('orchestrat') || titleLower.includes('coordinat')) {
		return 'orchestrator';
	}
	if (titleLower.includes('analyz') || titleLower.includes('process')) {
		return 'analysis';
	}
	
	return 'orchestrator'; // Default
}

// Smart collapse logic - auto-collapse after completion
export function useActionListAutoCollapse(
	type: 'finalized' | 'inactive_not_finalized' | 'active',
	completionTime?: Date
): boolean {
	const [shouldCollapse, setShouldCollapse] = useState(false);

	useEffect(() => {
		if (type === 'finalized' && completionTime) {
			const timer = setTimeout(() => {
				setShouldCollapse(true);
			}, 30000); // Auto-collapse after 30 seconds

			return () => clearTimeout(timer);
		}
	}, [type, completionTime]);

	return shouldCollapse;
}

// Action list manager for handling multiple lists
export class ActionListManager {
	private static lists: Map<string, ActionListProps> = new Map();
	private static listeners: Set<() => void> = new Set();

	static addList(list: ActionListProps): void {
		this.lists.set(list.id, list);
		this.notifyListeners();
	}

	static updateList(id: string, updates: Partial<ActionListProps>): void {
		const existing = this.lists.get(id);
		if (existing) {
			this.lists.set(id, { ...existing, ...updates });
			this.notifyListeners();
		}
	}

	static removeList(id: string): void {
		this.lists.delete(id);
		this.notifyListeners();
	}

	static getLists(): ActionListProps[] {
		return Array.from(this.lists.values());
	}

	static subscribe(listener: () => void): () => void {
		this.listeners.add(listener);
		return () => this.listeners.delete(listener);
	}

	private static notifyListeners(): void {
		this.listeners.forEach(listener => listener());
	}

	// Move completed tasks above master list
	static moveCompletedTasksUp(): void {
		const lists = Array.from(this.lists.values());
		const completed = lists.filter(list => list.type === 'finalized');
		const active = lists.filter(list => list.type === 'active');
		const inactive = lists.filter(list => list.type === 'inactive_not_finalized');

		// Reorder: completed first, then inactive, then active
		const reordered = [...completed, ...inactive, ...active];
		
		this.lists.clear();
		reordered.forEach(list => this.lists.set(list.id, list));
		this.notifyListeners();
	}
}