import { useState } from 'react';
import Box from '@mui/material/Box';
import {
    Avatar, Dialog, DialogContent, Button, TextField, InputAdornment, IconButton, Typography
} from "@mui/material";
import { AppRegistration, Visibility, VisibilityOff, HowToReg } from '@mui/icons-material';


// Register component
export default function Register({ open, handleSubmit }) {

    const [showPass, setShowPass] = useState(false);

    return (
        <Dialog
            open={open}
            keepMounted
            maxWidth="xs"
            onClose={handleSubmit}
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
                    <AppRegistration sx={{ color: '#D3D2D2' }} />
                </Avatar>
                <Typography component="h1" variant="h5" sx={{ color: '#D3D2D2' }}>
                    Sign up
                </Typography>

                <Box required component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
                    <TextField
                        required
                        fullWidth
                        name="email"
                        className='login__input'
                        placeholder="Enter your Name*"
                        sx={{ my: 3 }}
                    />
                    <TextField
                        required
                        fullWidth
                        name="email"
                        type="email"
                        className='login__input'
                        placeholder="Enter your Email*"
                        sx={{ mb: 3 }}
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
                        Sign Up &nbsp; <HowToReg />
                    </Button>
                    <Button
                        fullWidth
                        variant="text"
                        onClick={handleSubmit}
                        sx={{ color: '#D3D2D2', '&:hover': { color: '#fff' } }}
                    >
                        Already have an account? Sign in
                    </Button>
                </Box>
            </DialogContent>
        </Dialog>
    );
}
