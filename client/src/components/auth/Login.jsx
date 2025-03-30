import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import { useState } from 'react';
import { toast } from 'react-toastify';
import {
    Avatar, Dialog, DialogContent, Button, TextField, InputAdornment, IconButton, Typography
} from '@mui/material';
import { LockOutlined, Visibility, VisibilityOff, Login as LoginIcon } from '@mui/icons-material';

import Register from './Register';
import { useAuth } from '../../hooks/useAuth';
import { useLoading } from '../../hooks/useLoading';


// Login component
export default function Login({ open, setOpen }) {
    const { http, refreshAuth } = useAuth();
    const { setLoading } = useLoading();
    const [openReg, setOpenReg] = useState(false);
    const [showPass, setShowPass] = useState(false);

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpenRegister = () => {
        setOpenReg(true);
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            setLoading(true);
            await http.post('/login', {
                email: e?.target?.email?.value,
                password: e?.target?.password?.value,
            });
            await refreshAuth();
            toast.success('Login successful!!');
            setOpen(false);
        } catch (error) {
            console.error(error);
            toast.error(error?.response?.data?.error ?? 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            setLoading(true);
            await http.post('/register', {
                name: e.target.name.value,
                email: e.target.email.value,
                password: e.target.password.value,
            });
            toast.success('Registration successful!!');
            setOpenReg(false);
        } catch (error) {
            console.error(error);
            toast.error(error?.response?.data?.error ?? 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog
            open={open}
            keepMounted
            maxWidth="xs"
            onClose={handleClose}
            sx={{
                '& .MuiDialog-paper': { color: '#D3D2D2', borderRadius: '8px', backgroundColor: '#1d1e20' },
            }}
        >
            <DialogContent
                sx={{
                    margin: 2,
                    display: 'flex',
                    alignItems: 'center',
                    flexDirection: 'column',
                    backgroundColor: 'inherit',
                }}
            >
                <Avatar sx={{ bgcolor: '#36383A' }}>
                    <LockOutlined sx={{ color: '#D3D2D2' }} />
                </Avatar>
                <Typography component="h1" variant="h5" sx={{ color: '#D3D2D2' }}>
                    Sign in
                </Typography>

                <Box required component="form" onSubmit={handleLogin} sx={{ width: '100%' }}>
                    <TextField
                        required
                        fullWidth
                        name="email"
                        type="email"
                        className="login__input"
                        placeholder="Enter your Email*"
                        sx={{ my: 3 }}
                    />
                    <TextField
                        required
                        fullWidth
                        name="password"
                        className="login__input"
                        placeholder="Enter your password*"
                        type={showPass ? 'text' : 'password'}
                        slotProps={{
                            input: {
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton
                                            edge="end"
                                            sx={{ color: '#D3D2D2' }}
                                            onClick={() => setShowPass(!showPass)}
                                        >
                                            {showPass ? <Visibility /> : <VisibilityOff />}
                                        </IconButton>
                                    </InputAdornment>
                                ),
                            },
                        }}
                    />
                    <Button
                        fullWidth
                        type="submit"
                        variant="contained"
                        endIcon={<LoginIcon />}
                        sx={{ mt: 4, mb: 3 }}
                    >
                        Sign In
                    </Button>
                    <Button
                        fullWidth
                        variant="text"
                        onClick={handleOpenRegister}
                        sx={{ color: '#D3D2D2', '&:hover': { color: '#fff' } }}
                    >
                        Don’t have an account? Sign Up
                    </Button>
                </Box>
            </DialogContent>
            {openReg && <Register open={openReg} setOpen={setOpenReg} handleSubmit={handleRegister} />}
        </Dialog>
    );
}

Login.propTypes = {
    open: PropTypes.bool.isRequired,
    setOpen: PropTypes.func.isRequired,
};
