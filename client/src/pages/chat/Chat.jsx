/* eslint-disable react-hooks/exhaustive-deps */
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
import { useLoading } from "../../hooks/useLoading";
import TypingIndicator from "../../components/typing/TypingIndicator";


// Chat component
export default function Chat() {

    const navigate = useNavigate();
    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);
    const { setLoading } = useLoading();

    const [files, setFiles] = useState([]);
    const [aiLoad, setAiLoad] = useState(false);
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
            setLoading(true);
            const response = await axios.get("http://localhost:5000/files");
            toast.success(response?.data?.message || "Files fetched successfully.");
            setFiles(response?.data?.files);
        } catch (error) {
            toast.error(error?.response?.data?.message || "Failed to fetch uploaded files.");
            console.error("Failed to fetch uploaded files:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event) => {
        const files = Array.from(event.target.files);
        const formData = new FormData();
        files.forEach((file) => formData.append("files", file));

        try {
            setLoading(true);
            toast.info("Sending code snapshots to AI Dev Agent for analysis, it may take a few seconds...");
            const response = await axios.post("http://localhost:5000/upload", formData);
            toast.success(response?.data?.message || "Files uploaded successfully.");
            fetchUploadedFiles();
        } catch (error) {
            console.error("File upload failed:", error);
        } finally {
            setLoading(false);
        }
        return;
    };

    const removeFile = (file) => {
        try {
            setLoading(true);
            axios.delete(`http://localhost:5000/files/${file}`);
            toast.success("File removed successfully.");
            setFiles(files.filter((f) => f !== file));
        } catch (error) {
            console.error("Failed to remove file:", error);
        } finally {
            setLoading(false);
        }
    };


    const handleSendMessage = async () => {
        if (!inputText.trim()) return;

        setInputText("");
        const updatedMessages = [...messages, { sender: "user", text: inputText }];
        setMessages(updatedMessages);

        try {
            setAiLoad(true);
            const response = await axios.post("http://localhost:5000/chat", { query: inputText });
            setMessages([...updatedMessages, { sender: "bot", text: response.data.response }]);
        } catch (error) {
            console.error("Failed to send message:", error);
            setMessages([...updatedMessages, { sender: "bot", text: "Sorry, I couldn't process that." }]);
        } finally {
            setAiLoad(false);
        }
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
                            {aiLoad && <TypingIndicator />}
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
                        disabled={aiLoad}
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