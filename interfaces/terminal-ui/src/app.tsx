#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { ChatInterface } from './components/ChatInterface';

const App: React.FC = () => {
  return <ChatInterface />;
};

render(<App />);