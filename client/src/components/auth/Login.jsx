import { useState } from 'react';
import Box from '@mui/material/Box';
import {
    Avatar, Dialog, DialogContent, Button, TextField, InputAdornment, IconButton, Typography
} from "@mui/material";
import { LockOutlined, Visibility, VisibilityOff, Login as LoginIcon } from '@mui/icons-material';

import Register from './Register';


// Login component
export default function Login({ open, setOpen }) {
    const [openReg, setOpenReg] = useState(false);
    const [showPass, setShowPass] = useState(false);

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpenRegister = () => {
        setOpenReg(true);
    };

    const handleLogin = (e) => {
        e.preventDefault();
    };

    const handleRegister = () => {
        setOpenReg(false);
        setOpen(true);
    };

    return (
        <Dialog
            open={open}
            keepMounted
            maxWidth="xs"
            onClose={handleClose}
            sx={{
                '& .MuiDialog-paper': { color: '#D3D2D2', borderRadius: '8px', backgroundColor: '#1d1e20' }
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
                        className='login__input'
                        placeholder="Enter your Email*"
                        sx={{ my: 3 }}
                    />
                    <TextField
                        required
                        fullWidth
                        name="password"
                        className='login__input'
                        placeholder="Enter your password*"
                        type={showPass ? "text" : "password"}
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
                        sx={{ mt: 4, mb: 3 }}
                    >
                        Sign In &nbsp; <LoginIcon />
                    </Button>
                    <Button
                        fullWidth
                        variant="text"
                        onClick={handleOpenRegister}
                        sx={{ color: '#D3D2D2', '&:hover': { color: '#fff' } }}
                    >
                        Don't have an account? Sign Up
                    </Button>
                </Box>
            </DialogContent>
            {openReg && <Register open={openReg} handleSubmit={handleRegister} />}
        </Dialog>
    );
}