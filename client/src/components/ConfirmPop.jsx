import PropTypes from 'prop-types';
import {
    Dialog, DialogTitle, DialogContent, Button, DialogContentText, DialogActions
} from '@mui/material';


// ConfirmPop component
export default function ConfirmPop({ open, setOpen, confirmAction }) {
    return (
        <Dialog
            fullWidth
            open={open}
            maxWidth='xs'
            onClose={() => setOpen(false)}
        >
            <DialogTitle>Confirm Action</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    Are you sure you want to proceed with this action?
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button variant='outlined' color="primary" onClick={() => setOpen(false)}>
                    Cancel
                </Button>
                <Button variant='contained' color="error" onClick={confirmAction}>
                    Yes, Confirm
                </Button>
            </DialogActions>
        </Dialog>
    )
}

ConfirmPop.propTypes = {
    open: PropTypes.bool.isRequired,
    setOpen: PropTypes.func.isRequired,
    confirmAction: PropTypes.func.isRequired
};
