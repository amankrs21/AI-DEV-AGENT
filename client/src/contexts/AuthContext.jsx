/* eslint-disable react-hooks/exhaustive-deps */
import { createContext, useState, useEffect, useMemo } from 'react';
import { Typography, CircularProgress } from '@mui/material';
import PropTypes from 'prop-types';
import axios from 'axios';


// AuthContext provides authentication state and methods
const AuthContext = createContext({
    http: null,
    userData: null,
    isAuthLoading: true,
    isAuthenticated: false,
    logout: () => Promise.resolve(),
    refreshAuth: () => Promise.resolve(),
    baseURL: '',
});
export { AuthContext };


// AuthProvider component wraps the application and provides authentication context
export const AuthProvider = ({ children }) => {
    const [userData, setUserData] = useState(null);
    const [isAuthLoading, setIsAuthLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // const baseUrl = 'http://192.168.1.39:5000/api';
    const baseUrl = window.location.origin + '/api';

    const http = useMemo(() => {
        const instance = axios.create({
            baseURL: baseUrl,
            withCredentials: true,
        });

        instance.interceptors.response.use(
            (response) => response,
            (error) => {
                if (!error.response && error.message === 'Network Error') {
                    console.warn('Network error, possibly CORS issue');
                    // logout();
                } else if (error.response?.status === 401) {
                    // Don’t auto-logout on every 401; let specific logic handle it
                    console.warn('401 received, checking context');
                }
                return Promise.reject(error);
            }
        );
        return instance;
    }, []);

    const refreshAuth = async () => {
        try {
            const response = await http.get('/validate');
            setUserData(response.data);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Validation failed:', error);
            setUserData(null);
            setIsAuthenticated(false);
        }
    };

    useEffect(() => {
        const validateSession = async () => {
            try {
                const response = await http.get('/validate');
                setUserData(response.data);
                setIsAuthenticated(true);
            } catch (error) {
                console.error('Initial session validation failed:', error);
                setUserData(null);
                setIsAuthenticated(false);
            } finally {
                setIsAuthLoading(false);
            }
        };

        validateSession();
    }, [http]);

    const logout = async () => {
        try {
            await http.post('/logout');
            setUserData(null);
            setIsAuthenticated(false);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    const value = useMemo(
        () => ({
            http,
            userData,
            isAuthLoading,
            isAuthenticated,
            logout,
            refreshAuth,
            baseURL: baseUrl,
        }),
        [userData, isAuthLoading, isAuthenticated, http]
    );

    return (
        <AuthContext.Provider value={value}>
            {!isAuthLoading ? (
                children
            ) : (
                <div className='auth__loading'>
                    <CircularProgress color="primary" size="3rem" />
                    <Typography variant="h6" color="primary" fontWeight={600} sx={{ mt: 2 }}>
                        Please wait, validating your session...
                    </Typography>
                </div>
            )}
        </AuthContext.Provider>
    );
};

AuthProvider.propTypes = {
    children: PropTypes.node.isRequired,
};
