import PropTypes from 'prop-types';
import { useState, useEffect, useRef } from "react";
import { TextField, InputAdornment, IconButton } from '@mui/material';
import { Send, ArrowUpward } from '@mui/icons-material';


// Chat input component
export default function ChatInput({ onSend, isLoading }) {

    const inputRef = useRef();
    const [inputText, setInputText] = useState("");

    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.setAttribute('maxLength', '12000');
        }
    }, []);

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
            maxRows={7}
            value={inputText}
            inputRef={inputRef}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="What’s your code Q?"
            className="welcome__textarea"
            error={inputText.length > 11999}
            helperText={inputText.length > 11999 ? "Input too long, max 12000 length supported" : ""}
            slotProps={{
                input: {
                    'aria-label': 'Enter your coding question',
                    endAdornment: (
                        <InputAdornment position="end">
                            <IconButton
                                sx={{
                                    color: '#fff',
                                    padding: '6px',
                                    background: '#1976d2',
                                    '&:hover': { background: '#1565c0' },
                                    display: inputText.trim() || isLoading ? 'flex' : 'none',
                                }}
                                disabled={!inputText.trim() || isLoading}
                                onClick={handleSend}
                                size="small"
                            >
                                <ArrowUpward size="small" />
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
    isLoading: PropTypes.bool,
    onSend: PropTypes.func.isRequired,
};
