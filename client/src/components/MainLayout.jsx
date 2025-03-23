/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useState } from "react";

import Title from "./AppHeader";
import FileManager from "./FileManager";
import ChatLayout from "./chat/ChatLayout";
import WelcomePrompt from "./WelcomePrompt";
import { useAuth } from "../hooks/useAuth";
import { useLoading } from "../hooks/useLoading";


// Main layout component
export default function MainLayout() {

    const { http } = useAuth();
    const { setLoading } = useLoading();
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        if (messages.length === 0) { getChatHistory(); }
    }, []);

    const getChatHistory = async () => {
        try {
            setLoading(true);
            const response = await http.get("/history");
            setMessages(response.data);
        } catch (error) {
            console.error("Failed to fetch chat history:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='main'>
            <div className='main__left'>
                <Title />
            </div>

            <div className='main__center'>
                {messages?.length > 0 ? (
                    <ChatLayout messages={messages} setMessages={setMessages} />
                ) : (
                    <WelcomePrompt setMessages={setMessages} />
                )}
            </div>

            <div className='main__right'>
                <FileManager setMessages={setMessages} />
            </div>

        </div>
    );
}