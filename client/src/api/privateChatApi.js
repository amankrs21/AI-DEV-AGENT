// Private Chat API
export const privateStreamChat = async ({
    query,
    baseURL,
    setMessages,
    chatId = null,
    setChatId = null,
    setAiLoad = null,
    credentials = "include",
}) => {
    try {
        setMessages((prevMessages) => [...prevMessages, { user: query }]);

        const response = await fetch(`${baseURL}/chat`, {
            credentials,
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, chat_id: chatId }),
        });

        if (!response.ok) throw new Error("Failed to fetch response");

        if (setAiLoad) { setAiLoad(false); }

        if (setChatId) {
            const newChatId = response.headers.get("X-Chat-ID");
            if (newChatId) setChatId(newChatId);
        }

        // Initialize streaming
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        // Add an empty bot message to start streaming into
        setMessages((prevMessages) => [...prevMessages, { bot: "" }]);

        // Stream the response
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
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

        return true;
    } catch (error) {
        console.error("Failed to stream message:", error);
        setMessages((prevMessages) => [
            ...prevMessages,
            { bot: "Sorry, I couldn’t process that." },
        ]);
        return false;
    }
};
