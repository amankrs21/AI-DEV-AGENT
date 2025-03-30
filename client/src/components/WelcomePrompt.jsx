import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import { useEffect, useState } from 'react';

import ChatInput from './chat/ChatInput';
import TypewriterEffect from './typing/TypewriterEffect';
import { useAuth } from '../hooks/useAuth';
import { publicStreamChat } from '../api/publicChatApi';
import { privateStreamChat } from '../api/privateChatApi';


// Welcome Prompt component
export default function WelcomePrompt({ setChatId, setMessages, setPublicChat, fetchHistory }) {

    const { baseURL, isAuthenticated, userData } = useAuth();

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
        if (isAuthenticated) {
            const success = await privateStreamChat({
                baseURL,
                query: text,
                chatId: null,
                setMessages,
                setChatId,
            });
            if (success) { await fetchHistory(); }
        } else {
            const success = await publicStreamChat({
                baseURL,
                setMessages,
                query: text,
                setPublicChat,
            });
            if (!success) {
                toast.error("Failed to send message. Please reload the page.");
            }
        }
    };

    return (
        <div className="welcome">
            {isAuthenticated ? (
                <h2 style={{ color: 'white' }}>
                    {greeting}, {userData?.name.split(' ')[0]} 😊
                </h2>
            ) :
                <h2 style={{ color: 'white' }}>Hello! {greeting} 😊</h2>
            }
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
        </div>
    );
};

WelcomePrompt.propTypes = {
    setChatId: PropTypes.func.isRequired,
    setMessages: PropTypes.func.isRequired,
    setPublicChat: PropTypes.func.isRequired,
    fetchHistory: PropTypes.func.isRequired,
};
