#!/usr/bin/env node

/**
 * MAO Terminal UI Playground - TypeScript/Node.js Edition
 * Explore what Claude Code-style terminal UIs can actually do!
 */

import { useState, useEffect } from 'react';
import { render, Text, Box, Newline, useInput, useApp } from 'ink';
import Spinner from 'ink-spinner';
import SelectInput from 'ink-select-input';
import TextInput from 'ink-text-input';
import { Transform } from 'stream';

// Types for our playground components
interface ThemeOption {
  label: string;
  value: string;
  colors: {
    text: string;
    diffRemoval: string;
    diffAddition: string;
  };
}

interface Settings {
  autoCompact: boolean;
  useTodoList: boolean;
  verboseOutput: boolean;
  theme: string;
  notifications: string;
  editorMode: string;
  model: string;
}

// Theme definitions based on your draft
const THEMES: ThemeOption[] = [
  {
    label: 'Dark Mode',
    value: 'dark',
    colors: {
      text: '#ffffff',
      diffRemoval: '#6b5251',
      diffAddition: '#506d51'
    }
  },
  {
    label: 'Light Mode', 
    value: 'light',
    colors: {
      text: '#131313',
      diffRemoval: '#bf88a4',
      diffAddition: '#6ca36c'
    }
  },
  {
    label: 'Dark Mode Colorblind-Friendly',
    value: 'dark-colorblind',
    colors: {
      text: '#ffffff',
      diffRemoval: '#6d1813', 
      diffAddition: '#18516d'
    }
  },
  {
    label: 'Light Mode Colorblind-Friendly',
    value: 'light-colorblind',
    colors: {
      text: '#11100f',
      diffRemoval: '#bea4a3',
      diffAddition: '#87a4c0'
    }
  },
  {
    label: 'Dark Mode ANSI Colors Only',
    value: 'dark-ansi',
    colors: {
      text: '#ffffff',
      diffRemoval: '#a41e1a',
      diffAddition: '#29a423'
    }
  },
  {
    label: 'Light Mode ANSI Colors Only',
    value: 'light-ansi', 
    colors: {
      text: '#010101',
      diffRemoval: '#a41e19',
      diffAddition: '#29a424'
    }
  }
];

// Progress indicator animations (like Claude Code's asterisk)
const PROGRESS_FRAMES = ['⋅', '·', '‧', '•', '●', '◉', '⬢', '⬣'];
const RELAY_FRAMES = [
  '○ ○ ○ ○',
  '● ○ ○ ○', 
  '✓ ● ○ ○',
  '✓ ✓ ● ○',
  '✓ ✓ ✓ ●',
  '✓ ✓ ✓ ✓'
];

// Main App Component
const App = () => {
  const [screen, setScreen] = useState<'menu' | 'settings' | 'progress' | 'themes'>('menu');
  const [settings, setSettings] = useState<Settings>({
    autoCompact: true,
    useTodoList: true,
    verboseOutput: false,
    theme: 'dark',
    notifications: 'bell',
    editorMode: 'normal',
    model: 'default'
  });

  const { exit } = useApp();

  useInput((input, key) => {
    if (input === 'q' || (key.ctrl && input === 'c')) {
      exit();
    }
    if (input === 'm') {
      setScreen('menu');
    }
  });

  switch (screen) {
    case 'menu':
      return <MainMenu onSelect={setScreen} />;
    case 'settings':
      return <SettingsScreen settings={settings} onUpdate={setSettings} onBack={() => setScreen('menu')} />;
    case 'progress':
      return <ProgressPlayground onBack={() => setScreen('menu')} />;
    case 'themes':
      return <ThemeShowcase onBack={() => setScreen('menu')} />;
    default:
      return <MainMenu onSelect={setScreen} />;
  }
};

// Main Menu Component
const MainMenu = ({ onSelect }: { onSelect: (screen: string) => void }) => {
  const menuItems = [
    { label: '⚙️  Settings Screen Demo', value: 'settings' },
    { label: '🔄 Progress Indicators Demo', value: 'progress' },
    { label: '🎨 Theme Showcase', value: 'themes' },
    { label: '❌ Exit', value: 'exit' }
  ];

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">
        🎭 MAO Terminal UI Playground (TypeScript/Node.js)
      </Text>
      <Text color="gray">Explore Claude Code-style terminal capabilities</Text>
      <Newline />
      
      <SelectInput
        items={menuItems}
        onSelect={(item) => {
          if (item.value === 'exit') {
            process.exit(0);
          } else {
            onSelect(item.value);
          }
        }}
      />
      
      <Newline />
      <Text color="gray">Use ↑↓ to navigate, Enter to select, 'q' to quit, 'm' for menu</Text>
    </Box>
  );
};

