import PropTypes from 'prop-types';
import { useEffect, useRef, useState } from 'react';
import { Container, IconButton } from '@mui/material';
import { ArrowDownward } from '@mui/icons-material';

import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import { useAuth } from '../../hooks/useAuth';
import TypingIndicator from '../typing/TypingIndicator';


// Chat layout component
export default function ChatLayout({ messages, setMessages }) {
    const { baseURL } = useAuth();
    const messagesEndRef = useRef(null);
    const [aiLoad, setAiLoad] = useState(false);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleChatSend = async (text) => {
        setMessages((prevMessages) => [
            ...prevMessages,
            { user: text },
        ]);

        try {
            setAiLoad(true);
            const response = await fetch(`${baseURL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: text }),
            });
            if (!response.ok) throw new Error("Failed to fetch response");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            setMessages((prevMessages) => [
                ...prevMessages,
                { bot: "" },
            ]);

            let isFirstChunk = true;
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                if (isFirstChunk) {
                    setAiLoad(false);
                    isFirstChunk = false;
                }
                setMessages((prevMessages) => {
                    const lastMessage = prevMessages[prevMessages.length - 1];
                    if (lastMessage.bot !== undefined) {
                        return [
                            ...prevMessages.slice(0, -1),
                            { bot: lastMessage.bot + chunk },
                        ];
                    }
                    return [...prevMessages, { bot: chunk }];
                });
            }
        } catch (error) {
            console.error("Failed to stream message:", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { bot: "Sorry, I couldn’t process that." },
            ]);
            setAiLoad(false);
        }
    };

    return (
        <div className="chat">
            <div className="chat__messages">
                <Container maxWidth="md" >
                    {messages.length === 0 ? (
                        <p style={{ color: '#D3D2D2' }}>No messages yet...</p>
                    ) : (
                        messages.map((msg, index) => (
                            <div key={index} className="message-pair">
                                {msg.user && <ChatMessage msg={{ user: msg.user }} />}
                                {msg.bot && <ChatMessage msg={{ bot: msg.bot }} />}
                            </div>
                        ))
                    )}

                    {aiLoad && <TypingIndicator message="thinking" />}

                    <div className="chat__scrollToBottom">
                        <IconButton
                            sx={{ backgroundColor: '#36383A', '&:hover': { backgroundColor: '#2F3135' } }}
                            onClick={scrollToBottom}
                        >
                            <ArrowDownward color="primary" />
                        </IconButton>
                    </div>
                    <div ref={messagesEndRef} />
                </Container>
            </div>
            <Container maxWidth="md" className="chat__input">
                <ChatInput onSend={handleChatSend} />
            </Container>
        </div>
    );
}

ChatLayout.propTypes = {
    messages: PropTypes.array.isRequired,
    setMessages: PropTypes.func.isRequired,
};
