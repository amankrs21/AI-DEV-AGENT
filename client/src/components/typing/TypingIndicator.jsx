import React from "react";
import "./TypingIndicator.css";

const TypingIndicator = ({ message = "Hold on, AI is thinking! 🤖" }) => (

    <div className="typing-indicator-wrapper">
        <p className="typing-text">{message}</p>
        <div className="typing-indicator-container">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
        </div>
    </div>
);

export default TypingIndicator;
