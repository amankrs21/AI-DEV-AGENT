import PropTypes from 'prop-types';
import { useState } from "react";
import { Send } from '@mui/icons-material';
import { TextField, InputAdornment, IconButton } from '@mui/material';


// Chat input component
export default function ChatInput({ onSend }) {

    const [inputText, setInputText] = useState("");

    const handleSend = () => {
        if (inputText.trim()) {
            onSend(inputText);
            setInputText("");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <TextField
            autoFocus
            multiline
            minRows={3}
            maxRows={8}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="What’s your code Q?"
            className="welcome__textarea"
            slotProps={{
                input: {
                    'aria-label': 'Enter your coding question',
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                sx={{
                                    color: '#fff',
                                    padding: '10px',
                                    background: inputText.trim() ? '#1976d2' : '#555',
                                    '&:hover': { background: inputText.trim() ? '#1565c0' : '#666' },
                                }}
                                disabled={!inputText.trim()}
                                onClick={handleSend}
                                size="small"
                            >
                                <Send />
                            </IconButton>
                        </InputAdornment>
                    ),
                },
            }}
            sx={{ '& .MuiOutlinedInput-notchedOutline': { border: 'none' } }}
        />
    )
}

ChatInput.propTypes = {
    onSend: PropTypes.func.isRequired,
};
