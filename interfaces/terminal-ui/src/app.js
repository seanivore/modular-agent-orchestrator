#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { ChatInterface } from './components/ChatInterface.js';

const App = () => {
  return React.createElement(ChatInterface);
};

render(React.createElement(App));