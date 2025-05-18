
const ChatMessageUser = ({ msg }) => {
    return (
        <div className='chat-message-wrapper-user'>
            <pre>
                {msg?.user}
            </pre>
        </div>
    )
}

export default ChatMessageUser;
