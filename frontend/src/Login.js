// Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Change useHistory to useNavigate
import axios from 'axios';  // Make sure to import axios

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorData, setErrorData] = useState(null); // Add state for error messages
    const navigate = useNavigate(); // Use useNavigate instead of useHistory

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('/api/login', {
                email,
                password,
            });

            // Handle success (e.g., redirect to dashboard)
            console.log('Login successful:', response.data);
            navigate('/dashboard'); // Use navigate instead of history.push
        } catch (error) {
            if (error.response) {
                console.error('Login failed:', error.response.data);
                setErrorData(`Login failed: ${error.response.data.message || 'Invalid credentials.'}`); // Set error message in state
            } else {
                console.error('Error:', error.message);
                setErrorData('Login failed: An unexpected error occurred.'); // Generic error message
            }
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Login</h1>
            {errorData && <p style={{ color: 'red' }}>{errorData}</p>} {/* Display error message */}
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button className="btn" type="submit">Login</button>
        </form>
    );
};

export default Login;
