
// TypingIndicator component
const TypingIndicator = ({ message = "AI is thinking!" }) => (

    <div className="typing-indicator-wrapper">
        <p className="typing-text">{message}</p>
        <div className="typing-indicator-container">
            <span className="typing-indicator-dot"></span>
            <span className="typing-indicator-dot"></span>
            <span className="typing-indicator-dot"></span>
        </div>
    </div>
);

export default TypingIndicator;
