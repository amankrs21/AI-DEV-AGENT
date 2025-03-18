import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Typography, Button, Box, Paper } from "@mui/material";
import { CloudUpload, FolderOpen, InsertDriveFile } from "@mui/icons-material";


// Home page component
export default function Home() {

    const navigate = useNavigate();
    const [selectedOption, setSelectedOption] = useState(null);

    const handleOptionSelect = (option) => {
        setSelectedOption(option);
    };

    const handleFileSelect = (event) => {
        const files = Array.from(event.target.files);
        navigate("/chat", { state: { files } });
    };

    return (
        <Container maxWidth="md" sx={{ textAlign: "center", mt: 5 }}>

            <Typography variant="h3" gutterBottom>
                Welcome to AI Dev Agent
            </Typography>

            <Typography variant="body1" sx={{ mb: 3 }}>
                AI Dev Agent is your AI-powered coding assistant. It helps analyze code, debug issues,
                and suggest improvements effortlessly. Select specific files to analyze, and let AI assist
                you in solving problems faster and smarter.
            </Typography>

            <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
                <Typography variant="h5" gutterBottom>
                    Choose Your Analysis Type
                </Typography>

                <Box sx={{ display: "flex", justifyContent: "center", gap: 3, mt: 2 }}>
                    <Button
                        variant={selectedOption === "project" ? "contained" : "outlined"}
                        startIcon={<FolderOpen />}
                        onClick={() => handleOptionSelect("project")}
                        sx={{ width: "200px", p: 2 }}
                        disabled
                    >
                        Full Project
                    </Button>

                    <Button
                        variant={selectedOption === "files" ? "contained" : "outlined"}
                        startIcon={<InsertDriveFile />}
                        onClick={() => handleOptionSelect("files")}
                        sx={{ width: "200px", p: 2 }}
                    >
                        Specific Files
                    </Button>
                </Box>

                {selectedOption === "files" && (
                    <Box sx={{ mt: 3 }}>
                        <input
                            type="file"
                            multiple
                            onChange={handleFileSelect}
                            style={{ display: "none" }}
                            id="file-input"
                        />
                        <label htmlFor="file-input">
                            <Button
                                variant="contained"
                                component="span"
                                startIcon={<CloudUpload />}
                                sx={{ width: "200px", p: 2 }}
                            >
                                Select Files
                            </Button>
                        </label>
                    </Box>
                )}

            </Paper>
        </Container>
    );
}
