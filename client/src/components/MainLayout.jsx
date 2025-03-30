/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect, useState } from "react";

import Title from "./AppHeader";
import ChatLayout from "./chat/ChatLayout";
import WelcomePrompt from "./WelcomePrompt";
import NavbarActions from "./NavbarActions";
import { useAuth } from "../hooks/useAuth";
import { useLoading } from "../hooks/useLoading";


// Main layout component
export default function MainLayout() {

    const { setLoading } = useLoading();
    const { http, isAuthenticated } = useAuth();

    const [chatId, setChatId] = useState(null);
    const [history, setHistory] = useState([]);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const initialChatId = urlParams.get('chatId');

        if (isAuthenticated && initialChatId && chatId !== initialChatId) {
            setChatId(initialChatId);
            handleOpenHistory(initialChatId);
        } else if (isAuthenticated && history.length == 0) {
            getChatHistory();
            if (!initialChatId) {
                window.history.replaceState({}, '', window.location.pathname);
            }
        } else if (!isAuthenticated) {
            setChatId(null);
            setMessages([]);
            window.history.replaceState({}, '', window.location.pathname);
        }

        const publicSessionId = localStorage.getItem("publicSessionId");
        if (!publicSessionId) {
            const generateUUID = () => {
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                    const r = (Math.random() * 16) | 0;
                    const v = c === 'x' ? r : (r & 0x3) | 0x8;
                    return v.toString(16);
                });
            };
            localStorage.setItem("publicSessionId", crypto.randomUUID ? crypto.randomUUID() : generateUUID());
        }

    }, [chatId, isAuthenticated]);

    const getChatHistory = async () => {
        try {
            const response = await http.get("/history");
            setHistory(response?.data);
        } catch (error) {
            console.error("Failed to fetch chat history:", error);
        }
    };

    const handleOpenHistory = async (e) => {
        if (e === null) {
            setChatId(null);
            setMessages([]);
            window.history.pushState({}, '', '/');
            return;
        }
        try {
            setLoading(true);
            const response = await http.get(`/history/${e}`);
            setMessages(response?.data);
            if (response?.data?.length === 0) {
                setChatId(null);
                setMessages([]);
                window.history.replaceState({}, '', window.location.pathname);
                return;
            }
            setChatId(e);
        } catch (error) {
            console.error("Failed to fetch chat history:", error);
        } finally {
            setLoading(false);
        }
    }


    return (
        <div className='main'>
            <div className='main__left'>
                <Title />
            </div>

            <div className='main__center'>
                {chatId === null ? (
                    <WelcomePrompt
                        setChatId={setChatId}
                        setMessages={setMessages}
                        fetchHistory={getChatHistory}
                    />
                ) : (
                    <ChatLayout
                        chatId={chatId}
                        messages={messages}
                        setMessages={setMessages}
                    />
                )}
            </div>

            <div className='main__right'>
                <NavbarActions
                    chatId={chatId}
                    history={history}
                    setChatId={setChatId}
                    setHistory={setHistory}
                    setMessages={setMessages}
                    handleOpen={(e) => handleOpenHistory(e)}
                />
            </div>

        </div>
    );
}