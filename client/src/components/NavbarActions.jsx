import { toast } from 'react-toastify';
import { useEffect, useRef, useState } from 'react';
import { Button, IconButton, Typography } from '@mui/material';
import { ExpandMore, ExpandLess, AutoDelete, Delete } from '@mui/icons-material';

import Login from './auth/Login';
import LogoutPop from './LogoutPop';
import ConfirmPop from './ConfirmPop';
import { useAuth } from '../hooks/useAuth';
import { useLoading } from '../hooks/useLoading';


// Navbar actions component
export default function NavbarActions({ chatId, history, setChatId, setHistory, setMessages, handleOpen }) {

    const navbarAction = useRef(null);
    const { setLoading } = useLoading();
    const { isAuthenticated, http, logout } = useAuth();

    const [open, setOpen] = useState(false);
    const [expanded, setExpanded] = useState(false);
    const [openLogin, setOpenLogin] = useState(false);
    const [openLogout, setOpenLogout] = useState(false);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navbarAction.current && !navbarAction.current.contains(event.target)) {
                setExpanded(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleLogout = async (e) => {
        if (e) {
            setOpenLogout(false);
            await logout();
        }
        setOpenLogout(false);
    };

    const handleClearHistory = async () => {
        setOpen(false);
        try {
            setLoading(true);
            await http.delete('/history');
            toast.success('Chat history cleared successfully');
            setHistory([]);
            setMessages([]);
            setChatId(null);
            window.history.replaceState({}, '', window.location.pathname);
        } catch (error) {
            console.error(error);
            toast.error(error?.response?.data?.error || 'Failed to clear chat history');
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            setLoading(true);
            await http.delete(`/history/${id}`);
            toast.success('Chat history deleted successfully');
            setHistory((prevHistory) => prevHistory.filter((item) => item.id !== id));
            if (id === chatId) {
                setChatId(null);
                window.history.replaceState({}, '', window.location.pathname);
            }
        } catch (error) {
            console.error(error);
            toast.error(error?.response?.data?.error || 'Failed to delete chat history');
        } finally {
            setLoading(false);
        }
    };

    const handleOpenChat = (id) => {
        setExpanded(false);
        handleOpen(id);
    }

    const handleOpenNewChat = () => {
        setExpanded(false);
        handleOpen(null);
    }

    return (
        <div className="navbar__actions" ref={navbarAction}>

            {openLogin && <Login open={openLogin} setOpen={setOpenLogin} />}
            {openLogout && <LogoutPop open={openLogout} handleLogout={(e) => handleLogout(e)} />}
            {open && <ConfirmPop open={open} setOpen={setOpen} confirmAction={handleClearHistory} />}

            <Button variant="outlined" onClick={() => setExpanded(!expanded)}>
                History {expanded ? <ExpandLess color="primary" /> : <ExpandMore color="primary" />}
            </Button>
            {isAuthenticated ? (
                <Button variant="contained" color="error" onClick={() => setOpenLogout(true)}>
                    Logout
                </Button>
            ) : (
                <Button variant="contained" onClick={() => setOpenLogin(true)}>
                    Login
                </Button>
            )}
            {expanded && (
                <div className="navbar__content">
                    {isAuthenticated ? (
                        <>
                            <Button
                                sx={{ mb: 1 }}
                                fullWidth
                                size="small"
                                color="error"
                                variant="contained"
                                endIcon={<AutoDelete />}
                                onClick={() => setOpen(true)}
                            >
                                Clear Chat History
                            </Button>
                            <Button fullWidth size="small" variant='contained' onClick={handleOpenNewChat}>
                                Start New Chat
                            </Button>
                            <ul>
                                {history?.length > 0 ? (
                                    history.map((item, index) => (
                                        <li key={item.id || index} onClick={() => handleOpenChat(item.id)}>
                                            <span className="chat-name">{item.name}</span>
                                            <IconButton
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleDelete(item.id);
                                                }}
                                                aria-label="Delete chat"
                                            >
                                                <Delete color="error" fontSize="small" />
                                            </IconButton>
                                        </li>
                                    ))
                                ) : (
                                    <li className="no-history">
                                        <Typography variant="substitle1">
                                            No chat history available
                                        </Typography>
                                    </li>
                                )}
                            </ul>
                        </>
                    ) : (
                        <div
                            style={{
                                padding: '20px',
                                borderRadius: '4px',
                                textAlign: 'center',
                                border: '1px dashed #ccc',
                            }}
                        >
                            <Typography variant="body1" gutterBottom>
                                Please login to save and manage your chat history
                            </Typography>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={() => setOpenLogin(true)}
                                sx={{ mt: 1 }}
                            >
                                Login to Continue
                            </Button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}