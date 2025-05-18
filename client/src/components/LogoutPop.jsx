import PropTypes from 'prop-types';
import {
    Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle
} from '@mui/material';


// Logout confirmation dialog
export default function LogoutPop({ open, handleLogout }) {

    return (
        <Dialog
            fullWidth
            open={open}
            maxWidth='xs'
            onClose={() => handleLogout(false)}
            sx={{
                '& .MuiDialog-paper': { color: '#D3D2D2', borderRadius: '8px', backgroundColor: '#1d1e20' },
            }}
        >
            <DialogTitle>
                {"Confirm Logout?"}
            </DialogTitle>
            <DialogContent>
                <DialogContentText sx={{ color: '#D3D2D2' }}>
                    Are you sure you want to logout?
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button variant='outlined' onClick={() => handleLogout(false)}>No</Button>
                <Button variant='contained' color="error" onClick={() => handleLogout(true)}>
                    Yes, Logout
                </Button>
            </DialogActions>
        </Dialog>
    )
};

LogoutPop.propTypes = {
    open: PropTypes.bool.isRequired,
    handleLogout: PropTypes.func.isRequired
};
