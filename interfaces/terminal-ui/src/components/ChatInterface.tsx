import React, { useState, useEffect } from 'react';
import { Box, Text, useInput, useApp } from 'ink';

interface Message {
  type: 'user' | 'mao' | 'system';
  content: string;
  timestamp: Date;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const { exit } = useApp();

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
        content: '> Try "how do we start building?"',
        timestamp: new Date()
      }
    ]);
  }, []);

  const addMessage = (type: Message['type'], content: string) => {
    setMessages(prev => [...prev, { type, content, timestamp: new Date() }]);
  };

  const handleSubmit = async (userInput: string) => {
    if (!userInput.trim()) return;
    
    addMessage('user', userInput);
    setInput('');
    setIsTyping(true);

    // Handle slash commands
    if (userInput.startsWith('/')) {
      const command = userInput.slice(1).toLowerCase();
      
      switch (command) {
        case 'help':
          setTimeout(() => {
            addMessage('mao', 'Available commands:\n  /help - Show this help\n  /config - Change settings\n  /goal - Create a workflow\n  /exit - Quit Mao');
            setIsTyping(false);
          }, 500);
          break;
          
        case 'config':
          setTimeout(() => {
            addMessage('mao', 'Configuration options:\n  Theme: dark mode CVD\n  Model: claude-sonnet-4\n  Provider: anthropic direct');
            setIsTyping(false);
          }, 500);
          break;
          
        case 'exit':
          exit();
          break;
          
        default:
          setTimeout(() => {
            addMessage('mao', `Command "/${command}" not recognized. Try /help for available commands.`);
            setIsTyping(false);
          }, 300);
      }
    } else {
      // Handle regular conversation
      setTimeout(() => {
        addMessage('mao', `I understand you want to: "${userInput}"\n\nLet me help you create a workflow for that. What specific deliverable are you looking for?`);
        setIsTyping(false);
      }, 800);
    }
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

  const renderMessage = (msg: Message, index: number) => {
    const getMessageColor = () => {
      switch (msg.type) {
        case 'user': return '#bbbcbb';
        case 'mao': return '#f1d771'; 
        case 'system': return '#ffffff';
        default: return '#ffffff';
      }
    };

    const getPrefix = () => {
      switch (msg.type) {
        case 'user': return '> ';
        case 'mao': return '● ';
        case 'system': return '';
        default: return '';
      }
    };

    // Handle system messages with boxes differently
    if (msg.type === 'system' && (msg.content.includes('Mao is ready') || msg.content.includes('Try "'))) {
      return (
        <Box key={index} borderStyle="round" padding={1} marginY={0}>
          <Text color={getMessageColor()}>{msg.content}</Text>
        </Box>
      );
    }

    return (
      <Box key={index} marginY={0}>
        <Text color={getMessageColor()}>
          {getPrefix()}{msg.content}
        </Text>
      </Box>
    );
  };

  return (
    <Box flexDirection="column" height="100%" padding={1}>
      {/* Header - handled by first system message */}
      
      {/* Message History */}
      <Box flexDirection="column" flexGrow={1}>
        {messages.map(renderMessage)}
        
        {isTyping && (
          <Box marginY={1}>
            <Text color="#f1d771">● Mao is thinking...</Text>
          </Box>
        )}
      </Box>

      {/* Input Area */}
      <Box marginTop={1}>
        <Text color="#82d0ff">> </Text>
        <Text color="#ffffff">{input}</Text>
        <Text color="#82d0ff">|</Text>
      </Box>

      {/* Tip */}
      <Box marginTop={1}>
        <Text color="#bbbcbb">  ?  /help for help, /config to change settings</Text>
      </Box>
    </Box>
  );
};