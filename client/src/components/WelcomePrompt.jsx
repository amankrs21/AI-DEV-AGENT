import { useEffect, useState } from 'react';

import ChatInput from './chat/ChatInput';
import TypewriterEffect from './typing/TypewriterEffect';
import { useAuth } from '../hooks/useAuth';
import { Container } from '@mui/material';


// Welcome Prompt component
export default function WelcomePrompt({ setMessages }) {

    const { baseURL } = useAuth();
    const [greeting, setGreeting] = useState("Good Morning");

    useEffect(() => {
        const date = new Date();
        const hours = date.getHours();
        if (hours < 12) setGreeting("Good Morning");
        else if (hours >= 12 && hours < 17) setGreeting("Good Afternoon");
        else if (hours >= 17 && hours < 20) setGreeting("Good Evening");
        else setGreeting("Good Night");
    }, []);

    const handleChatSend = async (text) => {
        setMessages((prevMessages) => [
            ...prevMessages,
            { user: text },
        ]);

        try {
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
        }
    };

    return (
        <Container maxWidth="md" className="welcome">
            <h2 style={{ color: 'white' }}>Hello! {greeting} 😊</h2>
            <h2>How can I assist you today?</h2>

            <ChatInput onSend={handleChatSend} />

            <h3 className="welcome__typewriter">
                <TypewriterEffect
                    strings={[
                        "Analyze, debug, and optimize your code effortlessly.",
                        "Get smart suggestions to level up your code.",
                        "Complete and refactor code like a pro.",
                        "Upload your files to get started.",
                    ]}
                    delay={50}
                    deleteSpeed={20}
                />
            </h3>
        </Container>
    );
}