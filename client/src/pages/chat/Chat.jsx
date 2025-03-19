import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import {
    Container, Typography, List, ListItem, ListItemText, Button, Collapse, IconButton,
    TextField, Card, InputAdornment,
} from "@mui/material";
import { ExpandMore, ExpandLess, Delete, CloudUpload, Send } from "@mui/icons-material";

import './Chat.css';
import Message from "./Message";


// Chat component
export default function Chat() {

    const navigate = useNavigate();
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    const [files, setFiles] = useState([]);
    const [inputText, setInputText] = useState("");
    const [isExpanded, setIsExpanded] = useState(false);
    const [messages, setMessages] = useState([
        { sender: "bot", text: "Hi there! What feature or bug issue would you like to work on today?" }
    ]);

    useEffect(() => {
        const isFileUploaded = localStorage.getItem("isFileUploaded");
        if (!isFileUploaded) {
            toast.error("Please upload files to analyze.");
            navigate("/home");
        } else {
            fetchUploadedFiles();
        }
    }, [navigate]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const fetchUploadedFiles = async () => {
        try {
            const response = await axios.get("http://localhost:5000/uploaded-files");
            setFiles(response.data);
        } catch (error) {
            console.error("Failed to fetch uploaded files:", error);
        }
    };

    const handleFileUpload = async (event) => {
        const files = Array.from(event.target.files);
        const formData = new FormData();
        files.forEach((file) => formData.append("files", file));

        try {
            const response = await axios.post("http://localhost:5000/upload-files", formData);
            toast.success(response?.data?.message || "Files uploaded successfully.");
            fetchUploadedFiles();
        } catch (error) {
            console.error("File upload failed:", error);
        }
        return;
    };

    const removeFile = (file) => {
        try {
            axios.delete(`http://localhost:5000/remove-file/${file}`);
            toast.success("File removed successfully.");
            setFiles(files.filter((f) => f !== file));
        } catch (error) {
            console.error("Failed to remove file:", error);
        }
    };


    const handleSendMessage = async () => {
        if (!inputText.trim()) return;

        const updatedMessages = [...messages, { sender: "user", text: inputText }];
        setMessages(updatedMessages);

        try {
            const response = await axios.post("http://localhost:5000/chat-mistral", { query: inputText });

            setMessages([...updatedMessages, { sender: "bot", text: response.data.response }]);
        } catch (error) {
            console.error("Failed to send message:", error);
            setMessages([...updatedMessages, { sender: "bot", text: "Sorry, I couldn't process that." }]);
        }

        setInputText("");
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
                            <ListItemText primary={file} />
                            <IconButton onClick={() => removeFile(file)}>
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
                    hidden
                    multiple
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                />
            </Collapse>

            <div className="chat-content">
                <Container maxWidth="md">
                    <Card raised className="chat-card">
                        <div className="chat-messages">
                            {messages.map((msg, index) => (
                                <div
                                    key={index}
                                    style={{
                                        marginTop: "8px",
                                        padding: "12px",
                                        borderRadius: "8px",
                                        backgroundColor: msg.sender === "bot" ? "#fff" : "#D3D3D3",
                                        color: msg.sender === "bot" ? "black" : "white",
                                        alignSelf: msg.sender === "bot" ? "flex-start" : "flex-end",
                                        display: "inline-block",
                                        maxWidth: "95%",
                                    }}
                                >
                                    <Message key={index} msg={msg} />
                                </div>
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