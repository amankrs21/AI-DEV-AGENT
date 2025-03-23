import { createContext, useMemo } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

// AuthContext
const AuthContext = createContext({
    http: null,
    baseURL: '',
});
export { AuthContext };

// AuthProvider component
export const AuthProvider = ({ children }) => {
    const baseURL = 'http://localhost:5000/api';

    // Fix: Properly create and return the axios instance
    const http = useMemo(() => {
        return axios.create({
            baseURL: baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }, [baseURL]); // Add baseURL as dependency

    const value = useMemo(() => ({
        http,
        baseURL,
    }), [http, baseURL]); // Add baseURL as dependency

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired
};