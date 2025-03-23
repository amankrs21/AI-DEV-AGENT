/* eslint-disable react-hooks/exhaustive-deps */
import { toast } from "react-toastify";
import { useState, useEffect, useRef } from "react";
import { Button, IconButton } from "@mui/material";
import { ExpandMore, ExpandLess, Delete, AutoDelete, CloudUpload } from "@mui/icons-material";

import { useAuth } from "../hooks/useAuth";
import { useLoading } from "../hooks/useLoading";
import ConfirmPop from "./ConfirmPop";


// File manager component
export default function FileManager({ setMessages }) {

    const { http } = useAuth();
    const { setLoading } = useLoading();

    const fileInputRef = useRef(null);
    const fileManagerRef = useRef(null);
    const [files, setFiles] = useState([]);
    const [open, setOpen] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const toggleExpanded = () => setIsExpanded((prev) => !prev);

    useEffect(() => {
        if (files.length === 0) {
            fetchUploadedFiles();
        }
    }, []);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (fileManagerRef.current && !fileManagerRef.current.contains(event.target)) {
                setIsExpanded(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const fetchUploadedFiles = async () => {
        try {
            setLoading(true);
            const response = await http.get("/files");
            setFiles(response?.data || []);
        } catch (error) {
            toast.error(error?.response?.data?.message || "Failed to fetch uploaded files.");
            console.error("Failed to fetch uploaded files:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event) => {
        const files = event.target.files;
        if (!files || files.length === 0) {
            toast.error("No files selected");
            return;
        }
        const formData = new FormData();
        Array.from(files).forEach((file) => { formData.append("files", file); });
        try {
            setLoading(true);
            toast.info("Uploading files, please wait...");
            const response = await http.post("/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            toast.success(response?.data?.message || "Files uploaded successfully.");
            fetchUploadedFiles();
        } catch (error) {
            toast.error(error?.response?.data?.message || "File upload failed");
            console.error("File upload failed:", error);
        } finally {
            setLoading(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        }
    };

    const handleRemoveFile = async (file) => {
        try {
            setLoading(true);
            await http.delete(`/files/${file}`);
            toast.success("File removed successfully.");
            fetchUploadedFiles();
        } catch (error) {
            toast.error(error?.response?.data?.message || "Failed to remove file");
            console.error("Failed to remove file:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleClearHistory = async () => {
        try {
            setOpen(false);
            setLoading(true);
            await http.delete("/history");
            setMessages([]);
            setFiles([]);
            toast.success("Chat history cleared successfully");
        } catch (error) {
            toast.error(error?.response?.data?.message || "Failed to clear chat history");
            console.error("Failed to clear chat history:", error);
        } finally {
            setLoading(false);
        }
    }


    return (
        <div className="filemanager" ref={fileManagerRef}>
            {open && <ConfirmPop open={open} setOpen={setOpen} confirmAction={handleClearHistory} />}
            <div className="filemanager__header" onClick={toggleExpanded}>
                <h3>
                    Files Tracked: {files.length}
                    <IconButton size="small">
                        {isExpanded ? <ExpandLess color="primary" /> : <ExpandMore color="primary" />}
                    </IconButton>
                </h3>
            </div>
            {isExpanded && (
                <div className="filemanager__content">
                    <Button
                        fullWidth
                        size="small"
                        color="error"
                        variant="contained"
                        startIcon={<AutoDelete />}
                        onClick={() => setOpen(true)}
                    >
                        Clear Chat History
                    </Button>
                    <Button
                        fullWidth
                        size="small"
                        variant="outlined"
                        sx={{ my: 1 }}
                        startIcon={<CloudUpload />}
                        onClick={() => fileInputRef.current.click()}
                    >
                        Add File
                    </Button>
                    <input
                        hidden
                        multiple
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileUpload}
                    />
                    <ul>
                        {files.map((file, index) => (
                            <li key={index}>
                                {file}
                                <IconButton onClick={() => handleRemoveFile(file)}>
                                    <Delete color="error" />
                                </IconButton>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}