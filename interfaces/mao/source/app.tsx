import React from 'react';
import ChatInterface from './components/ChatInterface.js';

type Props = {
	name: string | undefined;
};

export default function App({name = 'Stranger'}: Props) {
	return <ChatInterface username={name} />;
}
