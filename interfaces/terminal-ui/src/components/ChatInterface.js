import React, { useState, useEffect, useRef } from 'react';
import { Box, Text, useInput, useApp } from 'ink';
import { PythonBridge } from '../api/PythonBridge.js';

export const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const { exit } = useApp();
  const pythonBridge = useRef(null);

  // Initialize Python bridge
  useEffect(() => {
    pythonBridge.current = new PythonBridge();
    
    // Test connection
    setTimeout(async () => {
      try {
        const response = await pythonBridge.current.sendCommand('ping', {});
        if (response.success) {
          setIsConnected(true);
          addMessage('system', '✓ Connected to Mao backend');
        } else {
          setIsConnected(false);
          addMessage('error', '⚠ Backend connection failed - using mock responses');
        }
      } catch (error) {
        setIsConnected(false);
        addMessage('error', '⚠ Backend connection failed - using mock responses');
      }
    }, 1000);

    // Cleanup on unmount
    return () => {
      if (pythonBridge.current) {
        pythonBridge.current.disconnect();
      }
    };
  }, []);

  // Initialize with welcome messages
  useEffect(() => {
    setMessages([
      {
        type: 'system',
        content: '~(=^‥^)  Mao is ready to help!\n   user: seanivore',
        timestamp: new Date()
      },
      {
        type: 'mao', 
        content: 'Say "hello" to Mao.\n    ├ Describe your workflow \n    ├ Ask a question \n    └ Share your goal',
        timestamp: new Date()
      },
      {
        type: 'system',
        content: '> Try "how do we start building?" or "/help"',
        timestamp: new Date()
      }
    ]);
  }, []);

  const addMessage = (type, content) => {
    setMessages(prev => [...prev, { type, content, timestamp: new Date() }]);
  };

  const handleSubmit = async (userInput) => {
    if (!userInput.trim()) return;
    
    addMessage('user', userInput);
    setInput('');
    setIsTyping(true);

    try {
      let response;

      // Handle slash commands
      if (userInput.startsWith('/')) {
        const command = userInput.slice(1).toLowerCase();
        
        if (command === 'exit') {
          exit();
          return;
        }

        if (isConnected && pythonBridge.current) {
          // Use real backend for slash commands
          response = await pythonBridge.current.executeSlashCommand(command);
          
          if (response.success) {
            addMessage('mao', response.data.message || 'Command executed successfully');
          } else {
            addMessage('error', response.error || 'Command failed');
          }
        } else {
          // Fallback mock responses
          await handleMockSlashCommand(command);
        }
      } else {
        // Handle regular conversation/goals
        if (isConnected && pythonBridge.current) {
          // Check if it looks like a goal request
          if (userInput.toLowerCase().includes('goal') || 
              userInput.toLowerCase().includes('workflow') ||
              userInput.toLowerCase().includes('create') ||
              userInput.toLowerCase().includes('build')) {
            response = await pythonBridge.current.processGoal(userInput);
          } else {
            response = await pythonBridge.current.chat(userInput);
          }
          
          if (response.success) {
            addMessage('mao', response.data.message || response.data);
          } else {
            addMessage('error', response.error || 'Request failed');
          }
        } else {
          // Fallback mock conversation
          await handleMockConversation(userInput);
        }
      }
    } catch (error) {
      addMessage('error', `Error: ${error}`);
    } finally {
      setIsTyping(false);
    }
  };

  const handleMockSlashCommand = async (command) => {
    switch (command) {
      case 'help':
        setTimeout(() => {
          addMessage('mao', 'Available commands:\n  /help - Show this help\n  /config - Change settings\n  /goal - Create a workflow\n  /stats - Show statistics\n  /exit - Quit Mao');
          setIsTyping(false);
        }, 500);
        break;
        
      case 'config':
        setTimeout(() => {
          addMessage('mao', 'Configuration options:\n  Theme: dark mode CVD\n  Model: claude-sonnet-4\n  Provider: anthropic direct\n  Status: Mock mode (backend disconnected)');
          setIsTyping(false);
        }, 500);
        break;
        
      case 'stats':
        setTimeout(() => {
          addMessage('mao', 'System Statistics:\n  Sessions: 0\n  Workflows: 0\n  Tools: 8 available\n  Status: Mock mode');
          setIsTyping(false);
        }, 500);
        break;
        
      default:
        setTimeout(() => {
          addMessage('mao', `Command "/${command}" not recognized. Try /help for available commands.`);
          setIsTyping(false);
        }, 300);
    }
  };

  const handleMockConversation = async (userInput) => {
    setTimeout(() => {
      addMessage('mao', `I understand you want to: "${userInput}"\n\nLet me help you create a workflow for that. What specific deliverable are you looking for?\n\n[Note: Using mock responses - backend disconnected]`);
      setIsTyping(false);
    }, 800);
  };

  useInput((input, key) => {
    if (key.return) {
      handleSubmit(input);
      setInput('');
    } else if (key.backspace || key.delete) {
      setInput(prev => prev.slice(0, -1));
    } else if (input.length === 1 && !key.ctrl && !key.meta) {
      setInput(prev => prev + input);
    }
  });

  const renderMessage = (msg, index) => {
    const getMessageColor = () => {
      switch (msg.type) {
        case 'user': return '#bbbcbb';
        case 'mao': return '#f1d771'; 
        case 'system': return '#ffffff';
        case 'error': return '#ff6b6b';
        default: return '#ffffff';
      }
    };

    const getPrefix = () => {
      switch (msg.type) {
        case 'user': return '> ';
        case 'mao': return '● ';
        case 'system': return '';
        case 'error': return '⚠ ';
        default: return '';
      }
    };

    // Handle system messages with boxes differently
    if (msg.type === 'system' && (msg.content.includes('Mao is ready') || msg.content.includes('Try "'))) {
      return React.createElement(Box, { key: index, borderStyle: "round", padding: 1, marginY: 0 },
        React.createElement(Text, { color: getMessageColor() }, msg.content)
      );
    }

    return React.createElement(Box, { key: index, marginY: 0 },
      React.createElement(Text, { color: getMessageColor() }, getPrefix() + msg.content)
    );
  };

  return React.createElement(Box, { flexDirection: "column", height: "100%", padding: 1 },
    // Message History
    React.createElement(Box, { flexDirection: "column", flexGrow: 1 },
      ...messages.map(renderMessage),
      
      isTyping && React.createElement(Box, { marginY: 1 },
        React.createElement(Text, { color: "#f1d771" }, "● Mao is thinking...")
      )
    ),

    // Input Area
    React.createElement(Box, { marginTop: 1 },
      React.createElement(Text, { color: "#82d0ff" }, "> "),
      React.createElement(Text, { color: "#ffffff" }, input),
      React.createElement(Text, { color: "#82d0ff" }, "|")
    ),

    // Status Bar
    React.createElement(Box, { marginTop: 1 },
      React.createElement(Text, { color: "#bbbcbb" }, "  ?  /help for help, /config to change settings "),
      React.createElement(Text, { color: isConnected ? '#90ee90' : '#ff6b6b' },
        isConnected ? '● connected' : '● mock mode'
      )
    )
  );
};