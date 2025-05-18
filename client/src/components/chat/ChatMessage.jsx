import rehypeRaw from "rehype-raw";
import ReactMarkdown from "react-markdown";
import { Highlight, themes } from "prism-react-renderer";
import { useState } from "react";
import { toast } from "react-toastify";
import { IconButton } from "@mui/material";
import { ContentCopy } from "@mui/icons-material";


// Chat message component
const ChatMessage = ({ msg }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = (code) => {
        navigator.clipboard.writeText(code).then(() => {
            setCopied(true);
            toast.success("Code copied to clipboard!");
            setTimeout(() => setCopied(false), 2000);
        }).catch((err) => {
            toast.error("Failed to copy code!");
            console.error("Copy failed:", err);
        });
    };

    const messageText = msg.bot || msg.user || "No message content";
    const sender = msg.bot ? "bot" : msg.user ? "user" : "unknown";

    return (
        <div className={`chat-message-wrapper ${sender}`}>
            <ReactMarkdown
                children={messageText}
                rehypePlugins={[rehypeRaw]}
                components={{
                    h1: ({ children }) => <h1 className="markdown-heading">{children}</h1>,
                    h2: ({ children }) => <h2 className="markdown-heading">{children}</h2>,
                    h3: ({ children }) => <h3 className="markdown-heading">{children}</h3>,
                    h4: ({ children }) => <h4 className="markdown-heading">{children}</h4>,
                    ol: ({ children }) => <ol className="markdown-list">{children}</ol>,
                    ul: ({ children }) => <ul className="markdown-list">{children}</ul>,
                    li: ({ children }) => <li className="markdown-list-item">{children}</li>,
                    code({ inline, className, children, ...props }) {
                        const codeContent = String(children).replace(/\n$/, "");
                        const match = /language-(\w+)/.exec(className || "");
                        if (!inline && match) {
                            return (
                                <div className="code-block-wrapper">
                                    <Highlight
                                        theme={themes.vsDark}
                                        code={codeContent}
                                        language={match[1]}
                                    >
                                        {({ className, style, tokens, getLineProps, getTokenProps }) => (
                                            <pre
                                                className={className}
                                                style={{
                                                    ...style,
                                                    margin: 0,
                                                    padding: "12px",
                                                    fontSize: "13px",
                                                    borderRadius: "5px",
                                                    background: "#121314",
                                                }}
                                            >
                                                {tokens.map((line, i) => {
                                                    const lineProps = getLineProps({ line, key: i });
                                                    const { key: lineKey, ...restLineProps } = lineProps;
                                                    return (
                                                        <div key={lineKey} {...restLineProps}>
                                                            {line.map((token, key) => {
                                                                const tokenProps = getTokenProps({ token, key });
                                                                const { key: tokenKey, ...restTokenProps } = tokenProps;
                                                                return <span key={tokenKey} {...restTokenProps} />;
                                                            })}
                                                        </div>
                                                    );
                                                })}
                                            </pre>
                                        )}
                                    </Highlight>
                                    <IconButton
                                        aria-label="copy code"
                                        onClick={() => handleCopy(codeContent)}
                                        className="copy-button"
                                        sx={{
                                            position: "absolute",
                                            top: 8,
                                            right: 8,
                                            color: "white",
                                            backgroundColor: "rgba(0, 0, 0, 0.6)",
                                            "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.8)" },
                                            opacity: copied ? 1 : 0.7,
                                            transition: "opacity 0.3s",
                                        }}
                                    >
                                        <ContentCopy fontSize="small" />
                                    </IconButton>
                                </div>
                            );
                        }
                        return (
                            <code className={`inline-code ${className || ""}`} {...props}>
                                {codeContent}
                            </code>
                        );
                    },
                }}
            />
        </div>
    );
};

export default ChatMessage;
