import axios from "axios";
import { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import {
    Container, Typography, List, ListItem, ListItemText, Button, Collapse, IconButton,
    TextField, Card, InputAdornment,
} from "@mui/material";
import { ExpandMore, ExpandLess, Delete, CloudUpload, Send } from "@mui/icons-material";
import './Chat.css';

export default function ChatCopy1() {

    const location = useLocation();
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const [inputText, setInputText] = useState("");
    const [isExpanded, setIsExpanded] = useState(false);
    const [files, setFiles] = useState(location.state?.files || []);
    const [messages, setMessages] = useState([
        { sender: "bot", text: "Hi there! What feature or bug issue would you like to work on today?" }
    ]);

    useEffect(() => {
        if (files.length > 0) {
            uploadFilesToBackend(files);
        }
    }, [files]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const uploadFilesToBackend = async (files) => {
        const formData = new FormData();
        files.forEach((file) => formData.append("files", file));
        try {
            await axios.post("http://localhost:5000/upload-files", formData);
            console.log("Files uploaded successfully.");
        } catch (error) {
            console.error("File upload failed:", error);
        }
    };

    const removeFile = (index) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    const handleSendMessage = () => {
        if (!inputText.trim()) return;
        setMessages([...messages, { sender: "user", text: inputText }]);
        setInputText("");
        setTimeout(() => {
            setMessages((prev) => [
                ...prev,
                { sender: "bot", text: "Got it! I'll analyze that and get back to you." }
            ]);
        }, 1000);
    };

    const handleFileUpload = (event) => {
        setFiles([...files, ...event.target.files]);
    };

    const handleEnterPress = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="main-container">

            <div className="app-bar">
                <Typography variant="h6" align="center">DEV AGENT</Typography>
                <div style={{ zIndex: 1000 }}>
                    <Typography
                        variant="h6"
                        sx={{ display: "flex", alignItems: "center", cursor: "pointer" }}
                        onClick={() => setIsExpanded(!isExpanded)}
                    >
                        {files.length} file{files.length !== 1 ? "s" : ""} referenced
                        <IconButton>{isExpanded ? <ExpandLess /> : <ExpandMore />}</IconButton>
                    </Typography>
                </div>
            </div>

            <Collapse in={isExpanded} className="chat-reference-body">
                <List dense style={{ padding: 0, margin: 0 }}>
                    {files.map((file, index) => (
                        <ListItem key={index} style={{ padding: "0px 10px" }}>
                            <ListItemText primary={file.name} />
                            <IconButton onClick={() => removeFile(index)}>
                                <Delete color="error" />
                            </IconButton>
                        </ListItem>
                    ))}
                </List>
                <Button
                    fullWidth
                    variant="contained"
                    startIcon={<CloudUpload />}
                    onClick={() => fileInputRef.current.click()}
                >
                    Add More Files
                </Button>
                <input
                    type="file"
                    ref={fileInputRef}
                    hidden
                    multiple
                    onChange={handleFileUpload}
                />
            </Collapse>

            <div className="chat-content">
                <Container maxWidth="md">
                    <Card raised className="chat-card">
                        <div className="chat-messages">
                            {messages.map((msg, index) => (
                                <Typography
                                    key={index}
                                    sx={{
                                        mt: 1,
                                        p: 1.5,
                                        borderRadius: 2,
                                        color: msg.sender === "bot" ? "black" : "white",
                                        bgcolor: msg.sender === "bot" ? "#f1f1f1" : "#1976d2",
                                        alignSelf: msg.sender === "bot" ? "flex-start" : "flex-end",
                                        display: 'inline-block',
                                        maxWidth: '95%',
                                    }}
                                >
                                    {msg.text}
                                </Typography>
                            ))}
                            <div ref={messagesEndRef} />
                        </div>
                    </Card>
                </Container>
            </div>

            <div className="bottom-input">
                <Container maxWidth="md" className="input-container">
                    <TextField
                        autoFocus
                        fullWidth
                        multiline
                        maxRows={5}
                        value={inputText}
                        variant="outlined"
                        placeholder="How can I help you?"
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyDown={handleEnterPress}
                        slotProps={{
                            input: {
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton
                                            sx={{ background: '#1976d2', color: '#fff' }}
                                            disabled={!inputText.trim()}
                                            onClick={handleSendMessage}
                                        >
                                            <Send color={inputText.trim() ? 'inherit' : 'disabled'} />
                                        </IconButton>
                                    </InputAdornment>
                                ),
                            },
                        }}
                    />
                </Container>

            </div>
        </div>
    );
}