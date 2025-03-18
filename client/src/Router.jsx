import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// import { AuthProvider } from './contexts/AuthContext';
import Home from './pages/home/Home';
import Chat from './pages/chat/Chat';
import Project from './pages/project/Project';


// Router component to render the application routes
export default function Router() {

    return (
        <BrowserRouter>
            {/* <AuthProvider> */}
            <Routes>

                <Route path='*' element={<Navigate to='/home' />} />
                <Route path="/" element={<Navigate to="/home" />} />

                <Route path='/home' element={<Home />} />
                <Route path='/chat' element={<Chat />} />
                <Route path='/project' element={<Project />} />

            </Routes>
            {/* </AuthProvider> */}
        </BrowserRouter>
    )
}
