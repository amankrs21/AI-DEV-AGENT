import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { IconButton, Box } from "@mui/material";
import { ContentCopy } from "@mui/icons-material";
import { useState } from "react";
import { toast } from "react-toastify";

import "./Chat.css";

const Message = ({ msg }) => {
    const [copied, setCopied] = useState(false); // Track copy state for feedback

    const handleCopy = (code) => {
        navigator.clipboard.writeText(code).then(() => {
            setCopied(true);
            toast.success("Code copied to clipboard!");
            setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
        }).catch((err) => {
            toast.error("Failed to copy code!");
            console.error("Copy failed:", err);
        });
    };

    return (
        <div className="react-markdown-wrapper">
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                    code({ inline, className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || "");
                        const codeContent = String(children).replace(/\n$/, "");
                        return !inline && match ? (
                            <Box sx={{ position: "relative", display: "inline-block", width: "100%" }}>
                                <SyntaxHighlighter
                                    style={vscDarkPlus}
                                    language={match[1]}
                                    PreTag="div"
                                >
                                    {codeContent}
                                </SyntaxHighlighter>
                                <IconButton
                                    aria-label="copy code"
                                    onClick={() => handleCopy(codeContent)}
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
                            </Box>
                        ) : (
                            <code className={className} {...props}>
                                {children}
                            </code>
                        );
                    },
                }}
            >
                {msg.text}
            </ReactMarkdown>
        </div>
    );
};

export default Message;