import Box from '@mui/material/Box';
import { Typography, CircularProgress } from '@mui/material';
import { useEffect, useState } from 'react';

import { useLoading } from '../hooks/useLoading';

// Loading spinner
export default function Loading() {
    const { loading } = useLoading();
    const [message, setMessage] = useState('Loading...');

    useEffect(() => {
        let timer;
        if (loading) {
            timer = setTimeout(() => {
                setMessage("Please wait, it's taking longer than usual.");
            }, 5000);
        }
        return () => {
            clearTimeout(timer);
            setMessage('Loading...');
        };
    }, [loading]);

    if (!loading) {
        return null;
    }

    return (
        <Box sx={{
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 9999,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            flexDirection: 'column',
            justifyContent: 'center',
            backdropFilter: 'blur(1px)',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
        }}>
            <CircularProgress color="primary" size="3rem" />
            <Typography variant="h6" color="primary" fontWeight={600} sx={{ mt: 2 }}>
                {message}
            </Typography>
        </Box>
    );
}