// Settings Screen Component (based on your draft)
const SettingsScreen = ({ 
  settings, 
  onUpdate, 
  onBack 
}: { 
  settings: Settings; 
  onUpdate: (settings: Settings) => void; 
  onBack: () => void; 
}) => {
  const [selectedSetting, setSelectedSetting] = useState(0);
  
  const settingItems = [
    { 
      label: `Auto-compact: ${settings.autoCompact ? 'true' : 'false'}`, 
      key: 'autoCompact',
      type: 'boolean'
    },
    { 
      label: `Use todo list: ${settings.useTodoList ? 'true' : 'false'}`, 
      key: 'useTodoList',
      type: 'boolean'
    },
    { 
      label: `Verbose output: ${settings.verboseOutput ? 'true' : 'false'}`, 
      key: 'verboseOutput',
      type: 'boolean'
    },
    { 
      label: `Theme: ${settings.theme}`, 
      key: 'theme',
      type: 'select'
    },
    { 
      label: `Notifications: ${settings.notifications}`, 
      key: 'notifications',
      type: 'text'
    },
    { 
      label: `Editor mode: ${settings.editorMode}`, 
      key: 'editorMode',
      type: 'text'
    },
    { 
      label: `Model: ${settings.model}`, 
      key: 'model',
      type: 'text'
    }
  ];

  useInput((input, key) => {
    if (key.escape) {
      onBack();
    }
    if (key.upArrow) {
      setSelectedSetting(Math.max(0, selectedSetting - 1));
    }
    if (key.downArrow) {
      setSelectedSetting(Math.min(settingItems.length - 1, selectedSetting + 1));
    }
    if (key.return) {
      const item = settingItems[selectedSetting];
      if (item.type === 'boolean') {
        onUpdate({
          ...settings,
          [item.key]: !settings[item.key as keyof Settings]
        });
      }
    }
  });

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">⚙️ CONFIGURATION SETTINGS</Text>
      <Text color="gray">Configure Mao preferences</Text>
      <Newline />
      
      {settingItems.map((item, index) => (
        <Box key={item.key}>
          <Text color={index === selectedSetting ? 'yellow' : 'white'}>
            {index === selectedSetting ? '▶ ' : '  '}{item.label}
          </Text>
        </Box>
      ))}
      
      <Newline />
      <Text color="gray">Use ↑↓ to navigate, Enter to toggle, Esc to go back</Text>
    </Box>
  );
};

// Progress Indicators Demo
const ProgressPlayground = ({ onBack }: { onBack: () => void }) => {
  const [progressFrame, setProgressFrame] = useState(0);
  const [relayFrame, setRelayFrame] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;
    
    const interval = setInterval(() => {
      setProgressFrame((prev) => (prev + 1) % PROGRESS_FRAMES.length);
      setRelayFrame((prev) => (prev + 1) % RELAY_FRAMES.length);
    }, 200);

    return () => clearInterval(interval);
  }, [isRunning]);

  useInput((input, key) => {
    if (key.escape) {
      onBack();
    }
    if (input === 's') {
      setIsRunning(!isRunning);
    }
  });

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">🔄 Progress Indicators Demo</Text>
      <Text color="gray">Claude Code-style animations</Text>
      <Newline />
      
      <Text>Anthropic-style growing/shrinking:</Text>
      <Text color="yellow">  {PROGRESS_FRAMES[progressFrame]} Processing...</Text>
      <Newline />
      
      <Text>Relay race progress (your idea!):</Text>
      <Text color="green">  {RELAY_FRAMES[relayFrame]}</Text>
      <Newline />
      
      <Text>Ink Spinner component:</Text>
      <Text color="blue">  <Spinner type="dots" /> Loading...</Text>
      <Newline />
      
      <Text color="gray">Press 's' to start/stop animation, Esc to go back</Text>
      <Text color="gray">Animation running: {isRunning ? '✓' : '✗'}</Text>
    </Box>
  );
};

// Theme Showcase
const ThemeShowcase = ({ onBack }: { onBack: () => void }) => {
  const [selectedTheme, setSelectedTheme] = useState(0);

  useInput((input, key) => {
    if (key.escape) {
      onBack();
    }
    if (key.upArrow) {
      setSelectedTheme(Math.max(0, selectedTheme - 1));
    }
    if (key.downArrow) {
      setSelectedTheme(Math.min(THEMES.length - 1, selectedTheme + 1));
    }
  });

  const currentTheme = THEMES[selectedTheme];

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold color="cyan">🎨 Theme Showcase</Text>
      <Text color="gray">Choose the text style that looks best with your terminal</Text>
      <Newline />
      
      {THEMES.map((theme, index) => (
        <Box key={theme.value} flexDirection="column">
          <Text color={index === selectedTheme ? 'yellow' : 'white'}>
            {index === selectedTheme ? '▶ ' : '  '}{index + 1}. {theme.label}
          </Text>
          {index === selectedTheme && (
            <Box flexDirection="column" marginLeft={4}>
              <Text>   - White text → {theme.colors.text}</Text>
              <Text>   - Diff removal → {theme.colors.diffRemoval}</Text>
              <Text>   - Diff addition → {theme.colors.diffAddition}</Text>
            </Box>
          )}
        </Box>
      ))}
      
      <Newline />
      <Text color="gray">Use ↑↓ to navigate themes, Esc to go back</Text>
    </Box>
  );
};

// Render the app
render(<App />);

export {};