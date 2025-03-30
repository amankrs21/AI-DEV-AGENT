/* eslint-disable react-hooks/exhaustive-deps */
import PropTypes from "prop-types";
import { toast } from "react-toastify";
import { useEffect, useRef, useState } from "react";
import { ArrowDownward } from "@mui/icons-material";
import { Container, IconButton } from "@mui/material";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "../typing/TypingIndicator";
import { useAuth } from "../../hooks/useAuth";
import { publicStreamChat } from "../../api/publicChatApi";
import { privateStreamChat } from "../../api/privateChatApi";


// Chat layout component
export default function ChatLayout({ chatId, messages, setMessages }) {
    const { baseURL, isAuthenticated } = useAuth();

    const messagesEndRef = useRef(null);
    const chatContainerRef = useRef(null);
    const [aiLoad, setAiLoad] = useState(false);
    const [autoScroll, setAutoScroll] = useState(true);

    useEffect(() => {
        if (chatId) {
            window.history.pushState({}, "", `?chatId=${chatId}`);
        }
    }, [chatId]);

    useEffect(() => {
        if (autoScroll) {
            scrollToBottom();
        }
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleScroll = () => {
        const chatContainer = chatContainerRef.current;
        if (chatContainer) {
            const isUserNearBottom =
                chatContainer.scrollHeight - chatContainer.scrollTop <=
                chatContainer.clientHeight + 50;
            setAutoScroll(isUserNearBottom);
        }
    };

    const handleChatSend = async (text) => {
        setAiLoad(true);
        setAutoScroll(true);
        if (isAuthenticated) {
            await privateStreamChat({
                baseURL,
                query: text,
                chatId,
                setMessages,
                setAiLoad,
            });
        } else {
            toast.info("You have only 5 free messages. Please login to continue.");
            const success = await publicStreamChat({
                baseURL,
                setAiLoad,
                setMessages,
                query: text,
            });
            if (!success) {
                toast.error("Failed to send message. Please reload the page.");
            }
        }
        setAiLoad(false);
    };

    return (
        <div className="chat">
            <div
                className="chat__messages"
                ref={chatContainerRef}
                onScroll={handleScroll}
            >
                <Container className="chat__container">
                    {messages.length === 0 ? (
                        <p style={{ color: "#D3D2D2" }}>No messages yet...</p>
                    ) : (
                        messages.map((msg, index) => (
                            <div key={index} className="message-pair">
                                {msg.user && <ChatMessage msg={{ user: msg.user }} />}
                                {msg.bot && <ChatMessage msg={{ bot: msg.bot }} />}
                            </div>
                        ))
                    )}

                    {aiLoad && <TypingIndicator message="thinking" />}

                    {!autoScroll && (
                        <div className="chat__scrollToBottom">
                            <IconButton
                                sx={{
                                    backgroundColor: "#36383A",
                                    "&:hover": { backgroundColor: "#2F3135" },
                                }}
                                onClick={() => {
                                    scrollToBottom();
                                    setAutoScroll(true);
                                }}
                            >
                                <ArrowDownward color="primary" />
                            </IconButton>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </Container>
            </div>
            <div className="chat__input">
                <Container className="chat__container">
                    <ChatInput onSend={handleChatSend} />
                </Container>
            </div>
        </div>
    );
}

ChatLayout.propTypes = {
    chatId: PropTypes.string,
    messages: PropTypes.array.isRequired,
    setMessages: PropTypes.func.isRequired,
};
